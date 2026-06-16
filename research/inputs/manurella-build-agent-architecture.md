# **State-of-the-Art Sub-Agent Architecture for the Manurella Build Domain**

The paradigm of software engineering is undergoing a fundamental transition from human-driven, AI-assisted development to highly autonomous, repository-level execution ecosystems. The Manurella Agentic Framework is designed to operate as a runtime-agnostic orchestration layer that significantly elevates the performance of weaker, non-frontier Small Language Models (SLMs) through controlled context, strict evaluation rubrics, and the Model Context Protocol (MCP). While the initial runtime target is Kilo Code, the architectural topology must remain entirely portable across diverse host environments, including Codex, ChatGPT, Gemini, and bespoke Python/MCP tooling infrastructures1.  
This report details the foundational v0 sub-agent architecture for the Manurella Build domain. It provides an exhaustive mapping of competencies, defines the rigid boundaries between top-level and internal sub-agents, establishes strict context engineering protocols, and outlines an optimization strategy designed specifically for the cognitive limitations of 7B-32B parameter models.

## **1\. Critique of Alternative Decompositions**

The design of the Manurella sub-agent architecture relies heavily on empirical evidence derived from the failures and successes of preceding multi-agent systems (MAS) and monolithic agents across industry benchmarks such as SWE-bench Verified and SWE-EVO3. Distinguishing between proven empirical evidence, project experience, architectural hypotheses, and future speculation is critical for establishing a resilient v0 baseline.

### **1.1 The Failure of Flat Multi-Agent Systems (Evidence)**

Early agentic paradigms defaulted to "flat" multi-agent teams where diverse personas (e.g., a "QA Agent" and a "Developer Agent") collaborated in unstructured, peer-to-peer dialogues. Empirical evidence indicates that flat architectures degrade as task complexity scales6. In flat systems, responsibility is blurred, creating a structural bias where agents reaffirm each other's hallucinations rather than verifying them6. Furthermore, peer-to-peer interactions incur ![][image1] communication complexity, leading to severe token exhaustion and cognitive overload for the underlying models7.

### **1.2 Limitations of Monolithic Agents (Evidence)**

Conversely, single-agent architectures (e.g., early iterations of SWE-agent) equip one monolithic model with a vast Agent-Computer Interface (ACI), providing access to file navigation, Bash execution, and text editing simultaneously8. While highly effective for localized, single-file bug fixes, these systems suffer from context dilution on multi-file, repository-level tasks5. Evidence from Claude 3.5 Sonnet and GPT-4o deployments reveals that monolithic agents frequently lose sight of the overarching architectural intent because their context windows become polluted with intermediate Bash outputs and grep results.

### **1.3 The Hierarchical Supervisor-Worker Topology (Hypothesis)**

Based on the limitations of flat and monolithic designs, the core architectural hypothesis for the Manurella Build domain is that a **Hierarchical Supervisor-Worker Topology** will yield the highest success rate, particularly for weaker models. This approach, supported by findings in Agentless and AgentOrchestra architectures, strictly separates strategy from execution6. A meta-agent or supervisor holds the strategic context, while ephemeral worker agents execute narrow, bounded tasks without the ability to make global system decisions6. This ![][image2] layered coordination is essential for isolating task state and forcing intermediate verification7.

## **2\. Mapping the Major Competencies in Modern Software Building**

Modern software building requires diverse competencies ranging from high-level system design to low-level execution and deployment. To facilitate a robust sub-agent decomposition, these competencies must be mapped into discrete operational domains that an AI agent can reliably process.

| Competency Domain | Build Domain Scope Covered | Architectural Implementation Strategy |
| :---- | :---- | :---- |
| **System Design & Planning** | Product planning, architecture, database/API design | Handled by top-level planning agents. Produces structured .kilo/plans/ artifacts and high-level markdown specifications13. |
| **Code Synthesis & Evolution** | Frontend, backend, refactoring | Handled by highly constrained editor sub-agents that manipulate Abstract Syntax Trees (ASTs) or apply strict unified diffs9. |
| **Verification & Quality** | QA, unit/integration testing, debugging | Handled by isolated execution-verifier sub-agents running inside sandboxed Docker environments to provide execution-grounded feedback14. |
| **Auditing & Standards** | Security, code review, performance profiling | Handled by critic sub-agents that utilize static analysis tools, linters, and adaptive rubrics to assess non-functional requirements16. |
| **Operations & Delivery** | DevOps, CI/CD, observability, release workflows, documentation | Handled by orchestrators interacting with external MCP servers (e.g., GitHub, GitLab, Jira) to manage state outside the codebase18. |

## **3\. The v0 Sub-Agent Decomposition: Top-Level vs. Internal**

The Manurella architecture enforces a strict bifurcation between **Top-Level Selectable Agents** and **Internal Sub-Agents**.  
**Top-Level Selectable Agents** are personas explicitly chosen by the user (or a routing layer) at the initiation of a session. They act as state managers, session owners, and supervisors. They maintain the semantic intent of the user's request, hold the long-term context, and manage the branching logic. However, they are fundamentally restricted from performing direct codebase execution.  
**Internal Sub-Agents** are hidden, stateless worker nodes invoked exclusively by top-level agents. They are spun up to execute a specific, isolated task (e.g., "Find the file containing the database connection pool" or "Run the test suite and extract the stack trace") and return a deterministic output before terminating.  
This separation prevents the supervisor from experiencing cognitive overload and ensures that weaker models are only tasked with one specific cognitive operation at a time.

