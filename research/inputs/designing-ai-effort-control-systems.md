# **Operationalizing Test-Time Compute: A Comparative Analysis of Frontier Effort Controls and the Architecture of the Manurella Agentic Engine**

## **The Paradigm of Test-Time Compute and Behavior Control**

The operational paradigm of large language models has undergone a structural shift from single-turn next-token prediction to test-time compute scaling. Rather than relying solely on the raw capability ceiling established during pre-training and alignment, modern frontier systems utilize serial test-time compute1. This architecture allows the underlying model to generate multiple, sequential reasoning steps internally before producing a final output1. Empirically, accuracy on mathematically dense and logic-sensitive tasks scales logarithmically with the volume of serial reasoning tokens allocated to the request1. This paradigm enables models to explore alternative reasoning paths, identify contradictions, and backtrack when initial assumptions fail1.  
However, the expansion of test-time compute introduces unique behavioral challenges, particularly within autonomous software engineering agents. Traditional evaluation frameworks often assess coding agents using a binary success signal, such as whether a generated patch passes a target test suite5. Trace analyses on benchmarks like SWE-bench Verified reveal that this outcome-only view frequently obscures sub-optimal problem-solving pathways5. Approximately 10.7% of successful trajectories exhibit behaviors classified as "Lucky Passes"—solutions characterized by regression cycles, blind retries, missing validation steps, or disordered exploration5. To address this instability, modern systems utilize structured process-level guidance5. Implementations like AgentLens and SWE-TRACE use Process Reward Models to evaluate intermediate steps, steering the agent away from wasteful computational branches early in the execution lifecycle5.  
Consequently, behavioral controls have emerged as a critical mechanism to regulate agent trajectories8. Effort controls act as direct dials that alter not only the length of the internal thinking chain but also the fundamental interaction style of the model8. Lower effort configurations prioritize latency and token efficiency, prompting the model to combine operations into fewer tool calls, proceed directly to actions without explanatory preambles, and output terse confirmations8. Conversely, higher effort configurations instruct the model to draft explicit plans, detail architectural assumptions, write extensive code comments, and systematically verify results8.

## **Comparative Evaluation of Frontier Thinking and Effort Implementations**

Frontier artificial intelligence providers have approached test-time compute management through distinct API architectures, budget visibility models, and tool integration paradigms. The following table delineates the structural differences between the three primary native implementations: Anthropic Claude, OpenAI O-Series, and Google Gemini.

| Architectural Dimension | Anthropic Claude (Sonnet 4.6 / Opus 4.7 & 4.8) | OpenAI O-Series (gpt-5.5 / gpt-5.5-pro) | Google Gemini (Gemini 3 / 2.5) |
| :---- | :---- | :---- | :---- |
| **Native API Parameter** | output\_config.effort combined with thinking: {"type": "adaptive"} \[cite: 8, 11\] | reasoning.effort under the Responses API2 | thinking\_config.thinking\_level or thinking\_budget \[cite: 13, 14, 15\] |
| **Supported Levels** | low, medium, high (default), xhigh, max \[cite: 8\] | none, minimal, low, medium (default), high, xhigh \[cite: 2, 12\] | LOW, MEDIUM, HIGH (or token values 0 to 32,768)13 |
| **Thinking Visibility** | Optional ("summarized" or "omitted"); full reasoning is encrypted in signatures for multi-turn continuity17 | Invisible reasoning tokens returned in metadata; option to include encrypted content2 | Direct access via candidates\[0\].content.parts.thought or summarized thought blocks16 |
| **Multi-Turn State Management** | Managed client-side by appending thinking blocks, or automated via server-side task budgets11 | Stateful via the Responses API (store: true) or chained via previous\_response\_id \[cite: 2, 12\] | Automatic via Firebase/Vertex SDKs utilizing thought signatures13 |
| **Tool Calling Interaction** | Higher effort increases plan preambles and tool iterations; lower effort combines operations and bypasses preambles8 | Tool calls are interleaved with thinking; starting with GPT-5.4, tool calls are blocked if effort is set to none \[cite: 2\] | High thinking levels optimize complex function calling and multi-step tool execution sequences15 |
| **Context Compaction** | Context compaction summaries automatically compress older history as conversations approach limits (beta)19 | Automatic context management with customizable compaction thresholds (compact\_threshold)2 | Leverages massive native context windows (up to 2M) with automatic caching and retrieval13 |

### **The Anthropic Claude Effort and Task Budget Architecture**

Anthropic's computational management paradigm splits the control of individual execution steps from the total budget of the multi-turn agentic rollout8. The primary mechanism for regulating step-level reasoning is the effort parameter, which operates alongside adaptive thinking8. Under adaptive thinking, the model dynamically determines whether and how much to use extended thinking based on the complexity of each request17. The effort setting serves as a behavioral bias rather than a rigid constraint8. Even at lower levels, Claude will think if confronted with a highly complex problem, but it will allocate fewer tokens than it would under a high or max setting8. On newer models like Claude Opus 4.8 and Claude Opus 4.7, manual token configuration is deprecated, and adaptive thinking is the exclusive mode8.  
Anthropic manages long-horizon execution costs through the API's task\_budget configuration11. This schema, activated under the task-budgets-2026-03-13 beta header, allows developers to set a token allocation (minimum 20,000 tokens) across an entire agentic loop11. The API injects an internal countdown marker server-side, visible only to the model11. Claude uses this signal to track its remaining token budget and pace its execution, allowing it to conclude its operations and summarize its progress before the budget is completely exhausted11.  
To optimize latency, Anthropic supports omitting visible thinking blocks from responses17. However, the full reasoning content remains encrypted inside a signature field17. In multi-turn stateless applications, developers must pass these signatures back to the server unchanged, enabling the model to reconstruct its context and maintain logical continuity across turns17.

