# Neo4j Complete Schema - AEON Cyber DT v3.0

**File**: 03_NEO4J_COMPLETE_SCHEMA_v3.0_2025-11-19.md
**Created**: 2025-11-19 11:47:00 UTC
**Modified**: 2025-11-19 11:47:00 UTC
**Version**: v3.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete executable Neo4j schema creation script
**Status**: ACTIVE

## Document Overview

This document provides the complete, executable Neo4j Cypher schema for AEON Cyber Digital Twin v3.0, including all constraints, indexes, and validation procedures.

---

## Schema Initialization Script

### Step 1: Database Preparation

```cypher
// =========================================
// AEON Cyber DT v3.0 Schema Initialization
// =========================================
// Version: 3.0.0
// Date: 2025-11-19
// Purpose: Complete knowledge graph schema creation
// =========================================

// Clear existing schema (CAUTION: Only for fresh installations)
// CALL apoc.schema.assert({},{},true);

// Enable auto-indexing for UUIDs
// CALL db.index.fulltext.awaitEventuallyConsistentIndexRefresh();
```

---

### Step 2: Node Constraints

```cypher
// =========================================
// UNIQUE CONSTRAINTS (Primary Keys)
// =========================================

// CVE Constraints
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS
FOR (c:CVE) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT cve_cveid_unique IF NOT EXISTS
FOR (c:CVE) REQUIRE c.cveId IS UNIQUE;

// CWE Constraints
CREATE CONSTRAINT cwe_id_unique IF NOT EXISTS
FOR (w:CWE) REQUIRE w.id IS UNIQUE;

CREATE CONSTRAINT cwe_cweid_unique IF NOT EXISTS
FOR (w:CWE) REQUIRE w.cweId IS UNIQUE;

// CAPEC Constraints
CREATE CONSTRAINT capec_id_unique IF NOT EXISTS
FOR (a:CAPEC) REQUIRE a.id IS UNIQUE;

CREATE CONSTRAINT capec_capecid_unique IF NOT EXISTS
FOR (a:CAPEC) REQUIRE a.capecId IS UNIQUE;

// Asset Constraints
CREATE CONSTRAINT asset_id_unique IF NOT EXISTS
FOR (a:Asset) REQUIRE a.id IS UNIQUE;

CREATE CONSTRAINT asset_assetid_unique IF NOT EXISTS
FOR (a:Asset) REQUIRE a.assetId IS UNIQUE;

// Software Constraints
CREATE CONSTRAINT software_id_unique IF NOT EXISTS
FOR (s:Software) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT software_softwareid_unique IF NOT EXISTS
FOR (s:Software) REQUIRE s.softwareId IS UNIQUE;

// ThreatActor Constraints
CREATE CONSTRAINT threat_actor_id_unique IF NOT EXISTS
FOR (t:ThreatActor) REQUIRE t.id IS UNIQUE;

CREATE CONSTRAINT threat_actor_actorid_unique IF NOT EXISTS
FOR (t:ThreatActor) REQUIRE t.actorId IS UNIQUE;

// Campaign Constraints
CREATE CONSTRAINT campaign_id_unique IF NOT EXISTS
FOR (c:Campaign) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT campaign_campaignid_unique IF NOT EXISTS
FOR (c:Campaign) REQUIRE c.campaignId IS UNIQUE;

// Indicator Constraints
CREATE CONSTRAINT indicator_id_unique IF NOT EXISTS
FOR (i:Indicator) REQUIRE i.id IS UNIQUE;

CREATE CONSTRAINT indicator_indicatorid_unique IF NOT EXISTS
FOR (i:Indicator) REQUIRE i.indicatorId IS UNIQUE;

// Alert Constraints
CREATE CONSTRAINT alert_id_unique IF NOT EXISTS
FOR (a:Alert) REQUIRE a.id IS UNIQUE;

CREATE CONSTRAINT alert_alertid_unique IF NOT EXISTS
FOR (a:Alert) REQUIRE a.alertId IS UNIQUE;

// MITRE Tactic Constraints
CREATE CONSTRAINT mitre_tactic_id_unique IF NOT EXISTS
FOR (t:MitreTactic) REQUIRE t.id IS UNIQUE;

CREATE CONSTRAINT mitre_tactic_tacticid_unique IF NOT EXISTS
FOR (t:MitreTactic) REQUIRE t.tacticId IS UNIQUE;

// MITRE Technique Constraints
CREATE CONSTRAINT mitre_technique_id_unique IF NOT EXISTS
FOR (t:MitreTechnique) REQUIRE t.id IS UNIQUE;

CREATE CONSTRAINT mitre_technique_techniqueid_unique IF NOT EXISTS
FOR (t:MitreTechnique) REQUIRE t.techniqueId IS UNIQUE;

CREATE CONSTRAINT mitre_technique_externalid_unique IF NOT EXISTS
FOR (t:MitreTechnique) REQUIRE t.externalId IS UNIQUE;

// Organization Constraints
CREATE CONSTRAINT organization_id_unique IF NOT EXISTS
FOR (o:Organization) REQUIRE o.id IS UNIQUE;

CREATE CONSTRAINT organization_orgid_unique IF NOT EXISTS
FOR (o:Organization) REQUIRE o.organizationId IS UNIQUE;

// Department Constraints
CREATE CONSTRAINT department_id_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT department_deptid_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.departmentId IS UNIQUE;

// Control Constraints
CREATE CONSTRAINT control_id_unique IF NOT EXISTS
FOR (c:Control) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT control_controlid_unique IF NOT EXISTS
FOR (c:Control) REQUIRE c.controlId IS UNIQUE;

// Mitigation Constraints
CREATE CONSTRAINT mitigation_id_unique IF NOT EXISTS
FOR (m:Mitigation) REQUIRE m.id IS UNIQUE;

CREATE CONSTRAINT mitigation_mitigationid_unique IF NOT EXISTS
FOR (m:Mitigation) REQUIRE m.mitigationId IS UNIQUE;

// Malware Constraints
CREATE CONSTRAINT malware_id_unique IF NOT EXISTS
FOR (m:Malware) REQUIRE m.id IS UNIQUE;

CREATE CONSTRAINT malware_malwareid_unique IF NOT EXISTS
FOR (m:Malware) REQUIRE m.malwareId IS UNIQUE;

// Exploit Constraints
CREATE CONSTRAINT exploit_id_unique IF NOT EXISTS
FOR (e:Exploit) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT exploit_exploitid_unique IF NOT EXISTS
FOR (e:Exploit) REQUIRE e.exploitId IS UNIQUE;

// User Constraints (for NER10 integration)
CREATE CONSTRAINT user_id_unique IF NOT EXISTS
FOR (u:User) REQUIRE u.id IS UNIQUE;

CREATE CONSTRAINT user_userid_unique IF NOT EXISTS
FOR (u:User) REQUIRE u.userId IS UNIQUE;
```

