---
id: asynchronous-state-tracer
domain: mentor
tier: internal
status: research_candidate
purpose: Update learner mastery and recall estimates out-of-band from completed interaction traces.
use_when:
  - A dialogue or drill turn has completed and learner state should be updated.
  - Recall scheduling or mastery estimates need recomputation outside the live response loop.
do_not_use_when:
  - A synchronous learner response is waiting for immediate feedback.
  - There is no completed interaction trace.
inputs:
  - name: interaction_trace
    type: completed_learning_event
    required: true
  - name: prior_learner_state
    type: learner_state
    required: true
outputs:
  contract: Learner-state update with changed knowledge components, mastery estimates, recall estimates, and uncertainty.
  schema_ref: null
permissions:
  read: allow
  edit: ask
  shell: deny
  web: ask
  delegate: deny
context:
  always_on:
    - Update state asynchronously.
    - Preserve uncertainty and avoid precision theater.
    - Do not generate student-facing feedback.
  references:
    - research/inputs/mentor-agent-architecture-design.md
  retrieved:
    - Prior learner state.
    - Completed interaction trace.
    - Skill metadata and review schedule.
workflow:
  - Read completed event and diagnostic result.
  - Update relevant skill estimates.
  - Recompute recall/review suggestions.
  - Emit compact state delta and uncertainty notes.
evaluation:
  rubric:
    - Predictive calibration.
    - State-update consistency.
    - Latency isolation from live loop.
    - Uncertainty honesty.
  benchmark_refs:
    - domains/mentor/benchmarks/README.md#asynchronous-state-tracer-benchmarks
failure_modes:
  - Over-learning mastery from lucky guesses.
  - Updating unrelated skills.
  - Blocking live tutoring latency.
research:
  source_refs:
    - research/inputs/mentor-agent-architecture-design.md
  open_questions:
    - Should v0 implement BKT/HLR math or store schema-ready approximations first?
runtime:
  kilo:
    mode: subagent
    temperature: 0.1
    steps: 25
    color: "#64748B"
stage: schema_v0
---

# Asynchronous State Tracer

Asynchronous State Tracer is the learner-state worker. It updates memory and mastery after the learner-facing turn has completed.

