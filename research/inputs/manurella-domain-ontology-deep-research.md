# Manurella Domain Ontology for a Runtime-Agnostic Cognitive Agent Framework

## Executive conclusion

The strongest evidence does **not** support treating **Build, Muse, Pixel, and Mentor** as Manurella’s stable top-level ontology. That scheme mixes at least four different kinds of things: a likely domain pack (**Build**), a creative ideation stance (**Muse**), a medium/craft specialization (**Pixel**), and an instructional persona or workflow (**Mentor**). Cognitive-architecture research argues for separating internal faculties such as memory, action selection, and planning from task domains; domain-driven design argues for stable bounded contexts rather than one giant undifferentiated model; and modern benchmark science shows that research, coding, web/OS action, creative production, and tutoring each require materially different tools, risks, and evaluation suites. citeturn10search3turn0search8turn1search5turn4search7turn4search0turn4search1turn2search11turn16search13

**Recommended project hypothesis:** Manurella should use a **layered, hybrid-compositional ontology** with a small stable kernel, universal cognitive faculties, reusable shared capabilities, and **five top-level domain packs**: **Inquiry, Engineering, Authoring, Operations, and Learning**. This is the smallest set I can justify that still cleanly separates distinct work objects, permissions, risk envelopes, toolchains, and benchmark baskets. It also keeps the ontology maintainable: domain packs stay few, while most growth happens through subdomains, workflows, personas, tool adapters, and evaluation recipes rather than through endless new “agents.” citeturn10search3turn1search5turn9search3turn9search6turn9search1turn0search2turn15search0

Under this design, **Build** should survive only as a product-facing alias for a narrower internal domain called **Engineering**. **Pixel** should be demoted to a **visual subdomain and medium pack** under **Authoring**. **Muse** should be treated as a **universal ideation capability** plus an optional **creative-director persona**, not a domain. **Mentor** should be treated as an **instructional persona/workflow** anchored primarily in the **Learning** domain pack, while remaining composable with any content domain. That placement best fits the evidence on bounded contexts, information architecture, modality-specific evaluation, and learning science. citeturn1search5turn7search10turn13search1turn13search0turn13search14turn5search0turn5search1turn5search10

A second strong conclusion is architectural: **domains are not runtimes, and effort tiers are not domains**. MCP servers, A2A peers, queues, traces, checkpointers, and model providers belong to runtime infrastructure and orchestration. “Low, Medium, High, Max, Ultra, private Sentient” belong to an **execution-policy axis** that controls compute budget, search breadth, verification depth, and approval requirements. Benchmarks such as BrowseComp show test-time compute can materially change results, while recent work also shows that more agents or more coordination only help on some tasks and can degrade performance or efficiency on others when budgets are equalized. This makes it dangerous to equate “more specialized agents” with “better architecture.” citeturn20search4turn19search1turn19search12turn12search0turn12search3turn18search12turn3search8turn15search1

**Safe decisions to adopt now:**  
use a layered ontology; cap stable top-level domain packs at five; keep knowledge graphs, provenance, routing, verification, and governance as shared cross-domain capabilities; model workflows and personas separately from domains; and build the Framework Atlas on open semantic standards such as RDF, SKOS, OWL, SHACL, SPARQL, and PROV-O. citeturn0search1turn9search1turn9search0turn0search2turn6search8turn15search0

**Decisions that still require experiments:**  
whether **Authoring** should remain one top-level pack or later split into **Document/Narrative** and **Visual/Audiovisual**; whether **Operations** should absorb more personal-assistant functions; whether internal multi-agent decomposition meaningfully beats a strong single-agent planner on Manurella’s own task mix; and whether **Learning** should remain top-level once production telemetry is available. citeturn13search14turn13search1turn13search0turn19search1turn19search12turn16search13

## Terminology and layer model

This report uses four evidence labels. **Evidence** means directly grounded in cited research papers, standards, benchmarks, or first-party technical documents. **Inference** means a conclusion logically drawn from multiple sources. **Project hypothesis** means a concrete design recommendation for Manurella that is justified but still unproven in this product. **Speculation** means a longer-term possibility that should not harden into ontology yet. That distinction matters because ontology mistakes are expensive: they distort routing, evaluation, permissions, and maintainability long before they show up in UI. Ontology engineering guidance has long emphasized defining domain scope, competency questions, reuse strategy, and maintenance responsibility up front rather than treating taxonomy as branding. citeturn9search3turn9search6turn1search4

### Layer definitions

The cleanest model for Manurella is a stack in which each layer answers a different design question.

