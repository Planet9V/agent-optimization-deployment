# REFERENCE_CYPHER_QUERIES.md

**File:** REFERENCE_CYPHER_QUERIES.md
**Created:** 2025-11-25 22:30:00 UTC
**Modified:** 2025-11-25 22:30:00 UTC
**Version:** v1.0.0
**Author:** WAVE 4 Training Data Architecture
**Purpose:** 100+ Cypher queries for NER11 entity and relationship analysis in Neo4j
**Status:** ACTIVE

---

## Executive Summary

This reference contains 100+ Neo4j Cypher queries organized by entity type, relationship pattern, and analytical use case. Queries enable entity extraction, relationship analysis, threat pattern discovery, and organizational risk assessment.

---

## SECTION 1: ENTITY DISCOVERY QUERIES

### 1.1 COGNITIVE_BIAS Queries

```cypher
-- Query 1.1.1: Find all instances of normalcy bias
MATCH (bias:COGNITIVE_BIAS {subtype: "NORMALCY_BIAS"})
RETURN bias.id, bias.text, bias.intensity, bias.consequence_severity
ORDER BY bias.intensity DESC
LIMIT 50;

-- Query 1.1.2: Find cognitive biases by intensity level
MATCH (bias:COGNITIVE_BIAS)
WHERE bias.intensity >= 7
RETURN bias.subtype, COUNT(*) as count, AVG(bias.intensity) as avg_intensity
GROUP BY bias.subtype
ORDER BY count DESC;

-- Query 1.1.3: Find biases affecting specific decision domains
MATCH (bias:COGNITIVE_BIAS)
WHERE bias.decision_domain = "security_investment"
RETURN bias.subtype, bias.awareness_level, COUNT(*) as frequency
GROUP BY bias.subtype, bias.awareness_level
ORDER BY frequency DESC;

-- Query 1.1.4: Find high-consequence biases organizational leaders unaware of
MATCH (bias:COGNITIVE_BIAS)
WHERE bias.consequence_severity IN ["HIGH", "CRITICAL"]
  AND bias.awareness_level = "UNAWARE"
RETURN bias.subtype, COUNT(*) as count
ORDER BY count DESC
LIMIT 20;

-- Query 1.1.5: Cognitive bias prevalence by sector
MATCH (org:ORGANIZATION)-[]->(bias:COGNITIVE_BIAS)
RETURN org.sector, bias.subtype, COUNT(*) as count
ORDER BY org.sector, count DESC;
```

### 1.2 THREAT_PERCEPTION Queries

```cypher
-- Query 1.2.1: Find threat misperceptions (perceived imaginary threats)
MATCH (perc:THREAT_PERCEPTION {subtype: "PERCEIVED_IMAGINARY"})
RETURN perc.threat_name, perc.organizational_context,
       perc.alignment_to_reality, COUNT(*) as frequency
GROUP BY perc.threat_name, perc.organizational_context
ORDER BY frequency DESC
LIMIT 30;

-- Query 1.2.2: Find unperceived real threats
MATCH (perc:THREAT_PERCEPTION {subtype: "UNPERCEIVED_REAL"})
RETURN perc.threat_name, perc.perception_source, COUNT(*) as count
ORDER BY count DESC;

-- Query 1.2.3: Reality alignment assessment by organization size
MATCH (org:ORGANIZATION)-[]->(perc:THREAT_PERCEPTION)
RETURN org.size, AVG(perc.alignment_to_reality) as avg_alignment,
       MIN(perc.alignment_to_reality) as min_alignment,
       MAX(perc.alignment_to_reality) as max_alignment
GROUP BY org.size;

-- Query 1.2.4: Threat perception influenced by media
MATCH (perc:THREAT_PERCEPTION)
WHERE perc.perception_source = "media"
RETURN perc.threat_name, perc.subtype, COUNT(*) as count
ORDER BY count DESC
LIMIT 25;

-- Query 1.2.5: Perception severity alignment
MATCH (perc:THREAT_PERCEPTION)
WHERE perc.subtype IN ["SEVERITY_OVERESTIMATED", "SEVERITY_UNDERESTIMATED"]
RETURN perc.subtype, COUNT(*) as count, AVG(perc.alignment_to_reality)
GROUP BY perc.subtype;
```

### 1.3 DECISION_PATTERN Queries

```cypher
-- Query 1.3.1: Find reactive vs. preventive decisions by sector
MATCH (org:ORGANIZATION)-[]->(decision:DECISION_PATTERN)
RETURN org.sector, decision.subtype, COUNT(*) as count
ORDER BY org.sector, count DESC;

-- Query 1.3.2: Decision quality assessment
MATCH (decision:DECISION_PATTERN)
RETURN decision.decision_quality, COUNT(*) as count,
       AVG(decision.stakeholder_involvement) as avg_involvement
GROUP BY decision.decision_quality
ORDER BY count DESC;

-- Query 1.3.3: Compliance-driven decisions by regulatory framework
MATCH (org:ORGANIZATION)-[]->(decision:DECISION_PATTERN {subtype: "COMPLIANCE_DRIVEN"})
RETURN org.compliance_framework, COUNT(*) as count
ORDER BY count DESC;

-- Query 1.3.4: Find cost-constrained decisions leading to poor outcomes
MATCH (decision:DECISION_PATTERN {subtype: "COST_CONSTRAINED"})
WHERE decision.decision_quality IN ["POOR", "HARMFUL"]
RETURN decision.id, decision.decision_quality, COUNT(*) as count;

-- Query 1.3.5: Authority-imposed decisions and outcomes
MATCH (decision:DECISION_PATTERN {subtype: "AUTHORITY_IMPOSED"})
RETURN decision.decision_quality, decision.decision_speed, COUNT(*) as count
ORDER BY count DESC;
```

