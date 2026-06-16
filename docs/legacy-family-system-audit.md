# Legacy Family System Audit

## Purpose

This document reserves the audit track for the original Family System v13. The old system is evidence, not the new source of truth.

## Known Source Files

- `C:\Users\rehan\Desktop\Projects\Logic Equation Solver\Family System v13.yaml`
- `C:\Users\rehan\Desktop\Projects\Logic Equation Solver\my old stuff\Family System v13.yaml`

## Why It Matters

Family System v13 produced unusually strong output in Kilo with non-frontier models because it supplied architecture around the model: role specialization, orchestration, rules, and likely implicit repair behavior.

It also exposed the main failure mode Manurella is designed to avoid: one giant runtime-specific YAML became hard to validate, hard to migrate, difficult to test, and vulnerable to Kilo format changes.

## Audit Questions

1. What role topology created the strongest output?
2. Which instruction blocks were genuinely load-bearing?
3. What implicit mode, effort, repair, or verification controls existed?
4. What context and memory structure improved continuity?
5. Which sections created token bloat, contradiction, or routing ambiguity?
6. Which permissions were too broad?
7. Which assumptions broke when Kilo changed its system?
8. Which patterns map cleanly to Manurella agents, skills, graph nodes, evals, or runtime controls?

## Extraction Rules

- Extract patterns, not bulk text.
- Preserve evidence links back to the source section being mined.
- Convert useful ideas into modular specs before runtime export.
- Keep large legacy content out of always-on prompts.
- Promote only after at least one baseline-vs-guided eval shows value.

## Future Output

The audit should eventually produce:

- a role-topology map
- a list of reusable patterns
- a list of deprecated patterns
- migration notes into the cognitive graph
- candidate eval tasks that reproduce the old system's strongest behavior
