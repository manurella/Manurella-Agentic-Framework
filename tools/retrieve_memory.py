"""Compile a bounded memory retrieval packet with lifecycle and staleness filtering."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pathlib
import sys
from datetime import datetime
from typing import Any

import yaml

from apply_memory_decision import application_result
from evaluate_memory_proposal import DEFAULT_STORE, checker, errors, evaluate, load_yaml, validate_store


PACKET_SCHEMA = pathlib.Path("schemas/memory/memory-retrieval-packet.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/memory-retrieval")
RETRIEVABLE_TYPES = {"episodic", "semantic", "procedural", "project_state", "user_preference", "failure_lesson"}
EVIDENCE_RANK = {
    "human_confirmed": 0,
    "benchmark_supported": 1,
    "corroborated": 2,
    "single_source": 3,
    "unverified": 4,
}


def timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"date-time must include an offset: {value}")
    return parsed


def scope_matches(record_scope: dict[str, Any], requested_scope: dict[str, Any], principal_ref: str | None) -> bool:
    if record_scope["kind"] == "global":
        return record_scope["ref"] is None or record_scope["ref"] == principal_ref
    return record_scope == requested_scope


def retrieval_packet(
    root: pathlib.Path,
    store: dict[str, Any],
    as_of: str,
    principal_ref: str | None,
    scope: dict[str, Any],
    requested_types: list[str],
    max_items: int,
) -> dict[str, Any]:
    validate_store(root, store)
    as_of_time = timestamp(as_of)
    if max_items < 1:
        raise ValueError("max_items must be at least 1")
    if len(requested_types) != len(set(requested_types)) or not set(requested_types) <= RETRIEVABLE_TYPES:
        raise ValueError("requested_types must be unique retrievable memory types")

    omitted = {key: 0 for key in ("expired", "review_overdue", "lifecycle", "scope", "type", "conflict", "limit")}
    eligible: list[dict[str, Any]] = []
    for record in store["records"]:
        lifecycle_allowed = record["lifecycle"] == "active" or (
            record["lifecycle"] == "candidate" and record["memory_type"] == "episodic"
        )
        if not lifecycle_allowed:
            omitted["lifecycle"] += 1
        elif record["expires_at"] is not None and timestamp(record["expires_at"]) <= as_of_time:
            omitted["expired"] += 1
        elif timestamp(record["review_after"]) <= as_of_time:
            omitted["review_overdue"] += 1
        elif not scope_matches(record["scope"], scope, principal_ref):
            omitted["scope"] += 1
        elif record["memory_type"] not in requested_types:
            omitted["type"] += 1
        else:
            eligible.append(record)

    claims: dict[tuple[str, str], dict[str, list[str]]] = {}
    for record in eligible:
        key = (record["claim"]["subject"], record["claim"]["predicate"])
        claims.setdefault(key, {}).setdefault(record["claim"]["object"], []).append(record["memory_id"])
    conflict_refs = sorted(
        memory_id
        for objects in claims.values()
        if len(objects) > 1
        for ids in objects.values()
        for memory_id in ids
    )
    conflict_set = set(conflict_refs)
    if conflict_set:
        omitted["conflict"] = len(conflict_set)
        eligible = [record for record in eligible if record["memory_id"] not in conflict_set]

    eligible.sort(
        key=lambda record: (
            EVIDENCE_RANK[record["evidence_status"]],
            -timestamp(record["created_at"]).timestamp(),
            record["memory_id"],
        )
    )
    omitted["limit"] = max(0, len(eligible) - max_items)
    selected_records = eligible[:max_items]
    selected = [
        {
            "memory_ref": record["memory_id"],
            "memory_type": record["memory_type"],
            "scope": copy.deepcopy(record["scope"]),
            "claim": copy.deepcopy(record["claim"]),
            "trust": record["trust"],
            "evidence_status": record["evidence_status"],
            "source_refs": copy.deepcopy(record["provenance"]["source_refs"]),
        }
        for record in selected_records
    ]
    identity = json.dumps(
        {"as_of": as_of, "principal_ref": principal_ref, "scope": scope, "requested_types": requested_types, "max_items": max_items},
        sort_keys=True,
        separators=(",", ":"),
    )
    packet = {
        "schema_version": "memory-retrieval-packet.v0",
        "packet_id": f"memory-retrieval.{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:12]}",
        "as_of": as_of,
        "principal_ref": principal_ref,
        "scope": scope,
        "requested_types": requested_types,
        "selected": selected,
        "omitted": omitted,
        "conflict_refs": conflict_refs,
    }
    issues = errors(checker(root, PACKET_SCHEMA), packet)
    if issues:
        raise ValueError("invalid memory retrieval packet: " + "; ".join(issues))
    return packet


def fixture_store(root: pathlib.Path, case: dict[str, Any], path: pathlib.Path) -> dict[str, Any]:
    store = {
        "schema_version": "memory-store.v0",
        "updated_at": "2026-06-21T00:00:00Z",
        "records": copy.deepcopy(case.get("existing_records", [])),
    }
    for fixture_ref in case.get("promotion_fixtures", []):
        promotion_path = root / fixture_ref
        promotion_case = load_yaml(promotion_path)
        decision = evaluate(root, promotion_case["proposal"], fixture_ref, store)
        result, store = application_result(
            root,
            decision,
            f"fixture://{promotion_path.name}",
            store,
            f"fixture://{path.name}",
            "2026-06-21T10:00:00Z",
        )
        if result["disposition"] != "applied":
            raise ValueError(f"fixture promotion was not applied: {fixture_ref}")
    return store


def fixture_summary(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "selected_refs": [item["memory_ref"] for item in packet["selected"]],
        "omitted": packet["omitted"],
        "conflict_refs": packet["conflict_refs"],
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_yaml(path)
        request = case["request"]
        try:
            packet = retrieval_packet(
                root,
                fixture_store(root, case, path),
                request["as_of"],
                request.get("principal_ref"),
                request["scope"],
                request["requested_types"],
                request["max_items"],
            )
            actual = fixture_summary(packet)
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: selected={len(packet['selected'])}, omitted={sum(packet['omitted'].values())}")
    if not paths or failures:
        print(f"Memory retrieval fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Memory retrieval fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--store", type=pathlib.Path, default=DEFAULT_STORE)
    parser.add_argument("--as-of")
    parser.add_argument("--principal-ref")
    parser.add_argument("--scope-kind", choices=["global", "project", "domain", "task"])
    parser.add_argument("--scope-ref")
    parser.add_argument("--type", dest="requested_types", action="append", choices=sorted(RETRIEVABLE_TYPES))
    parser.add_argument("--max-items", type=int, default=8)
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            return run_fixtures(root)
        if not args.as_of or not args.scope_kind or not args.requested_types:
            raise ValueError("provide --as-of, --scope-kind, and at least one --type, or use --fixtures")
        if args.scope_kind != "global" and not args.scope_ref:
            raise ValueError("non-global retrieval scope requires --scope-ref")
        store_path = args.store if args.store.is_absolute() else root / args.store
        packet = retrieval_packet(
            root,
            load_yaml(store_path),
            args.as_of,
            args.principal_ref,
            {"kind": args.scope_kind, "ref": args.scope_ref},
            args.requested_types,
            args.max_items,
        )
        print(yaml.safe_dump(packet, sort_keys=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
