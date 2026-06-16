# Cognitive Graph Specification

## Purpose

The Cognitive Graph is Manurella's evolving reasoning map.

It connects domains, agents, skills, tools, context, evals, failure modes, research evidence, modes, and effort levels so runtime decisions are explicit instead of hidden inside one large prompt.

The graph is a control artifact. It is not a claim of consciousness or sentience.

## Source Of Truth

V0 uses git-versioned files:

```text
cognition/
  README.md
  graph.yaml
  mindmap.md
```

Large research evidence stays in `research/inputs/`. Stable conclusions are promoted into `research/synthesis/`, `specs/`, `docs/`, and `cognition/`.

## Node Types

| Type | Prefix | Purpose |
| --- | --- | --- |
| `domain` | `dom.` | Owns a domain pack and permission boundary. |
| `agent` | `agt.` | Top-level selectable specialist or orchestrator. |
| `subagent` | `sub.` | Internal bounded specialist. |
| `skill` | `skl.` | Reusable procedural capability or instruction module. |
| `tool` | `tool.` | Local command, script, MCP capability, or runtime tool. |
| `context` | `ctx.` | Reference, memory, source file, research input, or retrieved artifact. |
| `eval` | `eval.` | Benchmark, smoke test, or scored run record. |
| `failure_mode` | `fail.` | Known failure pattern to avoid or mitigate. |
| `mode` | `mode.` | Runtime workflow shape such as Fast or Standard. |
| `effort` | `effort.` | Reasoning depth level from Low through Ultra. |
| `routing_rule` | `route.` | Conditional routing decision. |
| `research_evidence` | `evidence.` | Research source or synthesized claim. |

## Edge Types

| Type | Source | Target | Meaning |
| --- | --- | --- | --- |
| `owns` | domain | agent/subagent/context | Domain ownership. |
| `orchestrates` | agent | subagent | Delegation relationship. |
| `uses_skill` | agent/subagent | skill | Procedural capability used by node. |
| `uses_tool` | agent/subagent/skill | tool | Tool dependency. |
| `uses_context` | node | context | Context source may be loaded. |
| `enforces` | mode/domain | node | Policy or permission constraint. |
| `sets_effort` | routing_rule/mode | effort | Effort selection rule. |
| `mitigates` | node | failure_mode | Node reduces known failure risk. |
| `can_fail_with` | node | failure_mode | Known risk. |
| `evaluated_by` | node | eval | Eval covers the node. |
| `supported_by` | node/edge | research_evidence | Evidence support. |
| `routes_to` | routing_rule | node | Runtime route target. |
| `supersedes` | node/edge | node/edge | Replacement relationship. |

## Required Node Fields

```yaml
id: string
type: domain | agent | subagent | skill | tool | context | eval | failure_mode | mode | effort | routing_rule | research_evidence
label: string
status: draft | active | accepted | deprecated
summary: string
owners:
  - string
evidence:
  - string
updated_at: YYYY-MM-DD
```

## Required Edge Fields

```yaml
id: string
type: owns | orchestrates | uses_skill | uses_tool | uses_context | enforces | sets_effort | mitigates | can_fail_with | evaluated_by | supported_by | routes_to | supersedes
source: node_id
target: node_id
status: draft | active | deprecated
confidence: number # 0.0 to 1.0
weight: number # relative routing strength, 0.0 to 1.0
evidence:
  - string
updated_at: YYYY-MM-DD
```

## Mutation Rules

### Add

Create a new node or edge when a new domain concept, agent, skill, tool, eval, or failure mode is needed.

Requirements:

- include evidence or mark as `draft`
- define owner
- define expected eval path before `accepted`

### Strengthen

Increase confidence or weight after successful repeated use.

Allowed evidence:

- passing deterministic verifier
- improved benchmark score
- reduced latency/cost with equal quality
- human-reviewed successful run

### Weaken

Decrease confidence or weight after degraded behavior.

Triggers:

- timeout
- verifier failure
- user correction
- wrong routing
- context overload
- unsafe permission request

### Deprecate

Mark node or edge as inactive for new routing while preserving history.

Use when:

- concept is superseded
- agent is merged
- tool is unsafe or unavailable
- eval shows repeated underperformance

### Merge

Combine redundant nodes when they have the same purpose and compatible contracts.

Requirements:

- preserve source ids in history
- update incoming/outgoing edges
- record reason in evidence

### Remove From Active Use

Do not hard delete in v0. Remove only from active routing.

## Mode And Effort Semantics

Modes are graph nodes:

- `mode.fast`
- `mode.standard`

Efforts are graph nodes:

- `effort.low`
- `effort.medium`
- `effort.high`
- `effort.extra-high`
- `effort.max`
- `effort.ultra`

Mode selects workflow shape. Effort selects reasoning depth. They must be recorded separately in evals.

## Confidence Policy

Confidence is evidence quality, not personal certainty.

V0 scale:

- `0.0-0.2`: speculative
- `0.3-0.5`: plausible but weakly tested
- `0.6-0.7`: supported by local evidence
- `0.8-0.9`: repeatedly supported across runs
- `1.0`: reserved for invariants or deterministic facts

Do not use `1.0` for prompts, agents, or routing rules.

## Runtime Read Policy

At runtime, an adapter or future controller should read only the graph slice required for the task:

1. task domain
2. selected mode
3. selected effort
4. candidate agents/subagents
5. relevant context nodes
6. known failure modes
7. required eval/verifier nodes

The graph must reduce context load, not become another giant always-on prompt.

## V0 Validation Rules

- all node ids are unique
- all edge ids are unique
- every edge source and target exists
- every active node has evidence or is explicitly marked draft
- every active agent has at least one eval or benchmark reference
- every active tool edge has a permission note
- every mode/effort change is reflected in eval records

## Non-Goals

- no automatic self-modification in v0
- no graph database requirement in v0
- no GNN routing in v0
- no claim that the graph is sentient
- no hidden memory mutation without review

## Research Hooks

- should graph confidence use simple scores first or Bayesian updates?
- how should repeated failures decay edge weights?
- which visual format best supports review: Mermaid, FigJam, Obsidian Canvas, or generated SVG?
- when should a graph mutation require an ADR?
- how should graph slices be compiled into Kilo, Codex, ChatGPT, and Gemini adapters?
