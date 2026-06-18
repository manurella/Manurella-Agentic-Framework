# Tools

Local tools that enforce Manurella framework structure.

## Self Check

Run the full local framework smoke suite:

```powershell
python tools/self_check.py --repo .
```

It runs the framework validator, Interpreter contract fixture suite, Kilo exporter dry-run, result-record helper smoke, Mentor packet helper smoke, Mentor output scorer smoke, Mentor run recorder smoke, comparator smoke, and removes its temporary smoke records.

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
