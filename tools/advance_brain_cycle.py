"""Revise Brain workspace state from typed observations and choose bounded control."""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from compile_brain_workspace import (
    bundle_validator,
    compile_validated,
    validation_errors,
)
from validate_interpreter import load_mapping, materialize_fixture


SCHEMA_DIR = pathlib.Path("schemas/brain")
EVENT_SCHEMA = SCHEMA_DIR / "observation-event.schema.json"
RESULT_SCHEMA = SCHEMA_DIR / "brain-cycle-result.schema.json"
FIXTURE_DIR = pathlib.Path("evals/fixtures/brain-cycle")
TRUSTED = {"trusted_runtime", "trusted_user"}


def schema_registry(root: pathlib.Path) -> Registry:
    registry = Registry()
    for path in sorted((root / SCHEMA_DIR).glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(schema["$id"], resource)
        registry = registry.with_resource(path.name, resource)
    return registry


def validator(root: pathlib.Path, relative: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / relative).read_text(encoding="utf-8"))
    return Draft202012Validator(
        schema,
        registry=schema_registry(root),
        format_checker=FormatChecker(),
    )


def add_unique(target: list[str], values: list[str], limit: int | None = None) -> None:
    for value in values:
        if value not in target and (limit is None or len(target) < limit):
            target.append(value)


def select_strategy(bundle: dict[str, Any], disposition: str | None = None) -> str:
    context = bundle["context_packet"]
    state = bundle["brain_state"]
    operation = context["operation"]
    if operation in {"clarify", "confirm", "refuse"}:
        return operation
    if disposition == "replan":
        return "model_predictive_replan" if state["task"]["project_id"] else "plan_and_execute"
    if disposition == "repair":
        return "reactive_tool"
    if operation == "respond":
        return "direct_response"
    if state["task"]["project_id"] and context["routing"]["mode"] == "standard":
        return "hierarchical_decomposition"
    if state["capabilities"]["likely_tools"]:
        return "reactive_tool"
    return "plan_and_execute"


def stop_reason(bundle: dict[str, Any]) -> tuple[str, str]:
    operation = bundle["context_packet"]["operation"]
    return {
        "clarify": ("awaiting_clarification", "clarify"),
        "confirm": ("awaiting_confirmation", "confirm"),
        "refuse": ("policy_refusal", "refuse"),
    }[operation]


