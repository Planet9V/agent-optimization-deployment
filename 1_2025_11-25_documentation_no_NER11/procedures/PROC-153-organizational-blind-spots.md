# PROC-153: Organizational Blind Spot Detection ETL

**Metadata:**
- **Procedure ID**: PROC-153
- **Enhancement**: E19 - Organizational Blind Spots
- **Priority**: Critical
- **Frequency**: Monthly (incident-triggered for major breaches)
- **Dependencies**: PROC-151 (Dyadic analysis), PROC-152 (Triad analysis)
- **Estimated Duration**: 30-45 minutes
- **Target Size**: ~6KB

---

## 1. PURPOSE

Extract, transform, and load organizational blind spot data to identify systemic security gaps created by institutional pathology, counter-transference dynamics, and cultural dysfunction.

### McKenney Questions Addressed
- **Q4 (Psychological Patterns)**: What organizational projections onto security create blind spots?
- **Q7 (Organizational Dynamics)**: How does institutional dysfunction manifest as security vulnerabilities?
- **Q8 (Threat Actor Behavior)**: Which threats are organizationally invisible due to cultural denial?

### Business Value
- Detect organizationally-invisible threats missed despite technical coverage
- Identify cultural dysfunctions creating persistent security gaps
- Predict incident post-mortem biases and learning failures
- Design cultural interventions to restore organizational awareness

---

## 2. PRE-CONDITIONS

### Required Data Availability
- [ ] Incident post-mortem reports (12 months minimum)
- [ ] Alert fatigue statistics (false positive rates, alert suppression data)
- [ ] Mean Time to Detect (MTTD) data by incident type
- [ ] Organizational communication patterns (executive, board, all-hands)
- [ ] Security tool coverage maps and gap assessments
- [ ] Team expertise assessments and skill gap data
- [ ] Budget allocation history (5 years recommended)
- [ ] Threat intelligence feeds (actual vs perceived threats)
- [ ] Penetration test results (blind spots revealed in exercises)
- [ ] HR training records and compliance data

### System Requirements
- [ ] Neo4j database with temporal analytics capability
- [ ] Python 3.9+ with NLP and statistical analysis libraries
- [ ] Access to SIEM for alert fatigue metrics
- [ ] Anomaly detection algorithms for pattern recognition

### Access Permissions
- [ ] Read access to incident database and post-mortems
- [ ] Read access to organizational communications (board level)
- [ ] Read access to budget and finance systems
- [ ] Write access to Neo4j graph database

---

## 3. DATA SOURCES

### 3.1 Incident Post-Mortem Analysis

**Primary Sources:**
1. **Incident Post-Mortem Reports** → Root cause patterns, blame attribution
2. **Lessons Learned Repositories** → Learning vs repeat failures
3. **Incident Classification Data** → Blind spot incident types

**Extraction Targets:**
- **Repeat Incident Patterns**: Same incident type recurring despite "lessons learned"
- **Blame Attribution**: Language analysis for scapegoating vs systemic accountability
- **Organizational Denial**: Incidents downplayed or mis-categorized
- **Learning Effectiveness**: `(Lessons documented - Lessons implemented) / Lessons documented`

### 3.2 Alert Fatigue and Detection Blindness

**Primary Sources:**
1. **SIEM Alert Statistics** → False positive rates, alert suppression
2. **SOC Analyst Feedback** → Alert fatigue surveys, tuning requests
3. **MTTD Analysis** → Time to detection by incident severity

**Extraction Targets:**
- **Alert Fatigue Index**: `(Suppressed alerts + Ignored alerts) / Total alerts`
- **Detection Lag**: MTTD exceeding organizational tolerance
- **Alert Tuning Gap**: Unaddressed high-noise alerts creating operational blindness

### 3.3 Organizational Communication Pathology

**Primary Sources:**
1. **Executive Communications** → Security perception, budget justifications
2. **Board Minutes** → Risk appetite, security prioritization
3. **All-Hands Meetings** → Organizational security messaging
4. **Budget Allocation History** → Security investment vs rhetoric gap

**Extraction Targets:**
- **Omnipotence Projection**: "Our security will prevent any attack" language
- **Scapegoating**: Blame directed at security team for business risks
- **Devaluation**: Under-resourcing while expecting perfect security
- **Denial**: Refusal to acknowledge residual risk

---

## 4. TRANSFORMATION LOGIC

### 4.1 Blind Spot Pattern Recognition