| Layer | What it defines | What it must not define | Basis |
|---|---|---|---|
| **Runtime infrastructure** | models, inference providers, queues, tracing, persistence, MCP/A2A adapters, schedulers, human-approval hooks | user-facing domains | Evidence + inference from MCP, A2A, OpenTelemetry, ports/adapters docs. citeturn18search12turn3search8turn15search12turn8search9 |
| **Kernel** | planner/router, state model, policy engine, provenance ledger, evaluation loop, pack registry | medium brands or personas | Inference from cognitive-architecture separation of memory/action/decision and runtime decoupling patterns. citeturn10search3turn10search0turn11search1turn8search9 |
| **Cognitive faculties** | perceive, remember, reason, act, verify, learn/adapt | task domains | Evidence from CoALA, Soar, ACT-R, LIDA. citeturn10search3turn10search0turn11search1turn10search2 |
| **Shared capabilities** | reusable services built from faculties: search, retrieval, verification, translation, KG lookup, tutoring moves, style transfer, planning, policy checks | stable top-level routing labels | Inference. The same capabilities recur across benchmark families and domains. citeturn4search0turn4search1turn13search1turn16search13 |
| **Domain packs** | bounded contexts with distinct work objects, tools, permissions, risks, memory schemas, and benchmark baskets | UI personalities, raw runtimes, or compute tiers | Evidence + inference from DDD, ontology engineering, and benchmark separation. citeturn1search5turn9search3turn4search7 |
| **Workflows** | task recipes composed from capabilities and packs | long-lived ontology roots | Inference. Most user requests are workflow-shaped, not domain-pure. citeturn4search0turn2search11turn2search3 |
| **Interface personas** | interaction style, explanation mode, tone, coaching stance, initiative policy | capability boundaries or permissions | Evidence from IA/HCI and learning science. citeturn7search3turn7search2turn5search0turn5search10 |
| **Tools** | external actions and data access: web, files, code runtimes, design systems, calendars, CRMs, IDEs, shells | domain semantics by themselves | Evidence from tool-augmented LM and MCP docs. citeturn2search1turn18search12turn3search1 |

### Stable ontology principle

The ontology should be anchored in **external work objects and commitments**, not in internal cognitive moves and not in fashionable agent counts. That principle follows directly from bounded-context thinking and from the failure of broad one-score benchmarks. A user request such as “research new CRM vendors and draft a slide deck” is not asking for “memory + reasoning + writing + image.” It is asking for a workflow that crosses evidence gathering, comparison, narrative synthesis, and presentation authoring. The ontology should therefore expose a **primary domain anchor** and then compose secondary capabilities. citeturn1search5turn4search7turn4search0turn13search14

### Semantic substrate for the Framework Atlas

For a live Framework Atlas, the substrate should be **RDF 1.2** for graph data, **SKOS** for labels and hierarchical concept schemes, **OWL 2** for formal semantics, **SHACL** for validation and machine-consumable shapes, **SPARQL 1.2** for query access, and **PROV-O** for provenance. SHACL is especially valuable because it supports validation and, increasingly, generation of interfaces, code, and inferencing rules from explicit shapes; PROV-O gives a standard way to track claims, activities, agents, and evidence; and OpenTelemetry gives runtime traces that can be linked back into the Atlas. citeturn0search1turn9search1turn9search0turn0search2turn0search14turn6search8turn15search0turn15search1

## Competing ontology models and why most fail

### Comparison matrix

| Decomposition model | Canonical examples | Strengths | Weaknesses | Adversarial verdict |
|---|---|---|---|---|
| **Medium or craft based** | text, code, image, audio, video | Easy local tool mapping; good for renderer/editor selection; matches creative-generation benchmarks like GenEval and VBench and coding benchmarks like SWE-bench. citeturn13search1turn13search0turn4search1 | Fragments user intent across media; duplicates planning, grounding, memory, and verification; creates routing ambiguity on mixed-medium requests. | Useful as **subdomain/media packs**, bad as top level. |
| **Human-outcome based** | research, build, publish, operate, teach | More aligned with how users phrase work; clearer benchmark baskets; better bounded contexts. GAIA, WebArena, OSWorld, SWE-bench, and TutorBench all reflect outcome-rich work rather than single modalities. citeturn4search0turn2search11turn2search3turn4search1turn16search13 | Some requests still span outcomes; labels can become fuzzy unless domains are tied to work objects and permissions. | Best candidate for top-level packs. |
| **Cognitive-function based** | memory, planning, reasoning, verification, acting | Closest to cognitive architecture and useful for internal design and evaluation of faculties. citeturn10search3turn10search0turn11search1turn10search2 | Terrible for user routing because nearly every serious task uses several faculties at once. | Correct for the **kernel**, wrong for user-facing domain ontology. |
| **Hybrid compositional** | top-level outcome packs + cross-cutting faculties + media/persona/workflow facets | Best at avoiding duplication; preserves runtime agnosticism; supports semantic Atlas modeling and plugin-style extensibility. citeturn1search5turn9search6turn0search2turn15search0 | Higher governance burden; weak teams can let it decay into ontology sprawl. | Recommended, with strict pack-boundary tests. |

### Evidence and counterarguments

The attraction of a medium-based model is real. Image, video, and music generation do have distinct evaluators and failure surfaces: GenEval probes compositional image alignment, VBench breaks video quality into fine-grained dimensions, and music-generation evaluation increasingly requires human-preference-aligned metrics. Code generation has its own execution-based testing culture through SWE-bench. So a purely medium-based taxonomy will look superficially “clean” to builders because tools and benchmarks line up neatly. citeturn13search1turn13search0turn13search3turn4search1

