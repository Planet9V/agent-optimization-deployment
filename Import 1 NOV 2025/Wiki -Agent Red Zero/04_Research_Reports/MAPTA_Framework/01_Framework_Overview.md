# Part 1 of 3: Framework Overview

**Series**: MAPTA Framework
**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_Architecture_Components.md)

---

# MAPTA Framework: Comprehensive Research Report
## Multi-Agent Penetration Testing AI for Web Applications

**Research Date:** October 16, 2025
**Research Confidence:** High (85%)
**Primary Sources:** Academic papers (arXiv:2508.20816), GitHub repository, benchmark data

---

## Executive Summary

MAPTA (Multi-Agent Penetration Testing AI) represents a breakthrough in autonomous web application security assessment, combining large language model orchestration with tool-grounded execution and end-to-end exploit validation. As the first open-source multi-agent penetration testing AI system, MAPTA achieves 76.9% success on the 104-challenge XBOW benchmark while maintaining cost efficiency at $0.117 median per challenge.

**Key Achievements:**
- Perfect performance on SSRF and misconfiguration vulnerabilities (100%)
- 83% success on broken authorization
- 85% success on server-side template injection (SSTI)
- 83% success on SQL injection
- 19 real-world vulnerabilities discovered (14 severe: RCE, command injection)
- Average cost of $3.67 per open-source assessment

---

## 1. Multi-Agent Architecture & Coordination

### 1.1 Three-Role Agent System

MAPTA implements a sophisticated coordinator/executor architecture with three specialized agent roles:

#### **Coordinator Agent**
- **Primary Role:** Strategic planning and high-level attack-path reasoning
- **Capabilities:**
  - Tool orchestration across 8 integrated tools
  - Delegation to sandbox agents
  - Direct command execution (run_command)
  - Python runtime access (run_python)
  - Report synthesis and alerting
  - Attack strategy formulation

- **Decision-Making Pattern:**
  - Analyzes target application characteristics
  - Generates attack hypotheses based on reconnaissance
  - Selects appropriate tools (nmap, ffuf, custom scripts)
  - Delegates tactical execution to sandbox agents
  - Aggregates results and synthesizes findings

#### **Sandbox Agents (1..N)**
- **Primary Role:** Tactical execution in isolated LLM contexts
- **Capabilities:**
  - Shell command execution (run_command)
  - Python script execution (run_python)
  - Focused context per subtask
  - Shared Docker environment access

- **Isolation Strategy:**
  - Each sandbox agent receives isolated prompts
  - Separate LLM memory per agent prevents cross-talk
  - Maintains focus on specific subtasks
  - Prevents prompt bloat from unrelated context

#### **Validation Agent**
- **Primary Role:** Concrete proof-of-concept verification
- **Capabilities:**
  - Consumes candidate PoC artifacts (HTTP sequences, payloads, scripts)
  - Executes exploits in sandboxed environment
  - Returns pass/fail with concrete evidence
  - Validates exploitability through observation

- **Validation Criteria:**
  - **CTF Scenarios:** Flag capture confirmation
  - **Real-World:** Observable side-effects (state changes, data access, RCE)
  - Evidence-based verification (no theoretical findings)

### 1.2 Coordination Patterns

#### **Semi-Decentralized Architecture**
MAPTA balances centralized strategy with distributed execution:

```
┌─────────────────────────────────────┐
│      Coordinator Agent              │
│  - Strategic planning               │
│  - Tool selection                   │
│  - Result aggregation               │
└────────┬────────────────────────────┘
         │
         ├──────────┬──────────┬───────────┐
         ▼          ▼          ▼           ▼
    ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
    │Sandbox1│ │Sandbox2│ │SandboxN│ │Validation│
    │Agent   │ │Agent   │ │Agent   │ │Agent     │
    └───┬────┘ └───┬────┘ └───┬────┘ └────┬─────┘
        │          │          │            │
        └──────────┴──────────┴────────────┘
                      │
              ┌───────▼────────┐
              │ Shared Docker  │
              │  Container     │
              │  Environment   │
              └────────────────┘
```

#### **Communication Flow**
1. **Delegation:** Coordinator → Sandbox (task assignment)
2. **Execution:** Sandbox → Docker (tool invocation)
3. **Reporting:** Sandbox → Coordinator (results)
4. **Validation:** Coordinator → Validation Agent (PoC verification)
5. **Synthesis:** All results → Coordinator (final report)

#### **Coordination Advantages**
- **Optimal Balance:** Strategic decision-making with tactical execution
- **Context Management:** Isolated cognition, shared state
- **Scalability:** Multiple sandbox agents per coordinator
- **State Preservation:** Shared Docker enables artifact reuse

---

## 2. Specialist Agent Roles Deep Dive

### 2.1 Coordinator Agent: Strategic Intelligence

**Tool Arsenal (8 tools):**
1. `delegate_to_sandbox` - Task distribution to sandbox agents
2. `run_command` - Direct shell execution
3. `run_python` - Python script execution
4. `read_file` - Artifact examination
5. `write_file` - Script/payload creation
6. `alert_finding` - Vulnerability reporting
7. `request_validation` - PoC verification trigger
8. `synthesize_report` - Final report generation

