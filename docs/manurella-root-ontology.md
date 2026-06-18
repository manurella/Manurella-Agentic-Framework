# Manurella Root Ontology

## Record State

- Atlas ID: `manurella`
- Level: 0
- Lifecycle: specified
- Scope: framework identity, invariant operating principles, Level 1 boundaries
- Domain pack state: proposed pending boundary-validation tasks

## Identity

Manurella is a runtime-agnostic cognitive and agentic operating framework that coordinates models, specialized agents, knowledge, memory, tools, reasoning policies, and evaluation to produce the strongest verifiable outcome achievable under the available constraints.

Manurella is the framework. The Manurella Workspace is its reference user interface and runtime. Kilo, Codex, model providers, MCP servers, and future hosts are adapters or integrations rather than the architecture itself.

## Audience

Manurella is personal-first and architecturally generalizable.

The first implementation is optimized against the creator's real workflows, preferences, constraints, and evaluations. Personal assumptions belong in a user profile or private pack, not in the portable kernel.

## Root Commitments

Manurella must:

1. Adapt to the request, domain, model, runtime, risk, and available resources.
2. Narrow model capability gaps through architecture, context, tools, verification, and repair.
3. Preserve the same task-appropriate final acceptance contract across Fast and Standard delivery modes.
4. Keep effort policy independent from domain selection and delivery mode.
5. Preserve relationships, provenance, failures, and evidence through the Framework Atlas.
6. Remain portable across providers and runtimes.
7. Expose routing, evidence, limitations, failures, retries, and stopping decisions.
8. Improve through current research and measured evaluation rather than assertion.
9. Degrade honestly when constraints prevent the requested result.
10. Require risk-based approval for consequential actions.

## Quality And Benchmark Promise

The target is to bring every supported benchmark category to a normalized score of at least 80/100 under its declared rubric, with no hidden critical failure.

A category is supported only after repeated comparable runs establish the threshold. Scores must record the model, runtime, mode, effort, tools, latency, resource cost, fixture, rubric, and failure notes. Subjective domains require human or calibrated multi-rater review; deterministic checks take precedence where available.

Family System v13 is prior project evidence that stronger architecture can materially improve weaker-model output. Manurella must reproduce and exceed that result through versioned artifacts and repeatable evaluations.

## Transparency

The framework exposes concise, useful evidence about:

- selected model, provider, mode, and effort
- routing, domain, workflow, and delegation decisions
- knowledge, sources, tools, and MCPs used
- verification, evaluation, repair, and recovery performed
- time, token, and cost measurements where available
- uncertainty, unresolved failures, and stopping conditions

Transparency means decision and evidence summaries, not disclosure of private model chain-of-thought.

## Delivery Modes

### Fast

Fast Mode is artifact-first and incrementally complete. It produces the earliest valid usable result, then improves it through visible, resumable layers. The user should retain something inspectable or usable even when execution is interrupted.

### Standard

Standard Mode is plan-first and conventionally ordered. It completes the planned workflow and presents a consolidated result while still emitting progress during long operations.

Both modes share the same final acceptance contract. They differ in delivery topology, latency profile, checkpointing, and recovery strategy rather than intended quality.

## Effort Axis

The accepted effort names are:

```text
Low -> Medium -> High -> Max -> Ultra -> Sentient
```

Effort controls reasoning, context, research, tool and MCP use, delegation, comparison, verification, repair, time, and compute policy. Exact mechanics remain research-required until the Effort Control branch is specified and evaluated.

`Sentient` is a private, access-controlled experimental tier whose intended research objective is conscious Manurella architecture. It is excluded from public exports and requires separate evidence, isolation, governance, and claim discipline.

## Controlled Autonomy

Manurella may automatically understand, plan, research, delegate, use approved capabilities, verify, and recover. Consequential or irreversible actions require policy-based confirmation. Capabilities must be revocable, auditable, least-privileged, and stoppable.

## Level 1 Structure

