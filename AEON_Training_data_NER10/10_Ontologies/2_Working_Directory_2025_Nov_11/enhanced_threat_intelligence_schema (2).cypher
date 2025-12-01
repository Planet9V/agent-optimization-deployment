
// =============================================================================
// ENHANCED CRITICAL INFRASTRUCTURE THREAT INTELLIGENCE SCHEMA
// Comprehensive coverage of all critical sectors with academic research integration
// =============================================================================

// -----------------------------------------------------------------------------
// CRITICAL INFRASTRUCTURE SECTOR COVERAGE
// -----------------------------------------------------------------------------

CREATE CONSTRAINT sector_id IF NOT EXISTS FOR (s:CriticalSector) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT subsector_id IF NOT EXISTS FOR (ss:SubSector) REQUIRE ss.id IS UNIQUE;

// NIST Critical Infrastructure Sectors (16 sectors)
CREATE (:CriticalSector {
    id: 'sector_energy',
    name: 'Energy Sector',
    nist_category: 'Energy',
    criticality: 'Extreme',
    subsectors: ['Electricity', 'Oil', 'Natural Gas', 'Renewables'],
    regulatory_frameworks: ['NERC CIP', 'FERC', 'DOE Guidelines'],
    threat_landscape: 'High',
    recovery_time_objective: '4 hours'
});

CREATE (:CriticalSector {
    id: 'sector_water',
    name: 'Water and Wastewater Systems',
    nist_category: 'Water',
    criticality: 'Extreme',
    subsectors: ['Drinking Water', 'Wastewater Treatment', 'Stormwater'],
    regulatory_frameworks: ['EPA', 'AWWA Standards'],
    threat_landscape: 'Medium-High',
    recovery_time_objective: '8 hours'
});

CREATE (:CriticalSector {
    id: 'sector_transportation',
    name: 'Transportation Systems',
    nist_category: 'Transportation',
    criticality: 'High',
    subsectors: ['Aviation', 'Rail', 'Highway', 'Maritime', 'Pipeline'],
    regulatory_frameworks: ['TSA', 'FAA', 'FRA', 'PHMSA'],
    threat_landscape: 'Medium',
    recovery_time_objective: '12 hours'
});

CREATE (:CriticalSector {
    id: 'sector_communications',
    name: 'Communications',
    nist_category: 'Communications',
    criticality: 'High',
    subsectors: ['Telecom', 'Internet', 'Broadcasting', 'Satellite'],
    regulatory_frameworks: ['FCC', 'NTIA'],
    threat_landscape: 'High',
    recovery_time_objective: '2 hours'
});

// Additional sectors: Financial, Healthcare, Emergency Services, etc.

// -----------------------------------------------------------------------------
// COMPREHENSIVE VULNERABILITY MANAGEMENT (CVE/CAPEC/CWE)
// -----------------------------------------------------------------------------

CREATE CONSTRAINT cve_id IF NOT EXISTS FOR (c:CVE) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT capec_id IF NOT EXISTS FOR (c:CAPEC) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT cwe_id IF NOT EXISTS FOR (c:CWE) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT epss_id IF NOT EXISTS FOR (e:EPSS) REQUIRE e.id IS UNIQUE;

// CVE Nodes with Enhanced Details
CREATE (:CVE {
    id: 'CVE-2023-12345',
    cve_id: 'CVE-2023-12345',
    description: 'Buffer overflow in industrial PLC firmware allows remote code execution',
    severity: 'CRITICAL',
    cvss_score: 9.8,
    cvss_vector: 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
    published_date: '2023-05-15',
    last_modified: '2023-05-20',
    exploit_available: true,
    exploit_maturity: 'WEAPONIZED',
    patch_available: false,
    remediation_deadline: '2023-08-15',
    affected_versions: ['V1.0-V2.5'],
    vendor_advisory: 'Vendor-Specific Advisory ID',
    references: ['https://nvd.nist.gov/vuln/detail/CVE-2023-12345']
});

// CAPEC (Common Attack Pattern Enumeration and Classification)
CREATE (:CAPEC {
    id: 'capec_100',
    capec_id: 'CAPEC-100',
    name: 'Buffer Overflow via Environment Variables',
    abstraction: 'Standard',
    status: 'Draft',
    description: 'Attackers exploit buffer overflow vulnerabilities...',
    likelihood: 'High',
    severity: 'High',
    prerequisites: ['Target software must have buffer overflow vulnerability'],
    mitigations: ['Input validation', 'Bounds checking', 'Memory protection'],
    related_weaknesses: ['CWE-119', 'CWE-120']
});

