# PROC-151: Lacanian Dyad Psychological Analysis ETL

**Metadata:**
- **Procedure ID**: PROC-151
- **Enhancement**: E17 - Lacanian Dyad Analysis
- **Priority**: High
- **Frequency**: Weekly (incident-triggered for major events)
- **Dependencies**: PROC-141 (Real/Imaginary/Symbolic foundations)
- **Estimated Duration**: 45-60 minutes
- **Target Size**: ~6KB

---

## 1. PURPOSE

Extract, transform, and load defender-attacker dyadic relationship data using Lacanian psychoanalytic frameworks to identify psychological blind spots, transference dynamics, and escalation risks in cybersecurity operations.

### McKenney Questions Addressed
- **Q4 (Psychological Patterns)**: How do defender and attacker identities mirror and construct each other?
- **Q7 (Organizational Dynamics)**: What unconscious dynamics create security blind spots?

### Business Value
- Identify psychological blind spots causing security gaps
- Detect escalation spirals wasting resources
- Predict organizational dysfunction risks
- Design targeted interventions for dyadic issues

---

## 2. PRE-CONDITIONS

### Required Data Availability
- [ ] Incident response reports (last 12 months)
- [ ] SOC team communications (Slack, email archives)
- [ ] Threat intelligence reports and attribution assessments
- [ ] MITRE ATT&CK TTP mappings for observed attacks
- [ ] Organizational communications (budget, board minutes)
- [ ] Historical MTTD/MTTR metrics
- [ ] Training and certification records

### System Requirements
- [ ] Neo4j database running and accessible
- [ ] Python 3.9+ environment with dependencies installed
- [ ] Access to SIEM and threat intelligence platforms
- [ ] Natural language processing libraries (transformers, spacy)

### Access Permissions
- [ ] Read access to incident response database
- [ ] Read access to team communication platforms (with consent)
- [ ] Read access to threat intelligence systems
- [ ] Write access to Neo4j graph database

---

## 3. DATA SOURCES

### 3.1 Defender Profile Extraction

**Primary Sources:**
1. **Incident Response Reports** → Competence belief, fear intensity
2. **SOC Communications** (Slack/email) → Vigilance self-image, cultural characteristics
3. **MTTD/MTTR Metrics** → Actual performance validation
4. **Security Policies** → Control desire, symbolic register content
5. **Training Records** → Competence gap analysis

**Extraction Targets:**
- **Identity Vector Ψ_d**: `[Competence_belief, Vigilance_self_image, Control_desire, Recognition_need, Fear_intensity]`
- **Imaginary Register**: ideal_self, feared_self, projected_attacker, fantasy_scenarios
- **Symbolic Register**: organizational_rules, cultural_norms, compliance_frameworks

### 3.2 Attacker Profile Modeling

**Primary Sources:**
1. **MITRE ATT&CK TTPs** → Skill belief, sophistication scoring
2. **Threat Intelligence Reports** (Mandiant, CrowdStrike) → Motivation, OPSEC quality
3. **Attack Infrastructure Analysis** (passive DNS, IP reputation) → Exposure fear
4. **Malware Analysis** → Technical capability assessment
5. **Attribution Reports** → Organizational structure, resources

**Extraction Targets:**
- **Identity Vector Ψ_a**: `[Skill_belief, Stealth_self_image, Success_desire, Reputation_need, Exposure_fear]`
- **Dark Triad Scores**: machiavellianism, narcissism, psychopathy
- **Imaginary Register**: ideal_self, feared_self, projected_defender

---

## 4. TRANSFORMATION LOGIC

### 4.1 Defender Profile Construction (Agent 1 Logic)

```python
def construct_defender_profile(incident_reports, communications, metrics, policies):
    """Extract defender psychological profile."""

    # Step 1: Identity vector from communications NLP
    competence_belief = extract_from_language(
        communications,
        indicators=["we're capable", "we can handle"],
        counter_indicators=["beyond our expertise", "need help"]
    )

    vigilance_self_image = analyze_response_patterns(
        metrics,
        measures=["proactive_detection_rate", "alert_response_time"]
    )

    control_desire = measure_policy_complexity(
        policies,
        indicators=["restrictive_rules", "change_control_rigidity"]
    )

    recognition_need = analyze_reporting_patterns(
        incident_reports,
        indicators=["success_emphasis", "credit_seeking_language"]
    )

    fear_intensity = extract_emotional_markers(
        communications,
        indicators=["worry", "concern", "catastrophizing"]
    )

    # Step 2: Imaginary register
    imaginary_register = {
        "ideal_self": extract_aspirations(communications),
        "feared_self": extract_anxieties(communications),
        "projected_other": extract_attacker_descriptions(threat_intel),
        "fantasy_scenarios": identify_unrealistic_expectations(communications)
    }

    # Step 3: Symbolic register
    symbolic_register = {
        "organizational_rules": parse_policies(policies),
        "cultural_norms": extract_culture_indicators(communications),
        "compliance_frameworks": list_frameworks(certifications)
    }

    return {
        "defender_id": generate_id(),
        "identity_vector": [competence_belief, vigilance_self_image, control_desire, recognition_need, fear_intensity],
        "imaginary_register": imaginary_register,
        "symbolic_register": symbolic_register,
        "behavioral_indicators": {
            "avg_response_time": calculate_mttr(metrics),
            "proactive_detection_rate": calculate_proactive_rate(metrics)
        }
    }
```