The problem is that users rarely think in those boxes, and neither do real tasks. A market-research brief that ends in a memo, slide deck, and spreadsheet would touch text, tables, charts, and possibly images, but its unifying success criterion is **evidence-backed decision support**, not medium mastery. Likewise, a front-end implementation based on a visual mockup is ultimately judged by executable behavior, tests, and integration, not by “pixels” alone. Medium-based top levels therefore optimize the wrong axis. They organize renderers, not work. That is a classic information-architecture mistake: good IA must optimize organization, labeling, navigation, and search around user wayfinding, not around internal production silos. citeturn4search0turn2search11turn4search1turn7search10turn7search2

A cognitive-function model has the opposite problem. It is theoretically elegant. CoALA, Soar, ACT-R, and LIDA all emphasize recurring internal modules such as memory, action selection, and learning, and those distinctions are exactly what a runtime kernel needs. But a user should almost never route manually to “memory,” “verification,” or “planning.” Those are faculties, not bounded work domains. If Manurella exposes them as top-level families, routing ambiguity will explode because every hard request requires more than one. citeturn10search3turn10search0turn11search1turn10search2

The best-supported answer is therefore a **hybrid compositional architecture**: outcome-centered domain packs at the top; cognitive faculties and shared capabilities below them; and media, personas, workflows, and runtimes modeled as orthogonal facets. This is the only decomposition I found that is consistent with cognitive-architecture literature, semantic-web standards, DDD bounded contexts, real tool protocols, and the current benchmark landscape. The counterargument is that hybrid systems can become ungovernable. I agree. That is why Manurella needs explicit creation/split/merge/retire tests rather than intuition-driven taxonomy growth. citeturn10search3turn1search5turn9search6turn18search12turn3search8turn4search7

## Recommended top-level architecture

### Recommended domain packs

**Project hypothesis:** Manurella’s stable top-level domain packs should be **Inquiry, Engineering, Authoring, Operations, and Learning**.

| Domain pack | Core work object | Typical terminal success condition | Why it deserves top-level status | Representative benchmarks |
|---|---|---|---|---|
| **Inquiry** | claims, evidence sets, options, analyses, decisions | factual adequacy, citation quality, reasoning, decision usefulness | Open-web and multimodal evidence gathering has distinct tools and evaluation pressure in GAIA, BrowseComp, BrowseComp-Plus, MMMU, HLE, and MMLU-Pro. citeturn4search0turn16search3turn20search1turn4search2turn20search0turn16search2 | GAIA, BrowseComp, BrowseComp-Plus, MMMU, HLE, MMLU-Pro |
| **Engineering** | executable systems, codebases, automations, tests, schemas | code correctness, build success, regression pass rate, system behavior | Software tasks require write access, execution, test oracles, and repository memory unlike ordinary authoring. citeturn4search1turn2search3turn2search2 | SWE-bench, OSWorld, AgentBench |
| **Authoring** | communicative and creative artifacts for humans | artifact quality, adherence to brief, composition, style, clarity, audience fit | Writing, image, video, and audiovisual creation share human-facing artifact semantics yet use distinct subdomain evaluators. citeturn13search14turn13search1turn13search0 | WritingBench, GenEval, VBench, CMI-Bench |
| **Operations** | tasks, transactions, schedules, workflows, external system state | correct completion of real-world actions with policy compliance | Web/desktop/computer-use environments create a distinct action space and safety surface. citeturn2search11turn2search3turn17search1turn17search7 | WebArena, OSWorld, AgentBench, SafeArena, AgentDojo |
| **Learning** | learner state, misconceptions, practice plans, feedback loops | learning gain, appropriate explanation, adaptive scaffolding, mastery progression | Tutoring is not just “explaining nicely”; it requires diagnostic pedagogy, scaffolding, and learner modeling supported by learning-science literature and tutoring benchmarks. citeturn5search0turn5search1turn5search10turn16search13turn16search17 | TutorBench, MathTutorBench, human learning-outcome studies |

The crucial choice here is **Authoring** instead of “Media” or “Creative.” “Media” would drag the ontology back toward medium-based decomposition. “Creative” would overfit to one subset of output work and underfit ordinary business documents, presentations, briefs, and persuasive writing. “Authoring” is broader and cleaner: it denotes human-facing artifact production across text, slides, visual design, audio, and video while remaining distinct from engineering of executable systems. That distinction is defensible because their toolchains, permissions, and benchmark cultures are genuinely different. citeturn13search14turn13search1turn13search0turn4search1

### Domain and capability decision table

