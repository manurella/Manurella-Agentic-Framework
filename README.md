# Manurella Agentic Framework

Manurella Agentic Framework is a runtime-agnostic agent framework for producing stronger, more reliable output from weaker or cheaper models through better task framing, specialist domain packs, eval-driven iteration, controlled memory, and runtime adapters.

The project starts from the lessons of `Family System v13`, but it is not another monolithic prompt file. The framework is built around portable specifications that can be compiled into Kilo Code agents first, then later into Codex instructions/skills, ChatGPT/Gemini workflows, and a custom Python runtime.

## V0 Goal

V0 proves this loop:

1. Define a small portable kernel and specialist domain-pack format.
2. Compile a few domain packs into valid Kilo Code agent files.
3. Run the same benchmark tasks against baseline model output and Manurella-guided output.
4. Score outputs with deterministic checks and human/LLM rubrics.
5. Iterate from measured failures, not vibes.

The current execution spine is `docs/master-execution-plan.md`.

## First Domains

- `build`: software building, architecture, QA, security, deployment, and documentation.
- `muse`: writing, story, script, narrative critique, and creative development.
- `pixel`: art direction and precise image-generation prompt engineering.
- `mentor`: language tutoring first, then broader teaching/learning workflows.

## Repository Map

- `docs/charter.md`: purpose, constraints, and v0 success criteria.
- `docs/architecture.md`: layered architecture and first implementation decisions.
- `docs/master-execution-plan.md`: delivery sequence, checkpoints, and promotion gates.
- `docs/decisions/`: ADRs for decisions that should not be lost.
- `specs/evals.md`: evaluation categories, metrics, and v0 benchmark plan.
- `specs/runtime-packet-protocol.md`: checkpointed runtime packets for Kilo and other unstable runtimes.
- `research/`: external research inputs and synthesis.
- `adapters/kilo/`: Kilo Code export target and examples.
- `domains/`: portable specialist domain packs.
- `domains/build/frontend-quality-gate.md`: frontend accessibility, visual, state, and performance evidence gate.
- `tools/`: future prompt compiler, eval runner, and memory tooling.

## Commit Style

Use Conventional Commits:

- `docs:` documentation and specs
- `feat:` framework features or new domain/adapters
- `test:` eval cases and validation logic
- `fix:` corrections
- `chore:` repository maintenance
