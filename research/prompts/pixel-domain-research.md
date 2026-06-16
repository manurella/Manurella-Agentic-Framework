# Research Prompt: Pixel Domain

```text
You are a principal visual-design researcher, art director, image-generation specialist, and agent-systems architect.

Research task:
Design a state-of-the-art sub-agent architecture for the Manurella Pixel domain.

Project context:
Manurella Agentic Framework is a runtime-agnostic framework for improving weaker/free model output through specialist domain packs, controlled context, evaluation, memory, tools, and adapters. Kilo Code is the first runtime target, but the architecture must remain portable to Codex, ChatGPT, Gemini, and custom Python/MCP tooling.

Pixel domain scope:
Art direction, image prompt design, visual composition, style systems, brand/character consistency, model-specific prompt adaptation, image generation repair, moodboards, references, multi-image continuity, and evaluation of generated outputs.

Research requirements:
1. Map the major competencies inside visual art direction and modern image-generation workflows.
2. Propose the best v0 sub-agent decomposition.
3. Explain which sub-agents should be top-level selectable agents and which should be internal subagents.
4. Define each sub-agent's purpose, use-when boundary, do-not-use boundary, required context, tools/permissions, output contract, evaluation rubric, and common failure modes.
5. Identify what should be always-on prompt, what should be reference material, and what should be retrieved only when needed.
6. Recommend a v0, v1, and v2 expansion path.
7. Propose benchmark tasks for each sub-agent.
8. Explain how to optimize this domain for weaker/non-frontier models.
9. Cite current sources where relevant, including current image-generation model behavior and prompt practices.

Constraints:
- Do not assume one prompt style works across all image models.
- Treat generation outputs as stochastic and evaluate across repeated trials.
- Preserve visual consistency and repair loops as first-class concerns.
- Distinguish evidence, project experience, hypothesis, and speculation.
- Include critique of alternative decompositions.
```