// CWE (Common Weakness Enumeration)
CREATE (:CWE {
    id: 'cwe_119',
    cwe_id: 'CWE-119',
    name: 'Improper Restriction of Operations within the Bounds of a Memory Buffer',
    abstraction: 'Class',
    status: 'Incomplete',
    description: 'The software performs operations on a memory buffer...',
    likelihood: 'High',
    consequences: ['Execute unauthorized code', 'Modify memory', 'Read memory'],
    detection_methods: ['Manual analysis', 'Automated static analysis'],
    potential_mitigations: ['Use safe string functions', 'Bounds checking']
});

// EPSS (Exploit Prediction Scoring System)
CREATE (:EPSS {
    id: 'epss_2023_12345',
    cve_id: 'CVE-2023-12345',
    epss_score: 0.975,
    percentile: 0.99,
    prediction_date: '2023-05-16',
    confidence_interval: [0.95, 0.99],
    model_version: 'v2023.01.01'
});

// -----------------------------------------------------------------------------
// MITRE ATT&CK FRAMEWORK COMPREHENSIVE COVERAGE
// -----------------------------------------------------------------------------

CREATE CONSTRAINT tactic_id IF NOT EXISTS FOR (t:Tactic) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT technique_id IF NOT EXISTS FOR (t:Technique) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT subtechnique_id IF NOT EXISTS FOR (st:SubTechnique) REQUIRE st.id IS UNIQUE;

// MITRE ATT&CK Tactics
CREATE (:Tactic {
    id: 'tactic_ta0043',
    tactic_id: 'TA0043',
    name: 'Reconnaissance',
    description: 'The adversary is trying to gather information...',
    phase: 'Pre-attack',
    platform: ['Enterprise', 'ICS', 'Mobile'],
    version: 'v12',
    created: '2023-01-01',
    modified: '2023-06-01'
});

// MITRE ATT&CK Techniques
CREATE (:Technique {
    id: 'technique_t1595',
    technique_id: 'T1595',
    name: 'Active Scanning',
    description: 'Adversaries may execute active reconnaissance scans...',
    tactic: 'Reconnaissance',
    platform: ['Enterprise', 'ICS'],
    data_sources: ['Network Traffic', 'Packet Capture'],
    detection: ['Network monitoring', 'IDS/IPS alerts'],
    mitigation: ['Network segmentation', 'Port security']
});

// MITRE ATT&CK Sub-techniques
CREATE (:SubTechnique {
    id: 'subtechnique_t1595.001',
    subtechnique_id: 'T1595.001',
    name: 'Scanning IP Blocks',
    description: 'Adversaries may scan victim IP blocks...',
    parent_technique: 'T1595',
    platform: ['Enterprise', 'ICS'],
    data_sources: ['Network Traffic'],
    detection: ['Port scan detection'],
    mitigation: ['Firewall rules', 'Rate limiting']
});

// -----------------------------------------------------------------------------
// THREAT INTELLIGENCE AND CONTEMPORARY THREATS
// -----------------------------------------------------------------------------

CREATE CONSTRAINT threat_actor_id IF NOT EXISTS FOR (ta:ThreatActor) REQUIRE ta.id IS UNIQUE;
CREATE CONSTRAINT campaign_id IF NOT EXISTS FOR (c:Campaign) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT ioc_id IF NOT EXISTS FOR (i:IOC) REQUIRE i.id IS UNIQUE;
CREATE CONSTRAINT ttp_id IF NOT EXISTS FOR (t:TTP) REQUIRE t.id IS UNIQUE;

// Threat Actors
CREATE (:ThreatActor {
    id: 'ta_apt29',
    name: 'APT29',
    aliases: ['Cozy Bear', 'The Dukes'],
    country: 'Russia',
    motivation: 'Espionage',
    target_sectors: ['Government', 'Energy', 'Defense'],
    sophistication: 'Advanced',
    first_seen: '2008',
    attribution_confidence: 'High',
    mitre_group_id: 'G0016'
});

// Campaigns
CREATE (:Campaign {
    id: 'campaign_solarwinds',
    name: 'SolarWinds Campaign',
    threat_actors: ['APT29'],
    start_date: '2020-03-01',
    end_date: '2020-12-13',
    target_sectors: ['Government', 'Technology', 'Energy'],
    impact: 'Significant',
    iocs_count: 150,
    ttps_count: 45,
    attribution_confidence: 'High'
});

