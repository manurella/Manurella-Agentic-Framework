# Research Prompt: Domain Decomposition

Use this prompt when we need deeper research before expanding a domain pack.

```text
You are a principal agent-systems architect and domain specialist.

Research task:
Design a rigorous sub-agent decomposition for the following Manurella domain:

[DOMAIN NAME]

Current domain purpose:
[PASTE CURRENT DOMAIN README]

Project context:
Manurella Agentic Framework is a runtime-agnostic framework for improving weaker/free model output through specialist domain packs, controlled context, evaluation, memory, tools, and adapters. Kilo Code is the first runtime target, but the framework must remain portable to Codex, ChatGPT, Gemini, and custom Python/MCP tooling.

Requirements:
1. Identify the best sub-agent boundaries for this domain.
2. For each sub-agent, define:
   - purpose
   - use when
   - do not use when
   - required context
   - permissions/tool needs
   - output contracts
   - evaluation rubric
   - common failure modes
3. Explain which sub-agents should be top-level selectable agents and which should be internal subagents.
4. Identify what should be always-on prompt, what should be reference material, and what should be retrieved only when needed.
5. Recommend a minimal v0 subset and a later v1/v2 expansion.
6. Include benchmark task ideas for each sub-agent.
7. Cite current sources where relevant.

Constraints:
- Do not produce generic AI role descriptions.
- Optimize for weaker/non-frontier models.
- Prefer verifiable outputs and clear boundaries.
- Avoid context stuffing.
- Distinguish evidence from speculation.
```

