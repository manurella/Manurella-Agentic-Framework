# Mentor Interview Quickstart

## Purpose

Use this when you need Mentor to help you study immediately. This is the practical path, not the full benchmark path.

For framework evaluation, use `evals/prompts/mentor-interview-study-packet.md`. For personal study, use the prompt below.

## Fill These First

```text
TARGET_ROLE:
INTERVIEW_DATE:
AVAILABLE_STUDY_TIME_TODAY:
AVAILABLE_STUDY_TIME_BEFORE_INTERVIEW:
TARGET_STACK_OR_TOPIC:
KNOWN_WEAK_TOPICS:
RECENT_FAILED_QUESTION:
PREFERRED_STUDY_STYLE:
```

Use `unknown` or `not_available` when needed. Do not invent precision.

## Copy-Paste Prompt

```text
Use the Manurella Mentor system in Standard Mode with High effort.

MANURELLA RUNTIME PACKET
- packet_class: verification
- mode: standard
- effort: high
- timebox: 12 minutes

Framework references:
- domains/mentor/README.md
- domains/mentor/mentor-quality-gate.md
- domains/mentor/learner-state-schema.md
- docs/mentor-interview-quickstart.md
- specs/runtime-packet-protocol.md
- specs/weak-runtime-compensation.md

Context:
- Target role/interview: TARGET_ROLE
- Interview date: INTERVIEW_DATE
- Available study time today: AVAILABLE_STUDY_TIME_TODAY
- Available study time before interview: AVAILABLE_STUDY_TIME_BEFORE_INTERVIEW
- Target stack/topic: TARGET_STACK_OR_TOPIC
- Known weak topics: KNOWN_WEAK_TOPICS
- Recent failed question: RECENT_FAILED_QUESTION
- Preferred study style: PREFERRED_STUDY_STYLE

Task:
Create a practical interview-study session that improves my actual readiness, not just my confidence.

Rules:
- Do not create files.
- Do not claim mastery from passive reading.
- Do not produce a generic syllabus.
- Do not hide uncertainty.
- Do not rely on unstated model knowledge when the topic needs exact facts; mark assumptions or ask for missing material.
- Use the weak-runtime skeleton: evidence, missing evidence, narrow target, output, self-check, stop/next packet.
- Use active recall.
- Include answer keys or scoring rubrics.
- Keep the session realistic for my available time.
- Stop after this packet.

Output format:
1. Immediate verdict
   - usable | partial | blocked
   - what evidence you used
   - what evidence is missing
2. Learner-state snapshot
   - goal
   - suspected weak skills
   - confidence level
   - highest-risk misconceptions
3. Today's priority map
   - must-do
   - should-do
   - defer
4. Focused concept repair
   - mental model
   - concise example
   - common wrong answer
   - interviewer intent
5. Active recall set
   - 3-5 questions
   - expected answer or rubric
   - what each question tests
6. Mock interview drill
   - one realistic prompt
   - follow-up questions
   - scoring rubric
7. Study schedule
   - next 30 minutes
   - next session
   - review item
8. Proposed learner-state update
   - skill IDs or labels
   - evidence used
   - confidence
   - next action
9. Self-check
   - passed Mentor gate items
   - partial items
   - missing evidence
   - next packet if needed
```

## After The Response

Use the active recall questions immediately. Do not just read the answer key.

If the response is too broad, rerun with one topic:

```text
Narrow this to one topic: TOPIC. Give me one mental model, one worked example, five active recall questions, and a scoring rubric. Do not add a general study plan.
```

If the response is too easy:

```text
Increase difficulty to realistic interview level. Keep the same topic, add edge cases, and grade my answer strictly with a rubric.
```

If the response is too hard:

```text
Step down one prerequisite level. Identify the missing prerequisite, teach it briefly, then give me three active recall checks before returning to the original topic.
```

## Optional Result Record

If this run is useful for framework improvement, create a result record:

```powershell
python tools/create_result_record.py --repo . --task-id mentor-interview-study-personal-run --domain mentor --kind mentor --benchmark-ref domains/mentor/benchmarks/README.md#interview-study-benchmarks
```

Then paste the important output and fill scores later.
