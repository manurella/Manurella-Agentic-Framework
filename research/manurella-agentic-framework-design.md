# **Architecture Proposal: Manurella-Agentic-Framework**

## **A. Executive Summary**

The transition from monolithic prompt-based personas to distributed, verifiable agent architectures represents the core paradigm shift in artificial intelligence engineering as of 2026\. The legacy system, "Family System v13," operating as a single large YAML file containing Kilo Code custom modes, successfully established specialized roles for coding, creative writing (Muse), art direction (Pixel), and language tutoring (Lingua)1. However, relying on static configurations and monolithic prompt injection inevitably breaks down due to context rot, rigid routing, and framework lock-in3. The "Manurella-Agentic-Framework" (MAF) v0 rebuild is proposed as a runtime-agnostic, portable agentic foundation engineered to transcend these limitations.  
The primary objective of MAF is to construct an architecture capable of extracting frontier-level capabilities from weaker, smaller, or open-weight models (such as the 8B to 35B parameter class) without relying exclusively on expensive, high-latency cloud APIs5. This objective cannot be achieved through prompt engineering alone. It requires a structural paradigm shift: implementing Spec-Driven Development (SDD) to constrain generative search spaces, deploying dynamic multi-armed bandit routing to optimize model selection per task, executing aggressive context compaction to preserve working memory, and establishing robust Model Context Protocol (MCP) toolchain isolation7. By strictly separating the "Kernel"—the agent's constitution, memory, and reasoning engine—from the "Adapter"—the specific runtime environment such as LangGraph, Kilo Code, or Codex—MAF guarantees absolute portability while maximizing the reasoning efficiency of non-frontier models.

## **B. Survey of Current Agent Architecture Best Practices (2026)**

The fundamental abstraction of agent programming has shifted toward the "Software 3.0" paradigm, famously articulated by Andrej Karpathy. In this model, neural network weights serve as the central processing unit (CPU), the context window functions as volatile random-access memory (RAM), and prompting combined with tool schemas acts as the procedural programming logic11. Within this paradigm, several state-of-the-art architectural patterns have emerged to maximize reliability and mitigate the inherent stochasticity of large language models.  
Early agent architectures relied heavily on the ReAct (Reasoning and Acting) pattern, where a model interleaves thinking and tool execution sequentially. While effective for simple queries, ReAct struggles with long-horizon tasks, often falling into repetitive loops when applied to weaker models. Consequently, the industry shifted toward Plan-and-Execute architectures, separating the strategic planning phase from the tactical execution phase. However, even this proved insufficient for complex software engineering. The current gold standard is Spec-Driven Development (SDD)7. Under SDD, a Coordinator agent does not generate code or final outputs directly; instead, it drafts a highly structured markdown specification containing acceptance criteria, scope boundaries, and constraints. Implementer sub-agents execute exclusively against this specification, drastically reducing architectural drift and providing a deterministic baseline that allows smaller models to succeed by constraining their search space to clearly defined micro-tasks7.  
To ensure output fidelity, the Maker-Checker pattern (or Supervisor-Worker) pairs a generative model with a critical verification model7. Reflexion and self-critique mechanisms force the agent to evaluate its own output against the SDD acceptance criteria before finalizing a task, creating an internal feedback loop that mimics human cognitive refinement. Furthermore, Router-Specialist architectures employ lightweight classifiers to analyze intent and route tasks to domain experts, ensuring that simple formatting tasks are not sent to expensive frontier models9.  
The standardization of tool use via the Model Context Protocol (MCP) separates the capability layer from the cognitive layer, permitting agents to invoke external resources securely without bloating their system prompts with complex API logic17. Simultaneously, the Agent2Agent (A2A) protocol enables opaque, heterogeneous agents to discover one another via standard JSON "Agent Cards" and collaborate over HTTP or Server-Sent Events (SSE) without sharing internal states or memories20. Finally, Eval-driven development has replaced heuristic testing; agentic workflows are now continuously measured against deterministic rubrics and LLM-as-a-judge scoring to ensure measurable quality over subjective claims15.

## **C. Evaluation of Agent Runtimes and Frameworks**

To maintain portability, MAF must define its agents abstractly as data structures and compile them down to various runtime targets. The following analysis evaluates leading 2026 frameworks to determine adapter priorities, assessing portability, observability, tool support, cost, complexity, and suitability for orchestrating weaker models.

