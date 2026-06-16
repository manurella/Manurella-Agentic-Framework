# **The Manurella Agent Authoring Doctrine: A Standards-Based Framework for Enterprise Multi-Agent Systems**

## **Platform Foundations and the Multi-Agent Paradigm**

The deployment of large language model agents in enterprise production highlights a key system design pattern: task execution reliability depends less on the raw intelligence of the underlying foundation model than on the infrastructure layer that wraps it, known as the agent execution harness1. In early experimental iterations, systems were often built using simple prompt structures, where models were expected to perform complex, multi-step actions based on basic instructions2. These setups frequently failed in real-world scenarios due to unhandled exceptions, run-time loops, and cascading errors4.  
The Manurella agent authoring framework addresses these challenges by replacing unstructured prompt strategies with a deterministic, application-bounded orchestration system1. Drawing on engineering principles established in complex data processing platforms, Manurella coordinates data discovery, standardization, execution, and explainability across multi-agent environments1. By structuring unstructured technical documentation and applying strict system interfaces, the framework ensures that autonomous agents operate within verified boundaries7. This framework supports a structured transition from experimental prototypes to enterprise deployments, helping organizations control task accuracy, lower execution costs, and mitigate security risks11.

## **The Core Deficit of Persona-Based Prompting**

Traditional agent development often relies on persona-based prompting, where an LLM is instructed with a shallow role definition such as "you are an expert frontend agent"2. This approach introduces several systematic failure modes when scaled to complex production environments2:

* **System Drift and Boundary Creep**: Lacking explicit execution boundaries, the agent often attempts to resolve issues outside its functional domain3. A frontend agent instructed only by role may attempt to rewrite backend database queries, construct custom API routes, or make unverified system calls, increasing the risk of cascading failures2.  
* **High Output Variance**: Without a structured execution contract, the agent resolves ambiguities inconsistently14. The same prompt can produce divergent code layouts, styles, or libraries across runs, which increases maintenance overhead and degrades code consistency14.  
* **Security Surface Expansion**: Persona prompts typically lack runtime constraints2. If an agent is exposed to untrusted external inputs—such as third-party code libraries, pull request descriptions, or user comments—it becomes vulnerable to prompt injection and social engineering9. Lacking strict permission controls, the agent can act as a "confused deputy," executing unauthorized system changes or exposing internal environment variables6.

The Manurella doctrine mitigates these issues by separating the agent’s execution logic into structured playbooks and modular skills3. Rather than relying on a monolithic system prompt, agents are designed with narrow functional scopes, strict input and output schemas, and isolated tool interfaces2. This approach limits the impact of potential prompt manipulation and ensures that the agent's reasoning remains safe, auditable, and predictable9.

## **Taxonomic Delineation: Agents vs. Skills vs. Checklist Items**

To construct maintainable multi-agent systems, developers must distinguish among three distinct software abstractions: Agents, Skills, and Checklist Items17. Confusing these patterns can result in "context bloat," where an agent's context window is filled with unused procedural rules, increasing latency and operational costs12.  
An Agent is a stateful, non-deterministic decision-maker that observes its environment, plans multi-step strategies, invokes tools, and self-corrects based on runtime feedback2. It manages context, retains memory across sessions, and executes planning loops to resolve complex tasks21.  
A Skill is a stateless, modular capability bundle that instructs an agent on how to execute a specific, reusable procedure17. Typically defined as a markdown file with structured YAML frontmatter, a skill is loaded into the agent's context window only when triggered by specific keywords or phrases17. This progressive loading model keeps the agent's context window clean and prevents performance degradation12.  
A Checklist Item (or deterministic pipeline step) is a static verification check, type validation, or linting rule enforced by the hosting infrastructure4. These are deterministic code constructs that execute without LLM planning, ensuring that outputs strictly adhere to project invariants20.  
The table below contrasts these three execution models across key operational dimensions:

| Architectural Dimension | Agent | Skill | Checklist / Pipeline Item |
| :---- | :---- | :---- | :---- |
| **Execution Model** | Non-deterministic planning loop4 | Reusable procedural template17 | Deterministic, sequential execution path20 |
| **State Retention** | Stateful; maintains memory across sessions21 | Stateless; executes within a single window21 | Stateless; fixed input-output validation |
| **Operational Control** | Autonomous self-correction22 | Reusable and parameter-driven17 | Static verification and strict enforcement24 |
| **Context Window Cost** | High; scales with conversational turns12 | Low; loaded on-demand using triggers17 | Zero; executes outside the language model |
| **Implementation Layer** | Application-bounded service1 | Reusable file-based asset (.md)17 | CI/CD build check or system hook4 |
| **Vulnerability to Injection** | High; requires runtime validation9 | Low; operates within scoped parameters13 | Zero; protected by hard-coded logic |

## **The Twelve-Point Agent Specification Framework**

Under the Manurella Agent Authoring Doctrine, every agentic component must be defined using a twelve-point specification blueprint3. This framework replaces loose persona prompts with structured, auditable parameters that govern how the agent processes information, accesses tools, handles errors, and progresses through deployments2.

\+---------------------------------------------------------------------------------+  
|                       12-POINT AGENT SPECIFICATION BLUEPRINT                    |  
\+---------------------------------------------------------------------------------+  
|  1\. Purpose                  | Defines the agent's core operational objective.   |  
|  2\. Use When                 | Verifiable activation triggers and conditions.   |  
|  3\. Do Not Use When          | Negative boundaries to prevent scope creep.      |  
|  4\. Required Inputs          | Structural input schemas and parameters.         |  
|  5\. Output Contract          | Strict schemas (JSON/Protobuf) for output.       |  
|  6\. Workflow                 | Step-by-step state machine and planning loops.   |  
|  7\. Context Policy           | Controls memory retention and folder access.     |  
|  8\. Permissions              | Security scopes (Read-Only, Reversible, Exec).   |  
|  9\. Effort Behavior          | Reasoning token allocation and latency targets.   |  
| 10\. Failure Modes            | Structured error handling and fallbacks.        |  
| 11\. Eval Rubric              | Quality and security measurement criteria.       |  
| 12\. Promotion Requirements   | Testing thresholds to advance to production.     |  
\+---------------------------------------------------------------------------------+

The twelve-point specification blueprint consists of the following parameters:

1. **Purpose**: The core operational objective of the agent3.  
2. **Use When**: The specific conditions and verifiable triggers under which the agent should be activated17.  
3. **Do Not Use When**: Negative boundary constraints that define when the agent must halt execution or delegate the task to another system component3.  
4. **Required Inputs**: The precise data models, configuration parameters, and schema definitions required to initialize execution3.  
5. **Output Contract**: The file formats, programmatic schemas, or structured models (such as JSON Schema or Protobuf schemas) to which the output must conform3.  
6. **Workflow**: The step-by-step state machine, planning loop, and verification phases the agent executes23.  
7. **Context Policy**: Rules governing the context window, defining which memory buffers, vector databases, and file paths are accessible to prevent token drift5.  
8. **Permissions**: The security model restricting the agent’s execution privileges, categorized as read-only, reversible write, or irreversible write16.  
9. **Effort Behavior**: The configuration of reasoning tokens, model parameters, and compute resources optimized for the agent's task complexity27.  
10. **Failure Modes**: A catalog of expected errors and the corresponding fallback strategies or escalation paths to trigger3.  
11. **Eval Rubric**: The metric-driven criteria used to score the agent's output for correctness, security, and performance3.  
12. **Promotion Requirements**: The verification thresholds (such as unit, integration, and security tests) required to promote the agent across environments11.

## **Decomposed Frontend Agent Specifications**

To illustrate the application of this doctrine, the frontend engineering lifecycle is decomposed into six specialized agents. Each agent is defined in accordance with the twelve-point specification blueprint, ensuring they function as modular components within a secure execution harness1.

### **Agent: frontend-architect**

#### **Purpose**

The frontend-architect designs high-level page layouts, configures file hierarchies, defines routing structures, and establishes global design token maps24. It ensures that all structural dependencies comply with system architecture guidelines before any component implementation begins24.

#### **Use When**

Activated during initial workspace setups, when establishing new routing modules, or when refactoring global design tokens and layout architectures28.

#### **Do Not Use When**

The task involves writing individual UI components, editing local styles, fixing linter errors in functional views, or adjusting CSS padding values24.

#### **Required Inputs**

Product requirement schemas, wireframe layouts, design tokens in JSON format, and structural configuration templates14.

#### **Output Contract**

Generates a structured directory configuration, module export paths, routing tables, and global CSS variable declarations mapping to design tokens24.

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "type": "object",  
  "properties": {  
    "scaffoldPaths": { "type": "array", "items": { "type": "string" } },  
    "routingMap": { "type": "object" },  
    "resolvedTokens": { "type": "object" }  
  },  
  "required": \["scaffoldPaths", "routingMap", "resolvedTokens"\]  
}

#### **Workflow**

The agent retrieves and processes JSON style files, extracting core styling parameters14. It constructs the file framework, creates the layout system, and outputs compile-ready routing files28. It then runs a compilation pass to ensure the layout contains no circular imports or build errors24.

#### **Context Policy**

The agent has access only to global configuration files, routing structures, and design token files28. It ignores local component source files, testing templates, and media assets to maintain a lean context window5.

#### **Permissions**

Granted read-write access to the /src/styles/, /src/routes/, and root configuration directories18. Blocked from accessing the host system’s terminal or executing arbitrary shell commands16.

#### **Effort Behavior**

Allocates up to 8,000 reasoning tokens per cycle to analyze structural relationships, prioritizing layout correctness over execution latency27.

#### **Failure Modes**

On encountering circular routing loops or missing token imports, the agent halts execution, reverts pending changes, and outputs a validation error identifying the structural conflict3.

#### **Eval Rubric**

The output must achieve a 100% compilation success rate, contain zero circular dependencies, and map every design attribute directly to an approved token24.

#### **Promotion Requirements**

Must compile cleanly with zero TypeScript errors under strict mode and pass a structural dependency audit within the CI pipeline24.

### **Agent: component-implementer**

#### **Purpose**

The component-implementer generates React and TypeScript component code14. It constructs UI primitives, buttons, form controls, and layout cards, ensuring that all components are modular, styled using design tokens, and visually consistent24.

#### **Use When**

Activated when translating UI specifications, Figma design tokens, or visual layouts into functional code components14.

#### **Do Not Use When**

The task involves managing complex page routing, orchestrating asynchronous state sync systems, or writing database access controllers24.

#### **Required Inputs**

Component wireframe designs, styling variables, and references to existing component libraries to encourage reuse14.

#### **Output Contract**

Generates React component code, TypeScript property interfaces, and styling setups bound to approved variables24.

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "type": "object",  
  "properties": {  
    "componentCode": { "type": "string" },  
    "exportedProps": { "type": "array", "items": { "type": "string" } }  
  },  
  "required": \["componentCode", "exportedProps"\]  
}

#### **Workflow**

The agent queries the design registry to locate and reuse existing UI components rather than generating redundant styles29. It writes layout properties, bounds styling properties to active variables, applies semantic HTML tags, and formats the output24.

#### **Context Policy**

Access is limited to the directory of the target component and the global design token schemas28. Direct access to parent layout modules or adjacent functional states is blocked to prevent context creep5.

#### **Permissions**

Granted read-write access to the /src/components/ directory18. Blocked from modifying network rules or global system settings16.

#### **Effort Behavior**

Operates on a medium model sizing profile, targeting execution latencies under 30 seconds per component compile loop27.

#### **Failure Modes**

If the output contains hard-coded styling values (such as raw hex codes or unauthorized spacing values), the system halts compilation, reverts the build, and re-runs the styling mapping pass18.

#### **Eval Rubric**

The component must compile cleanly with zero TypeScript errors, contain zero hard-coded styles, and pass static layout analyses24.

#### **Promotion Requirements**

Must pass automated linter validation, compile without warnings in a sandbox, and register successfully with the component catalog24.

### **Agent: state-flow-specialist**

#### **Purpose**

The state-flow-specialist manages client-side data flows, state synchronization, form validations, data hooks, and route-state maps28. It integrates static visual components with state managers and backend endpoints30.

#### **Use When**

Activated when components require data hooks, state integrations, user authentication state mappings, or custom side-effect handlers28.

#### **Do Not Use When**

The task involves modifying CSS classes, adjusting page margins, or running visual pixel regression audits14.

#### **Required Inputs**

API data contracts, state flow diagrams, and target component file paths4.

#### **Output Contract**

Generates state managers, custom hooks, and state context files24.

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "type": "object",  
  "properties": {  
    "stateHookCode": { "type": "string" },  
    "exposedStateActions": { "type": "array", "items": { "type": "string" } }  
  },  
  "required": \["stateHookCode", "exposedStateActions"\]  
}

#### **Workflow**

The agent maps component layouts to corresponding state flows30. It writes custom state hook structures, creates error fallbacks, and validates hook patterns to prevent unnecessary component updates3.

#### **Context Policy**

Access is restricted to state hooks, context configurations, data contracts, and the target functional components28. Visual assets and raw stylesheets are excluded from the context window5.

#### **Permissions**

Granted read-write access to /src/hooks/ and /src/state/ directories18. Blocked from modifying visual asset files or deployment configurations16.

#### **Effort Behavior**

Allocates up to 4,000 reasoning tokens per cycle to trace side effects and identify potential memory leaks or race conditions27.

#### **Failure Modes**

