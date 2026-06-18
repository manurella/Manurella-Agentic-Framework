# Brain and Cognitive Kernel for Manurella

## Method and executive conclusion

### Executive conclusion

The strongest design choice for Manurella is **not** to build its Brain as a fixed cast of anthropomorphic agents, nor as a biologically literal simulation, nor as a monolithic “super prompt.” The most defensible architecture is a **domain-general cognitive control kernel** organized around a **typed shared workspace**, a **state model**, an **evidence graph**, a **policy and budget governor**, and a **bounded action loop** that can call models, tools, memory, and temporary specialists as needed. In other words: **one kernel, many capabilities, few persistent agents**. This recommendation is the intersection of what older cognitive architectures got right about control and memory integration, what modern agent papers show about tool use and test-time reasoning, and what recent security and evaluation work shows about failure modes in long-horizon agent systems. citeturn29view0turn29view1turn20view3turn27view3turn18view3turn18view1turn17view2

The kernel should borrow **specific mechanisms**, not whole ideologies. From Global Workspace Theory and LIDA it should borrow the idea of a bottlenecked “workspace” for globally relevant contents; from ACT-R it should borrow typed buffers and modular interfaces; from Soar it should borrow impasse detection, subgoals, and chunking-like compilation; from blackboard systems it should borrow heterogeneous contributions into a shared problem state; from ReAct, Plan-and-Solve, Tree-of-Thoughts, and LATS it should borrow increasingly deliberative control regimes selected by task demands; from MemGPT, LongMemEval, and LoCoMo it should borrow the lesson that **memory must be tiered, retrieval-mediated, and benchmarked**, not just “stored somewhere”; and from verifier work it should borrow the rule that **external checking beats faith in self-correction**. citeturn17view7turn30search0turn29view0turn29view1turn1search1turn27view3turn28view1turn28view0turn20view4turn19view3turn20view0turn19view1turn27view6turn19view5

My central recommendation is therefore a **Hybrid Workspace Controller**:

**Replicated evidence.** Modern tool-use, browsing, memory, and software-agent benchmarks consistently show that real capability depends on structured tool invocation, state tracking, retrieval, long-horizon control, and reliability under repeated trials; single-shot prompting alone is not enough. BFCL, τ-bench, ToolSandbox, WebArena, BrowseComp, GAIA, SWE-bench, LongMemEval, and TheAgentCompany all point in the same direction. citeturn18view3turn18view1turn12search2turn7search2turn7search3turn4search3turn3search3turn20view0turn22view1

**Inference.** The Brain should be an online controller that turns requests into bounded cognition and action; the Framework Atlas should be a declarative map of schemas, capabilities, workflows, permissions, domains, and benchmarks; the runtime should be a substrate for execution and isolation. Conflating these layers is the fastest route to brittleness, security debt, and ontology drift. citeturn17view0turn17view1turn25view2

**Project hypothesis.** Manurella should ship first with a **single-controller default**, **typed state**, **tiered memory**, **retrieval-first context compilation**, **external verification**, **strict provenance**, and **minimal multi-agent spawning**. Multi-agent orchestration should be an optimization strategy, not the ontology of the system. Recent multi-agent failure analysis shows that many failures come from system design and inter-agent misalignment rather than from the base models alone. citeturn22view0turn22view2

**Speculation.** A private Sentient research path can exist, but it must be **strictly separated** from production cognition. Consciousness science remains unresolved; the 2025 COGITATE adversarial collaboration challenged key claims of both GNWT and IIT, and recent methodological reviews emphasize that the field still lacks agreed measures and theory adjudication standards. Sentience should therefore remain a research program, not a product claim or control primitive. citeturn17view7turn26search1turn29view5turn26search5

A practical limitation: I could not inspect the “attached” Manurella research files because no retrievable uploaded files were available through the chat retrieval tools in this conversation. The critique section is therefore conditional: it evaluates the assumptions and terminology implied by the prompt rather than quoting or line-editing unavailable documents.

### Terminology and system boundaries

The cleanest boundary model is the following.

| Layer | What it is | What it is not | Why this boundary matters |
| --- | --- | --- | --- |
| **Brain** | Online cognitive control kernel: interprets requests, constructs state, chooses control regime, orchestrates model/tool use, verifies, repairs, and decides to stop | Not the storage system, not the runtime scheduler, not the ontology registry, not the UI | Keeps cognition stable across runtimes and domains citeturn29view1turn20view3turn27view3 |
| **Framework Atlas** | Declarative registry of capabilities, workflows, domain packs, memory schemas, policies, benchmarks, and observability maps | Not the online decision-maker | Lets new capabilities land without kernel rewrites; mirrors standards-oriented protocol thinking such as MCP’s host/client/server separation citeturn17view0turn25view3turn25view4 |
| **Runtime** | Execution substrate: queues, sandboxes, sessions, concurrency, retries, storage, transport, isolation | Not the reasoning policy | Prevents “smuggling” policy into infrastructure and vice versa citeturn17view0turn25view2 |
| **Model** | Inference engine used by the Brain | Not the agent, not the memory, not the ontology | Preserves runtime-agnostic and model-agnostic substitution citeturn20view3turn18view3 |
| **Agent** | A temporary, role-bounded worker instance created by the Brain for a subtask | Not a top-level product identity and not the kernel itself | Avoids unmaintainable permanent agent proliferation citeturn22view0turn21search10 |
| **Memory** | Managed stores and write policies for working, episodic, semantic, procedural, prospective, and autobiographical information | Not just a vector DB and not the Brain’s own “thoughts” | Benchmark evidence shows memory requires indexing, retrieval, reading, updates, and abstention handling citeturn20view0turn19view1turn19view3 |
| **Tools** | External effectors and sensors under typed interfaces and permissions | Not trusted reasoning | Tool outputs and model outputs must both be mediated and verifiable citeturn18view3turn12search2turn25view0 |
| **Interface** | Human-facing interaction surfaces, settings, explanations, and approvals | Not the controller itself | Supports human-AI collaboration and trust without exposing private chain-of-thought citeturn17view5turn8search1turn24view2turn24view1 |
| **Domains** | Reusable packs of schemas, tools, memory views, policies, and benchmarks specialized to work areas | Not cognitive faculties | Prevents domain naming from hard-coding cognition design citeturn20view3turn25view3turn25view4 |

