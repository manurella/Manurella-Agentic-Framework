# Build Kilo Smoke Results

## Purpose

These runs test whether the Build domain can produce small documentation edits through Kilo without scope expansion, generated-file edits, or timeout.

Benchmark reference: `domains/build/benchmarks/README.md#orchestrator-benchmarks`

## Run 1: Standard-Like Delegated Smoke

### Metadata

- `task_id`: build-kilo-smoke-standard-001
- `date`: 2026-06-16
- `domain`: build
- `benchmark_ref`: `domains/build/benchmarks/README.md#orchestrator-benchmarks`
- `runtime`: Kilo Code
- `model`: unknown
- `execution_profile`: standard-like pre-profile export
- `adapter_version`: pre-`feat: add kilo runtime profiles`
- `prompt_version`: initial Build Kilo smoke prompt
- `agent_ids`: build-orchestrator, localizer, editor, verifier, critic observed by behavior
- `reviewer`: human plus Codex repo inspection

### Task

Prompt summary:

```text
Use the Manurella Build system to make one tiny documentation-only clarity improvement, avoid generated .kilo/agents files, keep the change minimal, and report agent usage and verification.
```

Success criteria:

- Make one meaning-preserving documentation edit.
- Avoid generated Kilo files.
- Provide verification evidence.
- Report which agents were used.

### Runtime Outcome

- `status`: partial
- `timeout_status`: upstream_idle_timeout
- `target_latency`: not specified
- `actual_latency`: roughly 30-40 minutes
- `specialist_call_count`: unknown
- `repair_loop_count`: unknown
- `verifier_count`: 1 observed
- `changed_artifacts`: `domains/build/README.md`
- `output_path`: not captured

### Verification

Verification performed:

- Kilo-created `verification_result.txt` checked targeted README lines.
- Codex inspected the diff and removed the loose root verification artifact after recording the result.

Evidence:

```text
The verifier confirmed the targeted README lines but did not perform a broader baseline comparison.
The run hit {"code":504,"message":"Upstream idle timeout exceeded","metadata":{"error_type":"timeout"}}.
```

Verification gaps:

- No exact model recorded.
- No exact specialist count recorded.
- No full transcript archived.
- No broad diff baseline was performed by Kilo.

### Scores

Use 1-5 where applicable.

- `correctness`: 4
- `instruction_adherence`: 3
- `specificity`: 4
- `structure`: 4
- `domain_quality`: 3
- `safety`: 4
- `efficiency`: 1
- `recovery`: 2

### Notes

Quality notes:

- Agent routing, scoped editing, verifier evidence, and critic-style reporting showed promising behavior.
- The high latency and upstream idle timeout make this profile unsuitable for smoke tests.

Failure modes:

- Timeout.
- Over-budget run duration.
- Verification artifact was created at repository root instead of a structured eval path.

Next tuning action:

- Add runtime profiles and test a quick profile with delegation disabled.

## Run 2: Quick Profile Smoke

### Metadata

- `task_id`: build-kilo-smoke-quick-001
- `date`: 2026-06-16
- `domain`: build
- `benchmark_ref`: `domains/build/benchmarks/README.md#orchestrator-benchmarks`
- `runtime`: Kilo Code
- `model`: unknown
- `execution_profile`: quick
- `adapter_version`: `feat: add kilo runtime profiles`
- `prompt_version`: quick Build Kilo smoke prompt
- `agent_ids`: direct Build agent behavior; no subagent delegation observed in repo diff
- `reviewer`: human plus Codex repo inspection

### Task

Prompt summary:

```text
Use the Manurella Build system in QUICK profile. Make one tiny documentation-only clarity improvement, do not delegate, do not create files, change only one existing documentation/spec file, and report elapsed time, changed file, verification, and whether quick was sufficient.
```

Success criteria:

- Finish under the quick-profile target if possible.
- Avoid delegation.
- Avoid generated `.kilo/agents` edits.
- Change exactly one existing documentation/spec file.
- Perform at most one direct verification check.

### Runtime Outcome

- `status`: pass
- `timeout_status`: none reported
- `target_latency`: under 5 minutes
- `actual_latency`: reported as much better; exact value not captured
- `specialist_call_count`: 0 observed from constraints and diff
- `repair_loop_count`: 0 observed
- `verifier_count`: unknown
- `changed_artifacts`: `README.md`
- `output_path`: not captured

### Verification

Verification performed:

- Codex inspected `git diff`.
- Codex inspected `git status --short --untracked-files=all`.

Evidence:

```text
README.md changed one sentence:
"getting stronger..." -> "producing stronger..."

Only README.md was modified. No generated .kilo/agents files changed. No loose verification artifact was present.
```

Verification gaps:

- Exact elapsed time was not captured.
- Kilo's final transcript was not archived.
- The model name was not captured.

### Scores

Use 1-5 where applicable.

- `correctness`: 5
- `instruction_adherence`: 5
- `specificity`: 4
- `structure`: 4
- `domain_quality`: 3
- `safety`: 5
- `efficiency`: 4
- `recovery`: not applicable

### Notes

Quality notes:

- The quick profile produced a valid meaning-preserving edit with no scope expansion.
- Disabling delegation and lowering `steps` appears useful for smoke tests.

Failure modes:

- Missing exact latency and model metadata.

Next tuning action:

- Run a controlled Standard profile test with explicit delegation budget and exact timing.
