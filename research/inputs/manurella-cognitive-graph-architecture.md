# **Architectural Specification of the Manurella Dynamic Cognitive Graph Engine**

## **Theoretical Foundations and System Ontology**

The design of autonomous systems capable of operating in non-stationary computing environments requires extensive internal models that represent states, actions, and sequential relationships1. Rather than relying on static, hand-authored workflow paths, the Manurella portable agentic framework employs a Dynamic Cognitive Graph as an evolving reasoning map1. This architecture shifts from localized, egocentric execution sequences to global, allocentric representations, supporting advanced planning, transfer learning, and structural compositionality1.  
The cognitive graph operates via two distinct phases: offline optimization, during which the topological structure and transition representations are updated, and online execution, during which these structures are queried to arbitrate execution decisions1. The cognitive graph acts as a hybrid world model, deconstructing tasks across three primary operational layers6:

* **The Connector Layer:** Describes reachability, dependencies, and action sequences across the graph2.  
* **The Simulator Layer:** Evaluates dynamic operational rules, predicting future state transitions6.  
* **The Reasoner Layer:** Leverages logical relationships, semantic constraints, and causal pathways to guide plan synthesis6.

To implement this layered hierarchy, the cognitive graph structures its declarative knowledge through a strict global workspace ontology7. This global workspace decomposes agent execution into typed, auditable nodes and weighted, bi-temporal edges7. Table 1 defines the operational taxonomy of the node types that constitute the Manurella Cognitive Graph.

| Node Type | Unique Identifier Pattern | Primary Schema Attributes | Cognitive & Structural Role in the Workspace |
| :---- | :---- | :---- | :---- |
| **Domain** | dom\_\<string\> | name, description, security\_tier, governance\_scope | Defines isolation boundaries and limits permissions for agents11. |
| **Agent** | agt\_\<string\> | name, backbone\_model, temperature, system\_instructions | Resolves high-level requirements and decomposes tasks13. |
| **Subagent** | sub\_\<string\> | name, parent\_agent, specialization, context\_window | A localized execution unit optimized for focused, high-volume tasks13. |
| **Skill** | skl\_\<string\> | name, implementation\_ref, input\_schema, output\_schema | Encapsulates a reusable procedural block or local transaction flow3. |
| **Tool/MCP** | mcp\_\<string\> | server\_uri, method\_name, parameter\_json\_schema, timeout | Represents external capabilities exposed via Model Context Protocol servers15. |
| **Mode** | mod\_\<string\> | policy\_name, latency\_profile, cost\_coefficient | Governs task dispatch, optimizing between Fast and Standard pathways5. |
| **Effort** | eff\_\<string\> | level\_label, token\_budget, max\_depth, concurrency\_limit | Configures the allocation of test-time compute and orchestration limits14. |
| **Context Source** | ctx\_\<string\> | source\_type, uri, provenance\_trace, bi\_temporal\_markers | Maps memory segments, local databases, or session logs9. |
| **Eval Result** | evl\_\<string\> | metric\_name, score, confidence, timestamp | Tracks runtimes, accuracy, and token costs of executed paths18. |
| **Failure Mode** | flm\_\<string\> | breakdown\_class, diagnostic\_signature, impact\_radius | Catalogues structural failures, selection confusion, and context rot21. |
| **Routing Rule** | rtr\_\<string\> | eval\_expression, target\_node, fallthrough\_node | Codifies transitions based on contextual and performance parameters20. |
| **Research Evidence** | evd\_\<string\> | source\_citation, factual\_assertion, validation\_benchmark | Anchors system configurations to empirical research findings9. |

## **Edge Typology, Weighted Parameters, and Bi-Temporal Topology**

Nodes in the Manurella Cognitive Graph are connected by typed, directed, and dynamically weighted edges that represent operational dependencies, semantic flows, and causal connections2. In non-stationary environments, static relationships lead to outdated planning decisions, as APIs deprecate, service configurations change, or network access shifts6.  
To prevent these issues, the cognitive graph implements a bi-temporal edge model9. This model separates event time (![][image1]), which represents the period during which the relationship is factually true in the environment, from ingestion time (![][image2]), which tracks when the relationship was recorded within the platform9.  
This bi-temporal design allows the framework to reconstruct historical states (answering queries like "What was the active routing sequence prior to the update on date ![][image3]?") and supports temporal edge invalidation without deleting historical data10. Rather than executing hard deletes that destroy planning context and audit trails, obsolete or failing edges are marked as invalid by setting the end of their validity window (![][image4]) to the current timestamp10.  
Edges also possess dynamic attributes: connection strength (![][image5]), confidence level (![][image6]), and transition features7. Transition features capture four distinct dimensions that determine the affinity between connected nodes27:

* **Path Distance (![][image7]):** The topological and computational distance between nodes27.  
* **Visibility (![][image8]):** The structural reachability and visibility between nodes within the graph27.  
* **Recency (![][image9]):** The time elapsed since the connection was last successfully traversed27.  
* **Frequency (![][image10]):** The total volume of successful executions along the connection27.

Connection strength is calculated dynamically using an active inference-based utility model7:  
![][image11]  
where ![][image12] represents the normalized historical benefit (success rate or cost efficiency) of traveling from node ![][image13] to node ![][image14], and ![][image15] represents the probability of a successful transition calculated under active environment parameters7. Table 2 details the primary edge relationships within the system ontology.

| Edge Relationship | Source Node Class | Destination Node Class | Bi-Temporal Constraints | Operational Semantics and Data Flow |
| :---- | :---- | :---- | :---- | :---- |
| **orchestrates** | Agent | Subagent | Dynamic (![][image1] active) | Establishes command chains; passes system prompts and execution boundaries13. |
| **implements** | Subagent / Agent | Skill | Static (![][image16]) | Maps execution units to reusable, local procedural scripts3. |
| **utilizes** | Skill / Subagent | Tool/MCP | Dynamic (![][image1] active) | Defines permission boundaries and passes Model Context Protocol schemas11. |
| **enforces** | Domain | Agent / Tool/MCP | Invariant | Applies fine-grained security policies and isolated execution limits3. |
| **triggers** | Routing Rule | Node (Any) | Dynamic (![][image1] active) | Executes conditional transitions based on operational flags and metrics20. |
| **mitigates** | Node (Any) | Failure Mode | Dynamic (![][image1] active) | Maps active execution paths to fallback patterns for known failures21. |
| **grounds** | Context Source | Node (Any) | Bi-Temporal tracking | Feeds historical data, session logs, and facts to contextualize planning9. |
| **supports** | Research Evidence | Node / Edge (Any) | Static (![][image16]) | Validates structural parameters with empirical benchmark data9. |
| **transitions\_to** | Node (Any) | Node (Any) | Dynamic (![][image1] active) | Represents sequential progression or multi-hop paths during execution1. |

## **Cognitive Plasticity and Graph Mutation Rules**

To adapt to non-stationary environments, the cognitive graph implements dynamic topological plasticity6. Rather than relying on rigid structures, the network modifies its nodes and edges online based on execution outcomes6. These updates are governed by formal, differentiable operators that manipulate the graph's topology in real time.

### **Add Operator**

Instantiates a new node ![][image17] or directed edge ![][image18] in the active graph topology. When a new tool or routing path is registered, the Add operator creates the corresponding entities, initializing edge weights based on baseline prior distributions7:  
![][image19]  
This allows the framework to construct prior beliefs about unvisited paths28.

### **Remove Operator**

The engine avoids hard deletions to preserve audit trails and historical records9. The Remove operator executes a logical deletion by updating the bi-temporal edge properties, setting the end of the validity interval to the current timestamp:  
![][image20]  
The edge remains in the historical database but is skipped during active runtime execution passes10.

### **Merge Operator**

When the engine identifies structural redundancy (such as identical tools or skills registered under slightly different names), it merges the candidate nodes ![][image21] and ![][image22]32. The merge operation is triggered when the semantic cosine similarity of their schemas and descriptions exceeds an adaptive threshold ![][image23]22:  
![][image24]  
Upon meeting this condition, a unified node ![][image25] is created, and the corresponding incoming and outgoing edges are aggregated using a weighted average20:  
![][image26]  
The original nodes ![][image21] and ![][image22] are logically deprecated10.

### **Weaken Operator**

Reduces the structural relevance of an edge in response to performance degradation, network timeouts, or negative feedback9. The weakening mechanism applies an exponential decay function combined with a step penalty tied to the severity of the failure:  
![][image27]  
where ![][image28] is the temporal decay constant, ![][image29] is the elapsed idle time, ![][image30] is the scaling factor for registered failures, and ![][image31] is the failure metric of the registered Failure Mode node ![][image32]6.

### **Strengthen Operator**

Reinforces highly reliable trajectories, successful tool executions, and accurate classifications9. When an execution path returns a positive evaluation score, the connection strength is updated asymptotically toward unity:  
![][image33]  
where ![][image34] represents the learning rate, and ![][image35] is the normalized confidence and quality score returned by the corresponding Eval Result node ![][image36]18.

### **Deprecate Operator**

Applies to nodes that fall below a minimum utilization threshold ![][image37] or are flagged as structurally hazardous12. Deprecation marks the target node with a negative trust index, immediately setting the end of the validity window for all connecting edges to the current timestamp (![][image38]) and redirecting future queries to fallback endpoints12.

### **Memory Consolidation**

To manage bounded memory growth and optimize storage, the framework runs a periodic consolidation process5. By default, this runs as a weekly background process (e.g., scheduled at Sunday 3:00 AM to minimize peak computational and API costs)12. During consolidation, the engine compresses long-term episodic memory graphs into simplified parametric states5.  
Weak edges (![][image39]) are pruned, redundant execution chains are merged, and verified assertions are distilled into the core model5. A rolling window (such as a 50-event risk window) is maintained separately, ensuring that critical security events and failure histories are preserved during compaction12.

## **Real-Time Dynamic Routing and Runtime Orchestration**

During execution, the Manurella framework uses the cognitive graph to route, contextualize, and execute user requests13. Execution is structured as an adaptive traversal through the ontology, dynamically adjusting its latency profile and computational footprint5.

### **Graph-Based Query Resolution vs. Raw API Calls**

To minimize token consumption and avoid context window saturation, the system prioritizes schema-driven graph queries over raw, multi-step API lookups11. In traditional architectures, an agent must discover, retrieve, and parse raw API responses, which can consume hundreds of thousands of tokens and introduce significant latency11.  
The Manurella framework addresses this by using schema annotations as a routing index over the graph11. When a query is ingested, a type selector identifies the required entity types and relationships, compiling them into a structured query (such as Harness Query Language or Cypher)9. This query is executed directly against the cognitive graph, returning focused, aggregated results11. Table 3 compares the token overhead and execution steps of these two approaches.

| Architectural Dimension | Traditional MCP / Raw API Path | Manurella Schema-Driven Graph Path |
| :---- | :---- | :---- |
| **API Discovery Overhead** | Resolves endpoints dynamically across multiple modules (\~2,000 tokens)11. | The Type Selector identifies target schemas and relationship indexes (\~4,000 tokens)11. |
| **Data Retrieval Footprint** | Retrieves full objects with unneeded fields and metadata (\~100,000–150,000 tokens)11. | Executes structured, focused queries directly against the graph store11. |
| **Correlation & Join Logic** | The model reconstructs joins and identifies relationships within the context window (\~50,000–80,000 tokens)11. | Relationships are explicitly defined and joined natively in the graph (\~2,000 tokens)11. |
| **Synthesis & Formatting** | Compiles unstructured payloads into a final response (\~30,000–50,000 tokens)11. | Summarizes clean, pre-aggregated query results (\~3,000 tokens)11. |
| **Typical Total Token Cost** | **\~180,000 – 340,000 tokens** \[cite: 11\] | **\~9,000 – 11,000 tokens** \[cite: 11\] |

### **Runtime Traversal and Cognitive Modes**

The orchestrator selects the appropriate routing mode based on the complexity of the incoming query and active performance requirements14:

1. **Fast Mode (Low Latency):** Bypasses multi-hop graph planning for simple, high-frequency, or repetitive requests5. The system queries local vector stores or cached execution patterns, achieving response latencies under 300ms10.  
2. **Standard Mode (Deliberate Planning):** Used when the query requires multi-step composition or crosses multiple domains1. The system generates an explicit execution plan, traverses the cognitive graph, and dynamically invokes specialized subagents2.

Dynamic routing introduces a lightweight classification step before execution, which can add a latency penalty of 50ms to 200ms per decision14. To mitigate this overhead, the system uses hybrid routing14.  
The primary planner (such as a high-capacity reasoning model) defines the global task structure once, and then maps individual steps to faster execution models or local scripts14. Dynamic model selection is applied at the step level, reserving high-capacity models for complex planning and routing simpler, high-volume tasks to lower-cost models13.

### **Computational Effort Allocation**

Computational effort is scaled dynamically across six structured levels14. This categorization allows the framework to trade off execution quality, token budgets, and latency limits based on the task complexity14. Table 4 defines these effort profiles.

| Effort Level | Token Budget | Max Path Depth | Collaboration Pattern | Primary Use Cases |
| :---- | :---- | :---- | :---- | :---- |
| **Low** | Up to 4K tokens14 | 1 Hop | Single Agent (no delegation)21 | Simple file reads, single API calls, and cached lookups12. |
| **Medium** | 4K to 32K tokens14 | 2 Hops | Static Coordinator \+ Implementer14 | Local file modifications, basic validation, and schema generation14. |
| **High** | 32K to 128K tokens14 | 4 Hops | Dynamic Routing with verification | Multi-hop analysis, cross-module data joins, and plan synthesis11. |
| **Extra High** | 128K to 256K tokens | 6 Hops | Verification with human gatekeepers | Refactoring large codebases and compiling compliance audits14. |
| **Max** | 256K to 1M tokens | 10 Hops | Autonomous Multi-Agent Consensus21 | Dynamic tool generation and multi-file code execution2. |
| **Ultra** | Bounded by convergence | Infinite | Calibrated Oversight with parallel debate | Multi-agent research tasks and clinical diagnostic validation3. |

### **Graph Neural Network (GNN) Routing and Aggregation**

For complex questions, the system formulates agent selection as a graph-guided routing problem20. The active query, context entities, and available agent profiles are embedded into a unified subgraph20. A heterogeneous Graph Neural Network (GNN) propagates information across node types to produce a task-aware routing distribution over agents20.  
Instead of relying on a single best agent, the framework uses soft supervision to distribute the task across multiple complementary agents20. The system aggregates their outputs using a weighted vote based on historical performance weights, balancing their individual strengths to generate the final prediction20.

## **Closed-Loop Evaluation and Adaptive Policy Tuning**

The Manurella Cognitive Graph operates as a closed-loop system where execution outcomes continuously shape planning policies20. Rather than relying on static configurations, the network adjusts model routing, agent selection, and tool allocation based on performance evaluations14. This adaptation mitigates three critical failure modes:

* **Classifier Drift:** Occurs when an LLM-based routing model relies on obsolete task distributions or outdated prompt patterns, causing incorrect tool or model dispatch30.  
* **Context Rot:** Occurs when a model's working memory becomes saturated with irrelevant tools or redundant schemas, degrading the attention mechanism and increasing hallucinations22.  
* **Coordination-Harm:** Occurs when a multi-agent consensus pattern is applied to deterministic, single-step tasks, introducing unnecessary latency, token costs, and compounding citation errors14.

The closed-loop architecture addresses these vulnerabilities through specific dynamic feedback mechanisms:

\[User Input Query\]  
        │  
        ▼  
┌────────────────────────────────────────┐  
│        Type / Domain Selector          │  
└────────────────────────────────────────┘  
        │  
        ├────────────────────────────────────┐  
        ▼ (Cost/Billing/Sec)                 ▼ (Complex Task)  
┌────────────────────────────────────────┐ ┌────────────────────────────────────────┐  
│     Harness Query Language (HQL)       │ │          Cognitive Graph RAG           │  
│        (Tier 1 Schema Graph)           │ │          (Multi-hop Traversal)         │  
└────────────────────────────────────────┘ └────────────────────────────────────────┘  
        │                                            │  
        ▼                                            ▼  
┌───────────────────────────────────────────────────────────────────────────────────┐  
│                           Central Orchestrator Agent                              │  
│                (Applies Conformal Calibration & Routing Rules)                    │  
└───────────────────────────────────────────────────────────────────────────────────┘  
        │  
        ├────────────────────────────────────┐  
        ▼ (Meets Thresholds)                 ▼ (Violates/Fails)  
┌────────────────────────────────────────┐ ┌────────────────────────────────────────┐  
│        Subagent Execution Loop         │ │            Failure Mode Node           │  
│  (Keeps active tools \< 10-20 limit)    │ │   (Triggers Weaken & Deprecate Rules)  │  
└────────────────────────────────────────┘ └────────────────────────────────────────┘  
        │                                            │  
        ▼                                            ▼  
┌────────────────────────────────────────┐ ┌────────────────────────────────────────┐  
│            Eval Result Node            │ │        Dynamic Fallback Routing        │  
│    (Triggers Strengthen Mutations)     │ │        (Escalates to High-Effort)      │  
└────────────────────────────────────────┘ └────────────────────────────────────────┘

### **Mitigating Coordination-Harm**

