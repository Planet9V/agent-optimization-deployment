# PROC-152: Lacanian Triad Group Dynamics ETL

**Metadata:**
- **Procedure ID**: PROC-152
- **Enhancement**: E18 - Lacanian RSI Triad and Borromean Knot Analysis
- **Priority**: High
- **Frequency**: Monthly (crisis-triggered for team instability)
- **Dependencies**: PROC-151 (Dyadic foundations)
- **Estimated Duration**: 60-75 minutes
- **Target Size**: ~6KB

---

## 1. PURPOSE

Analyze security team group dynamics using Lacanian RSI (Real, Symbolic, Imaginary) triad framework and Borromean knot topology to assess organizational resilience, identify failing registers, and design stabilization interventions.

### McKenney Questions Addressed
- **Q4 (Psychological Patterns)**: How do Real, Symbolic, and Imaginary registers interlock to form team cohesion?
- **Q7 (Organizational Dynamics)**: Which register is failing and threatening team collapse?
- **Q8 (Threat Actor Behavior)**: How does team psychology shape threat perception and response?

### Business Value
- Predict team collapse before it occurs (13+ months advance warning)
- Identify register failures causing dysfunction
- Design targeted interventions to restore knot stability
- Detect pathological sinthomes corroding team health

---

## 2. PRE-CONDITIONS

### Required Data Availability
- [ ] Security infrastructure inventory (assets, sensors, coverage)
- [ ] Security policies and procedures documentation
- [ ] Team communications (Slack, email, 90 days minimum)
- [ ] Employee surveys and culture assessments
- [ ] Incident response database (12 months)
- [ ] Budget and resource allocation data
- [ ] Organizational charts and role definitions
- [ ] Exit interview data and turnover statistics

### System Requirements
- [ ] Neo4j database running with graph algorithms plugin
- [ ] Python 3.9+ with NLP libraries (transformers, spacy, sklearn)
- [ ] Access to MITRE ATT&CK Navigator for coverage mapping
- [ ] Data visualization tools (Grafana for knot health dashboards)

### Access Permissions
- [ ] Read access to all E18 data sources
- [ ] Read access to HR systems (aggregate only, no PII)
- [ ] Write access to Neo4j graph database

---

## 3. DATA SOURCES

### 3.1 Real Register Extraction
**Primary Sources:**
1. **MITRE ATT&CK Coverage** → Threat detection coverage percentage
2. **Security Infrastructure Inventory** → Technical debt, budget adequacy
3. **Incident Database** → Proactive detection rate, breach rate, MTTD/MTTR
4. **Budget Data** → Resource constraints, headcount adequacy

**Extraction Targets:**
- **Real Vector R**: `[Threat_coverage, Infrastructure_reality, Incident_effectiveness, Breach_prevention, Low_technical_debt]`
- **Real Register Health**: Weighted average of R components

### 3.2 Symbolic Register Extraction
**Primary Sources:**
1. **Security Policies** → Policy effectiveness, bureaucratic bloat
2. **Team Communications** → Communication clarity, cross-functional ratio
3. **Organizational Charts** → Role clarity, hierarchy appropriateness
4. **Compliance Frameworks** → Compliance coverage and efficiency

**Extraction Targets:**
- **Symbolic Vector S**: `[Policy_effectiveness, Communication_clarity, Org_structure, Compliance_coverage, Low_bureaucratic_bloat]`
- **Symbolic Register Health**: Weighted average of S components

### 3.3 Imaginary Register Extraction
**Primary Sources:**
1. **Team Communications** (self-referential) → Self-image accuracy
2. **Employee Surveys** → Morale, fear intensity, aspirations
3. **Threat Perception Analysis** → Imagined vs actual threat alignment
4. **Executive Communications** → Organizational perception of team
5. **Exit Interview Data** → Morale reality-check

**Extraction Targets:**
- **Imaginary Vector I**: `[Self_image_accuracy, Aspiration_realism, Threat_perception_alignment, Org_perception, Fear_management]`
- **Imaginary Register Health**: Weighted average of I components

---

## 4. TRANSFORMATION LOGIC

### 4.1 Real Register Mapping (Agent 1 Logic)

