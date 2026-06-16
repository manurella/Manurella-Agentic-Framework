# Architecture

## Core Decision

Manurella is a portable specification system with adapters, not a single agent runtime.

The canonical source should be runtime-neutral files in this repository. Runtime-specific formats, such as Kilo Code agent Markdown files or Codex skills, are generated outputs.

## Layers

### 1. Kernel

The kernel defines invariants shared by every runtime:

- task contract shape
- specialist/domain-pack shape
- permission model
- memory categories
- evaluation metadata
- adapter output requirements

The kernel must stay small. It should hold durable rules, not domain encyclopedias.

### 2. Router

The router decides the execution path:

- answer directly
- ask a clarifying question
- use one specialist
- run a maker-checker workflow
- request research
- refuse or escalate

V0 router behavior is rule-based. Contextual bandits are deferred until we have enough scored results.

### 3. Domain Packs

Domain packs contain specialist behavior and domain-specific rubrics.

Initial packs:

- `build`: software architecture, coding, QA, security, deployment, documentation
- `muse`: writing, story, scripts, creative critique
- `pixel`: art direction and image prompt engineering
- `mentor`: language learning first, general teaching later

Domain packs should be modular. Large examples and knowledge libraries belong in references/resources, not always-on prompt bodies.

### 4. Tool Layer

Tools are explicit capabilities with schemas, side-effect levels, and permission requirements.

V0 starts with no custom MCP server unless a task proves it is needed. The first likely tools are:

- prompt compiler
- Kilo exporter
- eval runner
- trace logger

MCP is the preferred long-term integration boundary, but MCP tools must be treated as hostile until permissioned and logged.

### 5. Memory Layer

V0 memory is file-based and explicit:

- project state
- user preferences
- domain references
- successful examples
- failures and lessons

No automatic immortal vector memory in v0. Memory must be curated before it affects future runs.

### 6. Evaluation Layer

The eval layer is the scoreboard:

- deterministic checks where possible
- rubric scoring where subjective quality matters
- trajectory notes for tool use and recovery
- baseline comparison
- cost/latency notes where measurable

The first eval target is Kilo because it gives practical access to free models.

### 7. Runtime Control Layer

The runtime control layer defines how much reasoning, delegation, tool use, and wall-clock time a run may spend.

It exists because Manurella's claim is not "think forever." The claim is better output per model, cost, and time budget.

V0 control dimensions:

- execution profile: quick, standard, or deep
- specialist-call budget
- repair-loop budget
- verifier requirement
- timeout and resume policy
- adapter-supported runtime knobs

### 8. Runtime Adapters

Adapters compile the portable specs into runtime-specific formats.

V0 priority:

1. Kilo Code agent Markdown files
2. Codex `AGENTS.md` and skills
3. ChatGPT/Gemini instruction packs
4. Python runtime / LangGraph later

Adapters should be one-way exports. Runtime quirks must not leak back into the kernel unless promoted through an ADR.

## First Architecture Trade-Offs

- Use documentation/specs first because the domain is still being discovered.
- Use Kilo first because it is the practical testbed.
- Defer custom Python runtime until the Kilo adapter and eval loop prove the abstractions.
- Defer real RL and fine-tuning until scored trajectories exist.
- Prefer small specialist prompts plus retrieved references over massive always-on prompts.
