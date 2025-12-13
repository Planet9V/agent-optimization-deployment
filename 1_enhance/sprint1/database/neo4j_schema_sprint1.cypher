// ═══════════════════════════════════════════════════════════════════════════
// AEON DT Neo4j Schema - Sprint 1 Implementation
// Created: 2025-12-12
// Purpose: Core schema for SBOM, Equipment, and EOL tracking
// ═══════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────
// STEP 1: Clear Existing Schema (Development Only - Comment Out for Production)
// ───────────────────────────────────────────────────────────────────────────

// MATCH (n) DETACH DELETE n;
// DROP CONSTRAINT IF EXISTS sbom_id_unique;
// DROP CONSTRAINT IF EXISTS component_id_unique;
// DROP CONSTRAINT IF EXISTS cve_id_unique;
// DROP CONSTRAINT IF EXISTS equipment_id_unique;
// DROP CONSTRAINT IF EXISTS vendor_id_unique;
// DROP CONSTRAINT IF EXISTS eol_status_id_unique;

// ───────────────────────────────────────────────────────────────────────────
// STEP 2: Create Constraints (Unique IDs)
// ───────────────────────────────────────────────────────────────────────────

// SBOM Constraints
CREATE CONSTRAINT sbom_id_unique IF NOT EXISTS
FOR (s:SBOM) REQUIRE s.sbom_id IS UNIQUE;

CREATE CONSTRAINT sbom_name_unique IF NOT EXISTS
FOR (s:SBOM) REQUIRE s.name IS UNIQUE;

// Component Constraints
CREATE CONSTRAINT component_id_unique IF NOT EXISTS
FOR (c:Component) REQUIRE c.component_id IS UNIQUE;

// CVE Constraints
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS
FOR (v:CVE) REQUIRE v.cve_id IS UNIQUE;

// Equipment Constraints
CREATE CONSTRAINT equipment_id_unique IF NOT EXISTS
FOR (e:Equipment) REQUIRE e.equipment_id IS UNIQUE;

CREATE CONSTRAINT equipment_serial_unique IF NOT EXISTS
FOR (e:Equipment) REQUIRE (e.serial_number, e.sector) IS UNIQUE;

// Vendor Constraints
CREATE CONSTRAINT vendor_id_unique IF NOT EXISTS
FOR (v:Vendor) REQUIRE v.vendor_id IS UNIQUE;

CREATE CONSTRAINT vendor_name_unique IF NOT EXISTS
FOR (v:Vendor) REQUIRE v.name IS UNIQUE;

// EOL Status Constraints
CREATE CONSTRAINT eol_status_id_unique IF NOT EXISTS
FOR (e:EOLStatus) REQUIRE e.status_id IS UNIQUE;

// ───────────────────────────────────────────────────────────────────────────
// STEP 3: Create Indexes for Performance
// ───────────────────────────────────────────────────────────────────────────

// SBOM Indexes
CREATE INDEX sbom_name_idx IF NOT EXISTS FOR (s:SBOM) ON (s.name);
CREATE INDEX sbom_sector_idx IF NOT EXISTS FOR (s:SBOM) ON (s.sector);
CREATE INDEX sbom_created_idx IF NOT EXISTS FOR (s:SBOM) ON (s.created_at);

// Component Indexes
CREATE INDEX component_name_idx IF NOT EXISTS FOR (c:Component) ON (c.name);
CREATE INDEX component_version_idx IF NOT EXISTS FOR (c:Component) ON (c.version);
CREATE INDEX component_vendor_idx IF NOT EXISTS FOR (c:Component) ON (c.vendor);
CREATE INDEX component_type_idx IF NOT EXISTS FOR (c:Component) ON (c.type);

// CVE Indexes
CREATE INDEX cve_severity_idx IF NOT EXISTS FOR (v:CVE) ON (v.severity);
CREATE INDEX cve_published_idx IF NOT EXISTS FOR (v:CVE) ON (v.published_date);
CREATE INDEX cve_score_idx IF NOT EXISTS FOR (v:CVE) ON (v.cvss_score);

