# Build Frontend Evaluation

## Purpose

This benchmark evaluates whether Manurella's experimental Build/frontend graph slice improves frontend output over a baseline prompt.

The frontend nodes are still draft candidates. This benchmark is a promotion gate, not proof of acceptance.

## Industry Standard Anchors

Use current industry-standard frontend checks as objective evidence where possible:

- WCAG 2.2 Level AA for accessibility conformance targets: <https://www.w3.org/TR/WCAG22/>
- axe-core or equivalent automated accessibility checks: <https://github.com/dequelabs/axe-core>
- Lighthouse for automated page quality audits: <https://developer.chrome.com/docs/lighthouse/overview>
- Core Web Vitals thresholds for performance and user experience: <https://web.dev/articles/vitals>
- Playwright for browser behavior and visual comparison checks: <https://playwright.dev/docs/accessibility-testing> and <https://playwright.dev/docs/test-snapshots>

These checks do not replace human judgment. Automated accessibility and visual checks are evidence inputs; final scoring must also inspect keyboard flow, semantic intent, responsive behavior, and task fit.

## Run Matrix

Run each task in at least two conditions:

| Condition | Runtime policy | Purpose |
| --- | --- | --- |
| Baseline | Same model, no Manurella Build guidance | Measure raw model/runtime output. |
| Build-guided Standard/High | Build runtime policy, Standard Mode, High effort | Measure default serious Manurella guidance. |
| Build-guided Fast/High | Build runtime policy, Fast Mode, High effort | Optional for tiny UI tasks where speed matters. |

Use the same model, repository seed, task prompt, and timebox for baseline and guided runs unless the benchmark explicitly tests runtime mode trade-offs.

## Task 1: Component Implementation

Goal: implement a small reusable UI component from a compact product brief.

Prompt shape:

```text
Implement a reusable [component] for [product context]. Preserve existing project conventions. Include loading, empty, error, and populated states. The component must be responsive and accessible.
```

Required evidence:

- changed files
- component or page screenshot at mobile and desktop viewport
- unit/component test or documented reason no test harness exists
- accessibility scan result when the app can render
- visual notes for layout fit and text overflow

Primary scores:

- semantic component structure
- responsive stability
- accessibility
- state coverage
- implementation minimality
- verification evidence

## Task 2: State-Flow Repair

Goal: repair a frontend interaction bug involving client, server, URL, form, async, or cache state.

Prompt shape:

```text
Fix the UI state bug where [observable behavior]. Preserve existing state-management conventions and verify the corrected user flow.
```

Required evidence:

- root-cause note distinguishing client state, server state, URL state, form state, and async effects
- relevant test or browser flow
- no unrelated state-management library changes
- before/after behavior summary

Primary scores:

- state-boundary correctness
- race-condition avoidance
- minimality
- behavior verification
- regression-risk notes

## Task 3: Accessibility And Visual QA Review

Goal: audit an existing UI change without rewriting it.

Prompt shape:

```text
Review this frontend change for accessibility, visual stability, responsive behavior, and user-flow risk. Do not edit files. Return material findings only, with evidence and suggested fixes.
```

Required evidence:

- axe/Lighthouse accessibility output when runnable
- keyboard navigation notes
- mobile and desktop screenshot review
- exact files or selectors behind each finding
- explicit approval when no material issues are found

Primary scores:

- material finding recall
- false-positive control
- WCAG relevance
- visual and responsive evidence
- fix specificity

## Task 4: Performance Smoke

Goal: catch obvious frontend performance regressions in a small implementation or review.

Prompt shape:

```text
Evaluate this frontend change for obvious performance regressions. Focus on bundle impact, render work, layout shift, data loading, and unnecessary client work.
```

Required evidence:

- Lighthouse or equivalent performance audit when a runnable page exists
- Core Web Vitals risk notes: LCP, INP, CLS
- bundle or dependency impact when the task changes imports
- render or data-loading risk notes

Primary scores:

- identification of real performance risks
- avoidance of speculative optimization
- threshold awareness
- practical repair guidance

## Industry Standard Gates

Use these as hard or soft gates depending on the repository's available tooling.

| Category | Preferred check | Gate |
| --- | --- | --- |
| Accessibility automation | axe-core, Playwright accessibility scan, or Lighthouse accessibility | No critical/serious automated violations introduced. |
| Accessibility manual | WCAG 2.2 AA-oriented keyboard, focus, label, name/role/value, contrast, and semantic review | No blocker in the changed workflow. |
| Performance | Lighthouse or lab-equivalent measurement | No obvious LCP, INP/TBT, CLS, payload, or main-thread regression. |
| Visual regression | Playwright screenshot comparison or before/after screenshots | No incoherent overlap, clipping, unreadable text, or unintended layout shift at mobile and desktop sizes. |
| Behavior | Playwright E2E, component test, unit test, or equivalent manual browser evidence | Critical user path works. |
| Code quality | project lint/typecheck/tests where available | No new known lint/type errors in touched surface. |

Core Web Vitals target references:

- LCP: good at 2.5 seconds or less
- INP: good at 200 milliseconds or less
- CLS: good at 0.1 or less

When only lab tools are available, record the limitation. Lighthouse cannot fully replace field INP measurement, so TBT may be used as a lab proxy.

## Scoring

Use 1-5 scores.

| Score | Meaning |
| --- | --- |
| 1 | Fails task or introduces material regression. |
| 2 | Partially useful but misses important requirements or evidence. |
| 3 | Acceptable but has notable gaps. |
| 4 | Strong result with minor gaps. |
| 5 | Excellent result with strong evidence and no material gaps. |

Required dimensions:

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

Promotion signal:

- Guided output should beat baseline by at least 0.5 average points across two or more tasks before any frontend graph node moves beyond draft.
- A single excellent run is not enough for promotion.
- Any serious accessibility, security, data-loss, or destructive-scope regression blocks promotion regardless of average score.

## Result Record Requirements

Each run must record:

- model and runtime
- mode and effort
- prompt version
- graph node ids used or intentionally not used
- industry checks attempted
- commands run
- screenshots or report paths
- latency and timeout status
- specialist calls
- changed artifacts
- scores and reviewer notes

## First Kilo Trial Recommendation

Start with Task 3, Accessibility And Visual QA Review.

Reason: it is read-only, lower risk, and directly tests whether Manurella improves frontend judgment before allowing implementation authority.
