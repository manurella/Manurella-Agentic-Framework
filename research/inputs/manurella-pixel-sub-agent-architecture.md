# **State-of-the-Art Sub-Agent Architecture for the Manurella Pixel Domain: A Framework for Stochastic Visual Generation**

The automation of visual design, art direction, and high-fidelity image generation has evolved beyond the limitations of single-turn, zero-shot prompting. Modern generative models exhibit exceptional rendering capabilities but fundamentally suffer from stochastic variability, fragile prompt adherence, and inconsistent character or style continuity across multiple frames1. The Manurella Agentic Framework requires a robust, modular, and runtime-agnostic architecture to elevate the output of both frontier and non-frontier generative models3. While Kilo Code serves as the initial runtime target for this deployment, utilizing its native workspace storage, Agent Manager, and isolated Git worktrees, the underlying architecture is strictly designed for portability to Codex, ChatGPT, Gemini, and custom Python or Model Context Protocol (MCP) tooling environments3.  
The visual domain, designated here as the Manurella Pixel domain, encompasses a broad array of distinct tasks: art direction, image prompt design, visual composition, style systems, brand and character consistency, model-specific prompt adaptation, image generation repair, moodboards, references, multi-image continuity, and the evaluation of generated outputs. Addressing this scope requires treating image generation not as a deterministic linguistic translation task, but as a state-conditioned, iteratively refined action space where outputs must be evaluated across repeated trials6.

## **Mapping Competencies in Visual Art Direction and Image-Generation Workflows**

To construct a resilient agentic framework, it is imperative to map the primary competencies required for professional-grade visual generation. The generation process represents a complex orchestration of visual reasoning, technical model manipulation, and critical evaluation, where evidence demonstrates that monolithic approaches inevitably degrade8. Project experience within agentic workflows indicates that separating the creative intent from the technical execution is the foundation of reliable generation.

### **Art Direction and Intent Parsing**

Professional art direction requires the translation of abstract client or user intent into concrete, deterministic visual parameters. This competency involves establishing a hierarchical composition that defines the foreground, middle-ground, and background, thereby preventing flat or cluttered outputs10. Furthermore, it necessitates the deliberate selection of a color palette, the articulation of mood and atmosphere, and the dictation of camera technicalities. For example, evidence demonstrates that specifying precise focal lengths, apertures (e.g., f/1.8), and lighting setups (e.g., "soft diffused lighting," "dramatic side lighting") significantly anchors the stochastic output of models like Imagen 3 and Flux.1, moving them away from generic aesthetic defaults12. The competency of art direction also involves identifying whether visual elements should be embedded within the image itself or applied as separate overlay layers (such as HTML/CSS text), a critical distinction in production workflows14.

### **Model-Specific Syntax and Prompt Optimization**

A foundational constraint in modern generative AI is that no single prompt style functions universally across all image models. A high-performing prompt for one architecture often triggers penalties or hallucinations in another. Mastering this competency requires an architectural mechanism to dynamically adapt prompts to the target API.  
Evidence from current image-generation model behaviors highlights these divergent syntactic requirements. Flux.1 thrives on precise, natural language descriptions and highly detailed, hierarchical spatial layouts10. It explicitly penalizes traditional Stable Diffusion prompt weighting methodologies and suffers from specific hallucination triggers, such as the phrase "white background" degrading outputs in its \[dev\] variant10. Conversely, Midjourney v6 and v7 are capable of processing natural language but rely heavily on a proprietary, syntax-heavy parameter system. Optimizing for Midjourney requires mastery of aspect ratio definitions (--ar), style reference URLs (--sref), character references (--cref), stylization weights (--s), and multi-prompt weightings using double colons (::) to prioritize conflicting concepts16. Furthermore, Midjourney explicitly penalizes comma-separated keyword lists, whereas earlier models relied on them17. Imagen 3 operates under a strict 480-token maximum limit and prioritizes short, highly specific modifiers, requiring distinct API configuration parameters to control aspects like human generation blocking and text rendering13. GPT Image 2 relies on an internal reasoning phase prior to generation, excelling at 8-frame coherence and embedded UI text, but requires explicit directives to utilize web search for contemporary stylistic anchoring1.

### **Visual Continuity and Identity Management**

Maintaining consistency across multiple generations—whether for UI mockups, conceptual storyboarding, or e-commerce lifestyle imagery—presents a profound challenge due to the latent diffusion process. Project experience demonstrates that identity anchoring requires the systematic application of unified prompt constraints, often referred to as "Character Bibles," which enforce strict stylistic DNA across all generations22. Additionally, it requires the programmatic passing of reference images. Evaluating consistency in this competency requires stress-testing generated assets against identity drift across varied poses, facial expressions, lighting environments, and wardrobe changes24. Successful continuity management ensures that a character or brand element remains recognizable and structurally intact even when the background or camera angle shifts dramatically25.