### 1.4 ORGANIZATION Queries

```cypher
-- Query 1.4.1: Critical infrastructure organization assessment
MATCH (org:ORGANIZATION {subtype: "CRITICAL_INFRASTRUCTURE"})
RETURN org.name, org.sector, org.size, org.maturity_level, org.financial_health
ORDER BY org.sector;

-- Query 1.4.2: Organizations by maturity level and sector
MATCH (org:ORGANIZATION)
RETURN org.sector, org.maturity_level, COUNT(*) as count
ORDER BY org.sector, org.maturity_level;

-- Query 1.4.3: Healthcare organizations with compliance framework
MATCH (org:ORGANIZATION {subtype: "HEALTHCARE"})
RETURN org.compliance_framework, COUNT(*) as count
ORDER BY count DESC;

-- Query 1.4.4: Organizations under financial stress
MATCH (org:ORGANIZATION)
WHERE org.financial_health IN ["STRESSED", "CRITICAL"]
RETURN org.size, COUNT(*) as count
GROUP BY org.size;

-- Query 1.4.5: Enterprise organizations by compliance requirement
MATCH (org:ORGANIZATION {size: "ENTERPRISE"})
RETURN org.compliance_framework, COUNT(*) as count
ORDER BY count DESC
LIMIT 15;
```

### 1.5 ROLE Queries

```cypher
-- Query 1.5.1: CISO positions and influence levels
MATCH (role:ROLE {subtype: "CISO"})
RETURN role.influence_level, role.technical_depth, role.decision_authority,
       COUNT(*) as count
GROUP BY role.influence_level, role.technical_depth, role.decision_authority
ORDER BY count DESC;

-- Query 1.5.2: Technical roles in security team
MATCH (role:ROLE)
WHERE role.subtype IN ["SECURITY_ENGINEER", "SECURITY_ARCHITECT", "SOC_ANALYST"]
RETURN role.subtype, role.technical_depth, COUNT(*) as count
ORDER BY role.subtype;

-- Query 1.5.3: Decision authority by role type
MATCH (role:ROLE)
RETURN role.subtype, role.decision_authority, COUNT(*) as count
ORDER BY role.subtype, count DESC;

-- Query 1.5.4: High-influence roles
MATCH (role:ROLE)
WHERE role.influence_level IN ["HIGH", "CRITICAL"]
RETURN role.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 1.5.5: Board-level versus operational roles
MATCH (role:ROLE)
RETURN CASE WHEN role.subtype IN ["BOARD_MEMBER", "CEO", "CFO", "CIO", "CISO"]
       THEN "Executive"
       ELSE "Operational"
       END as role_level,
       COUNT(*) as count;
```

### 1.6 CAPABILITY_GAP Queries

```cypher
-- Query 1.6.1: Critical severity capability gaps
MATCH (gap:CAPABILITY_GAP)
WHERE gap.severity = "CRITICAL"
RETURN gap.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 1.6.2: Capability gaps by exploitability
MATCH (gap:CAPABILITY_GAP)
RETURN gap.subtype, gap.exploitability, COUNT(*) as count
ORDER BY gap.subtype, gap.exploitability;

-- Query 1.6.3: Gaps requiring long remediation time
MATCH (gap:CAPABILITY_GAP)
WHERE gap.remediation_timeline IN ["QUARTERS", "YEARS"]
RETURN gap.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 1.6.4: High-cost, critical gaps
MATCH (gap:CAPABILITY_GAP)
WHERE gap.severity = "CRITICAL"
  AND gap.remediation_cost = "HIGH"
RETURN gap.subtype, gap.exploitability, COUNT(*) as count;

-- Query 1.6.5: Skills gaps versus technical gaps
MATCH (gap:CAPABILITY_GAP)
RETURN gap.subtype, COUNT(*) as count
ORDER BY count DESC;
```

---

## SECTION 2: RELATIONSHIP DISCOVERY QUERIES

### 2.1 Psychological Relationships

```cypher
-- Query 2.1.1: Bias influences decision pattern chain
MATCH (bias:COGNITIVE_BIAS)-[r1:INFLUENCES]->(decision:DECISION_PATTERN)-[r2:CREATES]->(threat_perc:THREAT_PERCEPTION)
RETURN bias.subtype, decision.subtype, threat_perc.subtype,
       COUNT(*) as frequency
GROUP BY bias.subtype, decision.subtype, threat_perc.subtype
ORDER BY frequency DESC
LIMIT 30;

-- Query 2.1.2: Organizational stress manifests as bias
MATCH (stress:ORGANIZATIONAL_STRESS)-[r:MANIFESTS_AS]->(bias:COGNITIVE_BIAS)
RETURN stress.subtype, bias.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.1.3: Bias causes gap neglect
MATCH (bias:COGNITIVE_BIAS)-[r:CAUSES_NEGLECT]->(gap:CAPABILITY_GAP)
RETURN bias.subtype, gap.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.1.4: Complete decision-making chain
MATCH path = (bias:COGNITIVE_BIAS)-[r1:INFLUENCES]->
             (decision:DECISION_PATTERN)-[r2:CREATES]->
             (threat_perc:THREAT_PERCEPTION)-[r3:PREDICTS]->
             (prediction:PREDICTION_OUTCOME)
RETURN nodes(path), relationships(path)
LIMIT 20;

-- Query 2.1.5: Bias-stress correlations
MATCH (stress:ORGANIZATIONAL_STRESS)-[r:MANIFESTS_AS]->(bias:COGNITIVE_BIAS)
RETURN stress.subtype, bias.subtype, bias.intensity, COUNT(*) as count
ORDER BY count DESC;
```

### 2.2 Threat Relationships

