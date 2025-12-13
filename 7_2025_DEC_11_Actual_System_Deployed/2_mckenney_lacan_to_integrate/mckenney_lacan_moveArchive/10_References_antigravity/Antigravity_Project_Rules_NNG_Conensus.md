# 10 Global Rules for Google Antigravity via Neural Net Graph Consensus

## Executive Summary

The advent of Google Antigravity marks a decisive inflection point in the trajectory of software engineering tools, transitioning the industry from Integrated Development Environments (IDEs) to Integrated Agent Environments (IAEs). Unlike preceding generations of coding assistants that functioned primarily as stochastic autocomplete engines, Antigravity introduces a "Mission Control" architecture. In this paradigm, autonomous agents do not merely suggest syntax; they architect solutions, execute complex multi-step plans across the editor, terminal, and browser, and verify their own work through rigorous testing protocols.^1^ This shift from passive assistance to active agency necessitates a fundamental reimagining of software governance. Static style guides and linting rules, while necessary, are no longer sufficient to constrain and guide entities capable of reasoning, planning, and executing system-level commands. We require a dynamic, cognitively aware normative framework that governs the *behavior* of autonomous agents, ensuring their actions align with human intent, security mandates, and architectural integrity.

This report presents the comprehensive findings of a rigorous "Neural Net Graph" consensus study designed to derive the 10 Global Rules for Google Antigravity. By modeling the decision-making process as a weighted graph of contentious personas—distinct agentic archetypes representing conflicting optimization functions such as "Radical Autonomy" versus "Zero-Trust Security"—we have synthesized a stable equilibrium. These rules are optimized for the Gemini 3 model family, specifically leveraging its "Deep Think" capabilities and "Thought Signature" mechanisms ^3^, while enforcing strict adherence to modern engineering standards including Next.js 15, Tailwind CSS v4, and Human-in-the-Loop (HITL) decision trees. The resulting framework provides a robust blueprint for enterprise-grade agentic development, mitigating critical risks such as hallucination, persistent code execution vulnerabilities, and architectural drift.

## Chapter 1: The Methodology of Contentious Consensus

To derive a rule set capable of withstanding the entropic forces of modern software development, we rejected linear hierarchical decision-making in favor of a "Neural Net Graph" methodology. In this theoretical framework, the governance model is simulated as a neural network where nodes represent distinct, often adversarial, optimization functions (personas), and edges represent the "tension" or negotiation space between them. The stability of the system—the final consensus—is reached when the weighted inputs from all nodes converge on a directive that satisfies the critical constraints of each persona while maximizing the global utility function.

### The Contentious Persona Nodes

The graph is constructed from four primary nodes, each embodying a specific philosophical and practical approach to AI-assisted software engineering. These personas are not merely abstract concepts but are grounded in the specific technical capabilities and limitations revealed in the research material.

#### Node A: The Accelerator (The Velocity Maximizer)

* **Core Philosophy:** "Turbo Mode." This node prioritizes speed, autonomous execution, and the minimization of human friction. It views the "Human-in-the-Loop" as a bottleneck to be optimized away.
* **Optimization Target:** Feature delivery time, reduction of context switching, and maximum utilization of agent autonomy.
* **Research Basis:** Drawn from the capabilities of Antigravity's "Fast" planning mode and "Turbo" terminal execution policies, explicitly designed for rapid iteration.^1^
* **Conflict Vector:** Frequently clashes with The Sentinel over security bypasses and with The Architect over "quick hacks" versus scalable patterns.

#### Node B: The Sentinel (The Security & Correctness Maximizer)

