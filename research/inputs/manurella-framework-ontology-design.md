# **Manurella Framework: Domain Ontology and Cognitive Architecture Analysis**

## **A. Executive Conclusion**

The proposed Manurella framework represents a highly ambitious attempt to unify cognitive agents, external tool ecosystems, bitemporal memory, and hierarchical reasoning into a general-purpose, runtime-agnostic architecture. However, an adversarial analysis of the initially proposed domain ontology—Build, Muse, Pixel, and Mentor—reveals severe structural vulnerabilities and epistemic category errors. The initial categorization conflates human-centric output mediums (Pixel) with cognitive scaffolding (Mentor) and generalized workflows (Muse), a fundamental error in ontology engineering that guarantees routing ambiguity, redundant tool allocation, and compounding multi-agent failure cascades.  
The analysis indicates that to support robust, scalable human-AI interaction without encountering the "topology tax" that plagues contemporary multi-agent systems, Manurella must abandon medium-based and persona-based categorizations altogether1. Instead, the framework must adopt a Hybrid Compositional Ontology grounded in the strict separation of runtime infrastructure, cognitive persistence semantics, universal capabilities, and boundary-enforced domain packs. By leveraging the Model Context Protocol (MCP) as a standardized, demilitarized transport layer3 and implementing a bitemporal operator algebra (TOKI) for state conflict resolution6, Manurella can circumvent the structural limitations of isolated agents.  
The resulting stable top-level architecture rejects "Pixel" entirely, refactors "Muse" into a universal generative capability, solidifies "Build" as an Engineering domain, recontextualizes "Mentor" as an Extraheric Scaffolding domain, and introduces critical missing domains for Operations and Synthesis. This architecture ensures that test-time reasoning effort scales orthogonally to domain constraints, preventing the exponential inter-agent misalignment and task verification failures observed in unconstrained agent meshes8.

## **B. Terminology and Layer Model**

To prevent definitional overlap and ensure a mathematically coherent architecture, Manurella must be stratified into a rigorous seven-layer model. This ensures that persistence semantics, computational capabilities, and user interfaces are entirely decoupled, preventing the common failure wherein a single agent conflates conversational state, world state, and tool-selection logic in an undifferentiated context window11.

### **1\. Runtime Infrastructure (Transport and Protocol)**

The foundational communication layer must be strictly governed by the Model Context Protocol (MCP), acting as a vendor-neutral boundary4. It handles routing via JSON-RPC 2.0, connection lifecycles, and cryptographic boundaries. MCP provides six core primitives: Resources for application-controlled data, Tools for executable functions, Prompts for reusable templates, Sampling for model delegation, Roots for filesystem boundary definition, and Elicitation for user-in-the-loop queries4. By enforcing MCP at the lowest level, Manurella avoids bespoke integration code and standardizes the execution surface.

### **2\. Cognitive Substrate (Persistence Semantics)**

Traditional cognitive architectures like CoALA and JEPA treat all long-term state equally, leading to category errors where factual claims and ephemeral experiences undergo identical decay mechanisms15. Manurella must adopt the four-layer decomposition proposed by Roynard (2026), which separates state strictly by its required persistence mechanics16. Knowledge represents factual, structural data and is governed by indefinite supersession; it never decays, only yielding to newer evidence via cryptographic provenance. Memory stores episodic experiences and is governed by Ebbinghaus decay, fading if not reinforced. Wisdom encapsulates procedural routing and action-shaping policies, updating only through evidence-gated revision. Intelligence is the ephemeral inference pass of the Large Language Model itself, possessing no inherent state16.

### **3\. Universal Capabilities**

Universal capabilities represent modality-agnostic functions available across all domains. Examples include code execution environments (via MCP tool translation)19, generic semantic search, and basic multi-step planning. Bounding code execution strictly to an engineering domain artificially limits data analysis and administrative workflows, which also rely on programmatic execution.

### **4\. Domain Packs (Top-Level Architecture)**

Domains are highly cohesive, loosely coupled ontological boundaries that dictate specific state spaces, restricted MCP tool sets, and evaluation benchmarks. A domain is a bounding box for authorized action and context, not a separate LLM or standalone agent. Domains define the epistemic boundaries within which the LLM is permitted to operate, isolating risk and preventing tool explosion11.

### **5\. Workflows**

Workflows are directed acyclic graphs (DAGs) or state machines composed of Universal Capabilities and Domain Packs executed in sequence or parallel. A workflow represents a specific business process or user request, dynamically chaining domains to achieve an outcome without permanently merging their ontologies.

### **6\. Reasoning Control Gates**

The deterministic decision policy executing over the cognitive substrate. Based on the AgentAtlas taxonomy, Manurella must enforce a six-state control space prior to any action: Act, Ask, Refuse, Stop, Confirm, and Recover21. This prevents agents from blindly acting when clarification is required, routing ambiguous scenarios immediately to the Elicitation protocol.

### **7\. Interface Personas**

The user-facing manifestation of the agent, applying stylistic prompts and interaction modalities over the underlying domains. Personas dictate tone and presentation but have zero influence on tool permissions, cognitive persistence, or control logic.

## **C. Competing Ontology Comparison Matrix**