### **3.1 Top-Level Selectable Agents**

#### **3.1.1 The Architect (Planner)**

| Attribute | Definition |
| :---- | :---- |
| **Purpose** | Translates ambiguous user requirements into concrete system designs, data models, and step-by-step implementation plans13. |
| **Use-When Boundary** | Activated for product planning, architecture decisions, database/API schema design, and generating initial project scaffolds. |
| **Do-Not-Use Boundary** | Must not be used for writing production code, executing tests, or modifying active application logic. |
| **Required Context** | User query, overarching business constraints, existing .kilo/plans/ directory, and enterprise architectural standards. |
| **Tools/Permissions** | File creation restricted to plan directories, MCP resources for reading external docs (e.g., Confluence, Jira)18, Sequential Thinking server. |
| **Output Contract** | Structured markdown specifications (e.g., requirement.md, design.md, tasks.md) detailing the exact sub-goals required for implementation19. |
| **Evaluation Rubric** | Completeness (Are all user constraints addressed?), Orthogonality (Are components properly decoupled?), and Feasibility (Can the design be implemented within the selected tech stack?). |
| **Common Failure Modes** | Over-engineering, failing to specify data contracts between frontend and backend, and ignoring existing repository conventions. |

The Architect operates entirely in the abstract domain. Empirical observations indicate that allowing a model to plan and code simultaneously results in premature convergence, where the agent begins writing code before understanding the full dependency graph. By forcing the Architect to output a verified markdown plan, the system establishes a ground truth that subsequent agents can be evaluated against.

#### **3.1.2 The Orchestrator (Developer)**

| Attribute | Definition |
| :---- | :---- |
| **Purpose** | Acts as the primary workflow coordinator for feature implementation, refactoring, and DevOps tasks. It delegates tasks to internal sub-agents to achieve the goals defined by the Architect13. |
| **Use-When Boundary** | Activated for writing frontend/backend features, executing refactors, modifying CI/CD pipelines, and writing documentation. |
| **Do-Not-Use Boundary** | Strictly prohibited from editing source code or running Bash commands directly. It must invoke internal sub-agents. |
| **Required Context** | The active task from tasks.md, user constraints, repository structure, and AGENTS.md coding rules19. |
| **Tools/Permissions** | Sub-agent invocation (Localizer, Editor, Verifier, Critic), task-state management, Sequential Thinking MCP server for strategic branching21. |
| **Output Contract** | A finalized, passing Git commit or a structured failure trajectory indicating exhausted avenues. |
| **Evaluation Rubric** | Goal Success Rate (Did the final state meet the intent?), Trajectory Efficiency (Were sub-agents used logically?), and Error Recovery Rate23. |
| **Common Failure Modes** | Sycophancy (accepting a failing sub-agent result without pushing back), infinite looping on unresolvable tasks, and context drift over long horizons24. |

The Orchestrator is the backbone of the Manurella execution engine. By stripping the Orchestrator of the ability to edit files directly, the architecture eliminates the risk of accidental codebase corruption caused by a hallucinating supervisor. The Orchestrator relies entirely on the Sequential Thinking MCP server to explicitly declare its scope, evaluate branches, and manage state22.

#### **3.1.3 The Explorer (Debugger/Observability)**

| Attribute | Definition |
| :---- | :---- |
| **Purpose** | A read-only diagnostic persona focused on answering technical questions, tracing logic flows, and analyzing observability/telemetry data13. |
| **Use-When Boundary** | Activated for debugging production issues, code review comprehension, analyzing performance bottlenecks, and general codebase Q\&A. |
| **Do-Not-Use Boundary** | Must not propose or implement codebase modifications. All write operations to the repository are blocked. |
| **Required Context** | User query, application logs, stack traces, and localized code chunks. |
| **Tools/Permissions** | search\_dir, grep, read\_file, MCP integrations for observability platforms (e.g., Sentry, AppSignal)26, and read-only Bash. |
| **Output Contract** | A detailed analytical report identifying root causes, logic flaws, or system behaviors, complete with exact line-number citations. |
| **Evaluation Rubric** | Factual Accuracy (Are the citations real?), Depth of Analysis, and Relevance to the queried issue. |
| **Common Failure Modes** | Hallucinating connections between unrelated microservices, failure to navigate deep directory structures, and misinterpreting stale log data. |

### **3.2 Internal Sub-Agents (Workers)**

#### **3.2.1 The Localizer**

| Attribute | Definition |
| :---- | :---- |
| **Purpose** | Navigates the repository to isolate the exact files, classes, and line numbers relevant to the Orchestrator's objective, preventing context bloat for the Editor10. |
| **Use-When Boundary** | Invoked whenever the system must determine *where* a modification belongs or *how* a specific dependency operates. |
| **Do-Not-Use Boundary** | Strictly read-only. Cannot generate code or run tests. |
| **Required Context** | The specific task description and the file system structure. |
| **Tools/Permissions** | AST parsing tools, find\_file, grep, read\_file\_chunk. |
| **Output Contract** | A structured JSON array of file paths and line ranges required for the task, alongside a brief justification for each9. |
| **Evaluation Rubric** | Top-1 and Top-5 Localization Recall, Precision (avoiding irrelevant files)10. |
| **Common Failure Modes** | Test-file over-prediction (finding the test but not the source), failing to identify cross-file dependencies, and returning overly large code chunks10. |