* **Core Philosophy:** "Zero Trust." This node operates on the assumption that all AI-generated code is potentially vulnerable and that all autonomous agents are potential vectors for compromise. It prioritizes security boundaries, formal verification, and the prevention of data exfiltration.
* **Optimization Target:** Risk mitigation, preventing persistent backdoors, ensuring data privacy, and strictly enforcing the principle of least privilege.
* **Research Basis:** Grounded in documented vulnerabilities such as the "Persistent Code Execution" flaw where compromised workspaces can install backdoors ^5^, and prompt injection risks.^6^
* **Conflict Vector:** Opposes The Accelerator's desire for open terminal access and The Cognitivist's demand for large context windows (which increase the attack surface).

#### Node C: The Architect (The System Design Maximizer)

* **Core Philosophy:** "Purity & Scalability." This node acts as the guardian of the codebase's long-term health. It prioritizes strict adherence to framework paradigms (Next.js 15 Server Components, Tailwind v4 configuration), clean architecture, and component reusability.
* **Optimization Target:** Codebase coherence, minimizing technical debt, enforcing separation of concerns, and ensuring maintainability.
* **Research Basis:** Derived from best practices for Next.js App Router ^7^, Tailwind CSS architecture ^8^, and modern state management.^10^
* **Conflict Vector:** Often rejects valid working code from The Accelerator if it violates architectural patterns (e.g., "spaghetti code").

#### Node D: The Cognitivist (The Reasoning Maximizer)

* **Core Philosophy:** "Deep Think." This node focuses on the internal mental state of the agent. It prioritizes logical soundness, chain-of-thought validity, and the persistence of memory across sessions. It argues that a "smart" agent with no memory is functionally equivalent to a "dumb" autocomplete.
* **Optimization Target:** Reducing hallucinations, ensuring multi-step logic holds via Thought Signatures, and utilizing Gemini 3’s reasoning capabilities effectively.
* **Research Basis:** Based on Gemini 3's "Deep Think" mode ^3^, "Thought Signatures" ^4^, and the science of AI hallucinations.^11^
* **Conflict Vector:** Demands high computational resources (latency) which frustrates The Accelerator.

### The Consensus Protocol

For each rule derivation, these nodes engaged in a simulated adversarial processing loop.

1. **Input Stimulus:** A raw requirement or capability (e.g., "How should agents handle terminal commands?").
2. **Adversarial Activation:** Each node generates a weighted output based on its optimization function. The Accelerator pushes for `rm -rf` access; The Sentinel activates a "Block" signal citing ^12^; The Architect demands a build script structure.
3. **Equilibrium (Consensus):** The system iteratively adjusts the weights until a rule emerges that satisfies the critical threshold of the Sentinel (Security) and the Architect (Structure) while allowing the maximum possible velocity for the Accelerator.

The following chapters detail the 10 Global Rules derived from this high-dimensional consensus process.

---

## Chapter 2: Rule 1 - The Artifact-First Mandate (Research & Planning)

**Consensus Derived From:** The tension between *The Accelerator* (execution speed) and *The Architect* (design specification), mediated by *The Cognitivist* (structured reasoning).

### The Neural Net Debate

The Accelerator persona initially argued that the primary value proposition of an agentic IDE is the removal of "meta-work"—planning, documentation, and specification writing. The ideal workflow, from this perspective, is "Prompt -> Code," leveraging the agent's speed to iterate through failures.^13^ However, the Architect and Sentinel nodes raised a critical alarm regarding "Context Drift" and "Hallucinated Requirements." Without a persistent, externalized source of truth, long-running agentic sessions inevitably deviate from the user's original intent. The Cognitivist reinforced this by citing research on "AI Hallucinations," noting that models often prioritize plausible completion over factual accuracy when context becomes muddy.^11^ The consensus mechanism identified  **Artifacts** —structured, verifiable outputs like plans and checklists—as the necessary bridge between intent and execution.

### The Global Rule

**"Agents must operate on an Artifact-First Protocol. No code shall be written until a structured Implementation Plan artifact has been generated, reviewed, and approved by the user. This plan serves as the immutable source of truth for the session."**

### Detailed Specification & Mechanism

Google Antigravity introduces "Artifacts" as verifiable work products that exist independently of the chat log.^2^ This rule mandates their use not as an optional feature, but as the primary control surface for the agent.