---

### Step 3: Node Property Indexes

```cypher
// =========================================
// NODE PROPERTY INDEXES
// =========================================

// CVE Indexes
CREATE INDEX cve_published_date IF NOT EXISTS
FOR (c:CVE) ON (c.publishedDate);

CREATE INDEX cve_severity IF NOT EXISTS
FOR (c:CVE) ON (c.baseSeverity);

CREATE INDEX cve_cvss_score IF NOT EXISTS
FOR (c:CVE) ON (c.cvssV3Score);

CREATE INDEX cve_status IF NOT EXISTS
FOR (c:CVE) ON (c.status);

// CWE Indexes
CREATE INDEX cwe_name IF NOT EXISTS
FOR (w:CWE) ON (w.name);

CREATE INDEX cwe_abstraction IF NOT EXISTS
FOR (w:CWE) ON (w.abstraction);

CREATE INDEX cwe_status IF NOT EXISTS
FOR (w:CWE) ON (w.status);

// CAPEC Indexes
CREATE INDEX capec_name IF NOT EXISTS
FOR (a:CAPEC) ON (a.name);

CREATE INDEX capec_abstraction IF NOT EXISTS
FOR (a:CAPEC) ON (a.abstraction);

CREATE INDEX capec_severity IF NOT EXISTS
FOR (a:CAPEC) ON (a.typicalSeverity);

CREATE INDEX capec_status IF NOT EXISTS
FOR (a:CAPEC) ON (a.status);

// Asset Indexes
CREATE INDEX asset_name IF NOT EXISTS
FOR (a:Asset) ON (a.name);

CREATE INDEX asset_type IF NOT EXISTS
FOR (a:Asset) ON (a.assetType);

CREATE INDEX asset_criticality IF NOT EXISTS
FOR (a:Asset) ON (a.criticality);

CREATE INDEX asset_ip IF NOT EXISTS
FOR (a:Asset) ON (a.ipAddress);

CREATE INDEX asset_hostname IF NOT EXISTS
FOR (a:Asset) ON (a.hostname);

CREATE INDEX asset_risk IF NOT EXISTS
FOR (a:Asset) ON (a.riskScore);

CREATE INDEX asset_department IF NOT EXISTS
FOR (a:Asset) ON (a.department);

CREATE INDEX asset_location IF NOT EXISTS
FOR (a:Asset) ON (a.location);

CREATE INDEX asset_os IF NOT EXISTS
FOR (a:Asset) ON (a.operatingSystem);

CREATE INDEX asset_status IF NOT EXISTS
FOR (a:Asset) ON (a.status);

// Software Indexes
CREATE INDEX software_name IF NOT EXISTS
FOR (s:Software) ON (s.name);

CREATE INDEX software_vendor IF NOT EXISTS
FOR (s:Software) ON (s.vendor);

CREATE INDEX software_product IF NOT EXISTS
FOR (s:Software) ON (s.product);

CREATE INDEX software_version IF NOT EXISTS
FOR (s:Software) ON (s.version);

CREATE INDEX software_cpe IF NOT EXISTS
FOR (s:Software) ON (s.cpe23Uri);

CREATE INDEX software_eol IF NOT EXISTS
FOR (s:Software) ON (s.isEndOfLife);

CREATE INDEX software_vuln_count IF NOT EXISTS
FOR (s:Software) ON (s.vulnerabilityCount);

// ThreatActor Indexes
CREATE INDEX threat_actor_name IF NOT EXISTS
FOR (t:ThreatActor) ON (t.name);

CREATE INDEX threat_actor_type IF NOT EXISTS
FOR (t:ThreatActor) ON (t.actorType);

CREATE INDEX threat_actor_nationality IF NOT EXISTS
FOR (t:ThreatActor) ON (t.nationality);

CREATE INDEX threat_actor_status IF NOT EXISTS
FOR (t:ThreatActor) ON (t.status);

CREATE INDEX threat_actor_first_seen IF NOT EXISTS
FOR (t:ThreatActor) ON (t.firstSeen);

// Campaign Indexes
CREATE INDEX campaign_name IF NOT EXISTS
FOR (c:Campaign) ON (c.name);

CREATE INDEX campaign_status IF NOT EXISTS
FOR (c:Campaign) ON (c.status);

CREATE INDEX campaign_start IF NOT EXISTS
FOR (c:Campaign) ON (c.startDate);

CREATE INDEX campaign_end IF NOT EXISTS
FOR (c:Campaign) ON (c.endDate);

// Indicator Indexes
CREATE INDEX indicator_value IF NOT EXISTS
FOR (i:Indicator) ON (i.value);

CREATE INDEX indicator_type IF NOT EXISTS
FOR (i:Indicator) ON (i.type);

CREATE INDEX indicator_valid_from IF NOT EXISTS
FOR (i:Indicator) ON (i.validFrom);

CREATE INDEX indicator_valid_until IF NOT EXISTS
FOR (i:Indicator) ON (i.validUntil);

CREATE INDEX indicator_confidence IF NOT EXISTS
FOR (i:Indicator) ON (i.confidenceScore);

CREATE INDEX indicator_status IF NOT EXISTS
FOR (i:Indicator) ON (i.status);

CREATE INDEX indicator_expired IF NOT EXISTS
FOR (i:Indicator) ON (i.isExpired);

CREATE INDEX indicator_last_seen IF NOT EXISTS
FOR (i:Indicator) ON (i.lastSeen);

// Alert Indexes
CREATE INDEX alert_type IF NOT EXISTS
FOR (a:Alert) ON (a.alertType);

CREATE INDEX alert_severity IF NOT EXISTS
FOR (a:Alert) ON (a.severity);

CREATE INDEX alert_status IF NOT EXISTS
FOR (a:Alert) ON (a.status);

CREATE INDEX alert_detection_time IF NOT EXISTS
FOR (a:Alert) ON (a.detectionTime);

CREATE INDEX alert_assigned_to IF NOT EXISTS
FOR (a:Alert) ON (a.assignedTo);

CREATE INDEX alert_priority IF NOT EXISTS
FOR (a:Alert) ON (a.priority);

CREATE INDEX alert_source_ip IF NOT EXISTS
FOR (a:Alert) ON (a.sourceIp);

CREATE INDEX alert_dest_ip IF NOT EXISTS
FOR (a:Alert) ON (a.destinationIp);

CREATE INDEX alert_correlation_id IF NOT EXISTS
FOR (a:Alert) ON (a.correlationId);

CREATE INDEX alert_risk IF NOT EXISTS
FOR (a:Alert) ON (a.riskScore);

CREATE INDEX alert_false_positive IF NOT EXISTS
FOR (a:Alert) ON (a.falsePositive);

CREATE INDEX alert_true_positive IF NOT EXISTS
FOR (a:Alert) ON (a.truePositive);

// MITRE Tactic Indexes
CREATE INDEX mitre_tactic_name IF NOT EXISTS
FOR (t:MitreTactic) ON (t.name);

CREATE INDEX mitre_tactic_matrix IF NOT EXISTS
FOR (t:MitreTactic) ON (t.matrix);

// MITRE Technique Indexes
CREATE INDEX mitre_technique_name IF NOT EXISTS
FOR (t:MitreTechnique) ON (t.name);

CREATE INDEX mitre_technique_matrix IF NOT EXISTS
FOR (t:MitreTechnique) ON (t.matrix);

CREATE INDEX mitre_technique_is_sub IF NOT EXISTS
FOR (t:MitreTechnique) ON (t.isSubTechnique);

CREATE INDEX mitre_technique_parent IF NOT EXISTS
FOR (t:MitreTechnique) ON (t.parentTechniqueId);

// Organization Indexes
CREATE INDEX organization_name IF NOT EXISTS
FOR (o:Organization) ON (o.name);

CREATE INDEX organization_industry IF NOT EXISTS
FOR (o:Organization) ON (o.industry);

CREATE INDEX organization_country IF NOT EXISTS
FOR (o:Organization) ON (o.country);

// Department Indexes
CREATE INDEX department_name IF NOT EXISTS
FOR (d:Department) ON (d.name);

CREATE INDEX department_parent IF NOT EXISTS
FOR (d:Department) ON (d.parentDepartmentId);

CREATE INDEX department_function IF NOT EXISTS
FOR (d:Department) ON (d.function);

// Control Indexes
CREATE INDEX control_name IF NOT EXISTS
FOR (c:Control) ON (c.name);

CREATE INDEX control_type IF NOT EXISTS
FOR (c:Control) ON (c.controlType);

CREATE INDEX control_effectiveness IF NOT EXISTS
FOR (c:Control) ON (c.effectivenessScore);

CREATE INDEX control_status IF NOT EXISTS
FOR (c:Control) ON (c.implementationStatus);

// Mitigation Indexes
CREATE INDEX mitigation_name IF NOT EXISTS
FOR (m:Mitigation) ON (m.name);

CREATE INDEX mitigation_status IF NOT EXISTS
FOR (m:Mitigation) ON (m.status);

CREATE INDEX mitigation_urgency IF NOT EXISTS
FOR (m:Mitigation) ON (m.urgency);

CREATE INDEX mitigation_type IF NOT EXISTS
FOR (m:Mitigation) ON (m.mitigationType);

// Malware Indexes
CREATE INDEX malware_name IF NOT EXISTS
FOR (m:Malware) ON (m.name);

CREATE INDEX malware_type IF NOT EXISTS
FOR (m:Malware) ON (m.malwareType);

CREATE INDEX malware_family IF NOT EXISTS
FOR (m:Malware) ON (m.family);

CREATE INDEX malware_first_seen IF NOT EXISTS
FOR (m:Malware) ON (m.firstSeen);

CREATE INDEX malware_last_seen IF NOT EXISTS
FOR (m:Malware) ON (m.lastSeen);

// Exploit Indexes
CREATE INDEX exploit_name IF NOT EXISTS
FOR (e:Exploit) ON (e.name);

CREATE INDEX exploit_availability IF NOT EXISTS
FOR (e:Exploit) ON (e.availabilityType);

CREATE INDEX exploit_publication_date IF NOT EXISTS
FOR (e:Exploit) ON (e.publicationDate);

CREATE INDEX exploit_poc IF NOT EXISTS
FOR (e:Exploit) ON (e.proofOfConcept);

CREATE INDEX exploit_weaponized IF NOT EXISTS
FOR (e:Exploit) ON (e.weaponized);

// User Indexes (for NER10 integration)
CREATE INDEX user_email IF NOT EXISTS
FOR (u:User) ON (u.email);

CREATE INDEX user_username IF NOT EXISTS
FOR (u:User) ON (u.username);

CREATE INDEX user_status IF NOT EXISTS
FOR (u:User) ON (u.status);

CREATE INDEX user_department IF NOT EXISTS
FOR (u:User) ON (u.departmentId);
```

