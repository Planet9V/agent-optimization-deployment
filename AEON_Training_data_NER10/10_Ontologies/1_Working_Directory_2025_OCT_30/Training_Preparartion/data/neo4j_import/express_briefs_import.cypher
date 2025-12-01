// ============================================
// Neo4j Cypher Statements
// Express Attack Briefs Entity & Relationship Import
// ============================================


// ========== EAB_2025_Q2_Threat_Landscape_Report.docx ==========


// Document Node
CREATE (doc:Document {
    name: "EAB_2025_Q2_Threat_Landscape_Report.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "deeper analysis",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "EAB_2025_Q2_Threat_Landscape_Report.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "EAB_2025_Q2_Threat_Landscape_Report.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "analysis of the quarter's most significant incidents reveals consistent targeting patterns and commo",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "EAB_2025_Q2_Threat_Landscape_Report.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Technical Analysis",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "EAB_2025_Q2_Threat_Landscape_Report.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "voice phishing",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "EAB_2025_Q2_Threat_Landscape_Report.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_6:CWE {
    name: "20",
    type: "CWE"
})
WITH e_6
MATCH (doc:Document {name: "EAB_2025_Q2_Threat_Landscape_Report.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-001-VOLTZITE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-001-VOLTZITE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "- malware analysis",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-001-VOLTZITE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "CIP-008",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-001-VOLTZITE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "your water",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "Use water",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "density data",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "Islamic Revolutionary Guard Corps Cyber Electronic Command (IRGC-CEC)",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Use color coding",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "Spear-phishing",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "valve manipulation",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "Dosing Manipulation",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_9:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_10:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_11:CWE {
    name: "Use water-themed blue gradients",
    type: "CWE"
})
WITH e_11
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_11)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_12:CWE {
    name: "20",
    type: "CWE"
})
WITH e_12
MATCH (doc:Document {name: "NCC-OTCE-EAB-002-CYBERAV3NGERS-Unified.md.docx"})
CREATE (e_12)-[:MENTIONED_IN]->(doc)


// Relationship: USES
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CWE {name: "20"})
MERGE (source)-[:USES]->(target)


