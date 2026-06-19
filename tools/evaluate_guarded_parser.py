"""Replay promoted inference captures through guarded selection and record observations."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from compile_model_inference import guarded_inference_decision
from evaluate_model_inference import load_candidate, load_yaml
from evaluate_task_frame_parser import load_corpus
from parse_task_frame import error_messages


RESULT_SCHEMA = pathlib.Path("schemas/evals/guarded-parser-observation-result.schema.json")
DECISION_SCHEMA = pathlib.Path("schemas/interpreter/guarded-parser-decision.schema.json")


def validator(root: pathlib.Path, schema_path: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / schema_path).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def repo_ref(root: pathlib.Path, path: pathlib.Path) -> str:
    resolved = path if path.is_absolute() else root / path
    try:
        return resolved.resolve().relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"evidence path must be inside the repository: {resolved}") from exc


def observe(
    root: pathlib.Path,
    observation_id: str,
    candidate_paths: list[pathlib.Path],
    promotion_path: pathlib.Path,
) -> dict[str, Any]:
    corpus = {case["case_id"]: case for case in load_corpus(root)}
    promotion_ref = repo_ref(root, promotion_path)
    promotion = load_yaml(root / promotion_ref)
    decision_checker = validator(root, DECISION_SCHEMA)
    observations: list[dict[str, Any]] = []
    candidate_refs: list[str] = []
    run_ids: set[str] = set()

    for candidate_path in candidate_paths:
        candidate_ref = repo_ref(root, candidate_path)
        metadata, inferences = load_candidate(root, root / candidate_ref)
        if metadata["run_id"] in run_ids:
            raise ValueError(f"duplicate candidate run_id: {metadata['run_id']}")
        run_ids.add(metadata["run_id"])
        candidate_refs.append(candidate_ref)
        if set(inferences) != set(corpus):
            raise ValueError(f"candidate run {metadata['run_id']} must cover the complete benchmark corpus")

        for case_id in sorted(corpus):
            case = corpus[case_id]
            decision = guarded_inference_decision(
                root,
                case["envelope"],
                case.get("locale", "en-US"),
                inferences[case_id],
                metadata["model"],
                metadata["prompt_version"],
                promotion,
                promotion_ref,
            )
            issues = error_messages(decision_checker, decision)
            if issues:
                raise ValueError(f"invalid guarded decision for {metadata['run_id']}/{case_id}: {'; '.join(issues)}")
            candidate = decision["candidate"]
            observations.append(
                {
                    "run_id": metadata["run_id"],
                    "case_id": case_id,
                    "disposition": decision["disposition"],
                    "selected_parser": decision["selected_parser"],
                    "identity_match": decision["promotion"]["identity_match"],
                    "schema_valid": candidate["schema_valid"],
                    "trust_aligned": candidate["trust_aligned"],
                    "semantic_valid": candidate["semantic_valid"],
                    "routing_valid": candidate["routing_valid"],
                    "issues": candidate["issues"],
                }
            )

    counts = {
        disposition: sum(item["disposition"] == disposition for item in observations)
        for disposition in ("candidate_selected", "fallback_promotion", "fallback_validation")
    }
    total = len(observations)
    result = {
        "schema_version": "guarded-parser-observation-result.v0",
        "observation_id": observation_id,
        "evidence_class": "representative_replay",
        "promotion_ref": promotion_ref,
        "candidate_run_refs": candidate_refs,
        "observations": observations,
        "summary": {
            "runs_total": len(run_ids),
            "requests_total": total,
            **counts,
            "selection_rate": counts["candidate_selected"] / total,
        },
        "activation": {
            "status": "insufficient_live_evidence",
            "default_mode": "shadow",
            "reasons": [
                "Representative benchmark replays do not count as independently captured live requests.",
                "Human residual-risk review has not approved default activation.",
            ],
        },
    }
    issues = error_messages(validator(root, RESULT_SCHEMA), result)
    if issues:
        raise ValueError("invalid guarded observation result: " + "; ".join(issues))
    return result


def run_self_test(root: pathlib.Path) -> None:
    result = observe(
        root,
        "guarded-observation-self-test",
        [pathlib.Path("evals/results/stepfun-inference-v1.inference-candidate.yaml")],
        pathlib.Path("evals/results/stepfun-inference-v1-promotion.parser-promotion.yaml"),
    )
    summary = result["summary"]
    if summary["requests_total"] != 6 or summary["candidate_selected"] != 6:
        raise ValueError("self-test did not select all six promoted replay candidates")
    if result["activation"]["default_mode"] != "shadow":
        raise ValueError("representative replay incorrectly enabled guarded mode by default")
    print("guarded parser observation self-test passed: replay=6/6, default=shadow")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--observation-id", default="guarded-parser-observation")
    parser.add_argument("--candidate-run", type=pathlib.Path, action="append", default=[])
    parser.add_argument("--promotion", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.self_test:
            run_self_test(root)
            return 0
        if not args.candidate_run or args.promotion is None or args.output is None:
            raise ValueError("provide --candidate-run, --promotion, and --output")
        output = args.output if args.output.is_absolute() else root / args.output
        results_root = (root / "evals/results").resolve()
        if results_root not in output.resolve().parents:
            raise ValueError("guarded observation output must be stored under evals/results/")
        if output.exists() and not args.overwrite:
            raise ValueError(f"output already exists: {output}")
        result = observe(root, args.observation_id, args.candidate_run, args.promotion)
        output.write_text(yaml.safe_dump(result, sort_keys=False), encoding="utf-8", newline="\n")
        print(f"wrote: {output}")
        print(yaml.safe_dump({"summary": result["summary"], "activation": result["activation"]}, sort_keys=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
