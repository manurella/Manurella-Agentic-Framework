# Execution Observation Boundary

## Record State

- Phase: 5
- Lifecycle: implemented v0 ingestion boundary
- Runtime posture: provider-neutral normalized capture
- Side effects: none

## Purpose

Runtime execution output is evidence input, not authority. `tools/ingest_runtime_observation.py` converts one validated adapter capture into a typed Brain observation bundle while preserving exact session, packet, and projection lineage.

The v0 boundary intentionally does not parse Kilo event payload semantics. Kilo JSON output is treated as an unstable raw event stream until an observed-version corpus supports a provider-specific parser. The normalized capture records event count and cryptographic digests instead.

## Trust And Privacy

Direct CLI ingestion is unverified by default. An unattested capture emits one `model_inferred`/`no_change` event, carries no verification or artifact evidence into Brain, and cannot request recovery. The adapter caller must explicitly use `--attest-runtime-capture` only after it produced the normalized lifecycle metadata and observed the referenced artifacts. The ingester then trusts only those normalized runtime fields and typed verifier fields. It never embeds:

- raw event payloads
- model output text
- tool arguments or responses
- reasoning or chain-of-thought
- model-authored completion claims

The emitted statement is selected from fixed framework text. Raw stream and model output identity survive only as SHA-256 digests.

## Semantic Rules

- The supplied projection must equal the deterministic projection recomputed from the validated session; schema-valid projection substitution is rejected.
- Capture lineage must match that runtime session and adapter projection exactly.
- Capture files cannot self-assert trust; adapter attestation is an out-of-band caller decision.
- `completed` requires timeout status `none` and exit code `0`.
- `failed` requires timeout status `none` and a nonzero exit code.
- `timeout`, `cancelled`, and `unknown` termination cannot claim verification.
- Acceptance `complete` requires verification `pass`.
- Model-output presence and stream availability must agree with their digests.
- A completed run without verification or observed artifacts is `no_change`, not progress.
- Timeout, cancellation, and unknown termination emit a recovery signal anchored to the existing checkpoint and prior packet.
- Policy-blocked execution emits an unsafe observation and never requests automatic recovery.

## Next Depth-First Path

```text
runtime-neutral session compilation [implemented]
-> Kilo operation-packet projection and validation [implemented]
-> execution observation ingestion [implemented]
-> recovery/resume integration [implemented]
-> Phase 5 end-to-end adapter evidence [next]
```