// Indicators of Compromise (IOCs)
CREATE (:IOC {
    id: 'ioc_malware_hash',
    type: 'File Hash',
    value: 'a1b2c3d4e5f6...',
    hash_type: 'SHA256',
    malware_family: 'Sunburst',
    first_seen: '2020-03-15',
    last_seen: '2020-12-13',
    confidence: 'High',
    source: 'FireEye',
    tags: ['SolarWinds', 'APT29', 'Backdoor']
});

// TTPs (Tactics, Techniques, and Procedures)
CREATE (:TTP {
    id: 'ttp_sunburst_backdoor',
    name: 'Sunburst Backdoor Communication',
    description: 'Malware communicates with C2 using DNS over HTTPS',
    techniques: ['T1071.001', 'T1568.002'],
    detection_rules: ['Sigma', 'YARA', 'Snort'],
    mitigation: ['Network monitoring', 'DNS filtering'],
    references: ['MITRE ATT&CK', 'CISA Alert AA20-352A']
});

// -----------------------------------------------------------------------------
// ACADEMIC RESEARCH AND THREAT REPORTS
// -----------------------------------------------------------------------------

CREATE CONSTRAINT research_paper_id IF NOT EXISTS FOR (rp:ResearchPaper) REQUIRE rp.id IS UNIQUE;
CREATE CONSTRAINT threat_report_id IF NOT EXISTS FOR (tr:ThreatReport) REQUIRE tr.tr IS UNIQUE;
CREATE CONSTRAINT conference_id IF NOT EXISTS FOR (c:Conference) REQUIRE c.id IS UNIQUE;

// Academic Research Papers
CREATE (:ResearchPaper {
    id: 'paper_ics_cybersecurity_2023',
    title: 'Advanced Persistent Threats in Industrial Control Systems',
    authors: ['Dr. Smith, J.', 'Prof. Johnson, A.'],
    publication: 'IEEE Transactions on Industrial Informatics',
    year: 2023,
    doi: '10.1109/TII.2023.1234567',
    abstract: 'This paper analyzes APT campaigns targeting ICS...',
    keywords: ['ICS', 'APT', 'Cybersecurity', 'Critical Infrastructure'],
    citation_count: 45,
    impact_factor: 8.5,
    references: ['CVE-2023-12345', 'CAPEC-100', 'T1595']
});

// Threat Intelligence Reports
CREATE (:ThreatReport {
    id: 'report_cisa_aa23_123a',
    title: 'Russian State-Sponsored Cyber Threats to Critical Infrastructure',
    publisher: 'CISA',
    report_id: 'AA23-123A',
    publication_date: '2023-05-15',
    threat_level: 'HIGH',
    target_sectors: ['Energy', 'Water', 'Transportation'],
    key_findings: ['Increased targeting of OT systems', 'New TTPs observed'],
    recommendations: ['Implement network segmentation', 'Update incident response plans'],
    iocs: ['ioc_malware_hash'],
    ttps: ['ttp_sunburst_backdoor']
});

// Security Conferences
CREATE (:Conference {
    id: 'conf_blackhat_2023',
    name: 'Black Hat USA 2023',
    location: 'Las Vegas, NV',
    date: '2023-08-05',
    tracks: ['ICS Security', 'Threat Intelligence', 'Vulnerability Research'],
    key_speakers: ['Industry experts', 'Government officials'],
    proceedings: ['paper_ics_cybersecurity_2023']
});

// -----------------------------------------------------------------------------
// ENHANCED RELATIONSHIPS FOR COMPREHENSIVE MODELING
// -----------------------------------------------------------------------------

// Sector to Infrastructure Mapping
MATCH (s:CriticalSector {id: 'sector_energy'}), (f:Facility {id: 'facility_001'})
CREATE (f)-[:BELONGS_TO_SECTOR {
    relationship_type: 'Facility-Sector',
    criticality_weight: 0.9,
    regulatory_compliance: 'NERC CIP',
    audit_frequency: 'Quarterly'
}]->(s);

