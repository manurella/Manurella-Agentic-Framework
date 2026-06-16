"""Export Manurella agent definitions to Kilo Markdown agents."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import textwrap
from typing import Any

import yaml


REQUIRED_KEYS = {
    "id",
    "domain",
    "tier",
    "status",
    "purpose",
    "use_when",
    "do_not_use_when",
    "inputs",
    "outputs",
    "permissions",
    "context",
    "workflow",
    "evaluation",
    "failure_modes",
    "research",
}

KNOWN_DOMAINS = {"build", "pixel", "muse", "mentor"}
TOP_LEVEL = "top_level"
INTERNAL = "internal"
PROFILE_NAMES = {"quick", "standard", "deep"}

PROFILE_CONFIG: dict[str, dict[str, Any]] = {
    "quick": {
        "target_latency": "under 5 minutes",
        "max_specialist_calls": "0 by default",
        "max_repair_loops": "0",
        "deep_reasoning": "disabled unless the user explicitly asks",
        "top_level_step_cap": 16,
        "internal_step_cap": 8,
        "rules": [
            "Do not delegate by default.",
            "Use one direct verification check when applicable.",
            "Stop and report if the task is larger than a quick run.",
        ],
    },
    "standard": {
        "target_latency": "5-15 minutes",
        "max_specialist_calls": "up to 3",
        "max_repair_loops": "1",
        "deep_reasoning": "allowed for planning, diagnosis, or critique",
        "top_level_step_cap": None,
        "internal_step_cap": None,
        "rules": [
            "Delegate only when the specialist has a narrow task slice.",
            "Run or design verification for objective changes.",
            "Stop after one failed repair loop unless new evidence appears.",
        ],
    },
    "deep": {
        "target_latency": "agreed before the run",
        "max_specialist_calls": "explicitly planned",
        "max_repair_loops": "explicitly planned",
        "deep_reasoning": "allowed with compact intermediate artifacts",
        "top_level_step_cap": None,
        "internal_step_cap": None,
        "rules": [
            "State the checkpoint before doing worker calls.",
            "Keep intermediate reasoning compact and artifact-shaped.",
            "Stop on timeout, repeated blockers, or the agreed checkpoint.",
        ],
    },
}


class ExportError(Exception):
    """Raised for deterministic export validation failures."""


def read_agent(path: pathlib.Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ExportError(f"{path}: missing YAML frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ExportError(f"{path}: malformed YAML frontmatter")

    data = yaml.safe_load(parts[1]) or {}
    if not isinstance(data, dict):
        raise ExportError(f"{path}: frontmatter must be a mapping")

    missing = sorted(REQUIRED_KEYS - set(data))
    if missing:
        raise ExportError(f"{path}: missing required keys: {', '.join(missing)}")

    agent_id = data["id"]
    if path.stem != agent_id:
        raise ExportError(f"{path}: filename must match id '{agent_id}'")

    if data["domain"] not in KNOWN_DOMAINS:
        raise ExportError(f"{path}: unknown domain '{data['domain']}'")

    if data["tier"] not in {TOP_LEVEL, INTERNAL}:
        raise ExportError(f"{path}: tier must be top_level or internal")

    return data, parts[2].strip()


def one_line(value: str, limit: int = 240) -> str:
    normalized = re.sub(r"\s+", " ", value).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "..."


def list_items(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, list):
        return [str(item) for item in values]
    return [str(values)]


def yaml_block(data: dict[str, Any]) -> str:
    dumped = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=False,
        default_flow_style=False,
        width=1000,
    ).strip()
    return f"---\n{dumped}\n---\n"


def kilo_mode(agent: dict[str, Any]) -> str:
    runtime = agent.get("runtime") or {}
    kilo = runtime.get("kilo") or {}
    explicit = kilo.get("mode")
    if explicit:
        return explicit
    return "primary" if agent["tier"] == TOP_LEVEL else "subagent"


def same_domain_internal_agents(agents: list[dict[str, Any]], domain: str) -> list[str]:
    return sorted(
        agent["id"]
        for agent in agents
        if agent["domain"] == domain and agent["tier"] == INTERNAL
    )


def map_permissions(agent: dict[str, Any], all_agents: list[dict[str, Any]], profile: str) -> dict[str, Any]:
    source = agent.get("permissions") or {}
    for key in ("read", "edit", "shell", "web", "delegate"):
        if key not in source:
            raise ExportError(f"{agent['id']}: missing permission '{key}'")

    permission: dict[str, Any] = {
        "read": source["read"],
        "glob": source["read"],
        "grep": source["read"],
        "edit": source["edit"],
        "bash": source["shell"],
        "webfetch": source["web"],
        "websearch": source["web"],
        "todowrite": "ask" if agent["tier"] == TOP_LEVEL else "deny",
        "todoread": "allow" if agent["tier"] == TOP_LEVEL else "deny",
    }

    if source["delegate"] == "allow":
        allowed = same_domain_internal_agents(all_agents, agent["domain"])
        task_rules: dict[str, str] = {"*": "deny"}
        for item in allowed:
            task_rules[item] = "allow"
        permission["task"] = task_rules
    elif source["delegate"] == "ask":
        permission["task"] = "ask"
    else:
        permission["task"] = "deny"

    if agent["domain"] in {"pixel", "muse", "mentor"} and permission["bash"] == "allow":
        raise ExportError(f"{agent['id']}: non-build agents must not export bash: allow in v0")

    if profile == "quick":
        permission["task"] = "deny"

    return permission


def profile_steps(agent: dict[str, Any], kilo: dict[str, Any], profile: str) -> int | None:
    raw_steps = kilo.get("steps")
    cap_key = "top_level_step_cap" if agent["tier"] == TOP_LEVEL else "internal_step_cap"
    cap = PROFILE_CONFIG[profile][cap_key]

    if raw_steps is None:
        return cap

    try:
        steps = int(raw_steps)
    except (TypeError, ValueError) as exc:
        raise ExportError(f"{agent['id']}: Kilo steps must be an integer") from exc

    if steps <= 0:
        raise ExportError(f"{agent['id']}: Kilo steps must be positive")

    if cap is None:
        return steps
    return min(steps, int(cap))


def frontmatter(agent: dict[str, Any], all_agents: list[dict[str, Any]], profile: str) -> dict[str, Any]:
    runtime = agent.get("runtime") or {}
    kilo = runtime.get("kilo") or {}
    data: dict[str, Any] = {
        "description": one_line(agent["purpose"]),
        "mode": kilo_mode(agent),
        "permission": map_permissions(agent, all_agents, profile),
    }

    for key in ("model", "temperature", "top_p", "color", "variant", "hidden", "disable"):
        if key in kilo:
            data[key] = kilo[key]

    steps = profile_steps(agent, kilo, profile)
    if steps is not None:
        data["steps"] = steps

    if data["mode"] not in {"primary", "subagent", "all"}:
        raise ExportError(f"{agent['id']}: invalid Kilo mode '{data['mode']}'")

    if len(data["description"]) > 240:
        raise ExportError(f"{agent['id']}: description exceeds 240 characters")

    return data


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def input_list(items: list[dict[str, Any]]) -> str:
    lines = []
    for item in items:
        required = "required" if item.get("required") else "optional"
        lines.append(f"- `{item.get('name')}` ({item.get('type')}, {required})")
    return "\n".join(lines) if lines else "- None"


def runtime_control_section(profile: str) -> str:
    config = PROFILE_CONFIG[profile]
    rules = bullet_list(list_items(config["rules"]))
    return f"""## Runtime Control

