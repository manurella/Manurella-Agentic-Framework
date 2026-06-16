# **State-of-the-Art Sub-Agent Architecture for the Manurella Muse Domain**

## **Introduction to the Manurella Muse Domain**

The Manurella Agentic Framework represents a critical advancement in runtime-agnostic artificial intelligence architectures. Designed specifically to elevate the outputs of weaker, open-weight, or free-tier models, the framework achieves frontier-level performance through the orchestration of specialist domain packs, stringent context control, deterministic memory structures, and modular tool adapters. Within this ecosystem, the Manurella Muse domain targets the highly subjective, complex, and long-horizon tasks associated with professional creative writing, storytelling, scriptwriting, and interactive narrative design. While Kilo Code serves as the initial runtime target, the architecture proposed herein is fundamentally portable, ensuring seamless deployment across Codex, ChatGPT, Gemini, and custom Python or Model Context Protocol (MCP) tooling environments.  
Large language models inherently struggle with long-form narrative generation. Empirical evidence demonstrates that models generate highly localized, statistically probable text that degrades over extended contexts, suffering from "objective drift" where goals and plans shift unintentionally1. When generating narratives exceeding a few thousand words, monolithic models frequently contradict established facts, violate world-building rules, and homogenize authorial voice, replacing distinct stylistic prose with generic, probability-smoothed text1. Furthermore, single-pass generation flattens creative quality by failing to separate the cognitive load of plotting from the mechanical execution of syntax.  
To counteract these fundamental architectural limitations, the Muse domain cannot rely on a singular, monolithic generation strategy. Instead, it necessitates a sophisticated, multi-agent decomposition that explicitly mirrors the collaborative, specialized workflows of professional writers, editors, and narrative designers. This report provides an exhaustive architectural blueprint for the v0 sub-agent decomposition of the Manurella Muse domain. It maps the competencies of traditional publishing and interactive narrative design, critiques alternative system decompositions, outlines the specific boundaries, contexts, and evaluation metrics for each proposed sub-agent, and establishes a forward-looking roadmap for system expansion. The ensuing analysis distinguishes between empirical evidence derived from current computational linguistics research, project experiences associated with framework development, and speculative hypotheses regarding future multi-modal expansions.

## **Mapping Professional Creative Writing and Editing Workflows**

To design an effective agentic architecture, one must first deconstruct the human workflows it intends to augment or simulate. The professional creation of long-form prose and interactive narrative design relies on distinct cognitive phases, each demanding entirely different context windows, evaluation rubrics, and conceptual tools. A fundamental error in early artificial intelligence story generators was the conflation of these distinct disciplines into a single generative action.

### **Narrative Design and Worldbuilding**

Narrative design differs fundamentally from traditional prose writing. While a traditional game writer or novelist focuses on the literal words on the page—dialogue, barks, lore entries, and item descriptions—a narrative designer focuses on the architecture of the experience. This includes agency, environmental storytelling, interactive branching, tension pacing, and systemic worldbuilding5. Competencies in this phase include establishing the "rules" of the world, defining faction dynamics, structuring non-linear story modules, and mapping character archetypes before drafting begins.  
Theoretical frameworks are foundational to this stage. Robert McKee emphasizes that storytelling is about principles, not rules, and requires the pursuit of archetypes rather than stereotypes to unearth universally human experiences9. John Truby posits that characters must not be designed in isolation but as an interconnected web, where the cast is formed through moral and psychological contrasts11. Lajos Egri further argues that strong drama emerges strictly from clear moral causation and premise11. In a professional workflow, the worldbuilding phase functions as the invisible iceberg beneath the water, establishing a coherent setting that dictates the parameters of the plot long before dialogue is written13. Translating this to an agentic framework requires a dedicated pre-production phase that generates a structured "Story Prototype" comprising character nodes and logical constraints14.

### **Developmental and Structural Editing**

Often termed substantive or content editing, developmental editing evaluates the manuscript from a macro-level perspective15. A developmental editor does not correct grammar, syntax, or spelling. Rather, they analyze Aristotelian plot structures, pacing, thematic resonance, character arcs, and the overall narrative tension15. In a professional workflow, this phase requires assessing the manuscript against high-level narrative theories to identify structural plot holes, causeless effects, and unearned emotional climaxes.  
This structural assessment often relies on Gérard Genette’s theories of narrative order, distinguishing between the chronological order of the story and the non-linear narrative order presented to the reader through analepsis (flashbacks) and prolepsis (flash-forwards)19. The competency here lies in ensuring that despite non-linear presentation, the causal and logical relationships among events remain intact. For an artificial intelligence system, this requires an agent capable of abstracting raw text back into a structural outline to evaluate its logical flow, identifying where character motivations fail or where the rising action sags15.

### **Line Editing and Stylistic Refinement**