---

### Step 4: Full-Text Search Indexes

```cypher
// =========================================
// FULL-TEXT SEARCH INDEXES
// =========================================

// CVE Full-Text
CREATE FULLTEXT INDEX cve_description_fulltext IF NOT EXISTS
FOR (c:CVE) ON EACH [c.description, c.cveId];

// CWE Full-Text
CREATE FULLTEXT INDEX cwe_description_fulltext IF NOT EXISTS
FOR (w:CWE) ON EACH [w.name, w.description, w.extendedDescription];

// CAPEC Full-Text
CREATE FULLTEXT INDEX capec_description_fulltext IF NOT EXISTS
FOR (a:CAPEC) ON EACH [a.name, a.description, a.extendedDescription];

// Asset Full-Text
CREATE FULLTEXT INDEX asset_name_fulltext IF NOT EXISTS
FOR (a:Asset) ON EACH [a.name, a.hostname, a.fqdn];

// Software Full-Text
CREATE FULLTEXT INDEX software_fulltext IF NOT EXISTS
FOR (s:Software) ON EACH [s.name, s.vendor, s.product, s.description];

// ThreatActor Full-Text
CREATE FULLTEXT INDEX threat_actor_fulltext IF NOT EXISTS
FOR (t:ThreatActor) ON EACH [t.name, t.description];

// Campaign Full-Text
CREATE FULLTEXT INDEX campaign_fulltext IF NOT EXISTS
FOR (c:Campaign) ON EACH [c.name, c.description];

// Indicator Full-Text
CREATE FULLTEXT INDEX indicator_fulltext IF NOT EXISTS
FOR (i:Indicator) ON EACH [i.value, i.description];

// Alert Full-Text
CREATE FULLTEXT INDEX alert_fulltext IF NOT EXISTS
FOR (a:Alert) ON EACH [a.title, a.description, a.details];

// MITRE Technique Full-Text
CREATE FULLTEXT INDEX mitre_technique_fulltext IF NOT EXISTS
FOR (t:MitreTechnique) ON EACH [t.name, t.description];

// Malware Full-Text
CREATE FULLTEXT INDEX malware_fulltext IF NOT EXISTS
FOR (m:Malware) ON EACH [m.name, m.description];

// Exploit Full-Text
CREATE FULLTEXT INDEX exploit_fulltext IF NOT EXISTS
FOR (e:Exploit) ON EACH [e.name, e.description];

// Control Full-Text
CREATE FULLTEXT INDEX control_fulltext IF NOT EXISTS
FOR (c:Control) ON EACH [c.name, c.description];

// Mitigation Full-Text
CREATE FULLTEXT INDEX mitigation_fulltext IF NOT EXISTS
FOR (m:Mitigation) ON EACH [m.name, m.description];
```

