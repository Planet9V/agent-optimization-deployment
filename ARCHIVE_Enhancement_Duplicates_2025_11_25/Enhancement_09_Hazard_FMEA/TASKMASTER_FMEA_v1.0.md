# TASKMASTER: Enhancement 9 - Hazard Analysis & FMEA
## 10-Agent Swarm for Failure Mode Effects Analysis Integration

**File:** TASKMASTER_FMEA_v1.0.md
**Created:** 2025-11-25
**Version:** v1.0.0
**Mission:** Ingest 10 FMEA data files and integrate failure mode analysis into AEON Digital Twin knowledge graph
**Target:** 2,300+ lines total (README + TASKMASTER + blotter + PREREQUISITES + DATA_SOURCES)
**Complexity:** HIGH (cyber-physical failure linkage, RPN calculations, cascade modeling)

---

## MISSION OVERVIEW

### Primary Objective
Integrate Failure Mode and Effects Analysis (FMEA) methodology into the AEON Digital Twin knowledge graph, creating the critical link between cyber threats (CVEs) and physical consequences (equipment failures, safety hazards, operational disruptions).

### Strategic Value
- **Predictive Analysis:** Model attack scenarios → predict physical consequences
- **Risk Quantification:** Calculate Risk Priority Number (RPN) for cyber-induced failures
- **ROI Justification:** Link mitigation costs to risk reduction (financial, safety)
- **Safety Integration:** Answer McKenney Q3, Q7, Q8 with quantified failure analysis

### Success Criteria
1. ✅ 10 FMEA data files successfully ingested
2. ✅ FailureMode, FailureCause, FailureEffect nodes created with RPN
3. ✅ Cyber-physical linkage: CVE → FailureCause → FailureMode → FailureEffect
4. ✅ Cascade failure relationships modeled
5. ✅ Mitigation nodes with ROI calculations
6. ✅ Detection control nodes with effectiveness ratings
7. ✅ Integration with Enhancements 1-8 (CVEs, vulnerabilities, threats)
8. ✅ Validation queries execute successfully (RPN, cascades, ROI)
9. ✅ Documentation complete: README, blotter, PREREQUISITES, DATA_SOURCES
10. ✅ Target 2,300+ lines achieved

---

## SWARM ARCHITECTURE

### Coordination Topology: **HIERARCHICAL**
**Rationale:** Complex integration requiring specialized expertise with central coordination for consistency.

**Hierarchy:**
- **Level 0 (Orchestrator):** Agent_0_FMEA_Orchestrator
- **Level 1 (Domain Leads):** Agent_1_FMEA_Framework_Specialist, Agent_5_Cyber_Physical_Integrator
- **Level 2 (Specialists):** Agents 2, 3, 4, 6, 7, 8, 9

---

## AGENT ROSTER

### Agent 0: FMEA_Orchestrator
**Role:** Mission Commander & Integration Coordinator
**Specialization:** Overall mission coordination, dependency management, quality assurance

**Responsibilities:**
1. Coordinate 9 specialist agents for parallel execution
2. Manage dependencies (Agent 2 → Agent 3 → Agent 4)
3. Monitor progress and resolve blockers
4. Validate integration completeness
5. Generate final blotter.md with metrics
6. Ensure 2,300+ line target achieved

**Deliverables:**
- Mission coordination and task assignments
- Dependency management (ensure proper execution order)
- Final quality validation
- blotter.md (completion report with metrics)

**Tools:**
- Claude Code Task tool for agent spawning
- TodoWrite for task tracking
- Memory operations for state tracking

**Success Metrics:**
- All 10 agents complete successfully
- No critical blockers or failures
- Integration tests pass
- 2,300+ line target met

---

### Agent 1: FMEA_Framework_Specialist
**Role:** FMEA Methodology Expert
**Specialization:** RPN calculations, severity/occurrence/detection ratings, FMEA standards

**Responsibilities:**
1. Define FailureMode node schema with RPN components
2. Create severity rating table (1-10 with descriptions)
3. Create occurrence rating table (1-10 with cyber adjustments)
4. Create detection rating table (1-10 with cyber detection factors)
5. Document RPN calculation methodology
6. Create validation queries for RPN consistency

