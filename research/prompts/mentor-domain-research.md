# Research Prompt: Mentor Domain

```text
You are a principal learning-systems researcher, language-learning specialist, and agent-systems architect.

Research task:
Design a state-of-the-art sub-agent architecture for the Manurella Mentor domain.

Project context:
Manurella Agentic Framework is a runtime-agnostic framework for improving weaker/free model output through specialist domain packs, controlled context, evaluation, memory, tools, and adapters. Kilo Code is the first runtime target, but the architecture must remain portable to Codex, ChatGPT, Gemini, and custom Python/MCP tooling.

Mentor domain scope:
Language learning first, then expansion into general tutoring and learning systems. Include placement, curriculum planning, explanations, correction, practice design, spaced repetition, learner modeling, feedback tone, progress tracking, and transfer to non-language subjects.

Research requirements:
1. Map the major competencies inside effective language teaching and general tutoring.
2. Propose the best v0 sub-agent decomposition.
3. Explain which sub-agents should be top-level selectable agents and which should be internal subagents.
4. Define each sub-agent's purpose, use-when boundary, do-not-use boundary, required context, tools/permissions, output contract, evaluation rubric, and common failure modes.
5. Identify what should be always-on prompt, what should be reference material, and what should be retrieved only when needed.
6. Recommend a v0, v1, and v2 expansion path.
7. Propose benchmark tasks for each sub-agent.
8. Explain how to optimize this domain for weaker/non-frontier models.
9. Cite current sources where relevant, including evidence from learning science and language acquisition research.

Constraints:
- Do not produce generic tutor personas.
- Avoid overclaiming learner-state precision.
- Prefer adaptive, testable teaching moves.
- Distinguish evidence, project experience, hypothesis, and speculation.
- Include critique of alternative decompositions.
```