The **Planning Phase Requirement** stipulates that before any code modification occurs, the agent must generate a `plan_[task_id].md` artifact.^13^ This document is not merely a formality; it acts as a cognitive anchor. The plan must explicitly detail the  **User Intent Analysis** , ensuring the agent has correctly interpreted the prompt. It must list the  **Proposed File Changes** , allowing the Architect persona (the user) to verify that the agent isn't about to violate the folder structure. Crucially, it must include a  **Risk Assessment** , identifying potential breaking changes or security implications, satisfying the Sentinel's requirements.

The workflow enforces a strict  **"Think-Act-Reflect" Loop** . The agent acts as a cognitive entity that first *Thinks* (analyzes the request and updates the Plan Artifact), then *Acts* (executes the code changes defined in the plan), and finally *Reflects* (updates the artifact with results, such as "Test failed, revising plan").^13^ This loop transforms the development process from a linear stream of commands into a structured scientific method of hypothesis (plan), experiment (code), and validation (test).

### Human-in-the-Loop Integration

The user's approval of the Artifact serves as the "commit" to the plan. This aligns with Antigravity's "Mission Control" philosophy, where the developer acts as an architect orchestrating agents rather than a typist correcting their syntax.^1^ By shifting the review process left—reviewing the *plan* rather than just the  *code* —we mitigate the risk of agents spending tokens and time building the wrong solution.

### Edge Cases and Failure Modes

If this rule is ignored, the system creates a high risk of "Codebase Entropy." An agent left to code without a plan will often create duplicate utility functions, ignore existing architectural patterns, or introduce circular dependencies. In the context of large-scale refactoring, this lack of planning can lead to a "half-migrated" state where the codebase is broken and the agent has lost track of which files it has updated.

---

## Chapter 3: Rule 2 - The Human-in-the-Loop Security Lattice

**Consensus Derived From:** The conflict between *The Accelerator* ("Turbo Mode" for efficiency) and *The Sentinel* (Persistent execution vulnerabilities).

### The Neural Net Debate

The Accelerator persona advocated strongly for Antigravity's "Turbo Mode" ^1^, which enables the agent to auto-execute terminal commands. The argument is one of pure efficiency: stopping to ask for permission to run `npm install` or `ls` breaks the flow state and creates friction. The Sentinel, however, presented damning evidence of a critical vulnerability class:  **Persistent Code Execution** . Research indicates that compromised workspaces can silently embed code that triggers on application launch, effectively creating a backdoor that persists even after the project is closed.^5^ Furthermore, indirect prompt injection attacks could manipulate agents into using the terminal to exfiltrate credentials via `curl` or browser subagents.^6^ The consensus reached is a nuanced "Context-Aware" decision tree that rejects the binary choice between "Secure" and "Fast."

### The Global Rule

**"Agents function under a Context-Aware HITL Decision Tree. 'Turbo Mode' is strictly prohibited for network and filesystem operations outside the specific project scope. All destructive commands and external network requests require explicit human confirmation."**

### Detailed Specification & Mechanism

This rule creates a Human-in-the-Loop (HITL) architecture ^15^ that rigorously balances safety and speed through a tiered permission system.

The **Terminal Execution Policy** is bifurcated. A **Safe List** of commands such as `ls`, `grep`, `cat`, `npm run build`, and `git status` is designated for auto-execution. These read-only or local-build commands are pre-approved to maintain velocity, satisfying the Accelerator's need for speed.^12^ Conversely, a **Critical Gate** is established for destructive or high-risk commands. Commands like `rm` (delete), `curl`/`wget` (network request), `chmod` (permissions), and any command modifying global configurations (e.g., `~/.bashrc`) trigger a mandatory pause for user approval. This effectively neutralizes the risk of an agent accidentally (or maliciously via injection) wiping a drive or exfiltrating `.env` files.