The determination of Manurella’s top-level architecture requires evaluating four distinct decomposition models. The analysis demonstrates that only a Hybrid Compositional approach satisfies the strict requirements for mutual exclusivity, collective exhaustion, and mathematical coherence.

| Decomposition Model | Core Principle | Epistemic Strengths | Structural Vulnerabilities and Critiques | Final Verdict |
| :---- | :---- | :---- | :---- | :---- |
| **Medium / Craft-Based** | Division by output modality (e.g., Text, Code, Image, Audio, Video). | Intuitive for end-users accustomed to legacy software applications (e.g., word processors vs. image editors). | Fundamentally obsolete in the era of natively multimodal LLMs. Creates severe routing ambiguity when tasks cross mediums, such as writing a Python script to generate an SVG graphic. Conflates the representation of data with the cognitive faculty required to produce it. | **Rejected.** Fails to capture the underlying reasoning mechanics, leading to redundant tool instantiation across domains. |
| **Human-Outcome-Based** | Division by functional goals aligned with enterprise value chains, such as the NIST 200-1 Taxonomy (e.g., Decision Making, Content Creation, Detection, Process Automation)23. | Excellent for retrospective benchmark coverage, legal compliance, and organizational impact assessment23. | Exhibits extreme overlap in operational capabilities. A single workflow, such as diagnosing a system outage, requires Detection, Content Synthesis, and Decision Making simultaneously, leading to redundant agent switching and latency cascades. | **Rejected as Top-Level.** Highly valuable for post-hoc trajectory evaluation and logging, but unworkable as a runtime routing ontology. |
| **Cognitive-Function-Based** | Division by psychological or neuro-symbolic acts, mirroring frameworks like CoALA or BFO (e.g., separating perception, semantic retrieval, working memory, and planning)15. | Highly rigorous; maps perfectly to the LLM lifecycle and hardware constraints, preventing epistemic drift and aligning with psychological dissociations like Tulving's trichotomy16. | Too granular for user-directed domain assignment. Forces the user or the orchestrator to manage sub-cognitive routines manually, violating the "personal-first" and high-level collaborative requirement of Manurella. | **Adopted as Substrate (Layer 2\)**, but rejected as the top-level domain ontology. |
| **Hybrid Compositional** | Domains represent bounded, specialized ecosystems of tools, state, and context, mapped onto a shared cognitive substrate and accessed by a central intelligence. | Eliminates the multi-agent "topology tax"1. A single underlying model assumes different Domain Packs, preventing duplication while scaling context efficiently. Matches the reality of modern MCP tool environments. | Requires strict, mathematically sound boundary tests to prevent "domain bloat." Cross-domain state must be meticulously managed using bitemporal logic to avoid contradictions during context handoffs6. | **Recommended.** Provides the optimal balance of architectural generalizability, operational isolation, and user comprehension. |

In the context of formal ontology engineering, approaches like the Basic Formal Ontology (BFO) and the Descriptive Ontology for Linguistic and Cognitive Engineering (DOLCE) highlight the danger of flawed ontological commitments. BFO relies on a realist 3D endurantist view, where objects are wholly present and endure through time, whereas DOLCE takes a descriptive, language-based approach27. Manurella must favor an extensional, 4D perdurantist approach for its digital artifacts and state management. If an agent modifies a codebase, "the code yesterday" and "the code today" must be treated as different temporal slices of the same 4D entity to maintain bitemporal consistency and prevent state drift6. The Hybrid Compositional model natively supports this by treating domains as temporal ecosystems rather than static objects.

## **D. Objective Boundary Tests for Ontology Management**

To prevent the arbitrary proliferation of domains, Manurella requires deterministic, objective boundary tests for creating, splitting, merging, or retiring domains. Without these guardrails, the framework will succumb to over-specialization, resulting in the N-squared communication path failures characteristic of sprawling agent meshes2.  
The creation of a new top-level domain must satisfy the strict isolation criterion. A candidate domain must require a fundamentally distinct set of MCP Roots (filesystem boundaries) and MCP Tools that cannot be safely exposed to an existing domain without violating the principle of least privilege5. If a proposed domain operates on the exact same data structures and API endpoints as an existing domain, it is a Workflow or a Persona, not a Domain. Furthermore, a domain must be subject to an independent, externally validated benchmark. If performance in the proposed domain cannot be measured orthogonally to existing domains—for instance, if evaluating it simply recapitulates SWE-Bench Verified30—it lacks ontological independence.  
Splitting an existing domain becomes necessary under the bitemporal contradiction criterion. If tasks within a single domain begin to exhibit contradictory persistence semantics—meaning the Knowledge layer is constantly forced to supersede facts because sub-tasks operate on entirely different truth paradigms—the domain has become epistemically contaminated and must be split6. Conversely, domains must be merged if an empirical analysis of multi-hop routing reveals that greater than eighty percent of tasks initiated in Domain A require an immediate, unprompted context handoff to Domain B. Such heavy coupling indicates that the boundary is artificial and induces a latency cascade without providing security or cognitive benefits11. Domains are retired if their exclusive MCP tools are deprecated or if their underlying capabilities are subsumed entirely by the Universal Capabilities layer.

