# Interpreter And Task Model Research Synthesis

## Purpose

This synthesis reconciles two 2026 Interpreter research reports with Manurella's audited Family System behavior and accepted Brain boundary.

Research inputs:

- `research/inputs/manurella-interpreter-deep-research-2026.md`
- `research/inputs/manurella-interpreter-task-model-research-2026.md`
- `specs/core-operating-protocol.md`
- `docs/family-system-mechanism-map.md`
- `specs/brain-cognitive-kernel.md`

## Research Failure And Correction

The research prompt asked for a critique of the Family A-E classifier without expanding the project-specific labels. One report consequently interpreted A-E as an Autoencoder architecture and built a false critique and replacement taxonomy around that assumption.

That failure originated in the prompt context. Future research prompts must define every project-specific term, distinguish accepted facts from open questions, name canonical attachments, and instruct the researcher to report inaccessible context instead of inventing a substitute meaning.

The affected report remains preserved as negative evidence. Its useful source references and independent observations may still be considered, but conclusions derived from the Autoencoder interpretation are rejected.

## Canonical Family Meanings

```text
Class A: Quick Task
Class B: Feature Or Multi-Step Task
Class C: Full Project Or Large Build
Class D: Conversation Or Brainstorm
Class E: Ambiguous Request
```

These labels remain useful compatibility projections. They are not the Brain's primary task representation.

The existing project states are also preserved as project postures:

```text
genesis | sprint | audit | salvage | reimagine | resume
```

They determine how Manurella approaches existing work. They do not replace task lifecycle, artifact state, or a project dependency graph.

## Promoted Conclusions

1. The Interpreter is a trust-aware compiler from human interaction into structured work objects.
2. Task classification is multidimensional rather than one mutually exclusive enum.
3. The raw request and source references are immutable provenance.
4. Inferred values, user-confirmed values, runtime-derived values, and policy-derived values remain distinguishable.
5. Task Frames evolve through nondestructive versioning.
6. Acceptance Contracts are first-class versioned objects.
7. Clarification is impact- and risk-driven rather than certainty-maximizing.
8. Cross-domain work uses a root frame with linked child work items.
9. The Interpreter emits routing hints; the Router owns routing and handoff packets.
10. Structured decoding can guarantee syntax where supported, but not semantic correctness or safety.

## Rejected Conclusions

- A-E means Autoencoder.
- A-E should be replaced with Atomic, Bounded, Conversational, Dynamic, and Episodic.
- Every task should use BDI, HTN, and Behavior Trees.
- Plans, tool arguments, and runtime responses belong inside the Task Frame.
- Scalar entropy or model confidence is sufficient for clarification decisions.
- A supervisor model creates a security boundary.
- Removing markup or URLs makes untrusted content safe.
- Fast Mode must switch to Standard when ambiguity appears.
- Modes determine model size, temperature, or final quality.
- Constrained decoding guarantees correct meaning.

## V0 Direction

V0 uses:

- a compact versioned Task Frame
- a separate Acceptance Contract
- typed ambiguities and assumptions
- explicit risk, reversibility, permissions, and confirmation requirements
- deterministic clarification rules
- actual Family A-E compatibility projection
- project posture compatibility
- schema validation plus semantic checks
- benchmark fixtures covering conversation, direct work, projects, ambiguity, correction, cross-domain work, and consequential action

## Experiment-Required Decisions

- ambiguity and clarification calibration
- confidence composition
- domain-specific acceptance rubric generation
- subjective evaluator reliability
- automatic child-frame decomposition
- adaptive clarification burden
- learned routing hints

## Next Vertical Slice

After specification, implement and validate:

```text
Task Frame schema -> Acceptance Contract schema -> validator -> compatibility projection -> fixture suite
```