Line editing operates at the paragraph and sentence level, occupying the space between structural overhauls and mechanical corrections. Its primary competency is the refinement of prose style, tone, pacing, and linguistic flow18. A line editor eliminates redundant expressions, tightens verbose stage directions, and removes "filter words" (such as "she noticed," "he felt," or "they wondered") to create narrative immediacy and immerse the reader directly in the character's perspective22.  
Crucially, the line editor must preserve and elevate the author's unique voice. Current large language models suffer heavily in this domain, often veering toward purple prose, clichés, and a homogenized "AI voice" that lacks stylistic diversity4. Professional line editing requires an acute understanding of linguistic style and rhythm, separating the literal events of the story from the stylistic execution of the telling.

### **Copyediting and Proofreading**

Copyediting is the rigorous, often deterministic enforcement of mechanical consistency. It relies heavily on standardized frameworks, most notably the Chicago Manual of Style (CMOS), and project-specific "Style Sheets"24. Competencies include enforcing grammatical rules, maintaining timeline consistency, tracking character attributes (such as eye color or specific tattoos), standardizing the spelling of fictional locations, and correcting syntax22.  
The creation of a style sheet acts as a "second brain" for the editorial team, documenting capitalization, hyphenation, and specific terminology to ensure that details are consistently applied over the course of a massive manuscript22. This is a highly rules-based phase that acts as a quality assurance checkpoint. In an agentic framework, this maps directly to an internal validation sub-agent that operates independently of creative generation, serving purely to ensure mechanical and continuous integrity.

## **Critique of Alternative System Decompositions**

Before finalizing the v0 architecture for the Manurella Muse domain, it is necessary to evaluate and critique existing approaches to large language model narrative generation. Analyzing the failure modes of alternative decompositions justifies the necessity of the proposed multi-agent structure.

### **The Limitations of Monolithic and Flat Sequential Generation**

Early approaches to artificial intelligence story generation relied on flat, sequential prompting, wherein a model was simply instructed to write a story based on a premise. Empirical evidence demonstrates that this approach catastrophically fails in long-form generation1. Models rapidly exhaust their context windows, leading to severe narrative entropy. They contradict their own established facts, forget character traits, violate world rules, and lose causal logic1. Furthermore, single-pass generation flattens creative quality. Because the model must simultaneously compute plot logic, character voice, and grammatical correctness within a single inference pass, the resulting prose is inherently safe, homogenized, and predictable3. It is hypothesized that weaker models like Kilo Code will degrade even faster under monolithic prompting, necessitating strict task isolation.

### **The Vulnerabilities of Pure Bottom-Up Sandbox Simulations**

Recent multi-agent frameworks, such as BookWorld or StoryBox, utilize bottom-up, emergent narrative generation. In these systems, individual agents act as characters in a simulated sandbox environment, and the story emerges organically from their unscripted interactions based on predefined personas30. While this produces high local consistency and surprising micro-interactions, it is structurally flawed for professional, directed prose generation. Unconstrained sandbox simulations lack an overarching authorial intent. They fail to pace tension effectively, struggle to build structured Aristotelian narrative arcs, and rarely deliver satisfying thematic conclusions32. They require a top-down orchestrator to prevent the narrative from meandering endlessly. While useful for interactive roleplay, pure sandboxes are insufficient for authoring a structured novel or screenplay.

### **The Efficacy of Hierarchical and Collaborative Frameworks**

The proposed architecture for Manurella Muse adopts a hybrid top-down planning and bottom-up execution model, drawing upon the successes of hierarchical frameworks like Dramatron, SCORE, StoryWriter, and Agents' Room3.  
By decoupling planning from writing—utilizing methodologies such as Detailed Outline Control (DOC) and Skeleton-of-Thought (SoT)—the system dramatically mitigates the cognitive load on the underlying model36. Instead of forcing a single model to track grammar, pacing, plot, and character arcs simultaneously, tasks are isolated. A multi-agent decomposition utilizing a shared "scratchpad" allows specialized agents to act on discrete elements of the text iteratively21. This hierarchical structure ensures that high-level narrative goals dictate scene-level generation, which is subsequently refined by specialized editorial agents acting in closed feedback loops21.

## **Proposed v0 Sub-Agent Decomposition**

To accurately reflect professional publishing workflows while maintaining system efficiency, the v0 architecture distinguishes between top-level selectable agents and internal sub-agents. Top-level agents are user-facing entities that manage major phases of the creative lifecycle. Internal sub-agents are specialized, background utilities invoked dynamically by the top-level agents to handle specific, computationally narrow micro-tasks, thereby protecting weaker models from context overload.

### **Top-Level Selectable Agents**

1. The Orchestrator (Muse Lead): Functions as the primary user interface and dispatch system.  
2. The World and Character Architect: Focuses entirely on pre-production, worldbuilding, and lore generation.  
3. The Narrative Designer (PlotWeaver): Handles high-level plot outlining, structural pacing, and chapter breakdowns.  
4. The Developmental Editor: Critiques existing drafts for macro-level structural flaws, theme, and character arcs.  
5. The Line and Style Editor: Refines prose, emulates specific authorial voices, and improves sentence-level flow.