#### **3.2.2 The Editor**

| Attribute | Definition |
| :---- | :---- |
| **Purpose** | Generates precise, syntactically correct codebase modifications based on the isolated context provided by the Localizer. |
| **Use-When Boundary** | Invoked exclusively after the exact target lines have been localized and verified. |
| **Do-Not-Use Boundary** | Must not explore the repository or run diagnostic commands. It assumes the provided context is complete. |
| **Required Context** | Target file chunks, Orchestrator's task instruction, and relevant SKILL.md syntax rules20. |
| **Tools/Permissions** | apply\_diff, str\_replace, create\_file9. |
| **Output Contract** | A unified diff or structured replacement block that applies cleanly to the codebase. |
| **Evaluation Rubric** | Diff Applicability Rate (Does the patch apply cleanly?) and Syntax Correctness29. |
| **Common Failure Modes** | Indentation errors (critical in Python), hallucinating variables outside the provided chunk, and deleting adjacent required logic. |

#### **3.2.3 The Verifier**

| Attribute | Definition |
| :---- | :---- |
| **Purpose** | Implements execution-grounded verification. It applies the Editor's patch in a sandbox, executes unit/integration tests, and parses the output14. |
| **Use-When Boundary** | Invoked after every code modification before control returns to the Orchestrator. |
| **Do-Not-Use Boundary** | Must not attempt to write fixes or edit code. |
| **Required Context** | The task requirements, testing framework conventions, and the bash environment state. |
| **Tools/Permissions** | Sandboxed Bash, run\_tests, container execution capabilities. |
| **Output Contract** | A deterministic Pass/Fail boolean and a heavily truncated, highly specific error log or stack trace if the execution failed15. |
| **Evaluation Rubric** | False Positive Rate (Passing broken code) and Signal-to-Noise Ratio (Truncating verbose logs effectively). |
| **Common Failure Modes** | Testing the wrong module, failing to install requisite environment dependencies, and hallucinating success based on a silent failure31. |

#### **3.2.4 The Critic**

| Attribute | Definition |
| :---- | :---- |
| **Purpose** | Audits proposed diffs against non-functional requirements including security vulnerabilities, performance regressions, and style guidelines16. |
| **Use-When Boundary** | Invoked in parallel with the Verifier or prior to finalize a task to ensure production readiness. |
| **Do-Not-Use Boundary** | Does not assess functional correctness. |
| **Required Context** | The proposed diff, coding-rules.md, and relevant security SKILL.md guidelines19. |
| **Tools/Permissions** | Static analysis integration, linter execution, Sequential Thinking server for deep risk assessment32. |
| **Output Contract** | A structured array of specific violations with line numbers or a definitive "Approval." |
| **Evaluation Rubric** | Adherence to predefined static rubrics and false-positive identification rates17. |
| **Common Failure Modes** | Pedantic looping (rejecting valid code for trivial aesthetic reasons) and conflicting with the Verifier's requirements. |

## **4\. Context Engineering and Memory Management**

A foundational hypothesis of the Manurella framework is that context exhaustion is the primary failure mode of LLM-based software agents. Weaker models, in particular, degrade rapidly when exposed to append-only memory logs or excessive repository noise33. Context engineering is therefore treated as a core architectural discipline, categorized into three strict tiers34.

### **4.1 Always-On Prompt (The System Backbone)**

The Always-On Prompt is the immutable payload provided to the agent at every inference step.

* **Identification:** It defines the agent's exact persona (e.g., "You are the Localizer").  
* **Format:** It mandates the strict JSON-RPC or XML structure required for tool invocation and output generation35.  
* **Exclusions:** It explicitly *must not* contain project documentation, large API references, or full file contents. It is structurally rigid to enforce behavioral compliance.

### **4.2 Reference Material (Progressive Disclosure)**

Reference materials inject domain expertise dynamically utilizing the open format SKILL.md specification28.

* **Mechanism:** At session startup, the Orchestrator is presented only with Level 1 metadata (Skill names and one-sentence descriptions) for all installed capabilities (e.g., react-hooks-refactoring, aws-deployment)20.  
* **Invocation:** If the user requests a database migration, the Orchestrator identifies the semantic match and retrieves the specific database-migration skill. This loads Level 2 (markdown instructions) and Level 3 (bundled python scripts or JSON templates) directly into the active context window20.  
* **Project Conventions:** Global rules, such as indentation standards or continuous integration constraints, are stored in AGENTS.md or coding-rules.md and are referenced globally without bloating the Always-On prompt19.

### **4.3 Retrieved Context (Ephemeral State)**

Retrieved context represents data that is actively fetched, utilized for a specific step, and subsequently summarized or discarded.

