# Manurella Framework Atlas Constitution

## Purpose

The Manurella Framework Atlas is the versioned architectural knowledge graph, implementation index, evidence ledger, and Agile backlog for the framework.

It keeps the whole system navigable while preserving connections between intent, research, specifications, implementation, evaluation, failures, and future work. It is not merely a diagram and must not become a conflicting copy of detailed specifications.

## Source-Of-Truth Boundary

The Atlas is canonical for:

- component identity and hierarchy
- typed relationships between components
- lifecycle and maturity state
- implementation and evidence links
- known gaps, risks, and next actions
- traversal order and active delivery path

Dedicated specifications, agent definitions, research records, source files, and evaluations remain canonical for their detailed content. Atlas nodes reference those artifacts instead of duplicating them.

## Core Rules

1. Every component has a permanent unique identifier.
2. Every meaningful relationship is explicit and typed.
3. Every status claim is supported by the evidence required for that status.
4. Missing, disputed, or uncertain knowledge is recorded rather than silently assumed.
5. No component is complete merely because prose exists.
6. A component cannot be production-ready without implementation and evaluation evidence.
7. Changes to architecture, implementation, or evidence must update the affected Atlas path.
8. Generated visualizations are projections of canonical repository data, never independent sources of truth.

## Depth Model

| Level | Scope |
| --- | --- |
| 0 | Manurella |
| 1 | Major systems |
| 2 | Capabilities |
| 3 | Components |
| 4 | Mechanisms and contracts |
| 5 | Agents, workflows, tools, and prompts |
| 6 | Implementation artifacts |
| 7 | Tests, benchmarks, and evidence |

This is a navigation model, not a rigid limit. A branch may be deeper when the domain requires it, but every added level must clarify ownership, behavior, or verification.

## Lifecycle

```text
idea
-> research-required
-> researched
-> specified
-> implemented
-> validated
-> production-ready
-> deprecated or superseded
```

Lifecycle states are evidence gates, not subjective progress labels. A component may move backward when an evaluation exposes a broken assumption or when its evidence becomes obsolete.

## Connected Depth-First Agile Method

Manurella develops through connected depth-first vertical slices rather than broad layers of unfinished definitions.

1. Establish only enough of the top-level map to understand the system boundary.
2. Select the highest-value unresolved user journey or architectural risk.
3. Follow that path downward through every required dependency.
4. Continue until the path reaches executable implementation and evaluation evidence.
5. Record every dependency, handoff, feedback loop, and shared capability discovered along the path.
6. Propagate findings and status changes back upward through the connected nodes.
7. Deliver a usable checkpoint before selecting the next sibling branch.
8. Revisit earlier nodes when evidence contradicts their assumptions.

The traversal is depth-first for progress and connected for correctness. Local work remains traceable to the root purpose, while discoveries at depth can refine the architecture above them.

## Vertical-Slice Completion

A depth-first slice is complete only when it has:

- a user or system outcome
- a defined entry point and stopping condition
- connected dependencies and contracts
- an implementation or executable artifact
- verification appropriate to its risk
- recorded failures and unresolved gaps
- updated Atlas relationships and lifecycle states
- one explicit next branch

Research alone, specifications alone, generated prompts alone, and unscored model output do not complete a slice.

## Relationship Model

The initial canonical relationship vocabulary is:

- `contains`
- `depends_on`
- `routes_to`
- `implements`
- `validates`
- `evolves`
- `supersedes`

Additional relationship types require a clear semantic distinction and validation rule. Synonyms must not be added merely for wording preference.

## Visualization And Editing

The first interactive Atlas is read-only and generated from validated repository data. It must support progressive disclosure, search, filtering, backlinks, and hierarchy, dependency, execution-flow, agent-family, cognitive, and roadmap projections.

Direct editing may be added only after the schema, validation, conflict handling, and change-review workflow are stable. The interface must never mutate canonical data without validation and a reviewable repository change.

## Governance

Each checkpoint identifies:

- the active Atlas path
