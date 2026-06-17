# Runtime Packet Protocol

## Purpose

Runtime packets make Manurella usable on unstable or weaker agent runtimes. A packet is a small, checkpointed unit of work with explicit inputs, allowed actions, evidence requirements, and stop conditions.

This protocol exists because long silent agent runs are not a quality strategy. They create timeout risk, hidden drift, weak evidence, and unusable eval data.

## Packet Shape

Every runtime packet must define:

```yaml
packet_id: string
objective: string
mode: fast | standard
effort: low | medium | high | extra-high | max | ultra
timebox_minutes: number
allowed_actions:
  - read
  - edit
  - shell
  - browser
  - web
  - delegate
forbidden_actions:
  - string
inputs:
  - string
expected_output:
  - string
evidence_required:
  - string
stop_conditions:
  - string
resume_state:
  - string
```

## Packet Classes

### 1. Scout Packet

Use when the task needs orientation.

Allowed:

- read files
- list relevant artifacts
- summarize current state

Forbidden:

- edits
- broad refactors
- unsupported claims

Output:

- target files
- likely risks
- recommended next packet

### 2. Design Packet

Use when architecture or agent definition must be decided before implementation.

Allowed:

- inspect specs and research
- compare options
- create a short decision artifact

Forbidden:

- implementation edits unless explicitly requested
- unbounded research

Output:

- decision
- trade-offs
- acceptance gates
- next implementation packet

### 3. Implementation Packet

Use when the task requires file changes.

Allowed:

- edit only named files or named scope
- run listed checks

Forbidden:

- unrelated cleanup
- generated/runtime files unless requested
- speculative broad edits

Output:

- changed files
- verification evidence
- unresolved risks

### 4. Verification Packet

Use when output quality must be proven.

Allowed:

- run listed checks
- inspect screenshots/logs/diffs
- create result records

Forbidden:

- fixing issues unless packet explicitly permits repair

Output:

- pass/fail/partial
- evidence paths
- gaps
- next repair packet if needed

### 5. Research Packet

Use when external knowledge is required.

Allowed:

- gather research from named sources or user-provided research outputs
- synthesize applicable patterns

Forbidden:

- promoting research directly into accepted agents
- unsupported claims

Output:

- claims
- source notes
- adoption/defer decisions
- eval implications

## Kilo Runtime Rules

Kilo packets must be short and explicit.

When the model is unknown, weak, or already produced shallow/generic output, apply `specs/weak-runtime-compensation.md` inside the packet. The model must expose its evidence, assumptions, narrow target, output, and self-check before it continues.

Default limits:

| Packet class | Fast timebox | Standard timebox | Delegation |
| --- | ---: | ---: | --- |
| Scout | 3 min | 6 min | none |
| Design | 5 min | 10 min | at most 1 |
| Implementation | 5 min | 12 min | at most 1 |
| Verification | 5 min | 10 min | none by default |
| Research | 8 min | 15 min | none unless requested |

Kilo must stop at the packet boundary even if more work remains.

Kilo must not:

- claim unavailable tool results
- create eval result files inside fixture folders
- edit generated `.kilo/agents` files unless the packet is an adapter/export packet
- continue after timeout by restarting the full workflow
- use hidden long delegation without reporting specialist count

## Timeout Recovery

On timeout or upstream idle failure:

1. Record `timeout_status`.
2. Preserve any created artifact.
3. Identify the last completed packet.
4. Resume with a narrower packet.
5. Lower delegation before lowering quality gates.

Timeout does not mean the model "needed more time." It may mean the packet was too large, the runtime stream idled, delegation ran away, or the prompt failed to force evidence checkpoints.

If the timeout came from stream or upstream idle behavior, the next packet must include an early checkpoint output before doing deeper work.

## Evidence Rules

Evidence must be concrete:

- file path and line
- diff summary
- command and result
- screenshot path and inspected issue
- test log path
- eval record path
- explicit `not_run` or `not_available`

Never record `actual_latency: 0` unless the measured runtime was actually zero, which should not happen for a model run.

## Prompt Header Template

```text
MANURELLA RUNTIME PACKET

packet_id:
packet_class: scout | design | implementation | verification | research
mode:
effort:
timebox:

Objective:

Allowed actions:

Forbidden actions:

Inputs:

Evidence required:

Stop conditions:
- Stop when the packet output is complete.
- Do not continue into the next packet.
- If blocked, return the blocker and the smallest next packet.
```

## Promotion Rule

Any eval or agent definition that repeatedly causes timeout must be redesigned into smaller packets before it can be promoted.