### **VLM-Guided Evaluation and Iterative Repair**

Because T2I model outputs are inherently stochastic, generating the final asset in a single pass is statistically improbable for complex prompts. Therefore, the framework must possess the competency to operate in a closed, self-correcting loop. Following generation, an audit phase must occur where a Vision-Language Model (VLM) evaluates the pixel data against the initial textual intent. Frameworks such as Continuous Reasoning and Agentic Feedback Tuning (CRAFT) provide evidence that decomposing dense prompts into Dependency-Structured Visual Questions (DVQ) allows a VLM to deliver highly targeted, binary feedback on specific compositional constraints9. Subsequent repair phases utilize this VLM critique to either refine the image through localized edits (e.g., using ControlNet or in-painting) or to regenerate the image entirely with a revised prompt6.

## **Critique of Alternative Agentic Decompositions**

Before proposing the definitive v0 architecture, it is necessary to critically evaluate alternative, naive sub-agent decompositions that frequently appear in early-stage generative frameworks. Understanding their failure modes informs the robust design required for the Manurella Pixel domain.  
The Single-Agent Prompt Enhancer (SAPE) approach utilizes one large language model to interpret a user's request, rewrite the prompt, submit it to an API, and return the resulting image28. Project experience overwhelmingly indicates that this monolithic approach fails in production environments. It entangles abstract creative reasoning, strict syntax formatting, and error handling into a single context window, inevitably leading to context degradation and instruction ignoring. Furthermore, SAPE architectures cannot handle the nuances of multi-image consistency or perform iterative repair because they lack the modularity to systematically compare sequential visual outputs against baseline constraints.  
Alternatively, the linear "Generate-and-Filter" pipeline generates a large batch of images and utilizes a CLIP or VLM model to select the highest-scoring output. While computationally parallel, this approach is fundamentally inefficient and ignores the potential of active, localized repair. If a prompt structurally fails to render a specific relational concept—such as a toaster interacting with a microwave—generating one hundred variants will statistically yield one hundred failures, as the underlying prompt remains flawed29. It lacks a corrective feedback loop, wasting compute resources without advancing the generation state.  
The Multi-Agent Prompt Enhancer (MAPE) decomposes the task into routing, rewriting, and composing phases, representing a step forward from SAPE for complex compositional generation28. However, the critical flaw of MAPE is that it operates entirely pre-generation. It optimizes the text formulation but remains completely blind to the actual visual output produced by the diffusion model6. Once the image is rendered, MAPE offers no recourse for hallucinated objects, spatial errors, or missing details.  
The proposed paradigm for the Manurella Pixel domain is a State-Aware Agentic Framework. Modeled after robust systems like Generation Navigator and the Audit & Repair architecture, this approach treats each generated image as a distinct "state" within an episodic rollout6. Specialized agents audit this state, and a navigator makes a deterministic decision to either stop the process because the constraints are met, refine the existing image through localized pixel editing, or regenerate the image entirely by altering the upstream prompt6.

## **Proposed v0 Sub-Agent Decomposition**

The v0 architecture for the Manurella Pixel domain decomposes visual generation into one Top-Level Selectable Agent and four Internal Sub-Agents. This hierarchical separation isolates user-facing creative negotiation from the highly technical, model-specific execution loop. In the Kilo Code runtime, the Top-Level agent is surfaced directly to the user via .kilocodemodes or the Agent Manager workspace interface, while the internal sub-agents are invoked dynamically via background Inter-Process Communication (IPC) or autonomous tool-calling orchestration3.

### **Top-Level vs. Internal Designation**

The PixelDirector is designated as the sole Top-Level Selectable agent. The rationale for this designation is rooted in user experience and context preservation. The human user requires a single, cohesive point of contact for art direction and ideation. Exposing the internal negotiation—such as a syntax translator arguing with a VLM judge over a failed render—would overwhelm the user and pollute the conversational context window with programmatic formatting. The PixelDirector maintains the semantic thread, queries the user for missing constraints, and abstracts the complexity of the internal swarm.  
The internal sub-agents—comprising the SyntaxSpecialist, the ContinuityAnchor, the AuditJudge, and the RepairTechnician—operate below the user's visibility horizon. They communicate via structured JSON contracts, execute API calls, process image tensors, and iterate on failures without requiring human intervention until a satisfactory state is achieved.

### **Sub-Agent Definitions: The Core Architectural Contract**

The following definitions establish the strict operational boundaries, context requirements, tool permissions, and evaluation metrics for each agent in the Manurella Pixel v0 architecture.

#### **PixelDirector (Top-Level Orchestrator)**

