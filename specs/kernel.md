# Kernel Specification

## Purpose

The kernel is the runtime-neutral contract for Manurella. It defines what an agent, task, permission, memory reference, and evaluation record mean before any adapter converts them into Kilo, Codex, ChatGPT, Gemini, or a Python runtime.

The kernel must stay small. Domain expertise belongs in domain packs and references. Runtime quirks belong in adapters.

## Kernel Object Model

### Agent

An `Agent` is a portable specialist definition.

Required fields:

- `id`: stable kebab-case identifier.
- `display_name`: human-readable name.
- `domain`: owning domain pack.
- `purpose`: one sentence describing the agent's job.
- `use_when`: trigger conditions.
- `do_not_use_when`: non-trigger conditions.
- `instruction_blocks`: ordered prompt sections.
- `permissions`: capability policy.
- `context_policy`: what context may be loaded and when.
- `output_contracts`: accepted response shapes.
- `eval_rubrics`: rubrics used to score outputs.
- `adapter_hints`: runtime-specific preferences that do not change the agent's meaning.

Optional fields:

- `model_preferences`
- `temperature_preferences`
- `examples`
- `references`
- `memory_policy`

### Task Contract

A `TaskContract` is the minimum work order accepted by the framework.

Required fields:

- `goal`: what the user wants.
- `domain`: expected domain, or `unknown`.
- `inputs`: files, text, images, links, or context references.
- `constraints`: hard limits and user preferences.
- `success_criteria`: measurable done conditions.
- `risk_level`: `low`, `medium`, `high`, or `blocked`.
- `allowed_tools`: tools the task may use.
- `expected_output`: response or artifact format.
- `execution_profile`: `quick`, `standard`, or `deep`.

### Permission Policy

Permissions are capability declarations, not vibes.

Default policy:

- `read`: allowed for scoped files/resources.
- `edit`: denied unless explicitly scoped.
- `shell`: denied unless explicitly required.
- `web`: ask or deny depending on runtime.
- `mcp`: allow only named tools/resources.
- `delegate`: allow only named agents.

Permission levels:

- `allow`
- `ask`
- `deny`

### Memory Reference

Memory is never automatically trusted. A memory record must include:

- `id`
- `type`: `project_state`, `user_preference`, `domain_knowledge`, `procedure`, `failure_lesson`
- `scope`: global, project, domain, or task
- `source`
- `created_at`
- `confidence`
- `expires_at` or `review_after`
- `content`

### Evaluation Record

Every benchmark run should record:

- `task_id`
- `agent_id`
- `runtime`
- `model`
- `prompt_version`
- `adapter_version`
- `output_path`
- `scores`
- `cost_notes`
- `latency_notes`
- `execution_profile`
- `timeout_status`
- `specialist_call_count`
- `repair_loop_count`
- `failure_modes`
- `reviewer`
- `created_at`

## Kernel Invariants

- The canonical agent definition is runtime-neutral.
- Adapters may narrow permissions but must not silently broaden them.
- A task without success criteria is not executable as an eval task.
- Research claims must stay in `research/` until promoted into specs or ADRs.
- Runtime-generated files are outputs, not the source of truth.
- Runtime depth is budgeted by `specs/runtime-control.md`.
- Full RL/fine-tuning is out of scope until enough scored trajectories exist.

## Research Hooks

These areas need deeper research before implementation hardens:

- best schema for portable agent definitions
- optimal prompt length and ordering for non-frontier models
- practical router features for small benchmark sets
- memory decay and conflict resolution
- MCP security patterns for local developer machines
