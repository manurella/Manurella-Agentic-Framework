"""Compile a runtime recovery session from a typed execution observation."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT_ADAPTER = pathlib.Path(__file__).resolve().parents[1] / "adapters" / "kilo"
if str(ROOT_ADAPTER) not in sys.path:
    sys.path.insert(0, str(ROOT_ADAPTER))

from project_runtime_session import project_session, projection_validator  # noqa: E402

from advance_brain_cycle import advance  # noqa: E402
from compile_acceptance_contract import compile_bundle  # noqa: E402
from compile_brain_workspace import compile_validated, find_banned  # noqa: E402
from compile_runtime_operation import compile_packet, packet_summary  # noqa: E402
from compile_runtime_session import (  # noqa: E402
    UNENFORCED_CONTROLS,
    compile_session,
    execution_status,
    session_validator,
    validation_errors,
)
from ingest_runtime_observation import fixture_capture, ingest  # noqa: E402
from retrieve_memory import fixture_store  # noqa: E402
from validate_interpreter import load_mapping  # noqa: E402


SCHEMA = pathlib.Path("schemas/runtime/runtime-recovery-result.schema.json")
OBSERVATION_SCHEMA = pathlib.Path("schemas/runtime/execution-observation-bundle.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/runtime-recovery")
RECOVERABLE_STATUSES = {"timeout", "cancelled", "unknown"}


def schema_registry(root: pathlib.Path) -> Registry:
    registry = Registry()
    paths = [
        *sorted((root / "schemas" / "runtime").glob("*.json")),
        *sorted((root / "schemas" / "brain").glob("*.json")),
        *sorted((root / "schemas" / "memory").glob("*.json")),
        *sorted((root / "schemas" / "adapters").glob("*.json")),
    ]
    for path in paths:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(schema["$id"], resource)
        registry = registry.with_resource(path.name, resource)
    return registry


def validator(root: pathlib.Path, relative: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / relative).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema,
        registry=schema_registry(root),
        format_checker=FormatChecker(),
    )


def lineage_errors(
    root: pathlib.Path,
    prior_session: dict[str, Any],
    prior_projection: dict[str, Any],
    observation_bundle: dict[str, Any],
) -> list[str]:
    operation = prior_session["operation_packet"]
    expected = {
        "session_id": prior_session["session_id"],
        "packet_id": operation["packet_id"],
        "projection_id": prior_projection["projection_id"],
    }
    errors = [
        f"observation lineage {key} mismatch: expected {value!r}, got {observation_bundle['lineage'].get(key)!r}"
        for key, value in expected.items()
        if observation_bundle["lineage"].get(key) != value
    ]
    if prior_projection != project_session(root, prior_session):
        errors.append("prior projection does not match the deterministic session projection")
    if prior_projection["source_session_id"] != prior_session["session_id"]:
        errors.append("prior projection source_session_id does not match prior session")
    if prior_projection["source_packet_id"] != operation["packet_id"]:
        errors.append("prior projection source_packet_id does not match prior packet")
    recovery = observation_bundle["recovery"]
    if recovery["prior_packet_ref"] != operation["packet_id"]:
        errors.append("recovery prior_packet_ref does not match prior packet")
    if recovery["checkpoint_ref"] != operation["resume"]["checkpoint_ref"]:
        errors.append("recovery checkpoint_ref does not match prior packet checkpoint")
    return errors


def recovery_errors(observation_bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    recovery = observation_bundle["recovery"]
    source = observation_bundle["source_capture"]
    observations = observation_bundle["observations"]
    if not recovery["required"]:
        errors.append("observation bundle does not require recovery")
    if recovery["reason"] == "none":
        errors.append("recoverable observation requires a non-none recovery reason")
    if source["capture_trust"] != "trusted_runtime":
        errors.append("runtime recovery requires adapter-attested capture trust")
    if source["invocation_status"] not in RECOVERABLE_STATUSES:
        errors.append("runtime recovery requires timeout, cancellation, or unknown invocation status")
    for event in observations:
        if event["trust"] != "trusted_runtime":
            errors.append(f"recovery observation {event['observation_id']!r} is not trusted_runtime")
        if event["effect"] != "blocked":
            errors.append(f"recovery observation {event['observation_id']!r} is not blocked")
    return errors


def compile_recovery_session(
    root: pathlib.Path,
    prior_session: dict[str, Any],
    cycle: dict[str, Any],
    observation_bundle: dict[str, Any],
    recovered_at: str,
) -> dict[str, Any]:
    operation = compile_packet(
        root,
        cycle,
        prior_packet_ref=prior_session["operation_packet"]["packet_id"],
    )
    if operation["packet_class"] != "recovery":
        raise ValueError(f"Brain cycle did not compile to a recovery packet: {operation['packet_class']}")
    revised = cycle["revised_workspace_bundle"]
    decision = cycle["control_decision"]
    session = {
        "schema_version": "runtime-session-bundle.v0",
        "session_id": f"{prior_session['session_id']}.recovery.{observation_bundle['source_capture']['capture_id']}",
        "compiled_at": recovered_at,
        "source": copy.deepcopy(prior_session["source"]),
        "lineage": {
            "task_frame_ref": prior_session["lineage"]["task_frame_ref"],
            "acceptance_contract_ref": prior_session["lineage"]["acceptance_contract_ref"],
            "routing_decision_id": prior_session["lineage"]["routing_decision_id"],
            "brain_state_ref": decision["state_ref"],
            "control_decision_id": decision["decision_id"],
        },
        "execution": {
            "status": execution_status(revised, operation),
            "packet_class": operation["packet_class"],
            "selected_domain": operation["assignment"]["domain"],
            "selected_agent": operation["assignment"]["agent"],
            "memory_scope": copy.deepcopy(prior_session["execution"]["memory_scope"]),
            "selected_memory_count": prior_session["execution"]["selected_memory_count"],
        },
        "memory_context": copy.deepcopy(prior_session["memory_context"]),
        "operation_packet": operation,
        "adapter_boundary": {
            "target": "runtime_neutral",
            "status": "pending_projection",
            "unenforced_controls": UNENFORCED_CONTROLS,
        },
    }
    issues = validation_errors(session_validator(root), session)
    banned = find_banned(session)
    if issues or banned:
        details = [*issues, *(f"banned recovery session key: {item}" for item in banned)]
        raise ValueError("invalid recovery runtime session: " + "; ".join(details))
    return session


def compile_recovery(
    root: pathlib.Path,
    workspace: dict[str, Any],
    prior_session: dict[str, Any],
    prior_projection: dict[str, Any],
    observation_bundle: dict[str, Any],
    recovered_at: str | None = None,
) -> dict[str, Any]:
    recovered = recovered_at or observation_bundle["captured_at"]
    issues = validation_errors(session_validator(root), prior_session)
    issues.extend(validation_errors(projection_validator(root), prior_projection))
    issues.extend(validation_errors(validator(root, OBSERVATION_SCHEMA), observation_bundle))
    if issues:
        raise ValueError("invalid recovery input: " + "; ".join(issues))
    semantic = [
        *lineage_errors(root, prior_session, prior_projection, observation_bundle),
        *recovery_errors(observation_bundle),
    ]
    if semantic:
        raise ValueError("invalid runtime recovery semantics: " + "; ".join(semantic))

    cycle = advance(root, workspace, observation_bundle["observations"])
    decision = cycle["control_decision"]
    if decision["disposition"] != "stop_blocked":
        raise ValueError(f"recovery observation did not stop as blocked: {decision['disposition']}")
    recovery_session = compile_recovery_session(root, prior_session, cycle, observation_bundle, recovered)
    projection = project_session(root, recovery_session)
    result = {
        "schema_version": "runtime-recovery-result.v0",
        "recovery_id": f"runtime-recovery.{observation_bundle['source_capture']['capture_id']}",
        "recovered_at": recovered,
        "prior": {
            "session_id": prior_session["session_id"],
            "packet_id": prior_session["operation_packet"]["packet_id"],
            "projection_id": prior_projection["projection_id"],
        },
        "observation_bundle_id": observation_bundle["bundle_id"],
        "recovery_reason": observation_bundle["recovery"]["reason"],
        "privacy": copy.deepcopy(observation_bundle["privacy"]),
        "brain_cycle_result": cycle,
        "recovery_session": recovery_session,
        "adapter_projection": projection,
    }
    output_issues = validation_errors(validator(root, SCHEMA), result)
    banned = find_banned(result)
    if output_issues or banned:
        details = [*output_issues, *(f"banned recovery result key: {item}" for item in banned)]
        raise ValueError("invalid runtime recovery result: " + "; ".join(details))
    return result


def summary(result: dict[str, Any]) -> dict[str, Any]:
    session = result["recovery_session"]
    projection = result["adapter_projection"]
    return {
        "recovery_reason": result["recovery_reason"],
        "disposition": result["brain_cycle_result"]["control_decision"]["disposition"],
        "next_operation": result["brain_cycle_result"]["control_decision"]["next_operation"],
        "packet_class": session["operation_packet"]["packet_class"],
        "execution_status": session["execution"]["status"],
        "projection_status": projection["projection_status"],
        "allowed_actions": session["operation_packet"]["allowed_actions"],
        "blocked_actions": session["operation_packet"]["blocked_actions"],
        "prior_packet_ref": session["operation_packet"]["resume"]["prior_packet_ref"],
        "raw_payload_embedded": result["privacy"]["raw_event_payload_embedded"],
        "model_output_embedded": result["privacy"]["model_output_embedded"],
    }


def fixture_result(root: pathlib.Path, case: dict[str, Any], path: pathlib.Path) -> dict[str, Any]:
    observation_case_path = root / case["execution_observation_fixture"]
    observation_case = load_mapping(observation_case_path)
    runtime_case_path = root / observation_case["runtime_session_fixture"]
    runtime_case = load_mapping(runtime_case_path)
    source_case = load_mapping(root / runtime_case["source_fixture"])
    interpreter, interpreter_errors = compile_bundle(root, source_case["envelope"], "en-US")
    if interpreter_errors or interpreter is None:
        raise ValueError("Interpreter compilation failed: " + "; ".join(interpreter_errors))
    workspace = compile_validated(root, interpreter)
    session = compile_session(
        root,
        source_case["envelope"],
        fixture_store(root, runtime_case, runtime_case_path),
        "2026-06-22T10:00:00Z",
    )
    projection = project_session(root, session)
    capture = fixture_capture(observation_case, session, projection)
    observation_bundle = ingest(
        root,
        session,
        projection,
        capture,
        capture_trusted=observation_case.get("trusted_capture", True),
    )
    for key, value in case.get("observation_override", {}).items():
        observation_bundle[key] = value
    if case.get("tamper_lineage"):
        observation_bundle["lineage"]["packet_id"] = "packet.tampered"
    return compile_recovery(root, workspace, session, projection, observation_bundle)


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        try:
            result = fixture_result(root, case, path)
            actual = summary(result)
            if "expected_error" in case:
                raise ValueError(f"expected error containing {case['expected_error']!r}, but recovery passed")
        except ValueError as exc:
            expected_error = case.get("expected_error")
            if expected_error and expected_error in str(exc):
                print(f"PASS {path.as_posix()}: rejected={expected_error}")
                continue
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: class={actual['packet_class']}, projection={actual['projection_status']}")
    if not paths or failures:
        print(f"Runtime recovery fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Runtime recovery fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--workspace", type=pathlib.Path)
    parser.add_argument("--session", type=pathlib.Path)
    parser.add_argument("--projection", type=pathlib.Path)
    parser.add_argument("--observation-bundle", type=pathlib.Path)
    parser.add_argument("--recovered-at")
    parser.add_argument("--fixtures", action="store_true")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    return parser.parse_args(argv)


def resolve(root: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    return path if path.is_absolute() else root / path


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            return run_fixtures(root)
        if not all((args.workspace, args.session, args.projection, args.observation_bundle)):
            raise ValueError("provide --workspace, --session, --projection, and --observation-bundle, or use --fixtures")
        result = compile_recovery(
            root,
            load_mapping(resolve(root, args.workspace)),
            load_mapping(resolve(root, args.session)),
            load_mapping(resolve(root, args.projection)),
            load_mapping(resolve(root, args.observation_bundle)),
            args.recovered_at,
        )
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