The PixelDirector acts as the creative lead, translating vague or incomplete user requests into comprehensive, unambiguous design briefs.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To parse user intent, establish visual moodboards, define compositional hierarchy, negotiate creative constraints, and orchestrate the internal generation and repair loop until the output satisfies the brief. |
| **Use-When Boundary** | Activated whenever a user requests visual asset creation, UI mockup generation, storyboard visualization, brand identity exploration, or image editing. |
| **Do-Not-Use Boundary** | Must not directly write API-specific prompt strings (e.g., injecting \--ar 16:9 or syntax weights). Must not directly execute API calls to T2I models. |
| **Required Context** | Complete user conversation history; project brand guidelines; semantic memory bank of previously established aesthetics within the workspace. |
| **Tools / Permissions** | DelegateToSyntaxSpecialist, DelegateToContinuityAnchor, RequestAudit, RequestRepair, AskUserForClarification. |
| **Output Contract** | Emits a structured JSON "Art Direction Brief" containing discrete fields for: Subject, Style, Composition, Lighting, Color Palette, Mood, and required Text Elements12. |
| **Evaluation Rubric** | User acceptance rate of final images; the number of conversational turns required to achieve a locked, unambiguous brief. |
| **Common Failure Modes** | Over-constraining the brief with conflicting aesthetic goals; hallucinating user requirements not present in the chat history; failing to ask clarifying questions when user intent is critically underspecified. |

#### **SyntaxSpecialist (Internal Sub-Agent)**

Generative models process language fundamentally differently based on their training distribution. The SyntaxSpecialist acts as the compiler, transforming the PixelDirector's abstract brief into highly optimized, model-specific execution strings.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To translate the structured Art Direction Brief into exact, technically optimized prompts and parameters tailored to the specific target model (e.g., Flux, Midjourney v7, Imagen 3). |
| **Use-When Boundary** | Triggered automatically by the PixelDirector once a brief is locked, or triggered by the RepairTechnician when a structurally altered prompt is required to fix a hallucination6. |
| **Do-Not-Use Boundary** | Must not alter the semantic intent of the brief. Must not invent new subjects, characters, or stylistic elements not explicitly approved by the Director. |
| **Required Context** | The Art Direction Brief; API schemas; syntax constraint rules for the target model (e.g., token limits, negative prompting formatting, parameter syntax). |
| **Tools / Permissions** | RetrieveModelDocs (to fetch specific parameter syntax for unfamiliar or updated models), ExecuteGenerationAPI. |
| **Output Contract** | A finalized string, multi-prompt array, or JSON payload formatted strictly for the target generator API, ensuring all technical formatting is flawlessly applied. |
| **Evaluation Rubric** | Prompt compilation error rate (API rejections); token efficiency; strict adherence to target model best practices (e.g., active language for Flux11, permutation prompts for Midjourney17). |
| **Common Failure Modes** | Keyword stuffing for models that penalize it (e.g., Flux17); exceeding hard token limits resulting in truncation; appending unsupported or deprecated parameters. |

#### **ContinuityAnchor (Internal Sub-Agent)**

Maintaining multi-image consistency requires rigorous tracking of visual identity vectors. The ContinuityAnchor functions as the persistent memory for brand and character states.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To ensure character, style, and environmental consistency across multiple generations by managing reference images, tracking Style DNA, and injecting Character Bibles1. |
| **Use-When Boundary** | Activated when a request implies a sequence, when the user requests variations of a previously generated asset, or when strict brand identity guidelines must be maintained across disparate outputs. |
| **Do-Not-Use Boundary** | Must not be invoked for single, isolated, exploratory generations where stylistic drift is acceptable or creative variance is desired. |
| **Required Context** | The project's local rules directory (e.g., .kilocode/rules/) containing visual identity definitions4; high-resolution base reference images; previously generated outputs in the active session. |
| **Tools / Permissions** | ExtractStyleReference, ExtractCharacterReference, UpdateCharacterBible, EvaluatePoseStress. |
| **Output Contract** | Provides the SyntaxSpecialist with exact, verified image URLs for style/character parameters, or injects a standardized, high-density "style DNA" paragraph directly into the prompt payload23. |
| **Evaluation Rubric** | Identity Lock Score (measuring facial and anatomical drift against the anchor); Style Lock Score (verifying rendering style holds across varying lighting environments)24. |
| **Common Failure Modes** | Supplying low-resolution or heavily obscured reference images leading to corrupted latent extraction22; failing to align the reference image pose with the action described in the text prompt25. |

#### **AuditJudge (Internal Sub-Agent)**

