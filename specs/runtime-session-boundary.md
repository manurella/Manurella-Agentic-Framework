# Runtime Session Boundary

## Record State

- Phase: 5
- Lifecycle: implemented v0 compiler boundary
- Runtime posture: provider-neutral
- Side effects: none

## Purpose

The runtime session boundary compiles the implemented control spine into one adapter-ready artifact:

```text
trusted input envelope
-> Interpreter Task Frame, Acceptance Contract, and Clarification Decision
-> Core routing decision
-> Brain workspace and initial control cycle
-> governed memory retrieval
-> permission-bounded operation packet
-> runtime session bundle
```

`tools/compile_runtime_session.py` performs this composition without invoking a model, executing an action, writing memory, or mutating the Framework Atlas.

## Privacy Boundary

The session bundle does not embed the full Interpreter bundle. It carries only stable lineage identifiers, a bounded memory retrieval packet, and the operation packet. Fields that can expose raw transcript or internal reasoning state remain forbidden:

- `raw_request`
- `turn_refs`
- `untrusted_data_refs`
- `tool_arguments`
- `tool_responses`
- `reasoning`
- `chain_of_thought`

The normalized operation objective remains visible because an adapter needs a bounded mission. Retrieved or tool content cannot rewrite that objective.

## Permission Semantics

Only actions whose checked-in agent permission is `allow` appear in `allowed_actions`. Both `ask` and `deny` remain in `blocked_actions`; the packet's `action_policy` preserves which condition applies. A runtime adapter may narrow this policy but cannot broaden it.

## Memory Scope

V0 selects one deterministic retrieval scope:

1. project scope when the Task Frame has a project ID
2. selected domain scope for delegated non-project work
3. task scope for Core-owned non-project work

Authenticated principal filtering remains mandatory. The single-scope policy is a transparent baseline; hierarchical cross-scope ranking remains eval-required.

## Adapter Boundary

The compiler reports `pending_projection` and explicitly marks controls it does not enforce:

- provider execution
- model selection
- native effort control
- token accounting
- cost accounting

No provider-specific run may be described as executed merely because a session bundle compiled successfully.

## Next Depth-First Path

```text
runtime-neutral session compilation [implemented]
-> Kilo operation-packet projection and validation [next]
-> execution observation ingestion
-> recovery/resume integration
-> Phase 5 end-to-end adapter evidence
```
