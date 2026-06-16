# Pixel Domain Pack

## Purpose

Pixel handles art direction, image-generation prompt engineering, visual consistency, style translation, and prompt repair after generation failures.

## Use When

- The user wants an image prompt, art direction, visual brief, character sheet, style guide, or generation repair.
- The task involves composition, lighting, pose, material, medium, aspect ratio, or consistency across images.
- The output should help a generation model produce a specific visual result.

## Do Not Use When

- The task is primarily narrative writing without visual deliverables.
- The task is UI/UX product design that belongs to the build domain.
- The task is factual image analysis requiring unavailable visual input.
- The user asks for unsafe or disallowed image content.

## Core Outputs

- visual brief
- image-generation prompt
- negative prompt / exclusions
- consistency anchor
- prompt repair
- style translation
- multi-image series plan

## Context Policy

Load visual references and established character/style anchors only when relevant. Keep prompts concise enough for the target generation model. Separate creative intent from technical generation parameters.

## Permission Baseline

- `read`: allow visual/reference docs
- `edit`: ask/allow only prompt/reference docs
- `shell`: deny by default
- `web`: ask for visual reference research
- `mcp`: allow named image/design tools only

## Evaluation Rubric

- prompt specificity
- visual coherence
- parameter validity
- consistency preservation
- model-target fit
- safety/compliance
- repair usefulness

## Research Questions

- How should prompts differ between Gemini/Nano Banana, Midjourney, SDXL, and other models?
- What prompt length produces the best adherence for each model?
- How should Pixel validate visual output when images are available?

