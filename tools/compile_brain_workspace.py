"""Compile validated Interpreter and Core artifacts into bounded Brain workspace state."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from compile_core_packet import build_validators, compile_core_projection
from validate_interpreter import load_mapping, materialize_fixture, validate_bundle, versioned_ref


SCHEMA_DIR = pathlib.Path("schemas/brain")
BUNDLE_SCHEMA = SCHEMA_DIR / "workspace-bundle.schema.json"
FIXTURE_DIR = pathlib.Path("evals/fixtures/brain-workspace")
BANNED_CONTEXT_KEYS = {
    "raw_request",
    "turn_refs",
    "untrusted_data_refs",
    "tool_arguments",
    "tool_responses",
    "reasoning",
    "chain_of_thought",
}


def unique(values: Iterable[str | None]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def statements(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": item["id"],
            "statement": item["statement"],
            "source_refs": unique(item.get("source_refs", [])),
        }
        for item in items
    ]


def criterion_text(acceptance: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for field in ("required_outcomes", "required_artifacts", "hard_checks"):
        values.extend(item["statement"] for item in acceptance[field])
    return unique(values)


def operation_for(disposition: str) -> str:
    return {
        "clarify": "clarify",
        "confirm": "confirm",
        "refuse": "refuse",
        "direct": "respond",
        "delegate": "delegate",
    }[disposition]


def compile_workspace(data: dict[str, Any], routing: dict[str, Any]) -> dict[str, Any]:
    task = data["task_frame"]
    acceptance = data["acceptance_contract"]
    clarification = data["clarification_decision"]
    identity = task["identity"]
    task_ref = versioned_ref(identity["frame_id"], identity["version"])
    state_id = f"state.{identity['frame_id']}@{identity['version']}"
    state_ref = f"{state_id}#1"
    blocked = routing["disposition"] in {"clarify", "confirm", "refuse"}
    operation = operation_for(routing["disposition"])
    cycle_budget = 2 if routing["mode"] == "fast" else (8 if routing["family_class"] == "C" else 6)
    repair_budget = 0 if routing["mode"] == "fast" else 1
    context_items_max = 12 if routing["mode"] == "fast" else 24

    uncertainty = task["uncertainty"]
    epistemic = statements([*uncertainty["ambiguities"], *uncertainty["missing_information"]])
    environmental = statements(uncertainty["assumptions"])
    contradictions = statements(uncertainty["contradictions"])
    execution = [
        {"id": f"routing-question.{index}", "statement": value, "source_refs": []}
        for index, value in enumerate(task["routing_hints"]["unresolved_routing_questions"], 1)
    ]
    policy = [
        {
            "id": item["id"],
            "statement": f"Permission required: {item['capability']}",
            "source_refs": [],
        }
        for item in task["governance"]["permissions_required"]
        if item["status"] == "required"
    ] + [
        {
            "id": item["id"],
            "statement": f"Confirmation required: {item['subject']}",
            "source_refs": [],
        }
        for item in task["governance"]["confirmations_required"]
        if item["status"] == "required"
    ]
    blockers = unique(
        [
            *(clarification["affected_uncertainty_ids"] if clarification["blocks_execution"] else []),
            *(item["id"] for item in task["governance"]["permissions_required"] if item["status"] == "required"),
            *(item["id"] for item in task["governance"]["confirmations_required"] if item["status"] == "required"),
        ]
    )
    preferences = unique(
        f"{key}={value}"
        for key, value in task["execution_preferences"].items()
        if value is not None
    )
    dependency_refs = unique(item["ref"] for item in task["scope"]["dependencies"])
    evidence_refs = unique([*task["source"]["trusted_context_refs"], *dependency_refs])
    outcome_claims = [
        {"id": item["id"], "statement": item["statement"], "source_refs": []}
        for item in task["objective"]["desired_outcomes"]
    ]
    goal_claim = {
        "id": "claim.goal",
        "statement": task["objective"]["normalized_goal"],
        "source_refs": unique(task["source"]["trusted_context_refs"]),
    }

    brain_state = {
        "schema_version": "brain-state.v0",
        "state_id": state_id,
        "revision": 1,
        "updated_at": task["lifecycle"]["updated_at"],
        "task": {
            "task_frame_ref": task_ref,
            "acceptance_contract_ref": task["acceptance_contract_ref"],
            "goal": task["objective"]["normalized_goal"],
            "status": "blocked" if blocked else "active",
            "project_id": identity["project_id"],
            "project_posture": routing["project_posture"],
            "dependencies": dependency_refs,
            "blockers": blockers,
        },
        "world": {"observations": [], "assumptions": environmental},
        "user": {
            "preferences": preferences,
            "permissions_required": [item["id"] for item in task["governance"]["permissions_required"] if item["status"] == "required"],
            "confirmations_required": [item["id"] for item in task["governance"]["confirmations_required"] if item["status"] == "required"],
        },
        "self": {
            "mode": routing["mode"],
            "effort": routing["effort"],
            "selected_domain": routing["selected_domain"],
            "selected_agent": routing["selected_agent"],
            "cycle_budget": cycle_budget,
            "repair_budget": repair_budget,
        },
        "uncertainty": {
            "epistemic": epistemic,
            "environmental": environmental,
            "execution": execution,
            "policy": policy,
            "contradictions": contradictions,
            "blocking": blocked,
        },
        "capabilities": {
            "required": unique(task["routing_hints"]["required_capabilities"]),
            "likely_tools": unique(task["routing_hints"]["likely_tools"]),
        },
    }
    workspace = {
        "schema_version": "active-workspace.v0",
        "workspace_id": f"workspace.{identity['frame_id']}@{identity['version']}",
        "state_ref": state_ref,
        "volatile": True,
        "claims": [goal_claim, *outcome_claims],
        "evidence_refs": evidence_refs,
        "plan_steps": [
            {
                "step_id": "step.next-operation",
                "operation": operation,
                "status": "blocked" if blocked else "ready",
                "blocked_by": blockers,
            }
        ],
        "observations": [],
        "contradictions": contradictions,
        "unresolved_questions": [
            {
                "id": item["id"],
                "statement": item["statement"],
                "source_refs": item["source_refs"],
            }
            for item in [*epistemic, *execution]
        ],
        "dependencies": dependency_refs,
        "budgets": {
            "cycles_remaining": cycle_budget,
            "repairs_remaining": repair_budget,
            "context_items_max": context_items_max,
        },
    }
    context = {
        "schema_version": "context-packet.v0",
        "packet_id": f"context.{identity['frame_id']}@{identity['version']}.1",
        "state_ref": state_ref,
        "operation": operation,
        "mission": task["objective"]["normalized_goal"],
        "trusted_claims": [goal_claim, *outcome_claims][:context_items_max],
        "evidence_refs": evidence_refs[:context_items_max],
        "constraints": unique(
            item["statement"]
            for item in [*task["constraints"]["hard"], *task["constraints"]["exclusions"]]
        ),
        "acceptance_criteria": criterion_text(acceptance),
        "routing": {
            "domain": routing["selected_domain"],
            "agent": routing["selected_agent"],
            "secondary_domains": routing["secondary_domains"],
            "mode": routing["mode"],
            "effort": routing["effort"],
        },
        "budgets": {
            "cycles": cycle_budget,
            "repairs": repair_budget,
            "context_items": context_items_max,
        },
        "omissions": {
            "untrusted_data_count": len(task["source"]["untrusted_data_refs"]),
            "reason": "Untrusted data is referenced only through controlled retrieval and is not copied into the context packet.",
        },
    }
    return {
        "schema_version": "workspace-bundle.v0",
        "brain_state": brain_state,
        "active_workspace": workspace,
        "context_packet": context,
    }


def bundle_validator(root: pathlib.Path) -> Draft202012Validator:
    registry = Registry()
    for path in sorted((root / SCHEMA_DIR).glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(schema["$id"], resource)
        registry = registry.with_resource(path.name, resource)
    schema = json.loads((root / BUNDLE_SCHEMA).read_text(encoding="utf-8"))
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def validation_errors(checker: Draft202012Validator, document: dict[str, Any]) -> list[str]:
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(checker.iter_errors(document), key=lambda item: tuple(str(part) for part in item.absolute_path))
    ]


def find_banned(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in BANNED_CONTEXT_KEYS:
                found.append(child_path)
            found.extend(find_banned(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_banned(child, f"{path}[{index}]"))
    return found


def compile_validated(root: pathlib.Path, data: dict[str, Any]) -> dict[str, Any]:
    task_validator, acceptance_validator, _ = build_validators(root)
    issues = validate_bundle(data, task_validator, acceptance_validator)
    if issues:
        raise ValueError("invalid Interpreter bundle: " + "; ".join(item.render() for item in issues))
    routing = compile_core_projection(data)
    bundle = compile_workspace(data, routing)
    errors = validation_errors(bundle_validator(root), bundle)
    banned = find_banned(bundle["context_packet"])
    if errors or banned:
        details = [*errors, *(f"banned context key: {item}" for item in banned)]
        raise ValueError("invalid Brain workspace bundle: " + "; ".join(details))
    return bundle


def summary(bundle: dict[str, Any]) -> dict[str, Any]:
    state = bundle["brain_state"]
    context = bundle["context_packet"]
    return {
        "task_status": state["task"]["status"],
        "operation": context["operation"],
        "domain": context["routing"]["domain"],
        "mode": context["routing"]["mode"],
        "effort": context["routing"]["effort"],
        "blocking_uncertainty": state["uncertainty"]["blocking"],
        "blocker_count": len(state["task"]["blockers"]),
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        source = root / case["interpreter_fixture"]
        try:
            data = materialize_fixture(source, load_mapping(source))
            actual = summary(compile_validated(root, data))
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: status={actual['task_status']}, operation={actual['operation']}, domain={actual['domain']}")
    if not paths or failures:
        print(f"Brain workspace fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Brain workspace fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--input", type=pathlib.Path)
    parser.add_argument("--fixtures", action="store_true")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures == bool(args.input):
            raise ValueError("choose exactly one of --fixtures or --input")
        if args.fixtures:
            return run_fixtures(root)
        path = args.input if args.input.is_absolute() else root / args.input
        data = materialize_fixture(path, load_mapping(path))
        bundle = compile_validated(root, data)
        if args.format == "json":
            print(json.dumps(bundle, indent=2, ensure_ascii=True))
        else:
            print(yaml.safe_dump(bundle, sort_keys=False, allow_unicode=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
