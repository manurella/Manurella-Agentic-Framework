# Runtime Control Specification

## Purpose

Runtime control defines how Manurella spends reasoning, tool calls, delegation, and time.

The goal is not to make every task shallow. The goal is to reserve deep reasoning for tasks that justify it, keep cheap tasks fast, and make latency/cost part of the quality claim.

## Control Principles

- Quality is measured against time, cost, and failure rate, not output quality alone.
- Deep reasoning is a budgeted mode, not the default behavior for every task.
- Every delegated agent must have a narrow purpose, expected output, and stopping condition.
- A run that times out without a useful artifact is a failure, even if intermediate reasoning was strong.
- Runtime adapters may narrow budgets but must not silently remove required verification.

## Runtime Modes

Modes control the workflow envelope: whether the run should be direct and lightweight or use the normal agentic loop.

### Fast Mode

Use for low-risk answers, tiny documentation edits, straightforward explanations, and single-agent checks.

Budget:

- target latency: under 5 minutes
- delegation: none by default
- verification: one direct check when applicable
- deep reasoning: disabled unless the user explicitly asks

Stop when:

- the answer or edit is complete
- the direct verifier passes
- the task turns out to be higher risk than declared

### Standard Mode

Use for normal Build tasks, creative drafting with critique, image prompt repair, and teaching tasks with diagnosis.

Budget:

- target latency: 5-15 minutes
- delegation: up to 3 specialist calls
- verification: required when the task has objective checks
- deep reasoning: allowed for planning, diagnosis, or critique, but not for every step

Stop when:

- success criteria are met with evidence
- one repair loop fails to improve the result
- the task needs research, external context, or a higher budget

## Effort Levels

Effort controls reasoning depth separately from mode. It follows the Claude-Code-style user experience requested for Manurella.

Effort levels:

- `low`: fastest acceptable reasoning for simple or latency-sensitive work
- `medium`: balanced reasoning for routine agentic tasks
- `high`: default high-quality reasoning for non-trivial work
- `extra-high`: extended reasoning for difficult coding, research, and multi-step work
- `max`: maximum single-run reasoning depth when quality matters more than latency
- `ultra`: deepest orchestration mode for frontier-grade work, broad verification, and checkpointed multi-agent execution

Effort is not a hard token budget in v0. It is a routing and prompt-policy signal until a runtime exposes a native effort control.

Use higher effort when:

- the task has ambiguous requirements
- multiple valid architectures compete
- the cost of a wrong answer is high
- a verifier failed and the cause is unclear
- creative or teaching quality depends on hidden structure

Use lower effort when:

- the task is mechanical
- the verifier is direct and cheap
- the edit is already localized
- the model is producing repetitive analysis
- the user prioritizes speed or cost

## Delegation Budget

Every delegated call must include:

- task slice
- required inputs
- forbidden scope
- expected output shape
- verifier or reviewer for the result

Default v0 limits:

| Mode | Max specialist calls | Max repair loops | Main use |
| --- | ---: | ---: | --- |
| Fast | 0 | 0 | direct answer or tiny edit |
| Standard | 3 | 1 | normal guided work |

If a specialist needs broader context than assigned, it should return `blocked: insufficient_context` instead of searching freely.

## Timeout Policy

When a runtime reports timeout, idle timeout, or upstream failure:

1. Save any artifact that exists.
2. Record the last known completed step.
3. Mark the run as `timeout`, not `pass`.
4. Decide whether to resume with a narrower checkpoint or lower delegation budget.
5. Add latency and failure notes to the benchmark record.

The next prompt after a timeout should prefer continuation from artifacts over re-running the full workflow.

Extended reasoning outputs should be summarized into compact artifacts: plans, hypotheses, decision records, checklists, rubrics, or diffs.

## Adapter Obligations

Runtime adapters should expose control through whatever knobs the runtime provides:

- step budgets
- model or variant hints
- temperature/top-p
- permission prompts
- task/delegation limits
- mode-specific prompt text
- effort-specific reasoning policy
- timeout/resume guidance

Adapters must record unsupported controls explicitly instead of pretending they exist.

## Evaluation Fields

Every scored run should record:

- mode: `fast` or `standard`
- effort: `low`, `medium`, `high`, `extra-high`, `max`, or `ultra`
- target latency
- actual latency
- timeout status
- specialist call count
- repair loop count
- verifier count
- model/runtime
- quality score
- cost or quota notes where available

## V0 Defaults

Until enough benchmark data exists:

- default Build mode: `standard`
- default Muse mode: `standard`
- default Pixel mode: `standard`
- default Mentor mode: `standard`
- default casual chat mode: `fast`
- default effort: `high`
- default research synthesis effort: `extra-high`

Mode and effort can be overridden by the user, benchmark definition, or domain orchestrator.

Build-specific inheritance rules live in `domains/build/runtime-policy.md`. Other domains should add equivalent runtime policy docs before promoting agents to `accepted`.

## Research Hooks

- Measure whether stricter `steps` values reduce Kilo timeout without hurting quality.
- Compare `fast` versus `standard` mode outcomes rather than treating time as a universal hard limit.
- Test whether specialist descriptions or prompt-body delegation rules have more impact on Kilo routing.
- Compare single-agent Standard runs against delegated Standard runs for latency and score.
- Study effort levels from current leading coding-agent workflows before promoting them into adapter defaults.
- Decide when a custom MCP/eval runner should enforce budgets externally instead of relying on prompts.