```python
def detect_organizational_blind_spots(incident_data, alert_data, org_comms, budget_data, threat_landscape):
    """Identify systemic blind spots from organizational pathology."""

    blind_spots = []

    # Pattern 1: Repeat Incident Blind Spots
    repeat_incidents = identify_repeat_patterns(
        incident_data,
        time_window=12,  # months
        threshold=2  # Same incident type twice = pattern
    )

    for pattern in repeat_incidents:
        lessons_documented = count_lessons_documented(pattern['incident_type'])
        lessons_implemented = count_lessons_implemented(pattern['incident_type'])
        implementation_gap = (lessons_documented - lessons_implemented) / lessons_documented

        if implementation_gap > 0.5:  # >50% of lessons not implemented
            blind_spots.append({
                "type": "learning_failure",
                "category": "repeat_incident",
                "incident_type": pattern['incident_type'],
                "occurrence_count": pattern['count'],
                "implementation_gap": implementation_gap,
                "description": f"Organizational inability to learn from {pattern['incident_type']} incidents",
                "severity": "High" if pattern['count'] > 3 else "Moderate",
                "root_cause": "Systemic denial or under-resourcing"
            })

    # Pattern 2: Alert Fatigue Blind Spots
    alert_fatigue_sources = identify_high_noise_alerts(alert_data)

    for alert_source in alert_fatigue_sources:
        false_positive_rate = alert_source['false_positives'] / alert_source['total_alerts']

        if false_positive_rate > 0.7 and alert_source['tuning_requested'] and not alert_source['tuned']:
            blind_spots.append({
                "type": "operational_blindness",
                "category": "alert_fatigue",
                "alert_source": alert_source['name'],
                "false_positive_rate": false_positive_rate,
                "suppressed_alerts": alert_source['suppressed_count'],
                "description": f"Alert fatigue on {alert_source['name']} creating operational blindness",
                "severity": "Critical" if false_positive_rate > 0.9 else "High",
                "root_cause": "Under-investment in alert tuning or tool sprawl"
            })

    # Pattern 3: Organizationally Invisible Threats
    imagined_threats = extract_threat_emphasis(org_comms)
    actual_threats = extract_actual_threats(threat_landscape, incident_data)

    invisible_threats = set(actual_threats) - set(imagined_threats)

    for threat in invisible_threats:
        threat_prevalence = calculate_prevalence(threat, incident_data)

        if threat_prevalence > 0.1:  # Threat causes >10% of incidents but not discussed
            blind_spots.append({
                "type": "cultural_denial",
                "category": "invisible_threat",
                "threat_type": threat,
                "incident_percentage": threat_prevalence * 100,
                "organizational_awareness": 0,  # Not in org communications
                "description": f"{threat} invisible to organizational awareness despite {threat_prevalence*100:.0f}% of incidents",
                "severity": "Critical",
                "root_cause": "Cultural taboo, executive blind spot, or scapegoating distraction"
            })

    # Pattern 4: Counter-Transference Blind Spots
    counter_transference = analyze_organizational_projections(org_comms, budget_data)

    for projection in counter_transference:
        if projection['type'] == 'omnipotence_projection':
            blind_spots.append({
                "type": "counter_transference",
                "category": "omnipotence_projection",
                "description": "Organization projects fantasy of perfect security onto team",
                "evidence": projection['evidence'],
                "severity": "High",
                "impact": "Team cannot admit gaps, honest risk communication impossible",
                "root_cause": "Executive denial of residual risk"
            })
        elif projection['type'] == 'scapegoating':
            blind_spots.append({
                "type": "counter_transference",
                "category": "scapegoating",
                "description": "Organization scapegoats security for business risk",
                "evidence": projection['evidence'],
                "severity": "Critical",
                "impact": "Defensive reporting, risk hiding, delayed incident disclosure",
                "root_cause": "Blame culture, unrealistic expectations"
            })
        elif projection['type'] == 'devaluation':
            blind_spots.append({
                "type": "counter_transference",
                "category": "devaluation",
                "description": "Organization devalues security through under-resourcing",
                "budget_gap": projection['budget_gap'],
                "severity": "High",
                "impact": "Technical debt, coverage gaps, inadequate tools",
                "root_cause": "Organizational priority misalignment"
            })

    return {
        "blind_spot_count": len(blind_spots),
        "blind_spots_by_severity": categorize_by_severity(blind_spots),
        "blind_spots": sorted(blind_spots, key=lambda x: severity_score(x['severity']), reverse=True)
    }
```