## **E. Recommended Top-Level Architecture**

The recommended top-level architecture for Manurella leverages a single, continuous Intelligence layer (the LLM) that dynamically mounts Domain Packs. The analysis of the Multi-Agent System Failure Taxonomy (MAST), encompassing over 1,600 execution traces across frameworks like AutoGen and MetaGPT, reveals that inter-agent misalignment and task verification failures account for the vast majority of execution crashes9. Agents disobey role specifications, ignore inputs from peers, and enter infinite conversational loops9. Manurella must therefore eschew peer-to-peer agent meshes entirely.  
Instead, Manurella utilizes a unified orchestrator that switches Context Boundaries. Each Top-Level Domain acts as an enforced scope containing authorized MCP Tool Subsets, ensuring strict isolation of execution environments4. The domains operate over specific persistence schemas utilizing the TOKI bitemporal operator algebra, maintaining an audit row for contradiction resolution to ensure that state drift does not corrupt cross-domain workflows6. Evaluative Oracles are baked into the domain definition, providing telemetry mapped to the AgentAtlas nine-category trajectory failure tracking system, which isolates primary error sources such as Goal Misinterpretation, Wrong Tool Selection, and Observation Failure21.

## **F. Placement Analysis for Build, Muse, Pixel, and Mentor**

The original proposed domain family reflects a blend of functional and anthropomorphic biases that fail the objective boundary tests outlined above.

### **1\. Build: Retain and Refine as "Engineering"**

The "Build" domain is highly valid as a top-level domain, but should be formalized as Engineering. Software engineering, system architecture, and formal logic require distinct state management, specifically interaction with version control, continuous integration environments, and iterative compilation feedback. Engineering tasks require specialized MCP roots for filesystem boundaries and tools capable of executing stateful terminal commands5. It relies heavily on AgentAtlas control states like Act and Recover, navigating deep dependency trees and compiler errors. Its ontological independence is verified by its distinct evaluation mechanisms, specifically SWE-Bench Verified and its variants22.

### **2\. Muse: Downgrade to Universal Capability**

"Muse" implies ideation, brainstorming, and creative synthesis. Ontologically, ideation is a point on the Human-AI Task Tensor corresponding to the AI integration dimension35. Brainstorming is utilized equally in Engineering for system design and in Data Analysis for hypothesis generation. Elevating Muse to a top-level domain creates artificial silos, forcing the user to switch domains simply to brainstorm a solution to a coding problem. Generative synthesis is a Universal Capability that must be available globally across all domains, interacting heavily with the LLM's inherent semantic retrieval functions.

### **3\. Pixel: Exclude and Deprecate**

The "Pixel" domain categorizes capabilities by the visual output medium. Under a modern, natively multimodal architecture, distinguishing between text, spatial reasoning, and pixel generation is an anachronistic category error. A multimodal LLM processes images, text, and audio in a unified embedding space. Isolating visual generation into a separate domain creates profound routing ambiguity; generating UI code from a visual mockup straddles Build and Pixel, requiring constant, lossy handoffs. Multimodal generation and ingestion must be treated as basic I/O within the Universal Capabilities layer.

### **4\. Mentor: Retain and Refactor as "Scaffolding"**

Traditional AI operates via Replacement (automating a full cognitive subtask) or Augmentation (enhancing efficiency without displacing agency). "Mentor" relies on an Extraheric mode37, where the AI intentionally abstains from completing the task to solicit critical thinking, analytical reasoning, and creative generation from the human user. This encompasses Socratic dialogue, educational tutoring, and collaborative review. The Extraheric mode requires fundamentally inverted success metrics. Instead of optimizing for Final Task Success or time-to-completion, the domain optimizes for human germane cognitive load and knowledge retention37. It requires heavy use of the MCP Elicitation capability to prompt the user rather than solving the problem directly13. Because its interaction paradigm, evaluation metrics, and tool constraints differ entirely from Engineering, it passes the boundary tests and stands as a Top-Level Domain.

## **G. Missing-Domain Analysis**

To achieve collective exhaustion of general human-AI work without generating an unmaintainable number of agents, the ontology requires the addition of two critical domains that address tasks currently causing severe hallucination and latency cascades in single-agent architectures.

### **1\. Operations (Orchestration and Administration)**

The proposed framework entirely lacks a domain for environment configuration, scheduling, permission management, and multi-system business workflows. Evaluating models via interactive benchmarks demonstrates that administrative workflows—such as HR onboarding, inventory management, and multi-system alignment—are persistent bottlenecks where current models fail due to stale or conflicting artifacts39. Operations requires isolated permissions to interact with the host system's meta-state, utilizing MCP tools for SaaS platforms, calendars, and organizational databases. It operates under strict constraint violation monitoring to prevent unauthorized systemic changes21.

### **2\. Synthesis (Analysis and Empirical Research)**

Distinct from Engineering (which builds and mutates systems), Synthesis operates on existing data to extract patterns, test statistical hypotheses, conduct intelligence gathering, and perform multi-hop research. It requires access to distinct MCP tools, such as data warehouse connectors and advanced semantic search endpoints33. Crucially, it must manage strict epistemic boundaries to prevent the model from hallucinating statistical noise or falling into "directional freezing" under agreement pressure20. Synthesis is heavily reliant on the Knowledge layer's indefinite supersession semantics, constantly updating world-facts based on newly analyzed data16.