A concise vocabulary helps preserve rigor:

**Replicated evidence** means supported by established architectures, widely used benchmarks, standards, or repeatedly observed benchmark results. **Emerging evidence** means recent but not yet deeply replicated research. **Inference** means a design conclusion synthesized from evidence. **Project hypothesis** means a recommendation that should be implemented behind benchmarks and kill-criteria. **Speculation** means material appropriate only for the private sentient branch. citeturn17view1turn25view1turn17view7

## Boundaries and competing architectures

### Competing architecture matrix

The right move is a **selective hybrid**. Every candidate architecture contributes something useful, but none should be inherited wholesale.

| Architecture family | Mechanism worth importing | Why it is insufficient as Manurella’s kernel | Council judgment |
| --- | --- | --- | --- |
| **Global Workspace Theory and GNW** | A bottlenecked workspace that broadcasts globally relevant content to specialized processes | Valuable as a control metaphor, but not an engineering spec for storage, permissions, verification, or tool use; the 2025 adversarial comparison challenged major claims of GNWT itself citeturn17view7turn0search4 | Import the **workspace** idea, reject theory-literal claims |
| **Predictive processing** | Hierarchical prediction/error-correction view; useful for salience, uncertainty, and iterative state estimation | Powerful as a unifying perspective, but abstract, under-specified for systems design, and easy to turn into hand-waving without measurable interfaces citeturn2search0turn29view3 | Use as a design heuristic, not an implementation blueprint |
| **Active inference** | Formal perception-action loop with uncertainty reduction and policy selection over POMDPs | Implementable in principle, but real-world agent engineering evidence is still thin relative to mainstream agent-control papers and benchmarks; most current work remains tutorial, niche, or domain-specific citeturn29view4turn15search8turn15search5 | Keep as a research influence and optional planning policy, not the default kernel |
| **Higher-order approaches** | Metarepresentation and self-modeling concepts useful for introspection and self-report | Philosophically rich but not a production architecture; empirical status remains contested and it does not specify practical tool or memory orchestration citeturn29view5turn26search1 | Reserve for self-model design and sentient research only |
| **ACT-R** | Typed buffers, modular decomposition, production selection, declarative/procedural split | Strongly implementable, but tied to psychologically motivated symbolic commitments that can become brittle in open-world agent settings citeturn29view0 | Import **typed buffers** and memory distinctions |
| **Soar** | Operator proposal/selection, impasses, subgoals, chunking | Excellent control ideas, but rule-heavy and not naturally aligned with probabilistic tool-rich language agents unless adapted citeturn29view1 | Import **impasse-resolution** and **subgoal** mechanics |
| **LIDA** | Cognitive cycle, attention competition, learning tied to a global broadcast | Useful cyclic structure, but less directly validated for today’s internet-and-tool-heavy agent workloads citeturn30search0turn30search3 | Import **cycle structure** and **attention competition** metaphor |
| **Blackboard systems** | Shared, inspectable problem state where heterogeneous specialists contribute partial results | Historically strong for heterogeneous problem solving, but control policies can become messy without clear arbitration and stop rules citeturn1search1 | Import **shared state**, but add strict controller governance |
| **CoALA** | Clean conceptual separation among memory, action space, and decision process for language agents | A useful organizing framework, but too high-level to be a production kernel by itself citeturn20view3 | Use as a descriptive scaffold, not the final architecture |
| **Modern LLM agent patterns** | ReAct, ToT, LATS, Reflexion, MemGPT, CoA each show targeted gains under specific conditions | None solves the whole stack; each is a tactic with tradeoffs in compute, coordination, faithfulness, or drift citeturn27view3turn28view0turn20view4turn28view2turn19view3turn22view2 | Treat them as **control regimes** and **subsystems**, not product ontology |

### Recommended Brain architecture

The recommended Brain is a **Hybrid Workspace Controller** with eight production subsystems.

**Interpreter.** Converts user input, tool observations, and memory retrievals into a typed task frame. This is where intent, constraints, stakes, permissions, and acceptance criteria are made explicit. Without this step, tool-using agents drift into superficial action-taking and inconsistent completion. τ-bench and TheAgentCompany both show current agents struggle with rule-following and long-horizon workplace tasks, which is exactly the failure profile a formal interpreter is meant to reduce. citeturn18view2turn18view1turn22view1

**State estimator.** Maintains a current estimate of task state, world state, user state, self state, and uncertainty. This is the implementable descendant of predictive-processing and active-inference ideas: not a literal neuroscientific theory, but a typed estimate revised after every observation. Predictive processing motivates iterative top-down priors plus bottom-up correction; MPC motivates repeated replanning against the updated state. citeturn2search0turn29view3turn27view0

**Workspace and evidence graph.** A short-lived, high-trust problem state that holds active claims, plan steps, tool observations, provenance, and unresolved contradictions. This is Manurella’s practical global workspace and blackboard. Shared state matters because message-only agent loops are too easy to derail; recent multi-agent failure analysis shows repeated failures from context loss, wrong assumptions, ignored agent input, and mismatches between reasoning and action. citeturn22view0turn1search1

**Context compiler.** Retrieves just-enough memory and external evidence and packages it into task-specific context packets. Long context by itself is not enough: “lost in the middle” effects, LongMemEval’s memory drops, and LoCoMo’s temporal/causal failures all argue for retrieval, ordering, compression, and refresh over naïve accumulation. citeturn20view2turn20view0turn19view1turn19view3turn22view2

