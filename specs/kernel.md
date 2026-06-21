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
- `mode`: `fast` or `standard`.
- `effort`: `low`, `medium`, `high`, `extra-high`, `max`, or `ultra`.

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
- `type`: episodic, semantic, procedural, project state, user preference, failure lesson, or Atlas mutation
- `scope`: global, project, domain, or task with a scoped owner/reference
- structured claim: subject, predicate, object, and statement
- provenance: source, evidence, and observation references
- `created_at`
- `evidence_status`: unverified, single-source, corroborated, benchmark-supported, or human-confirmed
- `expires_at` or `review_after`
- lifecycle, supersession references, and user-control policy

The executable contract and promotion rules live in `specs/memory-and-atlas.md` and `schemas/memory/`. Scalar confidence is intentionally deferred until comparable historical calibration exists.

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
- `mode`
- `effort`
- `timeout_status`
- `specialist_call_count`
- `repair_loop_count`
- `failure_modes`
- `reviewer`
- `created_at`

### Cognitive Graph

The Cognitive Graph is the runtime-neutral relationship map for Manurella.

It records:

- domains
- agents and subagents
- skills and tools
- context sources
- eval records
- failure modes
- modes
- effort levels
- routing rules
- research evidence

The v0 schema is defined in `specs/cognitive-graph.md`.

## Kernel Invariants

- The canonical agent definition is runtime-neutral.
- Adapters may narrow permissions but must not silently broaden them.
- A task without success criteria is not executable as an eval task.
- Research claims must stay in `research/` until promoted into specs or ADRs.
- Runtime-generated files are outputs, not the source of truth.
- Runtime depth is budgeted by `specs/runtime-control.md`.
- Core routing, handoff, project-state, recovery, and quality-review behavior is defined by `specs/core-operating-protocol.md`.
- Cognitive graph changes must be git-versioned and evidence-linked.
- Full RL/fine-tuning is out of scope until enough scored trajectories exist.

## Research Hooks

These areas need deeper research before implementation hardens:

- best schema for portable agent definitions
- optimal prompt length and ordering for non-frontier models
- practical router features for small benchmark sets
- memory decay and conflict resolution
- MCP security patterns for local developer machines