---

### Step 5: Relationship Indexes

```cypher
// =========================================
// RELATIONSHIP PROPERTY INDEXES
// =========================================

// EXPLOITS Relationship
CREATE INDEX exploits_score IF NOT EXISTS
FOR ()-[r:EXPLOITS]-() ON (r.exploitabilityScore);

// DEMONSTRATES Relationship
CREATE INDEX demonstrates_applicability IF NOT EXISTS
FOR ()-[r:DEMONSTRATES]-() ON (r.applicabilityScore);

// AFFECTS Relationship
CREATE INDEX affects_vulnerable IF NOT EXISTS
FOR ()-[r:AFFECTS]-() ON (r.vulnerable);

// RELATED_TO Relationship
CREATE INDEX related_to_type IF NOT EXISTS
FOR ()-[r:RELATED_TO]-() ON (r.relationshipType);

// RUNS Relationship
CREATE INDEX runs_status IF NOT EXISTS
FOR ()-[r:RUNS]-() ON (r.status);

CREATE INDEX runs_usage IF NOT EXISTS
FOR ()-[r:RUNS]-() ON (r.usageType);

// HAS_VULNERABILITY Relationship
CREATE INDEX has_vuln_status IF NOT EXISTS
FOR ()-[r:HAS_VULNERABILITY]-() ON (r.status);

CREATE INDEX has_vuln_risk IF NOT EXISTS
FOR ()-[r:HAS_VULNERABILITY]-() ON (r.assetRiskScore);

CREATE INDEX has_vuln_detected IF NOT EXISTS
FOR ()-[r:HAS_VULNERABILITY]-() ON (r.detectedDate);

// CONNECTS_TO Relationship
CREATE INDEX connects_to_type IF NOT EXISTS
FOR ()-[r:CONNECTS_TO]-() ON (r.connectionType);

CREATE INDEX connects_to_port IF NOT EXISTS
FOR ()-[r:CONNECTS_TO]-() ON (r.destinationPort);

// ATTRIBUTED_TO Relationship
CREATE INDEX attributed_confidence IF NOT EXISTS
FOR ()-[r:ATTRIBUTED_TO]-() ON (r.confidenceLevel);

// USES Relationship
CREATE INDEX uses_first_seen IF NOT EXISTS
FOR ()-[r:USES]-() ON (r.firstSeen);

CREATE INDEX uses_last_seen IF NOT EXISTS
FOR ()-[r:USES]-() ON (r.lastSeen);

// TARGETS Relationship
CREATE INDEX targets_compromised IF NOT EXISTS
FOR ()-[r:TARGETS]-() ON (r.compromised);

CREATE INDEX targets_impact IF NOT EXISTS
FOR ()-[r:TARGETS]-() ON (r.impactLevel);

// INDICATES Relationship
CREATE INDEX indicates_confidence IF NOT EXISTS
FOR ()-[r:INDICATES]-() ON (r.confidenceScore);

// TRIGGERED_BY Relationship
CREATE INDEX triggered_time IF NOT EXISTS
FOR ()-[r:TRIGGERED_BY]-() ON (r.triggerTime);

// RELATED_ALERT Relationship
CREATE INDEX related_alert_type IF NOT EXISTS
FOR ()-[r:RELATED_ALERT]-() ON (r.correlationType);

CREATE INDEX related_alert_score IF NOT EXISTS
FOR ()-[r:RELATED_ALERT]-() ON (r.correlationScore);

// PART_OF Relationship
CREATE INDEX part_of_matrix IF NOT EXISTS
FOR ()-[r:PART_OF]-() ON (r.matrix);

// USES_TECHNIQUE Relationship
CREATE INDEX uses_technique_first IF NOT EXISTS
FOR ()-[r:USES_TECHNIQUE]-() ON (r.firstObserved);

CREATE INDEX uses_technique_last IF NOT EXISTS
FOR ()-[r:USES_TECHNIQUE]-() ON (r.lastObserved);

// MITIGATES Relationship
CREATE INDEX mitigates_effectiveness IF NOT EXISTS
FOR ()-[r:MITIGATES]-() ON (r.effectivenessScore);

CREATE INDEX mitigates_status IF NOT EXISTS
FOR ()-[r:MITIGATES]-() ON (r.implementationStatus);

// PROTECTS Relationship
CREATE INDEX protects_effectiveness IF NOT EXISTS
FOR ()-[r:PROTECTS]-() ON (r.effectivenessScore);

// EXPLOITED_BY Relationship
CREATE INDEX exploited_public IF NOT EXISTS
FOR ()-[r:EXPLOITED_BY]-() ON (r.publiclyAvailable);

CREATE INDEX exploited_weaponized IF NOT EXISTS
FOR ()-[r:EXPLOITED_BY]-() ON (r.weaponized);

CREATE INDEX exploited_wild IF NOT EXISTS
FOR ()-[r:EXPLOITED_BY]-() ON (r.observedInWild);
```