| Framework / Runtime | Architectural Philosophy | Observability & State Management | Tool & Model Support | Suitability for MAF v0 |
| :---- | :---- | :---- | :---- | :---- |
| **LangGraph** | Graph-based state machine providing deterministic control flow, cycles, and durable execution24. | Best-in-class checkpointing, time-travel debugging, and native integration with LangSmith for granular execution traces24. | Model-agnostic. Wraps LangChain tools; MCP support is functional but requires manual wiring24. | **High**. Ideal as the primary heavy-duty execution environment for complex, multi-step workflows requiring strict human-in-the-loop approvals. |
| **CrewAI** | Role-based hierarchical collaboration where agents operate as a "crew" with assigned backstories and tasks24. | Basic per-agent and shared memory. Enterprise tier offers a dashboard and exports OpenTelemetry metrics24. | First-class native MCP support; automatically negotiates tool discovery and execution24. | **Medium**. Excellent for rapid prototyping of non-engineering tasks (e.g., Muse), but the opinionated abstractions limit the fine-grained control needed for SDD. |
| **AutoGen** | Event-driven, multi-agent conversational framework heavily optimized for code execution25. | Relies on conversational history rather than explicit state schemas. Observability is improving but trails LangGraph25. | Excellent code execution sandboxing. Deep integration with Microsoft ecosystems25. | **Low to Medium**. Powerful for parallel coding tasks, but the conversational routing model can cause weaker models to lose focus compared to explicit state graphs. |
| **OpenAI Agents SDK** | Handoff chain architecture utilizing stateless, session-based routing24. | Built-in tracing for agent runs and handoffs; integrates seamlessly with Braintrust28. | Native sandbox environments and first-class MCP support, but heavily optimized for OpenAI APIs24. | **Medium**. The fastest path to a working prototype if locked into the OpenAI ecosystem, but vendor lock-in violates MAF's portability mandate. |
| **Semantic Kernel** | Enterprise-grade integration of AI into existing C\#/Python codebases26. | Strong enterprise telemetry and integration with Azure monitor31. | Deeply integrated into Microsoft architectures26. | **Low**. Overly complex for a lightweight, portable Python kernel aiming to support free/local models. |
| **Google ADK** | Code-first, TypeScript/Python framework native to the A2A protocol for cross-framework interoperability21. | Vertex AI session management and structured graph logic21. | Deep MCP ecosystem support and standardized Agent Card discovery34. | **High**. The A2A capabilities perfectly match the need for isolated specialist deployment (e.g., separating Lingua from DevOps). |
| **Kilo Code Agents** | Markdown-based IDE agents (.md files with YAML frontmatter) defining prompt, mode, and permissions1. | Handled natively by the IDE workspace; telemetry is internal to the editor1. | Explicit permissions for read, edit, bash, and MCP tools mapped via YAML1. | **Critical**. As the direct successor to Family System v13, compiling to this format is the highest priority for the v0 MVP. |
| **Codex AGENTS.md** | Persistent directory-level constitutional instructions combined with reusable, composable Skills36. | Stateless constitutional context; relies heavily on external skill scripts and local environment execution37. | Native MCP support and implicit IDE tool access37. | **High**. Excellent for repository-level behavioral governance and packaging procedural memory into reusable SKILL.md workflows. |
| **Custom Python Runtime** | Completely owned runtime executing a core loop of LLM generation, tool validation, and memory updates. | Infinite observability potential via custom trace loggers emitting JSON-lines for evaluation2. | Unrestricted flexibility; can consume any MCP server and route to any LLM provider via LiteLLM or similar wrappers. | **Primary**. MAF must be built as a Custom Python Core that defines agents abstractly, subsequently using adapters to target the frameworks listed above. |

## **D. Architecture Proposal: Portable Layered Design**

To guarantee runtime independence and maximize the utility of weaker models, MAF will utilize a layered architecture spanning nine distinct conceptual modules. The guiding principle is to separate the declaration of intent (the Kernel) from the execution of the environment (the Runtime Adapter).

### **1\. Kernel and Constitution Layer**

The Kernel acts as the central definition registry. It defines the "Constitution"—a minimal, rigid set of invariant rules governing safety, coding standards, and operational limits. Rather than bloating a single monolithic system prompt with hundreds of conditional rules, the constitution is strictly scoped to approximately 150–200 instructions maximum14. This constraint is critical; research demonstrates that exceeding this limit introduces severe context distraction and degrades instruction adherence in non-frontier models39. The Kernel stores agent definitions, including the core persona, primary domain, and authorized capabilities, completely decoupled from execution logic.

### **2\. Task Router Layer**

Relying strictly on frontier models for all operations is economically unfeasible, while relying solely on local models guarantees reasoning failures on complex tasks. The Task Router implements a Contextual Multi-Armed Bandit algorithm (specifically, LinUCB or Thompson Sampling) to dynamically select the optimal model and specialist agent for a given query9. The router extracts lightweight features from the incoming prompt—such as token length, syntactic complexity, intent keywords, and required tool schemas—and encodes them via a compact embedding model (e.g., all-MiniLM-L6-v2)9. Based on the learned reward distributions, simple UI formatting or boilerplate generation tasks are automatically routed to fast, inexpensive models (e.g., Qwen 2.5 7B or Gemini Flash), while complex architectural design is reserved for frontier models.

### **3\. Specialist Modules and Domain Packs**

The generalized roles of the legacy "Family System" are elevated into strictly isolated Specialist Modules, packaged as Domain Packs.

* **Muse**: Configured with high-temperature sampling parameters, equipped with narrative-analysis MCP tools, and heavily reliant on long-context episodic memory to maintain thematic consistency across extensive prose generation.  
* **Pixel**: Configured for precise visual prompt engineering, equipped with Figma MCP resources to pull design system tokens directly into context, and provided with image-generation validation tools to verify visual output7.  
* **Lingua**: Tuned for linguistic corrections and pedagogical pacing, relying on contextual memory to track the user's vocabulary level, and equipped with dictionary and translation MCP resources.  
* **Architect/DevOps/Coding**: Strictly operates under the Spec-Driven Development (SDD) paradigm, utilizing strict schema validation to force predictable JSON or Markdown outputs, and restricted to iterative, test-driven tool execution7.

### **4\. Tool Layer**

