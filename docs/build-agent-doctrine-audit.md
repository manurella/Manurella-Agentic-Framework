# Build Agent Doctrine Audit

## Purpose

This audit checks the current Build domain agents against `docs/agent-authoring-doctrine.md` before the framework promotes a frontend sub-agent slice.

## Scope

Audited files:

- `domains/build/agents/architect.md`
- `domains/build/agents/build-orchestrator.md`
- `domains/build/agents/explorer.md`
- `domains/build/agents/localizer.md`
- `domains/build/agents/editor.md`
- `domains/build/agents/verifier.md`
- `domains/build/agents/critic.md`
- `domains/build/README.md`

## Summary

The Build topology is a good v0 backbone. It avoids the weak pattern of "you are a software agent" and instead separates planning, orchestration, read-only investigation, localization, editing, verification, and critique.

The topology should remain in `research_candidate` until benchmark evidence is stronger. Mode and effort behavior now has a Build-domain default in `domains/build/runtime-policy.md`; per-agent overrides should wait for eval evidence.

## Agent Findings

| Agent | Boundary | Doctrine status | Notes |
| --- | --- | --- | --- |
| `architect` | Top-level planning and architectural sequencing | Pass with gaps | Clear purpose, triggers, permissions, output contract, and failure modes. Must not edit. Inherits Build runtime policy until per-agent evals justify overrides. |
| `build-orchestrator` | Top-level implementation supervisor | Pass with gaps | Strong delegation loop and verifier requirement. Inherits Build runtime policy; still needs a stronger failure trajectory schema. |
| `explorer` | Top-level read-only investigation | Pass with gaps | Good evidence policy and read-only boundary. Needs command safety rules for shell-assisted diagnostics. |
| `localizer` | Internal context narrowing | Pass with gaps | Strong precision goal. Needs benchmarked localization recall and a decision on search-only versus AST-assisted localization. |
| `editor` | Internal scoped patch production | Pass with gaps | Correctly narrow and low-permission. Inherits patch caution and scope limits from Build runtime policy; still needs direct patch-vs-write policy by runtime. |
| `verifier` | Internal execution-grounded validation | Pass with gaps | Strong separation from repair. Needs command allowlist guidance and compact log schema. |
| `critic` | Internal non-functional risk audit | Pass with gaps | Good material-risk posture. Needs stable rubrics for security, performance, maintainability, and frontend quality. |

## Doctrine Coverage

Current strengths:

- Every audited agent has purpose, `use_when`, `do_not_use_when`, inputs, outputs, permissions, context tiers, workflow, evaluation rubric, failure modes, research links, and Kilo runtime metadata.
- Top-level agents do not directly own narrow mutation work.
- Internal agents are scoped to one transformation or judgment.
- Permission boundaries are mostly least-privilege.
- The Build domain README explicitly keeps frontend, backend, QA, security, DevOps, and documentation as references, rubrics, or skills until evals justify standalone agents.

Current gaps:

- `mode_behavior` is inherited from `domains/build/runtime-policy.md` rather than authored per agent.
- `effort_behavior` is inherited from `domains/build/runtime-policy.md` rather than authored per agent.
- Benchmarks are referenced but not yet deep enough to promote agents to `accepted`.
- The frontend slice is represented in the cognitive graph as draft candidate nodes, not accepted agents.
- Legacy Family System lessons have not been mined into Build topology decisions.
- Kilo can export permissions, but some boundaries still depend on prompt compliance and evals rather than runtime enforcement.

## Promotion Readiness

Status: keep all current Build agents at `research_candidate`.

Do not promote any Build agent to `accepted` until:

1. The agent has explicit mode and effort behavior or inherits `domains/build/runtime-policy.md`.
2. At least two benchmark tasks are recorded for that agent.
3. The Kilo adapter export is validated for the agent's expected runtime mode.
4. Permission behavior is checked against the target runtime's real enforcement limits.
5. The cognitive graph links the agent to its known failure modes and eval evidence.

## Completed Checkpoint

The Build/frontend graph slice has been added as candidate nodes, not accepted agents:

- `frontend-architect`
- `component-implementer`
- `state-flow-specialist`
- `accessibility-auditor`
- `visual-qa-specialist`
- `performance-reviewer`

Each node starts with `draft` status and links to the authoring doctrine, Build domain, runtime control, and frontend-specific failure modes.

## Next Checkpoint

Design the first frontend eval before promoting any frontend graph node. The eval should compare baseline output against Build-guided output and score accessibility, visual stability, state correctness, implementation minimality, and verification evidence.
