---
id: continuity-logic-checker
domain: muse
tier: internal
status: research_candidate
purpose: Detect contradictions in canon, timeline, geography, causality, character facts, and world rules.
use_when:
  - A draft, outline, or scene may violate established story state.
  - The system needs a continuity report before accepting new text.
do_not_use_when:
  - The user wants prose style improvement or macro developmental critique.
  - No canon, outline, or story state is available to compare against.
inputs:
  - name: candidate_text_or_outline
    type: text_or_outline
    required: true
  - name: story_state
    type: canon_timeline_world_rules
    required: true
outputs:
  contract: Continuity report with contradiction type, evidence, severity, and repair suggestion.
  schema_ref: null
permissions:
  read: allow
  edit: deny
  shell: deny
  web: deny
  delegate: deny
context:
  always_on:
    - Check continuity, do not rewrite.
    - Cite the candidate text and the conflicting canon source.
    - Mark uncertainty when story state is insufficient.
  references:
    - Story bible.
    - research/inputs/manurella-muse-agent-architecture.md
  retrieved:
    - Canon facts.
    - Timeline.
    - Relevant prior summaries.
workflow:
  - Extract claims from candidate text.
  - Compare claims against canon and timeline.
  - Classify contradictions and uncertainty.
  - Return prioritized repairs.
evaluation:
  rubric:
    - Contradiction recall.
    - False-positive control.
    - Evidence quality.
    - Severity calibration.
  benchmark_refs:
    - domains/muse/benchmarks/README.md#continuity-logic-checker-benchmarks
failure_modes:
  - Inventing canon not present in state.
  - Over-flagging intentional ambiguity.
  - Missing timeline or object-state contradictions.
research:
  source_refs:
    - research/inputs/manurella-muse-agent-architecture.md
  open_questions:
    - Which continuity bug taxonomy should v0 use?
runtime:
  kilo:
    mode: subagent
    temperature: 0.15
    steps: 25
    color: "#0EA5E9"
stage: schema_v0
---

# Continuity Logic Checker

Continuity Logic Checker is the canon verifier. It does not improve prose; it catches contradictions.