### **OpenAI Responses API and Interleaved Computational Allocation**

OpenAI’s reasoning architecture, spanning models like gpt-5.5 and gpt-5.5-pro, has transitioned away from the traditional Chat Completions API in favor of the Responses API2. Under this architecture, reasoning models use interleaved thinking, allowing them to switch dynamically between generating hidden reasoning tokens and emitting visible outputs2. The reasoning.effort parameter controls this computational allocation, supporting values from none (which disables reasoning) to xhigh (reserved for high-value asynchronous research tasks)2. For example, gpt-5.5-pro is engineered with a context window of 1,050,000 tokens and 128,000 max output tokens to support intense, multi-minute reasoning processes on highly complex tasks2.  
The Responses API natively manages multi-turn state via the store: true parameter, maintaining reasoning and tool context automatically across the conversation2. If developers manage state statelessly (store: false), they must manually extract and append all reasoning items from previous turns2. Excluding these items forces the model to restart its reasoning process at every turn, leading to high latency and excessive token consumption2.  
Furthermore, because output token limits restrict all generated tokens—including reasoning, visible text, and hidden formatting tokens—OpenAI recommends reserving a buffer of at least 25,000 tokens when setting max\_output\_tokens to prevent premature truncation during the thinking phase2.

### **Google Gemini Dynamic Thinking and Thought Summaries**

Google’s Gemini 3.x and 2.5 series models manage test-time compute through the thinkingConfig object inside GenerationConfig13. Gemini 3.x models use dynamic thinking, where the model decides when and how much to think up to a threshold configured via thinking\_level (supporting LOW, MEDIUM, and HIGH tiers)13. For Gemini 2.5 models, this control is mapped to a numeric thinkingBudget token count, where a value of \-1 enables dynamic thinking with an 8,192-token ceiling, and a value of 0 completely disables the thinking phase13.  
Gemini provides direct access to these internal steps through structured thought summaries, allowing real-time monitoring of the model's trajectory without imposing the latency penalties associated with streaming raw reasoning tokens13. The Firebase AI Logic SDKs automatically manage thought signatures to preserve context during multi-turn tool calling sequences13.

### **Agentic Frameworks and Simulated Test-Time Compute**

When native model effort controls are absent or insufficient, developer frameworks simulate test-time compute through explicit orchestration layers21.  
Kilo Code provides an open-source IDE and CLI extension that coordinates tasks across specialized modes, such as Architect, Code, Debug, and Ask, using slash commands like /architect, /fast, and /ultra-plan22. It includes an open model gateway to route tasks across local runners like Ollama and commercial providers23.  
OpenAI’s Codex operates as an autonomous coding agent that runs inside isolated cloud sandboxes preloaded with the target repository27. It uses models like codex-1 and gpt-5.3-codex to run tasks and generate complete pull requests27. It supports three safety modes: auto-approve, confirm-on-write, and confirm-everything28.  
On benchmarks, Codex (powered by GPT-5.5) leads on Terminal-Bench 2.0 (measuring terminal and systems tasks), while Claude Opus 4.7 leads on SWE-bench Pro (measuring multi-file refactoring)28.  
Other frameworks rely on structured environments to manage execution safety and accuracy29. AWS Bedrock AgentCore provides secure, microVM-isolated environments that run Claude Code or Codex, tracking every execution via CloudTrail and OpenTelemetry29.  
Aider and SWE-agent implement automated lint-and-test loops, executing compilers or test runners on edited files and triggering auto-rollbacks if a non-zero exit code is detected, which eliminates compile errors before any git commits are written30.  
For state management, LangGraph provides a robust framework using state machines with nodes and conditional edges, enabling self-correcting Generator-Critic loops that route unsatisfactory outputs back to the generator for revision33.  
For multi-agent delegation, frameworks enforce strict protocols to manage responsibility and permission boundaries35. The Delegation Authority System (DAS) model utilizes a three-point verification lifecycle consisting of pre-execution intent checking (using keyword filters and context-enriched Natural Language Inference), at-execution tool manifest enforcement, and post-execution output schema validation to prevent cascading failures in multi-agent networks37.

## **The Manurella Engine Effort System Specification**

The Manurella agentic engine implements a modular execution framework across six distinct effort tiers: Low, Medium, High, Extra High, Max, and Ultra. Each tier is optimized for specific computational, contextual, and verification profiles.

### **Low Effort Tier**

The Low Effort Tier is engineered to minimize latency and operational costs, making it ideal for routine tasks such as simple code search, syntax classification, and straightforward text generation8.

