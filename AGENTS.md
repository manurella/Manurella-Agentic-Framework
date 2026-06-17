# Manurella Agentic Framework Instructions

## Runtime Boot

- Start from `MANURELLA.md` before major framework work.
- Use `domains/core/agents/manurella-orchestrator.md` as the main routing contract.
- Apply `specs/core-operating-protocol.md` for task class, project state, handoff, quality review, and recovery behavior.
- Treat Build, Muse, Pixel, and Mentor as specialist domains, not as the whole framework.
- Keep work agile: make the smallest baseline slice usable, validate it, then polish.
- Research is mandatory when domain boundaries, benchmarks, or methodology are uncertain, but research must become specs, agents, evals, tools, or graph updates.

## Working Rules

- Do not claim state-of-the-art quality by assertion; earn it through baseline-vs-guided evals.
- Preserve runtime agnosticism. Kilo is the first adapter, not the framework itself.
- Keep durable memory in `cognition/graph.yaml`, `cognition/mindmap.md`, and focused docs.
- Write eval records only under `evals/results/`.
- Prefer targeted changes over broad rewrites.
- Preserve the useful Family System behavior: direct answers for simple requests, bounded handoffs for delegated work, and quality review before accepting specialist output.

## Validation

- Run `python tools\validate_framework.py --repo .` after framework structure changes.
- Run `python tools\self_check.py --repo .` before a baseline checkpoint when edits touch tools, adapters, graph, or agents.

## Commit Style

- Use Conventional Commits.
- The user handles commits; provide commands instead of committing directly.
