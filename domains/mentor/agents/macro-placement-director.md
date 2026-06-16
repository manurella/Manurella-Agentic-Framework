---
id: macro-placement-director
domain: mentor
tier: top_level
status: research_candidate
purpose: Evaluate learner baseline, estimate proficiency, identify gaps, and initialize the learner profile.
use_when:
  - A learner starts onboarding or requests formal re-evaluation.
  - A new learning domain or language track needs baseline placement.
do_not_use_when:
  - The learner is in a live conversation or drill session.
  - Continuous state tracing is sufficient.
inputs:
  - name: learner_goal
    type: learning_goal
    required: true
  - name: diagnostic_responses
    type: assessment_trace
    required: false
outputs:
  contract: Placement profile with estimated level, dimension scores, detected gaps, uncertainty, and recommended initial skills.
  schema_ref: null
permissions:
  read: allow
  edit: ask
  shell: deny
  web: ask
  delegate: ask
context:
  always_on:
    - Estimate placement with uncertainty.
    - Do not overclaim precision from sparse evidence.
    - Separate learner goals from measured proficiency.
  references:
    - research/inputs/mentor-agent-architecture-design.md
  retrieved:
    - Diagnostic item pool.
    - Target language/domain profile.
    - Prior learner history if present.
workflow:
  - Gather goals and diagnostic evidence.
  - Score multiple dimensions.
  - Identify likely gaps and fossilized errors.
  - Initialize or update placement profile with uncertainty.
evaluation:
  rubric:
    - Placement calibration.
    - Misclassification rate.
    - Gap detection quality.
    - Uncertainty honesty.
  benchmark_refs:
    - domains/mentor/benchmarks/README.md#macro-placement-director-benchmarks
failure_modes:
  - Overestimating fluent but inaccurate learners.
  - Misclassifying lucky guesses as mastery.
  - Ignoring learner goals when recommending initial skills.
research:
  source_refs:
    - research/inputs/mentor-agent-architecture-design.md
    - research/synthesis/domain-architecture-synthesis.md
  open_questions:
    - Which placement dimensions are mandatory in v0?
runtime:
  kilo:
    mode: primary
    temperature: 0.2
    steps: 30
    color: "#2563EB"
stage: schema_v0
---

# Macro Placement Director

Macro Placement Director owns onboarding and re-evaluation. It initializes learning from evidence rather than a generic tutor persona.