---

### Step 6: Vector Indexes for Embeddings

```cypher
// =========================================
// VECTOR INDEXES FOR SEMANTIC SEARCH
// =========================================
// Note: Requires Neo4j 5.11+ with vector index support

// CVE Description Embeddings (384-dimensional for all-MiniLM-L6-v2)
CALL db.index.vector.createNodeIndex(
  'cve_embedding_index',
  'CVE',
  'descriptionEmbedding',
  384,
  'cosine'
);

// CWE Description Embeddings
CALL db.index.vector.createNodeIndex(
  'cwe_embedding_index',
  'CWE',
  'descriptionEmbedding',
  384,
  'cosine'
);

// CAPEC Description Embeddings
CALL db.index.vector.createNodeIndex(
  'capec_embedding_index',
  'CAPEC',
  'descriptionEmbedding',
  384,
  'cosine'
);

// MITRE Technique Description Embeddings
CALL db.index.vector.createNodeIndex(
  'mitre_technique_embedding_index',
  'MitreTechnique',
  'descriptionEmbedding',
  384,
  'cosine'
);

// ThreatActor Description Embeddings
CALL db.index.vector.createNodeIndex(
  'threat_actor_embedding_index',
  'ThreatActor',
  'descriptionEmbedding',
  384,
  'cosine'
);

// Campaign Description Embeddings
CALL db.index.vector.createNodeIndex(
  'campaign_embedding_index',
  'Campaign',
  'descriptionEmbedding',
  384,
  'cosine'
);

// Malware Description Embeddings
CALL db.index.vector.createNodeIndex(
  'malware_embedding_index',
  'Malware',
  'descriptionEmbedding',
  384,
  'cosine'
);

// Exploit Description Embeddings
CALL db.index.vector.createNodeIndex(
  'exploit_embedding_index',
  'Exploit',
  'descriptionEmbedding',
  384,
  'cosine'
);

// Asset Description Embeddings
CALL db.index.vector.createNodeIndex(
  'asset_embedding_index',
  'Asset',
  'descriptionEmbedding',
  384,
  'cosine'
);
```

