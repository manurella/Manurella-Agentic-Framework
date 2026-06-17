# Result Record Template

## Metadata

- `task_id`:
- `date`:
- `domain`:
- `benchmark_ref`:
- `runtime`:
- `model`:
- `mode`:
- `effort`:
- `adapter_version`:
- `prompt_version`:
- `agent_ids`:
- `reviewer`:

## Task

Prompt summary:

```text

```

Success criteria:

- 

Constraints:

- 

## Runtime Outcome

- `status`: pass | partial | fail | timeout
- `timeout_status`: none | upstream_idle_timeout | user_stopped | unknown
- `target_latency`:
- `actual_latency`:
- `specialist_call_count`:
- `repair_loop_count`:
- `verifier_count`:
- `changed_artifacts`:
- `output_path`:

## Verification

Verification performed:

- 

Evidence:

```text

```

Verification gaps:

- 

Frontend evidence when applicable:

- `wcag_target`: WCAG 2.2 AA | other | not_applicable
- `accessibility_tool`: axe | lighthouse | playwright_accessibility | manual | not_run
- `accessibility_result_path`:
- `lighthouse_result_path`:
- `core_web_vitals`: LCP / INP or TBT / CLS
- `playwright_result_path`:
- `screenshot_paths`:
- `visual_diff_result`:
- `viewport_coverage`:
- `keyboard_flow_checked`: yes | no | not_applicable
- `screen_reader_semantics_checked`: yes | no | not_applicable

## Scores

Use 1-5 where applicable.

- `correctness`:
- `instruction_adherence`:
- `specificity`:
- `structure`:
- `domain_quality`:
- `safety`:
- `efficiency`:
- `recovery`:

Frontend scores when applicable:

- `accessibility`:
- `visual_stability`:
- `responsive_fit`:
- `state_correctness`:
- `behavior_correctness`:
- `performance`:
- `implementation_minimality`:
- `verification_evidence`:

Mentor evidence when applicable:

- `target_skill`:
- `learner_evidence_used`:
- `diagnosis_confidence`: low | medium | high | not_applicable
- `teaching_strategy`:
- `active_recall_included`: yes | no
- `answer_key_or_rubric_included`: yes | no
- `learner_state_update_proposed`: yes | no
- `next_review_or_action`:

Mentor scores when applicable:

- `diagnostic_precision`:
- `pedagogical_fit`:
- `active_recall_quality`:
- `feedback_quality`:
- `review_schedule_quality`:
- `learner_state_honesty`:
- `interview_readiness_value`:

## Notes

Quality notes:

- 

Failure modes:

- 

Next tuning action:

- 
