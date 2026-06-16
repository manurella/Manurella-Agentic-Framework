# Pixel Benchmarks

## Purpose

These benchmark stubs define how Pixel agents graduate from research candidates to accepted agents. They are not full datasets yet.

## Pixel Director Benchmarks

1. Underspecified intent task: given "I need a banner image for my new coffee shop website", produce a complete non-contradictory brief or ask focused clarifying questions.
2. Multi-image project intake: convert a request for a recurring character series into a brief plus continuity requirements.

Metrics:

- brief completeness
- clarification turn count
- contradiction count
- user acceptance rate

## Syntax Specialist Benchmarks

1. Model-switching translation: compile the same brief for two target models with different prompt styles and parameters.
2. Token-limit challenge: preserve the essential brief under a strict token budget.

Metrics:

- prompt/API validity
- semantic fidelity
- token efficiency
- unsupported syntax count

## Continuity Anchor Benchmarks

1. Identity lock and pose stress: preserve a character across varied poses, lighting, and camera angles.
2. Brand style lock: preserve palette, typography notes, materials, and mood across multiple assets.

Metrics:

- identity lock score
- style lock score
- invariant/variant separation quality
- prompt bloat

## Audit Judge Benchmarks

1. Dependency-structured composition task: evaluate object counts, spatial relationships, text accuracy, and style constraints against a brief.
2. False-positive control task: approve acceptable artistic variation without inventing failures.

Metrics:

- error recall
- false-positive rate
- human-evaluator alignment
- uncertainty calibration

## Repair Technician Benchmarks

1. Iterative salvage task: repair a flawed generation while preserving successful composition/style elements.
2. Anti-regression task: fix one failed constraint without breaking three passed constraints.

Metrics:

- iterations to acceptance
- anti-regression success
- repair specificity
- correct local-edit versus regeneration decision

