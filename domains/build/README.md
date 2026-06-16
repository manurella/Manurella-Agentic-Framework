# Build Domain Pack

## Purpose

The build domain handles software project work: architecture, coding, QA, security, deployment, documentation, and technical planning.

## Use When

- The user wants to build, modify, debug, audit, test, deploy, or document software.
- The task has concrete files, commands, systems, or technical requirements.
- The output should be verifiable by tests, builds, linters, diffs, logs, or specs.

## Do Not Use When

- The task is primarily creative writing.
- The task is primarily art direction or image prompting.
- The task is a language-learning session.
- The user only wants casual explanation with no project consequence.

## Core Outputs

- implementation plan
- architecture note
- code patch
- test plan
- security review
- deployment/runbook note
- technical documentation

## Context Policy

Read project guidance first. Then inspect only the files needed for the task. Prefer targeted search over reading whole large files. Never claim completion without a verifier.

## Permission Baseline

- `read`: allow project files
- `edit`: ask/allow only inside scoped project files
- `shell`: ask for commands with side effects
- `web`: ask/allow for current docs and version checks
- `mcp`: allow only named tools

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
- What is the minimum Kilo prompt needed for reliable build-domain behavior?