```cypher
-- Query 2.2.1: Threat actor exploits vulnerability leading to impact
MATCH (actor:THREAT_ACTOR)-[r1:EXPLOITS]->(vuln:VULNERABILITY)-[r2:CAUSES]->(impact:IMPACT_TYPE)
RETURN actor.subtype, vuln.subtype, impact.subtype, COUNT(*) as frequency
GROUP BY actor.subtype, vuln.subtype, impact.subtype
ORDER BY frequency DESC
LIMIT 30;

-- Query 2.2.2: Attack vector to tactical pattern mapping
MATCH (vector:ATTACK_VECTOR)-[r:MANIFESTS]->(pattern:TACTICAL_PATTERN)
RETURN vector.subtype, pattern.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.2.3: Threat actor employment of attack vectors
MATCH (actor:THREAT_ACTOR)-[r:EMPLOYS]->(vector:ATTACK_VECTOR)
RETURN actor.subtype, vector.subtype, COUNT(*) as count
ORDER BY actor.subtype, count DESC;

-- Query 2.2.4: Complete threat chain from actor to impact
MATCH path = (actor:THREAT_ACTOR)-[r1:EMPLOYS]->
             (vector:ATTACK_VECTOR)-[r2:MANIFESTS]->
             (pattern:TACTICAL_PATTERN)-[r3:SUPPORTS_OBJECTIVE]->
             (objective:STRATEGIC_OBJECTIVE)
RETURN COUNT(path) as chains
LIMIT 25;

-- Query 2.2.5: Threat actor targeting by organization type
MATCH (actor:THREAT_ACTOR)-[r:TARGETS]->(org:ORGANIZATION)
RETURN actor.subtype, org.sector, org.size, COUNT(*) as count
ORDER BY actor.subtype, count DESC;
```

### 2.3 Intelligence Relationships

```cypher
-- Query 2.3.1: IOC correlates with threat actor
MATCH (ioc:INDICATOR_OF_COMPROMISE)-[r:CORRELATES_WITH]->(actor:THREAT_ACTOR)
RETURN ioc.subtype, actor.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.3.2: IOC indicates compromise through attack vector
MATCH (ioc:INDICATOR_OF_COMPROMISE)-[r1:INDICATES_COMPROMISE]->(vector:ATTACK_VECTOR)
RETURN ioc.subtype, vector.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.3.3: Tactical pattern exhibits strategy
MATCH (pattern:TACTICAL_PATTERN)-[r:SUPPORTS_OBJECTIVE]->(objective:STRATEGIC_OBJECTIVE)
RETURN pattern.subtype, objective.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.3.4: Threat actor exhibits MITRE tactics
MATCH (actor:THREAT_ACTOR)-[r:EXHIBITS]->(pattern:TACTICAL_PATTERN)
RETURN actor.subtype, pattern.technique_id, COUNT(*) as count
ORDER BY actor.subtype, count DESC;

-- Query 2.3.5: Intelligence chain from IOC to objective
MATCH path = (ioc:INDICATOR_OF_COMPROMISE)-[r1:INDICATES_COMPROMISE]->
             (vector:ATTACK_VECTOR)-[r2:MANIFESTS]->
             (pattern:TACTICAL_PATTERN)-[r3:SUPPORTS_OBJECTIVE]->
             (objective:STRATEGIC_OBJECTIVE)
RETURN COUNT(path) as intelligence_chains;
```

### 2.4 Organizational Relationships

```cypher
-- Query 2.4.1: Role responsible for process
MATCH (role:ROLE)-[r:RESPONSIBLE_FOR]->(process:PROCESS)
RETURN role.subtype, process.subtype, COUNT(*) as count
ORDER BY role.subtype, count DESC;

-- Query 2.4.2: Organization manages process
MATCH (org:ORGANIZATION)-[r:MANAGES]->(process:PROCESS)
RETURN org.sector, process.subtype, COUNT(*) as count
ORDER BY org.sector, process.subtype;

-- Query 2.4.3: Process addresses capability gap
MATCH (process:PROCESS)-[r:ADDRESSES]->(gap:CAPABILITY_GAP)
RETURN process.subtype, gap.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.4.4: Process reveals vulnerability
MATCH (process:PROCESS {subtype: "AUDIT_COMPLIANCE"})-[r:REVEALS]->(vuln:VULNERABILITY)
RETURN vuln.subtype, COUNT(*) as count
ORDER BY count DESC;

-- Query 2.4.5: Organization-process-gap chain
MATCH path = (org:ORGANIZATION)-[r1:MANAGES]->
             (process:PROCESS)-[r2:ADDRESSES]->
             (gap:CAPABILITY_GAP)
RETURN org.sector, process.subtype, gap.subtype, COUNT(path) as count
ORDER BY count DESC
LIMIT 30;
```

---

## SECTION 3: THREAT PATTERN DISCOVERY

### 3.1 APT Campaign Analysis

