#  **Maximizing Google Antigravity, Gemini CLI 3, and Autonomous Workflows in Enterprise Software Engineering**

## **Executive Summary**

The discipline of software engineering is currently navigating a pivotal transition from "human-centric, tool-assisted" development to "agent-centric, human-orchestrated" architectures. This shift is not merely an incremental improvement in developer productivity tools but a fundamental reimagining of the development lifecycle itself. Spearheading this transformation is Google's integrated ecosystem comprising **Google Antigravity**, **Gemini CLI 3**, **Google AI Studio**, and **Google Code Wiki**. These platforms collectively introduce an "agent-first" paradigm where autonomous AI entities—powered by the massive 1-million-token context windows of Gemini 3 Pro—assume responsibility for planning, execution, verification, and documentation.

This report serves as an exhaustive technical analysis and operational guide for enterprise architects and senior engineers seeking to maximize the utility of these advanced tools. It deconstructs the bifurcation of the Antigravity IDE into "Editor" and "Manager" views, explicating how this architecture enables the parallelization of engineering tasks across large, complex codebases. It provides a granular examination of the Gemini CLI 3 extension framework and the **Model Context Protocol (MCP)**, demonstrating how to extend agent capabilities to external systems like PostgreSQL databases and cloud infrastructure. Furthermore, it details the implementation of "headless" background automation via GitHub Actions to streamline Pull Request (PR) workflows and introduces Google Code Wiki as the solution to the perennial problem of documentation decay. By synthesizing these tools into cohesive, specific workflows, engineering teams can transition from writing code to orchestrating solutions, effectively multiplying their output and maintaining rigorous quality standards in an increasingly complex digital landscape.

## ---

**1\. The Agent-First Paradigm: Deconstructing Google Antigravity**

The introduction of Google Antigravity marks a decisive departure from the traditional Integrated Development Environment (IDE) model. While historically, IDEs like Visual Studio Code (VS Code) or IntelliJ IDEA have served as sophisticated text editors with integrated tooling, Antigravity redefines the environment as a "Mission Control" center for autonomous agents. This distinction is critical: in a traditional IDE, the human is the primary actor, and the AI (e.g., autocomplete) is the assistant. In Antigravity, the AI agent is the primary actor for execution, and the human assumes the role of architect and reviewer.1

### **1.1 The Bifurcated Interface Architecture**

To support this inversion of control, Antigravity introduces a bifurcated user interface architecture that splits the developer’s operational context into two distinct but deeply integrated views: the **Editor View** and the **Manager View**. Understanding the distinct cognitive and operational modes of these views is essential for maximizing the platform's utility on large projects.

#### **1.1.1 The Editor View: Synchronous Precision**

The Editor View retains the familiar ergonomics of Visual Studio Code, ensuring a low barrier to entry for developers migrating from the existing ecosystem. However, it is augmented with a "sidebar agent" that offers significantly higher autonomy than predecessors like GitHub Copilot.1

* **Operational Mode:** Synchronous, low-latency interaction.
* **Primary Use Case:** This view is optimized for "Fast Mode" operations—granular tasks that require immediate human verification or intervention. Examples include refactoring a specific function, debugging a localized race condition, or generating unit tests for a currently open file.2
* **Agent Interaction:** The agent in this view has direct access to the editor’s AST (Abstract Syntax Tree) and file system. It can perform "inline" edits, where the developer highlights a block of code and prompts the agent to "optimize this query" or "add error handling," with changes applied directly to the buffer.3

#### **1.1.2 The Manager View: Asynchronous Orchestration**

The Manager View (often referred to as "Mission Control") is the defining innovation of Antigravity. It is a visual dashboard designed for high-level orchestration, enabling the developer to spawn, monitor, and interact with multiple agents working asynchronously across different "workspaces" or functional areas of the codebase.1

