# Domain Architecture Synthesis

## Status

Research synthesis, not accepted architecture.

Sources:

- `research/inputs/mentor-agent-architecture-design.md`
- `research/inputs/manurella-build-agent-architecture.md`
- `research/inputs/manurella-muse-agent-architecture.md`
- `research/inputs/manurella-pixel-sub-agent-architecture.md`

## Core Finding

The four domain research reports converge on the same architectural rule:

Top-level agents should preserve user intent, long-horizon state, phase ownership, and routing. Internal sub-agents should do narrow, bounded transformations, validation, repair, or state updates.

This means the first provisional skeletons are useful as scaffolding, but several of them are too broad or too role-flavored to become final. We should not freeze them.

## Source Verification Gate

The reports are valuable research inputs, but their citations are not automatically accepted.

Before a claim is promoted into a spec or ADR:

- prefer primary sources such as papers, official docs, standards, and benchmark pages
- verify that cited papers, docs, and model capabilities actually exist
- mark blogs, Medium posts, Reddit threads, marketing pages, and secondary summaries as supporting context only
- distinguish current evidence from proposed architecture and speculation
- avoid anchoring Manurella to runtime-specific details unless the current runtime docs confirm them

## Cross-Domain Architecture Pattern

The strongest shared pattern is:

1. User-facing top-level domain agent receives intent.
2. Top-level agent converts intent into structured state.
3. Internal specialists perform narrow work through strict input/output contracts.
4. Verifier, judge, critic, or policy agents check the output.
5. Repair agents modify only failed dimensions.
6. State/memory agents update durable state outside the main response loop.

For weaker and non-frontier models, the framework should prefer:

- strict schemas over free-form replies
- narrow tool calls over broad shell/API access
- execution-grounded or artifact-grounded verification
- progressive disclosure over prompt stuffing
- deterministic early stopping
- explicit failure trajectories
- accumulation patterns when structured JSON is too large for one model call

## Build Domain Candidate

Research candidate topology:

Top-level selectable agents:

- `architect`: creates plans, specs, task breakdowns, data/API designs, and architectural decisions.
- `orchestrator`: coordinates implementation from an approved task plan but delegates direct edits and verification.
- `explorer`: read-only debugging, observability, review, and codebase comprehension.

Internal sub-agents:

- `localizer`: finds exact files, symbols, and line ranges.
- `editor`: produces precise patches from localized context.
- `verifier`: runs tests/builds and returns compact pass/fail evidence.
- `critic`: audits diffs for security, performance, maintainability, and style risks.

Important correction from provisional skeleton:

Frontend, backend, QA, security, DevOps, and docs may be better represented as skills, references, rubrics, or critic modes in v0 rather than separate top-level agents. They can become sub-specialists later if evals prove the need.

Research needed next:

- Whether Build v0 should collapse technical-role agents into `architect/orchestrator/explorer` plus internal workers.
- How Kilo can represent internal sub-agents and restrict direct editing by supervisors.
- What minimum eval harness proves the Localizer -> Editor -> Verifier -> Critic loop.

## Muse Domain Candidate

Research candidate topology:

Top-level selectable agents:

- `muse-lead`: routes creative intent and maintains project scratchpad.
- `world-character-architect`: worldbuilding, lore, character webs, setting rules, and style bible foundations.
- `narrative-designer`: plot structure, outlines, event graphs, pacing, and chapter/scene plans.
- `developmental-editor`: macro critique for structure, theme, character motivation, and pacing.
- `line-style-editor`: sentence-level style, rhythm, voice, and prose refinement.

Internal sub-agents:

- `eventseed-subtasker`: breaks macro outlines into atomic scene beats.
- `scene-drafter`: turns one approved beat into prose.
- `continuity-logic-checker`: detects canon, timeline, causal, and world-rule contradictions.
- `copyeditor`: enforces style sheet, grammar, spelling, terminology, and mechanical consistency.
- `context-coordinator`: retrieves summaries, entities, and prior events without stuffing the full manuscript.

Important correction from provisional skeleton:

`story-architect`, `worldbuilder`, `prose-editor`, and `script-doctor` are conceptually useful, but Muse needs clearer separation between pre-production, outline design, drafting, macro editing, line editing, continuity checking, and copyediting.

Research needed next:

- Whether screenwriting/script work is a top-level specialist or a mode inside narrative design plus scene drafting.
- How to evaluate creative outputs without flattening style diversity.
- How to represent story state: text scratchpad first, graph memory later.

## Pixel Domain Candidate

Research candidate topology:

Top-level selectable agents:

- `pixel-director`: user-facing art director that turns intent into structured visual briefs and orchestrates generation.

Internal sub-agents:

- `syntax-specialist`: compiles visual briefs into model-specific prompt/API payloads.
- `continuity-anchor`: maintains character, brand, style, and reference consistency.
- `audit-judge`: uses VLM-style checks or human-review rubrics to compare generated assets against the brief.
- `repair-technician`: performs targeted prompt repair, regeneration, or local edit instructions without regressing passed constraints.

Important correction from provisional skeleton:

Pixel should not expose several user-facing specialists in v0. A single user-facing director is cleaner because image generation already has high stochastic and API-specific complexity. Promptsmith, visual director, consistency keeper, and generation repair map well to internal roles, but `audit-judge` is missing and should be first-class.

Research needed next:

- Which image models are first-class targets.
- Which prompt syntax differences are evidence-backed versus folk practice.
- How to run repeated-trial evaluations for stochastic outputs.
- How to represent visual anchors portably without depending on one vendor.

## Mentor Domain Candidate

Research candidate topology:

Top-level selectable agents:

- `macro-placement-director`: onboarding, placement, CEFR-style baseline, and profile initialization.
- `curriculum-planner-sequencer`: skill graph planning, prerequisites, unit progression, and review scheduling.
- `conversational-interlocutor`: live role-play and communicative practice.
- `targeted-practice-drillmaster`: focused drills, active recall, and controlled practice.

Internal sub-agents:

- `linguistic-diagnostic-specialist`: classifies student responses as optimal, valid-suboptimal, or incorrect and extracts errors.
- `sla-pedagogical-policy-engine`: chooses correction/scaffolding strategy from learner state and diagnostic payload.
- `comprehensible-input-synthesizer`: creates student-facing language at the right difficulty level.
- `asynchronous-state-tracer`: updates learner state with BKT/HLR-style mastery and recall estimates outside the live loop.

Important correction from provisional skeleton:

Mentor should not be a generic tutor persona. The strongest architecture is a tutoring system with placement, curriculum, live interaction, drills, diagnostics, pedagogical policy, synthesis, and asynchronous state updates.

Research needed next:

- Whether language learning should start with one language pair or a language-neutral schema.
- Which learner-state math is appropriate for v0 without overclaiming precision.
- How to test correction quality and avoid false negatives on valid alternate phrasing.

## Foundation Implications

The next architecture pass should update the provisional domain skeletons, but only after we create a schema that can represent:

- top-level vs internal agents
- phase ownership
- strict input and output contracts
- permissions
- context tiering
- evaluation rubric
- failure modes
- promotion status
- research status

Without that schema, the repo will keep collecting Markdown roles instead of becoming a real framework.

## Promotion Recommendation

Do not promote the current agent skeletons directly.

Next steps:

1. Preserve the four research reports under `research/inputs/`.
2. Add a candidate architecture synthesis under `research/synthesis/`.
3. Create `specs/agent-schema.md`.
4. Rewrite the four domain skeletons from the schema.
5. Create benchmark stubs before exporting to Kilo.