// CVE to CAPEC to CWE Chain
MATCH (cve:CVE {id: 'CVE-2023-12345'}), (capec:CAPEC {id: 'capec_100'})
CREATE (cve)-[:EXPLOITED_BY_PATTERN {
    relationship_type: 'CVE-CAPEC',
    exploit_complexity: 'Low',
    reliability: 'High',
    references: ['NVD', 'MITRE']
}]->(capec);

MATCH (capec:CAPEC {id: 'capec_100'}), (cwe:CWE {id: 'cwe_119'})
CREATE (capec)-[:EXPLOITS_WEAKNESS {
    relationship_type: 'CAPEC-CWE',
    mapping_confidence: 'High',
    mitigation_alignment: true
}]->(cwe);

// MITRE ATT&CK Framework Relationships
MATCH (tactic:Tactic {id: 'tactic_ta0043'}), (tech:Technique {id: 'technique_t1595'})
CREATE (tech)-[:PART_OF_TACTIC {
    relationship_type: 'Technique-Tactic',
    phase_order: 1,
    detection_priority: 'Medium'
}]->(tactic);

MATCH (tech:Technique {id: 'technique_t1595'}), (subtech:SubTechnique {id: 'subtechnique_t1595.001'})
CREATE (subtech)-[:SPECIALIZATION_OF {
    relationship_type: 'SubTechnique-Technique',
    specificity_level: 'High',
    detection_coverage: 'Medium'
}]->(tech);

// Threat Intelligence Relationships
MATCH (ta:ThreatActor {id: 'ta_apt29'}), (camp:Campaign {id: 'campaign_solarwinds'})
CREATE (ta)-[:ASSOCIATED_WITH {
    relationship_type: 'Actor-Campaign',
    attribution_confidence: 'High',
    role: 'Primary actor',
    timeframe: '2020'
}]->(camp);

MATCH (camp:Campaign {id: 'campaign_solarwinds'}), (ioc:IOC {id: 'ioc_malware_hash'})
CREATE (camp)-[:USES_IOC {
    relationship_type: 'Campaign-IOC',
    first_seen: '2020-03-15',
    last_seen: '2020-12-13',
    prevalence: 'High'
}]->(ioc);

// Academic Research Integration
MATCH (rp:ResearchPaper {id: 'paper_ics_cybersecurity_2023'}), (cve:CVE {id: 'CVE-2023-12345'})
CREATE (rp)-[:ANALYZES_VULNERABILITY {
    relationship_type: 'Research-CVE',
    analysis_depth: 'Comprehensive',
    novel_insights: true,
    practical_applications: ['Detection rules', 'Mitigation strategies']
}]->(cve);

MATCH (tr:ThreatReport {id: 'report_cisa_aa23_123a'}), (ta:ThreatActor {id: 'ta_apt29'})
CREATE (tr)-[:DOCUMENTS_THREAT {
    relationship_type: 'Report-Actor',
    confidence_level: 'High',
    actionable_intelligence: true,
    classification_level: 'TLP:AMBER'
}]->(ta);

// -----------------------------------------------------------------------------
// PRIORITIZATION AND SCORING MECHANISMS
// -----------------------------------------------------------------------------

// Risk Scoring Algorithm
CREATE (:RiskScoring {
    id: 'risk_algorithm_v1',
    name: 'Critical Infrastructure Risk Prioritization',
    version: '1.0',
    factors: ['CVSS Score', 'EPSS Score', 'Sector Criticality', 'Asset Criticality', 'Threat Landscape'],
    weights: [0.3, 0.25, 0.2, 0.15, 0.1],
    formula: 'Risk = (CVSS * 0.3) + (EPSS * 0.25) + (Sector_Crit * 0.2) + (Asset_Crit * 0.15) + (Threat_Landscape * 0.1)',
    threshold_high: 0.8,
    threshold_medium: 0.5,
    threshold_low: 0.3
});

// Threat Intelligence Prioritization
CREATE (:ThreatPrioritization {
    id: 'threat_priority_v1',
    name: 'Contemporary Threat Prioritization',
    factors: ['Recency', 'Relevance', 'Impact', 'Sophistication', 'Attribution Confidence'],
    time_decay: 0.1, // 10% decay per month
    sector_relevance_weight: 0.3,
    impact_multiplier: 1.5
});

// -----------------------------------------------------------------------------
// ADVANCED INDEXING AND PERFORMANCE OPTIMIZATION
// -----------------------------------------------------------------------------