```cypher
-- Query 3.1.1: Complete APT attack chain
MATCH (actor:THREAT_ACTOR {subtype: "NATION_STATE"})-[r1:EMPLOYS]->
       (vector:ATTACK_VECTOR)-[r2:EXPLOITS]->
       (vuln:VULNERABILITY)-[r3:CAUSES]->
       (impact:IMPACT_TYPE)
RETURN actor.id, vector.subtype, vuln.cve_id, impact.subtype
ORDER BY actor.id
LIMIT 50;

-- Query 3.1.2: Nation-state targeting patterns
MATCH (actor:THREAT_ACTOR {subtype: "NATION_STATE"})-[r1:TARGETS]->(org:ORGANIZATION),
       (actor)-[r2:FOLLOWS_PATTERN]->(objective:STRATEGIC_OBJECTIVE)
RETURN actor.id, org.sector, objective.subtype, COUNT(*) as targeting_frequency
ORDER BY actor.id, targeting_frequency DESC;

-- Query 3.1.3: APT toolkit analysis
MATCH (actor:THREAT_ACTOR {subtype: "NATION_STATE"})-[r1:EMPLOYS]->(vector:ATTACK_VECTOR),
       (actor)-[r2:EXHIBITS]->(pattern:TACTICAL_PATTERN)
RETURN actor.id, vector.subtype, pattern.technique_id, COUNT(*) as usage_count
ORDER BY actor.id, usage_count DESC;

-- Query 3.1.4: Nation-state sophistication assessment
MATCH (actor:THREAT_ACTOR {subtype: "NATION_STATE"})-[r:EXHIBITS]->(pattern:TACTICAL_PATTERN)
RETURN actor.id, COUNT(DISTINCT pattern.technique_id) as technique_count,
       AVG(pattern.sophistication_requirement) as avg_sophistication
GROUP BY actor.id
ORDER BY technique_count DESC;

-- Query 3.1.5: Geographic targeting patterns
MATCH (actor:THREAT_ACTOR {subtype: "NATION_STATE"})-[r:TARGETS]->(org:ORGANIZATION)
WHERE org.geographic_location IS NOT NULL
RETURN actor.id, org.geographic_location, COUNT(*) as target_count
ORDER BY actor.id, target_count DESC;
```

### 3.2 Ransomware Analysis

```cypher
-- Query 3.2.1: Ransomware attack patterns
MATCH (vector:ATTACK_VECTOR {subtype: "MALWARE_DELIVERY"})-[r1:MANIFESTS]->
       (pattern:TACTICAL_PATTERN)-[r2:SUPPORTS_OBJECTIVE]->
       (objective:STRATEGIC_OBJECTIVE {subtype: "FINANCIAL_THEFT"})
RETURN vector.subtype, pattern.technique_id, COUNT(*) as frequency
ORDER BY frequency DESC;

-- Query 3.2.2: Sector targeting of ransomware
MATCH (actor:THREAT_ACTOR)-[r1:EMPLOYS]->(vector:ATTACK_VECTOR {subtype: "MALWARE_DELIVERY"}),
       (actor)-[r2:TARGETS]->(org:ORGANIZATION)
RETURN org.sector, COUNT(DISTINCT actor) as actor_count, COUNT(*) as target_frequency
ORDER BY target_frequency DESC;

-- Query 3.2.3: Ransomware impact analysis
MATCH (vector:ATTACK_VECTOR {subtype: "MALWARE_DELIVERY"})-[r:EXPLOITS]->
       (vuln:VULNERABILITY)-[r2:CAUSES]->(impact:IMPACT_TYPE)
RETURN impact.subtype, COUNT(*) as frequency
ORDER BY frequency DESC;

-- Query 3.2.4: Ransomware victim profile
MATCH (actor:THREAT_ACTOR)-[r:TARGETS]->(org:ORGANIZATION),
       (vector:ATTACK_VECTOR {subtype: "MALWARE_DELIVERY"})-[r2:CAUSES]->
       (impact:IMPACT_TYPE {subtype: "FINANCIAL_LOSS"})
RETURN org.sector, org.size, org.financial_health, COUNT(*) as victim_count
ORDER BY victim_count DESC;

-- Query 3.2.5: Double extortion pattern
MATCH (pattern1:TACTICAL_PATTERN {subtype: "EXFILTRATION"})-[r1:SUPPORTS_OBJECTIVE]->
       (objective:STRATEGIC_OBJECTIVE {subtype: "FINANCIAL_THEFT"}),
       (pattern2:TACTICAL_PATTERN {subtype: "ENCRYPTION"})
RETURN COUNT(DISTINCT pattern1) as exfiltration_count
LIMIT 20;
```

### 3.3 Supply Chain Attack Analysis

```cypher
-- Query 3.3.1: Supply chain attack chain
MATCH (vector:ATTACK_VECTOR {subtype: "SUPPLY_CHAIN"})-[r1:EXPLOITS]->
       (vuln:VULNERABILITY {subtype: "THIRD_PARTY_VULNERABILITY"})-[r2:CAUSES]->
       (impact:IMPACT_TYPE)
RETURN vector.subtype, vuln.id, impact.subtype, COUNT(*) as frequency
ORDER BY frequency DESC;

-- Query 3.3.2: Trusted vendor as attack vector
MATCH (actor:THREAT_ACTOR)-[r1:EMPLOYS]->(vector:ATTACK_VECTOR {subtype: "SUPPLY_CHAIN"}),
       (actor)-[r2:TARGETS]->(org:ORGANIZATION)
RETURN actor.subtype, COUNT(DISTINCT org) as targeted_orgs
ORDER BY targeted_orgs DESC;

-- Query 3.3.3: Downstream impact of single supply chain attack
MATCH (ioc:INDICATOR_OF_COMPROMISE)-[r1:INDICATES_COMPROMISE]->
       (vector:ATTACK_VECTOR {subtype: "SUPPLY_CHAIN"}),
       (vector)-[r2:EXPLOITS]->(vuln:VULNERABILITY)
RETURN ioc.id, COUNT(DISTINCT vuln) as affected_systems
ORDER BY affected_systems DESC;

-- Query 3.3.4: Software vendor breach impact
MATCH (org1:ORGANIZATION {role: "VENDOR"})-[r1:COMPROMISED_BY]->
       (incident:HISTORICAL_EVENT {subtype: "MAJOR_BREACH"}),
       (org2:ORGANIZATION)-[r2:AFFECTED_BY]->(incident)
RETURN org1.name, COUNT(DISTINCT org2) as downstream_impact
ORDER BY downstream_impact DESC
LIMIT 20;

-- Query 3.3.5: Third-party dependency risks
MATCH (org:ORGANIZATION)-[r1:DEPENDS_ON]->(vendor:ORGANIZATION),
       (vendor)-[r2:HAS]->(gap:CAPABILITY_GAP {severity: "CRITICAL"})
RETURN org.name, vendor.name, gap.subtype, COUNT(*) as risk_count
ORDER BY risk_count DESC;
```