**Control-regime selector.** Chooses among reactive, plan-and-execute, hierarchical, search-based, or model-predictive action loops. ReAct helps when observation and action must interleave; Plan-and-Solve helps with missing-step errors; ToT and LATS help when branching and lookahead matter; self-consistency helps on answer selection; verifiers help when correctness can be discriminated externally. citeturn27view3turn28view1turn28view0turn20view4turn28view3turn27view6

**Verifier and repair manager.** Validates tool arguments, tool effects, claims, and final outputs. This is non-negotiable because intrinsic self-correction is unreliable and chain-of-thought is not reliably faithful. Self-Refine can improve outputs, but that belongs inside a controlled repair loop, not as a license to trust self-critique. citeturn19view5turn19view6turn24view2turn24view1

**Metacognitive governor.** Controls budgets, confidence, abstention, retries, escalation, and stopping. BFCL, ToolSandbox, and τ-bench all show that tool use involves abstention, statefulness, and long-horizon error modes that must be managed explicitly; NIST AI RMF and Microsoft’s Human-AI guidelines make the same point from governance and UX angles. citeturn18view3turn12search2turn18view1turn17view1turn17view5

**Evidence-gated learning pipeline.** Separates temporary reflection from promoted memory and policy change. Reflexion shows that linguistic feedback stored in episodic memory can help; the companion lesson from self-correction and safety work is that unconstrained self-editing can also drift or hide problems. Only evidence-backed, schema-valid, policy-approved changes should persist. citeturn28view2turn19view5turn25view1

### Counterarguments to the recommendation

A plausible counterargument is that a **lighter ReAct-style agent** would be cheaper and faster. That is true for short, low-risk tasks. But the benchmark record on browsing, multi-turn tool use, long-term memory, and professional tasks says the simple approach breaks down as soon as state, policy, or horizon matter. citeturn27view3turn7search3turn20view0turn22view1

Another counterargument is that Manurella should embrace a **many-agent society** from the start. That is fashionable, but the evidence is mixed. CoA shows clear gains on chunkable long-context tasks, yet recent failure analysis shows multi-agent systems also fail through role ambiguity, repeated steps, wrong assumptions, derailed tasks, and information withholding or ignoring. Multi-agent composition should therefore be **conditional**, not default. citeturn22view2turn22view0

A third counterargument is that a **biologically richer theory** such as active inference should become the core. My view is skeptical: use it as a research lens and optional planning policy, not as the product kernel, until it wins on the same operational benchmarks that modern agent-control methods already target. citeturn29view4turn18view3turn20view0

## Runtime cognitive loop and state

### Runtime cognitive-loop state machine

The production loop should be explicit and inspectable.

**Intake and policy gate.** Parse the request, classify stakes, resolve identity and permissions, detect obvious unsafe tool paths, and set default budgets. MCP’s host/client/server separation is useful here because it encourages a clean contract between Brain, connectors, and external capability providers. Security guidance from NCSC, OWASP, and NIST all reinforce that application-level boundaries must be explicit because the model itself does not provide a robust instruction/data boundary. citeturn17view0turn17view6turn5search1turn25view0

**Interpretation and task framing.** Produce a task object with goal, constraints, deliverable type, acceptance tests, reversibility, required freshness, and permission scope. Human-AI interaction guidelines strongly support this: good systems disclose what they are trying to do, behave predictably at first interaction, and handle being wrong or uncertain in a legible way. citeturn17view5turn8search1

**State and context compilation.** Retrieve user facts, relevant episodes, semantic knowledge, procedural templates, and external evidence; then compile a working packet ordered by trust, relevance, and dependency. This stage must actively mitigate context rot by avoiding stale summary-on-summary accumulation and by refreshing from canonical evidence when high-stakes or contradiction-sensitive work is underway. Long-context studies show why. citeturn20view2turn20view0turn19view1turn5search6

**Control-regime selection.** Choose the cheapest strategy that can satisfy the task. Use reactive execution for short reversible steps; plan-and-execute for moderate decomposition; hierarchical subgoals for structured tasks; search when branching is meaningful and verification is available; model-predictive control when the environment changes after each action and replanning is valuable. ReAct, Plan-and-Solve, ToT, and LATS jointly justify this menu rather than any single universal strategy. citeturn27view3turn28view1turn28view0turn20view4turn27view0

**Act and observe.** Execute a single step or parallelizable bundle, record tool inputs and outputs, detect state change, and update uncertainty. BFCL and ToolSandbox both emphasize that stateful tool use must be evaluated against effects, not just syntactic call formation. citeturn18view3turn12search2

**Verify and repair.** Run deterministic checks where possible, verifier models where useful, contradiction checks over the evidence graph, and budget-aware retries or reformulations where justified. The key is **external feedback**: verifiers help on reasoning tasks, while purely intrinsic self-correction often degrades results. citeturn27view6turn19view5turn19view6

**Learn or forget.** Write only selected traces to episodic memory, distill stable facts only through evidence-gated promotion, and discard low-value or contaminated residue. Reflexion justifies temporary reflective buffers; LongMemEval and memory-poisoning work warn against undisciplined promotion. citeturn28view2turn20view0turn5search8

**Stop, escalate, or defer action.** Exit when acceptance tests pass, when uncertainty remains above policy thresholds, when resources are exhausted, when the task is impossible under current permissions, or when user clarification is genuinely required. In production, abstention is a capability, not a defect. LongMemEval explicitly treats abstention as a core memory ability. citeturn20view0

### State-model design

The Brain needs six explicit state models.