**Decision-Making Intelligence:**
- **Reconnaissance-Driven:** Analyzes nmap/ffuf results to inform next steps
- **Hypothesis Generation:** Formulates attack vectors based on discovered services
- **Tool Selection Logic:** Chooses appropriate tools based on target characteristics
- **Adaptive Strategy:** Adjusts approach based on success/failure feedback

**Example Workflow:**
```
1. Initial reconnaissance with nmap
   → Discovers port 80 (HTTP), port 3306 (MySQL)
2. Delegates web enumeration to Sandbox-1 (ffuf)
   → Identifies /admin endpoint, /api/v1/users
3. Delegates SQL injection testing to Sandbox-2
   → Tests /api/v1/users?id= parameter
4. Receives positive SQLI indicator
5. Requests validation of SQLI payload
6. Receives confirmed exploitation
7. Synthesizes final vulnerability report
```

### 2.2 Sandbox Agents: Tactical Executors

**Specialized Execution Context:**
- **Focused Prompts:** Task-specific instructions without full attack context
- **Isolated Memory:** No awareness of other sandbox operations
- **Tool Limitation:** Only run_command and run_python (intentional constraint)
- **Efficiency:** Reduced token usage through focused context

**State Management:**
- **Persistent Filesystem:** Scripts/artifacts accessible to all agents
- **Credential Sharing:** Job-scoped secrets available in container
- **Dependency Reuse:** Python libraries installed once, used by all
- **Reconnaissance Sharing:** Scan results persist across subtasks

**Example Sandbox Execution:**
```bash
# Sandbox-1: Web enumeration
ffuf -u http://target/FUZZ -w /wordlist.txt -o /results/ffuf.json

# Sandbox-2: Exploit testing (reuses ffuf results from /results/)
python3 /scripts/sqli_test.py --url http://target/api/v1/users
```

### 2.3 Validation Agent: Empirical Verification

**Critical Innovation:** Transforms vulnerability assessment from hypothesis → empirical proof

**Validation Process:**
1. **Artifact Consumption:** Receives candidate PoC (HTTP sequence, payload, script)
2. **Execution:** Runs exploit in sandboxed Docker environment
3. **Observation:** Monitors for concrete evidence
4. **Verification:** Confirms exploitability with observable proof
5. **Reporting:** Pass/fail with evidence artifacts

**Validation Types:**
- **CTF Scenarios:** Flag retrieval confirmation
- **Authentication Bypass:** Session token acquisition
- **SQL Injection:** Data extraction verification
- **RCE:** Command execution confirmation
- **SSRF:** Internal resource access proof
- **File Operations:** Read/write confirmation

**False Positive Elimination:**
Traditional tools report theoretical vulnerabilities; MAPTA requires concrete exploitation:
```
Traditional: "Potential SQL injection detected" (hypothesis)
MAPTA: "SQL injection confirmed - extracted user table with 1,247 records" (proof)
```

---

## 3. Docker Container Strategy

### 3.1 Per-Job Container Architecture

**Design Philosophy:** Single ephemeral container per assessment job

**Key Innovation:** Shared container for all agents in a job, isolated containers across jobs

```
Job A: [Coordinator + Sandbox-1 + Sandbox-2 + Validation] → Container-A
Job B: [Coordinator + Sandbox-1 + Sandbox-N] → Container-B
Job C: [Coordinator + Validation] → Container-C
```

### 3.2 Container Lifecycle

**Phase 1: Creation**
```bash
# Container instantiation
docker run -d --name mapta-job-<uuid> \
  -e TARGET_URL=<target> \
  -e CREDENTIALS=<job-secrets> \
  -v /tools:/tools:ro \
  ubuntu-derivative:latest

# Tool installation
apt-get install -y nmap ffuf python3-pip
pip3 install requests beautifulsoup4 sqlmap
```

**Phase 2: Operation**
- All sandbox agents execute within same container
- Filesystem artifacts persist: `/results/`, `/scripts/`, `/artifacts/`
- Credentials stored in environment variables
- Network access configured per job requirements
- Shared Python environment with installed dependencies

**Phase 3: Termination**
```bash
# Evidence extraction
docker cp mapta-job-<uuid>:/results /local/evidence/
docker cp mapta-job-<uuid>:/logs /local/logs/

# Secret purging
docker exec mapta-job-<uuid> rm -rf /credentials /secrets

# Container removal
docker stop mapta-job-<uuid>
docker rm mapta-job-<uuid>
```

### 3.3 Advantages of Single Container Strategy

**1. State Persistence Across Agents**
- Reconnaissance results accessible to all agents
- Scripts/exploits reusable without re-transmission
- Dependencies installed once, used by all
- Reduces redundant operations

**2. Cost Efficiency**
- Amortized setup costs (tool installation, network configuration)
- No container overhead per sandbox agent
- Reduced data transfer between container/host
- Faster execution through artifact reuse

**3. Context Isolation Despite Shared Environment**
- LLM contexts separated (distinct prompts/memory)
- Prevents prompt bloat from unrelated operations
- No cross-talk between sandbox agents
- Coordinator maintains holistic view

