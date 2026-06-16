# Manurella Cognitive Graph Mind Map

```mermaid
mindmap
  root((Manurella))
    Domains
      Build
        Agents
          Build Orchestrator
          Architect
          Explorer
        Subagents
          Localizer
          Editor
          Verifier
          Critic
        Failure Modes
          Scope Expansion
          Timeout
          Weak Verification
    Runtime Control
      Modes
        Fast
        Standard
      Effort
        Low
        Medium
        High
        Extra High
        Max
        Ultra
    Evidence
      Research Inputs
      Synthesis
      Eval Results
    Evolution
      Add
      Strengthen
      Weaken
      Deprecate
      Merge
```

## Reading The Map

- Domains own agents and constraints.
- Agents delegate only through explicit graph edges.
- Modes change workflow shape.
- Effort changes reasoning depth.
- Evals strengthen or weaken graph edges.
- Failure modes must be linked to mitigations.

## V0 Focus

The first mature slice should be:

```text
Build -> frontend work -> specialist topology -> verification -> eval feedback
```

This slice is intentionally not complete yet. The graph should grow from evaluated behavior, not from speculative completeness.
