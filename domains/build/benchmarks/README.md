# Build Benchmarks

## Purpose

These benchmark stubs define how Build agents graduate from research candidates to accepted agents. They are not full datasets yet.

## Architect Benchmarks

1. Ambiguous feature planning: given a vague feature request and repo summary, produce a scoped plan with assumptions, affected systems, and verifiers.
2. Architecture boundary task: given a proposed cross-cutting change, identify whether an ADR is needed and propose a reversible design.

Metrics:

- plan completeness
- feasibility
- unnecessary complexity score
- verifier specificity

## Orchestrator Benchmarks

1. Small bugfix trajectory: coordinate localization, patching, verification, and critique for a contained failing test.
2. Failed verifier recovery: respond to a failing test result by choosing a different repair path without looping.
3. Kilo runtime smoke test: perform a minimal documentation-only edit while reporting which agents were used, what each did, and what verification was performed.

Metrics:

- end-to-end success
- number of worker calls
- evidence quality
- error recovery rate

Observed v0 Kilo smoke result:

- Build agents loaded and produced a bounded documentation edit.
- Runtime behavior showed good signs for agent routing, scoped editing, verifier evidence, and critic-style reporting.
- Latency was high at roughly 30-40 minutes and the run hit `504 Upstream idle timeout exceeded`.
- The verifier confirmed only the targeted README lines and did not perform a broader baseline comparison.
- Future runtime policy should investigate explicit extended-reasoning controls comparable to strong coding-agent workflows, while keeping those controls measurable through latency and quality evals.

## Explorer Benchmarks

1. Root-cause analysis: diagnose a failure from source snippets and logs without editing.
2. Code review comprehension: explain behavioral risk in a diff with exact file/line evidence.

Metrics:

- citation accuracy
- causal correctness
- hypothesis/evidence separation

## Localizer Benchmarks

1. Single-file localization: find the source file and exact range for a failing unit test.
2. Multi-file localization: identify source, config, and test files needed for a repository-level behavior.

Metrics:

- top-1 recall
- top-5 recall
- range precision
- irrelevant context count

## Editor Benchmarks

1. Exact-context patch: produce a patch from localized snippets that applies cleanly.
2. Minimality challenge: fix behavior without changing unrelated formatting or public API.

Metrics:

- patch applicability
- syntax correctness
- minimality
- pass rate after verification

## Verifier Benchmarks

1. Command selection: choose the narrowest valid test/build command for a given change.
2. Log compression: summarize a noisy failing output without losing the root failure signal.

Metrics:

- false positive rate
- false negative rate
- signal-to-noise ratio
- command relevance

## Critic Benchmarks

1. Material-risk review: find security or data-loss risk in a passing patch.
2. False-positive control: approve a valid patch without inventing stylistic blockers.

Metrics:

- material finding recall
- false-positive rate
- severity calibration
- evidence quality