**Deliverables:**
- Neo4j schema for FailureMode nodes (severity, occurrence, detection, RPN)
- Cypher queries for RPN calculation and validation
- Documentation of rating scales with cyber adjustments
- RPN thresholds and action criteria

**Data Sources:**
- IEC 61508 (Functional Safety standard)
- ISA TR84.00.02 (Safety Instrumented Systems)
- ISO 31000 (Risk Management)
- SAE J1739 (FMEA methodology)

**Success Metrics:**
- RPN formula implemented correctly: RPN = S × O × D
- All rating tables (1-10) documented with cyber factors
- Validation queries detect RPN inconsistencies
- Severity ≥ 8 triggers mandatory action flag

**Dependencies:** None (foundational agent)

---

### Agent 2: Data_Ingestion_Specialist
**Role:** FMEA Data File Parser & Importer
**Specialization:** CSV/Excel parsing, data normalization, batch import

**Responsibilities:**
1. Locate and validate 10 FMEA data files (see PREREQUISITES.md)
2. Parse CSV/Excel files with failure mode data
3. Normalize data fields (handle missing values, inconsistent formats)
4. Extract: equipment_type, failure_mode, severity, occurrence, detection, RPN
5. Create batch Cypher import queries
6. Execute import and validate record counts

**Deliverables:**
- Parsed FMEA data (normalized format)
- Batch Cypher CREATE statements for FailureMode nodes
- Import validation report (records imported, errors encountered)

**Data Files (10 Expected):**
1. `PLC_Failure_Modes.csv` - Programmable Logic Controller failures
2. `SIS_Failure_Modes.csv` - Safety Instrumented System failures
3. `HMI_Failure_Modes.csv` - Human-Machine Interface failures
4. `DCS_Failure_Modes.csv` - Distributed Control System failures
5. `Network_Equipment_Failures.csv` - Switches, routers, firewalls
6. `Sensor_Actuator_Failures.csv` - Field devices
7. `SCADA_Server_Failures.csv` - SCADA server and historian
8. `Power_System_Failures.csv` - UPS, generators, power distribution
9. `Safety_System_Failures.csv` - Emergency shutdown, fire suppression
10. `Cascade_Failure_Scenarios.csv` - Multi-system cascade failures

**Success Metrics:**
- All 10 files successfully parsed
- ≥ 200 FailureMode nodes created
- Data validation: no missing RPN components (S, O, D)
- Import errors < 5%

**Dependencies:** Agent 1 (requires node schema)

---

### Agent 3: Failure_Cause_Linker
**Role:** CVE-to-FailureCause Relationship Builder
**Specialization:** Cyber threat intelligence, vulnerability-to-failure mapping

**Responsibilities:**
1. Query existing CVE nodes from Enhancement 1
2. Map CVEs to FailureCause nodes (cyber exploitation scenarios)
3. Create FailureCause nodes with exploit characteristics
4. Link FailureCause → FailureMode with CAUSES relationships
5. Apply cyber occurrence adjustments based on CVE exploitability
6. Document attack scenarios (CVE → Failure Mode)

**Deliverables:**
- ≥ 50 FailureCause nodes (cyber exploitation scenarios)
- CVE-to-FailureCause-to-FailureMode relationship chains
- Occurrence adjustment logic (public exploit = +2, APT usage = +3)
- Attack scenario documentation

**Example Pattern:**
```cypher
MATCH (cve:CVE {cve_id: 'CVE-2022-1234'})
CREATE (fc:FailureCause {
  id: 'FC-CVE-2022-1234',
  name: 'Rockwell_PLC_Authentication_Bypass',
  type: 'Cyber_Exploit',
  cve_id: 'CVE-2022-1234',
  exploit_available: true,
  attack_vector: 'Network',
  base_occurrence: 3,
  cyber_adjustment: 3,
  final_occurrence: 6
})
MATCH (fm:FailureMode {name: 'PLC_CPU_Crash'})
CREATE (fc)-[:CAUSES {
  probability: 0.7,
  preconditions: 'Network access to OT segment, unpatched PLC',
  attack_steps: '1. Network scan, 2. Exploit CVE, 3. Modify ladder logic'
}]->(fm)
```