Upon execution completion, the system compares the performance of multi-agent configurations against single-agent baselines across predefined task domains21. If structured compliance checks or deterministic mathematical steps yield lower quality or higher error rates under multi-agent synthesis compared to a direct, single-agent run, the system flags a coordination-harm exception21.  
This evaluation triggers a mutation in the corresponding Routing Rule node: the edge connecting the parent task to the multi-agent Agent node is weakened (![][image40]), and a new edge is strengthened (![][image41]) routing directly to a single, optimized Subagent or deterministic Skill14. For deterministic tasks, the system escalates to multi-agent patterns only when local confidence drops below a critical threshold21.

### **Dynamic Tool Thresholding and Schema Management**

To prevent context rot and selection confusion, the cognitive system enforces a dynamic schema limit22. Empirical benchmarks show that model execution reliability degrades significantly when a model must choose from more than 10 to 20 tools within a single context window22. To resolve this, the cognitive graph acts as a tool routing layer22.  
When the active tool pool for an agent context exceeds 15 tools, the graph engine executes a dynamic clustering mutation22. It groups the tools based on their semantic domain annotations and creates specialized sub-graphs11. At runtime, the central orchestrator is only presented with high-level domain routers or lightweight classifiers14. The actual tool schemas are lazy-loaded on demand, ensuring that no individual execution context is exposed to schema noise22.  
If an Eval Result captures a tool selection error or parameter hallucination, the system immediately tightens the schema limits for that session, reducing the active tool context to a maximum of 10 tools and routing through explicit subagent boundaries22.

### **Conformal Calibration and Drift Control**

The system implements Calibrated Collective Oversight to govern the dynamic adjustments of routing policies18. When classifier drift is detected—such as when the routing model's predictions shift toward a single-dimensional choice regardless of task complexity—a built-in drift monitor activates18.  
The system applies Conformal Decision Theory to calculate a dynamic risk-penalty multiplier based on empirical execution metrics18. If the error rate on validation benchmarks exceeds a user-specified threshold, the system restricts the trust regions of the active routing models18. This restriction:

* Forces the immediate reweighting of preference parameters18.  
* Limits further exploratory transitions along unverified edges18.  
* Triggers an automatic fallback to local, deterministic rule-based edges until stable validation baselines are restored18.

## **System Security, Sandboxing, and Governance**

Because autonomous agents can construct tools and execute local code, enforcing security boundary isolation is a critical requirement3. The Manurella framework implements a zero-trust execution environment to mitigate risks such as remote code execution, unauthorized file modifications, and prompt injection3.

\[System Input\] ──► \[Dual-LLM Quarantine\] ──► \[Policy.toml Validation\] ──► \[Isolated Sandbox Execution\]

### **Zero-Permissions-By-Default Model**

Agents begin with zero system permissions3. Access to directories, external APIs, and local execution resources is blocked by default and must be explicitly configured3. Any request to increase permissions must provide an audit rationale, which is logged for administrator review3.

### **Out-of-Context Policy Enforcement**

To prevent prompt injection or context compression from overriding security controls, policies are stored outside the agent's context window3. A static configuration file (policy.toml) is loaded from disk before every action and evaluated by an independent policy engine3.  
This ensures that security limits (such as token spend caps, file system access boundaries, and binary constraints) remain active even if the agent's context window becomes saturated3.

### **Isolated Sandboxing and Verification**

All execution tasks, code generation, and package updates run inside an isolated sandbox environment3. This sandbox separates the host system from the agent's workspace, restricting network access, file write operations, and system process execution to authorized paths3.  
Before any code is executed or a skill is registered, the code is evaluated by an isolated runtime checker, preventing compile-time or runtime exploits3.

### **Dual-LLM Quarantine Architecture**

To protect against prompt injection, raw inputs from untrusted sources (such as external APIs or messaging channels) do not enter the main agent's planning loop12. Incoming data is routed through a dual-model quarantine layer12:

* **The Quarantine Guard (Local Model):** A small local model evaluates the input for injection payloads or formatting anomalies, running at low latency12.  
* **The Sanitized Gateway:** Once verified, the sanitized payload is converted into structured parameters before being passed to the main orchestrator agent12.

## **Visual Rendition and Force-Directed Mind Mapping**

To support debugging and auditability, the cognitive graph can be rendered as an interactive, force-directed mind map2. This visualization maps topological metrics to visual attributes, turning raw logs into an inspectable, explorable interface35.

### **Physics Engine Dynamics**

The visualization layout is calculated in real time using a force-directed model:

1. **Electrostatic Repulsion (![][image42]):** All nodes act as charged particles, repelling each other to prevent overlap:  
   ![][image43]  
   where ![][image44] is the distance between nodes, and ![][image45] is the repulsion coefficient.  
2. **Edge Spring Tension (![][image46]):** Active edges act as springs, pulling related nodes together:  
   ![][image47]  
   where ![][image48] is the target edge length, and ![][image49] represents the edge tension. Tension scales with the connection strength (![][image50]), placing stronger relationships closer together in the visualization35.  
3. **Frictional Dampening:** A dampening factor is applied at each simulation step, stabilizing the layout and preventing jitter.

### **Visual Attribute Mapping**

Visual styling is mapped to node properties to reflect their role and status in the system35. Table 5 defines these visual mapping rules.

| Visual Attribute | Target Metric | Visual Range / Behavior | Operational Meaning |
| :---- | :---- | :---- | :---- |
| **Node Size** | Degree Centrality | ![][image51] to ![][image52] diameter | Reflects structural importance; domain hubs and primary agents appear larger13. |
| **Edge Thickness** | Connection Strength (![][image50]) | ![][image53] to ![][image51] width | Represents connection utility; highly active paths are rendered with thicker lines9. |
| **Edge Style** | Edge Temporal Status | Solid, Dashed, or Dotted lines | Solid represents active paths; dashed lines indicate deprecated or inactive paths10. |
| **Edge Color** | Edge Weight State | High ![][image54]: Green; Low ![][image54]: Yellow | Provides an immediate visual indicator of path health and reliability9. |
| **Active Glow** | Execution Step Tracking | Animated glowing pulse | Highlights the currently executing node and active transition in real time35. |
| **Failure Highlight** | Failure Mode Event | Steady red glow | Nodes associated with a failure mode flash red to assist with diagnostics21. |

The visual schema uses a standardized color-coding matrix to classify node types35. Domains are colored in deep purple, orchestrator agents in blue, and subagents in teal13. Reusable skills are rendered in green, external Model Context Protocol tools in orange, effort levels in yellow, and failure modes in crimson red3.

## **Serialization Topology: Hybrid Format Matrix**

Managing an evolving cognitive graph requires segregating machine-readable structural states from human-readable documentation and logs11. Structured datasets (nodes, mathematical weights, temporal intervals, schemas) are stored in JSON/YAML for serialization and deserialization10. Descriptive context, audit logs, and diagnostic evaluations are stored in Markdown to support manual human-in-the-loop overrides and administrative audits12. Table 6 defines this serialization mapping.

| Component / Subsystem | Serialization Target | Primary Schema / Structure | Systemic Justification & Performance Impact |
| :---- | :---- | :---- | :---- |
| **Global Graph Topology** | JSON | Unified node index, typed vertices, and schema properties13. | Loaded into memory for fast indexing, neighbor traversal, and distance metrics10. |
| **Dynamic Edge State** | JSON | Directed pointer arrays, connection strengths, bi-temporal markers (![][image55])9. | Updated continuously by learning algorithms; must serialize quickly without locking6. |
| **System Security Policies** | YAML (policy.toml) | Strict key-value properties, sandbox configurations, destination rules3. | Evaluated on disk before execution to prevent memory corruption or injection exploits3. |
| **Execution Trace Logs** | Markdown | Action-observation sequences, model-to-model messages, error context templates18. | Retains developer-readable records of planning steps and decisions18. |
| **Audit Trails & Provenance** | Markdown | Ingestion documents, source lineage statements, confidence ratings, verified assertions9. | Supports explanation generation and corporate compliance audits9. |
| **Governance Overrides** | Markdown | Direct weight overrides, node deprecations, policy updates, and manual audit signatures. | Enables human operators to inspect, override, or approve high-risk actions12. |

## **Production-Grade Frontend Development Use Case**

To demonstrate the application of this architecture, a real-world frontend development task is formalized: **"Construct a responsive user login interface with client-side reactive verification and a network API integration for authentication that falls back to localized caching during network timeouts."**  
This scenario requires a domain boundary, dynamic orchestration, tool selection constraints, latency optimization, failure mitigations, and performance-based updates.

### **Declarative Graph Schema (YAML)**

This YAML configuration represents the serialized blueprint of the cognitive graph, establishing the nodes and edge relationships before execution13.

YAML  
version: "2.0"  
graph\_id: "cog\_graph\_frontend\_login\_form"  
metadata:  
  created\_at: "2026-03-30T09:00:00Z"  
  framework: "Manurella"

nodes:  
  \- id: "dom\_frontend"  
    type: "Domain"  
    properties:  
      name: "Frontend UI Development"  
      description: "Functional boundary for React interface design and validation"  
      security\_tier: "restricted\_client\_sandbox"

  \- id: "agt\_ui\_orchestrator"  
    type: "Agent"  
    properties:  
      name: "UI Orchestrator Agent"  
      backbone\_model: "claude-sonnet-4-6"  
      temperature: 0.2  
      system\_instructions: "Coordinate UI generation, local state management, and validation."

  \- id: "sub\_state\_validator"  
    type: "Subagent"  
    properties:  
      name: "State Validation Analyst"  
      parent\_agent: "agt\_ui\_orchestrator"  
      specialization: "Local client-side state validation and error compiling"  
      context\_window: 16384

  \- id: "sub\_api\_synchronizer"  
    type: "Subagent"  
    properties:  
      name: "API Sync Bridge"  
      parent\_agent: "agt\_ui\_orchestrator"  
      specialization: "Handling asynchronous API transmissions and caching fallbacks"  
      context\_window: 16384

  \- id: "skl\_reactive\_validation"  
    type: "Skill"  
    properties:  
      name: "Client-side Schema Validation"  
      implementation\_ref: "file:///usr/local/manurella/skills/reactive\_validator.py"  
      input\_schema:  
        type: "object"  
        properties:  
          username: { "type": "string" }  
          password: { "type": "string" }  
      output\_schema:  
        type: "object"  
        properties:  
          is\_valid: { "type": "boolean" }  
          errors: { "type": "array" }

  \- id: "mcp\_axios\_generator"  
    type: "Tool/MCP"  
    properties:  
      server\_uri: "http://localhost:8012/mcp/http\_client\_generator"  
      method\_name: "generate\_api\_client"  
      parameter\_json\_schema:  
        type: "object"  
        properties:  
          endpoint\_url: { "type": "string" }  
          retry\_limit: { "type": "integer" }  
          caching\_fallback: { "type": "boolean" }  
      timeout: 5000

  \- id: "mod\_fast\_mode"  
    type: "Mode"  
    properties:  
      policy\_name: "Fast Mode"  
      latency\_profile: "sub\_100ms"  
      cost\_coefficient: 0.1

  \- id: "mod\_standard\_mode"  
    type: "Mode"  
    properties:  
      policy\_name: "Standard Mode"  
      latency\_profile: "medium\_delay"  
      cost\_coefficient: 1.0

  \- id: "eff\_medium"  
    type: "Effort"  
    properties:  
      level\_label: "Medium Effort"  
      token\_budget: 32768  
      max\_depth: 3  
      concurrency\_limit: 2

  \- id: "ctx\_validated\_credentials"  
    type: "Context Source"  
    properties:  
      source\_type: "session\_cache"  
      uri: "mem://session/current\_auth\_state"  
      provenance\_trace: "user\_input\_verification"

  \- id: "rtr\_dispatch\_rule"  
    type: "Routing Rule"  
    properties:  
      eval\_expression: "context.has\_async\_network\_calls \== false"  
      target\_node: "mod\_fast\_mode"  
      fallthrough\_node: "mod\_standard\_mode"

  \- id: "flm\_network\_timeout"  
    type: "Failure Mode"  
    properties:  
      breakdown\_class: "tool\_network\_failure"  
      diagnostic\_signature: "HTTP\_TIMEOUT\_EXCEEDED"  
      impact\_radius: "component\_offline"

edges:  
  \- id: "edg\_orch\_validator"  
    source: "agt\_ui\_orchestrator"  
    target: "sub\_state\_validator"  
    relationship: "orchestrates"  
    properties:  
      weight: 0.95  
      t\_valid\_start: "2026-03-30T09:00:00Z"

  \- id: "edg\_orch\_sync"  
    source: "agt\_ui\_orchestrator"  
    target: "sub\_api\_synchronizer"  
    relationship: "orchestrates"  
    properties:  
      weight: 0.90  
      t\_valid\_start: "2026-03-30T09:00:00Z"

  \- id: "edg\_impl\_validation"  
    source: "sub\_state\_validator"  
    target: "skl\_reactive\_validation"  
    relationship: "implements"  
    properties:  
      weight: 1.00  
      t\_valid\_start: "2026-03-30T09:00:00Z"

  \- id: "edg\_tool\_axios"  
    source: "sub\_api\_synchronizer"  
    target: "mcp\_axios\_generator"  
    relationship: "utilizes"  
    properties:  
      weight: 0.85  
      t\_valid\_start: "2026-03-30T09:00:00Z"

  \- id: "edg\_enforce\_frontend"  
    source: "dom\_frontend"  
    target: "agt\_ui\_orchestrator"  
    relationship: "enforces"  
    properties:  
      weight: 1.00  
      t\_valid\_start: "2026-03-30T09:00:00Z"

  \- id: "edg\_mitigate\_timeout"  
    source: "sub\_api\_synchronizer"  
    target: "flm\_network\_timeout"  
    relationship: "mitigates"  
    properties:  
      weight: 0.70  
      t\_valid\_start: "2026-03-30T09:00:00Z"

### **Runtime Trace and Graph Adaptation (Markdown)**

This human-readable log records the step-by-step execution details and structural graph mutations observed during the session18.

# **Session Execution Log: Reactive Login Component**

*Session ID: ses\_frontend\_build\_react\_4402*  
*Timestamp: 2026-03-30T10:15:22Z*  
*Orchestrator: agt\_ui\_orchestrator*

## **Step 1: Processing User Goal Input**

The user initiated a task with the following instruction:  
"Construct a responsive user login interface with client-side reactive verification and a network API integration for authentication that falls back to localized caching during network timeouts."  
Upon parsing this instruction, the system logged the following execution trace:

* **Semantic Parsers Activated:** Identified primary domains: dom\_frontend11.  
* **Active Agent Selection:** Assigned agt\_ui\_orchestrator as the primary coordinator13.  
* **Initial Path Evaluation:** Checked context structures. The system detected that the request contains asynchronous actions (calling a remote authentication server).  
* **Active Routing Evaluation:**  
  * Evaluated rtr\_dispatch\_rule20.  
  * Expression: context.has\_async\_network\_calls \== false returned false.  
  * **Decision:** Fall back to mod\_standard\_mode14.  
* **Effort Profile Selected:** eff\_medium assigned (up to 32K token context window)14.

## **Step 2: Executing Client-Side Validation (Fast Pathway)**

The orchestrator first processed the reactive validation form elements. Because this step can run locally without external service calls, the system routed the action through sub\_state\_validator13.

* **Subagent Invoked:** sub\_state\_validator13.  
* **Skill Activated:** skl\_reactive\_validation16.  
* **Local Processing Trace:**  
  * Compiled React state bindings for input fields.  
  * Generated pattern-matching validation scripts for formatting constraints.  
* **Validation Output:** Execution successful. Returned code template for reactive verification.  
* **Dynamic Reinforcement:**  
  * Triggered Strengthen operator on edg\_orch\_validator and edg\_impl\_validation6.  
  * New edge weight calculated:  
    ![][image56]

## **Step 3: API Integration and Failure Event**

The system then prepared to generate the network interface using sub\_api\_synchronizer to integrate the remote authentication bridge13.

* **Subagent Invoked:** sub\_api\_synchronizer13.  
* **Tool Called via MCP:** mcp\_axios\_generator method generate\_api\_client with parameters:  
  JSON  
  {  
    "endpoint\_url": "https://api.auth.internal/v1/login",  
    "retry\_limit": 3,  
    "caching\_fallback": true  
  }

* **Sandbox Status:** Active execution.  
* **System Event Error:** The external authentication gateway did not respond within the 5000ms threshold17. The isolated compiler returned a connection failure, triggering a known failure node21.  
* **Failure Node Activated:** flm\_network\_timeout21.

## **Step 4: Closed-Loop Graph Mutation**

Following the connection timeout, the graph engine activated its closed-loop feedback rules to update its planning topology and mitigate the failure6.

### **Incurring the Weaken Mutation**

The system applied the Weaken operator to the edge connecting sub\_api\_synchronizer to mcp\_axios\_generator due to the network timeout6.

* **Mathematical Edge Decay:**  
  ![][image57]  
* **Result:** The connection weight dropped from ![][image58] to ![][image59], signaling that this path has degraded in reliability7.

### **Dynamic Path Re-Routing and Local Caching Activation**

* **Dynamic Rerouting Triggered:** Because W\_{\\text{sync}\\to\\text{axios}} fell below the stability threshold (![][image60]), agt\_ui\_orchestrator searched for alternate paths connected to mitigation nodes21.  
* **Pathway Discovered:** Found fallback path mapping to local storage cache mechanisms.  
* **Graph Adaptation Action:** The compiler generated code injecting local\_storage caching logic into the login component state, storing the login payload when offline and syncing it when connectivity is restored12.  
* **New Node Addition:**  
  * Created ctx\_local\_sync\_queue under Context Source to store offline verification queues12.  
  * Created dynamic edge edg\_fallback\_sync connecting sub\_api\_synchronizer to ctx\_local\_sync\_queue.  
  * Initialized connection strength: ![][image61]7.