### **Internal Sub-Agents**

1. The EventSeed and SubTasker: Breaks down macro-outlines into atomic, actionable scene beats.  
2. The Scene Drafter: The primary generation engine that converts atomic scene beats into narrative prose.  
3. The Continuity and Logic Checker: A background validation agent that flags contradictions in state, timeline, or world rules.  
4. The Copyeditor: A strict, rules-based agent that enforces the Style Sheet and corrects mechanical syntax errors.  
5. The Context Coordinator: Dynamically summarizes past chapters and extracts relevant semantic relationships to manage context windows.

## **Detailed Sub-Agent Architectural Definitions**

The following tables and narrative descriptions define the strict boundaries, contexts, output contracts, and evaluation rubrics for each critical agent within the Manurella Muse ecosystem.

### **The Orchestrator (Muse Lead)**

The Orchestrator serves as the central nervous system of the framework. It does not write prose or outline plots; rather, it parses user intent and routes execution to the appropriate specialist. Inspired by the central orchestrator in the Agents' Room framework, it maintains the global "scratchpad" where intermediate outputs are stored and shared among agents21. This prevents redundant processing and ensures that all agents operate on a unified state representation.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To act as the central dispatcher, interpreting user queries, managing the global scratchpad, and routing tasks to specialized agents. |
| **Use-When Boundary** | Initializing a new project, handling ambiguous user requests, or transitioning between major workflow phases (e.g., moving from outlining to drafting). |
| **Do-Not-Use Boundary** | Never used for actual prose generation, deep editing, or creative brainstorming. |
| **Required Context** | The user prompt, current project state (phase), and the active global scratchpad. |
| **Tools/Permissions** | Access to agent-routing APIs, read/write access to the global scratchpad, permission to halt execution and query the user for clarification. |
| **Output Contract** | Strict JSON command payload dictating the next agent to invoke, the payload of instructions, and state updates. |
| **Evaluation Rubric** | Routing accuracy (percentage of tasks sent to the correct specialist), execution speed, and task completion rates. |
| **Common Failure Modes** | Over-delegation (calling too many agents for a simple task), infinite loops between agents, and misinterpreting subtle user intent. |

### **The Narrative Designer (PlotWeaver)**

The Narrative Designer is responsible for the structural scaffolding of the story. It operates on the principles of Detailed Outline Control (DOC), which shifts the creative burden from the main drafting procedure to the planning stage37. By generating a highly granular outline, it ensures that subsequent drafting agents have a clear roadmap, reducing the likelihood of hallucinations or objective drift. It utilizes non-linear narration strategies, breaking events into sub-events and weaving them across chapters to create engaging structures3.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To generate structured, detailed outlines and map narratives using concepts of narrative order and causal logic19. |
| **Use-When Boundary** | The user requests a story outline, chapter breakdown, or when a developmental edit requires structural rerouting. |
| **Do-Not-Use Boundary** | Sentence-level prose drafting, copyediting, or deep character psychological profiling. |
| **Required Context** | The overarching premise, the Story Prototype (Role Graph and Plot Graph)14, and target length constraints. |
| **Tools/Permissions** | Read access to Worldbuilding documents; Write access to the Outline module. |
| **Output Contract** | A structured sequence of event tuples (Time, Location, Characters Involved, Goal, Conflict, Outcome)3. |
| **Evaluation Rubric** | Evaluated on *Flexibility* and *Originality* metrics, and structural coherence (absence of causal logic violations)29. |
| **Common Failure Modes** | "Railroading" (creating highly predictable, linear plots), resolving narrative tension too quickly, or failing to interweave subplots effectively3. |

### **The Scene Drafter (Internal Sub-Agent)**

The Scene Drafter is the workhorse of the ecosystem. It is an internal agent invoked exclusively when an atomic outline node is approved for expansion. To optimize performance for weaker models, the Scene Drafter is never exposed to the entire manuscript. Instead, it receives a tightly constrained context window containing only the immediate event tuple, the style sheet, and a dynamic summary of the preceding text. This approach, akin to the Skeleton-of-Thought methodology, allows for high-quality parallel generation3.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To transform atomic event tuples provided by the Narrative Designer into immersive, stylistic narrative prose. |
| **Use-When Boundary** | Automatically invoked by the Orchestrator or Narrative Designer when an outline node is approved for expansion3. |
| **Do-Not-Use Boundary** | Plotting future chapters, revising existing text, or making macro-level narrative decisions. |
| **Required Context** | The specific atomic event tuple, the immediately preceding text, the compressed historical summary, and the project Style Sheet3. |
| **Tools/Permissions** | Write access strictly limited to the active draft scratchpad. No access to future outline nodes to prevent premature reveals. |
| **Output Contract** | Raw narrative prose formatted in Markdown, conforming strictly to specified length and tone constraints. |
| **Evaluation Rubric** | *Fluency* and *Elaboration* metrics, stylistic consistency, and strict adherence to the provided outline constraints39. |
| **Common Failure Modes** | Sycophancy (rushing to a happy resolution despite dark prompts), purple prose, cliché generation, and ignoring subtle constraints provided in the outline4. |