## **H. Cross-Domain Routing and Bitemporal Composition**

A primary failure vector in multi-agent and cross-domain architectures is the topology tax—the compounding of errors and epistemic degradation during context handoffs1. When the Engineering domain hands a structured dataset to the Synthesis domain, differing persistence states and unsynchronized memories can cause catastrophic hallucinations. Manurella must enforce a strict routing and composition model to maintain coherence.  
Before crossing a domain boundary, the orchestrator must pass through the AgentAtlas six-state control decision policy21. If the user's intent is materially underspecified, the orchestrator must transition to the Ask state, triggering an MCP Elicitation request to the user, rather than guessing the target domain and initiating an incorrect execution tree13. If the intent is clear, the orchestrator safely transitions to Act within the newly mounted domain.  
Cross-domain communication cannot rely on passing raw, unstructured context windows, which quickly leads to context collapse11. Instead, domains interact by reading and writing to standardized MCP Resources and updating the Roynard Knowledge and Memory layers4. When domains disagree on a specific state—for instance, if Operations logs a server configuration that Engineering subsequently mutates—the system relies on the TOKI bitemporal operator algebra. TOKI treats contradiction resolution as write-time concurrency control, utilizing an evidence-weighted merge that commits the winner to the current row while securely writing the loser to an audit row. This preserves replay consistency and prevents belief-drift skew, ensuring that the losing fact remains algebraically recoverable6.

## **I. Domain Mapping and Risk Architecture**

The following matrix maps each finalized Top-Level Domain to its required operational parameters, ensuring that the theoretical ontology translates directly into runtime constraints.

| Domain | Primary MCP Tools & Roots | Persistence Semantics | Primary Trajectory Risks (AgentAtlas/MAST) |
| :---- | :---- | :---- | :---- |
| **Engineering** | Code Execution, GitHub API, Filesystem Roots, Linter/Compiler hooks33. | Wisdom (procedural patterns), Knowledge (system architecture facts). | Looping/over-action on failed compiles; State drift due to unobserved mutations11. |
| **Operations** | SaaS APIs (Slack, SharePoint), DB Toolboxes, System Meta-state33. | Memory (episodic schedules), Knowledge (organizational hierarchies). | Constraint violation (permissions); Unsafe trust of external content; Inter-agent misalignment9. |
| **Synthesis** | Advanced RAG, BigQuery Toolboxes, Data visualization execution33. | Knowledge (indefinite supersession of factual claims)17. | Over-search without terminating; Hallucination of statistical significance; Epistemic boundary failure20. |
| **Scaffolding** | Elicitation, Prompt Templates, Educational metric telemetry13. | Memory (user interaction history), Wisdom (tutoring strategies). | Goal misinterpretation (solving the problem instead of teaching); Extraneous cognitive load generation22. |

## **J. Extensibility Model without Kernel Changes**

To prevent the architecture from becoming rigid, Manurella requires an extensibility model that permits the introduction of new domains and capabilities without modifying the core orchestrator kernel. This is achieved natively through the Model Context Protocol (MCP). Because the kernel speaks a standardized JSON-RPC 2.0 dialect, new domains are introduced simply by connecting new MCP Servers3.  
Crucially, as the number of connected tools grows, loading all tool definitions upfront overloads the context window, a primary driver of single-agent failure11. Manurella circumvents this by presenting MCP servers as code APIs. The agent discovers tools dynamically by exploring the filesystem roots, listing available servers, and reading specific tool schema files to understand interfaces on demand. The agent then writes and executes code to interact with these servers, keeping intermediate data in the execution environment. This progressive disclosure ensures that the kernel remains lightweight while the capability surface area scales infinitely4.

## **K. Benchmark Coverage and the Quality Gate**

To enforce a strict 80/100 minimum quality gate, Manurella must be evaluated using benchmarks that systematically separate final outcome success from trajectory quality and control-decision accuracy. As demonstrated by recent multi-axis evaluation frameworks, a single accuracy column is no longer sufficient for deployable agents22.

| Evaluation Layer | Primary Benchmark Target | Evaluated Metric (Outcome \+ Trajectory) | Quality Gate Threshold |
| :---- | :---- | :---- | :---- |
| **Layer 6: Control** | AgentAtlas | Control-Decision Accuracy (Act/Ask/Refuse/Stop) | \> 85% Accuracy on 6-state prediction; 0% hallucinated execution21. |
| **Engineering** | SWE-Bench Verified / Pro | Issue Resolution Rate \+ AST Validation \+ Bash-only stability | \> 75% outcome; \< 5% Trajectory looping or syntax errors22. |
| **Synthesis** | GAIA / FrontierMath | Multi-hop reasoning accuracy \+ Evidence validation | \> 80% on clean state; explicit penalty tracking for Over-search (SAAS)22. |
| **Operations** | OSWorld / WebArena | End-state system alignment \+ UI observation success | \> 80% strict accuracy without wrong-state replacement or premature termination9. |
| **Scaffolding** | Human-in-the-loop (HITL) | Extraneous vs. Germane Load Optimization | High Elicitation precision; near-zero "unauthorized task completion"13. |