| Candidate | Recommended classification | Decision | Rationale |
|---|---|---|---|
| **Build** | **Top-level alias only if narrowed; internal pack = Engineering** | Keep, but rename internally | “Build” is too broad in plain English; it can mean code, decks, brands, or plans. Internally it should mean executable technical systems only. citeturn1search5turn7search10turn4search1 |
| **Muse** | **Universal capability + optional persona** | Demote from domain | Ideation, divergence, reframing, and variation are cross-domain behaviors. They help Inquiry, Authoring, Learning, and sometimes Engineering, but do not define a bounded context. citeturn10search3turn13search14turn5search0 |
| **Pixel** | **Subdomain/media pack under Authoring** | Demote from top level | Pixel is visual craft, not a domain of work. It should route to image/layout/render/edit pipelines while inheriting shared authoring policies. citeturn13search1turn13search0 |
| **Mentor** | **Persona + workflow anchored to Learning** | Demote from top level | Effective tutoring needs pedagogy-specific state and assessment, but “mentor” is still a stance and interaction policy, not the ontology root. citeturn16search13turn5search0turn5search10 |
| **Research** | **Subdomain of Inquiry** | Include | Research is central but narrower than Inquiry, which also covers analysis, comparison, explanation, and decision support. citeturn4search0turn16search3 |
| **Analysis** | **Subdomain of Inquiry** | Include | Distinct deliverables but same evidence-centered bounded context. citeturn4search7turn16search2 |
| **Communication** | **Workflow and subdomain of Authoring** | Include, not top level | Communication artifacts exist across all domains; making it top-level would duplicate Authoring and Learning heavily. citeturn13search14turn7search10 |
| **Planning** | **Workflow** | Include | Planning appears in everything from operations to tutoring; it is not a bounded context. citeturn10search3turn2search0 |
| **Verification** | **Universal capability** | Include | ReAct, SWE-bench, AgentDojo, and provenance standards all show checking must recur across domains. citeturn2search0turn4search1turn17search1turn15search0 |
| **Memory** | **Universal capability / infrastructure** | Include | Memory is architectural, not domainal. citeturn10search3turn10search0turn11search1 |
| **Knowledge graph** | **Shared semantic capability** | Include | Useful for durable knowledge, provenance, and Atlas discovery; should not swallow all working memory. citeturn0search1turn9search1turn15search0turn6search5 |
| **Governance** | **Universal capability** | Include | Safety, policy, and compliance apply to every action-taking pack. citeturn3search2turn14search0turn14search1turn3search3 |
| **Personal assistant** | **Scope/profile, not domain** | Include as profile | “Personal-first” is a scope and memory partitioning strategy, not a work domain. |
| **Multi-agent** | **Workflow/infrastructure strategy** | Include, not top level | Coordination patterns are execution choices. Do not encode them as domains. citeturn12search0turn19search1turn19search12 |
| **Finance/legal/health specialist** | **Deferred vertical packs** | Defer | High-value, but require domain policies and regulated benchmark design beyond the core ontology. citeturn14search0turn3search2 |

### Placement analysis for Build, Muse, Pixel, and Mentor

**Build** belongs in the ontology only if it stops pretending to cover all making. The evidence from SWE-bench, OSWorld, AgentBench, and MCP/runtime docs is overwhelming: software and automation work have distinct action spaces, write permissions, test oracles, repository memory, and safety implications. That justifies a top-level pack. But the internal name should be **Engineering**, because “Build” is too semantically overloaded for precise routing. If the product team loves the name, keep it as a surface label and map it to `domain_pack: engineering`. citeturn4search1turn2search3turn2search2turn18search12

**Muse** should not survive as a domain. Ideation is a mode, not a bounded context. It shows up in creative writing, concept generation, product invention, research hypothesis formation, lesson design, and strategic option creation. In cognitive terms, it is a composition of divergent search, analogy, variation, and critique; in product terms, it is a configurable persona and workflow. Making it top-level would guarantee duplication across Inquiry, Authoring, and Learning. citeturn10search3turn13search14turn5search0

**Pixel** is even more clearly not top-level. Modern visual work is important, but benchmark science already distinguishes it as a modality-specialized subspace: GenEval focuses on compositional text-image alignment; VBench decomposes video quality into motion, stability, and relational dimensions. Those are specialized authoring evaluators, not reasons to create a separate root family parallel to research, engineering, and operations. Pixel should therefore live at `authoring.visual`. citeturn13search1turn13search0

**Mentor** is trickier because learning science really does justify a distinct bounded context. Bloom’s tutoring literature, cognitive apprenticeship, worked-example research, and self-regulated learning models all point to tutoring behaviors that are not interchangeable with generic explanation. TutorBench and MathTutorBench strengthen that case. The mistake is not to create a learning pack; the mistake is to confuse **Learning** with **Mentor**. “Mentor” is how the system interacts. **Learning** is what the bounded context is about. citeturn5search1turn5search0turn5search3turn5search10turn16search13turn16search17

### Missing-domain analysis

The original family misses at least two top-level packs that general human-AI work requires.

**Inquiry** is missing, and that omission is serious. GAIA, BrowseComp, BrowseComp-Plus, MMMU, HLE, and MMLU-Pro together capture a large basin of value: research, fact finding, multimodal evidence interpretation, option comparison, and decision support. Without a first-class Inquiry pack, those tasks would be forced into either “Muse” or “Mentor,” which is semantically wrong, or into “Build,” which is worse. citeturn4search0turn16search3turn20search1turn4search2turn20search0turn16search2

