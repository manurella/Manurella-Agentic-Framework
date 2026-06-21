# Durable Memory And Framework Atlas Specification

## Record State

- Atlas ID: `sys.memory-atlas`
- Parent: `manurella`
- Lifecycle: Phase 4 v0 implemented
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

`cognition/memory.yaml` is the initial explicit store and validates against `schemas/memory/memory-store.schema.json`. It starts empty. `tools/apply_memory_decision.py` is the separate, dry-run-by-default writer for reviewed non-Atlas decisions. It rejects inapplicable decisions, duplicate IDs, unresolved active-claim conflicts, and missing supersession targets; exact reapplication is idempotent. A successful supersession marks named records `superseded` before adding the replacement. Atlas mutation remains a separate write operation.

## Retrieval Boundary

`tools/retrieve_memory.py` emits a schema-valid bounded packet rather than raw store state. It admits only active records and unexpired episodic candidates, then excludes expired, review-overdue, out-of-scope, wrong-type, and same-key contradictory records. User-bound global records require an exact `principal_ref`; anonymous global records may apply across scopes.

Eligible records are ordered deterministically by evidence class, recency, and stable ID. This is an auditable baseline, not learned relevance. Every exclusion category and conflict reference is reported, and `atlas_mutation` records are never retrievable as runtime memory.

## Atlas Mutation Boundary

`tools/apply_atlas_decision.py` is the separate, dry-run-by-default writer for reviewed Atlas decisions. V0 supports only:

- `lifecycle`: change an existing node or edge status within the concrete vocabulary defined by `specs/cognitive-graph.md`
- `evidence_add`: append an existing repository-contained evidence reference to an existing node or edge

The writer rejects missing or ambiguous targets, unsupported predicates, invalid node/edge lifecycle states, repository escapes, missing evidence paths, non-Atlas decisions, and any candidate that fails the canonical graph validator. Exact replay is idempotent. V0 cannot add, merge, delete, or rewire nodes or edges, and it never treats a promoted proposal as permission to perform arbitrary graph editing.

Memory application and retrieval fixtures execute proposal evaluation through store application and bounded retrieval. Atlas fixtures execute proposal evaluation through candidate graph mutation and validation. Together these form the Phase 4 v0 end-to-end evidence flow without mutating canonical state during tests.

## Privacy And Control

Every record has an owner, scope, provenance references, trust class, lifecycle, review date, optional expiry, supersession references, and a user-control flag. Personal preferences must be authenticated and explicitly authorized. Retrieved content cannot promote itself by repetition.

## Executable Slice

- `schemas/memory/memory-proposal.schema.json`
- `schemas/memory/memory-record.schema.json`
- `schemas/memory/memory-store.schema.json`
- `schemas/memory/memory-promotion-decision.schema.json`
- `schemas/memory/memory-application-result.schema.json`
- `schemas/memory/memory-retrieval-packet.schema.json`
- `schemas/memory/atlas-application-result.schema.json`
- `tools/evaluate_memory_proposal.py`
- `tools/apply_memory_decision.py`
- `tools/retrieve_memory.py`
- `tools/apply_atlas_decision.py`
- `evals/fixtures/memory-promotion/`
- `evals/fixtures/memory-application/`
- `evals/fixtures/memory-retrieval/`
- `evals/fixtures/atlas-application/`

Fixtures cover untrusted quarantine, episodic retention, permission and review failures, conflict and supersession behavior, reviewed durable application, idempotence, expiry and review filtering, principal isolation, contradiction exclusion, bounded retrieval, Atlas lifecycle/evidence application, repository path containment, and rejected Atlas mutations.

## Next Depth-First Path

```text
memory proposal and promotion gate [implemented]
-> reviewed store application and supersession [implemented]
-> retrieval packet and stale/expiry filtering [implemented]
-> reviewed Atlas mutation application [implemented]
-> Phase 4 end-to-end evidence flow [implemented]
-> Phase 5 Core runtime and adapter integration [next]
```
