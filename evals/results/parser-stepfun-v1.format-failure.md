# StepFun Parser V1 Format Failure

## Metadata

- `task_id`: parser-stepfun-v1
- `date`: 2026-06-18
- `domain`: core
- `benchmark_ref`: `evals/fixtures/parser-benchmark/`
- `runtime`: Kilo Code
- `model`: `stepfun/step-3.7-flash:free`
- `prompt_version`: `interpreter-parser-benchmark.v1`
- `candidate_path`: `evals/results/parser-stepfun-v1.parser-candidate.yaml`

## Outcome

- `status`: fail
- `promotion`: vetoed
- `failure_gate`: candidate YAML parsing
- `evaluator_result`: no parser-eval record produced because the candidate could not be loaded

## Evidence

The candidate used a flow-style YAML sequence with an unquoted question:

```yaml
unresolved_routing_questions: [Which project should be resumed?]
```

PyYAML rejected the document at line 383 because `?` has YAML syntax meaning in that context.

## Decision

Do not repair or score the captured candidate. Preserve it as raw model evidence. The next prompt version requires block-style sequences and quoted punctuation-bearing scalars before the same StepFun candidate is rerun.
