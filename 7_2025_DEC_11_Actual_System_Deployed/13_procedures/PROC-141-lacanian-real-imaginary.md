# PROC-141: Lacanian Real/Imaginary/Symbolic Foundations ETL

**Metadata:**
- **Procedure ID**: PROC-141
- **Enhancement**: E14 - Lacanian Real/Imaginary/Symbolic Registers
- **Priority**: Critical (foundational for E17, E18)
- **Frequency**: Bi-weekly (foundational analysis)
- **Dependencies**: None (foundational procedure)
- **Estimated Duration**: 30-45 minutes
- **Target Size**: ~6KB

---

## 1. PURPOSE

Extract, transform, and load foundational Lacanian RSI (Real, Symbolic, Imaginary) register data for security team psychological profiling. This procedure establishes the baseline register mappings required for dyadic (E17) and triad (E18) analyses.

### McKenney Questions Addressed
- **Q4 (Psychological Patterns)**: How do Real, Symbolic, and Imaginary registers structure team psychology?
- **Q7 (Organizational Dynamics)**: What are the three fundamental registers organizing security operations?

### Business Value
- Establish baseline psychological registers for all advanced analyses
- Identify register misalignments causing operational dysfunction
- Provide foundational framework for dyadic and triad analyses
- Enable systematic psychological intervention design

---

## 2. PRE-CONDITIONS

### Required Data Availability
- [ ] Security infrastructure inventory (Real register foundation)
- [ ] Security policies and procedures (Symbolic register foundation)
- [ ] Team communications and self-assessments (Imaginary register foundation)
- [ ] Actual incident data (Real register validation)
- [ ] Organizational structure and compliance frameworks (Symbolic register)
- [ ] Team surveys and morale data (Imaginary register)

### System Requirements
- [ ] Neo4j database running
- [ ] Python 3.9+ with NLP libraries
- [ ] Access to organizational data sources

### Access Permissions
- [ ] Read access to all organizational security data
- [ ] Write access to Neo4j graph database

---

## 3. DATA SOURCES

### 3.1 Real Register (Material Reality)
**Primary Sources:**
1. **Infrastructure Inventory** → Actual security capabilities
2. **Incident Database** → Real threats encountered
3. **MITRE ATT&CK Coverage** → Actual detection coverage
4. **Budget Data** → Material resource constraints

**Extraction Targets:**
- Actual threat coverage percentage
- Real infrastructure capabilities
- Factual incident handling metrics

### 3.2 Symbolic Register (Language & Rules)
**Primary Sources:**
1. **Security Policies** → Organizational rules
2. **Compliance Frameworks** → External regulatory constraints
3. **Communication Patterns** → Shared language systems
4. **Organizational Structure** → Role definitions and hierarchies

**Extraction Targets:**
- Policy effectiveness metrics
- Communication clarity scores
- Organizational structure clarity

### 3.3 Imaginary Register (Identity & Perception)
**Primary Sources:**
1. **Team Communications** → Self-image and aspirations
2. **Employee Surveys** → Morale and identity
3. **Threat Perception Analysis** → How team sees threats
4. **Executive Communications** → How organization sees team

**Extraction Targets:**
- Self-image accuracy
- Aspiration realism
- Threat perception alignment

---

## 4. TRANSFORMATION LOGIC

### 4.1 Real Register Mapping

```python
def map_real_register(infrastructure, incidents, coverage):
    """Map the Real register (actual material reality)."""

    # Actual capabilities
    total_assets = infrastructure['total_assets']
    monitored_assets = infrastructure['monitored_assets']
    coverage_percentage = monitored_assets / total_assets

    # Actual threats
    actual_threat_actors = extract_unique(incidents, 'attributed_actor')
    actual_attack_vectors = extract_unique(incidents, 'initial_access_vector')

    # Material constraints
    budget_adequacy = calculate_budget_adequacy(infrastructure['budget'])
    technical_debt = calculate_technical_debt(infrastructure)

    return {
        "real_register_id": "Real_" + infrastructure['team_id'],
        "actual_capabilities": {
            "coverage_percentage": coverage_percentage,
            "monitored_assets": monitored_assets,
            "total_assets": total_assets
        },
        "actual_threats": {
            "threat_actors": actual_threat_actors,
            "attack_vectors": actual_attack_vectors,
            "incident_count": len(incidents)
        },
        "material_constraints": {
            "budget_adequacy": budget_adequacy,
            "technical_debt": technical_debt
        },
        "real_health_score": calculate_real_health(coverage_percentage, budget_adequacy, technical_debt)
    }
```

### 4.2 Symbolic Register Mapping

