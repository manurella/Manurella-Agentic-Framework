"""Apply reviewed memory decisions to the canonical file store with supersession checks."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys
from typing import Any

import yaml

from evaluate_memory_proposal import (
    DECISION_SCHEMA,
    DEFAULT_STORE,
    checker,
    errors,
    evaluate,
    load_yaml,
    validate_store,
)


RESULT_SCHEMA = pathlib.Path("schemas/memory/memory-application-result.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/memory-application")


def application_result(
    root: pathlib.Path,
    decision: dict[str, Any],
    decision_ref: str,
    store: dict[str, Any],
    store_ref: str,
    applied_at: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    decision_issues = errors(checker(root, DECISION_SCHEMA), decision)
    if decision_issues:
        raise ValueError("invalid memory decision: " + "; ".join(decision_issues))
    validate_store(root, store)
    updated = copy.deepcopy(store)
    before = len(updated["records"])
    record = decision["record"]
    disposition = "rejected"
    reason = "decision_not_applicable"
    record_id = record["memory_id"] if isinstance(record, dict) else None
    superseded: list[str] = []

    if decision["target_store"] == "atlas":
        reason = "atlas_requires_separate_apply"
    elif decision["disposition"] not in {"retain_episodic", "promote_durable"} or record is None:
        reason = "decision_not_applicable"
    else:
        by_id = {item["memory_id"]: item for item in updated["records"]}
        existing = by_id.get(record_id)
        if existing == record:
            disposition, reason = "no_change", "already_applied"
        elif existing is not None:
            reason = "duplicate_record_conflict"
        else:
            missing = [ref for ref in record["supersedes_refs"] if ref not in by_id]
            active_conflicts = [
                item["memory_id"]
                for item in updated["records"]
                if item["lifecycle"] == "active"
                and item["claim"]["subject"] == record["claim"]["subject"]
                and item["claim"]["predicate"] == record["claim"]["predicate"]
                and item["claim"]["object"] != record["claim"]["object"]
                and item["memory_id"] not in record["supersedes_refs"]
            ]
            if missing:
                reason = "supersession_target_missing"
            elif active_conflicts:
                reason = "active_claim_conflict"
            else:
                for item in updated["records"]:
                    if item["memory_id"] in record["supersedes_refs"]:
                        item["lifecycle"] = "superseded"
                        superseded.append(item["memory_id"])
                updated["records"].append(copy.deepcopy(record))
                updated["updated_at"] = applied_at
                validate_store(root, updated)
                disposition, reason = "applied", "record_applied"

    result = {
        "schema_version": "memory-application-result.v0",
        "application_id": f"application.{decision['decision_id']}",
        "decision_ref": decision_ref,
        "store_ref": store_ref,
        "disposition": disposition,
        "reason_code": reason,
        "record_id": record_id,
        "superseded_refs": superseded,
        "records_before": before,
        "records_after": len(updated["records"]),
    }
    result_issues = errors(checker(root, RESULT_SCHEMA), result)
    if result_issues:
        raise ValueError("invalid memory application result: " + "; ".join(result_issues))
    return result, updated


def summary(result: dict[str, Any], store: dict[str, Any]) -> dict[str, Any]:
    return {
        "disposition": result["disposition"],
        "reason_code": result["reason_code"],
        "records_after": result["records_after"],
        "active_records": sum(item["lifecycle"] == "active" for item in store["records"]),
        "candidate_records": sum(item["lifecycle"] == "candidate" for item in store["records"]),
        "superseded_records": sum(item["lifecycle"] == "superseded" for item in store["records"]),
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_yaml(path)
        promotion_path = root / case["promotion_fixture"]
        promotion_case = load_yaml(promotion_path)
        store = {
            "schema_version": "memory-store.v0",
            "updated_at": "2026-06-21T00:00:00Z",
            "records": copy.deepcopy(promotion_case.get("existing_records", [])),
        }
        try:
            decision = evaluate(root, promotion_case["proposal"], promotion_path.relative_to(root).as_posix(), store)
            result: dict[str, Any] = {}
            for _ in range(case.get("apply_times", 1)):
                result, store = application_result(
                    root,
                    decision,
                    f"fixture://{promotion_path.name}",
                    store,
                    "fixture://memory-store",
                    "2026-06-21T10:00:00Z",
                )
            actual = summary(result, store)
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: disposition={actual['disposition']}, records={actual['records_after']}")
    if not paths or failures:
        print(f"Memory application fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Memory application fixtures passed: {len(paths)} case(s)")
    return 0


def atomic_write(path: pathlib.Path, document: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8", newline="\n")
    temporary.replace(path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--decision", type=pathlib.Path)
    parser.add_argument("--store", type=pathlib.Path, default=DEFAULT_STORE)
    parser.add_argument("--applied-at")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            return run_fixtures(root)
        if not args.decision or not args.applied_at:
            raise ValueError("provide --decision and --applied-at, or use --fixtures")
        decision_path = args.decision if args.decision.is_absolute() else root / args.decision
        store_path = args.store if args.store.is_absolute() else root / args.store
        if root not in store_path.resolve().parents:
            raise ValueError("memory store must be inside the repository")
        result, updated = application_result(
            root,
            load_yaml(decision_path),
            decision_path.resolve().relative_to(root).as_posix(),
            load_yaml(store_path),
            store_path.resolve().relative_to(root).as_posix(),
            args.applied_at,
        )
        if args.apply and result["disposition"] == "applied":
            atomic_write(store_path, updated)
            print(f"updated: {store_path}")
        elif not args.apply:
            print("dry-run: canonical memory was not modified")
        print(yaml.safe_dump(result, sort_keys=False).rstrip())
        return 0 if result["disposition"] != "rejected" else 2
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
