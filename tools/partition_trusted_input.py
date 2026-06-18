"""Validate and deterministically partition Interpreter input by authority."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ENVELOPE_SCHEMA = pathlib.Path("schemas/interpreter/trusted-input-envelope.schema.json")
PARTITION_SCHEMA = pathlib.Path("schemas/interpreter/trust-partition.schema.json")
DEFAULT_FIXTURE_DIR = pathlib.Path("evals/fixtures/trust-partitioner")

POLICY_KINDS = {"system_policy", "runtime_policy"}
UNTRUSTED_KINDS = {"retrieved_content", "tool_output", "model_output", "artifact_content"}
USER_CONTROL_CLAIMS = {"goal", "autonomy", "permission", "confirmation", "constraint"}


def load_mapping(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def load_schema(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load schema {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"schema {path} must contain an object")
    Draft202012Validator.check_schema(data)
    return data


def schema_errors(data: Any, validator: Draft202012Validator) -> list[str]:
    errors = sorted(validator.iter_errors(data), key=lambda error: tuple(str(part) for part in error.path))
    return [f"schema.{'.'.join(str(part) for part in error.path) or '$'}: {error.message}" for error in errors]


def classify_item(item: dict[str, Any]) -> str:
    kind = item["kind"]
    origin = item["source"]["origin"]
    verified = item["authentication"]["status"] == "verified"
    authority = item["claimed_authority"]
    if kind in POLICY_KINDS and origin in {"system", "runtime"} and verified and authority == "policy":
        return "trusted_policy_refs"
    if kind == "user_instruction" and origin == "user" and verified and authority == "user_instruction":
        return "authenticated_user_instruction_refs"
    if kind == "prior_confirmed_state" and origin == "user" and verified and authority == "prior_state":
        return "prior_confirmed_state_refs"
    return "untrusted_data_refs"


def partition_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema_version": "trust-partition.v0",
        "envelope_ref": envelope["envelope_id"],
        "disposition": "ready",
        "execution_blocked": False,
        "trusted_policy_refs": [],
        "authenticated_user_instruction_refs": [],
        "prior_confirmed_state_refs": [],
        "untrusted_data_refs": [],
        "rejected_control_claims": [],
        "issues": [],
    }

    seen_ids: set[str] = set()
    for item in envelope["items"]:
        item_id = item["item_id"]
        if item_id in seen_ids:
            result["issues"].append({
                "code": "duplicate_item_id", "item_ref": item_id, "severity": "blocking",
                "message": "input item identifiers must be unique within an envelope",
            })
            continue
        seen_ids.add(item_id)
        partition = classify_item(item)
        result[partition].append(item_id)

        claims = set(item["control_claims"])
        allowed_claims: set[str] = set()
        if partition == "trusted_policy_refs":
            allowed_claims = USER_CONTROL_CLAIMS | {"policy"}
        elif partition == "authenticated_user_instruction_refs":
            allowed_claims = USER_CONTROL_CLAIMS
        rejected = sorted(claims - allowed_claims)
        if rejected:
            result["rejected_control_claims"].append({
                "item_ref": item_id,
                "claims": rejected,
                "reason": "the derived trust partition does not authorize these control claims",
            })
            result["issues"].append({
                "code": "unauthorized_control_claim", "item_ref": item_id, "severity": "warning",
                "message": "control-plane claims were quarantined as untrusted data",
            })

        if item["kind"] in UNTRUSTED_KINDS and item["claimed_authority"] != "data":
            result["issues"].append({
                "code": "untrusted_authority_claim", "item_ref": item_id, "severity": "warning",
                "message": "retrieved, tool, model, and artifact content cannot acquire instruction authority",
            })

    if envelope["purpose"] == "task_intake" and not result["authenticated_user_instruction_refs"]:
        result["issues"].append({
            "code": "missing_authenticated_user_instruction", "item_ref": None, "severity": "blocking",
            "message": "task intake requires at least one authenticated user instruction",
        })

    result["execution_blocked"] = any(issue["severity"] == "blocking" for issue in result["issues"])
    if result["execution_blocked"]:
        result["disposition"] = "blocked"
    elif result["rejected_control_claims"] or result["issues"]:
        result["disposition"] = "quarantined"
    return result


def validators(root: pathlib.Path) -> tuple[Draft202012Validator, Draft202012Validator]:
    checker = FormatChecker()
    return (
        Draft202012Validator(load_schema(root / ENVELOPE_SCHEMA), format_checker=checker),
        Draft202012Validator(load_schema(root / PARTITION_SCHEMA), format_checker=checker),
    )


def validate_and_partition(
    envelope: dict[str, Any], envelope_validator: Draft202012Validator, partition_validator: Draft202012Validator
) -> tuple[dict[str, Any] | None, list[str]]:
    errors = schema_errors(envelope, envelope_validator)
    if errors:
        return None, errors
    partition = partition_envelope(envelope)
    return partition, schema_errors(partition, partition_validator)


def run_fixtures(root: pathlib.Path, fixture_dir: pathlib.Path) -> int:
    envelope_validator, partition_validator = validators(root)
    paths = sorted([*fixture_dir.rglob("*.yaml"), *fixture_dir.rglob("*.yml")])
    if not paths:
        print(f"error: no trust partition fixtures under {fixture_dir}", file=sys.stderr)
        return 1
    failures = 0
    for path in paths:
        try:
            fixture = load_mapping(path)
            partition, errors = validate_and_partition(
                fixture.get("envelope"), envelope_validator, partition_validator
            )
        except (TypeError, ValueError) as exc:
            partition, errors = None, [str(exc)]
        expected_schema = fixture.get("expected_schema", "pass")
        expected = fixture.get("expected_partition")
        actual_schema = "fail" if errors else "pass"
        mismatch = actual_schema != expected_schema or (not errors and expected is not None and partition != expected)
        if mismatch:
            failures += 1
            print(f"FAIL {path.as_posix()}: schema={actual_schema}", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
            if partition is not None and expected is not None and partition != expected:
                print(f"  expected: {json.dumps(expected, sort_keys=True)}", file=sys.stderr)
                print(f"  actual:   {json.dumps(partition, sort_keys=True)}", file=sys.stderr)
        else:
            disposition = partition["disposition"] if partition else "schema-rejected"
            print(f"PASS {path.as_posix()}: schema={actual_schema}, disposition={disposition}")
    if failures:
        print(f"Trust partition fixture validation failed: {failures}/{len(paths)} case(s)")
        return 1
    print(f"Trust partition fixture validation passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--input", type=pathlib.Path)
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures or not args.input:
            return run_fixtures(root, root / DEFAULT_FIXTURE_DIR)
        envelope_validator, partition_validator = validators(root)
        envelope = load_mapping(args.input if args.input.is_absolute() else root / args.input)
        partition, errors = validate_and_partition(envelope, envelope_validator, partition_validator)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors or partition is None:
        return 1
    print(yaml.safe_dump(partition, sort_keys=False).rstrip())
    return 2 if partition["execution_blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
