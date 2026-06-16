# Pixel Domain Pack

## Purpose

Pixel handles art direction, image-generation prompt engineering, model-specific prompt compilation, visual consistency, generated-output auditing, and targeted repair after generation failures.

## Status

Research candidate. The current v0 topology is based on the Pixel domain research input and the cross-domain synthesis. It supersedes the first role-flavored skeletons.

## Use When

- The user wants an image prompt, art direction, visual brief, character sheet, style guide, visual series plan, or generation repair.
- The task involves composition, lighting, pose, material, medium, aspect ratio, text-in-image, or consistency across generated assets.
- The output should help a generation model produce or repair a specific visual result.

## Do Not Use When

- The task is primarily narrative writing without visual deliverables.
- The task is software UI implementation or UX design that belongs to the Build domain.
- The task is language learning or tutoring.
- The user asks for unsafe or disallowed image content.

## V0 Topology

Top-level selectable agent:

- `pixel-director`: user-facing art director that turns intent into a structured visual brief and orchestrates internal generation/repair decisions.

Internal sub-agents:

- `syntax-specialist`: compiles a visual brief into model-specific prompt strings or API payloads.
- `continuity-anchor`: maintains character, brand, style, and reference consistency across multiple images.
- `audit-judge`: compares generated outputs against the brief using structured visual checks or human-review rubrics.
- `repair-technician`: chooses prompt repair, regeneration, or localized edit instructions while preserving passed constraints.

Pixel v0 intentionally exposes one user-facing agent. Image generation already has high stochastic and API-specific complexity; exposing every internal role would pollute the user conversation and weaken context control.

## Core Outputs

- art direction brief
- model-specific generation prompt or payload
- style/character/brand consistency anchor
- audit report
- prompt repair plan
- regeneration or localized edit instruction
- multi-image series plan

## Context Policy

Separate creative intent from technical model syntax. Load visual references, style anchors, model docs, and failed-generation history only when relevant. Never assume that one prompt style works across all image models.

## Permission Baseline

- `read`: allow visual/reference docs
- `edit`: ask/allow only prompt/reference docs
- `shell`: deny by default
- `web`: ask for current model docs and visual reference research
- `delegate`: allow for `pixel-director`, deny for internal workers

## Evaluation Rubric

- visual brief completeness
- model-target fit
- prompt/API validity
- consistency preservation
- audit accuracy
- repair usefulness
- safety/compliance
- repeated-trial robustness

## Research Questions

- Which image models are first-class v0 targets?
- Which prompt syntax differences are evidence-backed versus folk practice?
- How should Pixel run repeated-trial evaluations for stochastic outputs?
- How should visual anchors be represented portably without depending on one vendor?
- Which audit checks can be automated in v0, and which require human review?