## **L. Failure Modes: Specialization versus Collapse**

The ontological design of Manurella must actively defend against recognized failure modes documented across the multi-agent literature.  
Over-specialization creates the Topology Tax. If a task is decomposed into too many micro-domains, the system relies on excessive inter-agent communication. The MAST taxonomy identifies this as Inter-Agent Misalignment, where agents create lossy translations during handoffs, withhold information, ignore inputs from peers, or engage in conversation resets that derail the task8. Manurella mitigates this by enforcing broad, highly cohesive Top-Level Domains and relying on a central orchestrator mounting different contexts, rather than deploying parallel autonomous agents to argue with one another.  
Conversely, under-specialization causes Context Collapse. A single agent forced to hold conversational state, world state, tool-selection logic, and control flow in one undifferentiated context window will inevitably fail11. This leads to Tool Explosion, where selection accuracy degrades as the tool count grows, and State Drift, where the agent acts on world states that have changed mid-run. Manurella mitigates this through dynamic MCP tool loading via code execution and the strict bitemporal state management of the TOKI algebra, ensuring the context window only contains the exact semantic footprint required for the immediate action6.

## **M. Reasoning Effort Tiers and the Framework Atlas**

The framework proposes reasoning effort tiers ranging from Low to Sentient. Crucially, these tiers must not dictate domain definitions. Instead, they operate orthogonally as dynamic allocators of test-time compute, representing inference-time reasoning scale46. Scaling laws for 2025 and 2026 demonstrate that allocating additional compute at test time improves performance monotonically on knowledge-intensive tasks, enabling advanced self-correction, backtracking, verification, and problem decomposition47.  
A "Low" effort tier restricts the agent to a single forward pass, appropriate for routine Operations tasks. An "Ultra" tier allocates massive reasoning-token budgets (e.g., 16,000+ tokens per generation call) for deep internal deliberation and multi-path trajectory validation, required for complex Engineering or Synthesis tasks47. Effort modulates the depth and rigor of the AgentAtlas control decisions—dictating how aggressively the model verifies its trajectory—entirely independent of which Domain Pack is currently mounted.  
These dynamic shifts have profound implications for the interactive Framework Atlas. The Atlas serves as the user-facing spatial representation of the ontology. Given the Hybrid Compositional model, the Atlas must not present a static tree of isolated chatbots. Instead, it must visualize the Context Boundary in real-time. As a user shifts a workflow from Operations to Engineering, the Atlas visually represents the unloading of Operations MCP Roots and the loading of Engineering MCP Tools. Simultaneously, it displays the current test-time compute allocation, rendering the AI’s persistence semantics and reasoning budget transparent to the user, thereby satisfying strict requirements for human-centered AI transparency and usability23.

## **N. V0, V1, and Long-Term Rollout**

**V0 (Kernel and Substrate Validation):** The initial phase must focus exclusively on the core infrastructure. This includes deploying the MCP runtime for all tool and resource connections4 and instantiating the Roynard four-layer cognitive substrate with TOKI contradiction resolution6. V0 should deploy only the Engineering domain to validate the AgentAtlas six-state control policy against the SWE-Bench Verified dataset, establishing a baseline for trajectory stability21.  
**V1 (Ontology Expansion and Dynamic Loading):** Phase two introduces the Operations and Synthesis domains. Crucially, V1 must implement dynamic tool loading via code execution to prevent tool explosion within the LLM context window19. The Framework Atlas UI is deployed in this phase to visualize domain transitions and reasoning effort allocation to end-users.  
**Long-Term (Scaffolding and Autonomous Generalization):** The final phase introduces the Scaffolding domain, optimizing for Extraneous versus Germane cognitive load in human-AI collaboration37. Long-term rollout also enables Sentient-tier test-time compute for fully autonomous, long-horizon workflow execution, utilizing evidence-gated self-correction and multi-agent pipeline validation without succumbing to the topology tax.

## **O. Machine-Readable Draft Tree**

YAML  
manurella\_ontology\_v1:  
  layer\_1\_runtime:  
    protocol: "Model Context Protocol (MCP) 2025-11-25"  
    transports: \["stdio", "SSE"\]  
    capabilities: \["Roots", "Sampling", "Elicitation", "Tools", "Resources", "Prompts"\]  
  layer\_2\_cognitive\_substrate:  
    knowledge: { semantics: "indefinite\_supersession", logic: "TOKI\_bitemporal\_algebra" }  
    memory: { semantics: "ebbinghaus\_decay" }  
    wisdom: { semantics: "evidence\_gated\_revision" }  
    intelligence: { semantics: "ephemeral\_inference" }  
  layer\_3\_universal\_capabilities:  
    \- "generative\_synthesis"  
    \- "code\_execution\_environment"  
    \- "semantic\_retrieval"  
  layer\_4\_top\_level\_domains:  
    engineering:  
      description: "Codebase architecture, formal logic, deterministic compilation."  
      benchmarks: \["SWE-Bench\_Verified", "SWE-Bench\_Pro"\]  
    synthesis:  
      description: "Data analysis, statistical hypothesis testing, intelligence extraction."  
      benchmarks: \["GAIA", "FrontierMath"\]  
    operations:  
      description: "Meta-system coordination, scheduling, permission orchestration."  
      benchmarks: \["OSWorld", "WebArena"\]  
    scaffolding:  
      description: "Extraheric human-AI interaction, educational tutoring, code-review."  
      benchmarks: \["HITL\_Cognitive\_Load\_Metrics"\]  
  layer\_6\_control\_gates:  
    states: \["Act", "Ask", "Refuse", "Stop", "Confirm", "Recover"\]