* **Operational Mode:** Asynchronous, parallel execution.
* **Primary Use Case:** This view handles "Deep Think" or "Planning Mode" tasks—complex, multi-step objectives that may take minutes or hours to complete. Examples include "Migrate the entire authentication system from session-based to JWT," "Update all API endpoints to match the new schema," or "Research and implement a new caching strategy".2
* **Parallelization:** The Manager View allows a single developer to effectively clone their productivity. A user can dispatch one agent to investigate a backend bug, a second agent to update frontend CSS documentation, and a third to run a comprehensive test suite—all simultaneously. The interface visualizes these parallel streams, showing the state of each agent (e.g., *Planning*, *Reading Files*, *Executing Terminal Commands*, *Verifying*).3

### **1.2 The "Artifact-First" Protocol: Bridging Autonomy and Trust**

One of the most significant challenges in adopting autonomous AI agents is the "Black Box" problem: how can a developer trust code generated by an AI without reviewing every character? Antigravity addresses this through the **Artifact-First Protocol**. Instead of displaying a stream of raw tool calls (e.g., fs.readFile, subprocess.exec), agents are programmed to generate high-level, human-readable deliverables called **Artifacts**.1

**Table 1: Taxonomy of Antigravity Artifacts**

| Artifact Category                          | Description & Utility                                                                                                                                                          | Verification Workflow                                                                                                                                                                                                         |
| :----------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Strategic Plans**                  | A markdown-based roadmap generated before any code is written. It outlines the agent's understanding of the task, the files it intends to touch, and the logic it will employ. | **Pre-Execution Review:** The developer reads the plan in the Manager View. If the strategy is flawed (e.g., "Don't use library X, use library Y"), the developer corrects it here, preventing wasted compute cycles. 2 |
| **Task Lists**                       | Dynamic checklists that update in real-time as the agent progresses through the plan.                                                                                          | **Progress Monitoring:** Allows the developer to see exactly where the agent is in the workflow (e.g., "Step 3/10: Updating database schema"). 3                                                                        |
| **Code Diffs**                       | Standardized diff views showing the exact changes proposed to the codebase.                                                                                                    | **Code Review:** Similar to a Pull Request review, the developer can scan the diffs for logic errors or style violations before accepting the changes. 2                                                                |
| **Visual Evidence (Screenshots)**    | Images captured by the agent from the integrated browser, showing the UI state before and after changes.                                                                       | **Visual Regression Testing:** The developer can instantly verify that a CSS change didn't break the layout without running the app themselves. 1                                                                       |
| **Behavioral Evidence (Recordings)** | Video files of the agent interacting with the application (clicking, scrolling, typing).                                                                                       | **Functional Verification:** Proves that complex flows (e.g., "User Login \-\> Dashboard Load") are functioning as expected. 2                                                                                          |
| **Test Logs**                        | Structured output from test runners (e.g., Jest, PyTest) invoked by the agent.                                                                                                 | **Automated Validation:** Green checkmarks indicate that the agent's code passes the project's rigorous test suite. 5                                                                                                   |

This protocol transforms the developer's role from "writer" to "reviewer." By focusing on Artifacts, the developer maintains rigorous quality control without getting bogged down in implementation details.

### **1.3 The Integrated Browser: Closing the Feedback Loop**

A critical differentiator for Antigravity is its integrated "Headless" Chrome browser (via Puppeteer/Chromium), which provides agents with a "visual cortex." Unlike text-only coding assistants that "hallucinate" how a UI might look, Antigravity agents can actually *see* and *interact* with the application they are building.6

**Mechanism of Action:**

1. **Instantiation:** The agent uses the terminal to start the local development server (e.g., npm start).
2. **Navigation:** It commands the integrated browser to navigate to localhost:3000.
3. **Interaction:** Using the **Chrome DevTools MCP** or internal browser tools, the agent can click buttons, type into input fields, and navigate routes.8
4. **Verification:** The agent captures screenshots or analyzes the DOM to verify that the requested feature (e.g., "Add a Submit button") is present and functional.
5. **Self-Correction:** If the agent detects a console error or a visual regression (e.g., overlapping text), it can autonomously read the error log, formulate a fix, apply it to the code, and re-test—all without human intervention.8

## ---

**2\. Orchestrating Multi-Part Projects: The "Manager View" Workflow**

The user query specifically asks about the process for "working on multiple parts of a GitHub project at once." In traditional workflows, this would require context switching: stashing changes, switching branches, and reloading mental models. Antigravity solves this through **Asynchronous Multi-Agent Orchestration**.1

