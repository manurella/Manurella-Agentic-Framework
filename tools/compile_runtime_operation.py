"""Compile a Brain cycle result into a portable runtime operation packet."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from advance_brain_cycle import advance, expand_events
from compile_brain_workspace import compile_validated, find_banned
from validate_interpreter import load_mapping, materialize_fixture


SCHEMA = pathlib.Path("schemas/runtime/operation-packet.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/runtime-operation")
ALL_ACTIONS = ("read", "edit", "shell", "browser", "web", "delegate", "respond")
CLASS_BY_NEXT = {
    "clarify": "clarification",
    "confirm": "confirmation",
    "refuse": "refusal",
    "respond": "direct",
    "delegate": "delegation",
    "verify": "verification",
    "repair": "repair",
    "replan": "replan",
    "escalate": "escalation",
}
OUTPUT_BY_CLASS = {
    "direct": ["direct_response"],
    "clarification": ["clarification_question"],
    "confirmation": ["confirmation_request"],
    "refusal": ["bounded_refusal"],
    "delegation": ["bounded_handoff_result", "observation_events"],
    "verification": ["verification_result", "observation_events"],
    "repair": ["repaired_artifact", "verification_result", "observation_events"],
    "replan": ["revised_plan", "next_operation_packet"],
    "recovery": ["recovery_checkpoint", "narrower_next_packet"],
    "escalation": ["escalation_record", "smallest_unblocking_request"],
    "stop": ["stop_record"],
}


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def packet_class(decision: dict[str, Any]) -> str:
    disposition = decision["disposition"]
    if disposition == "stop_budget":
        return "recovery"
    if disposition == "stop_blocked" and decision["next_operation"] == "stop":
        return "recovery"
    if disposition in {"stop_complete", "stop_unsafe"}:
        return "stop"
    return CLASS_BY_NEXT[decision["next_operation"]]


def read_agent_policy(root: pathlib.Path, domain: str, agent: str, mode: str) -> dict[str, str]:
    path = root / "domains" / domain / "agents" / f"{agent}.md"
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"agent permission source lacks frontmatter: {path}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"agent permission source has malformed frontmatter: {path}")
    document = yaml.safe_load(parts[1]) or {}
    permissions = document.get("permissions")
    if not isinstance(permissions, dict):
        raise ValueError(f"agent permission source lacks permissions: {path}")
    for key in ("read", "edit", "shell", "web", "delegate"):
        if permissions.get(key) not in {"allow", "ask", "deny"}:
            raise ValueError(f"agent permission source has invalid {key!r}: {path}")
    policy = {
        "read": permissions["read"],
        "edit": permissions["edit"],
        "shell": permissions["shell"],
        "browser": permissions["web"],
        "web": permissions["web"],
        "delegate": permissions["delegate"],
        "respond": "allow",
    }
    if mode == "fast":
        policy["delegate"] = "deny"
    return policy


def requested_actions(kind: str) -> list[str]:
    if kind in {"direct", "clarification", "confirmation", "refusal", "escalation"}:
        return ["respond"]
    if kind in {"stop"}:
        return []
    if kind in {"replan", "recovery"}:
        return ["read"]
    if kind == "delegation":
        return ["read", "edit", "shell", "browser", "web", "delegate"]
    if kind == "verification":
        return ["read", "shell", "browser", "web"]
    if kind == "repair":
        return ["read", "edit", "shell", "browser", "web"]
    return ["read"]


def timebox(kind: str, mode: str) -> int:
    if kind == "stop":
        return 1
    if kind in {"clarification", "confirmation", "refusal", "direct"}:
        return 3 if mode == "fast" else 6
    if kind == "recovery":
        return 3 if mode == "fast" else 6
    if kind in {"verification", "replan", "escalation"}:
        return 5 if mode == "fast" else 10
    return 5 if mode == "fast" else 12


def compile_packet(
    root: pathlib.Path,
    cycle: dict[str, Any],
    prior_packet_ref: str | None = None,
) -> dict[str, Any]:
    bundle = cycle["revised_workspace_bundle"]
    state = bundle["brain_state"]
    workspace = bundle["active_workspace"]
    context = bundle["context_packet"]
    decision = cycle["control_decision"]
    kind = packet_class(decision)
    policy = read_agent_policy(
        root,
        context["routing"]["domain"],
        context["routing"]["agent"],
        context["routing"]["mode"],
    )
    requested = requested_actions(kind)
    actions = [action for action in requested if policy[action] != "deny"]
    blocked_actions = [action for action in requested if policy[action] == "deny"]
    last_step = workspace["observations"][-1]["id"] if workspace["observations"] else None
    original_repairs = context["budgets"]["repairs"]
    retry_count = max(0, original_repairs - workspace["budgets"]["repairs_remaining"])
    acceptance_evidence = context["acceptance_criteria"] if kind in {"delegation", "verification", "repair"} else []
    packet = {
        "schema_version": "operation-packet.v0",
        "packet_id": f"packet.{decision['decision_id']}",
        "state_ref": decision["state_ref"],
        "control_decision_id": decision["decision_id"],
        "packet_class": kind,
        "strategy": decision["strategy"],
        "objective": context["mission"],
        "assignment": {
            "domain": context["routing"]["domain"],
            "agent": context["routing"]["agent"],
            "secondary_domains": context["routing"]["secondary_domains"],
        },
        "mode": context["routing"]["mode"],
        "effort": context["routing"]["effort"],
        "timebox_minutes": timebox(kind, context["routing"]["mode"]),
        "action_policy": policy,
        "allowed_actions": actions,
        "blocked_actions": blocked_actions,
        "forbidden_actions": unique(
            [
                "scope_expansion",
                "policy_mutation",
                "persistent_memory_write",
                "raw_transcript_forwarding",
                "unbounded_delegation",
                *( ["runtime_action"] if kind == "stop" else [] ),
            ]
        ),
        "inputs": unique(
            [
                decision["state_ref"],
                state["task"]["acceptance_contract_ref"],
                *context["evidence_refs"],
            ]
        ),
        "permissions": {
            "required_permission_refs": state["user"]["permissions_required"],
            "required_confirmation_refs": state["user"]["confirmations_required"],
        },
        "expected_outputs": OUTPUT_BY_CLASS[kind],
        "evidence_required": acceptance_evidence,
        "stop_conditions": unique(
            [
                *(f"Control reason: {reason}" for reason in decision["reason_codes"]),
                "Stop at this packet boundary and preserve produced artifacts.",
                "Return the exact blocker instead of restarting or expanding scope.",
            ]
        ),
        "resume": {
            "checkpoint_ref": workspace["workspace_id"],
            "prior_packet_ref": prior_packet_ref,
            "artifact_refs": workspace["evidence_refs"],
            "last_completed_step": last_step,
            "retry_count": retry_count,
            "max_retries": original_repairs,
        },
    }
    schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    checker = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(checker.iter_errors(packet), key=lambda item: tuple(str(part) for part in item.absolute_path))
    ]
    banned = find_banned(packet)
    if errors or banned:
        raise ValueError(
            "invalid runtime operation packet: "
            + "; ".join([*errors, *(f"banned key: {item}" for item in banned)])
        )
    return packet


def packet_summary(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "packet_class": packet["packet_class"],
        "strategy": packet["strategy"],
        "allowed_actions": packet["allowed_actions"],
        "blocked_actions": packet["blocked_actions"],
        "retry_count": packet["resume"]["retry_count"],
        "max_retries": packet["resume"]["max_retries"],
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        cycle_case_path = root / case["brain_cycle_fixture"]
        cycle_case = load_mapping(cycle_case_path)
        source = root / cycle_case["interpreter_fixture"]
        try:
            initial = compile_validated(root, materialize_fixture(source, load_mapping(source)))
            cycle = advance(root, initial, expand_events(cycle_case.get("events", [])))
            actual = packet_summary(compile_packet(root, cycle, case.get("prior_packet_ref")))
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: class={actual['packet_class']}, actions={actual['allowed_actions']}")
    if not paths or failures:
        print(f"Runtime operation fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Runtime operation fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--cycle-result", type=pathlib.Path)
    parser.add_argument("--prior-packet-ref")
    parser.add_argument("--fixtures", action="store_true")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            if args.cycle_result:
                raise ValueError("--fixtures cannot be combined with --cycle-result")
            return run_fixtures(root)
        if not args.cycle_result:
            raise ValueError("provide --cycle-result or use --fixtures")
        path = args.cycle_result if args.cycle_result.is_absolute() else root / args.cycle_result
        packet = compile_packet(root, load_mapping(path), args.prior_packet_ref)
        if args.format == "json":
            print(json.dumps(packet, indent=2, ensure_ascii=True))
        else:
            print(yaml.safe_dump(packet, sort_keys=False, allow_unicode=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
