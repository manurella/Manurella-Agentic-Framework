# Domain Pack Specification

## Purpose

A domain pack is a portable specialist package. It defines domain behavior, context requirements, permissions, examples, and rubrics without committing to a runtime.

Domain packs replace the old habit of stuffing every instruction into a global YAML prompt.

## Required Files

Each domain pack should eventually contain:

```text
domains/<domain>/
  README.md
  agents/
  rubrics/
  examples/
  references/
```

V0 may start with only `README.md`.

## README Contract

Each domain `README.md` must include:

- `Purpose`
- `Use When`
- `Do Not Use When`
- `Core Outputs`
- `Context Policy`
- `Permission Baseline`
- `Evaluation Rubric`
- `Research Questions`

## Agent Contract

Each agent definition should eventually define:

- `id`
- `display_name`
- `purpose`
- `trigger_description`
- `non_trigger_description`
- `core_instructions`
- `response_style`
- `allowed_tools`
- `forbidden_tools`
- `output_contracts`
- `eval_rubrics`

## Prompt Design Rules

- Keep the always-on prompt small.
- Prefer clear task contracts over persona-heavy prose.
- Put large examples in `examples/`.
- Put deep domain references in `references/`.
- Convert recurring successful workflows into procedures.
- Include refusal/escalation behavior for unsafe or impossible tasks.

## Adapter Rules

Adapters may transform domain packs into:

- Kilo `.kilo/agents/*.md`
- Codex `AGENTS.md` / `SKILL.md`
- ChatGPT/Gemini instruction packs
- Python runtime agent definitions

Adapters must preserve:

- purpose
- trigger boundaries
- permission intent
- output contracts
- evaluation metadata

Adapters may not silently add tools, broaden file access, or remove safety constraints.

