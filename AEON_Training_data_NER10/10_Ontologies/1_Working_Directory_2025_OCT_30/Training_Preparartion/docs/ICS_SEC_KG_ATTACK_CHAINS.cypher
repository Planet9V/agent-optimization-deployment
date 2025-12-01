// ICS-SEC-KG Attack Chain Import
// Generated from ICS-SEC-KG OWL Ontology
// Week 1 Proof-of-Concept: Complete CVE→ATT&CK Chains

// Create indexes for performance
CREATE INDEX IF NOT EXISTS FOR (n:CVE) ON (n.id);
CREATE INDEX IF NOT EXISTS FOR (n:CWE) ON (n.id);
CREATE INDEX IF NOT EXISTS FOR (n:CAPEC) ON (n.capecId);
CREATE INDEX IF NOT EXISTS FOR (n:AttackTechnique) ON (n.techniqueId);

// Import 0 complete attack chains