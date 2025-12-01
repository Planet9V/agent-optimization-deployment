# Part 2 of 3: Architecture & Components

**Series**: MAPTA Framework
**Navigation**: [← Part 1](./01_Framework_Overview.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 3 →](./03_Implementation_Guide.md)

---


```
┌─────────────────────────────────────────────────────────┐
│                    LLM Layer (Isolated)                 │
├──────────────────┬──────────────────┬──────────────────┤
│ Coordinator      │ Sandbox-1        │ Sandbox-2        │
│ Context          │ Context          │ Context          │
│ ----------------│ ----------------│ ----------------│
│ Full attack path│ Enum task only   │ Exploit task only│
│ Strategic view  │ No global context│ No global context│
│ Tool orchestr.  │ Focused execution│ Focused execution│
└──────────────────┴──────────────────┴──────────────────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────┐
│            Execution Layer (Shared Container)            │
│  - Filesystem: /results/, /scripts/, /artifacts/        │
│  - Credentials: Environment variables                    │
│  - Tools: nmap, ffuf, python3, sqlmap                   │
│  - Network: Target access configuration                 │
└──────────────────────────────────────────────────────────┘
```

### 5.2 LLM Context Isolation Benefits

**Problem Addressed:** Prompt bloat and cross-talk in multi-step assessments

**Traditional Single-Agent Approach:**
```
Agent Context (After 50 tool calls):
- Initial reconnaissance (10K tokens)
- Web enumeration results (15K tokens)
- Vulnerability testing logs (20K tokens)
- Failed exploit attempts (30K tokens)
- Current task: SQLI validation
→ Total: 75K tokens, mostly irrelevant to current task
→ Result: Degraded performance, hallucinations, high cost
```

**MAPTA Multi-Agent Approach:**
```
Coordinator Context:
- High-level attack strategy (5K tokens)
- Delegated task summaries (3K tokens)
- Validation results (2K tokens)
→ Total: 10K tokens, strategic overview only

Sandbox-2 Context (SQLI testing):
- Task: Test SQLI on /api/users
- Available tools: run_command, run_python
- Previous results: /results/ffuf.json
→ Total: 2K tokens, focused on current task
→ Result: Efficient, focused execution
```

**Advantages:**
1. **Token Efficiency:** Reduced context size per agent (60-80% reduction)
2. **Focus:** Agents reason only about relevant information
3. **Scalability:** Context growth linear, not exponential
4. **Cost:** Lower token consumption per decision

### 5.3 Shared Execution State Benefits

Despite isolated LLM contexts, shared Docker environment enables:

**1. Artifact Reuse**
```bash
# Coordinator delegates reconnaissance
Sandbox-1: nmap -A target > /results/nmap.txt

# Later, another sandbox references results
Sandbox-2: python3 exploit.py --targets /results/nmap.txt
# No need to re-transmit nmap results through LLM context
```

**2. Dependency Sharing**
```bash
# First sandbox installs dependencies
Sandbox-1: pip3 install requests beautifulsoup4

# Later sandboxes reuse installation
Sandbox-2: python3 -c "import requests" # Already installed
```

**3. Credential Management**
```bash
# Credentials set once in container environment
export API_KEY=<job-secret>
export SESSION_TOKEN=<auth-token>

# All agents access credentials
Sandbox-N: curl -H "Authorization: Bearer $SESSION_TOKEN" target/api
```

**4. State Continuity**
```bash
# Sandbox-1 establishes session
/results/session_cookies.txt created

# Sandbox-2 maintains session
curl --cookie /results/session_cookies.txt target/admin
```

### 5.4 Cross-Job Isolation

While agents within a job share a container, jobs remain strictly isolated:

```
Job-A Container: Assessment of target-A.com
├─ Network: Access to target-A.com only
├─ Credentials: Job-A secrets
├─ Filesystem: /results/job-A/
└─ Lifecycle: Job-A duration

Job-B Container: Assessment of target-B.com
├─ Network: Access to target-B.com only
├─ Credentials: Job-B secrets
├─ Filesystem: /results/job-B/
└─ Lifecycle: Job-B duration

→ No data leakage between jobs
→ No credential mixing
→ Parallel job execution possible
```

---

## 6. Unique Features vs Traditional Pentest Tools

### 6.1 Comparative Analysis

| Feature | Traditional Tools (Burp, ZAP, Metasploit) | MAPTA |
|---------|-------------------------------------------|-------|
| **Automation Level** | Semi-automated (human-driven) | Fully autonomous |
| **Intelligence** | Rule-based pattern matching | LLM reasoning + learning |
| **Validation** | Theoretical detection | Concrete PoC execution |
| **False Positives** | High (20-40%) | Low (validation-based) |
| **Cost Model** | Per-license or per-scan | Per-assessment ($0.12-$3.67) |
| **Adaptability** | Fixed rule sets | Adaptive strategy |
| **Tool Integration** | Manual orchestration | Intelligent tool selection |
| **Reporting** | Template-based | Context-aware synthesis |
| **Learning** | No improvement over time | Potential for case-based learning |