---

### Step 7: Schema Validation Procedures

```cypher
// =========================================
// SCHEMA VALIDATION STORED PROCEDURES
// =========================================

// Procedure: Validate node counts
CALL apoc.custom.asProcedure(
  'aeon.validateNodeCounts',
  'RETURN
    size((n:CVE)) as cve_count,
    size((n:CWE)) as cwe_count,
    size((n:CAPEC)) as capec_count,
    size((n:Asset)) as asset_count,
    size((n:Software)) as software_count,
    size((n:ThreatActor)) as threat_actor_count,
    size((n:Campaign)) as campaign_count,
    size((n:Indicator)) as indicator_count,
    size((n:Alert)) as alert_count,
    size((n:MitreTactic)) as mitre_tactic_count,
    size((n:MitreTechnique)) as mitre_technique_count,
    size((n:Organization)) as organization_count,
    size((n:Department)) as department_count,
    size((n:Control)) as control_count,
    size((n:Mitigation)) as mitigation_count,
    size((n:Malware)) as malware_count,
    size((n:Exploit)) as exploit_count,
    size((n:User)) as user_count',
  'read',
  [
    ['cve_count', 'INTEGER'],
    ['cwe_count', 'INTEGER'],
    ['capec_count', 'INTEGER'],
    ['asset_count', 'INTEGER'],
    ['software_count', 'INTEGER'],
    ['threat_actor_count', 'INTEGER'],
    ['campaign_count', 'INTEGER'],
    ['indicator_count', 'INTEGER'],
    ['alert_count', 'INTEGER'],
    ['mitre_tactic_count', 'INTEGER'],
    ['mitre_technique_count', 'INTEGER'],
    ['organization_count', 'INTEGER'],
    ['department_count', 'INTEGER'],
    ['control_count', 'INTEGER'],
    ['mitigation_count', 'INTEGER'],
    ['malware_count', 'INTEGER'],
    ['exploit_count', 'INTEGER'],
    ['user_count', 'INTEGER']
  ]
);

// Procedure: Validate relationship counts
CALL apoc.custom.asProcedure(
  'aeon.validateRelationshipCounts',
  'RETURN
    size(()-[:EXPLOITS]->()) as exploits_count,
    size(()-[:DEMONSTRATES]->()) as demonstrates_count,
    size(()-[:AFFECTS]->()) as affects_count,
    size(()-[:RELATED_TO]->()) as related_to_count,
    size(()-[:RUNS]->()) as runs_count,
    size(()-[:HAS_VULNERABILITY]->()) as has_vulnerability_count,
    size(()-[:CONNECTS_TO]->()) as connects_to_count,
    size(()-[:BELONGS_TO]->()) as belongs_to_count,
    size(()-[:ATTRIBUTED_TO]->()) as attributed_to_count,
    size(()-[:USES]->()) as uses_count,
    size(()-[:TARGETS]->()) as targets_count,
    size(()-[:INDICATES]->()) as indicates_count,
    size(()-[:TRIGGERED_BY]->()) as triggered_by_count,
    size(()-[:RELATED_ALERT]->()) as related_alert_count,
    size(()-[:PART_OF]->()) as part_of_count,
    size(()-[:SUBTECHNIQUE_OF]->()) as subtechnique_of_count,
    size(()-[:IMPLEMENTS]->()) as implements_count,
    size(()-[:USES_TECHNIQUE]->()) as uses_technique_count,
    size(()-[:MITIGATES]->()) as mitigates_count,
    size(()-[:PROTECTS]->()) as protects_count,
    size(()-[:REQUIRES]->()) as requires_count,
    size(()-[:EXPLOITED_BY]->()) as exploited_by_count,
    size(()-[:DELIVERS]->()) as delivers_count,
    size(()-[:VARIANT_OF]->()) as variant_of_count',
  'read',
  [
    ['exploits_count', 'INTEGER'],
    ['demonstrates_count', 'INTEGER'],
    ['affects_count', 'INTEGER'],
    ['related_to_count', 'INTEGER'],
    ['runs_count', 'INTEGER'],
    ['has_vulnerability_count', 'INTEGER'],
    ['connects_to_count', 'INTEGER'],
    ['belongs_to_count', 'INTEGER'],
    ['attributed_to_count', 'INTEGER'],
    ['uses_count', 'INTEGER'],
    ['targets_count', 'INTEGER'],
    ['indicates_count', 'INTEGER'],
    ['triggered_by_count', 'INTEGER'],
    ['related_alert_count', 'INTEGER'],
    ['part_of_count', 'INTEGER'],
    ['subtechnique_of_count', 'INTEGER'],
    ['implements_count', 'INTEGER'],
    ['uses_technique_count', 'INTEGER'],
    ['mitigates_count', 'INTEGER'],
    ['protects_count', 'INTEGER'],
    ['requires_count', 'INTEGER'],
    ['exploited_by_count', 'INTEGER'],
    ['delivers_count', 'INTEGER'],
    ['variant_of_count', 'INTEGER']
  ]
);

// Procedure: Validate schema integrity
CALL apoc.custom.asProcedure(
  'aeon.validateSchemaIntegrity',
  'MATCH (n)
   WHERE n.id IS NULL OR n.createdAt IS NULL
   RETURN labels(n) as node_type, count(*) as missing_required_properties',
  'read',
  [
    ['node_type', 'LIST OF STRING'],
    ['missing_required_properties', 'INTEGER']
  ]
);
```

