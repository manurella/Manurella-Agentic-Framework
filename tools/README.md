# Tools

Local tools that enforce Manurella framework structure.

## Self Check

Run the full local framework smoke suite:

```powershell
python tools/self_check.py --repo .
```

It runs the framework validator, trust-partition and Interpreter fixtures, Core/Brain/runtime packet fixtures, memory promotion/application/retrieval fixtures, Kilo exporter and session-projection checks, result-record and Mentor helper smokes, comparator smokes, and removes its temporary records.

## Trusted Input Partitioner

Validate trusted input envelopes and run the adversarial partition suite:

```powershell
python tools/partition_trusted_input.py --repo . --fixtures
```

Partition one envelope:

```powershell
python tools/partition_trusted_input.py --repo . --input path/to/envelope.yaml
```

The partitioner derives authority from item kind, origin, and verified authentication evidence. Content cannot grant itself authority. System/runtime policy, authenticated user instruction, prior confirmed state, and untrusted data remain separate; unauthorized control claims are quarantined, and task intake without an authenticated user instruction is blocked. The result contains references and findings, not copied content.

## Task Frame Parser Baseline

Run the conservative natural-language parser fixtures:

```powershell
python tools/parse_task_frame.py --repo . --fixtures
```

Compile one validated trusted input envelope into a schema-valid Task Frame:

```powershell
python tools/parse_task_frame.py --repo . --input path/to/envelope.yaml --locale en-LK
```

The parser consumes only authenticated user-instruction content as intent. Trusted policy and prior state become context references; retrieved, tool, model, and artifact content remain untrusted references and cannot alter the goal. The baseline recognizes bounded work types, project posture, file artifacts, explicit constraints, coarse domains, vague requests, and high-risk action verbs. It fails closed on unauthenticated task intake and requires permission plus confirmation for external or destructive action.

This is a deterministic reference baseline and security regression oracle, not a claim of general natural-language understanding. Unknown language is preserved as user-authored intent and conservatively classified; production parsing still needs schema-constrained model output, semantic validation, and baseline-vs-guided evaluations.

## Acceptance Contract Compiler

Run the end-to-end acceptance fixtures:

```powershell
python tools/compile_acceptance_contract.py --repo . --fixtures
```

Compile one trusted input envelope into a complete validated Interpreter bundle:

```powershell
python tools/compile_acceptance_contract.py --repo . --input path/to/envelope.yaml --locale en-LK
```

The compiler runs trust partitioning and Task Frame parsing, derives required outcomes and artifacts, constraints, forbidden results, quality thresholds, evidence requirements, verification checks, stop/escalation conditions, signoff, and one Clarification Decision. Consequential or irreversible work requires confirmation and authenticated human signoff. Open material uncertainty produces a blocking clarification question.

Every successful fixture is validated by the canonical Interpreter semantic gate and compiled through the Core routing schema. The compiler is deterministic and conservative: it does not invent domain-specific tests or claim that generic rubric language replaces specialist acceptance criteria.

## Task Frame Parser Evaluator

Run the no-network evaluator self-test:

```powershell
python tools/evaluate_task_frame_parser.py --repo . --self-test
```

Write a deterministic baseline record:

```powershell
python tools/evaluate_task_frame_parser.py --repo . --run-id parser-baseline-v0 --baseline-only
```

Compare a captured model candidate stored under `evals/results/`:

```powershell
python tools/evaluate_task_frame_parser.py --repo . --run-id parser-candidate-v1 --candidate evals/results/parser-candidate-v1.parser-candidate.yaml
```

The evaluator uses `evals/fixtures/parser-benchmark/`, not the parser's development fixtures. It measures Task Frame schema validity, complete bundle semantic validity, Core routing validity, critical-field accuracy, and safety-critical pass rate. A safety failure vetoes promotion. Candidate and result shapes are defined under `schemas/evals/`, and result records are written only under `evals/results/`.

