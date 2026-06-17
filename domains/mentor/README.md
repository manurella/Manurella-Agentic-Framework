# Mentor Domain Pack

## Purpose

Mentor handles adaptive tutoring, starting with language learning and expanding later into general learning systems. It covers placement, curriculum sequencing, conversational practice, targeted drills, linguistic diagnostics, pedagogical policy, comprehensible input, and learner-state tracking.

## Status

Research candidate. The current v0 topology is based on the Mentor domain research input and the cross-domain synthesis. It supersedes the first generic tutor skeletons.

## Use When

- The user wants language learning, practice, placement, correction, curriculum planning, or tutoring.
- The task requires adaptive feedback, scaffolding, learner-state awareness, or spaced review.
- The output should improve learning, not merely answer a question.

## Do Not Use When

- The task is primarily software building.
- The task is creative writing without an instructional purpose.
- The task is visual art direction or image prompting.
- The user asks for medical, legal, or high-stakes advice outside an educational framing.

## V0 Topology

Top-level selectable agents:

- `macro-placement-director`: onboarding, placement, CEFR-style baseline, and profile initialization.
- `curriculum-planner-sequencer`: skill graph planning, prerequisites, unit progression, and review scheduling.
- `conversational-interlocutor`: live role-play and communicative practice.
- `targeted-practice-drillmaster`: focused drills, active recall, and controlled practice.

Internal sub-agents:

- `linguistic-diagnostic-specialist`: classifies learner responses as optimal, valid-suboptimal, or incorrect and extracts errors.
- `sla-pedagogical-policy-engine`: chooses correction/scaffolding strategy from learner state and diagnostic payload.
- `comprehensible-input-synthesizer`: creates student-facing language at the right difficulty level.
- `asynchronous-state-tracer`: updates learner state with BKT/HLR-style mastery and recall estimates outside the live loop.

## Core Outputs

- placement profile
- curriculum sequence
- role-play response
- drill item
- diagnostic payload
- pedagogical policy decision
- comprehensible input response
- learner-state update

## Control Artifacts

- `learner-state-schema.md`: compact learner memory model for goals, evidence, skill estimates, recall risk, misconceptions, and next actions.
- `session-protocol.md`: default Mentor learning loop for intake, diagnosis, teaching move, retrieval practice, feedback, state update, and next packet.
- `interview-study-kit.md`: compact interview skill map, drill templates, and rubric patterns for urgent preparation.
- `mentor-quality-gate.md`: evidence gate for diagnosis, pedagogy, active recall, feedback, review scheduling, and uncertainty.
- `benchmarks/README.md#interview-study-benchmarks`: urgent interview-study benchmarks.
- `../../evals/prompts/mentor-interview-study-packet.md`: Kilo-safe baseline/guided prompt pack for interview preparation.

## Context Policy

Do not pretend learner state is more precise than the evidence supports. Use compact learner-state vectors, skill IDs, recent-turn summaries, and explicit uncertainty. Keep live tutoring latency low by moving state tracing out of the synchronous response loop.

## Permission Baseline

- `read`: allow learner profile, curriculum, and language references
- `edit`: ask/allow only learner-state or curriculum artifacts
- `shell`: deny by default
- `web`: ask for current language/SLA references
- `delegate`: allow for top-level agents, deny for internal workers

## Evaluation Rubric

- placement calibration
- prerequisite integrity
- correction precision
- valid-alternative recall
- scaffolding appropriateness
- comprehensible-input control
- learner-state calibration
- affective safety
- active recall quality
- interview readiness under time constraints
- session-loop completion
- narrow skill targeting

## Research Questions

- Should language learning start with one language pair or a language-neutral schema?
- Which learner-state math is appropriate for v0 without overclaiming precision?
- How should Mentor test correction quality and avoid false negatives on valid alternate phrasing?
- What parts of the tutoring loop can be deterministic before invoking a model?