## **P. Explicit Decisions Safe to Adopt Now Versus Decisions Requiring Experiments**

**Decisions Safe to Adopt Now:** The deprecation of medium-based domains is mathematically and practically sound; "Pixel" must be eliminated, and multimodal capabilities integrated universally. The adoption of the Model Context Protocol (MCP) as the strict standard for all external tool and resource connections should proceed immediately to prevent fragmented API integrations and secure cryptographic boundaries3. Furthermore, decoupling effort tiers from domain definitions and treating test-time compute scaling as a global hyperparameter is strongly supported by recent scaling laws and should be hardcoded into the orchestrator48. Finally, the adoption of the AgentAtlas control states (Act, Ask, Refuse, Stop, Confirm, Recover) as the primary routing mechanism ensures measurable trajectory safety from day one21.  
**Decisions Requiring Experimental Validation (Deferred):** While theoretically sound, the exact parameters for the TOKI bitemporal algebra—specifically the thresholds for evidence-weighted merging in the Knowledge layer—require real-world A/B testing to prevent audit row bloat and ensure acceptable latency6. Similarly, traditional accuracy benchmarks fail for the Scaffolding domain; measuring an increase in "human germane load" requires bespoke psychometric and UX testing prior to V1 deployment37. Finally, the Sentient-tier boundaries representing the highest level of test-time compute must undergo rigorous lab testing to establish safety limits against "looping or over-action" trajectory failures before any public release22.

## **Q. Open Research Questions**

The architectural analysis reveals persistent gaps that require targeted research. How can persistent semantic memory be safely shared across different users operating within the same organizational Operations domain without violating zero-trust MCP Root boundaries52? Additionally, can the nine-category trajectory failure model be applied dynamically *during* inference as streaming guardrails, halting token generation before a cascading failure occurs, rather than relying on post-hoc evaluation40? Finally, the limits of test-time compute in completely replacing train-time capabilities remain ambiguous; defining the exact crossover point where an increase in reasoning effort yields diminishing returns against systemic state drift will dictate the ultimate scalability of the Manurella framework11.

#### **Works cited**

