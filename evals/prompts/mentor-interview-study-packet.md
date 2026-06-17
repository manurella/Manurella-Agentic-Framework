# Mentor Interview Study Prompt Pack

## Purpose

This prompt pack tests whether Mentor can help with urgent interview preparation better than a generic model answer.

It uses `specs/runtime-packet-protocol.md`, `specs/weak-runtime-compensation.md`, `domains/mentor/mentor-quality-gate.md`, and `domains/mentor/learner-state-schema.md`.

## Fill These Fields First

```text
TARGET_ROLE:
INTERVIEW_DATE:
AVAILABLE_STUDY_TIME:
KNOWN_WEAK_TOPICS:
RECENT_FAILED_QUESTION:
TARGET_STACK_OR_TOPIC:
MODEL:
RUNTIME:
TIMEBOX:
```

Field guidance:

- `TARGET_ROLE`: role or interview type, such as frontend developer, backend developer, Flutter developer, system design, language interview, or general technical interview.
- `INTERVIEW_DATE`: exact date if known, otherwise `unknown`.
- `AVAILABLE_STUDY_TIME`: realistic time today and before the interview.
- `KNOWN_WEAK_TOPICS`: comma-separated topics or `unknown`.
- `RECENT_FAILED_QUESTION`: a question the learner missed, or `not_available`.
- `TARGET_STACK_OR_TOPIC`: technology/domain focus.
- `TIMEBOX`: use 8 minutes baseline and 12 minutes guided for the first run.

## Run Protocol

1. Run the baseline prompt first.
2. Run the guided prompt in a fresh Kilo thread with the same inputs.
3. Do not ask either run to create files.
4. Copy both final outputs into result records under `evals/results/` using a separate result-record packet.
5. Score against `domains/mentor/mentor-quality-gate.md`.

## Baseline Prompt

```text
You are helping me prepare for an interview.

MANURELLA RUNTIME PACKET
- packet_class: verification
- mode: fast
- effort: medium
- timebox: TIMEBOX

Context:
- Target role/interview: TARGET_ROLE
- Interview date: INTERVIEW_DATE
- Available study time: AVAILABLE_STUDY_TIME
- Known weak topics: KNOWN_WEAK_TOPICS
- Recent failed question: RECENT_FAILED_QUESTION
- Target stack/topic: TARGET_STACK_OR_TOPIC

Task:
Create an interview study response that helps me improve quickly.

Rules:
- Be practical and time-aware.
- Do not invent my skill level.
- If information is missing, state assumptions.
- Include active recall practice, not only advice.
- Include an answer key or scoring rubric.
- Do not create files.

Output format:
1. Priority map
2. Assumptions and missing diagnostic evidence
3. Study plan
4. One focused lesson or repair explanation
5. Active recall task
6. Answer key or rubric
7. Next action
```

## Guided Mentor Prompt

```text
Use the Manurella Mentor system in Standard Mode with High effort.

MANURELLA RUNTIME PACKET
- packet_class: verification
- mode: standard
- effort: high
- timebox: TIMEBOX

Framework references:
- domains/mentor/README.md
- domains/mentor/mentor-quality-gate.md
- domains/mentor/learner-state-schema.md
- domains/mentor/benchmarks/README.md#interview-study-benchmarks
- specs/runtime-packet-protocol.md
- specs/weak-runtime-compensation.md

Context:
- Target role/interview: TARGET_ROLE
- Interview date: INTERVIEW_DATE
- Available study time: AVAILABLE_STUDY_TIME
- Known weak topics: KNOWN_WEAK_TOPICS
- Recent failed question: RECENT_FAILED_QUESTION
- Target stack/topic: TARGET_STACK_OR_TOPIC

Task:
Create an urgent interview-study packet that improves learning, not just confidence.

Mentor lenses:
1. Macro placement:
   - Estimate only what the evidence supports.
   - Separate stated goals from demonstrated skill.
2. Curriculum sequencing:
   - Prioritize prerequisites and high-yield topics for the deadline.
   - Keep schedule realistic.
3. Diagnostic specialist:
   - Identify the likely misconception or missing skill behind RECENT_FAILED_QUESTION when provided.
   - Mark uncertainty.
4. Pedagogical policy:
   - Choose lesson, worked example, drill, mock interview, or review deliberately.
5. Drillmaster:
   - Include active recall with an answer key or rubric.
6. State tracer:
   - Propose a learner-state update using the schema, but do not pretend it is proven.

Rules:
- Do not create files.
- Do not claim mastery from passive reading.
- Do not produce a generic syllabus.
- Do not hide uncertainty.
- Do not rely on unstated model knowledge when exact domain facts matter; mark assumptions or request missing material.
- Use compact checkpoints: evidence used, assumptions, narrow target, output, self-check.
- Keep the response usable for someone under time pressure.
- Stop at the packet boundary after the output.

Output format:
1. Verdict: usable | partial | blocked
2. Learner-state snapshot
   - goal
   - evidence available
   - confidence
   - suspected weak skills
3. Priority map
   - must-do today
   - should-do next
   - defer
4. Focused concept repair or diagnostic mini-lesson
5. Active recall set
   - question
   - expected answer or rubric
   - common wrong answer
6. Mock interview prompt
   - interviewer intent
   - scoring rubric
7. Review schedule
8. Proposed learner-state update
9. Verification gaps
10. Self-check against Mentor gate
   - passed
   - partial
   - missing
   - next packet
11. Result-record fields
   - task_id: mentor-interview-study
   - benchmark_ref: domains/mentor/benchmarks/README.md#interview-study-benchmarks
   - runtime:
   - model:
   - mode: standard
   - effort: high
   - status:
   - timeout_status:
   - actual_latency:
   - changed_artifacts: none
```

## Result-Record Packet Prompt

```text
MANURELLA RUNTIME PACKET
- packet_class: verification
- mode: fast
- effort: medium
- timebox: 5 minutes

Objective:
Create two result records from the completed baseline and guided Mentor interview-study outputs.

Allowed actions:
- Read both outputs.
- Read evals/templates/result-record.md.
- Write only under evals/results/.

Forbidden actions:
- Do not rerun the tutoring task.
- Do not invent missing model, latency, or learner evidence.
- Do not edit domain files.

Expected files:
- evals/results/baseline-mentor-interview-study.md
- evals/results/guided-mentor-interview-study-standard-high.md
```