```python
def map_symbolic_register(policies, org_structure, communications):
    """Map the Symbolic register (language, rules, structure)."""

    # Policy system
    total_policies = len(policies)
    utilized_policies = count_utilized_policies(policies)
    policy_effectiveness = utilized_policies / total_policies

    # Communication clarity
    communication_clarity = analyze_communication_clarity(communications)

    # Organizational structure
    role_clarity = assess_role_clarity(org_structure)
    hierarchy_appropriateness = assess_hierarchy(org_structure)

    return {
        "symbolic_register_id": "Symbolic_" + org_structure['team_id'],
        "policy_system": {
            "total_policies": total_policies,
            "policy_effectiveness": policy_effectiveness,
            "bureaucratic_bloat": 1 - policy_effectiveness
        },
        "communication": {
            "clarity_score": communication_clarity,
            "shared_language": extract_shared_terminology(communications)
        },
        "structure": {
            "role_clarity": role_clarity,
            "hierarchy_appropriateness": hierarchy_appropriateness
        },
        "symbolic_health_score": calculate_symbolic_health(policy_effectiveness, communication_clarity, role_clarity)
    }
```

### 4.3 Imaginary Register Mapping

```python
def map_imaginary_register(team_comms, surveys, threat_perceptions):
    """Map the Imaginary register (identity, self-image, aspirations)."""

    # Self-image
    self_assessments = extract_self_assessments(team_comms)
    self_image_accuracy = validate_self_image(self_assessments, actual_performance)

    # Aspirations
    aspirations = extract_aspirations(team_comms)
    aspiration_realism = assess_aspiration_realism(aspirations)

    # Threat perception
    imagined_threats = extract_threat_emphasis(threat_perceptions)
    actual_threats = get_actual_threats()
    perception_alignment = calculate_perception_alignment(imagined_threats, actual_threats)

    # Morale and fear
    morale = extract_morale(surveys)
    fear_intensity = extract_fear_markers(team_comms)

    return {
        "imaginary_register_id": "Imaginary_" + team_comms['team_id'],
        "self_image": {
            "accuracy": self_image_accuracy,
            "ideal_self": extract_ideal_self(team_comms),
            "feared_self": extract_feared_self(team_comms)
        },
        "aspirations": {
            "realism_score": aspiration_realism,
            "aspirations_list": aspirations
        },
        "threat_perception": {
            "alignment_score": perception_alignment,
            "imagined_threats": imagined_threats,
            "perception_gaps": identify_gaps(imagined_threats, actual_threats)
        },
        "emotional_state": {
            "morale": morale,
            "fear_intensity": fear_intensity
        },
        "imaginary_health_score": calculate_imaginary_health(self_image_accuracy, aspiration_realism, morale)
    }
```

### 4.4 Register Alignment Analysis

```python
def analyze_register_alignment(real_register, symbolic_register, imaginary_register):
    """Analyze alignment across RSI registers."""

    # R-S alignment (Do policies match reality?)
    real_threats = real_register['actual_threats']['threat_actors']
    policy_coverage = symbolic_register['policy_system']['policy_effectiveness']
    RS_alignment = calculate_policy_threat_alignment(real_threats, policy_coverage)

    # S-I alignment (Do policies validate identity?)
    policy_effectiveness = symbolic_register['policy_system']['policy_effectiveness']
    team_identity = imaginary_register['self_image']['ideal_self']
    SI_alignment = calculate_policy_identity_alignment(policy_effectiveness, team_identity)

    # I-R alignment (Does identity match reality?)
    self_image = imaginary_register['self_image']['accuracy']
    actual_performance = real_register['actual_capabilities']['coverage_percentage']
    IR_alignment = calculate_identity_reality_alignment(self_image, actual_performance)

    return {
        "RS_alignment": RS_alignment,
        "SI_alignment": SI_alignment,
        "IR_alignment": IR_alignment,
        "overall_coherence": (RS_alignment + SI_alignment + IR_alignment) / 3.0,
        "misalignment_risks": identify_misalignment_risks(RS_alignment, SI_alignment, IR_alignment)
    }
```

---

## 5. NEO4J SCHEMA

### Node Labels