Use `evals/prompts/interpreter-parser-benchmark.md` to capture candidates from any runtime. The evaluator verifies schema, exact authenticated raw request and turn references, exact trusted and untrusted reference projection, Interpreter semantics, Core routing, critical-field accuracy, and safety. No external model currently passes the complete repeated-run gate.

The legacy full-frame prompt is deprecated for promotion because its source fixtures exposed gold `expected_fields`. Keep historical results as diagnostic records only.

## Parser Repeated-Run Promotion

Aggregate independent parser eval records into one promotion decision:

```powershell
python tools/evaluate_parser_promotion.py --repo . --promotion-id parser-stepfun-v2-promotion --eval evals/results/parser-stepfun-v2.parser-eval.yaml --eval evals/results/parser-stepfun-v2-repeat-1.parser-eval.yaml
```

The tool requires at least two records for the exact same model and prompt version. Every supplied run must have passed its individual parser gate. Mixed model/prompt identities, duplicate records, insufficient runs, or any failed repeat block promotion. Results are written under `evals/results/*.parser-promotion.yaml`.

## Shadow Task Frame Parser

Evaluate a captured model Task Frame without allowing it to control execution:

```powershell
python tools/shadow_parse_task_frame.py --repo . --input evals/fixtures/parser-benchmark/paraphrased-edit.yaml --candidate-run evals/results/parser-stepfun-v2-repeat-1.parser-candidate.yaml --case-id parser-benchmark.paraphrased-edit
```

The adapter always keeps the deterministic rule parser authoritative. It validates candidate schema, exact authenticated source projection, untrusted-data references, full Interpreter semantics, and Core routing. The decision reports whether the model candidate would have been eligible, while missing or invalid candidates are rejected without repair. Shadow mode cannot activate model output even when it is valid.

Run its adversarial smoke suite with:

```powershell
python tools/shadow_parse_task_frame.py --repo . --self-test
```

Evaluate a complete captured run through shadow mode:

```powershell
python tools/evaluate_shadow_parser.py --repo . --run-id parser-shadow-run --candidate-run evals/results/parser-candidate.parser-candidate.yaml --promotion evals/results/parser-model.parser-promotion.yaml
```

Guarded-mode design is recommended only when every corpus case is shadow-eligible and the repeated-run promotion record passes.

## Model Inference Compiler

Create a bounded model packet from a trusted input envelope:

```powershell
python tools/compile_model_inference.py --repo . --input evals/fixtures/parser-benchmark/indirect-injection.yaml --emit-packet
```

Compile a schema-valid semantic inference into a complete Task Frame and evaluate it in shadow mode:

```powershell
python tools/compile_model_inference.py --repo . --input path/to/envelope.yaml --inference path/to/task-frame-inference.yaml --model exact-model --prompt-version task-frame-inference.v0
```

The model inference contract excludes source, identity, provenance, permissions, confirmations, lifecycle, and tool actions. The deterministic compiler binds those fields, derives approval requirements and blocking state, then sends the assembled frame through the existing shadow validator. This prevents authentication evidence or retrieved content from becoming authority merely because a model emitted it.

After repeated-run promotion passes, guarded mode may select a validated inference candidate:

```powershell
python tools/compile_model_inference.py --repo . --input path/to/envelope.yaml --inference-run evals/results/promoted.inference-candidate.yaml --case-id case.id --mode guarded --promotion evals/results/promoted.parser-promotion.yaml
```

Guarded mode requires an exact model and prompt-version match with a passing promotion record. The assembled candidate must still pass schema, trust, semantic, and Core-routing validation for the current request. Any promotion mismatch or validation failure selects the deterministic rule baseline. Shadow mode remains the default.

Replay promoted captures through guarded selection and record representative observations:

```powershell
python tools/evaluate_guarded_parser.py --repo . --observation-id guarded-replay --candidate-run evals/results/first.inference-candidate.yaml --candidate-run evals/results/repeat.inference-candidate.yaml --promotion evals/results/promoted.parser-promotion.yaml --output evals/results/guarded-replay.guarded-observation.yaml
```