### 4.2 Systemic Dysfunction Index Calculation

```python
def calculate_systemic_dysfunction_index(blind_spots, org_data):
    """
    Δ_org = Σ [Blind_spot_severity × Recurrence × Organizational_resistance]
    """

    dysfunction_components = []

    for bs in blind_spots:
        # Severity scoring
        severity_map = {"Critical": 1.0, "High": 0.7, "Moderate": 0.4, "Low": 0.2}
        severity_score = severity_map.get(bs['severity'], 0.5)

        # Recurrence (how long has this blind spot persisted?)
        recurrence = calculate_recurrence(bs, org_data['historical_incidents'])

        # Organizational resistance (how hard to fix?)
        if bs['type'] == 'counter_transference':
            resistance = 0.9  # Cultural change is hard
        elif bs['type'] == 'learning_failure':
            resistance = 0.7  # Process change moderate difficulty
        elif bs['type'] == 'operational_blindness':
            resistance = 0.5  # Technical fix easier
        else:
            resistance = 0.6

        dysfunction_score = severity_score * recurrence * resistance
        dysfunction_components.append(dysfunction_score)

    total_dysfunction = sum(dysfunction_components)

    # Normalize to 0-1 scale
    systemic_dysfunction_index = min(1.0, total_dysfunction / 10.0)

    # Classify organizational health
    if systemic_dysfunction_index < 0.3:
        org_health = "Healthy - Minor blind spots, good learning culture"
    elif 0.3 <= systemic_dysfunction_index < 0.6:
        org_health = "Moderate dysfunction - Structural issues present"
    elif 0.6 <= systemic_dysfunction_index < 0.8:
        org_health = "Severe dysfunction - Cultural intervention needed"
    else:
        org_health = "Critical dysfunction - Organizational crisis"

    return {
        "systemic_dysfunction_index": systemic_dysfunction_index,
        "organizational_health": org_health,
        "dysfunction_components": dysfunction_components,
        "primary_dysfunction_drivers": identify_top_drivers(blind_spots, dysfunction_components)
    }
```

---

## 5. NEO4J SCHEMA

### Node Labels