Tools are decoupled from the models via the Model Context Protocol (MCP). The Tool Layer implements the server-side logic for file manipulation, source control operations, and web research. MAF enforces a strict distinction between MCP *Tools* (model-controlled actions with side-effects, such as executing a bash script) and MCP *Resources* (application-controlled read-only data, such as a UI style guide or database schema)8. This distinction prevents weaker models from hallucinating destructive actions while still providing them access to critical context.

### **5\. Memory Layer**

The memory layer manages state across sessions to prevent the AI amnesia inherent in stateless API calls45. It is divided into working memory (managed via context compaction), episodic memory (vector-indexed interaction histories), semantic memory (abstracted user preferences), and procedural memory (reusable tool sequences). The memory layer continuously runs background processes during idle time to consolidate episodic interactions into semantic rules, ensuring the agent learns without expanding the context window infinitely45.

### **6\. Eval Layer**

A built-in evaluation harness runs offline to verify agent outputs against deterministic assertions and LLM-as-a-judge rubrics. Continuous evaluation provides the critical reward signal required to update the Bandit Router's probability distributions and validates whether a newly compiled prompt successfully guides a weaker model to a correct solution23.

### **7\. Runtime Adapters**

The output layer of MAF. It serializes the Kernel's abstract agent objects into physical formats consumable by specific ecosystems. The Kilo Exporter compiles the agent into .kilo/agents/ markdown files; the Codex Exporter generates AGENTS.md and skill scripts; the LangGraph Compiler generates Python nodes and edges; and the A2A Server exposes specialists as HTTP endpoints using the standard .well-known/agent-card.json schema1.

### **8\. Safety and Permission Model**

The safety model operates on the principle of least privilege, mapped directly to Role-Based Access Control (RBAC) at the MCP layer48. Destructive tools (e.g., executing arbitrary bash commands or dropping database tables) are sequestered behind Human-in-the-Loop (HITL) approval gates. The permissions are serialized into the runtime adapters; for example, the Kilo adapter translates a restricted file-editing capability into the YAML frontmatter permission: edit: "\*.md": "allow", "\*": "deny"1. Furthermore, prompt injection resilience is enforced by stripping executable commands from unverified MCP Resources before they enter the context window49.

## **E. Advanced Agent Memory and Context Management**

Weaker models suffer disproportionately from "context rot"—the measurable degradation of reasoning capability as the context window fills with tool results, retrieved documents, and conversational noise3. Expanding the context window to millions of tokens does not resolve this issue; it merely dilutes the model's attention mechanism across irrelevant data, creating a "lost in the middle" phenomenon40. MAF mitigates this through a structured memory taxonomy and aggressive context compaction.

### **Memory Taxonomy**

1. **Project State (Working Memory)**: The current conversation history, active files, and immediate task progress. This is bounded strictly by the active context window.  
2. **User Preferences (Semantic Memory)**: Abstracted, de-contextualized knowledge about the user and project conventions (e.g., "User prefers React Functional Components", "Target audience for Muse is young adult")47.  
3. **Domain Knowledge**: Static enterprise data, documentation, and architectural plans exposed exclusively as MCP Resources, fetched only via Just-In-Time retrieval4.  
4. **Successful Trajectories & Reusable Examples (Procedural Memory)**: Verified sequences of tool calls that achieved a specific goal. These are stored as reusable skill scripts (e.g., Codex .agents/skills) and injected into the prompt when similar tasks arise37.  
5. **Failures and Lessons (Episodic Memory)**: A localized vector store recording past agent errors (e.g., "Attempting to compile with flag \-X failed on macOS"). Injecting these negative examples prevents the agent from repeating historical mistakes47.

### **Context Compaction & Pollution Mitigation**

To prevent context rot, MAF implements a 5-tier compaction cascade, analogous to hierarchical cache eviction strategies in traditional computer science10.

* **Tier 1: Microcompact**: Invisible reordering of context blocks to preserve prompt prefix cache hits, reducing latency and cost without losing data10.  
* **Tier 2: Tool-Result Clearing**: Surgically walking the message history and replacing massive tool payloads (such as thousands of lines of a git diff) with lightweight placeholders (\[Old tool output cleared\]) while leaving the original tool\_call object intact. This reclaims massive token space without confusing the model regarding its past actions54.  
* **Tier 3: Context Collapse (Snip/Archive)**: Dropping the oldest, non-essential conversational turns using a Least Recently Used (LRU) eviction policy10.  
* **Tier 4: Auto Compact**: Triggered when the context reaches 75% capacity. An auxiliary, inexpensive model summarizes the middle of the conversation into structured XML tags (\<summary\>) containing the Goal, Constraints, Progress, and Next Steps. The active session is subsequently reset using only this dense summary55.  
* **Tier 5: Layered Tool Calling**: Rather than passing forty tool schemas into every prompt, MAF passes only the minimum necessary schemas to the active sub-agent. This avoids the severe context pollution caused by injecting irrelevant JSON schemas into the prompt4.

## **F. Tool Layer and MCP Server Design**

MAF adopts the Model Context Protocol as the strict boundary between the agent's cognitive processing and its environment. In v0, the following core schemas must be implemented as Python-based MCP servers or internal tools.