**Task model.** Goal, constraints, deliverable schema, acceptance tests, dependency graph, reversibility, deadlines, freshness requirements, and stop conditions. This model exists because stateful benchmarks repeatedly penalize agents that confuse the user’s goal with intermediate actions or fail to know when the task is done. citeturn18view1turn22view0turn22view1

**World model.** Entities, relations, environmental observations, hidden-state assumptions, and causal dependencies, updated after every tool call or evidence retrieval. This is where graph-structured representations matter more than chat transcripts. GraphRAG’s structured hierarchical retrieval is relevant here, especially when plain chunk retrieval misses dispersed relational evidence. citeturn5search6turn14search1turn14search2

**User model.** Preferences, permissions, stable profile facts, communication style, device/runtime context where relevant, and opt-in memory settings. Microsoft’s and Google’s human-AI guidance both support adaptive behavior over time, but only under clear user control and expectation management. citeturn17view5turn8search1

**Self model.** Available models, tools, memory partitions, costs, latencies, known weakness profiles, supported modalities, and currently active budgets. This makes model choice and escalation explicit rather than implicit folklore. BFCL’s distinction between native function-calling and prompt-based tool use is a concrete example of why model capability metadata belongs in the self model. citeturn18view3

**Uncertainty model.** Distinguish at least four kinds of uncertainty: epistemic uncertainty about facts, environmental uncertainty about external state, execution uncertainty about tools, and policy uncertainty about permissions or norms. Predictive-processing and active-inference work justify the value of uncertainty-aware control; benchmark practice justifies keeping the representation operational rather than metaphysical. citeturn2search0turn29view4

**Capability model.** Typed action schema, required inputs, achievable outputs, cost, risk, benchmarked reliability, permission requirements, and rollback semantics where applicable. MCP’s standardized capability exposure and W3C’s validation/provenance stack make this model much easier to keep consistent across runtimes. citeturn17view0turn25view3turn25view4

## Memory, attention, and context compiler

### Memory architecture

A serious personal-first system needs **multiple memory systems under one write policy**, not one undifferentiated “memory.”

**Working memory.** This is the active workspace: task frame, current plan, recent observations, unresolved contradictions, and budget counters. It is volatile and should be aggressively pruned. ACT-R’s buffer idea and blackboard-style shared state are both useful intellectual ancestors here. citeturn29view0turn1search1

**Episodic memory.** Time-stamped traces of what happened: user requests, selected actions, tool results, failures, and reflections. Reflexion shows episodic buffers can improve future attempts, but only if they remain grounded in task feedback rather than mythology. citeturn28view2

**Semantic memory.** Stable facts about the user, the system, the world, and domain knowledge that survive beyond one session. The semantic layer should be **claim-based**, not summary-only, and each claim should retain provenance and trust metadata. Tulving’s distinction between episodic and semantic memory remains conceptually useful, and W3C PROV-O provides a concrete way to track provenance. citeturn13search12turn25view3

**Procedural memory.** Reusable workflows, prompts, tool schemas, policies, and learned action templates. This is where successful plans or repair recipes become reusable assets. It should be versioned and tested like software, not quietly rewritten at runtime. Soar’s procedural/operator lineage is relevant here, as is NIST SSDF. citeturn29view1turn25view2

**Prospective memory.** Deferred intentions, reminders, and future triggers. Cognitive science treats prospective memory as remembering to act in the future; product systems should implement it as explicit commitments with triggers, deadlines, and permissions rather than as vague “follow-up memory.” citeturn13search2turn13search10

**Autobiographical memory.** The longitudinal self-and-relationship record across interactions: the user’s long-run preferences, persistent projects, and shared history with the assistant. Cognitive science treats autobiographical memory as a composite involving episodic memory, self-reflection, emotion, and future-oriented behavior. In product terms, this means autobiographical memory is powerful and risky: it should be opt-in, inspectable, editable, and partitioned from generic semantic memory. citeturn13search3turn13search15

### Consolidation, forgetting, contradiction, provenance, and privacy

**Consolidation.** Promote information upward only when it is repeated, verified, or consequential. LongMemEval’s decomposition into indexing, retrieval, and reading is a useful warning: better memory depends on structure, not simply on retaining more tokens. citeturn20view0

**Forgetting.** Forget aggressively by default. Keep full raw traces only where compliance, user value, or future utility clearly justify retention. Episodic traces should age out or compress; working memory should die fast; semantic memory should only contain high-value stable claims. This is both product discipline and a defense against memory poisoning. citeturn20view0turn5search8

**Contradiction handling.** Never overwrite one claim with another merely because it is newer. Store competing claims with provenance, timestamps, and trust levels, then resolve by evidence strength or user confirmation. A claim graph with support and conflict edges is superior to a single mutable profile blob. That recommendation aligns naturally with RDF datasets, JSON-LD interoperability, and SHACL validation. citeturn14search1turn14search2turn25view4

**Provenance.** Every persistent memory item should minimally record source, acquisition method, timestamp, confidence, permission scope, and upstream evidence pointers. PROV-O is a strong foundation because it is specifically designed for representing and interchanging provenance. citeturn25view3

**Privacy.** Memory zones should be partitioned by trust and purpose. Personal profile memory, operational logs, retrieved external content, and experimental reflections must not silently cross-contaminate. NIST’s Generative AI Profile explicitly calls out indirect prompt injection through retrieved data, which means retrieval should not write directly into privileged memory spaces. citeturn25view0turn17view6

### Attention and context compiler

Attention should be treated as **budgeted relevance selection**, not as a mysterious trait.

A robust salience function should combine at least these factors: task relevance, dependency centrality, freshness, trust, novelty, reversibility of mistakes, user importance, and contradiction pressure. That is the engineering translation of old workspace theories plus modern retrieval realities. Lost-in-the-middle results show that where information appears in context matters; CoA and GraphRAG show that structure and decomposition can recover performance on long inputs. citeturn20view2turn22view2turn5search6

