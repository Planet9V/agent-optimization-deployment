#!/usr/bin/env python3
"""Wave 10 Provenance: 15,000 provenance and attestation nodes"""
import logging, json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave10ProvenanceExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_10_provenance.jsonl"

    def log_operation(self, operation: str, details: dict):
        log_entry = {"timestamp": datetime.utcnow().isoformat(), "operation": operation, "details": details}
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def create_provenance(self) -> int:
        """Create 8,000 Provenance nodes in 160 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 161):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (p:Provenance {{
                  provenanceID: "PROV-" + toString({batch_num * 1000} + idx),
                  subjectRef: "ARTIFACT-" + toString({batch_num * 100} + idx),
                  
                  provenanceType: CASE idx % 4
                    WHEN 0 THEN "slsa"
                    WHEN 1 THEN "in_toto"
                    WHEN 2 THEN "custom"
                    ELSE "sbom_provenance"
                  END,
                  
                  slsaLevel: CASE idx % 5
                    WHEN 0 THEN "SLSA_BUILD_LEVEL_1"
                    WHEN 1 THEN "SLSA_BUILD_LEVEL_2"
                    WHEN 2 THEN "SLSA_BUILD_LEVEL_3"
                    WHEN 3 THEN "SLSA_BUILD_LEVEL_4"
                    ELSE "SLSA_BUILD_LEVEL_0"
                  END,
                  
                  builder_id: "https://builder.example.com/builder/" + toString(idx % 10),
                  builder_version: toString((idx % 5) + 1) + "." + toString(idx % 10) + ".0",
                  
                  buildType: CASE idx % 5
                    WHEN 0 THEN "https://slsa.dev/container-based-build/v0.1"
                    WHEN 1 THEN "https://slsa.dev/github-actions-workflow/v1"
                    WHEN 2 THEN "https://slsa.dev/jenkins-build/v1"
                    WHEN 3 THEN "https://in-toto.io/attestation/build/v0.1"
                    ELSE "custom-build-type"
                  END,
                  
                  invocation_configSource_uri: "https://github.com/org/repo@refs/heads/main",
                  invocation_configSource_digest: "sha256:abc" + toString({batch_num * 10000} + idx),
                  invocation_configSource_entryPoint: CASE idx % 3
                    WHEN 0 THEN ".github/workflows/build.yml"
                    WHEN 1 THEN "Jenkinsfile"
                    ELSE "build.sh"
                  END,
                  
                  buildStartedOn: datetime(),
                  buildFinishedOn: datetime(),
                  reproducible: CASE idx % 4 WHEN 0 THEN true ELSE false END,
                  
                  materials_uri: "git+https://github.com/org/repo@" + toString({batch_num * 100} + idx),
                  materials_digest: "sha256:def" + toString({batch_num * 10000} + idx),
                  
                  byproducts: CASE idx % 3
                    WHEN 0 THEN ["build.log", "test-results.xml"]
                    WHEN 1 THEN ["coverage.xml", "lint-report.json"]
                    ELSE []
                  END,
                  
                  metadata_buildInvocationID: "build-" + toString({batch_num * 1000} + idx),
                  metadata_completeness_parameters: CASE idx % 2 WHEN 0 THEN true ELSE false END,
                  metadata_completeness_environment: CASE idx % 2 WHEN 0 THEN true ELSE false END,
                  metadata_completeness_materials: true,
                  metadata_reproducible: CASE idx % 4 WHEN 0 THEN true ELSE false END,
                  
                  externalParameters: CASE idx % 3
                    WHEN 0 THEN ["BUILD_TYPE=release", "TARGET_ARCH=amd64"]
                    WHEN 1 THEN ["NODE_VERSION=18", "NPM_VERSION=9"]
                    ELSE []
                  END,
                  
                  internalParameters: CASE idx % 3
                    WHEN 0 THEN ["WORKSPACE=/workspace", "CACHE_DIR=/cache"]
                    ELSE []
                  END,
                  
                  verifiable: CASE idx % 3 WHEN 0 THEN true ELSE false END,
                  verified: CASE idx % 5 WHEN 0 THEN true ELSE false END,
                  verifiedBy: CASE idx % 5 WHEN 0 THEN "https://verifier.example.com" ELSE null END,
                  
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                if batch_num % 20 == 0:
                    self.log_operation(f"provenance_batch_{batch_num}", {"count": batch_num * 50})

            result = session.run("""
            MATCH (p:Provenance) WHERE p.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(p) as total, count(DISTINCT p.provenanceID) as unique_ids
            """)
            stats = result.single()
            assert stats['total'] == 8000, f"Expected 8000 Provenance, got {stats['total']}"
            assert stats['unique_ids'] == 8000, "Duplicate provenanceIDs found"
            logging.info(f"✅ Provenance nodes created: {stats['total']}")
            return stats['total']

    def create_attestations(self) -> int:
        """Create 5,000 Attestation nodes in 100 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 101):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (a:Attestation {{
                  attestationID: "ATT-" + toString({batch_num * 1000} + idx),
                  subjectRef: "ARTIFACT-" + toString({batch_num * 100} + idx),
                  
                  attestationType: CASE idx % 6
                    WHEN 0 THEN "https://slsa.dev/provenance/v0.2"
                    WHEN 1 THEN "https://in-toto.io/attestation/v0.1"
                    WHEN 2 THEN "https://cyclonedx.org/attestation/v1.0"
                    WHEN 3 THEN "https://spdx.org/attestation/v2.3"
                    WHEN 4 THEN "https://www.openvex.dev/ns/v0.2.0"
                    ELSE "custom-attestation"
                  END,
                  
                  predicateType: CASE idx % 6
                    WHEN 0 THEN "https://slsa.dev/provenance/v0.2"
                    WHEN 1 THEN "https://in-toto.io/attestation/link/v0.9"
                    WHEN 2 THEN "https://cyclonedx.org/schema/bom/1.5"
                    WHEN 3 THEN "https://spdx.org/rdf/2.3.0/terms/Document"
                    WHEN 4 THEN "https://openvex.dev/ns/v0.2.0"
                    ELSE "custom-predicate"
                  END,
                  
                  subject_name: "artifact-" + toString({batch_num * 100} + idx),
                  subject_digest_alg: "sha256",
                  subject_digest_value: "sha256:xyz" + toString({batch_num * 10000} + idx),
                  
                  predicateContent: "{{...predicate JSON content...}}",
                  
                  attestedBy: CASE idx % 4
                    WHEN 0 THEN "https://github.com/actions"
                    WHEN 1 THEN "https://jenkins.example.com"
                    WHEN 2 THEN "https://gitlab.com/ci"
                    ELSE "https://builder.example.com"
                  END,
                  
                  attestedOn: datetime(),
                  validFrom: datetime(),
                  validUntil: CASE idx % 10 WHEN 0 THEN datetime() ELSE null END,
                  
                  signature_algorithm: CASE idx % 3
                    WHEN 0 THEN "ecdsa-sha2-nistp256"
                    WHEN 1 THEN "rsa-sha256"
                    ELSE "ed25519"
                  END,
                  signature_value: "sig-" + toString({batch_num * 10000} + idx),
                  signature_keyid: "keyid-" + toString(idx % 20),
                  
                  bundle_mediaType: "application/vnd.dev.sigstore.bundle+json;version=0.2",
                  bundle_verificationMaterial: "{{...verification material...}}",
                  
                  verified: CASE idx % 4 WHEN 0 THEN true ELSE false END,
                  verifiedBy: CASE idx % 4 WHEN 0 THEN "https://rekor.sigstore.dev" ELSE null END,
                  verifiedAt: CASE idx % 4 WHEN 0 THEN datetime() ELSE null END,
                  
                  transparency_logIndex: CASE idx % 4 WHEN 0 THEN toInteger(1000000 + idx) ELSE null END,
                  transparency_logID: CASE idx % 4 WHEN 0 THEN "https://rekor.sigstore.dev" ELSE null END,
                  
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("""
            MATCH (a:Attestation) WHERE a.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(a) as total, count(DISTINCT a.attestationID) as unique_ids
            """)
            stats = result.single()
            assert stats['total'] == 5000, f"Expected 5000 Attestations, got {stats['total']}"
            assert stats['unique_ids'] == 5000, "Duplicate attestationIDs found"
            logging.info(f"✅ Attestation nodes created: {stats['total']}")
            return stats['total']

    def create_vulnerability_attestations(self) -> int:
        """Create 2,000 VulnerabilityAttestation nodes in 40 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 41):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (va:VulnerabilityAttestation {{
                  vexID: "VEX-" + toString({batch_num * 1000} + idx),
                  subjectRef: "COMP-" + toString({batch_num * 100} + idx),
                  vulnerabilityRef: "CVE-2024-" + toString(10000 + (idx % 9999)),
                  
                  vexFormat: CASE idx % 3
                    WHEN 0 THEN "openvex"
                    WHEN 1 THEN "csaf"
                    ELSE "cyclonedx_vex"
                  END,
                  
                  status: CASE idx % 5
                    WHEN 0 THEN "not_affected"
                    WHEN 1 THEN "affected"
                    WHEN 2 THEN "fixed"
                    WHEN 3 THEN "under_investigation"
                    ELSE "unknown"
                  END,
                  
                  statusNotes: CASE idx % 5
                    WHEN 0 THEN "Component does not use vulnerable code path"
                    WHEN 1 THEN "Vulnerability confirmed, patch available"
                    WHEN 2 THEN "Fixed in version " + toString((idx % 10) + 2) + ".0.0"
                    WHEN 3 THEN "Investigating potential impact"
                    ELSE "Status unknown, awaiting analysis"
                  END,
                  
                  justification: CASE idx % 5 WHEN 0 THEN CASE idx % 8
                    WHEN 0 THEN "component_not_present"
                    WHEN 1 THEN "vulnerable_code_not_present"
                    WHEN 2 THEN "vulnerable_code_not_in_execute_path"
                    WHEN 3 THEN "vulnerable_code_cannot_be_controlled_by_adversary"
                    WHEN 4 THEN "inline_mitigations_already_exist"
                    ELSE "component_not_exploitable"
                  END ELSE null END,
                  
                  actionStatement: CASE idx % 5
                    WHEN 1 THEN "Update to version " + toString((idx % 10) + 2) + ".0.0 immediately"
                    WHEN 2 THEN "No action required - fixed in current version"
                    WHEN 3 THEN "Monitor for updates from vendor"
                    ELSE "Review risk assessment and apply mitigations"
                  END,
                  
                  impactStatement: CASE idx % 5
                    WHEN 1 THEN "High impact - remote code execution possible"
                    WHEN 2 THEN "Medium impact - information disclosure risk"
                    ELSE "Low impact - requires local access"
                  END,
                  
                  supplier: "vendor-" + toString(idx % 10) + ".com",
                  author: "security-team@company.com",
                  timestamp: datetime(),
                  lastUpdated: datetime(),
                  version: toString((idx % 3) + 1),
                  
                  cwes: CASE idx % 4
                    WHEN 0 THEN ["CWE-79", "CWE-89"]
                    WHEN 1 THEN ["CWE-22", "CWE-78"]
                    WHEN 2 THEN ["CWE-502", "CWE-611"]
                    ELSE ["CWE-20"]
                  END,
                  
                  cvssScore: toFloat(1.0 + (idx % 90) / 10.0),
                  cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                  
                  exploitability: CASE idx % 4
                    WHEN 0 THEN "not_exploitable"
                    WHEN 1 THEN "exploitable"
                    WHEN 2 THEN "proof_of_concept"
                    ELSE "unknown"
                  END,
                  
                  references: ["https://nvd.nist.gov/vuln/detail/CVE-2024-" + toString(10000 + (idx % 9999))],
                  
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("""
            MATCH (va:VulnerabilityAttestation) WHERE va.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(va) as total, count(DISTINCT va.vexID) as unique_ids
            """)
            stats = result.single()
            assert stats['total'] == 2000, f"Expected 2000 VulnerabilityAttestations, got {stats['total']}"
            assert stats['unique_ids'] == 2000, "Duplicate vexIDs found"
            logging.info(f"✅ VulnerabilityAttestation nodes created: {stats['total']}")
            return stats['total']

    def execute(self):
        try:
            start = datetime.utcnow()
            logging.info("🎯 Wave 10 Provenance Started")
            
            prov_count = self.create_provenance()
            att_count = self.create_attestations()
            vex_count = self.create_vulnerability_attestations()
            
            total = prov_count + att_count + vex_count
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
    Wave10ProvenanceExecutor().execute()
