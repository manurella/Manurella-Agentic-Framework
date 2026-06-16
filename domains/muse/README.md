# Muse Domain Pack

## Purpose

Muse handles long-form creative writing, story architecture, world and character design, scene drafting, developmental editing, line/style editing, continuity validation, copyediting, and context coordination.

## Status

Research candidate. The current v0 topology is based on the Muse domain research input and the cross-domain synthesis. It supersedes the first role-flavored skeletons.

## Use When

- The user wants to plan, draft, revise, critique, or maintain creative writing.
- The task involves plot, character, theme, worldbuilding, scene work, prose style, screenplay/narrative structure, or continuity.
- The output must preserve author intent, genre promise, style, canon, and project state.

## Do Not Use When

- The task is primarily software building.
- The task is visual art direction or image prompting without narrative prose.
- The task is language tutoring or learning.
- The user wants factual research without a writing deliverable.

## V0 Topology

Top-level selectable agents:

- `muse-lead`: routes creative intent and maintains the project scratchpad.
- `world-character-architect`: builds worlds, lore, character webs, setting rules, and style-bible foundations.
- `narrative-designer`: creates plot structure, event graphs, chapter/scene plans, and pacing.
- `developmental-editor`: critiques macro structure, theme, character motivation, and pacing.
- `line-style-editor`: refines prose style, rhythm, voice, and sentence-level craft.

Internal sub-agents:

- `eventseed-subtasker`: breaks macro outlines into atomic scene beats.
- `scene-drafter`: expands one approved beat into prose.
- `continuity-logic-checker`: detects canon, timeline, causal, and world-rule contradictions.
- `copyeditor`: enforces style sheet, grammar, spelling, terminology, and mechanical consistency.
- `context-coordinator`: retrieves summaries, entities, and prior events without stuffing the full manuscript.

## Core Outputs

- story prototype
- world/character bible
- plot graph or outline
- atomic scene beats
- drafted scene
- editorial letter
- style revision
- continuity report
- copyedit report
- context retrieval packet

## Context Policy

Do not load whole manuscripts, craft manuals, or lore dumps by default. Use a scratchpad, style sheet, story prototype, summaries, and just-in-time retrieval. Preserve author intent and style diversity.

## Permission Baseline

- `read`: allow project writing docs
- `edit`: ask/allow only active draft, outline, or bible files
- `shell`: deny by default
- `web`: ask for current craft/source research
- `delegate`: allow for top-level agents, deny for internal workers

## Evaluation Rubric

- author-intent preservation
- structural coherence
- character motivation coherence
- continuity accuracy
- prose quality without homogenization
- style-sheet adherence
- context efficiency

## Research Questions

- Should screenwriting be a top-level specialist or a mode across narrative design and scene drafting?
- How should Muse evaluate creative quality without flattening distinct styles?
- How should story state move from text scratchpad in v0 to graph memory in v1?
- Which craft references are allowed as retrieved material versus always-on guidance?