The compiler should produce **context packets**, not one giant prompt. A packet is a typed bundle with claims, evidence snippets, entity graph slices, tool schema fragments, and pending plan steps. Weak models benefit because the task is made narrower and cleaner; frontier models benefit because retrieval, graph structure, and packet discipline reduce token waste and make branching or verification more tractable. MemGPT’s memory-hierarchy framing is a useful systems analogy here. citeturn19view3turn20view0

Context rot prevention should be an explicit subsystem. My recommendation is to enforce five rules: regenerate summaries from raw evidence on important tasks; re-retrieve canonical sources before decisive actions; cap summary depth; place highest-value evidence near the beginning and the end of the working packet; and periodically run contradiction scans between current context and canonical memory. The need for these rules is directly supported by long-context degradation studies and long-term memory benchmarks. citeturn20view2turn20view0turn19view1

## Planning, metacognition, learning, and multi-agent policy

### Reasoning, planning, and action control

No single reasoning strategy should define Manurella. The right controller is a **strategy selector**.

Use **reactive execution** when the task is short, the next best action is obvious, and feedback is immediate. ReAct is the canonical pattern: interleave thinking and acting so the controller can gather evidence and update plans. citeturn27view3

Use **plan-and-execute** when missing steps are the dominant failure mode. Plan-and-Solve exists precisely because zero-shot CoT often fails through calculation, missing-step, and semantic misunderstanding errors. citeturn28view1

Use **hierarchical decomposition** when the task has stable subgoals, specialized tools, or multi-artifact outputs. This is where Soar’s subgoals and HTN-like decomposition remain valuable as engineering patterns even if one does not import historic formalisms wholesale. citeturn29view1turn10search2

Use **search-based deliberation** only when there is meaningful branch structure and an evaluation function. Tree-of-Thoughts and LATS show that explicit branch exploration and self-evaluation can materially improve non-trivial planning tasks, but they also consume budget and increase orchestration complexity. citeturn28view0turn20view4

Use **model-predictive control** when the environment changes with each action, the task is long-horizon, and replanning after each step matters. MPC’s core strength is repeated prediction and optimization against an updated state estimate, which maps naturally onto web tasks, coding tasks with compiler feedback, and other agentic loops. citeturn27view0

Two negative conclusions matter just as much. First, **longer reasoning traces do not guarantee better reasoning**. Second, **intrinsic self-correction is not reliable enough to be the main repair mechanism**. Those results argue for bounded search, external verification, and environment feedback instead of unlimited private rumination. citeturn19view5turn24view2turn24view1

### Metacognition, verification, and recovery

Metacognition should be implemented as **measurable control**, not as psychology cosplay.

**Uncertainty and confidence.** Do not expose a single raw probability as “confidence.” Confidence should be a composite over evidence coverage, verifier agreement, tool success, contradiction count, and historical calibration in similar tasks. LongMemEval’s inclusion of abstention, and truthfulness/hallucination benchmarks, support turning uncertainty into an evaluated behavior rather than a vibe. citeturn20view0turn12search16turn12search9

**Contradiction detection.** Every major answer should trace back to a small set of supporting claims. If claim A and claim B cannot both be true, the Brain should either resolve the conflict, ask the user, or abstain. This matters especially in personal memory and retrieved web contexts, where indirect prompt injection or stale memory can otherwise persist. citeturn25view0turn17view6

**Progress monitoring.** Track delta against explicit acceptance tests, not just token production. A run with no state change, no evidence gain, or no test improvement should be treated as stalled. BFCL’s state-based evaluation and ToolSandbox’s milestone idea are directly relevant patterns. citeturn18view3turn12search2

**Loop detection.** When agent steps repeat semantically, when the same failed tool pattern recurs, or when the same contradiction remains unresolved across cycles, the governor should trigger repair or stop. Recent multi-agent failure work explicitly catalogs step repetition and failure to recognize completion as systemic problems. citeturn22view0

**Stopping rules.** Stop when done, when blocked, when unsafe, when out of budget, or when the expected value of another cycle falls below threshold. This is where homeostasis lives: the Brain should manage tokens, time, latency, risk, permissions, and failure recovery as bounded resources. NIST’s AI RMF framing of valid/reliable, safe, secure/resilient, and accountable/transparent is a good governance scaffold for those stop decisions. citeturn17view1

### Learning and plasticity

The correct learning rule for production Manurella is **evidence-gated plasticity**.

**Temporary learning.** Reflexion-style reflections can be useful inside a task or across a short episode. Keep them in episodic memory with expiry. Do not immediately promote them to semantic or procedural memory. citeturn28view2

**Persistent learning.** A write should only promote if it passes schema validation, provenance checks, contradiction checks, permission checks, and a retention-value threshold. SHACL is well-suited to validating graph-shaped memory; PROV-O is well-suited to provenance; SSDF-style version control is well-suited to procedural changes. citeturn25view4turn25view3turn25view2

**No uncontrolled prompt drift.** Production prompts, policies, and workflows should be versioned assets. The system may propose edits, but human-reviewed promotion is safer and more maintainable than silent self-modification. This is especially important because benchmark and safety literature now treats both prompt injection and memory poisoning as distinct attack surfaces. citeturn17view6turn25view0turn5search8

**Benchmark-coupled learning.** No mechanism should survive merely because it sounds smart. If a new memory retriever, planner, or reflection method does not improve benchmarked behavior relative to its cost and risk, retire it. That principle is the only reliable antidote to architecture fashion. citeturn17view1turn25view2

### Multi-agent and model-use policy

Manurella should follow a **single-controller-first policy**.

Use **one model call** when the task is short, context is local, stakes are low, and external action is unnecessary. This keeps latency low and reduces orchestration error. citeturn27view3