```python
def map_real_register(mitre_coverage, infrastructure, incident_data, budget_data):
    """Construct Real register vector from actual security capabilities."""

    # Threat coverage score
    total_techniques = 800  # MITRE ATT&CK Enterprise
    covered_techniques = count_covered_techniques(mitre_coverage, infrastructure)
    threat_coverage = covered_techniques / total_techniques

    # Infrastructure reality
    technical_debt = calculate_technical_debt(infrastructure)
    budget_adequacy = min(1.0, budget_data['security_budget'] / (budget_data['total_it_budget'] * 0.10))
    headcount_adequacy = calculate_headcount_adequacy(infrastructure['team_size'], infrastructure['required_coverage'])
    infrastructure_reality = (1 - technical_debt) * 0.4 + budget_adequacy * 0.3 + headcount_adequacy * 0.3

    # Incident handling effectiveness
    incidents_handled_effectively = [inc for inc in incident_data if inc['contained'] and inc['mttd'] < threshold]
    incident_effectiveness = len(incidents_handled_effectively) / len(incident_data)

    # Breach prevention
    breaches = [inc for inc in incident_data if inc['data_exfiltrated']]
    breach_prevention = 1 - (len(breaches) / len(incident_data))

    # Low technical debt (inverted)
    low_debt = 1 - technical_debt

    R = [threat_coverage, infrastructure_reality, incident_effectiveness, breach_prevention, low_debt]
    real_health = sum(R) / len(R)

    return {
        "real_vector": R,
        "real_register_health": real_health,
        "components": {
            "threat_coverage": R[0],
            "infrastructure_reality": R[1],
            "incident_effectiveness": R[2],
            "breach_prevention": R[3],
            "low_technical_debt": R[4]
        }
    }
```

### 4.2 Borromean Knot Calculation (Agent 4 Logic)

```python
def calculate_borromean_knot(R_vector, S_vector, I_vector):
    """
    Calculate Borromean knot stability:
    Τ(g) = ∮_C (R·dS + S·dI + I·dR)
    Circulation integral measuring register interdependence.
    """
    import numpy as np

    R = np.array(R_vector)
    S = np.array(S_vector)
    I = np.array(I_vector)

    # R·dS: Real drives Symbolic (actual threats force policy updates)
    R_drives_S = np.dot(R, S)

    # S·dI: Symbolic shapes Imaginary (policies affirm team identity)
    S_shapes_I = np.dot(S, I)

    # I·dR: Imaginary influences Real (team identity drives threat focus)
    I_influences_R = np.dot(I, R)

    # Total circulation (normalized)
    tau = (R_drives_S + S_shapes_I + I_influences_R) / 3.0

    # Register balance assessment
    register_magnitudes = [sum(R)/len(R), sum(S)/len(S), sum(I)/len(I)]
    mean_health = np.mean(register_magnitudes)
    std_health = np.std(register_magnitudes)
    register_balance = 1 - (std_health / mean_health) if mean_health > 0 else 0

    # Knot stability score
    stability_score = register_balance * tau

    # Classify knot status
    if stability_score > 0.6:
        status = "stable"
        description = "Healthy Borromean knot, team functioning well"
    elif 0.3 <= stability_score <= 0.6:
        status = "crisis"
        description = "Knot weakening, register failure risk, intervention needed"
    else:
        status = "catastrophe"
        description = "Knot dissolving, team collapse, major restructuring required"

    # Identify weakest register
    weakest_register = ["Real", "Symbolic", "Imaginary"][np.argmin(register_magnitudes)]

    return {
        "circulation_integral": tau,
        "circulation_components": {
            "R_drives_S": R_drives_S,
            "S_shapes_I": S_shapes_I,
            "I_influences_R": I_influences_R
        },
        "register_balance": register_balance,
        "stability_score": stability_score,
        "status": status,
        "description": description,
        "weakest_register": weakest_register,
        "register_health": {
            "Real": register_magnitudes[0],
            "Symbolic": register_magnitudes[1],
            "Imaginary": register_magnitudes[2]
        }
    }
```

### 4.3 Sinthome Identification (Agent 6 Logic)