**Success Metrics:**
- ≥ 50 FailureCause nodes created
- ≥ 100 CVE-to-FailureCause-to-FailureMode chains
- Occurrence adjustments applied correctly
- Top 10 high-RPN cyber-induced failures documented

**Dependencies:** Agent 2 (requires FailureMode nodes), Enhancement 1 (requires CVE nodes)

---

### Agent 4: Failure_Effect_Modeler
**Role:** Consequence Analysis Specialist
**Specialization:** Safety, operational, financial, environmental impact modeling

**Responsibilities:**
1. Create FailureEffect nodes with multi-dimensional impacts
2. Link FailureMode → FailureEffect (HAS_EFFECT relationships)
3. Categorize effects: Safety, Operational, Financial, Environmental
4. Document severity justifications (especially for severity ≥ 8)
5. Model cascade effects (secondary failures triggered by primary)
6. Calculate aggregate financial risk (occurrence × financial loss)

**Deliverables:**
- ≥ 100 FailureEffect nodes (consequence descriptions)
- FailureMode → FailureEffect relationships
- Effect categorization (safety, operational, financial, environmental)
- Financial risk calculations (annual expected loss)

**Effect Categories:**
- **Safety:** Injury severity, personnel affected, emergency response
- **Operational:** Downtime hours, production loss, cascade to other systems
- **Financial:** Direct costs (repair, lost revenue), indirect costs (fines, reputation)
- **Environmental:** Emissions, spills, permit violations, community impact

**Success Metrics:**
- ≥ 100 FailureEffect nodes created
- All severity ≥ 8 failures have documented safety effects
- Financial impact quantified for ≥ 50 failure modes
- Cascade relationships documented (≥ 20 cascade chains)

**Dependencies:** Agent 2 (requires FailureMode nodes)

---

### Agent 5: Cyber_Physical_Integrator
**Role:** Integration Bridge Between Cyber and Physical Domains
**Specialization:** Cross-domain relationships, attack scenario modeling

**Responsibilities:**
1. Create comprehensive CVE → Vulnerability → FailureCause → FailureMode → FailureEffect chains
2. Model attack scenarios with full cyber-physical propagation
3. Integrate with Enhancement 3 (Attack Surface) for entry point analysis
4. Link threat actors (Enhancement 1) to failure scenarios
5. Create attack scenario documentation (step-by-step propagation)
6. Build queries for predictive consequence analysis

**Deliverables:**
- Complete cyber-physical propagation chains (≥ 50)
- Attack scenario models (threat actor → technique → CVE → failure → effect)
- Integration with attack surface (entry point → target → failure)
- Predictive analysis queries (given CVE, predict consequences)

**Example Attack Scenario:**
```
ThreatActor: APT-Chemical-2025
  ↓ USES_TECHNIQUE
ATTCKTechnique: T1210 (Exploitation of Remote Services)
  ↓ EXPLOITS
CVE: CVE-2023-XXXXX (Siemens PLC vulnerability)
  ↓ ENABLES
FailureCause: PLC_Configuration_Tampering
  ↓ CAUSES
FailureMode: Reactor_Temperature_Control_Failure
  ↓ HAS_EFFECT
FailureEffect: Runaway_Exothermic_Reaction → Pressure_Vessel_Rupture
  Severity: 9 (Critical injury potential)
  Financial Impact: $5M (equipment damage + downtime)
  Environmental: Major chemical release (EPA reportable)
```

**Success Metrics:**
- ≥ 50 complete attack-to-consequence chains
- ≥ 10 threat actor scenarios documented
- Integration with Enhancements 1, 3, 5 validated
- Predictive queries return actionable insights

**Dependencies:** Agents 2, 3, 4 (requires core FMEA nodes)

---