**RealRegisterFoundation**
```cypher
CREATE (r:RealRegisterFoundation {
  id: STRING,
  coverage_percentage: FLOAT,
  actual_threat_count: INT,
  budget_adequacy: FLOAT,
  technical_debt: FLOAT,
  real_health_score: FLOAT,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**SymbolicRegisterFoundation**
```cypher
CREATE (s:SymbolicRegisterFoundation {
  id: STRING,
  policy_effectiveness: FLOAT,
  communication_clarity: FLOAT,
  role_clarity: FLOAT,
  bureaucratic_bloat: FLOAT,
  symbolic_health_score: FLOAT,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**ImaginaryRegisterFoundation**
```cypher
CREATE (i:ImaginaryRegisterFoundation {
  id: STRING,
  self_image_accuracy: FLOAT,
  aspiration_realism: FLOAT,
  threat_perception_alignment: FLOAT,
  morale: FLOAT,
  fear_intensity: FLOAT,
  imaginary_health_score: FLOAT,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

### Relationships

**ALIGNS_WITH**
```cypher
CREATE (r:RealRegisterFoundation)-[a:ALIGNS_WITH {
  alignment_score: FLOAT,
  alignment_type: STRING,  // "RS", "SI", "IR"
  misalignment_risk: STRING,
  created_at: DATETIME
}]->(s:SymbolicRegisterFoundation)
```

---

## 6. EXECUTION STEPS

### Step 1: Extract Real Register
```bash
python /scripts/extract_real_register.py \
  --infrastructure /data/infrastructure_inventory.json \
  --incidents /data/incidents_12mo.json \
  --coverage /data/mitre_coverage.json \
  --output /data/staging/real_register.json
```

### Step 2: Extract Symbolic Register
```bash
python /scripts/extract_symbolic_register.py \
  --policies /data/security_policies/ \
  --org_structure /data/org_structure.json \
  --communications /data/team_comms/ \
  --output /data/staging/symbolic_register.json
```

### Step 3: Extract Imaginary Register
```bash
python /scripts/extract_imaginary_register.py \
  --team_comms /data/team_comms/ \
  --surveys /data/employee_surveys.json \
  --threat_perceptions /data/threat_intel_reports/ \
  --output /data/staging/imaginary_register.json
```

### Step 4: Analyze Register Alignment
```bash
python /scripts/analyze_register_alignment.py \
  --real /data/staging/real_register.json \
  --symbolic /data/staging/symbolic_register.json \
  --imaginary /data/staging/imaginary_register.json \
  --output /data/staging/register_alignment.json
```

### Step 5: Load to Neo4j
```bash
python /scripts/load_rsi_foundations_to_neo4j.py \
  --staging_dir /data/staging/ \
  --neo4j_uri bolt://localhost:7687 \
  --neo4j_user neo4j \
  --neo4j_password <password>
```

---

## 7. CYPHER QUERIES

### 7.1 Assess Register Health
```cypher
MATCH (r:RealRegisterFoundation), (s:SymbolicRegisterFoundation), (i:ImaginaryRegisterFoundation)
WHERE r.id CONTAINS 'Team_Alpha'
  AND s.id CONTAINS 'Team_Alpha'
  AND i.id CONTAINS 'Team_Alpha'
RETURN r.real_health_score AS real_health,
       s.symbolic_health_score AS symbolic_health,
       i.imaginary_health_score AS imaginary_health
```

### 7.2 Identify Misalignments
```cypher
MATCH (r:RealRegisterFoundation)-[a:ALIGNS_WITH]->(s:SymbolicRegisterFoundation)
WHERE a.alignment_score < 0.5
RETURN r.id AS source_register,
       s.id AS target_register,
       a.alignment_type AS misalignment,
       a.misalignment_risk AS risk
```

---

## 8. VERIFICATION QUERIES

### 8.1 Validate Health Scores
```cypher
MATCH (n)
WHERE n:RealRegisterFoundation OR n:SymbolicRegisterFoundation OR n:ImaginaryRegisterFoundation
  AND (n.real_health_score < 0 OR n.real_health_score > 1
    OR n.symbolic_health_score < 0 OR n.symbolic_health_score > 1
    OR n.imaginary_health_score < 0 OR n.imaginary_health_score > 1)
RETURN count(n) AS invalid_health_scores
// Expected: 0
```

---

## 9. ROLLBACK PROCEDURE

### 9.1 Remove Recent Load
```cypher
MATCH (n)
WHERE (n:RealRegisterFoundation OR n:SymbolicRegisterFoundation OR n:ImaginaryRegisterFoundation)
  AND n.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (n)-[r]-()
DELETE r, n
```

---

## 10. PERFORMANCE METRICS

**Expected Metrics:**
- **Execution Time**: 30-45 minutes
- **Data Volume**: ~200 policies, ~500 communications analyzed
- **Graph Nodes Created**: 3 per team (R, S, I)
- **Quality Score**: >0.85

**Success Criteria:**
- All 3 registers successfully mapped
- All health scores within [0, 1]
- Alignment scores calculated
- Misalignment risks identified

---

## 11. RELATED PROCEDURES
- **PROC-151**: Lacanian Dyad Analysis (uses RSI foundations)
- **PROC-152**: Triad Group Dynamics (uses RSI foundations)
- **PROC-153**: Organizational Blind Spots (extends RSI analysis)

---

**Document Control:**
- **Last Updated**: 2025-11-26
- **Version**: 1.0
- **Author**: AEON FORGE ETL Architecture Team
- **Status**: OPERATIONAL
