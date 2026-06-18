# Tools

Local tools that enforce Manurella framework structure.

## Self Check

Run the full local framework smoke suite:

```powershell
python tools/self_check.py --repo .
```

It runs the framework validator, trust-partition fixtures, Interpreter contract fixtures, Core routing projection fixtures, Kilo exporter dry-run, result-record helper smoke, Mentor packet helper smoke, Mentor output scorer smoke, Mentor run recorder smoke, comparator smoke, and removes its temporary smoke records.

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

Use `evals/prompts/interpreter-parser-benchmark.md` to capture candidates from any runtime. StepFun 3.7 Flash with prompt v2 is the first candidate to pass this evaluator, recorded in `evals/results/parser-stepfun-v2.parser-eval.yaml`. One passing run is benchmark qualification, not automatic production adoption; repeat the run independently and retain deterministic semantic validation and fallback in any runtime integration.

## Parser Repeated-Run Promotion

Aggregate independent parser eval records into one promotion decision:

```powershell
python tools/evaluate_parser_promotion.py --repo . --promotion-id parser-stepfun-v2-promotion --eval evals/results/parser-stepfun-v2.parser-eval.yaml --eval evals/results/parser-stepfun-v2-repeat-1.parser-eval.yaml
```

The tool requires at least two records for the exact same model and prompt version. Every supplied run must have passed its individual parser gate. Mixed model/prompt identities, duplicate records, insufficient runs, or any failed repeat block promotion. Results are written under `evals/results/*.parser-promotion.yaml`.

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