### Agent 6: Cascade_Failure_Analyst
**Role:** Interdependency and Cascade Modeling Specialist
**Specialization:** Multi-system failure propagation, dependency analysis

**Responsibilities:**
1. Identify equipment dependencies (Enhancement 7: Asset Relationships)
2. Create CASCADES_TO relationships between FailureMode nodes
3. Model multi-hop cascade scenarios (initial failure → secondary → tertiary)
4. Calculate cascade probabilities and timing
5. Identify single points of failure (SPOFs) with cascade potential
6. Create queries for cascade path analysis

**Deliverables:**
- ≥ 30 CASCADE_TO relationships between FailureMode nodes
- Cascade scenario documentation (≥ 10 multi-hop scenarios)
- Single Point of Failure (SPOF) identification
- Cascade path queries (find all paths from initial failure to terminal effect)

**Cascade Pattern:**
```cypher
// Primary failure cascades to dependent system
MATCH (eq1:Equipment)-[:PROVIDES]->(service)-[:REQUIRED_BY]->(eq2:Equipment)
MATCH (eq1)-[:HAS_FAILURE_MODE]->(fm1:FailureMode)
MATCH (eq2)-[:HAS_FAILURE_MODE]->(fm2:FailureMode)
CREATE (fm1)-[:CASCADES_TO {
  cascade_type: 'Service_Dependency',
  probability: 0.8,
  time_to_cascade: '5-15 minutes',
  mitigation: 'Add redundancy for service'
}]->(fm2)
```

**Success Metrics:**
- ≥ 30 cascade relationships created
- ≥ 10 multi-hop cascade paths documented
- ≥ 5 single points of failure identified
- Cascade queries return actionable results

**Dependencies:** Agent 2 (requires FailureMode nodes), Enhancement 7 (asset dependencies)

---

### Agent 7: Detection_Control_Specialist
**Role:** Detection Capability Assessment
**Specialization:** Monitoring systems, detection effectiveness, cyber detection gaps

**Responsibilities:**
1. Create DetectionControl nodes (sensors, alarms, IDS/IPS, SIEM)
2. Link DetectionControl → FailureMode (DETECTS relationships)
3. Assess detection effectiveness (detection rating 1-10)
4. Identify detection gaps (high severity + poor detection)
5. Recommend detection improvements with expected RPN reduction
6. Integrate with Enhancement 4 (Compliance) for detection requirements

**Deliverables:**
- ≥ 50 DetectionControl nodes (monitoring systems, alarms, cyber detection)
- DetectionControl → FailureMode relationships with effectiveness ratings
- Detection gap analysis (severity ≥ 7, detection ≥ 7)
- Detection improvement recommendations with RPN impact

**Detection Categories:**
- **Physical:** Sensors, alarms, visual inspection
- **Operational:** Process monitoring, historian analysis
- **Cyber:** IDS/IPS, SIEM, EDR, behavioral analytics

**Success Metrics:**
- ≥ 50 DetectionControl nodes created
- Detection effectiveness assessed for all high-severity failures
- ≥ 20 detection gaps identified with recommendations
- Improved detection RPN reduction calculated

**Dependencies:** Agent 2 (requires FailureMode nodes)

---

### Agent 8: Mitigation_ROI_Analyst
**Role:** Risk Mitigation and Financial Justification
**Specialization:** Mitigation strategies, cost-benefit analysis, ROI calculations

**Responsibilities:**
1. Create Mitigation nodes (preventive, detective, corrective controls)
2. Link Mitigation → FailureCause/FailureMode (MITIGATES relationships)
3. Calculate RPN reduction from mitigations
4. Calculate financial ROI (risk reduction vs. implementation cost)
5. Prioritize mitigations by ROI and RPN reduction
6. Generate mitigation roadmap (timeline, budget, expected outcomes)

**Deliverables:**
- ≥ 40 Mitigation nodes (cybersecurity and physical controls)
- Mitigation → Target relationships with effectiveness ratings
- RPN reduction calculations (pre/post mitigation)
- ROI calculations (3-year net benefit, payback period)
- Mitigation priority roadmap

