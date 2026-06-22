"""Compile trusted task intake into one bounded runtime-neutral session bundle."""

from __future__ import annotations

import argparse
from functools import lru_cache
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from advance_brain_cycle import advance
from compile_acceptance_contract import compile_bundle
from compile_brain_workspace import compile_validated, find_banned
from compile_core_packet import compile_core_projection
from compile_runtime_operation import compile_packet
from evaluate_memory_proposal import DEFAULT_STORE, load_yaml
from retrieve_memory import RETRIEVABLE_TYPES, fixture_store, retrieval_packet
from validate_interpreter import load_mapping


SCHEMA = pathlib.Path("schemas/runtime/runtime-session-bundle.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/runtime-session")
UNENFORCED_CONTROLS = [
    "provider_execution",
    "model_selection",
    "native_effort",
    "token_accounting",
    "cost_accounting",
]


def schema_registry(root: pathlib.Path) -> Registry:
    registry = Registry()
    paths = [
        *sorted((root / "schemas" / "runtime").glob("*.json")),
        *sorted((root / "schemas" / "memory").glob("*.json")),
    ]
    for path in paths:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        resource = Resource.from_contents(schema)
        registry = registry.with_resource(schema["$id"], resource)
        registry = registry.with_resource(path.name, resource)
    return registry


@lru_cache(maxsize=4)
def session_validator(root: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    return Draft202012Validator(
        schema,
        registry=schema_registry(root),
        format_checker=FormatChecker(),
    )


def validation_errors(checker: Draft202012Validator, document: dict[str, Any]) -> list[str]:
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(checker.iter_errors(document), key=lambda item: tuple(str(part) for part in item.absolute_path))
    ]


def authenticated_principal(envelope: dict[str, Any]) -> str:
    principals = {
        item["source"].get("principal_ref")
        for item in envelope["items"]
        if item["kind"] == "user_instruction"
        and item["source"]["origin"] == "user"
        and item["authentication"]["status"] == "verified"
        and item["source"].get("principal_ref")
    }
    if len(principals) != 1:
        raise ValueError("runtime session requires exactly one authenticated user principal")
    return next(iter(principals))


def memory_scope(interpreter: dict[str, Any], routing: dict[str, Any]) -> dict[str, str | None]:
    identity = interpreter["task_frame"]["identity"]
    if identity["project_id"]:
        return {"kind": "project", "ref": identity["project_id"]}
    if routing["selected_domain"] != "core":
        return {"kind": "domain", "ref": f"dom.{routing['selected_domain']}"}
    return {"kind": "task", "ref": f"task://{identity['frame_id']}@{identity['version']}"}


def execution_status(workspace: dict[str, Any], packet: dict[str, Any]) -> str:
    if packet["packet_class"] == "stop":
        return "terminal"
    if workspace["brain_state"]["task"]["status"] == "blocked":
        return "blocked"
    return "ready_for_adapter"


def compile_session(
    root: pathlib.Path,
    envelope: dict[str, Any],
    store: dict[str, Any],
    compiled_at: str,
    locale: str = "en-US",
    max_memories: int = 8,
) -> dict[str, Any]:
    interpreter, interpreter_errors = compile_bundle(root, envelope, locale)
    if interpreter_errors or interpreter is None:
        raise ValueError("Interpreter compilation failed: " + "; ".join(interpreter_errors))
    principal_ref = authenticated_principal(envelope)
    routing = compile_core_projection(interpreter)
    workspace = compile_validated(root, interpreter)
    cycle = advance(root, workspace, [])
    operation = compile_packet(root, cycle)
    scope = memory_scope(interpreter, routing)
    memory = retrieval_packet(
        root,
        store,
        compiled_at,
        principal_ref,
        scope,
        sorted(RETRIEVABLE_TYPES),
        max_memories,
    )
    if memory["packet_id"] not in operation["inputs"]:
        operation["inputs"].append(memory["packet_id"])

    revised = cycle["revised_workspace_bundle"]
    decision = cycle["control_decision"]
    session = {
        "schema_version": "runtime-session-bundle.v0",
        "session_id": f"runtime-session.{envelope['envelope_id']}",
        "compiled_at": compiled_at,
        "source": {
            "envelope_id": envelope["envelope_id"],
            "session_ref": envelope.get("session_ref"),
            "received_at": envelope["received_at"],
            "principal_ref": principal_ref,
        },
        "lineage": {
            "task_frame_ref": routing["task_frame_ref"],
            "acceptance_contract_ref": routing["acceptance_contract_ref"],
            "routing_decision_id": routing["decision_id"],
            "brain_state_ref": decision["state_ref"],
            "control_decision_id": decision["decision_id"],
        },
        "execution": {
            "status": execution_status(revised, operation),
            "packet_class": operation["packet_class"],
            "selected_domain": routing["selected_domain"],
            "selected_agent": routing["selected_agent"],
            "memory_scope": scope,
            "selected_memory_count": len(memory["selected"]),
        },
        "memory_context": memory,
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
        details = [*issues, *(f"banned session key: {item}" for item in banned)]
        raise ValueError("invalid runtime session bundle: " + "; ".join(details))
    return session


def summary(session: dict[str, Any]) -> dict[str, Any]:
    operation = session["operation_packet"]
    execution = session["execution"]
    return {
        "status": execution["status"],
        "packet_class": execution["packet_class"],
        "strategy": operation["strategy"],
        "domain": execution["selected_domain"],
        "agent": execution["selected_agent"],
        "allowed_actions": operation["allowed_actions"],
        "blocked_actions": operation["blocked_actions"],
        "memory_scope": execution["memory_scope"],
        "selected_memory_count": execution["selected_memory_count"],
        "principal_ref": session["source"]["principal_ref"],
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        source = root / case["source_fixture"]
        source_case = load_mapping(source)
        try:
            session = compile_session(
                root,
                source_case["envelope"],
                fixture_store(root, case, path),
                "2026-06-22T10:00:00Z",
            )
            actual = summary(session)
            rendered = yaml.safe_dump(session, sort_keys=False, allow_unicode=False).lower()
            leaked = [text for text in case.get("forbidden_text", []) if text.lower() in rendered]
            if leaked:
                raise ValueError("forbidden text leaked into session: " + ", ".join(leaked))
            if "expected_error" in case:
                raise ValueError(f"expected error containing {case['expected_error']!r}, but compilation passed")
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
            print(f"PASS {path.as_posix()}: class={actual['packet_class']}, status={actual['status']}")
    if not paths or failures:
        print(f"Runtime session fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Runtime session fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--input", type=pathlib.Path)
    parser.add_argument("--store", type=pathlib.Path, default=DEFAULT_STORE)
    parser.add_argument("--compiled-at")
    parser.add_argument("--locale", default="en-US")
    parser.add_argument("--max-memories", type=int, default=8)
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            return run_fixtures(root)
        if not args.input or not args.compiled_at:
            raise ValueError("provide --input and --compiled-at, or use --fixtures")
        input_path = args.input if args.input.is_absolute() else root / args.input
        store_path = args.store if args.store.is_absolute() else root / args.store
        source = load_mapping(input_path)
        envelope = source.get("envelope", source)
        session = compile_session(
            root,
            envelope,
            load_yaml(store_path),
            args.compiled_at,
            args.locale,
            args.max_memories,
        )
        if args.format == "json":
            print(json.dumps(session, indent=2, ensure_ascii=True))
        else:
            print(yaml.safe_dump(session, sort_keys=False, allow_unicode=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