* **Mechanism:** This includes file chunks fetched by the Localizer, truncated test logs generated by the Verifier, and data fetched via external MCP servers (e.g., reading a Slack thread or a Jira ticket)1.  
* **Pruning:** Raw execution logs are never appended blindly to the ongoing conversational history. The Verifier must compress standard error outputs into semantic summaries before returning state to the Orchestrator, thereby preserving the token budget and protecting the model's reasoning capabilities31.

## **5\. Optimizing for Weaker and Non-Frontier Models**

The Manurella framework is specifically engineered to elevate the performance of Small Language Models (SLMs) in the 1B to 32B parameter range (e.g., Qwen-2.5-7B, Llama-3-8B, GLM-5). While these models offer significant advantages in latency, cost predictability, and edge-deployment capabilities, they suffer from degraded long-horizon reasoning and a propensity for context collapse39. The architecture mitigates these weaknesses through structural scaffolding.

### **5.1 Elimination of Unaided Self-Correction**

Research emphatically demonstrates that prompting an SLM to natively "reflect" on its own generated code without external stimuli is counterproductive15. An SLM cannot identify its own logical flaws merely by re-reading its output. Therefore, the Manurella framework relies exclusively on **Execution-Grounded Verification**14. The model generates a patch, the Verifier compiles or tests it, and the resulting stack trace is fed back to the model. The SLM is not reflecting; it is reacting to novel, objective diagnostic data, effectively turning a generative task into a concrete repair loop15.

### **5.2 The Sequential Thinking MCP Server**

To prevent SLMs from falling into "tunnel vision" (repeatedly executing the same failing Bash command) or sycophancy, the Orchestrator and Planner agents are required to interface with a Sequential Thinking MCP server21.

* **Structured Cognition:** Rather than allowing the LLM to generate an unstructured, rambling chain-of-thought, the model must invoke the process\_thought tool with specific parameters: thought\_number, total\_thoughts, stage (e.g., Problem Definition, Research, Analysis), and is\_revision21.  
* **Branching and Backtracking:** If an approach fails execution testing, the model is guided to use the branch\_from\_thought parameter. This makes the cognitive fork explicit and prevents the model from silently dropping context22.  
* **Supervisory Guards:** The MCP server operates as an external supervisor. If the model attempts to declare a task complete (next\_thought\_needed: false) before satisfying the original requirements, or if it exceeds its allotted thought budget without reaching a conclusion, the server intercepts the output and returns a warning prompt, forcing the SLM to re-evaluate24.

### **5.3 Constrained Agent-Computer Interfaces (ACI)**

SLMs struggle heavily with complex tool schemas and ambiguous terminal environments. The ACI must be severely constrained9. Instead of a generic execute\_command tool that allows an SLM to hallucinate dangerous or syntactically invalid bash scripts, the tools are highly specialized: run\_pytest\_on\_file, search\_exact\_string, replace\_lines. This drastically reduces the probability of syntax errors in the tool-calling layer9.

## **6\. Evaluation Rubrics and Benchmark Integration**

Evaluating agent performance in the Build domain using traditional reference-based metrics (e.g., BLEU, ROUGE) is fundamentally flawed, as these metrics measure surface-level string overlap and are blind to goal-directed reasoning and functional correctness17. To ensure reliability, Manurella utilizes domain-specific **Adaptive Rubrics** and standardized benchmark tasks.

### **6.1 Adaptive Rubric-Based Evaluation**

The framework leverages dynamic, task-specific rubrics to evaluate internal outputs, similar to the LLM-as-a-Judge paradigm but rigidly constrained46.

* **Mechanism:** When the Critic evaluates the Editor's code, it does not use a generic "helpfulness" prompt. The rubric generation service analyzes the initial requirement and generates verifiable, orthogonal dimensions45.  
* **Example Rubric:**  
  1. *Correctness (Execution):* Does the code pass the Verifier's unit test? (Deterministic Pass/Fail).  
  2. *Minimalism (Static):* Does the patch avoid modifying logic outside the requested scope? (Scored 1-5).  
  3. *Style Adherence (Static):* Does the code comply with the dependency injection patterns defined in AGENTS.md? (Scored 1-5)47.  
* By ensuring the criteria are measurable and independent, the system prevents a minor stylistic error from masking a functionally perfect implementation17.

### **6.2 Proposed Benchmark Tasks per Sub-Agent**

To empirically validate the architecture, each sub-agent must be tested against isolated sub-benchmarks derived from industry standards:

| Sub-Agent | Benchmark Target | Evaluation Metric |
| :---- | :---- | :---- |
| **Orchestrator** | *Terminal-Bench 2.0*, *SWE-bench Pro* \[cite: 10, 48\] | End-to-end task resolution rate, Trajectory Efficiency (token expenditure per successful state change). |
| **Localizer** | *SWE-bench Lite* (Retrieval Subset)4 | Top-1 and Top-5 File/Line Localization Recall and Precision (Micro-F1 score)10. |
| **Editor** | *HumanEvalFix*, *RepoExec* \[cite: 9, 31\] | Diff Applicability Rate, Syntax Compilation Success Rate, Pass@1 with exact localization provided29. |
| **Verifier** | Synthetic Bug Injection Dataset | False Positive Rate (passing broken code), Signal-to-Noise Ratio (ability to truncate error logs accurately)16. |
| **Architect** | *SWE-EVO* (Multi-step modification planning)5 | Plan Completeness, Semantic similarity to ground-truth architectural design decisions. |

