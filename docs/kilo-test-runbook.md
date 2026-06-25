# Kilo Test Runbook

## Purpose

This runbook keeps Kilo tests small, measurable, and useful for Manurella. Use it whenever testing generated `.kilo/agents` files.

## Before Testing

Run from the repository root:

```powershell
python tools/validate_framework.py --repo .
python adapters/kilo/export_agents.py --all --output .kilo/agents --mode standard --effort high --dry-run
```

Expected:

- validator has zero errors
- Kilo exporter dry-run completes
- warnings are recorded, not ignored

## Runtime Rules

- Use runtime packets from `specs/runtime-packet-protocol.md`.
- Run baseline and guided outputs in separate Kilo threads.
- Do not ask the same run to create result records.
- Capture exact model, runtime, mode, effort, elapsed time, timeout status, and changed artifacts.
- For runtime-session projection runs, compile a `runtime-adapter-evidence-bundle.v0` after normalizing the Kilo capture.
- If the previous run looked generic, shallow, or confused, add `specs/weak-runtime-compensation.md` to the prompt and require evidence, assumptions, narrow target, output, and self-check.
- Stop at packet boundaries. Do not let Kilo continue into repairs or documentation unless the packet asks for it.

## First Mentor Test

For immediate personal study, use `docs/mentor-interview-quickstart.md`.

For framework evaluation, use the benchmark flow below.

Use:

- `evals/prompts/mentor-interview-study-packet.md`
- `domains/mentor/mentor-quality-gate.md`
- generated `.kilo/agents/macro-placement-director.md`
- generated `.kilo/agents/curriculum-planner-sequencer.md`
- generated `.kilo/agents/targeted-practice-drillmaster.md`

Sequence:

1. Fill the prompt fields.
2. Run baseline prompt.
3. Save output.
4. Start a fresh Kilo thread.
5. Run guided Mentor prompt.
6. Save output.
7. Use `tools/record_mentor_run.py` for guided Mentor outputs when captured text is available.
8. Use `tools/create_result_record.py` for baseline or unscored records.
9. Use `tools/compare_results.py` to compare them.

For a guided Mentor output saved at `evals/results/captured-mentor-output.md`:

```powershell
python tools/record_mentor_run.py --repo . --task-id guided-mentor-interview-study-standard-high --output-text evals/results/captured-mentor-output.md --model "MODEL_NAME" --actual-latency "LATENCY" --timeout-status none --overwrite
```

## First Build Frontend Test

Use:

- `evals/prompts/build-frontend-accessibility-visual-qa.md`
- `domains/build/frontend-quality-gate.md`
- generated `.kilo/agents/build-orchestrator.md`

Sequence:

1. Run baseline review packet.
2. Run guided review packet in a fresh Kilo thread.
3. Create result records in `evals/results/`.
4. Compare baseline and guided records.
5. Record any timeout or screenshot-inspection failure.

## Result Creation

Example:

```powershell
python tools/create_result_record.py --repo . --task-id baseline-mentor-interview-study --domain mentor --kind mentor --benchmark-ref domains/mentor/benchmarks/README.md#interview-study-benchmarks
python tools/create_result_record.py --repo . --task-id guided-mentor-interview-study-standard-high --domain mentor --kind mentor --benchmark-ref domains/mentor/benchmarks/README.md#interview-study-benchmarks
```

Then fill missing fields from the saved Kilo outputs.

## Runtime Adapter Evidence

For typed runtime-session tests, keep these artifacts separate:

1. Brain workspace checkpoint.
2. Runtime session bundle.
3. Kilo session projection.
4. Normalized execution capture with stream/model digests.
5. Runtime adapter evidence bundle.
6. Human-readable result record under `evals/results/`.

After the Kilo run is normalized into `execution-capture.v0`, compile the evidence bundle:

```powershell
python tools/compile_adapter_evidence.py --repo . --workspace path/to/workspace-bundle.yaml --session path/to/session.yaml --projection path/to/projection.yaml --capture path/to/capture.yaml --attest-runtime-capture --model "exact-model-name" --mode standard --effort high --adapter-version runtime-session-projection.v0 --prompt-version runtime-session-projection.v0
```

Do not use `model: unknown` for new live evidence. If the exact model is unavailable, record the run as diagnostic prose only, not promotion evidence.

## Comparison

```powershell
python tools/compare_results.py --baseline evals/results/baseline-mentor-interview-study.md --guided evals/results/guided-mentor-interview-study-standard-high.md --threshold 0.5
```

Promotion signal is only a signal. It does not promote an agent by itself. Promotion still requires `specs/promotion-gates.md`.

## Timeout Handling

If Kilo times out:

1. Save whatever output exists.
2. Record `timeout_status`.
3. Do not rerun the full prompt.
4. Resume with a narrower runtime packet.
5. Prefer lowering delegation before lowering quality gates.

If the failure is stream or upstream idle related, require an early checkpoint in the next prompt before deeper work:

```text
Before the main answer, output:
1. Evidence read
2. Assumptions
3. Narrow target

Then continue only if the packet still fits the timebox.
```
