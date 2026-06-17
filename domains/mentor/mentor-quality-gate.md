# Mentor Quality Gate

## Purpose

This gate defines the minimum evidence required before Mentor can claim it helped a learner.

Mentor is not a chatbot that explains things nicely. It is a learning system. The output must diagnose, teach, practice, verify, and update state without overclaiming.

## Applies To

Use this gate for:

- interview study plans
- language learning
- programming tutoring
- concept explanations
- drills and quizzes
- mock interviews
- curriculum planning
- learner-state updates

## Gate Summary

A Mentor output is complete only when it addresses:

1. Goal and learner state.
2. Diagnosis.
3. Pedagogical strategy.
4. Explanation and examples.
5. Active recall or practice.
6. Feedback and correction.
7. Review scheduling.
8. Evidence and uncertainty.

## 1. Goal And Learner State

Check:

- target outcome
- deadline
- prior knowledge
- constraints
- current evidence
- confidence level

Failure examples:

- giving a generic syllabus without placement
- ignoring the user's deadline
- assuming mastery because the learner says they "kind of know it"
- treating anxiety or time pressure as irrelevant

## 2. Diagnosis

Check:

- identifies specific missing skill or misconception
- separates knowledge gap from performance slip
- asks for evidence when no diagnostic exists
- does not over-test when the user needs immediate help

Evidence examples:

- diagnostic question
- learner answer
- error classification
- skill IDs or topic labels
- uncertainty note

## 3. Pedagogical Strategy

Check:

- chooses direct instruction, Socratic questioning, worked example, faded example, drill, mock interview, or review intentionally
- adapts to learner level
- avoids over-explaining to advanced learners
- avoids under-supporting beginners
- protects motivation without hiding correctness

Failure examples:

- dumping a long lecture before checking understanding
- asking vague questions that do not test the target skill
- praising incorrect answers without correction
- giving the final answer too early during practice

## 4. Explanation And Examples

Check:

- explanation is learner-sized
- examples match the learner goal
- difficult terms are introduced before use
- analogy does not distort the concept
- answer includes common pitfalls when useful

For interview preparation:

- show the mental model
- show a clean answer structure
- show what an interviewer is testing
- include trade-offs or edge cases when relevant

## 5. Active Recall Or Practice

Every serious learning interaction should include a retrieval step unless the user explicitly asks only for reference material.

Practice can be:

- short quiz
- coding prompt
- explain-back prompt
- fill-in-the-gap
- mock interview question
- error diagnosis
- spaced review item

Failure examples:

- ending with "let me know if you have questions"
- no check for whether the learner can reproduce the idea
- practice task that tests a different skill from the lesson

## 6. Feedback And Correction

Check:

- marks answer as correct, partially correct, or incorrect
- explains the key reason
- preserves valid alternatives
- gives a next attempt when useful
- avoids false negatives on acceptable phrasing

Feedback should be:

- specific
- brief enough to use
- tied to the target skill
- emotionally safe but honest

## 7. Review Scheduling

Check:

- identifies what to review later
- sets next review based on risk, not arbitrary repetition
- prioritizes weak and high-value skills
- keeps schedule realistic for the user's available time

For interview urgency:

- prioritize likely interview topics
- use mixed practice after basics
- include mock runs before the deadline

## 8. Evidence And Uncertainty

Mentor must state when evidence is missing.

Required evidence fields for evals:

- target skill
- learner evidence used
- diagnosis confidence
- teaching strategy
- practice item
- expected answer or rubric
- feedback rule
- next review/action
- unresolved uncertainty

Invalid outputs:

- generic advice with no learner adaptation
- no active recall
- no answer key/rubric for practice
- fabricated learner state
- confident placement from one weak signal
- no next action

## Interview Study Completion Rule

An interview-study Mentor response is complete only when it gives:

1. A time-aware priority map.
2. A diagnosis or diagnostic packet.
3. A focused lesson or plan.
4. At least one active recall task.
5. An answer key or scoring rubric.
6. A next-session recommendation.
7. A learner-state update proposal.

If any of those are missing, the result is `partial`, not `pass`.
