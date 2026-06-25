# Runtime Adapter Evidence Boundary

## Record State

- Phase: 5
- Lifecycle: implemented v0 evidence compiler boundary
- Runtime posture: provider-neutral evidence chain, Kilo first
- Side effects: none

## Purpose

Adapter evidence must prove the whole runtime handoff chain, not just save a loose model transcript. `tools/compile_adapter_evidence.py` consumes a durable Brain workspace checkpoint, runtime session, deterministic Kilo projection, and normalized execution capture. It validates the chain, ingests the capture into an execution-observation bundle, and compiles recovery when the observation contains a trusted recoverable runtime blockage.

The output is a `runtime-adapter-evidence-bundle.v0` record that can be stored under `evals/results/` for actual runs. It contains IDs, digests, typed lifecycle metadata, observation outcome, and optional recovery result. It does not embed raw Kilo event payloads or model output text.

## Required Evidence

Every live adapter evidence bundle must provide:

- exact runtime name
- exact model name
- adapter version
- prompt/projection version
- runtime session ID
- operation packet ID
- projection ID
- capture ID
- raw-event stream digest when a raw stream exists
- model-output digest when model output exists
- typed verification status
- observed artifact refs, if any

The compiler rejects `model: unknown` by default. Older records with unknown model metadata remain historical diagnostics; new Phase 5 evidence should not repeat that gap unless the caller explicitly opts into an unknown-model exception for quarantine or backfill work.

## Trust Rules

- A capture document cannot grant itself trust.
- `--attest-runtime-capture` is a caller assertion that the adapter process observed lifecycle metadata and artifact refs directly.
- Unattested captures remain model-inferred no-change observations.
- Trusted recoverable timeout, cancellation, or unknown status flows through the recovery compiler.
- Projection substitution, tampered lineage, and schema-valid mismatches fail before evidence is emitted.

## Privacy Rules

The evidence bundle may contain:

- schema-valid IDs
- fixed framework statements
- runtime lifecycle metadata
- SHA-256 digests
- artifact refs
- typed verification results
- recovery packet/session/projection metadata

The evidence bundle must not contain:

- raw event payloads
- model output text
- tool arguments or responses
- reasoning or chain-of-thought
- raw transcript text

## Next Depth-First Path

```text
runtime-neutral session compilation [implemented]
-> Kilo operation-packet projection and validation [implemented]
-> execution observation ingestion [implemented]
-> recovery/resume integration [implemented]
-> Phase 5 end-to-end adapter evidence [implemented]
-> Phase 5 live Kilo evidence capture and result records [next]
```
