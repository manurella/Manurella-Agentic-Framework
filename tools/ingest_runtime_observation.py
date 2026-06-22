"""Ingest a normalized runtime capture into privacy-bounded Brain observations."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime
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

from compile_runtime_session import compile_session, session_validator, validation_errors  # noqa: E402
from retrieve_memory import fixture_store  # noqa: E402
from validate_interpreter import load_mapping  # noqa: E402


CAPTURE_SCHEMA = pathlib.Path("schemas/runtime/execution-capture.schema.json")
BUNDLE_SCHEMA = pathlib.Path("schemas/runtime/execution-observation-bundle.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/runtime-execution-observation")
NO_VERIFICATION = {"status": "not_run", "acceptance_status": "not_evaluated", "check_ids": []}


def schema_registry(root: pathlib.Path) -> Registry:
    registry = Registry()
    paths = [
        *sorted((root / "schemas" / "runtime").glob("*.json")),
        *sorted((root / "schemas" / "brain").glob("*.json")),
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
    return Draft202012Validator(schema, registry=schema_registry(root), format_checker=FormatChecker())


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def semantic_capture_errors(capture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    invocation = capture["invocation"]
    status = invocation["status"]
    timeout = invocation["timeout_status"]
    exit_code = invocation["exit_code"]
    verification = capture["verification"]
    stream = capture["stream"]
    model = capture["model_output"]

    if parse_time(invocation["ended_at"]) < parse_time(invocation["started_at"]):
        errors.append("invocation ended_at precedes started_at")
    if parse_time(capture["captured_at"]) < parse_time(invocation["ended_at"]):
        errors.append("captured_at precedes invocation ended_at")

    allowed_timeouts = {
        "completed": {"none"},
        "failed": {"none"},
        "timeout": {"upstream_idle_timeout", "unknown"},
        "cancelled": {"user_stopped", "unknown"},
        "policy_blocked": {"none"},
        "unknown": {"unknown"},
    }
    if timeout not in allowed_timeouts[status]:
        errors.append(f"invocation status {status!r} is inconsistent with timeout_status {timeout!r}")
    if status == "completed" and exit_code != 0:
        errors.append("completed invocation requires exit_code 0")
    if status == "failed" and (exit_code is None or exit_code == 0):
        errors.append("failed invocation requires a nonzero exit_code")

    expected_verification = {
        "not_run": ({"not_evaluated"}, False),
        "pass": ({"partial", "complete"}, True),
        "fail": ({"failed"}, True),
        "partial": ({"partial"}, True),
    }
    accepted, require_checks = expected_verification[verification["status"]]
    if verification["acceptance_status"] not in accepted:
        errors.append("verification status and acceptance_status are inconsistent")
    if require_checks != bool(verification["check_ids"]):
        errors.append("verification check_ids do not match verification status")
    if status != "completed" and verification != NO_VERIFICATION:
        errors.append("non-completed invocation cannot claim verification")

    if stream["output_format"] == "not_available":
        if stream["event_count"] != 0 or stream["raw_events_sha256"] is not None:
            errors.append("unavailable stream requires zero events and no digest")
    elif stream["raw_events_sha256"] is None:
        errors.append("raw_json_events stream requires a digest")
    if model["present"] != (model["sha256"] is not None):
        errors.append("model output presence and digest are inconsistent")
    return errors


def lineage_errors(
    root: pathlib.Path,
    session: dict[str, Any],
    projection: dict[str, Any],
    capture: dict[str, Any],
) -> list[str]:
    expected = {
        "session_id": session["session_id"],
        "packet_id": session["operation_packet"]["packet_id"],
        "projection_id": projection["projection_id"],
    }
    errors = [
        f"lineage {key} mismatch: expected {value!r}, got {capture['lineage'].get(key)!r}"
        for key, value in expected.items()
        if capture["lineage"].get(key) != value
    ]
    if projection != project_session(root, session):
        errors.append("projection does not match the deterministic session projection")
    if projection["source_session_id"] != session["session_id"]:
        errors.append("projection source_session_id does not match session")
    if projection["source_packet_id"] != session["operation_packet"]["packet_id"]:
        errors.append("projection source_packet_id does not match session packet")
    if projection["projection_status"] != "ready_for_interactive_cli":
        errors.append("execution capture requires a projection ready for interactive CLI")
    if capture["adapter"] != "kilo":
        errors.append("Kilo projection capture must use adapter 'kilo'")
    return errors


def observation_semantics(capture: dict[str, Any]) -> tuple[str, str, str, str | None]:
    status = capture["invocation"]["status"]
    verification = capture["verification"]
    artifacts = capture["observed_artifact_refs"]
    if status == "policy_blocked":
        return "runtime_event", "unsafe", "Runtime execution was blocked by the active permission boundary.", "unsafe.permission-boundary"
    if status == "timeout":
        return "runtime_event", "blocked", "Runtime invocation ended before acceptance after an upstream idle timeout.", "blocked.upstream-idle"
    if status == "cancelled":
        return "runtime_event", "blocked", "Runtime invocation was stopped before the projected operation was accepted.", "blocked.user-stopped"
    if status == "unknown":
        return "runtime_event", "blocked", "Runtime invocation ended with an unknown terminal status.", "blocked.runtime-status-unknown"
    if status == "failed":
        return "runtime_event", "failure", "Runtime invocation failed before the projected operation was accepted.", "failure.runtime-invocation"
    if verification["status"] == "fail":
        return "verification_result", "failure", "Runtime verification failed for the projected operation.", "failure.runtime-verification"
    if verification["status"] == "pass" and verification["acceptance_status"] == "complete":
        return "verification_result", "acceptance_evidence", "Runtime verification completed all acceptance checks for the projected operation.", None
    if verification["status"] in {"pass", "partial"}:
        return "verification_result", "progress", "Runtime verification produced bounded evidence for the projected operation.", None
    if artifacts:
        return "artifact_change", "progress", "Runtime completed the projected operation and observed bounded artifact evidence.", None
    return "runtime_event", "no_change", "Runtime completed without verified progress evidence.", None


def recovery_semantics(capture: dict[str, Any]) -> tuple[bool, str]:
    status = capture["invocation"]["status"]
    timeout = capture["invocation"]["timeout_status"]
    if status == "timeout" and timeout == "upstream_idle_timeout":
        return True, "upstream_idle_timeout"
    if status == "cancelled" and timeout == "user_stopped":
        return True, "user_stopped"
    if status in {"timeout", "cancelled", "unknown"}:
        return True, "runtime_status_unknown"
    return False, "none"


def ingest(
    root: pathlib.Path,
    session: dict[str, Any],
    projection: dict[str, Any],
    capture: dict[str, Any],
    capture_trusted: bool = False,
) -> dict[str, Any]:
    issues = validation_errors(session_validator(root), session)
    issues.extend(validation_errors(projection_validator(root), projection))
    issues.extend(validation_errors(validator(root, CAPTURE_SCHEMA), capture))
    if issues:
        raise ValueError("invalid execution-observation input: " + "; ".join(issues))
    semantic = [*semantic_capture_errors(capture), *lineage_errors(root, session, projection, capture)]
    if semantic:
        raise ValueError("invalid execution capture semantics: " + "; ".join(semantic))

    kind, effect, statement, repeat_suffix = observation_semantics(capture)
    recovery_required, recovery_reason = recovery_semantics(capture)
    event_verification = copy.deepcopy(capture["verification"])
    event_evidence = list(capture["observed_artifact_refs"])
    preserved_artifacts = list(capture["observed_artifact_refs"])
    if not capture_trusted:
        kind = "runtime_event"
        effect = "no_change"
        statement = "An unattested runtime capture was ingested for review without execution authority."
        repeat_suffix = None
        event_verification = copy.deepcopy(NO_VERIFICATION)
        event_evidence = []
        recovery_required, recovery_reason = False, "none"
        preserved_artifacts = []
    operation = session["operation_packet"]
    source_ref = f"runtime://{capture['adapter']}/capture/{capture['capture_id']}"
    observation = {
        "schema_version": "observation-event.v0",
        "observation_id": f"observation.{capture['capture_id']}",
        "observed_at": capture["captured_at"],
        "kind": kind,
        "source_ref": source_ref,
        "trust": "trusted_runtime" if capture_trusted else "model_inferred",
        "effect": effect,
        "statement": statement,
        "evidence_refs": event_evidence,
        "repeat_key": f"{repeat_suffix}.{operation['packet_id']}" if repeat_suffix else None,
        "verification": event_verification,
    }
    bundle = {
        "schema_version": "execution-observation-bundle.v0",
        "bundle_id": f"execution-observation.{capture['capture_id']}",
        "captured_at": capture["captured_at"],
        "adapter": capture["adapter"],
        "lineage": copy.deepcopy(capture["lineage"]),
        "source_capture": {
            "capture_id": capture["capture_id"],
            "capture_trust": "trusted_runtime" if capture_trusted else "unverified",
            "invocation_status": capture["invocation"]["status"],
            "timeout_status": capture["invocation"]["timeout_status"],
            "exit_code": capture["invocation"]["exit_code"],
            "event_count": capture["stream"]["event_count"],
            "raw_events_sha256": capture["stream"]["raw_events_sha256"],
            "model_output_sha256": capture["model_output"]["sha256"],
        },
        "privacy": {
            "raw_event_payload_embedded": False,
            "model_output_embedded": False,
            "digest_only": True,
        },
        "observations": [observation],
        "recovery": {
            "required": recovery_required,
            "reason": recovery_reason,
            "checkpoint_ref": operation["resume"]["checkpoint_ref"],
            "prior_packet_ref": operation["packet_id"],
            "preserved_artifact_refs": preserved_artifacts,
        },
    }
    output_issues = validation_errors(validator(root, BUNDLE_SCHEMA), bundle)
    banned_keys = {"raw_event_payload", "model_output_text", "tool_arguments", "tool_responses", "reasoning", "chain_of_thought"}
    stack: list[Any] = [bundle]
    present_keys: set[str] = set()
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            present_keys.update(str(key) for key in value)
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    banned = sorted(banned_keys & present_keys)
    if output_issues or banned:
        details = [*output_issues, *(f"banned observation field: {key}" for key in banned)]
        raise ValueError("invalid execution observation bundle: " + "; ".join(details))
    return bundle


def summary(bundle: dict[str, Any]) -> dict[str, Any]:
    event = bundle["observations"][0]
    return {
        "effect": event["effect"],
        "trust": event["trust"],
        "kind": event["kind"],
        "verification_status": event["verification"]["status"],
        "acceptance_status": event["verification"]["acceptance_status"],
        "evidence_count": len(event["evidence_refs"]),
        "recovery_required": bundle["recovery"]["required"],
        "recovery_reason": bundle["recovery"]["reason"],
        "raw_payload_embedded": bundle["privacy"]["raw_event_payload_embedded"],
        "model_output_embedded": bundle["privacy"]["model_output_embedded"],
    }


def fixture_capture(case: dict[str, Any], session: dict[str, Any], projection: dict[str, Any]) -> dict[str, Any]:
    capture = copy.deepcopy(case["capture"])
    capture["lineage"] = {
        "session_id": session["session_id"],
        "packet_id": session["operation_packet"]["packet_id"],
        "projection_id": projection["projection_id"],
    }
    capture["lineage"].update(case.get("lineage_override", {}))
    return capture


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        runtime_case_path = root / case["runtime_session_fixture"]
        runtime_case = load_mapping(runtime_case_path)
        source_case = load_mapping(root / runtime_case["source_fixture"])
        try:
            session = compile_session(root, source_case["envelope"], fixture_store(root, runtime_case, runtime_case_path), "2026-06-22T10:00:00Z")
            projection = project_session(root, session)
            projection.update(case.get("projection_override", {}))
            bundle = ingest(
                root,
                session,
                projection,
                fixture_capture(case, session, projection),
                capture_trusted=case.get("trusted_capture", True),
            )
            actual = summary(bundle)
            if "expected_error" in case:
                raise ValueError(f"expected error containing {case['expected_error']!r}, but ingestion passed")
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
            print(f"PASS {path.as_posix()}: effect={actual['effect']}, recovery={actual['recovery_reason']}")
    if not paths or failures:
        print(f"Runtime execution observation fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Runtime execution observation fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--session", type=pathlib.Path)
    parser.add_argument("--projection", type=pathlib.Path)
    parser.add_argument("--capture", type=pathlib.Path)
    parser.add_argument(
        "--attest-runtime-capture",
        action="store_true",
        help="Treat normalized lifecycle metadata as adapter-attested runtime evidence.",
    )
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def resolve(root: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    return path if path.is_absolute() else root / path


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            return run_fixtures(root)
        if not all((args.session, args.projection, args.capture)):
            raise ValueError("provide --session, --projection, and --capture, or use --fixtures")
        bundle = ingest(
            root,
            load_mapping(resolve(root, args.session)),
            load_mapping(resolve(root, args.projection)),
            load_mapping(resolve(root, args.capture)),
            capture_trusted=args.attest_runtime_capture,
        )
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
