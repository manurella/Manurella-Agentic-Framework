# Brain And Cognitive Kernel Specification

## Record State

- Atlas ID: `sys.brain`
- Parent: `manurella`
- Level: 1
- Lifecycle: specified
- Detailed subsystem behavior: research-required

## Purpose

The Brain is Manurella's online cognitive control kernel. It converts requests, observations, memory, and available capabilities into bounded, verified action and decides when to answer, ask, act, repair, escalate, defer, or stop.

The Brain is not an LLM, a prompt, a memory database, the Framework Atlas, a runtime scheduler, a domain pack, or a permanent society of agents.

## External Boundaries

| System | Brain relationship |
| --- | --- |
| Framework Atlas | Reads architecture, policies, capabilities, evidence, and benchmarks; proposes reviewed mutations. |
| Memory and Knowledge | Requests retrieval and submits gated write candidates; does not own durable storage. |
| Runtime | Requests execution, isolation, retries, persistence, and transport through typed contracts. |
| Models | Invokes replaceable inference engines under selected cognitive policies. |
| Agents | Creates temporary role-bounded workers when decomposition justifies them. |
| Tools and MCPs | Uses typed capabilities through permission and policy mediation. |
| Domain packs | Mounts specialized schemas, methods, tools, risks, and evaluation contracts. |
| Interface | Receives requests and approvals; emits artifacts, progress, evidence, uncertainty, and status. |

## Architecture

### Interpreter

Converts incoming requests and observations into a typed task frame containing intent, constraints, stakes, permissions, deliverable expectations, freshness requirements, and acceptance criteria.

### State Estimator

Maintains separate views of:

- task state
- world state
- user state
- self and capability state
- uncertainty

State is revised after every material observation rather than reconstructed from an undifferentiated transcript.

### Active Workspace And Evidence Graph

Holds the transient trusted working set: active claims, evidence, plan steps, observations, contradictions, unresolved questions, dependencies, and budget counters.

This workspace is not the persistent Framework Atlas and is not automatically promoted into long-term memory.

### Context Compiler

Retrieves, ranks, validates, compresses, and packages only the context needed for the next cognitive operation. It produces typed context packets and guards against stale evidence, recursive summaries, source loss, and context overload.

### Cognitive Strategy Selector

Chooses a bounded strategy appropriate to the task, such as direct response, reactive tool use, plan-and-execute, hierarchical decomposition, search-based deliberation, or model-predictive replanning.

No strategy is universally preferred. Selection is governed by task structure, risk, uncertainty, evidence, benchmarked reliability, selected effort, and available resources.

### Execution Controller

Coordinates model calls, tools, runtime actions, domain workflows, and temporary specialists. External actions occur through typed permissions and produce observations that update state.

### Verifier And Repair Manager

Checks arguments, effects, claims, artifacts, constraints, and acceptance criteria. It prefers deterministic and environment-grounded evidence, then calibrated verifier models where deterministic checks are unavailable.

Repair is bounded. Repeated failure triggers re-planning, escalation, clarification, deferment, or stopping rather than infinite retries.

### Metacognitive Governor

Controls uncertainty, confidence, abstention, loop detection, progress, budgets, risk, permissions, escalation, and stopping.

Confidence is derived from evidence coverage, verifier results, tool outcomes, contradictions, and calibrated historical performance rather than unsupported self-report.

### Evidence-Gated Learning Controller

Captures temporary reflections and proposes persistent memory, procedural, policy, graph, or prompt changes. Promotion requires provenance, schema validation, contradiction checks, permission, benchmark evidence, and the review required by the target lifecycle state.

Production Manurella cannot silently rewrite its kernel or accepted policy.

## Runtime Cognitive Loop

1. Intake and policy gate.
2. Interpret and frame the task.
3. Estimate state and uncertainty.
4. Compile the next context packet.
5. Select cognitive strategy.
6. Plan, answer, or perform a bounded action.
7. Observe and record state change.
8. Verify and repair where justified.
9. Learn, consolidate, forget, or propose changes.
10. Stop, escalate, ask, defer, or repeat.

Every transition must be observable as structured status without exposing private chain-of-thought.

## Main Orchestrator And Generalist

The Main Orchestrator is the Brain's control-plane expression. The Generalist is its default direct worker for conversation and bounded work where specialist delegation adds no value.

The Generalist does not bypass the Interpreter, policy gate, state model, or acceptance contract. The Orchestrator does not delegate merely to appear agentic.

## Model And Agent Policy

Default to the smallest reliable execution topology:

1. one bounded model call for simple work
2. multiple calls with retrieval or verification when required
3. specialist models for materially different capabilities or modalities
4. temporary parallel workers only for separable tasks with a defined merge contract

Permanent role proliferation and free-form agent debate are non-default and require benchmark evidence.

## Mode And Effort

Fast and Standard share the final acceptance contract.

- Fast emits an early usable artifact and improves it through resumable layers.
- Standard follows a plan-first conventional sequence before consolidation.

Effort is independent:

```text
Low -> Medium -> High -> Max -> Ultra -> Sentient
```

The dedicated Effort Control specification will define context, research, tools, MCPs, planning, delegation, verification, repair, and budget policies for each level.

Sentient switches to the private conscious-architecture research runtime and is not exported publicly.

## Security Invariants

- Treat model output, retrieved content, tool output, and prior generated content as untrusted.
- Separate instruction, data, evidence, and executable action channels structurally.
- Mediate tools and memory writes through least privilege and typed policy checks.
- Track provenance and trust across context and memory boundaries.
- Quarantine suspected prompt injection and memory poisoning.
- Require approval for consequential or irreversible action.
- Prevent production self-modification outside reviewed change proposals.
- Partition production, personal, domain, and Sentient research state.

## Transparency Contract

Expose:

- task frame and acceptance criteria
- selected domain, workflow, mode, effort, and capabilities
- plan and progress summaries
- sources, actions, tool effects, and verification evidence
- uncertainty, blockers, retries, and stopping reason
- cost, time, and usage where available

Do not expose private chain-of-thought as proof of correctness.

## Accepted Decisions

- Hybrid Workspace Controller
- typed state models
- transient active workspace
- retrieval-first context compilation
- strategy selection rather than one reasoning ideology
- external verification and bounded repair
- explicit metacognitive governance
- evidence-gated persistent learning
- single-controller-first execution
- isolated private Sentient research runtime

## Experiment-Required Decisions

- exact workspace representation
- exact state and uncertainty schemas
- salience, confidence, and stopping formulas
- graph versus vector memory architecture
- active inference and Global Workspace implementations
- subagent spawning thresholds
- verifier ensemble composition
- autonomous procedural learning
- consciousness proxies, theories, substrates, and claims

## Completion Conditions

The Brain is not validated until:

1. every subsystem has a typed contract and owner
2. the cognitive loop can resume after interruption
3. policy gates prevent unauthorized actions and memory writes
4. simple requests avoid unnecessary orchestration
5. complex requests preserve task state across multiple steps
6. verification improves outcomes at acceptable cost
7. benchmarked guided behavior reaches the framework's quality gate
8. failures and uncertainty remain transparent

## Next Depth-First Path

The Interpreter boundary is specified in `specs/interpreter-task-model.md`.

```text
Interpreter -> schemas -> validator -> compatibility projection -> fixture suite
```