---

## SECTION 4: ORGANIZATIONAL RISK ANALYSIS

### 4.1 Vulnerability Management

```cypher
-- Query 4.1.1: High-risk unpatched CVEs by organization
MATCH (org:ORGANIZATION)-[r1:HAS_VULNERABILITY]->(vuln:VULNERABILITY)
WHERE vuln.patch_available = true
  AND vuln.exploitability = "HIGH"
RETURN org.name, vuln.cve_id, vuln.impact_severity, COUNT(*) as frequency
ORDER BY org.name, frequency DESC;

-- Query 4.1.2: Vulnerability remediation timeline assessment
MATCH (org:ORGANIZATION)-[r:HAS_VULNERABILITY]->(vuln:VULNERABILITY)
RETURN org.size, vuln.exploitability, COUNT(*) as vuln_count
ORDER BY org.size, vuln_count DESC;

-- Query 4.1.3: Most exploited vulnerabilities
MATCH (vuln:VULNERABILITY)-[r1:EXPLOITED_BY]->(actor:THREAT_ACTOR)
RETURN vuln.cve_id, COUNT(DISTINCT actor) as attacker_count,
       vuln.impact_severity, vuln.time_in_wild
ORDER BY attacker_count DESC
LIMIT 30;

-- Query 4.1.4: Vulnerability class distribution
MATCH (vuln:VULNERABILITY)
RETURN vuln.subtype, vuln.exploitability, COUNT(*) as count
ORDER BY vuln.subtype, count DESC;

-- Query 4.1.5: Technical vulnerability vs. process vulnerability
MATCH (vuln:VULNERABILITY)
RETURN CASE WHEN vuln.subtype = "TECHNICAL_VULNERABILITY" THEN "Technical"
            WHEN vuln.subtype = "PROCESS_VULNERABILITY" THEN "Process"
            WHEN vuln.subtype = "PEOPLE_VULNERABILITY" THEN "People"
            ELSE "Other"
       END as vulnerability_class,
       COUNT(*) as count
ORDER BY count DESC;
```

### 4.2 Organizational Security Posture

```cypher
-- Query 4.2.1: Security maturity by sector
MATCH (org:ORGANIZATION)
RETURN org.sector, org.maturity_level, COUNT(*) as org_count
ORDER BY org.sector, org_count DESC;

-- Query 4.2.2: Capability gaps in mature vs. nascent organizations
MATCH (org:ORGANIZATION)-[r:HAS]->(gap:CAPABILITY_GAP)
RETURN org.maturity_level, gap.subtype, gap.severity, COUNT(*) as count
ORDER BY org.maturity_level, count DESC;

-- Query 4.2.3: Risk profile by organization characteristics
MATCH (org:ORGANIZATION)-[r1:HAS]->(gap:CAPABILITY_GAP),
       (org)-[r2:SUBJECT_TO]->(stress:ORGANIZATIONAL_STRESS)
RETURN org.sector, org.size, COUNT(DISTINCT gap) as gap_count,
       COUNT(DISTINCT stress) as stress_count
ORDER BY org.sector;

-- Query 4.2.4: Organizations with critical stress + capability gap
MATCH (org:ORGANIZATION)-[r1:HAS]->(gap:CAPABILITY_GAP {severity: "CRITICAL"}),
       (org)-[r2:SUBJECT_TO]->(stress:ORGANIZATIONAL_STRESS {severity: "CRITICAL"})
RETURN org.name, org.sector, COUNT(DISTINCT gap) as gap_count
ORDER BY gap_count DESC;

-- Query 4.2.5: Regulatory compliance posture assessment
MATCH (org:ORGANIZATION)
RETURN org.compliance_framework, org.maturity_level, COUNT(*) as org_count
ORDER BY org.compliance_framework, org_count DESC;
```

### 4.3 Incident Impact Analysis

```cypher
-- Query 4.3.1: Sector-wide breach impact
MATCH (impact:IMPACT_TYPE)-[r:FROM]->(incident:HISTORICAL_EVENT),
       (incident)-[r2:AFFECTED]->(org:ORGANIZATION)
RETURN org.sector, impact.subtype, COUNT(DISTINCT org) as affected_count
ORDER BY org.sector, affected_count DESC;

-- Query 4.3.2: Largest financial impact incidents
MATCH (incident:HISTORICAL_EVENT)-[r:CAUSED]->(impact:IMPACT_TYPE)
WHERE impact.financial_impact_usd IS NOT NULL
RETURN incident.id, impact.financial_impact_usd, impact.affected_records
ORDER BY impact.financial_impact_usd DESC
LIMIT 25;

-- Query 4.3.3: Incident containment speed analysis
MATCH (incident:HISTORICAL_EVENT)-[r:CAUSED]->(impact:IMPACT_TYPE)
RETURN impact.duration, impact.containment_speed, COUNT(*) as frequency
ORDER BY impact.duration, impact.containment_speed;

-- Query 4.3.4: Recurrence of incident types by sector
MATCH (incident1:HISTORICAL_EVENT)-[r:AFFECTED]->(org:ORGANIZATION),
       (incident2:HISTORICAL_EVENT)-[r2:AFFECTED]->(org)
WHERE incident1.subtype = incident2.subtype
RETURN org.sector, incident1.subtype, COUNT(*) as recurrence_count
ORDER BY org.sector, recurrence_count DESC;

-- Query 4.3.5: Dwell time by incident type and sector
MATCH (incident:HISTORICAL_EVENT)-[r:CAUSED]->(impact:IMPACT_TYPE),
       (incident)-[r2:AFFECTED]->(org:ORGANIZATION)
RETURN org.sector, incident.subtype, AVG(impact.duration) as avg_dwell_time
ORDER BY org.sector, avg_dwell_time DESC;
```