// Equipment Indexes
CREATE INDEX equipment_name_idx IF NOT EXISTS FOR (e:Equipment) ON (e.name);
CREATE INDEX equipment_sector_idx IF NOT EXISTS FOR (e:Equipment) ON (e.sector);
CREATE INDEX equipment_type_idx IF NOT EXISTS FOR (e:Equipment) ON (e.equipment_type);
CREATE INDEX equipment_vendor_idx IF NOT EXISTS FOR (e:Equipment) ON (e.vendor_name);

// Vendor Indexes
CREATE INDEX vendor_name_idx IF NOT EXISTS FOR (v:Vendor) ON (v.name);
CREATE INDEX vendor_sector_idx IF NOT EXISTS FOR (v:Vendor) ON (v.primary_sector);

// EOL Status Indexes
CREATE INDEX eol_status_idx IF NOT EXISTS FOR (e:EOLStatus) ON (e.status);
CREATE INDEX eol_date_idx IF NOT EXISTS FOR (e:EOLStatus) ON (e.eol_date);

// ───────────────────────────────────────────────────────────────────────────
// STEP 4: Create Full-Text Search Indexes
// ───────────────────────────────────────────────────────────────────────────

// Full-text search for SBOM
CALL db.index.fulltext.createNodeIndex(
  "sbomFullText",
  ["SBOM"],
  ["name", "description", "sector"]
) IF NOT EXISTS;

// Full-text search for Components
CALL db.index.fulltext.createNodeIndex(
  "componentFullText",
  ["Component"],
  ["name", "description", "vendor"]
) IF NOT EXISTS;

// Full-text search for Equipment
CALL db.index.fulltext.createNodeIndex(
  "equipmentFullText",
  ["Equipment"],
  ["name", "description", "model", "serial_number"]
) IF NOT EXISTS;

// Full-text search for CVEs
CALL db.index.fulltext.createNodeIndex(
  "cveFullText",
  ["CVE"],
  ["cve_id", "description"]
) IF NOT EXISTS;

// ───────────────────────────────────────────────────────────────────────────
// STEP 5: Sample Data - Vendors
// ───────────────────────────────────────────────────────────────────────────

