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
- Stop at packet boundaries. Do not let Kilo continue into repairs or documentation unless the packet asks for it.

## First Mentor Test

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
7. Use `tools/create_result_record.py` to create two result records.
8. Use `tools/compare_results.py` to compare them.

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