---

## SECTION 5: PSYCHOHISTORY PREDICTION

### 5.1 Predictive Chains

```cypher
-- Query 5.1.1: Cognitive bias → outcome prediction
MATCH (bias:COGNITIVE_BIAS)-[r1:INFLUENCES]->
       (decision:DECISION_PATTERN)-[r2:CREATES]->
       (threat_perc:THREAT_PERCEPTION)-[r3:PREDICTS]->
       (prediction:PREDICTION_OUTCOME)
RETURN bias.subtype, prediction.subtype, prediction.probability, COUNT(*) as frequency
ORDER BY frequency DESC
LIMIT 30;

-- Query 5.1.2: Capability gap → vulnerability → incident prediction
MATCH (gap:CAPABILITY_GAP)-[r1:CREATED_BY]->(bias:COGNITIVE_BIAS),
       (gap)-[r2:EXPOSES]->(vuln:VULNERABILITY),
       (vuln)-[r3:EXPLOITED_IN]->(incident:PREDICTION_OUTCOME)
RETURN gap.subtype, vuln.subtype, incident.subtype, incident.probability
ORDER BY incident.probability DESC;

-- Query 5.1.3: Organizational stress → poor decisions → breach risk
MATCH (stress:ORGANIZATIONAL_STRESS)-[r1:MANIFESTS_AS]->(bias:COGNITIVE_BIAS),
       (bias)-[r2:INFLUENCES]->(decision:DECISION_PATTERN {decision_quality: "POOR"}),
       (decision)-[r3:LEADS_TO]->(prediction:PREDICTION_OUTCOME {subtype: "LIKELY_OUTCOME"})
RETURN stress.subtype, bias.subtype, prediction.severity
ORDER BY prediction.severity DESC;

-- Query 5.1.4: Threat perception misalignment → attack success probability
MATCH (perc:THREAT_PERCEPTION)-[r1:CREATES]->(decision:DECISION_PATTERN),
       (decision)-[r2:LEADS_TO]->(outcome:PREDICTION_OUTCOME)
WHERE perc.alignment_to_reality < 50
RETURN perc.threat_name, outcome.probability, outcome.severity
ORDER BY outcome.probability DESC;

-- Query 5.1.5: Complete psychohistory prediction chain
MATCH path = (event:HISTORICAL_EVENT)-[r0:INSPIRED]->
             (perc:THREAT_PERCEPTION)-[r1:CREATES]->
             (bias:COGNITIVE_BIAS)-[r2:INFLUENCES]->
             (decision:DECISION_PATTERN)-[r3:LEADS_TO]->
             (prediction:PREDICTION_OUTCOME)
RETURN nodes(path), [r IN relationships(path) | type(r)] as chain_types
LIMIT 20;
```

### 5.2 Validation Queries

```cypher
-- Query 5.2.1: Validate predictions against historical events
MATCH (prediction:PREDICTION_OUTCOME)-[r:VALIDATED_BY]->(event:HISTORICAL_EVENT)
RETURN prediction.subtype, COUNT(*) as validated_count,
       100 * COUNT(*) / (SELECT COUNT(*) FROM PREDICTION_OUTCOME) as validation_rate
GROUP BY prediction.subtype
ORDER BY validated_count DESC;

-- Query 5.2.2: Prediction accuracy by type
MATCH (prediction:PREDICTION_OUTCOME)-[r:VALIDATED_BY]->(event:HISTORICAL_EVENT)
WHERE event.actual_outcome = prediction.subtype
RETURN prediction.subtype, COUNT(*) as accurate_count,
       COUNT(*) as total_predictions
ORDER BY accurate_count DESC;

-- Query 5.2.3: Hindsight bias validation
MATCH (event:HISTORICAL_EVENT)-[r:CONTRADICTS]->(prediction:PREDICTION_OUTCOME)
WHERE prediction.probability < 50
RETURN prediction.subtype, COUNT(*) as hindsight_bias_count
ORDER BY hindsight_bias_count DESC;

-- Query 5.2.4: Prediction confidence vs. accuracy
MATCH (prediction:PREDICTION_OUTCOME)
RETURN prediction.probability, COUNT(*) as prediction_count,
       100 * COUNT(FILTER(p IN [prediction] WHERE p.validated = true)) / COUNT(*) as accuracy_rate
GROUP BY prediction.probability
ORDER BY prediction.probability DESC;

-- Query 5.2.5: Sector-specific prediction accuracy
MATCH (prediction:PREDICTION_OUTCOME)-[r:AFFECTS]->(org:ORGANIZATION),
       (prediction)-[r2:VALIDATED_BY]->(event:HISTORICAL_EVENT)
RETURN org.sector, prediction.subtype,
       COUNT(*) as prediction_count,
       SUM(CASE WHEN prediction.was_correct THEN 1 ELSE 0 END) as correct_count
ORDER BY org.sector;
```

---

## SECTION 6: THREAT INTELLIGENCE QUERIES

### 6.1 IOC Tracking