**Operations** is also missing, and it is the other major gap. WebArena and OSWorld show that web and computer-use tasks form a distinct regime of action, memory, and risk. AgentDojo and SafeArena show that this regime also has a distinct threat model, especially around prompt injection, malicious task misuse, and unsafe tool use. If Manurella intends to coordinate calendars, email, browser work, CRMs, spreadsheets, desktop tools, or external services, Operations has to exist as a first-class pack. citeturn2search11turn2search3turn17search1turn17search7

The more debatable candidate is **Learning**. A skeptical view would say it can be modeled as Authoring plus Inquiry plus a Mentor persona. I reject that for now. The pedagogical literature and the 2025 tutoring benchmarks suggest distinct learner-state representations, error-diagnosis moves, and adaptation strategies that justify a separate pack. Still, this is a place where telemetry should eventually confirm or falsify the design. citeturn5search0turn5search1turn5search10turn16search13turn16search17

### Cross-domain routing model

Routing should follow a **single-anchor, multi-capability** rule:

1. Identify the **terminal work object** and **dominant success criterion**.  
2. Choose one **anchor domain pack**.  
3. Attach secondary capabilities, subdomains, and media/persona facets.  
4. Use subagents only when subtasks are separable and the benefits outweigh coordination cost. citeturn1search5turn12search0turn19search1turn19search12

| Request type | Anchor pack | Secondary composition |
|---|---|---|
| “Research competitors and write a recommendation memo.” | Inquiry | Authoring.document + verification + evidence grounding |
| “Turn this mockup into a working React app.” | Engineering | Authoring.visual as input interpreter + verification/tests |
| “Create a campaign concept and render ad variations.” | Authoring | Muse persona + Inquiry for audience data + Pixel subdomain |
| “Teach me calculus using mistakes from my last homework.” | Learning | Inquiry.math content + Mentor persona + assessment workflow |
| “Book travel, handle rescheduling, and email the itinerary.” | Operations | Authoring.document + governance + approval checkpoints |
| “Analyze our CRM options, then configure a trial workspace.” | Operations if execution is requested; Inquiry if recommendation only | Inquiry or Operations respectively, with shared evidence ledger |

This routing rule cuts ambiguity because it forces Manurella to ask, implicitly: **What world state will be judged when the task is done?** If the answer is “a decision memo with justified evidence,” anchor Inquiry. If it is “a running system,” anchor Engineering. If it is “a human-facing artifact,” anchor Authoring. If it is “a changed external system state,” anchor Operations. If it is “improved learner understanding,” anchor Learning. That criterion is more stable than topic, medium, or persona. citeturn1search5turn4search0turn4search1turn2search11turn16search13

### Domain creation, split, merge, and retirement tests

These are **project hypotheses**, but they are the kind Manurella should formalize early.

| Governance action | Objective trigger |
|---|---|
| **Create new top-level domain** | Candidate cluster has a distinct work object, a distinct tool-permission-risk envelope, at least one separable benchmark basket, and improves quality by **≥ 8 points** or reduces cost/latency by **≥ 25%** versus composition within existing packs. |
| **Split a domain** | Internal routing confusion exceeds **15%**, tool overlap between subclusters falls below **50%**, or risk policies diverge enough that shared defaults become unsafe or misleading. |
| **Merge domains** | Benchmark baskets substantially overlap, shared tools exceed **70%**, and specialization yields **< 5-point** quality lift over a merged pack. |
| **Retire a domain** | Traffic share remains **< 3%** for two release cycles and no benchmark or policy evidence shows a meaningful gain over representing it as a workflow, persona, or subdomain. |

The numeric thresholds are not handed down by literature, but the logic is: bounded contexts are justified by consistency boundaries, ontology engineering by competency questions and maintenance scope, and evaluation science by discriminative measurement rather than branding. These thresholds operationalize those ideas. citeturn1search5turn9search3turn9search6turn4search7

### Effort tiers and why they must stay orthogonal

**Low, Medium, High, Max, Ultra, and private Sentient** should not become de facto domain labels. They should be stored as **execution-policy profiles** that change search depth, verification loops, simulation count, human approval requirements, and compute budget. BrowseComp explicitly highlights test-time compute scaling, and recent work on multi-agent versus single-agent systems shows that gains often depend more on budget and task parallelizability than on ontological specialization. citeturn20search4turn19search1turn19search12

A sensible operating model is:

| Tier | Expected behavior |
|---|---|
| **Low** | minimal planning, one-pass draft, lightweight retrieval, no expensive external verification |
| **Medium** | structured plan, modest retrieval, one verification pass |
| **High** | broader search, cross-source reconciliation, tests or critiques, provenance bundle |
| **Max** | adversarial checks, multiple retrieval or test rounds, stronger approval gates for actions |
| **Ultra** | exhaustive or near-exhaustive search/test regimes, simulation-heavy workflows, benchmark mode |
| **private Sentient** | internal experimental tier only; isolated environments, maximum traceability, no ontology semantics attached |

That separation prevents a common failure mode: users learning that “Ultra means research” or “Build means high effort.” It should never mean that. Any pack may run at any tier subject to policy. citeturn20search4turn17search1turn17search4