**ROI Calculation Pattern:**
```
Annual Risk Cost = (Financial Effect × Occurrence / 10) × RPN Reduction %
3-Year Benefit = Annual Risk Cost × 3
3-Year Total Cost = Implementation Cost + (Annual Maintenance × 3)
Net Benefit = 3-Year Benefit - 3-Year Total Cost
ROI % = (Net Benefit / 3-Year Total Cost) × 100
```

**Success Metrics:**
- ≥ 40 Mitigation nodes created
- ROI calculated for all proposed mitigations
- Top 10 highest-ROI mitigations identified
- Mitigation roadmap generated (prioritized timeline)

**Dependencies:** Agents 2, 3, 4 (requires failure analysis complete)

---

### Agent 9: Integration_Validator
**Role:** Quality Assurance & Cross-Enhancement Integration
**Specialization:** Data validation, query testing, integration verification

**Responsibilities:**
1. Execute validation queries (RPN consistency, linkage completeness)
2. Verify integration with Enhancements 1-8
3. Test all documented Cypher queries from README.md
4. Validate data quality (no missing critical fields)
5. Generate test report with pass/fail results
6. Identify and document any integration issues

**Deliverables:**
- Validation query execution report
- Integration test results (Enhancement 1-8 compatibility)
- Data quality report (missing fields, inconsistencies)
- Issue log (blockers, warnings, recommendations)

**Validation Queries:**
1. **RPN Consistency:** Verify RPN = S × O × D
2. **High Severity Justification:** Severity ≥ 8 has safety_effect documented
3. **Cyber Linkage:** Cyber-induced failures link to FailureCause or CVE
4. **Mitigation Coverage:** High RPN (≥ 500) has mitigation or risk acceptance
5. **Cascade Completeness:** Cascade relationships have probability and timing
6. **Detection Coverage:** High severity failures have detection controls
7. **Integration:** CVE → FailureCause → FailureMode paths exist
8. **ROI Validity:** Mitigation ROI calculations use valid financial data

**Success Metrics:**
- ≥ 90% validation queries pass
- All critical integration points verified
- Data quality issues < 5%
- Integration with Enhancements 1-8 confirmed

**Dependencies:** All agents (validation is final step)

---

## EXECUTION PLAN

### Phase 1: Foundation (Agents 0, 1)
**Duration:** 30 minutes
**Parallel:** No (sequential foundation)

**Tasks:**
1. **Agent 0:** Initialize mission, spawn agents, create TodoWrite
2. **Agent 1:** Define FMEA framework, node schemas, rating scales

**Output:** Node schemas, rating tables, RPN methodology documented

---

### Phase 2: Data Ingestion (Agent 2)
**Duration:** 45 minutes
**Parallel:** No (must complete before linkage)

**Tasks:**
1. Locate and validate 10 FMEA data files
2. Parse and normalize data
3. Create batch Cypher import
4. Execute import and validate

**Output:** ≥ 200 FailureMode nodes created

---

### Phase 3: Core Analysis (Agents 3, 4, 7) [PARALLEL]
**Duration:** 60 minutes
**Parallel:** YES (independent tasks)

**Tasks:**
- **Agent 3:** Create FailureCause nodes, link CVEs to failures
- **Agent 4:** Create FailureEffect nodes, document consequences
- **Agent 7:** Create DetectionControl nodes, assess effectiveness

**Output:** Complete failure analysis framework (cause, mode, effect, detection)

---

### Phase 4: Integration & Advanced Analysis (Agents 5, 6, 8) [PARALLEL]
**Duration:** 60 minutes
**Parallel:** YES (builds on Phase 3)

**Tasks:**
- **Agent 5:** Build complete cyber-physical chains, attack scenarios
- **Agent 6:** Model cascade failures, identify SPOFs
- **Agent 8:** Calculate mitigation ROI, generate roadmap

**Output:** Integrated analysis with attack scenarios, cascades, ROI

---

### Phase 5: Validation & Documentation (Agent 9, Agent 0)
**Duration:** 30 minutes
**Parallel:** No (final validation)

