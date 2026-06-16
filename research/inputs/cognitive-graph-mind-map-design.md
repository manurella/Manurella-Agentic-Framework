# **Implementation Blueprint for the Menuella Cognitive Graph: Spatial-Semantic Representation and Multi-Layer Visual Mapping**

## **Theoretical Foundations and Cognitive Systems Synthesis**

Modern independent restaurants require highly integrated digital ecosystems to escape the fragmentation of disconnected transactional tools1. Rather than managing separate stacks for online ordering, menu adjustments, SEO, loyalty programs, and kitchen operations, systems must be consolidated onto a single execution pipeline1. The Menuella operating system models this unified environment as a dynamic network of weighted states, conceptualized as a cognitive graph1.  
Traditional knowledge graphs provide static ontological structures but lack the cognitive plasticity to represent evolving relationships, operational pressure, computational effort, and real-time failure states3. By modeling restaurant operations as non-Euclidean path-based networks, the platform allows actions, physical constraints, and menu configurations to co-evolve6. In this architecture, a physical menu item—such as the signature Manurella Sticks appetizer7—is not represented merely as an isolated row in a relational database. Instead, it is modeled as an active node within a multi-dimensional spatial-conceptual map6.  
To handle complex sequences like ordering funnels and kitchen pipelines, the system leverages successor representations to model state trajectories9. The successor representation, ![][image1], measures the expected discounted future occupancy of a target state, ![][image2], from a starting state, ![][image3]9:  
![][image4]  
Here, the discount factor, ![][image5], represents the step-by-step transition friction, such as customer drop-off during checkout or queue delays2. Under this formulation, physical-conceptual distances between nodes are encoded as reciprocal connection strengths, mimicking CA3 hippocampal place cell synaptic resistance12. When two concepts co-occur frequently—such as an order modifier pairing extra-spicy pasta with premium sparkling water—long-term potentiation reduces synaptic resistance, establishing an optimized low-friction path across the graph11.

                        \[ Customer Add-To-Cart State \]  
                                      │  
                             (Transition Friction)  
                                      ▼  
                        \[ Target Recommendation Node \]  
                             (Manurella Sticks)  
                                      │  
                 ┌────────────────────┴────────────────────┐  
                 ▼                                         ▼  
     \[ Low-Friction Path \]                      \[ Overloaded Buffer \]  
    (LTP Lowered Resistance)                  (Physical Station Barrier)  
                 │                                         │  
                 ▼                                         ▼  
    \[ Target Recommendations \]                 \[ State Transition Bypass \]

To manage the execution of these pathways, the platform coordinates fast and slow processes, mirroring the dual-process theory of cognition13.

* **System 1 (Implicit / Fast):** Executes low-latency, heuristic-driven operations such as instant cart validation, pricing calculations, and localized menu rendering11. This ensures that the frontend interface remains highly responsive under load2.  
* **System 2 (Explicit / Slow):** Executes computationally heavy operations, such as calculating neural pairings, running collaborative filters, and evaluating kitchen queue constraints11. System 2 updates the weights of System 1, compiling complex models into fast, executable pathways11.

System-level decisions are evaluated on the fly using an interpretable Weight-Calculation model, where the execution weight of any operational edge is computed as the product of its operational benefit and its occurrence probability17:  
![][image6]  
In the ordering domain, the "Benefit" represents the financial contribution margin of an item, defined as its menu price minus its Cost of Goods Sold (COGS), while the "Probability" represents the neural probability that a guest will accept the suggestion11:  
![][image7]  
To prevent semantic aliasing—where a single entity like "Manurella Sticks" behaves differently depending on the context—the architecture employs Clone-Structured Cognitive Graphs (CSCG)7. Instead of routing all interactions through one global node, the system instantiates "clones" of an entity for different context states (e.g., appetizer menus, checkout upsells, or late-night operations)11. This allows the platform to learn distinct transition probabilities and isolate localized physical bottlenecks without corrupting the broader schema11.  
To manage operational complexity under pressure, the network adjusts its connectivity using the Adaptive Memory Allocation Principle (AMAP)5. During off-peak hours, the graph expands to a dense state, exploring non-obvious pairings to maximize basket sizes5. During peak periods (e.g., Friday night rushes), the system transitions to a sparse state, pruning non-essential paths to reduce cognitive load on line staff1. This behavior is managed through a Seven-Dimensional Graph Health Framework5 and optimized via online stochastic gradient descent (SGD)5.  
For maintenance and operations, the platform integrates helper sub-systems: "Manuela 2.0" uses scraping and documentation processing to expose system configurations as an API19, while "Medula AI" provides interactive chat training to help staff memorize complex graph dependencies offline20.

## **Comparative Evaluation of Graph Representation Technologies**

To establish the v0 approach for the Menuella Cognitive Graph, seven technologies were evaluated against the core requirements of human readability, machine readability, relationship evolution, domain expansion, multi-layer overlays, and version-control compatibility.

