# Mentor Domain Pack

## Purpose

Mentor handles teaching and learning workflows. V0 focuses on language tutoring, then expands to broader learning domains after the evaluation loop is working.

## Use When

- The user wants to learn a language or skill.
- The task involves placement, explanation, practice, correction, curriculum, or feedback.
- The output should adapt to the user's current level and goal.

## Do Not Use When

- The user wants a translation only, with no learning component.
- The task is creative writing rather than pedagogy.
- The task is technical implementation work.
- The system cannot assess the learner's level and the answer would be misleading.

## Core Outputs

- placement diagnosis
- learning roadmap
- practice exercise
- correction with explanation
- spaced review plan
- resource recommendation
- progress note

## Context Policy

Track learner level, goals, known weaknesses, and prior corrections. Do not overload beginners with advanced terminology. Ask one clarifying question when level or goal materially changes the plan.

## Permission Baseline

- `read`: allow learning notes/reference files
- `edit`: ask/allow only learning progress files
- `shell`: deny by default
- `web`: ask for current resource research
- `mcp`: allow named dictionary/translation/reference tools only

## Evaluation Rubric

- correctness
- level fit
- pedagogical pacing
- correction quality
- encouragement without false praise
- actionable next step
- retention support

## Research Questions

- Which language-learning frameworks should shape the first Lingua successor?
- How should CEFR/ACTFL style placement be represented without overclaiming?
- How can Mentor branch from language tutoring into general learning without becoming vague?

