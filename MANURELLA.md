# Manurella Brain

This is the boot file for a fresh agent session in this repository.

## Identity

Manurella Agentic Framework is a runtime-agnostic agent framework that improves model output through:

- a small kernel
- a main routing orchestrator
- specialist domain packs
- cognitive graph memory
- runtime modes and effort policies
- packetized execution for weak or unstable runtimes
- eval-driven iteration

The framework starts from the old Family System lessons, but v0 is not a giant prompt. It is a modular system that can be compiled into Kilo agents first and later into Codex, ChatGPT/Gemini workflows, MCP tools, and a custom runtime.

## Family-Level Baseline

Manurella's baseline must match the useful definition style of Family System v13:

- agents have judgment, convictions, and operating behavior, not just labels
- behavior comes before knowledge
- the orchestrator evaluates output quality, not only routes tasks
- every delegated task has a bounded handoff packet
- quick tasks stay quick
- large tasks use project state, slices, checkpoints, and recovery records
- domain quality is enforced through gut checks and evidence

The extraction map is `docs/family-system-mechanism-map.md`.
The runtime-neutral behavior contract is `specs/core-operating-protocol.md`.

## Main Router

Use `domains/core/agents/manurella-orchestrator.md` as the primary routing contract.

The orchestrator decides whether a request belongs to:

- `build`: software, architecture, QA, security, DevOps, docs, debugging
- `muse`: stories, scripts, prose, creative development, continuity, editing
- `pixel`: image prompting, art direction, visual continuity, audit, repair
- `mentor`: teaching, tutoring, study planning, interview prep, learner state
- `core`: framework governance, routing, evals, research intake, graph updates, adapter work

## Operating Loop

1. Classify the request and domain.
2. Classify the task class: Quick, Multi-step, Full project, Conversation, or Ambiguous.
3. Classify project state when there is an existing artifact.
4. Choose Fast or Standard mode.
5. Choose effort level: Low, Medium, High, Extra High, Max, or Ultra.
6. Load only the domain references needed for the current packet.
7. Produce directly or delegate one bounded artifact through a handoff packet.
8. Run the quality gate before accepting the output.
9. Verify with a tool, checklist, rubric, benchmark, or result record.
10. Update graph/docs only when a durable fact changed.

## Baseline Priority

The current v0 baseline target is practical usability, not perfect research coverage:

1. Root boot files exist.
2. Main orchestrator exports to Kilo.
3. All four specialist domains have selectable agents.
4. Framework validation passes.
5. Self-check passes.
6. Next Kilo run can start from generated agents and packetized prompts.

## Non-Negotiables

- Do not bury the framework inside Mentor or Build.
- Do not use research as a substitute for runnable artifacts.
- Do not let Kilo timeout destroy the workflow; use packets and durable records.
- Do not promote agents without evidence.
- Do not create huge always-on prompts. Route, retrieve, and verify.
- Do not delegate without mission, focus, references, and acceptance criteria.
- Do not accept specialist output that fails the domain gut check.
- Do not start a full pipeline for a direct answer or quick task.