### **2.1 The Parallelization Architecture**

In the Manager View, each task is encapsulated in its own execution environment, effectively a containerized "workspace" context. This ensures that the state of Agent A (working on the database) does not pollute the state of Agent B (working on the frontend).

Scenario: The Full-Stack Feature ImplementationImagine a requirement to "Add a User Profile feature with an avatar upload." This involves database changes, API updates, and frontend UI work.Step 1: Decomposition and DelegationThe developer acts as the Engineering Manager. Instead of tackling the tasks sequentially, they spawn three distinct agents in the Manager View:

* **Agent 1 (Backend \- Database):** "Create a migration for the users table to add an avatar\_url column. Update the SQLAlchemy models."
* **Agent 2 (Backend \- API):** "Create a new endpoint POST /api/user/avatar that handles file uploads to S3 and updates the user record. Use the boto3 library."
* **Agent 3 (Frontend \- UI):** "Create a AvatarUpload React component using the project's design system. It should POST to the new API endpoint."

Step 2: The "Deep Think" PhaseFor these complex tasks, the developer enables "Planning Mode" (Deep Think). The agents do not immediately write code. Instead, they scan the codebase (using the 1M token context) to understand existing patterns.5

* Agent 1 checks alembic configurations.
* Agent 2 checks existing API error handling patterns.
* Agent 3 checks the shadcn/ui component library for file upload styles.

Step 3: Plan Review and SynchronizationEach agent presents a Plan Artifact. The developer reviews them. Crucially, the developer can spot conflicts here. If Agent 2 plans to name the endpoint /upload but Agent 3 expects /avatar, the developer corrects this in the plan before execution.2Step 4: Asynchronous ExecutionOnce approved, the agents execute in parallel.

* Agent 1 runs the migration script locally.
* Agent 2 writes the Python code and generates a test.
* Agent 3 builds the React component and uses the integrated browser to test the visual state.

Step 5: Integration
Because the agents are working on separate files (models vs. routes vs. components), Git conflicts are minimized. The developer reviews the Code Diff Artifacts from all three agents. If satisfied, they can "Accept All" changes, effectively merging three streams of work into the working directory simultaneously.3

### **2.2 Best Workflow: The "Router-Specialist" Pattern**

To maximize this capability, advanced users employ a "Router-Specialist" workflow, often defined in the project's **Context Files** (GEMINI.md).5

* **The Router Agent:** A primary agent that sits in the Manager View. The user gives it a high-level goal: "Implement the User Profile."
* **Delegation:** The Router analyzes the goal and effectively "prompts" sub-agents (or creates sub-tasks) for the specific components (DB, API, UI).
* **Synthesis:** The Router monitors the progress of the sub-tasks and synthesizes the final report for the user.
* **Configuration:** This behavior is codified in the .antigravity/rules.md file, instructing the agent to "Break down complex tasks into sub-components and request user approval for parallel execution plans".5

## ---

**3\. Maximizing Google AI Studio & The 1-Million Token Context**

While Antigravity manages the *execution*, **Google AI Studio** and the **Gemini 3 Pro** model provide the *intelligence* and *contextual understanding* required for large codebases. The 1-million (and up to 2-million) token context window is a game-changer for legacy systems.9

### **3.1 The "Repo-to-Context" Workflow**

To effectively work on a "large complex codebase," the model must "know" the entire code structure. Piecemeal feeding of files is inefficient.

**The Process:**

1. **Repo Flattening (repo2txt):** Use a tool like repo2txt or gitingest to convert the entire repository into a single, massive text file or Markdown document. This process traverses the directory tree, respecting .gitignore but concatenating all source files.11
2. **Ingestion:** Drag and drop this massive file into Google AI Studio. Gemini 3 Pro can ingest \~700,000 lines of code in a single prompt.
3. **Context Caching:** For repetitive tasks, use **Context Caching**. This features allows you to "pay once" to process the heavy repo context and then make cheap, fast queries against it repeatedly. This is vital for cost management and latency reduction.10

### **3.2 "Vibe Coding" at Enterprise Scale**