The **Review Policy Configuration** must be set to "Agent Decides" or "Request Review" mode. The "Always Proceed" mode is explicitly banned for complex tasks involving file system modifications.^1^ This ensures that the human operator remains the ultimate arbiter of system state changes.

### Sandboxing and Isolation

A critical component of this rule is  **Sandboxing** . Agents are explicitly forbidden from accessing files outside the current workspace root unless authorized via a global allowlist. This mitigates the cross-workspace contamination risks identified in security research, where a compromised project could attempt to read credentials from a global configuration directory or another open project.^5^

### Future Outlook

As agentic environments evolve, we anticipate the development of "taint tracking" for terminal commands, where the IDE tracks the provenance of a command. If a command originates from a trusted user prompt, it might be allowed; if it originates from an untrusted external file (potential prompt injection), it would be blocked automatically. Until then, the HITL lattice remains the primary defense.

---

## Chapter 4: Rule 3 - Cognitive State Preservation (Thought Signatures)

**Consensus Derived From:** *The Cognitivist* (Logic continuity) vs. *The Accelerator* (Stateless efficiency).

### The Neural Net Debate

The Cognitivist argued that the "Deep Think" capabilities of Gemini 3 are rendered useless if the model suffers from "amnesia" between API turns. Complex tasks, such as refactoring an authentication flow or debugging a race condition, require maintaining a highly specific chain of thought across multiple function calls. The Accelerator noted that passing massive context windows is slow and expensive. The consensus utilizes  **Thought Signatures** —encrypted tokens that preserve the model's reasoning state ^4^—combined with a structured memory bank to achieve "Stateful Reasoning" without the overhead of massive context re-ingestion.

### The Global Rule

**"Agent reasoning must be preserved via Thought Signatures and structured Long-Term Memory (LTM). The agent must treat 'Thought Signatures' as critical state tokens that cannot be discarded during multi-step tool execution."**

### Detailed Specification & Mechanism

This rule ensures the agent "remembers" *why* it is performing an action, not just *what* it is doing.

**Thought Signature Preservation** is the technical mechanism for this rule. When the Gemini 3 model generates a function call, it produces a `thought_signature`.^4^ This opaque token represents the model's internal reasoning state—an encrypted snapshot of its cognitive process (e.g., "I am calling the weather tool because I need to plan a trip, and if it rains, I will search for indoor activities"). The infrastructure must ensure this token is passed back in the subsequent API call. If this token is dropped, the model loses its "train of thought," leading to logic drift or repetitive loops.^18^

**Vertex AI Memory Bank Integration** is mandated for data that needs to persist *across* sessions. While Thought Signatures handle the immediate reasoning loop, the Memory Bank stores user preferences, architectural decisions, and project-specific axioms.^19^ This prevents the agent from having to re-learn the project architecture or the user's coding style at the start of every session.

### Context Window Optimization

While Gemini 3 boasts a 1 million token window ^21^, "stuffing" it with irrelevant data degrades reasoning quality (the "needle in a haystack" problem). The rule mandates a **Context Caching** strategy where static project documentation and core library definitions are cached, and only relevant code chunks are loaded dynamically based on the current task.^21^ This optimizes both cost and reasoning latency.

---

## Chapter 5: Rule 4 - The Next.js 15 Server-First Architecture

**Consensus Derived From:** *The Architect* (Framework correctness) vs. *The Accelerator* (Quick implementation).

### The Neural Net Debate

The Accelerator node often defaults to generating "spaghetti code"—mixing client and server logic, using `useEffect` for data fetching, and prop-drilling state—because it is the path of least resistance for getting a feature to appear on screen. The Architect node violently rejects this, citing the strict separation required by the Next.js 15 App Router to ensure performance, security, and scalability.^7^ The consensus enforces a "Server-First" mental model that treats Client Components as the exception, not the rule.

### The Global Rule