If a state loop conflict is detected, the agent reverts the compilation state, halts execution, and generates a state-trace map pointing to the conflict3.

#### **Eval Rubric**

The state flow must achieve 100% test coverage on asynchronous actions and contain zero memory leak signatures13.

#### **Promotion Requirements**

Must pass asynchronous testing sweeps, compile with strict typing rules, and run cleanly without state warning logs24.

### **Agent: accessibility-auditor**

#### **Purpose**

The accessibility-auditor conducts WCAG 2.2 AA compliance audits on HTML structures and live URLs31. It scans markup for keyboard traps, evaluates contrast ratios, reviews landmark navigation structures, and checks assistive technology support31.

#### **Use When**

Activated during staging deployment sweeps, pull request validation checks, or pre-merge automation loops to verify interaction accessibility31.

#### **Do Not Use When**

The task involves writing component styling variables, configuring state hooks, or auditing API latencies24.

#### **Required Inputs**

Page DOM nodes, live verification URLs, and target WCAG guidelines31.

#### **Output Contract**

Generates compliance validation profiles detailing accessibility scores, violations, target CSS selectors, and code remediation instructions31.

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "type": "object",  
  "properties": {  
    "overallCompliance": { "type": "boolean" },  
    "accessibilityErrors": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "criterion": { "type": "string" },  
          "severity": { "type": "string" },  
          "selector": { "type": "string" },  
          "fix": { "type": "string" }  
        }  
      }  
    }  
  },  
  "required": \["overallCompliance", "accessibilityErrors"\]  
}

#### **Workflow**

The agent runs an automated test scan using axe-core to check for structural violations32. It parses CSS properties to calculate luminance parameters and evaluate contrast ratios31. It then runs a simulated keyboard tab cycle using Playwright to identify potential focus traps and verify visual focus indicators31.

#### **Context Policy**

Access is limited to DOM trees, generated HTML output files, and visual style properties9. Backend service files and API routes are excluded16.

#### **Permissions**

Granted execution privileges for visual verification modules and read-only access to local markup directories18. Blocked from modifying codebase components directly18.

#### **Effort Behavior**

Operates with a lightweight reasoning footprint, leveraging automated heuristics to keep scan execution times under 15 seconds27.

#### **Failure Modes**

On discovering focus traps or unresolvable contrast issues, the agent registers a critical blocking error and exports a remediation patch containing the correct color token overrides31.

#### **Eval Rubric**

Must accurately detect 100% of detectable structural violations and calculate contrast metrics down to single-pixel luminance values31.

#### **Promotion Requirements**

The audited build must achieve zero high-severity accessibility errors and pass automated keyboard interaction testing32.

#### **Mathematical Audit Formulations**

The relative luminance ![][image1] of a color is calculated using the following formula31:  
![][image2]  
where ![][image3], and ![][image4] represent the sRGB color components normalized to ![][image5]31:  
![][image6]  
![][image7]  
The contrast ratio ![][image8] between two colors is then calculated as31:  
![][image9]  
where ![][image10] is the relative luminance of the lighter color, and ![][image11] is the relative luminance of the darker color31. WCAG AA guidelines require a contrast ratio of at least ![][image12] for body text and ![][image13] for large text31.

### **Agent: visual-qa-specialist**

#### **Purpose**

The visual-qa-specialist conducts pixel-level visual regression testing14. It compares live page screenshots against Figma designs, identifies layout misalignments, and verifies that padding, typography, and spacing conform to specifications14.

#### **Use When**

Activated post-compilation on staging builds, during component update sweeps, or during visual regression test runs14.

#### **Do Not Use When**

The task involves refactoring data hooks, validating bundle sizes, or testing screen-reader states24.

#### **Required Inputs**

Component files, visual screenshots of the live URL, and original Figma design coordinate nodes29.

#### **Output Contract**

Generates pixel deviation maps and visual difference logs showing spacing variances and color mismatches14.

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "type": "object",  
  "properties": {  
    "similarityIndex": { "type": "number" },  
    "deviations": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "selector": { "type": "string" },  
          "deltaX": { "type": "number" },  
          "deltaY": { "type": "number" }  
        }  
      }  
    }  
  },  
  "required": \["similarityIndex", "deviations"\]  
}

#### **Workflow**

The agent extracts design metrics from Figma files14. It navigates a headless browser to the target staging URL, captures a screenshot, and applies a visual comparison algorithm to generate a pixel difference map35. It then queries DOM layout coordinates to verify spacing parameters14.

#### **Context Policy**

Access is limited to image directories, stylesheets, and coordinate manifests14. Access to programmatic data stores is blocked5.

#### **Permissions**

Granted permission to execute local visual regression modules and access staging URLs35. Blocked from modifying code repositories18.

#### **Effort Behavior**

Allocates up to 5,000 reasoning tokens per cycle to trace visual elements, prioritizing spatial accuracy27.

#### **Failure Modes**

If dynamic content loading causes visual discrepancies, the agent replaces the dynamic components with static layout blocks and runs the layout comparison again14.

#### **Eval Rubric**

Must accurately identify spatial misalignments down to 1px and log any color codes that deviate from the design system14.

#### **Promotion Requirements**

Must achieve a visual similarity score of ![][image14] and contain zero style-token alignment violations29.

#### **Visual Similarity Calculations**

Visual similarity evaluations calculate spatial deviations using the Structural Similarity Index Measure (SSIM)35:  
![][image15]  
where ![][image16] and ![][image17] are the average pixel intensities, ![][image18] and ![][image19] are the image variances, and ![][image20] is the covariance of the image frames35.

### **Agent: performance-reviewer**

#### **Purpose**

The performance-reviewer audits production build outputs, JavaScript bundle sizes, loading latency parameters, and asset distributions12. It ensures that build artifacts do not exceed performance budgets12.

#### **Use When**

Activated on production build targets during staging validation, pull request verification, or automated release checks12.

#### **Do Not Use When**

The task involves modifying raw styles, writing React components, or running keyboard-only accessibility checks24.

#### **Required Inputs**

Staging deploy URLs, bundle maps, and maximum asset size budgets12.

#### **Output Contract**

Generates bundle weight breakdowns, runtime loading diagnostics, first paint scores, and split recommendations12.

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "type": "object",  
  "properties": {  
    "totalWeightKB": { "type": "number" },  
    "firstPaint": { "type": "number" },  
    "performanceWarnings": { "type": "array", "items": { "type": "string" } }  
  },  
  "required": \["totalWeightKB", "firstPaint", "performanceWarnings"\]  
}

#### **Workflow**

The agent analyzes code distribution manifests to identify heavy dependencies12. It runs headless loading evaluations, measures render times, and parses build configurations to identify optimization opportunities26.

#### **Context Policy**