* **Reasoning Configuration:** The engine completely disables native adaptive thinking, setting the thinking budget to zero13. The model operates in a direct, next-token generation pattern, relying on immediate pattern recognition and pre-trained heuristics3.  
* **Context Loading Changes:** Ingestion is restricted strictly to the active file buffer or immediate user prompt. Systemic directory indexing, repository maps, and dependency graphs are entirely unloaded to minimize input token costs.  
* **Delegation Rules:** Single-agent execution only38. The system is blocked from decomposing the task or spawning any sub-agents, forcing the primary model to resolve the request in a single turn.  
* **Verification Thresholds:** Programmatic verification is entirely disabled. The agent bypasses syntax checks, linters, and unit tests, writing its raw output directly to the workspace31.  
* **Output Requirements:** Terse, direct completions8. The agent emits code blocks or text answers directly, omitting design preambles, summaries, or post-execution explanations8.  
* **Core Failure Modes:** Highly prone to syntax errors, referencing missing or invalid helper functions, and failing on tasks requiring context outside the immediate file3.  
* **Runtime Simulation Strategies:** On runtimes lacking native effort controls, Low Effort is simulated by appending strict system directives that forbid chain-of-thought generation or step-by-step reasoning, forcing the model to respond in a single direct output block:  
  XML  
  \<system\_instructions\>  
  Execute the task immediately. Do not generate preambles, chain-of-thought blocks, or explanations. Format code blocks immediately. Bypassing reasoning is mandatory.  
  \</system\_instructions\>

### **Medium Effort Tier**

The Medium Effort Tier represents the balanced baseline for standard interactive software development, feature refactoring, and tool-heavy workspace tasks8.

* **Reasoning Configuration:** Lightweight adaptive thinking is enabled, with thinking tokens capped at a low ceiling (e.g., 2,048 tokens) to prevent latency spikes while allowing basic logical validation3.  
* **Context Loading Changes:** Ingests the active file plus its immediate import declarations, adjacent file headers, and a lightweight folder layout tree to provide basic structural context.  
* **Delegation Rules:** Single-agent orchestration with restricted helper calls38. The primary model can delegate highly isolated subtasks to single-turn helper agents, such as generating a regex string or parsing a single JSON schema38.  
* **Verification Thresholds:** Static analysis checks are triggered on file modifications30. If the local linter (e.g., eslint or flake8) returns a non-zero exit code, the agent is allowed exactly one correction loop to fix the syntax4.  
* **Output Requirements:** Standard structured format25. The agent outputs a brief planning statement prior to modifying files, followed by the code changes, and concludes with a concise summary of the changes8.  
* **Core Failure Modes:** Vulnerable to regression bugs where changes break remote, unloaded modules, and occasional early truncation on long-horizon generation tasks.  
* **Runtime Simulation Strategies:** Simulated by appending a standard prompt wrapper that requests a brief two-step outline before code execution, alongside explicit syntax check instructions:  
  XML  
  \<system\_instructions\>  
  Before writing code, output a brief \<plan\> containing no more than three bullet points. Execute the code, then perform a quick mental dry-run to verify syntactic correctness.  
  \</system\_instructions\>

### **High Effort Tier**

The High Effort Tier is designed for complex reasoning, architectural refactoring, and multi-file debugging tasks8.

* **Reasoning Configuration:** Full adaptive thinking is enabled8. The model is permitted to utilize up to its default high-capacity thinking threshold (e.g., 16,384 tokens) to traverse deep logical branches3.  
* **Context Loading Changes:** Integrates a comprehensive repository index23. The system loads the target files, their full dependency graph, and queries the codebase map using keyword and semantic search vectors.  
* **Delegation Rules:** Spawns specialized multi-agent teams25. The Orchestrator agent decomposes the objective into discrete subtasks and delegates execution to specialized Coder and Debugger agents25.  
* **Verification Thresholds:** Sandbox compilation and testing30. The agent executes the codebase compiler and triggers the local unit test suite (e.g., pytest or jest) on modified files30. Up to three correction loops are allowed on test failures4.  
* **Output Requirements:** Thorough architectural plans8. The output must contain a detailed design justification, comments on all modified lines of code, and a list of verified files.  
* **Core Failure Modes:** High token consumption and increased latency, with the agent occasionally over-explaining trivial decisions or stalling during validation loops28.  
* **Runtime Simulation Strategies:** Programmatically orchestrated using a three-node LangGraph state machine: a Planning Node, a Code Generation Node, and a Test-and-Compile Node33. The graph routes execution dynamically:  
  Python  
  def route\_execution(state: AgentState):  
      if state\["test\_exit\_code"\] \!= 0 and state\["revision\_count"\] \< 3:  
          return "code\_generator"  
      return "end"

### **Extra High Effort Tier**

The Extra High Effort Tier is optimized for long-horizon, autonomous engineering tasks (exceeding 30 minutes) requiring extensive multi-file alterations and deep system reasoning8.