1. The Compounding Errors Problem: Why Multi-Agent Systems Fail and the Architecture That Fixes It | Zartis, [https://www.zartis.com/the-compounding-errors-problem-why-multi-agent-systems-fail-and-the-architecture-that-fixes-it/](https://www.zartis.com/the-compounding-errors-problem-why-multi-agent-systems-fail-and-the-architecture-that-fixes-it/)  
2. The Agent Mesh Illusion: Why More Agents Usually Means Worse Results \- DEV Community, [https://dev.to/aws-builders/the-agent-mesh-illusion-why-more-agents-usually-means-worse-results-277p](https://dev.to/aws-builders/the-agent-mesh-illusion-why-more-agents-usually-means-worse-results-277p)  
3. What is Model Context Protocol (MCP)? A guide | Google Cloud, [https://cloud.google.com/discover/what-is-model-context-protocol](https://cloud.google.com/discover/what-is-model-context-protocol)  
4. Specification \- Model Context Protocol, [https://modelcontextprotocol.io/specification/2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)  
5. MCP Core Concepts: Mastering the Model Context Protocol for AI Integration \- GitHub, [https://github.com/microsoft/mcp-for-beginners/blob/main/01-CoreConcepts/README.md](https://github.com/microsoft/mcp-for-beginners/blob/main/01-CoreConcepts/README.md)  
6. TOKI: A Bitemporal Operator Algebra for Contradiction Resolution in LLM-Agent Persistent Memory \- arXiv, [https://arxiv.org/html/2606.06240v1](https://arxiv.org/html/2606.06240v1)  
7. TOKI: A Bitemporal Operator Algebra for Contradiction Resolution in LLM-Agent Persistent Memory \- arXiv, [https://arxiv.org/pdf/2606.06240](https://arxiv.org/pdf/2606.06240)  
8. \[PDF\] Why Do Multi-Agent LLM Systems Fail? | Semantic Scholar, [https://www.semanticscholar.org/paper/Why-Do-Multi-Agent-LLM-Systems-Fail-Cemri-Pan/c83b6a023a5c5ec71b44920a41b41fc007266c44](https://www.semanticscholar.org/paper/Why-Do-Multi-Agent-LLM-Systems-Fail-Cemri-Pan/c83b6a023a5c5ec71b44920a41b41fc007266c44)  
9. (PDF) Why Do Multi-Agent LLM Systems Fail? \- ResearchGate, [https://www.researchgate.net/publication/389947144\_Why\_Do\_Multi-Agent\_LLM\_Systems\_Fail](https://www.researchgate.net/publication/389947144_Why_Do_Multi-Agent_LLM_Systems_Fail)  
10. Why Do Multi-Agent LLM Systems Fail? \- arXiv, [https://arxiv.org/pdf/2503.13657](https://arxiv.org/pdf/2503.13657)  
11. Why Single Agents Fail at Scale: The Five-Mode Failure Taxonomy | Ranjan Kumar, [https://ranjankumar.in/single-agent-failure-modes-multi-agent-taxonomy](https://ranjankumar.in/single-agent-failure-modes-multi-agent-taxonomy)  
12. Model Context Protocol for .NET, Full MCP Client for Local AI Agents, LM-Kit, [https://lm-kit.com/solutions/ai-agents/mcp/](https://lm-kit.com/solutions/ai-agents/mcp/)  
13. Understanding MCP features: Tools, Resources, Prompts, Sampling, Roots, and Elicitation, [https://workos.com/blog/mcp-features-guide](https://workos.com/blog/mcp-features-guide)  
14. The Model Context Protocol (MCP): Deep dive into structure and concepts \- HMS Analytical Software, [https://www.analytical-software.de/en/the-model-context-protocol-mcp-deep-dive-into-structure-and-concepts/](https://www.analytical-software.de/en/the-model-context-protocol-mcp-deep-dive-into-structure-and-concepts/)  
15. Cognitive Architectures for Language Agents \- arXiv, [https://arxiv.org/html/2309.02427v3](https://arxiv.org/html/2309.02427v3)  
16. arXiv:2604.11364v1 \[cs.AI\] 13 Apr 2026, [https://arxiv.org/pdf/2604.11364](https://arxiv.org/pdf/2604.11364)  
17. \[2604.11364\] The Missing Knowledge Layer in Cognitive Architectures for AI Agents \- arXiv, [https://arxiv.org/abs/2604.11364](https://arxiv.org/abs/2604.11364)  
18. Daily Papers \- Hugging Face, [https://huggingface.co/papers?q=persistence%20semantics](https://huggingface.co/papers?q=persistence+semantics)  
19. Code execution with MCP: building more efficient AI agents \- Anthropic, [https://www.anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp)  
20. Daily Papers \- Hugging Face, [https://huggingface.co/papers?q=epistemic%20boundaries](https://huggingface.co/papers?q=epistemic+boundaries)  
21. AgentAtlas: Beyond Outcome Leaderboards for LLM Agents \- arXiv, [https://arxiv.org/html/2605.20530](https://arxiv.org/html/2605.20530)  
22. AgentAtlas: Beyond Outcome Leaderboards for LLM Agents \- arXiv, [https://arxiv.org/html/2605.20530v1](https://arxiv.org/html/2605.20530v1)  
23. AI Use Taxonomy: A Human-Centered Approach | NIST, [https://www.nist.gov/publications/ai-use-taxonomy-human-centered-approach](https://www.nist.gov/publications/ai-use-taxonomy-human-centered-approach)  
24. AI Use Taxonomy: A Human-Centered Approach \- NIST Technical Series Publications, [https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.200-1.pdf](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.200-1.pdf)  
25. Disclosing artificial intelligence use in scientific research and publication: When should disclosure be mandatory, optional, or unnecessary? \- Taylor & Francis, [https://www.tandfonline.com/doi/full/10.1080/08989621.2025.2481949](https://www.tandfonline.com/doi/full/10.1080/08989621.2025.2481949)  
26. Upper ontology \- Wikipedia, [https://en.wikipedia.org/wiki/Upper\_ontology](https://en.wikipedia.org/wiki/Upper_ontology)  
27. BFO/DOLCE Primitive Relation Comparison \- Department of Computer Science and Engineering, [https://cse.buffalo.edu/sneps/Bibliography/sey09a.pdf](https://cse.buffalo.edu/sneps/Bibliography/sey09a.pdf)  
28. Everyone Has an Ontology Now. Almost Nobody Has an Ontology: Extended Analysis | by Dr Nicolas Figay \- Medium, [https://medium.com/@nfigay/everyone-has-an-ontology-now-almost-nobody-has-an-ontology-extended-analysis-4f72f519c211](https://medium.com/@nfigay/everyone-has-an-ontology-now-almost-nobody-has-an-ontology-extended-analysis-4f72f519c211)  
29. BFO and DOLCE: So Far, So Close… \- SciSpace, [https://scispace.com/pdf/bfo-and-dolce-so-far-so-close-3ud3lsq4xm.pdf](https://scispace.com/pdf/bfo-and-dolce-so-far-so-close-3ud3lsq4xm.pdf)  
30. SWE-bench Verified, [https://www.swebench.com/verified.html](https://www.swebench.com/verified.html)  
31. Why Do Multi-Agent LLM Systems Fail? \- arXiv, [https://arxiv.org/html/2503.13657v3](https://arxiv.org/html/2503.13657v3)  
32. Why Do Multi-Agent LLM Systems Fail?, [https://neurips.cc/media/neurips-2025/Slides/121528\_lmjNn1F.pdf](https://neurips.cc/media/neurips-2025/Slides/121528_lmjNn1F.pdf)  
33. Model Context Protocol (MCP) explained: A practical technical overview for developers and architects \- CodiLime, [https://codilime.com/blog/model-context-protocol-explained/](https://codilime.com/blog/model-context-protocol-explained/)  
34. Saving SWE-Bench: A Benchmark Mutation Approach for Realistic Agent Evaluation \- arXiv, [https://arxiv.org/html/2510.08996v4](https://arxiv.org/html/2510.08996v4)  
35. \[2503.15490\] Toward a Human-AI Task Tensor: A Taxonomy for Organizing Work in the Age of Generative AI \- arXiv, [https://arxiv.org/abs/2503.15490](https://arxiv.org/abs/2503.15490)  
36. Research \- Dr. Anil R. Doshi, [https://www.anilrdoshi.com/research](https://www.anilrdoshi.com/research)  
37. Taxonomy of Human-AI Interaction Modes \- Emergent Mind, [https://www.emergentmind.com/topics/taxonomy-of-human-ai-interaction-modes](https://www.emergentmind.com/topics/taxonomy-of-human-ai-interaction-modes)  
38. Human-Centered AI | NIST \- National Institute of Standards and Technology, [https://www.nist.gov/programs-projects/human-centered-ai](https://www.nist.gov/programs-projects/human-centered-ai)  
39. Daily Papers \- Hugging Face, [https://huggingface.co/papers?q=Agent%20benchmarks](https://huggingface.co/papers?q=Agent+benchmarks)  
40. (PDF) Directional Freezing in Language Models: Residual-Trajectory Metrics for Detecting Overconfident Agreement Dynamics S 4 OS: A Research Scaffold for Semantic Stability Monitoring \- ResearchGate, [https://www.researchgate.net/publication/406994485\_Directional\_Freezing\_in\_Language\_Models\_Residual-Trajectory\_Metrics\_for\_Detecting\_Overconfident\_Agreement\_Dynamics\_S\_4\_OS\_A\_Research\_Scaffold\_for\_Semantic\_Stability\_Monitoring](https://www.researchgate.net/publication/406994485_Directional_Freezing_in_Language_Models_Residual-Trajectory_Metrics_for_Detecting_Overconfident_Agreement_Dynamics_S_4_OS_A_Research_Scaffold_for_Semantic_Stability_Monitoring)  
41. Daily Papers \- Hugging Face, [https://huggingface.co/papers?q=trajectory-level%20penalties](https://huggingface.co/papers?q=trajectory-level+penalties)  
42. \[2605.20530\] AgentAtlas: Beyond Outcome Leaderboards for LLM Agents \- arXiv, [https://arxiv.org/abs/2605.20530](https://arxiv.org/abs/2605.20530)  
43. Kasra Mazaheri's research works \- ResearchGate, [https://www.researchgate.net/scientific-contributions/Kasra-Mazaheri-2350384119](https://www.researchgate.net/scientific-contributions/Kasra-Mazaheri-2350384119)  
44. SWE-bench Leaderboards, [https://www.swebench.com/index.html](https://www.swebench.com/index.html)  
45. Risk Analysis Techniques for Governed LLM-based Multi-Agent Systems \- Netlify, [https://gradientinstitute-v3.netlify.app/assets/gradient\_multiagent\_report.pdf](https://gradientinstitute-v3.netlify.app/assets/gradient_multiagent_report.pdf)  
46. Augmenting large language models with psychologically grounded models of causal reasoning for planning under uncertainty \- Frontiers, [https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1730614/full](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1730614/full)  
47. How Inference Compute Shapes Frontier LLM Evaluation \- arXiv, [https://arxiv.org/html/2606.17930v1](https://arxiv.org/html/2606.17930v1)  
48. Scaling Laws, Foundation Models, and the AI Singularity: A Critical Appraisal of 2023- 2025 Evidence \- ResearchGate, [https://www.researchgate.net/publication/399498402\_Scaling\_Laws\_Foundation\_Models\_and\_the\_AI\_Singularity\_A\_Critical\_Appraisal\_of\_2023-\_2025\_Evidence](https://www.researchgate.net/publication/399498402_Scaling_Laws_Foundation_Models_and_the_AI_Singularity_A_Critical_Appraisal_of_2023-_2025_Evidence)  
49. Test-Time Compute: Why the Future of AI Is Thinking Longer, Not Training Bigger, [https://pub.towardsai.net/test-time-compute-why-the-future-of-ai-is-thinking-longer-not-training-bigger-0ec197b299ae](https://pub.towardsai.net/test-time-compute-why-the-future-of-ai-is-thinking-longer-not-training-bigger-0ec197b299ae)  
50. Who Benefits from AI Explanations? Towards Accessible and Interpretable Systems \- arXiv, [https://arxiv.org/html/2508.10806v1](https://arxiv.org/html/2508.10806v1)  
51. MCP Docs \- Model Context Protocol （MCP）, [https://modelcontextprotocol.info/docs/](https://modelcontextprotocol.info/docs/)  
52. Daily Papers \- Hugging Face, [https://huggingface.co/papers?q=persistent%20memory%20overlay](https://huggingface.co/papers?q=persistent+memory+overlay)