Guarded replay results use `representative_replay` evidence. They verify selection and fallback mechanics but cannot authorize default activation because benchmark replays are not independently captured live requests. The result contract therefore fixes `default_mode` to `shadow` and records `insufficient_live_evidence`.

For an authorized, sensitivity-reviewed live request, first obtain semantic YAML with `evals/prompts/interpreter-guarded-live-capture.md`, then record the guarded decision:

```powershell
python tools/record_guarded_live_observation.py --repo . --observation-id live-001 --input path/to/live-envelope.yaml --inference path/to/live-inference.yaml --model stepfun/step-3.7-flash:free --prompt-version interpreter-inference-benchmark.v1 --sensitivity-review non_sensitive --output evals/results/live-001.guarded-live-observation.yaml
```

The result stores a SHA-256 request fingerprint and source references, not copied request text or the selected Task Frame. Human review defaults to `pending`; a completed review requires `--review-status pass|fail`, `--reviewer`, and at least one `--review-note`. Individual live records always keep the default parser mode at `shadow`. Activation thresholds remain research- and review-required rather than being inferred from one successful request.

## Blinded Model Inference Evaluation

Regenerate blinded packets from the private gold corpus:

```powershell
python tools/evaluate_model_inference.py --repo . --prepare-packets --overwrite
```

Evaluate a captured inference candidate:

```powershell
python tools/evaluate_model_inference.py --repo . --run-id inference-run-v0 --candidate evals/results/inference-run-v0.inference-candidate.yaml
```

Models read only `evals/fixtures/parser-inference-benchmark/`. The evaluator privately joins those case IDs to `evals/fixtures/parser-benchmark/` for scoring, compiles each inference through the deterministic authority boundary, and then applies the existing schema, trust, semantic, routing, accuracy, and safety gates.

The first blinded StepFun v0 result is `evals/results/stepfun-inference-v0.parser-eval.yaml`: 27/37 critical fields, 2/2 safety cases, and 2/6 semantic and routing passes. It is a failed promotion result and the baseline for inference prompt v1.

The first blinded StepFun v1 result is `evals/results/stepfun-inference-v1.parser-eval.yaml`: 26/37 critical fields with 100% schema, semantic, routing, and safety validity. It passes the individual evaluator but remains unpromoted until an unchanged independent v1 repeat passes the repeated-run gate.

## Brain Workspace Compiler

Compile a validated Interpreter fixture through Core routing into Brain State, a volatile Active Workspace, and a bounded Context Packet:

```powershell
python tools/compile_brain_workspace.py --repo . --input evals/fixtures/interpreter/project.yaml
python tools/compile_brain_workspace.py --repo . --fixtures
```

The compiler carries only provenance-approved trusted references into the privileged context packet. Raw requests, transcript references, untrusted-data references, tool payloads, and reasoning traces are excluded. The v0 cycle and context budgets are transparent regression baselines, not learned confidence or optimality claims.

Advance compiled state through typed observations and exercise the control-loop fixtures:

```powershell
python tools/advance_brain_cycle.py --repo . --workspace path/to/workspace-bundle.yaml --observations path/to/observation-events.yaml
python tools/advance_brain_cycle.py --repo . --fixtures
```

Only trusted runtime and authenticated user observations revise privileged state. External and model-inferred observations are quarantined without copying their statement text. The governor selects direct, reactive, hierarchical, repair, replan, stop, or escalation behavior from explicit verification, progress, safety, and budget state; it does not emit an unsupported confidence score.

Compile a Brain cycle result into a portable runtime operation packet:

```powershell
python tools/compile_runtime_operation.py --repo . --cycle-result path/to/brain-cycle-result.yaml --prior-packet-ref packet://previous
python tools/compile_runtime_operation.py --repo . --fixtures
```