CREATE (v1:Vendor {
  vendor_id: "VEN-001",
  name: "Microsoft Corporation",
  primary_sector: "all",
  support_email: "support@microsoft.com",
  support_phone: "+1-800-642-7676",
  website: "https://www.microsoft.com",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (v2:Vendor {
  vendor_id: "VEN-002",
  name: "Cisco Systems",
  primary_sector: "defense",
  support_email: "tac@cisco.com",
  support_phone: "+1-800-553-2447",
  website: "https://www.cisco.com",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (v3:Vendor {
  vendor_id: "VEN-003",
  name: "Red Hat, Inc.",
  primary_sector: "all",
  support_email: "support@redhat.com",
  support_phone: "+1-888-733-4281",
  website: "https://www.redhat.com",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (v4:Vendor {
  vendor_id: "VEN-004",
  name: "Fortinet",
  primary_sector: "defense",
  support_email: "support@fortinet.com",
  support_phone: "+1-866-648-4638",
  website: "https://www.fortinet.com",
  created_at: datetime(),
  updated_at: datetime()
});

// ───────────────────────────────────────────────────────────────────────────
// STEP 6: Sample Data - Components
// ───────────────────────────────────────────────────────────────────────────

CREATE (c1:Component {
  component_id: "COMP-001",
  name: "Windows Server",
  version: "2022",
  vendor: "Microsoft Corporation",
  type: "operating_system",
  description: "Enterprise server operating system",
  license: "Commercial",
  cpe: "cpe:2.3:o:microsoft:windows_server:2022:*:*:*:*:*:*:*",
  purl: "pkg:windows/windows-server@2022",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (c2:Component {
  component_id: "COMP-002",
  name: "IOS XE",
  version: "17.9.3",
  vendor: "Cisco Systems",
  type: "firmware",
  description: "Cisco network device operating system",
  license: "Commercial",
  cpe: "cpe:2.3:o:cisco:ios_xe:17.9.3:*:*:*:*:*:*:*",
  purl: "pkg:cisco/ios-xe@17.9.3",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (c3:Component {
  component_id: "COMP-003",
  name: "OpenSSL",
  version: "3.0.8",
  vendor: "OpenSSL Project",
  type: "library",
  description: "Cryptographic library",
  license: "Apache-2.0",
  cpe: "cpe:2.3:a:openssl:openssl:3.0.8:*:*:*:*:*:*:*",
  purl: "pkg:github/openssl/openssl@3.0.8",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (c4:Component {
  component_id: "COMP-004",
  name: "Red Hat Enterprise Linux",
  version: "8.7",
  vendor: "Red Hat, Inc.",
  type: "operating_system",
  description: "Enterprise Linux distribution",
  license: "Commercial",
  cpe: "cpe:2.3:o:redhat:enterprise_linux:8.7:*:*:*:*:*:*:*",
  purl: "pkg:rpm/redhat/rhel@8.7",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (c5:Component {
  component_id: "COMP-005",
  name: "Apache",
  version: "2.4.57",
  vendor: "Apache Software Foundation",
  type: "web_server",
  description: "HTTP server",
  license: "Apache-2.0",
  cpe: "cpe:2.3:a:apache:http_server:2.4.57:*:*:*:*:*:*:*",
  purl: "pkg:github/apache/httpd@2.4.57",
  created_at: datetime(),
  updated_at: datetime()
});

// ───────────────────────────────────────────────────────────────────────────
// STEP 7: Sample Data - CVEs
// ───────────────────────────────────────────────────────────────────────────

CREATE (cve1:CVE {
  cve_id: "CVE-2023-36884",
  description: "Windows Search Remote Code Execution Vulnerability",
  severity: "CRITICAL",
  cvss_score: 9.8,
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  published_date: date("2023-07-11"),
  last_modified: date("2023-07-15"),
  cwe_id: "CWE-94",
  references: [
    "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-36884"
  ],
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (cve2:CVE {
  cve_id: "CVE-2023-20273",
  description: "Cisco IOS XE Web UI Privilege Escalation Vulnerability",
  severity: "HIGH",
  cvss_score: 7.2,
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H",
  published_date: date("2023-09-27"),
  last_modified: date("2023-10-02"),
  cwe_id: "CWE-269",
  references: [
    "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-iosxe-webui-privesc-j22SaA4z"
  ],
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (cve3:CVE {
  cve_id: "CVE-2023-0464",
  description: "OpenSSL X.509 Certificate Validation Vulnerability",
  severity: "HIGH",
  cvss_score: 7.5,
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
  published_date: date("2023-03-22"),
  last_modified: date("2023-03-28"),
  cwe_id: "CWE-295",
  references: [
    "https://www.openssl.org/news/secadv/20230322.txt"
  ],
  created_at: datetime(),
  updated_at: datetime()
});

// ───────────────────────────────────────────────────────────────────────────
// STEP 8: Sample Data - Equipment
// ───────────────────────────────────────────────────────────────────────────

CREATE (e1:Equipment {
  equipment_id: "EQ-001",
  name: "Primary Domain Controller",
  equipment_type: "server",
  sector: "defense",
  vendor_name: "Microsoft Corporation",
  model: "Windows Server 2022",
  serial_number: "SRV-DC-001",
  location: "Data Center Alpha",
  criticality: "HIGH",
  status: "active",
  purchase_date: date("2023-01-15"),
  warranty_expiration: date("2026-01-15"),
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (e2:Equipment {
  equipment_id: "EQ-002",
  name: "Core Router",
  equipment_type: "network_device",
  sector: "defense",
  vendor_name: "Cisco Systems",
  model: "Catalyst 9300",
  serial_number: "NET-RTR-002",
  location: "Network Operations Center",
  criticality: "CRITICAL",
  status: "active",
  purchase_date: date("2022-06-20"),
  warranty_expiration: date("2025-06-20"),
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (e3:Equipment {
  equipment_id: "EQ-003",
  name: "Web Application Server",
  equipment_type: "server",
  sector: "civilian",
  vendor_name: "Red Hat, Inc.",
  model: "RHEL 8.7",
  serial_number: "SRV-WEB-003",
  location: "Public Services DMZ",
  criticality: "MEDIUM",
  status: "active",
  purchase_date: date("2023-03-10"),
  warranty_expiration: date("2026-03-10"),
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (e4:Equipment {
  equipment_id: "EQ-004",
  name: "Perimeter Firewall",
  equipment_type: "security_appliance",
  sector: "defense",
  vendor_name: "Fortinet",
  model: "FortiGate 600E",
  serial_number: "SEC-FW-004",
  location: "Network Perimeter",
  criticality: "CRITICAL",
  status: "active",
  purchase_date: date("2022-11-01"),
  warranty_expiration: date("2025-11-01"),
  created_at: datetime(),
  updated_at: datetime()
});

// ───────────────────────────────────────────────────────────────────────────
// STEP 9: Sample Data - SBOM
// ───────────────────────────────────────────────────────────────────────────

CREATE (s1:SBOM {
  sbom_id: "SBOM-001",
  name: "Defense Infrastructure SBOM",
  sector: "defense",
  sbom_version: "1.0",
  spec_version: "SPDX-2.3",
  description: "Complete software inventory for defense sector infrastructure",
  organization: "AEON Defense Technology",
  contact: "sbom@aeon-defense.mil",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (s2:SBOM {
  sbom_id: "SBOM-002",
  name: "Civilian Services SBOM",
  sector: "civilian",
  sbom_version: "1.0",
  spec_version: "SPDX-2.3",
  description: "Software inventory for civilian government services",
  organization: "AEON Civilian Technology",
  contact: "sbom@aeon-civilian.gov",
  created_at: datetime(),
  updated_at: datetime()
});

// ───────────────────────────────────────────────────────────────────────────
// STEP 10: Sample Data - EOL Status
// ───────────────────────────────────────────────────────────────────────────

CREATE (eol1:EOLStatus {
  status_id: "EOL-001",
  status: "active",
  eol_date: date("2026-10-13"),
  eos_date: date("2027-10-13"),
  extended_support_available: true,
  extended_support_cost: 15000.00,
  replacement_recommended: false,
  notes: "Mainstream support until 2026, extended support available",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (eol2:EOLStatus {
  status_id: "EOL-002",
  status: "approaching_eol",
  eol_date: date("2024-06-30"),
  eos_date: date("2025-06-30"),
  extended_support_available: true,
  extended_support_cost: 25000.00,
  replacement_recommended: true,
  notes: "End of life approaching, plan replacement",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (eol3:EOLStatus {
  status_id: "EOL-003",
  status: "active",
  eol_date: date("2029-05-31"),
  eos_date: date("2030-05-31"),
  extended_support_available: true,
  extended_support_cost: 10000.00,
  replacement_recommended: false,
  notes: "Long-term support available",
  created_at: datetime(),
  updated_at: datetime()
});

CREATE (eol4:EOLStatus {
  status_id: "EOL-004",
  status: "active",
  eol_date: date("2025-11-01"),
  eos_date: date("2026-11-01"),
  extended_support_available: true,
  extended_support_cost: 20000.00,
  replacement_recommended: false,
  notes: "Standard support lifecycle",
  created_at: datetime(),
  updated_at: datetime()
});

// ───────────────────────────────────────────────────────────────────────────
// STEP 11: Create Relationships - SBOM to Components
// ───────────────────────────────────────────────────────────────────────────

MATCH (s:SBOM {sbom_id: "SBOM-001"}), (c:Component {component_id: "COMP-001"})
CREATE (s)-[:HAS_COMPONENT {added_date: datetime()}]->(c);

MATCH (s:SBOM {sbom_id: "SBOM-001"}), (c:Component {component_id: "COMP-002"})
CREATE (s)-[:HAS_COMPONENT {added_date: datetime()}]->(c);

MATCH (s:SBOM {sbom_id: "SBOM-001"}), (c:Component {component_id: "COMP-003"})
CREATE (s)-[:HAS_COMPONENT {added_date: datetime()}]->(c);

MATCH (s:SBOM {sbom_id: "SBOM-002"}), (c:Component {component_id: "COMP-004"})
CREATE (s)-[:HAS_COMPONENT {added_date: datetime()}]->(c);

MATCH (s:SBOM {sbom_id: "SBOM-002"}), (c:Component {component_id: "COMP-005"})
CREATE (s)-[:HAS_COMPONENT {added_date: datetime()}]->(c);

// ───────────────────────────────────────────────────────────────────────────
// STEP 12: Create Relationships - Component Dependencies
// ───────────────────────────────────────────────────────────────────────────

MATCH (c1:Component {component_id: "COMP-001"}), (c2:Component {component_id: "COMP-003"})
CREATE (c1)-[:DEPENDS_ON {
  dependency_type: "runtime",
  version_constraint: ">=3.0.0",
  required: true
}]->(c2);

MATCH (c1:Component {component_id: "COMP-002"}), (c2:Component {component_id: "COMP-003"})
CREATE (c1)-[:DEPENDS_ON {
  dependency_type: "runtime",
  version_constraint: ">=3.0.0",
  required: true
}]->(c2);

MATCH (c1:Component {component_id: "COMP-004"}), (c2:Component {component_id: "COMP-003"})
CREATE (c1)-[:DEPENDS_ON {
  dependency_type: "runtime",
  version_constraint: ">=3.0.0",
  required: true
}]->(c2);

MATCH (c1:Component {component_id: "COMP-005"}), (c2:Component {component_id: "COMP-003"})
CREATE (c1)-[:DEPENDS_ON {
  dependency_type: "runtime",
  version_constraint: ">=3.0.0",
  required: true
}]->(c2);

// ───────────────────────────────────────────────────────────────────────────
// STEP 13: Create Relationships - Component to CVE
// ───────────────────────────────────────────────────────────────────────────

MATCH (c:Component {component_id: "COMP-001"}), (v:CVE {cve_id: "CVE-2023-36884"})
CREATE (c)-[:HAS_VULNERABILITY {
  discovered_date: date("2023-07-11"),
  patched: false,
  patch_available: true,
  patch_version: "2022-Update-KB5030123"
}]->(v);

MATCH (c:Component {component_id: "COMP-002"}), (v:CVE {cve_id: "CVE-2023-20273"})
CREATE (c)-[:HAS_VULNERABILITY {
  discovered_date: date("2023-09-27"),
  patched: true,
  patch_available: true,
  patch_version: "17.9.4"
}]->(v);

MATCH (c:Component {component_id: "COMP-003"}), (v:CVE {cve_id: "CVE-2023-0464"})
CREATE (c)-[:HAS_VULNERABILITY {
  discovered_date: date("2023-03-22"),
  patched: false,
  patch_available: true,
  patch_version: "3.0.9"
}]->(v);

// ───────────────────────────────────────────────────────────────────────────
// STEP 14: Create Relationships - Equipment to Software
// ───────────────────────────────────────────────────────────────────────────

MATCH (e:Equipment {equipment_id: "EQ-001"}), (c:Component {component_id: "COMP-001"})
CREATE (e)-[:RUNS_SOFTWARE {
  installed_date: date("2023-01-20"),
  is_primary: true
}]->(c);

MATCH (e:Equipment {equipment_id: "EQ-002"}), (c:Component {component_id: "COMP-002"})
CREATE (e)-[:RUNS_SOFTWARE {
  installed_date: date("2022-06-25"),
  is_primary: true
}]->(c);

MATCH (e:Equipment {equipment_id: "EQ-003"}), (c:Component {component_id: "COMP-004"})
CREATE (e)-[:RUNS_SOFTWARE {
  installed_date: date("2023-03-15"),
  is_primary: true
}]->(c);

MATCH (e:Equipment {equipment_id: "EQ-003"}), (c:Component {component_id: "COMP-005"})
CREATE (e)-[:RUNS_SOFTWARE {
  installed_date: date("2023-03-16"),
  is_primary: false
}]->(c);

// ───────────────────────────────────────────────────────────────────────────
// STEP 15: Create Relationships - Equipment to Vendor
// ───────────────────────────────────────────────────────────────────────────

MATCH (e:Equipment {equipment_id: "EQ-001"}), (v:Vendor {vendor_id: "VEN-001"})
CREATE (e)-[:FROM_VENDOR {
  purchase_date: date("2023-01-15"),
  warranty_terms: "3 years standard support"
}]->(v);

MATCH (e:Equipment {equipment_id: "EQ-002"}), (v:Vendor {vendor_id: "VEN-002"})
CREATE (e)-[:FROM_VENDOR {
  purchase_date: date("2022-06-20"),
  warranty_terms: "3 years standard support with 24/7 TAC"
}]->(v);

MATCH (e:Equipment {equipment_id: "EQ-003"}), (v:Vendor {vendor_id: "VEN-003"})
CREATE (e)-[:FROM_VENDOR {
  purchase_date: date("2023-03-10"),
  warranty_terms: "3 years enterprise support"
}]->(v);

MATCH (e:Equipment {equipment_id: "EQ-004"}), (v:Vendor {vendor_id: "VEN-004"})
CREATE (e)-[:FROM_VENDOR {
  purchase_date: date("2022-11-01"),
  warranty_terms: "3 years FortiCare support"
}]->(v);

// ───────────────────────────────────────────────────────────────────────────
// STEP 16: Create Relationships - Equipment to EOL Status
// ───────────────────────────────────────────────────────────────────────────

MATCH (e:Equipment {equipment_id: "EQ-001"}), (eol:EOLStatus {status_id: "EOL-001"})
CREATE (e)-[:HAS_STATUS {
  last_reviewed: date("2025-12-12"),
  next_review: date("2026-06-12")
}]->(eol);

MATCH (e:Equipment {equipment_id: "EQ-002"}), (eol:EOLStatus {status_id: "EOL-002"})
CREATE (e)-[:HAS_STATUS {
  last_reviewed: date("2025-12-12"),
  next_review: date("2024-03-31")
}]->(eol);

MATCH (e:Equipment {equipment_id: "EQ-003"}), (eol:EOLStatus {status_id: "EOL-003"})
CREATE (e)-[:HAS_STATUS {
  last_reviewed: date("2025-12-12"),
  next_review: date("2026-12-12")
}]->(eol);

MATCH (e:Equipment {equipment_id: "EQ-004"}), (eol:EOLStatus {status_id: "EOL-004"})
CREATE (e)-[:HAS_STATUS {
  last_reviewed: date("2025-12-12"),
  next_review: date("2025-05-01")
}]->(eol);

// ═══════════════════════════════════════════════════════════════════════════
// QUERY PATTERNS FOR SPRINT 1 APIS
// ═══════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────
// API-01: Get SBOM by Sector
// ───────────────────────────────────────────────────────────────────────────
// MATCH (s:SBOM {sector: $sector})-[:HAS_COMPONENT]->(c:Component)
// OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:CVE)
// RETURN s.sbom_id, s.name,
//        collect(DISTINCT c.component_id) as components,
//        collect(DISTINCT v.cve_id) as vulnerabilities
// ORDER BY s.created_at DESC;

// ───────────────────────────────────────────────────────────────────────────
// API-02: Get Component Dependencies
// ───────────────────────────────────────────────────────────────────────────
// MATCH (c:Component {component_id: $component_id})-[d:DEPENDS_ON*1..3]->(dep:Component)
// RETURN c.name as component,
//        dep.name as dependency,
//        dep.version as version,
//        length(d) as depth
// ORDER BY depth;

// ───────────────────────────────────────────────────────────────────────────
// API-03: Get Vulnerabilities by Severity
// ───────────────────────────────────────────────────────────────────────────
// MATCH (c:Component)-[r:HAS_VULNERABILITY]->(v:CVE {severity: $severity})
// RETURN c.component_id, c.name, c.version,
//        v.cve_id, v.cvss_score, v.description,
//        r.patched, r.patch_available, r.patch_version
// ORDER BY v.cvss_score DESC;

// ───────────────────────────────────────────────────────────────────────────
// API-04: Get Equipment by Sector
// ───────────────────────────────────────────────────────────────────────────
// MATCH (e:Equipment {sector: $sector})-[:RUNS_SOFTWARE]->(c:Component)
// OPTIONAL MATCH (e)-[:HAS_STATUS]->(eol:EOLStatus)
// OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:CVE)
// RETURN e.equipment_id, e.name, e.criticality,
//        collect(DISTINCT c.name) as software,
//        eol.status as eol_status, eol.eol_date,
//        count(DISTINCT v) as vulnerability_count
// ORDER BY e.criticality DESC;

// ───────────────────────────────────────────────────────────────────────────
// API-05: Get Equipment EOL Status
// ───────────────────────────────────────────────────────────────────────────
// MATCH (e:Equipment)-[:HAS_STATUS]->(eol:EOLStatus)
// WHERE eol.eol_date <= date($threshold_date)
// RETURN e.equipment_id, e.name, e.sector, e.criticality,
//        eol.status, eol.eol_date, eol.replacement_recommended,
//        eol.extended_support_available, eol.extended_support_cost
// ORDER BY eol.eol_date ASC;

// ───────────────────────────────────────────────────────────────────────────
// API-06: Full-Text Search Across Components
// ───────────────────────────────────────────────────────────────────────────
// CALL db.index.fulltext.queryNodes("componentFullText", $search_term)
// YIELD node, score
// MATCH (node)-[:HAS_VULNERABILITY]->(v:CVE)
// RETURN node.component_id, node.name, node.version,
//        node.vendor, score,
//        count(v) as vulnerability_count
// ORDER BY score DESC
// LIMIT 20;

// ───────────────────────────────────────────────────────────────────────────
// API-07: Get Critical Equipment with Vulnerabilities
// ───────────────────────────────────────────────────────────────────────────
// MATCH (e:Equipment {criticality: "CRITICAL"})-[:RUNS_SOFTWARE]->(c:Component)
// MATCH (c)-[r:HAS_VULNERABILITY]->(v:CVE)
// WHERE r.patched = false AND v.severity IN ["CRITICAL", "HIGH"]
// RETURN e.equipment_id, e.name, e.sector,
//        c.name as component, c.version,
//        v.cve_id, v.severity, v.cvss_score,
//        r.patch_available, r.patch_version
// ORDER BY v.cvss_score DESC;

// ───────────────────────────────────────────────────────────────────────────
// API-08: Get Vendor Equipment Summary
// ───────────────────────────────────────────────────────────────────────────
// MATCH (v:Vendor)<-[:FROM_VENDOR]-(e:Equipment)
// OPTIONAL MATCH (e)-[:HAS_STATUS]->(eol:EOLStatus)
// RETURN v.vendor_id, v.name,
//        count(DISTINCT e) as equipment_count,
//        collect(DISTINCT e.sector) as sectors,
//        count(CASE WHEN eol.status = "approaching_eol" THEN 1 END) as approaching_eol_count,
//        count(CASE WHEN eol.status = "end_of_life" THEN 1 END) as eol_count
// ORDER BY equipment_count DESC;

// ═══════════════════════════════════════════════════════════════════════════
// PERFORMANCE OPTIMIZATION RECOMMENDATIONS
// ═══════════════════════════════════════════════════════════════════════════

/*
RECOMMENDATION 1: Index Usage
─────────────────────────────
- All primary queries leverage existing indexes on sector, criticality, and dates
- Full-text indexes provide fast search across large datasets
- Composite indexes on (serial_number, sector) prevent duplicates efficiently

RECOMMENDATION 2: Relationship Directionality
──────────────────────────────────────────────
- Use consistent relationship directions for optimal traversal:
  (SBOM)-[:HAS_COMPONENT]->(Component)
  (Component)-[:DEPENDS_ON]->(Component)
  (Equipment)-[:RUNS_SOFTWARE]->(Component)
  (Equipment)-[:FROM_VENDOR]->(Vendor)

RECOMMENDATION 3: Query Optimization
────────────────────────────────────
- Use OPTIONAL MATCH for nullable relationships (vulnerabilities, EOL status)
- Limit relationship depth with *1..3 on transitive queries
- Apply WHERE filters early in query execution
- Use LIMIT on paginated results

RECOMMENDATION 4: Data Model Scalability
─────────────────────────────────────────
- Equipment nodes support multi-sector deployment
- CVE nodes are shared across components (avoid duplication)
- Vendor nodes are normalized and reused
- EOL status can be versioned if historical tracking needed

RECOMMENDATION 5: Caching Strategy
───────────────────────────────────
- Cache frequently accessed queries:
  * SBOM by sector (TTL: 1 hour)
  * Critical equipment vulnerabilities (TTL: 15 minutes)
  * EOL status approaching (TTL: 1 day)
- Invalidate cache on mutations to related nodes

RECOMMENDATION 6: Batch Operations
───────────────────────────────────
- Use UNWIND for bulk inserts of components/equipment
- Batch relationship creation in transactions
- Consider periodic MERGE instead of CREATE for idempotency

RECOMMENDATION 7: Monitoring
────────────────────────────
- Track query performance with PROFILE/EXPLAIN
- Monitor index hit rates
- Alert on queries exceeding 1000ms
- Review slow query logs weekly
*/

// ═══════════════════════════════════════════════════════════════════════════
// END OF SCHEMA
// ═══════════════════════════════════════════════════════════════════════════
