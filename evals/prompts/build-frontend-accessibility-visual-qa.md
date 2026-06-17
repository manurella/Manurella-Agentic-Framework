# Build Frontend Accessibility And Visual QA Prompt Pack

## Purpose

This prompt pack runs the first Build/frontend eval: Task 3 from `domains/build/benchmarks/frontend-eval.md`.

It compares a baseline frontend review against a Manurella Build-guided Standard/High review. The task is read-only. Do not use this prompt to edit, fix, refactor, or generate code.

## Fill These Fields First

```text
TARGET_REPO:
REVIEW_SCOPE:
CHANGE_REF:
ROUTE_URL:
DEV_SERVER_COMMAND:
ACCESSIBILITY_COMMAND:
LIGHTHOUSE_COMMAND:
PLAYWRIGHT_COMMAND:
SCREENSHOT_COMMAND:
TIMEBOX:
MODEL:
RUNTIME:
```

Field guidance:

- `TARGET_REPO`: repository or project under review.
- `REVIEW_SCOPE`: exact files, diff, route, component, PR, or uncommitted change to inspect.
- `CHANGE_REF`: commit, branch, PR, diff, or `working tree`.
- `ROUTE_URL`: local or deployed page URL if the UI is runnable.
- `DEV_SERVER_COMMAND`: command to start the app, or `not_available`.
- `ACCESSIBILITY_COMMAND`: axe, Playwright accessibility, Lighthouse accessibility, or `not_available`.
- `LIGHTHOUSE_COMMAND`: Lighthouse command if available, or `not_available`.
- `PLAYWRIGHT_COMMAND`: behavior or visual test command if available, or `not_available`.
- `SCREENSHOT_COMMAND`: screenshot capture command if available, or `not_available`.
- `TIMEBOX`: suggested `10 minutes` for baseline and `15 minutes` for Build-guided.
- `MODEL`: exact model used in Kilo.
- `RUNTIME`: Kilo Code version or `unknown`.

## Run Protocol

1. Run the baseline prompt first.
2. Reset or discard any runtime side effects before the guided run.
3. Run the Build-guided Standard/High prompt on the same target, same model, same scope, and same available commands.
4. Do not compare the two outputs until both are complete.
5. Record both runs using `evals/templates/result-record.md`.
6. Mark unavailable checks as `not_available` or `not_run`; do not invent evidence.
7. Keep target fixtures and eval results separate. Do not write result records inside `evals/fixtures/**`.
8. Use `specs/runtime-packet-protocol.md` when running in Kilo or another unstable runtime.
9. Apply `domains/build/frontend-quality-gate.md` before judging the guided output.
10. If screenshots exist, inspect them before finalizing. Screenshot paths without inspected observations do not count as evidence.

## Baseline Prompt