| Technology | Human Readability | Machine Readability | Relationship Evolution | Domain Expansion | Multi-Layer Overlays (Effort, Eval, Failure) | Git/Version Control Compatibility |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Mermaid** | High (Simple declarative markdown syntax)21 | Low (Mainly for rendering; difficult to parse nested attributes) | Poor (Requires manual syntax re-wiring for relationship shifts) | Medium (Domains can be added as subgraphs, but scale is limited) | Poor (No native support for complex custom metadata fields) | Excellent (Plain-text line diffs) |
| **Graphviz (DOT)** | Medium (Verbose parsing structures)22 | Medium (Parsable, but requires specific library interpreters)22 | Medium (Programmatic edge weight generation is supported) | Medium (Supports clusters, but can become unreadable at scale) | Medium (Supports custom attributes, but difficult to render as rich text) | Excellent (Highly deterministic line-by-line syntax) |
| **JSON Graph (JGF)** | Low (Highly verbose, deeply nested JSON structure)23 | Excellent (Native JSON parsing with formal schema validation)23 | High (Dynamic node and edge property modifications)24 | High (Supports native hyperedges and groupings)24 | High (Arbitrary nested metadata blocks allowed)24 | Poor (Formatting and sorting changes cause massive diffs) |
| **YAML Graph** | High (Clean indentation-based visual structure)26 | Excellent (Strict schema validation; maps directly to data structures)27 | High (Pointers via anchors and aliases prevent duplication)26 | High (Declarative directory splits support modular expansion)29 | High (Clean nested keys for metrics, effort, and bottlenecks)29 | Excellent (Highly readable, line-by-line git diffs)29 |
| **Neo4j (Cypher)** | Low (Requires a query interface; stored in binary files) | Excellent (Highly optimized transactional engine) | Excellent (Dynamic schema changes; relationships are first-class entities) | Excellent (Extremely scale-tolerant graph traversal) | Excellent (Native property graphs support dense metric layers) | Poor (Database dumps are binary or massive SQL-like transactions) |
| **Obsidian Canvas** | High (Visual spatial mapping for infinite canvas environments)30 | High (Standardized open JSON-based structure)31 | Medium (Connections can be added; lacks native anchor referencing) | High (Supports groups, nested canvases, and portals)30 | Medium (Limited custom metadata rendering within visual cards)30 | Medium (JSON-based layout updates yield readable line diffs)32 |
| **Figma / FigJam** | Excellent (Polished UI; supports real-time multiplayer editing)33 | Low (Requires parsing proprietary cloud-hosted APIs) | Poor (Visual nodes are decoupled from system implementation) | High (Infinite visual canvas support) | Poor (Requires manual styling of shapes to display metrics) | None (Cloud-hosted; changes tracked via custom history only) |

### **Comparative Analysis of Technologies**

