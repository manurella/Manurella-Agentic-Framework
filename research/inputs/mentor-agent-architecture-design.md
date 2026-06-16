# **Architectural Specifications for the Manurella Mentor Domain: A State-of-the-Art Multi-Agent Tutoring Framework**

## **Macro-Competency Mapping in Language Acquisition and Intelligent Tutoring**

To construct an agentic framework capable of delivering personalized instruction at scale, the underlying system must translate core competencies from cognitive science and second language acquisition (SLA) into explicit, testable computational moves.1 Conventional computer-assisted language learning (CALL) software relies on static branching paths that fail to capture the dynamic linguistic and affective shifts of a live student.1 Conversely, modern generative architectures risk unconstrained conversational drift, sacrificing pedagogical rigor for conversational fluency.4 This design balances these forces by mapping the macro-competencies of effective human tutoring onto a runtime-agnostic, multi-agent architecture.5

| Competency Area | Educational & Cognitive Mechanism | SLA Theoretical Foundation | Architectural Implementation |
| :---- | :---- | :---- | :---- |
| **Placement Evaluation** | Multi-dimensional testing assessing productive and receptive performance across lexical, grammatical, and syntactic dimensions.2 | Vygotsky's Zone of Proximal Development (ZPD) and CEFR proficiency standards.2 | *Macro-Placement & Placement Director* executing adaptive diagnostics and establishing the baseline user profile state.5 |
| **Curriculum Planning** | Graph-based skill sequencing mapping specific user objectives to discrete knowledge components.8 | Bruner's Spiral Curriculum (iterative re-visitation with increasing complexity).9 | *Curriculum Planner & Sequencer* generating dynamic, non-linear progression trees over structured skill models.8 |
| **Concept Explanation** | Controlled information presentation utilizing worked examples and faded scaffolding.9 | Cognitive Load Theory (managing intrinsic load while minimizing extraneous load).9 | *Comprehensible Input Synthesizer* dynamically adjusting structural complexity and injecting meta-cognitive prompts.2 |
| **Error Correction** | Context-aware, immediate corrective feedback (CF) balanced to optimize uptake and self-repair.3 | Schmidt's Noticing Hypothesis and Swain's Output Hypothesis (pushed output driving restructuring).15 | *Linguistic Diagnostic Specialist* and *SLA Pedagogical Policy Engine* selecting the optimal feedback type.1 |
| **Practice Design** | Scaffolding transitions from highly controlled substitution drills to free communicative production.7 | Pearson & Gallagher's Gradual Release of Responsibility (GRR) ("I do, we do, you do").9 | *Targeted Practice & Drillmaster* managing active, constructive, and interactive practice modes.10 |
| **Spaced Repetition** | Exponential review intervals calculated dynamically from active recall success metrics.18 | Ebbinghaus's Forgetting Curve and the psychological Spacing Effect.18 | *Asynchronous State Tracer* executing Half-Life Regression (HLR) and Free Spaced Repetition Scheduler (FSRS) calculations.21 |
| **Learner Modeling** | Probabilistic tracking of latent knowledge variables across sequential interactions.23 | Hidden Markov Model formulations of cognitive skill acquisition.23 | *Asynchronous State Tracer* maintaining Bayesian Knowledge Tracing (BKT) probability matrices.23 |
| **Feedback Tone** | Dynamic adjustment of conversational threat levels to preserve student motivation and decrease anxiety.27 | Krashen's Affective Filter Hypothesis (negative emotions block comprehension and intake).28 | *SLA Pedagogical Policy Engine* modulating instruction to keep the student's affective filter low.27 |
| **Progress Tracking** | Continuous streaming of interaction data into instructor-facing diagnostic metrics.6 | Formative Assessment and resolving the "Blind Instructor Problem".6 | *Asynchronous State Tracer* emitting telemetry schemas to analytics pipelines.6 |
| **Subject Domain Transfer** | Portability of diagnostic, policy, and synthesis mechanics to non-language domains.5 | Transfer of Learning and structural schema generalizability.30 | Standardized Spoke-and-Wheel coordination protocols adaptable to logic, math, or coding environments.4 |

## **Architectural Paradigm: The Spoke-and-Wheel Model vs. Alternative Decompositions**

The target implementation runtime for the Manurella Agentic Framework is Kilo Code, but the sub-agent architecture is designed to remain strictly portable to Codex, ChatGPT, Gemini, and custom Python/Model Context Protocol (MCP) tooling.5 To ensure that weaker, free-tier, or locally deployed open-source models can execute this framework reliably without suffering from semantic drift or formatting degradation, the synchronous teaching layer is organized as a Spoke-and-Wheel architecture.4  
\[Evidence\] In this model, parallel specialist agents (the Spokes) process specific dimensions of the user interaction independently, while a centralized orchestrating agent (the Hub Synthesizer) coordinates their outputs.4 Centralized coordination in parallel multi-agent configurations has been shown to improve performance by up to 80.9% on parallelizable tasks compared to independent agent setups, while containing error propagation to 4.4x (as opposed to 17.2x in uncoordinated chains).34  
\[Project Experience\] Prior prototype deployments (such as the ITAS framework evaluated in graduate-level STEM courses) confirm that consolidating linguistic analysis, pedagogical strategy selection, and natural language synthesis into a single agent prompt introduces severe cognitive overload, resulting in high rates of task-boundary hallucinations.4 Decomposing the system by *domain* (e.g., separating the linguistic parser from the pedagogical policy generator) rather than by *task* (e.g., separating planner from teacher) ensures that each sub-agent maintains a highly localized context window and a narrow, predictable failure mode.4 An agent that only parses grammar cannot hallucinate vocabulary indices or invent timestamps.4

### **Critique of Alternative Decompositions**

* **The Monolithic Tutor Persona**: In this alternative, a single comprehensive prompt directs the model to behave as an empathetic, adaptive tutor.2 While simple to implement, empirical testing shows that weaker models consistently default to conversational responses that overlook structural errors (diagnostic drift), or conversely, provide overly dense grammatical explanations that overload the student's working memory.4  
* **The Sequential Cascade Chain**: In this configuration, user input is passed sequentially through a pipeline: User Input ![][image1] Diagnostic Agent ![][image1] Policy Agent ![][image1] Response Agent.33 \[Evidence\] While logically intuitive, this model exhibits severe reasoning instability when executing on smaller parameters.33 A single diagnostic error at the beginning of the chain propagates downstream, leading to a cascade of inappropriate teaching moves that confuse the learner and damage system trust.17  
* **Symmetric Multi-Agent Debate**: This setup involves multiple peer-learner agents debating solution paths in front of the student.32 While effective for inducing cognitive conflict in structured STEM subjects like mathematics, debate configurations are highly inefficient for real-time conversational language tutoring.32 They introduce prohibitive token consumption and latency overheads that violate the sub-4-second conversational response threshold required for classroom deployments.34

The Spoke-and-Wheel design solves these limitations by running analytical spokes in parallel, ensuring the central Synthesizer receives structured, validated inputs before constructing the student-facing response.4

## **Sub-Agent Functional Classifications: Selectable vs. Internal**

To maintain a clean system architecture, sub-agents are divided into two tiers: Top-Level Selectable Agents, which are directly exposed to the runtime environment and coordinate major learning modes, and Internal Sub-Agents, which are abstracted behind orchestration boundaries to perform specialized analytical calculations.5

| Agent Name | Structural Tier | Exposure & Visibility Boundary | Primary Operational Purview | Core Orchestration Pattern |
| :---- | :---- | :---- | :---- | :---- |
| **Macro-Placement & Placement Director** | Top-Level Selectable | Exposed directly to the client runtime during onboarding or unit transitions.8 | Establishes the user's initial baseline CEFR proficiency and constructs the core student profile.2 | Executes a structured diagnostic battery, passing findings directly to the student database.8 |
| **Curriculum Planner & Sequencer** | Top-Level Selectable | Exposed to the client runtime at the start of each learning block or unit.8 | Generates the optimal sequence of target skills based on student goals and current mastery gaps.8 | Queries the master skill database and runs optimization algorithms to sequence the dynamic learning path.8 |
| **Conversational Interlocutor** | Top-Level Selectable | Selectable by the user/client for open-ended or role-play practice.3 | Simulates realistic conversations to drive natural production and low-anxiety output.2 | Orchestrates the *Linguistic Diagnostic Specialist*, *SLA Pedagogical Policy Engine*, and *Comprehensible Input Synthesizer* in a synchronous Spoke-and-Wheel loop.4 |
| **Targeted Practice & Drillmaster** | Top-Level Selectable | Selectable by the user/client for focused skill reinforcement.8 | Administers controlled structural exercises, fill-in-the-blank drills, and active recall tests.10 | Executes strict sequential question-answer loops targeting specific, isolated knowledge components.9 |
| **Linguistic Diagnostic Specialist** | Internal Sub-Agent | Completely abstracted behind the Top-Level Selectable Agents.4 | Conducts three-way diagnostic parsing of student inputs (optimal vs. valid suboptimal vs. incorrect).17 | Operates as a parallel analytical spoke; processes the raw user utterance and outputs a structured error payload.4 |
| **SLA Pedagogical Policy Engine** | Internal Sub-Agent | Completely abstracted behind the Top-Level Selectable Agents.4 | Resolves the assistance dilemma by selecting the appropriate corrective feedback or scaffolding strategy.11 | Operates as a parallel analytical spoke; matches the diagnostic payload against the student's mastery history.4 |
| **Asynchronous State Tracer** | Internal Sub-Agent | Runs out-of-band; completely invisible to the synchronous client loop.10 | Computes updated latent mastery probabilities (BKT) and memory half-life decay curves (HLR).21 | Executes asynchronously post-interaction; reads raw interaction logs and commits atomic parameter updates.10 |

## **Detailed Sub-Agent Specifications**

### **1\. Macro-Placement & Placement Director**

* **Purpose**: Evaluates the student's productive and receptive language capabilities during onboarding to establish an initial CEFR proficiency mapping and construct the baseline student profile.2  
* **Use-When Boundary**: Triggers automatically upon initial user registration, or when a student requests a formal re-evaluation after a prolonged period of absence.  
* **Do-Not-Use Boundary**: Must not be executed during standard conversational sessions or targeted drills, where continuous state tracing is preferred.21  
* **Required Context**:  
  * Target language domain profile (vocabulary mappings, morphosyntactic hierarchies, phonological properties).14  
  * User-declared learning goals (e.g., professional, travel, academic).8  
  * Historical diagnostic calibration datasets (reference correlations between test items and CEFR tiers).  
* **Tools and Permissions**: Write access to the student profile database; read access to the master diagnostic question pool.10  
* **Output Contract (Strict JSON Schema)**:

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "PlacementEvaluationPayload",  
  "type": "object",  
  "properties": {  
    "estimated\_cefr\_level": {  
      "type": "string",  
      "enum":  
    },  
    "dimension\_scores": {  
      "type": "object",  
      "properties": {  
        "lexical\_precision": { "type": "number", "minimum": 0.0, "maximum": 1.0 },  
        "morphosyntactic\_accuracy": { "type": "number", "minimum": 0.0, "maximum": 1.0 },  
        "pragmatic\_comprehension": { "type": "number", "minimum": 0.0, "maximum": 1.0 }  
      },  
      "required": \["lexical\_precision", "morphosyntactic\_accuracy", "pragmatic\_comprehension"\]  
    },  
    "detected\_fossilized\_errors": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "grammar\_concept\_id": { "type": "string" },  
          "description": { "type": "string" }  
        },  
        "required": \["grammar\_concept\_id", "description"\]  
      }  
    },  
    "recommended\_initial\_skills": {  
      "type": "array",  
      "items": { "type": "string" }  
    }  
  },  
  "required": \["estimated\_cefr\_level", "dimension\_scores", "detected\_fossilized\_errors", "recommended\_initial\_skills"\]  
}

* **Evaluation Rubric**:  
  * *Diagnostic Stability*: Measured by the correlation between predicted placement level and the user's performance across their first 50 learning trials. Target Pearson ![][image2].  
  * *Calibration Accuracy*: Misclassification rate relative to gold-standard human placement interviews must remain below 10%.  
* **Common Failure Modes**:  
  * *Novice Cold-Start Floor*: Misclassifying absolute beginners as A2 due to lucky guesses on multiple-choice diagnostic items.25  
  * *Fluency-Accuracy Disparity*: Overestimating the overall CEFR level of a student who demonstrates high lexical range but severe, systemic morphosyntactic fossilization.43

### **2\. Curriculum Planner & Sequencer**

* **Purpose**: Maps the student's personal goals to required language skills and calculates the optimal, personalized learning path over the domain knowledge graph.8  
* **Use-When Boundary**: Executes at the start of each learning unit, or dynamically when the *Asynchronous State Tracer* flags that a student has achieved mastery across all active target skills.8  
* **Do-Not-Use Boundary**: Must not be used during live conversational turns to resolve immediate errors.1  
* **Required Context**:  
  * Master domain model (concept dependency graph, prerequisite nodes).1  
  * Current student state vector (mastered concepts, active gaps, historical struggle patterns).8  
  * Target professional or personal goal taxonomy.8  
* **Tools and Permissions**: Read/Write access to the student curriculum state; read access to the master domain knowledge graph.8  
* **Output Contract (Strict JSON Schema)**:

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "CurriculumSequencePayload",  
  "type": "object",  
  "properties": {  
    "current\_unit\_id": { "type": "string" },  
    "skill\_progression\_path": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "step\_order": { "type": "integer" },  
          "knowledge\_component\_id": { "type": "string" },  
          "prerequisite\_satisfied": { "type": "boolean" },  
          "instructional\_delivery\_mode": {   
            "type": "string",   
            "enum":   
          }  
        },  
        "required": \["step\_order", "knowledge\_component\_id", "prerequisite\_satisfied", "instructional\_delivery\_mode"\]  
      }  
    },  
    "dynamic\_optimization\_metric": { "type": "number" }  
  },  
  "required": \["current\_unit\_id", "skill\_progression\_path", "dynamic\_optimization\_metric"\]  
}

* **Evaluation Rubric**:  
  * *Prerequisite Integrity*: Zero occurrences of sequencing a highly complex skill (e.g., conditional past tense) before its dependency prerequisites (e.g., simple past tense) are satisfied.8  
  * *Path Efficiency*: Ratio of trials-to-mastery on optimized paths compared to historical static sequences. Target improvement ![][image3].  
* **Common Failure Modes**:  
  * *Goal-Curriculum Mismatch*: Mapping a professional business goal to highly informal, colloquial conversational modules.8  
  * *Looping Deadlocks*: Generating circular dependency loops in the dynamic path when a student continuously fails to master a critical prerequisite node.33

### **3\. Conversational Interlocutor**

* **Purpose**: Simulates realistic, context-specific interactions to drive low-anxiety language production while coordinating internal sub-agents to execute targeted instructional moves.2  
* **Use-When Boundary**: Activated when the student selects communicative role-play, free-form conversation, or task-based dialogue simulation.  
* **Do-Not-Use Boundary**: Must not be used for structured grammatical conjugation drills or isolated vocabulary flashcard testing.10  
* **Required Context**:  
  * Active scenario definition (narrative graph, role-play constraints, situational goals).5  
  * Dialogic history window (strictly limited to the preceding 10 conversational turns).29  
  * Current target linguistic components (specific grammar structures or lexical items to prompt).2  
* **Tools and Permissions**: Read/Write access to active session state buffers.29  
* **Output Contract (Strict JSON Schema)**:

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "ConversationalOutputPayload",  
  "type": "object",  
  "properties": {  
    "interlocutor\_utterance": { "type": "string" },  
    "scaffolding\_prompt\_overlay": { "type": "string" },  
    "active\_conversational\_stage": { "type": "string" },  
    "comprehensible\_input\_index": { "type": "number", "minimum": 0.0, "maximum": 1.0 }  
  },  
  "required": \["interlocutor\_utterance", "scaffolding\_prompt\_overlay", "active\_conversational\_stage", "comprehensible\_input\_index"\]  
}

* **Evaluation Rubric**:  
  * *Affective Preservation*: Student turn-retention rate. Conversational drops or premature session exits must be minimized below 5%.3  
  * *Target Injection Rate*: Successful elicitation of active target linguistic structures within a standard 10-turn dialogue window without breaking narrative consistency.2  
* **Common Failure Modes**:  
  * *Conversational Takeover*: Writing paragraphs of complex prose that dominate the interaction, violating the target ![][image4] comprehension boundary.4  
  * *Scenario Abandonment*: Diverging from the structured role-play constraints (e.g., ordering food at a restaurant) to discuss unrelated general topics introduced by the user.4

### **4\. Targeted Practice & Drillmaster**

* **Purpose**: Coordinates high-frequency structural drills, fill-in-the-blank grammar exercises, and active recall trials targeting specific, isolated knowledge components.10  
* **Use-When Boundary**: Executed when the curriculum sequences a focused practice block to reinforce newly introduced forms.8  
* **Do-Not-Use Boundary**: Must not be used for open-ended, pragmatic conversation where interaction flow is the primary metric.3  
* **Required Context**:  
  * Target knowledge component ID (grammar rule or lexical lemma).10  
  * Student performance history for the active target concept.10  
  * Localized exercise template arrays.  