"Vibe Coding" refers to prompting with high-level intent rather than technical specificity.13 With the massive context loaded, this becomes a powerful enterprise tool.

* **Architectural Queries:** "Analyze the entire codebase and generate a PlantUML sequence diagram for the Order Processing flow. Identify any circular dependencies."
* **Legacy Refactoring:** "We need to migrate from winston logger to pino across the entire backend. Identify every file that imports winston, refactor the logging calls to match the pino API, and generate a pull request description."
* **Visual-to-Code:** Upload a screenshot of a legacy UI and a Figma design of the new UI. Prompt: "Refactor the existing LegacyTable.js component to match this new design, utilizing our ui-kit library found in src/components/ui." The multimodal capabilities of Gemini 3 Pro allow it to bridge the visual and code domains seamlessly.9

## ---

**4\. The "Background Layer": Automated PRs and GitHub Integration**

The user query asks about "Background PR automation." This is achieved not just through the IDE, but by integrating Gemini directly into the CI/CD pipeline via **GitHub Actions** and the **Gemini CLI**. This creates a "headless" agent that works even when the developer is asleep.15

### **4.1 The run-gemini-cli GitHub Action**

Google provides an official GitHub Action that embeds the Gemini agent into the repository workflow. This allows for event-driven, autonomous development tasks.

**Workflow Implementation:**

Step 1: Configuration
Create a workflow file .github/workflows/gemini-agent.yml.

YAML

name: Gemini Agent
on:
  issues:
    types:\[opened, edited\]
  pull\_request:
    types:\[opened, synchronize\]
  issue\_comment:
    types:\[created\]

jobs:
  gemini-agent:
    runs-on: ubuntu-latest
    permissions:
    contents: write
    pull-requests: write
    issues: write
    steps:
    \- uses: actions/checkout@v4
    \- name: Run Gemini CLI
    uses: google-github-actions/run-gemini-cli@v1
    with:
    api\_key: ${{ secrets.GEMINI\_API\_KEY }}
    github\_token: ${{ secrets.GITHUB\_TOKEN }}
    command: ${{ github.event.comment.body |

| github.event.issue.body }}

Note: This YAML configuration is a representative logic structure based on standard GitHub Actions patterns for the Gemini CLI integration.15

**Step 2: "Headless" Use Cases**

* **Automated Triage:** When a new issue is opened, the action triggers Gemini to read the issue body, analyze the codebase, and attempt to reproduce the bug or suggest a fix. It can auto-label the issue (e.g., "bug", "frontend").15
* **Background Code Review:** On every PR open, Gemini scans the diff. It uses the "Ruthless Reviewer" persona (defined in extensions) to check for security vulnerabilities, style violations, and logic errors, posting them as comments on the PR.15
* **On-Demand Fixes:** A developer can comment @gemini-cli /fix on a PR line. The action detects the comment, runs the agent to generate a fix for that specific function, and pushes a commit to the branch automatically. This is "Background PR Automation" in its purest form.15

## ---

**5\. Gemini CLI 3 & The Extension Ecosystem**

The **Gemini CLI 3** is the command-line interface that brings agentic capabilities to the terminal. It is highly extensible, allowing developers to create custom tools and workflows.

### **5.1 The Extension Architecture**

Gemini CLI 3 extensions are packages that bundle **Prompts**, **Custom Commands**, and **MCP Servers**. They are located in \~/.gemini/extensions/.15

Structure of gemini-extension.json:To create a "specific workflow," a developer creates an extension. The configuration file gemini-extension.json is the heart of this:

* **mcpServers:** Defines connections to external tools (e.g., a Database or Cloud API).
* **commands:** Maps slash commands (e.g., /deploy) to specific prompt files.
* **contextFileName:** Points to a markdown file that gives the agent its "System Instructions" for this extension.15

### **5.2 Key Extensions for Complex Codebases**

The user asked about "Gemini CLI 3 extensions." Several are critical for enterprise workflows:

1. **The "Nana Banana" Extension:** Mentioned in research as a "quirky" example 18, this extension demonstrates the capability to inject *personality* and *multimodal generation* (images) into the CLI. While seemingly fun, it proves the framework can handle non-text outputs and distinct personas, which is useful for creating a "Senior Architect" persona vs. a "Junior Coder" persona.
2. **GitHub MCP Extension:** Connects the agent to the GitHub API. Allows commands like /gh list-prs or /gh create-issue. It enables the agent to act as a project manager.20
3. **PostgreSQL MCP Extension:** Gives the agent direct read/write access to a database. The agent can inspect schemas, run queries to debug data issues, and write migration scripts.20
4. **Filesystem MCP:** The most fundamental extension. It gives the agent secure, granular access to read and write files on the local machine, essential for any coding task.22

## ---

**6\. Dynamic Knowledge: Google Code Wiki**

For large codebases, documentation is rarely up to date. **Google Code Wiki** (codewiki.google) addresses this by treating documentation as a dynamic, living entity.23

### **6.1 The Mechanics of "Living Documentation"**

Code Wiki is not a static text file. It is an automated system that scans the repository after **every commit**.

1. **Graph Generation:** It parses the code to build a knowledge graph (nodes \= classes/functions, edges \= dependencies/calls).25
2. **Regeneration:** It uses Gemini to rewrite the documentation for any changed components, ensuring the "Docs" always match the "Code."
3. **Hyperlinking:** It creates deep links. Clicking a function name in the Wiki takes you directly to the definition in the source code.26

### **6.2 The Code Wiki Gemini CLI Extension**

For "private repository support," Google is releasing a **Code Wiki Gemini CLI extension**. This allows the Code Wiki engine to run *locally* on the developer's machine or internal server.27

* **Workflow:** The developer runs gemini codewiki init. The tool indexes the local repo and serves a local web server (e.g., localhost:8080) hosting the dynamic wiki. This ensures proprietary code never leaves the corporate network while still benefiting from AI-generated, up-to-date documentation.

## ---

**7\. Designing the Ultimate Workflow: A Step-by-Step Guide**

To "effectively maximize" these tools, a developer should adopt the following integrated workflow:

**Phase 1: Setup & Initialization**

1. **Install Antigravity & Gemini CLI 3\.**
2. **Clone the Antigravity Workspace Template:** This provides the .antigravity/ structure and artifacts/ directories.5
3. **Run /init:** Use the Gemini CLI to scan the repo and auto-generate the GEMINI.md context file, establishing the baseline knowledge.29
4. **Configure Extensions:** Install the GitHub MCP and Postgres MCP extensions in \~/.gemini/settings.json to give the agent necessary external access.15

**Phase 2: Execution (The "Deep Work" Loop)**

1. **Task Ingestion:** Receive a feature request (e.g., "Add Dark Mode").
2. **Mission Control:** Open Antigravity Manager View. Spawn two agents:
   * *Agent A (CSS Specialist):* "Identify all color variables in src/styles and create a dark mode theme mapping."
   * *Agent B (Component Updater):* "Update the ThemeContext provider to support toggling."
3. **Planning:** Review the **Plan Artifacts** from both agents. Ensure they agree on the variable naming convention.
4. **Parallel Action:** Agents execute. Agent A writes CSS; Agent B writes React code.
5. **Verification:** Agents use the **Integrated Browser** to toggle the theme and take screenshots.
6. **Review:** Developer reviews the screenshots and code diffs.

**Phase 3: Automation (The "Background" Loop)**

1. **Commit:** Developer accepts changes and pushes to a branch.
2. **PR Creation:** Developer runs gemini gh create-pr \--title "Add Dark Mode" \--body "Implements dark mode via ThemeContext." using the CLI.
3. **Background Review:** The **GitHub Action** triggers. The "Ruthless Reviewer" agent scans the PR in the cloud and comments: "Missing dark mode variable for Sidebar component."
4. **Fix:** Developer comments @gemini-cli /fix on the PR. The background agent pushes the fix.
5. **Documentation:** **Code Wiki** detects the merge to main and automatically updates the "Theming" section of the project documentation to include the new Dark Mode implementation.

## ---

**8\. Conclusion**