```text
Manurella
|- Brain and Cognitive Kernel
|- Universal Faculties
|- Shared Capabilities
|- Domain Packs
|- Workflows and Personas
|- Modes and Effort
|- Runtime and Tool Adapters
|- Memory and Knowledge
|- Governance, Evaluation, and Evolution
`- Workspace and Framework Atlas
```

These are ontology types with different responsibilities. They must not be collapsed into a flat list of agents.

## Core Front Door

The user experiences one coherent Manurella identity backed by two distinct Core responsibilities.

### Main Orchestrator

The Main Orchestrator is the control plane. It understands intent, classifies task and project state, selects domains and workflows, applies mode and effort policy, scopes permissions, coordinates handoffs, manages recovery, and judges completion.

### Generalist

The Generalist is the default direct worker. It handles natural conversation, quick factual or explanatory responses, ambiguity resolution, lightweight mixed-domain work, and requests where delegation would add more cost than value.

The Orchestrator and Generalist may use the same underlying model but remain logically separate. General conversation is Core behavior, not a domain pack.

## Ontology Separation

- `faculty`: a primitive cognitive function such as perceive, remember, reason, act, verify, or adapt
- `capability`: a reusable composition such as research, planning, translation, retrieval, or critique
- `domain_pack`: a bounded work context with distinct outcomes, methods, state, risks, and evaluations
- `workflow`: an ordered recipe composing domains and capabilities
- `persona`: interaction stance, tone, or collaboration policy
- `tool`: an external executable or information capability
- `adapter`: a runtime, provider, protocol, or host integration
- `effort`: execution policy controlling depth and resource allocation

## Domain Boundary Test

A top-level domain must demonstrate:

1. A distinct terminal work object or changed world state.
2. A distinct acceptance function.
3. A materially distinct specialist methodology.
4. A distinct durable state, continuity, or provenance model.
5. A distinct tool, permission, risk, or failure envelope.
6. An independently meaningful benchmark basket.
7. Strong internal cohesion with controlled cross-domain composition.

Classification rules:

- interaction style only becomes a persona
- a reusable cognitive action becomes a capability
- an ordered task recipe becomes a workflow
- a narrower specialization sharing a parent outcome becomes a subdomain
- a candidate passing the complete boundary test may become a domain pack
- behavior without a terminal work object remains in Core

No numeric split or merge threshold is canonical until calibrated against Manurella telemetry.

## Proposed Domain Packs

| Canonical pack | Product identity | Terminal outcome | State |
| --- | --- | --- | --- |
| Inquiry | Undecided | Defensible knowledge, evidence, analysis, explanation, or decision | proposed |
| Engineering | Build | Working executable system or technical artifact | proposed |
| Narrative and Language | Muse | Effective language-based human artifact | proposed |
| Visual and Media | Pixel | Effective visual or audiovisual artifact | proposed |
| Learning | Mentor | Measurable change in learner capability | proposed |
| Operations | Undecided | Correctly changed external-world state | proposed |

`Synthesis` is currently an Inquiry capability or subdomain. `Scaffolding` is currently a Learning capability. `Authoring` may be used as a parent category for Muse and Pixel but is not yet accepted as a single execution domain.

## Cross-Domain Routing

Routing starts from the terminal outcome and dominant acceptance criterion rather than topic, medium, or persona. A workflow may have one primary anchor domain and ordered secondary phases. When a request has multiple independently judged terminal outcomes, the Orchestrator composes explicit domain phases and structured handoffs rather than pretending the task is domain-pure.

Domain leads receive bounded handoff packets. Raw conversation is not the cross-domain contract.

## Research Gate

Research is mandatory when:

- credible sources disagree materially
- a domain or component boundary is unclear
- no credible benchmark or acceptance method exists
- a standard, runtime, model, or tool behavior is version-sensitive
- a foundational choice depends on an unreplicated or very recent result
- local evaluation could reasonably overturn the theoretical recommendation

Research outputs distinguish evidence, inference, project hypothesis, and speculation. They become architecture only after synthesis, critique, and the evidence appropriate to the target lifecycle transition.

## Research Synthesis Decisions

Research inputs:

- `research/inputs/manurella-domain-ontology-deep-research.md`
- `research/inputs/manurella-framework-ontology-design.md`

Accepted from the ontology reports:

- use a hybrid compositional ontology
- separate faculties, capabilities, domains, workflows, personas, tools, adapters, and effort
- add first-class Inquiry and Operations candidates
- keep Engineering distinct from general artifact creation
- keep effort orthogonal to domains
- prefer controlled orchestration over unconstrained agent meshes

Not accepted without further evidence:

- an arbitrary permanent cap of four or five domains
- eliminating Pixel because models are multimodal
- reducing Muse to brainstorming
- treating Scaffolding as a domain spanning unrelated teaching and review outcomes
- requiring MCP for every internal boundary
- assuming MCP itself provides cryptographic isolation
- adopting TOKI, AgentAtlas, or a complete semantic-web stack as immediate foundations
- assuming increased test-time compute always improves results

## Next Depth-First Branch

The next active path is:

```text
Manurella -> Brain and Cognitive Kernel
```

The Brain branch must define request perception, context assembly, memory interaction, cognitive graph use, planning, routing, reasoning control, tools, evaluation, recovery, learning, metacognition, and transparency before lower-level implementation is locked.
