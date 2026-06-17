# Build Frontend Quality Gate

## Purpose

This gate defines the minimum evidence required before Manurella can claim a frontend implementation or frontend review is high quality.

It is promoted from the first frontend accessibility/visual QA eval failure. The failure showed that a model can list accessibility issues while still missing obvious visual evidence, mixing fixture files with result records, and reporting weak verification.

## Applies To

Use this gate for Build-domain tasks involving:

- UI implementation
- frontend code review
- accessibility review
- visual QA
- responsive layout
- design-to-code work
- browser behavior
- stateful forms, dialogs, menus, drawers, navigation, or dashboards

## Gate Summary

A frontend result is not complete until it has evidence for:

1. Structure and scope.
2. Accessibility.
3. Visual and responsive fit.
4. State and user flow.
5. Performance smoke risk.
6. Verification record quality.

If a check cannot run, record `not_available` or `not_run` and explain the impact.

## 1. Structure And Scope

Check:

- existing project conventions
- component boundaries
- routing and state ownership
- design system or styling patterns
- scope expansion
- generated-file or fixture pollution

Evidence examples:

- files inspected
- diff summary
- affected components/routes
- explicit no-edit/read-only confirmation when applicable

Failure examples:

- creating eval result files inside fixture folders
- editing runtime-generated files during a read-only eval
- changing unrelated styling or content
- using a new UI abstraction when existing patterns are sufficient

## 2. Accessibility

Check WCAG 2.2 AA-oriented risks:

- semantic landmarks
- headings
- form labels
- name, role, value
- keyboard access
- focus order and visible focus
- modal focus trap and Escape handling
- background inertness for modal surfaces
- alt text and decorative image handling
- contrast
- reduced motion
- error and status announcements

Evidence examples:

- source lines
- axe/Lighthouse/Playwright output
- keyboard walkthrough notes
- screenshot notes for focus or contrast problems

Blocker/high examples:

- keyboard-inoperable critical control
- dialog that traps or loses user focus
- unlabeled critical form controls
- unreadable essential text
- fake button implemented as non-interactive element

## 3. Visual And Responsive Fit

Screenshots are first-class evidence. If screenshots exist, they must be inspected before final judgment.

Check:

- broken images or media
- overlap
- clipping
- hidden overflow
- horizontal scroll on mobile
- text overflow
- unstable card/grid resizing
- drawer/modal fit
- spacing hierarchy
- desktop and mobile viewport fit
- dark/light theme assumptions
- layout shift after async updates

Evidence examples:

- screenshot paths
- viewport sizes
- visible issue descriptions
- source lines for responsible CSS/HTML

Failure examples:

- screenshot shows a broken avatar/image and the review does not mention it
- `overflow-x: hidden` hides layout overflow
- fixed `min-width` breaks phone viewport
- asynchronous insertion shifts core layout without reserving space

## 4. State And User Flow

Check:

- loading, empty, pending, success, error, and disabled states
- form validation
- async behavior
- cache/server/client/URL state boundaries
- dialog/menu open-close behavior
- focus restoration
- navigation validity
- retry and cancellation behavior

Evidence examples:

- source lines
- browser interaction notes
- Playwright trace or test output
- manual flow checklist

Failure examples:

- invite form accepts empty email and reports success
- mobile menu button has no state or behavior
- drawer close target cannot be activated by keyboard
- success toast appears without validation or pending state

## 5. Performance Smoke

Check obvious risk, not full optimization:

- LCP candidate and media size
- render-blocking work
- bundle or dependency expansion
- main-thread heavy interactions
- layout shift
- repeated unnecessary client work
- large client-only rendering where server/static output would work

Evidence examples:

- Lighthouse path
- manual source note
- screenshot/CLS note
- dependency diff

## 6. Verification Record Quality

Every frontend eval record must include:

- `runtime`
- `model`
- `mode`
- `effort`
- `actual_latency`
- `timeout_status`
- `changed_artifacts`
- `accessibility_tool`
- `lighthouse_result_path`
- `playwright_result_path`
- `screenshot_paths`
- `viewport_coverage`
- `keyboard_flow_checked`
- `screen_reader_semantics_checked`
- verification gaps

Invalid records:

- `actual_latency: 0` for a real model run
- invented tool results
- screenshot paths listed but not inspected
- no distinction between baseline and guided output
- result files written inside fixture target folders

## Build/Frontend Specialist Boundaries

The current frontend graph nodes are draft research aids until evals prove they improve output.

- `frontend-architect`: plans structure, state ownership, component boundaries, accessibility strategy, and verification path.
- `accessibility-auditor`: checks semantics, keyboard, focus, labels, contrast, and assistive-technology affordances.
- `visual-qa-specialist`: inspects screenshots and responsive fit.
- `state-flow-specialist`: checks form, async, URL, cache, and interaction state.
- `performance-reviewer`: checks frontend performance smoke risk.

Do not invoke all specialists by default. Pick the smallest set needed for the packet.

## Completion Rule

Frontend work is complete only when:

1. Material findings or implementation changes are grounded in evidence.
2. Screenshots, if available, were inspected.
3. Objective tools, if available, were run or marked unavailable.
4. Verification gaps are explicit.
5. The result is recorded outside the target fixture.

If any of those fail, the result is `partial`, `fail`, or `blocked`, not `pass`.