### 6.2 Unique Innovations

#### **1. End-to-End Autonomous Operation**
**Traditional:**
- Security analyst initiates scan
- Tool executes predefined tests
- Analyst reviews findings (many false positives)
- Analyst manually validates vulnerabilities
- Analyst writes report

**MAPTA:**
- System receives target URL
- Autonomous reconnaissance, hypothesis generation, testing
- Automatic PoC validation (no analyst intervention)
- Evidence-backed findings only
- Automated report synthesis

**Impact:** 10-50x reduction in analyst time per assessment

#### **2. LLM-Driven Hypothesis Generation**
**Traditional Tools:**
```python
# Fixed pattern matching
if 'id=' in url_params:
    test_sql_injection(param='id')
```

**MAPTA:**
```
Coordinator observes: /api/users?id=123 returns user data
Coordinator reasons: "Numeric ID parameter may lack validation"
Coordinator generates: Multiple SQLI payloads adapted to response patterns
Coordinator delegates: Sandbox agent executes contextual testing
Coordinator adapts: Refines approach based on WAF detection
```

**Impact:** Higher success on complex vulnerabilities requiring creative approaches

#### **3. Multi-Agent Coordination**
**Traditional:**
- Linear workflow: Scan → Analyze → Exploit
- No parallel task execution
- Single tool perspective

**MAPTA:**
- Parallel reconnaissance by multiple sandbox agents
- Simultaneous testing of multiple vulnerabilities
- Coordinator synthesizes findings across agents
- Efficient resource utilization

**Impact:** 3-5x faster assessment completion

#### **4. Proof-of-Concept Validation Pipeline**
**Traditional:**
- Tools report: "Potential vulnerability detected"
- Analyst must manually verify each finding
- High false positive rate (20-40%)

**MAPTA:**
- System reports: "Vulnerability confirmed with concrete exploitation"
- Automatic validation with evidence artifacts
- Minimal false positives (<5%)

**Impact:** Dramatically reduced analyst verification time

#### **5. Cost-Performance Transparency**
**Traditional:**
- Opaque cost model (license fees, analyst time)
- No performance metrics
- Unknown success rates

**MAPTA:**
- Complete token-level accounting
- Per-challenge cost visibility ($0.073-$0.357)
- Benchmark success rates (76.9% on XBOW)
- Reproducible evaluation

**Impact:** Predictable budgeting and ROI analysis

#### **6. Open-Source and Reproducible**
**Traditional:**
- Proprietary tools (Burp Suite Pro, Metasploit Pro)
- Closed-source algorithms
- Non-reproducible results

**MAPTA:**
- Fully open-source (GitHub: arthurgervais/mapta)
- Published methodology (arXiv:2508.20816)
- Reproducible benchmarks
- Community contributions enabled

**Impact:** Academic validation, transparency, customization

### 6.3 Limitations Compared to Traditional Tools

**1. Blind SQL Injection**
- MAPTA: 0% success rate on blind SQLI
- Issue: Absence of explicit response cues for timing-based payloads
- Traditional: Manual time-based analysis by experienced analysts

**2. Complex XSS Scenarios**
- MAPTA: 57% success on XSS (vs 83% on standard SQLI)
- Issue: Context-dependent payload encoding, DOM manipulation complexity
- Traditional: Burp Suite Intruder with manual payload refinement

**3. Logic Vulnerabilities**
- MAPTA: Limited success on business logic flaws
- Issue: Requires deep application context and workflow understanding
- Traditional: Manual testing by analysts with domain expertise

**4. Stealth and Evasion**
- MAPTA: No explicit stealth mode
- Issue: May trigger IDS/IPS through aggressive testing
- Traditional: Manual rate-limiting and evasion techniques

**5. Custom Application Protocols**
- MAPTA: Focused on HTTP/HTTPS web applications
- Traditional: Metasploit supports diverse protocols (SMB, RDP, etc.)

### 6.4 Complementary Hybrid Approach

**Optimal Strategy:** MAPTA + Traditional Tools + Human Expertise

```
┌───────────────────────────────────────────────────────┐
│ Phase 1: MAPTA Autonomous Assessment                  │
│ - Handles common vulnerabilities (SQLI, SSTI, etc.)  │
│ - Validates findings with PoC                         │
│ - Generates initial security baseline                 │
│ Cost: $3-5 per application                           │
│ Time: 1-3 hours                                       │
└───────────┬───────────────────────────────────────────┘
            ▼
┌───────────────────────────────────────────────────────┐
│ Phase 2: Traditional Tool Specialization             │
│ - Burp Suite: Advanced XSS, CSRF testing             │
│ - SQLMap: Blind SQLI with time-based inference       │
│ - Nikto: Server misconfigurations                    │
│ Cost: License + 2-4 analyst hours                    │
│ Time: 4-8 hours                                       │
└───────────┬───────────────────────────────────────────┘
            ▼
┌───────────────────────────────────────────────────────┐
│ Phase 3: Human Expert Analysis                        │
│ - Business logic vulnerabilities                      │
│ - Complex authorization flaws                         │
│ - Creative attack scenarios                           │
│ Cost: 8-16 analyst hours                             │
│ Time: 1-2 days                                        │
└───────────────────────────────────────────────────────┘

Total: Comprehensive coverage with optimized resource allocation
```

