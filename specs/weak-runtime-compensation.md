# Weak Runtime Compensation Protocol

## Purpose

This protocol defines how Manurella should behave when the active model or runtime has weak domain knowledge, shallow reasoning, unstable streaming, or poor instruction adherence.

It does not pretend a weak model is a frontier model. It forces a weaker model to work through smaller, verifiable moves so the framework can recover quality through structure, evidence, and iteration.

## When To Use

Apply this protocol when any of these are true:

- the model misses obvious evidence
- the model gives generic advice instead of task-specific output
- the model invents knowledge, tool results, or learner state
- reasoning appears shallow or circular
- stream, connection, or upstream idle timeouts occur
- the run uses Kilo/free models or an unknown model

## Operating Rules

### 1. Declare Knowledge Boundary

Before giving a confident answer, state what knowledge is available and what is missing.

Required distinction:

- known from provided context
- inferred from weak evidence
- unknown or needs retrieval

If a domain fact matters and is not in provided context, use the allowed retrieval path or mark it as an assumption. Do not fill gaps with confident-sounding guesses.

### 2. Use Local Framework Context First

For Manurella tasks, local framework files outrank generic model memory.

The model must consult or apply the relevant local control files before final output:

- runtime packet protocol for scope and stop rules
- domain quality gate for output acceptance
- learner-state, frontend, muse, or pixel domain files when applicable
- eval result records when repairing known failure modes

### 3. Compress Reasoning Into Checkpoints

Do not run long silent reasoning. Use compact checkpoints:

1. evidence read
2. assumptions
3. decision
4. output
5. self-check

Each checkpoint should be short enough to survive unstable streams. If the runtime may timeout, output the current checkpoint and stop rather than continuing silently.

### 4. Prefer Narrow Skill Targets

Weak models fail when asked to solve broad domains at once.

Convert broad tasks into narrow targets:

- "frontend interview prep" becomes one topic, one misconception, one drill
- "visual QA" becomes screenshot evidence, accessibility evidence, responsive evidence, state evidence
- "write a story" becomes premise, scene purpose, conflict, continuity anchor, draft

### 5. Force Self-Check Against A Gate

Every serious output must include a final self-check against the relevant gate:

- what passed
- what is partial
- what is missing
- what should be the next packet

The self-check is not a second essay. It is a compact checklist.

### 6. Treat Timeout As A Design Signal

Timeout is not proof that more time was needed.

Classify timeout as one of:

- packet too large
- hidden delegation or runaway loop
- stream/provider idle failure
- missing checkpoint output
- model stuck in low-value reasoning

The next run must reduce packet size or add a checkpoint before increasing effort.

## Weak-Model Output Skeleton

Use this skeleton when a model has shown weak reasoning or generic output:

```text
1. Evidence I used
2. Missing evidence or assumptions
3. Narrow target for this packet
4. Output
5. Self-check against gate
6. Stop or next packet
```

## Promotion Rule

If a guided run still performs like a generic baseline, do not promote the agent or prompt. Record the failure, add a narrower benchmark, and decide whether the domain needs:

- stronger local knowledge
- more examples
- a deterministic helper tool
- retrieval or web access
- a smaller packet boundary
- a different specialist decomposition