## **Step 5: Final Evaluation Output**

The compiled component code was verified against local test cases.

JavaScript  
// Output react component with dynamic sync state  
import React, { useState, useEffect } from 'react';  
import axios from 'axios';

export default function LoginForm() {  
  const \[username, setUsername\] \= useState('');  
  const \[password, setPassword\] \= useState('');  
  const \[errors, setErrors\] \= useState({});  
  const \[syncStatus, setSyncStatus\] \= useState('online');

  const validateForm \= () \=\> {  
    let localErrors \= {};  
    if (\!username.includes('@')) localErrors.username \= "Invalid email format";  
    if (password.length \< 8) localErrors.password \= "Password must be at least 8 characters";  
    setErrors(localErrors);  
    return Object.keys(localErrors).length \=== 0;  
  };

  const handleSubmit \= async (e) \=\> {  
    e.preventDefault();  
    if (\!validateForm()) return;

    const payload \= { username, password, timestamp: new Date().toISOString() };

    try {  
      setSyncStatus('syncing');  
      await axios.post('https://api.auth.internal/v1/login', payload, { timeout: 5000 });  
      setSyncStatus('success');  
    } catch (error) {  
      // Offline fallback generated dynamically by the cognitive graph mitigation pathway  
      console.warn("Primary authentication gateway offline. Preserving payload locally.", error);  
      const queue \= JSON.parse(localStorage.getItem('auth\_sync\_queue') || '\[\]');  
      queue.push(payload);  
      localStorage.setItem('auth\_sync\_queue', JSON.stringify(queue));  
      setSyncStatus('offline\_cached');  
    }  
  };

  return (  
    \<form onSubmit\={handleSubmit} className\="p-6 max-w-sm mx-auto bg-white rounded-xl shadow-md space-y-4"\>  
      \<div\>  
        \<label className\="block text-sm font-medium text-gray-700"\>Email Address\</label\>  
        \<input   
          type\="text"   
          value\={username}   
          onChange\={(e) \=\> setUsername(e.target.value)}  
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"  
        /\>  
        {errors.username && \<p className\="text-red-500 text-xs mt-1"\>{errors.username}\</p\>}  
      \</div\>  
      \<div\>  
        \<label className\="block text-sm font-medium text-gray-700"\>Password\</label\>  
        \<input   
          type\="password"   
          value\={password}   
          onChange\={(e) \=\> setPassword(e.target.value)}  
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"  
        /\>  
        {errors.password && \<p className\="text-red-500 text-xs mt-1"\>{errors.password}\</p\>}  
      \</div\>  
      \<button type\="submit" className\="w-full py-2 px-4 bg-blue-500 text-white rounded-md hover:bg-blue-600"\>  
        Sign In  
      \</button\>  
      \<div className\="text-center text-xs text-gray-500 mt-2"\>  
        Status: {syncStatus}  
      \</div\>  
    \</form\>  
  );  
}

* **Final Output Validation:** Form rendered and fallback logic verified locally.  
* **Evaluation Status:** Successful with fallback mechanism12.  
* **Closed-loop Update Complete:** The modified cognitive graph state has been serialized to active disk memory, ensuring subsequent planning sessions prioritize offline validation safeguards6.

#### **Works cited**