The critical evaluation engine of the closed-loop system, functioning as a specialized, objective image assessment model31.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To evaluate generated pixel data against the original Art Direction Brief using a Vision-Language Model (VLM), identifying visual inconsistencies, anatomical hallucinations, lighting errors, or missing semantic elements2. |
| **Use-When Boundary** | Automatically triggered immediately following every generation or image editing action executed by the swarm. |
| **Do-Not-Use Boundary** | Must not generate images or execute pixel edits; it is strictly a diagnostic, analytical, and scoring agent. |
| **Required Context** | The original Art Direction Brief; the generated image tensor/file; the specific prompt utilized by the SyntaxSpecialist; baseline evaluation metrics for text legibility and compositional framing. |
| **Tools / Permissions** | GenerateDVQ (Dependency-Structured Visual Questions to decompose the brief into binary checkable facts)9. |
| **Output Contract** | A structured JSON "Consistency Report" containing a binary pass/fail matrix for specific constraints, and a textual critique of observed artifacts (e.g., "The left hand exhibits six fingers; the embedded text is misspelled")7. |
| **Evaluation Rubric** | Recall rate of actual visual errors; false positive rate (hallucinating errors that do not exist in the image); statistical correlation with human preference benchmarks (e.g., Auto SxS)27. |
| **Common Failure Modes** | VLM hallucination (the judge incorrectly parsing complex, overlapping visual layouts); over-penalization of minor artistic liberties that do not detract from the core intent. |

#### **RepairTechnician (Internal Sub-Agent)**

Operating on the critique provided by the AuditJudge, this agent determines and executes the optimal recovery strategy to salvage or replace flawed generations.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To systematically resolve visual errors identified in the Consistency Report by applying targeted edits, altering generation states, or refining prompts without discarding successful elements of the image6. |
| **Use-When Boundary** | Activated exclusively when the AuditJudge returns a Consistency Report containing failed visual constraints or detected artifacts. |
| **Do-Not-Use Boundary** | Must not alter or rewrite constraints that the AuditJudge marked as successful, explicitly preventing quality regressions during the repair loop2. |
| **Required Context** | The generated image; the detailed Consistency Report; the original prompt utilized; the historical trajectory of previous repair attempts for the current asset. |
| **Tools / Permissions** | InvokeControlNetEdit (for localized pixel modification), TriggerRegeneration (routes instructions back to SyntaxSpecialist), ApproveFinalState (routes the asset to the PixelDirector). |
| **Output Contract** | Emits a localized edit instruction (e.g., generating a mask over a corrupted hand and prompting for structural repair) or a structurally revised global prompt designed to mitigate the specific failure7. |
| **Evaluation Rubric** | Iteration budget efficiency (the number of loops required to achieve a passing state); regression rate (measuring whether a localized fix degraded the surrounding composition). |
| **Common Failure Modes** | Entering infinite repair loops by attempting to fix a fundamentally flawed base image; over-editing a localized region causing the image to diverge entirely from the reference identity or style7. |

## **Context Management Architecture**

A profound failure point in agentic visual generation frameworks is context bloat. Feeding an LLM or VLM the entire, unfiltered history of an art direction session degrades its attention mechanism, limiting its ability to adhere to specific, immediate visual constraints. The Manurella Pixel domain implements a strict, tri-tiered context hierarchy. This architecture is highly compatible with runtime environments like Kilo Code, which utilizes local .kilocode workspaces, but translates effectively to standard MCP context management4.

### **Always-On Context (The System Prompt)**

This foundational layer consumes a minimal but persistent token footprint and dictates the immutable behavior of the sub-agents. It contains the core operational instructions, definitions of JSON tool schemas, safety bounds, and the routing logic that governs inter-agent communication. In a Kilo Code deployment, this is analogous to the foundational agent-runtime configuration injected via environment variables upon process spawning32. For example, the SyntaxSpecialist operates under an always-on directive: *"Do not generate conversational filler or explain your reasoning to the user. Output only the exact API string or the defined JSON execution payload."*

### **Reference Material (Retrieved on Session Load)**

This intermediate layer represents the persistent visual identity of the active project. It is loaded selectively when the PixelDirector initializes a new session or worktree. It contains Character Bibles, exact brand color hex codes, standardized aspect ratio requirements, and baseline moodboard descriptions. In the Kilo Code runtime, this data is extracted from the {workspace}/.kilocode/rules/ and {workspace}/.kilocode/workflows/ directories4. The ContinuityAnchor relies on this layer to intercept requests. If a user states, "Render our main mascot drinking coffee," the agent retrieves the exact, pre-approved fifty-word physical description of the mascot from the reference layer, ensuring identity lock without requiring the user to restate the parameters23.

### **Dynamically Retrieved Material (Just-in-Time Context)**

