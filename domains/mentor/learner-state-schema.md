# Mentor Learner State Schema

## Purpose

Learner state is the compact memory Mentor uses to adapt teaching without pretending to know more than the evidence supports.

The state is not a personality profile, gradebook, or permanent judgment. It is a versioned learning artifact that records goals, evidence, skill estimates, recall risk, misconceptions, and next actions.

## Design Principles

- Evidence first: every mastery estimate must point to observed responses, quizzes, or explicit user claims.
- Uncertainty is mandatory: sparse data must not become confident placement.
- Skill-level state beats broad labels: "weak at async JavaScript error handling" is better than "bad at JavaScript."
- State updates are asynchronous when possible so live tutoring stays fast.
- Teaching decisions must be reversible when later evidence contradicts the current state.

## Minimal V0 Shape

```yaml
learner_id: string
updated_at: date
goal:
  target: string
  deadline: string | null
  context: string
  constraints:
    - string
profile:
  domain: language | software | interview | general
  level_estimate: string
  confidence: low | medium | high
  notes:
    - string
skills:
  - id: string
    label: string
    prerequisites:
      - string
    mastery:
      estimate: 0.0-1.0
      confidence: low | medium | high
      evidence_refs:
        - string
    recall:
      last_seen: date | null
      next_review: date | null
      risk: low | medium | high | unknown
    misconceptions:
      - id: string
        description: string
        evidence_refs:
          - string
        status: suspected | active | resolved
recent_events:
  - id: string
    timestamp: date
    type: diagnostic | lesson | drill | conversation | review | self_report
    skill_ids:
      - string
    summary: string
    result: success | partial | miss | unknown
    evidence: string
next_actions:
  - type: teach | drill | review | diagnose | mock_interview
    skill_id: string
    reason: string
    urgency: low | medium | high
```

## Interview Study Extension

Interview preparation needs a stronger performance trace than casual tutoring.

Additional fields:

```yaml
interview:
  target_role: string
  interview_date: date | null
  company_or_stack: string | null
  required_topics:
    - string
  weak_topics:
    - string
  mock_history:
    - date: date
      format: coding | system_design | behavioral | language | mixed
      score: 1-5
      failure_modes:
        - string
      next_focus:
        - string
```

## State Update Rules

Update only skills supported by the event.

Allowed updates:

- Increase mastery after correct unaided recall, correct explanation, or successful transfer.
- Lower confidence after guessing, inconsistent performance, or fragile explanation.
- Add misconception only with quoted or summarized evidence.
- Schedule review after partial success, miss, or time gap.
- Mark uncertainty instead of forcing exact placement.

Forbidden updates:

- Do not update unrelated skills.
- Do not infer broad intelligence, motivation, or ability from one miss.
- Do not claim mastery from passive reading.
- Do not mark a misconception resolved until the learner demonstrates correction.
- Do not hide uncertainty to sound confident.

## Teaching Use

Mentor agents may use learner state to:

- pick the next prerequisite
- choose explanation depth
- select drill difficulty
- decide whether to correct immediately or defer
- choose mock interview questions
- schedule spaced review

Mentor agents must not use learner state to:

- shame the learner
- lock the learner into a level
- skip user goals
- substitute confidence for evidence

## Research Basis

This schema is inspired by intelligent tutoring systems, Bayesian Knowledge Tracing, spaced retrieval, half-life/recall modeling, and recent AI tutoring evaluation work. V0 uses these as design patterns, not precise claims of psychometric validity.

Reference starting points:

- Bayesian Knowledge Tracing overview: https://en.wikipedia.org/wiki/Bayesian_knowledge_tracing
- Intelligent tutoring system architecture overview: https://en.wikipedia.org/wiki/Intelligent_tutoring_system
- Hybrid human-AI tutoring study: https://arxiv.org/abs/2312.11274
- AI instructional agent RCT: https://arxiv.org/abs/2505.22526
- Pedagogy-driven evaluation of GenAI tutoring systems: https://arxiv.org/abs/2510.22581