```text
You are reviewing a frontend change.

MANURELLA RUNTIME PACKET
- `packet_class`: verification
- `mode`: fast
- `effort`: medium
- `timebox`: TIMEBOX

Task:
Review REVIEW_SCOPE in TARGET_REPO for accessibility, visual stability, responsive behavior, and user-flow risk.

Context:
- Change reference: CHANGE_REF
- Route/page if runnable: ROUTE_URL
- Available commands:
  - Dev server: DEV_SERVER_COMMAND
  - Accessibility: ACCESSIBILITY_COMMAND
  - Lighthouse: LIGHTHOUSE_COMMAND
  - Playwright: PLAYWRIGHT_COMMAND
  - Screenshot: SCREENSHOT_COMMAND

Rules:
- Read-only review only.
- Do not edit files.
- Do not create patches.
- Do not create result files inside the target fixture or application folder.
- Do not create `eval.md` inside `evals/fixtures/**`.
- Do not refactor.
- Do not invent command results.
- If a command is unavailable or cannot run, state that as a verification gap.
- Return material findings only. Avoid stylistic preferences unless they create real user risk.
- If screenshots are provided or discoverable in the repo, inspect them and mention any visible broken media, overlap, clipping, unreadable text, or responsive failure.
- Stop after producing the review. Do not continue into repairs or result-record creation unless explicitly asked in a separate packet.

What to check:
- WCAG 2.2 AA-oriented accessibility risks: keyboard flow, focus order, labels, name/role/value, semantic landmarks, contrast, alternative text, and visible focus.
- Visual stability: overlap, clipping, layout shift, text overflow, unreadable text, broken spacing, and responsive fit at mobile and desktop sizes.
- User-flow risk: blocked interactions, confusing states, missing empty/error/loading states, and broken navigation.
- Performance smoke risk: obvious LCP, INP/TBT, CLS, payload, main-thread, or unnecessary client-work risk if visible from the change.

Industry checks:
- Run available accessibility, Lighthouse, Playwright, or screenshot commands if they are safe and already configured.
- If no runnable UI exists, perform static review and record the limitation.

Output format:
1. Verdict: pass | pass_with_notes | fail | blocked
2. Findings:
   - Severity: blocker | high | medium | low
   - Evidence: file/selector/route/command/screenshot note
   - Why it matters:
   - Suggested fix:
3. Checks attempted:
4. Verification gaps:
5. Scores from 1-5:
   - accessibility:
   - visual_stability:
   - responsive_fit:
   - behavior_correctness:
   - performance:
   - verification_evidence:
   - instruction_adherence:
   - trajectory_efficiency:
6. Result-record fields:
   - status:
   - timeout_status:
   - actual_latency:
   - changed_artifacts:
   - accessibility_tool:
   - accessibility_result_path:
   - lighthouse_result_path:
   - core_web_vitals:
   - playwright_result_path:
   - screenshot_paths:
   - viewport_coverage:
   - keyboard_flow_checked:
   - screen_reader_semantics_checked:
```

## Build-Guided Standard/High Prompt

```text
Use the Manurella Build system in Standard Mode with High effort.

MANURELLA RUNTIME PACKET
- `packet_class`: verification
- `mode`: standard
- `effort`: high
- `timebox`: TIMEBOX

Benchmark:
- domains/build/benchmarks/frontend-eval.md
- Task 3: Accessibility And Visual QA Review

Runtime policy:
- Read-only review.
- Do not edit files.
- Do not create patches.
- Do not refactor.
- Do not create result files inside the target fixture or application folder.
- Do not create `eval.md` inside `evals/fixtures/**`.
- Use the Build runtime policy for Standard Mode and High effort.
- Apply `domains/build/frontend-quality-gate.md`.
- Use `specs/runtime-packet-protocol.md`; stop at the verification packet boundary.
- Treat the experimental frontend graph nodes as draft research aids only, not official agents.
- Use frontend-architect, accessibility-auditor, visual-qa-specialist, state-flow-specialist, and performance-reviewer concepts only as review lenses.
- If delegation is available, use at most 2 specialist calls. If delegation is not available, perform the lenses sequentially yourself.
- Stop with evidence, not speculation.
- If screenshots are provided or discoverable in the repo, inspect them before finalizing. Call out visible broken media, overlap, clipping, unreadable text, or responsive failure.

Task:
Review REVIEW_SCOPE in TARGET_REPO for accessibility, visual stability, responsive behavior, and user-flow risk.

Context:
- Change reference: CHANGE_REF
- Route/page if runnable: ROUTE_URL
- Available commands:
  - Dev server: DEV_SERVER_COMMAND
  - Accessibility: ACCESSIBILITY_COMMAND
  - Lighthouse: LIGHTHOUSE_COMMAND
  - Playwright: PLAYWRIGHT_COMMAND
  - Screenshot: SCREENSHOT_COMMAND

Review lenses:
1. Frontend structure:
   - Does the change preserve existing component, route, styling, and state conventions?
   - Does it introduce scope expansion?
2. Accessibility:
   - Check WCAG 2.2 AA-oriented risks: keyboard access, focus order, labels, name/role/value, landmarks, contrast, alternative text, visible focus, and reduced-motion risk.
   - Use axe, Lighthouse, or Playwright accessibility if available.
3. Visual and responsive QA:
   - Check mobile and desktop fit, text overflow, overlap, clipping, layout shift, dark/light assumptions, spacing, and hierarchy.
   - Use screenshots or visual comparison if available.
4. State and user flow:
   - Check loading, empty, error, disabled, pending, and success states.
   - Check client/server/URL/form/async state risks if relevant.
5. Performance smoke:
   - Check obvious LCP, INP/TBT, CLS, bundle, render, data-loading, and unnecessary client-work risks.
   - Use Lighthouse if available; record lab limitations.

Industry gates:
- Accessibility automation: no critical or serious axe/Lighthouse/Playwright violations introduced.
- Accessibility manual: no blocker in keyboard, focus, labels, semantics, or contrast.
- Visual: no incoherent overlap, clipping, unreadable text, or unintended layout shift at mobile and desktop sizes.
- Behavior: critical user path works or the absence of runnable behavior is recorded.
- Performance: no obvious LCP, INP/TBT, CLS, payload, or main-thread regression.
- Record `not_run` or `not_available` explicitly instead of making a pass/fail claim when evidence is missing.
- A screenshot showing a broken image, clipped drawer, hidden overflow, overlap, or unreadable text is material evidence and must affect the verdict.

Output format:
1. Verdict: pass | pass_with_notes | fail | blocked
2. Material findings only:
   - Severity: blocker | high | medium | low
   - Lens: structure | accessibility | visual | state | performance
   - Evidence: file/selector/route/command/screenshot note
   - Why it matters:
   - Suggested fix:
3. Checks attempted:
4. Verification gaps:
5. Scores from 1-5:
   - accessibility:
   - visual_stability:
   - responsive_fit:
   - state_correctness:
   - behavior_correctness:
   - performance:
   - implementation_minimality:
   - verification_evidence:
   - instruction_adherence:
   - trajectory_efficiency:
6. Result-record fields:
   - task_id: build-frontend-a11y-visual-qa
   - benchmark_ref: domains/build/benchmarks/frontend-eval.md#task-3-accessibility-and-visual-qa-review
   - runtime:
   - model:
   - mode: standard
   - effort: high
   - agent_ids:
   - status:
   - timeout_status:
   - actual_latency:
   - specialist_call_count:
   - repair_loop_count:
   - verifier_count:
   - changed_artifacts:
   - wcag_target: WCAG 2.2 AA
   - accessibility_tool:
   - accessibility_result_path:
   - lighthouse_result_path:
   - core_web_vitals:
   - playwright_result_path:
   - screenshot_paths:
   - visual_diff_result:
   - viewport_coverage:
   - keyboard_flow_checked:
   - screen_reader_semantics_checked:
7. Promotion note:
   - State explicitly that this single run cannot promote any frontend graph node.
```

## Result Record Instructions

Create two result records after the runs:

- `baseline-build-frontend-a11y-visual-qa`
- `guided-build-frontend-a11y-visual-qa-standard-high`

Use `evals/templates/result-record.md`.

Required scoring dimensions:

- `accessibility`
- `visual_stability`
- `responsive_fit`
- `state_correctness`
- `behavior_correctness`
- `performance`
- `implementation_minimality`
- `verification_evidence`
- `instruction_adherence`
- `trajectory_efficiency`

Comparison rule:

- Guided output must beat baseline by at least 0.5 average points across two or more frontend tasks before any frontend graph node can move beyond draft.
- A single successful Task 3 run is signal only.
- Any serious accessibility regression, destructive scope expansion, or invented verification blocks promotion.

## How To Run In Kilo

1. Open Kilo in the target frontend repository.
2. Fill the fields at the top of this file.
3. Paste the baseline prompt and save the final response.
4. Reset the conversation or start a new run with the same repo state.
5. Paste the Build-guided Standard/High prompt and save the final response.
6. Copy both summaries into result records under `evals/results/` in this repository.

Do not ask Kilo to create the result records in the same run as the review. Use a separate result-record packet after both outputs exist.

Recommended first run:

- `TIMEBOX`: 10 minutes baseline, 15 minutes guided.
- `mode`: `standard` for guided.
- `effort`: `high` for guided.
- `changed_artifacts`: should be `none` because this is a read-only eval.

## Result-Record Packet Prompt

Use this only after both baseline and guided final responses exist.

```text
MANURELLA RUNTIME PACKET
- packet_class: verification
- mode: fast
- effort: medium
- timebox: 5 minutes

Objective:
Create two result records from the already-completed baseline and guided frontend QA outputs.

Allowed actions:
- Read the baseline output.
- Read the guided output.
- Read evals/templates/result-record.md.
- Write result records only under evals/results/.

Forbidden actions:
- Do not edit fixture files.
- Do not edit app/source files.
- Do not create eval.md inside evals/fixtures/**.
- Do not rerun the review.
- Do not invent missing model, latency, tool, or screenshot evidence.

Expected output:
- evals/results/baseline-build-frontend-a11y-visual-qa.md
- evals/results/guided-build-frontend-a11y-visual-qa-standard-high.md
- A short summary of missing metadata.
```
