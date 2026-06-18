# Cognitive Architecture Synthesis

> Historical v0 synthesis. `research/synthesis/brain-cognitive-kernel-synthesis.md`
> supersedes its Brain boundary, mode/effort ladder, and Sentient conclusions. Retain
> this file as provenance for the Cognitive Graph research path.

## Purpose

This synthesis promotes the stable findings from the cognitive research batch into Manurella v0 direction.

Raw research inputs:

- `research/inputs/manurella-cognitive-architecture-design.md`
- `research/inputs/manurella-cognitive-graph-architecture.md`
- `research/inputs/cognitive-graph-evolution-framework.md`
- `research/inputs/cognitive-graph-mind-map-design.md`
- `research/inputs/designing-ai-effort-control-systems.md`
- `research/inputs/manurella-agent-authoring-doctrine.md`

## Core Conclusion

Manurella needs a Cognitive Graph: a versioned, human-auditable map of domains, agents, skills, tools, context, eval evidence, failure modes, routing rules, modes, and effort levels.

The graph is not a claim of sentience. It is an engineering control layer that makes agent behavior explicit, inspectable, and evolvable.

## Neuroscience-Inspired Design Primitives

The biology metaphor is useful when translated carefully:

| Biological idea | Manurella translation |
| --- | --- |
| neurons | graph nodes such as agents, skills, tools, contexts, failure modes |
| synapses | typed weighted edges between nodes |
| plasticity | eval-driven strengthen/weaken/deprecate mutations |
| pruning | remove active use of weak or redundant paths while preserving history |
| consolidation | promote repeated successful behavior into specs or domain packs |
| attention | context selection and salience scoring |
| working memory | current task contract, active trace, retrieved context |
| long-term memory | curated project/domain graph and research evidence |
| prediction error | verifier failure, eval mismatch, timeout, human correction |
| homeostasis | permission ceilings, budgets, and stability gates |

Do not copy biology literally. The graph should stay deterministic enough to review in git and conservative enough to avoid self-modifying prompt drift.

## Cognitive Graph Role

The Cognitive Graph answers questions that a flat prompt cannot:

- Which domain should handle this task?
- Which agent or specialist should be active?
- What mode and effort are justified?
- What context is relevant and what should stay unloaded?
- What tools are allowed?
- What verifier or critic should judge the result?
- What failure modes are known for this path?
- What eval evidence supports this route?
- What changed after a failed run?

## Mode And Effort Separation

Mode controls workflow shape:

- `fast`: shortest workflow that can still satisfy the same acceptance bar.
- `standard`: default serious workflow with bounded delegation and verification.

Effort controls reasoning depth:

- `low`
- `medium`
- `high`
- `extra-high`
- `max`
- `ultra`

For runtimes with native effort controls, adapters should map effort directly where possible. For runtimes without native controls, adapters simulate effort through prompt policy, context loading, delegation limits, verifier requirements, and external runtime control.

## Agent Authoring Findings

The research strongly supports the existing Manurella direction: agents are not personas.

A real agent must define:

- purpose
- use boundaries
- non-use boundaries
- inputs
- output contract
- workflow
- context policy
- permissions
- mode/effort behavior
- failure modes
- eval rubric
- promotion requirements

The frontend example is the first recommended testbed because it exposes the weakness of shallow role prompts. A serious frontend system needs distinct concerns such as architecture, implementation, state flow, accessibility, visual QA, and performance review.

## Graph Evolution Findings

Graph changes must be evidence-bound.

Supported v0 mutation types:

- `add`
- `weaken`
- `strengthen`
- `deprecate`
- `merge`
- `remove_from_active_use`

Hard deletes should be avoided in v0. Historical relationships are useful for audit and regression analysis.

Mutation evidence can come from:

- deterministic verifier results
- benchmark scores
- runtime traces
- timeout/failure records
- human review
- repeated successful runs across models/runtimes

## Visualization Findings

The v0 visual layer should be simple and git-friendly:

- Markdown overview for humans.
- YAML graph for machine-readable structure.
- Mermaid diagrams for lightweight visual checks.

Heavy graph databases, GNN routing, and dynamic force-directed renderers should wait until the graph schema stabilizes.

## V0 Promotion Decisions

Promote now:

- Cognitive Graph concept.
- Typed node and edge taxonomy.
- Mode and effort as graph nodes.
- Eval-driven mutation rules.
- Human-review gates for graph changes.
- Mermaid/YAML/Markdown v0 representation.

Keep as research:

- GNN routing.
- Bayesian mutation math.
- automated graph mutation.
- dual-LLM quarantine architecture.
- force-directed production renderer.
- full active-inference optimization.

## Next Research Hooks

- Determine whether `ultra` should be a single effort level or a compound protocol.
- Define frontend graph slice in detail.
- Test whether graph-guided Standard Mode beats prompt-only Standard Mode.
- Design an MCP graph-query tool after graph schema stabilizes.
- Define how eval scores update edge confidence without overfitting to one model.