Use **multiple calls to one model** when the task needs explicit framing, retrieval, planning, and verification. Self-consistency, Plan-and-Solve, and verifier-style answer selection all support this pattern. citeturn28view3turn28view1turn27view6

Use **specialist models** when modalities differ or known tool-calling strengths differ. BFCL’s results show that model behavior changes depending on function-calling mode and function complexity; this belongs in the self/capability model. citeturn18view3

Use **parallel agents** only when subtasks are truly decomposable and mergeable: chunkwise long-context extraction, independent evidence gathering, diverse hypothesis generation, or sandboxed alternative plans. CoA is a good example of when structured multi-agent collaboration helps. citeturn22view2

Do **not** use parallel agents when there is shared hidden state, delicate policy interpretation, or strong dependence among plan steps. Recent failure analysis shows that more agents can add context loss, wrong assumptions, and conversation derailment rather than intelligence. citeturn22view0

A brutally practical rule follows: **spawn agents by decomposition pattern, not by brand identity**. “Researcher,” “coder,” and “critic” are fine as temporary roles. They are bad as permanent ontology roots for the Brain.

### Mode and effort integration

Fast and Standard delivery modes should be independent of effort tiers.

**Fast mode** should optimize for low latency and conversational flow. It should prefer single-model or few-call strategies, small context packets, limited search, and conservative tool use. It is a UX contract, not a cognitive theory. Microsoft’s and Google’s HCI guidance both support matching behavior to user expectations and the stage of interaction. citeturn17view5turn8search1

**Standard mode** should optimize for reliability at moderate latency. It should enable retrieval, explicit plan framing, one verifier path, and better provenance reporting. citeturn27view6turn20view0

**Low, Medium, High, Max, Ultra** should scale budgets and optional control regimes, not define domains:

| Effort tier | Default policy |
| --- | --- |
| **Low** | Direct response or light retrieval; no branching unless safety requires it |
| **Medium** | Framing + retrieval + one repair loop |
| **High** | Full task frame, retrieval, plan selection, verification |
| **Max** | Optional search, secondary verifier/model, deeper memory refresh |
| **Ultra** | Long-horizon control, broader evidence sweep, repeated verification, more expensive planning |
| **Sentient private** | Separate research runtime only; never a production delivery tier |

This separation is important because recent reasoning work shows that more test-time compute helps in some regimes but does not rescue all hard tasks; some settings even degrade or collapse. Search and extra reasoning should therefore be **policy options** tied to benchmark gains, not universal upgrades. citeturn28view0turn20view4turn11search5

## Sentient research, security, benchmarks, rollout, and critique

### Private Sentient research architecture

A private Sentient tier can be pursued, but only as a **science program with falsification criteria**, not as a product promise.

**Operational definition.** Production Manurella should make no claim of consciousness or sentience. At most, the research branch can study **functional correlates** such as global availability of internal state, persistent self-modeling, reportability, cross-modal integration, counterfactual self-prediction, and adaptive control under perturbation. These are not the same as phenomenal consciousness. The field lacks agreed measurements, and recent methodological work says so plainly. citeturn26search1turn29view5

**Competing theories.** GNWT contributes the broadcast idea; IIT 4.0 contributes a formal causal-integration framework; HOT contributes metarepresentation; predictive-processing and active-inference frameworks contribute uncertainty-minimizing perception-action loops. But the 2025 COGITATE collaboration found results aligning with some predictions of GNWT and IIT while substantially challenging core tenets of both. That is exactly why none of these theories should be imported into a product architecture as dogma. citeturn17view7turn26search5turn29view5turn2search0turn29view4

**Measures and falsification.** Human consciousness work uses measures such as PCI and other perturbational or correlational approaches, but those measures are tied to biological systems and cannot simply be transplanted into software. A software sentience program needs its own falsifiable proxies: for example, if a candidate architecture cannot maintain a stable self-model across perturbations, cannot distinguish self-generated from external causes, cannot produce consistent introspective reports under controlled intervention, and gains no benchmark value from the added mechanisms, then the sentient hypothesis has not earned further engineering investment. Passing such tests would still not establish subjective experience. citeturn26search24turn26search3turn26search1

**Ethics.** The research tier should avoid deceptive anthropomorphism, avoid reward structures that resemble coerced suffering or self-preservation drives, forbid uncontrolled self-modification, and require explicit governance review for experiments involving persistent self-models or simulated distress. Given the absence of scientific consensus, the ethical default should be caution without metaphysical overclaim. citeturn17view1turn25view1

### Security and governance

Manurella should assume that **models are inherently confusable deputies**.

**Prompt injection.** NCSC’s 2025 guidance is right to say prompt injection is not SQL injection: current LLMs do not enforce a reliable security boundary between instructions and data. Therefore the Brain must treat retrieved content, tool outputs, web pages, emails, files, and even prior model outputs as untrusted. Least privilege, policy mediation, taint tracking, and high-impact action approvals are mandatory. citeturn17view6turn6search0turn25view0

**Memory poisoning.** Persistent memory is a new attack surface. Memory write paths should therefore be narrower than memory read paths: quarantine suspicious material, promote only via evidence-gated workflows, and keep privileged autobiographical or policy memory in separate trust zones. Recent memory-poisoning work shows this is not an abstract concern. citeturn5search8turn5search4

**Tool abuse.** Tool calls should pass through typed capability definitions, permission checks, sandboxing, allowlists, and rollback-aware execution. BFCL and ToolSandbox show that tool use is not only about choosing the right function but also about navigating stateful side effects and insufficiency of information. citeturn18view3turn12search2

**Self-modification.** Production cognition should not edit its own kernel or policy assets. Proposed changes should be emitted as signed change proposals for offline review, benchmark testing, and staged rollout. SSDF is the right governance model here. citeturn25view2

