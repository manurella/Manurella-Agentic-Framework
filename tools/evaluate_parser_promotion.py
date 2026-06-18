"""Aggregate parser eval records into a repeated-run promotion decision."""

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


EVAL_SCHEMA = pathlib.Path("schemas/evals/parser-eval-result.schema.json")
PROMOTION_SCHEMA = pathlib.Path("schemas/evals/parser-promotion-result.schema.json")


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def validator(path: pathlib.Path) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def errors(checker: Draft202012Validator, data: Any) -> list[str]:
    return [
        f"{'/'.join(str(part) for part in issue.absolute_path) or '<root>'}: {issue.message}"
        for issue in sorted(checker.iter_errors(data), key=lambda issue: list(issue.absolute_path))
    ]


def result_ref(root: pathlib.Path, path: pathlib.Path) -> str:
    resolved = path.resolve()
    results_root = (root / "evals" / "results").resolve()
    if results_root not in resolved.parents:
        raise ValueError(f"eval result must be stored under evals/results/: {path}")
    return resolved.relative_to(root).as_posix()


def aggregate(
    root: pathlib.Path,
    promotion_id: str,
    paths: list[pathlib.Path],
    minimum_runs: int,
) -> dict[str, Any]:
    if minimum_runs < 2:
        raise ValueError("minimum_runs must be at least 2")
    if len(paths) != len({path.resolve() for path in paths}):
        raise ValueError("eval result paths must be unique")

    eval_checker = validator(root / EVAL_SCHEMA)
    loaded: list[tuple[pathlib.Path, dict[str, Any]]] = []
    for path in paths:
        resolved = path if path.is_absolute() else root / path
        document = load_yaml(resolved)
        validation_errors = errors(eval_checker, document)
        if validation_errors:
            raise ValueError(f"invalid parser eval {resolved}: {'; '.join(validation_errors)}")
        if document.get("candidate") is None:
            raise ValueError(f"parser eval has no candidate: {resolved}")
        loaded.append((resolved, document))

    if not loaded:
        raise ValueError("provide at least one parser eval result")

    model = loaded[0][1]["candidate"]["model"]
    prompt_version = loaded[0][1]["candidate"]["prompt_version"]
    for path, document in loaded[1:]:
        candidate = document["candidate"]
        if candidate["model"] != model or candidate["prompt_version"] != prompt_version:
            raise ValueError(
                f"mixed candidate identity at {path}: expected {model!r} with {prompt_version!r}"
            )

    runs = []
    for path, document in loaded:
        summary = document["candidate"]["summary"]
        runs.append(
            {
                "run_id": document["run_id"],
                "result_ref": result_ref(root, path),
                "status": document["promotion"]["status"],
                "schema_valid_rate": summary["schema_valid_rate"],
                "semantic_valid_rate": summary["semantic_valid_rate"],
                "routing_valid_rate": summary["routing_valid_rate"],
                "critical_field_accuracy": summary["critical_field_accuracy"],
                "safety_pass_rate": summary["safety_pass_rate"],
            }
        )

    passed = sum(1 for run in runs if run["status"] == "pass")
    reasons = []
    if len(runs) < minimum_runs:
        reasons.append(f"Only {len(runs)} run(s) supplied; at least {minimum_runs} are required.")
    failed_ids = [run["run_id"] for run in runs if run["status"] != "pass"]
    if failed_ids:
        reasons.append("Required repeat runs failed: " + ", ".join(failed_ids))

    result = {
        "schema_version": "parser-promotion-result.v0",
        "promotion_id": promotion_id,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "model": model,
        "prompt_version": prompt_version,
        "minimum_runs": minimum_runs,
        "runs": runs,
        "summary": {
            "runs_total": len(runs),
            "runs_passed": passed,
            "pass_rate": passed / len(runs),
            "minimum_critical_field_accuracy": min(run["critical_field_accuracy"] for run in runs),
            "minimum_safety_pass_rate": min(run["safety_pass_rate"] for run in runs),
            "minimum_semantic_valid_rate": min(run["semantic_valid_rate"] for run in runs),
            "minimum_routing_valid_rate": min(run["routing_valid_rate"] for run in runs),
        },
        "promotion": {
            "status": "fail" if reasons else "pass",
            "reasons": reasons or ["Every required independent run passed its parser promotion gate."],
        },
    }
    promotion_errors = errors(validator(root / PROMOTION_SCHEMA), result)
    if promotion_errors:
        raise ValueError("invalid parser promotion result: " + "; ".join(promotion_errors))
    return result


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def write_result(root: pathlib.Path, result: dict[str, Any], overwrite: bool) -> pathlib.Path:
    name = slug(result["promotion_id"])
    if not name:
        raise ValueError("promotion_id must contain an alphanumeric character")
    output = root / "evals" / "results" / f"{name}.parser-promotion.yaml"
    if output.exists() and not overwrite:
        raise ValueError(f"result already exists: {output}")
    output.write_text(yaml.safe_dump(result, sort_keys=False), encoding="utf-8", newline="\n")
    return output


def self_test(root: pathlib.Path) -> None:
    first = root / "evals" / "results" / "parser-stepfun-v2.parser-eval.yaml"
    repeat = root / "evals" / "results" / "parser-stepfun-v2-repeat-1.parser-eval.yaml"
    if first.exists() and repeat.exists():
        result = aggregate(root, "parser-promotion-self-test", [first, repeat], 2)
        if result["promotion"]["status"] != "fail" or result["summary"]["runs_passed"] != 1:
            raise ValueError("self-test expected one passing and one failing repeat")
    print("parser promotion self-test passed")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--promotion-id", default="parser-promotion")
    parser.add_argument("--eval", type=pathlib.Path, action="append", default=[])
    parser.add_argument("--minimum-runs", type=int, default=2)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.self_test:
            self_test(root)
            return 0
        result = aggregate(root, args.promotion_id, args.eval, args.minimum_runs)
        output = write_result(root, result, args.overwrite)
        print(f"wrote: {output}")
        print(yaml.safe_dump({"summary": result["summary"], "promotion": result["promotion"]}, sort_keys=False).rstrip())
        return 0 if result["promotion"]["status"] == "pass" else 2
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
