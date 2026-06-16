# Manurella v0 Charter

## Purpose

Manurella exists to prove that agent architecture can close part of the model-quality gap. The target is not to make small models magically become frontier models. The target is to make weaker, cheaper, or free models produce measurably better results by giving them better structure:

- clearer tasks
- smaller specialist contexts
- explicit acceptance criteria
- controlled tools
- reusable domain knowledge
- evaluation feedback
- runtime-specific adapters

## Origin

The previous `Family System v13` proved that role specialization and a stronger orchestration backbone can improve output quality in Kilo Code, even with non-frontier models. It also exposed the failure mode: one giant YAML became hard to validate, hard to migrate, too broad in permissions, and too easy to break when Kilo changed its agent format.

Manurella v0 rebuilds the idea as a portable framework instead of a monolithic prompt.

## Non-Goals

- Do not create another all-in-one prompt file.
- Do not optimize for one runtime at the expense of portability.
- Do not implement real fine-tuning, DPO, or RL before there is an evaluation dataset.
- Do not add broad tool permissions by default.
- Do not treat LLM-as-judge scores as truth without deterministic checks or human review.

## V0 Success Criteria

V0 is successful when the repo contains:

1. A portable kernel/domain-pack specification.
2. A Kilo Code adapter that can emit valid `.kilo/agents/*.md` files.
3. Initial domain packs for `build`, `muse`, `pixel`, and `mentor`.
4. A small benchmark suite with at least two tasks per domain.
5. Rubrics that compare baseline model output against Manurella-guided output.
6. A local results log that records model, prompt version, adapter version, score, and failure notes.

## Operating Principle

Every improvement must eventually be testable. If we cannot say what output got better, under what task, against what baseline, and at what cost, then it is not yet an engineering claim.

## Reinforcement Strategy

V0 uses reinforcement-inspired evaluation, not full reinforcement learning:

- collect outputs
- score them
- inspect failures
- improve prompts/specs/tools
- rerun the same tests

Contextual bandit routing, DPO, and trajectory learning are later-stage options after enough scored data exists.