* **Reasoning Configuration:** Permitted to exhaust up to 32,768 thinking tokens per step16. The system utilizes server-side task budgets with budget-countdown markers, enabling the agent to dynamically scale its thinking depth as the budget consumes11.  
* **Context Loading Changes:** Implements context compaction19. As the multi-turn session approaches the model's context threshold, older conversation history, tool outputs, and intermediate planning steps are summarized, preserving active code blocks and dependency states12.  
* **Delegation Rules:** Uses hierarchical agent teams with sovereign sub-agent sandboxing29. The Orchestrator spawns parallel sub-agents to research external documentation and analyze API behaviors in parallel, passing summarized context back to the parent thread29.  
* **Verification Thresholds:** Three-point validation is enforced: pre-execution intent checking, at-execution scope verification via a strict tool manifest proxy, and post-execution output schema validation37.  
* **Output Requirements:** Generates complete, unified multi-file patches10. Explanations are decoupled from code generation and rendered in separate web layouts or plans10.  
* **Core Failure Modes:** Refusal-like behavior if the initial task budget is set too low for the requested scope, and premature termination of tasks with partial results11.  
* **Runtime Simulation Strategies:** Simulating this tier requires wrapping the API in a loop manager that manually tracks token consumption11. The manager decrements a remaining token counter from a master budget and dynamically appends a customized countdown instruction to the system prompt of each subsequent turn:  
  Python  
  remaining\_tokens \= total\_budget \- client\_cumulative\_usage  
  system\_prompt\_update \= f"System Notice: You are in an agentic loop. Remaining budget: {remaining\_tokens} tokens. Pace your reasoning and wrap up prior to budget exhaustion."

### **Max Effort Tier**

The Max Effort Tier is engineered for critical, highly complex engineering tasks, security audits, and mathematical optimization passes3.

* **Reasoning Configuration:** Complete reasoning compute allocation3. The model is permitted to utilize the absolute maximum thinking token limit of the model (e.g., 64,000+ tokens) with no artificial constraints8.  
* **Context Loading Changes:** Full-repository workspace graph loading. The system maps the entire codebase into a local directed acyclic graph (DAG), tracking every class inheritance, module dependency, and import relationship, supplemented by real-time external documentation search.  
* **Delegation Rules:** Multi-agent consensus networks1. The Orchestrator executes multiple parallel generation branches (trajectories) and resolves conflicting outputs through a centralized learned scoring model or consensus voting1.  
* **Verification Thresholds:** Continuous sandboxed test-to-pass verification5. Every change must pass a full system regression test suite34. Sandbox environments operate with kernel-level isolations to safely execute generated shell scripts and binaries27.  
* **Output Requirements:** Deliver flawless, production-ready implementation patches, accompanied by a complete automated test suite covering edge cases, performance profiling data, and a rollback plan.  
* **Core Failure Modes:** Extreme token expenditures, long latencies (often taking minutes to respond), and a tendency to overthink and over-engineer simple logic3.  
* **Runtime Simulation Strategies:** Simulated by executing ![][image1] independent parallel generation rollouts (![][image2])1. The engine uses a secondary specialized scoring agent to act as a Process Reward Model (PRM), rating the intermediate reasoning steps of each rollout and selecting the highest-scoring trajectory for final execution6.

### **Ultra Effort Tier**

The Ultra Effort Tier is the theoretical maximum of the Manurella engine, designed for autonomous architectural design, legacy system migrations, and multi-day, self-directed code maintenance.

* **Reasoning Configuration:** Hyper-scaled test-time compute1. Combines continuous serial reasoning with real-time heuristic tree search (e.g., Monte Carlo Tree Search over generation branches), running on a persistent background server.  
* **Context Loading Changes:** Continuous context-graph updating. The engine processes multi-gigabyte codebases through streaming vector indexes, maintaining active semantic caches and utilizing dynamic prompt compression to maintain clean context windows.  
* **Delegation Rules:** Sovereign autonomous networks35. The system deploys a network of agents that dynamically assess competence, manage task queues, balance processing loads, and re-delegate work to alternative sub-agents based on real-time trust and reputation metrics35.  
* **Verification Thresholds:** Continuous adversarial debate4. A Generator agent and an Adversarial Critic agent engage in continuous debate cycles, attempting to break the proposed solution via edge-case test generation until a mathematical or functional consensus is reached4.  
* **Output Requirements:** Complete production-ready repositories, automated continuous integration (CI) workflows, comprehensive design docs, and fully audited pull requests delivered directly to the enterprise git server28.  
* **Core Failure Modes:** Extreme computational and financial cost, potential cascading failures in delegation networks, deadlock scenarios where agents await infinite loops of validation, and high susceptibility to regional rate limit timeouts.  
* **Runtime Simulation Strategies:** Simulated by deploying a highly complex multi-tier LangGraph agent network integrated with an external Postgres database to manage persistent state across sessions28. OpenTelemetry tracking is injected via a sidecar collector to continuously monitor intermediate variables, memory usage, and tool execution status29.

## **Technical Integration and Cross-Provider Mapping Specification**

To implement the Manurella effort tiers across diverse platforms, developers must map each tier to provider-specific configuration payloads. The following mapping table provides the precise configurations for Kilo, Codex, ChatGPT (Responses API), Gemini, and a custom Python/MCP runtime environment.