---

## 7. Research Paper Insights & Academic Approach

### 7.1 Publication Details

**Title:** Multi-Agent Penetration Testing AI for the Web
**Authors:** Isaac David, Arthur Gervais
**Institution:** University College London (UCL)
**Publication:** arXiv:2508.20816
**Date:** August 28, 2025
**Repository:** https://github.com/arthurgervais/mapta

### 7.2 Research Contributions

#### **1. First Open-Source Multi-Agent Pentest AI**
- No prior open-source autonomous pentest systems at comparable capability
- Commercial alternatives exist but lack transparency and reproducibility
- MAPTA achieves competitive performance (within 7.7% of commercial systems)

#### **2. Comprehensive Cost-Performance Analysis**
**Novel Methodology:**
- Complete token-level accounting across all 104 XBOW challenges
- Per-challenge cost breakdown ($0.073 success vs $0.357 failure)
- Total evaluation cost: $21.38
- Resource efficiency correlation with success rates

**Previous Gap:** Prior AI security research lacked rigorous cost analysis

#### **3. End-to-End PoC Validation Framework**
**Innovation:** Mandatory concrete exploitation verification
- Eliminates theoretical-only vulnerability reports
- Reduces false positives through empirical validation
- Provides actionable security intelligence

**Previous Gap:** Traditional AI approaches reported theoretical vulnerabilities without validation

#### **4. Real-World Vulnerability Discovery**
**Research Impact:**
- 19 vulnerabilities discovered in popular open-source projects (8K-70K stars)
- 14 severe findings: RCE, command injection, secret exposure, arbitrary file writes
- 10 CVEs under review
- Responsible disclosure completed

**Practical Validation:** MAPTA's effectiveness extends beyond benchmarks to real-world impact

#### **5. Reproducible Benchmark Methodology**
**Contributions:**
- Evaluated on XBOW benchmark (104 challenges, diverse vulnerability types)
- Fixed 43 outdated XBOW Docker images (provided to community)
- Published complete evaluation logs and exploit scripts
- Enabled scientific reproducibility in security research

### 7.3 Academic Rigor

#### **Evaluation Methodology**

**Blackbox Testing:**
- No source code access during XBOW evaluation
- Only target URLs and challenge descriptions provided
- Simulates external attacker perspective

**Whitebox Validation:**
- Source code review for real-world project assessments
- Verified exploitability with application maintainers
- Responsible disclosure process

**Statistical Analysis:**
- Success rate: 76.9% (80/104 challenges)
- Per-vulnerability-type performance breakdown
- Cost-performance correlation analysis
- Resource efficiency metrics

#### **Comparative Evaluation**

**Baseline Comparison:**
- XBOW commercial system: 84.6% success
- MAPTA: 76.9% success (7.7% gap)
- Performance gap primarily in blind SQLI and complex XSS

**Traditional Tool Comparison:**
- Traditional DAST: 40-60% success (high false positives)
- MAPTA: 76.9% success (low false positives)
- Cost: Traditional ($500-$2000 per scan) vs MAPTA ($3.67 per assessment)

### 7.4 Research Limitations Acknowledged

**Transparency in Limitations:**

1. **Blind SQL Injection:** 0% success rate
   - Issue: Timing-based inference requires explicit methodology
   - Future work: Time-based payload generation and analysis

2. **Cross-Site Scripting:** 57% success (lower than SQLI)
   - Issue: Context-dependent encoding complexity
   - Future work: Advanced XSS payload generation

3. **Business Logic Vulnerabilities:** Not explicitly tested
   - Issue: Requires deep application semantics understanding
   - Future work: Application workflow modeling

4. **Cost at Scale:** $21.38 for 104 challenges = $0.206 average
   - Open question: Cost scalability for enterprise-scale continuous testing
   - Future work: Cost optimization strategies

### 7.5 Theoretical Framework

#### **Multi-Agent Systems Theory**
Paper draws on established MAS principles:
- **Coordination patterns:** Hierarchical delegation (coordinator → executors)
- **Communication protocols:** Task assignment, result aggregation
- **Distributed problem-solving:** Parallel subtask execution
- **Knowledge sharing:** Shared execution environment

#### **LLM Orchestration Patterns**
Novel application of LLM orchestration:
- **Tool-augmented reasoning:** LLMs select and configure security tools
- **Cognitive offloading:** Context isolation reduces cognitive load
- **Hypothesis-testing loop:** Generate → Test → Validate → Refine


---

**Navigation**: [← Part 1](./01_Framework_Overview.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 3 →](./03_Implementation_Guide.md)
**Part 2 of 3** | Lines 418-834 of original document