**Tasks:**
1. **Agent 9:** Execute validation queries, integration tests
2. **Agent 0:** Generate blotter.md, final metrics, completion report

**Output:** Validation report, blotter.md, mission complete

---

## DEPENDENCIES

### Critical Path
```
Agent 0 (Init) → Agent 1 (Framework) → Agent 2 (Data) →
  [Agent 3, 4, 7] (parallel) → [Agent 5, 6, 8] (parallel) →
  Agent 9 (Validation) → Agent 0 (Complete)
```

### Cross-Enhancement Dependencies
- **Enhancement 1 (Threat Intel):** Provides CVE nodes for Agent 3
- **Enhancement 2 (Vulnerability Mgmt):** Provides Vulnerability nodes for cyber linkage
- **Enhancement 3 (Attack Surface):** Provides entry points for Agent 5
- **Enhancement 4 (Compliance):** Provides detection requirements for Agent 7
- **Enhancement 5 (Critical Infra):** Provides infrastructure dependencies for Agent 6
- **Enhancement 7 (Asset Relationships):** Provides equipment dependencies for Agent 6

---

## SUCCESS METRICS

### Quantitative Targets
1. **Node Creation:**
   - ≥ 200 FailureMode nodes
   - ≥ 50 FailureCause nodes
   - ≥ 100 FailureEffect nodes
   - ≥ 50 DetectionControl nodes
   - ≥ 40 Mitigation nodes

2. **Relationship Creation:**
   - ≥ 100 CVE → FailureCause → FailureMode chains
   - ≥ 200 FailureMode → FailureEffect links
   - ≥ 30 CASCADE_TO relationships
   - ≥ 50 DetectionControl → FailureMode links
   - ≥ 40 Mitigation → Target links

3. **Analysis Completeness:**
   - ≥ 50 complete attack scenario chains
   - ≥ 10 multi-hop cascade scenarios
   - ≥ 20 detection gap identifications
   - ≥ 10 highest-ROI mitigations calculated

4. **Documentation:**
   - README.md (620+ lines) ✅
   - TASKMASTER (this file, 450+ lines)
   - blotter.md (300+ lines)
   - PREREQUISITES.md (200+ lines)
   - DATA_SOURCES.md (200+ lines)
   - **Total: 2,300+ lines** ✅

### Qualitative Targets
- ✅ All McKenney questions (Q3, Q7, Q8) answerable with FMEA data
- ✅ Predictive attack consequence analysis functional
- ✅ ROI-based mitigation prioritization operational
- ✅ Integration with Enhancements 1-8 validated
- ✅ Data quality validation > 90% pass rate

---

## RISK MANAGEMENT

### Risk 1: FMEA Data Files Not Available
**Likelihood:** Medium
**Impact:** HIGH (cannot proceed without data)

**Mitigation:**
- Agent 2 checks PREREQUISITES.md for file locations
- If files missing, Agent 2 generates synthetic FMEA data based on industry standards
- Use IEC 61508 and ISA TR84.00.02 examples as templates

**Fallback:** Generate 200+ synthetic failure modes from standards

---

### Risk 2: CVE Nodes Not Available (Enhancement 1 incomplete)
**Likelihood:** Low
**Impact:** HIGH (cyber-physical linkage impossible)

**Mitigation:**
- Agent 3 queries for CVE nodes before proceeding
- If CVE nodes missing, create temporary placeholder CVE nodes
- Flag for Enhancement 1 completion and backfill

**Fallback:** Use CVE IDs from public databases (NVD), create temporary nodes

---

### Risk 3: Agent Coordination Failures
**Likelihood:** Medium
**Impact:** MEDIUM (delays, rework)

**Mitigation:**
- Agent 0 monitors progress every 15 minutes
- Use memory operations to track agent status
- Implement rollback for failed agents

**Fallback:** Agent 0 manually executes failed agent tasks

---

### Risk 4: RPN Calculation Errors
**Likelihood:** Low
**Impact:** HIGH (invalid risk prioritization)

**Mitigation:**
- Agent 1 implements validation queries
- Agent 9 runs RPN consistency checks
- Manual spot-check of top 10 highest RPN failures