The convergence of Google Antigravity, Gemini CLI 3, and Code Wiki represents a maturation of AI in software engineering. We are moving past the novelty of "chatting with code" to a disciplined, industrialized process of **Agentic Engineering**. By leveraging the **Manager View** for parallel orchestration, the **Model Context Protocol** for tool integration, and **GitHub Actions** for headless automation, developers can handle codebases of immense complexity with greater speed and reliability. The key to success lies in shifting the human mindset: trust the **Artifacts**, govern via **Context Files**, and let the agents handle the implementation.

#### **Works cited**

1. Google Antigravity \- Wikipedia, accessed December 6, 2025, [https://en.wikipedia.org/wiki/Google\_Antigravity](https://en.wikipedia.org/wiki/Google_Antigravity)
2. Tutorial : Getting Started with Google Antigravity | by Romin Irani \- Medium, accessed December 6, 2025, [https://medium.com/google-cloud/tutorial-getting-started-with-google-antigravity-b5cc74c103c2](https://medium.com/google-cloud/tutorial-getting-started-with-google-antigravity-b5cc74c103c2)
3. Build with Google Antigravity, our new agentic development platform, accessed December 6, 2025, [https://developers.googleblog.com/en/build-with-google-antigravity-our-new-agentic-development-platform/](https://developers.googleblog.com/en/build-with-google-antigravity-our-new-agentic-development-platform/)
4. Getting Started with Google Antigravity, accessed December 6, 2025, [https://codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
5. study8677/antigravity-workspace-template: The ultimate ... \- GitHub, accessed December 6, 2025, [https://github.com/study8677/antigravity-workspace-template](https://github.com/study8677/antigravity-workspace-template)
6. How to Set Up and Use Google Antigravity | Codecademy, accessed December 6, 2025, [https://www.codecademy.com/article/how-to-set-up-and-use-google-antigravity](https://www.codecademy.com/article/how-to-set-up-and-use-google-antigravity)
7. Google Antigravity Review: A Beginner's Guide to the AI IDE, accessed December 6, 2025, [https://www.aifire.co/p/google-antigravity-review-a-beginner-s-guide-to-the-ai-ide](https://www.aifire.co/p/google-antigravity-review-a-beginner-s-guide-to-the-ai-ide)
8. Google Antigravity Review: How Strong Is This Free Agent-First IDE? \- DEV Community, accessed December 6, 2025, [https://dev.to/james\_miller\_8dc58a89cb9e/google-antigravity-review-how-strong-is-this-free-agent-first-ide-10d5](https://dev.to/james_miller_8dc58a89cb9e/google-antigravity-review-how-strong-is-this-free-agent-first-ide-10d5)
9. Gemini 3 for developers: New reasoning, agentic capabilities \- Google Blog, accessed December 6, 2025, [https://blog.google/technology/developers/gemini-3-developers/](https://blog.google/technology/developers/gemini-3-developers/)
10. Understand and count tokens | Gemini API \- Google AI for Developers, accessed December 6, 2025, [https://ai.google.dev/gemini-api/docs/tokens](https://ai.google.dev/gemini-api/docs/tokens)
11. My AI Workflow for Understanding Any Codebase \- Peter Steinberger, accessed December 6, 2025, [https://steipete.me/posts/2025/understanding-codebases-with-ai-gemini-workflow](https://steipete.me/posts/2025/understanding-codebases-with-ai-gemini-workflow)
12. Gemini Developer API pricing, accessed December 6, 2025, [https://ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)
13. I'm ready to try Google's Antigravity coding tool, and these new usage limits are my green light \- Chrome Unboxed, accessed December 6, 2025, [https://chromeunboxed.com/im-ready-to-try-googles-antigravity-coding-tool-and-these-new-usage-limits-are-my-green-light/](https://chromeunboxed.com/im-ready-to-try-googles-antigravity-coding-tool-and-these-new-usage-limits-are-my-green-light/)
14. Vibe Coding Explained: Tools and Guides | Google Cloud, accessed December 6, 2025, [https://cloud.google.com/discover/what-is-vibe-coding](https://cloud.google.com/discover/what-is-vibe-coding)
15. google-gemini/gemini-cli: An open-source AI agent that brings the power of Gemini directly into your terminal. \- GitHub, accessed December 6, 2025, [https://github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
16. google-gemini/gemini-cli-action \- GitHub, accessed December 6, 2025, [https://github.com/google-gemini/gemini-cli-action](https://github.com/google-gemini/gemini-cli-action)
17. ZhangYu-zjut/awesome-Antigravity: The comprehensive ... \- GitHub, accessed December 6, 2025, [https://github.com/ZhangYu-zjut/awesome-Antigravity](https://github.com/ZhangYu-zjut/awesome-Antigravity)
18. Google DeepMind Gemini CLI 3.0 & GenKit Extension Framework \- Geeky Gadgets, accessed December 6, 2025, [https://www.geeky-gadgets.com/gemini-cli-3-0-ai-coding-assistant/](https://www.geeky-gadgets.com/gemini-cli-3-0-ai-coding-assistant/)
19. Google DeepMind Gemini CLI 3.0 & GenKit: A Powerful Extension, accessed December 6, 2025, [https://siit.co/blog/google-deepmind-gemini-cli-3-0-and-genkit-a-powerful-extension-framework-redefining-ai-development/48873](https://siit.co/blog/google-deepmind-gemini-cli-3-0-and-genkit-a-powerful-extension-framework-redefining-ai-development/48873)
20. Top 10 Best MCP Servers to Improve Your AI Workflows \- Oxylabs, accessed December 6, 2025, [https://oxylabs.io/blog/best-mcp-servers](https://oxylabs.io/blog/best-mcp-servers)
21. Top 10 Best MCP (Model Context Protocol) Servers in 2025 \- GBHackers, accessed December 6, 2025, [https://gbhackers.com/best-mcp-model-context-protocol-servers/](https://gbhackers.com/best-mcp-model-context-protocol-servers/)
22. Example Servers \- Model Context Protocol, accessed December 6, 2025, [https://modelcontextprotocol.io/examples](https://modelcontextprotocol.io/examples)
23. Introducing Code Wiki: Accelerating your code understanding \- Google Developers Blog, accessed December 6, 2025, [https://developers.googleblog.com/en/introducing-code-wiki-accelerating-your-code-understanding/](https://developers.googleblog.com/en/introducing-code-wiki-accelerating-your-code-understanding/)
24. Google Code Wiki Aims to Solve Documentation's Oldest Problem \- DevOps.com, accessed December 6, 2025, [https://devops.com/google-code-wiki-aims-to-solve-documentations-oldest-problem/](https://devops.com/google-code-wiki-aims-to-solve-documentations-oldest-problem/)
25. Google's Code Wiki Just Read My Mind — And My Code. | by Vikas Ranjan \- Medium, accessed December 6, 2025, [https://medium.com/google-cloud/googles-code-wiki-just-read-my-mind-and-my-code-17075e14fbec](https://medium.com/google-cloud/googles-code-wiki-just-read-my-mind-and-my-code-17075e14fbec)
26. Google Code Wiki: Free AI That Finally Understands Your Entire Codebase, accessed December 6, 2025, [https://www.mejba.me/blog/google-code-wiki-free-ai-documentation-tool-guide](https://www.mejba.me/blog/google-code-wiki-free-ai-documentation-tool-guide)
27. Google's New AI Tool Solves a Problem for Every Lazy Developer \- It's FOSS, accessed December 6, 2025, [https://itsfoss.com/news/google-code-wiki/](https://itsfoss.com/news/google-code-wiki/)
28. Google Launches Code Wiki: A Living Documentation System for Developers \- TechGig, accessed December 6, 2025, [https://content.techgig.com/technology/google-code-wiki-launch-dynamic-documentation/articleshow/125535784.cms](https://content.techgig.com/technology/google-code-wiki-launch-dynamic-documentation/articleshow/125535784.cms)
29. This Week in Gemini CLI \- Google Cloud \- Medium, accessed December 6, 2025, [https://medium.com/google-cloud/hot-new-features-of-the-week-in-gemini-cli-d7cda5cb9833](https://medium.com/google-cloud/hot-new-features-of-the-week-in-gemini-cli-d7cda5cb9833)