// ========== NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "first malware",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "process manipulation",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "ICS malware",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "protocol abuse",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_6:CWE {
    name: "28",
    type: "CWE"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_7:CWE {
    name: "damage",
    type: "CWE"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_8:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_9:CAPEC {
    name: "behavioral detection",
    type: "CAPEC"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_10:CWE {
    name: "24",
    type: "CWE"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_11:CAPEC {
    name: "Defend your",
    type: "CAPEC"
})
WITH e_11
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Enhanced.md.docx"})
CREATE (e_11)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "first malware",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "energy distribution",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_4:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_5:CWE {
    name: "29",
    type: "CWE"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_6:CWE {
    name: "20",
    type: "CWE"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "ICS malware",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "\" Malware",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-009-FROSTYGOOP-Unified.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "your manufacturing",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "malware dev",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Use color progression",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Heat overlay",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_6:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-010-RANSOMHUB-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-010-RANSOMHUB-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "29",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Credential Dumping",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-010-RANSOMHUB-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "Color progression",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "Credential stuffing",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "protocol analysis",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "credential abuse",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_6:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-011-BLACKCAT-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "29",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Spear-phishing",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Credential stuffing",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_6:CWE {
    name: "20",
    type: "CWE"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_7:CWE {
    name: "27",
    type: "CWE"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "dependency analysis",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_9:CAPEC {
    name: "malware analysis",
    type: "CAPEC"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-012-STORMOUS-Unified.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:CAPEC {name: "Spear-phishing"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Spear-phishing"})
MATCH (target:CAPEC {name: "Credential stuffing"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "dependency analysis"})
MATCH (target:CAPEC {name: "malware analysis"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-013-RHYSIDA-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-013-RHYSIDA-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// ========== NCC-OTCE-EAB-014-METEORCOMM-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-014-METEORCOMM-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-014-METEORCOMM-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-014-METEORCOMM-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "27",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-014-METEORCOMM-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_4:VULNERABILITY {
    name: "feasibility",
    type: "VULNERABILITY"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-014-METEORCOMM-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Protocol Analysis",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-014-METEORCOMM-Unified.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "20",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "27",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "61",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_4:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Behavioral analysis",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_6:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-015-POLAND-RF-Unified.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "Behavioral analysis"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "protocol analysis",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "Use color progression",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "Cleartext conversion points Shared Databases: Single SQL injection reaches everything Common",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Use color",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "Critical Dependencies",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "electricity",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "verification during",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Relationship: USES
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "Use color progression"})
MERGE (source)-[:USES]->(target)


// ========== NCC-OTCE-EAB-016-PTC-SCADA-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-016-PTC-SCADA-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "27",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "20",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-016-PTC-SCADA-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:CWE {name: "27"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "transport manipulation",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "Spear Phishing",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "27",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "29",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_5:CWE {
    name: "20",
    type: "CWE"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "Targeted Phishing",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "Upload your",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "Reverse engineering analysis",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-017-RAIL-SUPPLY-CHAIN-Unified.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:CWE {name: "27"})
MATCH (target:CWE {name: "29"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CWE {name: "27"})
MATCH (target:CWE {name: "29"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-018-VOLTZITE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-018-VOLTZITE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "Grid overlay",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "disruptions during",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-018-VOLTZITE-RAIL-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-018-VOLTZITE-RAIL-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "27",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-RAIL-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "28",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-RAIL-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-RAIL-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_4:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-RAIL-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "principal abuse",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-018-VOLTZITE-RAIL-Unified.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:CWE {name: "20"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:CWE {name: "27"})
MATCH (target:CWE {name: "28"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: USES
MATCH (source:CWE {name: "27"})
MATCH (target:CWE {name: "28"})
MERGE (source)-[:USES]->(target)


// Relationship: TARGETS
MATCH (source:CWE {name: "27"})
MATCH (target:CWE {name: "28"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-019-AQUAPHANTOM-WATER-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-019-AQUAPHANTOM-WATER-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "T0866 - Exploitation of Remote Services Persistence",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-019-AQUAPHANTOM-WATER-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "dosing PLCs",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-019-AQUAPHANTOM-WATER-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "process manipulation",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-019-AQUAPHANTOM-WATER-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Critical Water Infrastructure",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-019-AQUAPHANTOM-WATER-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "Grid overlay",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "velocity",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "optimal manipulation for maximum impact          current_speed = self.get_train_telemetry(train_id)[",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Use color progression",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_6:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "Use color coding",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-020-GRAINKEEPER-FOOD-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-020-GRAINKEEPER-FOOD-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "- malware analysis",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-FOOD-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "GPS manipulation",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-FOOD-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-FOOD-Unified.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "GPS Manipulation",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-020-GRAINKEEPER-FOOD-Unified.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-021-CHEMLOCK-Unified.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-021-CHEMLOCK-Unified.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "process data",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-021-CHEMLOCK-Unified.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-021-CHEMLOCK-Unified.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-022-TREASURY-BREACH-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-022-TREASURY-BREACH-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-022-TREASURY-BREACH-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-022-TREASURY-BREACH-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-023-QILIN-SURGE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-023-QILIN-SURGE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-023-QILIN-SURGE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "Out-of-bounds Write",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-023-QILIN-SURGE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-023-QILIN-SURGE-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CWE {name: "Out-of-bounds Write"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "breakthroughs immediately",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "20",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_5:CWE {
    name: "27",
    type: "CWE"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "Innovation Sharing",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "Vulnerability",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "Geographic distribution",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_9:CWE {
    name: "Immediate isolation of critical systems from general network access Backup Validation",
    type: "CWE"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_10:CWE {
    name: "cryptocurrency-based operations Cyber Warfare Preparedness: National cyber warfare capability develo",
    type: "CWE"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-024-DRAGONFORCE-ECOSYSTEM-Enhanced.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:CWE {name: "27"})
MATCH (target:CWE {name: "20"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "energy distribution",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "credential abuse",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_4:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_5:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "damage during",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_7:CWE {
    name: "Immediate isolation of critical control systems from network access Administrative Access Restrictio",
    type: "CWE"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "Behavioral analysis",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_9:CWE {
    name: "Development of Volt Typhoon infrastructure-specific indicators Machine Learning Detection: AI-powere",
    type: "CWE"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_10:CWE {
    name: "Immediate isolation of critical control systems from internet access Monitoring Enhancement: Deploym",
    type: "CWE"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_11:CWE {
    name: "International coordination for infrastructure protection against state-sponsored threats Economic Se",
    type: "CWE"
})
WITH e_11
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_11)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_12:CWE {
    name: "analysis of SCADA and control system compromise techniques Strategic Pre-positioning Assessment: Int",
    type: "CWE"
})
WITH e_12
MATCH (doc:Document {name: "NCC-OTCE-EAB-025-VOLT-TYPHOON-INFRASTRUCTURE-Enhanced.md.docx"})
CREATE (e_12)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: USES
MATCH (source:CAPEC {name: "credential abuse"})
MATCH (target:CWE {name: "20"})
MERGE (source)-[:USES]->(target)


// Relationship: USES
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:CAPEC {name: "damage during"})
MERGE (source)-[:USES]->(target)


// Relationship: USES
MATCH (source:CAPEC {name: "damage during"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:USES]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CWE {name: "Immediate isolation of critical control systems fr"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "medication dispensing",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "spear-phishing",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Protocol Abuse",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "protocol exploitation",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_6:CWE {
    name: "Medical record alteration for additional extortion pressure Healthcare Network Architecture Exploita",
    type: "CWE"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_7:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "operators developing",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_9:CAPEC {
    name: "Behavioral analysis",
    type: "CAPEC"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_10:CAPEC {
    name: "protocol abuse",
    type: "CAPEC"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-026-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "spear-phishing"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Protocol Abuse"})
MATCH (target:CAPEC {name: "protocol exploitation"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Protocol Abuse"})
MATCH (target:CAPEC {name: "protocol exploitation"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "cryptocurrency exploitation Objective 4:",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "Cryptocurrency conversion",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "20",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_5:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_6:CWE {
    name: "cryptocurrency exploitation International financial monitoring evasion through decentralized asset m",
    type: "CWE"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "cryptocurrency conversion",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "international distribution",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_9:CAPEC {
    name: "Cryptocurrency",
    type: "CAPEC"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_10:CWE {
    name: "Inconsistent cryptocurrency regulation across",
    type: "CWE"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_11:CAPEC {
    name: "cryptocurrency",
    type: "CAPEC"
})
WITH e_11
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_11)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_12:CWE {
    name: "International cooperation for cryptocurrency theft investigation and asset recovery Next-Generation ",
    type: "CWE"
})
WITH e_12
MATCH (doc:Document {name: "NCC-OTCE-EAB-027-LAZARUS-CRYPTO-EXCHANGE-Enhanced.md.docx"})
CREATE (e_12)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CWE {name: "20"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CWE {name: "20"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: ENABLES
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:CAPEC {name: "Cryptocurrency"})
MERGE (source)-[:ENABLES]->(target)


// Relationship: ENABLES
MATCH (source:CAPEC {name: "Cryptocurrency"})
MATCH (target:CWE {name: "Inconsistent cryptocurrency regulation across"})
MERGE (source)-[:ENABLES]->(target)


// Relationship: ENABLES
MATCH (source:CAPEC {name: "Cryptocurrency"})
MATCH (target:CWE {name: "Inconsistent cryptocurrency regulation across"})
MERGE (source)-[:ENABLES]->(target)


// Relationship: ENABLES
MATCH (source:CWE {name: "Inconsistent cryptocurrency regulation across"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:ENABLES]->(target)


// ========== NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "spear-phishing",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "potential manipulation",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "concern amplification",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "amplification",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: WEAKNESS
MERGE (e_7:WEAKNESS {
    name: "weakness",
    type: "WEAKNESS"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_8:CWE {
    name: "International election security standard development and implementation coordination Response Coordi",
    type: "CWE"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_9:CWE {
    name: "Blockchain-based election verification and audit trail technology development Quantum-Resistant Cryp",
    type: "CWE"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_10:CAPEC {
    name: "practice sharing",
    type: "CAPEC"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_11:CAPEC {
    name: "Comprehensive analysis",
    type: "CAPEC"
})
WITH e_11
MATCH (doc:Document {name: "NCC-OTCE-EAB-028-COZY-BEAR-ELECTION-Enhanced.md.docx"})
CREATE (e_11)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:CAPEC {name: "Comprehensive analysis"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:WEAKNESS {name: "weakness"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:WEAKNESS {name: "weakness"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "protocol abuse",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "manipulation during",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Protocol Manipulation",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "protocol vulnerability",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "dependency analysis",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-029-SANDWORM-ENERGY-GRID-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "Vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Protocol Manipulation"})
MATCH (target:CAPEC {name: "protocol vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "dependency analysis",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Medication dispensing",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_5:CWE {
    name: "Components",
    type: "CWE"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "damage amplification",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "similarity analysis",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "Malware Analysis",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-030-LOCKBIT-4-HEALTHCARE-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "devastating",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "critical manufacturing",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "protocol manipulation",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_4:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "manipulation during",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "Infrastructure Manufacturing",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "protocol analysis",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_8:CAPEC {
    name: "warfare expansion",
    type: "CAPEC"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-031-BLACKCAT-DRAGONFORCE-ALLIANCE-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:CAPEC {name: "protocol manipulation"})
MATCH (target:CAPEC {name: "critical manufacturing"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "spear-phishing",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "disruptions during peak",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "probing",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "system manipulation",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "system manipulation during",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-032-RHYSIDA-GOVERNMENT-SECTOR-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:CWE {name: "20"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "probing"})
MATCH (target:CAPEC {name: "system manipulation"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "devastating",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "spear-phishing",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "dependency exploitation",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "dependency manipulation and access blocking",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "exploitation demonstrating",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_8:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-033-ROYAL-RANSOMWARE-MSP-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "exploitation demonstrating"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "exploitation demonstrating"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "Discovery during",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "trusted software",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "detection evasion",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Software distribution",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_5:CWE {
    name: "20",
    type: "CWE"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "provider infrastructure abuse",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "capability abuse",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_8:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_9:CAPEC {
    name: "infrastructure software",
    type: "CAPEC"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-034-SOLARWINDS-NETWORK-MONITORING-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "Akira Manufacturing",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "credential abuse",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "protocol abuse",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "process manipulation",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_5:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_6:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "Critical manufacturing",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-035-AKIRA-MANUFACTURING-EXTORTION-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Relationship: USES
MATCH (source:CAPEC {name: "protocol abuse"})
MATCH (target:CAPEC {name: "process manipulation"})
MERGE (source)-[:USES]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:CAPEC {name: "Critical manufacturing"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Critical manufacturing"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Critical manufacturing"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-036-APT29-CLOUD-RECONNAISSANCE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-036-APT29-CLOUD-RECONNAISSANCE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "20",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-036-APT29-CLOUD-RECONNAISSANCE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-036-APT29-CLOUD-RECONNAISSANCE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-037-PLAY-EDUCATION-RANSOMWARE-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-037-PLAY-EDUCATION-RANSOMWARE-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-037-PLAY-EDUCATION-RANSOMWARE-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "education",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-037-PLAY-EDUCATION-RANSOMWARE-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "voice phishing",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "67",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "20",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Voice Phishing",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "Spear Phishing",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "Targeted phishing",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_7:CAPEC {
    name: "protocol abuse",
    type: "CAPEC"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_8:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-038-SCATTERED-SPIDER-SOCIAL-ENGINEERING-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Spear Phishing"})
MATCH (target:CAPEC {name: "Spear Phishing"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_2:CAPEC {
    name: "amplification",
    type: "CAPEC"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "Vulnerability Discovery",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "Vendor software",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_5:CAPEC {
    name: "targeted spear phishing",
    type: "CAPEC"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "dependency analysis",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_7:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-039-CL0P-SUPPLY-CHAIN-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "amplification"})
MERGE (source)-[:TARGETS]->(target)


// Relationship: TARGETS
MATCH (source:CAPEC {name: "Vendor software"})
MATCH (target:CAPEC {name: "targeted spear phishing"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-040-APT31-GOVERNMENT-EMAIL-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-040-APT31-GOVERNMENT-EMAIL-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "credential abuse",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-040-APT31-GOVERNMENT-EMAIL-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-040-APT31-GOVERNMENT-EMAIL-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_3:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-040-APT31-GOVERNMENT-EMAIL-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "targeted spear phishing",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-040-APT31-GOVERNMENT-EMAIL-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Relationship: USES
MATCH (source:CAPEC {name: "credential abuse"})
MATCH (target:CWE {name: "20"})
MERGE (source)-[:USES]->(target)


// Relationship: USES
MATCH (source:CWE {name: "20"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:USES]->(target)


// ========== NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CAPEC
MERGE (e_1:CAPEC {
    name: "Vulnerability Analysis",
    type: "CAPEC"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "spear phishing",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_4:CWE {
    name: "next-generation ransomware a7b2c5d8e1f3a6b9c4d7e2f5a8b3c6d9e4f7a1b5c8d2e4f7a3b6c9d5e8f1a4b7: Advance",
    type: "CWE"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_5:CWE {
    name: "Build critical infrastructure resilience against advanced ransomware Advanced Threat Hunting Next-Ge",
    type: "CWE"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_6:CAPEC {
    name: "cryptocurrency",
    type: "CAPEC"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-041-LOCKBIT-BLACK-SUCCESSOR-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "spear phishing"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: USES
MATCH (source:CAPEC {name: "Vulnerability Analysis"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:USES]->(target)


// Relationship: USES
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:USES]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "vulnerability"})
MATCH (target:CAPEC {name: "spear phishing"})
MERGE (source)-[:TARGETS]->(target)


// ========== NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "20",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_3:CWE {
    name: "Analysis of cross-chain bridge protocols and",
    type: "CWE"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_4:CAPEC {
    name: "protocol exploitation",
    type: "CAPEC"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_5:CWE {
    name: "Use of advanced cryptocurrency mixing services and privacy coins Decentralized Exchange Trading: Com",
    type: "CWE"
})
WITH e_5
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_5)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_6:CWE {
    name: "Use of cross-chain transfers for transaction trail obfuscation Privacy Coin Utilization: Use of priv",
    type: "CWE"
})
WITH e_6
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_6)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_7:CWE {
    name: "Analysis of blockchain transactions and cryptocurrency flow patterns Smart Contract Auditing: Detail",
    type: "CWE"
})
WITH e_7
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_7)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_8:CWE {
    name: "Use of blockchain networks for command and control communication Decentralized C2: Utilization of de",
    type: "CWE"
})
WITH e_8
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_8)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_9:CAPEC {
    name: "flash loan",
    type: "CAPEC"
})
WITH e_9
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_9)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_10:CAPEC {
    name: "cryptocurrency tracking",
    type: "CAPEC"
})
WITH e_10
MATCH (doc:Document {name: "NCC-OTCE-EAB-042-LAZARUS-WEB3-DEFI-Enhanced.md.docx"})
CREATE (e_10)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-043-VOLT-TYPHOON-TRANSPORTATION-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-043-VOLT-TYPHOON-TRANSPORTATION-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: CWE
MERGE (e_1:CWE {
    name: "Initial critical infrastructure reconnaissance and capability development 2023: First major infrastr",
    type: "CWE"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-043-VOLT-TYPHOON-TRANSPORTATION-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: CWE
MERGE (e_2:CWE {
    name: "20",
    type: "CWE"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-043-VOLT-TYPHOON-TRANSPORTATION-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Entity: CAPEC
MERGE (e_3:CAPEC {
    name: "credential abuse",
    type: "CAPEC"
})
WITH e_3
MATCH (doc:Document {name: "NCC-OTCE-EAB-043-VOLT-TYPHOON-TRANSPORTATION-Enhanced.md.docx"})
CREATE (e_3)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_4:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_4
MATCH (doc:Document {name: "NCC-OTCE-EAB-043-VOLT-TYPHOON-TRANSPORTATION-Enhanced.md.docx"})
CREATE (e_4)-[:MENTIONED_IN]->(doc)


// ========== NCC-OTCE-EAB-044-IRANIAN-APT-UTILITIES-SCADA-Enhanced.md.docx ==========


// Document Node
CREATE (doc:Document {
    name: "NCC-OTCE-EAB-044-IRANIAN-APT-UTILITIES-SCADA-Enhanced.md.docx",
    type: "Express_Attack_Brief",
    processed_date: date()
})


// Entity: VULNERABILITY
MERGE (e_1:VULNERABILITY {
    name: "vulnerability",
    type: "VULNERABILITY"
})
WITH e_1
MATCH (doc:Document {name: "NCC-OTCE-EAB-044-IRANIAN-APT-UTILITIES-SCADA-Enhanced.md.docx"})
CREATE (e_1)-[:MENTIONED_IN]->(doc)


// Entity: VULNERABILITY
MERGE (e_2:VULNERABILITY {
    name: "Vulnerability",
    type: "VULNERABILITY"
})
WITH e_2
MATCH (doc:Document {name: "NCC-OTCE-EAB-044-IRANIAN-APT-UTILITIES-SCADA-Enhanced.md.docx"})
CREATE (e_2)-[:MENTIONED_IN]->(doc)


// Relationship: EXPLOITS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:EXPLOITS]->(target)


// Relationship: USES
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:USES]->(target)


// Relationship: TARGETS
MATCH (source:VULNERABILITY {name: "Vulnerability"})
MATCH (target:VULNERABILITY {name: "vulnerability"})
MERGE (source)-[:TARGETS]->(target)