**4. Security Boundaries**
- Container isolation between concurrent jobs
- Network segmentation per assessment
- Credential scope limited to job
- Evidence retained, secrets purged

### 3.4 Docker vs Traditional Isolation Approaches

| Approach | Isolation Level | State Sharing | Cost | Complexity |
|----------|----------------|---------------|------|------------|
| **MAPTA (Single Container/Job)** | Job-level | Within job | Low | Medium |
| VM per Agent | Agent-level | None | Very High | High |
| Container per Agent | Agent-level | Requires orchestration | High | High |
| No Isolation | None | Global | Very Low | Low |

---

## 4. Proof-of-Concept Validation Methodology

### 4.1 Validation Philosophy

**Core Principle:** Distinguish theoretical vulnerabilities from practical exploits through sandboxed proof-of-concept execution.

**Transformation:** Vulnerability assessment moves from hypothesis generation → empirical validation

### 4.2 Validation Workflow

```
┌────────────────────────────────────────────────────────┐
│ Phase 1: Vulnerability Hypothesis                      │
│ Coordinator: "Potential SQLI at /api/users?id="       │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2: PoC Artifact Creation                         │
│ Sandbox Agent: Generate exploit payload/script        │
│ Output: HTTP request sequence OR Python script        │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│ Phase 3: Validation Request                            │
│ Coordinator → Validation Agent                         │
│ Payload: {artifact: sqli_exploit.py, target: /api}   │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│ Phase 4: Concrete Execution                            │
│ Validation Agent: Execute exploit in Docker           │
│ Monitor: Response codes, data extraction, side-effects│
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│ Phase 5: Evidence Collection                           │
│ - Success: Flag/data extracted, screenshot, logs      │
│ - Failure: Error logs, response analysis              │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│ Phase 6: Pass/Fail Decision                            │
│ Return: {status: PASS/FAIL, evidence: artifacts}     │
└────────────────────────────────────────────────────────┘
```

### 4.3 Validation Criteria by Vulnerability Type

#### **SQL Injection**
- **Evidence:** Extracted database records, table schemas, or error messages confirming DBMS
- **PoC:** Python script with parameterized payload execution
- **Confirmation:** Data retrieval or observable database modification

#### **Server-Side Template Injection (SSTI)**
- **Evidence:** Template expression evaluation (7*7=49 in response)
- **PoC:** HTTP request with template payload
- **Confirmation:** Arithmetic/string operations reflected in response

#### **Remote Code Execution (RCE)**
- **Evidence:** Command output, reverse shell connection, file creation
- **PoC:** Shell command sequence or exploit script
- **Confirmation:** System-level operation execution

#### **Server-Side Request Forgery (SSRF)**
- **Evidence:** Internal resource access, metadata service queries
- **PoC:** HTTP request with internal URL payload
- **Confirmation:** Response from internal service

#### **Broken Authorization**
- **Evidence:** Access to restricted resources with insufficient privileges
- **PoC:** HTTP request sequence with modified tokens/cookies
- **Confirmation:** Successful access to admin/user-specific data

#### **Cross-Site Scripting (XSS)**
- **Evidence:** JavaScript execution in browser context
- **PoC:** HTTP request with XSS payload
- **Confirmation:** Alert dialog, DOM manipulation, or cookie access

### 4.4 False Positive Elimination

**Traditional Approach (High False Positives):**
```
Scanner: Detects 'id' parameter
Analysis: Assumes potential SQLI
Report: "Possible SQL injection vulnerability"
Reality: Parameter sanitized, not exploitable
Result: False positive, wasted investigation time
```

**MAPTA Approach (Empirical Validation):**
```
Scanner: Detects 'id' parameter
Hypothesis: Potential SQLI
Validation: Execute SQLI payload in sandbox
Observation: Request blocked by WAF, no data extracted
Validation Result: FAIL - Not exploitable
Report: No vulnerability (or informational: WAF present)
Result: No false positive
```

**Impact:**
- Dramatically reduced false positive rate
- Actionable findings only
- Evidence-backed vulnerability reports
- Saves analyst time on verification

### 4.5 Resource Efficiency Correlation

**Key Finding:** Success strongly correlates with resource efficiency

| Outcome | Median Tool Calls | Median Cost | Observation |
|---------|------------------|-------------|-------------|
| Success | ~25 calls | $0.073 | Efficient exploitation |
| Failure | ~60 calls | $0.357 | Exhaustive attempts fail |

**Practical Implication:** Early-stopping threshold at ~40 tool calls or $0.30 per challenge
- Challenges requiring >40 calls unlikely to succeed
- Cost-benefit analysis favors stopping after threshold
- Enables continuous testing within budget constraints

---

## 5. Context Isolation Approach

### 5.1 Dual-Layer Isolation

MAPTA implements a novel isolation strategy: **LLM cognition isolation + shared execution environment**


---

**Navigation**: [📚 Series Overview](./00_Series_Overview.md) | [Part 2 →](./02_Architecture_Components.md)
**Part 1 of 3** | Lines 1-417 of original document
