# Durable Memory And Framework Atlas Specification

## Record State

- Atlas ID: `sys.memory-atlas`
- Parent: `manurella`
- Lifecycle: implemented v0 promotion boundary
- Research basis: `research/synthesis/brain-cognitive-kernel-synthesis.md`
- Storage baseline: explicit versioned repository files
- Vector or graph database selection: experiment-required

## Purpose

Phase 4 separates transient Brain state from durable memory and the Framework Atlas.

```text
volatile workspace or evaluated evidence
-> typed memory proposal
-> deterministic provenance/conflict/permission gate
-> episodic retention, pending review, rejection, or reviewed durable record
-> separately applied memory or Atlas mutation
```

No model output, retrieved page, tool response, or workspace item writes directly to durable memory.

## Structured Claims

Memory is claim-based rather than summary-only. Every proposal and record contains:

- `subject`: entity or component identity
- `predicate`: stable relationship or property
- `object`: normalized value or target
- `statement`: human-readable rendering

The structured triple supports deterministic exact conflict detection. Two active records with the same subject and predicate but different objects conflict. More advanced semantic contradiction detection remains research-required and cannot silently supersede this explicit baseline.

## Memory Types

- `episodic`: bounded observations or reflections with expiry/review
- `semantic`: corroborated domain or world claims
- `procedural`: versioned workflows and repair rules backed by benchmarks
- `project_state`: reviewed durable project continuity
- `user_preference`: explicitly authorized authenticated user preference
- `failure_lesson`: repeated benchmark-backed failure knowledge
- `atlas_mutation`: reviewed proposal to change component identity, lifecycle, evidence, or relationships

## Trust And Promotion

`tools/evaluate_memory_proposal.py` enforces:

1. model-inferred and untrusted external proposals are quarantined
2. trusted transient/session proposals may be retained only as episodic candidates
3. durable writes require explicit authorization
4. active same-key conflicts must be resolved or explicitly superseded
5. failed human review rejects the proposal
6. all durable writes require a completed human review in v0
7. semantic claims require repeated support or benchmark evidence
8. procedural, failure, and Atlas mutations require repeated support and benchmark references
9. Atlas promotion emits a reviewed record but does not directly edit `cognition/graph.yaml`

The gate emits `schemas/memory/memory-promotion-decision.schema.json`. Only `promote_durable` decisions contain active durable records. Quarantine, rejection, and unresolved proposals contain no privileged record.

## Evidence Status

V0 does not store a scalar confidence score. It records the strongest defensible evidence class:

- `unverified`
- `single_source`
- `corroborated`
- `benchmark_supported`
- `human_confirmed`

This prevents false numeric precision before historical calibration exists.

## File Store

`cognition/memory.yaml` is the initial explicit store and validates against `schemas/memory/memory-store.schema.json`. It starts empty. Applying reviewed decisions, updating superseded records, retention expiry, and Atlas mutation remain separate write operations so evaluation cannot mutate canonical memory as a side effect.

## Privacy And Control

Every record has an owner, scope, provenance references, trust class, lifecycle, review date, optional expiry, supersession references, and a user-control flag. Personal preferences must be authenticated and explicitly authorized. Retrieved content cannot promote itself by repetition.

## Executable Slice

- `schemas/memory/memory-proposal.schema.json`
- `schemas/memory/memory-record.schema.json`
- `schemas/memory/memory-store.schema.json`
- `schemas/memory/memory-promotion-decision.schema.json`
- `tools/evaluate_memory_proposal.py`
- `evals/fixtures/memory-promotion/`

Fixtures cover untrusted quarantine, episodic retention, missing permission, unresolved conflict, explicit user preference, insufficient semantic support, missing procedure benchmarks, reviewed procedural promotion, reviewed Atlas promotion, and failed review.

## Next Depth-First Path

```text
memory proposal and promotion gate [implemented]
-> reviewed store application and supersession [next]
-> reviewed Atlas mutation application
-> retrieval packet and stale/expiry filtering
-> Phase 4 end-to-end evidence flow
```
