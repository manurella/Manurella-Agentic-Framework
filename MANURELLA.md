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
2. Choose Fast or Standard mode.
3. Choose effort level: Low, Medium, High, Extra High, Max, or Ultra.
4. Load only the domain references needed for the current packet.
5. Produce or delegate one bounded artifact.
6. Verify with a tool, checklist, rubric, benchmark, or result record.
7. Update graph/docs only when a durable fact changed.

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