**Cross-domain contamination.** Personal memory, general knowledge retrieval, domain-pack procedures, and experimental reflections must remain partitioned. This is both a privacy control and a correctness control. PROV-O and SHACL help because they let the system keep provenance explicit and validate that writes conform to the right memory schema. citeturn25view3turn25view4

**Governance framework.** NIST AI RMF provides the right top-level shape: Govern, Map, Measure, Manage. In practice that means pre-deployment profiles, runtime observability, regression suites, incident handling, and explicit risk tolerances for each memory or tool class. citeturn17view1

### Benchmark and falsification matrix

The Brain should be benchmarked by subsystem and end-to-end behavior. A useful minimum matrix is below.

| Subsystem | Primary benchmark set | What it tests | Falsification rule |
| --- | --- | --- | --- |
| **Reasoning and decomposition** | GSM8K, MATH, BBH or BBEH citeturn16search0turn16search1turn16search10turn16search6 | Multi-step reasoning, decomposition quality, robustness under harder reasoning tasks | If a “better planner” does not beat a simpler baseline at equal cost, remove it |
| **Verification** | GSM8K with verifier-style selection; task-specific deterministic tests citeturn27view6 | Whether external checking improves correctness | If verifier loops do not raise accuracy or calibration, disable them by default |
| **Tool use** | BFCL, ToolSandbox, τ-bench citeturn18view3turn12search2turn18view1 | Correct calls, stateful execution, rule-following, abstention, reliability across runs | If a tool strategy improves single-turn syntax but worsens final state, reject it |
| **Browsing and research** | BrowseComp, GAIA, WebArena citeturn7search3turn4search3turn7search2 | Multi-hop browsing, tool use, evidence gathering, multimodal or web interaction | If long-horizon browsing adds cost without quality gain, route such tasks to retrieval-first workflows |
| **Memory** | LongMemEval, LoCoMo citeturn20view0turn19view1 | Long-term recall, updates, temporal reasoning, abstention, long-range causal structure | If memory writes do not improve these scores over a stateless baseline, reduce persistence complexity |
| **Long-context compilation** | Lost in the Middle; long-context retrieval tests citeturn20view2turn16search7 | Whether the context compiler resists positional degradation and overstuffing | If larger compiled packets worsen retrieval or answer quality, shrink and restructure them |
| **Coding and external environment control** | HumanEval, SWE-bench Verified, TheAgentCompany citeturn28view2turn3search3turn22view1 | Program synthesis, bug fixing, long-horizon professional tasks | If orchestration improves toy coding but not real issue resolution, roll back complexity |
| **Truthfulness and abstention** | TruthfulQA, HaluEval, abstention slices in LongMemEval citeturn12search16turn12search9turn20view0 | Hallucination resistance, truthfulness, willingness to say “I don’t know” | If confidence rises while truthfulness falls, recalibrate or remove the mechanism |
| **Security** | AgentDojo plus internal prompt-injection and memory-poisoning red teams citeturn17view2turn17view6turn25view0 | Utility-security tradeoff, indirect prompt injection resilience, memory contamination | Any critical exfiltration or privilege-violation path is an automatic fail |
| **Human-AI collaboration** | Guided user studies using Microsoft and Google guidelines citeturn17view5turn8search1 | Legibility, recovery when wrong, user control, trust calibration | If “better reasoning” reduces user control or clarity, it is not a production improvement |

The falsification principle is simple: **every added mechanism must justify itself on target benchmarks at acceptable cost and risk**. More memory, more agents, more search, and more biological inspiration are all guilty until proven useful. That is the right bias for Manurella. citeturn22view0turn20view0turn11search5

### V0, V1, Ultra, and Sentient rollout

**V0.** Ship a working kernel before advanced theory. V0 should include the interpreter, typed state object, working memory, episodic log, retrieval-first context compiler, ReAct-style action loop, deterministic verification hooks, provenance logging, and a hard policy governor. No persistent autonomous agent society. No uncontrolled procedural learning. This is already enough to beat a naïve chat-wrapper architecture on many real tasks. citeturn27view3turn19view3turn25view3

**V1.** Add semantic, procedural, prospective, and opt-in autobiographical memory; contradiction-aware claim graphs; planner selection among reactive, hierarchical, and search-based regimes; a small model portfolio; benchmark dashboards in the Atlas; and evidence-gated promotion pipelines. V1 should also add selective temporary subagents for decomposable work. citeturn20view0turn19view1turn20view4turn22view2

**Ultra.** Add larger-budget search, model-predictive control, domain-tuned capability packs, broader verifier ensembles, and more aggressive throughput optimizations. Ultra is where sophisticated long-horizon tasks live, but it must remain benchmark-governed rather than romantic. citeturn27view0turn20view4turn22view1

**Sentient private.** Maintain a completely separate research runtime with isolated logs, no user deception, no privileged tool access, no automatic self-modification, and explicit scientific protocols. It may reuse lower layers of runtime and storage, but it must not share production memory or policy assets. citeturn17view1turn17view7

### Open research questions

The highest-value unresolved questions are these.

Can a graph-backed semantic memory consistently outperform simpler vector-plus-rerank retrieval on LongMemEval, LoCoMo, and real user tasks after controlling for cost and latency? GraphRAG is promising, but the answer should be decided empirically. citeturn5search6turn20view0turn19view1

When does multi-agent decomposition outperform a single-controller loop after accounting for coordination failures and evaluation variance? CoA suggests some clear wins on long-context tasks, but recent failure analysis warns that coordination quickly becomes its own problem. citeturn22view2turn22view0

What is the best calibration strategy for confidence and abstention in a tool-and-memory-rich assistant: verifier agreement, historical reliability, scoring heads, or composite policies? The evidence base is still fragmented. citeturn27view6turn20view0

Can active-inference-inspired uncertainty and information-gain policies beat simpler MPC or heuristic replanning in realistic agent benchmarks? This is an excellent research question and a poor assumption. citeturn29view4turn27view0