| Manurella Tier | Kilo CLI & Mode | Codex Profiles & Model | ChatGPT (Responses API) Payload | Gemini GenerationConfig | Python/MCP Runtime Config |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Low** | /effort low Mode: Ask \[cite: 22, 26\] | confirm-everything Model: gpt-5.3-codex-spark \[cite: 27, 28\] | {"model": "gpt-5.4-mini", "reasoning": {"effort": "none"}, "store": false} \[cite: 2\] | {"thinking\_config": {"thinking\_budget": 0}} \[cite: 13, 14\] | {"sandbox": "light", "timeout\_sec": 60, "mcp\_servers": \[\], "allowed\_tools": \["read\_file"\]} \[cite: 29\] |
| **Medium** | /effort medium Mode: Code \[cite: 9, 26\] | confirm-on-write Model: gpt-5.3-codex-spark \[cite: 27, 28\] | {"model": "gpt-5.5", "reasoning": {"effort": "low"}, "store": true} \[cite: 2\] | {"thinking\_config": {"thinking\_level": "LOW"}} \[cite: 13, 15\] | {"sandbox": "standard", "timeout\_sec": 180, "mcp\_servers": \["filesystem"\], "allowed\_tools": \["read", "write"\]} \[cite: 29\] |
| **High** | /effort high Mode: Architect \[cite: 9, 26\] | auto-approve Model: gpt-5.3-codex \[cite: 27, 28\] | {"model": "gpt-5.5", "reasoning": {"effort": "medium"}, "store": true} \[cite: 2\] | {"thinking\_config": {"thinking\_level": "MEDIUM"}} \[cite: 15\] | {"sandbox": "standard", "timeout\_sec": 600, "mcp\_servers": \["filesystem", "linter"\], "allowed\_tools": \["all\_local"\]} \[cite: 29\] |
| **Extra High** | /effort xhigh Mode: Orchestrator \[cite: 20, 26\] | auto-approve Model: codex-1 \[cite: 27, 28\] | {"model": "gpt-5.5", "reasoning": {"effort": "high"}, "store": true} \[cite: 2\] | {"thinking\_config": {"thinking\_level": "HIGH"}} \[cite: 15\] | {"sandbox": "microVM", "timeout\_sec": 1800, "mcp\_servers": \["all"\], "context\_compaction": true} \[cite: 19, 29\] |
| **Max** | /effort max Mode: Orchestrator \[cite: 8, 26\] | auto-approve Model: codex-1 \[cite: 27, 28\] | {"model": "gpt-5.5-pro", "reasoning": {"effort": "xhigh"}, "store": true} \[cite: 2\] | {"thinking\_config": {"thinking\_level": "HIGH", "thinking\_budget": 32768}} \[cite: 14, 16\] | {"sandbox": "microVM", "timeout\_sec": 3600, "mcp\_servers": \["all"\], "consensus\_rollouts": 8} \[cite: 1, 29\] |
| **Ultra** | /effort max Mode: /ultra-plan \[cite: 22, 26\] | auto-approve Model: codex-1 \[cite: 27, 28\] | {"model": "gpt-5.5-pro", "reasoning": {"effort": "xhigh"}, "store": true} \[cite: 2\] | {"thinking\_config": {"thinking\_level": "HIGH", "thinking\_budget": 32768}} \[cite: 14, 16\] | {"sandbox": "isolated-kernel", "timeout\_sec": 28800, "mcp\_servers": \["all"\], "consensus\_rollouts": 32} \[cite: 27, 29\] |

### **Python/MCP Runtime Simulation Architecture**

To orchestrate the complex requirements of high-tier runs in a non-native environment, developers can utilize the following complete, production-ready Python orchestration loop. This implementation simulates a high-effort process by wrapping an external model in an iterative execution sandbox with automated lint-checking and state recovery.

Python  
import os  
import subprocess  
import json  
from typing import Dict, Any, List, Tuple, Optional

