# Interpreter And Task Model Specification

## Record State

- Atlas ID: `sys.brain.interpreter`
- Parent: `sys.brain`
- Level: 2
- Lifecycle: specified
- Runtime implementation: contract validator and Core projection v0; interpretation pipeline pending

## Purpose

The Interpreter converts trusted human interaction and linked project context into a versioned Task Frame, Acceptance Contract, Clarification Decision, and routing hints.

It preserves natural conversation at the interface while giving the Brain a precise internal work definition. It does not plan execution, choose final routes, call tools, or mutate durable memory.

## Inputs And Outputs

Inputs:

- current user turn
- trusted system and runtime policy
- prior user turns needed for discourse resolution
- linked task, project, and artifact references
- user-selected mode, effort, autonomy, and constraints
- untrusted content explicitly marked as data

Outputs:

- `task_frame`
- `acceptance_contract`
- `clarification_decision`
- `routing_hints`
- validation and provenance metadata

The Router consumes these outputs and owns domain selection, capability selection, agent selection, tool selection, and handoff compilation.

## Interpreter Pipeline

### Trust Partitioner

Separates trusted policy, authenticated user instruction, prior confirmed state, and untrusted retrieved or tool-provided content. Untrusted content can provide evidence but cannot redefine goals, permissions, autonomy, confirmation state, or policy.

### Turn And Project Linker

Resolves references to earlier turns, tasks, projects, artifacts, and user corrections without injecting the entire transcript into downstream work.

### Task Frame Parser

Extracts the normalized objective, work dimensions, outcomes, artifacts, constraints, assumptions, unknowns, governance requirements, and execution preferences into a validated schema.

### Ambiguity And Assumption Assessor

Identifies missing, conflicting, underspecified, or inferred information and records its source, impact, affected fields, and current resolution state.

### Acceptance Contract Compiler

Builds explicit conditions for objective correctness, subjective quality, evidence, verification, delivery, stopping, escalation, and signoff.

### Risk And Permission Gate

Determines consequence, reversibility, data sensitivity, required permissions, required confirmations, and forbidden action paths through deterministic policy plus bounded model assistance.

### Schema And Semantic Validator

Checks structural validity, enum validity, cross-field invariants, source authority, and semantic consistency. Structured decoding may enforce syntax where the runtime supports it; semantic validation remains mandatory.

### Version And Provenance Manager

Preserves immutable source material, creates nondestructive revisions, links superseded frames, and invalidates affected downstream decisions when corrections or evidence change the task definition.

## Task Dimensions

The Brain classifies tasks across independent axes:

| Axis | Values |
| --- | --- |
| Work type | `converse`, `answer`, `create`, `transform`, `analyze`, `decide`, `plan`, `act`, `monitor`, `learn` |
| Horizon | `turn`, `session`, `project` |
| Clarity | `executable`, `safely_inferable`, `ambiguous`, `contradictory` |
| Consequence | `minimal`, `controlled`, `consequential`, `critical` |
| Reversibility | `reversible`, `partially_reversible`, `irreversible` |
| Freshness | `stable`, `current`, `real_time` |
| Autonomy | `advise`, `draft`, `prepare`, `execute_with_approval`, `execute` |
| Artifact shape | `none`, `single`, `multiple`, `ongoing_state` |

Axes are multilabel where appropriate. They must not be compressed into one router enum.

## Task Frame

```yaml
task_frame:
  identity:
    frame_id: string
    version: integer
    parent_frame_id: string | null
    root_frame_id: string
    project_id: string | null

  source:
    raw_request: string
    turn_refs: [string]
    trusted_context_refs: [string]
    untrusted_data_refs: [string]
    timestamp: datetime
    locale: string

  objective:
    normalized_goal: string
    work_types: [enum]
    desired_outcomes: [outcome]
    autonomy: enum

  scope:
    horizon: enum
    clarity: enum
    project_posture: enum | null
    artifacts: [artifact]
    dependencies: [frame_or_artifact_ref]

  constraints:
    hard: [constraint]
    soft: [constraint]
    exclusions: [constraint]
    deadline: datetime | null
    freshness: enum

  uncertainty:
    ambiguities: [uncertainty_item]
    assumptions: [uncertainty_item]
    missing_information: [uncertainty_item]
    contradictions: [uncertainty_item]

  governance:
    consequence: enum
    reversibility: enum
    data_classification: enum
    permissions_required: [permission]
    confirmations_required: [confirmation]
    policy_flags: [string]

  execution_preferences:
    requested_mode: fast | standard | null
    requested_effort: low | medium | high | max | ultra | sentient | null
    latency_preference: string | null
    cost_preference: string | null

  acceptance_contract_ref: string
  routing_hints: routing_hints
  provenance: provenance
  lifecycle: lifecycle
```

