"""Evaluate one captured parser run through the shadow adapter across the full corpus."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from evaluate_task_frame_parser import load_candidate, load_corpus
from shadow_parse_task_frame import shadow_decision


RESULT_SCHEMA = pathlib.Path("schemas/evals/shadow-parser-eval-result.schema.json")


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def relative_result_ref(root: pathlib.Path, path: pathlib.Path) -> str:
    resolved = path.resolve()
    results_root = (root / "evals/results").resolve()
    if results_root not in resolved.parents:
        raise ValueError(f"artifact must be stored under evals/results/: {path}")
    return resolved.relative_to(root).as_posix()


def validator(root: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / RESULT_SCHEMA).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_errors(checker: Draft202012Validator, data: Any) -> list[str]:
    return [
        f"{'/'.join(str(part) for part in issue.absolute_path) or '<root>'}: {issue.message}"
        for issue in sorted(checker.iter_errors(data), key=lambda issue: list(issue.absolute_path))
    ]


def build_result(
    root: pathlib.Path,
    run_id: str,
    candidate_path: pathlib.Path,
    promotion_path: pathlib.Path,
) -> dict[str, Any]:
    metadata, frames = load_candidate(root, candidate_path)
    promotion = load_yaml(promotion_path)
    if promotion.get("schema_version") != "parser-promotion-result.v0":
        raise ValueError("promotion result has unsupported schema_version")
    if promotion.get("model") != metadata["model"] or promotion.get("prompt_version") != metadata["prompt_version"]:
        raise ValueError("promotion result model and prompt must match candidate run")

    cases = []
    for fixture in load_corpus(root):
        case_id = fixture["case_id"]
        decision = shadow_decision(
            root,
            fixture["envelope"],
            fixture.get("locale", "en-US"),
            frames.get(case_id),
            metadata["model"],
            metadata["prompt_version"],
        )
        candidate = decision["candidate"]
        cases.append(
            {
                "case_id": case_id,
                "disposition": decision["disposition"],
                "would_be_eligible": candidate["would_be_eligible"],
                "schema_valid": candidate["schema_valid"],
                "trust_aligned": candidate["trust_aligned"],
                "semantic_valid": candidate["semantic_valid"],
                "routing_valid": candidate["routing_valid"],
                "issues": candidate["issues"],
            }
        )

    count = len(cases)
    eligible = sum(1 for case in cases if case["would_be_eligible"])
    promotion_status = promotion["promotion"]["status"]
    reasons = []
    if eligible != count:
        reasons.append(f"Only {eligible}/{count} shadow cases were eligible.")
    if promotion_status != "pass":
        reasons.append("The repeated-run parser promotion gate has not passed.")
    recommendation = "remain_shadow" if reasons else "eligible_for_guarded_design"
    result = {
        "schema_version": "shadow-parser-eval-result.v0",
        "run_id": run_id,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "candidate_run_ref": relative_result_ref(root, candidate_path),
        "promotion_ref": relative_result_ref(root, promotion_path),
        "runtime": metadata["runtime"],
        "model": metadata["model"],
        "prompt_version": metadata["prompt_version"],
        "cases": cases,
        "summary": {
            "cases_total": count,
            "eligible_cases": eligible,
            "eligibility_rate": eligible / count,
            "schema_valid_rate": sum(case["schema_valid"] for case in cases) / count,
            "trust_aligned_rate": sum(case["trust_aligned"] for case in cases) / count,
            "semantic_valid_rate": sum(case["semantic_valid"] for case in cases) / count,
            "routing_valid_rate": sum(case["routing_valid"] for case in cases) / count,
            "promotion_status": promotion_status,
        },
        "recommendation": {
            "status": recommendation,
            "reasons": reasons or ["Full-corpus shadow eligibility and repeated-run promotion both passed."],
        },
    }
    result_errors = schema_errors(validator(root), result)
    if result_errors:
        raise ValueError("invalid shadow parser eval result: " + "; ".join(result_errors))
    return result


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def write_result(root: pathlib.Path, result: dict[str, Any], overwrite: bool) -> pathlib.Path:
    name = slug(result["run_id"])
    if not name:
        raise ValueError("run_id must contain an alphanumeric character")
    output = root / "evals/results" / f"{name}.shadow-parser-eval.yaml"
    if output.exists() and not overwrite:
        raise ValueError(f"result already exists: {output}")
    output.write_text(yaml.safe_dump(result, sort_keys=False), encoding="utf-8", newline="\n")
    return output


def run_self_test(root: pathlib.Path) -> None:
    promotion = root / "evals/results/parser-stepfun-v2-promotion.parser-promotion.yaml"
    first = root / "evals/results/parser-stepfun-v2.parser-candidate.yaml"
    repeat = root / "evals/results/parser-stepfun-v2-repeat-1.parser-candidate.yaml"
    if not all(path.exists() for path in (promotion, first, repeat)):
        raise ValueError("self-test requires the durable StepFun v2 candidate and promotion records")
    first_result = build_result(root, "shadow-self-test-first", first, promotion)
    repeat_result = build_result(root, "shadow-self-test-repeat", repeat, promotion)
    if first_result["summary"]["eligible_cases"] != 0:
        raise ValueError("expected trust projection to reject every first-run shadow case")
    if repeat_result["summary"]["eligible_cases"] != 4:
        raise ValueError("expected four repeat-run shadow cases to be eligible")
    if first_result["recommendation"]["status"] != "remain_shadow":
        raise ValueError("failed repeated-run promotion must block guarded design")
    print("shadow parser eval self-test passed: first=0/6, repeat=4/6, recommendation=remain_shadow")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--run-id", default="shadow-parser-eval")
    parser.add_argument("--candidate-run", type=pathlib.Path)
    parser.add_argument("--promotion", type=pathlib.Path)
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
        if args.candidate_run is None or args.promotion is None:
            raise ValueError("provide --candidate-run and --promotion or select --self-test")
        candidate = args.candidate_run if args.candidate_run.is_absolute() else root / args.candidate_run
        promotion = args.promotion if args.promotion.is_absolute() else root / args.promotion
        result = build_result(root, args.run_id, candidate, promotion)
        output = write_result(root, result, args.overwrite)
        print(f"wrote: {output}")
        print(yaml.safe_dump({"summary": result["summary"], "recommendation": result["recommendation"]}, sort_keys=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