### **The Developmental Editor**

Operating as a critical feedback loop, the Developmental Editor assesses the output of the Narrative Designer or the compiled output of the Scene Drafter. It analyzes the text for thematic consistency, character motivation authenticity, and structural pacing15. It leverages the principles of narrative theory, evaluating whether the text adheres to the moral logic and character web established during pre-production9.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To analyze macro-level structural flaws, character motivation authenticity, pacing, and thematic resonance15. |
| **Use-When Boundary** | The user requests feedback on a completed outline or chapter, or when the system detects a potential drop in narrative tension. |
| **Do-Not-Use Boundary** | Correcting typos, enforcing grammar, altering stylistic prose, or checking minor factual continuity errors. |
| **Required Context** | The full text of the chapter/outline, the premise, and theoretical reference frames (e.g., character web dynamics, scene sequences)11. |
| **Tools/Permissions** | Read-only access to drafts; Write access exclusively to the Editorial Feedback log. |
| **Output Contract** | An "Editorial Letter" containing a high-level critique, categorized into Strengths, Structural Weaknesses, Character Inconsistencies, and Actionable Revision Strategies15. |
| **Evaluation Rubric** | Human-expert alignment (measured via Consensual Assessment Technique) and the actionable, pedagogical quality of the feedback39. |
| **Common Failure Modes** | Providing overly generic feedback (e.g., repeating "show, don't tell"), flattening style diversity by enforcing rigid formulaic beats, or misinterpreting avant-garde stylistic choices as structural errors4. |

### **The Continuity and Logic Checker (Internal Sub-Agent)**

Narrative consistency is the most fragile element in long-context generation. The Continuity and Logic Checker operates continuously in the background, utilizing methodologies derived from the SCORE framework and ConStory-Bench1. It tracks the symbolic logic states of characters and items, flagging when a destroyed item reappears or when a character's geographic location becomes impossible28.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To detect and flag contradictions across fine-grained error subtypes (e.g., timeline contradictions, dead characters reappearing, geographic impossibilities)1. |
| **Use-When Boundary** | Automatically triggered in the background after a Scene Drafter completes a chunk of text, prior to finalizing the draft29. |
| **Do-Not-Use Boundary** | Evaluating prose quality, pacing, emotional resonance, or thematic depth. |
| **Required Context** | The newly generated text, the Dynamic State Tracker (symbolic logic states of items/characters), and the World Rules database28. |
| **Tools/Permissions** | Read access to all generated data; Write access to the Error Flag registry. |
| **Output Contract** | A JSON array of flagged contradictions, including the error category, exact textual evidence span, and a brief rationale1. |
| **Evaluation Rubric** | High precision and recall on established continuity benchmarks, minimizing false positives29. |
| **Common Failure Modes** | Flagging intentional mysteries, nonlinear time jumps, or unreliable narrators as logical "errors"1. |

### **The Line and Style Editor**

The Line and Style Editor is critical for counteracting the homogenization inherent in large language models. This agent is trained to evaluate and emulate specific authorial styles, manipulating linguistic features, phrasal verbs, punctuation rhythm, and typographical patterns4. It systematically removes "filter words" to enhance narrative immediacy and ensures the prose matches the intended authorial voice22.

