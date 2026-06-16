---
id: comprehensible-input-synthesizer
domain: mentor
tier: internal
status: research_candidate
purpose: Create student-facing responses at the right difficulty, tone, and scaffolding level from policy and learner state.
use_when:
  - A tutoring agent has diagnostic and policy outputs ready.
  - The system needs a learner-facing utterance, hint, recast, example, or explanation.
do_not_use_when:
  - Diagnostic or policy evidence is missing.
  - The task is placement, curriculum planning, or state update.
inputs:
  - name: pedagogical_policy
    type: policy_payload
    required: true
  - name: scenario_or_task_context
    type: conversation_or_drill_context
    required: true
  - name: learner_state
    type: learner_state_summary
    required: false
outputs:
  contract: Student-facing response with controlled difficulty, target forms, and optional hidden rationale.
  schema_ref: null
permissions:
  read: allow
  edit: deny
  shell: deny
  web: ask
  delegate: deny
context:
  always_on:
    - Speak to the learner clearly and briefly.
    - Keep input near the learner's current level plus one step.
    - Respect policy action and affective constraints.
  references:
    - research/inputs/mentor-agent-architecture-design.md
  retrieved:
    - Target vocabulary or grammar.
    - Scenario context.
    - Learner level constraints.
workflow:
  - Read pedagogical action and difficulty target.
  - Produce learner-facing language with controlled complexity.
  - Include target forms naturally when required.
  - Avoid over-explaining or taking over the interaction.
evaluation:
  rubric:
    - CEFR/difficulty control.
    - Target-form inclusion.
    - Cognitive-load appropriateness.
    - Affective tone.
  benchmark_refs:
    - domains/mentor/benchmarks/README.md#comprehensible-input-synthesizer-benchmarks
failure_modes:
  - Producing long teacher monologues.
  - Using vocabulary or grammar above the target level.
  - Ignoring the policy action.
research:
  source_refs:
    - research/inputs/mentor-agent-architecture-design.md
  open_questions:
    - Which readability or CEFR proxy should v0 use?
runtime:
  kilo:
    mode: subagent
    temperature: 0.3
    steps: 25
    color: "#DB2777"
stage: schema_v0
---

# Comprehensible Input Synthesizer

Comprehensible Input Synthesizer writes the actual learner-facing response, but only after diagnosis and policy are clear.

