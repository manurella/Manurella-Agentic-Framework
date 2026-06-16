# ADR-0001 Runtime-Agnostic Kernel With Kilo-First Adapter

## Status

Accepted

## Context

`Family System v13` was effective because it provided structure, specialist roles, and operational rules around weaker models. It failed operationally because it was a monolithic Kilo custom-modes YAML file. Kilo changed its format, and the entire system became brittle.

The new framework must work first in Kilo Code because that is the immediate free-model testbed, but it should not be designed as a Kilo-only system.

## Decision

Manurella will define agents, domain packs, permissions, memory policy, and eval metadata in runtime-neutral repository specs. Runtime adapters will compile those specs into target formats.

The first adapter will target Kilo Code `.kilo/agents/*.md` files.

## Consequences

This adds some upfront structure, but it prevents another rewrite when a runtime changes. It also makes Kilo an output target rather than the source of truth.

The cost is that v0 must define a small schema before shipping usable agents. The benefit is that the same domain packs can later export to Codex, ChatGPT, Gemini, and custom Python tooling.