**OrganizationalBlindSpot**
```cypher
CREATE (obs:OrganizationalBlindSpot {
  id: STRING,
  type: STRING,  // "learning_failure", "operational_blindness", "cultural_denial", "counter_transference"
  category: STRING,  // "repeat_incident", "alert_fatigue", "invisible_threat", "omnipotence_projection"
  description: STRING,
  severity: STRING,  // "Critical", "High", "Moderate", "Low"
  root_cause: STRING,
  impact: STRING,
  recurrence_count: INT,  // How many times manifested
  first_detected: DATE,
  last_detected: DATE,
  organizational_awareness: FLOAT,  // 0-1, how aware is org of this blind spot
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**Organization**
```cypher
CREATE (org:Organization {
  id: STRING,  // "ACME_Corp"
  systemic_dysfunction_index: FLOAT,  // Δ_org value, 0-1
  organizational_health: STRING,  // "Healthy", "Moderate dysfunction", "Severe dysfunction", "Critical"
  learning_culture_score: FLOAT,  // 0-1
  blame_culture_index: FLOAT,  // 0-1
  risk_acceptance_maturity: FLOAT,  // 0-1
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**CounterTransference**
```cypher
CREATE (ct:CounterTransference {
  id: STRING,
  projection_type: STRING,  // "omnipotence", "scapegoating", "devaluation"
  description: STRING,
  evidence: LIST<STRING>,  // Quotes from communications
  strength: FLOAT,  // How intense the projection, 0-1
  impact_on_security: STRING,
  created_at: DATETIME
})
```

**IncidentPattern**
```cypher
CREATE (ip:IncidentPattern {
  id: STRING,
  incident_type: STRING,  // "phishing", "misconfig", etc.
  occurrence_count: INT,
  time_span_months: INT,
  lessons_documented: INT,
  lessons_implemented: INT,
  implementation_gap: FLOAT,  // 0-1
  created_at: DATETIME
})
```

### Relationships

**HAS_BLIND_SPOT**
```cypher
CREATE (org:Organization)-[hbs:HAS_BLIND_SPOT {
  discovered_date: DATE,
  severity: STRING,
  addressed: BOOLEAN,  // Has intervention been implemented?
  intervention_date: DATE,
  created_at: DATETIME
}]->(obs:OrganizationalBlindSpot)
```

**CAUSED_BY** (Blind spot caused by counter-transference)
```cypher
CREATE (obs:OrganizationalBlindSpot)-[cb:CAUSED_BY {
  mechanism: STRING,  // "Projection", "Denial", "Scapegoating"
  strength: FLOAT,
  created_at: DATETIME
}]->(ct:CounterTransference)
```

**MANIFESTS_AS** (Pattern manifests as incidents)
```cypher
CREATE (ip:IncidentPattern)-[ma:MANIFESTS_AS {
  incident_count: INT,
  most_recent: DATE,
  created_at: DATETIME
}]->(obs:OrganizationalBlindSpot)
```

**REQUIRES_INTERVENTION**
```cypher
CREATE (obs:OrganizationalBlindSpot)-[ri:REQUIRES_INTERVENTION {
  urgency: STRING,  // "Immediate", "High", "Moderate"
  estimated_cost: STRING,
  cultural_change_required: BOOLEAN,
  created_at: DATETIME
}]->(intervention:Intervention)
```

---

## 6. EXECUTION STEPS

### Step 1: Analyze Incident Post-Mortems
```bash
python /scripts/analyze_incident_postmortems.py \
  --incidents /data/incidents_12mo.json \
  --postmortems /data/postmortem_reports/ \
  --lessons_learned /data/lessons_learned_db.json \
  --output /data/staging/learning_failures.json
```

### Step 2: Calculate Alert Fatigue Metrics
```bash
python /scripts/calculate_alert_fatigue.py \
  --siem_alerts /data/siem_alert_history.csv \
  --analyst_feedback /data/soc_surveys.json \
  --tuning_requests /data/alert_tuning_tickets.json \
  --output /data/staging/alert_fatigue_analysis.json
```

### Step 3: Detect Organizationally Invisible Threats
```bash
python /scripts/detect_invisible_threats.py \
  --org_communications /data/executive_communications/ \
  --threat_landscape /data/threat_intel_feeds/ \
  --actual_incidents /data/incidents_12mo.json \
  --output /data/staging/invisible_threats.json
```

### Step 4: Analyze Organizational Counter-Transference
```bash
python /scripts/analyze_counter_transference.py \
  --exec_comms /data/executive_communications/ \
  --board_minutes /data/board_minutes/ \
  --budget_history /data/budget_allocations_5yr.json \
  --team_surveys /data/security_team_surveys.json \
  --output /data/staging/counter_transference.json
```

### Step 5: Calculate Systemic Dysfunction Index
```bash
python /scripts/calculate_dysfunction_index.py \
  --all_blind_spots /data/staging/ \
  --historical_data /data/historical_incidents.json \
  --output /data/staging/systemic_dysfunction.json
```

### Step 6: Design Cultural Interventions
```bash
python /scripts/design_cultural_interventions.py \
  --dysfunction_analysis /data/staging/systemic_dysfunction.json \
  --org_constraints /data/org_constraints.json \
  --output /data/staging/cultural_interventions.json
```

### Step 7: Load to Neo4j
```bash
python /scripts/load_blind_spot_analysis_to_neo4j.py \
  --staging_dir /data/staging/ \
  --neo4j_uri bolt://localhost:7687 \
  --neo4j_user neo4j \
  --neo4j_password <password>
```

---

## 7. CYPHER QUERIES

### 7.1 List Critical Organizational Blind Spots
```cypher
MATCH (org:Organization)-[hbs:HAS_BLIND_SPOT]->(obs:OrganizationalBlindSpot)
WHERE obs.severity IN ['Critical', 'High'] AND hbs.addressed = false
RETURN obs.type AS blind_spot_type,
       obs.category AS category,
       obs.description AS description,
       obs.severity AS severity,
       obs.root_cause AS root_cause,
       obs.recurrence_count AS times_manifested,
       org.id AS organization
ORDER BY obs.severity DESC, obs.recurrence_count DESC
LIMIT 10
```

### 7.2 Assess Organizational Health
```cypher
MATCH (org:Organization)
RETURN org.id AS organization,
       org.systemic_dysfunction_index AS dysfunction_index,
       org.organizational_health AS health_status,
       org.learning_culture_score AS learning_culture,
       org.blame_culture_index AS blame_culture
ORDER BY org.systemic_dysfunction_index DESC
```

### 7.3 Identify Counter-Transference Patterns
```cypher
MATCH (ct:CounterTransference)<-[cb:CAUSED_BY]-(obs:OrganizationalBlindSpot)
RETURN ct.projection_type AS projection,
       ct.description AS projection_description,
       ct.strength AS projection_strength,
       count(obs) AS blind_spots_created,
       collect(obs.description) AS specific_blind_spots
ORDER BY ct.strength DESC, count(obs) DESC
```

### 7.4 Track Repeat Incident Patterns
```cypher
MATCH (ip:IncidentPattern)-[ma:MANIFESTS_AS]->(obs:OrganizationalBlindSpot)
WHERE ip.implementation_gap > 0.5
RETURN ip.incident_type AS repeat_incident,
       ip.occurrence_count AS times_occurred,
       ip.lessons_documented AS lessons_documented,
       ip.lessons_implemented AS lessons_actually_implemented,
       ip.implementation_gap AS learning_failure_gap,
       obs.description AS resulting_blind_spot
ORDER BY ip.occurrence_count DESC, ip.implementation_gap DESC
```

### 7.5 Prioritize Cultural Interventions
```cypher
MATCH (obs:OrganizationalBlindSpot)-[ri:REQUIRES_INTERVENTION]->(intervention:Intervention)
WHERE ri.urgency IN ['Immediate', 'High']
RETURN intervention.strategy AS intervention_strategy,
       intervention.actions AS recommended_actions,
       ri.cultural_change_required AS cultural_work,
       count(obs) AS blind_spots_addressed,
       collect(obs.description)[0..3] AS sample_blind_spots
ORDER BY ri.urgency DESC, count(obs) DESC
```

---

## 8. VERIFICATION QUERIES

### 8.1 Validate Blind Spot Completeness
```cypher
MATCH (obs:OrganizationalBlindSpot)
WHERE obs.type IS NOT NULL
  AND obs.severity IN ['Critical', 'High', 'Moderate', 'Low']
  AND obs.root_cause IS NOT NULL
RETURN count(obs) AS valid_blind_spots
```

### 8.2 Check Dysfunction Index Range
```cypher
MATCH (org:Organization)
WHERE org.systemic_dysfunction_index < 0 OR org.systemic_dysfunction_index > 1
RETURN count(org) AS invalid_dysfunction_indices
// Expected: 0
```

### 8.3 Count Data Loads
```cypher
MATCH (org:Organization)-[hbs:HAS_BLIND_SPOT]->(obs:OrganizationalBlindSpot)
OPTIONAL MATCH (obs)-[cb:CAUSED_BY]->(ct:CounterTransference)
OPTIONAL MATCH (obs)-[ri:REQUIRES_INTERVENTION]->(intervention)
RETURN org.id AS organization,
       org.systemic_dysfunction_index AS dysfunction,
       count(DISTINCT obs) AS blind_spot_count,
       count(DISTINCT ct) AS counter_transference_count,
       count(DISTINCT intervention) AS intervention_count
```

---

## 9. ROLLBACK PROCEDURE

### 9.1 Remove Recent Load
```cypher
MATCH (obs:OrganizationalBlindSpot)
WHERE obs.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (obs)-[r]-()
DELETE r, obs

UNION

MATCH (ct:CounterTransference)
WHERE ct.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (ct)-[r]-()
DELETE r, ct
```

---

## 10. PERFORMANCE METRICS

**Expected Metrics:**
- **Execution Time**: 30-45 minutes
- **Data Volume**: ~500 incident post-mortems, ~10,000 alerts analyzed
- **Graph Nodes Created**: 15-40 per analysis
- **Quality Score**: >0.88

**Success Criteria:**
- At least 5 organizational blind spots identified
- Systemic dysfunction index within [0, 1]
- All blind spots have severity classification
- At least 3 cultural interventions recommended

---

## 11. TROUBLESHOOTING

**Issue**: No blind spots detected (rare)
- **Cause**: Excellent organizational health or insufficient data
- **Fix**: Review data completeness, validate extraction scripts

**Issue**: Dysfunction index > 1.0 (invalid)
- **Cause**: Calculation error or extreme organizational pathology
- **Fix**: Review normalization logic, cap at 1.0

---

## 12. RELATED PROCEDURES
- **PROC-151**: Lacanian Dyad Analysis (individual blind spots)
- **PROC-152**: Triad Group Dynamics (team-level dysfunction)
- **PROC-154**: Personality Team Fit (cultural compatibility)

---

**Document Control:**
- **Last Updated**: 2025-11-26
- **Version**: 1.0
- **Author**: AEON FORGE ETL Architecture Team
- **Status**: OPERATIONAL
