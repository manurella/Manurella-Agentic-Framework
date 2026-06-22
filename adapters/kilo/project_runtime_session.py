"""Project a runtime session bundle into a strict, zero-execution Kilo artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from export_agents import (
    ExportError,
    KNOWN_DOMAINS,
    MODE_CONFIG,
    core_routable_agents,
    discover_agents,
    mode_steps,
    read_agent,
    same_domain_internal_agents,
    yaml_block,
)


ROOT_TOOLS = pathlib.Path(__file__).resolve().parents[2] / "tools"
if str(ROOT_TOOLS) not in sys.path:
    sys.path.insert(0, str(ROOT_TOOLS))

from compile_runtime_session import compile_session, session_validator, validation_errors  # noqa: E402
from retrieve_memory import fixture_store  # noqa: E402
from validate_interpreter import load_mapping  # noqa: E402


SCHEMA = pathlib.Path("schemas/adapters/kilo-session-projection.schema.json")
FIXTURE_DIR = pathlib.Path("evals/fixtures/kilo-session-projection")
RESEARCH_REF = "research/synthesis/kilo-runtime-projection-synthesis.md"
UNSUPPORTED = [
    "direct_packet_ingestion",
    "native_effort_mapping",
    "stable_json_result_schema",
    "autonomous_permission_semantics",
    "session_resume_semantics",
    "timeout_exit_semantics",
]


def projection_validator(root: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def source_agent(root: pathlib.Path, domain: str, agent_id: str) -> dict[str, Any]:
    path = root / "domains" / domain / "agents" / f"{agent_id}.md"
    try:
        agent, _ = read_agent(path)
    except ExportError as exc:
        raise ValueError(str(exc)) from exc
    return agent


def delegation_targets(root: pathlib.Path, domain: str) -> list[str]:
    try:
        records = discover_agents(root, sorted(KNOWN_DOMAINS))
    except ExportError as exc:
        raise ValueError(str(exc)) from exc
    agents = [record[1] for record in records]
    if domain == "core":
        return core_routable_agents(agents)
    return same_domain_internal_agents(agents, domain)


def strict_permissions(root: pathlib.Path, session: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    operation = session["operation_packet"]
    allowed = set(operation["allowed_actions"])
    permission: dict[str, Any] = {
        "read": "allow" if "read" in allowed else "deny",
        "glob": "allow" if "read" in allowed else "deny",
        "grep": "allow" if "read" in allowed else "deny",
        "edit": "deny",
        "bash": "deny",
        "webfetch": "allow" if "web" in allowed else "deny",
        "websearch": "allow" if "web" in allowed else "deny",
        "task": "deny",
        "external_directory": "deny",
        "todowrite": "deny",
        "todoread": "deny",
    }
    if "delegate" in allowed:
        task: dict[str, str] = {"*": "deny"}
        for target in delegation_targets(root, operation["assignment"]["domain"]):
            task[target] = "allow"
        permission["task"] = task
    narrowed = [action for action in operation["allowed_actions"] if action in {"edit", "shell", "browser"}]
    return permission, narrowed


def memory_lines(session: dict[str, Any]) -> list[str]:
    selected = session["memory_context"]["selected"]
    if not selected:
        return ["- None selected."]
    return [
        f"- [{item['memory_ref']}] {item['claim']['statement']} (evidence: {item['evidence_status']})"
        for item in selected
    ]


def bullet_lines(values: list[str]) -> list[str]:
    return [*(f"- {value}" for value in values)] if values else ["- None."]


def render_prompt(session: dict[str, Any]) -> str:
    operation = session["operation_packet"]
    lines = [
        "# Manurella Kilo Runtime Projection",
        "",
        "This file is generated from a validated Manurella Runtime Session Bundle.",
        "Do not claim that provider execution occurred before this Kilo run.",
        "Do not broaden permissions, restart the full workflow, or infer missing authority.",
        "",
        "## Session",
        "",
        f"- Session: `{session['session_id']}`",
        f"- Operation packet: `{operation['packet_id']}`",
        f"- Packet class: `{operation['packet_class']}`",
        f"- Mode: `{operation['mode']}`",
        f"- Effort policy: `{operation['effort']}` (prompt policy only; not native Kilo effort)",
        "",
        "## Objective",
        "",
        operation["objective"],
        "",
        "## Allowed Manurella Actions",
        "",
        *bullet_lines(operation["allowed_actions"]),
        "",
        "## Blocked Manurella Actions",
        "",
        *bullet_lines(operation["blocked_actions"]),
        "",
        "## Governed Memory",
        "",
        *memory_lines(session),
        "",
        "## Expected Outputs",
        "",
        *bullet_lines(operation["expected_outputs"]),
        "",
        "## Evidence Required",
        "",
        *bullet_lines(operation["evidence_required"]),
        "",
        "## Stop Conditions",
        "",
        *bullet_lines(operation["stop_conditions"]),
        "",
        "## Execution Rules",
        "",
        "- Respect the generated Kilo permission frontmatter as a hard ceiling.",
        "- If a required action is denied, return the exact blocker.",
        "- Treat JSON CLI output as raw events, not a stable Manurella result object.",
        "- Stop at this operation-packet boundary and preserve artifact references.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def projection_status(session: dict[str, Any]) -> str:
    if session["execution"]["status"] == "terminal":
        return "terminal_no_run"
    if session["execution"]["status"] == "blocked":
        return "blocked_response_only"
    return "ready_for_interactive_cli"


def project_session(root: pathlib.Path, session: dict[str, Any]) -> dict[str, Any]:
    session_issues = validation_errors(session_validator(root), session)
    if session_issues:
        raise ValueError("invalid runtime session bundle: " + "; ".join(session_issues))
    operation = session["operation_packet"]
    source = source_agent(root, operation["assignment"]["domain"], operation["assignment"]["agent"])
    permission, narrowed = strict_permissions(root, session)
    runtime = source.get("runtime") or {}
    kilo = runtime.get("kilo") or {}
    steps = mode_steps(source, kilo, operation["mode"])
    if steps is None:
        cap_key = "top_level_step_cap" if source["tier"] == "top_level" else "internal_step_cap"
        steps = MODE_CONFIG[operation["mode"]][cap_key] or 16
    identity = json.dumps(
        {"session": session["session_id"], "packet": operation["packet_id"]},
        sort_keys=True,
        separators=(",", ":"),
    )
    suffix = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    agent_id = f"manurella-runtime-{suffix}"
    status = projection_status(session)
    frontmatter = {
        "description": f"Strict Manurella runtime projection for {operation['packet_class']} packet {operation['packet_id']}.",
        "mode": "primary",
        "permission": permission,
        "steps": steps,
        "temperature": float(kilo.get("temperature", 0.2)),
        "hidden": False,
        "disable": status == "terminal_no_run",
    }
    prompt = render_prompt(session)
    markdown = yaml_block(frontmatter) + "\n" + prompt
    message = f"Execute Manurella projection {agent_id}. Stop at the packet boundary and report exact evidence or blockers."
    argv = [] if status == "terminal_no_run" else ["kilo", "run", "--agent", agent_id, "--format", "json", message]
    projection = {
        "schema_version": "kilo-session-projection.v0",
        "projection_id": f"kilo-projection.{suffix}",
        "source_session_id": session["session_id"],
        "source_packet_id": operation["packet_id"],
        "research_ref": RESEARCH_REF,
        "projection_status": status,
        "narrowed_actions": narrowed,
        "agent": {
            "agent_id": agent_id,
            "path": f".kilo/agents/{agent_id}.md",
            "content_sha256": f"sha256:{hashlib.sha256(markdown.encode('utf-8')).hexdigest()}",
            "frontmatter": frontmatter,
            "prompt_body": prompt,
            "agent_markdown": markdown,
        },
        "invocation": {
            "argv": argv,
            "output_format": "not_applicable" if status == "terminal_no_run" else "raw_json_events",
            "unattended_safe": False,
            "executed": False,
        },
        "unsupported_controls": UNSUPPORTED,
    }
    issues = validation_errors(projection_validator(root), projection)
    rendered = yaml.safe_dump(projection, sort_keys=False, allow_unicode=False)
    forbidden = ["--auto", "--dangerously-skip-permissions", " ask\n", ": ask\n"]
    violations = [item for item in forbidden if item in rendered]
    if issues or violations:
        details = [*issues, *(f"forbidden strict projection token: {item}" for item in violations)]
        raise ValueError("invalid Kilo projection: " + "; ".join(details))
    return projection


def summary(projection: dict[str, Any]) -> dict[str, Any]:
    permission = projection["agent"]["frontmatter"]["permission"]
    task = permission["task"]
    task_targets = sorted(key for key, value in task.items() if key != "*" and value == "allow") if isinstance(task, dict) else []
    return {
        "projection_status": projection["projection_status"],
        "steps": projection["agent"]["frontmatter"]["steps"],
        "read": permission["read"],
        "edit": permission["edit"],
        "bash": permission["bash"],
        "webfetch": permission["webfetch"],
        "websearch": permission["websearch"],
        "task_targets": task_targets,
        "narrowed_actions": projection["narrowed_actions"],
        "argv_has_auto": "--auto" in projection["invocation"]["argv"],
        "executed": projection["invocation"]["executed"],
    }


def run_fixtures(root: pathlib.Path) -> int:
    failures = 0
    paths = sorted((root / FIXTURE_DIR).glob("*.yaml"))
    for path in paths:
        case = load_mapping(path)
        runtime_case_path = root / case["runtime_session_fixture"]
        runtime_case = load_mapping(runtime_case_path)
        source_case = load_mapping(root / runtime_case["source_fixture"])
        try:
            session = compile_session(
                root,
                source_case["envelope"],
                fixture_store(root, runtime_case, runtime_case_path),
                "2026-06-22T10:00:00Z",
            )
            allowed_override = case.get("operation_allowed_actions")
            if allowed_override is not None:
                operation = session["operation_packet"]
                operation["allowed_actions"] = allowed_override
                operation["blocked_actions"] = [
                    action for action in operation["blocked_actions"] if action not in allowed_override
                ]
                for action in allowed_override:
                    operation["action_policy"][action] = "allow"
            projection = project_session(root, session)
            actual = summary(projection)
            rendered = projection["agent"]["agent_markdown"].lower()
            leaked = [item for item in case.get("forbidden_text", []) if item.lower() in rendered]
            if leaked:
                raise ValueError("forbidden text leaked into Kilo projection: " + ", ".join(leaked))
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if actual != case["expected"]:
            print(f"FAIL {path.as_posix()}: expected={case['expected']} actual={actual}", file=sys.stderr)
            failures += 1
        else:
            print(f"PASS {path.as_posix()}: status={actual['projection_status']}, steps={actual['steps']}")
    if not paths or failures:
        print(f"Kilo session projection fixtures failed: {failures}/{len(paths)}")
        return 1
    print(f"Kilo session projection fixtures passed: {len(paths)} case(s)")
    return 0


def write_agent(root: pathlib.Path, projection: dict[str, Any]) -> pathlib.Path:
    target = (root / projection["agent"]["path"]).resolve()
    canonical = (root / ".kilo" / "agents").resolve()
    if canonical not in target.parents:
        raise ValueError("Kilo runtime agents may be written only under .kilo/agents/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(projection["agent"]["agent_markdown"], encoding="utf-8", newline="\n")
    return target


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--session", type=pathlib.Path)
    parser.add_argument("--write-agent", action="store_true")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.fixtures:
            return run_fixtures(root)
        if not args.session:
            raise ValueError("provide --session or use --fixtures")
        path = args.session if args.session.is_absolute() else root / args.session
        projection = project_session(root, load_mapping(path))
        if args.write_agent:
            print(f"wrote: {write_agent(root, projection)}")
        if args.format == "json":
            print(json.dumps(projection, indent=2, ensure_ascii=True))
        else:
            print(yaml.safe_dump(projection, sort_keys=False, allow_unicode=False).rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