## **7\. The Expansion Path (v0, v1, and v2)**

The Manurella architecture is designed to evolve progressively from tightly constrained, tool-augmented pipelines to fully autonomous, self-optimizing ecosystems3.

### **7.1 v0: Tool-Augmented Strict Pipeline**

* **Topology:** Rigid, single-threaded execution. The Orchestrator calls the Localizer, waits for the result, passes context to the Editor, and finally calls the Verifier.  
* **Focus:** Perfecting the Agent-Computer Interface (ACI), stabilizing the execution-grounded verification loop, and ensuring SLMs can reliably interact with the Sequential Thinking MCP server9.  
* **Capability:** Capable of resolving discrete, well-scoped GitHub issues (equivalent to SWE-bench Lite) and acting as a highly reliable coding assistant within a local IDE (e.g., Kilo Code CLI)4.

### **7.2 v1: Hierarchical Multi-Agent Teams**

* **Topology:** Parallel sub-agent execution and dynamic delegation. The Orchestrator can spin up multiple Localizer instances simultaneously to explore different subsystems (Domain-scoped parallel exploration)10.  
* **Focus:** Integration of advanced MCP servers for external system connectivity (e.g., Jira, Confluence, CI/CD pipelines) to manage state outside the local repository1. State management transitions from local context windows to persistent, graph-based memory structures51.  
* **Capability:** Autonomous feature implementation from high-level product specification documents to finalized pull requests, managing multi-file dependencies and repository-wide refactoring workflows3.

### **7.3 v2: Self-Evolving Ecosystems via Meta Context Engineering**

* **Topology:** Dynamic agent spawning and self-modifying context parameters.  
* **Focus:** Implementing Meta Context Engineering (MCE). The architecture introduces a bi-level optimization framework where a "meta-agent" monitors the historical success and failure trajectories of the internal sub-agents34. If the Editor consistently fails to correctly implement React hooks, the meta-agent dynamically rewrites the react-hooks SKILL.md file, evolving the system's operational instructions over time based on actual performance data28.  
* **Capability:** The system adapts to proprietary, undocumented enterprise codebases entirely on its own. It generates its own evaluation rubrics, synthesizes its own domain-specific skills, and continuously optimizes its pipeline without human intervention, representing a shift toward true open-ended evolution51.

#### **Works cited**

