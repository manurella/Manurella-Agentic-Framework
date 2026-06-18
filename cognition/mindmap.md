# Manurella Cognitive Graph Mind Map

```mermaid
mindmap
  root((Manurella))
    Brain
      Interpreter
        Task Frame Schema
        Acceptance Contract Schema
        Semantic Validator
        Family A-E Projection
        Project Posture Projection
        Contract Fixture Suite
      Core Router
        Routing Decision Schema
        Directness And Blocking Policy
        Primary And Secondary Domains
        Bounded Handoff Compiler
        Transcript Minimization
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
          Frontend Experimental
            Frontend Architect
            Component Implementer
            State Flow Specialist
            Accessibility Auditor
            Visual QA Specialist
            Performance Reviewer
        Failure Modes
          Scope Expansion
          Timeout
          Weak Verification
          Inaccessible UI
          Visual Drift
          State Flow Regression
          Frontend Performance Regression
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

## Current Depth-First Slice

The connected Interpreter-to-Core checkpoint is active:

```text
Interpreter
-> Trusted Input Envelope
-> Trust Partitioner
-> Task Frame Parser Baseline
-> Task Frame schema
-> Acceptance Contract Compiler
-> Acceptance Contract schema
-> Parser Benchmark Corpus
-> Model Candidate Evaluator
-> semantic validator
-> Family and project-posture projection
-> representative positive and negative fixtures
-> Core routing decision
-> bounded handoff projection
```

The deterministic input-to-Core path and runtime-neutral parser evaluation harness are implemented. A real external model candidate run and runtime execution remain later connected checkpoints.

## Experimental Frontend Slice

The frontend nodes are draft graph candidates only. They are not accepted agents, not exported runtime agents, and not official routing targets until benchmark evidence supports promotion.