Access is limited to build logs, diagnostic files, bundle manifests, and configuration files12. Raw design files and image assets are excluded5.

#### **Permissions**

Granted read access to target staging directories and execution privileges for performance diagnostics18. Blocked from modifying codebase files18.

#### **Effort Behavior**

Uses a lightweight model configuration, targeting compilation latencies under 15 seconds27.

#### **Failure Modes**

On detecting anomalous performance variations, the agent executes three successive tests and averages the results to ensure metric stability.

#### **Eval Rubric**

Must accurately identify duplicate dependency structures and trace bundle path size regressions12.

#### **Promotion Requirements**

Initial page weight must remain under 150KB, interactive delay must be under 1800ms, and code splitting must pass verification checks12.

## **Boundary Security, Authorization Tiers, and Systems Governance**

Security in multi-agent environments must be designed directly into the system architecture rather than handled via prompt-level instructions13. Treating all external data inputs as untrusted and enforcing validation checks at runtime prevents injection exploits from escalating permissions9.

\+---------------------------------------------------------------------------------+  
|                       MANURELLA SECURITY ARCHITECTURE                           |  
\+---------------------------------------------------------------------------------+  
|                                                                                 |  
|  \[UNTRUSTED INPUT\] \---\> \[AGENT BOUNDARY\] \---\> \[RUNTIME VERIFICATION HARNESS\]    |  
|  \- User Messages        \- Data Tagging        \- Scoped APIs                     |  
|  \- External Files       \- Schema Filters      \- Read-Only Checks     |  
|                                                     |                           |  
|                                                     v                           |  
|                                               \[TARGET SYSTEM\]                   |  
|                                               \- Sandboxed Workspace \[cite: 36\]  |  
|                                                                                 |  
\+---------------------------------------------------------------------------------+

### **The Verification-Validation-Execution (VVE) Pipeline**

To prevent unverified tool actions, the execution harness implements a strict pipeline1:

1. **Verification**: The agent suggests a tool call based on task requirements18.  
2. **Validation**: The system verifies the request against a hard-coded security schema, checking parameter formats and security boundaries2.  
3. **Execution**: The tool executes within a sandboxed environment, isolating system resources9.

### **Functional Identity and Permissions**

The doctrine moves away from persona-based permissions, implementing execution-based security models instead2. Rather than sharing an administrative token, agents use unique session IDs and are restricted to short-lived, least-privileged credentials16:

* **Read-Only**: Allowed to search directories, view styles, and read schema assets18.  
* **Reversible Write**: Allowed to create code files inside isolated staging directories16.  
* **Irreversible Write**: Actions like production deployments, library updates, or code merges must pass static verification checks and require human authorization16.

## **Continuous Verification and Promotion Mechanics**

The deployment of autonomous agents into production workflows requires continuous validation checks to maintain code quality and prevent system drift6. The Manurella framework establishes a three-stage promotion pipeline to verify agent outputs before they reach production11.

\+---------------------------------------------------------------------------------+  
|                          THREE-STAGE PROMOTION PIPELINE                         |  
\+---------------------------------------------------------------------------------+  
|                                                                                 |  
|  \[DEVELOPMENT\] \---------------------\> \[STAGING\] \----------------\> \[PRODUCTION\]   |  
|  \- Fast syntax checks                 \- Interactive runs         \- Live telemetry|  
|  \- Static analysis         \- Keyboard audits \[cite: 33\] \- Drift alerts|  
|                                                                                 |  
\+---------------------------------------------------------------------------------+

### **1\. Development Environment (DEV)**

In the development environment, agent outputs undergo fast static checks24:

* **Linter and Type Validation**: Outputs are verified against strict linter configurations to ensure formatting compliance24.  
* **Static Analysis**: Code structures are checked for token compliance and proper variable exports24.

### **2\. Staging Environment (STAGING)**

In staging, components undergo integration testing in simulated environments32:

* **Property-Based Testing**: Evaluates components across different viewports, checking that layout ratios remain stable under stress24.  
* **Adversarial Testing**: Probes input fields, routing paths, and parameters with injection scripts to confirm the runtime harness blocks unauthorized actions13.

### **3\. Production Environment (PRODUCTION)**

In production, the deployment is managed through continuous verification loops10:

* **Explainability Audits**: The system records planning files and tool logs, providing a complete audit trail of agent actions8.  
* **Drift Alerts**: Auditing systems monitor production outputs against original design tokens12. If style drift or unapproved modifications are detected, the system triggers alerts and rolls back changes to the last verified state10.

#### **Works cited**