* **Tools and Permissions**: Read access to the master exercise repository.39  
* **Output Contract (Strict JSON Schema)**:

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "DrillmasterOutputPayload",  
  "type": "object",  
  "properties": {  
    "drill\_id": { "type": "string" },  
    "drill\_type": {   
      "type": "string",   
      "enum":   
    },  
    "prompt\_text": { "type": "string" },  
    "expected\_lexical\_target": { "type": "string" },  
    "scaffolding\_hints": { "type": "array", "items": { "type": "string" } }  
  },  
  "required": \["drill\_id", "drill\_type", "prompt\_text", "expected\_lexical\_target", "scaffolding\_hints"\]  
}

* **Evaluation Rubric**:  
  * *Focus Adherence*: 100% of generated drills must target the designated knowledge component, preventing structural contamination from unassigned rules.  
  * *Hint Quality*: Generated hints must provide metalinguistic clues or contextual references rather than prematurely exposing the correct answer.43  
* **Common Failure Modes**:  
  * *Template Exhaustion*: Repeating identical sentence stems during a single drill session, inducing rote memorization rather than rule generalization.19  
  * *Ambiguity Leakage*: Generating fill-in-the-blank items where multiple unmodeled answers are linguistically valid, resulting in false negatives during grading.

### **5\. Linguistic Diagnostic Specialist**

* **Purpose**: Performs high-precision, three-way parsing of student responses to identify morphological, syntactic, and lexical deviations, separating optimal responses from valid suboptimal phrasings and outright errors.17  
* **Use-When Boundary**: Executes synchronously behind the scenes immediately upon receipt of any student response in active dialogue or drill runtimes.4  
* **Do-Not-Use Boundary**: Must never communicate directly with the student or attempt to explain grammar concepts.4  
* **Required Context**:  
  * The exact prompt presented to the student.24  
  * The raw student input string.24  
  * Expected target forms and acceptable syntactic variations.17  
* **Tools and Permissions**: Read-only query access to localized morphological dictionaries and syntactic knowledge graphs.17  
* **Output Contract (Strict JSON Schema)**:

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "LinguisticDiagnosticPayload",  
  "type": "object",  
  "properties": {  
    "evaluation\_category": {   
      "type": "string",   
      "enum":   
    },  
    "detected\_errors": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "error\_category": {   
            "type": "string",   
            "enum":   
          },  
          "erroneous\_substring": { "type": "string" },  
          "target\_linguistic\_correction": { "type": "string" },  
          "rule\_id": { "type": "string" }  
        },  
        "required": \["error\_category", "erroneous\_substring", "target\_linguistic\_correction", "rule\_id"\]  
      }  
    },  
    "alternative\_phrasings": { "type": "array", "items": { "type": "string" } }  
  },  
  "required": \["evaluation\_category", "detected\_errors", "alternative\_phrasings"\]  
}

* **Evaluation Rubric**:  
  * *Alternative Recall Rate*: Percentage of valid, native-like alternative phrasings correctly classified as VALID\_SUBOPTIMAL or OPTIMAL rather than INCORRECT.17 Target accuracy ![][image5].  
  * *Diagnostic Precision*: Error categorization accuracy compared to human annotator gold labels.17 Target precision ![][image6].  
* **Common Failure Modes**:  
  * *Over-Rejection Bias*: Systematically categorizing natural, colloquial regional variations or valid non-standard syntactic pathways as incorrect.17  
  * *Orthographic Over-Validation*: Overlooking subtle grammatical errors (such as incorrect gender markings in Romance languages) by misinterpreting them as minor spelling typos.17

### **6\. SLA Pedagogical Policy Engine**

* **Purpose**: Resolves the assistance dilemma by selecting the optimal corrective feedback type or scaffolding adjustment based on the student's estimated mastery and session metadata.35  
* **Use-When Boundary**: Executes synchronously immediately after the *Linguistic Diagnostic Specialist* returns a non-optimal evaluation payload.4  
* **Do-Not-Use Boundary**: Must not parse raw student text or formulate student-facing dialogue.1  
* **Required Context**:  
  * Active diagnostic payload from the *Linguistic Diagnostic Specialist*.4  
  * Current student state parameters (BKT mastery values, historical error counts for the target skill).23  
  * Recent feedback history (tracking feedback types delivered in the preceding 5 turns to prevent repetition).14  
* **Tools and Permissions**: Read-only access to the student profile state.  
* **Output Contract (Strict JSON Schema)**:

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "PedagogicalPolicyPayload",  
  "type": "object",  
  "properties": {  
    "selected\_pedagogical\_action": {  
      "type": "string",  
      "enum":  
    },  
    "scaffolding\_fading\_coefficient": { "type": "number" },  
    "cognitive\_load\_state": {   
      "type": "string",   
      "enum":   
    },  
    "affective\_filter\_mitigation\_flag": { "type": "boolean" }  
  },  
  "required": \["selected\_pedagogical\_action", "scaffolding\_fading\_coefficient", "cognitive\_load\_state", "affective\_filter\_mitigation\_flag"\]  
}

* **Evaluation Rubric**:  
  * *Scaffolding Alignment*: Percentage of corrective moves matching the learner's developmental stage.9 For high-mastery skills (![][image7]), the agent must select elicitation, repetition, or clarification requests to force active self-repair.14 Explicit corrections must be restricted to novice zones (![][image8]).31  
  * *Uptake Rate*: The ratio of successful self-corrections on the turn immediately following the feedback. Target uptake ![][image9] for intermediate learners.14  
* **Common Failure Modes**:  
  * *Scaffolding Traps*: Continuously providing highly intrusive explicit corrections to high-knowledge students, triggering the expertise reversal effect and degrading active retrieval.31  
  * *Frustration Loops*: Issuing open-ended clarification requests to absolute novices who lack the foundational schema to identify their own errors, leading to unproductive struggle.11

### **7\. Asynchronous State Tracer**

* **Purpose**: Processes student response outcomes out-of-band to calculate updated latent mastery probabilities and update memory decay half-lives.21  
* **Use-When Boundary**: Triggers asynchronously immediately after the completion of a synchronous dialogue turn or drill event.10  
* **Do-Not-Use Boundary**: Must never execute in the synchronous request-response flow to prevent introducing latency into student interactions.29  
* **Required Context**:  
  * Completed interaction trace (exercise prompt, student input, diagnostic evaluation payload, response latency, timestamp).10  
  * Pre-existing student state vectors.21  
  * Chronological time delta since the student last practiced the specific knowledge components.21  
* **Tools and Permissions**: Write access to the student profile database.10  
* **Output Contract (Strict JSON Schema)**:

JSON  
{  
  "$schema": "http://json-schema.org/draft-07/schema\#",  
  "title": "StateTracerUpdatePayload",  
  "type": "object",  
  "properties": {  
    "student\_id": { "type": "string" },  
    "last\_interaction\_timestamp": { "type": "integer" },  
    "updated\_knowledge\_components": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "knowledge\_component\_id": { "type": "string" },  
          "bkt\_posterior\_mastery": { "type": "number", "minimum": 0.0, "maximum": 1.0 },  
          "hlr\_decay\_half\_life\_seconds": { "type": "number" },  
          "predicted\_recall\_probability": { "type": "number", "minimum": 0.0, "maximum": 1.0 }  
        },  
        "required": \["knowledge\_component\_id", "bkt\_posterior\_mastery", "hlr\_decay\_half\_life\_seconds", "predicted\_recall\_probability"\]  
      }  
    }  
  },  
  "required": \["student\_id", "last\_interaction\_timestamp", "updated\_knowledge\_components"\]  
}

* **Evaluation Rubric**:  
  * *Predictive Performance*: Mean Absolute Error (MAE) of the predicted recall probability relative to observed next-session outcomes.21 Target MAE ![][image10].  
  * *Calibration Stability*: Area Under the ROC Curve (AUC) for binary success predictions.21 Target AUC ![][image11].  
* **Common Failure Modes**:  
  * *Parameter Over-Learning*: Unchecked progression of BKT mastery probabilities to near-ceiling values due to lucky guessing, ignoring the slip parameter boundaries.23  
  * *Truncation Errors*: System failures when processing exceptionally long interaction histories due to state parameter drift or database race conditions during rapid multi-turn drills.10

## **Context Partitioning and Memory Management**

To maintain execution stability and minimize inference costs when operating on highly constrained, weaker, or free model runtimes, context must be strictly partitioned into three isolated tiers.39

| Context Tier | Storage & Retrieval Mechanism | Injected Variables | Target Token Overhead | System Lifecycle |
| :---- | :---- | :---- | :---- | :---- |
| **Always-On System Prompt** 4 | Statically compiled in application memory; prepended directly to every API payload.55 | \- Sub-agent identity and role-boundary constraints.4 \- Strict JSON schema definitions and structural formatting guards.55 \- Negative constraints (e.g., prohibition of conversational text for internal spokes).4 | ![][image12] tokens. | Persistent across all sessions. |
| **Static Reference Materials** 4 | Cached locally; dynamically appended *only* when the orchestration layer flags active domain triggers.4 | \- Morphological paradigms and localized grammar sheets.14 \- SLA pedagogical feedback taxonomies.44 \- Scenario-specific constraint rules and CEFR vocabulary lexicons.2 | ![][image13] tokens (only when active). | Ephemeral; loaded on transition between distinct grammatical concepts or role-play scenarios. |
| **Just-In-Time Retrieved Context** 26 | Queried dynamically from database vector indexes (using RAG or direct primary key lookup) based on current task metadata.26 | \- Preceding 3 conversational history turns (compressed).29 \- Updated student BKT and HLR state variables.21 \- Specific vocabulary items flagged for review.21 | ![][image14] tokens. | Read-on-demand; discarded immediately post-inference turn. |

This partitioning is managed by the Kilo Code orchestration layer, which utilizes a lossless evidence-alias pattern to compress raw database values.54 Rather than transmitting verbose JSON payloads of historical student actions into the model prompt, metadata keys are stripped and mapped to short, row-oriented index representations.54 This pattern reduces input token count on large, evidence-heavy workflows, preventing context-window overload and safeguarding the attention mechanisms of smaller-parameter models.54

## **Optimization of Weaker and Non-Frontier Models**

\[Project Experience\] Deploying agentic frameworks onto weaker, open-source, or non-frontier models (e.g., Llama-3-8B or Qwen-2.5-7B) reveals critical performance bottlenecks.33 These models routinely fail at one-shot generation of complex structured data, drop nested keys under high-context stress, and suffer from cascade reasoning failures.33 To achieve production-grade stability on constrained models, five architectural optimizations are integrated directly into the framework:

### **1\. The Accumulator Pattern (Stateful Tool-Calling Builders)**

\[Project Experience\] Demanding that a weaker model produce a comprehensive 300-line JSON diagnostic and pedagogical response in a single inference pass is a major failure point in production.57 The model frequently outputs invalid JSON syntax, forgets required keys, or hallucinates content simply to satisfy structural completeness.56 The framework bypasses this by utilizing the Accumulator Pattern 57:

* **Mechanism**: The model is provided with a suite of highly focused, granular tool calls (e.g., add\_morphological\_error(erroneous\_substring, correction), set\_pedagogical\_action(action\_type)) and instructed to build its evaluation incrementally.57  
* **Impact**: The model never generates the final structured JSON object directly.57 Instead, each tool call executes a localized validation check, and the final structured payload is accumulated statefully in the application code.57 If the model fails mid-generation or runs out of token space, the system preserves the partial results committed up to that point, enabling immediate recovery.57

### **2\. Weak-Link Optimization (WORC Framework)**

Reasoning instability in multi-agent configurations occurs because errors generated by weaker sub-agents are amplified across downstream transitions, degrading consensus.33 The framework resolves this by implementing the WORC (Weak-link Optimization for Reasoning and Collaboration) protocol 33:

* **Mechanism**: During the orchestration cycle, a meta-learning weight predictor analyzes task complexity and historical performance features to dynamically identify the "weak-link" agent in the active graph.33  
* **Impact**: Rather than routing equal compute budgets across all nodes, the system allocates an uncertainty-driven repeated-sampling quota to the weak agent.33 By running parallel sampling paths on identified weak links, error propagation is mitigated, stabilizing the global multi-agent system.33

### **3\. Node-Sampling Sequence Refinement**

\[Evidence\] Applying structural optimization models (such as GPTSwarm or Node-Sampling) to agent execution paths demonstrates that longer, fixed sequences of agents do not linearly improve quality.53 Often, specific agents (such as rephrasing or grammar-checking nodes) introduce redundancy without improving utility.53

* **Mechanism**: The framework uses a regularized utility-scoring algorithm (![][image15]) to prune underperforming sub-agents.53  
* **Impact**: The sequence is dynamically compressed to apply only high-impact nodes (e.g., *NegativeWorded* or *TwoInOne* question generators) repeatedly, while omitting redundant rephrasing passes, achieving high-quality output while conserving token budgets.53

### **4\. LessonL Shared-Lesson Banking**

Weaker models often fail because they lack the high-parameter generalization capabilities required to resolve complex learning conflicts on the fly.58 The framework addresses this by implementing a centralized Lesson Banking mechanism 58:

* **Mechanism**: When a sub-agent encounters a failure (e.g., a false-positive grammar diagnostic rejected by user verification), a *Lesson Solicitation* routine compiles a concise explanation of the failure and banks it in a shared repository.58  
* **Impact**: Subsequent agent executions query this bank using semantic retrieval.58 Access to this shared memory repository allows smaller models to learn from historical system errors, enabling them to outperform much larger, un-scaffolded frontier models.58

### **5\. Short-Circuit Before-Agent Callbacks**

To prevent wasteful model invocation, the Kilo Code runtime target implements deterministic, code-based short-circuit checks.4 For instance, if a student submits an empty response field, a pre-agent callback immediately interrupts the loop and returns a pre-defined scaffolding prompt, saving model invocation costs.4

## **Sub-Agent Empirical Benchmark Tasks**

To validate performance across diverse target model runtimes, each sub-agent is evaluated against a formalized benchmark suite:

\[User Utterance\]   
       |  
       v  
\+------------------------------------------+  
|  Linguistic Diagnostic Specialist (LDS)  |  
|  \- Task: 3-way parsing of learner text  |  
|  \- Dataset: CoNLL-Shared Task GEC        | \---\> Metric: F\_0.5 \>= 0.88  
\+--------------------+---------------------+  
                     |  
               
                     v  
\+------------------------------------------+  
|    SLA Pedagogical Policy Engine (PPE)   |  
|  \- Task: Feedback strategy selection     |  
|  \- Dataset: SLA Teacher Dialogue Logs     | \---\> Metric: Cohen's Kappa \>= 0.82  
\+--------------------+---------------------+  
                     |  
               
                     v  
\+------------------------------------------+  
|  Comprehensible Input Synthesizer (CIS)  |  
|  \- Task: i+1 generation & CEFR control   |  
|  \- Dataset: Cambridge English Profile    | \---\> Metric: Perplexity \<= 12.5  
\+------------------------------------------+

### **1\. Linguistic Diagnostic Specialist Benchmark**

* **Task Definition**: Three-way diagnostic classification of non-native student utterances.17 Given an input string containing grammatical, spelling, or structural errors, the agent must categorize the step (Optimal, Valid Suboptimal, or Incorrect) and extract the exact erroneous substring.17  
* **Test Dataset**: A partitioned subset of the CoNLL-Shared Task on Grammatical Error Correction, augmented with simulated student errors reflecting common second-language interference patterns.17  
* **Target Metric**: ![][image16] score ![][image11] (prioritizing precision over recall to prevent false-positive corrections).17 Over-rejection rate on valid alternative phrasings must remain ![][image17].17

### **2\. SLA Pedagogical Policy Engine Benchmark**

* **Task Definition**: Scenario-based strategy selection.1 Given a diagnostic input payload, a historical student mastery vector, and session metadata, the agent must output the optimal feedback type matching Lyster & Ranta’s pedagogical taxonomy.14  
* **Test Dataset**: An evaluation set derived from human-expert-annotated SLA classroom dialogue transcripts, mapping student errors and mastery levels to professional teacher interventions.14  
* **Target Metric**: Cohen's ![][image18] indicating high agreement with expert pedagogical decisions.

### **3\. Comprehensible Input Synthesizer Benchmark**

* **Task Definition**: Constrained natural language generation.2 Given a selected pedagogical action and a target CEFR lexical constraint, the agent must synthesize a contextually coherent conversational response that strictly respects the target lexical boundaries.2  
* **Test Dataset**: The Cambridge English Profile database, cross-referenced with scenario-based dialogues.2  
* **Target Metric**: Generation Perplexity ![][image19] on target CEFR levels; 100% compliance on the injection of designated target vocabulary items without structural leakage.2

### **4\. Asynchronous State Tracer Benchmark**

* **Task Definition**: Sequential student performance prediction.21 Given a longitudinal series of student interaction records, the agent must compute updated latent mastery probabilities and predict active recall success on subsequent trials.23  
* **Test Dataset**: The Duolingo Half-Life Regression public dataset, containing 13 million learning traces tracking active recall performance over time.21  
* **Target Metric**: Area Under the ROC Curve (AUC) ![][image11]; Mean Absolute Error (MAE) of recall predictions ![][image10].21

## **Roadmap: Functional Evolution and Multi-Subject Expansion Path**

