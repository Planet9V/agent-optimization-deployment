#!/usr/bin/env python3
"""Wave 10 Licenses: 15,000 license and compliance nodes"""
import logging, json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave10LicensesExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_10_licenses.jsonl"

    def log_operation(self, operation: str, details: dict):
        log_entry = {"timestamp": datetime.utcnow().isoformat(), "operation": operation, "details": details}
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def create_software_licenses(self) -> int:
        """Create 8,000 SoftwareLicense nodes in 160 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 161):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (sl:SoftwareLicense {{
                  licenseID: "LIC-" + toString({batch_num * 1000} + idx),
                  spdxID: CASE idx % 20 
                    WHEN 0 THEN "MIT"
                    WHEN 1 THEN "Apache-2.0"
                    WHEN 2 THEN "GPL-3.0"
                    WHEN 3 THEN "BSD-3-Clause"
                    WHEN 4 THEN "ISC"
                    WHEN 5 THEN "MPL-2.0"
                    WHEN 6 THEN "LGPL-3.0"
                    WHEN 7 THEN "EPL-2.0"
                    WHEN 8 THEN "AGPL-3.0"
                    WHEN 9 THEN "BSD-2-Clause"
                    WHEN 10 THEN "Unlicense"
                    WHEN 11 THEN "CC0-1.0"
                    WHEN 12 THEN "GPL-2.0"
                    WHEN 13 THEN "LGPL-2.1"
                    WHEN 14 THEN "CDDL-1.0"
                    WHEN 15 THEN "PSF-2.0"
                    WHEN 16 THEN "Artistic-2.0"
                    WHEN 17 THEN "Zlib"
                    WHEN 18 THEN "BSL-1.0"
                    ELSE "Proprietary"
                  END,
                  
                  name: CASE idx % 20
                    WHEN 0 THEN "MIT License"
                    WHEN 1 THEN "Apache License 2.0"
                    WHEN 2 THEN "GNU General Public License v3.0"
                    WHEN 3 THEN "BSD 3-Clause License"
                    WHEN 4 THEN "ISC License"
                    WHEN 5 THEN "Mozilla Public License 2.0"
                    WHEN 6 THEN "GNU Lesser General Public License v3.0"
                    WHEN 7 THEN "Eclipse Public License 2.0"
                    WHEN 8 THEN "GNU Affero General Public License v3.0"
                    WHEN 9 THEN "BSD 2-Clause License"
                    WHEN 10 THEN "The Unlicense"
                    WHEN 11 THEN "Creative Commons Zero v1.0"
                    WHEN 12 THEN "GNU General Public License v2.0"
                    WHEN 13 THEN "GNU Lesser General Public License v2.1"
                    WHEN 14 THEN "Common Development and Distribution License 1.0"
                    WHEN 15 THEN "Python Software Foundation License 2.0"
                    WHEN 16 THEN "Artistic License 2.0"
                    WHEN 17 THEN "zlib License"
                    WHEN 18 THEN "Boost Software License 1.0"
                    ELSE "Proprietary License"
                  END,
                  
                  licenseType: CASE idx % 5
                    WHEN 0 THEN "permissive"
                    WHEN 1 THEN "copyleft"
                    WHEN 2 THEN "weak_copyleft"
                    WHEN 3 THEN "public_domain"
                    ELSE "proprietary"
                  END,
                  
                  osiApproved: CASE idx % 20 WHEN 19 THEN false ELSE true END,
                  fsfApproved: CASE idx % 20 WHEN 19 THEN false ELSE true END,
                  
                  commercial: CASE idx % 5 WHEN 4 THEN false ELSE true END,
                  derivative: CASE idx % 5 WHEN 1 THEN false ELSE true END,
                  distribution: CASE idx % 5 WHEN 4 THEN false ELSE true END,
                  modification: CASE idx % 5 WHEN 4 THEN false ELSE true END,
                  patentGrant: CASE idx % 4 WHEN 0 THEN true ELSE false END,
                  privateUse: true,
                  
                  attribution: CASE idx % 10 WHEN 9 THEN false ELSE true END,
                  copyleftScope: CASE idx % 5
                    WHEN 1 THEN "file"
                    WHEN 2 THEN "library"
                    WHEN 3 THEN "network"
                    ELSE "none"
                  END,
                  discloseSource: CASE idx % 5 WHEN 1 THEN true WHEN 2 THEN true ELSE false END,
                  
                  licenseText: "Full license text for " + CASE idx % 20 WHEN 0 THEN "MIT" WHEN 1 THEN "Apache-2.0" ELSE "other" END,
                  url: "https://spdx.org/licenses/" + CASE idx % 20 WHEN 0 THEN "MIT.html" WHEN 1 THEN "Apache-2.0.html" ELSE "license.html" END,
                  
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                if batch_num % 20 == 0:
                    self.log_operation(f"licenses_batch_{batch_num}", {"count": batch_num * 50})

            result = session.run("""
            MATCH (sl:SoftwareLicense) WHERE sl.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(sl) as total, count(DISTINCT sl.licenseID) as unique_ids
            """)
            stats = result.single()
            assert stats['total'] == 8000, f"Expected 8000 SoftwareLicenses, got {stats['total']}"
            assert stats['unique_ids'] == 8000, "Duplicate licenseIDs found"
            logging.info(f"✅ SoftwareLicense nodes created: {stats['total']}")
            return stats['total']

    def create_license_compliance(self) -> int:
        """Create 5,000 LicenseCompliance nodes in 100 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 101):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (lc:LicenseCompliance {{
                  complianceID: "COMP-" + toString({batch_num * 1000} + idx),
                  componentRef: "COMP-" + toString({batch_num * 100} + idx),
                  licenseRef: "LIC-" + toString(idx % 8000 + 1),
                  
                  complianceStatus: CASE idx % 5
                    WHEN 0 THEN "compliant"
                    WHEN 1 THEN "non_compliant"
                    WHEN 2 THEN "under_review"
                    WHEN 3 THEN "exception_granted"
                    ELSE "unknown"
                  END,
                  
                  riskLevel: CASE idx % 5
                    WHEN 0 THEN "low"
                    WHEN 1 THEN "medium"
                    WHEN 2 THEN "high"
                    WHEN 3 THEN "critical"
                    ELSE "unknown"
                  END,
                  
                  approved: CASE idx % 5 WHEN 0 THEN true WHEN 3 THEN true ELSE false END,
                  approvedBy: CASE idx % 5 WHEN 0 THEN "legal@company.com" WHEN 3 THEN "cto@company.com" ELSE null END,
                  approvedDate: CASE idx % 5 WHEN 0 THEN datetime() WHEN 3 THEN datetime() ELSE null END,
                  
                  conflictsWith: CASE idx % 10 WHEN 0 THEN ["GPL-3.0", "AGPL-3.0"] ELSE [] END,
                  compatibleWith: CASE idx % 10 WHEN 1 THEN ["MIT", "Apache-2.0", "BSD-3-Clause"] ELSE [] END,
                  
                  assessmentDate: datetime(),
                  assessor: "compliance-tool-v" + toString((idx % 3) + 1) + ".0.0",
                  
                  notes: CASE idx % 5
                    WHEN 1 THEN "Requires legal review due to copyleft scope"
                    WHEN 2 THEN "High risk - incompatible with commercial use"
                    ELSE "Standard compliance assessment"
                  END,
                  
                  remediationRequired: CASE idx % 5 WHEN 1 THEN true WHEN 2 THEN true ELSE false END,
                  remediationSteps: CASE idx % 5
                    WHEN 1 THEN ["Review license terms", "Consult legal team", "Document exception"]
                    WHEN 2 THEN ["Replace component", "Seek alternative", "Request exception"]
                    ELSE []
                  END,
                  
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("""
            MATCH (lc:LicenseCompliance) WHERE lc.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(lc) as total, count(DISTINCT lc.complianceID) as unique_ids
            """)
            stats = result.single()
            assert stats['total'] == 5000, f"Expected 5000 LicenseCompliance, got {stats['total']}"
            assert stats['unique_ids'] == 5000, "Duplicate complianceIDs found"
            logging.info(f"✅ LicenseCompliance nodes created: {stats['total']}")
            return stats['total']

    def create_license_policies(self) -> int:
        """Create 2,000 LicensePolicy nodes in 40 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 41):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (lp:LicensePolicy {{
                  policyID: "POL-" + toString({batch_num * 1000} + idx),
                  policyName: "License Policy " + toString({batch_num * 100} + idx),
                  
                  policyType: CASE idx % 4
                    WHEN 0 THEN "organizational"
                    WHEN 1 THEN "project_specific"
                    WHEN 2 THEN "regulatory"
                    ELSE "best_practice"
                  END,
                  
                  scope: CASE idx % 4
                    WHEN 0 THEN "company_wide"
                    WHEN 1 THEN "department"
                    WHEN 2 THEN "project"
                    ELSE "product"
                  END,
                  
                  allowedLicenses: ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"],
                  prohibitedLicenses: CASE idx % 3
                    WHEN 0 THEN ["GPL-3.0", "AGPL-3.0"]
                    WHEN 1 THEN ["Proprietary", "Custom"]
                    ELSE []
                  END,
                  restrictedLicenses: CASE idx % 3
                    WHEN 0 THEN ["LGPL-3.0", "MPL-2.0"]
                    ELSE []
                  END,
                  
                  requiresApproval: CASE idx % 3 WHEN 0 THEN true ELSE false END,
                  approvalAuthority: CASE idx % 3
                    WHEN 0 THEN "legal_team"
                    WHEN 1 THEN "engineering_lead"
                    ELSE "cto"
                  END,
                  
                  exceptionProcess: CASE idx % 2
                    WHEN 0 THEN "Submit exception request to legal team with business justification"
                    ELSE "Consult with engineering lead and document decision"
                  END,
                  
                  complianceChecks: ["SPDX validation", "License compatibility check", "Copyleft scope analysis"],
                  
                  enforcementLevel: CASE idx % 3
                    WHEN 0 THEN "mandatory"
                    WHEN 1 THEN "recommended"
                    ELSE "advisory"
                  END,
                  
                  version: toString((idx % 5) + 1) + ".0",
                  effectiveDate: datetime(),
                  expirationDate: CASE idx % 10 WHEN 0 THEN datetime() ELSE null END,
                  
                  owner: CASE idx % 3
                    WHEN 0 THEN "legal@company.com"
                    WHEN 1 THEN "compliance@company.com"
                    ELSE "cto@company.com"
                  END,
                  
                  lastReviewed: datetime(),
                  reviewFrequency: CASE idx % 3
                    WHEN 0 THEN "quarterly"
                    WHEN 1 THEN "annually"
                    ELSE "biannually"
                  END,
                  
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("""
            MATCH (lp:LicensePolicy) WHERE lp.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(lp) as total, count(DISTINCT lp.policyID) as unique_ids
            """)
            stats = result.single()
            assert stats['total'] == 2000, f"Expected 2000 LicensePolicies, got {stats['total']}"
            assert stats['unique_ids'] == 2000, "Duplicate policyIDs found"
            logging.info(f"✅ LicensePolicy nodes created: {stats['total']}")
            return stats['total']

    def execute(self):
        try:
            start = datetime.utcnow()
            logging.info("🎯 Wave 10 Licenses Started")
            
            license_count = self.create_software_licenses()
            compliance_count = self.create_license_compliance()
            policy_count = self.create_license_policies()
            
            total = license_count + compliance_count + policy_count
            duration = (datetime.utcnow() - start).total_seconds()
            
            logging.info("=" * 80)
            logging.info(f"✅ Total: {total} | Time: {duration:.2f}s | Rate: {total/duration:.2f} nodes/s")
            logging.info("=" * 80)
        except Exception as e:
            logging.error(f"Failed: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    Wave10LicensesExecutor().execute()
