"""Evaluate memory proposals against provenance, conflicts, permissions, and evidence gates."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


SCHEMA_DIR = pathlib.Path("schemas/memory")
PROPOSAL_SCHEMA = SCHEMA_DIR / "memory-proposal.schema.json"
STORE_SCHEMA = SCHEMA_DIR / "memory-store.schema.json"
DECISION_SCHEMA = SCHEMA_DIR / "memory-promotion-decision.schema.json"
DEFAULT_STORE = pathlib.Path("cognition/memory.yaml")
FIXTURE_DIR = pathlib.Path("evals/fixtures/memory-promotion")
TRUSTED = {"authenticated_user", "trusted_runtime", "validated_eval", "reviewed_research"}
BENCHMARK_GATED = {"procedural", "failure_lesson", "atlas_mutation"}
TARGET_STORE = {
    "episodic": "episodic",
    "semantic": "semantic",
    "procedural": "procedural",
    "project_state": "project",
    "user_preference": "semantic",
    "failure_lesson": "procedural",
    "atlas_mutation": "atlas",
}


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def registry(root: pathlib.Path) -> Registry:
    result = Registry()
    for path in sorted((root / SCHEMA_DIR).glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        resource = Resource.from_contents(schema)
        result = result.with_resource(schema["$id"], resource)
        result = result.with_resource(path.name, resource)
    return result


def checker(root: pathlib.Path, schema_path: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / schema_path).read_text(encoding="utf-8"))
    return Draft202012Validator(schema, registry=registry(root), format_checker=FormatChecker())


def errors(validator: Draft202012Validator, document: dict[str, Any]) -> list[str]:
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: tuple(str(part) for part in item.absolute_path))
    ]


def validate_store(root: pathlib.Path, store: dict[str, Any]) -> None:
    issues = errors(checker(root, STORE_SCHEMA), store)
    ids = [record["memory_id"] for record in store.get("records", []) if isinstance(record, dict) and "memory_id" in record]
    if len(ids) != len(set(ids)):
        issues.append("records: duplicate memory_id")
    if issues:
        raise ValueError("invalid memory store: " + "; ".join(issues))


def active_matches(store: dict[str, Any], proposal: dict[str, Any]) -> tuple[list[str], int]:
    claim = proposal["claim"]
    conflicts: list[str] = []
    identical = 0
    for record in store["records"]:
        if record["lifecycle"] != "active":
            continue
        existing = record["claim"]
        if existing["subject"] == claim["subject"] and existing["predicate"] == claim["predicate"]:
            if existing["object"] == claim["object"]:
                identical += 1
            else:
                conflicts.append(record["memory_id"])
    return conflicts, identical


def evidence_status(proposal: dict[str, Any], support_count: int) -> str:
    if proposal["memory_type"] == "user_preference" and proposal["trust"] == "authenticated_user":
        return "human_confirmed"
    if proposal["evidence"]["benchmark_refs"]:
        return "benchmark_supported"
    if support_count >= 2:
        return "corroborated"
    if proposal["provenance"]["evidence_refs"] or proposal["provenance"]["source_refs"]:
        return "single_source"
    return "unverified"


def make_record(proposal: dict[str, Any], lifecycle: str, memory_type: str | None = None) -> dict[str, Any]:
    support_count = proposal["evidence"]["support_count"]
    return {
        "schema_version": "memory-record.v0",
        "memory_id": f"memory.{proposal['proposal_id']}",
        "memory_type": memory_type or proposal["memory_type"],
        "scope": proposal["scope"],
        "claim": proposal["claim"],
        "provenance": proposal["provenance"],
        "trust": proposal["trust"],
        "evidence_status": evidence_status(proposal, support_count),
        "lifecycle": lifecycle,
        "owner": proposal["scope"]["ref"] or proposal["proposed_by"],
        "created_at": proposal["proposed_at"],
        "review_after": proposal["retention"]["review_after"],
        "expires_at": proposal["retention"]["expires_at"],
        "user_controllable": proposal["retention"]["user_controllable"],
        "supersedes_refs": proposal["supersedes_refs"],
    }


def evaluate(
    root: pathlib.Path,
    proposal: dict[str, Any],
    proposal_ref: str,
    store: dict[str, Any],
) -> dict[str, Any]:
    proposal_issues = errors(checker(root, PROPOSAL_SCHEMA), proposal)
    if proposal_issues:
        raise ValueError("invalid memory proposal: " + "; ".join(proposal_issues))
    validate_store(root, store)
    conflicts, identical = active_matches(store, proposal)
    support_count = proposal["evidence"]["support_count"] + identical
    review = proposal["evidence"]["human_review"]
    supersedes = set(proposal["supersedes_refs"])
    known_ids = {record["memory_id"] for record in store["records"]}
    invalid_supersedes = sorted(supersedes - known_ids)
    unresolved_conflicts = sorted(set(conflicts) - supersedes)
    record: dict[str, Any] | None = None

    if proposal["trust"] not in TRUSTED:
        disposition, target, reasons = "quarantine", "none", ["untrusted_source"]
    elif invalid_supersedes:
        disposition, target, reasons = "reject", "none", ["invalid_supersession_ref"]
    elif review["status"] == "fail":
        disposition, target, reasons = "reject", "none", ["human_review_failed"]
    elif proposal["retention"]["class"] != "durable":
        disposition, target, reasons = "retain_episodic", "episodic", ["session_retention"]
        record = make_record(proposal, "candidate", "episodic")
    elif unresolved_conflicts:
        disposition, target, reasons = "pending_review", "none", ["contradiction_unresolved"]
    elif not proposal["permissions"]["write_authorized"] or not proposal["permissions"]["authorization_ref"]:
        disposition, target, reasons = "pending_review", "none", ["write_permission_missing"]
    elif proposal["memory_type"] == "user_preference" and proposal["trust"] != "authenticated_user":
        disposition, target, reasons = "pending_review", "none", ["source_authority_mismatch"]
    elif review["status"] != "pass" or not review["reviewer"] or not review["notes"]:
        disposition, target, reasons = "pending_review", "none", ["human_review_pending"]
    elif proposal["memory_type"] in BENCHMARK_GATED and not proposal["evidence"]["benchmark_refs"]:
        disposition, target, reasons = "pending_review", "none", ["benchmark_evidence_missing"]
    elif proposal["memory_type"] in BENCHMARK_GATED and support_count < 2:
        disposition, target, reasons = "pending_review", "none", ["repeated_support_missing"]
    elif proposal["memory_type"] == "semantic" and support_count < 2 and not proposal["evidence"]["benchmark_refs"]:
        disposition, target, reasons = "pending_review", "none", ["repeated_support_missing"]
    else:
        disposition = "promote_durable"
        target = TARGET_STORE[proposal["memory_type"]]
        reasons = ["promotion_requirements_met"]
        promoted = copy_with_support(proposal, support_count)
        record = make_record(promoted, "active")

    decision = {
        "schema_version": "memory-promotion-decision.v0",
        "decision_id": f"memory-decision.{proposal['proposal_id']}",
        "proposal_ref": proposal_ref,
        "disposition": disposition,
        "target_store": target,
        "reason_codes": reasons,
        "detected_conflict_refs": conflicts,
        "record": record,
    }
    decision_issues = errors(checker(root, DECISION_SCHEMA), decision)
    if decision_issues:
        raise ValueError("invalid memory promotion decision: " + "; ".join(decision_issues))
    return decision


def copy_with_support(proposal: dict[str, Any], support_count: int) -> dict[str, Any]:
    copied = json.loads(json.dumps(proposal))
    copied["evidence"]["support_count"] = support_count
    return copied


def summary(decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "disposition": decision["disposition"],
        "target_store": decision["target_store"],
        "reason_codes": decision["reason_codes"],
        "conflict_count": len(decision["detected_conflict_refs"]),
        "record_emitted": decision["record"] is not None,
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_yaml(path)
        store = {
            "schema_version": "memory-store.v0",
            "updated_at": "2026-06-21T00:00:00Z",
            "records": case.get("existing_records", []),
        }
        try:
            actual = summary(evaluate(root, case["proposal"], path.relative_to(root).as_posix(), store))
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: disposition={actual['disposition']}, target={actual['target_store']}")
    if not paths or failures:
        print(f"Memory promotion fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Memory promotion fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--proposal", type=pathlib.Path)
    parser.add_argument("--store", type=pathlib.Path, default=DEFAULT_STORE)
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            return run_fixtures(root)
        if not args.proposal:
            raise ValueError("provide --proposal or use --fixtures")
        proposal_path = args.proposal if args.proposal.is_absolute() else root / args.proposal
        store_path = args.store if args.store.is_absolute() else root / args.store
        decision = evaluate(root, load_yaml(proposal_path), proposal_path.resolve().relative_to(root).as_posix(), load_yaml(store_path))
        rendered = yaml.safe_dump(decision, sort_keys=False)
        if args.output:
            output = args.output if args.output.is_absolute() else root / args.output
            if (root / "evals/results").resolve() not in output.resolve().parents:
                raise ValueError("memory decision output must be stored under evals/results/")
            if output.exists() and not args.overwrite:
                raise ValueError(f"output already exists: {output}")
            output.write_text(rendered, encoding="utf-8", newline="\n")
            print(f"wrote: {output}")
        else:
            print(rendered.rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