---

### Step 8: Common Query Patterns

```cypher
// =========================================
// COMMON QUERY PATTERNS & EXAMPLES
// =========================================

// Pattern 1: Asset vulnerability exposure with severity filtering
MATCH (a:Asset)-[r:HAS_VULNERABILITY]->(c:CVE)
WHERE r.status = 'OPEN'
  AND c.baseSeverity IN ['HIGH', 'CRITICAL']
RETURN a.name, a.assetType, c.cveId, c.baseSeverity, c.cvssV3Score, r.detectedDate
ORDER BY c.cvssV3Score DESC
LIMIT 100;

// Pattern 2: Threat actor TTPs with MITRE ATT&CK mapping
MATCH (ta:ThreatActor)-[u:USES_TECHNIQUE]->(t:MitreTechnique)-[p:PART_OF]->(tac:MitreTactic)
WHERE ta.status = 'ACTIVE'
RETURN ta.name, ta.actorType,
       collect(DISTINCT tac.name) as tactics,
       collect(DISTINCT t.name) as techniques
ORDER BY ta.name;

// Pattern 3: Attack path analysis (lateral movement)
MATCH path = (source:Asset)-[c:CONNECTS_TO*1..3]->(target:Asset)-[h:HAS_VULNERABILITY]->(cve:CVE)
WHERE source.zone = 'EXTERNAL'
  AND target.zone = 'INTERNAL'
  AND cve.baseSeverity IN ['HIGH', 'CRITICAL']
  AND h.status = 'OPEN'
RETURN source.name, target.name, length(path) as hop_count,
       collect(cve.cveId) as vulnerabilities
ORDER BY hop_count ASC, cve.cvssV3Score DESC
LIMIT 50;

// Pattern 4: Software inventory with vulnerability counts
MATCH (a:Asset)-[r:RUNS]->(s:Software)
OPTIONAL MATCH (s)<-[:AFFECTS]-(cve:CVE)
WHERE r.status = 'ACTIVE'
RETURN s.name, s.vendor, s.version, s.isEndOfLife,
       count(DISTINCT a) as asset_count,
       count(DISTINCT cve) as vulnerability_count
ORDER BY vulnerability_count DESC, asset_count DESC
LIMIT 100;

// Pattern 5: Campaign attribution and impact analysis
MATCH (c:Campaign)-[a:ATTRIBUTED_TO]->(ta:ThreatActor)
OPTIONAL MATCH (c)-[t:TARGETS]->(asset:Asset)
WHERE c.status = 'ACTIVE'
  AND a.confidenceLevel IN ['HIGH', 'MEDIUM']
RETURN c.name, c.campaignType, ta.name, ta.actorType,
       count(DISTINCT asset) as targeted_assets,
       sum(CASE WHEN t.compromised = true THEN 1 ELSE 0 END) as compromised_assets
ORDER BY targeted_assets DESC;

// Pattern 6: Mitigation coverage analysis
MATCH (asset:Asset)-[hv:HAS_VULNERABILITY]->(cve:CVE)
WHERE hv.status = 'OPEN'
OPTIONAL MATCH (m:Mitigation)-[mit:MITIGATES]->(cve)
RETURN asset.name, asset.assetType, cve.cveId, cve.baseSeverity,
       CASE WHEN m IS NULL THEN 'NO_MITIGATION' ELSE 'MITIGATED' END as mitigation_status,
       collect(m.name) as mitigations
ORDER BY cve.cvssV3Score DESC;

// Pattern 7: Alert correlation and incident analysis
MATCH (a1:Alert)-[r:RELATED_ALERT]->(a2:Alert)
WHERE r.correlationType = 'SAME_INCIDENT'
  AND a1.status = 'IN_PROGRESS'
MATCH (a1)-[:TRIGGERED_BY]->(i:Indicator)
RETURN a1.title, a1.severity, a1.detectionTime,
       count(DISTINCT a2) as related_alerts,
       collect(DISTINCT i.value) as indicators
ORDER BY a1.detectionTime DESC
LIMIT 50;

// Pattern 8: Semantic search using embeddings
// Find CVEs similar to a given description
CALL db.index.vector.queryNodes(
  'cve_embedding_index',
  5,  // top 5 results
  $queryEmbedding
)
YIELD node, score
RETURN node.cveId, node.description, node.baseSeverity, score
ORDER BY score DESC;

// Pattern 9: Organizational risk heatmap
MATCH (d:Department)<-[:BELONGS_TO]-(a:Asset)-[hv:HAS_VULNERABILITY]->(cve:CVE)
WHERE hv.status = 'OPEN'
RETURN d.name as department,
       count(DISTINCT a) as assets,
       count(DISTINCT cve) as vulnerabilities,
       avg(cve.cvssV3Score) as avg_cvss_score,
       sum(CASE WHEN cve.baseSeverity = 'CRITICAL' THEN 1 ELSE 0 END) as critical_vulns
ORDER BY avg_cvss_score DESC, critical_vulns DESC;

// Pattern 10: CWE weakness hierarchy traversal
MATCH path = (child:CWE)-[:RELATED_TO*]->(parent:CWE)
WHERE child.cweId = 'CWE-79' // Cross-site Scripting example
  AND all(r IN relationships(path) WHERE r.relationshipType = 'CHILD_OF')
RETURN [node in nodes(path) | node.name] as weakness_chain,
       length(path) as chain_depth;
```

