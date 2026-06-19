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

## Trusted Input And Partition Slice

The first live input boundary is implemented in:

- `schemas/interpreter/trusted-input-envelope.schema.json`
- `schemas/interpreter/trust-partition.schema.json`
- `tools/partition_trusted_input.py`
- `evals/fixtures/trust-partitioner/`

Each input item carries immutable content provenance, source metadata, claimed authority, authentication evidence, and explicit control claims. The partitioner derives authority from item kind, origin, and verified authentication; it never trusts a content-level claim by itself.

The output separates trusted policy, authenticated user instruction, prior confirmed state, and untrusted data. Unauthorized goal, autonomy, permission, confirmation, constraint, or policy claims are rejected and recorded. Retrieved, tool, model, and artifact content remains data even when its transport is authenticated. Task intake without an authenticated user instruction fails closed.

The `quarantined` disposition means untrusted control claims were rejected while a valid task instruction remains executable. `blocked` means the envelope cannot safely define an executable task. This slice performs structural partitioning, not natural-language prompt-injection detection, Task Frame parsing, or authentication itself; adapters must supply genuine authentication evidence.

## Task Frame Parser Baseline

The first natural-language parsing baseline is implemented in:

- `tools/parse_task_frame.py`
- `evals/fixtures/task-frame-parser/`

It consumes a validated trusted input envelope, reruns deterministic trust partitioning, and compiles only authenticated user-instruction content into the existing `task-frame.schema.json` contract. Untrusted content can contribute source references but cannot change the normalized goal, work types, autonomy, governance, or routing hints.

The baseline recognizes explicit work verbs, coarse domain signals, referenced file artifacts, project posture, user-stated exclusions, vague references, and external or destructive action. Vague instructions enter `awaiting_clarification`; unauthenticated task intake is rejected; external or destructive action receives policy-derived permission and confirmation requirements. Every inferred or policy-derived field is provenance-marked.

This parser is deliberately conservative and deterministic. It establishes a runnable baseline, security invariants, and regression fixtures; it does not prove robust semantic parsing across paraphrases, languages, corrections, multiple intents, implicit constraints, deadlines, or nuanced consequence. A production parser requires schema-constrained model decoding followed by the same deterministic validation and baseline-vs-guided evals.

## Acceptance Contract Compiler

The deterministic Acceptance Contract and Clarification Decision compiler is implemented in:

- `tools/compile_acceptance_contract.py`
- `evals/fixtures/acceptance-compiler/`

It derives required outcomes and artifacts, authenticated constraints, forbidden results, two critical quality dimensions, evidence and verification requirements, delivery format, stop conditions, escalation conditions, and signoff from a schema-valid Task Frame. Open material uncertainty compiles to `ask`; consequential or irreversible work compiles to `confirm`; executable low-risk work compiles to `proceed`.

The compiler validates reference reciprocity, version alignment, lifecycle, rubric weights, freshness, permission, confirmation, and signoff through the existing Interpreter validator. Successful fixture bundles are also compiled through the Core routing schema and checked for banned transcript fields.

Domain-specific acceptance logic remains a later specialist or model-backed refinement. The deterministic compiler supplies a complete safe baseline contract; it must not fabricate commands, tests, factual evidence, or subjective preferences absent from the Task Frame.

## Model-Backed Parser Evaluation Harness

The runtime-neutral parser evaluation harness is implemented in:

- `schemas/evals/parser-candidate-run.schema.json`
- `schemas/evals/parser-eval-result.schema.json`
- `tools/evaluate_task_frame_parser.py`
- `evals/fixtures/parser-benchmark/`
- `evals/prompts/interpreter-parser-benchmark.md`

The benchmark corpus is intentionally separate from parser development fixtures and includes paraphrase, implicit audit intent, cross-domain composition, vague resume, destructive euphemism, and indirect prompt injection. The evaluator always runs the deterministic baseline, then optionally scores captured model Task Frames from any runtime.

Metrics cover Task Frame schema validity, full bundle semantic validity, Core routing validity, critical-field accuracy, and safety-critical pass rate. Candidate output remains untrusted. One safety failure vetoes promotion, and candidates must beat baseline critical-field accuracy by the configured threshold while achieving perfect structural, semantic, routing, and safety rates.

The no-network self-test proves the harness and schemas. It does not constitute a model evaluation or justify promotion; that requires a captured candidate under `evals/results/` with exact runtime and model metadata.

The first durable deterministic baseline is `evals/results/parser-rule-baseline-v0.parser-eval.yaml`: structural, semantic, and Core routing validity are 100%, critical-field accuracy is 22/37, and safety-critical pass rate is 1/2. This establishes a meaningful baseline and demonstrates that deterministic structural reliability is not sufficient semantic or safety quality.

StepFun 3.7 Flash with `interpreter-parser-benchmark.v2` achieved high field accuracy in two runs, but neither now passes the complete gate. Full-corpus shadow evaluation found that the first run inserted authentication evidence into `trusted_context_refs`; the evaluator was strengthened to verify exact `turn_refs` and `trusted_context_refs`, withdrawing the earlier pass. The repeat preserved trust projection but failed one semantic and two Core-routing cases. `evals/results/parser-stepfun-v2-promotion.parser-promotion.yaml` blocks production promotion at zero passing runs out of two.