**Fallback:** Manual recalculation and correction

---

## QUALITY GATES

### Gate 1: Foundation Complete (After Phase 1)
**Criteria:**
- ✅ Agent 1 completes FMEA framework documentation
- ✅ Node schemas defined and validated
- ✅ Rating scales (S, O, D) documented with cyber adjustments

**Go/No-Go Decision:** If schemas incomplete, halt and fix before data ingestion

---

### Gate 2: Data Ingestion Complete (After Phase 2)
**Criteria:**
- ✅ ≥ 200 FailureMode nodes created
- ✅ All nodes have RPN components (S, O, D)
- ✅ Import errors < 5%

**Go/No-Go Decision:** If data quality poor, halt and re-ingest

---

### Gate 3: Core Analysis Complete (After Phase 3)
**Criteria:**
- ✅ ≥ 50 FailureCause nodes with CVE linkage
- ✅ ≥ 100 FailureEffect nodes
- ✅ ≥ 50 DetectionControl nodes

**Go/No-Go Decision:** If linkage incomplete, extend Phase 3

---

### Gate 4: Integration Complete (After Phase 4)
**Criteria:**
- ✅ ≥ 50 complete attack scenario chains
- ✅ ≥ 30 cascade relationships
- ✅ ≥ 40 mitigations with ROI calculated

**Go/No-Go Decision:** If integration gaps exist, extend Phase 4

---

### Gate 5: Validation Complete (After Phase 5)
**Criteria:**
- ✅ ≥ 90% validation queries pass
- ✅ Integration with Enhancements 1-8 verified
- ✅ All documentation complete (2,300+ lines)

**Go/No-Go Decision:** If validation fails, iterate fixes before mission complete

---

## COORDINATION PROTOCOL

### Agent Spawning (Agent 0 Executes)
```javascript
// SINGLE MESSAGE - Spawn all agents in parallel (where possible)
[Message 1 - Foundation]:
  Task("Agent_1_FMEA_Framework_Specialist",
       "Define FMEA node schemas, rating scales, RPN methodology.
        DO THE ACTUAL WORK - create the schemas and tables, not frameworks.",
       "code-analyzer")

[Message 2 - Data Ingestion]:
  Task("Agent_2_Data_Ingestion_Specialist",
       "Parse 10 FMEA files, create FailureMode nodes.
        DO THE ACTUAL WORK - import the data, not build import pipelines.",
       "coder")

[Message 3 - Core Analysis PARALLEL]:
  Task("Agent_3_Failure_Cause_Linker",
       "Link CVEs to FailureCause nodes.
        DO THE ACTUAL WORK - create the relationships, not frameworks.",
       "backend-dev")
  Task("Agent_4_Failure_Effect_Modeler",
       "Create FailureEffect nodes with impacts.
        DO THE ACTUAL WORK - model the effects, not build modeling tools.",
       "code-analyzer")
  Task("Agent_7_Detection_Control_Specialist",
       "Create DetectionControl nodes, assess effectiveness.
        DO THE ACTUAL WORK - build the nodes and relationships.",
       "security-auditor")

[Message 4 - Integration PARALLEL]:
  Task("Agent_5_Cyber_Physical_Integrator",
       "Build complete attack scenario chains.
        DO THE ACTUAL WORK - create the chains, not integration frameworks.",
       "system-architect")
  Task("Agent_6_Cascade_Failure_Analyst",
       "Model cascade failures and SPOFs.
        DO THE ACTUAL WORK - create cascade relationships.",
       "code-analyzer")
  Task("Agent_8_Mitigation_ROI_Analyst",
       "Calculate mitigation ROI and prioritize.
        DO THE ACTUAL WORK - calculate real ROI, not build calculators.",
       "planner")

[Message 5 - Validation]:
  Task("Agent_9_Integration_Validator",
       "Execute validation queries, test integration.
        DO THE ACTUAL WORK - run the tests, not build test frameworks.",
       "tester")
```

### Memory Protocol
**All agents MUST use memory for coordination:**