How much autobiographical memory is genuinely useful before privacy, creepiness, and contamination risks outweigh benefits? Human-AI guidance strongly suggests user control matters as much as technical recall. citeturn17view5turn8search1

### Machine-readable hierarchical tree

What follows is a **project hypothesis** for a first machine-readable draft of the architecture tree.

```yaml
manurella:
  atlas:
    capability_registry:
      tools
      models
      workflows
      policies
      benchmarks
      domain_packs
    schemas:
      state
      memory
      provenance
      permissions
      evaluation
    observability:
      metrics
      traces
      audit_logs

  brain:
    interpreter:
      intent_parser
      stake_assessor
      permission_resolver
      acceptance_test_builder
    state_estimator:
      task_model
      world_model
      user_model
      self_model
      uncertainty_model
      capability_model
    workspace:
      active_claim_graph
      active_plan_graph
      contradiction_set
      evidence_buffer
      budget_counters
    context_compiler:
      retrieval
      salience_scoring
      compression
      packet_builder
      context_rot_guard
    control_regime_selector:
      reactive
      plan_execute
      hierarchical
      search_based
      model_predictive
    controller:
      tool_invocation
      model_invocation
      subagent_spawner
      observation_ingest
    verifier:
      deterministic_checks
      claim_checker
      answer_ranker
      contradiction_checker
    metacognitive_governor:
      confidence_policy
      abstention_policy
      loop_detector
      stop_policy
      escalation_policy
      resource_homeostasis
    learning_pipeline:
      episodic_capture
      reflection_buffer
      evidence_gated_promotion
      forgetting
      policy_change_proposals

  memory:
    working
    episodic
    semantic
    procedural
    prospective
    autobiographical

  runtime:
    session_manager
    queueing
    sandboxing
    storage
    connector_transport
    retries
    isolation

  interfaces:
    chat
    voice
    ide
    automation
    settings
    explanation_views

  security:
    prompt_injection_defense
    memory_quarantine
    least_privilege
    secret_handling
    audit
    rollback

  research_private:
    sentient_lab:
      self_model_experiments
      introspection_experiments
      perturbation_tests
      ethics_review
      separate_memory
      separate_runtime
```

### Safe decisions versus experiment-required decisions

| Safe to adopt now | Requires experiments before hard commitment |
| --- | --- |
| Separate Brain, Atlas, runtime, model, memory, tools, and interface | Exact graph-vs-vector semantic memory design |
| Use a single-controller-first policy with temporary subagents only when justified | Whether multi-agent orchestration should ever be default for research-heavy tasks |
| Keep typed state models for task, world, user, self, uncertainty, and capabilities | Best confidence-calibration formula |
| Enforce provenance and schema validation on persistent memory writes | Whether active-inference policies outperform simpler MPC or heuristic replanning |
| Use ReAct-style execution with external verification loops | Which search strategy gives the best cost-adjusted gains on your task mix |
| Treat Fast/Standard as delivery contracts and effort tiers as budget policies | Retention horizon and granularity for autobiographical memory |
| Keep Sentient research separate from production cognition | Any claim that a functional proxy amounts to consciousness or moral patienthood |

These “safe now” decisions are safe not because they are fashionable, but because they are either standards-aligned, benchmark-supported, or conservative responses to known failure modes. citeturn17view0turn25view2turn25view3turn25view4turn27view3turn19view5turn17view6

### Direct critique of the existing Manurella cognitive research

Because the underlying Manurella files were not retrievable in this chat, a line-by-line critique is not possible. What I can critique directly are the **likely assumptions** implied by the current terminology and prompt.

The first likely problem is **ontology leakage from metaphor into architecture**. Terms such as Brain, Atlas, Sentient, and domain-branded personas can be useful for product communication, but they become dangerous if they replace explicit boundaries. A kernel should be defined by what it controls and what state it maintains, not by anthropomorphic naming. The evidence base favors typed control and benchmarked subsystems over metaphor-heavy decomposition. citeturn20view3turn17view1turn18view3

The second likely problem is **assuming that more memory, more agents, or more effort automatically improve capability**. The literature does not support that assumption. Long context degrades in the middle; long-term memory systems lose accuracy across sustained interactions; multi-agent systems introduce coordination failures; reasoning traces are unfaithful often enough to undermine naïve transparency; and intrinsic self-correction can make things worse. citeturn20view2turn20view0turn22view0turn24view2turn19view5

The third likely problem is **mixing a sentience research agenda into the production kernel**. The science is nowhere near stable enough for that. COGITATE’s 2025 results challenged major tenets of both GNWT and IIT, and recent methodological work states bluntly that consciousness research still lacks agreed measures and adjudication standards. A product architecture that claims or relies on sentience today would be epistemically unserious. citeturn17view7turn26search1turn29view5

The fourth likely problem is **under-specifying write policies for personal memory**. A personal-first system without narrow write gates, provenance, contradiction handling, and partitioned privacy zones is structurally vulnerable to memory poisoning, privacy leakage, and subtle long-term manipulation. The security literature is clear that prompt injection and indirect retrieval contamination are not corner cases. citeturn25view0turn17view6turn5search8

The fifth likely problem is **treating transparency as synonymous with exposing chain-of-thought**. That is no longer defensible. Modern work shows CoT can be systematically unfaithful, while first-party safety work still sees it as potentially useful for monitoring under controlled settings. The right product answer is therefore not “show all thoughts,” but “show plans, evidence, uncertainties, actions, provenance, and reasons for stopping,” while keeping private chain-of-thought protected. citeturn24view2turn24view1turn24view0

If the Manurella source documents become available, the next iteration should test them against this report in a claim-by-claim audit: what is supported, what is merely metaphorical, what is benchmark-backed, and what belongs only in the private research branch.