def advance(
    root: pathlib.Path,
    initial: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    initial_errors = validation_errors(bundle_validator(root), initial)
    if initial_errors:
        raise ValueError("invalid initial workspace bundle: " + "; ".join(initial_errors))
    event_checker = validator(root, EVENT_SCHEMA)
    for event in events:
        errors = validation_errors(event_checker, event)
        if errors:
            raise ValueError(f"invalid observation {event.get('observation_id', '<unknown>')}: {'; '.join(errors)}")

    revised = copy.deepcopy(initial)
    state = revised["brain_state"]
    workspace = revised["active_workspace"]
    context = revised["context_packet"]
    trusted_events = [event for event in events if event["trust"] in TRUSTED]
    quarantined = len(events) - len(trusted_events)
    cycles = max(0, workspace["budgets"]["cycles_remaining"] - len(events))
    repairs = workspace["budgets"]["repairs_remaining"]
    repeat_counts = Counter(
        event["repeat_key"] for event in trusted_events if event["repeat_key"]
    )
    repeated = max(repeat_counts.values(), default=0)
    state_changed = any(event["effect"] != "no_change" for event in trusted_events)
    evidence_gain = any(event["evidence_refs"] for event in trusted_events)
    unsafe = any(event["effect"] == "unsafe" for event in trusted_events)
    runtime_blocked = any(event["effect"] == "blocked" for event in trusted_events)
    failed = any(
        event["effect"] == "failure" or event["verification"]["status"] == "fail"
        for event in trusted_events
    )
    stalled = repeated >= 2 and any(event["effect"] == "no_change" for event in trusted_events)

    verification_events = [
        event for event in trusted_events if event["verification"]["status"] != "not_run"
    ]
    verification = (
        copy.deepcopy(verification_events[-1]["verification"])
        if verification_events
        else {"status": "not_run", "acceptance_status": "not_evaluated", "check_ids": []}
    )
    acceptance_complete = (
        verification["status"] == "pass" and verification["acceptance_status"] == "complete"
    )

    for event in trusted_events:
        item = {
            "id": event["observation_id"],
            "statement": event["statement"],
            "source_refs": list(dict.fromkeys([event["source_ref"], *event["evidence_refs"]])),
        }
        workspace["observations"].append(item)
        state["world"]["observations"].append(copy.deepcopy(item))
        add_unique(workspace["evidence_refs"], event["evidence_refs"])
        add_unique(
            context["evidence_refs"],
            event["evidence_refs"],
            context["budgets"]["context_items"],
        )
        if event["effect"] == "failure":
            state["uncertainty"]["execution"].append(
                {
                    "id": f"uncertainty.{event['observation_id']}",
                    "statement": event["statement"],
                    "source_refs": [event["source_ref"]],
                }
            )

    if quarantined:
        context["omissions"]["untrusted_data_count"] += quarantined
        state["uncertainty"]["environmental"].append(
            {
                "id": f"uncertainty.quarantined-observations.{state['revision'] + 1}",
                "statement": "One or more untrusted observations require validation before use.",
                "source_refs": [],
            }
        )

    initially_blocked = state["task"]["status"] == "blocked"
    if initially_blocked and not trusted_events:
        reason, next_operation = stop_reason(revised)
        disposition = "stop_blocked"
        reasons = [reason]
    elif unsafe:
        disposition, reasons, next_operation = "stop_unsafe", ["unsafe_observation"], "stop"
    elif acceptance_complete:
        disposition, reasons, next_operation = "stop_complete", ["acceptance_complete"], "stop"
    elif runtime_blocked or initially_blocked:
        disposition, reasons, next_operation = "stop_blocked", ["runtime_blocked"], "stop"
    elif cycles == 0:
        disposition, reasons, next_operation = "stop_budget", ["cycle_budget_exhausted"], "stop"
    elif failed and repeated >= 2:
        disposition, reasons, next_operation = "replan", ["verification_failed", "repeated_failure"], "replan"
    elif failed and repairs > 0:
        repairs -= 1
        disposition, reasons, next_operation = "repair", ["verification_failed", "repair_available"], "repair"
    elif failed:
        disposition, reasons, next_operation = "escalate", ["verification_failed"], "escalate"
    elif stalled:
        disposition, reasons, next_operation = "replan", ["stalled_progress"], "replan"
    else:
        disposition = "continue"
        reasons = ["trusted_progress" if state_changed or evidence_gain else "verification_pending"]
        next_operation = "verify" if state_changed or evidence_gain else context["operation"]

    revision = state["revision"] + len(events)
    if events:
        state["updated_at"] = events[-1]["observed_at"]
    state["revision"] = revision
    state_ref = f"{state['state_id']}#{revision}"
    workspace["state_ref"] = state_ref
    context["state_ref"] = state_ref
    workspace["budgets"]["cycles_remaining"] = cycles
    workspace["budgets"]["repairs_remaining"] = repairs
    if disposition == "stop_complete":
        state["task"]["status"] = "complete"
        workspace["plan_steps"][0]["status"] = "complete"
    elif disposition in {"stop_blocked", "stop_unsafe", "stop_budget", "escalate"}:
        state["task"]["status"] = "blocked"
        workspace["plan_steps"][0]["status"] = "blocked"
    elif verification["status"] in {"pass", "partial"}:
        state["task"]["status"] = "verifying"
    else:
        state["task"]["status"] = "active"

    decision = {
        "schema_version": "brain-control-decision.v0",
        "decision_id": f"control.{state['state_id']}#{revision}",
        "state_ref": state_ref,
        "strategy": select_strategy(revised, disposition),
        "disposition": disposition,
        "reason_codes": reasons,
        "progress": {
            "state_changed": state_changed,
            "evidence_gain": evidence_gain,
            "repeated_event_count": repeated,
            "contradictions_open": len(state["uncertainty"]["contradictions"]),
            "cycles_remaining": cycles,
            "repairs_remaining": repairs,
        },
        "verification": verification,
        "next_operation": next_operation,
    }
    result = {
        "schema_version": "brain-cycle-result.v0",
        "events_consumed": len(events),
        "events_quarantined": quarantined,
        "revised_workspace_bundle": revised,
        "control_decision": decision,
    }
    result_errors = validation_errors(validator(root, RESULT_SCHEMA), result)
    if result_errors:
        raise ValueError("invalid Brain cycle result: " + "; ".join(result_errors))
    return result


def expand_events(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    for item in items:
        event = copy.deepcopy(item)
        repeat = int(event.pop("repeat", 1))
        for index in range(1, repeat + 1):
            child = copy.deepcopy(event)
            if repeat > 1:
                child["observation_id"] = f"{event['observation_id']}.{index}"
            expanded.append(child)
    return expanded


def result_summary(result: dict[str, Any]) -> dict[str, Any]:
    decision = result["control_decision"]
    return {
        "strategy": decision["strategy"],
        "disposition": decision["disposition"],
        "next_operation": decision["next_operation"],
        "task_status": result["revised_workspace_bundle"]["brain_state"]["task"]["status"],
        "cycles_remaining": decision["progress"]["cycles_remaining"],
        "repairs_remaining": decision["progress"]["repairs_remaining"],
        "events_quarantined": result["events_quarantined"],
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        source = root / case["interpreter_fixture"]
        try:
            initial = compile_validated(root, materialize_fixture(source, load_mapping(source)))
            result = advance(root, initial, expand_events(case.get("events", [])))
            actual = result_summary(result)
            rendered = yaml.safe_dump(result, sort_keys=False)
            leaked = [
                event["observation_id"]
                for event in case.get("events", [])
                if event.get("trust") not in TRUSTED and event["statement"] in rendered
            ]
            if leaked:
                raise ValueError("untrusted observation text leaked: " + ", ".join(leaked))
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: strategy={actual['strategy']}, disposition={actual['disposition']}")
    if not paths or failures:
        print(f"Brain cycle fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Brain cycle fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--workspace", type=pathlib.Path)
    parser.add_argument("--observations", type=pathlib.Path)
    parser.add_argument("--fixtures", action="store_true")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            if args.workspace or args.observations:
                raise ValueError("--fixtures cannot be combined with input paths")
            return run_fixtures(root)
        if not args.workspace or not args.observations:
            raise ValueError("provide --workspace and --observations, or use --fixtures")
        workspace_path = args.workspace if args.workspace.is_absolute() else root / args.workspace
        observations_path = args.observations if args.observations.is_absolute() else root / args.observations
        initial = load_mapping(workspace_path)
        observation_document = load_mapping(observations_path)
        result = advance(root, initial, observation_document["events"])
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=True))
        else:
            print(yaml.safe_dump(result, sort_keys=False, allow_unicode=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
