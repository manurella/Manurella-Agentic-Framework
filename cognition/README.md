# Cognition

This directory contains Manurella's v0 Cognitive Graph.

The graph is the project map for reasoning, routing, context loading, tools, evals, failure modes, modes, and effort levels.

It is intentionally small in v0. The first goal is to make relationships inspectable in git, not to build a full graph database.

## Files

- `graph.yaml`: machine-readable graph seed.
- `mindmap.md`: human-readable visual map.

## Rules

- Keep raw research in `research/inputs/`.
- Promote stable claims through `research/synthesis/` before changing the graph.
- Prefer `draft` status until a node or edge has eval evidence.
- Do not hard delete nodes or edges. Deprecate them.
- Keep runtime-generated artifacts out of the graph source of truth.

## First Scope

The first graph slice is Build/frontend because it tests delicate agent design:

- frontend architecture
- component implementation
- state flow
- accessibility
- visual QA
- performance

Other domains should be added after the Build slice is validated.
