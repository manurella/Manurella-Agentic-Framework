# Kilo Runtime Projection Synthesis

## Record State

- Date: 2026-06-22
- Inputs: `Kilo Runtime Behavior Research.md`, `deep-research-report (5).md`
- Official web verification from this environment: blocked by HTTP 403
- Adoption posture: conservative intersection of both reports, preferring official Kilo citations

## Accepted Claims

1. `.kilo/agents/<id>.md` is the canonical project-local agent emission path. Other aliases remain compatibility observations, not Manurella targets.
2. Agent Markdown uses YAML frontmatter plus a prompt body. The accepted frontmatter surface is `description`, `mode`, `permission`, `steps`, and only source-pinned optional fields such as `model`, `temperature`, `top_p`, `variant`, `hidden`, `disable`, and `color`.
3. Agent modes are `primary`, `subagent`, and `all`.
4. Kilo permission values are `allow`, `ask`, and `deny`; scoped maps are supported for file, command, and task/delegation boundaries.
5. Kilo models web access separately as `webfetch` and `websearch` and delegation as `task`.
6. No reviewed source documents direct Runtime Session Bundle or Operation Packet ingestion. Manurella must render a sanitized prompt-compatible payload.
7. `kilo run --format json` is an event stream, not a stable Manurella result schema.
8. Native effort/variant values are provider-specific and cannot represent Manurella's effort lattice portably.

## Adapter Decisions

- Emit only explicit Manurella `allow` as Kilo `allow`.
- Lower Manurella `ask` and `deny` to Kilo `deny` in strict projections.
- Never add `--auto` or `--dangerously-skip-permissions` to generated invocation guidance.
- Use name-scoped `permission.task` maps with a deny-all fallback.
- Render bounded memory claims and operation fields only after the runtime-session privacy gate has passed.
- Generate deterministic artifacts and fixtures without invoking a model or spending quota.
- Treat the generated CLI argv as suggested operator guidance, not evidence that Kilo executed.

## Deferred Or Rejected

- Defer `.kilo/agent/` and `.opencode/agents/` aliases.
- Defer native effort-to-`variant` mapping.
- Defer ACP/direct structured packet integration.
- Reject prompt-file flags not present in reviewed official evidence.
- Reject unattended reliance on `--auto`; the reports found conflicting official descriptions.
- Reject assumptions about stable JSON event fields or session resume semantics without pinned-version captures.

## Primary Source URLs Reported

- <https://kilo.ai/docs/customize/custom-modes>
- <https://kilo.ai/docs/customize/custom-subagents>
- <https://kilo.ai/docs/customize/agent-permissions>
- <https://kilo.ai/docs/code-with-ai/platforms/cli>
- <https://kilo.ai/docs/code-with-ai/platforms/cli-reference>
- <https://github.com/kilo-org/kilocode>

## Residual Gaps

- Exact `--auto` behavior for a pinned installed Kilo build.
- Stability of alias agent directories.
- Stable JSON event schema, if any.
- Exact session resume and timeout exit behavior.
- Runtime parsing confirmation via `kilo debug agent` or equivalent on the installed version.

These gaps block unattended execution claims, not deterministic projection generation.
