# Evaluation Runs

This directory records benchmark and smoke-test runs for Manurella.

The purpose is to turn runtime behavior into evidence:

- what task was attempted
- which runtime, model, adapter, and execution profile were used
- how long the run took
- whether it timed out
- what changed
- what verification happened
- what should be tuned next

## Directory Layout

```text
evals/
  README.md
  results/
    build-kilo-smoke.md
  templates/
    result-record.md
```

## Rules

- Record failed runs, timeouts, and partial runs. They are useful signal.
- Do not treat a subjective impression as a score without notes.
- Do not overwrite earlier results after tuning. Add a new dated run or section.
- Record unknown fields as `unknown`, not guessed values.
- Keep raw transcripts outside the result file if they are long; link or summarize them.

## Minimum Record

Each run should include:

- `task_id`
- runtime and model
- domain and agent/profile
- adapter version or commit
- prompt summary
- latency and timeout status
- changed artifacts
- verification evidence
- scores or qualitative notes
- failure modes and next tuning action

The canonical field list is defined in `specs/kernel.md` and `specs/runtime-control.md`.