### 4.2 Mirroring Coefficient Calculation (Agent 3 Logic)

```python
def calculate_mirroring_coefficient(defender_profile, attacker_profile):
    """Calculate Λ(d,a): Dyadic mirroring coefficient."""

    Ψ_d = np.array(defender_profile['identity_vector'])
    Ψ_a = np.array(attacker_profile['identity_vector'])
    I_d = defender_profile['imaginary_register']
    I_a = attacker_profile['imaginary_register']
    S_d = defender_profile['symbolic_register']
    S_a = attacker_profile['symbolic_register']

    # Imaginary distance (semantic similarity)
    imaginary_distance = calculate_semantic_distance(
        I_d['projected_other'],  # How defender sees attacker
        I_a['ideal_self']  # How attacker sees self
    )

    mirror_coefficient = 1 / (1 + imaginary_distance)

    # Symbolic barrier (organizational separation)
    symbolic_distance = calculate_organizational_distance(S_d, S_a)
    resistance = np.exp(symbolic_distance)

    # Identity interaction
    identity_interaction = np.linalg.norm(Ψ_d - Ψ_a)

    # Final mirroring coefficient
    lambda_value = (mirror_coefficient * identity_interaction) / resistance

    # Stability assessment
    if lambda_value < 0.3:
        stability = "dissolved"
        risk = "Defender fighting imaginary threat, not actual attacker"
    elif 0.3 <= lambda_value < 0.7:
        stability = "stable"
        risk = "Low, effective threat modeling likely"
    elif 0.7 <= lambda_value < 1.0:
        stability = "unstable"
        risk = "Escalation spiral, resource waste, fixation"
    else:
        stability = "critical"
        risk = "Catastrophic blind spots, paranoia or complacency"

    return {
        "lambda": lambda_value,
        "stability": stability,
        "risk": risk,
        "components": {
            "mirror_coefficient": mirror_coefficient,
            "resistance": resistance,
            "identity_interaction": identity_interaction
        }
    }
```

### 4.3 Blind Spot Identification (Agent 4 Logic)

```python
def identify_blind_spots(defender_profile, attacker_profile, mirroring_analysis):
    """Calculate Β(d,a,t): Blind spot vulnerability index."""

    blind_spots = []

    # Type 1: Projection blind spots (inflation/deflation)
    projection_type = mirroring_analysis['mutual_perception']['defender_perception']['projection_type']

    if "inflation" in projection_type:
        # Over-focusing on imagined capabilities
        imagined_threats = defender_profile['imaginary_register']['imaginary_threat_emphasis']
        actual_ttp_focus = attacker_profile['ttp_sophistication']

        for threat in imagined_threats:
            if threat not in get_top_actual_threats(actual_ttp_focus):
                blind_spots.append({
                    "type": "omnipotence_projection",
                    "category": "over_investment",
                    "description": f"Defender over-focuses on {threat} due to inflated attacker image",
                    "actual_risk": "Low",
                    "perceived_risk": "High",
                    "impact": calculate_resource_waste(threat)
                })

    # Type 2: Identity protection blind spots
    competence_belief = defender_profile['identity_vector'][0]
    actual_detection_rate = defender_profile['behavioral_indicators']['proactive_detection_rate']

    if competence_belief > actual_detection_rate + 0.2:
        blind_spots.append({
            "type": "identity_protection",
            "category": "competence_illusion",
            "description": "Defender overestimates own detection capability",
            "gap": competence_belief - actual_detection_rate,
            "impact": 7.8
        })

    # Calculate total vulnerability index
    total_vulnerability = sum([
        bs['projection_error'] * bs['impact'] / bs.get('detectability', 0.3)
        for bs in blind_spots
    ])

    return {
        "total_vulnerability_index": total_vulnerability,
        "risk_level": categorize_risk(total_vulnerability),
        "blind_spot_count": len(blind_spots),
        "blind_spots": sorted(blind_spots, key=lambda x: x.get('impact', 0), reverse=True)
    }
```

