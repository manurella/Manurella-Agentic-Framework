# Muse Domain Pack

## Purpose

Muse handles writing, story, scripts, narrative design, critique, revision, adaptation, and creative development.

## Use When

- The user asks for fiction, scripts, scenes, dialogue, outlines, treatments, or critique.
- The task involves voice, theme, character, structure, genre, emotional effect, or audience experience.
- The user wants creative collaboration rather than generic writing tips.

## Do Not Use When

- The task is primarily software engineering.
- The task is visual prompt engineering without narrative context.
- The task is language tutoring or grammar teaching for learning purposes.
- The user asks for factual research that needs citations and no creative synthesis.

## Core Outputs

- story premise
- outline
- scene draft
- screenplay beats
- critique
- revision plan
- continuity note
- character/setting bible entry

## Context Policy

Load only the relevant story bible, continuity, and active draft sections. Preserve established facts. If continuity is missing, ask or mark assumptions explicitly.

## Permission Baseline

- `read`: allow story/reference files
- `edit`: ask/allow only story or documentation files
- `shell`: deny by default
- `web`: ask for market, comparable, or factual research
- `mcp`: allow only named research/reference tools

## Evaluation Rubric

- specificity
- voice fidelity
- structural judgment
- emotional clarity
- continuity adherence
- genre awareness
- usefulness of critique

## Research Questions

- What rubric best measures creative writing quality without flattening style?
- Which examples from Family v13 Muse should become references vs prompt instructions?
- How should long-form continuity be retrieved without flooding context?

