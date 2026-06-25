"""Compile typed end-to-end adapter evidence from a normalized runtime capture."""

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

from compile_acceptance_contract import compile_bundle  # noqa: E402
from compile_brain_workspace import bundle_validator, compile_validated, find_banned  # noqa: E402
from compile_runtime_recovery import compile_recovery  # noqa: E402
from compile_runtime_session import compile_session, session_validator, validation_errors  # noqa: E402
from ingest_runtime_observation import fixture_capture, ingest, validator as runtime_validator  # noqa: E402
from retrieve_memory import fixture_store  # noqa: E402
from validate_interpreter import load_mapping  # noqa: E402


SCHEMA = pathlib.Path("schemas/runtime/runtime-adapter-evidence-bundle.schema.json")
CAPTURE_SCHEMA = pathlib.Path("schemas/runtime/execution-capture.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/runtime-adapter-evidence")
UNKNOWN_VALUES = {"", "unknown", "not_captured", "not recorded", "not_recorded"}


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


def validator(root: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema,
        registry=schema_registry(root),
        format_checker=FormatChecker(),
    )


def require_exact_metadata(run: dict[str, str], allow_unknown_model: bool) -> list[str]:
    errors: list[str] = []
    if not allow_unknown_model and run["model"].strip().lower() in UNKNOWN_VALUES:
        errors.append("exact model is required for adapter evidence")
    for key in ("runtime", "adapter_version", "prompt_version"):
        if run[key].strip().lower() in UNKNOWN_VALUES:
            errors.append(f"{key} is required for adapter evidence")
    return errors


def outcome_status(observation_bundle: dict[str, Any]) -> str:
    event = observation_bundle["observations"][0]
    effect = event["effect"]
    recovery = observation_bundle["recovery"]
    invocation_status = observation_bundle["source_capture"]["invocation_status"]
    if effect == "acceptance_evidence":
        return "pass"
    if effect == "progress":
        return "partial"
    if effect == "failure":
        return "fail"
    if effect == "unsafe":
        return "unsafe"
    if effect == "blocked":
        if recovery["required"] and invocation_status == "timeout":
            return "timeout"
        return "blocked"
    return "no_change"


def compile_evidence(
    root: pathlib.Path,
    workspace: dict[str, Any],
    session: dict[str, Any],
    projection: dict[str, Any],
    capture: dict[str, Any],
    run: dict[str, str],
    capture_trusted: bool,
    allow_unknown_model: bool = False,
) -> dict[str, Any]:
    issues = validation_errors(bundle_validator(root), workspace)
    issues.extend(validation_errors(session_validator(root), session))
    issues.extend(validation_errors(projection_validator(root), projection))
    issues.extend(validation_errors(runtime_validator(root, CAPTURE_SCHEMA), capture))
    issues.extend(require_exact_metadata(run, allow_unknown_model))
    if issues:
        raise ValueError("invalid adapter evidence input: " + "; ".join(issues))

    observation_bundle = ingest(root, session, projection, capture, capture_trusted=capture_trusted)
    recovery_result = None
    if observation_bundle["recovery"]["required"]:
        recovery_result = compile_recovery(root, workspace, session, projection, observation_bundle)

    event = observation_bundle["observations"][0]
    verification = event["verification"]
    result = {
        "schema_version": "runtime-adapter-evidence-bundle.v0",
        "evidence_id": f"runtime-adapter-evidence.{capture['capture_id']}",
        "recorded_at": capture["captured_at"],
        "run": {
            "adapter": "kilo",
            "runtime": run["runtime"],
            "model": run["model"],
            "mode": run["mode"],
            "effort": run["effort"],
            "adapter_version": run["adapter_version"],
            "prompt_version": run["prompt_version"],
        },
        "lineage": {
            "session_id": session["session_id"],
            "packet_id": session["operation_packet"]["packet_id"],
            "projection_id": projection["projection_id"],
            "capture_id": capture["capture_id"],
        },
        "projection": {
            "projection_status": projection["projection_status"],
            "agent_id": projection["agent"]["agent_id"],
            "agent_path": projection["agent"]["path"],
            "content_sha256": projection["agent"]["content_sha256"],
            "invocation_output_format": projection["invocation"]["output_format"],
            "invocation_executed": projection["invocation"]["executed"],
            "unsupported_controls": projection["unsupported_controls"],
        },
        "capture": copy.deepcopy(observation_bundle["source_capture"]),
        "observation_bundle": observation_bundle,
        "recovery_result": recovery_result,
        "outcome": {
            "status": outcome_status(observation_bundle),
            "observation_effect": event["effect"],
            "verification_status": verification["status"],
            "acceptance_status": verification["acceptance_status"],
            "accepted": verification["status"] == "pass" and verification["acceptance_status"] == "complete",
            "recovery_required": observation_bundle["recovery"]["required"],
            "recovery_reason": observation_bundle["recovery"]["reason"],
            "evidence_refs": event["evidence_refs"],
        },
        "privacy": copy.deepcopy(observation_bundle["privacy"]),
    }
    output_issues = validation_errors(validator(root), result)
    banned = find_banned(result)
    if output_issues or banned:
        details = [*output_issues, *(f"banned adapter evidence key: {item}" for item in banned)]
        raise ValueError("invalid runtime adapter evidence bundle: " + "; ".join(details))
    return result