1. Cognitive Graphs: Representational Substrates for Planning \- PMC \- NIH, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12520196/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12520196/)  
2. Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects, [https://www.computer.org/csdl/magazine/ex/2026/02/11479408/2fzppK5pFQY](https://www.computer.org/csdl/magazine/ex/2026/02/11479408/2fzppK5pFQY)  
3. Orchestrating Self-Evolving Agents with CrewAI and NVIDIA NemoClaw, [https://blog.crewai.com/orchestrating-self-evolving-agents-with-crewai-and-nvidia-nemoclaw/](https://blog.crewai.com/orchestrating-self-evolving-agents-with-crewai-and-nvidia-nemoclaw/)  
4. Humans can navigate complex graph structures acquired during latent learning \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9201735/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9201735/)  
5. MemVerse: Multimodal Memory for Lifelong Learning Agents \- arXiv, [https://arxiv.org/html/2512.03627v2](https://arxiv.org/html/2512.03627v2)  
6. Graph World Models: Concepts, Taxonomy, and Future Directions \- arXiv, [https://arxiv.org/html/2604.27895v1](https://arxiv.org/html/2604.27895v1)  
7. Beyond the Black Box: A Cognitive Architecture for Explainable and Aligned AI \- arXiv, [https://arxiv.org/html/2512.03072v1](https://arxiv.org/html/2512.03072v1)  
8. A hierarchical active inference model of spatial alternation tasks and the hippocampal-prefrontal circuit \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11564537/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11564537/)  
9. Context Graph Tools Compared: Governance, MCP, Portability (2026) \- Atlan, [https://atlan.com/know/context-graph/context-graph-tools-compared/](https://atlan.com/know/context-graph/context-graph-tools-compared/)  
10. Graphiti: Knowledge graph memory for an agentic world \- Neo4j, [https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/)  
11. Why Harness AI Uses a Knowledge Graph, Not Raw APIs, [https://www.harness.io/blog/why-harness-ai-uses-knowledge-graph](https://www.harness.io/blog/why-harness-ai-uses-knowledge-graph)  
12. I built an AI agent after the OpenClaw mess — zero permissions by default, runs free on Ollama \- Reddit, [https://www.reddit.com/r/AI\_Agents/comments/1ry8x15/i\_built\_an\_ai\_agent\_after\_the\_openclaw\_mess\_zero/](https://www.reddit.com/r/AI_Agents/comments/1ry8x15/i_built_an_ai_agent_after_the_openclaw_mess_zero/)  
13. Agentic AI use case: Multimodal GraphRAG resource orchestration | Cloud Architecture Center, [https://docs.cloud.google.com/architecture/agentic-ai-multimodal-graph-rag-resource-orchestration](https://docs.cloud.google.com/architecture/agentic-ai-multimodal-graph-rag-resource-orchestration)  
14. Best AI Model for Coding Agents in 2026: A Routing Guide, [https://www.augmentcode.com/guides/ai-model-routing-guide](https://www.augmentcode.com/guides/ai-model-routing-guide)  
15. Enhancing Model Context Protocol (MCP) with Context-Aware Server Collaboration \- arXiv, [https://arxiv.org/html/2601.11595v2](https://arxiv.org/html/2601.11595v2)  
16. Model Context Protocol (MCP) \- Mendix Docs, [https://docs.mendix.com/agents/mcp/](https://docs.mendix.com/agents/mcp/)  
17. What is Model Context Protocol (MCP)? \- Neo4j, [https://neo4j.com/blog/genai/what-is-model-context-protocol-mcp/](https://neo4j.com/blog/genai/what-is-model-context-protocol-mcp/)  
18. Agentic Retrieval Updates \- Scouts by Yutori, [https://scouts.yutori.com/9ef0be1d-714f-4a27-b730-c3c27123d588](https://scouts.yutori.com/9ef0be1d-714f-4a27-b730-c3c27123d588)  
19. Context Graphs | Hands-on AI Playbook, [https://handsonai.info/agentic-building-blocks/context/context-graphs/](https://handsonai.info/agentic-building-blocks/context/context-graphs/)  
20. AgentRouter: A Knowledge-Graph-Guided LLM Router for Collaborative Multi-Agent Question Answering \- arXiv, [https://arxiv.org/html/2510.05445v1](https://arxiv.org/html/2510.05445v1)  
21. Dynamic Coordination Strategy Selection for Enterprise Multi-Agent Systems \- arXiv, [https://arxiv.org/html/2606.00804v2](https://arxiv.org/html/2606.00804v2)  
22. The Over-Tooled Agent Problem: Why More Tools Make Your LLM Dumber \- TianPan.co, [https://tianpan.co/blog/2026-04-19-over-tooled-agent-problem](https://tianpan.co/blog/2026-04-19-over-tooled-agent-problem)  
23. Telecom AI Agents: Ticket Routing and Issue Summaries \- Suhas Bhairav, [https://suhasbhairav.com/blog/ai-agents-for-telecom-ticket-routing-network-issue-summaries-and-customer-support](https://suhasbhairav.com/blog/ai-agents-for-telecom-ticket-routing-network-issue-summaries-and-customer-support)  
24. My agent knows EXACTLY what it did a week ago. Thanks to "hmem"-MCP \- Reddit, [https://www.reddit.com/r/vibecoding/comments/1rjlki3/my\_agent\_knows\_exactly\_what\_it\_did\_a\_week\_ago/](https://www.reddit.com/r/vibecoding/comments/1rjlki3/my_agent_knows_exactly_what_it_did_a_week_ago/)  
25. Mem0 vs Zep (Graphiti): AI Agent Memory Compared (2026) \- Vectorize, [https://vectorize.io/articles/mem0-vs-zep](https://vectorize.io/articles/mem0-vs-zep)  
26. Graphiti: Giving AI a Real Memory—A Story of Temporal Knowledge Graphs \- Presidio, [https://www.presidio.com/technical-blog/graphiti-giving-ai-a-real-memory-a-story-of-temporal-knowledge-graphs/](https://www.presidio.com/technical-blog/graphiti-giving-ai-a-real-memory-a-story-of-temporal-knowledge-graphs/)  
27. Cognitive Path Planning With Spatial Memory Distortion \- IEEE Computer Society, [https://www.computer.org/csdl/journal/tg/2023/08/09745822/1CbVo1JSjtK](https://www.computer.org/csdl/journal/tg/2023/08/09745822/1CbVo1JSjtK)  
28. Learning Dynamic Cognitive Map with Autonomous Navigation \- arXiv, [https://arxiv.org/html/2411.08447v1](https://arxiv.org/html/2411.08447v1)  
29. Agentic RAG in ZBrain: How intelligent retrieval is powering enterprise-ready AI, [https://zbrain.ai/agentic-rag/](https://zbrain.ai/agentic-rag/)  
30. LLM routing strategies for quality in AI applications \- n8n Blog, [https://blog.n8n.io/llm-routing/](https://blog.n8n.io/llm-routing/)  
31. Metareasoning, Opportunistic Exploration, and Explanations for Autonomous Indoor Navigation \- CUNY Academic Works, [https://academicworks.cuny.edu/cgi/viewcontent.cgi?article=5435\&context=gc\_etds](https://academicworks.cuny.edu/cgi/viewcontent.cgi?article=5435&context=gc_etds)  
32. Generative agents empowering human mobility computing \- The Innovation, [https://www.the-innovation.org/article/doi/10.59717/j.xinn-inform.2026.100020](https://www.the-innovation.org/article/doi/10.59717/j.xinn-inform.2026.100020)  
33. Proceedings of the Annual Meeting of the Cognitive Science Society \- eScholarship.org, [https://escholarship.org/uc/cognitivesciencesociety](https://escholarship.org/uc/cognitivesciencesociety)  
34. Modella AI, [https://www.modella.ai/](https://www.modella.ai/)  
35. Mindscape: A Live Cognitive Graph for Hermes Agent \- DEV Community, [https://dev.to/southy404/mindscape-a-live-cognitive-graph-for-hermes-agent-2b0h](https://dev.to/southy404/mindscape-a-live-cognitive-graph-for-hermes-agent-2b0h)  
36. Knowledge Graphs for LLMs: GraphRAG, Reasoning Ontologies & MCP Workflows — InfraNodus, [https://infranodus.com/docs/knowledge-graphs-for-llms](https://infranodus.com/docs/knowledge-graphs-for-llms)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAAWCAYAAACosj4+AAACE0lEQVR4Xu2VS0jUURTGv0ihUNRIFB9QK0GKAl8ghCAIbqKFCS4iwYW4sU2KohAIIq4MUjFciQtRF0IbIcHFSAuzXVAoRKARiKs2uRIf3+e517kzBuM44YDMBz+4/3Pu65xz7/0DGWV0zZVHGsjteEc6VEa2HWqnXU/IAVkmt+J8aVE/OSbd8Y6rVi4pIbtkizxw3/9DyWY6pv8RmSM3QuMlVUgOyQyi82WTV+SR7xRI/VWd8dAoQ1doSFHfyYvg+zHZI88CW6ifpMV/5JB9Un3mTl2/kNx8O6TSf2jXYXrLyU1SRT6QHySLvCefSb7r+5REyCxZJBUwyRfOp/4bZCyw3ScLsLEriCvXCKLp1YC3sEmGSRFsUamNbJJi8px8Jfec7zcsEOkOYsvVA7vFq7BqSBqrOaSHiO1/urt62Ga06AQsgkZnVzol3b4p2G34BlvEK3y/VCpfLtl0NpRZ/6RonQjshkt6A8/KJdWQdbJG5mHZ8RoiH11bkXS69l9S69padNC1JUWrLIVSUBov6U8Q9n+N8/3/KUUQgd0+lWYAdpakL7BJFG0fbDGVuBQ2Rplucn11rbXJZtIK25CyItWRP6QDVo2Eekk+wQ60PyOS3qxR8g4Wrcrejujhn0a0JPpZy/8G9h4piCXSSyZhc+nAX/inrpL42+Gl77vOJ4Vllk8Lh/LZ9NJmC1xbdt3qjBLqBFnFULIFIZssAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAaCAYAAADxNd/XAAACNklEQVR4Xu2XTahNURiGX/nJ/38hyk9Sogz8lJtuKQrFAEUZGpgoMnDLQCclKSMMDMjQ5JaRusMrAwMjhUwkpQyVMpAB79O3PmdbHeKKe7bOU09377X2WXutb31rr3WlAQMG/FfMt8N2Vl3RBqbZe/aT3VnVtYJd9rN9YGdWda1gxH6xp+uKfuekouO1c5sP9TN0dIV9Z1/aTeW+dRD1U3VhYZVdUBf2E3PsR7u1riicUwziX8PH5L7i/T9lnX1iF9UVkwz9emP31BU1h+xdO6XcE+2p3epJg46/smvriprris2LARyzNxQ5f02xoMfLc0cU+8Vlu6OU8btn5RpW26flerN9bw8rfks59XCl/AXamGe329d2iyJ92JMuNJ77IdvsY/tQsRvT+TV2t6JxphEO2KWKhpMT9nm5JgA31R0wg+W3G+1be1URkCG7tzwDB+1FRcfXK9r55fRJltmFdaHp2LHGfTYMvIjUQ6ANpjyjxlct1xZHFDbLo+rOXkLK5v5zXtFups8ffTyINtElyitLWTYM5CbX++xyRQQ/KCLK2WpUkZ7ADPTqzAZ7VvElJK3GFXsTaZrHmsX58O9CZ4k205oLKRuG/YoB0jHqc8AMgDQh/xk8vFDMXnLJzrC31V0zHGM65Zp38C5m40wpmxBEoHmsmK3vv1B1fUL6PFIszoRnSbPpjTLgvtcBkpTuVf5X4H+IW4rIAuum8622BSxRpMIde1yR++R1qyAVSJFWHgYHTISvLQ5aL+ugH20AAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAAA/klEQVR4Xu2Tvw7BUBSHjwQhBiOJwWgySSQGm4HFwmCXeACDxdJXIBEiMVsMRgmL8A7EK4hVYvDnd3JPuVpEdZL0S7709v7ak9tzb4k83JKHEzjU7MGU5GlLNoINyWwkYBW24RmuYAVGtPwCj3AAazAp2VvCcCby2MQHlzCuzX1FDF6hIfcFuL6nP8DFNrAMdzD7HDvjRKrgnlwWYrhnXIx32G/JHBGFHbil5945JkBq6/napUfveFMcwQUMUsWYHKne8fkqytxX8DlqwTmpz2TMM8erG8vcR3g1fVIv1EkVNeFxBh4kD2mZjRKph3SbkgXh9EW+oMcv5uHxv9wAy3018v889rsAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEMAAAAaCAYAAADsS+FMAAACxElEQVR4Xu2WTahOURSGl/yHJCJ/uUz8M2BCSkphwAClGEoGZEBdkcFXMjOSJJkYmZhJFINbBsTAhAxQlBhIJlJSeB9rr85u3+/y3b5Tup3z1Fv77HXO3mvvvdbax6ylpaWlpRaWSJulcaWhacyUHktvpHmFrXEckn5Jp0tDE7ku/ZC2lIYmcdg8Iko1kunSfOmbdFtalJ4bC7dHnSmySnpuw+vPoHmhLtkmfZJ+loaaIPq/Sp+llYVtGLOkt9LCor8fmLTc3JfmkdeNXdK7srNGTkoPpRmloWS9dEuaUBr6YI+NbnMvSHfKzppgXazvUmnoBtdqHtL8ePULi+t1c6dJD6SzpaEm+G/i/2lvaegG1+oGaaJ0VTplntvnpbnSUHrvgHmoMzh15n56j/Zlq0JwmfQ6tbFfNC/KhGqwz/yPF45LH82/K6HOxDxwzPy9E+ZpiJ35sT9K7/Ccf4dvT83LwT/ZKN2VnpkPMl4aMC9sm6zKZRZ0RZoirTZPBYgwDOjnJGDAqnHWpD42k00NIkUYt+S7eQFk7p3S2iRq0lHz2xDYoPCTeSiW4V/PKRIwWQyc05HupTaTHElt0iqK4RzpRWoDi8s3BzrS1NTGSao7RIrwTTe+mM+53/wAgr8dAL69t8o/+ikFfVHm8kGrTvdGsgPhyqmsk2abpxUORQGNzeIZYQvH40S3S8tTX85IN0B+AGzMTfN0YMPwDb/DP8anH/8mp75RQ6QMmYcj+X3GqqLIgmhTZ66Z52RHWiy9Ml9c3Om0cYhNXWp+ik+syu0P5ptMjdpqHuK7/3zp7+W5Tj2DOACItCONiCB8i9sR//Bthbl/vRb1ESGXcbyE02EyyPOdmkOE5JT1gPGijzHynzEWdy575lAo5Iwb8M2k7Blbvmk8h3/M060EjAl2mJ9w41lgXvnH7EnWCemTp0NLy3/mN7QpdFdJsn5fAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAaCAYAAADcx/BtAAADTUlEQVR4Xu2ZS6hNURjHP6HIO/LI43qlRFEGikgYMCBFUYQR5kKZSFJMDExISgaiGJCkZLBDGRgYSSnpGtKlhIk8/n/fWvY6n73P2eucdY97r/2rf53Wd/b61vqf9dxHpKam5t8zw2kqNNzE+hPmYk7mHmViQ4430CXoDDTRxPoT5mJO5t9iYqUcEW1sqDHQWOhEQWyfPibLTflFaIGLdYOrtsAxEpojaYwfDc2HhtmAaP5KJvPhVVAv9BN6Du125WzsBuiYi7HSHVDP7ydFZkIHoLfQeWizaKO6hTWZbd4J9UEZ9Ap6BM3NvxIF+04/MtEBZ6lssieT3EgL1x7GiirkD3HDFnYJ29bt0Ddov6jhE6CH0EtoVv61lhyCPkCfRPudSSKT+QArvCeNi/kI6IKLcUSHTIbuQktMeRWeis4A5uVSc1R0lmyDpgTfa4Y1+Qd0S7TNnsWiI/tZUFYVGpjU5ONSXOEa6L6LnQ7KCU23xreCOzMNXS/F61wM1uSimchZ2Cs6KmNJbrJfdx9D41wZK74NrXaxsAMcvRzFHM0xHBadwimwhto2Em8yR3ksyU3mZscK2SA2jHBtOik64hi75j4TniS2us9VmSe6TCy0gTaxhjYzmbFYkpvMkwEr/AKtgM5Be4J4mIyjt511+DK0V/JLRJGmiW6mVbCGDniTaSwN9iZfl8bjGJO9FjWBI9yP6BjYKO7a3PDK9AJa5h9ogTV00JjMSndBKxvDf5YSvxG2AzfXg7awA6yhzUxm32JJbnL4i3NDsyOV5R9FE/LA3w7rRDfSVBcWayjbaI+gnBU8WXCGxJLc5EmiZ0lWGq7FnnAp6YQe0TwpXuhYk3ly+S75IODafgV6L/ke4k1nP3lZaQaXRX6Pm3XRZSbaZP5SGfTAfbb0Qafk7xHeDtOhJ9Am6ez9gjWZpp6Fvoqe6e9A70TP5B72jfsNj3T+FGXxI9gqk0Zvok3mLYmdLnvBw8r40igVnBE8BnIz/Sx5R3gt5rpfBWuyZ7bo7XGtlJ9UOHPLTK5KtMmDkTKTq7BUOn8XXJvcBC55vAd0yn9h8k3RKR/7z8giaLwtjMD/M8L8Q95kf4Hh+xZ2ulswF3My90YTq6mpqakZwPwCRK7aP1JOZfsAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFMAAAAaCAYAAADL5WCkAAADB0lEQVR4Xu2YT6gOURjGX2EhfyJySeqSFPlzSxZWShILC0LKwsKChb3uTlnYKRaUS0LKQmRB7G7IAlkI3boUFlcpG8XG3+fpnfnumdd35jtzZr6vr9v51dO9c975Zs555sx73jMiiUQijunQYmgpNGBivWC+6L3n2EBVpkELRS/mMhOabdq6Be/9BroBnTWxXnAEegGdsIFQaOI96Df0F5qAHkGD0CzoEnQoP7nL0MzR7K+F/dwiGuMMrgOvtco2ZtDIKDOXQLehu9B6mezkHugl9BD6Bm3M2ruNz8xB6Cl0EXoMjUND7gmB0MS1ouP9UAy1iDKTnfkEfRe9iQuPT4nO1OfQgmK4a7Qzkzn0NXQrO+YDPw29b50RBicL374fouP6WAy3qGzmM9ELDsv/RuZwQLxh6CvOQR4QHSQfAGfROdHf73POK8OayYWAx1+hNVkbyfu2yGkLZZPoBGrMTBrJp82n7oMdpunuIMq4AN2BVthABayZK6HPogN3Z2tuMo2pSqNmcrA087gNGNh5ziguQp3g7OZM5MpfB2umO/B2Zu522kJp1MyjoheLeao+1omWVXWxZm6H/kifmpl3gnWcL1fGcF50sGUKwZq5SyYXi74186pptzAV3ITm2YCHK6KVQZlCsGb29Ws+Q7TE6GQm8+lJ21gC82UTWDN9C9Bc0Xpzs9MWSmNmEhr1QMoXlvvQcttYwkFpJm1YM1nfssyyGwfGacYypy2URs0kLF5ZD24w7dwd8InHGPNKdLtXB2sm4bZvQjSVEPZtWNQQF75tnRZW/nYn9BP6kh1bKpu5FXonmtzHoMvQW+gJtNo5rwqsR1m7XpP47Wc7M8k20cHzDRgR3cXsL5whshf6Jf48ymtyvFajUvxKVNlMwh0LDWAtyQ4MFMNRsM7ktZhG8g8nuULwmUn45eowtCP7vx3cArMCqEOUmf1ImZkhXJfwHZuPZGYGPxeyYqnDlDKTCyBzbtW043v1q8Av7UwVU8JMfnihmSzyWR30mjOi9z5mA4lEIpGI5x/0obXA7XlU3QAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAaCAYAAADFTB7LAAACAElEQVR4Xu2VMUgcQRSG/6ABRUGiQZEEgiYgKtEiqIiWaa0URDS2SW2haCE2gnXKIIhFqqQTwcJCsRHSWGgiRkFtRMFGiIUSkv/n7XCzc4eci7Ar3Acfx86bvd03780sUKJEdvlATyNvglgmeEvH6D69DWKZ4QU9jswkU/QfnQgDaVJG62kFXYWVtz82IyWq6AI9pxv0C72ge/R5blp6/KA79GV0fQQr73da7ialxSdYOVVWxzq9pl3e2EPRBkv+YxgoRA3dRv7kMzxceVtoZzCmChWVvG68in59lOESfRKMJ2EU+YkWnfw7+gf5k/WC+mP130gQuy+fkd/HRSdfSVdgh7Kopd/oCW2E9ecsnaE99JIOwhL7TVthbTIJe2AD/YUciqucPhqbhh1p1bBT4060c3fpMj2kw7Dzb5Nu0VewFlCfarc/Q27lB2BJuASbYck5VAWV00djSkSocmG8IHWwm55G18rMv9bqfIWVS+gh6t1e2Aq4cr1HfMU0X/f5+CXXR8BPKDEuU72YUA+t0SbEHzAPO7LaYSutFdfKv4G1jxtzuPkd3lgidCToy+I+ez9pN+I9pFY4gD10CNZrenndMwfrdzcm/KTHo7HEqEyLsJKHO16oRVyZtWkc2giKOXS/PquOMJ4Yv7yZ4zX9CzuO+oJYJlAZhErjdnWJR8F/aZdbwaZWxJIAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAaCAYAAACgoey0AAABYklEQVR4Xu2UzSqFURSGX6GIAVJSDMyFUkpkpGSi/AyUMpOhYiCSTNwA5mLiJ3EDLkAZGZiIgVJuwEzifVt79y1bTkfnfBN9Tz31rb3qrL332usABQUF/4k2Wu/iGtpKa91a1emid/SNToS1LfpJd0JcdRrpCaz4Cz0K68ewwjGuOpN0jB7Sdzrqciq67OJSqE196WI56LS3sL6KOtip/UZK0U+n0sVy0LXuuriHXiLbSG6osK49Mk+3XZwbKhyvSiO06nI6/SZ9gm1Oo7ZBm+gaHaTrIY5o42rVNH2gHS73jVPYOJ3Beu1neiB4j+wHVKyBzoS1m7Ae0UZeaS/tTnI/aKGdtDlNwB7bAey0Is67GKbPLhba6CP9oLNJ7k/oVDqdUPEVl9ujF8jGaYQuwjZ7jgr/C3QT4+F7iC6F73ZYCxboHKzP1/QK1op9WL8rQi1QO1L0GNOxU9FfH1RBQW58AQrMMPyImRw1AAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAaCAYAAACgoey0AAABLElEQVR4Xu2UwStEURSHj0QyhA1pFMlCSfZMY5QF2cl/ICtLxcJGyl/D1oqF2FnLzmI2LCRZ2uD7de+r6RhqGncWul99zbtnTu/de855zyyTyfwnht16wK2TsIlPeIoLeI2PuIddDXl/yhCe4QF+4jMu4hteWcKTr2MVbyycejrGl7FUJKXkBc+xz/+RGpX5xAc7gR6ssncU9fWnMmv4Di1M+z5u4IeFTWp9EXPEbvxVzj3O4mW06bzULEx1M6ZwxcKDyhZusIQ9+I7bOI5rOI+jeIdHFtAbMhmvv9Ed/Q3131fkFXdwC+diTBvUhipFUjvolCqXR6/goIupcnULVWgbzYBu5rnFkYa1vnSr+IATMTaDx9hbJLWC2tDvgxF92dRX3yrFx1wsk0nPFxXrKXjSw7GtAAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAaCAYAAADFTB7LAAAB6ElEQVR4Xu2WP0gdQRCHJyhB8E8Ug0ERxJBGFNSIhSGlQQIiohaBlBYiSoIWCmKRJr1YWQjaaSGkEgstjjQiBMHCKkUUQsTCJiAIQeLvx+xx9+a5pz71vSveBx/c7Sx3u3OzuydSpIhUw1rbmAaewXV4AH+4+1SxAE/gR3gOuzLDhec33IH98FJSmMH/cMw2poVS+A++tYFC80E0c9b9eKdCUgbrYR/cha/cPbeaVDEHp21jDJbAKjyCPRmRPMCXb8BeG4jRBj/DU9hqYo/Oc3gIX9pADK7uStuYL1rgmSQPYBk+sY35gvXHleuDi+bYtDXDd/ACDovWb7vo5r4NZ1y/KYlOJB6hTe56Eja660TC+uMe6KNbsgfYITqoAFaIlgkz/EX0uHwNJ+CSi9fBWYn4KrqD3EhYf9THkFwf58QWY/flokfldzgCGyQqiwHRicb7JVIFB2En/CuZL7JwthyM5afoi0OYqUC0ZCzM3gt3zcVov0gWHFAAxyX5z4WfYVN0kBa+hAsshNlakahvCfwE34hOpMb1YX3+cX28MIOBaIHzQT5Y+L4t6KltcHAQ1/3wso0nlG/Cd+YXnIdroovpIeBEmb33NpALe3BLNIsPwajo8/iv+c3EcoJbw622ghzwlUeRe3MFEDlOfly3ig4AAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABACAYAAACnZCtBAAAEx0lEQVR4Xu3dW4jtUxgA8E9R5BZHLiGXRO53IsoJCbmEB4XyxAsSoZQcD1IKkUu8nPAgvCjX5GGKB1KUErk8kEjijRe5rK+1/2evWTOz98ycc8zO/H71NbO//d8z3/yfvtb3X2siAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA+D/bXOK5JjaO8m3usRIHl9i5xF1N/rbRtWspa/iwxPejeC3G9T1cYofxpWtmtxL3l3i5xLdR623v74bxpQAAC11Z4qkSf5V4qMQ+o/w1Jf4p8WOJ80vsVGLHEueN8p+WOHp07Vo6O8a1fjz6PuOmEt9EbUh33XL12sh7l/fwy6h1DjVeG7Vh+73EpVuuBgBYxKlRm4b8OsiVqWwuckWolatFZ3a5tXZ4iT9LnNPlD4j6Nzzf5ddK1vhrn4x677NOAIAlZaP2d4kLmtzJUZuI75pcuj5mY8zYyro/j/Hq4OC4qH/DzV1+pXIUvJTd+8QEWctcn4ya17ABABMNK1FXNbmnozZxufozeDRqwzZLctz5Xixsyob69+7yq5Hjyk+6XDat75bYv8sv5cCo9/jiLn9G1HH01V0eAGCevaI2E/eMXu9b4oiozdofw0XFq1FHolsrG6DhOa5Jkc+nTZPj0J9KvB7jh/hz48ELJY5prttaWfNpo++zWbszVtYM5rg268x6BxdF3SjRN3EAAAvkKtXwrNexUZuflOPQYVS32Cg0H6a/tculzOV7/4UnYvFxYjafmc/mc3BQiT2b1ylrPaHLLSUbyK9KvBULf84kOVJ9M2qtk9zdvc57uNzaAIB1YGjYcmXqwlFuaNiy6Xl7lGudWOLnLpc7SXNUuC1W4pZjLhZv2E6PujrYrl7dEbVpa/1W4vIut5RsoDaXuKJ/Y4phFXDa7/mie52bO6Z9BgBYR7LpyWMncoVtMDfK54rbSlaUpvklxg/aT4o3hg9MkNe93yeLJ6O+t1//xirlKuQzUZu2Q6IeIdKvOC7lwai1TNq8AAAw1dAktXKMl7lhxa2VDdxHJR5pcvdGPRz2yCa3PQ1Hj/Sjxszng/wZg3yu7evm9UklXizxQExvvPJvfSXmj3lzpe7GmP7ZNBcL723rlKj1tbt0s7YPYnk/HwBYJ7K56cdv2Qjlwbm9XCnKHaV5Yv8tTS7HoXlESHue2/bSr8a1kQfm7jG+NA4tcVbMP6IkD/3NZmjz6Oskt8fi1+Smg8f7ZCN3r/a15Vi2tzFqfXkMSTo+ll8bALCOXBILNwrkKlTGUrIBGpqMwXWx8Dy0WbCpxDtdLnfH9seBrJVNJXZpXmdtOXYFAFi1bMqyOcujKQaz3GRkc5lHlRzW5GalucxRaNaXI+VB1paHAQMArFquBuXI9L4ml6PQPFdsFuX4Ng/+HczSyDE3emR9lzW5rC0DAGCbyNWgPPYjH8xvNyHMog1Rz1E7N+ZvQpgVWdsNUWs7qnsPAGDVskn7rMRLsW2P/9gesgn6Ieq/mprF/zCQtT0bs1kbAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwQv8CLCrNtCfSzq8AAAAASUVORK5CYII=>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAaCAYAAACkVDyJAAABl0lEQVR4Xu2UPyhGURjGH6EU+ROSwcCmZFEsJhkQkmzKYmBglM1mtMhEMkjKLiW7wSJlkpLFIElZ/Xme3u98jrdruef7Fvzq19d3nnvPOffe97zAP7+NbnpAb+l9wUu6S7cLztP6cEMqLXSKrtJ3ukZnInfoB30MN5SKYXoN20BMBd2CLdrsstzU0GO64AN8X9BvJjdd9IH2+YD002f65oMURpH9BEOwInqh4y5LYh22oAokVKaq9I7O0drilSVAx+KpoKeD3sA2sxiN67vORv8DvXSZVvsgZhI24YUPYBPrjCo/i8bbYBvx6NpTWueDmE3YhPr16FVqIb9gbppgT6YJp10memAVqnzJZblYgU12Thuicb0SbUDZHr6KRp1HXUmfIX6lKqxBWOOYiMaLhELRhD/5Sgdg3zGgTejoHMKagVDTGKNVsCOUdZaT6IQ1+hEfILs1JqP2p+/eCnuqGFVp/EaSCT1XjUIFFaMCzOrFyegJNHmlG1cj0HhZ0SIntJ0euawsbNArug+r3LKjnqk21+iDv8UnyV1TLC9NvJcAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAcCAYAAACtQ6WLAAAAkElEQVR4XmNgGBxAEIgZ0QVBgBWI/wOxJ7oECAgD8XMg1kSXgAEOdAGCgJkBYiwGUAHi00D8GojlkSVcgLifAeL8dCCOQJYEOdsUiDmBeAcQKyJLwoAOEL9nwBEADUD8D10QBPiB+AQQXwdiZSAORJa0AeLfQDwJiEsZ0BzlywAJUxC9nAGLf0HBJokuOOIBACXsEVMbAsH9AAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAsklEQVR4XmNgGNqAFYiF0AXRgRgQnwPin+gS6EAdiF8C8XV0CbIADxALAzEjugQymADEF4D4IRBvB2J+VGkIAPkyhwFiki8Q/wfidBQVUBANpTmAeCsQfwViY4Q0JpAG4gdAfBqIBVGlUIENEP8G4vkMBDxUzoDHfTBAtLUuQPyPgQRrYSGAAmSB2AqImRkgwfIJiPVRVEDBawaEJCi1TAdiFhQVUBAMxLOAeBIDxNThDwBwKR3PC74dWAAAAABJRU5ErkJggg==>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAaCAYAAACpSkzOAAABbUlEQVR4Xu2VvytGURjHv0IZDK8oGQxsFgbZmCx+RJJN6d1MMvgbjBaZ/JgkJStKBjOLlEkWAzPFQOH77blHx9NN7+0eA/nUp973+d7Ovfec55wL/PPbGKXrdIteZOq3anKRtn5eXYIeOkN36DutZv+DL/SJjmfXl2YVdiPPCH2j17TTZYXppvf00QdkGvYAr3TQZYWZhA127gOyBsvOkGCtlmGDbfqA3MHWacIHRWmmp7AbzUb1ejpEH2CdWZowbVe0zWWeOjrsi6SXLtBGH8SEadunDS7ztNMlX4RtjWPY7OQST9v81ygtoa2f6YDLkrIBe5tDfPPasBNiCraemr7AHGxvaX1zu7IPtjl1k9iT+KIIbVo1yi6sIUQTHYOt6y3tz+ql6aI3vphRS8fWjJpFJ4da2Xenui68aSk0TQewraDPRkwLEnesnliDenSa5NWToMGPaAfdc1lSVugl3YZ14o+hM037qeKDv80H/PlEUInA1i8AAAAASUVORK5CYII=>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGYAAAAWCAYAAAAy/emjAAADAklEQVR4Xu2YW4hNURjH/3LJLRKZXGJISubJrUiKKHJ5oTyIN3nxIIqG1OSSRlIo4kVIIg8UJXkYKbc35RYvyOVBeeJBcvn/+9Zqr7OaOe1t9umcmbN+9W/2Xmt9326+tdb3rXWARCKRSCQSTc0oagk1LO5I1I9J1DsnPScahMXUL+o2NTTqS9SRPdRfanvckagPI6kJ1BfqNTXbvZdB0Z03OG4ombz+R1CrqQ0FtIgaIOOy+UNdRjnOx1G/qfOo9LebGh28e5ZSX6nlcUdJFPXfUBOjNLYtbuwFL6hNUdsranLU5lmFnvvKoNb+a4JWyA9qbtzRCz6gmL/DKJ76ilBr/zVhHSrTjlbWQGoOdYN6Sw2izlCPYelIY9dQXdQF6io1E4b6Qn/eT5hK1HeHukjdpb4FfSEatwz2nevIduFa6iG1kroG8zPP9Ym8/rtDdVapT1kkr25Rw2VcJlpN/h/WP3QcFvyD1HhYUMRGWDpqodZTz6ipru8jslQxBpk/+TkGO1DsdG1C9t5WJ0EdProj/M4U6gjM/z6YzTlYUddC0snSk9d/Q3OSWgibFAX/FNUKK5pqf+/GKbinYSnhOSoDEd5/lMJ8GmtF5qfNtWliNcEeLQzZx0yDTXgn7NuXqBUwnwuoN8guw5osXyPz+m94lAIeUfepK6g8OXXAUoJQYLe65+/UfPesCdnrnoV2iwIV0oHspx6lTtkL1bd7sODFqGD/hC0AnXziGtHTYsjrv8+iO04XbCUqLbTDao14Cgu+dpmOwZo0pb6JMBvtPF9T9Fe7TpOnXaDAyd7bfobZa0GoTmnsDligX1LTYcygDlBDXJv374Ov8btQ3X+/YTP1AFb4w+Om7jzK9ydgAVc63ILskHAWNrFCxVSHBhVsoQDJ3ts+gdmLWdQnWKAVWAX6JmwXHoL90Co0KT6N+W8ehfmu5r9foXShIIXofazrE+FqVF98y47TkMb4No0N7bUD9gfvGqe6EaJiHyJ/YVs1/4n/QJOild7nLoPNgK9jTcs/nuWUvgMeP0kAAAAASUVORK5CYII=>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAaCAYAAABhJqYYAAAAm0lEQVR4XmNgGAX0BoxAzIwmxoHGBwN5ID4CxFegbBAQg/IVYYpAgAeIVwCxGRB/A+IiqDhI0RMg9oTywQDEMQViTiB+AMTSSHKSQCyOxIcDYyCezwBxOwxoMuBwdzoQR6OJofPhYCEQ6yPxQc5aisRHAQ1ArANlCwHxciDWhsuiARkgfsgAseEkEDuhSmMCYQaI71nRJUYB/QAAWh0QRxedrfYAAAAASUVORK5CYII=>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEUAAAAZCAYAAABnweOlAAADKklEQVR4Xu2XTciMURTHj3xEyGck5CUp+VooUmxEsWBhQylbFBuFWE3JEiWysZEkHwuFfGTxlo1SFiJFFqSsUEqRBefXuXfmPmeeed7neWeGd97mV/9m7sec5z7nnnPuHZE+fbrNLNVY3zkCGaOaIf9greNVR8UeONJhjYdU1/xAJ8Ehl8Jnr4BjTqmm+YFOMEf1SlVz/b3Cd9Va39kuhOE31Uo/0CO8UV2QDqb9FNWg6r5qYnaoZziv+qRa7AfKgAN8zSDsfqhOuv4Ijpru+rAxUzqzM3kbUdX2LtUf1U4/0Irnqveq1aFNihBuy0P7tJhT8nJyt5gDcBgP3a5aIPZ72scbUyuD7Yti9qNtwH5V2/NUH8ROoiGdSQH9pdqU9G0Qe6kYaldUn1VL6jMMKvo91STVQ8k6bn1o7w/tqkTbbBD2/aZUtT1b9VqsDJANhdRUt1XjxDzIxeyt6mAyB6fgZbydMiBWgHEijsUxvABMVT1SbQxtdveYlD8aB8RskzrYT21DajtCpB+W5vSHWBdRoVO47ZE6X1Ufg56pFqaTlBuS75RITSyceYnIfNWT8AlHxKIP51SlJlnbkNoGNpXUeCz5L13aKTHPhlookcI5v8YPBBh7KhYdwAL5zbb6jOHDM7EfbQP2q9qO74ozJ7uxDIQykeGdQvidUK0KbQrab2kO1wj5jRMi5P5VaYT7HdU71Zb6DINwx5nnXH9KPPl8X5pKrJdofqFalvSnUA+pi5f9QB4HxKp8CjUmVn2g6pMee+szsnD+k4akI9xSrQvfcTy7NCiWQiksELuoFRR77EfbHMXYT9knjUK6w41F2FA2tnRxppixcJSXb4TrdbGH8vA8cODcIE9NmgtlSitnp0TbeUUUsFG0Pi6eRWsYFltVP6V6LgOLZdEUxrQ4AideUfqUhagruoN8Ue3xne3CDt1U3fUDJaDALRW74JEOKSvEak67kL6tUgNHtTqV2maR2D/lqlDMz0pzvlNvCOvSV+8CuE7k3biBi2SscV2DIpwekf8LUvKBWC0848Zgglj/Zj8wmuGFX4od/2VvyqOeeOL5f+h9+nSZv3WxikjPCaoCAAAAAElFTkSuQmCC>

[image19]: <data:image/png;base64,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>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABACAYAAACnZCtBAAAEyElEQVR4Xu3dWahuUwAH8KWQeY5EkQzJPKTEC8kYD/Iiw4skJQ8I8XIjSWSOSKaSuZQ5yjEUFy+KyFB48cYLD0isv7XXPfvu6+RO56Nzfr/6d+5ee3/7+7799G+tvb9bCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMFPb1Ww5HWQ1m9TsOx0EAJiFPWq+Hf6ysGuGAADM3PE1v9dsMd3BKpvWPFdz0nQHAMBiuqjmz0nmxgfwt0/KmtcJAGAmtqnZveaHmi+Gf++w2hFLwzlrmV36CyZ2rbmltKKWa7Tb6rsBABZfisgl08G1lJLzds0jpd2UH5vVHLrqiCbHvVtz92R8fW1V80fNy9MdiySl9rPpIADALGxd80vNUdMd6yBl7LzR9mE1Z422u8xMnT0d3ABv1lw3HVwkKbUppf8nBxQlEgCWhRSrPju2Z2lLg+sqZW3H6eA/uKJm2+ngBviutM/8b6b3ny2UhR4oyNJxL7W5ThuzdG6IzFY+OR0EAJaem8r87NjtNefXHFnzQmkFJk9HflCzfWllZa7msZqna/YfxsbLoQ/UrBxt713zVM3rNV8OY1MpXc+Xdt78FtxeNV+VVh4fLm0WqZ9vp9Le+7XSlkNn8WTrPjUflVZKD6p5cbTvpdK+/5U1m5f2mfJ948TSft8un/2tYfyZmjdqzqx5teb6mmdrjhhec27NO6Wd57iaS0t7OjUlMX/zOSIzi7/VfF/WXH4GAJaYo2veL+0+tJSyOKHm2JqDh+37SitGnw7b0ctSZp1SGiLbWfZMwYte8DJDlZ8OyYzYVGaIPqzZr2ZFaceeXtp79WXVlMqc+7LSfi8uUqIWmhHb2HJP3s+lla3ThrE8iNCvR75nSmZKVcpbku8xN+w/vLTZxWxn+fiY0q5xzpXfvsuydN4j1zxP7ubBhpS4Q2oOHF6X8+U7j69hiuxCD0oAAEtMStb06dAVZf5/Prh4+JvSEilP/d6xzM71WZ9I6eilImWkH5fCMj6u+6bmiZqTa3YejeccKSvj4pO/OTZSdlJgZiXXZ/x0aN7/19F2l+9zammf7evReGbHpg9c9CLa5RrlWmdmMQUuMsPZX5cCm/N3uRZ95hEAWGbGJSkzRykNkZmwFISrS5t9u7G04/KEaZ/tyqxPSlxKRwpbZtbip2E8hS4l5ZUy/z59STYFMf/107ikpMRk+fO2Mn9sPlOWV08p63fP3caQ7zsuTzeUtiTal07vLW0WshfWXkC76WxZpJD1ewFznbLMmuvXX/d5aWUw3zlj2ZeS24s1ALDMXFDa8tz9o7HM6NxVWglJobpw2J/Zo5SvyL1o2ZcZopS7bF9V2msfLa1cJD+WtpyaJdmVNdfWPF6aLPP15dD8fa+0++rOKK20PVhzR2lLtVma/C/k+91cWoG8p7R71SKl9tbS7uX7uMzfmzZX5q9RpPBN7+nLOR8q7ZyXl3adUob761IA7xyOy1jeP/f4AQAsiszO9XvmAAD4H8pTkgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMvOXz+XuxTZ30T1AAAAAElFTkSuQmCC>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAABA0lEQVR4XmNgGAWjgL5ACIhZ0cQEgZgZTYwgkAHii0D8BYjdkcT/A3EDEp8g4ATi5QwQA58A8UKoOAsDxDAYnyjgCcR2QDwfiH8DsQ2SHMigdCQ+0QDkqtMMkHCCgUUMqIYTDUBeakUTW8eAajjRAGQYyMvIoA6NTzQAGeYHZYOSQwWSHAgEM0BiHARyGCDBAoo0rGAFAyRprGSAhF01kpwYEF8B4nIoHxQcW4GYA64CCxAAYkkg5kETB7kYZJEpA8QAkEFVKCpIACAX3QVicSBWAuKHQOwCxOpAzI+kjigActkpBkjMlgHxMyDWAeJmBjIMAwFGIBaGskF5mCxDRgENAQB5oyWQB1vqjwAAAABJRU5ErkJggg==>

[image22]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAaCAYAAABRqrc5AAABBUlEQVR4XmNgGAWjgDQgBMSsSHxGIBYEYmYkMbxABogvAvEXIHaHitUA8X8gboDy8QJOIF7OADHoCRAvhIovYoAYAuPjBZ5AbAfE84H4NxDbIMmBDEiHspOB+CsQGyOkMQHIFacZIOEAAiwMENcgG3oViEWQ+BgA5PRWJL4iEK9jQBgKCmiQa0E0TgAyBOQ1GIgA4jokPsgwmNdwApAhflA2KFqLkORAIBqIzaBsXwaI1zDACgZIFK9kgIQNcpoBgTkMCK8EAfEzJDkUIADEkkDMgyYO8grIYBgAhd1dJD5RAGTwNSibH4hPAPEUhDRxABStx6HsYAZI6pZHSJMGQN4dBfQCALOLJlOJ73yeAAAAAElFTkSuQmCC>

[image23]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADMAAAAaCAYAAAAaAmTUAAACPElEQVR4Xu2XTYiOURiGb6Hkb9LI5C8TakZMakQRSVmMBYthQTZq8lOkmKLY2FjYSRaSshLF1mIaC5mSUnZSJguTWMmGjQXuq+ccc743jcVMceq76+o7f+97nvOc5zzv+aS22vonWmz2m3VmdqOvKq0xz80989N8N7tbRlSk8+ZYKt8x783m372VicXcN3OaHTWqw7wwb5sdteqM4rywsGpF5jpiJswPM9zaXZdGzBOzSrE7r83SlhGV6JQ5XNQXmm9mS9FWhfKhX1u0zVKli9lgPpt5RdsCVRpmeJ9dKLXS3FTsUFXC4OumO9UJu2epPdcvm15z28xVZL4HZn0aw12O2wJi/Ki5kOrnFA47bfoUSabHvFPcMtBB89IsUySfD4pEhA28K38mtiveM6UIq4+KOxmTXCv6us0es0+xY2iJYvKsk0X9ivlk+hUT31KE66Di7ndAYeS21N5l3piLCl01jxVhj/FDZrkZMA8VDvmryGA8xO+fxCT5XHHOWDTi6vPI3FA4Bc+zs4fMCrWG6k7Fs6Vw0lezNdVZCHMhrlfHFe/aqIiKaSsbmXVUkSAQxhFiGLraPDWXUl9TGNd0Fm08jyMR5b2pzG4tSuUZE2k7nwlErBOSKIcY4QJ3NelZztZZs0OTO9gUho8rFsN4wj1/JghJQjqLsJv2zYRJ5hd1vFX+ccPbpccJrc6insUOTyXCuLmrvJfEUMUfxTGzK5U3Kbxfrb4ozs0J80oVfttK5SzKeZuRbNXW/6ZfB9pUlZqTu1YAAAAASUVORK5CYII=>

[image24]: <data:image/png;base64,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>

[image25]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAaCAYAAAAwspV7AAABgElEQVR4Xu2VPSuGURjHL6G8lZeBRN6SsliUQVKKZKEw+AYWE4OSJCWLT2ARBiw2ZTDYTRaDCSlfwCID/3/Xdbqv5/Zk8NR5kvOrX/d5v6/Oue5ziyQSicTfoQVWu3oFbIaVri0qnfAOvsFpa9uEn3Db6lGphaeigb3AI2s/Fg0q1KMyA8fhIfyAY66PAS27enS4S7eieUSqRHfLBxkdHtWuq/fCC8mCLAsMikcZWIJbrl4WGNSslXkNrLo+7tYAfIUHolfHGVx3YxZgt5W74B7ch+3wRnS9SfgE+2CjFM4vCl/CK+FcNLf8ndUjuuAD7LA2jgkfAY+aOckARuEJnIITcBg+25PpcQlrdJrM2/NHmkQXbsh3yPcFw4sIj/0dLsIRN4ZwN65Erx7O33B9g678K/IL8kU8giE4J7pTeRicn/coWd5yLgMtCeYCj5DUwxXRnVqz5731kX64Y+OuJcsdBh6umPDnKIm6XL3Yf7FNCnMxwLZWKzM1mCaJxP/mC6baO4jUt49IAAAAAElFTkSuQmCC>

[image26]: <data:image/png;base64,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>

[image27]: <data:image/png;base64,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>

[image28]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAxUlEQVR4Xu2RzQpBQRiGP0VRFmJhY4Fs7JRSVjZchVtwG+7Ayg24BQtp9uyVsrFxBRbIzzMNp+nrzGyVPPUs5n3PNDPfEfktKrjFKy5UFySHc3xiVnVBunjGpi5ijNFgUeVBGnjBvi5CZMS9Y6qLGA/cYVUXaZTxJu4UO+LoxGq4wYG4d5wkMrEW7nGFBVyKO2Xif/Shg0dci7uSxY7XbjDvdcIQD9hWuZ3WTNymBPtzDPb80GOEd6z7YclfpGD7vA7/fI8XXVkeg7zZxLIAAAAASUVORK5CYII=>

[image29]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAABTElEQVR4Xu2TMUsDQRBGR0wQIRA0IUE0hWCnYBEIpLJRCIi9YHotrNLYCvYhhX/AykJbU6SMpY2dhU2KVNoJFjbR72N25Rx2OZUr78GDu5m7nd3ZXZGcjFiG+7BqE1lyCj/hJZwzucx4hC+ihQYmF4Pf9mwwRh3uwAvRH19/poNwtTO4axMxTmARbooWYKG0li3BCVw18SA1+OCeOTBbxSIb31+E2Ya3sGATlgocw71EjIW4+VO4noiTedFJrcAbeOCeOU505YdwCBdNfEt0Necm7mGruPrUVpVFV9GxCdFZscgzbJgcacJ3+UWrYqvwcBAWOrMJcCSaS2UESzaYoA0/RAfjRfX4Vk3cO8dg0QX/gYezPxbdNBoqxlZcixZ5Er1LhKfqDd659y7sS2DjuQ/8+S/yLhFf5Aq24D1cc7lM4ax5bHmkc3Jy/sEXlSg+OEpvBVcAAAAASUVORK5CYII=>

[image30]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAA0ElEQVR4Xu2RvQ4BQRRGr0JICAohQrWdSqETpSdQaDyAR5DovYFerbedsNGqlTqJXtCIn+/unZ3czGbVij3JKebMT2ZniVL+kSwsuzEJXriHJ1hXvW1ajA68wg0sqD6FHzW2LOEbDlRrwTM8qGY5wgv0VOPNfAgfFuMJfZhXbU5ynbFqFp6YqXERBvAOuySbctFkk2TDAmZM25kWwBIcmh7Cd30Z13AFeyQH3OCW5B9Z+OkmJPdvwJqaqzjjcBF/bF/HX0RvXXUnkhjBhxtTFF9yNiRQU2KS/gAAAABJRU5ErkJggg==>

[image31]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAaCAYAAAAue6XIAAACmUlEQVR4Xu2WT6hNURSHl1AKScQT9UomSlEyEMqAgfwZYEBmUswVJQOSjJREyVMyMJGSxACDGxMxoZiIolBISgyQ+H3WOe/ts94+5x661Kv71a93z1rn7b3O2muvvc36jA2mRENLpkkTo/FfskQajMYM46VZ0qTEtkW6Yh50KyZLx6SzGV2QVo28OgqCfBSNNTyUbkjvpY2FbZy0T7plLQOeIK2Wtkp7pJ/S1eIZzR1+swrLd0k6ER0ZyOhF6Yz5+CShZIZ0zzzoP4LaY7D90ZFhrfRGWhQdGbZJu8yX/Ie0qer+7X8bbFnmSUPSJ/OlItgn0mvpmflAEQL8KO2IjgxTpbvm89RBOZySZkZHCi99k+6YD5ZmFh8Z+FL4Unabf9ziYM/B/74yD7oJPnxlNKaweb5Ky4vnWAblF98sfCXU3HNpdmKLHDcfK2pn+lLCMvMk1HLOqpPGYGGz9N2qX90p1NRf8c2RDpiPyW/mqeur86WT0ZhCPX6QFhbPuWD5/dh8R5e8tOqOroO2eNt8jm7wMdet2ocr8JUER0/ldwx2gfRUWl88l7QNlkyycmzYbhBsx5pXy7ZL78yzt9c8WHoi/fOzeb1G2ga71HyDXo6ODATLvOyTRjgKKYXyUCDAdVZ/qjwwX16WuQnqnfGo224QbJsEDDNoPvgRa6gd841AO4otLYWTkYy2bXFrzBPUCDXSsdEtplR5jqfQfzmJmKAOGjy1yipMD74c7BM6Qs/hvvBCOhrsKWSTrJ637nXIKtIJWI2ew+RsQC4gsa4HpMM2Uq/xHpCD47vV3eBvoa1Rt/HuwEFDkNT1ffNbVRPlh1+Ljl5Dbz5U/C0hs6elFYmtDlaF5ecS/l8g0A3R2JKD1qID9Okz1vgFg/WGC9necGIAAAAASUVORK5CYII=>

[image32]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAxElEQVR4XmNgGJJAAIiF0QWxAX4gXgHEF4H4DJSPF0wA4udAHA3EX4HYGFUaEzwB4j1A7APEfxmIsOE/EKejC+ICLED8G4ht0CXQQQQDxGR0fA5ZETLgAGJJIHYH4uNArALlg4IWL6gC4iJ0QVwA5P41QOyCLoELiADxVSBWQpfABTSB+C0Q86JL4AIg94NChigAcz8oDogCMPeDMF7AB8QBQGwIxJ+AeBKqNCYAKTgAxJkMRKZMkA0HgDgYiJlRpUYBAwBg5yHBZ/OmqQAAAABJRU5ErkJggg==>

[image33]: <data:image/png;base64,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>

[image34]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFIAAAAaCAYAAAAkJwuaAAADRElEQVR4Xu2YTahNURTH/0IR8pmPDDwyMRDiKUUkigEJA0UMDJTeiPJiLkOSgVBImJgoysDgFkURE18l9UjJAFEU8vH/t+5579z1zj1n7/Oud7s6v/p371373HPXWXvttde+QEVFRTiTqDHeOAyMpiZ6YydzHe15IP3mZarHD3QiW6kubyQjqVnUCmqEGyvDPGqsN5Kp1D205jfaxhzquTeS1dRL6jF1hnpKdTdcEY4CNJ/6TC11YwmrqOXe2CnoAU9Q9/0A+UQdg2WlUDBlW9J/RTELqWfUH+oL9RXNAzmKqlHjnf2fswy2HN5QF2EPeojaTm1JXZdHL/WBWuDs+vyAmpyyTYNl5TvYEo1FJSIvkEL3vwoLahCqCel6oB1zOgZmvwgF7AW1FuXrima+Rt2hJjQOYRMGZ0dyvbJrY8oeSkggten0UbOdPRPVgVfUE1h9Ui16S32E1ZAQJ29TU7wxEmWVsuucH4Blag3NA7kvZQ8lJJD63Z/USj/g0VZ/AzbjcughdaU+pix9BEvvPObCCvdQkbNyWs57igKZ9Z0iQgKZxEVdRC7KNuka9ZvakBpLMkS1KQ9lkJzK04z+q5uTOK1XT7sCqTFdE3x/ZV0fGmvBZpiT51O2LLSxaIPJU1FWix34DwKpJXUTjUeykzAnd6ZsWRzxhpLkZWTRZpP1nSJCAtlNfUNEIP2sJk6q11qUsmexBtmng1iSQB7wAzAflNVqeRJULrRJZrVLIYQEMs+nQcgh76SKq26grAxBdXQvwtulLJLAqF5n9W2/qMMYaK/0Xrb19c/jYN2D/P5etzVD91gMy7Z1aO73UURMlGZEdTDd/yXLunC3qjMTFoC7sA1LfWgsCp6aXz+pCfthD34W1uTr/W40+q026Ads48xCWfga9mxeyk5PjbqFwBWn2dBfR2mUYcEzUUcPpEk5DcustJOqwSFow1GWKUuyUEum5bYHloHNUCa1AsWgxxtjUG2sYfjPmTpN6WBwyg9EoOy55I0l0cFEfXJplEWtmtVYdlHvvTEC1cwL3lgCTepBb4xBLZBONLpRu9CJS+f32HO7amuXN5ZgG4oPIh3DccT9RdYqdKLTaU0baEVFRUXFEPkLIDi6POGtzEoAAAAASUVORK5CYII=>

[image35]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGkAAAAaCAYAAAC0NHJVAAAD+UlEQVR4Xu2ZS6hOURTHlzwi8o7kmVDyLBmQkQxIDFCUiZlHGQkhdUuKAYlMFDcDKRQGHgNxYyIGHoWRuuQRugOKuuSxfu3vdPdd33nsc+53z6fb+dV/8O19vrP3WeustdfeR6SiouL/YaCqn21MYYRtaAKDVRNU41T9TV9vwliMydjMoRQw+FXbmMFq1STbWDJrVGdUR1QjTV9vwliMydjMIYiF4v6QJa6z4KBbqn22I4Bnqqm2sUSSDERWmKJaajsKQHaZrhpiO2okzaGOiaoNqk7VX9Vj1aZa2w7VNdVP1dboDzWYwB7VQ9UY0xfCJXHOxyjNIM5AG1UdqjbVWdV91TSvPw/Yp1X1VbXI9EXEzSGVN+KctNd2iHvj95u2OapP4hxahCWqb6p1tqMk4gz0S7VFutbXO6pXki81z1O9FGdL9F1KchLcVA3zfrerTnq/i0B0EsE4LJShqgOqu9KVipkHkU+KCi1grIFWqK6oBnhts8VFFtlllNceCjYt1UnnVKO931wbEgU4drxtrLFY9UOSx7TMUD1VnbIdBbAGYg7nTRsVGHYh4heYvhBKd5Ila+I7VW/FRdxtceubfcsjI/AGZ0HKeSJu3bD3KYI1EA5KctIfcZGWl6Y6iZTA9TxEHBj0tWq+10ZuJ334EGVtqgemPY4W1SFpjIPAGijNSdjFXh9CU50UGddfoyJaxN0HR2JQKj/S4nbvGh8Mw9hZsCaS7jBckvLsd6yB+pyT2B+1Sb2TWFxZZLkPqQ5Roh/0LzKEOumL6p103TdOx6T7wp+GNVCfc1JSJEUPRTEQApF2QcKcxKZ5rG3sAdZAaYVDmqHTyPqvnUMmkZNCymqcw5pjq7booXjjQ4iczb2yYPO70jb2AGugVaob0v08jcKIAumFFHtBGu6k9+KcdFnqIyQONn7LbKOyTfXbtFFInJb60wWOTD5K2ItB1O1S3ZN8m8sk4gzEvKkeI1rFpVk27hA5DTuRxtNgvp/FZRUqw7hD3Lg5xMKFDGplQ9/SKfVHRYAjdquuiztaeS6udGbSlrXiDBMaIdwDI7arZkq90/MQZ6Cj4ox6WNxJCkZe7vXz8l4UV5InRb+/jlnZiIqbQ0PhTbLpwSequNKikgiiNLdpM4vh4sb/IN2NwH5rkHddGkkGmizu9GKzJL8EFEghe7sskubQMEhrHaq5tiMQHIODWkx7WfTEQDxzVqYJoSdzCIL9zyPVCYlPZVngZBbkRqwvRShqIJ71uBQ/WPYpOofcrBf3bSgP7LMoAoo4t1FgINJx3i+zs8Sl26L4X2ZLcxKwuIZuIoHvUM10EFBxsQHmSAqjlQVjMSZjFzkPrKioqKioaBr/ACu/7im4P67fAAAAAElFTkSuQmCC>

[image36]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAk0lEQVR4XmNgGAW0BAJALAzEjOgSMNAJxG+B+CQQnwbiG6jSEGAAxIeAWAbKB5kG0ggHIIEJQPwfymdmgCiuB+KLMEUgIALEVxkgCh9B8QYgjgFibiR1DJoMEHc9RxbEBmAKQY4nCIqB+BsSH+RuJyC+hCQGBqwMEB+uBOKFQPwAiFcxIEIAA0gCsTgDROMooAEAAE5uF3DBXYAKAAAAAElFTkSuQmCC>

[image37]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAaCAYAAAAnkAWyAAACN0lEQVR4Xu2WTaiNURSGX6H8RX4if/lJJgqlFDHCkIQyIEMMlIEilJRMFUoyUJQQhsrA4GZiYGAkIwNSBgZGhmI9rbU6q31v3brc79zyPfV2vr3XPud79zpr/0g9Pf8fM0xXTPeKHkRsa9OPrpnmR/xmE1sR/Z0xzbTT9NP0W278SMTWxPObiJ2MsXwHjprem36ZbptmRn/nfJAb3N8GjAvy2Nymn0lg+njT3zmv5QYxWtlk+h6xhU3svml30zcUKBcM3ip9lMFD092ILS8xuCNfM0MnzedihX1y8wcjVs0vNm0o7aFySW7wkbyW55meystmm3xB85mcLs9D55Tc/Ijc+AvT6oitMn017ZVP7Ib+zSLlt/a0nROBXQbzn+TlUTNL+3OMIfvP5BP8W5aZzrWdEyHNY5Jar+Z4CZM6rCm0w1SyrtHbJsZERkwfNYV2mMp60zeNXpgJu9BFDU7XFnak66Yfpu3Rt8N03jRdgwQApzbjD8j/Vc6Py6aN8msGWzTfeaLR586YZF1zdxnLIOaXtp2FQ/KDrr7smNwcLJGf4sBY2o/l71ornzAbwsoYw4TeyTeScZktz8aiNhBwSRsPJo+BhAMvE7FLHk/WyddRhX9uVjzz73+Jz07AHNsqZOYSJvLctDnaZJQ4bdYQpl9GDK6aXpkWyEto0uHlmbktGmQ6S4YyOhFjGEumz8YY1lyO5wJICZ5Rh5mvGWLR1VsoMa4UCeVUL3rE55R2xjvJek9PzyTzB853ZYIoQKV8AAAAAElFTkSuQmCC>

[image38]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJcAAAAaCAYAAAC6sc5/AAAEpUlEQVR4Xu2ZXahUVRTHV2hipmZkRSl6Ey1Ss6ASElGDfDBRxI8Sg15EfBGNgqRCGYqQ5L6Y4IMIIhG+hCAk+uDDRIKQLwql0QeYSCHRm4Eifqyfay9nz3bmNtM5M8ydu3/wZ2b21zln77XXWmePSCaTyWQymUwmk+kbJqoWqR5KKzKlMUq1QPVUWtHPjFYdVl1XvZbUZcpjveq2qpKU9zULVTdUx1Rjk7pMeZxR/aN6Pq3oZ7aL7agtaUWmVP5VnZARknpsFDOqVOPjRplCPKe6IvfPMYbW12BEJJd/qX5WzQm/RzIPq5ar1rYhkvQH6NyAB1VPqp5W3VKtE5vjJ+JG/Qw7aXNa+D+ZrLqpOij1E/6h6pHot/O66m/VG2lFSXR6/FYhrx1xOS07FRf9clpRgJ9U7yRlF1RTkzJnmTSvK4NOj98K74vltsONA2lBO8wQe4t5NK0owCVpz1g/l87u6E6P/19w1PONmPcaTmAThSLaSqkPYexwDvuK0I6x4jlPpoUl0u745J2E0TQBH0rfqsbRuQlTVBfDJ5CHbbhX27twZFLo3PNLsQEwrrdVe8Vyo8/Eks5qaEcdoY3kdI3qnGp6qLsstbCDUXlIZJxBsQSWsODQ3/ty/MELRSPi60xT7RIb/xOxPvvFForNEIecVsfvFuR7JPMwU3VU7P6Yc+7vlOpx1e9iYegDMc/PpmBzuOeDVarFYus2O7RBbIqlqmtiz898vyh2HeaQMuZpt9h6bFU9q/oltIG3pP6kgGs0e1FpiVdUp1XfiZ3SYxADYokwRvdHaMcN7RMLLz9K/WLGiSqT4iFxQGrjzA1lGCdG6hCy6J/yjJjRfiF27a/EJm9ANV9sUtwTxO671fG7CXN6XHVEdVb1UijHIDim4OQelog902qxFyOfY8owPKCO3+6NXxAzDsbEoKpiBkJ/Nh5r+oNqltg/AztD/Zti80rkcuL0gTklAhWGBZmUFordDId+gHFsCt+vql4N37mZj8N3wGulIbEitYNDHob+4CGLh0ohCefvKCaY1/00Z2pm0K2O323wAESCOOXAGPCq5L0p8YYkV/stqqO9b/oYvBvexmFdMcqvxebwsagOGNf/LcDgqrWqu+Vu0KXjC+OGQ47gD8tFuXHgQXH7HBZioAfFHgL3D+wg3h7ZbQhj8Zv2SaJ/ekyxQurDbUxq0BWx/vNUH0lr4/cCh6TmaVIwvAnhO3NWFXs+YOM1Wvhfpd4T4Zl4frxdI/D2fg2PUqwjc4WTYN1wCn7d0nBL5gZwuywasR9ws3gndiPnVxgdORoHhVWx/IwFBT65aYyBUMfD09/7/inWnwciB6Dte2Ke6LzUdjXG+qlqTCjz8X0T0J5cZajxew3m9nupX2CeATAo5pvFJXrgkd4Ndc1CPXMX/2/pa+g5MGNVxOaSsT2PA4yZ6wyKzRXXoz5ey9LBS7BQMfzGO3lYiheOOmJ9TBrSaONltI37Yyw7ot+0cy/ppG+zjBeXDTV+L4LHb3Rij9f354rTFt5M0zkANl4jaNtofOY6JvWg6e9hD15mW1qYyRSFnbRHGudZmUxhPK/LZDKZTKaL3AGaXtDlSYE/2gAAAABJRU5ErkJggg==>

[image39]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAaCAYAAABIIVmfAAADxElEQVR4Xu2YW4hNURjHP6EIIfeQCYXco5RLKRKJBymKUtTwQEqhlIzkwYsHEcnLKCElJZGUXWoUU56kxAPhDSVKSXw/317OOmv27cyZc2Zk/+pfM2udtffa67vuLVJSUlJS8r9zUHUx0BDVUNWxhLkdtkwWBOMXVNPiub4IzzMnVncYrJqq6hdOiJ1XyBixNZlwsaWqN6pfqmeqbfH4QNUq1eF4rl21WTXlz0qRiapW1VvVGdU6KXDDXoL9fVFdj3VKatsr58DZRGKGDOF8XomdEc74XvVSanDISCqHHDJBbG5DOCFmpGvhYB+DPX5QzfTGPqvOqwZ4Y0nsUX0SMx5nEEm6AXx1qFr8H+TBwbPwjmqQN84G2ShzRILPKNVt1exgvNEQnXdVL1Rrgrkk8H6i2me32DOdDMbTwPmyDJDkuDVxRJJvsELsYZM2i0FCozSS/qr1qk6xtMn/efAskXSNXnegDyQ5f4c03AAuzz9SDYvHuNEt1bJ4zr8JXo/3EwXNYJdYGrmsmhHMZUH6pL6lGeC5anQwl0QRA3Cvo2I1YHL1dD6EKDdgs1wIyH/HxUKeuSvx30DHszH+u5FgYArmaansqxbyDOA/bxZ5BviqeqhaK9ak/FDtleSOKRE6GG7wTbVI7IG3e/P+zTmUtLw/T7UvHFQOqSaFgwmw4SViHcRWsQJaD80yQIjLKPekYLfFoXP4zgBXpXohF3utGicWGWmWvaS6Hw6KdRILw8EERoitJ7qK5Pg8essAm8R+/06KOd5fA7AIz8MLfdxmXVFuNDfFcv5OKehBKeQV4UiKHWjW7+eKFXO/HrrfO4fOxXkKiyiuoYczTu8cqbZUTzUM9nRO9VHqK/ZEJW2nzwGxZ6JFLUKWAUg3P1UrvTF3fZc1chmpeiq2yM/9Dj89JdEmVny4IfUEqBP7xYzZHo91F2oBkUnvTwSGDpIFB8a+Wrwx/sfRXHTNl8rLFp1fCGmXucfSNaUMF3NKf084K3WMMymEC1Xyb2hhwAtPSPqD812IA6KtcxYnXeHFXK+n3heoC7wDdIq9ExStEx1inwpaY5Eyxnvz7JG6912qo8V5fqhIqs/piVgLTwt6Q7rxJswbLy1U2rcLNpL1wsJ6HuCsdDUSH7BWB2P1wrsAUdUWjKeBoYhe2m0cJdxjvRChi6Vy/aKO0WPMEqshy1XTgzlSUhi2JT0MYUsN4QspqcqHTxj+96WSBkFODA+a9EPuLWkyFCSKMB0V39FLmgxtGD023QodUkmT4cVprPRCN1BSUvKv8BtfKd/YeejWxQAAAABJRU5ErkJggg==>

[image40]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAAaCAYAAADovjFxAAACZUlEQVR4Xu2XP0hVURzHf4KCoSHSoJLSEE0JRQ6C2lSDDroUJBS0lYNTUEFLhLiJiA6GCOIQuvgPCSEaHjk6OElLDUVrODmJ1ffb79w693fffe9efU8dzgc+8Dw/3+X8fud3zj1PJBAIBJI8h3PGBtgIXxeJPdavyU0z/hZedbHzwC14DdbZgKUG9sBv8DfchQ/dOL98B750sUV4H175+02Ry/AJ/A6n4QC84GJnSStcFZ3vBvwJR2P/kUJB/idqaRONDdqAaKGW7eAZ0gQ/wh1v7B489P5Ohckz0few3huvhbMuxo7wuQQ34XUzXinmRZPKCufN+TPhPhNjp7LDS/JKNNGC6FkQcRtuudi4N05YFFuYSrICO+1gCdix3NYHsMvEOE8WtSTRvt+GF90Yi7EOe13M3ypcfXYBu6FajMBJ0fMpC0ycBUgrgu3yBGwVJspKsqKEk3gjOgnG3rnPhG+CIfe5WnArcBHYjVkoV4SCxLs8AU92Jho9gCvwyIv7W4Wrn/cc4AHaIlrgvN4VXZxyXXfiItgHLEn8dccifBVNhB2StUUjbsA90ddpXn/AIzglpZOwOfjkKgKTHYbd8fC/rRIdlKcFO2gCrtlAEcodjMVe/zGiBzDZTUmuNMf3Rav5IB6qGpzDC9Hzp+ytT/SWyzvCL9Et5MM3w1MzlqBZ9ILBZP2zICKtzarJjGhX5qEdfoafvDF2NeduFzYB90oBfnCfLbx6jkmGB1UQriqv5nnhb5ovom+8Z6IdvBD7jxR4M+yX9B9AvDKz3U4Tdudxi87twyLwt06HiQUCgUAgEAhk4g/N3IwWJGY7zwAAAABJRU5ErkJggg==>

[image41]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFEAAAAaCAYAAADPELCZAAACsElEQVR4Xu2YQchNQRTHj1CEJAuEiJJClKJIKRQLVoqi7LBWKBtJFkoSC5KShbAQJSlZ3CIbCytWLEgW6ksUO/H/fTOXueO+7755vXs/aX717717zp2ZO+edMzP3mWUymUwm5qh0NdI0abp0ssZ3wDWzNZH9irTU+/4FJkhLpKmxowHmvVKaEjt6wUAbpHfST+mltM/bJ0tbpOPed0PaLS0abWk2XzoovZcuSjss/YHbgue/Ln2R1ka+XpA4zOOrdEcakc5awpwK+xOomHnmfDtjh7lA346N48gq6bW550XfrP8gUk0fpeX+ep30WbosTSpvGguCx6APrZrGNKYTfGRkyGzpgbQisg+DhdI1aWbsSIDqSgkic6QKQw55+5nIXssJczcX5taEkk3SI++LOyKocWCHBc9w19zaNCgpQWS8umrjGvuTyF5Lue49lWZ4Gx3flzZ6X1jqZB9ZSDa2xWHpvLn1bRBSgthrySqD+Cqy10IaczMD0yEwiVPmJoHvpv8O7MS7/Pe2oJT5EamGQRhmEOmrEXZWbi4HJQP2B/6w1Mm+1HWQDWiOuYdN1VZzk0jN+s6DyEAMWA56y6pbOx29NRcIMjS1xFabKwmOQ6n6IP2QLlh1vW5i3IJIg73S+qr7d0flRtMVZPA56V7s6IOUIDZtLEVkr4VfgkFpwIYRZxp2zkyFtKfqag2e4Zi59ZdgppISRGCOHGlCjng7h/BGZkkvzDUI18KSsNS7gABeMlcVg0D7T9J3c2vqxKp79AzKErE5sD02t2Qt9td8ck1S9fXWQjoX5jqqW3dGpNP2d4a2Ba+UnM34TCGsqFhhAmyTnpm7v2SB9Fx6Y+51lk+eYW5wz5jwZrLdev+BwNrAu2VXkDlUR1c/WgnjEmyOfMus+/EzmUwmk8lkMv8JvwDv2rCviuD1ZgAAAABJRU5ErkJggg==>

[image42]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAaCAYAAAA9rOU8AAABrklEQVR4Xu2WzytFQRTHj1AiC1ES+RULShaiSKEoFkp+rGz8FZSsSDY2rCSlniILysLOwt7GioUslK0FZWEhvt/ODOdOlHrvziu9T33qzcy59543Z2buFSlQIDsm4O4f3ILNekl6dMFZeAY/4IJre4/hO3yFPXpJ+myLJlMUDogm+ADrgv5U6IBP8CUccHBGDmFZOJAG86KzcmX6akRLR0bgphlLFV+iPdM3Do9MOwpVojPCZHZEF+0KfIZLJi4KtkRMjPTCa1jvg2LB0jCZffneSYMwA0t8UAxsiThDHs4Iz5+odItu56gH2m+ciM7KKSwPxixTcEh013XCC2cFnIFNLq4RbsA12C56UC6KHpZ3cNTFJeiHb6KJhP7EtGjpmABhCZlAC3wUfdgAPIBjcFj0wUym1Y3zd852J2/KG1r4kuWf4nHQJ8kTehmeuz5uCMYxPifwRvdB36TozIQwASay7tqckVtY+xWRJbwxH2Dhor8x7Ta4ChtEk/Q7lDuWaytncIEXh50O/uNS02aJuL4qRd9xecWWKK9Ui36MXcK55FB8/CuFizjK98//5BO64VSDUPLDVQAAAABJRU5ErkJggg==>

[image43]: <data:image/png;base64,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>

[image44]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAaCAYAAABhJqYYAAAA3ElEQVR4Xu3RsQpBURzH8SNMFEVJBmWzMTAZLQaLLJ7AI4hdGeUFTLIoi9nCIBaDDKS8gE0GBr7n3us697iDwSS/+gzn9z/d0z1HiN9KGmtcUddmb4miihsK2sw1QRwQ0wduKaGll2rk1yLwoI2ic/zKHFtsMMECKccOK3k04YUffdwRUDfJ47rWQE3DpRMJHHFSOh9GWmckhwtWSievSl7ZTOmMlIV53EDp5CPIx+ihhvhzEBLmX4+tdQVnYZ4mT+1YvZ0M9phiiCx2WCKp7LMjryusrT965n++mwf7qiSKcZnKsAAAAABJRU5ErkJggg==>

[image45]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAaCAYAAADWm14/AAABuElEQVR4Xu2VPShGURjHH/ko+Y5SKINBLJSvwkgysJhQVoNSLMpkMchmMigWm0FJiOFmsBhMKBZESkkppeTj/++5p3Pv7bXcOme6v/p1u+c8732fc85znyuSkWE5hg/wBd4m5rwwDFfgL9xPzHljQTQBXr3TAB/hHayPT/lhAP7AHVgQjhXCGphvglyyLLr98+H9OLyBF/DABLkkgF+wX3Tls7AHPsF7G+YOrv5a9HXkcZByOASrTZBLmAB9g1swLzbrmDL4ATthKzyDE7EIx7TAc1gV3rMOdmERLIZT4bgz1uBk5J5dkc2IxbgOB0WLktdPOAbfYRusEK0bc2RzsAMuihbxaxjPMbZ4LjZGCTyBzZExPvQZHsFV0UTaRV/RAJbCbtE/XQpjG+GMaMKcZ3LTYneWCfCYRyQH/EESVj41K2NzYpPibhlM8qeiD64TG8/rtth47rDZtVTUim7haGSMiQei252EHfRS7NFuwkPRmkoFC5MNKXqGXCUfzC5K2LJZK72wS/TTzt+RK9FjSw3rgG9FLphIZWKM278h9nvinej2e6cJfsM92JeY84L5fPMt4RFk/MsfqjJKuZoaTcsAAAAASUVORK5CYII=>

[image46]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAAaCAYAAADi4p8jAAACeElEQVR4Xu2Xy8uPURDHRy4RQuSSa7JxV7IQSwtZyLXEH6AkForyxs7GSlhJuZSUlJWFy8KOsrAhJQopOwtlJfH9NGf6zXv8XiyeR+/z9vvWt99zZp7n/GbOmZkzx2yAAQYYTdggXvlHzizfdApLxX3iWfGneLGMgyfFF0U3vXzTSewRP4mLaoUwUbwjTq4VXcEs8bl4qlYk/Ek36rFe/CpureTn0vOZ9Nw5HDLPsYVJNkXclsadxTjxmrmDB8wLCw4/FJen9zqLjeI38XuS4fStNG4DFK51tbANHDbfvVdJNkG8ncZtgLzfWQubBo7cNXeQMM3yzWncWVBU3ps7SN6NOZw3d+6luGy4qi9umufnbvGNeNw8j8jXx+WdG+bd0K7yy3urin6qeMI87zlXGVPIjpkfUXRNzD9DfGo9MH5UnueJr8XTPfXviHMP5zLJO8JzJHwWj4hrxMXiDnGJef5GBODgE/GguVPRIKw174TomDDyWZKvNK8F04oMpz+UZ3DUPNJA6Fo5wt6aL8QPcW+RbRLfmRsZHdHVohvJEPI7OxC1IEDxYU7ALrNQUdWZj28bP8K2mBsy27wvZacAK49TOEfofRG3Fx1G5uYhQOjiUBwTc6xXxaOCXxZXm+8280Qk0F3dt4b74lhFJiVHLpk3BXFeYiyGXTC/VnHGgX6GhDOENE0FIP9iRyPHWCT0fM88OLjCPKdzC9ko+PMwHhCeGEZO97srjq8FBcjZ8QBzTkrjWh8gPNnNfjeeVpDDsw0QIUPidfOdJGz/VggbA39OVf1oflkmjJsGTt0TH4j7zVNh/rA3/gMIpzZv+sw/V1xQKwYYq/gFrA90BWWAA0QAAAAASUVORK5CYII=>

[image47]: <data:image/png;base64,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>

[image48]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAaCAYAAADIUm6MAAACHElEQVR4Xu2Wv0scURDHRzRE0WBE8QcKoihRBA2IgmAVJKVFVCz8A7QQC8EIEeQaG8FGrCRFUogIgpWFKOTATiuLIAQCUYQQwcZKsNDv13mPezs5wxnw3MP7wIe7e7N7O2/e7NsVyZPneVAET+E5PION0XB8KYCz8BomYVkkGnMG4Q1ctoG4k4QXsN2Mx57fcB++soG4k5NtQpg4+zynaJYc3E0IK52uTd7A77DLBrLAEvxsBy0Lkr5NxkQTr7KBR6YCHsJxGwhheyRFt8EG+C6IcRXWRZ+s2YS5/IJ9ZjwCD+L+XQI3YHcw/hP2uN98un6Eu7Dc/fbbZxOcgldwCE7DSz3t7lieMwFr4DH85GJHoseTQrjovrNga6LXuBdWcwV+gzOSOti2SQf8I6mW4nn+vnjrTIquIM/pdbFJ0erVi24CJ3BA9PwD2OpMwHnJsE08TLbSfXrsrPkuwxcwthNhch/cdxJOxFMK9yT1P0yYiXMCrD7Hh+F70esTu9IPJpx1C/wqmgSTIf2iq9AJX4omYm9wjjEJTppwE9iGxbBOohP3hCvN9n0wrAyTYyUSohffFK3sC7gK21yMYzzWvucwQSbqE/8hmjxhSzFJD5NMiK6av85oEM8Y3ixMmp/hGCvBxEn4wPJj/4LV961G+H/V8veDj7/tWFaZg19EK88ef4qt9b/YgjtwRPQpWBsNxxffCrwRX5tYnpziFoRpVBd+uJb3AAAAAElFTkSuQmCC>

[image49]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAaCAYAAAD8K6+QAAAChElEQVR4Xu2XTYiOURTHj4zCEDKZmXxLSeNjCiPDRlEohI1StspGmTJloUnsLITFJBJlQVM2lIUyWMnKQhQKJQtFSTby8f917u257juz8rzq6v3Xr3mec+773Huee865z5i11FJL/0oPxDvxVdzIfEVrt7gufomjma9oTTAP7LvYlPmK1jrxTYyItsxXtA6Zp+FgYpsWKFrs1E+xJdxfEi/Ea7E1DipRz8QbMVd0ifViwBp3sTgRwH1xWywMtqVijZgYB9WsY2JGbqxTdEQCg/fi1J/upum5mJcb61SHeRrOF9vER6t2rWjR6tM2f1zsDNfUWn+4Lk50wPRQPm1eWz3mn1ex5e8X18xTd4/oFEfEKvPDPdbLVXFOrBR3xD2xzHwexpwR3VZ94ewzn/+z6Au2DWFMFBn0NFyvMB+7t3I3ikWPijmJjQXRSB6LtYmd7vhBHDZ/OE1lh1hg3lWjCOyh+WJeil3mL4OUXyQ2my+cZyCegS/tvgeCDfHbC+brRLyEt2J5uB9XM3OD+W5Mzmy94pV5k/mR2Ellzjs0SzyxKgvGW8CQmJLcL7HqDCWQK+EvYi08nxJBfEwwB3P9tTaKg+Z1OFvcTHxxIkQKfzJvQqTaqDV+vbAT7DBnJiCCih1ysXkgNDPO1NXii3ndMz/9gFSvRdTJLfNd5E2eD/b48cxkXJ8VF8WkYBtrAQTBTrIDBIGo65gh280DHwr++CIIjEZGfZGqtYmJSQsWHUUaskjear4z7ValU648zadm97k/iux4JKbnjrpVa76PIepwWJwM93fNd7KpojvSJfnP+0Tmq0vUM23+svlxQ2qTCU1VPNBp+81MDVKfEkjPtZb+K/0GMOFqGar/yVAAAAAASUVORK5CYII=>

[image50]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAXCAYAAAAYyi9XAAAB0klEQVR4Xu2VTyjEURDHRyjCSZEowkVKilL+nFAccFGU4oaLnFAuSO6SIjdKHJWknLa4UW4uOHCXkyu+39+8Z9/O7mZb9iLf+tRrZt+8N/Nm5yfyr7+iBbBnKAGlYCWFb0q3Saux74IG50urPNAJnsAHuAUTzl4IesGS8+2DUVAb7RSpBtPgGWyBQVDsfN8qJvGgVlWiviHrEL3UsTVmIh7EoGegKLAXgB3nY6ahysEpaDb2jLQsGjQm+nZePeDc+TYCO8UL2EtkLP9Ol6DM2XjwCehyvrDczIrZMcusxEZhUDYP34yaBWuiDUTfoVtT7Mhht85KbIjwwDrRDGqc35b7QLRhrFrAnDVCixKPFakNvDm4PpLEFueBj6BSNHOfadbyBzLwOOhIdH9l75vox2IZ/Z+fpbQZ0P4qWtaxRFekEdF9d6ApsA+Ivv1kYIsUHnhvfNS7xC+Tapqsik4glp0Th2Inz4tePmmgsBli4MKtrV7AuiRn7sUBwXffluTf1IM+Y4s2MP10w5ddzIGeTiwjK9QNGo2PGSd06G9oBlyLDnRWIhQnVDguf0X94ApsgvbA7p8qJ2Jwmwnf78HYciL+hfiNvBH9UOdcHOoVID80fgIqV1+cHLFJqwAAAABJRU5ErkJggg==>

[image51]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAWCAYAAAA8VJfMAAABsklEQVR4Xu2UvyuFYRTHjxCiCBEpFpsYLQZJijJRBvwFxKDIpmQxIZMYDEqkyGIUBqOBlBgIIxNJ+fH9vud57z3vQ7pd14/kW59u93ue95znPc95H5F//XUVgAZQ7Qe+SivgBCyAbdAL0uyCVCsTjIJ0492AHvM/5WoHNZ43IvrGeZ6fMrWCY1BrvC0wJdEWsyPFEu9IqfOSUgl4ccyAQrAPysyaMH4JBsGh6BE8gmGQI9qVdXDhuAZtoA4cOY/Px0QjTPwsOslWzeBONL4mujG+5Zzz+MuuFIFKsARmQbbohjZAn4sForkDykETOJV4orB9fOtzh+0Axe5wva9b0bzLot2IaAhUmf+5okmeQKPzPirKoeN6f+hYiP4myLIBDgb77St8gAmpZIrWix4JN99hA2EyXxWih55I0Ql5v717oEv00jnzYsElwKD9POZFbyn/TJl8zPl2kDg0FD1OKwcnvE4zwCoYB/nOC767B7ALBsC06OHHFki86BWYBAein8096BfNYTdGFoMn9fIJvUhHWKAFdINOeXvv+u3lG33qckhEftFv0Y8UZcstjZHob9crH9trxuwi0+oAAAAASUVORK5CYII=>

[image52]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACYAAAAWCAYAAACsR+4DAAACJUlEQVR4Xu2UP0hWURjGH1EhSbJSkiBIJwmniAgCEZyMqMGCEMUGDQRx6w9NDU7i4CbiEukSBTmEOBQW4WSDkwjRorhIoCjYIKU+D+85957vcC/yQR9fiA/84N73/HvOe95zgFOdqnzqjwNOFeQSaSeVUVvJ1UTexEFYfJEskymyQTrCDqVUNXmNbGPfyCNY1iR9b5O2pEeJdJV8Jk+RbWyVNEYx9cvq+8+kTE2SXnIP2Ysdwoxfcf8yuUIGkx6mWnIeltl6h89y0XpApmEG84z9gpnbJ8/IDHkHMyKtuXYxS9Yd6v8TqbnrsOz79u/kMhkOYom+kFb3nWfsLtlDuvg4qQnadVtfuba/SG+tSuQHbPOSNq9s3yJ/YOup7zWyRDpdP9xH4QJ5xhZgWTpHupEafI40GxqrWDy+wcXvRHGNPSATsBufSLv8FAaQbawKdivrgtgH2GKbpMXF8ozpuBV/EcU1n+pWbU/CBk2kGvBnK7aC2FtyFpbmHjfGS0ei90yTah6pWGPK9EvXpuNOdAZWeCF95L379jfqBtLFQ90kv3G8sQsuHh+l6m6ODMDqUpvNlBp0/T/CMuUlc3pMbwexi7C6G3Htkjemvl6++MONKYNdsNvrzTTDxumSFUi79AXt+Yr0ORiD7UqTDZFdMorCXXpj8zDTmnMH9jzEfTzecLh+0dI110SP3Xes8Ci1obAcyqq8Giu7/ktjunEPA/TEnCwdAUm/iJBVD8e+AAAAAElFTkSuQmCC>

[image53]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAWCAYAAAA8VJfMAAABWklEQVR4Xu2UsStGURjGXyGUUiiZLCxKBoPVYJAyUf6IT9lYlSxGmWwGpaTIPyD5AwwsSiEMBiYGEr/nnnM/554+d/h8l6946te993m757n37T3H7F9/QQ3QH5tFSWGDsA+X2VIxGoI3eIZ3uMqWi9UIPFmdhTZDNzT65x7vfUt5oWq7uIF5OIUHeIEFaIN22INrzx1MwjCceU/vZ5QXOm6upuBd6DT3lxve01XD2AV9sAXr0GrugzSgJV/LKC+015wvdB9qzVxwrEc4gm1z3aioakMXzYWqvaEUJP8AWqJaWbUOHTW3nrbjdFQrq9rQFavc3mOYhXO4iGqJNAQT8Ar3/jlUGqrFl8wNUThIGhpJnqZVgzPgvSbYgWXo8F6yYLolQg7ts2Vp6C2swom5baNTbM7c3g0/TGwmb5pNBV6ljnypuL36o5ocDnmKQ39EvxI6EzGWqda7PgDX72ZwRSN/HwAAAABJRU5ErkJggg==>

[image54]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAWCAYAAADAQbwGAAABPklEQVR4Xu2SIUtDYRSGj+BAcWUYRBS0LK0INmHJZNAwBMOENTELIqzIGFaDZWJTEH+AiGBaN/gDxOC6mKzq++6cz52d3QsGg2EPPHA5786533fuRMb8FYfwIjgDi/A4I2tom6yE+jmLE3ANvsIv+ATrVi/AdXhk2SXchktsBAtwD/bgGdyweh/+ODVFyqLZQQxATfR0I6SBd3DK1SdhxzKe1DMLb2El1Ps0RZu6ortLVOG9ZSeuTviC+JIfuDc2cZfzVtuHLdF9Mru2Z8IPsGXPmWzK8MBl0essWh5PfyX60XLhF2LTB1yFp3DX5X4gd5e5Nw+HcFgaeAOnXc6BL3BOdBXp6rnwmum/yKvGBtbfRU+5Mxxl4wc+h4x8yuBl/uS5lOCjaJPfXcKv41dw2V34YM+RN9iW0VWM+e98A/8oSbkhuBLtAAAAAElFTkSuQmCC>

[image55]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFYAAAAXCAYAAACRUrg+AAAD3klEQVR4Xu2XS6iNURTHl1Dk/chbIpGYeJZIFCKPEuV1mUgGHgOKyOCWpJBCMlEukkhhoITB8SjPlCLyGCgxUEwYII/1a+11v312h3vOvSd9N+df/875vrUf/7X3WmvvT6SGGmqooYYaWjm6KqcpO6aGVgC051J3O+UZ5Vfl5MSWd7j2XOqeqvyuvKzskNjyDteeS93blL+UG1JDK4BrzxXWiIlK2TlulFOkmmFBcqIdEf2V75XPlaPDczVQaWq2T180AXSOk0w7z92LWuQAP5WnlW1SQzPQW3lDeVyKx9uq7BY9O2YoPyhnpoYyQB/XnmKQ/HnOf4JOyi/K8amhBWCsSsbbLZVHOLqvS/W1Vw3DlA+UPVJDC7BSyh/PF6hSoJsyUG3tLUVjgCyU4rQlhdqK1a+Lypdid8WjyrtiqUXb+WKHxQnlWeUIMWCLx/Nx4lTHdkV5UnlV+TGylQt0c2D5XOheIpl2dPucaH4qduvZqTwl5k9c1xmjIHYnvqC8FN4z3nLlTbHr6JTwHpBp+MYa7FUeVN6PjUQYYPADYkJ2KfuITQaWKp8p+yoXKx8rhwTbWzHHANFDFAHG2S92sGwO7wD9vS/OEnkpZisfKrdI6YMN3Sysa0d3nWRzFiSbk/lo/0k5Kbx7IsUHNW3wF6AJn1gP6vQ1sXH5CFkf2gACgzaLlC/Cu8YAmqC8I3bgsFtxsa8XiywwRrk2/P+snBj+E/o7wn+Ao76wjnrJPjmJNPoDLwM4nWKd8pvY4bQgsQF0c+i59vSQQnf8mftGMqfTrJormSb8ITLRxMawGfhNNqQb/Epsc3+IbYz3bQRRmF5V3GlftBViiwtei/UB1DoEjxQbA8FweLBzSyANBwZyoac/oK87nC6MAwdLLSzA0VLamZMN9jkBc3pWDVXOUQ5W9hNbQHSAWBNabym7BFsMSgIlspfynFg58L5/BXfcgljkkLbbxQYC1BFS3lOFBad0DJCsj0cHv0zGBuEQEUt/7/tOrH+phSXiqIejUkMTYE421ucE8ec6Ecoi1wc77anJ1FP8RBOL5Fr9cKQUUJo86BgPPw4rl0nma5NYJbZjFHrfbcC9cY9YsUb8IeVqyQ6585J9AfHRwaHnUccC0t/73hPrXwqzlA2SbWi5YE5qrs/JAhB9jrHKfcp54ZnIx58GMT2+Cbw/ojwmlgGbJCsvG8M7spOsoi1rRGkqC74rMXgmBTwC4mjD1jN6BukdlTb+DkGlopUsuS22CM1B+mlLNMZI7cBrZHxmANr6wRaDMpTW3fT5v8V0sQOKOvtI7PaTBlINzQQRydWrKtH2GxxiuiqUUN7EAAAAAElFTkSuQmCC>

[image56]: <data:image/png;base64,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>

[image57]: <data:image/png;base64,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RERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERETOKf8Pty2iygd6cPMAAAAASUVORK5CYII=>

[image58]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAZCAYAAAC2JufVAAACJUlEQVR4Xu2Vv0tVYRzGHymlSFBpkByKIoQWU9SGCHEoSqKgloYWcREiBBf9A8Q9HBpEiYaGRMIhQpe4NAUNLoViRT8QwyFEwSVBfR6/vtyv7znn3pvidj7w4XLe8573Puf98T1ATs7xUk+v0/PxjQo4Ra/R2vgGqaJNcSM5GzfETNGfdJK+pT0H7mZzgg7QVfqabtAJesb1UdACnaHjsP/4TO+7Pgnu0P6o7Qudpaejdk8d/UjvRe036Iq7Vqh3sEBjsP4+dAJN7Qt6M2ov0L/0StTuOUd/0adRezv97a4VSrNUMQ30E2wgz0u6g+QseBrpd/qP9rl2hdTyBP47VHjbrFDDUbtHs/wM1k82w2b8B73t+oVQd+lz2BLqQGWiMJv7v55KQgVa6CKK4eZhAQMKNeeuRS8dgb1YgquwE3OYUBrwEf0Dm6E3KAZbcv3S0P8t04vxDXGU5WuDlQIFEyHkOuzZUlyi20gesD2yNvor2MAPo3aP9oae1RgeFdE12LIp6CDsJHs0GZkH6SSdRrJYFpC+1zyazQKSVVxB9FJqD4VTAWpcH427Batpqajcf4AVw4COeVgWoTcK+yW83WVYkVQFD0U2LKFKReAWLFhAfTURJSu6WKDv6WM6Sodgn5DABVjt0SnzJ6uTfoPtSz2jk/eVtro+CvoENrP6xKi/9l3qyfNU0y5YqAfRvXLo2Q7Ys/rVdRoaV326YR/wnJycnHLsAp9xbhFvnR/KAAAAAElFTkSuQmCC>

[image59]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAZCAYAAACLtIazAAAC+0lEQVR4Xu2WS6iNURTHl1CESJ6lXMotEuVVokSIAQMSZaAoSjIwUGSgZGCgRBmIZIgBJRkwOCEpAwYeJQaKRN1EKOSxfu1v3bPOOnufzpWBwferf5299/r+3177sc4nUlNT8z8zUjW70kAZpJqgWqaaEsYM7z8sjHnGqOZJPmaIapyk93mGhnaWk6pPqouVjqmGt0R05pnqjeqC6qG0Jxr9+6Tdf6zqkuq56pzqq7TPY7Lqleqz6kyl+6pvLibLYtXR0MekeJCxTixSfZC0wsBuNSQla+T8Ifo/VY13bdiqequaXrVJkjiSO63apBpRjXWEhDDz7FL9lvzkDFb4mupX6F+i6nXtnD9E//eqGa4N6ySdgLlVmyQfqeb3R3SBrTxmHtpM4paUV4oXfVG9jgOOkj9Ef9oc+zlVm3t3RNLz+MBfJWlnPE7Cknwi6aLnsN1+oLoiaSdY9RMupuQP0Z8E6UOnVDskLeCCahwsSa4JxxXh3bHwlCZhSTJGTA7uHTHxuHI0SZSdKPlD9B+s2i7prlqy7PSkahxGqW6qNrq+5aof0tztNkqTGEiS8bgulWaxKPlD9L+sui0pqVnVuB3hWK099o41ccAoTaKbJCkaxNwJ/dwXdnellP3B+7PrL1U9bny/6rukuMOuP8LuMoeDccAoFQZLsiHlY2B3shH6SZJ+PEr+4P2nSb6Sr5B0fK9L+puiEPVJa7XO/W21cVbShD37JE2C8l/CqivFw7NQWst+zh+8P14b3JhhCZCknQqeu+piJko6Bcy5CEbxqNDmP9C+NtZK844ctyBlveqnND+zqHLnJVU/I+fPb+/P8xSPzdVvoBAdkHQnp1Z9FJwbkr6OgPfxYcC87Lki91QvVDsrxarGKt5VfVStcv0Y75b0F8Kd4G7wBRSJ/vz2/nBI0l22+0UMz/W4GN63R/VOUnKPJd3bvS6mCKvGkeGsb5EuViXAndumWi35j4fo39s63M9oSR7EzZT0XA6OKDHE8kxNTU1NTc2/5g/2ZMODvrGWmgAAAABJRU5ErkJggg==>

[image60]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAZCAYAAAC2JufVAAABqUlEQVR4Xu2VvyuFURjHH6HI7x8lC6UoEyUGyUQxUKQMFmVgV5TdX4FksMhISdINEysxYpGBQTEY8P12HJ77OOf1o2t7P/UZ3ufc873PPec954qkpPwvlbAbNtiBBKZgpy1G0PmFZizIBryEK3ALDmaNhimBe/AV3sNr48znR6VasvPv1FiQAThtamdwBxabuqYVHsNJOAabYb24leBcD/Nf1DOplYT8PLgK+0w9I+7X8Itj9MAlcRmaWXErQny+bapUEvKr4AnsMPU1cdsyZOqadvm6zV3wCDa+P/v8x49PfBLN53JfSbypeVNPogLuwn5V8/mxpoL5bIYTctHULRw2NZ//q6ba4IPkpqkb2GRqPv9XTeVq++rgISwz9T9tX+xFXxc3adTUY/D08s7i3aWJveg8ldH8ArgpX09RRsLvWowFcatr8flsQMMrITG/Bh6IOz2eZziunnl0GRw6xv5mDzVFmM9LVuczW+cHOYf7cAIuwjmYr8Z575zCC9ii6qQIbsNlU9fwktT5T5KdH4R/kL3iJo2YsZ/Apstt0aDzuXopKSkp3/EGLJplA/xefksAAAAASUVORK5CYII=>

[image61]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFYAAAAaCAYAAAAtzKvgAAADLklEQVR4Xu2YTahNURTHl3xEviOSr1dMJFGSfA4woJCiHlHPCAMzSZkgSVIGDEjpZSAGCklK0okZAyORUhiSRFHIx/9/197uOvvdvc+9vdx71f7Vv3fvWvuse84666y1zxPJZDKZzL/mIHQx0GhoDHSkga9PD5NFgf0CNMf52s1waDk0IXRUMBSaBi1zf2Mw/ixpIf4Q0RN6A/2GnkI7nZ3B1kKHnO8ytA2aXTtSZDq0B3oLnYU2QKOcr13wPHuhD9Al6CX0EOoxa2IsgV5AhWhh8No3isb02PiFtBa/RiH15IXwTtK3KXSIJv9aaGwjW6Ef0G73fTx0H3ruFyRgklhUHibxC7TZ2Gx8+m38GfVlcZhQJu8ONNLYh0HnnY+Va5kE3YbmB/Z2sQ76BV0XPU/PPNEKm2hsIWxzN0QLw8I8MHFshSQV/4mxRTksmrxC9Ec9q6C7znfC2AkTHSa7ndgWZeETxta2MLBbmCh/7Dhjfyzla0rF/xzYG+JP8hE01tmY4JvQCuezP8AqZbWyajuFf8piF86KTvFT9PhP0A7RCmcR8XH3pOKzmivhwGIQHuCn4z7omGhvoe+K+0y4A7C9qBm2iA6/ZrVAD4tSldhGM8GyX+rJ9QqHbyo+fZVwonMhm/di6Ay0y/jpK0SrmFXaqb5qGWxiX0NHRWcKK5aVy3icKb6npuI3lVgmk0n1ib0q5bvHIK+gqaKV7Cu3kwwmsVOgfikPL055xvsmuq8lqfgtJZaLt0NLy+6ancH8MOsGqoYXrykGr3FlaAQnRWPudd9T8ZmvSuxd4FAKK5L2j6LtoLfsaho2e8ZpVuf0sCi+fYVbRO4GOLEnG1sIb0qjfagvMJvYWPxnxhaFE5H7MgayvdVj20Q3cUB0APmbzUe7H3r/d0U9EdzhjHA2Tn6+IMz1ixwPRN/CfItIxW9qznAoFdA99zmEG+LjMrCSOw0v9BT0VfTxvgW9g9aYNbwezgxfhR6+CHx3PiaQu57TUp4tNj738Y3iJ+EUXC/xf6JwEPi3kW5kpuiWcbUMfJuKwSLpEd0G9kl62DE+t4CtxM9kMplMJpPJZP4r/gCAhdu12zHtdAAAAABJRU5ErkJggg==>