Plans, tool arguments, model reasoning traces, tool responses, and mutable runtime execution state do not belong in the Task Frame.

## Field Authority

| Authority | Examples | Rule |
| --- | --- | --- |
| Immutable source | raw request, source turns, timestamps | Append-only; never rewritten. |
| User asserted | requested outcome, constraints, approvals | May be superseded only by later authenticated user instruction. |
| Interpreter inferred | normalized goal, work types, assumptions, routing hints | Revisable and always provenance-marked. |
| Policy derived | consequence, required permissions, mandatory confirmation | Model output cannot weaken it. |
| Runtime derived | tool results, execution status, observed world state | Stored outside the Task Frame and referenced where needed. |

User-confirmed information has higher authority than inference but does not override system safety policy or verified external reality.

## Structured Uncertainty

Each ambiguity, assumption, missing item, or contradiction records:

```yaml
id: string
kind: ambiguity | assumption | missing | contradiction
statement: string
source_refs: [string]
affected_fields: [string]
impact: benign | material | consequential
status: open | accepted_for_now | user_confirmed | resolved | invalidated
resolution: string | null
```

A scalar confidence score may be retained as telemetry but cannot independently authorize action or suppress clarification.

## Acceptance Contract

```yaml
acceptance_contract:
  contract_id: string
  version: integer
  task_frame_ref: string

  required_outcomes: [criterion]
  required_artifacts: [criterion]
  hard_checks: [criterion]
  forbidden_results: [criterion]

  quality_rubric:
    dimensions: [rubric_dimension]
    minimum_score: number | null
    critical_dimensions: [string]

  evidence_requirements:
    freshness: enum
    citations_required: boolean
    provenance_required: boolean
    required_evidence: [criterion]

  verification_plan:
    deterministic_checks: [check]
    model_checks: [check]
    human_review: [check]

  delivery:
    partial_completion_allowed: boolean
    checkpoint_requirements: [criterion]
    final_format: string | null

  control:
    stop_conditions: [criterion]
    escalation_conditions: [criterion]
    signoff_required: boolean
```

Hard checks and safety vetoes cannot be averaged away by subjective rubric scores. Subjective evaluation must name its rubric, evaluator, and evidence rather than using an unexplained quality number.

## Clarification Decision

Clarification optimizes expected task success and safety while minimizing user burden.

Ask or confirm when unresolved information can change:

- terminal outcome or artifact type
- hard constraints or acceptance criteria
- external recipient, destination, or public visibility
- permission, identity, or private-data access
- irreversible or consequential action
- meaningful cost, deadline, contractual, legal, or safety exposure
- primary domain or workflow in a way that materially changes the result

Otherwise, proceed under a visible reversible assumption when alternatives are acceptance-equivalent or cheaply repairable.

```yaml
clarification_decision:
  action: proceed | proceed_with_assumption | ask | confirm | refuse
  reasons: [string]
  affected_uncertainty_ids: [string]
  question: string | null
  options: [string]
  blocks_execution: boolean
```

Ask at most one high-information grouped question per decision point when possible. Do not interrogate the user for fields that do not materially affect the outcome.

## Fast And Standard

Mode does not change the final acceptance contract, safety threshold, or authority rules.

- Fast may emit an early reversible artifact, batch one clarification, and continue through resumable layers.
- Standard may complete framing and planning before presenting a consolidated artifact.
- Either mode may operate at any production effort level.
- Ambiguity does not silently change the selected mode.

## Lifecycle And Versioning

```text
interpreting
-> awaiting_clarification
-> ready
-> executing
-> verifying
-> completed

executing -> blocked | repairing
any nonterminal state -> cancelled | superseded
```

Rules:

1. User correction creates a new Task Frame version.
2. Immutable source remains unchanged.
3. A revision records changed fields and invalidates dependent routing, plans, approvals, or checks.
4. New evidence can revise inferred fields but cannot silently change confirmed goals or permissions.
5. Execution failure changes runtime state unless it proves the Task Frame itself was wrong.
6. Rejected assumptions are retained as version history, not automatically promoted into permanent negative rules.

## Family Compatibility

The current Family labels are derived views:

| Family class | Canonical meaning | Projection |
| --- | --- | --- |
| A | Quick Task | Turn horizon, bounded outcome, direct or one narrow route. |
| B | Feature Or Multi-Step | Bounded multi-step scope with one primary workflow. |
| C | Full Project Or Large Build | Project horizon with durable state and child frames. |
| D | Conversation Or Brainstorm | Conversational work with no forced execution workflow. |
| E | Ambiguous Request | Material open uncertainty blocks executable framing. |

