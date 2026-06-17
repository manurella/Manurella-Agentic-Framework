# Mentor Interview Study Kit

## Purpose

This kit gives Mentor a compact local substrate for interview preparation. It prevents weak models from defaulting to generic study advice by supplying skill IDs, drill templates, and rubric patterns.

It is not a complete curriculum. It is the first v0 working set for urgent interview readiness.

## Skill ID Pattern

Use stable labels:

```text
interview.<track>.<skill>
```

Examples:

- `interview.core.problem-framing`
- `interview.core.complexity-explanation`
- `interview.frontend.accessibility-basics`
- `interview.frontend.state-ownership`
- `interview.flutter.widget-lifecycle`
- `interview.backend.api-contracts`
- `interview.system-design.capacity-shape`

## Core Interview Skills

### `interview.core.problem-framing`

Tests whether the learner can clarify requirements, constraints, inputs, outputs, and edge cases before solving.

Drill:

- Give a short problem.
- Ask for clarifying questions and assumptions.
- Score on specificity, edge cases, and avoiding premature implementation.

### `interview.core.solution-structure`

Tests whether the learner can explain the approach before details.

Drill:

- Ask for a three-part answer: idea, algorithm/workflow, trade-off.
- Penalize code-first answers that hide reasoning.

### `interview.core.complexity-explanation`

Tests whether the learner can state time, space, bottlenecks, and scaling limits.

Drill:

- Ask for best, average, worst case when relevant.
- Ask what input size breaks the approach.

### `interview.core.debugging-communication`

Tests whether the learner can reason from symptoms to hypotheses.

Drill:

- Provide a failure symptom.
- Ask for likely causes, first check, and what evidence would confirm it.

### `interview.core.tradeoff-language`

Tests whether the learner can compare options instead of giving one absolute answer.

Drill:

- Ask "when would you not use this?"
- Score on constraints, maintainability, performance, and risk.

## Frontend Track

### `interview.frontend.state-ownership`

Target:

- separate local UI state, server state, URL state, form state, and derived state

Common weak answer:

- "put it in global state" without explaining ownership, invalidation, or lifetime

Drill:

- Given a filterable dashboard, identify which state belongs in URL, cache, component, or form library.

### `interview.frontend.accessibility-basics`

Target:

- labels, roles, keyboard path, focus management, contrast, error announcements

Common weak answer:

- mentioning alt text only

Drill:

- Review a modal or form and list the minimum accessibility checks.

### `interview.frontend.render-performance`

Target:

- avoid unnecessary rerenders, heavy client work, layout shift, and blocking resources

Common weak answer:

- "use memo" without measuring or explaining data flow

Drill:

- Given a slow list, propose evidence-first diagnosis and two fixes.

### `interview.frontend.data-fetching`

Target:

- caching, loading state, error state, stale data, invalidation, optimistic updates

Common weak answer:

- only describing `fetch` or `useEffect`

Drill:

- Explain how a profile update should update visible cached data.

## Flutter Track

### `interview.flutter.widget-lifecycle`

Target:

- understand widget rebuilds, state objects, lifecycle hooks, and disposal

Common weak answer:

- treating rebuild as app restart or ignoring disposal

Drill:

- Explain when `initState`, `build`, and `dispose` run and what each should contain.

### `interview.flutter.state-management`

Target:

- choose local state, inherited state, provider/bloc/riverpod-style patterns based on scope and lifetime

Common weak answer:

- naming a package without explaining state ownership

Drill:

- Given a cart, auth session, and text field, place each state type and justify it.

### `interview.flutter.async-ui`

Target:

- handle loading, cancellation, errors, mounted checks, and user feedback

Common weak answer:

- assuming async result always arrives while widget remains mounted

Drill:

- Explain how to safely update UI after an async call.

## Backend Track

### `interview.backend.api-contracts`

Target:

- request/response shape, validation, error semantics, versioning, idempotency

Common weak answer:

- designing endpoints without failure behavior

Drill:

- Design a create-order endpoint and list validation, status codes, and idempotency strategy.

### `interview.backend.data-modeling`

Target:

- entities, relationships, constraints, indexes, migrations

Common weak answer:

- schema without constraints or query access patterns

Drill:

- Model users, projects, and memberships and explain indexes.

### `interview.backend.reliability`

Target:

- retries, timeouts, queues, observability, failure isolation

Common weak answer:

- "retry it" without idempotency or backoff

Drill:

- A payment webhook fails intermittently. Explain diagnosis and safe retry design.

## System Design Track

### `interview.system-design.capacity-shape`

Target:

- estimate users, requests, storage, hot paths, and growth risk

Common weak answer:

- drawing components before load assumptions

Drill:

- For a chat app, state assumptions and identify the first bottleneck.

### `interview.system-design.boundaries`

Target:

- split responsibilities across clients, services, databases, queues, and caches

Common weak answer:

- adding services without a reason

Drill:

- Explain what should be synchronous vs asynchronous in an upload pipeline.

### `interview.system-design.consistency`

Target:

- explain consistency needs, conflicts, transactions, eventual consistency, and user-visible guarantees

Common weak answer:

- claiming every system needs strong consistency

Drill:

- Decide consistency requirements for inventory, likes, and messages.

## Drill Template

Use this shape for urgent interview sessions:

```text
Skill:
Question:
Expected answer:
Strong answer signals:
- 
Common weak answer:
Follow-up:
Scoring:
- 5: complete, precise, trade-offs included
- 4: mostly correct, minor missing edge case
- 3: correct core, shallow trade-offs
- 2: partial, unclear reasoning
- 1: mostly incorrect or generic
Next action:
```

## Mock Interview Template

```text
Topic:
Difficulty:
Interviewer intent:
Prompt:
Follow-up 1:
Follow-up 2:
Rubric:
Expected strong answer:
Likely failure modes:
Post-answer feedback rule:
Next drill:
```

## Use With Learner State

When the learner misses a question:

- map the miss to the narrowest skill ID
- record the wrong mental model or missing step
- schedule one immediate retry and one later review
- do not mark mastery until the learner answers unaided
