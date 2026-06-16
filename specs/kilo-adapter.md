# Kilo Adapter Target Specification

## Purpose

The Kilo adapter compiles Manurella's runtime-neutral agent definitions into Kilo Code agent Markdown files.

The target is current Kilo Code agent files, not legacy `custom_modes.yaml`.

Sources checked:

- <https://kilo.ai/docs/customize/custom-modes>
- <https://kilo.ai/docs/customize/custom-subagents>

## Target Path

Project-local generated agents should be written to:

```text
.kilo/agents/<agent-id>.md
```

Kilo also recognizes `.kilo/agent/` and `.opencode/agents/`, but Manurella standardizes on `.kilo/agents/` for v0.

## Kilo Agent File Shape

Each exported file contains YAML frontmatter followed by a Markdown prompt body.

```md
---
description: Short trigger-focused summary used by Kilo's picker/orchestrator.
mode: primary | subagent | all
color: "#10B981"
permission:
  read: allow
  edit:
    "*.md": "allow"
    "*": "deny"
  bash: deny
steps: 25
temperature: 0.3
---

Prompt body goes here.
```

## Required Frontmatter

- `description`
- `mode`
- `permission`

## Optional Frontmatter

- `model`
- `temperature`
- `top_p`
- `steps`
- `color`
- `variant`
- `hidden`
- `disable`

## Permission Mapping

Manurella permission names map to Kilo permission types:

| Manurella | Kilo |
| --- | --- |
| `read` | `read`, `glob`, `grep` |
| `edit` | `edit` |
| `shell` | `bash` |
| `web` | `webfetch`, `websearch` |
| `delegate` | `task` |
| `todo` | `todowrite`, `todoread` |

Default export policy:

- Deny `bash` unless the agent is explicitly technical and needs command execution.
- Deny broad `edit` unless the domain pack author gave a scoped rule.
- Export creative and mentor agents as non-shell agents.
- Export checker/auditor agents with read-first permissions.
- Use `ask` for risky capabilities when Kilo supports it.
- Treat `steps` as the first Kilo-side runtime-control budget knob.

## Mode Mapping

- User-selectable orchestrators: `primary`
- Internal specialists: `subagent`
- Agents useful both directly and through delegation: `all`

V0 should favor `primary` for one top-level domain orchestrator and `subagent` for narrower specialists.

## Prompt Body Structure

The generated prompt body should use this order:

1. Role and purpose
2. Use boundaries
3. Operating workflow
4. Required context
5. Output contract
6. Safety/permission rules
7. Evaluation rubric summary

Adapters should not include large references inline. They should point to project files or domain references.

## Validation Rules

Before writing exported Kilo agents, validate:

- filename matches `id`
- frontmatter parses as YAML
- `description` exists and is under 240 characters
- `permission` exists
- no broad `edit: allow` unless approved
- no `bash: allow` on creative, pixel, or mentor specialists
- prompt body exists
- generated file is deterministic from source specs
- top-level agents with `delegate: allow` scope `permission.task` to internal agents from the same domain
- internal agents export `permission.task: deny` by default
- generated files include a source-file warning and should not be edited directly

## Research Hooks

- Test Kilo's exact behavior for generated `permission.task` maps in real sessions.
- Test whether Kilo uses `description` strongly enough for delegation or whether prompt body trigger text matters more.
- Decide whether generated `.kilo/agents` should be committed, ignored, or treated as release artifacts after v0 experiments.

## Exporter

The initial exporter lives at:

```text
adapters/kilo/export_agents.py
```

Usage:

```powershell
python adapters/kilo/export_agents.py --domain build --output .kilo/agents
python adapters/kilo/export_agents.py --all --output .kilo/agents
python adapters/kilo/export_agents.py --domain build --output .kilo/agents --profile quick --dry-run
```

The exporter requires PyYAML and intentionally fails closed on missing schema keys or unsafe permission expansion.

Runtime budget policy is defined in `specs/runtime-control.md`.

Supported profiles:

- `quick`: caps Kilo `steps`, denies `task`, and instructs agents to avoid delegation by default.
- `standard`: preserves source `steps` and uses the normal v0 agent workflow.
- `deep`: keeps source `steps` unchanged but adds deep-profile checkpoint and timeout instructions.
