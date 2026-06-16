# Agent Schema Specification

## Purpose

This schema defines the runtime-neutral shape of a Manurella agent. Runtime adapters, including Kilo, must compile from this structure instead of treating Markdown prompt files as the source of truth.

## Design Rule

Agents are not personas. Agents are bounded workflow components with explicit responsibilities, context needs, permissions, output contracts, evaluation rubrics, and failure modes.

Canonical authoring standards live in `docs/agent-authoring-doctrine.md`. This schema defines the machine-readable shape; the doctrine defines the quality bar for writing and promoting the agent.

## Agent Tiers

### Top-Level Agent

A top-level agent is directly selectable by a user or runtime router.

It may:

- receive user intent
- preserve long-horizon task state
- choose workflow phase
- delegate to internal agents
- ask clarifying questions
- produce final user-facing output

It should not perform narrow tool-heavy work when an internal agent can do it with a stricter contract.

### Internal Agent

An internal agent is invoked by a top-level agent or orchestrator.

It may:

- transform one structured input into one structured output
- inspect a bounded artifact
- validate, judge, or repair an output
- update durable state out-of-band

It should not negotiate user intent, change global goals, or expand task scope.

## Required Fields

Every agent definition must include:

```yaml
id: string
domain: build | muse | pixel | mentor
tier: top_level | internal
status: draft | research_candidate | accepted | deprecated
purpose: string
use_when:
  - string
do_not_use_when:
  - string
inputs:
  - name: string
    type: string
    required: boolean
outputs:
  contract: string
  schema_ref: string | null
permissions:
  read: allow | ask | deny
  edit: allow | ask | deny
  shell: allow | ask | deny
  web: allow | ask | deny
  delegate: allow | ask | deny
context:
  always_on:
    - string
  references:
    - string
  retrieved:
    - string
workflow:
  - string
evaluation:
  rubric:
    - string
  benchmark_refs:
    - string
failure_modes:
  - string
research:
  source_refs:
    - string
  open_questions:
    - string
```

## Optional Fields

```yaml
runtime:
  kilo:
    mode: primary | subagent | all
    temperature: number
    steps: integer
    color: string
    modes:
      fast:
        step_cap: integer
      standard:
        step_cap: integer | null
    efforts:
      low: string
      medium: string
      high: string
      extra-high: string
      max: string
      ultra: string
memory:
  reads:
    - string
  writes:
    - string
tool_contracts:
  - string
mode_behavior:
  fast: string
  standard: string
effort_behavior:
  low: string
  medium: string
  high: string
  extra-high: string
  max: string
  ultra: string
promotion_requirements:
  - string
```

`mode_behavior` and `effort_behavior` may be inherited from a documented domain default, such as `domains/build/runtime-policy.md`. Inheritance is valid only when the agent definition or domain README names the source. Agent-local behavior should override the domain default only when evals show that the general policy is insufficient.

## Context Tiering

Agent definitions must separate context into three tiers:

- `always_on`: minimal identity, boundary, formatting, and safety constraints.
- `references`: domain guides loaded only when the agent is invoked.
- `retrieved`: just-in-time context such as file chunks, learner state, style bible entries, image outputs, or test logs.

Large manuals, codebases, manuscripts, histories, or model docs must not be embedded directly in always-on prompts.

## Promotion Rules

An agent cannot move to `accepted` until it has:

1. Domain research support.
2. Clear top-level/internal tier classification.
3. Strict input and output contracts.
4. Permission boundaries.
5. Explicit mode and effort behavior, either directly in the agent or inherited from a named documented domain default.
6. At least two benchmark tasks.
7. Known failure modes.
8. A baseline-vs-guided evaluation plan.
9. Runtime adapter validation for the first target runtime.

## Kilo Adapter Notes

The Kilo adapter should map:

- `tier: top_level` to `mode: primary` unless explicitly marked `all`.
- `tier: internal` to `mode: subagent`.
- `permissions.shell` to Kilo `bash`.
- `permissions.delegate` to Kilo `task`.
- `permissions.web` to Kilo `webfetch` and `websearch`.

The adapter must fail closed on missing permissions.
