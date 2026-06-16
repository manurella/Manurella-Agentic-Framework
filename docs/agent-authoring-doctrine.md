# Agent Authoring Doctrine

## Purpose

This doctrine defines how Manurella agents are authored, reviewed, promoted, and kept portable across runtimes.

The rule is simple: no agent by label alone. An agent is not "a frontend agent" or "a writing agent." An agent is a bounded workflow component with explicit triggers, inputs, outputs, permissions, context policy, failure modes, and evidence.

## Source Basis

This doctrine is promoted from `research/inputs/manurella-agent-authoring-doctrine.md` and aligned with:

- `specs/agent-schema.md`
- `specs/runtime-control.md`
- `specs/cognitive-graph.md`
- `docs/research-doctrine.md`
- `docs/legacy-family-system-audit.md`
- `docs/build-agent-doctrine-audit.md`
- the legacy `Family System v13.yaml` source, which must be audited later for useful structural patterns rather than copied whole

## Agent, Skill, Checklist

Use an agent when the component owns workflow state, makes decisions, delegates work, or produces a contracted output that affects the route of the task.

Use a skill when the component is a reusable procedure, capability, or tool-use protocol that can be loaded only when needed.

Use a checklist when the component is a static quality gate, review rubric, or acceptance criterion that does not need agency.

If a component does not need decision authority, do not make it an agent.

## Required Authoring Shape

Every proposed agent must answer these questions before it can be promoted:

1. What exact problem does this agent solve?
2. When should it be invoked?
3. When should it not be invoked?
4. What inputs does it need?
5. What output contract must it satisfy?
6. What workflow does it follow?
7. What context is always-on, reference-only, and retrieved just in time?
8. What permissions does it need?
9. How does it behave in Fast Mode versus Standard Mode?
10. How does it behave across Low, Medium, High, Extra High, Max, and Ultra effort?
11. What failure modes is it likely to create?
12. What evaluation proves it improves output over the baseline?

## Writing Standards

Purpose must be one sentence with an action and a boundary.

`use_when` must contain observable triggers. It should be possible for a router or human to decide whether the trigger applies.

`do_not_use_when` must prevent overreach. A strong agent knows what work belongs elsewhere.

Inputs must be typed. If an agent needs files, briefs, screenshots, test logs, user preferences, research notes, or prior state, the spec must say so.

Outputs must be verifiable. Prefer schemas, checklists, diffs, plans, reports, or structured artifacts over vague prose.

Context must be tiered:

- `always_on`: minimal identity, scope, safety, output contract, and routing rules
- `references`: domain guides, examples, rubrics, and research loaded only when invoked
- `retrieved`: task-specific evidence such as files, logs, screenshots, learner state, manuscript state, or generated image results

Permissions must be least privilege. If an agent only judges, it should not edit. If it only edits, it should not shell out unless the workflow demands it.

Mode behavior and effort behavior must be separate. Fast versus Standard controls workflow shape and time pressure. Effort controls reasoning depth, decomposition, verification depth, and repair loops.

Failure modes must be material. Do not write generic warnings such as "may be wrong." Name the concrete failure: over-broad edits, invented framework details, inaccessible UI, style drift, continuity break, shallow pedagogy, unsupported image-model syntax, or unverified security advice.

## Mode Behavior

Fast Mode is for low-latency execution with the same output contract. It narrows exploration, reduces optional delegation, uses one repair loop by default, and reports assumptions plainly.

Standard Mode is for default serious work. It allows fuller context gathering, maker-checker workflows, stronger verification, and explicit unresolved-risk reporting.

Fast Mode must not mean sloppy mode. It means the agent chooses the shortest responsible route to the contracted output.

## Effort Behavior

Effort is a policy signal unless a runtime exposes native effort controls.

- Low: direct execution, minimal decomposition, one clear answer or change
- Medium: small plan, bounded context, basic verification
- High: default serious work, structured reasoning, local verification, clear residual risks
- Extra High: research-supported design, stronger alternatives analysis, deeper verification
- Max: multi-pass reasoning, critic/reviser loops, broader evidence gathering
- Ultra: checkpointed frontier-grade workflow, deliberate decomposition, extensive verification, and durable artifacts

Higher effort should improve judgment, evidence, and verification. It should not create unbounded verbosity.

## Frontend Slice Example

The frontend domain must not be represented as one vague "frontend agent." It decomposes into narrower components only when evaluation proves each boundary is useful.

Candidate Build/frontend components:

- `frontend-architect`: plans screen structure, state ownership, component boundaries, routing, accessibility strategy, and verification path
- `component-implementer`: implements scoped UI components from an accepted plan and existing design system rules
- `state-flow-specialist`: designs or audits client/server/UI state flow, async behavior, caching, and mutation boundaries
- `accessibility-auditor`: verifies semantic structure, keyboard flow, contrast, focus behavior, labels, and screen-reader affordances
- `visual-qa-specialist`: compares implementation against screenshots, design references, responsive constraints, and layout stability
- `performance-reviewer`: audits bundle impact, render cost, data loading, Core Web Vitals risk, and unnecessary client work

These should start as references, rubrics, or internal agents. Promote only after benchmarks show better output than the existing Build topology.

## Build Agent Audit

The current Build agents already follow the main doctrine pattern better than the legacy monolith:

- `architect` owns design direction and trade-off analysis.
- `build-orchestrator` coordinates task flow.
- `explorer` gathers bounded repository context.
- `localizer` maps requests to specific files and surfaces.
- `editor` performs scoped edits.
- `verifier` checks behavior and reports evidence.
- `critic` reviews risk and quality.

Known gaps:

- Mode and effort behavior are currently mostly injected by the Kilo adapter instead of authored per agent.
- Frontend subdomain boundaries are identified but not yet promoted into first-class Build graph nodes.
- Legacy Family System patterns have not yet been mined for structural lessons.
- Accepted-agent promotion still needs more scored baseline-vs-guided eval records.

## Promotion Gates

An agent moves through these statuses:

- `draft`: plausible component, not yet evidence-backed
- `research_candidate`: supported by research synthesis or legacy audit notes, but not benchmarked enough
- `accepted`: validated by evals, adapter export, permission review, failure-mode review, and cognitive graph links
- `deprecated`: retained for history but no longer active

An accepted agent must have:

1. A schema-compliant definition.
2. A cognitive graph node and relevant edges.
3. Domain research or legacy evidence.
4. Clear mode and effort behavior.
5. Permission review.
6. At least two benchmark tasks.
7. Baseline-vs-guided evaluation notes.
8. Runtime adapter validation for the target runtime.

## Legacy Family System Rule

`Family System v13.yaml` matters because it proved that stronger orchestration and role specialization can improve weak-model output. It also failed because it was a large monolithic runtime-specific artifact.

The next phase must audit it for:

- role topology that produced better output
- prompt structures that made weak models behave more deliberately
- implicit mode, effort, and repair-loop controls
- context and memory patterns that improved continuity
- permission and brittleness failures
- Kilo-format assumptions that broke after runtime changes

Do not copy the old YAML into the new framework. Mine it for evidence-backed patterns, convert those patterns into modular specs, link them in the cognitive graph, and validate them with evals.