class ManurellaOrchestrator:  
    def \_\_init\_\_(self, workspace\_path: str, session\_id: str):  
        self.workspace \= workspace\_path  
        self.session\_id \= session\_id  
        self.history: List\[Dict\[str, Any\]\] \= \[\]  
          
    def execute\_command(self, cmd: str) \-\> subprocess.CompletedProcess:  
        """Executes a command within the isolated workspace path."""  
        return subprocess.run(  
            cmd,  
            shell=True,  
            cwd=self.workspace,  
            capture\_output=True,  
            text=True  
        )

    def verify\_syntax(self, file\_path: str) \-\> bool:  
        """Runs lint-checking as part of the verification step."""  
        if file\_path.endswith(".py"):  
            res \= self.execute\_command(f"python \-m py\_compile {file\_path}")  
            return res.returncode \== 0  
        return True

    def run\_agentic\_loop(self, client: Any, user\_prompt: str, effort\_level: str) \-\> str:  
        """  
        Simulates test-time compute by implementing planning, action execution,  
        and post-execution validation loops.  
        """  
        \# Determine retry limits based on the mapped effort level  
        retry\_limits \= {  
            "Low": 0,  
            "Medium": 1,  
            "High": 3,  
            "Extra High": 5,  
            "Max": 10,  
            "Ultra": 20  
        }  
        max\_retries \= retry\_limits.get(effort\_level, 1)  
          
        \# Inject system-level behavioral constraints  
        system\_prompt \= (  
            f"You are the Manurella Agent operating at {effort\_level} effort.\\n"  
            "You must write your planning block inside \<plan\>\</plan\> tags.\\n"  
            "You must output file changes inside \<file path='filepath'\>code\</file\> blocks."  
        )  
          
        self.history.append({"role": "user", "content": user\_prompt})  
        attempt \= 0  
          
        while attempt \<= max\_retries:  
            \# Prepare request payload with standard system instructions  
            response \= client.chat.completions.create(  
                model="gpt-4o",  \# Non-native fallback model  
                messages=\[{"role": "system", "content": system\_prompt}\] \+ self.history,  
                temperature=0.1  
            )  
              
            raw\_content \= response.choices\[0\].message.content  
            self.history.append({"role": "assistant", "content": raw\_content})  
              
            \# Parse proposed file changes  
            file\_path, code\_contents \= self.\_extract\_code\_block(raw\_content)  
              
            if file\_path:  
                \# Execution phase  
                self.\_write\_file(file\_path, code\_contents)  
                  
                \# Verification phase  
                syntax\_valid \= self.verify\_syntax(file\_path)  
                if syntax\_valid:  
                    \# Successful compile terminates loop  
                    return f"Execution successful on attempt {attempt}: {file\_path}"  
                else:  
                    \# Failed validation triggers reflexive correction loop  
                    attempt \+= 1  
                    self.history.append({  
                        "role": "user",  
                        "content": f"Verification failed. The file {file\_path} failed compile checks. Please resolve the syntax errors."  
                    })  
            else:  
                \# No file writes proposed, terminating execution  
                return raw\_content  
                  
        raise RuntimeError(f"Task failed. Execution exceeded maximum retries for {effort\_level} effort.")

    def \_extract\_code\_block(self, content: str) \-\> Tuple\[Optional\[str\], Optional\[str\]\]:  
        """Helper to parse custom XML file structures from model outputs."""  
        try:  
            if "\<file path='" in content:  
                path\_start \= content.find("path='") \+ 6  
                path\_end \= content.find("'", path\_start)  
                file\_path \= content\[path\_start:path\_end\]  
                  
                code\_start \= content.find("\>", path\_end) \+ 1  
                code\_end \= content.find("\</file\>", code\_start)  
                return file\_path, content\[code\_start:code\_end\].strip()  
        except Exception:  
            pass  
        return None, None

    def \_write\_file(self, file\_path: str, content: str):  
        full\_path \= os.path.join(self.workspace, file\_path)  
        os.makedirs(os.path.dirname(full\_path), exist\_ok=True)  
        with open(full\_path, "w") as f:  
            f.write(content)

## **Architectural Conclusions and Implementation Rules**

To maximize efficiency, maintain execution safety, and prevent budget overruns in automated development pipelines, software engineering organizations must adhere to structured operational constraints.

### **Rule 1: Align Effort Level with Task Complexity**

The model class dictates the raw capabilities ceiling, whereas the effort setting dictates how much computational depth is spent to reach that ceiling9. Simple administrative tasks, basic queries, and file search actions must be routed to low or medium effort configurations to preserve compute credits and minimize latencies3. High and max settings should be reserved strictly for complex logical structures, regression debugging, and architectural changes3.

### **Rule 2: Implement Task Budgets in Autonomous Workflows**

To avoid runaway costs during unattended agent runs, pipelines should declare a total token budget via the task\_budget API11. This forces the model to monitor its own token usage against an internal countdown, ensuring it concludes its work and outputs a clean progress summary before running out of tokens11.

### **Rule 3: Decouple Generation from Verification Node Architecture**

Relying on a single model call to write and self-verify complex changes is a primary driver of agent failures and "Lucky Passes"4. Organizations should construct explicit state-machine workflows that separate the code generation node from isolated sandbox verification nodes4. Running automated test suites and compiler checks within isolated sandboxes ensures syntactic and functional correctness before committing changes to a repository4.

#### **Works cited**

