# Frontend A11y / Visual QA Fixture

Task: create a small static frontend evaluation fixture for Manurella under `evals/fixtures/frontend-a11y-visual-qa/`.

Implementation: added a local-only SaaS-style dashboard/settings panel with a header, form, avatar area, status cards, workflow panels, and a drawer interaction. Added plain CSS and JavaScript only, with no npm install or external assets. Added a lightweight Node static server so the fixture can be opened in a browser or accessed by Playwright at `http://127.0.0.1:4173/`.

The fixture intentionally includes realistic frontend issues across accessibility, responsive layout, visual stability, and user flow for evaluation, without including an issue answer key.

---

## Review record

1. Verdict: fail

2. Findings:
   - Severity: high
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/index.html:31-50`, `index.html:128-130`
     Why it matters: Form controls use visible `<span>` labels instead of associated `<label>` elements. Screen readers and voice input users do not get reliable name/role/value association for farm name, region, target, invite email, or role.
     Suggested fix: Wrap each label text in `<label for="...">` or associate it with the input/select via `for`/`id`.

   - Severity: high
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/index.html:118-120`, `styles.css:392-400`
     Why it matters: The drawer close target is a `<div>` with `aria-label="Close"` but no `role="button"`, `tabindex`, or keyboard activation. It is announced inconsistently and is not operable by keyboard.
     Suggested fix: Use a `<button type="button" aria-label="Close invite dialog">` for the close control.

   - Severity: high
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/index.html:115-145`, `app.js:22-35`, `app.js:59-64`
     Why it matters: The invite drawer is modal by `aria-modal`, but focus is not trapped, Escape is not handled, and focusable background controls remain reachable after opening. Users can become disoriented or interact behind the dialog.
     Suggested fix: Implement focus trapping, Escape-to-close, return focus to the opener, and disable or inert background content while the dialog is open.

   - Severity: medium
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/index.html:26`, `styles.css:136-140`
     Why it matters: The avatar image has no `alt`. Because it is decorative, it may still be announced by assistive technology and expose an unhelpful data URI.
     Suggested fix: Add `alt=""` to the avatar image.

   - Severity: medium
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/index.html:15-19`, `app.js:55-57`
     Why it matters: The top navigation links use `href="#"`, which can unexpectedly move focus/scroll to the top and do not represent real navigation. The hamburger button appears on mobile but has no menu behavior or `aria-expanded`/`aria-controls`.
     Suggested fix: Use real routes or buttons, and implement the mobile menu state with accessible expansion semantics.

   - Severity: medium
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/styles.css:36-40`, `styles.css:216-248`, `styles.css:288-338`
     Why it matters: Focus and several text colors are low contrast against light backgrounds, including secondary button text, muted helper text, route details, and focus outlines. This creates readability and keyboard-target risks for WCAG 2.2 AA.
     Suggested fix: Increase text and focus-indicator contrast to at least AA thresholds and avoid relying on muted gray for essential text.

   - Severity: high
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/styles.css:250-255`, `styles.css:445-479`, `styles.css:485-500`
     Why it matters: `.content { min-width: 720px; }` remains active on small viewports, and the drawer has `min-width: 430px` while its width can shrink below that. At phone widths, content is clipped or forces horizontal overflow because `body { overflow-x: hidden; }` hides the problem.
     Suggested fix: Remove fixed minimum widths from content/drawer internals or replace them with responsive widths such as `min-width: 0`, `width: 100%`, and safe max widths.

   - Severity: medium
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/app.js:37-42`
     Why it matters: A fourth status card is appended 1100ms after initial render, changing the status grid from three to four cards. This creates layout shift and animation-driven visual instability.
     Suggested fix: Render the complete initial card set server-side or reserve layout space before insertion.

   - Severity: medium
     Evidence: `evals/fixtures/frontend-a11y-visual-qa/index.html:128-139`, `app.js:65-68`
     Why it matters: Sending an invite accepts empty or invalid email values and always reports success with no validation, disabled/loading state, or error state.
     Suggested fix: Use native email validation or explicit validation, expose errors with `aria-describedby`, and provide pending/success/error states.

3. Checks attempted:
   - Read-only inspection of `evals/fixtures/frontend-a11y-visual-qa/index.html`, `styles.css`, and `app.js`.
   - Attempted Playwright navigation to the local file route; file protocol access was blocked.
   - No dev server, accessibility tooling, Lighthouse, Playwright automation, or screenshot tooling was available for this route.

4. Verification gaps:
   - Browser rendering and visual overlap/clipping could not be confirmed with screenshots because local file navigation was blocked and no dev server was available.
   - Automated keyboard traversal, screen reader announcements, contrast measurement, Lighthouse, and CLS/INP metrics were not run.
   - Runtime drawer behavior was inferred from source only; focus trap and background inert behavior were not executable-tested.

5. Scores from 1-5:
   - accessibility: 2
   - visual_stability: 3
   - responsive_fit: 2
   - behavior_correctness: 3
   - performance: 4
   - verification_evidence: 2
   - instruction_adherence: 5
   - trajectory_efficiency: 5

6. Result-record fields:
   - status: completed
   - timeout_status: not_applicable
   - actual_latency: 0
   - changed_artifacts: evals/fixtures/frontend-a11y-visual-qa/eval.md