---

### Step 9: Performance Tuning Recommendations

```cypher
// =========================================
// PERFORMANCE TUNING SETTINGS
// =========================================

// Recommended Neo4j configuration parameters (neo4j.conf)
/*
# Memory Settings (adjust based on available RAM)
dbms.memory.heap.initial_size=8g
dbms.memory.heap.max_size=8g
dbms.memory.pagecache.size=16g

# Query Performance
dbms.query_cache_size=500
cypher.min_replan_interval=1h
dbms.index_sampling.background_enabled=true
dbms.index_sampling.sample_size_limit=1000000

# Transaction Settings
dbms.transaction.timeout=60s
dbms.lock.acquisition.timeout=30s

# Parallel Execution
dbms.cypher.parallel_runtime.min_rows=10000

# Vector Index Settings
db.vector.enabled=true
db.vector.max_cache_size=10000

# Security
dbms.security.procedures.unrestricted=apoc.*,db.index.vector.*

# Logging
dbms.logs.query.enabled=true
dbms.logs.query.threshold=5s
*/
```

---

## Schema Verification Queries

```cypher
// Verify all constraints are created
SHOW CONSTRAINTS;

// Verify all indexes are created
SHOW INDEXES;

// Check index statistics
CALL db.stats.retrieve('GRAPH COUNTS');

// Verify vector indexes
CALL db.index.vector.queryNodes('cve_embedding_index', 1, [0.1] * 384) YIELD node RETURN count(node);
```

---

## Schema Metadata

```cypher
// Store schema metadata
CREATE (sm:SchemaMetadata {
  version: '3.0.0',
  createdDate: datetime('2025-11-19T11:47:00Z'),
  description: 'AEON Cyber DT v3.0 Complete Schema',
  nodeTypeCount: 18,
  relationshipTypeCount: 24,
  constraintCount: 36,
  indexCount: 150+,
  vectorIndexCount: 9,
  embeddingDimensions: 384,
  embeddingModel: 'all-MiniLM-L6-v2',
  supportedNeo4jVersion: '5.11+'
});
```

---

## Version History

- v3.0.0 (2025-11-19): Complete production schema with vector embeddings
- v2.5.0 (2025-11-11): Added malware and exploit schema
- v2.0.0 (2025-11-01): Initial comprehensive schema

---

**Document Classification**: TECHNICAL SPECIFICATION
**Confidentiality**: INTERNAL USE
**Review Cycle**: Quarterly
**Next Review**: 2026-02-19