1. Model Context Protocol architecture patterns for multi-agent AI systems \- IBM Developer, [https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems/](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems/)  
2. What is the Model Context Protocol (MCP)? \- Model Context Protocol, [https://modelcontextprotocol.io/docs/getting-started/intro](https://modelcontextprotocol.io/docs/getting-started/intro)  
3. How AI Agents Are Fundamentally Restructuring the Software Paradigm \- arXiv, [https://arxiv.org/html/2606.05608](https://arxiv.org/html/2606.05608)  
4. SGAgent: Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair \- arXiv, [https://arxiv.org/html/2602.23647v2](https://arxiv.org/html/2602.23647v2)  
5. SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios, [https://arxiv.org/html/2512.18470v5](https://arxiv.org/html/2512.18470v5)  
6. AgentOrchestra Explained: A Mental Model for Hierarchical Multi-Agent Systems \- Medium, [https://medium.com/@phoenixarjun007/agentorchestra-explained-a-mental-model-for-hierarchical-multi-agent-systems-c8985d083115](https://medium.com/@phoenixarjun007/agentorchestra-explained-a-mental-model-for-hierarchical-multi-agent-systems-c8985d083115)  
7. AgentOrchestra: Orchestrating Hierarchical Multi-Agent Intelligence with the Tool-Environment-Agent (TEA) Protocol | OpenReview, [https://openreview.net/forum?id=YcnKdeI9pp](https://openreview.net/forum?id=YcnKdeI9pp)  
8. Getting Up to Speed on Multi-Agent Systems, Part 1: The Landscape, [https://christophermeiklejohn.com/ai/agents/mas-series/2026/04/24/mas-series-01-the-landscape.html](https://christophermeiklejohn.com/ai/agents/mas-series/2026/04/24/mas-series-01-the-landscape.html)  
9. SWE-Agent Frameworks Overview \- Emergent Mind, [https://www.emergentmind.com/topics/swe-agent-frameworks](https://www.emergentmind.com/topics/swe-agent-frameworks)  
10. Exploration Structure in LLM Agents for Multi‑File Change Localization \- arXiv, [https://arxiv.org/html/2606.11976v1](https://arxiv.org/html/2606.11976v1)  
11. LLM-Based Agents in Software Engineering \- Emergent Mind, [https://www.emergentmind.com/topics/llm-based-agents-in-software-engineering](https://www.emergentmind.com/topics/llm-based-agents-in-software-engineering)  
12. What are Hierarchical AI Agents? \- IBM, [https://www.ibm.com/think/topics/hierarchical-ai-agents](https://www.ibm.com/think/topics/hierarchical-ai-agents)  
13. Using Agents \- Kilo Code, [https://kilo.ai/docs/code-with-ai/agents/using-agents](https://kilo.ai/docs/code-with-ai/agents/using-agents)  
14. MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution \- ResearchGate, [https://www.researchgate.net/publication/397202014\_MAGIS\_LLM-Based\_Multi-Agent\_Framework\_for\_GitHub\_Issue\_Resolution](https://www.researchgate.net/publication/397202014_MAGIS_LLM-Based_Multi-Agent_Framework_for_GitHub_Issue_Resolution)  
15. The Research on LLM Self-Correction \- Vadim's blog, [https://vadim.blog/the-research-on-llm-self-correction](https://vadim.blog/the-research-on-llm-self-correction)  
16. Helping LLMs improve code generation using feedback from testing and static analysis, [https://www.researchgate.net/publication/401605311\_Helping\_LLMs\_improve\_code\_generation\_using\_feedback\_from\_testing\_and\_static\_analysis](https://www.researchgate.net/publication/401605311_Helping_LLMs_improve_code_generation_using_feedback_from_testing_and_static_analysis)  
17. Rubric-Based Evaluations & LLM-as-a-Judge — Methodologies, Biases, and Empirical Validation in Domain-Specific Contexts. | by Adnan Masood, PhD. | Apr, 2026 | Medium, [https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80)  
18. AI Agent Skills to support software architecture, design and development \- GitHub, [https://github.com/odyssey4me/agent-skills](https://github.com/odyssey4me/agent-skills)  
19. Reusable AI agent skills for specification-driven development \- GitHub, [https://github.com/anyoneanderson/agent-skills](https://github.com/anyoneanderson/agent-skills)  
20. Deep Dive SKILL.md (Part 1/2) \- A B Vijay Kumar, [https://abvijaykumar.medium.com/deep-dive-skill-md-part-1-2-09fc9a536996](https://abvijaykumar.medium.com/deep-dive-skill-md-part-1-2-09fc9a536996)  
21. Sequential Thinking \- Awesome MCP Servers, [https://mcpservers.org/servers/arben-adm/mcp-sequential-thinking](https://mcpservers.org/servers/arben-adm/mcp-sequential-thinking)  
22. sequential-thinking | Skills Marketp... \- LobeHub, [https://lobehub.com/skills/mathews-tom-armory-sequential-thinking](https://lobehub.com/skills/mathews-tom-armory-sequential-thinking)  
23. Evaluating AI agents for production: A practical guide to Strands Evals \- AWS, [https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-for-production-a-practical-guide-to-strands-evals/](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-for-production-a-practical-guide-to-strands-evals/)  
24. Sit down and take notes, because I'm about to blow your mind. This shit actually works good asf with Claude Code \- Reddit, [https://www.reddit.com/r/ClaudeCode/comments/1rcvc15/sit\_down\_and\_take\_notes\_because\_im\_about\_to\_blow/](https://www.reddit.com/r/ClaudeCode/comments/1rcvc15/sit_down_and_take_notes_because_im_about_to_blow/)  
25. Multi-Agent AI Architecture: Patterns for Enterprise Development | Augment Code, [https://www.augmentcode.com/guides/multi-agent-ai-architecture-patterns-enterprise](https://www.augmentcode.com/guides/multi-agent-ai-architecture-patterns-enterprise)  
26. Sequential Thinking | MCP Servers \- Claude Code Marketplaces, [https://claudemarketplaces.com/mcp/modelcontextprotocol/servers/sequentialthinking](https://claudemarketplaces.com/mcp/modelcontextprotocol/servers/sequentialthinking)  
27. Exploration Structure in LLM Agents for Multi-File Change Localization \- arXiv, [https://arxiv.org/pdf/2606.11976](https://arxiv.org/pdf/2606.11976)  
28. Agent Skills | Microsoft Learn, [https://learn.microsoft.com/en-us/agent-framework/agents/skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills)  
29. SWE-Llama: Automated Code Repair Models \- Emergent Mind, [https://www.emergentmind.com/topics/swe-llama](https://www.emergentmind.com/topics/swe-llama)  
30. RefAgent: A Multi-agent LLM-based Framework for Automatic Software Refactoring \- arXiv, [https://arxiv.org/html/2511.03153v2](https://arxiv.org/html/2511.03153v2)  
31. HyperAgent: Generalist Software Engineering Agents to Solve Coding Tasks at Scale, [https://openreview.net/forum?id=PZf4RsPMBG](https://openreview.net/forum?id=PZf4RsPMBG)  
32. Sequential Thinking Multi-Agent System (MAS) \- Awesome MCP Servers, [https://mcpservers.org/servers/FradSer/mcp-server-mas-sequential-thinking](https://mcpservers.org/servers/FradSer/mcp-server-mas-sequential-thinking)  
33. Why Context Engineering Is Becoming the Core Infrastructure for Autonomous AI | by Miles K. | May, 2026 | Medium, [https://medium.com/@milesk\_33/why-context-engineering-is-becoming-the-core-infrastructure-for-autonomous-ai-aabb77027bf3](https://medium.com/@milesk_33/why-context-engineering-is-becoming-the-core-infrastructure-for-autonomous-ai-aabb77027bf3)  
34. 1 A conceptual overview of Meta Context Engineering (MCE) in a cartoon style. MCE operates as a bi-level optimization framework where a meta-agent drives skill evolution while a base-agent manages context optimization. \- arXiv, [https://arxiv.org/html/2601.21557v2](https://arxiv.org/html/2601.21557v2)  
35. Sequential Thinking in Claude Code: The 2026 Developer Blueprint \- Decodes Future, [https://www.decodesfuture.com/articles/sequential-thinking-in-claude-code](https://www.decodesfuture.com/articles/sequential-thinking-in-claude-code)  
36. A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System \- arXiv, [https://arxiv.org/html/2510.09721v3](https://arxiv.org/html/2510.09721v3)  
37. The SKILL.md Open Standard — Full Specification (2026) \- Agensi, [https://www.agensi.io/learn/skill-md-specification-open-standard](https://www.agensi.io/learn/skill-md-specification-open-standard)  
38. Mastering AI Agent Skills, [https://www.sohamkamani.com/ai/what-are-ai-agents-and-how-to-make-your-own/](https://www.sohamkamani.com/ai/what-are-ai-agents-and-how-to-make-your-own/)  
39. Small language models (SLMs) vs. large language models (LLMs) \- Invisible Technologies, [https://invisibletech.ai/blog/how-small-language-models-can-outperform-llms](https://invisibletech.ai/blog/how-small-language-models-can-outperform-llms)  
40. The Best Open-Source Small Language Models (SLMs) in 2026 \- BentoML, [https://www.bentoml.com/blog/the-best-open-source-small-language-models](https://www.bentoml.com/blog/the-best-open-source-small-language-models)  
41. Together AI \- Poe, [https://poe.com/togetherai](https://poe.com/togetherai)  
42. Schema | MCP Sequential Thinking Tools \- Glama, [https://glama.ai/mcp/servers/xinzhongyouhai/mcp-sequentialthinking-tools/schema](https://glama.ai/mcp/servers/xinzhongyouhai/mcp-sequentialthinking-tools/schema)  
43. sequentialthinking \- Sequential Thinking MCP Server \- Glama, [https://glama.ai/mcp/servers/zalab-inc/mcp-sequentialthinking/tools/sequentialthinking](https://glama.ai/mcp/servers/zalab-inc/mcp-sequentialthinking/tools/sequentialthinking)  
44. \[2511.22138\] TinyLLM: Evaluation and Optimization of Small Language Models for Agentic Tasks on Edge Devices \- arXiv, [https://arxiv.org/abs/2511.22138](https://arxiv.org/abs/2511.22138)  
45. AdaRubric: Task-Adaptive Rubrics for LLM Agent Evaluation \- arXiv, [https://arxiv.org/html/2603.21362v2](https://arxiv.org/html/2603.21362v2)  
46. Gen AI evaluation service overview | Gemini Enterprise Agent Platform, [https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview)  
47. Data quality and rubrics: how to build trust in your models | Snorkel AI, [https://snorkel.ai/blog/data-quality-and-rubrics-how-to-build-trust-in-your-models/](https://snorkel.ai/blog/data-quality-and-rubrics-how-to-build-trust-in-your-models/)  
48. Best LLMs for Coding in 2026: SWE-bench, HumanEval, and LiveCode Rankings | Onyx AI, [https://onyx.app/insights/best-llms-for-coding-2026](https://onyx.app/insights/best-llms-for-coding-2026)  
49. ICML Poster Nemotron-CORTEXA: Enhancing LLM Agents for Software Engineering Tasks via Improved Localization and Solution Diversity, [https://icml.cc/virtual/2025/poster/44274](https://icml.cc/virtual/2025/poster/44274)  
50. Architecture Overview \- Kilo Code, [https://kilo.ai/docs/contributing/architecture](https://kilo.ai/docs/contributing/architecture)  
51. Meta Context Engineering via Agentic Skill Evolution | Request PDF \- ResearchGate, [https://www.researchgate.net/publication/400237585\_Meta\_Context\_Engineering\_via\_Agentic\_Skill\_Evolution](https://www.researchgate.net/publication/400237585_Meta_Context_Engineering_via_Agentic_Skill_Evolution)  
52. How We Built an Agent That Edits Its Own Instructions \- Vadim's blog, [https://vadim.blog/skill-evolver-research-to-practice](https://vadim.blog/skill-evolver-research-to-practice)  
53. \[2601.21557\] Meta Context Engineering via Agentic Skill Evolution \- arXiv, [https://arxiv.org/abs/2601.21557](https://arxiv.org/abs/2601.21557)  
54. Daily Papers \- Hugging Face, [https://huggingface.co/papers?q=LLM-driven%20software%20engineering%20agents](https://huggingface.co/papers?q=LLM-driven+software+engineering+agents)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAaCAYAAAAXHBSTAAADAElEQVR4Xu2XS8hNURTHlzwi78gj6kMeiaK8UszoUx5JihgaKJkZyExJKZSExMBIJgZKIgzux4BSSjGRIokoKaEkj//fustZd93zuue795rcX/2796x9zj577b3W2vuI9Og4G6Fz0GloVWj7r4ypq1UWQnvr/4dBV6AZSbMMd/8HzQRoOjQ0NqSwHBqA+mJDCRZAJ931QWiZux4P7YeGOFvLnIU+Q2+h19BP0bAY529y0KHnMriwsYnjwC9Bs10beQAdkAqOjYKOQ8egSc7eD30SHfhcZzfuQkekwgtTWAS9l+a+1opO8Mpgz2UadE908GnsgH5Bt2OD6MvizFaBYXYHOhQbJMm1mpTM2+vQb+iUNM+QwU6vit7n2QKtC7YqMGe2S/L+Ja7NmAw9E3WuEA6U+ZMWWgZfdln03pHOxvifaTcFOKMMYxsof3ntQ9vsF0WdovZBUxvuUGwMr4K9CT7MgZ6R7FUiHGBNGp2aCD2CRtevPdtE295BN0XD96VoqH6Blia3/l0V9uuV1idhZfwRjRGGD3NlQ2wIzBEdoA8/s0WYX7dEJ4yD4DMnRAsRmQfdkGRyWmGzNKdAA5wNVq770NjQ5uEKciXZ2Rtn517y1V0be0RXwlYyFp81Ut2prHf+w0KKyqsozDXmHJ1i6TZWQ9/ddYQnhY+i/Xu4elQVCp2yxKtJvlOsinToKTTF2YtesFv0OW7cBsv2Q2ixs7XCCuhbNEY4YyyTLJdZ8ETBEIobX55TVhnpFPPWsNVlfrFqstqVOYYZhTllcNA8LfQ5G1+0S3TQ853dYznJ3ImwovGo5XNnBHRNtE+GNDfyrO0gi6OiIV3IJuiD6LKeF33wRd3GEMrjsGjuRGxGY+7QzpL+WBrLehmsBrCyloIrw3DaCW2FZkn+vmUwnOyzwcPPBYZ0WmhxcFU+J6zw8PTRUZgbnDnbgzoJneGW0o5zZiEsIuujsc2w6j4R/fzoCgylC3VVCasycBP3hawr0Bl+MrDotBsex/hp1KNHjy7zB1UbjLFZQ5FxAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEsAAAAaCAYAAAD/nKG4AAADzUlEQVR4Xu2YTahNURTHl1Dk2/MZJTKRV0hGvl6iGKAYUMwNKKUwkRiYCwMJj4F8RChSKDcGhEQxUQYkSkmEfORj/ey73t1vvbPPeYf7dF/dX/27nb3P3Wfv/1lr7X2vSJMmvYVhqv6+sQGp+zwZbKxqvO9IsEm1X+o8iR5iteq8BNP+iT6q26rPqheql6q7qrnxTRncU42JrvnuK9V71eyovRFgjdtU13xHGSaqLqpWqvpG7edUPyS8kSymqpa4to2qd6pP0nhmQYvqjgTjSjNTQjQQIR4i5rGExc9yfTxsr2qgax+sqkjjmgVrVdN9YxE3Vb9U631HxHIJ92DmiKidWvU6ujZ6g1m86CeqUb4jD0wgJPMKnpn1XGpFf4Dqsuq63RRRZJZtHtyXYriEqLaSwBxmSDp1SK24j+/mjQ/fVfN8Y4rJEkwgQvLYIl3N4pPrw3ZTRMos0pXielp1XMImcDTqNxaq3kjo/yChbt5QvVVNi+4zVknou6IaKWE9lJWvqkuSDgQ2sg2+McU6CbWo1XdE8LbapWsaYgJmbK9ex2SZxbHikOpp9RpYBJEZL2a+hEVaRK2RsMEsknA88QsngjCJeTBHUmtntQ8TaUsZQgnZ5xuzsAWdkHRow2LVTwkPXRG1W2ry6fFmWcoyDuPF0G+1Y5AE8xjXsAhOnfmWqRZIeB6LnxL1WUakzGJc5sX8crEFkQ55HJDsulbGLFuwT0uwCLX2XdLZLOvvF7VlgVEYjeHA/Wcl+5kGc6pIcW3reNtFZvEw0sCfpf7GLGrEnNptf/BmjVY9ql5Tnzj7UX+KYC57omsiDAMrkjaDORVlVgcMnheGPIRJUJT9gOwi7CaEusebZddZ5sZpCKTpMdURCRvBZtXQal8ejE1KGqQebbZ5ZW0MmFUULB1gAAOeklr4ApNjkC/S+TQfw+JYJG/G0yK1n03UE7ACzwQNfjU8lM7pjVlE8gUJ9yOKcN7vTqIoTkFgbrdUQyScIf3LBp4TG1wIzrMoFkGk8Ta/qc5IOFqk4OHtEibl4QXEsjTg6LBVwi+C+xKOBX43mqB6IF3H4DuTovti2qTrrkw2fJRwdEhFj98QugVp2CbhKMFnKsc97I5s82WxQ6lPf/tpRQrGEHlEgTfWIPqzMoCDLVGeFVU8+6QUbxx1wxZXL0gJosFvAsDOVpHuv8giWlVLfWNPQz3IS9cyUOxJTSvKMc8kHGOyoqQsjJH1B8B/4aqk/8L5GyjU1E4MonDvlvqYBKQ0J4B6zrcU41QHJexujc4OKbkDNmnSpElv4jdO+t+1/i6APAAAAABJRU5ErkJggg==>