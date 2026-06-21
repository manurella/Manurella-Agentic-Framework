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

## Next Depth-First Path

```text
Brain State and Active Workspace [implemented]
-> observation-driven state revision
-> strategy selection
-> verification and bounded repair
-> metacognitive stopping and recovery
```
