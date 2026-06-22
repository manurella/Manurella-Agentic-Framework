# Kilo Adapter

The Kilo adapter compiles Manurella runtime-neutral agent definitions into Kilo Code Markdown agents.

Current Kilo target:

- project agents live under `.kilo/agents/`
- the filename becomes the agent id
- YAML frontmatter configures `description`, `mode`, `permission`, `steps`, `temperature`, and related settings
- the Markdown body becomes the agent system prompt

Sources checked:

- <https://kilo.ai/docs/customize/custom-modes>
- <https://kilo.ai/docs/customize/custom-subagents>

## Source Of Truth

The source of truth is the Manurella domain agent definition:

```text
domains/<domain>/agents/<agent-id>.md
```

Generated Kilo files are runtime artifacts. Do not edit generated `.kilo/agents/*.md` files directly unless deliberately testing a runtime patch.

## Export Command

Generate Build agents into the project-local Kilo target:

```powershell
python adapters/kilo/export_agents.py --domain build --output .kilo/agents
```

Generate Fast Mode for smoke tests:

```powershell
python adapters/kilo/export_agents.py --domain build --output .kilo/agents --mode fast --effort low
```

Generate all domains:

```powershell
python adapters/kilo/export_agents.py --all --output .kilo/agents --mode standard --effort high
```

Validate without writing:

```powershell
python adapters/kilo/export_agents.py --domain build --output .kilo/agents --mode fast --effort low --dry-run
```

## Export Rules

- `tier: top_level` maps to `mode: primary` unless `runtime.kilo.mode` overrides it.
- `tier: internal` maps to `mode: subagent` unless `runtime.kilo.mode` overrides it.
- Missing permissions fail closed.
- `shell` maps to Kilo `bash`.
- `web` maps to Kilo `webfetch` and `websearch`.
- `delegate` maps to Kilo `task`.
- Top-level agents with `delegate: allow` receive a scoped `task` permission that allows only internal agents from the same domain.
- Internal agents cannot delegate by default.
- Creative, visual, and mentor agents deny `bash` by default.
- Prompt bodies include references to source files instead of embedding large research inputs.
- Runtime controls follow `specs/runtime-control.md`.
- Prompt bodies include global control references to `specs/runtime-packet-protocol.md`, `specs/promotion-gates.md`, and `docs/kilo-test-runbook.md`.
- Prompt bodies include domain control references, such as Build's frontend quality gate and Mentor's learner-state/quality gates.
- `--mode fast` narrows `steps` and denies `task` delegation to prevent small smoke tests from fanning out.
- `--mode standard` preserves each source agent's configured `steps`.
- `--effort low|medium|high|extra-high|max|ultra` controls reasoning depth in the generated prompt.
- Kilo does not currently expose a first-class effort field, so effort is exported as prompt policy rather than YAML frontmatter.

## Generated Prompt Shape

The Kilo prompt body uses this order:

1. Purpose
2. Use boundaries
3. Inputs and outputs
4. Workflow
5. Context policy
6. Permission policy
7. Manurella control references
8. Runtime control mode and effort
9. Evaluation rubric
10. Failure modes
11. Source references

## First Runtime Sample

Build is the first sample export because it has the cleanest verifier loop:

```text
architect / build-orchestrator / explorer
localizer / editor / verifier / critic
```

## Runtime Session Projection

Validate strict session projection without invoking Kilo or spending model quota:

```powershell
python adapters/kilo/project_runtime_session.py --repo . --fixtures
```

Project a previously compiled runtime session:

```powershell
python adapters/kilo/project_runtime_session.py --repo . --session path/to/runtime-session.yaml
```

Add `--write-agent` only when the generated per-session agent should be materialized under `.kilo/agents/`. The command prints a projection record containing the agent digest and suggested interactive CLI argv. It never executes that argv, never adds `--auto`, and treats JSON output as unversioned raw events.

After an adapter-runner normalizes the process lifecycle and hashes the raw event stream, ingest its capture without embedding model output:

```powershell
python tools/ingest_runtime_observation.py --repo . --session path/to/session.yaml --projection path/to/projection.yaml --capture path/to/capture.yaml
```

This direct form is deliberately unattested and produces quarantined evidence. `--attest-runtime-capture` is reserved for the adapter process that observed the invocation metadata and artifacts itself; it must never be set from model-authored output.
