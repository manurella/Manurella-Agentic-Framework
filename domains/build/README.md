# Build Domain Pack

## Purpose

The Build domain handles software project work: architecture, implementation, QA, security, deployment, documentation, debugging, and technical planning.

## Status

Research candidate. The current v0 topology is based on the Build domain research input and the cross-domain synthesis. It supersedes the first role-flavored skeletons.

## Use When

- The user wants to build, modify, debug, audit, test, deploy, or document software.
- The task has concrete files, commands, systems, or technical requirements.
- The output should be verifiable by tests, builds, linters, diffs, logs, or specs.

## Do Not Use When

- The task is primarily creative writing.
- The task is primarily art direction or image prompting.
- The task is a language-learning session.
- The user only wants casual explanation with no project consequence.

## V0 Topology

Top-level selectable agents:

- `architect`: planning, architecture, data/API design, and implementation task decomposition.
- `build-orchestrator`: implementation coordinator that preserves intent and delegates narrow work.
- `explorer`: read-only investigation, debugging, code review comprehension, and observability analysis.

Internal sub-agents:

- `localizer`: finds exact files, symbols, and line ranges.
- `editor`: produces precise patches from localized context.
- `verifier`: runs builds/tests/checks and returns compact evidence.
- `critic`: audits proposed changes for non-functional risks.

Specialized concerns such as frontend, backend, QA, security, DevOps, and documentation are v0 references, rubrics, or skills. They should become independent agents only after benchmarks show that the core topology is insufficient.

## Core Outputs

- implementation plan
- architecture note
- code patch
- test plan
- security or risk review
- deployment/runbook note
- technical documentation

## Context Policy

Read project guidance first. Then inspect only the files needed for the task. Prefer targeted search over reading whole large files. Never claim completion without verifier evidence.

## Permission Baseline

- `read`: allow project files
- `edit`: denied for top-level supervisors; ask/allow only for editor workers
- `shell`: denied for supervisors; ask for verifier or diagnostic commands
- `web`: ask/allow for current docs and version checks
- `delegate`: allow only for top-level supervisors

## Evaluation Rubric

- correctness
- architectural fit
- testability
- minimality of unrelated changes
- security posture
- clarity of handoff
- verification evidence

## Research Questions

- Which spec-driven workflow best improves small-model coding output?
- Which tasks benefit from separate planner/checker roles?
- What is the minimum Kilo prompt needed for reliable Build-domain behavior?
- Can Kilo technically prevent supervisors from editing directly, or must this be enforced by prompt and eval only?
- Which specialist concerns deserve skills first versus agents first?