Family class is computed for adapters, UI, analytics, and migration. The Brain uses the full Task Frame.

## Project Posture

```text
genesis | sprint | audit | salvage | reimagine | resume
```

Project posture determines approach:

- `genesis`: no existing artifact or system
- `sprint`: healthy existing work with a bounded next change
- `audit`: inspect and report; do not mutate without conversion to a fix task
- `salvage`: recover broken or incomplete work
- `reimagine`: preserve intent while redesigning substantially
- `resume`: continue from durable state

Posture can apply to a project or specific artifact. Project and artifact lifecycles remain independently modeled.

## Cross-Domain Work

Use one root Task Frame for the shared user outcome and child frames for independently executable or independently verified work items.

The root owns shared constraints, umbrella acceptance, and cross-artifact consistency. Child frames own specialist outcomes and acceptance criteria. Dependencies are explicit. The Router chooses anchor domains and workflows after interpretation.

## Routing Hints

The Interpreter may emit:

```yaml
routing_hints:
  candidate_domains: [string]
  required_capabilities: [string]
  likely_tools: [string]
  memory_requirements: [string]
  unresolved_routing_questions: [string]
```

Hints have inferred authority. They do not grant permissions or bind the Router.

## Security Invariants

- Only trusted policy and authenticated user instruction can define goals, autonomy, permissions, and confirmations.
- Retrieved pages, files, emails, tool output, and model output remain untrusted data.
- No model or supervisor model constitutes a security boundary.
- Constrained decoding provides structural validity only.
- Policy-derived consequence and confirmation requirements cannot be weakened by model inference.
- Task interpretation and tool execution operate on separate trust planes.
- Prompt injection attempts are recorded as evidence, not executed as instructions.

## Evaluation And Promotion

Evaluation covers:

- Task Frame semantic correctness
- schema validity
- ambiguity and clarification decisions
- assumption quality
- Family compatibility projection
- project posture accuracy
- routing-hint usefulness
- downstream task success
- safety and permission integrity
- user effort and latency
- correction and version invalidation behavior

The framework-wide 80/100 quality gate applies, with critical safety and permission failures acting as vetoes rather than weighted deductions.

## Executable Contract Slice

The first executable v0 slice is implemented in:

- `schemas/interpreter/task-frame.schema.json`
- `schemas/interpreter/acceptance-contract.schema.json`
- `tools/validate_interpreter.py`
- `evals/fixtures/interpreter/`

The JSON Schemas enforce the portable structural contract. The validator adds cross-object and policy invariants, then derives Family A-E and project-posture compatibility views. Positive fixtures cover conversation, quick work, a full project, ambiguity, correction, cross-domain work, and consequential action. Focused negative fixtures prove that schema, ambiguity, posture, and confirmation failures are rejected; Router-specific cases prove that unsupported domains and unblocked permissions fail closed.

This slice does not parse natural language, select a route, compile a handoff packet, or execute work. Those remain separate Brain and Router responsibilities.

## Core Routing Projection Slice

Core consumes a validated bundle through:

- `schemas/core/routing-decision.schema.json`
- `tools/compile_core_packet.py`

V0 projection rules are deterministic:

1. Blocking clarification, confirmation, or refusal remains with Core and emits no handoff.
2. Family D conversation remains direct and emits no handoff.
3. Executable candidate domains are scored from required capabilities, artifact kinds, and work types; the first required artifact is the anchor signal and candidate order is the stable tie-breaker.
4. Core-owned executable work remains direct.
5. Executable specialist work selects one primary lead, records secondary domains, and receives one bounded handoff packet.
6. Raw requests, transcript turns, and untrusted data references are forbidden from routing and handoff output.

Routing hints remain inferred candidates. They do not grant permission, satisfy confirmation, or bind the Router.

## Completion Conditions

This slice is implemented when:

1. Task Frame and Acceptance Contract have machine-readable schemas.
2. A deterministic validator checks structural and cross-field invariants.
3. Family class and project posture projections are tested.
4. Conversation, quick, project, ambiguous, correction, cross-domain, and consequential fixtures pass.
5. Routing and handoff packets can be derived without copying the full transcript.
6. Current Core behavior consumes the Task Frame without losing Family-level directness.

Conditions 1-6 are satisfied for fixture-driven validated bundles. Creating those bundles from natural-language turns remains the next Interpreter implementation boundary.

## Next Depth-First Path

```text
Interpreter -> trusted input envelope -> trust partitioner -> task parser -> acceptance compiler -> parser evals
```