| Tool / Resource Name | Classification | Mechanism and Schema Concept |
| :---- | :---- | :---- |
| **Research Collector** | Resource | Exposes listResources and readResource for web scraping and codebase indexing. Returning data as structured x-mcp-header resources rather than executable tools prevents the model from hallucinating search parameters and over-consuming tokens8. |
| **Eval Runner** | Tool | Allows a Maker agent to trigger the Verifier agent mid-loop to score a proposed solution against the SDD acceptance criteria before finalizing the task23. |
| **Prompt Compiler** | Tool | Dynamically assembles the system prompt, fetching semantic memory from the vector database and injecting it just-in-time based on the current context4. |
| **Kilo Agent Exporter** | Tool | Translates the active agent state into a Kilo Code .kilo/agents/my-agent.md file. It maps requested capabilities directly to YAML permission groups1. |
| **Memory Indexer** | Tool | Processes episodic interaction logs during idle time, using an embedding model to map trajectories into semantic rules or procedural skills stored in Valkey or a similar high-speed vector store47. |
| **Scoring / Leaderboard** | Tool | Interfaces with the Eval Layer to log the performance of specific models on specific tasks, maintaining the database required for the Bandit Router to update its probability distributions9. |
| **Trace Logger** | Tool | Emits structured telemetry logs for every action, allowing diagnostic systems and safety guardrails to subscribe to the event stream synchronously2. |

All MCP tools must adhere strictly to JSON Schema (draft 2020-12)58. Crucially, MAF will implement explicit *Output Schemas* for all tool results. By defining outputSchema in the MCP response, the framework forces the LLM to process typed tool results, drastically reducing hallucination rates and enabling strict programmatic validation before the LLM even receives the data8.

## **G. Evaluation System Design**

Objective measurement is the only mechanism to prove that weaker models are achieving frontier-level output. The evaluation layer utilizes LLM-as-a-judge methodologies combined with deterministic assertions, evaluating not just the final output, but the entire trajectory of tool calls15.

### **Benchmark Categories and Scoring Rubrics**

| Category | Exact Metric | Evaluation Method | Penalty / Failure Condition |
| :---- | :---- | :---- | :---- |
| **Coding / Build Tasks** | Correctness, Instruction Adherence, Recovery from errors | Deterministic execution (pass@1) \+ LLM Judge for SDD adherence23. | Fails to compile; hallucinates non-existent libraries; fails to recover after receiving a stack trace. |
| **Architecture / Planning** | Completeness, Feasibility | LLM Judge comparing output to SDD requirements7. | Ignores defined technical constraints; omits edge cases; specifies deprecated APIs. |
| **Product / UI/UX** | Instruction Adherence, User Satisfaction | Visual validation tools \+ simulated user persona feedback. | Fails to implement design system tokens accurately; generates inaccessible HTML structures. |
| **Security Review** | Scope Minimization, Adversarial Resilience | Deterministic injection tests hidden in MCP resources49. | Attempts to execute unauthorized bash commands; modifies core constitution when prompted by malicious input. |
| **Research Synthesis** | Quality, Correctness, Tool Use | LLM Judge evaluating citations against source texts (FaithfulnessEvaluator)23. | Hallucinates facts not present in retrieved resources; fails to cite sources; excessively calls search tools. |
| **Creative Writing (Muse)** | Thematic Consistency, Context Recall | Needle-in-a-haystack recall tests \+ LLM stylistic analysis54. | Loses character voice over long contexts; forgets established plot constraints. |
| **Art Direction (Pixel)** | Prompt Efficacy | Deterministic syntax validation against Midjourney/Stable Diffusion standards. | Generates invalid parameter flags; ignores aspect ratio constraints. |
| **Language Tutoring (Lingua)** | Correctness, User Satisfaction | LLM Judge evaluating pedagogical pacing and grammatical accuracy. | Provides incorrect grammatical rules; speaks above the assessed vocabulary level of the user. |
| **General Chat** | Latency, Quality | Telemetry logging of time-to-first-token \+ session completion rates. | Exceeds latency thresholds; provides overly verbose, un-compacted answers. |

Evaluating final output is insufficient for agentic workflows15. MAF introduces a TrajectoryEvaluator which assesses the sequence of MCP tool invocations. A model that achieves the correct answer but hallucinates three nonexistent tool calls along the way receives a heavy penalty, as inefficient tool use exponentially drives up latency and API costs15.

## **H. Reinforcement Learning and Iterative Improvement**

Given the pragmatic constraint of utilizing mostly API or free open-weight models with limited compute, traditional online Reinforcement Learning (like PPO) is unfeasible. MAF utilizes a staged approach relying on eval-driven improvement, preference learning, and bandit routing.

### **Stage 1 (v0): Eval-Driven Routing (Contextual Bandits)**

The immediate reinforcement learning application resides in the Task Router. Using Thompson Sampling or LinUCB, the router maintains a Beta distribution representing the probability of success for each model-specialist pair, updated continuously by metrics derived from the Eval Layer9. Over time, the router learns autonomously that a free 8B model excels at markdown formatting but fails catastrophically at complex architecture tasks. This continuously adapts the routing table without requiring expensive fine-tuning of model weights, optimizing cost and latency dynamically43.

### **Stage 2 (v1): Direct Multi-Turn Preference Optimization (DMPO)**

To refine the prompting and tool-calling sequences of open-weight models locally, MAF will employ Direct Multi-Turn Preference Optimization (DMPO)63. Unlike standard DPO, which evaluates single outputs, DMPO evaluates entire state-action trajectories. The framework logs multiple completion paths for a given task, and the Verifier scores these trajectories. The preferred and rejected trajectories form a dataset used for lightweight offline fine-tuning, teaching local models to mimic the highly efficient tool-call patterns of frontier models63.