Visual design suites like Figma and FigJam offer excellent design flexibility but lack semantic machine-readability33. This decouples visual representation from operational software execution3. While Neo4j provides a powerful, highly scalable engine for property graphs, it relies on complex external databases that cannot be tracked directly as source files in a code repository. Text-to-diagram generators like Mermaid and Graphviz work well with version control but lack the metadata density to represent complex operational properties, such as dual-process effort modes and physical queue limits11.  
JSON Graph Format (JGF) spec v2 supports structured property mapping and hyperedges but can be verbose and difficult to edit manually in plain text24. It is also prone to formatting changes that cause cluttered git diffs.  
In contrast, YAML graphs leverage block and flow structures, using anchors (&) and aliases (\*) to build clean, DRY (Don't Repeat Yourself) relationships26. This approach supports structured nested properties and validation via standard JSON Schema formats27.  
For visual environments, Obsidian Canvas uses an open, local-first JSON Canvas spec v1.031. This format defines node coordinates, textual cards, vault file embeddings, and edge groups without vendor lock-in30.

## **Recommended v0 Architectural Design**

To support human-centric visual design and programmatic machine-readability, the v0 architecture implements a **Hybrid Code-Canvas Dual-State Model**.  
This approach stores semantic data in declarative YAML files, which serve as the single source of truth27. A Python compilation script then processes these YAML files to generate the spatial and visual structures for an Obsidian .canvas layout31.

┌────────────────────────────────────────────────────────┐  
│               Developer Local Workspace                │  
│                                                        │  
│   ┌─────────────────────┐       ┌──────────────────┐   │  
│   │   YAML Graph Files  │ ────\> │ Python Sync CLI  │   │  
│   │ (Semantic Source of │ \<──── │ (canvas\_sync.py) │   │  
│   │       Truth)        │       └──────────────────┘   │  
│   └─────────────────────┘                 ▲            │  
│              │                            │            │  
│              ▼                            ▼            │  
│   ┌─────────────────────┐       ┌──────────────────┐   │  
│   │  JSON Schema Guard  │       │  Obsidian Visual │   │  
│   │ (Validation Layer)  │       │      Canvas      │   │  
│   └─────────────────────┘       │  (.canvas JSON)  │   │  
│                                 └──────────────────┘   │  
└───────────────────────────────────────────┼────────────┘  
                                            │ Commit Graph  
                                            ▼  
┌────────────────────────────────────────────────────────┐  
│                   Git Remote & CI/CD                   │  
│                                                        │  
│     ┌────────────────────────────────────────────┐     │  
│     │            GitHub Actions Runner           │     │  
│     │                                            │     │  
│     │  \- Lints & Validates Graph Schema          │     │  
│     │  \- Renders Structural Graphviz Layouts     │     │  
│     │  \- Posts Visual SVG Diffs on Pull Requests │     │  
│     └────────────────────────────────────────────┘     │  
└────────────────────────────────────────────────────────┘

This hybrid model addresses the project's core requirements:

1. **Human-Readable Overview:** Provided via the Obsidian Canvas UI, using visual groupings, colored cards, and zoom-scale rendering to make complex structures digestible30.  
2. **Machine-Readable Graph Data:** Maintained in clean YAML files and validated against strict schemas to serve as direct inputs for production models27.  
3. **Evolving Relationships & Domain Expansion:** Handled in the YAML files, using anchors and aliases to reference recurring parameters and prevent data duplication26.  
4. **Multi-Layer Overlays (Effort, Evaluation, Failure):** Represented as nested fields in the YAML schema29. The sync tool parses these fields and applies them as visual cues (such as colored card borders, dashes, and warning badges) on the canvas21.  
5. **Git Review Protocol:** Supported because changes are tracked as line-by-line YAML updates29, which are easily validated and previewed during pull request reviews.

## **Core Implementation Specifications**

### **Repository and File Structure**

menuella-cognitive-graph/  
├── .github/  
│   └── workflows/  
│       └── graph-validator.yml       \# CI pipeline for schema linting and PR validation  
├── schemas/  
│   ├── node-schema.json              \# Validator for cognitive node definitions  
│   └── edge-schema.json              \# Validator for semantic relationships  
├── graphs/  
│   ├── domains/  
│   │   ├── website.yaml              \# Node and edge data for SEO and digital menus  
│   │   ├── ordering.yaml             \# Node and edge data for carts and payments  
│   │   └── kitchen.yaml              \# Node and edge data for prep lines and capacity  
│   └── platform\_map.canvas           \# Generated visual Obsidian Canvas file  
├── tools/  
│   ├── canvas\_sync.py                \# Bi-directional compiler: YAML \<-\> Canvas  
│   └── requirements.txt              \# Script dependencies (PyYAML, jsonschema, click)  
└── README.md                         \# Setup guide and graphical design conventions

### **Cognitive Graph Schema Definition**

This JSON Schema validates node structures, edge mappings, and overlay definitions for the YAML files in the repository27.

JSON  
{  
  "$schema": "https://json-schema.org/draft/2020-12/schema",  
  "title": "MenuellaCognitiveGraphSchema",  
  "type": "object",  
  "required": \["graph"\],  
  "properties": {  
    "graph": {  
      "type": "object",  
      "required": \["id", "domain", "nodes", "edges"\],  
      "properties": {  
        "id": { "type": "string" },  
        "domain": {   
          "type": "string",   
          "enum": \["digital\_presence", "guest\_experience", "direct\_ordering", "kitchen\_operations", "core\_ml"\]   
        },  
        "nodes": {  
          "type": "object",  
          "additionalProperties": {  
            "type": "object",  
            "required": \["label", "type", "effort\_mode"\],  
            "properties": {  
              "label": { "type": "string" },  
              "type": { "type": "string", "enum": \["state", "computation", "action", "gateway"\] },  
              "effort\_mode": {  
                "type": "object",  
                "required": \["system", "computational\_cost"\],  
                "properties": {  
                  "system": { "type": "string", "enum": \["system\_1", "system\_2"\] },  
                  "computational\_cost": { "type": "string", "enum": \["low", "medium", "high"\] }  
                }  
              },  
              "eval\_score": {  
                "type": "object",  
                "properties": {  
                  "completion\_probability": { "type": "number", "minimum": 0, "maximum": 1 },  
                  "contribution\_margin\_usd": { "type": "number", "minimum": 0 },  
                  "f1\_score": { "type": "number", "minimum": 0, "maximum": 1 }  
                }  
              },  
              "failure\_modes": {  
                "type": "array",  
                "items": {  
                  "type": "object",  
                  "required": \["code", "impact", "active"\],  
                  "properties": {  
                    "code": { "type": "string" },  
                    "impact": { "type": "string", "enum": \["degraded", "halted", "ignored"\] },  
                    "active": { "type": "boolean" },  
                    "trigger\_condition": { "type": "string" }  
                  }  
                }  
              }  
            }  
          }  
        },  
        "edges": {  
          "type": "array",  
          "items": {  
            "type": "object",  
            "required": \["source", "target", "relation"\],  
            "properties": {  
              "source": { "type": "string" },  
              "target": { "type": "string" },  
              "relation": { "type": "string" },  
              "eval\_score": {  
                "type": "object",  
                "properties": {  
                  "transition\_probability": { "type": "number", "minimum": 0, "maximum": 1 }  
                }  
              },  
              "failure\_modes": {  
                "type": "array",  
                "items": {  
                  "type": "object",  
                  "required": \["code", "active"\],  
                  "properties": {  
                    "code": { "type": "string" },  
                    "active": { "type": "boolean" }  
                  }  
                }  
              }  
            }  
          }  
        }  
      }  
    }  
  }  
}

### **Visual and Graphical Conventions**

To ensure consistent formatting in the Obsidian Canvas, visual elements are mapped to semantic attributes (such as colors, shapes, and borders) to represent functional domains and live performance metrics21.

| Visual Attribute | Semantic Target | Visual Mapping | Visual Specification | Operational Interpretation |
| :---- | :---- | :---- | :---- | :---- |
| **Card Color** | Domain Scope1 | Green Card | Fill \#D1FAE5, Border \#059669 | Direct Ordering & Revenue: Handles carts, checkout, and payment processing1. |
|  |  | Amber Card | Fill \#FEF3C7, Border \#D97706 | Kitchen Operations: Monitors prep lines, printers, and terminal queues1. |
|  |  | Purple Card | Fill \#F3E8FF, Border \#7C3AED | Core Machine Learning: Runs recommendations and collaborative filtering11. |
|  |  | Blue Card | Fill \#DBEAFE, Border \#2563EB | Digital Presence: Manages QR menus, sites, and user acquisition1. |
| **Card Border** | Effort Mode13 | Standard Border | Solid line (1px width) | System 1: Immediate, low-cost execution paths and heuristic operations13. |
|  |  | Double Border | Double-stroke solid line (3px width) | System 2: Slow, multi-hop reasoning and resource-intensive processing13. |
| **Border Style** | Evaluation Score11 | Continuous Line | Clean, unbroken stroke | Optimal performance: High conversion rates and healthy latency metrics11. |
|  |  | Dotted Line | Intermittent, spaced dots | Fragile performance: Potential drop-offs, slow load times, or metric regressions2. |
| **Canvas Badges** | Active Blockages11 | Red Outline \+ Badge | Border \#EF4444, Red Glyph \[\!\] | System halted: Active operational issues, such as kitchen queue overloads11. |
|  |  | Gray Outline | Border \#9CA3AF, Dashed Border | Inactive guardrail: Passive safety limits or fallback logic11. |

## **Example Visual Node Graph: Predictive Neural Upsell Flow**

Below is a complete, validated YAML graph configuration representing the Menuella *Predictive Neural Upsell Flow*11.  
This example details how the system recommends high-margin items—like Manurella Sticks7—by evaluating neural probabilities11, checking physical kitchen limits11, and managing fallback pathways if a station is overloaded11.

YAML  
%YAML 1.2  
\---  
graph:  
  id: predictive\_neural\_upsell\_flow  
  domain: core\_ml  
  nodes:  
    \# \--- DIRECT ORDERING SCOPE \---  
    CART\_BUILD: \&ordering\_cart\_anchor  
      label: "Customer Building Cart on Direct Channel"  
      type: "state"  
      effort\_mode:  
        system: "system\_1"  
        computational\_cost: "low"  
      eval\_score:  
        completion\_probability: 0.94  
      failure\_modes:  
        \- code: "CART\_ABANDONMENT"  
          impact: "degraded"  
          active: false  
          trigger\_condition: "inactivity\_seconds \> 180"

    PROMPT\_UPSELL\_UI:  
      \<\<: \*ordering\_cart\_anchor  
      label: "Render Upsell Drawer: Suggest Manurella Sticks ($3.99)"  
      type: "action"  
      eval\_score:  
        completion\_probability: 0.62 \# target completion match percentage

    \# \--- CORE ML SCOPE \---  
    NEURAL\_RANKER:  
      label: "Run Neural Ranker Engine"  
      type: "computation"  
      effort\_mode:  
        system: "system\_2"  
        computational\_cost: "high"  
      eval\_score:  
        f1\_score: 0.88 \# target model accuracy  
        contribution\_margin\_usd: 2.80 \# margin check for Manurella Sticks  
      failure\_modes:  
        \- code: "MODEL\_TIMEOUT"  
          impact: "degraded"  
          active: false  
          trigger\_condition: "latency\_ms \> 120"

    \# \--- KITCHEN OPERATIONS SCOPE \---  
    FRYER\_QUEUE\_CHECK: \&kitchen\_queue\_anchor  
      label: "Verify Fryer Station Queue Capacity"  
      type: "gateway"  
      effort\_mode:  
        system: "system\_1"  
        computational\_cost: "low"  
      failure\_modes:  
        \- code: "STATION\_FRYER\_OVERLOADED"  
          impact: "halted"  
          active: true \# Active physical blockage  
          trigger\_condition: "fryer\_queue\_depth \> 10"

    POPULARITY\_FALLBACK:  
      label: "Trigger Naive Popularity Recommendations"  
      type: "action"  
      effort\_mode:  
        system: "system\_1"  
        computational\_cost: "low"  
      eval\_score:  
        completion\_probability: 0.15 \# baseline non-neural completion

  edges:  
    \# Triggers evaluation when item is added to cart  
    \- source: "CART\_BUILD"  
      target: "NEURAL\_RANKER"  
      relation: "triggers\_calculation"  
      eval\_score:  
        transition\_probability: 1.0

    \# ML output is verified against kitchen capacity  
    \- source: "NEURAL\_RANKER"  
      target: "FRYER\_QUEUE\_CHECK"  
      relation: "validates\_executability"  
      eval\_score:  
        transition\_probability: 0.98

    \# Standard path when kitchen has available capacity  
    \- source: "FRYER\_QUEUE\_CHECK"  
      target: "PROMPT\_UPSELL\_UI"  
      relation: "execute\_neural\_upsell"  
      eval\_score:  
        transition\_probability: 0.38  
      failure\_modes:  
        \- code: "STATION\_FRYER\_OVERLOADED"  
          active: true \# System routes around the fryer if capacity is exceeded

    \# Fallback path if fryer is overloaded  
    \- source: "FRYER\_QUEUE\_CHECK"  
      target: "POPULARITY\_FALLBACK"  
      relation: "route\_around\_bottleneck"  
      eval\_score:  
        transition\_probability: 0.62  
      failure\_modes:  
        \- code: "STATION\_FRYER\_OVERLOADED"  
          active: false \# Backup path used successfully

## **Git-Based Change Review and Validation Protocol**

To maintain the integrity of the Cognitive Graph across updates, modifications must go through a structured version-control review process. This pipeline ensures that updates to the YAML files are linted, validated, and visually audited before being merged into the codebase27.

### **Local Verification and Linting Steps**

Before pushing updates, developers run a local git pre-commit hook to parse the YAML configurations and validate them against the JSON schemas27. This ensures that common errors, such as syntax mistakes or missing fields, are caught during development26.

Bash  
\# 1\. Install verification packages  
pip install jsonschema pyyaml

\# 2\. Run schema validation on graph files  
jsonschema \--instance graphs/domains/ordering.yaml schemas/node-schema.json

If validation fails, the commit is rejected, protecting the repository from invalid code structures.

### **Automated Pull Request Workflow**

When a pull request is opened, an automated pipeline verifies the changes. The pipeline lints the YAML, validates it against the schema, and renders a visual representation of the updates27.

YAML  
name: "Cognitive Graph Integration Guard"

on:  
  pull\_request:  
    paths:  
      \- 'graphs/domains/\*\*'  
      \- 'schemas/\*\*'

jobs:  
  validate-and-diff:  
    runs-on: ubuntu-latest  
    steps:  
      \- name: Checkout Codebase  
        uses: actions/checkout@v4  
        with:  
          fetch-depth: 0

      \- name: Setup Python Environment  
        uses: actions/setup-python@v5  
        with:  
          python-version: '3.11'

      \- name: Install Validation Dependencies  
        run: |  
          python \-m pip install \--upgrade pip  
          pip install jsonschema pyyaml graphviz

      \- name: Validate YAML Formats  
        run: |  
          python \-c "  
          import yaml, jsonschema, json  
          schema \= json.load(open('schemas/node-schema.json'))  
          data \= yaml.safe\_load(open('graphs/domains/ordering.yaml'))  
          jsonschema.validate(instance=data, schema=schema)  
          "

      \- name: Generate Visual Graph Diff Diagram  
        run: |  
          \# Render graph differences as visual SVG maps  
          python tools/canvas\_sync.py \--render-diff \--origin origin/main \--target HEAD

### **Visual Code Reviews and Structural Diffs**

Reviewing large YAML changes in raw text can make it difficult to spot structural shifts, such as altered paths or new failure states23.  
To make reviews more intuitive, the pipeline generates a visual layout of the graph differences and posts it directly as a comment on the Pull Request22:

─────────────────────────────────────────────────────────────────────────────  
\[Automated BOT Comment\] Cognitive Graph Review Report  
─────────────────────────────────────────────────────────────────────────────

Validation Status: PASS ✅  
Detected Schema Version: v1.2 \[cite: 36\]

Visual Structural Diff (Main vs. Pull Request):

          ┌───────────────────────────────────┐  
          │      Ordering: CART\_BUILD         │  
          └─────────────────┬─────────────────┘  
                            │  
                            ▼  
          ┌───────────────────────────────────┐  
          │      ML: NEURAL\_RANKER            │  
          └─────────────────┬─────────────────┘  
                            │  
                ┌───────────┴───────────┐  
                ▼ \[No Change\]           ▼ \[NEW ROUTE ADDED\]  
     ┌─────────────────────┐   ┌───────────────────────────┐  
     │ FRYER\_QUEUE\_CHECK   │   │  POPULARITY\_FALLBACK      │  
     └─────────────────────┘   │ (Dotted Line / Alternate) │  
                               └───────────────────────────┘

Changes Summary:  
\- Added Edge: \[FRYER\_QUEUE\_CHECK\] ──(route\_around\_bottleneck)──\> \[POPULARITY\_FALLBACK\]  
\- Active Failure Flag Modifiers: Node \[FRYER\_QUEUE\_CHECK\] has failure mode  
  "STATION\_FRYER\_OVERLOADED" flagged as Active.  
─────────────────────────────────────────────────────────────────────────────

By presenting both a visual map and raw code diffs29, developers can review semantic updates clearly within GitHub while the production environment stays updated with validated, machine-readable configurations.

#### **Works cited**

1. About Menuella – Our Story, Vision & Mission, [https://www.menuella.com/about](https://www.menuella.com/about)  
2. Direct ordering & revenue – Blog | Menuella, [https://www.menuella.com/blog/category/direct-ordering-revenue](https://www.menuella.com/blog/category/direct-ordering-revenue)  
3. Cognitive Graphs: A General Architecture for Replayable Reasoning \- Programmer.ie: Modern AI programming, [https://www.programmer.ie/post/graph/](https://www.programmer.ie/post/graph/)  
4. Decision \- Aaron Bornstein, [http://aaron.bornstein.org/cv/pubs/2024\_ycb\_dec.pdf](http://aaron.bornstein.org/cv/pubs/2024_ycb_dec.pdf)  
5. (PDF) PacketNodes : An Adaptive Sparse-Dense Cognitive Graph Architecture for Human-AI Knowledge Co-Evolution \- ResearchGate, [https://www.researchgate.net/publication/405864928\_PacketNodes\_An\_Adaptive\_Sparse-Dense\_Cognitive\_Graph\_Architecture\_for\_Human-AI\_Knowledge\_Co-Evolution](https://www.researchgate.net/publication/405864928_PacketNodes_An_Adaptive_Sparse-Dense_Cognitive_Graph_Architecture_for_Human-AI_Knowledge_Co-Evolution)  
6. Structuring Knowledge with Cognitive Maps and Cognitive Graphs \- PMC \- NIH, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7746605/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7746605/)  
7. Brookville Deli & Caterers \- Hibu, [https://cdn.websites.hibu.com/a7f1bb76a84b4877bebf0e16da2e7764/files/uploaded/Regular%20Menu.pdf](https://cdn.websites.hibu.com/a7f1bb76a84b4877bebf0e16da2e7764/files/uploaded/Regular%20Menu.pdf)  
8. "Mental maps": Between memorial transcription and symbolic projection \- PubMed, [https://pubmed.ncbi.nlm.nih.gov/37057159/](https://pubmed.ncbi.nlm.nih.gov/37057159/)  
9. Design Principles of the Hippocampal Cognitive Map, [https://proceedings.neurips.cc/paper\_files/paper/2014/file/6083b607d0b81940c0280e465c79f5d5-Paper.pdf](https://proceedings.neurips.cc/paper_files/paper/2014/file/6083b607d0b81940c0280e465c79f5d5-Paper.pdf)  
10. Design Principles of the Hippocampal Cognitive Map \- NIPS, [https://papers.nips.cc/paper\_files/paper/2014/file/6083b607d0b81940c0280e465c79f5d5-Paper.pdf](https://papers.nips.cc/paper_files/paper/2014/file/6083b607d0b81940c0280e465c79f5d5-Paper.pdf)  
11. Neural Pairings: Using Order History to Drive High-Margin Discovery | Menuella, [https://www.menuella.com/blog/restaurant-order-history-high-margin-discovery-smart-upsells](https://www.menuella.com/blog/restaurant-order-history-high-margin-discovery-smart-upsells)  
12. The hippocampus as a cognitive graph \- PubMed \- NIH, [https://pubmed.ncbi.nlm.nih.gov/8783070/](https://pubmed.ncbi.nlm.nih.gov/8783070/)  
13. Cognitive Graph for Multi-Hop Reading Comprehension at Scale \- ACL Anthology, [https://aclanthology.org/P19-1259.pdf](https://aclanthology.org/P19-1259.pdf)  
14. Cognitive Graph for Multi-Hop Reading Comprehension at Scale \- Knowledge Engineering Group, [https://keg.cs.tsinghua.edu.cn/jietang/publications/ACL19-Ding-et-al-Cognitive\_Graph.pdf](https://keg.cs.tsinghua.edu.cn/jietang/publications/ACL19-Ding-et-al-Cognitive_Graph.pdf)  
15. \[1905.05460\] Cognitive Graph for Multi-Hop Reading Comprehension at Scale \- arXiv, [https://arxiv.org/abs/1905.05460](https://arxiv.org/abs/1905.05460)  
16. Predictive Neural Upsells for Restaurants | Menuella, [https://www.menuella.com/smart-upsells](https://www.menuella.com/smart-upsells)  
17. Beyond the Black Box: A Cognitive Architecture for Explainable and Aligned AI \- arXiv, [https://arxiv.org/html/2512.03072v1](https://arxiv.org/html/2512.03072v1)  
18. Clone-structured graph representations enable flexible learning and vicarious evaluation of cognitive maps \- PubMed, [https://pubmed.ncbi.nlm.nih.gov/33888694/](https://pubmed.ncbi.nlm.nih.gov/33888694/)  
19. Manuela 2.0: AI Revolutionizes Technical Documentation | Memori, [https://memori.ai/en/blog/manuela-2-0-ai-revolutionizes-technical-documentation](https://memori.ai/en/blog/manuela-2-0-ai-revolutionizes-technical-documentation)  
20. MEDULA AI, [https://medulaai.app/](https://medulaai.app/)  
21. gravis JSON Graph Format (gJGF) \- GitHub Pages, [https://robert-haas.github.io/gravis-docs/rst/format\_specification.html](https://robert-haas.github.io/gravis-docs/rst/format_specification.html)  
22. abargnesi \- npm | Profile, [https://npmjs.com/\~abargnesi](https://npmjs.com/~abargnesi)  
23. a general data format for RNA interactions \- PMC \- NIH, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10640394/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10640394/)  
24. jsongraph/json-graph-specification: A proposal for representing graph structure (nodes / edges) in JSON. \- GitHub, [https://github.com/jsongraph/json-graph-specification](https://github.com/jsongraph/json-graph-specification)  
25. JGF \- Maple Help \- Maplesoft, [https://www.maplesoft.com/support/help/maple/view.aspx?path=Formats/JGF](https://www.maplesoft.com/support/help/maple/view.aspx?path=Formats/JGF)  
26. YAML Glossary, [https://yaml.com/resources/glossary/](https://yaml.com/resources/glossary/)  
27. Configure WebAssembly Graph Definitions For Data Flow Graphs \- Azure IoT Operations, [https://learn.microsoft.com/en-us/azure/iot-operations/develop-edge-apps/howto-configure-wasm-graph-definitions](https://learn.microsoft.com/en-us/azure/iot-operations/develop-edge-apps/howto-configure-wasm-graph-definitions)  
28. colltoaction/yaml-graph-jsonschema: The YAML Representation Graph spec encoded as JSON \- GitHub, [https://github.com/colltoaction/yaml-graph-jsonschema](https://github.com/colltoaction/yaml-graph-jsonschema)  
29. AIP: A Graph Representation for Learning and Governing Agent Skills \- arXiv, [https://arxiv.org/html/2606.04781v1](https://arxiv.org/html/2606.04781v1)  
30. Developer-Mike/obsidian-advanced-canvas: Supercharge your canvas experience\! Graph view integration and unlimited styling options empower flowcharts, dynamic presentations, and interconnected knowledge. \- GitHub, [https://github.com/developer-mike/obsidian-advanced-canvas](https://github.com/developer-mike/obsidian-advanced-canvas)  
31. Announcing JSON Canvas: an open file format for infinite canvas data \- Obsidian, [https://obsidian.md/blog/json-canvas/](https://obsidian.md/blog/json-canvas/)  
32. Schema | obsidian-mcp-pro \- Glama, [https://glama.ai/mcp/servers/rps321321/obsidian-mcp-pro/schema](https://glama.ai/mcp/servers/rps321321/obsidian-mcp-pro/schema)  
33. Free Mind Map Template \- Milanote, [https://milanote.com/templates/brainstorming/mind-map](https://milanote.com/templates/brainstorming/mind-map)  
34. Free Mind Map Maker \- Whimsical, [https://whimsical.com/mind-maps](https://whimsical.com/mind-maps)  
35. Mind Map Prezi Template \- Saskia imanuella, [https://prezi.com/p/\_6r9ce5fveew/mind-map-prezi-template/](https://prezi.com/p/_6r9ce5fveew/mind-map-prezi-template/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEgAAAAZCAYAAACSP2gVAAADcUlEQVR4Xu2YS6hNYRTHlxBCiDyivEUU8ijFCEUhKY8yNCAZiCJGd2ImA68kkoFnykCKUo4MKBMDUqIuiQykFIU81u+sve7Z+7P3PvucyzlH7V/96+5vfft7rG+ttb9zRUpK/heGhA0tYJbqjWp39NxfNaxm7hwWqiaGjS1gu+qXqit6xjkXVLu8Q6Pg8ZOqh6rXqrOq4YkeSZjwvFjfx6rjqknxDmLOeR60tYI+qnOqr6olsfaRqgeRvWlWiG34u2ppYHMWiznniepnYHN2iDlvcmhoAQtUn1RbQoPST1WRXqT9QbFQJDzXBjbntGqj6rNYnoeMUT0Ti6penVaTkF7MzzrS+KZaFTYWYaDqhuqomIP2J81V2DDO8Ry/mTRXWaf6IRaN7YD06gobYzxVXRKLpoaYIFaD9oht/kzSXIX0GiC2iCwnYiOyGC8PnE1d6BsaGoRIidfLiiRrTwgZ0q0aH7TX5ZDYhslh0ueRakTMjuO2itUmatRLSQ/jd2I1KgvqEw6cGT1fVN1RDe7pUZ9BYtF+LXqeK7Ye1lgPSgeHuyE05EF6XRdLiylim4xHwWyxiGJhHmEsLi1McS7OzgLHX5Za5DAWc7OGovghbYqeT4mNs62nRzbskY9LWvRnglPui4XdKLE8ZaNEE07BOTgJcAyLoQ6lwXt5k78Sq1HHxFJ2tDTmHPAo4CCnikUf4xRJV8+QvDX+AYX1qlhEMBkh718yHBF3Rrfqi2pRrC0O94+8yZmHsV07pfGv3TTVW6mN8UI1L9Ejm4YdNFR1W5L3Hl5m4sOq+bF2oJ1CnLUpJk8r8DBDtTz2THT6QRRlveqI1NJ/ulj9ITLHeaccPPqK1Ksqc1T3xFLLoRgzSHgRJBVox54FC02rTx6ZofM+iN3kHW70d8WcmQaXQNawOnrmgCkPXDmKpKrvzd/PhZy9InYCOMqjwgsZG3KwEcakEPasCOKd8AsI7iA/eSBV9klyLE+brLvKe7F7Dj9AYbNYLaKeFYEPSHgoLYU7CE7MKuLcfUiFvKLKRwMHZf0kwDlcMYqkVAjOafpH69/A7yi3or+bgZ8C1L9/AdeXdvxGTLBM9VG1MjQUAKcSPXm34WYhaveGje2AmkJtqQTtReC9E5Jef3oDazogHfaPM2rFmrCxDVDT+HqODQ0lJSUlnchvVNusXKT7I9oAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAaCAYAAABozQZiAAAA3klEQVR4Xu3SPQ4BQRiA4U9oROUnEomWRqNSOQC1QuEKGk7gAhpR6cUVVApUNCIkEp1GpdASP+9kbOxOYmdbyb7Jk8jMZHfyLZF/KI0V+uZGkKq4Y2huBKmLJ2rmhq0IxlgjaexZy2CPnrEeqBamiJsbZlFkRU9XXVc1EP0A39q4YI4dNp/1FBLOoV8dUfj8zmPp2vMth5voK5ZEv0kNKlAxvFyuqHtOWOpgi4foB6jPY60o+rpOakAL0cPzTV13It7hVHBGw7X2szIOGGGGE5ry/c7W1EE1cfefIyxM3gBoIyqExACmAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAm0lEQVR4XmNgGAW0AsxALAbEwkDMiCYHBzlA/BaIDwHxFSC+gCqNALeBWBXKlgHiI0hycCAJxL+AeBIQawMxNxCLoKiAAhYg/o+EPwKxJ4oKJFAIxJeA+C8DRPFVVGkGBjUGiJUwIATEhxkgHoMDkJXLGVAdbgbEz4E4GEkMDAyA+AYQzwLifUD8CIjDGXCEI0gQ5HO8AT0KKAMA0PYZLAbjc+QAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,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>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE4AAAAaCAYAAAAZtWr8AAACqUlEQVR4Xu2YvWsVQRTFr0TBoIIfISI2UUyhRCyMiIWNiGhhF0QRsTT/gaQJQgpb0UIwAUExNoEggh9dwFIr0UoCUdBAwEZQBBP1HGbmvbc3O7vzdt7bDcn+4LDZuZvdnfPu3rm7IjU1G50eqB/aB21RsTLgdantOrDW4U1/hJ5AA8lQKTyA3kE3dWCtQ+Pm7FbDTDwlJsbMjGETdEgPWmjaujFuAPogJiPeQJ8S0XBo2BHoGbSQDDVYN8Yx02har91ntt2W9h/lo9AK9Av6B31OhhuUbhwndAmah96KyY670FVopOW4LLRxLNLc/273Ha4W9qnxEI5DP6VDxjGF90A7dSAQroD3oVnogIq1gzbuILQoqydJQzl5mtAuHTOOpvEkTF/qoYqNt+z7mBCTYbEthDbON0kax3u9qMZD8J3TEWzcNTHP/le75Q3RMMKV56X9O4sXYjI2Fm3cWeivrJ5k5cbdgUbVGLPmMrQXmrHbPC6ImWyWQtDG8bxphbxy43ZL+uPFon4DuqXGfSxBX3IUgjbON8nKjfPxGnoODemAB2ZGJ9DG+RaHHWLaihNqPISuGseWYhrarAMe7kmzLsagjdslprX54Q6wML4A7VfjIXTVOBb7kNrmGIbei3klikEbR7hAfZNmSeEPNAadbBxh4KOb16Lwf89Df8SUl7QfO8o49mNb9WAOh8V0+I+gYyoWSppx5Az0VMyiNSnmMdWT/g0ti7/u8Zyu5WrVnCS/hkQZx8WhCMwK3vgrabY2TiH4jCPnoOt2u03FHOwnY+ttYePoPl+TqiDLuDz4LvtYTObHUNg4XjirTnSTGONOQ1MSvqD5KGzcFT1QIjSMn41YI9P6yywG9UABeH0+7oWMqxJ+QqJxbJj5GahsXLOu36ZqampqNgz/AX1Xnk1EZN4oAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,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>

[image7]: <data:image/png;base64,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>