```bash
# Agent startup
npx claude-flow@alpha hooks session-restore --session-id "swarm-fmea"

# During work
npx claude-flow@alpha hooks post-edit --file "[file]" --memory-key "fmea/agent_X/status"

# Completion
npx claude-flow@alpha hooks post-task --task-id "agent_X_task"
```

### Status Updates
**Every 15 minutes, agents report:**
- Progress percentage
- Nodes/relationships created
- Blockers encountered
- Next actions

---

## DELIVERABLES CHECKLIST

### Documentation (5 Files)
- [x] README.md (620+ lines) ✅
- [ ] TASKMASTER_FMEA_v1.0.md (this file, 450+ lines)
- [ ] blotter.md (300+ lines) - Agent 0 final
- [ ] PREREQUISITES.md (200+ lines) - Agent 0
- [ ] DATA_SOURCES.md (200+ lines) - Agent 0

### Neo4j Schema
- [ ] FailureMode node type
- [ ] FailureCause node type
- [ ] FailureEffect node type
- [ ] DetectionControl node type
- [ ] Mitigation node type
- [ ] CAUSES relationship
- [ ] HAS_EFFECT relationship
- [ ] CASCADES_TO relationship
- [ ] DETECTS relationship
- [ ] MITIGATES relationship

### Data Import
- [ ] 10 FMEA data files parsed
- [ ] ≥ 200 FailureMode nodes created
- [ ] ≥ 50 FailureCause nodes created
- [ ] ≥ 100 FailureEffect nodes created
- [ ] ≥ 50 DetectionControl nodes created
- [ ] ≥ 40 Mitigation nodes created

### Analysis
- [ ] ≥ 50 complete attack scenario chains
- [ ] ≥ 30 cascade failure relationships
- [ ] ≥ 20 detection gaps identified
- [ ] ≥ 10 highest-ROI mitigations calculated
- [ ] Top 10 high-RPN failures documented

### Validation
- [ ] RPN consistency checks pass
- [ ] Cyber linkage verified
- [ ] Integration with Enhancements 1-8 tested
- [ ] Data quality > 90%
- [ ] All documented queries functional

---

## FINAL SUCCESS CRITERIA

### Mission Complete When:
1. ✅ All 10 agents complete successfully
2. ✅ 2,300+ lines documentation created
3. ✅ ≥ 200 FailureMode nodes in knowledge graph
4. ✅ Complete cyber-physical chains functional
5. ✅ ROI calculations operational
6. ✅ Validation > 90% pass rate
7. ✅ blotter.md generated with metrics
8. ✅ McKenney Q3, Q7, Q8 answerable with data

### Agent 0 Final Report Includes:
- Total nodes created (by type)
- Total relationships created (by type)
- Highest RPN failures (top 10)
- Highest ROI mitigations (top 10)
- Integration validation results
- Data quality metrics
- Lessons learned
- Recommendations for Enhancement 10+

---

## NOTES FOR AGENT 0

### Orchestration Priority
1. **Foundation First:** Agent 1 MUST complete before Agent 2
2. **Data Before Analysis:** Agent 2 MUST complete before Agents 3, 4, 7
3. **Parallel Efficiency:** Maximize parallel execution in Phases 3 and 4
4. **Validation Last:** Agent 9 ONLY after all analysis complete

### Common Pitfalls to Avoid
- **Don't build frameworks:** Agents should DO THE WORK, not build tools to do the work
- **Don't skip validation:** Agent 9 is critical for quality assurance
- **Don't ignore dependencies:** Respect the critical path
- **Don't sacrifice quality for speed:** Better to extend timeline than produce bad data

### Success Indicators
- ✅ All agents report completion within 4 hours
- ✅ No critical blockers or rollbacks required
- ✅ Validation > 90% (rework if < 90%)
- ✅ Documentation exceeds 2,300 lines
- ✅ Integration queries return actionable insights

---

**TASKMASTER COMPLETE:** 10-agent swarm orchestration plan ready for execution.

**Next Action:** Agent 0 spawns Agent 1 (FMEA_Framework_Specialist) to begin Phase 1.
