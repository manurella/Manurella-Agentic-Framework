# Promotion Gates

## Purpose

Promotion gates define what evidence is required before a Manurella artifact moves from idea to active framework behavior.

This prevents the framework from becoming a pile of convincing prompts. State-of-the-art behavior is a measured property, not a label.

## Status Ladder

### Draft

Use for plausible ideas, early domain decomposition, or research translations.

Required:

- clear purpose
- owner domain or framework layer
- known uncertainty

Not allowed:

- claiming quality improvement
- default runtime activation
- promotion to adapter output as trusted behavior

### Research Candidate

Use for components backed by research, legacy evidence, or strong design reasoning but not yet repeatedly benchmarked.

Required:

- source references
- failure modes
- preliminary benchmark plan
- graph node
- permission boundary if agent-like

Not allowed:

- accepted-agent claims
- broad default delegation
- removing verifier gates

### Accepted

Use only when repeated evals show the artifact improves outcomes.

Required:

1. Schema-compliant artifact.
2. Cognitive graph node and relevant edges.
3. Evidence links that exist.
4. Quality gate or rubric.
5. At least two benchmark tasks.
6. Baseline-vs-guided result records.
7. Runtime adapter validation when runtime-facing.
8. Known failure modes.
9. Validator pass with no structural errors.
10. Human review of residual risk.

Accepted does not mean perfect. It means useful enough to become default behavior under named conditions.

### Deprecated

Use when a component is superseded, harmful, or no longer adapter-compatible.

Required:

- replacement or reason
- date
- graph update
- migration note if runtime-facing

## Agent Promotion Checklist

An agent can move to `accepted` only when:

- `domains/<domain>/agents/<id>.md` has schema-compliant YAML frontmatter.
- `purpose` is bounded and action-oriented.
- `use_when` and `do_not_use_when` are observable.
- `inputs` and `outputs` are typed.
- `permissions` are least privilege.
- context is tiered into always-on, references, and retrieved.
- Fast and Standard behavior is local or inherited from a named runtime policy.
- effort behavior is local or inherited from a named runtime policy.
- failure modes are concrete.
- at least two benchmark tasks exist.
- at least two result records compare baseline and guided behavior.
- Kilo adapter dry-run succeeds if the agent exports to Kilo.
- `tools/validate_framework.py` passes.

## Quality Gate Promotion Checklist

A quality gate can move to active only when:

- it names the domain or artifact class it controls.
- it lists required evidence.
- it defines invalid outputs.
- it is linked to at least one eval or failure mode.
- it is referenced by a prompt pack, agent, or domain README.

## Eval Promotion Checklist

An eval prompt pack can become a standard benchmark only when:

- baseline and guided prompts are separated.
- result-record creation is separated from task execution.
- unavailable tools are explicitly recorded as `not_run` or `not_available`.
- model/runtime/mode/effort/latency fields are required.
- failure records are allowed and useful.
- the prompt uses runtime packets when Kilo or another unstable runtime is used.

## Tool Promotion Checklist

A tool can become part of the normal workflow only when:

- it has a README entry or command example.
- it has a bounded input/output contract.
- it fails clearly on invalid data.
- it avoids network access unless explicitly required.
- it is run successfully on the repository.

## Current V0 Promotion Commands

Run these before claiming a framework checkpoint is healthy:

```powershell
python tools/validate_framework.py --repo .
python adapters/kilo/export_agents.py --all --output .kilo/agents --mode standard --effort high --dry-run
```

Optional result-record skeleton:

```powershell
python tools/create_result_record.py --repo . --task-id example-task --domain mentor --kind mentor --benchmark-ref domains/mentor/benchmarks/README.md#interview-study-benchmarks
```

Optional baseline-vs-guided comparison:

```powershell
python tools/compare_results.py --baseline evals/results/baseline-example.md --guided evals/results/guided-example.md --threshold 0.5
```

## Stop Rule

If an artifact cannot pass its promotion gate, do not rename it as accepted. Keep it draft or research_candidate, record the failure, and add the smallest next packet needed to gather evidence.