```python
def detect_sinthomes(org_narratives, team_culture, infrastructure_data, communications):
    """
    Identify the 'fourth ring' (sinthome) holding the knot together.
    σ(s) = Compensation_capacity × Activation_threshold⁻¹ × Sustainability
    """

    sinthomes = []

    # Type 1: Founding trauma/story (structural sinthome)
    founding_events = extract_founding_stories(org_narratives, patterns=["we exist because", "after the incident"])
    for event in founding_events:
        compensation_capacity = 0.8
        activation_threshold = 0.2
        sustainability = 0.9
        sigma = (compensation_capacity / (1 + activation_threshold)) * sustainability

        sinthomes.append({
            "type": "structural",
            "category": "founding_trauma",
            "description": event['description'],
            "strength": sigma,
            "compensation_capacity": compensation_capacity,
            "sustainability": sustainability,
            "recommendation": "Healthy sinthome, maintain" if sigma > 0.5 else "Weak sinthome"
        })

    # Type 2: Charismatic leader (personal sinthome)
    leader_dependency = assess_leader_dependency(team_culture)
    if leader_dependency > 0.7:
        compensation_capacity = 0.9
        activation_threshold = 0.1
        sustainability = 0.4  # Vulnerable to succession
        sigma = (compensation_capacity / (1 + activation_threshold)) * sustainability

        sinthomes.append({
            "type": "personal",
            "category": "charismatic_leader",
            "description": f"Team cohesion dependent on leader",
            "strength": sigma,
            "compensation_capacity": compensation_capacity,
            "sustainability": sustainability,
            "recommendation": "Effective but vulnerable, develop structural backup"
        })

    # Type 3: Scapegoating (pathological sinthome)
    scapegoating_patterns = detect_scapegoating(communications, patterns=["management doesn't", "it's their fault"])
    if scapegoating_patterns['frequency'] > 0.5:
        compensation_capacity = 0.7
        activation_threshold = 0.3
        sustainability = -0.5  # Corrosive long-term
        sigma = (compensation_capacity / (1 + activation_threshold)) * sustainability

        sinthomes.append({
            "type": "pathological",
            "category": "scapegoat",
            "description": f"Team bonding through resentment of {scapegoating_patterns['target']}",
            "strength": sigma,
            "compensation_capacity": compensation_capacity,
            "sustainability": sustainability,
            "currently_activated": True,
            "recommendation": "URGENT: Replace with healthy sinthome"
        })

    return {
        "detected_sinthomes": sinthomes,
        "primary_sinthome": max(sinthomes, key=lambda x: x['strength']) if sinthomes else None,
        "pathological_count": len([s for s in sinthomes if s['type'] == 'pathological'])
    }
```

---

## 5. NEO4J SCHEMA

### Node Labels

