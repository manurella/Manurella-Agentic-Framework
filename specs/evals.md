# Evaluation Specification

## Why Evals Come First

Manurella's core claim is that better agent architecture improves output quality from weaker or cheaper models. That claim needs repeated tasks, baselines, and scoring. Without evals, we are only tuning by taste.

## V0 Evaluation Method

For each benchmark task:

1. Run the baseline model without Manurella guidance.
2. Run the same model through the relevant Manurella adapter/domain pack.
3. Save both outputs.
4. Score both outputs using the same rubric.
5. Record model, runtime, execution profile, prompt/domain version, score, latency, timeout status, notes, and failure type.

## Score Dimensions

Use a 1-5 scale unless a deterministic pass/fail check exists.

- `correctness`: factual or functional correctness
- `instruction_adherence`: follows task constraints and output format
- `specificity`: avoids vague generic output
- `structure`: uses an appropriate, usable organization
- `domain_quality`: reflects domain expertise
- `safety`: avoids unsafe or over-permissioned behavior
- `efficiency`: avoids unnecessary tool use, verbosity, or cost
- `recovery`: responds well to errors or conflicting evidence

## Initial Benchmark Categories

### Build

- small bugfix planning task
- architecture review task
- security review task
- test strategy task

### Muse

- story premise development
- scene critique
- screenplay beat restructuring
- long-context continuity check

### Pixel

- image prompt from a loose visual idea
- character consistency prompt
- style transfer/art-direction prompt
- prompt repair after bad generation

### Mentor

- beginner language placement
- grammar correction with explanation
- learning plan for a concrete goal
- correction without discouraging the learner

### General

- ambiguous user request
- direct answer vs delegation decision
- prompt-injection/adversarial instruction
- research synthesis with citations

## V0 Pass Condition

Manurella-guided output should beat baseline output by at least 0.5 average rubric points on the first curated benchmark set without increasing latency/cost beyond an agreed threshold.

This threshold is provisional. It should be revisited after the first real Kilo runs.

Runtime-control fields are defined in `specs/runtime-control.md`.
