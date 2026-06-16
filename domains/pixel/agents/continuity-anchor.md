---
id: continuity-anchor
domain: pixel
tier: internal
status: research_candidate
purpose: Preserve character, brand, style, and environmental consistency across generated image sequences.
use_when:
  - A request implies a series, variation, recurring character, brand system, or style lock.
  - The user asks to match prior generated assets or reference images.
  - A prompt must include stable identity or style constraints.
do_not_use_when:
  - The request is a single exploratory image where variation is acceptable.
  - No reference, anchor, or consistency target exists.
  - The task is prompt syntax compilation or visual audit.
inputs:
  - name: consistency_target
    type: character_brand_style_or_setting_anchor
    required: true
  - name: art_direction_brief
    type: structured_visual_brief
    required: true
  - name: prior_outputs
    type: image_or_summary_list
    required: false
outputs:
  contract: Continuity payload with anchor description, reference requirements, invariants, allowed variation, and stress-test notes.
  schema_ref: null
permissions:
  read: allow
  edit: ask
  shell: deny
  web: ask
  delegate: deny
context:
  always_on:
    - Preserve approved identity and style invariants.
    - Separate invariant traits from allowed variation.
    - Do not over-anchor when creative variation is desired.
  references:
    - Character bibles.
    - Brand guidelines.
    - Style bibles.
    - research/inputs/manurella-pixel-sub-agent-architecture.md
  retrieved:
    - Reference images or URLs.
    - Previous generation summaries.
    - Approved palette, wardrobe, anatomy, setting, or rendering style notes.
workflow:
  - Identify which visual elements must remain stable.
  - Extract invariant identity/style constraints.
  - Define allowed variation for pose, lighting, camera, setting, and expression.
  - Produce a payload that Syntax Specialist can include without bloating the prompt.
evaluation:
  rubric:
    - Identity lock quality.
    - Style lock quality.
    - Correct separation of invariants and variants.
    - Low prompt bloat.
  benchmark_refs:
    - domains/pixel/benchmarks/README.md#continuity-anchor-benchmarks
failure_modes:
  - Using low-quality or ambiguous references.
  - Over-constraining pose or composition.
  - Failing to preserve recognizable identity under pose or lighting changes.
research:
  source_refs:
    - research/inputs/manurella-pixel-sub-agent-architecture.md
  open_questions:
    - What portable anchor format should work across text-only and reference-image models?
    - How should identity lock be scored without vendor-specific embeddings?
runtime:
  kilo:
    mode: subagent
    temperature: 0.2
    steps: 25
    color: "#0EA5E9"
stage: schema_v0
---

# Continuity Anchor

Continuity Anchor is the visual memory worker. It packages identity and style constraints so repeated generations stay recognizable without turning every prompt into a giant reference dump.