The implementation roadmap is structured in three chronological phases to guide the system from its initial language-tutoring core to a generalized, multi-subject cognitive tutoring framework 5:

  v0: Conversational Core (Language First)  
  ├── Parallel Spoke-and-Wheel Architecture   
  ├── Kilo Code synchronous target implementation   
  ├── Basic BKT & HLR State Tracking   
  └── Corrective Feedback Taxonomy (Recast vs. Explicit)   
        │  
        ▼  
  v1: Portable Runtimes & Adaptive Scaffolding (6 Months)  
  ├── Model Context Protocol (MCP) tool integration \[56\]  
  ├── Portability adapters (Gemini, ChatGPT, Codex)   
  ├── Dynamic fading logic & worked example generation \[11, 13\]  
  └── Shared-memory Lesson Banking (LessonL)   
        │  
        ▼  
  v2: Collaborative Tutoring & Subject Transfer (12 Months)  
  ├── Multi-party peer-learning simulation   
  ├── Procedural logic proof diagnostic engine   
  ├── ICAP engagement framework integration   
  └── Automated scenario graph generation 

### **Phase v0: Conversational Core (Language First)**

* **Functional Scope**: Implementation of the primary Spoke-and-Wheel architecture optimized for French, Spanish, and English language learning first.2 The target execution environment is restricted to the Kilo Code runtime.4  
* **Core Runtimes**: Local Python wrappers, SQLite state tables.10  
* **Capabilities**:  
  * Parallel execution of the *Linguistic Diagnostic Specialist* and the *SLA Pedagogical Policy Engine*.4  
  * Synchronous response compilation by the *Comprehensible Input Synthesizer*.4  
  * Basic out-of-band *Asynchronous State Tracer* running standard BKT and HLR curves.21  
  * Feedback switching restricted to Recasts versus Explicit Corrections.44

### **Phase v1: Portable Runtimes and Adaptive Scaffolding (6-Month Milestone)**

* **Functional Scope**: Extension of the framework to support portability across Codex, ChatGPT, Gemini, and custom Model Context Protocol (MCP) tooling, alongside advanced adaptive scaffolding logic.5  
* **Core Runtimes**: MCP server configurations, Django/Node.js middleware layer, Firebase persistent logging.10  
* **Capabilities**:  
  * **MCP Tool Integration**: Allowing diagnostic spokes to query real-time dictionaries, linguistic corpuses, and custom translators dynamically via standardized tool-calling protocols.  
  * **Portable Adapters**: Decorator modules that handle structured JSON output generation on models that do not natively support strict schema parsing.55  
  * **Adaptive Fading**: Logic routines that transition from worked-example generators to completion tasks as student BKT mastery values cross pre-set thresholds.11  
  * **LessonL Integration**: Centralized lesson-banking databases enabling open-source local models to share failure metrics and recover from logic traps.58

### **Phase v2: Collaborative Tutoring and Subject Domain Transfer (12-Month Milestone)**

* **Functional Scope**: Transition of the architecture from language learning to structured STEM and humanities subjects (e.g., propositional logic proofs, computer programming syntax, algebra) and multi-party collaborative configurations.2  
* **Core Runtimes**: Django, n8n orchestration layers, BigQuery event streams.6  
* **Capabilities**:  
  * **Multi-Party Peer-Learning**: Simulating a digital classroom environment by instantiating asymmetric peer-agent profiles (e.g., *Conceptual-Error Peer Charlie* and *Procedural-Error Peer Alice*) alongside the main tutor, enabling collaborative learning-from-errors scenarios.32  
  * **STEM Subject Adaptation**: Remapping the diagnostic and policy spokes.4 The *Linguistic Diagnostic Specialist* translates to a *Procedural Proof Diagnostic Agent* using propositional logic knowledge graphs to validate steps.17 The *SLA Pedagogical Policy Engine* transitions to a *Cognitive Scaffolding Policy Agent* executing the ICAP engagement model.11  
  * **Automated Scenario Graphs**: Dynamically updating the narrative graph of instruction based on real-time learner motivation and cognitive load indices.5

## **Mathematical Formalization of the Learner Model State**

To track and predict student mastery and decay precisely, the *Asynchronous State Tracer* relies on two core mathematical frameworks.21

### **1\. Bayesian Knowledge Tracing (BKT) Update Logic**

For any targeted language skill or grammatical knowledge component, the student's mastery is modeled as a binary latent variable ![][image20], representing non-mastery or mastery respectively.23 Let the four model parameters be:

* ![][image21]: Prior probability of knowing the skill a priori.23  
* ![][image22]: Probability of transitioning from non-mastery to mastery after a practice opportunity.23  
* ![][image23]: Probability of making a mistake (slip) despite mastering the skill.23  
* ![][image24]: Probability of correctly applying the skill (guess) despite non-mastery.23

Upon observing a correct student response (![][image25]) at step ![][image26], the posterior probability of mastery is calculated as 23:  
![][image27]  
Upon observing an incorrect student response (![][image28]) at step ![][image26], the posterior probability of mastery is calculated as 23:  
![][image29]  
Following the calculation of the posterior, the mastery state is projected forward to account for the transition probability (learning) 23:  
![][image30]  
Mastery of the target skill is defined as achieving a projected probability ![][image31], triggering the system to fade explicit scaffolding.9

### **2\. Half-Life Regression (HLR) Forgetting Curves**