### Extensibility model and implications for the Framework Atlas

New domains should arrive as **pack manifests**, not kernel edits. Each pack should publish:

- semantic identifiers and labels in **SKOS/OWL**  
- capability dependencies and shapes in **SHACL**  
- tool ports and permission requirements  
- risk classifications and policies  
- benchmark recipes and quality gates  
- provenance schemas in **PROV-O**  
- optional personas and workflow templates. citeturn9search1turn9search0turn0search2turn15search0

That design turns the Framework Atlas into a live ontology browser rather than a static diagram. The Atlas should support four views, matching classic information-architecture practice: **organization** by domain/capability/tool/risk/benchmark, **labeling** with human-readable aliases, **navigation** across dependencies and compositions, and **search/facet filtering** for discovery. Good IA matters here because ontology failure is often not logical failure but discoverability failure. citeturn7search10turn7search3turn7search2

### Machine-readable draft tree

```yaml
manurella:
  version: "v0-draft"
  ontology_kind: "hybrid-compositional"
  kernel:
    planner_router:
      responsibilities:
        - anchor_domain_selection
        - workflow_composition
        - effort_tier_assignment
        - approval_checkpoint_insertion
    state_and_provenance:
      standards:
        - RDF_1_2
        - PROV_O
        - SHACL
        - SKOS
      stores:
        - working_state
        - durable_memory
        - evidence_graph
        - benchmark_history
    policy_engine:
      responsibilities:
        - permission_scoping
        - risk_classification
        - safety_rules
        - compliance_profiles
    evaluation_loop:
      responsibilities:
        - benchmark_execution
        - trace_auditing
        - regression_detection
        - continuous_improvement
    runtime_ports:
      protocols:
        - MCP
        - A2A
        - HTTP
        - queues
        - model_provider_adapters
        - OpenTelemetry
  cognitive_faculties:
    - perceive_intake
    - remember_retrieve
    - model_plan
    - synthesize_construct
    - act_execute
    - verify_critique
    - adapt_learn
    - govern_protect
  shared_capabilities:
    evidence_grounding:
      includes: [search, citation_management, claim_tracking, provenance]
    memory:
      includes: [episodic, semantic, task_state, user_profile]
    verification:
      includes: [tests, fact_checking, self_critique, adversarial_review]
    multimodal_transformation:
      includes: [text, tables, images, audio, video, slides]
    coordination:
      includes: [subtasking, handoffs, A2A_federation, approval_workflows]
    pedagogy_moves:
      includes: [diagnosis, scaffolding, worked_examples, mastery_tracking]
    style_and_persona:
      includes: [mentor, critic, muse, operator, analyst]
  domain_packs:
    inquiry:
      subdomains:
        - research
        - analysis
        - decision_support
        - explanation
        - forecasting
    engineering:
      aliases: [build]
      subdomains:
        - software
        - automations
        - data_systems
        - testing
        - infrastructure
    authoring:
      subdomains:
        - document_narrative
        - presentation
        - visual   # alias: pixel
        - audio
        - video
        - brand_content
    operations:
      subdomains:
        - calendar_email
        - browser_workflows
        - spreadsheets_records
        - project_coordination
        - service_orchestration
    learning:
      subdomains:
        - tutoring
        - coaching
        - assessment
        - curriculum_design
        - practice_feedback
  workflows:
    - inquire_then_brief
    - analyze_then_recommend
    - design_then_build
    - teach_then_assess
    - plan_then_execute
    - create_then_publish
  personas:
    - analyst
    - mentor
    - muse
    - critic
    - operator
    - concierge
  effort_tiers:
    - low
    - medium
    - high
    - max
    - ultra
    - private_sentient
```

## Benchmark coverage, risks, and failure modes

### Benchmark coverage matrix and the 80-point gate

A single benchmark score would be a profound mistake. HELM’s central argument is that useful evaluation needs broad scenario and metric coverage, and the current agent literature reinforces that point. Manurella should therefore gate quality with a **weighted basket**, not a leaderboard fetish. citeturn4search7turn4search11turn1search7

**Recommended minimum release gate:** **80/100 overall**, with **no domain-relevant safety or correctness subscore below 70**, and with **action-taking domains requiring safety/policy ≥ 85**.

| Dimension | Weight | Notes |
|---|---:|---|
| Task success / artifact correctness | 30 | execution-based where possible |
| Evidence quality / grounding / citation fidelity | 15 | mandatory for Inquiry and any evidence-bearing outputs |
| Verification / self-correction | 10 | tests, consistency checks, adversarial review |
| Safety / policy / permission compliance | 15 | hard gate for Operations and Engineering |
| User-fit / pedagogy / IA / usefulness | 10 | audience fit, clarity, instructional quality, navigability |
| Robustness / cross-domain composition | 10 | mixed workflows, noisy inputs, tool failures |
| Efficiency / cost / latency | 10 | budget-aware, tier-aware |

### Suggested benchmark basket by pack

