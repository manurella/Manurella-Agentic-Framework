# Manurella Master Execution Plan

## Purpose

This plan is the delivery spine for Manurella v0. It turns the research, legacy Family System lessons, domain packs, cognitive graph, runtime modes, and eval loop into one sequence of work.

The target is state-of-the-art output behavior for the available model/runtime, measured by baseline-vs-guided evals. Do not call the framework state of the art by assertion. Earn the claim through architecture, evidence, and repeated failure-driven improvement.

## Hard Constraints

- User time is limited; every checkpoint must produce usable artifacts.
- Kilo/free-model runs are unstable; long silent workflows must be split into checkpointed packets.
- The framework must remain runtime-agnostic; Kilo is the first test adapter, not the architecture.
- Research matters, but research must become specs, agents, evals, tools, or graph updates.
- Legacy Family System v13 is evidence, not canonical source. Mine it for useful mechanisms; do not recreate the monolith.

## North Star

Manurella improves output by combining:

1. A small portable kernel.
2. Domain packs with bounded agents, skills, and checklists.
3. A cognitive graph that maps relationships, failures, evals, and routing.
4. Runtime control through modes, effort levels, step budgets, delegation budgets, and verifier gates.
5. Eval-driven reinforcement loops.
6. Adapter-specific execution packets that prevent runtime weakness from corrupting architecture.

## Workstreams

### W1. Kernel And Doctrine

Goal: lock the durable rules that every runtime and domain inherits.

Artifacts:

- `specs/kernel.md`
- `specs/brain-cognitive-kernel.md`
- `specs/interpreter-task-model.md`
- `schemas/interpreter/task-frame.schema.json`
- `schemas/interpreter/acceptance-contract.schema.json`
- `schemas/interpreter/trusted-input-envelope.schema.json`
- `schemas/interpreter/trust-partition.schema.json`
- `schemas/core/routing-decision.schema.json`
- `tools/partition_trusted_input.py`
- `tools/parse_task_frame.py`
- `tools/compile_acceptance_contract.py`
- `tools/evaluate_task_frame_parser.py`
- `schemas/evals/parser-candidate-run.schema.json`
- `schemas/evals/parser-eval-result.schema.json`
- `tools/validate_interpreter.py`
- `tools/compile_core_packet.py`
- `specs/core-operating-protocol.md`
- `specs/agent-schema.md`
- `specs/runtime-control.md`
- `docs/agent-authoring-doctrine.md`
- `docs/research-doctrine.md`

Acceptance:

- Every accepted agent has typed inputs, output contract, permissions, mode behavior, effort behavior, failure modes, and eval refs.
- The main orchestrator uses Family-level task classification, handoff packets, quality review, and recovery rules.
- Fast Mode and Standard Mode are explicit workflow envelopes.
- Effort levels are reasoning-depth policies, not vague quality labels.
- Interpreter contracts pass structural, semantic, compatibility-projection, and negative fixture checks.
- Interpreter input is provenance-bound and partitioned by derived authority before parsing.
- A conservative parser baseline compiles authenticated user intent into schema-valid Task Frames and blocks unsafe authority promotion.
- A deterministic Acceptance Contract compiler completes validated Interpreter bundles and proves they compile through Core routing.
- A runtime-neutral parser evaluator compares the deterministic baseline with captured model candidates using structural, semantic, routing, accuracy, and safety gates.
- Core compiles validated bundles into direct, blocked, or delegated routing decisions without transcript leakage.

### W2. Cognitive Graph

Goal: make framework memory navigable instead of buried in prose.

Artifacts:

- `docs/atlas-constitution.md`
- `docs/manurella-root-ontology.md`
- `cognition/graph.yaml`
- `cognition/mindmap.md`
- graph update notes inside eval records

Acceptance:

- Work proceeds through connected depth-first vertical slices that end in implementation and evidence.
- Every active agent, mode, effort, eval, and recurring failure has a graph node.
- Promotion from draft to accepted requires graph evidence.
- Failures from evals create or update failure-mode nodes.

### W3. Domain Packs

Goal: define Core, Build, Muse, Pixel, and Mentor as modular domain systems.

Artifacts:

- `domains/core/`
- `domains/build/`
- `domains/muse/`
- `domains/pixel/`
- `domains/mentor/`

Acceptance:

- Core has a main routing orchestrator that can select the correct specialist domain.
- Each domain has a lead/orchestrator and specialist boundaries.
- Each domain has at least two benchmarks before any serious promotion claim.
- Each specialist is authored as agent, skill, or checklist based on actual authority needed.

### W4. Runtime Adapter

Goal: compile portable specs into usable Kilo behavior while preserving boundaries.

Artifacts:

- `adapters/kilo/export_agents.py`
- `specs/kilo-adapter.md`
- `.kilo/agents/` generated outputs
- runtime packet protocol

Acceptance:

- Adapter records unsupported controls instead of pretending they are enforceable.
- Kilo prompts are short enough to avoid runaway delegation.
- Timeout recovery resumes from artifacts, not from scratch.

### W5. Eval System

Goal: turn every serious claim into a scored comparison.

Artifacts:

- `evals/templates/result-record.md`
- `evals/prompts/`
- `evals/results/`
- fixtures and screenshots when needed

Acceptance:

- Every run records model, runtime, mode, effort, latency, timeout status, changed artifacts, tools, evidence, and failure notes.
- Baseline and guided outputs are recorded separately.
- Promotion requires repeated wins, not one successful run.

### W6. Tooling And MCP

Goal: add tooling only where it enforces quality or saves repeated manual work.

Candidate tools:

- eval record generator
- Kilo run packet generator
- screenshot/visual QA helper
- prompt compiler
- graph validator
- trace logger

Acceptance:

- Tool has a clear input/output contract.
- Tool reduces failure rate, latency, or manual burden.
- Tool output is recorded in eval artifacts.

## Immediate Critical Path

### Checkpoint A: Establish A Usable Baseline Router

Finish first because the framework is unusable without a main boot path.

Tasks:

1. Add root runtime instructions and the Manurella brain boot file.
2. Add a Core domain with the main Manurella Orchestrator.
3. Export the orchestrator and all specialist leads to Kilo.
4. Validate framework structure and run self-check.
5. Use the orchestrator as the default entrypoint for future Kilo tests.

Done when:

- `AGENTS.md`, `MANURELLA.md`, and `domains/core/agents/manurella-orchestrator.md` exist.
- Kilo export includes `manurella-orchestrator.md`.
- Validator and self-check pass.

### Checkpoint B: Stabilize The Build Testbed

Finish first because Build gives the clearest deterministic evidence.

Tasks:

1. Clean the current frontend eval into proper fixture and result-record separation.
2. Add a frontend QA gate that requires screenshot inspection when screenshots exist.
3. Add runtime packet instructions to prevent Kilo timeout and fake long reasoning.
4. Run a baseline and guided frontend QA eval with exact timing and model metadata.
5. Update `cognition/graph.yaml` with the result and failure modes.

Done when:

- `evals/results/` contains separate baseline and guided result records.
- The guided run is comparable to baseline on the same fixture.
- Timeout, screenshot, and verification evidence are explicit.

### Checkpoint C: Promote The First Build/Frontend Components

Tasks:

1. Keep `frontend-architect`, `accessibility-auditor`, `visual-qa-specialist`, `state-flow-specialist`, and `performance-reviewer` as draft until evidence exists.
2. Author them as structured specs only after the eval shows which boundaries matter.
3. Promote only the components that measurably improve findings, verification, or repair quality.

Done when:

- At least two frontend tasks show guided improvement over baseline.
- No promoted node has vague authority or missing permissions.

### Checkpoint D: Mentor Learning Agent Foundation

Tasks:

1. Define the Mentor lead and learning-state model.
2. Separate diagnosis, curriculum sequencing, comprehensible input, drill generation, conversation, and feedback.
3. Add a learner-state artifact that can help the user study without making false mastery claims.
4. Create interview-study benchmark tasks.

Done when:

- Mentor can produce a study plan, teach a concept, diagnose a failure, and generate practice with answer keys.
- Results are scored against baseline teaching output.

### Checkpoint E: Muse And Pixel Stabilization

Tasks:

1. Muse: separate story architecture, scene drafting, line editing, continuity, and critique.
2. Pixel: separate art direction, prompt syntax, continuity, repair, and judging.
3. Add benchmark fixtures for story and image-prompt tasks.

Done when:

- Each domain has at least two evals and a clear improvement hypothesis.

## Research Intake Protocol

Use external research when:

- a domain boundary is unclear
- a benchmark standard is missing
- a tool or model behavior is version-sensitive
- the framework risks copying outdated practice

Research must return:

- claims
- sources
- applicable architecture patterns
- failure modes
- what to adopt now
- what to defer
- eval implications

Research does not become accepted behavior until translated into specs and tested.

## Today Target

By the first serious checkpoint today, the repository should contain:

1. Root runtime boot files.
2. A main Manurella routing orchestrator.
3. A runtime packet protocol for Kilo.
4. A Build/frontend QA gate produced from the failed eval.
5. A cleaned eval instruction that prevents mixed fixture/result artifacts.
6. User-ready Kilo agents and prompts for the next test.

This is not v0 complete. It is the first usable control spine for getting to v0 without wasting runs.