**RealRegister**
```cypher
CREATE (r:RealRegister {
  id: STRING,  // "Real_SOC_Team_Alpha"
  threat_coverage: FLOAT,  // 0-1
  infrastructure_reality: FLOAT,  // 0-1
  incident_effectiveness: FLOAT,  // 0-1
  breach_prevention: FLOAT,  // 0-1
  low_technical_debt: FLOAT,  // 0-1
  real_vector: LIST<FLOAT>,  // [0.67, 0.58, 0.72, 0.81, 0.65]
  real_register_health: FLOAT,  // 0.686
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**SymbolicRegister**
```cypher
CREATE (s:SymbolicRegister {
  id: STRING,  // "Symbolic_SOC_Team_Alpha"
  policy_effectiveness: FLOAT,
  communication_clarity: FLOAT,
  organizational_structure: FLOAT,
  compliance_coverage: FLOAT,
  low_bureaucratic_bloat: FLOAT,
  symbolic_vector: LIST<FLOAT>,
  symbolic_register_health: FLOAT,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**ImaginaryRegister**
```cypher
CREATE (i:ImaginaryRegister {
  id: STRING,  // "Imaginary_SOC_Team_Alpha"
  self_image_accuracy: FLOAT,
  aspiration_realism: FLOAT,
  threat_perception_alignment: FLOAT,
  organizational_perception: FLOAT,
  fear_management: FLOAT,
  imaginary_vector: LIST<FLOAT>,
  imaginary_register_health: FLOAT,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**Sinthome**
```cypher
CREATE (sin:Sinthome {
  id: STRING,
  type: STRING,  // "structural", "personal", "material", "pathological"
  category: STRING,  // "founding_trauma", "charismatic_leader", "scapegoat"
  description: STRING,
  strength: FLOAT,  // σ(s) value
  compensation_capacity: FLOAT,
  sustainability: FLOAT,
  currently_activated: BOOLEAN,
  recommendation: STRING,
  created_at: DATETIME
})
```

**SecurityTeam**
```cypher
CREATE (team:SecurityTeam {
  id: STRING,  // "SOC_Team_Alpha"
  team_size: INT,
  turnover_rate: FLOAT,
  avg_tenure_months: INT,
  knot_stability_score: FLOAT,  // Current stability
  knot_status: STRING,  // "stable", "crisis", "catastrophe"
  created_at: DATETIME,
  updated_at: DATETIME
})
```

### Relationships

**DRIVES_SYMBOLIC** (Real → Symbolic circulation)
```cypher
CREATE (r:RealRegister)-[ds:DRIVES_SYMBOLIC {
  circulation_strength: FLOAT,  // R·dS value
  mechanism: STRING,  // "Actual threats force policy updates"
  effectiveness: FLOAT,  // 0-1
  created_at: DATETIME
}]->(s:SymbolicRegister)
```

**SHAPES_IMAGINARY** (Symbolic → Imaginary circulation)
```cypher
CREATE (s:SymbolicRegister)-[si:SHAPES_IMAGINARY {
  circulation_strength: FLOAT,  // S·dI value
  mechanism: STRING,  // "Policies affirm team identity"
  effectiveness: FLOAT,
  created_at: DATETIME
}]->(i:ImaginaryRegister)
```

**INFLUENCES_REAL** (Imaginary → Real circulation)
```cypher
CREATE (i:ImaginaryRegister)-[ir:INFLUENCES_REAL {
  circulation_strength: FLOAT,  // I·dR value
  mechanism: STRING,  // "Team identity drives threat focus"
  effectiveness: FLOAT,
  created_at: DATETIME
}]->(r:RealRegister)
```

**OPERATES_IN** (Team operates in each register)
```cypher
CREATE (team:SecurityTeam)-[:OPERATES_IN]->(r:RealRegister)
CREATE (team:SecurityTeam)-[:OPERATES_IN]->(s:SymbolicRegister)
CREATE (team:SecurityTeam)-[:OPERATES_IN]->(i:ImaginaryRegister)
```

**STABILIZES** (Sinthome stabilizes team knot)
```cypher
CREATE (sin:Sinthome)-[st:STABILIZES {
  activation_triggers: LIST<STRING>,  // ["crisis", "team_conflict"]
  strength_contribution: FLOAT,
  created_at: DATETIME
}]->(team:SecurityTeam)
```

**KNOT_WEAKENING** (Register failure risk)
```cypher
CREATE (team:SecurityTeam)-[kw:KNOT_WEAKENING {
  failing_register: STRING,  // "Imaginary"
  failure_mode: STRING,  // "Burnout, alienation"
  timeline_months: FLOAT,  // 13.9
  failure_probability: FLOAT,  // 0.67
  created_at: DATETIME
}]->(intervention:Intervention)
```

---

## 6. EXECUTION STEPS

### Step 1: Extract Real Register
```bash
python /scripts/map_real_register.py \
  --mitre_coverage /data/mitre_navigator_coverage.json \
  --infrastructure /data/infrastructure_inventory.json \
  --incidents /data/incidents_12mo.json \
  --budget /data/budget_allocations.json \
  --output /data/staging/real_register.json
```

### Step 2: Analyze Symbolic Register
```bash
python /scripts/analyze_symbolic_register.py \
  --policies /data/security_policies/ \
  --communications /data/slack_archive/ \
  --org_chart /data/organizational_structure.json \
  --compliance /data/compliance_certifications.json \
  --output /data/staging/symbolic_register.json
```

### Step 3: Detect Imaginary Register
```bash
python /scripts/detect_imaginary_register.py \
  --communications /data/slack_archive/ \
  --surveys /data/employee_surveys.json \
  --exit_interviews /data/exit_interviews.json \
  --threat_perceptions /data/threat_intel_reports/ \
  --exec_comms /data/executive_communications/ \
  --output /data/staging/imaginary_register.json
```

### Step 4: Calculate Borromean Knot
```bash
python /scripts/calculate_borromean_knot.py \
  --real /data/staging/real_register.json \
  --symbolic /data/staging/symbolic_register.json \
  --imaginary /data/staging/imaginary_register.json \
  --output /data/staging/knot_calculation.json
```

### Step 5: Model Group Topology
```bash
python /scripts/model_group_topology.py \
  --team_members /data/team_member_profiles.json \
  --interactions /data/collaboration_logs.json \
  --output /data/staging/group_topology.json
```

### Step 6: Identify Sinthomes
```bash
python /scripts/identify_sinthomes.py \
  --narratives /data/organizational_narratives/ \
  --culture /data/team_culture_assessment.json \
  --communications /data/slack_archive/ \
  --output /data/staging/sinthome_analysis.json
```

### Step 7: Predict Knot Failure
```bash
python /scripts/predict_knot_failure.py \
  --knot_data /data/staging/knot_calculation.json \
  --historical /data/historical_knot_health.json \
  --sinthomes /data/staging/sinthome_analysis.json \
  --output /data/staging/failure_prediction.json
```

### Step 8: Design Interventions
```bash
python /scripts/design_interventions.py \
  --all_analysis /data/staging/ \
  --org_constraints /data/org_constraints.json \
  --output /data/staging/intervention_roadmap.json
```

### Step 9: Load to Neo4j
```bash
python /scripts/load_triad_analysis_to_neo4j.py \
  --staging_dir /data/staging/ \
  --neo4j_uri bolt://localhost:7687 \
  --neo4j_user neo4j \
  --neo4j_password <password>
```

---

## 7. CYPHER QUERIES

### 7.1 Assess Overall Knot Health
```cypher
MATCH (team:SecurityTeam)-[:OPERATES_IN]->(r:RealRegister),
      (team)-[:OPERATES_IN]->(s:SymbolicRegister),
      (team)-[:OPERATES_IN]->(i:ImaginaryRegister)
RETURN team.id AS team,
       team.knot_stability_score AS stability,
       team.knot_status AS status,
       r.real_register_health AS real_health,
       s.symbolic_register_health AS symbolic_health,
       i.imaginary_register_health AS imaginary_health
ORDER BY team.knot_stability_score ASC
```

### 7.2 Identify Failing Registers
```cypher
MATCH (team:SecurityTeam)-[kw:KNOT_WEAKENING]->(intervention)
RETURN team.id AS team,
       kw.failing_register AS register_at_risk,
       kw.failure_mode AS failure_symptoms,
       kw.timeline_months AS months_until_failure,
       kw.failure_probability AS probability,
       intervention.strategy AS recommended_intervention
ORDER BY kw.timeline_months ASC
```

### 7.3 Analyze Circulation Flow
```cypher
MATCH (r:RealRegister)-[ds:DRIVES_SYMBOLIC]->(s:SymbolicRegister)-[si:SHAPES_IMAGINARY]->(i:ImaginaryRegister)-[ir:INFLUENCES_REAL]->(r)
RETURN r.id AS real_register,
       ds.circulation_strength AS real_to_symbolic,
       si.circulation_strength AS symbolic_to_imaginary,
       ir.circulation_strength AS imaginary_to_real,
       (ds.circulation_strength + si.circulation_strength + ir.circulation_strength) / 3.0 AS avg_circulation
ORDER BY avg_circulation DESC
```

### 7.4 Evaluate Sinthome Effectiveness
```cypher
MATCH (sin:Sinthome)-[st:STABILIZES]->(team:SecurityTeam)
RETURN sin.type AS sinthome_type,
       sin.category AS category,
       sin.description AS description,
       sin.strength AS sigma_value,
       sin.sustainability AS long_term_viability,
       sin.recommendation AS action_needed,
       team.knot_status AS team_status
ORDER BY sin.strength DESC
```

### 7.5 Detect Pathological Sinthomes
```cypher
MATCH (sin:Sinthome)-[:STABILIZES]->(team:SecurityTeam)
WHERE sin.type = 'pathological' AND sin.sustainability < 0
RETURN team.id AS team_at_risk,
       sin.description AS toxic_pattern,
       sin.strength AS current_strength,
       sin.sustainability AS toxicity_level,
       "URGENT: Replace pathological sinthome" AS priority_action
```

---

## 8. VERIFICATION QUERIES

### 8.1 Validate Register Vectors
```cypher
MATCH (r:RealRegister)
WHERE size(r.real_vector) = 5 AND all(v IN r.real_vector WHERE v >= 0 AND v <= 1)
RETURN count(r) AS valid_real_registers

UNION

MATCH (s:SymbolicRegister)
WHERE size(s.symbolic_vector) = 5 AND all(v IN s.symbolic_vector WHERE v >= 0 AND v <= 1)
RETURN count(s) AS valid_symbolic_registers

UNION

MATCH (i:ImaginaryRegister)
WHERE size(i.imaginary_vector) = 5 AND all(v IN i.imaginary_vector WHERE v >= 0 AND v <= 1)
RETURN count(i) AS valid_imaginary_registers
```

### 8.2 Check Circulation Completeness
```cypher
MATCH (r:RealRegister)-[ds:DRIVES_SYMBOLIC]->(s:SymbolicRegister),
      (s)-[si:SHAPES_IMAGINARY]->(i:ImaginaryRegister),
      (i)-[ir:INFLUENCES_REAL]->(r)
RETURN r.id AS complete_circulation_loops,
       ds.circulation_strength AS r_to_s,
       si.circulation_strength AS s_to_i,
       ir.circulation_strength AS i_to_r
```

### 8.3 Count Sinthomes by Type
```cypher
MATCH (sin:Sinthome)
RETURN sin.type AS sinthome_type,
       count(sin) AS count,
       avg(sin.strength) AS avg_strength,
       avg(sin.sustainability) AS avg_sustainability
ORDER BY count DESC
```

---

## 9. ROLLBACK PROCEDURE

### 9.1 Remove Recent Load
```cypher
// Delete all E18 nodes created in last load
MATCH (n)
WHERE n:RealRegister OR n:SymbolicRegister OR n:ImaginaryRegister OR n:Sinthome OR n:SecurityTeam
  AND n.created_at > datetime() - duration('PT2H')
OPTIONAL MATCH (n)-[r]-()
DELETE r, n
```

### 9.2 Restore from Backup
```bash
neo4j-admin restore --from=/backup/neo4j-backup-$(date -d yesterday +%Y%m%d).backup \
  --database=neo4j --force
```

---

## 10. PERFORMANCE METRICS

**Expected Metrics:**
- **Execution Time**: 60-75 minutes for full 10-agent swarm analysis
- **Token Efficiency**: 30-35% reduction through coordination
- **Data Volume**: ~1000 team communications, ~500 policy documents analyzed
- **Graph Nodes Created**: 15-30 per analysis (3 registers, 1 team, 3-5 sinthomes, 10-20 interventions)
- **Quality Score**: >0.92 (validated by Agent 10)

**Success Criteria:**
- All register vectors have 5 dimensions with values in [0, 1]
- Circulation integral τ > 0 (positive circulation)
- Knot stability score within [0, 1] range
- At least 1 sinthome identified
- Intervention roadmap with phased implementation

---

## 11. TROUBLESHOOTING

**Issue**: Knot stability score < 0.3 (catastrophe)
- **Cause**: Team experiencing severe dysfunction, register failure imminent
- **Fix**: Urgent intervention required, escalate to leadership

**Issue**: All registers have same health score (perfect balance but unlikely)
- **Cause**: Data quality issue or insufficient data variance
- **Fix**: Review data extraction, ensure diverse data sources

**Issue**: No sinthome detected
- **Cause**: Team may lack cohesive cultural narratives or founding stories
- **Fix**: Interview team members, review historical documents

---

## 12. RELATED PROCEDURES
- **PROC-151**: Lacanian Dyad Analysis (dyadic foundations)
- **PROC-141**: Lacanian Real/Imaginary/Symbolic Foundations
- **PROC-153**: Organizational Blind Spots (institutional pathology)

---

**Document Control:**
- **Last Updated**: 2025-11-26
- **Version**: 1.0
- **Author**: AEON FORGE ETL Architecture Team
- **Status**: OPERATIONAL