| Domain pack | Primary benchmark coverage | What it catches |
|---|---|---|
| **Inquiry** | GAIA; BrowseComp; BrowseComp-Plus; MMMU; HLE; MMLU-Pro citeturn4search0turn16search3turn20search1turn4search2turn20search0turn16search2 | open-world research, browsing persistence, multimodal evidence reasoning, high-difficulty subject reasoning |
| **Engineering** | SWE-bench; OSWorld; AgentBench citeturn4search1turn2search3turn2search2 | repository-scale fixes, computer-use execution, interactive coding/action tasks |
| **Authoring** | WritingBench; GenEval; VBench; CMI-Bench citeturn13search14turn13search1turn13search0turn13search11 | writing quality, image composition, video generation fidelity, music instruction following |
| **Operations** | WebArena; OSWorld; AgentBench; MultiAgentBench; SafeArena; AgentDojo citeturn2search11turn2search3turn2search2turn12search3turn17search7turn17search1 | web tasks, desktop tasks, coordination, misuse risk, prompt-injection exposure |
| **Learning** | TutorBench; MathTutorBench; human pedagogical rubrics grounded in tutoring science citeturn16search13turn16search17turn5search0turn5search1turn5search10 | adaptive explanations, feedback quality, support for active learning, pedagogical dialog |
| **Cross-cutting** | HELM; AgentDojo; OS-Harm; Do-Not-Answer; AbstentionBench; long-context tests like MMNeedle/HELMET citeturn4search7turn17search1turn17search4turn17search2turn17search14turn20search2turn4search3 | safety, abstention, long-context robustness, general transparency of performance |

The most important methodological choice is to keep **benchmark baskets aligned with ontology boundaries**. If a proposed new domain has no distinct benchmark basket, that is usually evidence it is not yet a real domain and should remain a workflow or subdomain instead. BrowseComp-Plus is especially instructive here because it was created precisely to disentangle retriever quality from overall deep-research-system behavior; Manurella should imitate that discipline for its own domain evolution. citeturn20search1turn20search10

### Risks from over-specialization

Over-specialization creates the seductive illusion of intelligence by multiplying labels. In practice it usually causes routing entropy, duplicated memory models, overlapping permissions, benchmark fragmentation, and expensive orchestration without commensurate quality gains. Recent work strengthens the skepticism: one 2026 analysis argues that single-agent systems can outperform multi-agent systems at equal reasoning-token budgets, while Google’s agent-scaling results indicate that coordination gains are task-dependent and strongest on parallelizable workloads, with degradation on sequential ones. citeturn19search1turn19search12

For Manurella, the concrete failure modes would be:

| Failure mode | Mechanism |
|---|---|
| Agent explosion | every subskill becomes a pseudo-domain or “persona-agent” |
| Routing ambiguity | similar requests match several branded families |
| Memory silos | duplicate user, task, and evidence state in separate packs |
| Governance drift | permissions and policies diverge across nearly identical agents |
| Benchmark theater | each tiny pack cherry-picks an easy metric |
| Coordination tax | more inter-agent turns, worse latency, more opportunity for compounding error |

These are not theoretical nitpicks. The gap between multi-agent promise and reality is now large enough that architecture by branding is irresponsible. AutoGen and CAMEL show that multi-agent conversation can be powerful, but newer evidence also shows strong conditions under which a simpler architecture wins. The right conclusion is not “never use subagents.” It is “subagents are an execution tactic, not an ontology.” citeturn12search0turn12search1turn19search1turn19search12

### Risks from under-specialization

Under-specialization is just as dangerous. A giant “general assistant” pack can look elegant until it tries to operate a shell, draft a marketing deck, tutor algebra, and book travel with one flattened memory schema and one policy surface. That produces poor tool selection, overbroad permissions, weak UX, and misleading benchmark success because the evaluation no longer matches the real task boundary. Web/OS agents, code agents, evidence agents, and tutors fail in different ways for reasons that are now well documented by WebArena, OSWorld, SWE-bench, AgentDojo, SafeArena, and TutorBench. citeturn2search11turn2search3turn4search1turn17search1turn17search7turn16search13

### Safety, security, and governance implications

Manurella’s governance cannot live “outside” the ontology. Domain packs must declare permissions, risk classes, and policy defaults because action surfaces differ radically. Operations and Engineering need stronger action controls than Inquiry; Authoring needs copyright, impersonation, and brand-safety controls; Learning needs pedagogical honesty and age-sensitive handling; Inquiry needs citation discipline and abstention when evidence is missing. NIST’s AI RMF, NIST’s adversarial-ML taxonomy, the EU AI Act, ISO/IEC 42001, and OWASP’s LLM risk guidance all point in the same direction: governance must be lifecycle-based, risk-aware, and integrated into system design rather than bolted on after deployment. citeturn3search2turn14search3turn14search0turn14search1turn3search3

MCP strengthens the case for embedding governance in the ontology because tool integration is now standardized and therefore easier to proliferate. The MCP specification and security guidance explicitly emphasize hosts, clients, servers, authorization, access controls, and security implications. OpenAI’s docs likewise warn builders to treat remote MCP servers as powerful capability surfaces. That means a pack manifest should state not only “what tools I use,” but also “what approval, data-handling, and risk posture those tools require.” citeturn18search12turn18search4turn18search0turn18search6turn18search2