| Parameter | Specification |
| :---- | :---- |
| **Purpose** | To refine prose rhythm, emulate specific authorial styles, remove filter words, and ensure immediate, immersive text4. |
| **Use-When Boundary** | When prose has been cleared of structural and continuity errors, and requires stylistic polishing before finalization. |
| **Do-Not-Use Boundary** | Altering plot outcomes, rewriting dialogue content (only style), or checking broad continuity and grammar. |
| **Required Context** | The raw draft, the project Style Sheet, and specific cognitive representations (linguistic features, concept mappings) of the target style25. |
| **Tools/Permissions** | Write access to apply differential edits (diffs) to the raw draft. |
| **Output Contract** | A revised text block that matches the linguistic style similarity metrics of the target author45. |
| **Evaluation Rubric** | Pairwise LLM-as-a-judge accuracy against target style references, *Linguistic Style Similarity* scoring, and reduction of cliché metrics45. |
| **Common Failure Modes** | "Over-editing" (stripping the author's original voice), homogenizing text into an "AI default" tone, or introducing semantic shifts during stylistic rewriting4. |

## **Context Strategy and Memory Management**

A critical constraint in designing an architecture for weaker or open-weight models is avoiding "context stuffing." Feeding giant craft manuals or the entirety of a 50,000-word manuscript into a model's prompt causes catastrophic forgetting, severely degrades instruction following, and radically increases inference costs48. To mitigate this, context within the Muse domain must be strictly segregated into three tiers: Always-On, Reference, and Retrieved.

### **Always-On Prompt**

The always-on context must be minimal, highly deterministic, and present in every inference call. It includes the system persona, the immediate task instructions, absolute negative constraints (e.g., strict formatting rules), and the current contents of the active "scratchpad"21. The scratchpad acts as the working memory space shared by collaborating agents, containing only the most immediate state variables required for the current operation.

### **Reference Material**

Reference material is loaded into the context window conditionally, based entirely on which specific agent is invoked:

* **The Project Style Sheet:** Loaded exclusively for the Line Editor and Copyeditor. It contains character name spellings, hyphenation rules, and specific stylistic preferences that act as the authoritative "second brain" for consistency22.  
* **The Story Prototype:** A dual-knowledge-graph structure utilized by CreAgentive, consisting of a Role Graph (character attributes, relationship strength, and direction) and a Plot Graph (interconnected events and scenes). This is referenced exclusively by the Narrative Designer and Developmental Editor14.

### **Retrieved Context (Semantic RAG)**

Information that is too large for the context window must be retrieved dynamically using a Hybrid Retrieval-Augmented Generation (RAG) approach28.

* **Episodic Memory Summaries:** Instead of feeding raw past chapters to the Scene Drafter, a Context Coordinator agent dynamically compresses historical text into hierarchical episode summaries using TF-IDF and semantic similarity. It retrieves and injects only the entities and events immediately relevant to the current scene3.  
* **Craft Theory Retrieval:** Giant manuals by McKee, Truby, or Egri are never loaded in full. Instead, if the Developmental Editor identifies a pacing issue, it uses RAG to retrieve specific principles (e.g., "Scene versus Sequel dynamics" or "Thematic revelation") to inform its critique9.  
* **Dynamic State Tracking:** The Continuity Checker queries a symbolic logic database that tracks whether an item is currently "active," "lost," or "destroyed." If an agent generates text where a destroyed item reappears, the system flags the narrative entropy and forces an update, maintaining long-term continuity28.

## **Optimization for Weaker and Non-Frontier Models**

The primary design constraint of the Manurella Agentic Framework is ensuring high-fidelity output from weaker models like Kilo Code. Conventional generation relies heavily on the zero-shot reasoning capabilities of massive frontier models. To achieve parity, the architecture employs several scaffolding techniques.  
First, the system relies on the Skeleton-of-Thought (SoT) and Detailed Outline Control (DOC) paradigms36. Weaker models cannot sustain long-horizon reasoning. By forcing the Narrative Designer to generate a highly granular, sentence-level outline, the creative burden is shifted entirely to the planning stage36. The Scene Drafter is then only asked to expand a single, atomic outline point into a few paragraphs. This drastically reduces the cognitive load, preventing the model from having to simultaneously plan and write, thereby lowering hallucination rates36.  
Second, the architecture utilizes rigorous prompt chaining. Weaker models struggle with complex, multi-constraint prompts. By breaking tasks into sequential micro-prompts—for instance, first determining character emotion, then describing the setting, and finally generating the dialogue—the system ensures all constraints are met deterministically27.  
Finally, the system employs Task Duality Verification. To ensure a weaker model adhered to the provided outline, a reverse-process is employed. After generation, a separate summarizing agent extracts an outline from the newly generated text. If the extracted outline does not match the input outline provided by the Narrative Designer, the text is flagged for rejection and regeneration41.

## **Benchmark Tasks for Sub-Agents**

Evaluating creative writing artificial intelligence requires abandoning generic, one-size-fits-all rubrics. "Creative quality" cannot be flattened into a single score. Therefore, the framework proposes specific, multi-dimensional benchmark tasks for each major sub-agent1.

### **Narrative Designer Benchmarks**

Evaluated against the Torrance Test of Creative Writing (TTCW), specifically targeting the *Flexibility* (the ability to shift narrative perspectives) and *Originality* metrics39.

* **Benchmark Task:** Given a highly clichéd premise, the agent must generate a detailed outline featuring at least two non-linear temporal shifts (analepsis/prolepsis) and successfully subvert a known trope without violating logical consistency.

### **Continuity and Logic Checker Benchmarks**

Evaluated against the ConStory-Bench taxonomy1.

* **Benchmark Task:** Process 1,000 synthetic narratives containing known, planted errors across 19 fine-grained subtypes (e.g., Timeline Contradictions, Forgotten Abilities, Geographic Impossibilities). The agent is scored strictly on precision, recall, and the minimization of false positives1.

### **Line and Style Editor Benchmarks**

Evaluated using pairwise LLM-as-a-judge comparisons and Linguistic Style Similarity scoring against high-quality human reference texts45.

* **Benchmark Task:** Rewrite a generic 500-word scene utilizing the specific linguistic features, phrasal verbs, and syntactical rhythm of a target author profile. The output is measured via distance-based stylometric analysis to ensure the emulation matches the target without altering the underlying semantic meaning45.

### **Scene Drafter Benchmarks**

Evaluated on Narrative Entropy, *Fluency*, and *Elaboration* metrics28.

* **Benchmark Task:** Expand a highly constrained DOC event tuple into 800 words of prose without violating any injected negative constraints (e.g., "Do not reveal the protagonist's true motive to the reader").

## **Expansion Path: v0, v1, and v2**

To ensure sustainable development and systematic scaling, the Muse domain architecture is designed to be deployed across three distinct evolutionary phases.

### **v0: The Deterministic Pipeline**

The v0 architecture focuses on rigid, top-down execution utilizing structured prompt chaining27. It establishes the core agents (Orchestrator, Designer, Drafter, Editor) communicating via a text-based scratchpad21. State tracking is managed via simple text summarization, and outlines are static once approved. This phase proves the efficacy of the Detailed Outline Control framework and establishes basic continuity checking. It is designed to be highly stable and computationally inexpensive, relying primarily on text gradients and basic API routing.

### **v1: Dynamic State Tracking and Graph Memory**

The v1 expansion introduces the Memory-Enhancement Module (MEM) and formalizes the Story Prototype using Temporal Knowledge Graphs14. Agents will no longer rely solely on text summaries; they will query and update symbolic logic states natively. For example, if a character argues with an ally, the system updates the relationship metric in the Role Graph dynamically14. This phase also introduces multi-agent deliberation, allowing the Developmental Editor and the Narrative Designer to actively debate and revise outlines prior to drafting, simulating a professional writers' room33.

### **v2: Emergent Sandboxes and Multimodal Integration**

The v2 expansion transitions the framework into a complex hybrid architecture. While maintaining top-down narrative control to ensure structural integrity, it will introduce bottom-up sandbox simulations for micro-interactions. Character agents, instantiated with specific psychological profiles, will be allowed to "play out" a scene in a simulated environment. This generates emergent interactions that the Narrative Designer then curates and structures into the final plot30. Furthermore, v2 will integrate multimodal agents, expanding narrative design to include visual storyboarding, generative video alignment, and interactive spatial layouts, utilizing tools akin to the Vidmento system31. This represents the ultimate realization of the Muse domain: a comprehensive, multi-modal narrative engine capable of producing industry-standard creative properties autonomously.

#### **Works cited**

1. Lost in Stories: Consistency Bugs in Long Story Generation by LLMs \- arXiv, [https://arxiv.org/html/2603.05890v1](https://arxiv.org/html/2603.05890v1)  
2. \[2606.03698\] Multi$^2$: Hierarchical Multi-Agent Decision-Making with LLM-Based Agents in Interactive Environments \- arXiv, [https://arxiv.org/abs/2606.03698](https://arxiv.org/abs/2606.03698)  
3. StoryWriter: A Multi-Agent Framework for Long Story Generation \- arXiv, [https://arxiv.org/pdf/2506.16445](https://arxiv.org/pdf/2506.16445)  
4. Can Good Writing Be Generative? Expert-Level AI Writing Emerges through Fine-Tuning on High-Quality Books \- arXiv, [https://arxiv.org/html/2601.18353v1](https://arxiv.org/html/2601.18353v1)  
5. Narrative designer \- Wikipedia, [https://en.wikipedia.org/wiki/Narrative\_designer](https://en.wikipedia.org/wiki/Narrative_designer)  
6. Game Narrative Designer | FindSkill.ai — Learn AI for Your Job, [https://findskill.ai/skills/gaming-entertainment/game-narrative-designer/](https://findskill.ai/skills/gaming-entertainment/game-narrative-designer/)  
7. Narrative Game Design: Stories Players Actually Feel, [https://kevurugames.com/blog/unveiling-the-art-of-narrative-game-design-a-comprehensive-guide/](https://kevurugames.com/blog/unveiling-the-art-of-narrative-game-design-a-comprehensive-guide/)  
8. What Does a Narrative Designer Do? And How to Become One? \- Game Design Skills, [https://gamedesignskills.com/game-design/narrative-designer/](https://gamedesignskills.com/game-design/narrative-designer/)  
9. Robert McKee's Storytelling Principles | PDF | Genre | Narrative \- Scribd, [https://www.scribd.com/document/413835563/Robert-McKee-Notebook](https://www.scribd.com/document/413835563/Robert-McKee-Notebook)  
10. Story Substance Structure Style and The Principles of Screenwriting by Robert McKee | PDF, [https://www.scribd.com/doc/89125950/Story-Substance-Structure-Style-and-the-Principles-of-Screenwriting-by-Robert-McKee](https://www.scribd.com/doc/89125950/Story-Substance-Structure-Style-and-the-Principles-of-Screenwriting-by-Robert-McKee)  
11. Screenwriting Book Reading List | ScriptSerious, [https://scriptserious.com/book-reading-list/](https://scriptserious.com/book-reading-list/)  
12. Constella: Supporting Storywriters' Interconnected Character Creation through LLM-based Multi-Agents \- arXiv, [https://arxiv.org/html/2507.05820v1](https://arxiv.org/html/2507.05820v1)  
13. World Building in a Script \- Erik Bork, [https://www.flyingwrestler.com/2025/12/world-building-in-a-script/](https://www.flyingwrestler.com/2025/12/world-building-in-a-script/)  
14. CreAgentive: An Agent Workflow Driven Multi-Category Creative Generation Engine \- arXiv, [https://arxiv.org/html/2509.26461v1](https://arxiv.org/html/2509.26461v1)  
15. Developmental Editor vs. Copyeditor: Key Differences in Book Editing, [https://ghostwritingsolution.com/blog/developmental-editor-vs-copyeditor-key-differences-in-book-editing/](https://ghostwritingsolution.com/blog/developmental-editor-vs-copyeditor-key-differences-in-book-editing/)  
16. Types Of Editing: How To Choose \- Jericho Writers, [https://jerichowriters.com/types-of-editing-how-to-choose/](https://jerichowriters.com/types-of-editing-how-to-choose/)  
17. What Is Structural Editing? When You Need It \- Editor World, [https://www.editorworld.com/article/What-is-Structural-Editing](https://www.editorworld.com/article/What-is-Structural-Editing)  
18. How to Navigate the Four Stages of Book Editing: A Professional Editor's Guide, [https://www.firstediting.com/blogs/how-to-navigate-the-four-stages-of-book-editing-a-professional-editors-guide/](https://www.firstediting.com/blogs/how-to-navigate-the-four-stages-of-book-editing-a-professional-editors-guide/)  
19. (PDF) StoryWriter: A Multi-Agent Framework for Long Story Generation \- ResearchGate, [https://www.researchgate.net/publication/392917083\_StoryWriter\_A\_Multi-Agent\_Framework\_for\_Long\_Story\_Generation](https://www.researchgate.net/publication/392917083_StoryWriter_A_Multi-Agent_Framework_for_Long_Story_Generation)  
20. Narrative and Generative AI \- DOKUMEN.PUB, [https://dokumen.pub/narrative-and-generative-ai.html](https://dokumen.pub/narrative-and-generative-ai.html)  
21. agents' room: narrative generation through multi-step collaboration \- arXiv, [https://arxiv.org/pdf/2410.02603](https://arxiv.org/pdf/2410.02603)  
22. Blog \- E.S. Editing Services, [https://www.erikasteeves.com/blog.html](https://www.erikasteeves.com/blog.html)  
23. A Practical Guide To The 3 Stages Of Editing A Book \- Janey Burton, [https://janeyburton.com/the-stages-of-editing-a-book/](https://janeyburton.com/the-stages-of-editing-a-book/)  
24. Module I Editing 101 \- UBC Wiki, [https://wiki.ubc.ca/Module\_I\_Editing\_101](https://wiki.ubc.ca/Module_I_Editing_101)  
25. Why Every Novel Needs a Style Sheet \- Invisible Ink Editing, [https://www.invisibleinkediting.com/blog/resources-for-authors/why-every-novel-needs-a-style-sheet/](https://www.invisibleinkediting.com/blog/resources-for-authors/why-every-novel-needs-a-style-sheet/)  
26. Comparing line editing and copy editing: which one does your book need? \- BookBaby, [https://www.bookbaby.com/resources/line-editing-vs-copy-editing](https://www.bookbaby.com/resources/line-editing-vs-copy-editing)  
27. Co-Writing Screenplays and Theatre Scripts with Language Models An Evaluation by Industry Professionals \- arXiv, [https://arxiv.org/pdf/2209.14958](https://arxiv.org/pdf/2209.14958)  
28. arXiv:2503.23512v1 \[cs.CL\] 30 Mar 2025, [https://arxiv.org/pdf/2503.23512?](https://arxiv.org/pdf/2503.23512)  
29. \[2603.05890\] Lost in Stories: Consistency Bugs in Long Story Generation by LLMs \- arXiv, [https://arxiv.org/abs/2603.05890](https://arxiv.org/abs/2603.05890)  
30. StoryBox: Collaborative Multi-Agent Simulation for Hybrid Bottom-Up Long-Form Story Generation Using Large Language Models \- arXiv, [https://arxiv.org/html/2510.11618v3](https://arxiv.org/html/2510.11618v3)  
31. awesome-llm-story-generation/README\_zh.md at main \- GitHub, [https://github.com/Picrew/awesome-llm-story-generation/blob/main/README\_zh.md](https://github.com/Picrew/awesome-llm-story-generation/blob/main/README_zh.md)  
32. Hybrid Bottom-Up Multi-Agent Narrative Generation \- Emergent Mind, [https://www.emergentmind.com/topics/hybrid-bottom-up-multi-agent-narrative-generation](https://www.emergentmind.com/topics/hybrid-bottom-up-multi-agent-narrative-generation)  
33. Plug-and-Play Dramaturge: A Divide-and-Conquer Approach for Iterative Narrative Script Refinement via Collaborative LLM Agents \- arXiv, [https://arxiv.org/html/2510.05188v2](https://arxiv.org/html/2510.05188v2)  
34. SCORE: Story Coherence and Retrieval Enhancement for AI Narratives \- arXiv, [https://arxiv.org/html/2503.23512v6](https://arxiv.org/html/2503.23512v6)  
35. google-deepmind/dramatron: Dramatron uses large language models to generate coherent scripts and screenplays. \- GitHub, [https://github.com/google-deepmind/dramatron](https://github.com/google-deepmind/dramatron)  
36. Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation \- arXiv, [https://arxiv.org/html/2307.15337v3](https://arxiv.org/html/2307.15337v3)  
37. \[2212.10077\] DOC: Improving Long Story Coherence With Detailed Outline Control \- arXiv, [https://arxiv.org/abs/2212.10077](https://arxiv.org/abs/2212.10077)  
38. STORYWRITER：长篇故事生成的多智能体框架 \- 51CTO, [https://www.51cto.com/article/819372.html](https://www.51cto.com/article/819372.html)  
39. Torrance Test of Creative Writing (TTCW) \- Emergent Mind, [https://www.emergentmind.com/topics/torrance-test-of-creative-writing-ttcw](https://www.emergentmind.com/topics/torrance-test-of-creative-writing-ttcw)  
40. Generating Long-form Story Using Dynamic Hierarchical Outlining with Memory-Enhancement \- arXiv, [https://arxiv.org/html/2412.13575v1](https://arxiv.org/html/2412.13575v1)  
41. Advancing Precise Outline-Conditioned Text Generation with Task Duality and Explicit Outline Control \- Hari Sundaram, [http://sundaram.cs.illinois.edu/pubs/2024/2024\_li\_precise\_eacl.pdf](http://sundaram.cs.illinois.edu/pubs/2024/2024_li_precise_eacl.pdf)  
42. Advancing LLM-Based Methods for Poetry Generation and Automated Evaluation \- Kent Academic Repository, [https://kar.kent.ac.uk/112926/1/74sawicki2026phdfinal.pdf](https://kar.kent.ac.uk/112926/1/74sawicki2026phdfinal.pdf)  
43. Types of Editing: A Breakdown for Writers (With Examples) \- Reedsy, [https://reedsy.com/blog/guide/editing/](https://reedsy.com/blog/guide/editing/)  
44. SCORE: Story Coherence and Retrieval Enhancement for AI Narratives \- arXiv, [https://arxiv.org/html/2503.23512v2](https://arxiv.org/html/2503.23512v2)  
45. Individualized Cognitive Simulation in Large Language Models: Evaluating Different Cognitive Representation Methods \- arXiv, [https://arxiv.org/html/2510.20252v1](https://arxiv.org/html/2510.20252v1)  
46. Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation | Digital Scholarship in the Humanities | Oxford Academic, [https://academic.oup.com/dsh/article/40/2/587/8118784](https://academic.oup.com/dsh/article/40/2/587/8118784)  
47. Automated Creativity Evaluation for Large Language Models: A Reference-Based Approach \- ACL Anthology, [https://aclanthology.org/2025.findings-emnlp.1171.pdf](https://aclanthology.org/2025.findings-emnlp.1171.pdf)  
48. A Multi-Agent LLM Framework with Hierarchical Citation Graph for Automated Survey Generation \- arXiv, [https://arxiv.org/html/2510.07733v3](https://arxiv.org/html/2510.07733v3)  
49. MUSR: TESTING THE LIMITS OF CHAIN-OF-THOUGHT WITH MULTISTEP SOFT REASONING \- OpenReview, [https://openreview.net/pdf?id=jenyYQzue1](https://openreview.net/pdf?id=jenyYQzue1)  
50. CreAgentive: Agent-Driven Narrative Engine \- Emergent Mind, [https://www.emergentmind.com/topics/creagentive-system](https://www.emergentmind.com/topics/creagentive-system)  
51. 19th Conference of the European Chapter of the Association for Computational Linguistics, [https://aclanthology.org/events/eacl-2026/](https://aclanthology.org/events/eacl-2026/)  
52. \[2209.14958\] Co-Writing Screenplays and Theatre Scripts with Language Models: An Evaluation by Industry Professionals \- arXiv, [https://arxiv.org/abs/2209.14958](https://arxiv.org/abs/2209.14958)  
53. DeepWriter: A Multi-Agent Collaboration Framework for Information-rich Ultra-long Book Writing, [https://ojs.aaai.org/index.php/AAAI/article/view/40648/44609](https://ojs.aaai.org/index.php/AAAI/article/view/40648/44609)  
54. Vidmento: Creating Video Stories Through Context-Aware Expansion With Generative Video, [https://arxiv.org/html/2601.22013v2](https://arxiv.org/html/2601.22013v2)