To aggressively minimize token usage and prevent attention distraction, technical documentation and historical error states are fetched exclusively when necessary to complete a specific action. This "Just-in-Time" layer includes API documentation for newly integrated models, edge-case syntax rules, and the logs of previous failed generation attempts from the active repair loop. Using standard search tools, the SyntaxSpecialist can fetch the documentation defining how Flux handles transparent material generation11 only when the user's brief specifically requests glass, water, or translucent fabrics. Once the prompt is compiled, this context is discarded from the active window.

## **Benchmarking the Sub-Agents**

To rigorously evaluate the effectiveness and reliability of the sub-agent architecture, the framework must be subjected to standardized benchmarking designed specifically for the unique failure modes of generative synthesis. The following benchmarks are proposed for each specific sub-agent.

### **1\. The Underspecified Intent Task (Evaluating the PixelDirector)**

* **Objective:** Measure the agent's ability to extrapolate a complete brief from vague input without hallucinating conflicting styles.  
* **Task:** The user inputs: "I need a banner image for my new coffee shop website."  
* **Evaluation:** The PixelDirector must seamlessly ask clarifying questions regarding the brand's aesthetic (e.g., modern, rustic, corporate), the preferred color palette, and the necessary compositional space for potential text overlays. Success is measured by the generation of a comprehensive, non-contradictory Art Direction Brief within a maximum of three conversational turns.

### **2\. The Model-Switching Translation Task (Evaluating the SyntaxSpecialist)**

* **Objective:** Measure syntactic flexibility and constraint adherence across divergent model architectures.  
* **Task:** Provide the agent with a complex brief requiring depth of field, neon lighting, and a specific cinematic mood. Command the agent to generate valid prompts for both Midjourney v7 and Imagen 3\.  
* **Evaluation:** The Midjourney output must accurately utilize parameter syntax (e.g., \--ar 16:9 \--style raw \--s 250\) and avoid natural language bloat18. The Imagen 3 output must respect the strict 480-token limit, utilize declarative modifiers, and appropriately configure the generation API payload20. API rejection equals failure.

### **3\. The Identity Lock and Pose Stress Task (Evaluating the ContinuityAnchor)**

* **Objective:** Evaluate the agent's ability to maintain physical and stylistic integrity across dynamic transformations.  
* **Task:** Provide a single reference image of a human character. Command the system to generate six images of the character performing anatomically distinct actions: walking, running, sitting, jumping, waving, and crouching24.  
* **Evaluation:** The AuditJudge computes an Identity Lock Score (comparing facial and hair silhouettes to the anchor reference) and checks for structural or rendering degradation during the complex pose shifts24.

### **4\. The Dependency-Structured Composition Task (Evaluating the AuditJudge)**

* **Objective:** Evaluate the VLM's ability to accurately detect relational physics and text rendering errors without false positives.  
* **Task:** Evaluate an image generated from the prompt: "A vintage typewriter on a wooden desk. A piece of paper is feeding into it. The exact text 'AGENTIC WORKFLOW' is printed in a blue serif font on the paper. A ceramic coffee mug rests to the left."  
* **Evaluation:** The AuditJudge must construct and answer a CRAFT-style DVQ matrix9:  
  * Is there a vintage typewriter on a desk? (Y/N)  
  * Is paper feeding into it? (Y/N)  
  * Does the text 'AGENTIC WORKFLOW' appear perfectly? (Y/N)  
  * Is the text in a blue serif font? (Y/N)  
  * Is there a coffee mug to the left? (Y/N)  
  * *Success is defined by the VLM's assessment perfectly matching a human evaluator's ground-truth assessment of the same image.*

### **5\. The Iterative Salvage Task (Evaluating the RepairTechnician)**

* **Objective:** Evaluate the agent's efficiency and anti-regression capabilities during a complex repair loop.  
* **Task:** Intentionally inject a structurally flawed initial prompt to force a generation anomaly (e.g., "A dog surfing, with three surfboards").  
* **Evaluation:** Measure the number of loop iterations required for the RepairTechnician to receive the anomaly report from the AuditJudge, isolate the error (excess surfboards), and execute a localized mask/edit or prompt rewrite to correct the subject count without destroying the style of the water or the dog7.

## **Optimizing for Weaker and Non-Frontier Models**

