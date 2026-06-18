# Nemotron Parser Candidate Runtime Failure

## Metadata

- `task_id`: parser-nemotron-super-v0
- `date`: 2026-06-18
- `domain`: core
- `benchmark_ref`: `evals/fixtures/parser-benchmark/`
- `runtime`: Kilo Code
- `model`: `kilo/nvidia/nemotron-3-super-120b-a12b:free`
- `prompt_version`: `interpreter-parser-benchmark.v0`

## Runtime Outcome

- `status`: timeout
- `timeout_status`: upstream_idle_timeout
- `actual_latency`: unknown
- `changed_artifacts`: none reported
- `output_path`: none

## Evidence

The user reported both `tool execution aborted` and an upstream idle failure. No candidate file was produced, so the run cannot be scored or compared for promotion.

## Recovery

Do not count this as a model-quality result. Any retry must use a fresh thread, a smaller packet or early checkpoint, and exact runtime metadata.