The compiler reads the selected agent's checked-in permissions and intersects them with packet class and mode. It never promotes model-inferred tool hints into authority. Only `allow` actions are executable; both approval-required (`ask`) and denied actions remain explicit in `blocked_actions`, with their exact status preserved in `action_policy`. Recovery packets resume from checkpoint and artifact references rather than restarting.

Compile trusted task intake through Interpreter, Core, Brain, memory retrieval, and the operation boundary:

```powershell
python tools/compile_runtime_session.py --repo . --input path/to/trusted-envelope.yaml --compiled-at 2026-06-22T10:00:00Z
python tools/compile_runtime_session.py --repo . --fixtures
```

The runtime session bundle excludes the full Interpreter bundle and banned transcript/reasoning fields. It contains lineage IDs, a principal-filtered memory packet, the permission-bounded operation packet, and an explicit list of controls still unenforced before adapter projection. Compilation performs no provider call, runtime action, memory write, or Atlas mutation.

Project validated runtime sessions into strict per-session Kilo agents without invoking Kilo:

```powershell
python adapters\kilo\project_runtime_session.py --repo . --fixtures
python adapters\kilo\project_runtime_session.py --repo . --session path\to\runtime-session.yaml --write-agent
```

The projector lowers confirmation-required authority to denial, narrows unscoped edit/shell/browser actions, emits only canonical `.kilo/agents/` artifacts, and marks its CLI argv as interactive and unexecuted.

Evaluate a typed durable-memory or Atlas proposal without mutating canonical state:

```powershell
python tools/evaluate_memory_proposal.py --repo . --proposal path/to/memory-proposal.yaml
python tools/evaluate_memory_proposal.py --repo . --fixtures
```

The evaluator checks provenance, source trust, exact structured-claim conflicts, supersession references, write authorization, human review, repeated support, and benchmark evidence. Untrusted content is quarantined; session material can remain episodic; durable and Atlas records are emitted only after their v0 promotion requirements pass. Evaluation never writes `cognition/memory.yaml` or `cognition/graph.yaml`.

Apply a reviewed non-Atlas decision to the canonical file store:

```powershell
python tools/apply_memory_decision.py --repo . --decision path/to/memory-decision.yaml --applied-at 2026-06-21T10:00:00Z --apply
python tools/apply_memory_decision.py --repo . --fixtures
```

The writer is dry-run by default and atomically replaces the store only with `--apply`. It validates decision/store contracts, rejects unresolved conflicts and invalid supersession, and treats exact replay as an idempotent no-op. Atlas decisions require their separate graph mutation boundary.

Retrieve bounded, current memory for one principal and scope:

```powershell
python tools/retrieve_memory.py --repo . --as-of 2026-06-21T10:00:00Z --principal-ref user.local --scope-kind project --scope-ref project.manurella --type user_preference --type project_state
python tools/retrieve_memory.py --repo . --fixtures
```

Retrieval excludes inactive, expired, review-overdue, principal-mismatched, scope-mismatched, wrong-type, and contradictory records. The packet reports each omission and orders eligible records by explicit evidence class, recency, then stable ID; it does not claim learned relevance.

Apply a reviewed Atlas decision through the guarded graph boundary:

```powershell
python tools/apply_atlas_decision.py --repo . --decision path/to/atlas-decision.yaml --applied-at 2026-06-21T10:00:00Z --apply
python tools/apply_atlas_decision.py --repo . --fixtures
```

The writer is dry-run by default and can modify only `cognition/graph.yaml`. V0 supports lifecycle changes and repository-contained evidence additions for existing nodes or edges. It rejects broader predicates, invalid status vocabularies, missing/ambiguous targets, path escapes, and candidates that fail graph validation. It does not add, remove, merge, or rewire graph entities.

## Interpreter Contract Validator

Validate the Task Frame and Acceptance Contract schemas, semantic invariants, Family A-E projections, project postures, and representative fixtures:

```powershell
python tools/validate_interpreter.py --repo .
```

Validate one Interpreter bundle directly:

```powershell
python tools/validate_interpreter.py --repo . --input evals/fixtures/interpreter/quick-task.yaml
```

The validator checks the versioned JSON Schemas under `schemas/interpreter/`, then applies invariants that JSON Schema alone cannot express: reference reciprocity, revision lineage, project context, uncertainty state, clarification blocking, audit non-mutation, consequential confirmation, permission records, freshness, and critical rubric references. It also derives the legacy Family A-E label and project posture for adapter compatibility.

## Core Routing Compiler

Compile one validated Interpreter bundle into a routing decision and optional bounded handoff packet:

```powershell
python tools/compile_core_packet.py --repo . --input evals/fixtures/interpreter/quick-task.yaml
```

Run routing expectations across all positive and negative Interpreter fixtures:

```powershell
python tools/compile_core_packet.py --repo . --fixtures
```

The compiler validates before routing, keeps conversation and blocked decisions in Core, selects one primary specialist for executable work, records secondary domains, and emits `schemas/core/routing-decision.schema.json`. Projection output forbids raw request, turn, and untrusted-data fields.

## Framework Validator

Run from the repository root:

```powershell
python tools/validate_framework.py --repo .
```

The validator checks:

- cognitive graph YAML
- duplicate graph node and edge IDs
- graph edge references
- evidence paths
- agent frontmatter shape
- agent permission values
- accepted-agent promotion minimums
- eval hygiene warnings

Errors fail validation. Warnings identify known quality risks that should be fixed before promotion or final reporting.

## Result Record Helper

Create a skeleton result record under `evals/results/`:

```powershell
python tools/create_result_record.py --repo . --task-id mentor-interview-study-run --domain mentor --kind mentor --benchmark-ref domains/mentor/benchmarks/README.md#interview-study-benchmarks
```

The helper refuses fixture output paths by construction and keeps eval records in the correct directory.

## Learner State Helper

Create an initial Mentor learner-state file:

```powershell
python tools/create_learner_state.py --repo . --learner-id rehan --target-role "Frontend Developer" --weak-topics "state ownership, accessibility" --output evals/results/rehan-learner-state.yaml --overwrite
```

The file follows `domains/mentor/learner-state-schema.md` and starts uncertain by design. It records weak topics as self-reported diagnostics, not mastered facts.

## Result Comparator

Compare baseline and guided records:

```powershell
python tools/compare_results.py --baseline evals/results/baseline-mentor-interview-study.md --guided evals/results/guided-mentor-interview-study-standard-high.md --threshold 0.5
```

The comparator reads shared numeric score fields, computes average delta, and reports whether the guided run met the promotion signal threshold.

## Mentor Packet Helper

Create a copy-paste Mentor interview-study packet:

```powershell
python tools/create_mentor_packet.py --repo . --target-role "Frontend Developer" --available-time "45 minutes today" --topic "state ownership" --weak-topics "React state, cache invalidation" --learner-state evals/results/rehan-learner-state.yaml
```

The helper fills the Manurella runtime packet, Mentor framework references, weak-runtime checkpoint, session protocol, and output contract.

## Mentor Output Scorer

Score a captured Mentor response against the v0 Mentor gate:

```powershell
python tools/score_mentor_output.py evals/results/captured-mentor-output.md --min-score 7
```

This is a deterministic structure/evidence check. It does not prove domain correctness, but it quickly flags missing target skill, active recall, rubric, feedback, learner-state update, next packet, and self-check.

## Mentor Run Recorder

Score a captured Mentor response and create a result record:

```powershell
python tools/record_mentor_run.py --repo . --task-id guided-mentor-state-ownership --output-text evals/results/captured-mentor-output.md --model "MODEL_NAME" --actual-latency "8 minutes" --timeout-status none --overwrite
```

This writes `evals/results/guided-mentor-state-ownership.md` through the result-record helper, embeds the scorer report as verification evidence, and fills comparison-ready 1-5 score fields from the Mentor gate score.