The Manurella Agentic Framework explicitly targets the enhancement of weaker, non-frontier, or local open-weights models, ensuring the architecture remains accessible, private, and cost-efficient. Relying on high-end, closed-source VLMs and API generators for every iteration of a continuous repair loop is financially prohibitive and introduces high latency28. The architecture incorporates several mechanisms to compensate for the limitations of smaller models.  
Evidence suggests that Parameter-Efficient Prompt Tuning (Soft Prompts) is highly effective for agentic systems33. Instead of relying on massive context windows to instruct a small model on how to behave, soft prompts—learned vector embeddings of 10 to 100 tokens—are prepended to the input at runtime. This allows a single deployment of an efficient, frozen base model to exhibit highly specialized behaviors. The PixelDirector utilizes one soft prompt embedding, while the AuditJudge utilizes another, significantly reducing inference costs and deployment complexity while approaching the performance of full fine-tuning33.  
To optimize the internal routing and reasoning of weaker LLMs (such as local 7B or 8B parameter models), the framework employs Visual Experience Distillation (VED)34. When a frontier model successfully completes a complex repair loop, the delta between the worst trajectory (the failed initial prompt) and the best trajectory (the successful, repaired prompt) is abstracted into a structured "visual experience." This data is utilized in an on-policy self-distillation loop, allowing the weaker student model to internalize effective search strategies, knowledge activation, and prompt construction. Over time, the weaker model learns the optimal syntax combinations without requiring costly iterative loops on future prompts34.  
Furthermore, the framework utilizes State-Conditioned Early Stopping to conserve compute resources. Instead of executing a fixed, expensive multi-step repair loop by default, the system relies on an explicit stopping criterion9. If a non-frontier generator produces an image that satisfies the AuditJudge's basic dependency-structured visual questions on the first attempt, the navigator immediately halts the loop in a Stop state, preserving the satisfactory image and preventing unnecessary API calls or degradation6. For complex prompt discovery, the SyntaxSpecialist can be backed by programmatic frameworks (e.g., DSPy logic), which treat prompt optimization as a heuristic search problem. A weaker LLM iteratively generates mutations and relies on the VLM for fitness scoring, treating each prompt as an arm in a Thompson-sampling bandit to balance exploration with exploitation36.

## **Expansion Path: v0 to v2**

The proposed sub-agent architecture is deliberately modular, designed to scale alongside the capabilities of the Kilo Code runtime and the rapid advancements in the broader generative AI ecosystem.  
The **v0 framework** establishes the Text-to-Image foundation. Its primary scope is the reliable translation of natural language intent into final image arrays. It features the implementation of the five core sub-agents and focuses heavily on prompt optimization across varied, text-reliant APIs (e.g., Flux, OpenAI GPT Image 2, Google Vertex Imagen). The AuditJudge relies on basic VLM evaluation of final PNG/JPEG outputs against textual briefs. The target use cases include UI mockups, conceptual storyboarding, and single-asset marketing creation.  
The **v1 expansion** transitions the framework toward Latent Space Editing and Reference Mastery. The focus shifts from pure prompt regeneration to localized image editing and structural control. The RepairTechnician is upgraded with advanced tools to perform automated image masking, in-painting, and ControlNet manipulation, allowing it to use Canny edges or Depth maps to force strict compositional adherence rather than relying on stochastic text adjustments2. The ContinuityAnchor gains the ability to train localized, temporary LoRAs (Low-Rank Adaptations) on-the-fly for mathematically perfect identity locking, moving beyond simple reference image passing. Furthermore, the framework integrates deeply into runtimes like Kilo Code's Browser Session Panel, auto-capturing web UI references and systematically separating embedded visual generation from editable HTML/CSS overlay layers4.  
The **v2 expansion** represents a paradigm shift into Multimodal and Temporal Expansion, extending the Pixel domain into motion and video generation. The ContinuityAnchor expands to support complex Video Reference Systems, managing Style, Character, and Setting references across temporal frames to prevent hallucination drift over time25. The AuditJudge undergoes a massive architectural shift to evaluate temporal consistency, utilizing specialized VLMs to check for texture flickering, physics degradation, and object permanence across multi-frame generations. This phase aims to produce production-ready, temporally coherent visual sequences that rival professional videography.

## **Conclusion**

The Manurella Pixel domain necessitates a fundamental departure from traditional, linear prompting workflows. Generative image models possess immense rendering power but are inherently stochastic, demanding rigorous syntax translation, persistent identity management, and active, VLM-guided repair loops to achieve professional-grade reliability.  
By decomposing visual generation into a state-aware ecosystem—orchestrated by a top-level PixelDirector and executed by internal specialists for syntax, continuity, evaluation, and repair—this architecture neutralizes the fragility of text-to-image models. Optimized for runtimes like Kilo Code while remaining universally portable, this framework minimizes context bloat through strict operational boundaries and hierarchical memory retrieval. Through the implementation of parameter-efficient tuning, visual experience distillation, and deterministic early-stopping, the architecture ensures that even weaker, non-frontier models can reliably produce visually consistent, high-fidelity outputs through structured agentic reasoning.

#### **Works cited**