```cypher
-- Query 6.1.1: IOC frequency analysis
MATCH (ioc:INDICATOR_OF_COMPROMISE)
RETURN ioc.subtype, COUNT(*) as frequency
ORDER BY frequency DESC;

-- Query 6.1.2: IOCs associated with threat actors
MATCH (ioc:INDICATOR_OF_COMPROMISE)-[r:CORRELATES_WITH]->(actor:THREAT_ACTOR)
RETURN actor.id, ioc.subtype, COUNT(*) as ioc_count
ORDER BY actor.id, ioc_count DESC;

-- Query 6.1.3: IOC first appearance timeline
MATCH (ioc:INDICATOR_OF_COMPROMISE)
WHERE ioc.first_observed IS NOT NULL
RETURN ioc.subtype, ioc.first_observed, COUNT(*) as ioc_count
ORDER BY ioc.first_observed DESC;

-- Query 6.1.4: Currently active IOCs
MATCH (ioc:INDICATOR_OF_COMPROMISE)
WHERE ioc.last_observed = date.today() OR ioc.last_observed > date.today() - duration({days: 30})
RETURN ioc.subtype, COUNT(*) as active_ioc_count
ORDER BY active_ioc_count DESC;

-- Query 6.1.5: IOC confidence assessment
MATCH (ioc:INDICATOR_OF_COMPROMISE)
RETURN ioc.confidence, COUNT(*) as ioc_count
ORDER BY ioc.confidence DESC;
```

### 6.2 MITRE ATT&CK Analysis

```cypher
-- Query 6.2.1: Most used tactics across all actors
MATCH (pattern:TACTICAL_PATTERN)
RETURN pattern.subtype, COUNT(*) as usage_count
ORDER BY usage_count DESC;

-- Query 6.2.2: Actor technique specialization
MATCH (actor:THREAT_ACTOR)-[r:EXHIBITS]->(pattern:TACTICAL_PATTERN)
RETURN actor.id, COUNT(DISTINCT pattern.subtype) as tactic_count,
       COUNT(DISTINCT pattern.technique_id) as technique_count
ORDER BY tactic_count DESC;

-- Query 6.2.3: Technique detection difficulty
MATCH (pattern:TACTICAL_PATTERN)
RETURN pattern.subtype, pattern.detection_difficulty, COUNT(*) as frequency
ORDER BY pattern.subtype, pattern.detection_difficulty;

-- Query 6.2.4: Prevention vs. detection difficulty
MATCH (pattern:TACTICAL_PATTERN)
WHERE pattern.prevention_difficulty IS NOT NULL
RETURN pattern.subtype, pattern.prevention_difficulty, pattern.detection_difficulty,
       COUNT(*) as frequency
ORDER BY pattern.subtype;

-- Query 6.2.5: Evolving tactics over time
MATCH (pattern:TACTICAL_PATTERN)-[r:OBSERVED_IN]->(campaign:HISTORICAL_EVENT)
WHERE campaign.event_date IS NOT NULL
RETURN pattern.subtype, campaign.event_date, COUNT(*) as observation_count
ORDER BY campaign.event_date DESC;
```

---

## SECTION 7: DECISION ANALYSIS QUERIES

### 7.1 Decision Quality Assessment

```cypher
-- Query 7.1.1: Decision quality distribution
MATCH (decision:DECISION_PATTERN)
RETURN decision.decision_quality, COUNT(*) as count
ORDER BY count DESC;

-- Query 7.1.2: Decision quality by stakeholder involvement
MATCH (decision:DECISION_PATTERN)
RETURN decision.decision_quality, decision.stakeholder_involvement, COUNT(*) as count
ORDER BY decision.decision_quality, count DESC;

-- Query 7.1.3: Poor decisions driven by bias
MATCH (bias:COGNITIVE_BIAS)-[r:INFLUENCES]->(decision:DECISION_PATTERN)
WHERE decision.decision_quality IN ["POOR", "HARMFUL"]
RETURN bias.subtype, COUNT(*) as poor_decision_count
ORDER BY poor_decision_count DESC;

-- Query 7.1.4: Decision outcomes by governance style
MATCH (decision:DECISION_PATTERN)
RETURN decision.subtype, decision.decision_quality, COUNT(*) as count
ORDER BY decision.subtype, count DESC;

-- Query 7.1.5: Rushed decisions and quality correlation
MATCH (decision:DECISION_PATTERN)
WHERE decision.decision_speed = "RUSHED"
RETURN decision.decision_quality, COUNT(*) as rushed_decision_count
ORDER BY rushed_decision_count DESC;
```

### 7.2 Compliance Decision Patterns

```cypher
-- Query 7.2.1: Compliance-driven vs. risk-based decisions
MATCH (decision:DECISION_PATTERN)
WHERE decision.subtype IN ["COMPLIANCE_DRIVEN", "REACTIVE_DECISION"]
RETURN decision.subtype, decision.decision_quality, COUNT(*) as count
ORDER BY decision.subtype, count DESC;

-- Query 7.2.2: Regulatory requirement impact
MATCH (req:EXTERNAL_FACTOR {subtype: "REGULATORY_REQUIREMENT"})-[r:DRIVEN_BY]->
       (decision:DECISION_PATTERN)
RETURN req.id, decision.decision_quality, COUNT(*) as decision_count
ORDER BY decision_count DESC;

-- Query 7.2.3: Compliance gaps despite regulation
MATCH (org:ORGANIZATION)-[r1:GOVERNED_BY]->(framework:EXTERNAL_FACTOR),
       (org)-[r2:HAS]->(gap:CAPABILITY_GAP {subtype: "GOVERNANCE_GAP"})
RETURN framework.id, COUNT(*) as non_compliant_orgs
ORDER BY non_compliant_orgs DESC;

-- Query 7.2.4: Over-compliance vs. actual risk
MATCH (org:ORGANIZATION)-[r1:GOVERNED_BY]->(framework:EXTERNAL_FACTOR),
       (org)-[r2:PERCEIVES]->(threat:THREAT_PERCEPTION)
WHERE threat.alignment_to_reality > 100
RETURN org.sector, COUNT(*) as over_compliant_orgs
ORDER BY over_compliant_orgs DESC;

-- Query 7.2.5: Compliance deadline-driven decisions
MATCH (event:EXTERNAL_FACTOR {subtype: "REGULATORY_REQUIREMENT"})-[r:DEADLINE]->(date),
       (decision:DECISION_PATTERN)-[r2:DRIVEN_BY]->(event)
RETURN event.id, decision.decision_speed, COUNT(*) as decision_count
ORDER BY decision_count DESC;
```

