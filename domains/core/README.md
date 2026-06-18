# Core Domain

Core owns framework-level routing, governance, runtime control, eval policy, cognitive graph maintenance, research intake, and adapter coordination.

Core is not a user-facing specialist domain like Build, Muse, Pixel, or Mentor. It is the framework spine that decides which specialist should act and what evidence is required before work is considered done.

## V0 Responsibilities

- Consume validated Task Frames, Acceptance Contracts, and Clarification Decisions.
- Compile bounded routing decisions and handoff packets without copying raw transcript state.
- Route user requests to the correct domain lead.
- Decide whether the current task is framework governance or specialist execution.
- Apply Fast/Standard mode and effort policy.
- Keep context lean by loading only relevant references.
- Require eval/result artifacts for serious claims.
- Update the cognitive graph when durable relationships, failure modes, tools, or evals change.

## V0 Non-Responsibilities

- Do not directly implement Build code changes.
- Do not directly write creative scenes when Muse should handle them.
- Do not directly compile image prompts when Pixel should handle them.
- Do not directly teach when Mentor should handle it.

## Agents

- `manurella-orchestrator`: main router and framework-level supervisor.

## Executable Projection

`tools/compile_core_packet.py` validates an Interpreter bundle before compiling `schemas/core/routing-decision.schema.json`. Conversation and Core-owned work stay direct. Ambiguity, confirmation, and refusal remain blocked in Core. Only executable specialist work receives a handoff packet.