## Rollout, open research questions, and decisions

### V0, V1, and long-term rollout

**V0** should prioritize ontology discipline over breadth. Ship the semantic kernel, shared evidence graph, pack registry, and only the five recommended top-level packs. Keep Build as a UX alias for Engineering, add Pixel only as `authoring.visual`, expose Mentor and Muse as personas, and hard-disable creation of new top-level packs until benchmark and routing telemetry exist. Use explicit SHACL shapes and pack manifests from day one so the Atlas is machine-readable rather than a diagram that will rot. citeturn0search2turn15search0turn9search1

**V1** should add telemetry-based domain governance. By then Manurella should be using provenance-linked traces, benchmark history, routing confusion metrics, and approval outcomes to decide whether any pack needs to split or merge. This is also the right stage for more explicit A2A federation and richer external MCP ecosystems, because the kernel and policy engine will already exist. citeturn15search1turn3search8turn18search12

The **long-term** direction is a pack ecosystem, not a larger root ontology. Vertical packs for legal, health, finance, or other regulated spaces may eventually be justified, but only if they pass the same bounded-context and benchmark tests. The long-term Atlas should become both a design surface and an auditable registry: every pack, workflow, persona, tool, benchmark, policy, and trace should be queriable through the same semantic model. citeturn14search0turn14search1turn15search0turn6search8

### Open research questions

Several questions remain meaningfully unsettled.

First, should **Authoring** remain one top-level pack? WritingBench, GenEval, and VBench suggest strong modality differences, but that still may not justify a root split if the work object remains “human-facing artifact” and shared workflows dominate. This needs telemetry and benchmark evidence, not taste. citeturn13search14turn13search1turn13search0

Second, how much internal multi-agent decomposition actually helps Manurella’s real workloads? AutoGen and MultiAgentBench show cases where coordination helps, while recent equal-budget studies and Google’s scaling work show cases where it hurts or only helps on parallelizable tasks. Manurella should run its own ablations before institutionalizing subagents. citeturn12search0turn12search3turn19search1turn19search12

Third, can **Learning** maintain top-level status once the system has enough real usage data? The current evidence says yes, because pedagogy and learner modeling are distinct enough. But if most “Mentor” traffic turns out to be thin wrappers around explanation rather than real instructional loops, then Learning may collapse into a workflow-rich subdomain rather than a permanent root. citeturn16search13turn16search17turn5search10

Fourth, how much of Manurella’s memory should be explicitly semantic? RDF/OWL/PROV/SHACL are excellent for durable concepts, shapes, provenance, and Atlas governance, but raw working memory and ephemeral reasoning traces may be better kept in simpler state stores. GraphRAG is helpful but should not become a religion. citeturn0search1turn15search0turn6search5turn6search13

### Decisions safe to adopt now versus decisions requiring experiments

| Safe to adopt now | Why |
|---|---|
| Separate runtime infrastructure, kernel, faculties, shared capabilities, domain packs, workflows, personas, and tools | Strong evidence across cognitive architectures, DDD, and standards. citeturn10search3turn1search5turn9search3 |
| Use five top-level packs: Inquiry, Engineering, Authoring, Operations, Learning | Best current balance of coverage versus maintainability. |
| Keep Build only as alias for Engineering | Prevents semantic overload and routing ambiguity. |
| Demote Muse and Mentor to personas/workflows; demote Pixel to Authoring.visual | Avoids mixing ontology kinds. |
| Treat memory, knowledge graphs, verification, governance, coordination, and effort tiers as cross-domain | Supported by architecture and benchmark evidence. citeturn10search3turn15search0turn20search4 |
| Build the Atlas on RDF/SKOS/OWL/SHACL/SPARQL/PROV-O and trace with OpenTelemetry | Strong standards basis and excellent runtime agnosticism. citeturn0search1turn9search1turn9search0turn0search2turn6search8turn15search0turn15search1 |

| Requires experiments | What to test |
|---|---|
| Whether Authoring later splits into Document/Narrative and Visual/Audiovisual | routing confusion, benchmark lift, policy divergence |
| Whether Learning remains top-level | real learner-state depth, benchmark gains, usage concentration |
| When to invoke subagents internally | equal-budget quality/cost ablations on Manurella tasks |
| Whether Operations should absorb more “personal assistant” behaviors | traffic analysis, policy needs, approval friction |
| Thresholds for create/split/merge/retire | calibration on actual routing and benchmark telemetry |
| Practical value of semantic memory depth | compare semantic Atlas + lightweight task state against heavier graph-first memory |

The short version is blunt: **Manurella should not be built as four mascot-like families.** It should be built as a governed ontology with a small number of durable top-level domain packs and a much richer set of shared capabilities, workflows, personas, and standards-based semantic metadata. That is the only design I found that is simultaneously defensible to cognitive scientists, ontology engineers, benchmark specialists, HCI practitioners, software architects, and safety reviewers. citeturn10search3turn1search5turn4search7turn14search1turn3search2