# Domain Decomposition Specification

## Purpose

Manurella domains are broad by design. Each top-level domain contains sub-specialists because one prompt cannot responsibly cover every workflow inside software building, creative writing, visual generation, or teaching.

This spec defines the first-pass decomposition. It is intentionally provisional and must not be treated as accepted architecture. Boundaries should be changed when domain research or eval results show a better split.

The current skeletons exist to make research concrete. They are not proof that the decomposition is correct.

## Decomposition Rules

- Split by workflow, not by personality.
- Add a sub-agent only when it owns a meaningfully different task shape, context need, permission profile, or rubric.
- Keep orchestration separate from production work.
- Prefer a small specialist plus references over a giant specialist prompt.
- Every sub-agent must have a `Use When` and `Do Not Use When` boundary.
- Every sub-agent must name its eval rubric before it is considered usable.

## Build Domain

V0 research-candidate topology:

Top-level selectable agents:

- `architect`: planning, architecture, data/API design, and task decomposition.
- `build-orchestrator`: implementation coordination through internal workers.
- `explorer`: read-only debugging, review, observability, and codebase comprehension.

Internal sub-agents:

- `localizer`: exact files, symbols, and line ranges.
- `editor`: precise patches from localized context.
- `verifier`: execution-grounded checks and compact evidence.
- `critic`: non-functional risk review.

Specialized frontend, backend, QA, security, DevOps, and documentation concerns are v0 references, rubrics, or skills until evals prove they deserve standalone agents.

Research needed:

- Whether Kilo can enforce delegate-only supervisors.
- Which specialist concerns deserve skills first versus agents first.
- What minimum eval harness proves the Localizer -> Editor -> Verifier -> Critic loop.

## Muse Domain

V0 research-candidate topology:

Top-level selectable agents:

- `muse-lead`: creative routing and project scratchpad.
- `world-character-architect`: worldbuilding, lore, character webs, and setting rules.
- `narrative-designer`: plot structure, event graphs, outlines, and pacing.
- `developmental-editor`: macro critique for structure, theme, motivation, and pacing.
- `line-style-editor`: prose style, rhythm, voice, and sentence-level refinement.

Internal sub-agents:

- `eventseed-subtasker`: macro outline to atomic scene beats.
- `scene-drafter`: one approved beat to prose.
- `continuity-logic-checker`: canon, timeline, causal, and world-rule contradictions.
- `copyeditor`: mechanics, style sheet, grammar, spelling, and terminology.
- `context-coordinator`: context retrieval and compression.

Research needed:

- How to evaluate creative quality without flattening distinct styles.
- Whether screenwriting is a top-level specialist or a mode across narrative design and scene drafting.
- How to represent story state: text scratchpad first, graph memory later.

## Pixel Domain

V0 research-candidate topology:

Top-level selectable agent:

- `pixel-director`: user-facing art director and generation/repair orchestrator.

Internal sub-agents:

- `syntax-specialist`: model-specific prompt/API payload compiler.
- `continuity-anchor`: character, brand, style, and reference consistency.
- `audit-judge`: structured visual output assessment.
- `repair-technician`: targeted prompt repair, regeneration, or local edit guidance.

Research needed:

- Which image models are first-class v0 targets.
- Which prompt syntax differences are evidence-backed versus folk practice.
- How to represent visual anchors portably across generation models.
- How to run repeated-trial evaluations for stochastic outputs.

## Mentor Domain

V0 research-candidate topology:

Top-level selectable agents:

- `macro-placement-director`: onboarding, placement, and profile initialization.
- `curriculum-planner-sequencer`: prerequisite-aware skill path and review planning.
- `conversational-interlocutor`: live role-play and communicative practice.
- `targeted-practice-drillmaster`: focused drills, active recall, and controlled practice.

Internal sub-agents:

- `linguistic-diagnostic-specialist`: three-way learner response classification and error extraction.
- `sla-pedagogical-policy-engine`: corrective feedback and scaffolding policy.
- `comprehensible-input-synthesizer`: student-facing response at the right difficulty.
- `asynchronous-state-tracer`: out-of-band learner-state updates.

Research needed:

- Whether language learning should start with one language pair or a language-neutral schema.
- Which learner-state math is appropriate for v0 without overclaiming precision.
- How to test correction quality and avoid false negatives on valid alternate phrasing.

## Promotion Rule

A sub-agent moves from skeleton to usable when it has:

1. A complete portable definition.
2. A Kilo export target.
3. At least two benchmark tasks.
4. A rubric.
5. One baseline-vs-guided evaluation run.
