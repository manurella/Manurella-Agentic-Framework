# Build Runtime Policy

## Purpose

This policy defines the default mode and effort behavior for Build-domain agents.

It is inherited by Build agents until an agent has enough benchmark evidence to justify a more specific policy. Inheritance prevents duplicated prompt policy while keeping `mode_behavior` and `effort_behavior` explicit enough for audits and adapters.

## Inheritance Rule

Build agents inherit this policy when their definition does not include local `mode_behavior` or `effort_behavior`.

An agent may override this policy only when:

1. The override is documented in the agent definition.
2. The override preserves the agent's permission boundary.
3. The override has a benchmark or eval reason.
4. The override does not silently expand runtime authority.

## Fast Mode

Fast Mode is for bounded, low-risk Build work where the same acceptance bar can be reached without the full agentic loop.

Default behavior:

- Use direct execution or a single top-level Build agent.
- Avoid specialist delegation by default.
- Gather only the context needed to answer, plan, or patch the immediate task.
- Use one direct verifier when an objective check exists.
- Stop and report if the task requires broader architecture, multiple files with unclear ownership, risky edits, or external research.

Default Build use cases:

- small documentation edits
- localized explanations
- simple code review questions
- already-localized tiny fixes
- direct verifier runs

Fast Mode must not lower the output contract. It only narrows workflow breadth.

## Standard Mode

Standard Mode is the default for serious Build work.

Default behavior:

- Start from a task contract and success criteria.
- Use the existing Build topology when the task benefits from it.
- Allow bounded delegation through Localizer, Editor, Verifier, and Critic.
- Require verifier evidence for source, config, generated artifact, or behavior changes.
- Use one repair loop by default when verification fails.
- Stop with a structured failure trajectory when evidence does not justify continuing.

Default Build use cases:

- implementation tasks
- architecture-to-implementation handoff
- debugging with likely source changes
- multi-file changes
- security, performance, deployment, or data-risk review
- frontend work that needs visual, accessibility, state, or performance checks

## Effort Behavior

Effort controls reasoning depth, not official agent status.

| Effort | Build behavior |
| --- | --- |
| `low` | Direct answer or direct edit only. Use when the task is already localized, low-risk, and easily verified. |
| `medium` | Small plan, bounded context read, one verification step where applicable. Use for routine Build work. |
| `high` | Default Build effort. Produce a task contract or concise plan, inspect relevant files, preserve permissions, verify, and report residual risk. |
| `extra-high` | Use for ambiguous architecture, debugging with unclear cause, frontend quality-sensitive work, security-sensitive review, or research-backed design. Compare alternatives before choosing. |
| `max` | Use when failure cost is high or the task spans multiple Build concerns. Require critic review, stronger verification, and explicit trade-off notes. |
| `ultra` | Use only for checkpointed frontier-grade Build work. Split into phases, preserve artifacts, use broad verification, and record eval-ready trajectory notes. |

Higher effort should increase decomposition quality, evidence quality, and verification depth. It should not create unbounded prose or unnecessary delegation.

## Agent Defaults

Top-level Build agents:

- `architect`: Fast gives a compact plan or refusal to over-scope; Standard gives staged architecture and verification design. Higher effort increases alternatives analysis and risk handling.
- `build-orchestrator`: Fast should rarely delegate; Standard runs the normal localization-edit-verification-critic loop when justified.
- `explorer`: Fast gathers narrow evidence; Standard traces across code, config, logs, and tests with clearer confidence labels.

Internal Build agents:

- `localizer`: Higher effort expands search breadth and dependency tracing, not edit authority.
- `editor`: Higher effort improves patch caution and assumptions, not scope breadth.
- `verifier`: Higher effort broadens verifier selection and log diagnosis, not repair authority.
- `critic`: Higher effort expands risk dimensions and evidence checks, not rewrite authority.

Experimental frontend graph nodes inherit this policy only for research and eval planning. They are not official runtime agents until promoted.

## Timeout Behavior

Build runs must treat timeout as a failed or partial run, not a pass.

On timeout:

1. Record the last completed phase.
2. Preserve any artifact that exists.
3. Record mode, effort, elapsed time, specialist calls, repair loops, and verifier count.
4. Resume from the smallest useful checkpoint instead of restarting the full workflow.

## Adapter Notes

The Kilo adapter may inject this policy as prompt text when an agent lacks local mode or effort behavior.

Adapters must record unsupported controls explicitly. If a runtime cannot enforce delegation, edit denial, shell denial, or effort behavior, the generated prompt must say that enforcement is policy-level and needs eval coverage.