def summary(result: dict[str, Any]) -> dict[str, Any]:
    recovery = result["recovery_result"]
    return {
        "status": result["outcome"]["status"],
        "capture_trust": result["capture"]["capture_trust"],
        "observation_effect": result["outcome"]["observation_effect"],
        "accepted": result["outcome"]["accepted"],
        "recovery_required": result["outcome"]["recovery_required"],
        "recovery_reason": result["outcome"]["recovery_reason"],
        "recovery_packet_class": recovery["recovery_session"]["operation_packet"]["packet_class"] if recovery else None,
        "projection_status": result["projection"]["projection_status"],
        "raw_payload_embedded": result["privacy"]["raw_event_payload_embedded"],
        "model_output_embedded": result["privacy"]["model_output_embedded"],
    }


def fixture_result(root: pathlib.Path, case: dict[str, Any]) -> dict[str, Any]:
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
    projection.update(case.get("projection_override", {}))
    capture = fixture_capture(observation_case, session, projection)
    return compile_evidence(
        root,
        workspace,
        session,
        projection,
        capture,
        case["run"],
        capture_trusted=observation_case.get("trusted_capture", True),
        allow_unknown_model=case.get("allow_unknown_model", False),
    )


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        try:
            actual = summary(fixture_result(root, case))
            if "expected_error" in case:
                raise ValueError(f"expected error containing {case['expected_error']!r}, but evidence compilation passed")
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
            print(f"PASS {path.as_posix()}: status={actual['status']}, recovery={actual['recovery_reason']}")
    if not paths or failures:
        print(f"Runtime adapter evidence fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Runtime adapter evidence fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--workspace", type=pathlib.Path)
    parser.add_argument("--session", type=pathlib.Path)
    parser.add_argument("--projection", type=pathlib.Path)
    parser.add_argument("--capture", type=pathlib.Path)
    parser.add_argument("--attest-runtime-capture", action="store_true")
    parser.add_argument("--runtime", default="Kilo Code")
    parser.add_argument("--model", default="unknown")
    parser.add_argument("--mode", choices=("fast", "standard", "unknown"), default="unknown")
    parser.add_argument("--effort", choices=("low", "medium", "high", "extra-high", "max", "ultra", "unknown"), default="unknown")
    parser.add_argument("--adapter-version", default="unknown")
    parser.add_argument("--prompt-version", default="unknown")
    parser.add_argument("--allow-unknown-model", action="store_true")
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
        if not all((args.workspace, args.session, args.projection, args.capture)):
            raise ValueError("provide --workspace, --session, --projection, and --capture, or use --fixtures")
        result = compile_evidence(
            root,
            load_mapping(resolve(root, args.workspace)),
            load_mapping(resolve(root, args.session)),
            load_mapping(resolve(root, args.projection)),
            load_mapping(resolve(root, args.capture)),
            {
                "runtime": args.runtime,
                "model": args.model,
                "mode": args.mode,
                "effort": args.effort,
                "adapter_version": args.adapter_version,
                "prompt_version": args.prompt_version,
            },
            capture_trusted=args.attest_runtime_capture,
            allow_unknown_model=args.allow_unknown_model,
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
