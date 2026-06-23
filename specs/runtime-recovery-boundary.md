# Runtime Recovery Boundary

## Record State

- Phase: 5
- Lifecycle: implemented v0 recovery compiler boundary
- Runtime posture: provider-neutral recovery, Kilo projection first
- Side effects: none

## Purpose

Runtime failure must shrink and resume work from durable artifacts, not restart the full workflow. `tools/compile_runtime_recovery.py` consumes a checkpoint Brain workspace, the prior runtime session, the prior adapter projection, and one typed `execution-observation-bundle.v0`. It advances Brain with the trusted blocked observation, compiles the resulting control decision into a `recovery` operation packet, wraps that packet in a new runtime session bundle, and projects it back through the Kilo adapter without executing Kilo.

The boundary is intentionally narrow. It handles runtime-blocked recovery signals such as upstream idle timeout, user stop, and unknown terminal status. Verification failure, acceptance completion, unsafe policy blocking, and unattested model claims use their existing Brain dispositions instead of this recovery path.

## Inputs

- A durable `workspace-bundle.v0` checkpoint matching the prior operation packet's `resume.checkpoint_ref`.
- The prior `runtime-session-bundle.v0`.
- The deterministic prior `kilo-session-projection.v0`.
- A typed `execution-observation-bundle.v0` emitted by the execution-observation boundary.

The workspace checkpoint is required because the runtime session carries references and the operation packet, not a hidden transcript or reconstructed workspace. Recovery must be explicit about which durable state is being resumed.

## Semantic Rules

- The prior projection must equal the deterministic projection recomputed from the prior runtime session.
- Observation lineage must match the prior session ID, prior packet ID, and prior projection ID exactly.
- Recovery metadata must point back to the prior packet and the same checkpoint ref.
- Recovery requires adapter-attested `trusted_runtime` capture trust.
- Recovery only accepts blocked observations from timeout, cancellation, or unknown runtime status.
- Non-recovery outcomes, unattested captures, policy-blocked unsafe observations, and verified completions are rejected by this compiler.
- The emitted recovery session carries the prior source and governed memory context, but updates Brain lineage to the new control decision.
- The emitted adapter projection is still non-executing and records `executed: false`.

## Output

The result is `runtime-recovery-result.v0`:

- prior session, packet, and projection lineage
- the observation bundle ID and recovery reason
- fixed privacy flags
- the Brain cycle result
- a recovery runtime session bundle
- a Kilo adapter projection for the recovery packet

Raw event payloads, model output text, tool arguments, tool responses, reasoning, and chain-of-thought remain excluded.

## Next Depth-First Path

```text
runtime-neutral session compilation [implemented]
-> Kilo operation-packet projection and validation [implemented]
-> execution observation ingestion [implemented]
-> recovery/resume integration [implemented]
-> Phase 5 end-to-end adapter evidence [next]
```