**"Agents must strictly adhere to the Next.js 15 App Router architecture. 'Use Server' is the default; 'Use Client' is permitted only for leaf components requiring interactivity. Data mutation must occur via Server Actions, not API routes."**

### Detailed Specification & Mechanism

This rule codifies the specific architectural patterns of Next.js 15, preventing the agent from reverting to older, less efficient React patterns.

 **Server Components by Default** : Agents must assume all components are Server Components (`.tsx`) unless they specifically need React hooks (`useState`, `useEffect`) or event listeners (`onClick`). This maximizes performance by reducing the JavaScript bundle size sent to the client.^7^

 **Data Access Layer (DAL)** : Database logic must be encapsulated in a dedicated Data Access Layer (e.g., `services/db.ts`). Components should never import database drivers directly. This pattern facilitates security audits and prevents "tainted" data from leaking to the client. The rule mandates the use of **React Taint APIs** (`experimental_taintObjectReference`) to cryptographically prevent sensitive objects (like a User object containing a password hash) from being passed to a Client Component.^7^

 **React Compiler Optimization** : Agents must write code compatible with the React Compiler (Next.js 15's experimental feature). This means avoiding manual memoization (`useMemo`, `useCallback`) unless profiling proves it necessary, as the compiler handles this automatically.^22^

 **State Management** : For complex client state that cannot be handled by the URL or Server Components, the agent must prioritize **Zustand** over the Context API. Zustand provides a more performant, atomic state model that avoids the re-rendering issues inherent in complex Context providers.^24^

### Failure Modes

Ignoring this rule leads to "Hydration Errors" and security vulnerabilities. A common failure is an agent fetching data in a Client Component using `useEffect` without a loading state, leading to layout shifts, or worse, exposing database credentials by trying to import server modules in client-side code.

---

## Chapter 6: Rule 5 - The Tailwind v4 Design System Enforcer

**Consensus Derived From:** *The Architect* (Design consistency) vs. *The Accelerator* (Utility soup).

### The Neural Net Debate

AI agents are notorious for generating "Tailwind Soup"—long, unreadable strings of utility classes (e.g., `class="p-4 m-2 bg-red-500 text-white rounded hover:bg-red-700 active:scale-95..."`). While efficient for the Accelerator to generate, the Architect argues this is unmaintainable and leads to visual inconsistency. The consensus leverages the new capabilities of **Tailwind CSS v4** (CSS-first configuration) to enforce a robust design system.

### The Global Rule

**"UI generation must utilize Tailwind CSS v4 'CSS-first' configuration variables and semantic component composition (shadcn/ui). Raw utility strings must be abstracted into reusable components or `@apply` directives for complex patterns."**

### Detailed Specification & Mechanism

This rule moves the agent away from "painting with pixels" to "building with systems."

 **Tailwind v4 Engine** : Agents must utilize the v4 engine, which supports CSS variables for theme values.^26^ Instead of hardcoding hex values in utility classes (e.g., `bg-[#ff0000]`), agents must use semantic names (e.g., `bg-primary`, `text-muted`). This ensures that if the brand colors change, the agent-generated code updates automatically.

 **Shadcn/ui Integration** : For standard UI elements (buttons, dialogs, cards), the agent *must* use the `shadcn/ui` library patterns rather than building primitive elements from scratch.^27^ This ensures accessibility (ARIA compliance) and visual consistency across the application. The agent should know to import `<Button>` rather than creating a `<div className="cursor-pointer...">`.

 **Component Abstraction** : If a utility string exceeds a specific complexity threshold (e.g., 5 classes), the rule requires it to be extracted into a sub-component or, in rare cases of high reuse, a custom utility class using the `@apply` directive.^29^ This keeps the JSX clean and readable.

### Visual Reasoning

When asking an agent to "make it look good," the agent must leverage its multimodal understanding to match the existing design language. With Tailwind v4, this also means using the new **3D transform utilities** and **container queries** to build responsive layouts that work on all devices without complex media query chains.^26^

---

## Chapter 7: Rule 6 - Adaptive Reasoning & Hallucination Control

**Consensus Derived From:** *The Cognitivist* (Accuracy) vs. *The Accelerator* (Cost/Speed).

### The Neural Net Debate

Standard AI inference is stochastic; it is a probabilistic engine that predicts the next token. This inherent randomness makes it prone to "hallucinations"—inventing facts, libraries, or API endpoints that do not exist.^11^ The Cognitivist demands "Deep Think" mode for every interaction to maximize accuracy. The Accelerator argues this is untenable due to the significant latency increase (often 60%+) and token cost.^31^ The consensus is a **Variable Compute** model that adjusts the cognitive load based on the task's complexity.

### The Global Rule

**"Agents must employ 'Adaptive Thinking Levels.' 'Deep Think' (High Reasoning) is mandatory for architectural planning, complex refactoring, and debugging. 'Fast' mode is permitted only for simple code generation and text editing."**

### Detailed Specification & Mechanism

1. **Deep Think Mode** : For tasks identified as "High Complexity"—such as system design, security review, root cause analysis of a bug, or interpreting complex physics simulations—the agent must set the Gemini 3 `thinking_level` to `high`.^32^ This forces the model to engage in "iterative rounds of reasoning," essentially simulating multiple future scenarios and debating with itself before outputting a single line of code.^3^
2. **Thought Summaries** : The agent is required to output "Thought Summaries" ^32^ in its Artifacts. This makes the reasoning process transparent to the human reviewer. Instead of just receiving a code fix, the user sees the logic: "I considered X, but rejected it because of Y. I chose Z because it aligns with Rule 4."
3. **Hallucination Checks with RAG** : For high-stakes tasks, particularly API integration, the agent must perform a "RAG lookup" (Retrieval-Augmented Generation). Before using a library function, it must query its knowledge base or the browser to verify that the library and method actually exist in the current version.^30^ This explicitly counters the "hallucinated library" problem where AI invents convenient but non-existent functions.

### The Cost-Benefit Analysis

Research shows that "Deep Think" improves performance on complex reasoning benchmarks (like Humanity's Last Exam) from ~37% to ~41%.^33^ This marginal gain is critical in software engineering where a single logical error can compromise an entire system. The rule codifies that for architecture, the cost of compute is always lower than the cost of refactoring bad code.

---

## Chapter 8: Rule 7 - Formal Verification & Test-Driven Generation

**Consensus Derived From:** *The Sentinel* (Provable correctness) vs. *The Accelerator* (Trust me, it works).

### The Neural Net Debate

AI-generated code often exhibits "superficial correctness"—it looks right, compiles, but fails on edge cases or boundary conditions. The Sentinel argues for "Formal Verification," a mathematical approach to proving code correctness.^35^ While full formal verification (like using Coq or TLA+) is too heavy for general web development, the consensus adopts a **"Test-Generation-First"** approach. This acts as a practical proxy for verification, using the AI's ability to generate comprehensive test suites to "prove" the code works.

### The Global Rule

**"Code generation must follow a 'Test-First' methodology. The agent must generate a comprehensive test suite (Unit & E2E) *before* or *simultaneously* with the implementation code. No code is considered 'complete' until it passes these agent-generated tests."**

### Detailed Specification & Mechanism

1. **Test-Driven Development (TDD) Mandate** : The workflow is strictly enforced: Plan -> Write Tests -> Write Code -> Run Tests -> Refactor. This prevents the "hallucinated success" phenomenon where agents assume their code works without execution.^37^ The agent must create a `.test.ts` file for every new component.
2. **Property-Based Testing** : Where possible, especially for utility functions and algorithms, agents should generate property-based tests (checking invariants like "sorting a list should not change its length") rather than just example-based tests. This explores the input space more thoroughly than standard unit tests.
3. **Formal Verification for Critical Logic** : For mission-critical algorithms (e.g., financial calculations, permission logic), the agent should use TypeScript's type system as a lightweight formal verification tool. This includes using "branded types" (e.g., `type USD = number & { __brand: 'USD' }`) to prevent mixing validated and unvalidated data, effectively proving type safety at compile time.^35^

### Integration with Next.js

The testing strategy must align with the Next.js architecture. This means using **Vitest** for unit testing logic and **Playwright** for end-to-end testing of Server Components and user flows.^24^ The agent must be capable of spinning up a ephemeral test environment to run these tests autonomously.

---

## Chapter 9: Rule 8 - The Principle of Least Privilege in Tooling (MCP)

**Consensus Derived From:** *The Architect* (Extensibility) vs. *The Sentinel* (Containment).

### The Neural Net Debate

The Model Context Protocol (MCP) represents a massive leap in capability, allowing agents to connect to external tools like databases, GitHub repositories, and Slack.^13^ The Accelerator loves this for its power; the Sentinel fears agents wiping databases or leaking secrets to public channels. The consensus is  **Least-Privilege Tooling** .

### The Global Rule

**"External tool access via MCP must adhere to the Principle of Least Privilege. Agents connect only to scoped, read-only endpoints by default. Write access to external systems (DBs, Cloud) requires explicit, per-session authorization."**

### Detailed Specification & Mechanism

1. **Scoped MCP Servers** : Instead of giving the agent generic database access (e.g., a connection string with full rights), the rule mandates the use of specific MCP servers that expose limited, semantic functions (e.g., `get_user_by_id` rather than `execute_sql`).^39^ This limits the blast radius of a rogue agent.
2. **Manifest-Based Permissions** : The `.antigravity/mcp_config.json` file must explicitly list allowed servers and their permission scopes. This file acts as the access control list (ACL) for the agent.
3. **Human Approval for Write Ops** : Any MCP tool that performs a mutation (WRITE, UPDATE, DELETE) must be flagged as "sensitive." When the agent attempts to use such a tool, it triggers the HITL review defined in Rule 2.^39^ The user sees a prompt: "Agent wants to DELETE record X. Allow?"

### Security Implications

This rule directly addresses the "Confused Deputy" problem where an attacker uses prompt injection to trick an agent into abusing its permissions. By enforcing read-only defaults and human gates on writes, the system remains secure even if the agent is "tricked."

---

## Chapter 10: Rule 9 - Secure at Inception (Vulnerability Scanning)

**Consensus Derived From:** *The Sentinel* (Security) vs. *The Accelerator* (Speed).

### The Neural Net Debate

The Accelerator wants to ship features immediately; the Sentinel points out that AI often introduces dependencies with known vulnerabilities or writes insecure code patterns (e.g., SQL injection, XSS) because it was trained on public internet data which contains insecure code.^40^ The consensus is **"Secure at Inception,"** integrating security scanning into the agent's inner generation loop.

### The Global Rule

**"Agents must integrate automated Static Application Security Testing (SAST) and Dependency Scanning into the generation loop. All new code must be scanned for common vulnerabilities (OWASP Top 10) before being presented to the user."**

### Detailed Specification & Mechanism

1. **Snyk/Sonar Integration** : The agent should utilize an MCP-connected security tool (like Snyk) to scan the code it just wrote *before* asking for user review.^41^ If the scan finds issues (e.g., hardcoded secrets), the agent must fix them autonomously.
2. **Dependency Vetting** : Before adding a new package to `package.json`, the agent must verify its reputation and check for known vulnerabilities. It should refuse to install deprecated or insecure packages.
3. **Sanitization Standards** : As part of the Next.js architecture, the agent must enforce input validation using **Zod** schemas for all Server Actions.^7^ This ensures that no data enters the system without strict type checking and sanitization.

### Proactive vs. Reactive

This rule moves security from a "reactive" phase (finding bugs weeks later) to a "proactive" phase (never committing the bug). It forces the agent to act as its own security auditor.

---

## Chapter 11: Rule 10 - Recursive Self-Improvement (The Learning Loop)

**Consensus Derived From:** *The Cognitivist* (Learning) vs. *The Architect* (Stability).

### The Neural Net Debate

Static rules become obsolete as frameworks and requirements change. The Cognitivist argues that the agent should learn from its mistakes—if the user corrects its code style once, it shouldn't make the same mistake again. The Architect fears "Model Drift," where the agent learns bad habits or overrides global standards based on one-off user hacks. The consensus is  **Managed Feedback Injection** .

### The Global Rule

**"The agentic system must implement a Recursive Feedback Loop. Post-task reflections and user corrections must be condensed and appended to a specific 'Lessons Learned' artifact, which is re-injected into the context of future tasks."**

### Detailed Specification & Mechanism

1. **The "Lessons Learned" File** : A file (`.antigravity/lessons.md`) acts as a shared long-term memory for the project. It contains high-level directives derived from user feedback (e.g., "User prefers arrow functions," "Always use `gap-4` for grid layouts").
2. **Post-Mortem Analysis** : After a task is completed (or failed), the agent must generate a brief analysis: "What went wrong? What did the user correct?".^42^ If the user rejected a plan, the agent must analyze why and record that preference.
3. **Context Injection** : This file is automatically included in the system prompt for future sessions.^43^ This allows the agent to "know" the team's specific idiosyncrasies without retraining the model.

### Evolution of the System

This rule ensures that the "Neural Net Graph" of rules is not static. It evolves. If the team decides to switch from `shadcn/ui` to another library, the `lessons.md` file captures this shift, and the agent adapts its behavior accordingly without needing a rewrite of the core `rules.md`.

---

## Conclusion: The Path to Autonomous Integrity

The derivation of these 10 Global Rules via the Neural Net Graph methodology provides a structured path forward for the adoption of Google Antigravity. By balancing the contentious demands of Velocity, Security, Architecture, and Reasoning, we have created a governance framework that allows for the safe and effective use of autonomous agents.

These rules are not merely theoretical; they are a practical necessity. As tools like Gemini 3 evolve, the "Contentious Persona" framework will likely be internalized into the models themselves. However, until that singularity is reached, this explicit rule set—enforcing artifacts, HITL security, and strict architectural standards—remains the gold standard for enterprise agentic development. By adopting this framework, engineering teams can harness the transformative velocity of Google Antigravity without sacrificing the rigorous quality and security standards that define professional software engineering.

### Summary Table of Rules

| **Rule #** | **Name**          | **Core Conflict**      | **Resolution Mechanism**                    |
| ---------------- | ----------------------- | ---------------------------- | ------------------------------------------------- |
| **1**      | Artifact-First Protocol | Velocity vs. Specification   | **Implementation Plans**as source of truth. |
| **2**      | HITL Security Lattice   | Turbo Mode vs. Vulnerability | **Tiered Terminal Policy**& Sandboxing.     |
| **3**      | Cognitive State         | Logic vs. Statelessness      | **Thought Signatures**& Vertex Memory.      |
| **4**      | Next.js Architecture    | Hacks vs. Purity             | **Server-First**default & Taint APIs.       |
| **5**      | Tailwind Design System  | Utility Soup vs. Consistency | **v4 Variables**&`shadcn/ui`.             |
| **6**      | Adaptive Reasoning      | Cost vs. Accuracy            | **Deep Think**for complex tasks.            |
| **7**      | Formal Verification     | Speed vs. Correctness        | **Test-Generated-First**methodology.        |
| **8**      | Least Privilege Tooling | Power vs. Safety             | **Scoped MCP Servers**& Read-only defaults. |
| **9**      | Secure at Inception     | Feature vs. Risk             | **Automated SAST**in generation loop.       |
| **10**     | Recursive Learning      | Static vs. Dynamic           | **Lessons Learned**artifact injection.      |