CREATE INDEX sector_criticality IF NOT EXISTS FOR (s:CriticalSector) ON (s.criticality);
CREATE INDEX cve_severity IF NOT EXISTS FOR (c:CVE) ON (c.severity);
CREATE INDEX cve_cvss_score IF NOT EXISTS FOR (c:CVE) ON (c.cvss_score);
CREATE INDEX epss_score IF NOT EXISTS FOR (e:EPSS) ON (e.epss_score);
CREATE INDEX threat_actor_sophistication IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.sophistication);
CREATE INDEX campaign_impact IF NOT EXISTS FOR (c:Campaign) ON (c.impact);

CREATE FULLTEXT INDEX research_search IF NOT EXISTS FOR (rp:ResearchPaper) ON EACH [rp.title, rp.abstract, rp.keywords];
CREATE FULLTEXT INDEX threat_report_search IF NOT EXISTS FOR (tr:ThreatReport) ON EACH [tr.title, tr.key_findings, tr.recommendations];
CREATE FULLTEXT INDEX cve_search IF NOT EXISTS FOR (c:CVE) ON EACH [c.cve_id, c.description];

// -----------------------------------------------------------------------------
// COMPREHENSIVE QUERY EXAMPLES FOR THREAT ANALYSIS
// -----------------------------------------------------------------------------

// 1. High-Risk Vulnerabilities by Sector
/*
MATCH (s:CriticalSector)<-[:BELONGS_TO_SECTOR]-(f:Facility)<-[:LOCATED_IN]-(sys:System)<-[:PART_OF]-(a:PhysicalAsset)
MATCH (a)<-[:AFFECTS]-(v:CVE)
MATCH (v)-[:HAS_EPSS]->(e:EPSS)
WHERE v.cvss_score >= 7.0 AND e.epss_score >= 0.7
RETURN s.name AS Sector, v.cve_id, v.cvss_score, e.epss_score, a.name AS Asset
ORDER BY (v.cvss_score * 0.3 + e.epss_score * 0.25 + s.criticality_weight * 0.2 + a.criticality * 0.15) DESC
*/

// 2. Contemporary Threat Campaign Analysis
/*
MATCH (ta:ThreatActor)-[:ASSOCIATED_WITH]->(c:Campaign)-[:USES_IOC]->(i:IOC)
MATCH (c)-[:USES_TTP]->(ttp:TTP)-[:MAPS_TO_TECHNIQUE]->(tech:Technique)
MATCH (tech)-[:PART_OF_TACTIC]->(tactic:Tactic)
WHERE c.start_date >= date('2023-01-01')
RETURN ta.name AS ThreatActor, c.name AS Campaign, tactic.name AS Tactic,
       COUNT(DISTINCT i) AS IOCs, COUNT(DISTINCT ttp) AS TTPs
ORDER BY c.impact DESC, COUNT(DISTINCT i) DESC
*/

// 3. Academic Research Impact on Threat Intelligence
/*
MATCH (rp:ResearchPaper)-[:ANALYZES_VULNERABILITY]->(v:CVE)
MATCH (v)<-[:EXPLOITS]-(t:Threat)-[:USED_BY]->(ta:ThreatActor)
MATCH (rp)-[:PRESENTED_AT]->(conf:Conference)
WHERE rp.year >= 2022 AND rp.citation_count >= 10
RETURN rp.title AS Research, v.cve_id, ta.name AS ThreatActor,
       conf.name AS Conference, rp.citation_count AS Citations
ORDER BY rp.citation_count DESC, rp.impact_factor DESC
*/

// 4. Multi-Sector Cascading Threat Analysis
/*
MATCH path = (ta:ThreatActor)-[:ASSOCIATED_WITH]->(c:Campaign)-[:TARGETS_SECTOR]->(s:CriticalSector)
MATCH (s)<-[:BELONGS_TO_SECTOR]-(f:Facility)<-[:LOCATED_IN]-(sys:System)<-[:PART_OF]-(a:PhysicalAsset)
MATCH (a)<-[:AFFECTS]-(v:CVE)<-[:EXPLOITS]-(t:Threat)
WHERE s.criticality IN ['Extreme', 'High']
RETURN ta.name AS Actor, s.name AS Sector, COUNT(DISTINCT v) AS Vulnerabilities,
       AVG(v.cvss_score) AS Avg_CVSS, MAX(s.criticality) AS Sector_Criticality
ORDER BY COUNT(DISTINCT v) DESC, AVG(v.cvss_score) DESC
*/