---

## 5. NEO4J SCHEMA

### Node Labels

**DefenderPersona**
```cypher
CREATE (d:DefenderPersona {
  id: STRING,  // "SOC_Team_Alpha"
  competence_belief: FLOAT,  // 0-1
  vigilance_self_image: FLOAT,  // 0-1
  control_desire: FLOAT,  // 0-1
  recognition_need: FLOAT,  // 0-1
  fear_intensity: FLOAT,  // 0-1
  identity_vector: LIST<FLOAT>,  // [0.72, 0.81, 0.89, 0.63, 0.71]
  ideal_self: STRING,
  feared_self: STRING,
  projected_attacker: STRING,
  policy_rigidity: FLOAT,  // 0-1
  avg_response_time: STRING,  // "4.2 hours"
  proactive_detection_rate: FLOAT,  // 0-1
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**AttackerPersona**
```cypher
CREATE (a:AttackerPersona {
  id: STRING,  // "APT29_Cozy_Bear"
  skill_belief: FLOAT,  // 0-1
  stealth_self_image: FLOAT,  // 0-1
  success_desire: FLOAT,  // 0-1
  reputation_need: FLOAT,  // 0-1
  exposure_fear: FLOAT,  // 0-1
  identity_vector: LIST<FLOAT>,
  ideal_self: STRING,
  feared_self: STRING,
  projected_defender: STRING,
  ttp_sophistication: FLOAT,  // 0-1
  dark_triad_machiavellianism: FLOAT,  // 0-1
  dark_triad_narcissism: FLOAT,  // 0-1
  dark_triad_psychopathy: FLOAT,  // 0-1
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**BlindSpot**
```cypher
CREATE (bs:BlindSpot {
  id: STRING,
  type: STRING,  // "omnipotence_projection", "identity_protection"
  category: STRING,  // "over_investment", "competence_illusion"
  description: STRING,
  actual_risk: STRING,  // "Low", "High"
  perceived_risk: STRING,
  vulnerability_score: FLOAT,  // Calculated vulnerability
  impact: FLOAT,  // 0-10
  projection_error: FLOAT,  // Gap magnitude
  detectability: FLOAT,  // 0-1
  created_at: DATETIME
})
```

**Intervention**
```cypher
CREATE (i:Intervention {
  id: STRING,
  strategy: STRING,  // "Reality-Testing", "Symbolic Mediation"
  mechanism: STRING,
  actions: LIST<STRING>,
  target: STRING,  // "Reduce Λ from 0.76 to < 0.5"
  timeline: STRING,  // "3 months"
  expected_outcome: STRING,
  feasibility: FLOAT,  // 0-1
  impact: FLOAT,  // 0-1
  priority: FLOAT,  // feasibility × impact
  created_at: DATETIME
})
```

### Relationships

**MIRRORS**
```cypher
CREATE (d:DefenderPersona)-[r:MIRRORS {
  mirroring_coefficient: FLOAT,  // λ value
  stability: STRING,  // "stable", "unstable", "critical"
  risk: STRING,
  mirror_coefficient: FLOAT,
  resistance: FLOAT,
  identity_interaction: FLOAT,
  imaginary_distance: FLOAT,
  symbolic_distance: FLOAT,
  escalation_risk: STRING,
  mutual_misperception_index: FLOAT,
  created_at: DATETIME
}]->(a:AttackerPersona)
```

**CREATED_BY** (BlindSpot created by dyadic mechanism)
```cypher
CREATE (bs:BlindSpot)-[r:CREATED_BY {
  dyadic_mechanism: STRING,  // "projection", "transference"
  awareness_level: STRING  // "unconscious", "partially_aware"
}]->(d:DefenderPersona)
```

**TRANSFERS** (Transference from past incident)
```cypher
CREATE (d:DefenderPersona)-[r:TRANSFERS {
  source_incident: STRING,
  source_date: DATE,
  current_situation: STRING,
  similarity_score: FLOAT,  // 0-1
  emotional_charge: FLOAT,  // 0-1
  transference_intensity: FLOAT,  // T_d value
  transference_type: STRING,  // "traumatic_over_reaction", "dismissive_under_reaction"
  perception_gap: FLOAT,
  created_at: DATETIME
}]->(:ThreatEvent {id: STRING})
```

**TARGETS** (Intervention targets dyadic relationship)
```cypher
MATCH (d:DefenderPersona)-[:MIRRORS]->(a:AttackerPersona)
CREATE (i:Intervention)-[:TARGETS]->(d)
```

---

## 6. EXECUTION STEPS

### Step 1: Extract Defender Profile
```bash
python /scripts/extract_defender_profile.py \
  --incidents /data/incidents_12mo.json \
  --communications /data/slack_archive/ \
  --metrics /data/siem_metrics.csv \
  --policies /data/security_policies/ \
  --output /data/staging/defender_profile.json
```

**Expected Output**: `defender_profile.json` with identity vectors and registers

### Step 2: Model Attacker Profile
```bash
python /scripts/model_attacker_profile.py \
  --ttps /data/mitre_attck_observed.json \
  --threat_intel /data/mandiant_reports/ \
  --infrastructure /data/passive_dns.csv \
  --malware /data/malware_analysis/ \
  --output /data/staging/attacker_profile.json
```

**Expected Output**: `attacker_profile.json` with attacker psychological profile

### Step 3: Calculate Mirroring Dynamics
```bash
python /scripts/calculate_mirroring.py \
  --defender /data/staging/defender_profile.json \
  --attacker /data/staging/attacker_profile.json \
  --output /data/staging/mirroring_analysis.json
```

**Expected Output**: Mirroring coefficient λ and stability assessment

### Step 4: Identify Blind Spots
```bash
python /scripts/identify_blind_spots.py \
  --defender /data/staging/defender_profile.json \
  --attacker /data/staging/attacker_profile.json \
  --mirroring /data/staging/mirroring_analysis.json \
  --output /data/staging/blind_spots.json
```

**Expected Output**: Blind spot vulnerability index Β(d,a,t) with ranked blind spots

### Step 5: Detect Transference Patterns
```bash
python /scripts/analyze_transference.py \
  --defender /data/staging/defender_profile.json \
  --incident_history /data/incidents_historical.json \
  --current_threats /data/current_threats.json \
  --output /data/staging/transference_analysis.json
```

**Expected Output**: Transference patterns and perception distortions

### Step 6: Design Interventions
```bash
python /scripts/recommend_interventions.py \
  --all_analysis /data/staging/ \
  --org_constraints /data/org_constraints.json \
  --output /data/staging/interventions.json
```

**Expected Output**: Prioritized intervention roadmap

### Step 7: Load to Neo4j
```bash
python /scripts/load_dyadic_analysis_to_neo4j.py \
  --staging_dir /data/staging/ \
  --neo4j_uri bolt://localhost:7687 \
  --neo4j_user neo4j \
  --neo4j_password <password>
```

**Expected Output**: Graph nodes and relationships created

---

## 7. CYPHER QUERIES

### 7.1 Find High-Risk Blind Spots
```cypher
MATCH (bs:BlindSpot)-[:CREATED_BY]->(d:DefenderPersona)-[m:MIRRORS]->(a:AttackerPersona)
WHERE bs.vulnerability_score > 30.0
RETURN bs.description AS blind_spot,
       bs.vulnerability_score AS risk_score,
       bs.impact AS impact,
       m.mirroring_coefficient AS lambda,
       d.id AS defender_team,
       a.id AS threat_actor
ORDER BY bs.vulnerability_score DESC
LIMIT 10
```

### 7.2 Detect Escalation Spirals
```cypher
MATCH (d:DefenderPersona)-[m:MIRRORS]->(a:AttackerPersona)
WHERE m.mirroring_coefficient >= 0.7 AND m.stability = 'unstable'
RETURN d.id AS defender,
       a.id AS attacker,
       m.mirroring_coefficient AS lambda,
       m.risk AS escalation_risk,
       m.mutual_misperception_index AS misperception
ORDER BY m.mirroring_coefficient DESC
```

### 7.3 List Prioritized Interventions
```cypher
MATCH (i:Intervention)-[:TARGETS]->(d:DefenderPersona)-[m:MIRRORS]->(a:AttackerPersona)
WHERE m.stability IN ['unstable', 'critical']
RETURN i.strategy AS intervention_strategy,
       i.actions AS recommended_actions,
       i.priority AS priority_score,
       i.timeline AS implementation_timeline,
       d.id AS target_team,
       m.stability AS knot_status
ORDER BY i.priority DESC
LIMIT 5
```

### 7.4 Analyze Transference Distortions
```cypher
MATCH (d:DefenderPersona)-[t:TRANSFERS]->(te:ThreatEvent)
WHERE t.transference_intensity > 0.5
RETURN d.id AS defender_team,
       t.source_incident AS past_trauma,
       t.current_situation AS current_threat,
       t.transference_type AS distortion_mechanism,
       t.perception_gap AS severity_distortion,
       t.emotional_charge AS trauma_intensity
ORDER BY t.transference_intensity DESC
```

---

## 8. VERIFICATION QUERIES

### 8.1 Validate Profile Completeness
```cypher
MATCH (d:DefenderPersona)
WHERE size(d.identity_vector) = 5
  AND all(v IN d.identity_vector WHERE v >= 0 AND v <= 1)
RETURN count(d) AS valid_defender_profiles

UNION

MATCH (a:AttackerPersona)
WHERE size(a.identity_vector) = 5
  AND all(v IN a.identity_vector WHERE v >= 0 AND v <= 1)
RETURN count(a) AS valid_attacker_profiles
```

### 8.2 Check Mirroring Coefficient Range
```cypher
MATCH ()-[m:MIRRORS]->()
WHERE m.mirroring_coefficient < 0 OR m.mirroring_coefficient > 2.0
RETURN count(m) AS invalid_lambda_values
// Expected: 0 (all λ values should be in valid range)
```

### 8.3 Count Data Loads
```cypher
MATCH (d:DefenderPersona)-[m:MIRRORS]->(a:AttackerPersona)
OPTIONAL MATCH (bs:BlindSpot)-[:CREATED_BY]->(d)
OPTIONAL MATCH (i:Intervention)-[:TARGETS]->(d)
RETURN d.id AS defender,
       a.id AS attacker,
       m.mirroring_coefficient AS lambda,
       m.stability AS stability,
       count(DISTINCT bs) AS blind_spot_count,
       count(DISTINCT i) AS intervention_count
```

---

## 9. ROLLBACK PROCEDURE

### 9.1 Remove Recent Load
```cypher
// Delete all nodes and relationships created in last load
MATCH (d:DefenderPersona)
WHERE d.created_at > datetime() - duration('PT1H')  // Last hour
OPTIONAL MATCH (d)-[r]-()
DELETE r, d

UNION

MATCH (a:AttackerPersona)
WHERE a.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (a)-[r]-()
DELETE r, a

UNION

MATCH (bs:BlindSpot)
WHERE bs.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (bs)-[r]-()
DELETE r, bs

UNION

MATCH (i:Intervention)
WHERE i.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (i)-[r]-()
DELETE r, i
```

### 9.2 Restore from Backup
```bash
# Stop Neo4j
sudo systemctl stop neo4j

# Restore from backup
neo4j-admin restore --from=/backup/neo4j-backup-$(date -d yesterday +%Y%m%d).backup \
  --database=neo4j --force

# Start Neo4j
sudo systemctl start neo4j
```

---

## 10. PERFORMANCE METRICS

**Expected Metrics:**
- **Execution Time**: 45-60 minutes for full 10-agent swarm analysis
- **Token Efficiency**: 32.3% reduction through agent coordination
- **Data Volume**: ~500 defender communications, ~200 threat intel reports analyzed
- **Graph Nodes Created**: 20-50 per analysis (2 personas, 5-15 blind spots, 10-30 interventions)
- **Quality Score**: >0.90 (validated by Agent 10)

**Success Criteria:**
- All identity vectors have 5 dimensions with values in [0, 1]
- Mirroring coefficient λ within [0, 2.0] range
- At least 3 blind spots identified per dyadic relationship
- At least 5 interventions recommended
- Quality validation passes all checks

---

## 11. TROUBLESHOOTING

**Issue**: Low mirroring coefficient (λ < 0.1)
- **Cause**: Defender and attacker not in dyadic relationship (fighting imaginary threat)
- **Fix**: Review threat attribution, validate actual attacker activity

**Issue**: Blind spot vulnerability index unrealistically high (>200)
- **Cause**: Data quality issues in profile extraction
- **Fix**: Review NLP extraction, validate sentiment analysis accuracy

**Issue**: No interventions recommended
- **Cause**: Knot stability = "stable", no intervention urgency
- **Fix**: Expected behavior for healthy dyadic relationships

---

## 12. RELATED PROCEDURES
- **PROC-141**: Lacanian Real/Imaginary/Symbolic Foundations
- **PROC-152**: Triad Group Dynamics (extends dyadic to 3+ parties)
- **PROC-153**: Organizational Blind Spots (institutional counter-transference)

---

**Document Control:**
- **Last Updated**: 2025-11-26
- **Version**: 1.0
- **Author**: AEON FORGE ETL Architecture Team
- **Status**: OPERATIONAL