To model long-term memory retention and optimize spaced review schedules, the framework calculates memory stability using Half-Life Regression.21 The probability ![][image32] of recalling a specific lexical item decays exponentially according to the lag time ![][image33] since the last practice opportunity 21:  
![][image34]  
where ![][image35] represents the half-life of the item in the student’s memory.21 This half-life ![][image35] is modeled as an exponential function of a feature vector ![][image36] (summarizing the student's unique learning history with the word, including total correct attempts, total lapses, and historical exposure) and a learned weight vector ![][image37] 21:  
![][image38]  
The optimal model weights ![][image37] are resolved globally by minimizing a loss function ![][image39] that combines squared error loss with ![][image40] regularization 21:  
![][image41]  
where ![][image42] represents the loss scaling parameter balancing probability prediction with direct half-life estimation, and ![][image43] represents the regularization weight.21  
Using this mathematical state representation, the *SLA Pedagogical Policy Engine* schedules reviews when the probability of recall ![][image44].48 This boundary—the "Goldilocks zone" of active recall—forces the student's cognitive processing to maximize retention strength without causing unproductive failure.18

#### **Works cited**

1. Teaching machines to teach: Adaptive tutoring systems powered by generative models | by Khayyam H. | Medium, accessed June 16, 2026, [https://medium.com/@khayyam.h/teaching-machines-to-teach-adaptive-tutoring-systems-powered-by-generative-models-1cbc84e4e3d8](https://medium.com/@khayyam.h/teaching-machines-to-teach-adaptive-tutoring-systems-powered-by-generative-models-1cbc84e4e3d8)  
2. Position: LLMs Can be Good Tutors in English Education \- ACL Anthology, accessed June 16, 2026, [https://aclanthology.org/2025.emnlp-main.885.pdf](https://aclanthology.org/2025.emnlp-main.885.pdf)  
3. Personalized language learning with an LLM chatbot: effects of immediate vs. delayed corrective feedback \- DiVA portal, accessed June 16, 2026, [https://www.diva-portal.org/smash/get/diva2:2043379/FULLTEXT01.pdf](https://www.diva-portal.org/smash/get/diva2:2043379/FULLTEXT01.pdf)  
4. ITAS: A Multi-Agent Architecture for LLM-Based Intelligent Tutoring \- arXiv, accessed June 16, 2026, [https://arxiv.org/html/2604.24808v1](https://arxiv.org/html/2604.24808v1)  
5. LLM-Powered Tutoring Solutions \- Emergent Mind, accessed June 16, 2026, [https://www.emergentmind.com/topics/llm-powered-tutoring-solutions](https://www.emergentmind.com/topics/llm-powered-tutoring-solutions)  
6. \[2604.24808\] ITAS: A Multi-Agent Architecture for LLM-Based Intelligent Tutoring \- arXiv, accessed June 16, 2026, [https://arxiv.org/abs/2604.24808](https://arxiv.org/abs/2604.24808)  
7. Scaffolding \- The Bell Foundation, accessed June 16, 2026, [https://www.bell-foundation.org.uk/resources/great-ideas/scaffolding/](https://www.bell-foundation.org.uk/resources/great-ideas/scaffolding/)  
8. \[2501.15749\] LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System \- arXiv, accessed June 16, 2026, [https://arxiv.org/abs/2501.15749](https://arxiv.org/abs/2501.15749)  
9. Scaffolding: Right support, right time | Evidence to Action \- Arc, accessed June 16, 2026, [https://arc.educationapps.vic.gov.au/learning/sites/evidence-to-action/9965](https://arc.educationapps.vic.gov.au/learning/sites/evidence-to-action/9965)  
10. CAHLR/OATutor-LLM-Learner: Open Source Intelligent Tutoring System w/ BKT (ReactJS and Firebase) \- GitHub, accessed June 16, 2026, [https://github.com/CAHLR/OATutor-LLM-Learner](https://github.com/CAHLR/OATutor-LLM-Learner)  
11. Adaptive Scaffolding for Cognitive Engagement in an Intelligent Tutoring System \- arXiv, accessed June 16, 2026, [https://arxiv.org/html/2602.07308v1](https://arxiv.org/html/2602.07308v1)  
12. Cognitive Load Theory and its application in the classroom : My College, accessed June 16, 2026, [https://my.chartered.college/early-career-hub/cognitive-load-theory-and-its-application-in-the-classroom/](https://my.chartered.college/early-career-hub/cognitive-load-theory-and-its-application-in-the-classroom/)  
13. Worked Examples: Manage Cognitive Load and Simplify Complex Concepts \- Eduaide.Ai, accessed June 16, 2026, [https://www.eduaide.ai/blog/worked-examples-manage-cognitive-load-and-simplify-complex-concepts](https://www.eduaide.ai/blog/worked-examples-manage-cognitive-load-and-simplify-complex-concepts)  
14. Providing Corrective Feedback in a Foreign Language Classroom \- Digital Promise, accessed June 16, 2026, [https://microcredentials.digitalpromise.org/explore/providing-corrective-feedback-in-a-foreign-languag](https://microcredentials.digitalpromise.org/explore/providing-corrective-feedback-in-a-foreign-languag)  
15. Schmidt, R. (2010). Attention, awareness, and individual differences in, accessed June 16, 2026, [https://nflrc.hawaii.edu/PDFs/SCHMIDT%20Attention,%20awareness,%20and%20individual%20differences.pdf](https://nflrc.hawaii.edu/PDFs/SCHMIDT%20Attention,%20awareness,%20and%20individual%20differences.pdf)  
16. The Output Hypothesis: From Theory to Practice \- Hawaii Pacific University, accessed June 16, 2026, [https://www.hpu.edu/research-publications/tesol-working-papers/2017/2017-new-with-metadata/06pannellpartschfuller\_output.pdf](https://www.hpu.edu/research-publications/tesol-working-papers/2017/2017-new-with-metadata/06pannellpartschfuller_output.pdf)  
17. Confirming Correct, Missing the Rest: LLM Tutoring Agents ... \- arXiv, accessed June 16, 2026, [https://arxiv.org/pdf/2605.16207](https://arxiv.org/pdf/2605.16207)  
18. Spaced repetition and the 2357 method \- Exams and Revision | Birmingham City University, accessed June 16, 2026, [https://www.bcu.ac.uk/exams-and-revision/best-ways-to-revise/spaced-repetition](https://www.bcu.ac.uk/exams-and-revision/best-ways-to-revise/spaced-repetition)  
19. How to Use Spaced Repetition to Boost Learner Retention | Maestro, accessed June 16, 2026, [https://maestrolearning.com/blogs/how-to-use-spaced-repetition/](https://maestrolearning.com/blogs/how-to-use-spaced-repetition/)  
20. Spaced repetition \- Wikipedia, accessed June 16, 2026, [https://en.wikipedia.org/wiki/Spaced\_repetition](https://en.wikipedia.org/wiki/Spaced_repetition)  
21. How we learn how you learn \- Duolingo Blog, accessed June 16, 2026, [https://blog.duolingo.com/how-we-learn-how-you-learn/](https://blog.duolingo.com/how-we-learn-how-you-learn/)  
22. Benchmark of Spaced Repetition Algorithms, accessed June 16, 2026, [https://expertium.github.io/Benchmark.html](https://expertium.github.io/Benchmark.html)  
23. Bayesian Knowledge Tracing (BKT) \- Emergent Mind, accessed June 16, 2026, [https://www.emergentmind.com/topics/bayesian-knowledge-tracing-bkt](https://www.emergentmind.com/topics/bayesian-knowledge-tracing-bkt)  
24. Exploring Knowledge Tracing in Tutor-Student Dialogues using LLMs \- arXiv, accessed June 16, 2026, [https://arxiv.org/html/2409.16490v2](https://arxiv.org/html/2409.16490v2)  
25. Bayesian knowledge tracing \- Wikipedia, accessed June 16, 2026, [https://en.wikipedia.org/wiki/Bayesian\_knowledge\_tracing](https://en.wikipedia.org/wiki/Bayesian_knowledge_tracing)  
26. TutorLLM: Customizing Learning Recommendations with Knowledge Tracing and Retrieval-Augmented Generation \- ePrints Soton \- University of Southampton, accessed June 16, 2026, [https://eprints.soton.ac.uk/500710/1/2502.15709v1.pdf](https://eprints.soton.ac.uk/500710/1/2502.15709v1.pdf)  
27. Intelligent tutoring system \- Wikipedia, accessed June 16, 2026, [https://en.wikipedia.org/wiki/Intelligent\_tutoring\_system](https://en.wikipedia.org/wiki/Intelligent_tutoring_system)  
28. Input hypothesis \- Wikipedia, accessed June 16, 2026, [https://en.wikipedia.org/wiki/Input\_hypothesis](https://en.wikipedia.org/wiki/Input_hypothesis)  
29. An Adaptive Multi-Agent Architecture with Reinforcement Learning and Generative AI for Intelligent Tutoring Systems: A Moodle-Based Case Study \- MDPI, accessed June 16, 2026, [https://www.mdpi.com/2076-3417/16/3/1323](https://www.mdpi.com/2076-3417/16/3/1323)  
30. Instructional scaffolding \- Wikipedia, accessed June 16, 2026, [https://en.wikipedia.org/wiki/Instructional\_scaffolding](https://en.wikipedia.org/wiki/Instructional_scaffolding)  
31. Expertise Reversal Effect and its Instructional Implications, accessed June 16, 2026, [https://my.chartered.college/impact\_article/expertise-reversal-effect-and-its-instructional-implications/](https://my.chartered.college/impact_article/expertise-reversal-effect-and-its-instructional-implications/)  
32. Beyond the AI Tutor: Social Learning with LLM Agents \- arXiv, accessed June 16, 2026, [https://arxiv.org/html/2604.02677v1](https://arxiv.org/html/2604.02677v1)  
33. Weak-Link Optimization for Multi-Agent Reasoning and Collaboration \- arXiv, accessed June 16, 2026, [https://arxiv.org/html/2604.15972v1](https://arxiv.org/html/2604.15972v1)  
34. From Prototype to Classroom: An Intelligent Tutoring System for Quantum Education \- arXiv, accessed June 16, 2026, [https://arxiv.org/html/2604.24807v1](https://arxiv.org/html/2604.24807v1)  
35. Exploring the Assistance Dilemma in Experiments with Cognitive Tutors \- ResearchGate, accessed June 16, 2026, [https://www.researchgate.net/publication/226963584\_Exploring\_the\_Assistance\_Dilemma\_in\_Experiments\_with\_Cognitive\_Tutors](https://www.researchgate.net/publication/226963584_Exploring_the_Assistance_Dilemma_in_Experiments_with_Cognitive_Tutors)  
36. \[2604.15972\] Weak-Link Optimization for Multi-Agent Reasoning and Collaboration \- arXiv, accessed June 16, 2026, [https://arxiv.org/abs/2604.15972](https://arxiv.org/abs/2604.15972)  
37. LLM-driven Effective Knowledge Tracing by Integrating Dual-channel Difficulty \- arXiv, accessed June 16, 2026, [https://arxiv.org/html/2502.19915v1](https://arxiv.org/html/2502.19915v1)  
38. Enhancing LLM Problem Solving via Tutor-Student Multi-Agent Interaction \- NASA ADS, accessed June 16, 2026, [https://ui.adsabs.harvard.edu/abs/2026arXiv260408931E/abstract](https://ui.adsabs.harvard.edu/abs/2026arXiv260408931E/abstract)  
39. AIdeas: Tutor AI, a LLM powered adaptive learning platform to help students catch up, accessed June 16, 2026, [https://builder.aws.com/content/3Au7vMH5cU5S4xpbFmRVLZve3NB/aideas-tutor-ai-a-llm-powered-adaptive-learning-platform-to-help-students-catch-up](https://builder.aws.com/content/3Au7vMH5cU5S4xpbFmRVLZve3NB/aideas-tutor-ai-a-llm-powered-adaptive-learning-platform-to-help-students-catch-up)  
40. \[2605.16207\] Confirming Correct, Missing the Rest: LLM Tutoring Agents Struggle Where Feedback Matters Most \- arXiv, accessed June 16, 2026, [https://arxiv.org/abs/2605.16207](https://arxiv.org/abs/2605.16207)  
41. arXiv:2207.03025v1 \[cs.AI\] 7 Jul 2022, accessed June 16, 2026, [https://arxiv.org/pdf/2207.03025](https://arxiv.org/pdf/2207.03025)  
42. Bayesian Knowledge Tracing, accessed June 16, 2026, [https://www.cs.williams.edu/\~iris/res/bkt-balloon/index.html](https://www.cs.williams.edu/~iris/res/bkt-balloon/index.html)  
43. Investigating Recast and Metalinguistic Feedback in Task-based Grammar Instruction \- Academy Publication, accessed June 16, 2026, [https://www.academypublication.com/issues/past/jltr/vol02/03/20.pdf](https://www.academypublication.com/issues/past/jltr/vol02/03/20.pdf)  
44. Corrective feedback: 'Prompts' better than 'recasts', and 'recasts' better than 'ignoring error', accessed June 16, 2026, [https://www.ncca.ie/media/1868/effective\_language-teaching\_corrective\_feedback.pdf](https://www.ncca.ie/media/1868/effective_language-teaching_corrective_feedback.pdf)  
45. Types of Corrective Feedback \- CARLA, accessed June 16, 2026, [https://archive.carla.umn.edu/cobaltt/modules/strategies/c\_feedback.pdf](https://archive.carla.umn.edu/cobaltt/modules/strategies/c_feedback.pdf)  
46. Strategies of Metalinguistic and Recast Feedback during Oral Interactions \- Redalyc, accessed June 16, 2026, [https://www.redalyc.org/journal/3057/305752034001/html/](https://www.redalyc.org/journal/3057/305752034001/html/)  
47. Worked-example effect \- Wikipedia, accessed June 16, 2026, [https://en.wikipedia.org/wiki/Worked-example\_effect](https://en.wikipedia.org/wiki/Worked-example_effect)  
48. How Duolingo Predicts When You'll Forget Using Data Mining | by Rohith R \- Medium, accessed June 16, 2026, [https://medium.com/@rohithparambil/how-duolingo-predicts-when-youll-forget-using-data-mining-2abab0a921f4](https://medium.com/@rohithparambil/how-duolingo-predicts-when-youll-forget-using-data-mining-2abab0a921f4)  
49. duolingo/halflife-regression \- GitHub, accessed June 16, 2026, [https://github.com/duolingo/halflife-regression](https://github.com/duolingo/halflife-regression)  
50. A Trainable Spaced Repetition Model for Language Learning \- Duolingo Research, accessed June 16, 2026, [https://research.duolingo.com/papers/settles.acl16.pdf](https://research.duolingo.com/papers/settles.acl16.pdf)  
51. Tracing Minds: A Comprehensive Journey Through Knowledge Tracing Models in an Educational Platform | by Alberto Riffaud | Medium, accessed June 16, 2026, [https://medium.com/@alriffaud/tracing-minds-a-comprehensive-journey-through-knowledge-tracing-models-in-an-educational-platform-d734cd8577af](https://medium.com/@alriffaud/tracing-minds-a-comprehensive-journey-through-knowledge-tracing-models-in-an-educational-platform-d734cd8577af)  
52. Parametric Constraints for Bayesian Knowledge Tracing from First Principles, accessed June 16, 2026, [https://educationaldatamining.org/edm2024/proceedings/2024.EDM-long-papers.2/index.html](https://educationaldatamining.org/edm2024/proceedings/2024.EDM-long-papers.2/index.html)  
53. Node-Sampling: adaptive multi-agent optimization in medical education \- Frontiers, accessed June 16, 2026, [https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1758333/full](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1758333/full)  
54. Best Structured Prompt Formats for LLMs, Ranked \- MightyBot, accessed June 16, 2026, [https://mightybot.ai/blog/best-structured-prompt-formats-for-llms/](https://mightybot.ai/blog/best-structured-prompt-formats-for-llms/)  
55. Producing Structured Outputs with agents \- Microsoft Learn, accessed June 16, 2026, [https://learn.microsoft.com/en-us/agent-framework/agents/structured-outputs](https://learn.microsoft.com/en-us/agent-framework/agents/structured-outputs)  
56. Why structured outputs / strict JSON schema became non-negotiable in production agents : r/AI\_Agents \- Reddit, accessed June 16, 2026, [https://www.reddit.com/r/AI\_Agents/comments/1qeetme/why\_structured\_outputs\_strict\_json\_schema\_became/](https://www.reddit.com/r/AI_Agents/comments/1qeetme/why_structured_outputs_strict_json_schema_became/)  
57. LLMs suck at generating large, structured data. Tips on how to get your AI agent to do it reliably \- DEV Community, accessed June 16, 2026, [https://dev.to/aws-builders/llms-suck-at-generating-large-structured-data-tips-on-how-to-get-your-ai-agent-to-do-it-reliably-3mop](https://dev.to/aws-builders/llms-suck-at-generating-large-structured-data-tips-on-how-to-get-your-ai-agent-to-do-it-reliably-3mop)  
58. A Multi-Agent Framework for Code LLMs to Learn and Improve \- OpenReview, accessed June 16, 2026, [https://openreview.net/forum?id=pY65QWWFlm](https://openreview.net/forum?id=pY65QWWFlm)  
59. The expertise reversal effect: cognitive load and motivational explanations \- PubMed, accessed June 16, 2026, [https://pubmed.ncbi.nlm.nih.gov/21443379/](https://pubmed.ncbi.nlm.nih.gov/21443379/)  
60. Individualized Bayesian Knowledge Tracing Models \- CMU School of Computer Science, accessed June 16, 2026, [https://www.cs.cmu.edu/\~ggordon/yudelson-koedinger-gordon-individualized-bayesian-knowledge-tracing.pdf](https://www.cs.cmu.edu/~ggordon/yudelson-koedinger-gordon-individualized-bayesian-knowledge-tracing.pdf)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAZCAYAAADe1WXtAAAAfklEQVR4XmNgGAWjYMCBLBB3AzEHugQlgB+INwOxJroEpaAciqkOzIBYBV0QGfAAsSQZ+BEQJwExJwMWUMEAUUAq/g/Er4A4noFKgBuI+xhwuJIcwALEU4GYEV2CXAAycCEQe6BLUAKkGSDpVARdghLACsRCDFT0+igYBQQAAC92Ft8h9ZYxAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEoAAAAaCAYAAAAQXsqGAAAC7UlEQVR4Xu2YS8iNQRjH/5Ii11wSUYiU5C4l8aUoRSRFLiU2Fl8sFCnJxoJSiI1IVq7ZKWHxxYKwklIuhUQIWZCSy//f8453zpzzvdfvsJl//eq8M+88Z+aZeZ55zgGioqKioqqoD5lFhoQdBaQxC8iksANmdyTpFbQPJoOCth7TMLKdjAo7akgLWE4+ktPkBTkPW0iehpKL5AlsbBfZhEanaK4vyTtygZyFfccnMjN9rWfVm6wkD8mVoK+qlpAfZHPyPILcJ2fcCxnSwvfA5uUkB2z0np2jfns8I3O9d9queeQOeUAWB31FNJt8JVdJX699BWxBefpMpgZtu2Ena0DyLEfpuXIUhLnAGS4rHfNp5DpZB8sJRbUB5hCFgy/nwLw5aexj2Pc7XSNHkIZfLUetJm/JJTKd3CJvyE40J70yUjjKzhbSL+hrJe1+lqPyFvcIaTgdg+Wsu2gc5xw1gawnh8gUFFinkuRlpJP8QOaTL2g8slU1HpZf5LC806XF1XHUDPIKqbN+oTlSZEPJXmwlneQ72Y+c+S0jC8lt2KmSp6VFpL97qaJOwG6XHShm6xTqOUrjFQ2jYTlSSVr2TiLbCS4H6vTlStdxmESryp2ioiHnVDf0npJx3rM2R/Z+kg6vPZRqLt208kGuZPBA2FhSk2F5SeXCqqCviLpL5rq6v5GBQbuv4Wg9/10wm9oE6TgsDagMcXIbIXIlYwrDKnI3nSsL/DqmjNzO3kRjqLrQyEq4Om3OGb7GkNdI+1wNdfjvG6l9pZ5MKS9VCTvlAuUhOSlrEWWk4lChsjZ51mWjvCOcdMF0JfiXjZyscf5clLdUrbsctY2cQ7oRrqBVDZZbmXeg9W78D2lBe2G3rkLxHuzan+i9I0eodNmXfHbSzyndYLqY9Pkomn/+yP5B8hz2M+c9SlTmCpWq4dIujYU5SvmjzNzklKWwsWvQ/UmXffXPQfaNGPUvpX8PbsCKvCLULV6joqKioqKi2q4/qeCmfqvxxtMAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAZCAYAAACPQVaOAAAC4ElEQVR4Xu2Xy6tOURjGH6HI3RG5RERSckmIMBDFgFwGlJmJiZk6ykAm/gFFUhIyIDFASeILJZGBQpmgXJIQxYBcnqd3rbPX9+5v9+1vOy6n9q+e7HU5+9vvep/1rgWoqfnXDKLG+05Hf2qY7+xrbKJeUKephW4s0o/qpg76gb/FSGoZNQOWmSI0byk12Q+Q+dQbak1ov6b2Ul09M+z5EPWQmpT0t0ST21mkU0ZTb2EZ+U79pIY0zTDOUM+oo9RFam3TKHCAeo7s+06GvjvUy6BH1EdqfZjTFvl9JXWPug2zRVWUBWVjYNI3m/oRxiJ63pG0hbJzmRoc2o2goaG9OyiizN9EiYy2QkEuhgWt4LUInaKPUSYXJH0qHOpTVoR+5xi1qmeG0aDeUbNC+yosmFh49lDbwrOQG0pntIg51BXqCbUVzVlqx2qYddPVVmYU7PHQHkXdRfOCCI1r3rrQ3gfbCvFdKlLp36ggDUjav8VM6hz1Cpm1yuD35xhYENGC2oPai0XBxnnTYHtalVYuO4Fs4WXhSvZtx3DYCu9CZ1kWI6gb1OakT0F+Dv+m+GBb4Y8ZFcNT1AfqfpxUBWVAL1XB8dkqgxbmCPXV9c+lPqFasIuQFSW57QLsN/RbOsLGZlPLMRVWQGTf7ejMwpGYgffIF6KyNvbIJZeQFSVVdDlE57nQb6rGlEb79AG1AZ1bNkW2VYGbF9oTYZVeFBUo2VHB6tbUimjfWJT2I78dYsUvRCsSK7COnSpHjucWNT1p68jQ0SH0sWeRv0Q0kP/4FH+mygl+/uHkOccEWKAKuDeYAsuoMpTqGzK7iS5Y4ZI1I9rbW5J2JG4J/426lHxB853ZX1T+KPFS4ZVeFiKPqWuwrMuS8YjxqChd952wLOsdO0NbC5266b9CNWEFLNiNbiyiC8l5arkfCCyhnsLuA3JUn0bW1XXRWzhFizYO2R26EL1ER0EZ6b9jNTU1NTW9yS/uj40KskGeAAAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAaCAYAAAAue6XIAAABMUlEQVR4Xu2UMUuCURSGT5RQJAQKidDqllNrtYqDkz+h1a2h1T8gDbY2tBTh6J8I6i+0hBA0KI1RYe/LRfA7XvFcP7og3Aee5ZwL9+V+5zsiicRmswVLsKAbkeDdh7q4jEs4hT3d+Gf24QX8hFeq52UHPsBf2Fa9VfCymi4aGYu780fcQ5nC5uEE9nUxkDsJCFuGu7poJGrYI/gubmYaqmchWtg9OBAXeAQf4XbmxGqihW3Cc3gDv+Fptp2BK60Cq0p+jVtPnXIdWjCFncFXfYIHujHHGXyFb8oP+OWpU24KC0FhzQc9RBsDwrmdwGNYFLegQ4galnPLQwx6L+7yEPKG5agMxYW9Vr0FuGNf4DPsiP2nmJEnLAP6bM0f0vAv58uuQ56w0anDri4mEolEQv4AiudIEzjOTeoAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAZCAYAAACPQVaOAAADAklEQVR4Xu2Xy6vNURTHlzwiz5BXSuSRCUmIKIlSHnlMlJkBExOpqwyk5B9QJJGQgYlHmEi5ZSAlA4WS8sgjIxEKeXw/9t5++7fu75zzuydd3Tqf+nbO3nv9fmevtddeex+zDh3+N0Olyb7TMVAa6Tv7G1ukV9IFaZEbSwyQuqSjfqCvYDXmSrOkEW4MmCCrkTNcGpe1F0jvpLWx/VY6YGUbvh+THkpTs/5KMG6VIr0FJ75I16Qr0kdpcMkiBOCTdFk6IZ2SvkkbM5sj0gsr5ncu9t2VXkc9kj5Y+bmmMLlV0j3pjoWot8tS6auV9w+rTCpOz/pwFicRDmzIxhLdUSkz9kUlWPnbVmNFq8DJJRacxnmfZnU4LP2SBrl++vLo48DCrF3FTQvOpMDtl7YXw38yp/aKNmKedEN6Im2zninYjDMWHPPQxwom6jh70EJGpJWjSOXPUJB8UNtmjnRReiMNc2ONaObseSu2CM4ultZZKDAEwmfSDOm5hUrL2FkrAk8Kt5W+rRhlIcJ7rfUqE/nPVt6zEy04223F/uNzazKIYHPImtcMf8yMtRDE99L9ZNQOVEFeSvnnWKhDmkxyhPYeC45ct1CsGkGQfCHzkA2pKJFtVy0UORZhmTShMK0HP3baQvrusPopnCDlOG54/qWFwoKzJ3OjCjhHf0qr/UBktIWApaLE+UuAlsc2gaXG1IZ9+kDaZK1Tthk4PN6Kd+Dsrvg9rfbO2E5wpmJXdQxBSt9UlKj8OJsXrbwIVsKPpwrMseMLRW/gXfOt/A72b56e7NduCxeKIbEPmPh3K1bK489UiqF39nj2vQdTLDjarCj0BiaDY1wVgdTjvOQzZ400KWuzVX5Y9bmZ6oCfI5nCTS2/M6fs6RPSxLj+IVITZz3YERRWB7un0vrY76Eo3fKdFgL7WNod29OkmcVw35AKBbed2bFdBffyzRbsVpaH/kLKX5JW+IEI19NnFu4DXIL6NQSKPd8oYEAR5Cyv+ndVgpdwntbRmPhMhw4dOnT4V/wG5w+DLWinI+EAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAZCAYAAACPQVaOAAAC90lEQVR4Xu2WS6hOURTHl1Dk/Yg8SuSRCUnIKyUDExIDyszExESKGMjEXPJKHiEDKRImUm4MJDJQHplw5RETUZQJ1s/a6zvnW77zfeceXN06v/p3z358++712GtvkZqa/80g1YTYGeivGhY7+xrrVa9VF1QLwpjTT7VTdTgO9BZEY7ZqhmpoGHOIxmTVCmkduXmq96rVqf1OtVc1pjHDvo+oHout1RYmt/pHfwJGfFVdU11RfVYNbJphPFO9VX1Q/VBtFIuSc1DVLdn+zqW+e6o3SU9Un1Rr05yOsLmVqgequ9L8D3vKYtU3aT4/RJlUnJrarH9ItbQxw8Dgp6rxqd2V5JmxK8kh8nekRERbwSYWiRmN8Tihp+wX2/SA0E+fe5/NdyXlU5xs+K5aldo3xYxxx+1RbU7fQOaUjmgRc1Q3VM9Vm6R1ChZxRsywCH2kIODUA6qj0uyUL2Lz1qT2PrGM8MhRpOanb6AgRadWZpbqkti5GhzGimhn7HnJjgh/43EhqhjsBk1TvRSrtGTZWckcTwpXSt9ODBfz8A7pHGU2yobzZ5YziLFdUlyZOT5k0pQ4EIjXzGgxJ35UPfRJVaAKsijlf0gYK8I3syHX3i5m7HWxYhXBwDKGwkLJihLZdlV1XCwIS1TjsqnloGqeFkvfLVI+hR1SjuuG378SKywYeyI/KTFCrBDdjgMtYC4O86LE/UsWLUttHEuNKQ3n9JFqnXRO2XZg8FjJ1sDYrdnwLxgjKhfFDAHSeVJjRjOevl6UqPz5Mw5eBAvBI16BuXaqXDkOa82V5jU4v/l71tktZqxnDkackuJnYbxTKYbR2GO579+YKGZorIxVYTMYxlMRPE09cg5nmmhH3VeNys0DrwNxj2QKd3PeOTF7/im+sZNJ3WLG5vFHRTS0qIhRlG6FPsCxvLi2pTYFbno23Dt4oeC1MzO1q4JjLquWx4EEz9MXYu8BKnqfBkdx5ts5jELHXV50hzdgEe7TMhqZflNTU1NT87f4CVs8jIz5zTM9AAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHQAAAAaCAYAAABmZHgNAAAEpklEQVR4Xu2ZSageRRDHSzSgROMS9wVRFImKW1xQRAQ1RFxJPAQiCAb1IgiKS0IQQTx4UEIwgiI8POjBPQfFg+ATxf0uiMJTEiWHIIoeVFzql5ri61dfz0zPfPPMwfnBn8d0v+7p6eqqru5PZGRk5P/FoZWGZin6HGnhYtUHqlNjxQC8p7ohFo40s0r1rOp51feV3qqe0XbVGtUyb5CAMb9WXRYrKl6SST8u+r4l/acGzhDrf12s2E8cobpIdabk5yPHBtU1sTDDcbFAOVF1QCxs42jVraqHVX+rHlXdVmmT6n3VP6ovvEECHvS41L+UPp4Ua/9X9cy7eGcpt6u+krIIQIi+S3VKrBiA41V7VC+qdqr2qg5c9B/TMC8sar7/V5k4jOtD1bFi455XfSqThc/czqkOlp5cr1pQnRTKGdQzYoM6KNQxqNNCWWSL1C+IEg4X+9AXYkUGxnqV6jPVR9I+4aUwBib4mKRsveqB5DnHYWJG4/tzwnB4uhs01h8iPVkuNmC8NIIRXxN7QRoWblZdmzznYHEsiLXl//vCtoBHdAVP3SHWdmuoKwUPeVv1Z6wQ+66NsTBhteplmfayC8W2EscNOhinq35UXRkrZLFRPLTyd051cvVcBwYnjNM37+iLr/S+We9KMYNi3K7h+ATVd6rfYoXYnDRFjgvEtq0UvJ0Fgoc7gxsU74keCBjuoaouXVFHioVQPLuJJ8Tazkt/YzjsXbMsCrhT9YPqDdXZoa4OvAxj1hkU40QPrIP53FYpzTvcoCSXJKGEYnKH3vjExz1ys1gy87Es9kb36Db4WPql/1lhO7gkFvaAfZWj0JdiWXobbQadl/LFep3qG5nOO9ygz6nOVZ0vNud4eGd8fyI0luIf2QYfvEvqQ3PpyoabKs2CG/IT1RWhro4hDcoclx7B6JP+740VbbCp03AhlDdxuer3WJihKSSRwdGPc7VMh/yUWQzK1sBe5qG27piVYyiDEv3og/5KYIz0z7Gny3j3beo0JJMtpcRDfYVxbMmBMdO0nLCcM7zDyu5qUE+GOD8+HepKaUuK2NtLYJuqi1Z3i0XJaLguC2YfntzQ8J5Q10SJQQnlhJjc0Yaz1yvJsx8NmmAP5axcCvsU5+T7pD15a8KPdLktqcu8MXYWBgskxfdP+mIBOryXsqYseooHxRrtVp0V6prwj2RB5CA1f131pkyuyEhG1qo+F3vnXFUOGP3b5DniZ+G2Gyau5naI7Y9DXSoAXsVtFd/lkJHGbJXvQk8lZQ6GyRkULhW7CHH8dOEXD62QRf0ikwG4KC/lMTEvTGEVxj5zYrVjXIdw2+ShfhaOIem/hIyTxUjOcb/qJ5n2fIzys1g2G+E4Mi/14ZOE7VUxI3LmZo563xT1gT2wNNw04eG2bq8FPPiPWLgf4FoRg3In3fWCYoXYjw1NrFHdIZYrNCWISwKr593q7yyQLBCKMNp5Mt0fXsldMve5I0sMYScXXrqAITEohiXxiWH1HLHkpuQumHBG2Iq/atTpEWs24rBh+889RZt3DbQ9KhaKJQbvyOJkZGSJwRhcEd4YKwaARCImHiMjIyMjIyMjg/AvuoQJLfd2uWwAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHQAAAAaCAYAAABmZHgNAAAEm0lEQVR4Xu2ZXahVRRTHl1iglGh+lKKhiWahZGgqhkYPKomWooKBPRXks4pGEnFJfPDBiDATCSRBKPEjkT6QoCNGivoqF8TgJGkYiBj2UGK6fs4e7px19sfss8+xB/cP/nj3mj1z9p41s2atrUhNTc3DxeOJuk0vxqwp4CXVSdVE29AFflQts8aafJ5X7VbtVV1O9E1yjT5VLVE96jsE4MyLqnm2IeGADIzjxdgrwptymCJu/FW24X9ihGqWaqqkz0cM9NugesU2iItIMxINMW3RjFatVL2n+k/1oWpNondUP6nuqs75DgHsoG2qQbYhgTF2iOt/J7nmt/jNWN5S9UtvIkAZxqquqb5UHVNdVw1uuSOOteLmmfkOeUz1l+rrRIw/tOWOkixVNVXjjR1n7RLnlEdMG7v5GWOzbJXsBRHDcNUZ1Re24QHCM7B4xwS21apNwXUMRJyr4uYjdCi7luj1XGCbq/pc2uc8ClYHD2xXDTDgIXEP8VRgf0O1KLhOg8XRFNeX+zuFY4EV2w1YoC+ovhd3lBRB6PtWdds2iHuvddaYwx7VV9LuUI41bBZs260xhsmqP1QLbIO0OsWHVv7dp5qQXGeBwwkvjM1vdMow1SmpnvWSYJ1XnVa9bNqyGKf6TfW3bRA3J7GRgx3HfBGyQ4fyTo3EZsHGRmPDlYLdY3cg4LgtSRvJiecJcSG06IdYXfRtSHVnMBGdLgqek3xgv2qaaStitjhnZjmU3VuUwBCyuQ+sQ/2CyXLoBSmXc9zHT7yN1++LS2Z+kdbd6Hd0EbxEx2HDwATMscYCRolLykhmPjZtsRQ5tCH5i9VvCv/7ZR1KG/dE488nQmMs/iWL4IF+l+zQXLSyQ15PlAeTRwl1QlxE6bS0CKniUHbmd6qFga3nDuVQp2PT2POYr/rHGlPIC0mk5IzjeVXaQ35IjEOpE3FmU6olYSFVHEpJR5TzuQf03KEc6nQkk40lZofykoxL2ZIGzgzrLMJymuM9fFwocqiHc/KI6m2pWMtJcVKEg7Joqv6UgQ826F9x/W6JC8NFSVFDshdMGz65oeN605ZHjEMJ5YTxtNKGUHgwuPalQR6saGrlMnwm7jj5QNx52gm+pEs7korm7UlxC8KLOpQMm37sXiIK+E1lwUZJE81mcZ2uSLnsz78kCyINzo7DqqMycI7xVeU11Vlxv7kvsQNO/zW4tvhauHS2F8Bz9IurP6lDwzBYBDkAfXkvD2f1J9I6Du+Fdga2EI4U79CPAjs7kKNiUmDj7+MSGWFmivvM5B/AC3ssfeJ2YQg7yI6ZJlY7zvUQbvN2qK+FyzghDRYV9SeTSj1a5tPdi+IWIznHRtUNaS/bflbdVC02diCq2XkIwzWL5pLq3UT8zefGBwZnYF64icWH26yzFtjBnD3dhIjUZ40F8EEdh/JN+mnT1g1wOuO/qXrWtPUcQsEPyb9VoKYl6cBphEI7HruSb8l8z63pMYSdtPBSBhyJQ3EsiY8Nq9PFZYfdKkNqcvD/S4CqFPH0HWmN4r6wUJiHyUhNj8EZFM/LbUMXIGW3iUdNTU1NTU1NTVe4B/SDExPKutoPAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAZCAYAAACPQVaOAAAC2UlEQVR4Xu2Wy8tNURjGH7lErlFuKRFJSiRElESRS24DZUZh8E2kKAN9Jf+AIrkkZGCCQknKVwYiGSiUlEsumZDCgFyep3cte+3XPufss+noq/3Ur866nHPWu953PWsBtWr9bw0k43ynU18y1Hf2Nm0gr8h5MteNRfUhe8hhP9AJbfMdBdIClY1Ug8mopD2bvCMrQvst2Y/8HH0+Qh6SCUl/oTS5VYm0Iy34BnlPXhawM8wbQj6RS+QYOUm+krVhXDpEXiBb39nQd4e8DjwiH5H/XlNph5eSe+Q2bNerajq5SzaRdWQqbLHXyO5knoJVkEIBrEnGonoCmivtDUQp87dQIqNFUpDzYUEreF9mZbSIHPedsMz1T9oKYE7SLpIqRMFE49lHtmTDuII2MtpIM8l18oRsRn6RrTSLrHR988hE11cm2G6YOcXMyaTS78iQ+iXtv9I0coG8IYPcWFkNh22cl4LVJqyCGYxK2VfSZPIc5rQaO4Ns41XClcq3lYbBdlhnrp0sz4C5aVGpKdiNru8nOYDmnuGvmZHkHPlA7sdJVSRj0Y9qwXLZdtUNuy6UoTL6DNvUSX4gkaohmpKq7TLM5JSEhWR0NrWc9GenYOW7FdVKeAx5jLzBtJI25gdZ5geCdCSuIqsU3b/aIJmipKzLY0pL5/QB7Npop2S9tGAtXI7qq0KL2kW2u37dqSrlomtIiuUbTekgLNjUtHT2m0p/Hh1Y1443iirSNaGFn/YDsPPaA3tQDEj6tfBvyDLl5e9U/bYP9mjy+Q+NhwXazBSqSBltFKy0nIxN2joq31FsZtGU/Bp3kC/Iv5nV13HpbCnYE34gSAuXGWkz9OB4SlaHfi+Z0k3fCcuyfKErtHWXT8mGOyf9scxC11Yj6V2+HvYqWpIf+i2V/EWy2A8ELSDPYO8BPYJ6tZRpuXlRxqNkpHL/+IZuKP2I7tMyjAjfqVWrVq1a/0q/AFw5ewJksFpNAAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAAB+ElEQVR4Xu2WzytmURjHH02Kxq/MRLNC+ZGSZqeGlSgblJWys2AjrCjZycpiaspmSpOFDX+AkoXY2mpKbMTCAlnYKPH9eu5b5573Pfeea7ibOZ/61H3Pc957z3N+iwQCgf+ZCtgVWWXFfKiHDXahRR9sE/3Wu9EB58Wv0Z/gDdyBm9FzeaxGMp/hPVy0AxHshG14CZ/gM/wVq5EBNrYfHsMeWBYPO2mEf6W4l+9ERzeJOtFR5LfZ+FKJDsFrOGOU8b18P2OZGIUncA92W7E0RkQbacOyabswAVeiLGPswSirhkeSYVQr4ST8A1usmC+r4k6U09gXV6KDotOVs6YAl9OBeLyfa2JOdEqsW7Gs8GOuRA/Eb40TV6KE7TXX/FfRGeiq/wr/dCGaKJ//hULPfnSiJrXwUHSUU/kC10RHdNmKZYEdtS/5JcpR/Q0f4ZgVS6QGLogmzeTfQh5TtwDbegsH7IAv3JA4nTck+6aUtBltif8x5ZPoKfxu/OYxmBlOi3F4LnpZ8GVC3ImmNdwkrf4P2GqVLVm/M8NRYG9xR+ahngTrrki8d5tFjyxzp+Q56EqGa52xn1J88WgSHUnGbXklzBU29ArOwil4JnptM9kVveb1GmWFy0Aphz3qdEZ1cqVddOpzKvM5kBdcU988TVufgUAgEHDxApIKddAybbbQAAAAAElFTkSuQmCC>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAACpElEQVR4Xu2XS6hOURiGX6GIcisHiUMiEcmtXCIZUMiMMpGBS4mBciKZyFDJZaZkIEkxFEl7hFDKgHJJ5JKBRJko8b6+tf699jpn/fuizsR+6un8e+1v7///9vrWt/YBWlpa/mdG0PnO0dG5MobTVXRsfCJC916GivefQCfHg//IUPqFXqOX3Gf9+DKG0E30M+w6/b1FJ4VBsPsfoFed3+mFQkQCXbiOPqb3YV/YlB76HDajIV9hM5BiGL1C+6LxmfQj3eiOx9AHdHMnwlAFLIzGkijB5bCElbgeQF220N/xIGxsTzwYoPLL6DkUH7Sq7S3yxPzx/k6EsdhZiwX0Nn1Bt0fnyjiJdKIqxxSj6B1Y3PFgfAP9QOe5Y1XMa/oTxYlQ4hOD41rModfpLjoyOpdCyaQSzdC9ceyFxck1dC59RvcFMZrt0y7mIZ1N19M3QUxjjtH39BC6NxVffk0TFdPoXeQJv4MlHaOq+4U87knxdD20Hs7Tg7DSKiMsv5gqia6gn+hOehZ5Empk2kaEZnSbi5sKqzgfN93FVGYGvQjrdirbOjQtXf1odesjyJuRZvIV7NobbmwRbNtRssIn/o2ecmOV0Lp8Sreie5mm6NaMLiO9dakja5a0nYRoltQU1WnFGfqIjutEGJrxDOkH+Rd9ue+02lqabCueHUgnGu+RITqnZAZ6eTmKPFFVTIb+CSmHgcY7TIElmXrSddF9TsD2Y08vbCmEFfIDxeT1hqYuqkY03gfB1q0a0mp3PAu2pMI3IV++OjeoqClp79Nr2m7YOgt/vLgJW1crg7Fees+N69oM9vro34o8S2H31DI5DOu4LwsRg4j2N71sqJT1uSpaNto/dd1a9H+V9Kg6/P2XuOMWofpWA6hi2b9NLS0tLS0p/gAcrIk9KL5n7QAAAABJRU5ErkJggg==>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAWCAYAAACFQBGEAAABtElEQVR4Xu2XzStEURjGX/lIISWRImVnJSllxYaSKLGzsFSSJdkoWdpbsPIf2NlYjGyUhVmwksJGFlKSonw8j3PPOPPOde/VLEyn86tft3nf907N4x7nXJFAIBDwny5dADWwFVapei3sUDXC2hBsk9J7vKIdbsE33RATwg18hodwB57AV7juzJFheCZmhteL4rYf8Gl4hy/R9bO4/Y0NjT0rw12G1c7cIHx0anwSGV5/YcIzGmFOfg8tDwd0w6EXPsBTVeeyvoM9qu4F5YY2KebenKrze1kfV3UvyBIal98E3BYTEpefZVWSQ1tQdS9IC+0SXsMNOAKvxCzFzmgmLTT2vSMptDjs5vARfS4nNG5G/L6s1pvb/p+/htYEj+VnvpzQjuBtRvmE819ERZAU2qaYnXHOqen5tI2Afe/QIbjYM9o+rItqPAzzr27n++CTlB5mOcfAeSTxjm4xJ3iG4O6KZAYewJbosz20cnbFDoEpMQdk++rE6xocLUx4gl0+cdolxR+/BO/hHjyX+DcCzi3CXTgbXfmm4fX7ZxpcatNwDDarngvDnhcz16B6gUAgEKgQvgD4WneoXhTDTAAAAABJRU5ErkJggg==>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAWCAYAAACFQBGEAAABz0lEQVR4Xu2XzStFQRjGX0kpivJdbJSFFVKkRMpHEhuWylJJKYrs/AlSNij/gVLXRhYXOxZWsmHBgigpxUY+nqeZc8/cOW5uUsedO7/6Nee8M6fLc2bOmSPi8Xg8+cEKrLOLmnLYBIvsDgNe2wWrYYHV5yQM4wW2W/VauAPv4S58hLOw0BwEeuEZ3NDteXq3m0xKNLQyeABPYZWujcM3uBAMAh3wScIgeQMYXltqhGOUwgSck2hoe6IC6jZqZA1+6uNmUbOPwZpUwjvYaNVzHj53FuE6bJBoaNff1MiShKGN6uNkqlfBm8H6sFXPebisjmG9qIe4HRDP7RoJQis2jpPmAAlDm7bqOQ+X34A+/k1oDOan0NjvDJ2wwjiPIzRuTfi72cqZHRsMa9+qxRHaIbzJ0is4oi6LBz683yX9j7oV9U8+6PN++ZsXAfudgNPcnvpD8FW3wVLgHu1DVIAmWxKG1gKfJbqZrRG1FeGWxEm49egTFRrb4BOIb9ULeCRqo0v4LOTsW9XnZEzUzA2uY7ss4UvGOYKlZhssq1Z4CU/gvKid/zYs0f2EIc3ATTihW96AvPj+zAQ/i3pEBcJNcCYY9BQclPRQPR6Px/OP+AK1H4CTGD1RCwAAAABJRU5ErkJggg==>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAWCAYAAACFQBGEAAABmklEQVR4Xu2XvytGURjHH0kpisHPIqUMJqRIiQUlsbAblUwM8jdYZET5D5TBZngZGUyyMLDIIKUYyI/v1zn33nOPt/u+Rd23p/OpT+f2nOe+w7dze58jEggEAvrp9AsejbAH1vgbDu1wBLbAKm9PFa1wE775G5Y2eAAf4CF8hCuw2m0C4/AC7tj1Mr2tA56GD/hq16/09g8N8Biew2Zbm4fvcC1qAkPwSZIgeRoZ3kDcoYx6WJDioR2JCWjUq29L0t8r5vQxWJcmeA+7vboKskK7hS9w0KuvS9I/a58L8a6Bv8v6tFdXQVZoDCwrtFrnueA2SBLakldXwV9C47ulQuO+OvIMjX9GHFPKlSe7IsgztBN4V6Y3cMa8lj9Zof3HHwH31ZEVGme0Tzjh1fck6e+Dz/J7mOXQzFGEI4k6usRM8AzBvyJ1wCt4KmbQJcNiTt9W1ATmxAzI0dWJ6wacjDuUEH0+xXQ/qX54Dc/gqpjJfx/WOT0MaRnuwgW78qah+v5ZCp7AMTGBZF3sGfYinJJ0qIFAIBCoIL4B/KZ7o2/Px6gAAAAASUVORK5CYII=>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEwAAAAaCAYAAAAdQLrBAAACxElEQVR4Xu2XS8gOURjHHyHXECG59BFKFkSUEiWssEBRNsqChRVJ2VtYuCQrKVnZyGWhLKQvK2FJ5FJYELKgyCWX/88zx3u+451535FvPun86lfvnHNm3plnzvOcM2aZTCbzfzBB3paf5dmkbyAZKmfIcWlHF3DOIjkn7Yjg+pPNn39Q0tcRTj4pv8shSV/TcPNb5BvZKx/I67KnNaSS8/KlPCMvyd1ycNTPb9oYc1G+la/kOqsZuMXyvZyVdjTMJvlFbjd/gLHyqrwnp7WGtYWxt+TEqI1r7Y2Od8m7cnpxPFs+l1/lhjCoW7aZv9XRSXuTfJPnrO9Mn2c+4whGGcPlZbk8aT9unjk8G1wojm+YB5hn7S3aOL8WM+UnuSztaBBunHSKmSKfyndJe0wYQ6bE7De/5qnieJRcKccUx1Plk2IMqVoLUoATD6YdDVIVMGZfGaGklAWM2cMsTCFF6SftmXG14aaoF6wgneBtba5pp8JaFTD6yugUsF7rW2pI8x3muwPSNsy4Wow3L5L8AVuMgVgxmwpYgG3FTfOiXyslWYEoquQ3deyFDcyK2XTA4ID5mNdpRxksrex3yOMR8or9YRH8C1QFjICU0anoh2uyimK8N1tvPqbqhfxioXwmr5mnJLAEh7dSxXxr/VG3jvx5ZjmMSQv0AvMVkv1TGdRTXvjqpJ3VkWvuLI7DfVC/Ahuj9kq4+GPzAhhDYT5hXVygH2CTST1htw98hZw2TxdeEITgcH9zizagrPBVEK92zMpj1lps2KQelcOK40nyjvm1DhdtbQkbtqVJe2CN+Y33JO39DQE6JD+Yb2/4vOHTZVU8yHzGfLTf69Ij8yJOluwxDzYBDiyRD+V9ecQ8jVkp95n/dyWdPmzpb7d3aQI+XdiGrLAuHiSCsZxDwDi/HdQvat1Wudb6BjSTyWQymUwm8w/xA8utr5l1IlLyAAAAAElFTkSuQmCC>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAZCAYAAAC/zUevAAABgUlEQVR4Xu2VvytGYRTHj5EJKSllMhj8KCyyKAaDiRgYWAzyH2CyohilxGBjMRj4A5SSxSyKRYhYGPh+u+fpnvd08ep9bhnupz69zznnvm+n53nOe0UKCn5mGG6W4Xr4Qp5swG1Y5QtgGl77ZGzq4Bmc9AWlGx77ZGza4APs9AWFTez5ZGy4A5+S7EigATbqegCumFp0wlGwiTF1ET7bh/ImHAWbuFFf4Yd9KG/CUXA3Ar3wwsSEU8MJoj2uZpmBrbBJP2tLy9lsSdIExzPQD3dNTEZhvXqkcRYcZf4efZfskS+B0/AC3ySZgO/gztyamE3eSfY0LfvEb9ijsJPhGZGk0QAbZsy8Zw3Own245GqZ8EE2cQBrXM3ylyZOYIeup2CzqVUE3y88tgCbeISDJhfok/Qe8HLumFpFcIzvTcwd4Fgz73mC7bpmE5ymKFTDQxPPa8z8AjyXdNvnJN0JXuAhXUeB/w3jcAKewi7Nr8Ir2KIxX/u8mPRSyhjRgoJ/wxc9JEtHBzyzYAAAAABJRU5ErkJggg==>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAACYUlEQVR4Xu2WPWgVQRSFT9CAEknESIKFkECijYj4g4WpUkgKE0sFhYiFdmqljZ3YxE6wCUqIIAhJGw1i8YidWCpaKBjBwoiIhRaKP+dwZ+K8Sebt7Aa0yH7wwds7s2/nzszeHaCmpmY9s4nucW6J2opop/vp1rjB0U07otgG2hbFKrGbXkLeoPXQT3SGTrvfGnwRGugxWP879C29T7uCPuIK/UknnY/pd7ox7JSLBjtMn9HDyJ+tXvoStqIhn2Grm2Iznacv6PYgfp7+oiNBTIk+gCWp9p1BWymOwx74iO6N2ooYo7/jICymQaU4QL/SOTRP0ijs3ptBTInKymhWz9Ip2h+15XId6US1jVOcwup9/AQ0gljlRPViX6Qf6K2orSwaaCrRBtLvuAbeKtHFIOYTnYBt39NYWZxWoA7vYIkWdi5ASTRQLVE/QbmJKkHPIF2CVeOWqMMN2IpejdrKoIlSBayS6G3kJxrjJ/hkFE/SSS/Dki6cnQT/YuvG6LMyi+aClYUKkrazvmVli1KrYnQP6c9Uqhgdot/oE3d9EJb03eUehu6L781CH3hthTeww0IufsAxirWqlEP0B2zrh7XCf16m3LVf+Y/LPf5uXU3ymtAq6NCgipw6lnnU9xqsv6cPNtDwdKTtGCev6qkTzwl3rRPRgtOfjnpgq3vUXet5Z2D/VelktBa0Iu/pBXqOvqbbmnoAD+kXeiSIaSJUDBXXznhKn9OBoI/YR1/BKm8DNjmqK/+FXbCtrwHrdxl0pNN9KkQ6iq6GJmUctrV7o7b1jfb4jkyL3s+ampqamhR/AGWghmhECrL3AAAAAElFTkSuQmCC>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEwAAAAaCAYAAAAdQLrBAAADEklEQVR4Xu2WS+hNQRzHv/KIyLM8yuMSCQskiQVlp5BQXgv/smAjC2FjYSPJzoYUQrKRKI9IurFQLGy8kgUSRRJFHnl8v/1m3DnjnHPvuf9H0Xzq0+3MnLlnzm9+85sDJBKJRKI76UvH06FxRxN60zF0vvstoj+dQkfQXlFft7IANsmuQpNfQ9/ROn1Cb9Ja45ZSHsPGHaH36FJkA6KF2AH7/xf0F31KFwX3dCtHYQ/eRAdGfe2win6nHbAXHUKv00d0bOO2XGbDFtCj8Z/o8qBtJz1FB7trzfuHU8/uURSwV/QcnY72Uv0nPUv7BG3TYBlxN2iLGQTLLGVQyAlYwP1iKqPkrj93ACtdmxaqKXqpYei6baUJr6AP6G1U/19NXC8Zolr0nH6M2kMUYAVaY332iDvIBuc1LJvCrFuGRiCbsgW2qkvc9QC6lT5ztosWYh4scApgvPJFlAVM8yxDQdD4D3QdLBGuwLa1R8Ve2RiyGTZOWdyUS/Qzneuulb7HYJP76m/qBFPpSdhW7ch25VIWsGYZoEVS9vhskUqAMvxW1r2Hsl35KDA36GG6O+rrLAqWAlXlQOhMwGbRPbAsUoYp03wgwpoY8p5epcPjjiJ8sdPvG7oezVelDNUsnVSqX9qOrW5FT7sBG0nvI/s8naoao52i77KYybBEafl9lY46dufA0rkGe8Bl11cVTVZBugarX/rPqpQFTHMtYi3yS8g+2H+qToVMoA+RPZQ051J0XOuoVnH06Fqn0Ux3PSnoK0LbbRvse2xi1FcVvZzqqraVR3PRnLQYRegkfBk3wpJBgQ4DNhq2qB1BmxLkfHCdy0G6IWrTpOqwP9AXd9He91SpT62wHVa49WyhrD1O39IZrs0HUMHt59r8B662WYjqs776/VbVqalxedbdPbnoJfWAOCM04W+wbXkr6usJ9GL7YSf3XnoBVlsXB/doMc/QL0GbUOZo7urTe5ymB5CtUXGQQuNS8BdFdUrto1C9YHcl4+hquhDV5lGDffdthH2QJv51VOhb9aIbk0gkEolE4r/hNwovuOF0wQtMAAAAAElFTkSuQmCC>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAACOUlEQVR4Xu2XP0iWURTGT2RgZKkIVpSIg7qJYNLgEIS4hWMNQdKig6CTIoibS22CCEJJrrraEA4fNCq4FEbQUEOQTg01CKnPw7kvvp7v/XPf65b3Bw9+3znn+7773D/nvYpEIpGIyF3olg06rkL3oUfutS9t0A0T4+evmFgQvdA01GQTOXAwC9AR9MTkyCD0BfoJHUC/oafiN9hZ6B+06rQt+jsN6SJfOEOPoV3oofgNgLCOJrmKNehE6o2yht87lIpNitbuQ7dT8Sxo9L2oyXGo43zan1HoM/QB6jM5X7jyNck2yhzjNfeacIX/QsfQsIvlQaNUMNehl9Aa1GVyVSkyyhVlfEXOttsA9MfFbb0l2CgP9hT0C1o2uVCKjJKbcv44cBW5mjRL00UkRl+Jbt/nUt+c6mDBD1GjpcUVKDNqocGvUKdNZECTNJjQLdrQ2BsKYcFr0RWdN7lQqhiluU/ubwjJbz0z8VzYKWdETZfOTgm+RptFHw93bKICPOeb0JJNlMGGxO38RsKbko/Ra6JbcCMV46PsXuq95QH0HVo38XdOleEguBW+iV4WqlJmlM/pOVGj7PaEK/NW9FGTB88nv/MwFUt+azEVC4LdkTPNjtxicnlwVfZEBzVhcoQ3G+asdqBWV8MJSuLJZLVDH6ER955jG3M1QTeji8AtZA2kHxvJhSFLW1Cjq+sUbVK8Kva4GOl3Me6Gmuiksa/8l/BovRBd6bIr4+WCe5z/SvnI93xGIpFIxHIKpoB32wrCTA0AAAAASUVORK5CYII=>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAaCAYAAABIIVmfAAADfklEQVR4Xu2ZS6hOURTH/0IReeeRt0TeA3RLpGRiIJJcpUQGJkYUZULJAGWAKMXNQCJ5DEQxuElRJiYeAwaUhCjCRB7r3zrbt7/tPPbZ3+7cj3t+9e/ec9Z5rL3X3mvtfT6gpqbm32ewaKSoj2uogL6i0aIBrqE3MEN0X/RTtA8aiKrhO/lu+kBfZjeby9Ehuig67Yjn2o05oveiF6L5js3QXzRJtMQ1BMDZNU000DUkzIL6Qp/oWxDjRetFe0S/RGeTY6rd2An1ca9rSOgUfRB1i86I7oqmWPYysPO7RJ9ECx2bDX2hT/StJdaJ3kAj3q6YQcK/aXwXbUGjLtwRPRVNMBd4ME/0BPoe6ivyA1DkkxfMad1o8SE5LILmynNopLjdorWiUdZ1ReQ1dqXosqifdY4pgjPioWi4dd6Xl6goAMbRpa6hRbhaYEc/E61wbCHkNZbnGGCbcdBO/Cxa4Nh8qCwAm6APYT2IyS5oGhjhGgLJayw7PysAXK1whpSlsgAcgz7Enr4xYNqZ7p5sAdPYtIKXFwDes9qx+eATALMwCA4AH86XfHMNCdxshK61N0M7IUtjoMvGPFhQueFaI3ouWt5s/kNPBYAwvb6G+lh6c7gd6uBj1wB90HHRxuR4JvQ633z6UfQqRz7PGiY6KXor2gCtK2n0ZAC4T9gK9fGIaFCzORt2cBfUwfOOjUwV3YKOVMJawU7zXbkwuLGgrz9EN0VDHRvJK8I+nZiGz730hT7Rt1Ijn7Aj2aEMQFpnHYDWBwP/vwD/WnEN2bvIEE5AfTUz0maV6Aaav89wdnEFVGbQ2PgEgL7QJ/pWmsPQmx+hkbv4l9v469C9gZ3/ue1ebB0XMRm6Bt+G7NRRhqIVB0dhp3XM2W1/JjAB4TMemIsyYF+8g9ZGrqCy/C/yKRXbkTztMDckhIyksdAN0j1oPm+FosYegnbYQejIZAfa+w8OJs5gLks5mNKw64artJlQ5FNUWCdK5znoPXSejf6CRoP46WCZdV0RPo2dCP2OxXqVtcLirpiDIgY+PkWBTps6wbV9rM1VGWI1di7+LtihxPKpEH6u4KcK1oj9iFtcfYnRWM7Go0gv5CHE8Mkbdn5WMaoC5vBL0AYzl4f8IsUfdIa4JwPgu69A68kpZKe7/w4OgA7oCu4q4nRmWTgQb0N9YG0LqYs1NTU1Nb2Q32wn4xMFuoKFAAAAAElFTkSuQmCC>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIoAAAAaCAYAAABo4cQnAAAD/ElEQVR4Xu2ZTahNURTHl1CEJC8SJSJJMvAtRvQin8nQzIC5kAy8iZSReBlIvSQpERIZGFwUSjEhpdQlMhBKUcjH+t19trPvfudjn/fonvPe+dW/9+7e+3yts/Zaa+8jUlNTU1Pzbxgfabgwxm+oCeOOaqbfOISZodroNw4HTqlOq26rXquuRr+tulWj/45uZ4lqud8YsUN1XtrPhba6g0rMWNVs1Qi/Q3mh2u43DnW2qQ6ofqh+iXnBVrtUv1WPxMwkl4linCvJkDBfzDk4/qfqaPS7yx1UUtaqnqgakpxWd6qey/CKpC02iHmhTa8desX0XVCNctr3iIlAeVhHm+R3lBCe6aPqs5j7bkiyozBJHqrOSLtNhjTjxEQGDENk8bkkpu+lamrUtkVMlFhnB6UwXcyxjK8SmyXbUYCI+UHV47UHMUU10vmNYcteJZOH34lJPau9PmiKMRqRhTSD+lRvpH868sGRODfXqBIhjjJBdU/MmEJQ2L1SPVXNVe1V3VV9VR2S9IKw0zDb/YhhwSnoo3iz+ZgUQiohChGNsjgi2cYuKyGOAmfFTIRgqJAJ0fYC31WHo771YsI0+W8gUPxRcLpFZp4Wto4Mg5fJPXP/br4lDx9U3Zf2yGEjEEbKgkh6Q8z5/zU8n//MWcJ+Xa0jwwh1FFI1gSCYVWJmJiHZz8mEc8I6s5K0xBqcJekxZ0wnIc+y2smrNyyLVV8kuZ5xsZEqLT3xAnCmMtok1FHsuMI8k/45ebfEF90vZi+BCDRHtSwe1jG4t6aYwjOElapvku8oJ8ScO6lGsxGYc5XRJv/dUZhpbu4mlNtVA4bDkZZGfeAvOTtBUtrJIiSiYNyGpBsRB+GaOEcZbRLqKGy6pT1jJhzk5uRZYlYHzECM468UkgpIH1ICqYFzh+pk68h8KEwZT9QLxToKewhp2KUj9+1DUX9R4msOxCY8n//MWSqSWiHUUZgsjCsExRIH9Uq8W/lJdU7iCMOqaFr0P2BwDN8JSAn7VG9V87y+LOy+S9omGkXwZTG2uBK1UYewdUBhT3ufxDYqk00sLDy4zweSXmPZbEFELARFK7t1DTHr62tilsjusrgMRlkk8c6jK9roC6FHTMQgcrjYHd4sMbtxGEsZbGKxkcRXQ/pHFmq6ppjAUAjCEGKmTJbk8OkbJcnYVcAWtEVSVhpVtQmpjG0Q1+lzsXsGeXnwvbTPWsJWkfV9WaAIva665XcMgCrahGBAJCGDkGqDsWEob4n5WGIP5GLHo79VZI2YGmywVNEmC8R8EC38DcvdBcwLm3hgt+SPqwLUX+yBDPbzRJVsghPflIKRpMZs82/yG4cwKyT/G1dNTU1NTU1NTWX4Aw3DEUAAjOaQAAAAAElFTkSuQmCC>

[image22]: <data:image/png;base64,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>

[image23]: <data:image/png;base64,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>

[image24]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANEAAAAaCAYAAAApFbmYAAAFnUlEQVR4Xu2bW6htUxjH/3LJneO4ho7j8oATIkRoh0JyyfGg44F4oBwvlNsLigdPpLyITh6ko4QQSlrx4MSDPIgXdcglCVEUcvl+xhr2WN+cc88159przrns8at/uzXGXGuO8c3vG+MbY8wtZTKZTCaT6Z7dTbv4wjXGrr5gjYEPdMa+piNUvKn/vCgcYHrRF1YQ+36YK9/DfV5EzlDo31oFP9iqOQ+mD5m+Mv1t+sH0q+ku016mDaYTly/tFB78/abtps9MX5h2mJ5MdPN/V0+C4V433esrHARO2vevNdn3t5YvHQy0rYlDtAmiZzVpZ/SS6ar0ogFxoOl00wkqH/TfM92pZnabCh7GI6bPTTcqOB7sr2DENxWcd924vGswxkWmTxWc/GXTtWNdp/BgfzddHr8wBkMRCATcelcXiX3/U5N9h7TvHyTlfRPt8aGaBUWbIMLG2Ae7YyM+X206OL1oIBxu+tb0jIKPfK9iCnu+wiB8liufCW78joKRcCgPzve+Qn3f4My040pfYVxq+tK0MSk7WcGoBFoZad8fdHWQ9v1xV9cXzJK05+fx3yZB0SaI4D6Few1pIPEw+JEtHJKUbVaYdVJ2Mz1nGqmdLQq8omCc51U+9UWuUYjqvqGtI5V3/nqF+suSsp2qdn4GjCZ97yuVreIKdRNERyrYsWrwGgJ7ml4z/eErFNqNb6Qwi36sEEwzww1+NG3yFQ4caeQLO4YRhPY+7CsU0rZtpk80uSHA9bS9jFvVrO9NnW/edBVEF5v+Mn1jOtbVDQXWsyxFfvEVCjZ6ypXhL6TqO115Y3A2bkA04qArcbbpAl/YMYyIfqaJkN8SEEzfKaQ8p7oyoO8E3KL0vYyugohBa6UMYAjQLwKoKoiYpZitUu5W+czVCNYJqzlFM0XGxf60asJ5Ko6GpGGXKCwUf0rKgeBgdGKU8qx23z2MdOeq2N+V5DdF6ugqiHDAqgygDW1tsw9frqAuiEYq9jvarzUxh3zXtJ+rA7YJcT6vvojtrVrflIHRRuO/KfG3MGBZ3xeFroKIe7Bhc5SvGONH+D5oE0TxO62JDob8j3Oo+LTC6E4DENvHLMT6gtmHWajJzMFuzUjF/sW+T+OArJtuSz4vKdjBH8T2QZdBVJYOAZsz5ySfl9SPbXoJImAvfaTij6ewK8WiksVln7AOwhhNFrZVMxGw0JzGAd9QMHaElKbKobqmiyDiWu7BFncZBFB6LIJ9+rBN3cYCvu45U+Flgpm4RcXdLE/dVJ5CoMWZa1pNS1zcNnlAOADnSmX9i2uisroIufsTmtx4IIAeSD5XsbfpVRX7u5K++/eb09NFELGtXzWIsh7leCAS0+Q62tqGM78qWC9xRkRbPXwfX/fMvCaKsKNFqnaTJk92GV3uUbgJuxh9QZtYhNJO2uJPn+tg94UNiTLY0WPk2qLJ3+WB8IpQmUMQlNMMKPMGBybVxCZN2tMkiEiHX1B45zCeo2EnDrXjAfS2cTkQaNinL7ADk0L6xgk7q4+p/BUfBuZVOfs8ScsGwVHje1FsDbOIf1STOW+X4Mx+REJ3pBfV8JvKR6FI2vftprcV3nC4XeVvbwwhlfP2iBqpPkCmCaKYOteJUZ+AisRUt09OU3imHK7iJzzXsl29mOqTrq8KROkxCu9DkeYsqX9HWS12aGXHT/t+g0L6UjXb8RtVa4NFYZogakNM5YZgH870CCK2xo92dRGeM7PQVl+RKULKg7E2+YoWsKkR1wanqHymGjrzCiJsw8Ie+yyCbQge1vobfUWmyHqF6b0qL24CDoKzHK+wTpz19/pgXkGEbQgi7DN02xxq+kjFF1MzNWxWMNysHKRhO0gd8woiYPMB+wwd3kTf4Asz03Gh6t+T+79znKrXh2sBZkr+/SWTyWQymUwmk8lkMjPwDwopZRExj+5+AAAAAElFTkSuQmCC>

[image25]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAaCAYAAAAJ1SQgAAABuUlEQVR4Xu2WTSsFURjHH6GIFMpLqEtSlJfyAVjYSTasfAAW9mKhW/ItWFgoCykLxU6xotggCxILW6UsiPj/O3NzesydO0fMzL3Nr37dO885073/mfMmkpJS8pTBRtgKa616JayxrosahtyDH/ATPsJXmIHVcA3O5DonBL6QOl0sRAvcgbuwH5Z7dX6ewQP4DAe9etxw5C3DNzih2gIZgg/wRczb1ayIedOnsF61RQ2n0RZ8l+8RGDrsiZgbFsU/KOFQuZdkDWGuJYfiGJadL2CTbrBgWD6UXt0QI85hO8V0ntcNCoadErNIJQXnsLNi5umwbvgjGuCkmAcVxnEJv7U5hc113pT8czXJ/Crshqr7wdXP3stG4SVstmpR4xS2Am5LuLBZdb0q5vBRpepR4hSWcGHal+CFJwM7VI1Bs6rmBw8nT2L+UBjv5Odv5cM5LOHGfAsHVL0PHsFpVSfs366LEdMGz8WEnRNzbi/ICLwRc9M1XIdX8Bj2WP1s4h7CnHp6VNBQuwrPvzwwcPnnkAhaeBhySRdLlS445n3n0A+a70UPgzJwN1yQ4tyjneDJqORDpqSkpPw7X9lrX5T/agnLAAAAAElFTkSuQmCC>

[image26]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAeCAYAAADgiwSAAAAAo0lEQVR4XmNgGOpABV0ABhSBeCG6IAy0ArELuiAIcADxViCWRhbMA+L/aPgnEFuCJHmAWBKII4D4H5QtBsTMIEkYKGeA6MIALEC8Boifo0uAgDgQ3wXiA2jiYGADxL+BeBK6BAgUMUDsC2KAWAFynDBIAmbfWyDWBGJjIF4MxJxgbQyQIHvIAPHGKiA2g0mAgC8QfwTiDUDsiSwBA7DAGAXIAAD8ORoJ0Ewr5QAAAABJRU5ErkJggg==>

[image27]: <data:image/png;base64,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>

[image28]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAaCAYAAAAJ1SQgAAAB90lEQVR4Xu2WzysFURTHj1BECuVHUY8k5FdZWJLshBKl7LGQrVgpWfgfWFgoRcpCURaKFWWFLEgUOyllYSG+3+6o63hzDc9782g+9cnMmftyz9xzz1yRiIh/TwYshuUw34pnwzzr/k/DJLfgC3yFd/AZxmAuXIQj74NDJgc2etoLEogyuAE3YRPM9OL8ewx34CNs8eJhwjndwzW47F0vfBjhoBXewCcxq6uZE7PSR7BQPQuDcdhl3deJqcJ4c//AoZhEpsV/MPfutaRHCfeJma9mCo7poIY/PIEl+oEFk+VLqdcPQmBe4ifbK6akfakS88MJ/UDBZAfFNKmwYUJ+ye6Jo1lx2blP2/SDX6II9ot5UUHsEfenjR2YX4tvJ8vgHlwR/72abvBF7EoCyTrr3GMVFlj3nfAUllqxVPGjMs6C6xIs2Vl1zybBcmJZpRq/BjUgX1QpG9O2uBtPDFaqGBOdVbF48HDyIGZyQbySz/9Lw89fvGT56aFOeDS8hM0q3gD34ZCKE46v0MEUwZXjIafdisXEzIlndycd8ELM2zqHS/AMHsBaa5xNWCX8DhvVLZyEo2Lmz+NsIHjW5IGB7Z8b3dV4mOSMDoYAF2JYTFnz2nevJkI17PauWfqu/f7nYaJMuEZMQ0jKG00neDL690lGREREJJ031RFhLBJLGL8AAAAASUVORK5CYII=>

[image29]: <data:image/png;base64,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>

[image30]: <data:image/png;base64,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>

[image31]: <data:image/png;base64,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>

[image32]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAcCAYAAABYvS47AAAAy0lEQVR4Xu2Qrw4BUBSHr42NIQmCKZrGVJMIgmIawVPwBF5AlhRPYARNVMmi5AkEvnP/2HFtqs1827fd+7tn95wdY/58jTQm1D2HBXW3NPGEGyzjAo/emi5aYhLvOA4PHsm6cuj4QxavWFVFghROdVDBPeZVJmcp7KnMtHGuA+N+f+syw74OYIgr4+a3yGrW2AgBZHCLdZXZ+S448nfZ5wRvzwqPtJWhU1g0btF6+RZZy864oT8S2h7ihxjZnbQ9Yyt6e2GgLEVvv8kDyKEfWFhqzL4AAAAASUVORK5CYII=>

[image33]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAZCAYAAADXPsWXAAAA2UlEQVR4XmNgGDFACIi9gVgEXYIUkAPE/4F4ChAzoskRDa4zQAx5D8Q6aHJEAXEgtgfiZgaIQa+BWBtFBREgA4hZGSAaQQaADAIZSDQQA+LTUDYoLCYwQAx5BldBBIgB4o1IfFB4gMIFZBBRIAKItwExJ5o4zKAGNHEMwA/Eh4DYA12CAeItUFTfBmJZNDkUgMsVMGDMAPFSOboEMtgFxEHogkiAhQFiCCj9gJIAVgAyhAddEA38ZIAYBErNGAAUDiBJUjAoLcEBKAx2YFFECF8EaR4Fo4BYAADk0Do9uxfBmQAAAABJRU5ErkJggg==>

[image34]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABDCAYAAAAh8FnvAAAClElEQVR4Xu3czatNURgH4CWUGyWRjyiRlJGBomQgmTJAUeYMMDLwJxgjJZHMzbiZKLeUiRLFhEyUjGRkYsL7tva5d5/t1jn3yz2O56lfu7XWPp3pr7322qUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAONhZ2R9dxIAgNGwK3Ih8rIobQAAIynLWpa215FTnTUAAEbAnua6JfK2vQAAwPLLkraiNb4cmWiNAQBYgNWRL5FfkSeRQ/3LA20cEAAAFiDL2p3IvsiOyM9Si1vvadnhyJlZcqRZT0dL/c1seT5zGwAA8/Go1GK1rhlviryP3Jy+Y3jnIje6kwAALMxkqYVtWzPO4jYVeRZZ28wNK8ve4+4kAMA4uR25HvkeuRK5FDkeeVr+3nfNdke+lnpoYK4ulvoO3IMyUwABAMZKlp0sZvnE60NrPsdZhrr2Rj4PmTXNbwa5Vur/zeewwN3I2ci9UosmAMDY2R7ZEPlW6iGAnixQ+a7ZUsuy+Kn0//dc3I+saq4HO2sAAGNjf6nvkPUOAeRpzSxs+dRqKWVZy63Xrd2FOcinc+lW5Hx7AQBgnGQxO9ka5+cz3kU2t+Z6FmtLNEvhw9J/yGCpCyIAwD8pt0NfRQ4049xezOJ0evqOxZdl7Wqphw3yoEAmv8fWe1oGAEBLbiPm9uebUg8gfIwc67tj8U2VPz92m+mVRgAAWvJzGFmWVpa6BZpXAABGyI/Ii+4kAADLbyJyotSna/kO23w/qwEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/Hd+A1mGXadauJOwAAAAAElFTkSuQmCC>

[image35]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAZCAYAAAAFbs/PAAAAyklEQVR4XmNgGF5gNxA/AuJXQPwAVQo3KAfi/1CaIGAB4jVA/BuIbdDksAJpBohT7gKxOKoUduACxP8YILaAbANp4kBRgQa2MkDcD/K0O1SsFSoWAVOEDJ4D8U8gtkUSwxsIIIn5QMwI5YNoEB8k7glThAxAEulIfBEgvgrET4BYEUkcDJSA+DQQCyKJTWFAdb8mkhyDHxDPQRZggJh8nQESWiCMYgsoNKKRBYDgKxAvBWJmIC5jQPgNDHiQOVAAUiAMxSiKR8HAAwBOoyQQQpcK6wAAAABJRU5ErkJggg==>

[image36]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAnElEQVR4XmNgGAVDFnAAsSQa5oFidDEw8AXi/2i4HIrRxcAAZsN7qMRPIHYEYg0gvgPEt4BYnwHJBhgIBuK/DBBNIEV7GCCGmCErQgesQDyLAaJpMZSPFzACcRkDwt0gNkgMJwA56zcQb2OAaAA5ESSGFbgwQNwMchLIKbBAwPCHJhCHQCWeAbE7VLyTAeG0u0DsCcScULlRMMAAABO7KKyFjrTTAAAAAElFTkSuQmCC>

[image37]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAZCAYAAAA4/K6pAAABGklEQVR4Xu3Suy6EURTF8SWiEIlLIyQkaJQK8QKiJSIKiWRaiUaFVqPQeAKNSuMBFOIFPIBCMzQ6CUFBXP7L/sQ5x1z6iZX88l32PvtkzjdSR2cYoxgsC+0yjVNc4Bh13KM/6WmYbmzhTbEwzRxuq2vTvOMa42Whygo+cIWxoqYBfGK/LCQZwqWiby8vSQuK6b62ypFigAdl2cUjZnCoxoP8zn0e4N4sPrQbxWfzvZtKi5Wf5yz+7XeYUgyoKYalvHhdsdhfKssSXtTmMyk28oB68V6TisJGWUjSizNF30lR+44LbnBjo8ziueL7PxnBOV4VZ5CmT7HBjuIf2zTefRtP2MQqDvCAeXT9trZOD9YUp76Miaz6n07LF+mXPNEtviQUAAAAAElFTkSuQmCC>

[image38]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABACAYAAACnZCtBAAACrklEQVR4Xu3dTaiMURgH8CMUsbBQkmQjJcpCLGQhST4ihbK3UJJEsVGkZM9OtrKgbCTJ4hYbWVFSSknKQrJhQz6ex3mn+84792Nzx+3e+/vVv+Y8Z5qZ5dP5eKcUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADmvC2RF5EjkYuRnf3TAABMt4+Rra3xp9ZrAACm2YnI9k5tU+RypzY/Mq95vaAZ9+oAALPGlVJXs351J/6DpZGNkWWd2kjkQOR75E+THU0959uyYcv5J5GXkcP90wAAM1s2O9siXyNfOnPDdr3U7/1WasO1rqnnb7od2Rc5GVnZZHepTdmSyN3Iw+b96Wapn3G+jK64AQDMKtnsXO0Wh2hX5FqpzVdaXOpvuN+M15bB7c9Tkc2dWk82aq9KbQDb594AAGaF3pbi3u7EEJ0t9Ttz27Mnx+2LBfm63Xy9KeOvnuVt0jWlNmxvO3MAADNePj7jUeR05EOpW5Tr+94xHIs642zYXndqeXngUGRDpw4AMKfkjczfkUvNOG9n3in11uVY8sxbPhttsuwvo1uek1ldasN2rjsBADDXrYi8i6xq1Q5GbrXGw5a3On+Weo4NAICOXE3LZqm9PZm3N4+1xsP2udRLAwAAjOFeqQ1bz55St0dzO3S8c2wPyuiz0SZKNmITnT3Lz3/eGuejO0ZaYwAAwvtSt0R78uxaNmx5G/NGqz4MT0s959Z7ztrRyOO+dwAA8G8l7HhrfCbyI/KsjL/CNhUulMEVuUzWAQBoWV4G/3cz//ppYacGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATIG/FBphSbW63SUAAAAASUVORK5CYII=>

[image39]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAYCAYAAAAoG9cuAAAAsklEQVR4XmNgGBSAEYiF0QWRATcQzwPi00AshiYHBsZA/AyILYGYF4iVUKUZGFiBeBUQHwBiHiDWhNIoAKT7JxCXQ/k5SHJwMAmIfwOxDQPE0ZtRpSEApGA+EOsA8X4glkGVhoD/DBArtgKxK5ocGIDC5Q8QXwfiMigfA4B8cQBKYwUgrzcA8UI0cRTQAcSzGDAVCaHxweAiEFcDcSsDJEpAgYkBJIE4gAESTsxociMdAADJWhgFVgRa7AAAAABJRU5ErkJggg==>

[image40]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAaCAYAAACzdqxAAAABJklEQVR4XmNgGAX0BgFAPBeIZ6HhmUAsjKSOZKALxCFAvBSI/wNxNpTvDMSsSOrIBpMYIAYzoktQAjSB+C0Qf0WXoBQEMUBcexpdglIAC4Y56BKUAF4gPswAMTgaTY4igBwMgmhyIAASg0UoJwMkKXYBsTpcBQ5AKBhA4ixAzMMASe9iQNwMxD+A2BdJHQoAuQbkUlzBAHKpH5TtAsSvoGx+ID4BxAcYIBZiAORkZowmBwIgMXEo2wGIfyOkGBYC8UMglkQSg4O1DBDXgnIdLBylgTgZiD8C8T+oGDpwZYA4JhhdwhKIfzJADMWHsaVreSC+CMThDFTOpasYIOFNVQAqlEC+BQGQa0GpAxYHZAOQodMYICUfCFcB8TIg5kZWNApGASoAAC0SOpeUOWn6AAAAAElFTkSuQmCC>

[image41]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABaCAYAAAAFKQq8AAAScUlEQVR4Xu3dC6h8W13A8V9UYg97XSlD4/+/cS2sNMXM1MxLJGZaREWlCf1Nepj2ILmlFnXsQfSwwq6WFV0keksPxJSKmluCvciKW4Ia/Y0wLDKKDK8999c1686addbes/ecfebM4/uBxf+ctefMf2bP3mv/9m89JkKSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSBrx/V17RlZd15f2qbZIkSbpiD+vKzeXPH7D8+cF5oyRJkq7eJ3blncXv7+7Ko4vfJUnSkaAb7c6u3K/eoCvx4mWZ6pO78q1ht6gkSUeHi/vzu/KgesOO8TruX1eeqA/qyk915QPrDQM+vCu/E2k8myRJanhmpAss3VOHhi60J9eVO0aw9mNdubcrT6y2nbK/78oX15UN7L8vWf77vK586vpmSZL0oV15fFc+uivv6crnr2/ea9e68qK4+i40uvIYh/V/XfmVatspe1ZX3lVXVvjs6AYlYKP8dlc+Zu0RkiQpbu/Kc5Y/v6orb19t2msEA/9VV16Rv440UP4dkYI2ZjsqYb8QVEuS9D7cqX9FXXniHhHjxhHlDNWiK39U1O+zt8Z+ZLPYdz8TKUj7nkgB2+PWHnHa2D//WldKkk4TFwUGLDNw+Vh9W10xEvvlJ+rKBroXvyyuvntxjNu68vpIg9uv2lmsMmp5LJtLU6z7xTCIlSRFGtj86XXlESEQfVtXbq03jHA9UjZqCM+/D9mqsc668uV15RXg83hzVcd4NrJsZN2UfG6sspCSpBNF9qi+aB4Tgqk7Is2EvKfaNhYTC14T7YwUXabfF2nAN2tn/cL65r3zBZECojkzgQ+P1aD3oVJ3L78p2pkjugDnfo2Hjv3B8iuSpBPFUgrHfCEgO0FQQLBF0LWt93bli+rKzlMjXUxz2ffMEN1rvM45bRuwkZWs63BnpNf4KfWGA0CQ+bFduaXecEFMEFnUlZKk00Agw8XxmDMZZQaHoG3b4JS/+9+68gARCL22rrwC7M9WsAa6/gh8/zlSF+mh+IdYH1rwjzFuHbUxfj7mD7SPwaO68tNd+YSu/EFXHrK+WZKOw8u68jl15REhQCuzX5R7Iq2ZNhXZHrrqDn0cEfuALtyrxP6nO5RMVF/5wkivlZmjh4BAgdda3vwQlBJ0zuFbIu2PQz/+5kYb9oblz9ycbTu5SDoqL+jKv8T5BoNZdCzc2LJtNmMTskL/U1fO7FVx/r2ORaDA6vcsesnr/N5IF6Ead99/WVfuCIEaGaNjyK49d8YyhEDnkJc+IajYhxmYLH1SB9JD5RDQXhBkfn2sgs6nRFqX70OKx4GbBtqFn4wUvPIz2bkhHx8pY7cP32LAe3tppOOor/0oF5Bm3/QtKM23g/xdpH3AzOWnrW++zyJWbWj5XHwV1wcvf+b1nK02SaeJk5LA7HqsBx7U9w3GZrVtGpnLwF0rDXlfl8oceL/bvn5mJFJ4feyjX4u0Cn79etnGMgYMat81go99uRg+oStvjPR6uJiVx1Pf+Kjy65TOIi2+OkcZ8tSu3BX9F6l995hIAUTr5kGb0e322kjH6c2ufNiynvN3ESmQePdyO+X2ZX19fnP8cJP7u5ECsDHdph/ZlT+N9jjKXaMdY2wo7/FLq23ZmICN7BiBWv5mBhZz/rdI+7m2iHbAluW29Fq9QToluTEi20Tj8oBlPSctg4ZbwRqP5SS9DIxpYUkCVkXvG7Q8B9LrBG1TMH6FbrPWuBv2Ew1cnY2kodm2m+4iuHCTMb1q7Kty3M9tkfbTWVG3DS6md3Tlu2O+7/h8YFf+PebLcnDRe2VdeYnoLnp1bJ85PmWcn9woZEwq4DhlEgfYtwTEpYfF6hzj/P+tWA/eyK5P6SmgTZ27Xf2lOJ8BHIu2rm9R36GAjTab794lwGrd/LBP3lLVLWI4YPv1rjyorpRODReVPNi67OIk/czdZAsN1aKunAEnN+NEOOH5995oLwswBxpYLm5TkG2kEW81QmA/tsa00EDtel0sPrtNGaVdoIuRRp/Bwxn78KKv7Tcj3W1zMZprqQ2ei9dGpm0OXHjmvgAPuYwL/qn4zEjnKcuiZBwLOSDjRuNstel9aC/72kjaiL+K9AXvY9dAJCgkK7dtgNXyG3E+AzhWzja2DAVsZMfZlw8t6kp0jdbt6CL6AzbO849a/nxW1EsnhwaJE5NUPDOVMupI0beQmSoDKYKfr+nKJy1/57sXucNqZeeGEKTlZRM4mTmpCdqm4P8tC/LroTxyWYdbu/Lg4ncQLH5GVZfxehiLQuNRZv54rdQRAPKYnKXM2JcXDVCm4nWUn2eN7go+M147wfkPxnyZqhLrpH1HrF+EeG2M15mCjMeTlj/TxcJ4IiYK0L1Ct02Z/WC9tEVXPivSl2VPeV+8NrqT53CRgO2xkT4Tjt3cNTckZ8odlL0dzucfifUsDscCy21kT+/K30QKRL42+r/5gr+jcF5xDOTfN+Gxb495u7QvErDRPtLetW6ahwI2zm3e7/278hFFPagjOGa/lt2/i2gHbFwP8v6jzHUzJR2kfIH6/VjPgvxt9GegqC+DsZd35fsjZVK+oSvPizTo/XUx7euQWOC1bBzyWLYpXTzc0f5HpL/L3RE/uvydblZeV0ZjW2e+SOPz2LoLk9dAPUEsXR9cGPN4K8ZmMNCaIIjH1GPjqKerbZd4HX3BAp8zgQDZARpEuhu+K9L4ksuW9yN32VM8I1IQQ2NOw84Fk+OFz5TPjIaci24+Ljl2fm5ZN8XQfptq24DtSV35k0h/f3esZ23rG4yMm4Q/jLRfNA+OhXrRaQbBc7PQGhZxUfsWsHGu0iXcuoEZCtgIxth31LEURzk29Qdi1ZVcPu8i2gGbpCXG7HAHxZTy+qTmYt66Wye7wZ1XKT+Ok7TuUhh7weI56zs5MigEgXdG+052CH/H//+Ny5/7LtwEDvw/GXfYLyl+z9g/PN8iUnD7T5GCQwr7kIsq+4HH1LP06Bakvg8XAQJEGqxNZSz+v77Pj4wf47QIIvPnnjM09WufE8EU3co3YvrnmV/nXZH+9seX/4KAuQ7qCUR/OabdMCB/xnPYJmAjmC6DBN4XN0hkJTg/+rLWHBtc7L3YXRzHFTcBZ9HfblwGPmPa3TnPwYsEbCCLyFAPhs6UhgI2zqEcsLEgdW4nKcysz8dqeW4slvXwGJYayDYx+PO2ekPnP6N9wScj1brYEgAsYtU48BhO2tzFOeTjIq3b1EIwxfMQtE1BQ0sXKH+bu0ZbzqL9Plt4rqGuvDzmg7R/iQZoKGC7DH0BW5a7GrI8ZpHPsVbP4GyVp9336DaOB4LaMsM5BYEXmcoS+/kiF6OWbQM23l+9T8gm1BkGSt8YpZx54MJdoouXsU0cX32mBmx/dqDl9uh3Lc7v67pwnPbt/4xM8426cgfyObhtwPbwOP9+/zzSDU1ZR4ZwE45nXgszXAnYbq5tHQ7YGP4x1N7RBvCcZVuwCAM2aRBjCPrWnZqSYQPPU15QHxjppK27HFueH/1frp0Dv7JbaAwu8Fzk8t1eK8hEnWEbkrN2fci0tbbvU4Yto2uX4CCjK42/mZqRGouG/9OWP5MlIvM5BV24ZD+fHf2f5Ry2DdhapmbY6Nbl/+ccK/E5cj4+tqovTQ3Y1MYEgTy2iuPsq4ttl21fMmy87xuRZrzzc15XrzQUsN0Z6fF9/+9ZnD/OF9EfsFHPTfc3VfXSyeDOi4tgeXKUg7OnjGHLawjlhoZuHDI4XKRBEEDDkS/Ytbsjjfuqg5NcGDPGCZ4zgWTPyHT13SnSyHAHR4NDA0ygRalna/G4OqDkOXnuVlBAUHVPtNdVuhbt/wMEsmVwtAvsr6Fgod7OhYIA9zKQGXlirD7Pr4w0GWAf1fvlIqYGbDnDUmZoyQaxNMNQ8I0HRBrDxvAGbeeNkc7tfJySAfqLtUdcLo4Xgu4pN2abTA3YaPc4B8peCW5oadvKsblDARu+LlJ7Ut8Atp4fi2gHbLSdb1j+/LjYfB5IR4lZjZxM+QRg7NkfrzZPmiVKNxrjoV4U6YRk3ANjF3LQkzMHDGCtxxoRBLFtTGEWKfj/+J07vxop/2+P1MX6iEiBJeOdeDyB2O2xeg23xvlB3DkrV08cyK5FaryeUtRdj7Sv+roFh/blZeE9DM0SZTtBOTgWCER5b3PjOevPkTIlkNklXlvd9bqtqQEbNyJ3xapbmvOHgOFXIz0PxzLDB1q4KC9i/y9o3HSVk5v6PCTSpKVdoS2sj1HKonjMZbvqgI3j7QVxPtDiuKMngp6QbFPAlgOzsg2iJ4EsGcdzHcgtoh2wvbQr71z+zPYp55N0dLg4EOTk4CojILu3qssYa7Mofuciw8mZu/b4t4VZe2Mbj03IKAwFJJvQCPVlEMlwbOqW4DFk8Li4111YNYLXetDuZSNTkwOyGu9tEemzoBGc6zM5dOwHjmNuMOYwNWDLWAqBY6oc8H7Lsgzh/xr7/70j0nvdZYD3mkiD+adgPBTB2yngsyBY2jTGboqpAVvfMca28pjcFLBl/B29GLST9LD0TeJYRDtgy3gejp1r9QZJq7uq1qw0MlTlhaEeD9Xnh+uKCyBoJFDcFgFp3zcdMP5uUxA2Fg0NmcD6jvKyEaz1fSb1eEMlfO5kinOG66II0l9ZV14iLvhkc+tJL31YVmGXARtjPFsTnIawvMnUIO9QTQm4x6I7fc4AMBsbsI21iOGAja7qq/peZukgEJhxV9wK2ghoWCiXk4s7dYI2gqgWgpYb0X93tQ2+v/MiQRDBWqvbkzu4PGbiovJd4ZzveywuxnwutW+ONIHjO2O+TNKxYFgANwF1tvlQPCZSUDQ2I0WwtquAjX1bz34dgzal78bjmORxwK1gZR/tMmCjTWbYBs6KekkVAhu6/loYs/ZDsfoWAS4YLQR+T68rL+h6XTERjUw9ng4EcU+oK7d0lXeFDJhm4kX9HvNnRXlhte3UEeT2zZo+BARqLMfTdx7WdhWwEQATCJPBnCqPzRvbrXeoaHcYYztXdvey7SpgI1ijm5hhO3StluPoJOlonMXux84dqjxDsw5wDw1ZVQLPMeqAjbGnZLMI/B4aae2tRxbbWfj07q581fLnZ3flZ2NzkJEnJdWY1cpyMr8XaULR50VaA42B7yUec+zZYGb38tkd+vEnSdoC0/EPuYtvlwhcyEgeOt7D2OVZ6oCNpRieVfzO2ohMTgDDD8gA5WEEZCLPImXNNh1feZZ47SxWEz1YBghMJKq7QMm4ELQdM953ax9Jkk5E3wLIWsf3zuYFUw8ZS+eMvfCXARtjzPi7susxj09lvCoZSGZs5m5Nti1iXFdlfp4S4zoZG8u4tnKiRF5Wp8T/fezHMN+/uagrJUmng0kPb60rtYbsUd/kmkOTA69NWS+UARv/1gFb7ibmX+pZf5CsLW7E+CCKQLgOwjK6AsvnuRnnH3sKARvv2fFZknTi+JYBis5jmQlmVh6Tsxg3eaIM2PIklXLR1pwZI6AlA/bZy/KSOL9OIQHd4yOtw/ieWB843tclSuaO5WfKxat5XL2Mx7F3iTLOlK9zGhNkS5KOGBeCN4eLTrYwC3rO9QH3wa0xrruyDNh4LF8XVn6DSbk0DNvL8W01Ar4nL39m3cHFalPvpAO6Q+kKzK+Tb3F4S5w/TgnWeP5jRTd2ud8lSSeMoG1M1uWU8NVlV7FG3i7QDU43bx8CsbJkTDRgBiiTDe6IVTcxx89/x/m/K79yLWeIFrH+tXHMfCQoqZf1eHWkrB4ZTgbds7ZijWBuEcfRXd3CPmNdREmSdILIhjGRYht0i9K1WWJNwWfE+tfOsQZjq6uTcW88vsQaWvXCuTeXhe7Wsiu2dOwL59K1zHqWkiTpRNG1yHiwi46NygvfXq/q+Z0xaPn5GetGhq4PmTTGDGYEey8ufm/hq6lYo+0YEVS/q66UJEmnh7XT6mzXNlhM902x+hYQupLf1pV77ntEGvPGWCwCuFaQxRg5AkgmGTwnUsD28lh97VALXau31JVHYq7PRpIkHTiCJ5aLqAfyzy3PBM0lL4RbI8P2qLqygQDxdXXlkSATyWSXYx0/KUmStkDQxrIR96s36ErQDVx//ZYkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZKk6f4fnj25XTm5+oUAAAAASUVORK5CYII=>

[image42]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAbCAYAAACnZAX6AAAA2klEQVR4Xu3SvwqBURjH8UcoShmITAqbUS5BWUwGkzuwyl3IQGajxTX4MyALxWK0GCSTSeF7nIPjxQUov/rUe57nPed9Or0i//xqXAgh4mx8ih9V7DHFDGXRh3zNEEukzFq9fELRrDPwmedbgtghbRfJFhPR/YqjJzU05X2UkeiNWfTsRhgr5O2iSR9HtFC3G2pW1QjYRZM+zig56pIQPcKnTWPRB6qDX+JBW563puJGDgNcUEDS6t+ibueADrrYoIE41phj8XjbihovJvpPUF+6x4uo6f/zQ7kCetAh+9Rm7nsAAAAASUVORK5CYII=>

[image43]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAxUlEQVR4Xu2RzQpBQRiGP0VRFmJhY4Fs7JRSVjZchVtwG+7Ayg24BQtp9uyVsrFxBRbIzzMNp+nrzGyVPPUs5n3PNDPfEfktKrjFKy5UFySHc3xiVnVBunjGpi5ijNFgUeVBGnjBvi5CZMS9Y6qLGA/cYVUXaZTxJu4UO+LoxGq4wYG4d5wkMrEW7nGFBVyKO2Xif/Shg0dci7uSxY7XbjDvdcIQD9hWuZ3WTNymBPtzDPb80GOEd6z7YclfpGD7vA7/fI8XXVkeg7zZxLIAAAAASUVORK5CYII=>

[image44]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEoAAAAaCAYAAAAQXsqGAAADDklEQVR4Xu2XW6hOQRTH/0KRWygnoQ4it6I8KJdILkkkl1I8KIVSXhR5UCTFm3iTe0nuKTqRcooH4dEbHvGEFEqu/7+153yz59sz33bq6KT51b/TrL32+vasWbNmDpDJZDKZ7jKj0ODwQYSh1LDA1odqo/oHdjEAfxe/19GX2kVdpc5T76ijJY9qVlG/qOfUaeok9Ym6h3IyXHzF9eNXJbNXs4P64o2nUG9g1ZHCJcrXFWqE74RG/MXF2MXf1+XRw7SaiFaylc9q2ASPB/a91PbAFqJEqUJSpOLL3pKRKE8iHMdQue6GrdAP6jI1tuTRYCc1MzQGHIZ9sD7cp04S6vik4rdM1HxY6XVQ46hTsH3+gprl+YUokYdgvhuoudQFWNL2eH6OM7DGmkITjU2kE+nG6xI1mtoP61FacJ9UfNmj8XVK3Ka2wBw/wCatSrkJS8Io5xwwnrqI5pNmGvWEWoNGg5TvMaSrVKfQHcQn0onERGA+at4PqAXUJOo9tcTzScVPJmoptYK6D+v+U71nsew7BlJDQqOHkjSdWobmla1iEOw7qn6zTqKqcHM4UIxT8ZOJcrylHqIxcf3VWC8rSAqV+kHqHDUH8arRysb6lyO2ON1NlOtJqiRVbCp+rUT9RPkkUGWpwsIqC1lOfaSeUreo79QNVCfkCDUhNAbEmu1a2DaPLYJ4BkumFs7hTjPZlYRUfNlT8f8gJzk7NhW2S1Q/z+6j3qSVUhN36HZ8AtbQtTUd+gBdIH1bFe53daD4aGLh5EL0nk7eRZ7NVdA12DxS8WVPolWW0+ZirEl9o9Z1eVQzEenjfiWsCrTS2pp10G/rJP3s2dqpVyjfnGejuTKuU1tRroqvKN/M/fhqE6IdFv9sMY6i3tFBPYatunrTwpLHv0VNXR+tfzO2US+puyUPq2Zt+XmeTdv9Eez7dTVQK6i6mbv4r1GOH/o1oX2rktSKtaHeCdXTaOU3wr5rcjGug27/qja9tx7x92RX3Nrx3ZGcatgZWH/S1WB4+CBTRuXpNCZ4lslkMpnM/8NvFPSzzZyF7cYAAAAASUVORK5CYII=>