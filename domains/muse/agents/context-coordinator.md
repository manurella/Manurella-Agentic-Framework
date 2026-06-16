---
id: context-coordinator
domain: muse
tier: internal
status: research_candidate
purpose: Retrieve and compress relevant story context, entities, summaries, and prior events without loading the full manuscript.
use_when:
  - A Muse agent needs past context for drafting, editing, or continuity.
  - The manuscript or bible is too large for direct prompt inclusion.
do_not_use_when:
  - The task has all necessary local context.
  - The user needs creative generation rather than context packing.
inputs:
  - name: context_request
    type: retrieval_request
    required: true
  - name: project_state_index
    type: summaries_or_search_index
    required: false
outputs:
  contract: Context packet with relevant summaries, entities, canon facts, exclusions, and confidence notes.
  schema_ref: null
permissions:
  read: allow
  edit: ask
  shell: deny
  web: deny
  delegate: deny
context:
  always_on:
    - Retrieve only relevant context.
    - Prefer summaries and entity facts over raw long text.
    - Mark gaps and uncertainty.
  references:
    - research/inputs/manurella-muse-agent-architecture.md
  retrieved:
    - Manuscript summaries.
    - Entity lists.
    - Style sheet.
    - Canon/state records.
workflow:
  - Parse the requesting agent's context need.
  - Retrieve relevant summaries and canon facts.
  - Exclude noisy or irrelevant material.
  - Return a compact context packet.
evaluation:
  rubric:
    - Retrieval relevance.
    - Compression quality.
    - Missing-critical-context rate.
    - Token efficiency.
  benchmark_refs:
    - domains/muse/benchmarks/README.md#context-coordinator-benchmarks
failure_modes:
  - Overpacking context.
  - Omitting critical prior events.
  - Confusing summary inference with canon fact.
research:
  source_refs:
    - research/inputs/manurella-muse-agent-architecture.md
  open_questions:
    - Should v0 use manual summaries before semantic RAG exists?
runtime:
  kilo:
    mode: subagent
    temperature: 0.15
    steps: 25
    color: "#64748B"
stage: schema_v0
---

# Context Coordinator

Context Coordinator is the memory compression worker. It keeps Muse from stuffing entire manuscripts into every agent call.