`interpreter-parser-benchmark.v3` makes the source projection explicit: authenticated instruction content references populate `turn_refs`; only trusted policy and prior-confirmed-state content references populate `trusted_context_refs`; authentication evidence never becomes task context; and untrusted content references populate `untrusted_data_refs` exactly.

The legacy full-frame model runs are non-blind diagnostics because their prompt exposed fixtures containing `expected_fields`. They cannot support promotion claims. The private gold corpus remains the scorer source, while models now receive only generated packets under `evals/fixtures/parser-inference-benchmark/`. `tools/evaluate_model_inference.py` validates that these packets contain no gold fields, envelopes, authentication records, or retrieved content before evaluating inference candidates.

The first blinded external inference result is `evals/results/stepfun-inference-v0.parser-eval.yaml`. StepFun achieved 27/37 critical fields (73.0%) versus the 22/37 deterministic baseline and passed both explicit safety cases. It failed promotion because only 2/6 assembled frames passed full Interpreter semantics and Core routing. The result supports the inference-only architecture but does not support model activation.

`task-frame-inference.v1` adds cross-field schema invariants: material or consequential ambiguity requires ambiguous or contradictory clarity; ambiguous work requires an ambiguity record; executable work requires at least one candidate domain; and project horizon requires project posture. Historical `v0` inference records remain valid under their original schema.

The first blinded v1 result is `evals/results/stepfun-inference-v1.parser-eval.yaml`. It passed schema, semantic, Core-routing, and both safety gates, scoring 26/37 critical fields (70.3%) against the 59.5% baseline. This clears the individual evaluator by 10.8 percentage points but remains below production promotion because `evals/results/stepfun-inference-v1-promotion.parser-promotion.yaml` contains only one run and repeated evidence requires at least two.

The independent blinded v1 repeat also passed every gate with 29/37 critical fields (78.4%). The repeated-run promotion record now passes at 2/2 runs, with minimum field accuracy 70.3% and minimum schema, semantic, routing, and safety rates of 100%.

`guarded-model-inference.v0` is therefore available as an explicit opt-in adapter mode. It selects an assembled inference frame only when the promotion record passes, model and prompt identities match exactly, and the current frame passes schema, trust, semantic, and Core-routing validation. Otherwise it selects the deterministic baseline. Shadow remains the default until broader runtime observation and human residual-risk review support a default change.

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

Conditions 1-6 are satisfied for both hand-authored fixtures and the deterministic input-to-bundle pipeline. The trusted input envelope, trust partition, Task Frame parser baseline, Acceptance Contract compiler, Clarification Decision, semantic validation, Core projection, model-evaluation harness, repeated-run promotion gate, shadow adapter, and full-corpus shadow evaluator are implemented. Both external runs fail the complete gate; production model parsing remains blocked.

## Next Depth-First Path

```text
Interpreter -> trusted input envelope [implemented] -> trust partitioner [implemented] -> task parser baseline [implemented] -> acceptance compiler [implemented] -> parser eval harness [implemented] -> external candidate benchmark [failed 0/2] -> repeated-run gate [blocked] -> shadow runtime adapter [implemented] -> full-corpus shadow evaluation [remain shadow]

## Shadow Parser Adapter

`tools/shadow_parse_task_frame.py` is the first runtime-neutral model-parser boundary. It accepts a validated trusted input envelope and an optional untrusted model Task Frame, then:

1. Compiles the deterministic baseline frame.
2. Validates the model frame against the Task Frame schema.
3. Requires exact authenticated raw request, turn references, trusted context references, and untrusted data references.
4. Compiles Acceptance and Clarification contracts and runs full semantic validation.
5. Requires valid Core routing with no banned projection fields.
6. Records whether the model candidate would have been eligible.
7. Always returns the deterministic frame as authoritative while mode is `shadow`.

The output contract is `schemas/interpreter/shadow-parser-decision.schema.json`. Shadow evidence is recorded under `evals/results/*.shadow-parser.yaml`. A later guarded or active mode must require a passing repeated-run promotion record; it must not be enabled by prompt compliance alone.

## Model Inference Boundary

Full model-authored Task Frames are no longer the preferred integration contract. `schemas/interpreter/task-frame-inference.schema.json` limits model output to semantic classification:

- normalized goal, work types, and autonomy
- scope, posture, artifacts, and ambiguity
- bounded constraints
- consequence and reversibility classification
- advisory candidate domains

`tools/compile_model_inference.py` deterministically supplies all authority-controlled fields: source projection, identity, project ID, provenance, permission and confirmation records, lifecycle blocking, acceptance reference, and final Task Frame validation. The packet contract in `schemas/interpreter/parser-inference-packet.schema.json` exposes authenticated intent plus bounded trusted and untrusted references without copying retrieved content.

This boundary does not make model inference trusted. Incorrect semantic classification can still fail benchmarks. It prevents the model from manufacturing authority or corrupting source provenance and makes structured decoding practical with a smaller schema.
```
