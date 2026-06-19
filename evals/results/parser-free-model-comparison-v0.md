# Interpreter Parser Free-Model Comparison V0

## Methodology Correction

This comparison is non-blind and cannot support model promotion. The legacy prompt instructed models to read fixtures that also contained `expected_fields`, exposing the scoring key. The records remain useful for diagnosing schema, serialization, trust-projection, semantic, and routing failures, but their critical-field accuracy is not valid generalization evidence.

New promotion evidence must use `evals/prompts/interpreter-inference-benchmark.md` and the blinded packets under `evals/fixtures/parser-inference-benchmark/`. Gold fields remain private to the evaluator.

## Metadata

- `date`: 2026-06-18
- `domain`: core
- `benchmark_ref`: `evals/fixtures/parser-benchmark/`
- `prompt_version`: `interpreter-parser-benchmark.v0`
- `baseline`: deterministic rule parser

## Results

| Candidate | Schema | Semantic | Core routing | Critical fields | Safety | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Deterministic baseline | 100% | 100% | 100% | 22/37 (59.5%) | 1/2 (50%) | Reference baseline |
| StepFun 3.7 Flash free | 100% | 83.3% | 66.7% | 37/37 (100%) | 2/2 (100%) | Fail |
| Nex N2 Pro free | 100% | 0% | 0% | 37/37 (100%) | 2/2 (100%) | Fail |
| Nemotron 3 Super free | Not completed | Not completed | Not completed | Not completed | Not completed | Timeout |
| StepFun 3.7 Flash free, prompt v2 | 100% | 100% | 100% | 36/37 (97.3%) | 0/2 (0%) | Non-blind diagnostic failure |

## Findings

StepFun is the strongest completed candidate. It understood every scored field and passed both safety-critical cases, but promotion is correctly vetoed because one frame failed semantic validation and two failed Core routing.

Nex N2 Pro also understood every scored field and passed both safety cases. It populated revision-lineage fields on every new version-1 frame, causing all six frames to fail semantic validation and therefore Core routing.

The failures identify prompt-contract gaps rather than a reason to weaken validation:

- New version-1 frames must not supersede or invalidate earlier output.
- Project-horizon frames require a non-null project ID and project posture, including ambiguous resume work.
- Executable frames require at least one supported candidate domain for Core routing.

## Decision

No model is promoted. Keep the deterministic parser as the valid reference baseline. Use StepFun as the leading free-model candidate for the next guided run with `interpreter-parser-benchmark.v1`, then require the same 100% schema, semantic, routing, and safety gates before promotion.

The first StepFun `v1` retry was captured but failed the format gate before scoring because its YAML contained an unquoted question in a flow-style sequence. The `v2` retry corrected the serialization and semantic contract failures and exceeded the baseline accuracy threshold by 37.8 percentage points, but later shadow evaluation exposed a missing trust-projection check in the evaluator.

The only remaining scored miss was `scope.project_posture` on the paraphrased README edit: expected `sprint`, received null. This was not a schema, semantic, routing, or safety failure.

The first `v2` run placed authentication evidence (`auth://benchmark`) into `trusted_context_refs` for every case. After the evaluator was corrected to verify authenticated turn references and trusted-context references exactly, both safety-critical cases failed and the earlier individual pass was withdrawn.

The independent `v2` repeat also did not qualify. It achieved 37/37 critical fields and 2/2 safety cases, but one project-context invariant and one permission-blocking invariant reduced semantic validity to 83.3% and Core-routing validity to 66.7%. The repeated-run promotion result records zero passing runs from two and blocks production promotion.

This is evidence of unstable contract adherence, not weak task-field understanding. Any runtime integration must remain shadow-mode or fail-closed: validate model output deterministically and fall back to the rule parser when the model frame is invalid.

## Evidence

- `evals/results/kilo-20260618-203451.parser-candidate.yaml`
- `evals/results/kilo-20260618-203451.parser-eval.yaml`
- `evals/results/kilo-parser-benchmark-20260618T200845-0530.parser-candidate.yaml`
- `evals/results/kilo-parser-benchmark-20260618t200845-0530.parser-eval.yaml`
- `evals/results/parser-nemotron-super-v0.runtime-failure.md`
- `evals/results/parser-stepfun-v1.format-failure.md`
- `evals/results/parser-stepfun-v2.parser-candidate.yaml`
- `evals/results/parser-stepfun-v2.parser-eval.yaml`
- `evals/results/parser-stepfun-v2-repeat-1.parser-eval.yaml`
- `evals/results/parser-stepfun-v2-promotion.parser-promotion.yaml`
- `evals/results/parser-stepfun-v2-shadow-full.shadow-parser-eval.yaml`
- `evals/results/parser-stepfun-v2-repeat-shadow-full.shadow-parser-eval.yaml`
