# Research Doctrine

## Purpose

Manurella is research-first because the framework's value depends on the quality of its foundations. A weak decomposition will produce weak agents, no matter how polished the prompt text looks.

The goal is not to create a large collection of roles. The goal is to build a runtime-agnostic operating system for better AI work: clearer task framing, better context selection, specialist routing, verification, repair, and continuous improvement.

## Core Philosophy

Architecture can narrow the model gap only when it gives the model better structure than the base runtime provides by default.

That means Manurella must improve:

- what context the model sees
- which specialist handles the task
- how the task is decomposed
- what output contract is required
- how errors are detected
- how failed outputs are repaired
- how performance is measured over time

If a domain foundation is wrong, later prompt engineering only hides the damage. The first serious work is therefore domain research, boundary design, and evaluation design.

## Research Before Locking

The current domain skeletons are provisional. They are not accepted architecture.

Before a top-level domain becomes stable, it needs individual research covering:

- domain competency map
- sub-agent boundary candidates
- orchestrator responsibilities
- specialist responsibilities
- context and reference strategy
- permissions and tool needs
- output contracts
- evaluation rubrics
- benchmark tasks
- common failure modes
- repair loops
- v0, v1, and v2 expansion path

After a top-level domain is researched, each accepted candidate sub-agent may need its own research pass before implementation. Domain research decides the architecture. Sub-agent research decides the operating workflow, references, rubrics, tools, and failure-repair logic.

Research findings must distinguish:

- evidence from current sources
- proven project experience
- plausible design hypotheses
- speculative future ideas

Only evidence-backed or evaluation-backed decisions should be promoted into specs.

## Main Domains

Manurella starts with four top-level domains:

- `build`: software and systems creation.
- `muse`: writing, story, script, and creative language work.
- `pixel`: visual art direction, image prompt design, generation repair, and style consistency.
- `mentor`: language learning first, then broader teaching and learning systems.

Each domain is large enough to require its own research pass. Shared framework patterns should emerge after the individual passes, not be forced before them.

## State Of The Art Requirement

"State of the art" is not a claim. It is a standard of work.

For Manurella, state of the art means:

1. Current external research is checked before foundational decisions.
2. Domain boundaries are justified, not guessed.
3. Prompts are treated as versioned artifacts.
4. Agent behavior is evaluated against benchmarks.
5. Weak model performance is compared against baseline prompts.
6. Failure cases are logged and turned into repair rules or evals.
7. Runtime adapters preserve the same architecture instead of rewriting it per tool.

## Promotion Rule

A domain architecture is not accepted until it has:

1. A research pass.
2. A proposed decomposition.
3. A critique pass against alternatives.
4. A minimal benchmark suite.
5. A baseline-vs-guided evaluation plan.
6. A documented decision record.