1. ChatGPT Images 2.0: What It Can Do and How to Use It for Real Work | MindStudio, [https://www.mindstudio.ai/blog/chatgpt-images-2-use-cases-workflows](https://www.mindstudio.ai/blog/chatgpt-images-2-use-cases-workflows)  
2. Audit & Repair: An Agentic Framework for Consistent Story Visualization in Text-to-Image Diffusion Models \- arXiv, [https://arxiv.org/html/2506.18900v1](https://arxiv.org/html/2506.18900v1)  
3. Agent Manager \- Kilo Code, [https://kilo.ai/docs/automate/agent-manager](https://kilo.ai/docs/automate/agent-manager)  
4. Kilo Code \-- Sandbox Analysis Report \- Agent Safehouse, [https://agent-safehouse.dev/docs/agent-investigations/kilo-code.html](https://agent-safehouse.dev/docs/agent-investigations/kilo-code.html)  
5. Cloud Agent \- Kilo Code, [https://kilo.ai/docs/code-with-ai/platforms/cloud-agent](https://kilo.ai/docs/code-with-ai/platforms/cloud-agent)  
6. Generation Navigator: A State-Aware Agentic Framework for Image Generation \- arXiv, [https://arxiv.org/html/2605.17969v1](https://arxiv.org/html/2605.17969v1)  
7. \[Literature Review\] Audit & Repair: An Agentic Framework for Consistent Story Visualization in Text-to-Image Diffusion Models \- Moonlight | AI Colleague for Research Papers, [https://www.themoonlight.io/en/review/audit-repair-an-agentic-framework-for-consistent-story-visualization-in-text-to-image-diffusion-models](https://www.themoonlight.io/en/review/audit-repair-an-agentic-framework-for-consistent-story-visualization-in-text-to-image-diffusion-models)  
8. Maestro: Self-Improving Text-to-Image Generation via Agent Orchestration \- arXiv, [https://arxiv.org/html/2509.10704v1](https://arxiv.org/html/2509.10704v1)  
9. CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation \- arXiv, [https://arxiv.org/html/2512.20362v2](https://arxiv.org/html/2512.20362v2)  
10. FLUX.1 Prompt Guide: Pro Tips and Common Mistakes to Avoid | getimg.ai, [https://getimg.ai/blog/flux-1-prompt-guide-pro-tips-and-common-mistakes-to-avoid](https://getimg.ai/blog/flux-1-prompt-guide-pro-tips-and-common-mistakes-to-avoid)  
11. FLUX.1 Prompt Manual: A Foundational Guide : r/FluxAI \- Reddit, [https://www.reddit.com/r/FluxAI/comments/1imha0t/flux1\_prompt\_manual\_a\_foundational\_guide/](https://www.reddit.com/r/FluxAI/comments/1imha0t/flux1_prompt_manual_a_foundational_guide/)  
12. FLUX.1 Zero to Pro Prompt Guide \- RentPrompts, [https://rentprompts.com/blog/flux1-zero-to-pro-prompt-guide](https://rentprompts.com/blog/flux1-zero-to-pro-prompt-guide)  
13. README.md \- RobinaMirbahar/vertex-ai-imagen3 \- GitHub, [https://github.com/RobinaMirbahar/vertex-ai-imagen3/blob/main/README.md](https://github.com/RobinaMirbahar/vertex-ai-imagen3/blob/main/README.md)  
14. gpt-image-2 Brings Reasoning to AI Video Asset Creation \- Tellers.AI, [https://tellers.ai/blog/gpt\_image\_2\_ai\_video\_creation\_openai\_2026-04-22](https://tellers.ai/blog/gpt_image_2_ai_video_creation_openai_2026-04-22)  
15. Any2Poster: Any-Source Poster Generation Across Modalities and Domains \- arXiv, [https://arxiv.org/html/2606.02915v1](https://arxiv.org/html/2606.02915v1)  
16. Midjourney prompts guide (2026) with V6 & V7 Tips \- Printify, [https://printify.com/blog/midjourney-prompts/](https://printify.com/blog/midjourney-prompts/)  
17. Midjourney V6 Prompt Guide: 15 Formulas That Actually Work in 2026 | Howard Huang, [https://www.whatshuang.com/posts/midjourney-prompts](https://www.whatshuang.com/posts/midjourney-prompts)  
18. The Ultimate Midjourney Prompt Guide (Devs & Designers) | ImaginePro Blog, [https://www.imaginepro.ai/blog/2025/7/midjourney-prompt-guide-developers-designers](https://www.imaginepro.ai/blog/2025/7/midjourney-prompt-guide-developers-designers)  
19. Imagen 3: A Guide With Examples in the Gemini API \- DataCamp, [https://www.datacamp.com/tutorial/imagen-3](https://www.datacamp.com/tutorial/imagen-3)  
20. Generate images using Imagen | Gemini API \- Google AI for Developers, [https://ai.google.dev/gemini-api/docs/imagen](https://ai.google.dev/gemini-api/docs/imagen)  
21. GPT Image 2: OpenAI's New Model for Professional Business Visuals \- Tensoria, [https://tensoria.fr/en/tools/gpt-image-2-openai-pro-images](https://tensoria.fr/en/tools/gpt-image-2-openai-pro-images)  
22. Imagen 3 Subject Consistency: How to Build Multi-Character Scenes for E-Commerce, [https://www.mindstudio.ai/blog/imagen-3-subject-consistency-e-commerce-product-photography/](https://www.mindstudio.ai/blog/imagen-3-subject-consistency-e-commerce-product-photography/)  
23. GPT Image 2 group image generation principle breakdown: 3 methods to achieve multi-image consistency – 2026, [https://help.apiyi.com/en/gpt-image-multi-image-generation-consistency-guide-en.html](https://help.apiyi.com/en/gpt-image-multi-image-generation-consistency-guide-en.html)  
24. Best AI Character Generator for Consistent Characters (2026) \- Neolemon, [https://www.neolemon.com/blog/best-ai-character-generator-for-consistent-characters/](https://www.neolemon.com/blog/best-ai-character-generator-for-consistent-characters/)  
25. What Is Sora's Reference System? How OpenAI Adds Character Consistency to AI Video, [https://www.mindstudio.ai/blog/what-is-sora-reference-system-character-consistency](https://www.mindstudio.ai/blog/what-is-sora-reference-system-character-consistency)  
26. How to Maintain Consistent Characters in Midjourney V7: A Masterclass \- Flowith Blog, [https://flowith.io/blog/midjourney-v7-consistent-characters-masterclass/](https://flowith.io/blog/midjourney-v7-consistent-characters-masterclass/)  
27. \[R\] CRAFT: thinking agent for image generation and edit : r/MachineLearning \- Reddit, [https://www.reddit.com/r/MachineLearning/comments/1qwhhqa/r\_craft\_thinking\_agent\_for\_image\_generation\_and/](https://www.reddit.com/r/MachineLearning/comments/1qwhhqa/r_craft_thinking_agent_for_image_generation_and/)  
28. APE: Agentic Prompt Enhancer for Image Generation and Editing \- arXiv, [https://arxiv.org/html/2606.00204v1](https://arxiv.org/html/2606.00204v1)  
29. CRAFT: Continuous Reasoning and Agentic Feedback Tuning \- Hugging Face, [https://huggingface.co/blog/flymy-ai/craft-1](https://huggingface.co/blog/flymy-ai/craft-1)  
30. FLUX 1 Prompts Guide – Including Best Practices, [https://flux-1.ai/flux-1-prompts/](https://flux-1.ai/flux-1-prompts/)  
31. Vision Language Models Learn to Assess Images with Specialists \- CVF Open Access, [https://openaccess.thecvf.com/content/WACV2026W/WVAQ/papers/V.\_Vision\_Language\_Models\_Learn\_to\_Assess\_Images\_with\_Specialists\_WACVW\_2026\_paper.pdf](https://openaccess.thecvf.com/content/WACV2026W/WVAQ/papers/V._Vision_Language_Models_Learn_to_Assess_Images_with_Specialists_WACVW_2026_paper.pdf)  
32. kilocode-legacy/AGENTS.md at main \- GitHub, [https://github.com/Kilo-Org/kilocode-legacy/blob/main/AGENTS.md](https://github.com/Kilo-Org/kilocode-legacy/blob/main/AGENTS.md)  
33. Prompt Tuning: Parameter-Efficient Optimization for Agentic AI Systems \- Comet, [https://www.comet.com/site/blog/prompt-tuning/](https://www.comet.com/site/blog/prompt-tuning/)  
34. GenEvolve · Self-Evolving Image Generation Agents via Tool-Orchestrated Visual Experience Distillation \- Sixiang Chen, [https://ephemeral182.github.io/GenEvolve/](https://ephemeral182.github.io/GenEvolve/)  
35. GenEvolve: Self-Evolving Image Generation Agents via Tool-Orchestrated Visual Experience Distillation \- arXiv, [https://arxiv.org/html/2605.21605v1](https://arxiv.org/html/2605.21605v1)  
36. Agentic prompt optimization with visual contrastive reasoning for fine-grained classification \- Amazon Science, [https://www.amazon.science/publications/agentic-prompt-optimization-with-visual-contrastive-reasoning-for-fine-grained-classification](https://www.amazon.science/publications/agentic-prompt-optimization-with-visual-contrastive-reasoning-for-fine-grained-classification)  
37. Optimizing generative AI prompts \- AWS Prescriptive Guidance, [https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-experimenting-prompt-optimization.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-experimenting-prompt-optimization.html)