1. Agent Harness Engineering: A Survey \- OpenReview, [https://openreview.net/pdf/f358711a95aaaf61fdeffd4ef3fc60fba9b8da57.pdf](https://openreview.net/pdf/f358711a95aaaf61fdeffd4ef3fc60fba9b8da57.pdf)  
2. Understanding AI agents: Construction, behavior, and boundary setting | F5, [https://www.f5.com/company/blog/understanding-ai-agents-construction-behavior-and-boundary-setting](https://www.f5.com/company/blog/understanding-ai-agents-construction-behavior-and-boundary-setting)  
3. Stop Prompting Your AI Agent. Give It a Playbook. \- SQLServerCentral, [https://www.sqlservercentral.com/articles/stop-prompting-your-ai-agent-give-it-a-playbook](https://www.sqlservercentral.com/articles/stop-prompting-your-ai-agent-give-it-a-playbook)  
4. Understanding and Building Skills, Agents, and Sub Agents | by Sravan Nerella | Another Integration Blog \- Medium, [https://medium.com/another-integration-blog/understanding-and-building-skills-agents-and-sub-agents-11670f6335cf](https://medium.com/another-integration-blog/understanding-and-building-skills-agents-and-sub-agents-11670f6335cf)  
5. Stop writing Agent prompts like Chatbot prompts. Here is a 4-section architecture for reliable Autonomous Agents. : r/PromptEngineering \- Reddit, [https://www.reddit.com/r/PromptEngineering/comments/1ruv5a4/stop\_writing\_agent\_prompts\_like\_chatbot\_prompts/](https://www.reddit.com/r/PromptEngineering/comments/1ruv5a4/stop_writing_agent_prompts_like_chatbot_prompts/)  
6. Clawed and Dangerous: Can We Trust Open Agentic Systems? \- arXiv, [https://arxiv.org/html/2603.26221v1](https://arxiv.org/html/2603.26221v1)  
7. Manuela 2.0: AI Revolutionizes Technical Documentation | Memori, [https://memori.ai/en/blog/manuela-2-0-ai-revolutionizes-technical-documentation](https://memori.ai/en/blog/manuela-2-0-ai-revolutionizes-technical-documentation)  
8. Generative AI: Manuela Veloso \- YouTube, [https://www.youtube.com/watch?v=KY01E32nZr4](https://www.youtube.com/watch?v=KY01E32nZr4)  
9. What Is Agent Boundary? Definition & Examples \- Non-Human Identity Management Group, [https://nhimg.org/glossary/agent-boundary/](https://nhimg.org/glossary/agent-boundary/)  
10. The Industrial AI Agent Manifesto: Governance Requirements for Trustworthy Autonomous Operations \- Digital Twin Consortium, [https://www.digitaltwinconsortium.org/2026/02/the-industrial-ai-agent-manifesto-governance-requirements-for-trustworthy-autonomous-operations/](https://www.digitaltwinconsortium.org/2026/02/the-industrial-ai-agent-manifesto-governance-requirements-for-trustworthy-autonomous-operations/)  
11. AI Agents in Action: A Playbook for Trusted Adoption, Authorization and Scaling, [https://reports.weforum.org/docs/WEF\_AI\_Agents\_in\_Action\_A\_Playbook\_for\_Trusted\_Adoption\_Authorization\_and\_Scaling\_2026.pdf](https://reports.weforum.org/docs/WEF_AI_Agents_in_Action_A_Playbook_for_Trusted_Adoption_Authorization_and_Scaling_2026.pdf)  
12. Model Context Protocol strategies on AWS \- AWS Prescriptive Guidance, [https://docs.aws.amazon.com/prescriptive-guidance/latest/mcp-strategies/introduction.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/mcp-strategies/introduction.html)  
13. AI Agent Prompt Engineering: Best Practices, Security, & Testing for Production, [https://www.inflectra.com/Ideas/Topic/AI-Agent-Prompt-Engineering.aspx](https://www.inflectra.com/Ideas/Topic/AI-Agent-Prompt-Engineering.aspx)  
14. Designing Autonomous AI Agents: How We Built a Multi-Agent Swarm for UI Development, [https://www.epam.com/insights/ai/blogs/building-multi-swarm-autonomous-ai-agent](https://www.epam.com/insights/ai/blogs/building-multi-swarm-autonomous-ai-agent)  
15. Designing AI agents to resist prompt injection \- OpenAI, [https://openai.com/index/designing-agents-to-resist-prompt-injection/](https://openai.com/index/designing-agents-to-resist-prompt-injection/)  
16. How to Prevent Prompt Injection in AI Agents, [https://goteleport.com/blog/prevent-prompt-injection/](https://goteleport.com/blog/prevent-prompt-injection/)  
17. Agent Skills: Microsoft Just Shipped What You've Been Building \- htek.dev, [https://htek.dev/articles/agent-skills-microsoft-just-shipped-what-youve-been-building](https://htek.dev/articles/agent-skills-microsoft-just-shipped-what-youve-been-building)  
18. For tool-using agents, where do you draw the security boundary?, [https://www.reddit.com/r/AI\_Agents/comments/1u5w3us/for\_toolusing\_agents\_where\_do\_you\_draw\_the/](https://www.reddit.com/r/AI_Agents/comments/1u5w3us/for_toolusing_agents_where_do_you_draw_the/)  
19. Why AI agents need guardrails and how to set them, [https://www.bcs.org/articles-opinion-and-research/why-ai-agents-need-guardrails-and-how-to-set-them/](https://www.bcs.org/articles-opinion-and-research/why-ai-agents-need-guardrails-and-how-to-set-them/)  
20. SAP Agentic AI in Practice: Concepts, Architecture, and Your First LangGraph Agent, [https://community.sap.com/t5/artificial-intelligence-blogs-posts/sap-agentic-ai-in-practice-concepts-architecture-and-your-first-langgraph/ba-p/14361699](https://community.sap.com/t5/artificial-intelligence-blogs-posts/sap-agentic-ai-in-practice-concepts-architecture-and-your-first-langgraph/ba-p/14361699)  
21. Agent vs Skill: The Distinction That Actually Matters in Agentic AI, [https://laxmikumars.medium.com/agent-vs-skill-the-distinction-that-actually-matters-in-agentic-ai-ea6577b20825](https://laxmikumars.medium.com/agent-vs-skill-the-distinction-that-actually-matters-in-agentic-ai-ea6577b20825)  
22. AI Agent vs Skill: Core Differences, Top Platforms, and Practical Guide \- Skywork, [https://skywork.ai/skypage/en/ai-agent-skill-differences/2065008040279474176](https://skywork.ai/skypage/en/ai-agent-skill-differences/2065008040279474176)  
23. Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills \- arXiv, [https://arxiv.org/html/2512.16301v3](https://arxiv.org/html/2512.16301v3)  
24. The AI Coding Agent Manifesto. Because “vibe coding” was never going… | by Shay Cohen | Wix Engineering | Medium, [https://medium.com/wix-engineering/the-ai-coding-agent-manifesto-c8f61629d677](https://medium.com/wix-engineering/the-ai-coding-agent-manifesto-c8f61629d677)  
25. Agent AI Playbook \- Kore.ai Docs, [https://docs.kore.ai/ai-for-service/agentai/agent-experience/playbook](https://docs.kore.ai/ai-for-service/agentai/agent-experience/playbook)  
26. Model Context Protocol architecture patterns for multi-agent AI systems \- IBM Developer, [https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems/](https://developer.ibm.com/articles/mcp-architecture-patterns-ai-systems/)  
27. A practical guide to building agents | OpenAI, [https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)  
28. I made a small AGENTS / CLAUDE harness in my last project from my experience in agile dev \- Reddit, [https://www.reddit.com/r/ClaudeCode/comments/1thkm1s/i\_made\_a\_small\_agents\_claude\_harness\_in\_my\_last/](https://www.reddit.com/r/ClaudeCode/comments/1thkm1s/i_made_a_small_agents_claude_harness_in_my_last/)  
29. How to make Claude Code follow your design system in Figma | by Sen Lin \- UX Collective, [https://uxdesign.cc/how-to-make-claude-code-follow-your-design-system-in-figma-559618cffaa9](https://uxdesign.cc/how-to-make-claude-code-follow-your-design-system-in-figma-559618cffaa9)  
30. Has anyone actually cracked a 10/10 AI workflow for Figma → React Native? \- Reddit, [https://www.reddit.com/r/reactnative/comments/1rt6sf0/has\_anyone\_actually\_cracked\_a\_1010\_ai\_workflow/](https://www.reddit.com/r/reactnative/comments/1rt6sf0/has_anyone_actually_cracked_a_1010_ai_workflow/)  
31. accessibility-auditor | naksha \- ClaudePluginHub, [https://www.claudepluginhub.com/agents/adityaraj0421-naksha/agents/accessibility-auditor](https://www.claudepluginhub.com/agents/adityaraj0421-naksha/agents/accessibility-auditor)  
32. Accessibility Auditor — AI agent skill | explainx.ai, [https://explainx.ai/skills/msitarzewski/agency-agents/Accessibility%20Auditor](https://explainx.ai/skills/msitarzewski/agency-agents/Accessibility%20Auditor)  
33. Accessibility Auditor | QASkills.sh, [https://qaskills.sh/skills/Pramod/accessibility-auditor](https://qaskills.sh/skills/Pramod/accessibility-auditor)  
34. accessibility-auditor — Agent Skill \- MCP.Directory, [https://mcp.directory/skills/accessibility-auditor](https://mcp.directory/skills/accessibility-auditor)  
35. AI in My Daily Work — Episode 4: Automating UI Regression Testing with AI Agents (Part-1), [https://medium.com/@designwithriaz/ai-in-my-daily-work-episode-4-automating-ui-regression-testing-with-ai-agents-part-1-6395c4459e31](https://medium.com/@designwithriaz/ai-in-my-daily-work-episode-4-automating-ui-regression-testing-with-ai-agents-part-1-6395c4459e31)  
36. New framework simplifies the complex landscape of agentic AI | VentureBeat, [https://venturebeat.com/orchestration/new-framework-simplifies-the-complex-landscape-of-agentic-ai](https://venturebeat.com/orchestration/new-framework-simplifies-the-complex-landscape-of-agentic-ai)  
37. The Industrial AI Agent Manifesto \- XMPro, [https://xmpro.com/the-industrial-ai-agent-manifesto/](https://xmpro.com/the-industrial-ai-agent-manifesto/)  
38. Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation, [https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI\_MCP\_SECURITY.pdf?ver=bmgiSbNQLP6Z\_GiWtRt6bg%3D%3D](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf?ver=bmgiSbNQLP6Z_GiWtRt6bg%3D%3D)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAaCAYAAACHD21cAAAAs0lEQVR4XmNgGHkgAIjnAvEsNDwTiIWR1GEAXSAOAeKlQPwfiLOhfGcgZkVShxNMYoBoZESXwAc0gfgtEH9FlyAEghggtp1GlyAEYM6cgy6BD/AC8WEGiMZoNDm8ANmZgmhyIMDMgCPACDnTEohZ0AVBNoBswuVMkE2T0QVBADkajNHkQAAkdhxdEATWMkBsA6UamD+kgTgZiD8C8T8gdoGKgwHI3T8ZIJrwYVwBNgpGIgAASSgq5DR3npcAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAaCAYAAAAqjnX1AAACO0lEQVR4Xu2WTUtVURSG32hi9KGVFJIOkhAMqYFEEwORRESUiIIgwYFTcRIWNGjWVDBwYCRRk6B+QdBAESJq4kBxIIFFFARNIoUErfdlnXPZd3Xcx2ORDs4DD3rX/jjr7r32vgcoKflvnKANtC6I7aMHg89/0Eqn6Dz9mPydpg8Th+nxSu+dsZ/20Zd0g36iP+hbWIK36Hildwan6DV6h27Se8lneZd+oOt0NB1QkAt0if6iT2EJCyXXQ18kbTeTeJReugJLOuQM/QybqChKRCv3np5zbSma9xtsR6OoHl7BVtPTTL+geJLdsAQv+QbHHH3gg1mkiXT4BjIIS/Cnb4igw7EAG6fVjDFLB3wwC3XShPUuri3QVqkmr7u2GCPY/he7QY/5YBb3YZM2wa6HTtjgNfqcNlZ65lNL38Dmm6lu2jlaLRXuqovrYaqpbW1FwGXYLaEkr7o2cRK2EKG64qJloaOvCRd9Ayz+xAdz6IeNk/rfswy7j1VC6vOVTiAnyUewzo9dvCaJF02yHbYrWyWZohOtPnpOlKP0Hayzv0x14hXXhV4EHT7tisbqAGVxGHb1qE8uY7COui784VBtqS29O9tgV8t5+j1pU91mcQC2A+rj5z0LWxjV+0p1UzXhg0JPB330IMVe0yHYNxeH6DPY4VDRb4XG34bNoaT0HqB3Aq1yF71IJyu9/wKd/PR3XD+PISqVWJIpnbDrTOV0BTkH5F+j7c8t+t1EqxF9tdoLtNAjPlhSUrLL/AaKGHdmo57G4gAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAZCAYAAADXPsWXAAAA6ElEQVR4Xu2SwQpBQRSGj6QoNnZWCiVlS9lYWdjwDN5EFl7AguIBlBXJXnkTG6VkzQL/MXfGzOmOa2V1v/oWd/6/e+fMXKKYKNpwDY+W/DwPHMGKaUcwhhO5CLrwAW+wJTKHNNzBvgxAHV7hE/ZE5lCCJ1iTAejQjzvRxawMwJbULvh8UiIz6FF0UbuBd1j9VP3oUc6wYFmEQ7iEedP2oEfZi3UmQWqHK/oyCsNXy8Ww62U4u1D4ob/Ro/hK/HV+CR9uRmQG/i+4dIA5kfEoA1L/SNONXBakXjK11pKwDGdB1rCymJj/8wKOpzDUOmiw4wAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAZCAYAAACsGgdbAAABdUlEQVR4Xu2WsS4FQRSGj4iEUBBCVG5Eo1CJQqVBxyNob+INvIFWS6HU6jQKCZ1CItEQBY1EoiChkAj/nzMj956bye6M2cp8yZe7mbM7+8/c3ZkVKeRnCk673wFTa5J+OCl670FT6+EWHsI92OouNcoo3IX7cMPUejiGI7ZRdKQcJUfbZ2qx8PpZOGQLjqSQK/AOXjlv4FLXGfVhQP5Tr3DR1DzRIY/gk+jIPfPwxdXqwuebzzn7foDvkjEkw1zCsY62CdHZZPgUsof8hmemjcdsYy2FEtJTQkoJWZ/sId9ElxsuOx6ud/eiy1MK2UNuwi+4I7pbUB6zbc2dMwxPRWd22bWF4PXP8AOuim63luiQ7HRbtNMDJ4+3XM3Thp8SvgH3fc4gB2K1Mxrq4xcb0jMuevG66MyFqLxBDSr7CIWsA79quK//lcZCzsAL25hIZcgTOCfxX+Z8+1u2MYLOL/PKkNfw0f0umFqTMOC56L351hf+Nz9oI2k9nPLzwAAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,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>

[image7]: <data:image/png;base64,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>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAaCAYAAAAjZdWPAAACB0lEQVR4Xu2WP0hVURzHv1JCUWrRUEHQQ1QILQiJlgyHBiGUEEFpclMoFwclWoRycBVaosVBAnWLwJa42Nbm1NQg2OCgTrra98vvPO69v9573ovGfcP9wId3z++c997v/LnnHKCk5Excpbdpq4v7clPwnv6hJ/SAHtM5epnepffipsWjpJboDp2kHSHeTlfpN/qbXg/xwrlFt2Cjq+Q9N+hPWH1T8AWWzBoar9dRuu+DRaGED2mfr3Ao6cgHi+AmLOnP9KKr8zymT32wCCZgSY/4imblEv1Kf9A2V/e/+UAf+GAWdHhEQT03Ypq+8sEc3Hdlze6si2XmE05PWvv1Ju33FTnw39UWesHFMqM1/Qv2QtZDp6Gm87QXVctNx74+k1Twb9KeFlhHGg1eCm13R/Ql0r2/Qt/ADp4kK7COdtF12J9tw2ZNdNKh8CyUsE9a79F8eO5Fert9jdoHXIoexKedOvCRfqd7dCbRroqS3kB65HUoqcPXYJ2pJiRqJR0hbrOI9EbwiD5JlOui6anQF3QMdimqt+aUtKyi747D7iXL9DnyJa3fSi4LtR1OlM8Fn/QgbIYGQlkXqrewLU2zUU1a6/1daBMhTlodTV7CNMqZRjoPPukpukvvhHI37HorNYKatWehfiG0iRAn/RDpNa145hfyrGg9y1oo7neVJLl3j5KSkoL4C/WYTSOqBB5HAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,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>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAaCAYAAACzdqxAAAAA30lEQVR4XmNgGAX0BgFAPBeIZ6HhmUAsjKSOZKALxCFAvBSI/wNxNpTvDMSsSOrIBpMYIAYzoktQAjSB+C0Qf0WXoBQEMUBcexpdglIAC4Y56BKUAF4gPswAMTgaTY4igBwMgmhyIAASQ45QBSCOQOLjBISCASTOAsQcQFwJxH+AeCGKCiwA5BqQS3EFA8ilfkhsbiA+wECEwcjJzBhNDgRAYuJoYgcYiDB4LQPEtaBcBwtHaSBOBuKPQPwPKoYMDjDgMdgSiH8yQAzFh7Gl6wMMeAymBBxgGDV4FAxjAACeJDZUaoH/sAAAAABJRU5ErkJggg==>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAaCAYAAACzdqxAAAABJklEQVR4XmNgGAX0BgFAPBeIZ6HhmUAsjKSOZKALxCFAvBSI/wNxNpTvDMSsSOrIBpMYIAYzoktQAjSB+C0Qf0WXoBQEMUBcexpdglIAC4Y56BKUAF4gPswAMTgaTY4igBwMgmhyIAASg0UoJwMkKXYBsTpcBQ5AKBhA4ixAzMMASe9iQNwMxD+A2BdJHQoAuQbkUlzBAHKpH5TtAsSvoGx+ID4BxAcYIBZiAORkZowmBwIgMXEo2wGIfyOkGBYC8UMglkQSg4O1DBDXgnIdLBylgTgZiD8C8T+oGDpwZYA4JhhdwhKIfzJADMWHsaVreSC+CMThDFTOpasYIOFNVQAqlEC+BQGQa0GpAxYHZAOQodMYICUfCFcB8TIg5kZWNApGASoAAC0SOpeUOWn6AAAAAElFTkSuQmCC>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADYAAAAZCAYAAAB6v90+AAABlElEQVR4Xu2WvytFYRjHv0IRmyIid8GqmAxGG4vBIimFP0D5I+zIxqTYSIlyy8RiMVgZKZtFie+359y85+W995zrXm56P/Wpc57znvc9z/vzAJFI5K9Y8gMBumiHF2umfV6slrTSAm3y4hUp0F0/GGCdvtErukPP6SvdcgvVkAl6TYu0M/2oPHP0CfkSO6GbdIUOpB/XjDbaS6fpO3ImNgjr8TXkS0z+FrkT07zdpvOwl/9NYrN0D5ZgNYmNwNaYOsbfTEJcwD6w34uXI1diLXTVuc+bmBJSh4gh+ghb4JU4pWeoY2IztN25z5OYjxorwhqvB5kT64b1mstPEtPoH6IBElNBnTsPjs9ObB/hNTNO72Fr021EnfLniZXOB9cFepBc688idMJrfakRnXvDSaxhpqKPNgFtJEdIj1SpQqlroWl8SaeSe3XAYlImy5+HX18WlmHv3MDO3UyUppBrEdYzquSW3uFzdMRoEjuGldXv1QbSm1GI7+oLMUZf8PX7qt0LMqFRnoT1fI/3LBKJRCKRevEBmhVnHcFBfHwAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACYAAAAZCAYAAABdEVzWAAABSklEQVR4Xu2VsStFcRTHj6SIUogMsrDIZjJYZLCI3fA2pUwUm39Aykr5IwzKYLibQSmbTJTJYqIk8TmdJ793vHf9Hr+n1O9Tn3r3nPfu/d7f797zRDKZv6MN+3EYB12vFej1xnyxHhd4jod4i2vYXvONNGigCTzCm9rWVxbwASeD2hueYndQ+y1D2INT+Ci2AKXM4TNOBzUNVoidKDXRwfx+d4kF2w1qKYkO5pnBaxz1jTqs4B2u+kYJTQXrw0VcxhOcFVvJ79BgV9LCYCEdYlu5KXHhmuXHwRQN5l+IVEQH06E64Gr6Qw237uopiAqm0/4Sj7EzqD+JBdsKaqmICqbP0B6OB7WPZ+yg+rkROuMK+Zx5Mej15vEF76vHDekVm/z7Ylt3hjti86wMPekGvuK269VDV0hvwltIySAfwSWsiP1FZTKZzH/gHae1RQIiRSrCAAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAAClUlEQVR4Xu2XTahOURSGX0ldIRdFRCiREslfYiRmSFGUmQETMVBMZKI7VLdbBqRkYCBlJpLBKQO/pUTKTyI/GUiUARLva+392Wffu8/fLQb2U2/fd9ZeZ39n7bP2WvsDMpnM/0wftcRpYjRWxzhqMdUfD0Ro7tVoOP80amZsHCVjqQ/UReqc+66Hr2MMtZn6SF2gPlND1ITQCTb/AZiP9ztT8kigGzdQ96ibsB/sygzqMeyNhujh9QZSzKdeO80O7Ar0K7XWXU+mblFbeh7GempZZEuiANfAAlbgWoC2bKV+xkaYbV9sDNgN87lLTQnsR5xdn0LZ95La3/MwVji1Yil1jXpC7YrG6hhAOlClcQofUIHynvP2y+5aGfOc+obyi1Dg04PrViyiLlF7qPHRWAoFkwq0QLpw1AV6w10r6wad7Q61kNpIvXDjo+IobO8cQnVR0QMW6BboHOopyntUi3sVdq/SNURZ98ONSffLw+3QfjhJHcTwyjcS8rmOboGK7dR36nBwfRt27yNn0xvdSb2DLYgyzgc71/k0RhXwLPUWlrZt6Jq6wreX99Qr6hR1DHavFlAsd+MKVvjAP1EnnK0R2pcPqG2oTtMUVcXoPJq1Lvn49uT3qNqM0GdcmYUODgWqF/L3xL7SqrV0aSse3yZiZPMtIsUCahP+FD49lxYn7KPKmALDA5LvSPYes2BBNlnpJmie47B+7JkH2wphhnxBOfhJsMqqtqEqKt/TsBYX7j0thrZUeBLy6auxv4qK0hvYMW0v9YyaWvIArsD21brApuKj/ae39hB2wtKZN2YVbE5tExUuVVxV7H+C+psOG0plfW+K2swO2Cmnagvpjfv5V7rrjFB+q182Ud3fpkwmk8mk+AXlaowf6uQ19QAAAABJRU5ErkJggg==>

[image15]: <data:image/png;base64,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>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAaCAYAAACzdqxAAAABKklEQVR4Xu2SvUoDURBGR1RQUIk/KHYqNtaiVRpBCxO0sLLUygfwGQTtfQURfx5BJGUgKbW0E3wDERTj+Zy7cPcSIRu7sAcOWb7snUzmjllJyeAxgWNp+F+W8RVvcSRkQ3iKTZwNWWG28RvPomwOn7GF01FeiAd8w5UoO8FO+OwbFW2YzznjCt9xI8oKo87iMQiNQWokfaPCB0mmbtW1LrGWfNcTmqsKH0WZLlPZHq7jjfmYzs03RM+XWDe/9F0/lmcfv/AD7/ARr/EJX7CNm7iEW37kdzz6h1NYxdGQ59BsVVxdLGIl5Hp5IeQputC1NIzRoYbl1+wvhs071Q9qBSdDvorj2UsZKqhV69ZVyiF+4g7eh2weL6xL4WPzwr2iBrImZsw3pmSQ+AEAeCu/c+FIbAAAAABJRU5ErkJggg==>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAaCAYAAABYQRdDAAABSUlEQVR4Xu2Tu0oEQRBFS1AQNPCFi2iimaGIgpmBgQqKiKmgkR9g4BcY+AsmRgY+UjORCQUNNVoMBFHwA8TA17lUj/bIsMzOJAp74LC7d5rq6t4asxYt/h/d2Pk7rMIoPuAxtoesDbfxEvtD1hRz+IG7UTaAt3iFvVFemHN8wrEo28LP8FkKFUzM71Xo6If4glMhaxp1lHd0qe+lUNHV6Le6U5fqVl0vRs8KoXtU0Y0oew7ZEk7iEa7hCi5jPazT6U7tZ2K+0aI3fMUTvMAJvME7vMZp85NoCg6Cuv8EdywH7abCWjSEPSHvwFrIUzTP2mgex/HRfBwzpLvFo9SIBbzHEfNGtMFwZoV5MY1T3E0jdMfpy7CHZ5bzam+aFy2CpqDPvMigecczmRUlmMV382513/vhsxKaiATXzQt2ZZ5WIJ2Qov/BH+YL+EQ3L2GpmMgAAAAASUVORK5CYII=>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAaCAYAAABYQRdDAAABcElEQVR4Xu2Uq0sEURSHj/jAZRXxUYwugsGg4COIyaRBg8lXNQh2QRC2CYLFqiAmwaIgNlkEQQTDsn+AsIpiMwgWg/r7ca47dw4MzFw3GPzgY+6cezhz575E/hADcAcuwZzpy0wrPIfHsA0uwE845ydlhUVPYQV2wxH4Djf8pBCaYYtrc4QcKUdcNzgVl7DDdoTSIFqwy3aEMgq3XXsMrnp9QYzDElyEy/AMzsQyPBrhFLyGr/DL+Azzor/sx9/gkCRwKJrEgk+u/QEfnUdRajpW4LqJscgLLJh4KrgdbmGfifM3g4tyPjgvTSZehXew08RTMSs6fxbGijaYFl4MV6LHj/BZhMPuPZh+WBZdnCo8ifVG8IObojvlBu6Lzn3i5uet0yt6EyWxBiddmzcT1+MeHtQyApiX6KN7oos7AXtqGb+gXfTk1QWetF3RM/8gelNxjgf9pKxwUbZEC1+453QsIwCuPu9PjpD+bMN/Ir4BZb1Bw0ctfj8AAAAASUVORK5CYII=>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAZCAYAAADe1WXtAAABWElEQVR4Xs2VrUsFQRRHr6CiPEHRIH6AaLEKfiT/AYMGLfq02uzWbYJR7GIyKohN5EWryaJFBJtNg0E9P2YW5w0IuzMP8cDhzd4Zhrsz9901+0fM4iE2sT+aq00fXuIZDuAmfuJauKgu2vQc73AE5/EN98NFKfRgrx8rQ2WqjDtCF17jcDyRwwY24mAOC3jgx4u4G8wlsYQ3uIXbeIErbSsCTvALX/HZjz/wyXv6s7QaulGVhm5TFyAe8RYHy0V12cG9KKbMXnAmildCmSij6SiucknedNXc+cUoVsTBqqgk3qOY/tf3OBnFK6MNWuYuS+i3wDn/nIUaxJi5pvEbBU6ZqwzV5jI+WOK5lyh7lZ02nTDXnVrm3jaZbnO99NhcPV/hUduKBEbNZbnunzXOatBCmSpLdf/COvDqQhvIIRy3jDoO0WekbCzqp6qEbFTDOleVX9l4/oZvLSs0+eaCuhcAAAAASUVORK5CYII=>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAZCAYAAADNAiUZAAABTElEQVR4Xu2UMShFURjHP6HoKYqUvIWyW8igDKyU6Q1MkskgA6XU2ySb7JKYDAxKMdxRGZSSEouULDYGC/+v73+793690Oueyf3Vr/fd/znvnXfOd7oiBQUFBb+wC7/gG3xm/QmfaHsyNR+a4Tucgg3MHuGlBFgsZhYuumwPvsB+l+eC7kR31OfyCwm46KRY/zyaVX2YF0Pww2Vt8A6WXa79nhc7+nO4DU/gJseO4A2c4Px9OM06gy4QiV0mRT+rcJDPafRUKql6RKwNag+N4DLnPMBR1jXpFPtSix+oge7qwIdif/YMtvL5VP72ez+ip9IBu+Ats5Ikl1B3vMZa566yrpv4lh/DcfjKfE6SHkZwhvVAKq8bPbJDuAF3xC7JutjFil8oS/AKrsBr2Ms8GNq7SOxYh+F9ZjQQTXALLoj1diw7HI5u2ugH/ifff/k10Y/TtqEAAAAASUVORK5CYII=>