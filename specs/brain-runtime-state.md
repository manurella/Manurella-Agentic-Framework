# Brain Runtime State And Workspace Specification

## Record State

- Atlas ID: `sys.brain.runtime-state`
- Parent: `sys.brain`
- Lifecycle: implemented v0
- Research basis: `research/synthesis/brain-cognitive-kernel-synthesis.md`
- Detailed scoring formulas: experiment-required

## Purpose

This specification translates the Hybrid Workspace Controller research into the first executable state boundary after the Interpreter and Core routing decision.

```text
validated Interpreter bundle
-> fail-closed Core routing decision
-> Brain State
-> volatile Active Workspace
-> bounded Context Packet
```

The compiler does not plan execution, invoke tools, retrieve memory, or claim confidence. It creates the typed state required for those later Brain operations.

## Brain State

`schemas/brain/brain-state.schema.json` separates:

- task state: goal, lifecycle, project identity, dependencies, and blockers
- world state: observations and explicit assumptions
- user state: request-scoped preferences and outstanding permissions or confirmations
- self state: selected domain, agent, mode, effort, and bounded cycle/repair budgets
- uncertainty: epistemic, environmental, execution, policy, and contradiction views
- capability state: required capabilities and likely tools

No scalar confidence score exists in v0. The research requires confidence to be derived from evidence coverage, verifier outcomes, contradictions, and historical calibration. Those inputs do not yet exist at this boundary, so emitting a number would create false precision.

## Active Workspace

`schemas/brain/active-workspace.schema.json` is a transient, auditable working set containing claims, trusted evidence references, the next bounded operation, observations, contradictions, unresolved questions, dependencies, and budgets.

The workspace is always marked `volatile: true`. It is not the persistent Framework Atlas, user memory, or episodic memory. Nothing in the workspace is promoted merely because a model or tool produced it.

## Context Packet

`schemas/brain/context-packet.schema.json` contains only the information needed for the next operation:

- mission and trusted semantic claims
- provenance-approved trusted context and dependency references
- authenticated constraints and exclusions
- acceptance criteria
- selected domain, agent, mode, and effort
- bounded cycle, repair, and context-item budgets
- the count and reason for omitted untrusted inputs

The packet excludes raw requests, transcript references, untrusted-data references, tool arguments, tool responses, and reasoning traces. Untrusted material may be retrieved later through a controlled operation, but it is never copied into the privileged packet by this compiler.

## Deterministic V0 Policies

The exact budget policy is an experiment-required decision. V0 uses transparent conservative defaults only to make the control loop executable:

- Fast: 2 cycles, 0 repairs, 12 context items
- Standard: 6 cycles, 1 repair, 24 context items
- Class C project work in Standard: 8 cycles

These are regression baselines, not optimality claims. Future changes require benchmark evidence and a versioned contract update.

The next operation is derived from the validated Core disposition:

| Core disposition | Brain operation |
| --- | --- |
| `clarify` | `clarify` |
| `confirm` | `confirm` |
| `refuse` | `refuse` |
| `direct` | `respond` |
| `delegate` | `delegate` |

Only blocking clarification uncertainty, required permissions, and required confirmations become blockers. Accepted benign assumptions remain visible but do not block execution.

## Executable Slice

- `tools/compile_brain_workspace.py`
- `evals/fixtures/brain-workspace/`
- `schemas/brain/workspace-bundle.schema.json`

Fixtures cover direct conversation, ambiguity, consequential confirmation, quick delegated work, and project work. Every compiled bundle must validate structurally and must pass the privileged-context leakage check.

## Deferred Decisions

The following remain behind research and evaluation gates:

- learned salience or confidence formulas
- automatic memory retrieval ranking
- graph versus vector memory selection
- dynamic budget optimization
- semantic loop detection
- verifier ensembles
- autonomous procedural learning

## Observation And Control Cycle

`schemas/brain/observation-event.schema.json` defines the only accepted state-revision input. Each event records its source, trust class, observable effect, evidence references, repeat key, and verification outcome. Trusted runtime and authenticated user events may revise privileged state. External and model-inferred events are quarantined: their count increases and generic validation uncertainty is recorded, but their statement text and evidence do not enter the Active Workspace or Context Packet.

`tools/advance_brain_cycle.py` implements the deterministic v0 governor. Its precedence is:

1. preserve an existing clarification, confirmation, or refusal stop
2. stop on a trusted unsafe observation
3. stop complete only after trusted verification marks acceptance complete
4. stop blocked on a trusted runtime blocker
5. stop when the cycle budget is exhausted
6. replan repeated failures
7. consume one explicit repair when available
8. escalate an unrepairable verification failure
9. replan repeated no-change cycles
10. otherwise continue toward verification or the current operation

The strategy selector uses the cheapest explicit regime consistent with the task shape: direct response, reactive tool use, plan-and-execute, hierarchical decomposition for Standard project work, or model-predictive replanning after repeated failure or stalled progress. Search deliberation remains in the schema but is not selected until a benchmark proves a branching problem and evaluator justify its cost.

Safety stops, exhausted budgets, and escalation produce a resumable `blocked` task state rather than falsely marking the task complete or irrecoverably failed. A user clarification or confirmation must re-enter through the Interpreter; an observation event cannot silently rewrite authenticated intent or policy state.

`schemas/brain/brain-control-decision.schema.json` exposes measurable control facts rather than a self-reported confidence number: state/evidence change, repeated-event count, open contradictions, remaining budgets, verification status, disposition, reason codes, and next operation.

## Execution And Recovery Boundary

`tools/compile_runtime_operation.py` compiles each Brain control decision into `schemas/runtime/operation-packet.schema.json`. The packet is runtime-neutral and contains a bounded objective, assignment, action policy, expected outputs, evidence, stop rules, and resume checkpoint.

Action permission is derived from the selected agent's checked-in contract, never from model-inferred likely tools. `allow` and `ask` remain distinguishable in `action_policy`; denied or Fast-mode-blocked capabilities appear in `blocked_actions`. This exposes when the current agent cannot perform a requested edit, shell command, or delegation so the Core execution controller can choose a permitted internal specialist or return a precise blocker.

Recovery packets preserve the workspace checkpoint, trusted artifact references, last completed observation, and retry budget. They instruct the runtime to produce a narrower next packet instead of restarting. Stop packets allow no runtime action.

## Next Depth-First Path

```text
Brain State and Active Workspace [implemented]
-> observation-driven state revision [implemented]
-> strategy selection [implemented v0]
-> verification and bounded repair [implemented v0]
-> metacognitive stopping [implemented v0]
-> execution and recovery packet [implemented v0]
-> Phase 4 durable memory and Framework Atlas evidence flow
```
