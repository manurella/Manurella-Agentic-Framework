"""Apply a reviewed Atlas decision through a narrow, validated graph mutation boundary."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys
from datetime import datetime
from typing import Any

import yaml

from evaluate_memory_proposal import DECISION_SCHEMA, checker, errors, evaluate, load_yaml
from validate_framework import Validator


RESULT_SCHEMA = pathlib.Path("schemas/memory/atlas-application-result.schema.json")
DEFAULT_GRAPH = pathlib.Path("cognition/graph.yaml")
FIXTURE_DIR = pathlib.Path("evals/fixtures/atlas-application")
NODE_STATUSES = {"draft", "active", "accepted", "deprecated"}
EDGE_STATUSES = {"draft", "active", "deprecated"}
SUPPORTED_PREDICATES = {"lifecycle", "evidence_add"}


def graph_errors(root: pathlib.Path, graph: dict[str, Any]) -> list[str]:
    validator = Validator(root)
    validator.validate_graph_data(graph)
    return validator.errors


def applied_date(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("applied_at must include a timezone offset")
    return parsed.date().isoformat()


def valid_evidence_ref(root: pathlib.Path, ref: str) -> bool:
    if "\\" in ref:
        return False
    local, separator, fragment = ref.partition("#")
    if not local or (separator and not fragment):
        return False
    relative = pathlib.PurePosixPath(local)
    if relative.is_absolute() or ".." in relative.parts or ":" in relative.parts[0]:
        return False
    if relative.as_posix() != local:
        return False
    resolved = (root / pathlib.Path(*relative.parts)).resolve()
    return resolved != root and root in resolved.parents and resolved.exists()


def find_target(graph: dict[str, Any], target_id: str) -> list[tuple[str, dict[str, Any]]]:
    matches: list[tuple[str, dict[str, Any]]] = []
    matches.extend(("node", item) for item in graph["nodes"] if item["id"] == target_id)
    matches.extend(("edge", item) for item in graph["edges"] if item["id"] == target_id)
    return matches


def atlas_application_result(
    root: pathlib.Path,
    decision: dict[str, Any],
    decision_ref: str,
    graph: dict[str, Any],
    graph_ref: str,
    applied_at: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    decision_issues = errors(checker(root, DECISION_SCHEMA), decision)
    if decision_issues:
        raise ValueError("invalid memory decision: " + "; ".join(decision_issues))
    current_issues = graph_errors(root, graph)
    if current_issues:
        raise ValueError("invalid current graph: " + "; ".join(current_issues))

    updated = copy.deepcopy(graph)
    record = decision["record"]
    claim = record["claim"] if isinstance(record, dict) else None
    target_id = claim["subject"] if claim else None
    predicate = claim["predicate"] if claim else None
    desired = claim["object"] if claim else None
    disposition = "rejected"
    reason = "decision_not_applicable"
    target_kind: str | None = None
    prior_value: str | None = None
    resulting_value: str | None = None
    validation_passed = False

    applicable = (
        decision["disposition"] == "promote_durable"
        and decision["target_store"] == "atlas"
        and isinstance(record, dict)
        and record["memory_type"] == "atlas_mutation"
    )
    if applicable:
        matches = find_target(updated, target_id)
        if not matches:
            reason = "target_missing"
        elif len(matches) > 1:
            reason = "target_ambiguous"
        else:
            target_kind, target = matches[0]
            if predicate not in SUPPORTED_PREDICATES:
                reason = "unsupported_predicate"
            elif predicate == "lifecycle":
                prior_value = target["status"]
                allowed = NODE_STATUSES if target_kind == "node" else EDGE_STATUSES
                if desired not in allowed:
                    reason = "invalid_lifecycle"
                elif prior_value == desired:
                    disposition, reason = "no_change", "already_applied"
                    resulting_value = desired
                    validation_passed = True
                else:
                    target["status"] = desired
                    resulting_value = desired
                    disposition, reason = "applied", "mutation_applied"
            else:
                prior_value = desired if desired in target["evidence"] else None
                if not valid_evidence_ref(root, desired):
                    reason = "evidence_path_invalid"
                elif prior_value is not None:
                    disposition, reason = "no_change", "already_applied"
                    resulting_value = desired
                    validation_passed = True
                else:
                    target["evidence"].append(desired)
                    resulting_value = desired
                    disposition, reason = "applied", "mutation_applied"

            if disposition == "applied":
                changed_on = applied_date(applied_at)
                target["updated_at"] = changed_on
                updated["updated_at"] = changed_on
                candidate_issues = graph_errors(root, updated)
                if candidate_issues:
                    updated = copy.deepcopy(graph)
                    disposition, reason = "rejected", "post_validation_failed"
                    validation_passed = False
                else:
                    validation_passed = True

    result = {
        "schema_version": "atlas-application-result.v0",
        "application_id": f"atlas-application.{decision['decision_id']}",
        "decision_ref": decision_ref,
        "graph_ref": graph_ref,
        "disposition": disposition,
        "reason_code": reason,
        "target_id": target_id,
        "target_kind": target_kind,
        "predicate": predicate,
        "prior_value": prior_value,
        "resulting_value": resulting_value,
        "validation_passed": validation_passed,
        "graph_nodes": len(graph["nodes"]),
        "graph_edges": len(graph["edges"]),
    }
    result_issues = errors(checker(root, RESULT_SCHEMA), result)
    if result_issues:
        raise ValueError("invalid Atlas application result: " + "; ".join(result_issues))
    return result, updated


def fixture_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "disposition": result["disposition"],
        "reason_code": result["reason_code"],
        "target_kind": result["target_kind"],
        "resulting_value": result["resulting_value"],
        "validation_passed": result["validation_passed"],
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_yaml(path)
        promotion_path = root / case["promotion_fixture"]
        promotion_case = load_yaml(promotion_path)
        proposal = copy.deepcopy(promotion_case["proposal"])
        if "proposal_id" in case:
            proposal["proposal_id"] = case["proposal_id"]
        if "claim" in case:
            proposal["claim"] = case["claim"]
        store = {"schema_version": "memory-store.v0", "updated_at": "2026-06-21T00:00:00Z", "records": []}
        graph = load_yaml(root / DEFAULT_GRAPH)
        try:
            decision = evaluate(root, proposal, promotion_path.relative_to(root).as_posix(), store)
            result: dict[str, Any] = {}
            for _ in range(case.get("apply_times", 1)):
                result, graph = atlas_application_result(
                    root,
                    decision,
                    f"fixture://{path.name}",
                    graph,
                    "fixture://graph.yaml",
                    "2026-06-21T10:00:00Z",
                )
            actual = fixture_summary(result)
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: disposition={actual['disposition']}, reason={actual['reason_code']}")
    if not paths or failures:
        print(f"Atlas application fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Atlas application fixtures passed: {len(paths)} case(s)")
    return 0


def atomic_write(path: pathlib.Path, document: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8", newline="\n")
    temporary.replace(path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--decision", type=pathlib.Path)
    parser.add_argument("--graph", type=pathlib.Path, default=DEFAULT_GRAPH)
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
        graph_path = args.graph if args.graph.is_absolute() else root / args.graph
        canonical_graph = (root / DEFAULT_GRAPH).resolve()
        if graph_path.resolve() != canonical_graph:
            raise ValueError("Atlas application may write only cognition/graph.yaml")
        result, updated = atlas_application_result(
            root,
            load_yaml(decision_path),
            decision_path.resolve().relative_to(root).as_posix(),
            load_yaml(graph_path),
            DEFAULT_GRAPH.as_posix(),
            args.applied_at,
        )
        if args.apply and result["disposition"] == "applied":
            atomic_write(graph_path, updated)
            print(f"updated: {graph_path}")
        elif not args.apply:
            print("dry-run: canonical Atlas was not modified")
        print(yaml.safe_dump(result, sort_keys=False).rstrip())
        return 0 if result["disposition"] != "rejected" else 2
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