Execution profile: `{profile}`

- Target latency: {config['target_latency']}
- Specialist calls: {config['max_specialist_calls']}
- Repair loops: {config['max_repair_loops']}
- Deep reasoning: {config['deep_reasoning']}

Profile rules:

{rules}
"""


def prompt_body(agent: dict[str, Any], source_path: pathlib.Path, profile: str) -> str:
    outputs = agent.get("outputs") or {}
    context = agent.get("context") or {}
    evaluation = agent.get("evaluation") or {}
    research = agent.get("research") or {}

    body = f"""# {agent['id']}

This Kilo agent is generated from `{source_path.as_posix()}`.

Do not edit this generated file directly. Update the Manurella source agent definition and rerun the Kilo adapter.

## Purpose

{agent['purpose']}

## Use When

{bullet_list(list_items(agent.get('use_when')))}

## Do Not Use When

{bullet_list(list_items(agent.get('do_not_use_when')))}

## Inputs

{input_list(agent.get('inputs') or [])}

## Output Contract

{outputs.get('contract', 'Not specified.')}

## Workflow

{bullet_list(list_items(agent.get('workflow')))}

## Context Policy

Always-on:

{bullet_list(list_items(context.get('always_on')))}

References to load only when useful:

{bullet_list(list_items(context.get('references')))}

Retrieved context:

{bullet_list(list_items(context.get('retrieved')))}

## Permission Policy

Respect the Kilo frontmatter permissions. If a needed action is denied, return a blocked result with the missing capability instead of working around it.

{runtime_control_section(profile)}

## Evaluation Rubric

{bullet_list(list_items(evaluation.get('rubric')))}

Benchmarks:

{bullet_list(list_items(evaluation.get('benchmark_refs')))}

## Failure Modes To Avoid

{bullet_list(list_items(agent.get('failure_modes')))}

## Source References

{bullet_list(list_items(research.get('source_refs')))}

## Open Questions

{bullet_list(list_items(research.get('open_questions')))}
"""
    return textwrap.dedent(body).strip() + "\n"


def discover_agents(root: pathlib.Path, domains: list[str]) -> list[tuple[pathlib.Path, dict[str, Any], str]]:
    records = []
    for domain in domains:
        agent_dir = root / "domains" / domain / "agents"
        if not agent_dir.exists():
            raise ExportError(f"missing agent directory: {agent_dir}")
        for path in sorted(agent_dir.glob("*.md")):
            data, body = read_agent(path)
            records.append((path, data, body))
    return records


def export_agents(
    root: pathlib.Path,
    domains: list[str],
    output: pathlib.Path,
    dry_run: bool,
    profile: str,
) -> list[pathlib.Path]:
    records = discover_agents(root, domains)
    all_agents = [record[1] for record in records]
    written: list[pathlib.Path] = []

    for source_path, agent, _source_body in records:
        relative_source = source_path.relative_to(root)
        target = output / f"{agent['id']}.md"
        content = yaml_block(frontmatter(agent, all_agents, profile)) + "\n" + prompt_body(
            agent,
            relative_source,
            profile,
        )
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
        written.append(target)
    return written


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--domain", action="append", choices=sorted(KNOWN_DOMAINS))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path(".kilo/agents"))
    parser.add_argument("--profile", choices=sorted(PROFILE_NAMES), default="standard")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    domains = sorted(KNOWN_DOMAINS) if args.all else args.domain

    try:
        written = export_agents(root, domains, output, args.dry_run, args.profile)
    except ExportError as exc:
        print(f"export failed: {exc}", file=sys.stderr)
        return 1

    action = "would write" if args.dry_run else "wrote"
    for path in written:
        print(f"{action}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