1. Claude's extended thinking \- Anthropic, [https://www.anthropic.com/news/visible-extended-thinking](https://www.anthropic.com/news/visible-extended-thinking)  
2. Reasoning models | OpenAI API, [https://developers.openai.com/api/docs/guides/reasoning](https://developers.openai.com/api/docs/guides/reasoning)  
3. Claude Code Effort Levels Explained: When to Use Low, Medium, High, and Max, [https://www.mindstudio.ai/blog/claude-code-effort-levels-explained](https://www.mindstudio.ai/blog/claude-code-effort-levels-explained)  
4. How Multi-Agent Self-Verification Actually Works (And Why It Changes Everything for Production AI) | by Yuval Mehta | Towards AI, [https://pub.towardsai.net/how-multi-agent-self-verification-actually-works-and-why-it-changes-everything-for-production-ai-71923df63d01](https://pub.towardsai.net/how-multi-agent-self-verification-actually-works-and-why-it-changes-everything-for-production-ai-71923df63d01)  
5. \[2605.12925\] AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation, [https://arxiv.org/abs/2605.12925](https://arxiv.org/abs/2605.12925)  
6. SWE-TRACE: Optimizing Long-Horizon SWE Agents through Rubric Process Reward Models and Heuristic Test-Time Scaling \- arXiv, [https://arxiv.org/html/2604.14820v1](https://arxiv.org/html/2604.14820v1)  
7. SWE-bench Verified, [https://www.swebench.com/verified.html](https://www.swebench.com/verified.html)  
8. Effort \- Claude API Docs, [https://platform.claude.com/docs/en/build-with-claude/effort](https://platform.claude.com/docs/en/build-with-claude/effort)  
9. Chooing the right options (Effort, Model, Thinking)? : r/ClaudeAI \- Reddit, [https://www.reddit.com/r/ClaudeAI/comments/1ttayd6/chooing\_the\_right\_options\_effort\_model\_thinking/](https://www.reddit.com/r/ClaudeAI/comments/1ttayd6/chooing_the_right_options_effort_model_thinking/)  
10. My take on coding agents: human-in-the-loop, developer-driven LangGraph workflows, hybrid search, transparent editable context : r/LangChain \- Reddit, [https://www.reddit.com/r/LangChain/comments/1tunown/my\_take\_on\_coding\_agents\_humanintheloop/](https://www.reddit.com/r/LangChain/comments/1tunown/my_take_on_coding_agents_humanintheloop/)  
11. Task budgets \- Claude API Docs, [https://platform.claude.com/docs/en/build-with-claude/task-budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets)  
12. Using GPT-5.5 | OpenAI API, [https://developers.openai.com/api/docs/guides/latest-model](https://developers.openai.com/api/docs/guides/latest-model)  
13. Thinking | Firebase AI Logic \- Google, [https://firebase.google.com/docs/ai-logic/thinking](https://firebase.google.com/docs/ai-logic/thinking)  
14. AG2 \+ Gemini Thinking Config Variants, [https://docs.ag2.ai/latest/docs/use-cases/notebooks/notebooks/agentchat\_gemini\_thinking\_config\_example/](https://docs.ag2.ai/latest/docs/use-cases/notebooks/notebooks/agentchat_gemini_thinking_config_example/)  
15. Thinking | Gemini Enterprise Agent Platform | Google Cloud Documentation, [https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking)  
16. Gemini thinking \- generateContent API | Google AI for Developers, [https://ai.google.dev/gemini-api/docs/thinking](https://ai.google.dev/gemini-api/docs/thinking)  
17. Adaptive thinking \- Claude API Docs, [https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)  
18. Azure OpenAI reasoning models \- GPT-5 series, o3-mini, o1, o1-mini \- Microsoft Foundry, [https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning)  
19. Introducing Claude Sonnet 4.6 \- Anthropic, [https://www.anthropic.com/news/claude-sonnet-4-6](https://www.anthropic.com/news/claude-sonnet-4-6)  
20. Introducing Claude Opus 4.7 \- Anthropic, [https://www.anthropic.com/news/claude-opus-4-7](https://www.anthropic.com/news/claude-opus-4-7)  
21. Building Smarter AI with an Agentic Framework \- Moveworks, [https://www.moveworks.com/us/en/resources/blog/what-is-agentic-framework](https://www.moveworks.com/us/en/resources/blog/what-is-agentic-framework)  
22. 7 Claude Code tips everyone should know (NEW features), [https://www.youtube.com/watch?v=brUQ9lGfc9s](https://www.youtube.com/watch?v=brUQ9lGfc9s)  
23. Kilo Code \- Learn AI \- Miraheze, [https://ai.miraheze.org/wiki/Kilo\_Code](https://ai.miraheze.org/wiki/Kilo_Code)  
24. Kilo Code: AI Coding Agent, Copilot, and Autocomplete \- Visual Studio Marketplace, [https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code)  
25. Understanding Kilo Code AI \- C\# Corner, [https://www.c-sharpcorner.com/blogs/understanding-kilo-code-ai](https://www.c-sharpcorner.com/blogs/understanding-kilo-code-ai)  
26. Using Modes \- Kilo Code Docs | PDF | Keyboard Shortcut | Operating System \- Scribd, [https://www.scribd.com/document/991600172/Using-Modes-Kilo-Code-Docs](https://www.scribd.com/document/991600172/Using-Modes-Kilo-Code-Docs)  
27. Codex (AI agent) \- Wikipedia, [https://en.wikipedia.org/wiki/Codex\_(AI\_agent)](https://en.wikipedia.org/wiki/Codex_\(AI_agent\))  
28. Claude Code vs Codex vs OpenCode: Which AI Coding Agent Is Actually The Best in 2026? | by unicodeveloper \- Medium, [https://medium.com/@unicodeveloper/claude-code-vs-codex-vs-opencode-which-ai-coding-agent-is-actually-the-best-in-2026-baa9f6fd5374](https://medium.com/@unicodeveloper/claude-code-vs-codex-vs-opencode-which-ai-coding-agent-is-actually-the-best-in-2026-baa9f6fd5374)  
29. It's safe to close your laptop now: Hosting coding agents on Amazon Bedrock AgentCore, [https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore/](https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore/)  
30. SWE-agent — Deep Dive & Build-Your-Own Guide \- DEV Community, [https://dev.to/truongpx396/swe-agent-deep-dive-build-your-own-guide-ade](https://dev.to/truongpx396/swe-agent-deep-dive-build-your-own-guide-ade)  
31. Document \--message \+ \--auto-test for headless CI/benchmark usage · Issue \#4923 \- GitHub, [https://github.com/Aider-AI/aider/issues/4923](https://github.com/Aider-AI/aider/issues/4923)  
32. Linting and testing \- Aider, [https://aider.chat/docs/usage/lint-test.html](https://aider.chat/docs/usage/lint-test.html)  
33. LangGraph Tutorial: Self-Correcting AI Agents and Agent Loops | ActiveWizards, [https://activewizards.com/blog/a-deep-dive-into-langgraph-for-self-correcting-ai-agents/](https://activewizards.com/blog/a-deep-dive-into-langgraph-for-self-correcting-ai-agents/)  
34. Building Production-Ready AI Agents with LangGraph: A Developer's Guide to Deterministic Workflows | Ranjan Kumar, [https://ranjankumar.in/building-production-ready-ai-agents-with-langgraph-a-developers-guide-to-deterministic-workflows](https://ranjankumar.in/building-production-ready-ai-agents-with-langgraph-a-developers-guide-to-deterministic-workflows)  
35. Intelligent AI Delegation \- arXiv, [https://arxiv.org/html/2602.11865v1](https://arxiv.org/html/2602.11865v1)  
36. Intelligent AI Delegation: Overview | by DhanushKumar, [https://ai.plainenglish.io/intelligent-ai-delegation-overview-bc89a1acce5c](https://ai.plainenglish.io/intelligent-ai-delegation-overview-bc89a1acce5c)  
37. Intent-Verified Delegation Chains for Securing Federal Multi-Agent AI Systems \- arXiv, [https://arxiv.org/html/2604.02767v1](https://arxiv.org/html/2604.02767v1)  
38. Understanding Delegation for AI Agents \- LM-Kit Docs, [https://docs.lm-kit.com/lm-kit-net/guides/glossary/ai-agent-delegation.html](https://docs.lm-kit.com/lm-kit-net/guides/glossary/ai-agent-delegation.html)  
39. 10 Best Kilo Code Alternatives in 2026 \- Vellum, [https://www.vellum.ai/blog/best-kilo-code-alternatives](https://www.vellum.ai/blog/best-kilo-code-alternatives)  
40. How to Use Aider: Atomic Git Commits & Architect Mode (2026 Guide) \- DeployHQ, [https://www.deployhq.com/guides/aider](https://www.deployhq.com/guides/aider)  
41. Effort, Thinking, and How Claude Opus 4.7 Changed the Rules | iBuildWith.ai, [https://www.ibuildwith.ai/blog/effort-thinking-opus-4-7-changed-the-rules/](https://www.ibuildwith.ai/blog/effort-thinking-opus-4-7-changed-the-rules/)  
42. Introduction to Kilo Code, [https://kilo.ai/docs/getting-started](https://kilo.ai/docs/getting-started)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAABB0lEQVR4XmNgGAWUghAgXgrEs9CwJ5KaeizyWIEuA8LA/0CcAcQBQCyCpCYNiL9B8QwGiHq8YBIDxDBGdAkgmAfE84GYD10CG9AE4rdA/BVN3AmIT6KJEQRBDBBXXYXyWYG4DIhXAbEETBGxAOZFkFeEgHgtEO8CYi5kRcQAXiA+zAAxLBqIr0PZ74FYB0kdUQDmRZjLQCAHyn8CxIpQMaIAzIuLgJgZKgYyAGQQSDwCKkYQCALxaQaEF2EAlDymQMUPIInjBbAk8QmI9dHkLIH4JxD/QxPHCUCxBrJ9HQNmzIGSRy8DRN6RAREEGABmKyzgYXgrVB7mYmS5R0AsB5UfBaNg6AIAvxpA9tWZAPEAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAaCAYAAAANIPQdAAACXElEQVR4Xu2WO2gUURSGfzGCmsQHCuIjig+UqMSIhWApYuMDEQvBTgsbsYigaCwCYmEIQQwIhohY2ghW6UQJRElsBEUQLRRRVGwEGwvN/3NmyN3j7nhndwlb3A8+lrlnZvaeueeeGSCRSLQye+kDOuq8FpzTTW+7eG8Qn0vW0310BZ3nYjVZTY/RS/QvvUVPwG6UsxaW2Dd6gx6i7UHco2uP+MEGUUKH6SN6l76jbyrOiOA4/UI3+QBsJafpIh+owRLYw7gKe+LN4Ch9GRzPp5fp7mCskA76hF534yP0HmzS9bIAVimv6TPY5MqiavsAe3AhmveYG6uJVuoHPRCMbaWnUd+kqqH7qIyVrJJW8rEsh1WStlNYTVtgFRjFKdgNtPdU+yfpr4ozmsc2+pB+pmdcrIgLsDlqL+6nXfQpSjwsNRvdYBmsRP9kx23hSU1GJThM+1HcxHKUzBBsXlJzPF9xRgF7YKumC1W2YiP9RAey42aSJ/cV1phiUUfXllpML9LfsDlrhf/LWdjJYTtWyd7MxlYF442ge27HbJnGrF7ODvod1k1zdK8p2GJoUWqiP1b3VJL6DdmZjZ9z42XJG44664vsuCwDqP56UxNS2YYN8x9WwrqdktGKhmg/avw5XepisaiBqRrGaQ9KfKE47tMJ2ukDiEhyEJbIK7rOxYS+cBTXH6xxsSL0xXTFDzbABvqWPnbjeoVof1Z9eLvoT8x2qty88Qi9ZH18YRCfazQ3VcUd2gf7vFMO9ZR/S6OEtAX0Xj+I+rdRIha9097TjxFO0s12WSKRSCRamxkAy3jRA2HvXAAAAABJRU5ErkJggg==>