---

## SECTION 8: ADVANCED ANALYTICS

### 8.1 Network Centrality

```cypher
-- Query 8.1.1: Most connected threat actors
MATCH (actor:THREAT_ACTOR)-[r]->(target)
RETURN actor.id, COUNT(r) as connection_count
ORDER BY connection_count DESC
LIMIT 20;

-- Query 8.1.2: Most exploited vulnerabilities (degree centrality)
MATCH (vuln:VULNERABILITY)-[r]->(impact:IMPACT_TYPE)
RETURN vuln.cve_id, vuln.id, COUNT(r) as impact_degree
ORDER BY impact_degree DESC
LIMIT 25;

-- Query 8.1.3: Most influential organizations in threat landscape
MATCH (org:ORGANIZATION)-[r]->(entity)
RETURN org.name, org.sector, COUNT(r) as influence_degree
ORDER BY influence_degree DESC
LIMIT 20;

-- Query 8.1.4: Betweenness centrality - critical path entities
MATCH path = shortestPath((source)-[*]-(target))
WHERE source <> target
  AND length(path) > 1
RETURN source, target, length(path) as distance
LIMIT 30;

-- Query 8.1.5: Community detection - related threat actors
MATCH (actor1:THREAT_ACTOR)-[r1]->(entity1),
       (actor2:THREAT_ACTOR)-[r2]->(entity1)
WHERE actor1 <> actor2
RETURN actor1.id, actor2.id, COUNT(DISTINCT entity1) as shared_targets
ORDER BY shared_targets DESC
LIMIT 30;
```

### 8.2 Trend Analysis

```cypher
-- Query 8.2.1: Rising threats by year
MATCH (incident:HISTORICAL_EVENT)
WHERE incident.event_date IS NOT NULL
RETURN incident.subtype, YEAR(incident.event_date) as year, COUNT(*) as incident_count
ORDER BY year DESC, incident_count DESC;

-- Query 8.2.2: Attacker sophistication trend
MATCH (actor:THREAT_ACTOR)-[r]->(pattern:TACTICAL_PATTERN),
       (pattern)-[r2:OBSERVED_IN]->(event:HISTORICAL_EVENT)
WHERE event.event_date IS NOT NULL
RETURN YEAR(event.event_date) as year, actor.sophistication,
       COUNT(DISTINCT pattern.technique_id) as technique_complexity
ORDER BY year DESC;

-- Query 8.2.3: Vulnerability type prevalence over time
MATCH (vuln:VULNERABILITY)-[r:DISCOVERED_IN]->(event:HISTORICAL_EVENT)
WHERE event.event_date IS NOT NULL
RETURN YEAR(event.event_date) as year, vuln.subtype, COUNT(*) as discovery_count
ORDER BY year DESC, discovery_count DESC;

-- Query 8.2.4: Sector-specific incident trends
MATCH (incident:HISTORICAL_EVENT)-[r:AFFECTED]->(org:ORGANIZATION)
WHERE incident.event_date IS NOT NULL
RETURN org.sector, YEAR(incident.event_date) as year, COUNT(*) as incident_count
ORDER BY org.sector, year DESC;

-- Query 8.2.5: Technology adoption and security impact
MATCH (factor:EXTERNAL_FACTOR {subtype: "TECHNOLOGY_TREND"})-[r:ENABLED]->
       (vector:ATTACK_VECTOR)
RETURN factor.id, vector.subtype, COUNT(*) as adoption_impact
ORDER BY adoption_impact DESC;
```

### 8.3 Scenario Analysis

```cypher
-- Query 8.3.1: What-if: Eliminate single critical gap
MATCH (gap:CAPABILITY_GAP {severity: "CRITICAL"})-[r:EXPLOITED_BY]->(actor:THREAT_ACTOR)
RETURN gap.id, COUNT(DISTINCT actor) as dependent_actors
ORDER BY dependent_actors DESC
LIMIT 15;

-- Query 8.3.2: Cascading failure analysis
MATCH path = (vuln1:VULNERABILITY)-[r1:ENABLES]->
             (vuln2:VULNERABILITY)-[r2:ENABLES]->
             (vuln3:VULNERABILITY)
RETURN COUNT(path) as cascade_count
LIMIT 20;

-- Query 8.3.3: Shared vulnerability exposure across organizations
MATCH (vuln:VULNERABILITY)-[r:AFFECTS]->(org1:ORGANIZATION),
       (vuln)-[r2:AFFECTS]->(org2:ORGANIZATION)
WHERE org1 <> org2
RETURN vuln.cve_id, COUNT(DISTINCT org1) as org_exposure
ORDER BY org_exposure DESC
LIMIT 30;

-- Query 8.3.4: Single point of failure analysis
MATCH (resource:PROCESS)-[r:DEPENDS_ON]->(provider)
WHERE NOT EXISTS ((resource)-[:BACKUP_FOR]->())
RETURN resource.subtype, COUNT(*) as spof_count
ORDER BY spof_count DESC;

-- Query 8.3.5: Attack scenario planning
MATCH (actor:THREAT_ACTOR)-[r1:TARGETS]->(org:ORGANIZATION),
       (org)-[r2:HAS]->(gap:CAPABILITY_GAP),
       (gap)-[r3:EXPLOITED_BY]->(vector:ATTACK_VECTOR)
RETURN actor.id, org.name, gap.subtype, vector.subtype
LIMIT 50;
```

---

**End of Cypher Queries Reference** (1,200 lines)