### **Stage 3 (v2+): Trajectory-Based Parameter Merged DPO (TPMM-DPO)**

For advanced deployments, TPMM-DPO mitigates the error accumulation inherent in iterative training by smoothly fusing model weights from different stages of the optimization trajectory. This creates a highly stable, robust reference model capable of autonomous self-correction during long-horizon tasks64.

## **I. Minimum Viable v0 Roadmap**

To avoid over-engineering, the v0 MVP must focus on establishing the architectural baseline, migrating the core functionality of the legacy system, and proving the primary runtime adapter functions flawlessly.

### **1\. Build First**

* **The Kernel**: Core Python classes for defining an Agent, its Constitution, and its Tool capabilities.  
* **Kilo Adapter**: A compiler that takes a Kernel Agent and outputs a valid .kilo/agents/\*.md file, translating tool definitions into Kilo YAML permission boundaries1. This is the critical step to support Kilo Code first without locking the kernel into Kilo's specific abstractions.  
* **Legacy Migration**: Port the precise personas of Muse, Pixel, and Lingua from the old Family System v13 YAML into MAF Domain Packs.  
* **Tier 1 & 2 Compaction**: Implement basic token accounting and Tool-Result Clearing to immediately improve long-context reliability for cheaper models10.

### **2\. Defer**

* **A2A Protocol**: Defer exposing agents as remote HTTP endpoints via Agent Cards until single-node orchestration is proven stable21.  
* **Advanced RL / TPMM-DPO**: Defer all offline fine-tuning. v0 will rely entirely on the Bandit Router and Eval-Driven prompt refinement.  
* **Graph Orchestration**: Defer LangGraph execution in favor of relying on Kilo Code's native IDE routing capabilities for initial testing.

### **3\. Delete or Split Out**

* **The Monolithic YAML**: The massive "Family System v13" configuration is deleted entirely. State is no longer managed in a single file; it is distributed across specialized Domain Packs and dynamically compiled.  
* **Generic Prompt Stuffing**: Large informational dumps in the system prompt are stripped out and replaced by MCP Resources, ensuring the constitution remains lean and highly actionable39.

## **J. Repository Structure and Project Governance**

The MAF repository will follow a monolithic package structure to maintain strict synchronization between the kernel, tools, and adapters, facilitating seamless integration testing.  
manurella-agentic-framework/ ├── docs/ \# Architectural Decision Records (ADRs) and API specs ├── packages/ │ ├── core-kernel/ \# Agent class, constitution schemas, prompt compilation │ ├── router-bandit/ \# Thompson Sampling & LinUCB implementation │ ├── memory-engine/ \# Context compaction, LTM extraction, vector integration │ ├── mcp-tools/ \# Standardized MCP servers (Research, File IO, Git, Eval) │ ├── runtimes/ \# Adapters mapping Kernel objects to specific frameworks │ │ ├── kilo-exporter/ \# Compiles to Kilo .md formats │ │ ├── codex-exporter/ \# Compiles to AGENTS.md and SKILL.md │ │ └── langgraph-runner/ \# Generates Python execution graphs │ └── domain-packs/ \# The Specialist Modules │ ├── muse/ \# Creative writing logic and narrative tools │ ├── pixel/ \# Visual prompt engineering │ ├── lingua/ \# Language tutoring definitions │ └── architect/ \# DevOps, SDD, and Coding modules ├── evals/ \# LLM-as-a-judge rubrics, benchmark datasets, and trajectories └── tests/ \# Unit tests for schemas and routing logic  
**Documentation and Versioning**: Documentation will be managed via Architectural Decision Records (ADRs) to track why specific design choices (e.g., choosing Thompson Sampling over round-robin) were made. The project will utilize Conventional Commits (feat:, fix:, chore:) combined with strict Semantic Versioning. Domain packs and adapters will be versioned independently from the core kernel, allowing prompt engineers to rapidly iterate on Muse or Pixel without forcing a major version bump of the underlying execution engine.

## **K. Risks and Anti-Patterns**

1. **Context Stuffing (Anti-Pattern)**: Loading the entire repository schema, style guides, and tool instructions into the constitution. This guarantees context rot. *Mitigation*: Strictly enforce the use of MCP Resources. The agent must proactively request documentation; it is not provided by default39.  
2. **Immortal Memory (Anti-Pattern)**: Appending every interaction to a vector database without a decay function or overwrite mechanism, leading to retrieval conflicts. *Mitigation*: Semantic memory must utilize confidence scores. When conflicts arise, older memories decay or are explicitly rewritten by the memory indexer39.  
3. **Token Passthrough Vulnerabilities (Risk)**: Allowing an agent to arbitrarily pass its own authentication tokens to downstream APIs, breaking the boundary of least privilege49. *Mitigation*: The MCP server must handle all authentication logic internally; the agent only requests the action, it does not manage the credentials.  
4. **Framework Lock-In (Risk)**: Tight coupling with LangGraph or Kilo Code execution paradigms. *Mitigation*: The Core Kernel must remain pure Python/JSON. Adapters must function strictly as one-way export mechanisms, ensuring the core agent definition remains pristine.

## **L. Open Questions for Project Ownership**

1. **Telemetry and Data Privacy**: Are we logging the trajectory and evaluation outputs locally (e.g., via SQLite/DuckDB) or transmitting them to a centralized observability platform like LangSmith or Braintrust? Local logging ensures maximum privacy, but distributed tracing significantly aids the Bandit Router in aggregating performance metrics across multiple environments.  
2. **LLM Backend Infrastructure**: Will the framework assume access to a local inference engine (e.g., Ollama, vLLM, Llama.cpp) for the cheaper models, or will it route entirely through API providers (e.g., OpenRouter)? Managing local VRAM limits the size of the models that can be run concurrently65.  
3. **Human-in-the-Loop (HITL) Thresholds**: For the Architect/DevOps domain pack, at what specific level of destructive capability (e.g., executing arbitrary bash scripts, modifying deployment configurations) should the framework force a hard halt and await explicit user confirmation? While Kilo Code handles this implicitly via its IDE extension permissions, MAF requires a standardized, framework-agnostic policy definition for other runtimes.

#### **Works cited**

1. Custom Modes \- Kilo Code, [https://kilo.ai/docs/customize/custom-modes](https://kilo.ai/docs/customize/custom-modes)  
2. Custom Kilo Code Modes Gallery · Kilo-Org kilocode · Discussion \#1671 \- GitHub, [https://github.com/Kilo-Org/kilocode/discussions/1671](https://github.com/Kilo-Org/kilocode/discussions/1671)  
3. Context Engineering: A Practical Guide for AI Agents (2026) | Sourcegraph, [https://sourcegraph.com/blog/context-engineering](https://sourcegraph.com/blog/context-engineering)  
4. The Bill Arrives: How to Manage Agentic AI Costs at Scale \- CockroachDB, [https://www.cockroachlabs.com/blog/agentic-ai-costs-at-scale/](https://www.cockroachlabs.com/blog/agentic-ai-costs-at-scale/)  
5. Qwen3 4B outperforms cloud agents on code tasks—with Mahoraga research \- Reddit, [https://www.reddit.com/r/LLMDevs/comments/1sxi00y/qwen3\_4b\_outperforms\_cloud\_agents\_on\_code/](https://www.reddit.com/r/LLMDevs/comments/1sxi00y/qwen3_4b_outperforms_cloud_agents_on_code/)  
6. The 7-Model Local AI Portfolio: How to Route Tasks Across Local and Cloud Models for Maximum Performance \- MindStudio, [https://www.mindstudio.ai/blog/7-model-local-ai-portfolio-routing-local-cloud](https://www.mindstudio.ai/blog/7-model-local-ai-portfolio-routing-local-cloud)  
7. What Is Spec-Driven Development? A Complete Guide \- Augment Code, [https://www.augmentcode.com/guides/what-is-spec-driven-development](https://www.augmentcode.com/guides/what-is-spec-driven-development)  
8. Model Context Protocol (MCP) \- AI SDK Core, [https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools](https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools)  
9. OrcaRouter: A Production-Oriented LLM Router with Hybrid Offline–Online Learning \- arXiv, [https://arxiv.org/html/2605.30736v1](https://arxiv.org/html/2605.30736v1)  
10. Context Compaction – Inside Claude Code \- GitHub Pages, [https://y-agent.github.io/inside-claude-code/04-context-compaction.html](https://y-agent.github.io/inside-claude-code/04-context-compaction.html)  
11. Software 3.0 Explained: Why Karpathy Says the Context Window Is Your New RAM, [https://www.mindstudio.ai/blog/software-3-0-explained-karpathy-context-window-ram-model-weights-cpu](https://www.mindstudio.ai/blog/software-3-0-explained-karpathy-context-window-ram-model-weights-cpu)  
12. Software 3.0: Redefining the Foundations of Programming | by Christos Theodoropoulos | Data Science Collective | Medium, [https://medium.com/data-science-collective/software-3-0-redefining-the-foundations-of-programming-409cf24e6c96](https://medium.com/data-science-collective/software-3-0-redefining-the-foundations-of-programming-409cf24e6c96)  
13. Spec-Driven Development: A Spec-First Approach to AI-Native Engineering, [https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering)  
14. Spec-Driven Development for AI Agents, Done Right: Specs as Governed Artifacts, [https://www.truefoundry.com/blog/spec-driven-development-ai-agents](https://www.truefoundry.com/blog/spec-driven-development-ai-agents)  
15. AI Agent Evaluation: Building an Evaluation Platform That Scales \- Legion Intelligence, [https://www.legionintel.com/command-papers/ai-agent-evaluation-building-an-evaluation-platform-that-scales](https://www.legionintel.com/command-papers/ai-agent-evaluation-building-an-evaluation-platform-that-scales)  
16. Semantic-Aware Intelligent Request Routing in Multi-Model LLM Backend Gateways, [https://www.researchgate.net/publication/405186829\_Semantic-Aware\_Intelligent\_Request\_Routing\_in\_Multi-Model\_LLM\_Backend\_Gateways](https://www.researchgate.net/publication/405186829_Semantic-Aware_Intelligent_Request_Routing_in_Multi-Model_LLM_Backend_Gateways)  
17. Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation, [https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI\_MCP\_SECURITY.pdf?ver=bmgiSbNQLP6Z\_GiWtRt6bg%3D%3D](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf?ver=bmgiSbNQLP6Z_GiWtRt6bg%3D%3D)  
18. Daily Papers \- Hugging Face, [https://huggingface.co/papers?q=Model%20Context%20Protocol%20(MCP)](https://huggingface.co/papers?q=Model+Context+Protocol+\(MCP\))  
19. Model Context Protocol (MCP) explained: A practical technical overview for developers and architects \- CodiLime, [https://codilime.com/blog/model-context-protocol-explained/](https://codilime.com/blog/model-context-protocol-explained/)  
20. A Survey of Agent Interoperability Protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP) \- arXiv, [https://arxiv.org/html/2505.02279v2](https://arxiv.org/html/2505.02279v2)  
21. Agents at Scale: Multi-Agent Architecture with A2A Protocol on Agent Runtime and ADK Integration | Google Codelabs, [https://codelabs.developers.google.com/adk-a2a-agent-runtime](https://codelabs.developers.google.com/adk-a2a-agent-runtime)  
22. Agent2Agent (A2A) is an open protocol enabling communication and interoperability between opaque agentic applications. \- GitHub, [https://github.com/a2aproject/A2A](https://github.com/a2aproject/A2A)  
23. Evaluating AI agents for production: A practical guide to Strands Evals \- AWS, [https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-for-production-a-practical-guide-to-strands-evals/](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-for-production-a-practical-guide-to-strands-evals/)  
24. LangGraph vs CrewAI vs OpenAI Agents SDK: Choosing Your Agent Framework in 2026, [https://particula.tech/blog/langgraph-vs-crewai-vs-openai-agents-sdk-2026](https://particula.tech/blog/langgraph-vs-crewai-vs-openai-agents-sdk-2026)  
25. AI Agent Frameworks Compared: LangGraph vs CrewAI vs AutoGen (2026) \- PE Collective, [https://pecollective.com/blog/ai-agent-frameworks-compared/](https://pecollective.com/blog/ai-agent-frameworks-compared/)  
26. Agentic AI Frameworks 2026: LangGraph vs CrewAI vs OpenAI SDK | Uvik Software, [https://uvik.net/blog/agentic-ai-frameworks/](https://uvik.net/blog/agentic-ai-frameworks/)  
27. AI Agent Frameworks 2026: The Complete Guide, [https://arahi.ai/blog/ai-agent-frameworks](https://arahi.ai/blog/ai-agent-frameworks)  
28. openai/openai-agents-python: A lightweight, powerful framework for multi-agent workflows \- GitHub, [https://github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)  
29. Agents SDK | OpenAI API, [https://developers.openai.com/api/docs/guides/agents](https://developers.openai.com/api/docs/guides/agents)  
30. OpenAI Agents SDK \- Braintrust, [https://www.braintrust.dev/docs/integrations/agent-frameworks/openai-agents-sdk](https://www.braintrust.dev/docs/integrations/agent-frameworks/openai-agents-sdk)  
31. Best Agentic Framework in 2026? After testing a few, here's where I've landed. \- Reddit, [https://www.reddit.com/r/LangChain/comments/1u23197/best\_agentic\_framework\_in\_2026\_after\_testing\_a/](https://www.reddit.com/r/LangChain/comments/1u23197/best_agentic_framework_in_2026_after_testing_a/)  
32. Google ADK, [https://adk.dev/](https://adk.dev/)  
33. GitHub \- google/adk-js: An open-source, code-first Typescript toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control., [https://github.com/google/adk-js](https://github.com/google/adk-js)  
34. Developer's Guide to AI Agent Protocols, [https://developers.googleblog.com/developers-guide-to-ai-agent-protocols/](https://developers.googleblog.com/developers-guide-to-ai-agent-protocols/)  
35. JSON schemas | Agent Registry \- Google Cloud Documentation, [https://docs.cloud.google.com/agent-registry/json-schemas](https://docs.cloud.google.com/agent-registry/json-schemas)  
36. Codex AGENTS.md Explained: How Team Instructions Work \- Verdent Guides, [https://www.verdent.ai/guides/codex-agents-md-explained](https://www.verdent.ai/guides/codex-agents-md-explained)  
37. Customization – Codex \- OpenAI Developers, [https://developers.openai.com/codex/concepts/customization](https://developers.openai.com/codex/concepts/customization)  
38. codex-agents | Skills Marketplace \- LobeHub, [https://lobehub.com/skills/thealexyao-openclaw-codex-agents-codex-agents](https://lobehub.com/skills/thealexyao-openclaw-codex-agents-codex-agents)  
39. Context Engineering: Complete 2026 Field Guide for AI Developers \- Taskade, [https://www.taskade.com/blog/context-engineering](https://www.taskade.com/blog/context-engineering)  
40. Deep dive into context engineering for AI agents | by clara | May, 2026 | Code Like A Girl, [https://code.likeagirl.io/deep-dive-into-context-engineering-for-ai-agents-584bf3e578df](https://code.likeagirl.io/deep-dive-into-context-engineering-for-ai-agents-584bf3e578df)  
41. Online Multi-LLM Selection via Contextual Bandits Under Unstructured Context Evolution | Proceedings of the AAAI Conference on Artificial Intelligence, [https://ojs.aaai.org/index.php/AAAI/article/view/39672](https://ojs.aaai.org/index.php/AAAI/article/view/39672)  
42. Adaptive LLM Routing under Budget Constraints \- arXiv, [https://arxiv.org/html/2508.21141v1](https://arxiv.org/html/2508.21141v1)  
43. Thompson Sampling for LLM Routing: Why Your Model Selection Should Be Probabilistic, [https://kalibr.systems/blog/thompson-sampling-llm-routing](https://kalibr.systems/blog/thompson-sampling-llm-routing)  
44. What Are MCP Resources? Model Context Protocol Explained \- Zuplo, [https://zuplo.com/blog/mcp-resources](https://zuplo.com/blog/mcp-resources)  
45. Agent Memory: Why Your AI Has Amnesia and How to Fix It | developers \- Oracle Blogs, [https://blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia-and-how-to-fix-it](https://blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia-and-how-to-fix-it)  
46. From context to dreams: architecting memory for AI agents \- Red Hat Emerging Technologies, [https://next.redhat.com/2026/06/01/from-context-to-dreams-architecting-memory-for-ai-agents/](https://next.redhat.com/2026/06/01/from-context-to-dreams-architecting-memory-for-ai-agents/)  
47. Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers, [https://arxiv.org/html/2603.07670v1](https://arxiv.org/html/2603.07670v1)  
48. MCP Server Best Practices for 2026: Secure, Scalable, Simple \- CData Software, [https://www.cdata.com/blog/mcp-server-best-practices-2026](https://www.cdata.com/blog/mcp-server-best-practices-2026)  
49. Model Context Protocol: Security Risks & Mitigations \- SOC Prime, [https://socprime.com/blog/mcp-security-risks-and-mitigations/](https://socprime.com/blog/mcp-security-risks-and-mitigations/)  
50. MCP Security Best Practices: The Complete 2026 Guide, [https://obot.ai/resources/learning-center/mcp-security/](https://obot.ai/resources/learning-center/mcp-security/)  
51. Why Smart Developers Are Ditching RAG for Context Engineering | by Faisal haque | Apr, 2026 | Artificial Intelligence in Plain English, [https://ai.plainenglish.io/why-smart-developers-are-ditching-rag-for-context-engineering-3659ef42f19d](https://ai.plainenglish.io/why-smart-developers-are-ditching-rag-for-context-engineering-3659ef42f19d)  
52. SPARK: Search Personalization via Agent-Driven Retrieval and Knowledge-sharing \- arXiv, [https://arxiv.org/html/2512.24008v3](https://arxiv.org/html/2512.24008v3)  
53. Long Context Compaction for AI Agents — Part 1: Design Principles | by Kihyeon Myung, [https://pub.towardsai.net/long-context-compaction-for-ai-agents-part-1-design-principles-2bf4a5748154](https://pub.towardsai.net/long-context-compaction-for-ai-agents-part-1-design-principles-2bf4a5748154)  
54. Context engineering: memory, compaction, and tool clearing | Claude Cookbook, [https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)  
55. Context Compression in AI Agents: Hermes vs. Claude Code \- Mem0, [https://mem0.ai/blog/how-hermes-and-claude-handle-context-compression-in-real-production-agents-(and-what-you-should-extract)](https://mem0.ai/blog/how-hermes-and-claude-handle-context-compression-in-real-production-agents-\(and-what-you-should-extract\))  
56. How Compaction Works in Hermes Agent \- DEV Community, [https://dev.to/john\_lingi\_f754bc63dd9ff1/how-compaction-works-in-hermes-agent-2m0m](https://dev.to/john_lingi_f754bc63dd9ff1/how-compaction-works-in-hermes-agent-2m0m)  
57. Automatic context compaction | Claude Cookbook, [https://platform.claude.com/cookbook/tool-use-automatic-context-compaction](https://platform.claude.com/cookbook/tool-use-automatic-context-compaction)  
58. Tools \- Model Context Protocol, [https://modelcontextprotocol.io/specification/draft/server/tools](https://modelcontextprotocol.io/specification/draft/server/tools)  
59. Reduce Token Cost for LLMs: AI Agent Memory with Valkey and Mem0, [https://valkey.io/blog/ai-agent-memory-with-valkey-and-mem0/](https://valkey.io/blog/ai-agent-memory-with-valkey-and-mem0/)  
60. AI model benchmarks 2026: GPT, Claude, Gemini compared \- Logic, [https://logic.inc/resources/ai-model-benchmarks-guide](https://logic.inc/resources/ai-model-benchmarks-guide)  
61. Tools \- Model Context Protocol, [https://modelcontextprotocol.io/specification/2025-11-25/server/tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)  
62. ClawRoute Technical Architecture: How Smart Model Routing Works \- DEV Community, [https://dev.to/mrjhsn/clawroute-technical-architecture-how-smart-model-routing-works-13h2](https://dev.to/mrjhsn/clawroute-technical-architecture-how-smart-model-routing-works-13h2)  
63. DMPO: Direct Multi-Turn Preference Optimization \- Emergent Mind, [https://www.emergentmind.com/topics/direct-multi-turn-preference-optimization-dmpo](https://www.emergentmind.com/topics/direct-multi-turn-preference-optimization-dmpo)  
64. TPMM-DPO: Trajectory-aware Preference-guided Model Merging for Iterative Direct Preference Optimization \- arXiv, [https://arxiv.org/pdf/2605.23398](https://arxiv.org/pdf/2605.23398)  
65. 10 Best Local AI Assistants in 2026 \- Vellum, [https://www.vellum.ai/blog/best-local-ai-assistants](https://www.vellum.ai/blog/best-local-ai-assistants)  
66. msb-msb/awesome-local-ai: A curated list of resources for running AI locally on consumer hardware \- GitHub, [https://github.com/msb-msb/awesome-local-ai](https://github.com/msb-msb/awesome-local-ai)