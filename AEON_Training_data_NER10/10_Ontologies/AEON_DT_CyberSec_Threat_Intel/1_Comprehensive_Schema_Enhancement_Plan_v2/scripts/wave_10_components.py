#!/usr/bin/env python3
"""
Wave 10 Components: Software Components, Packages, Container Images, Firmware, Libraries
Creates 50,000 SBOM component nodes with batch processing and verification
"""

import logging
import json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave10ComponentsExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_10_components.jsonl"

    def log_operation(self, operation: str, details: dict):
        """Log operation to JSONL file"""
        log_entry = {"timestamp": datetime.utcnow().isoformat(), "operation": operation, "details": details}
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def create_software_components(self) -> int:
        """Create 20,000 base SoftwareComponent nodes in 400 batches"""
        with self.driver.session() as session:
            component_types = [
                ("library", 8000, 160),
                ("framework", 4000, 80),
                ("application", 3000, 60),
                ("operating_system", 2000, 40),
                ("device", 1500, 30),
                ("firmware", 1500, 30)
            ]

            total_created = 0
            for comp_type, target_count, num_batches in component_types:
                for batch_num in range(1, num_batches + 1):
                    session.run(f"""
                    UNWIND range(1, 50) AS idx
                    CREATE (sc:SoftwareComponent {{
                      componentID: "{comp_type.upper()}-COMP-" + toString({batch_num * 1000} + idx),
                      purl: "pkg:{comp_type}/" + toLower("{comp_type}") + "-" + toString({batch_num * 100} + idx) + "@" + toString((idx % 10) + 1) + ".0.0",
                      cpe: "cpe:2.3:a:vendor:" + toLower("{comp_type}") + "_" + toString({batch_num * 100} + idx) + ":" + toString((idx % 10) + 1) + ".0.0:*:*:*:*:*:*:*",
                      swid: "swid:" + randomUUID(),

                      name: "{comp_type.title()} Component " + toString({batch_num * 100} + idx),
                      version: toString((idx % 10) + 1) + "." + toString(idx % 20) + "." + toString(idx % 50),
                      versionScheme: CASE idx % 4 WHEN 0 THEN "semver" WHEN 1 THEN "integer" WHEN 2 THEN "alpha" ELSE "custom" END,
                      group: CASE idx % 5 WHEN 0 THEN "com.vendor" WHEN 1 THEN "org.apache" WHEN 2 THEN "io.github" WHEN 3 THEN "com.company" ELSE "org.project" END,
                      namespace: "vendor.{comp_type}",

                      componentType: "{comp_type}",

                      supplier_name: CASE idx % 5 WHEN 0 THEN "Vendor Corp" WHEN 1 THEN "Apache Foundation" WHEN 2 THEN "GitHub Inc" WHEN 3 THEN "Company Ltd" ELSE "Project Org" END,
                      supplier_url: "https://vendor" + toString(idx % 10) + ".com",
                      supplier_contact: "security@vendor" + toString(idx % 10) + ".com",
                      supplier_organizationType: CASE idx % 4 WHEN 0 THEN "vendor" WHEN 1 THEN "contributor" WHEN 2 THEN "maintainer" ELSE "distributor" END,

                      author: "Author " + toString(idx),
                      publisher: "Publisher " + toString(idx % 20),

                      description: "{comp_type.title()} component providing various functionality for enterprise applications",
                      summary: "Production-grade {comp_type} component",
                      category: ["{comp_type}", "enterprise", "production"],
                      tags: ["stable", "verified", "sbom"],

                      license: CASE idx % 6 WHEN 0 THEN "MIT" WHEN 1 THEN "Apache-2.0" WHEN 2 THEN "GPL-3.0" WHEN 3 THEN "BSD-3-Clause" WHEN 4 THEN "LGPL-2.1" ELSE "MPL-2.0" END,
                      licenseExpression: CASE idx % 6 WHEN 0 THEN "MIT" WHEN 1 THEN "Apache-2.0" ELSE "GPL-3.0 OR MIT" END,
                      copyright: "Copyright (c) 2024 Vendor Corp",

                      hash_algorithm: "sha256",
                      hash_value: "abc" + toString({batch_num * 10000} + idx) + "def1234567890",

                      fileName: toLower("{comp_type}") + "-component-" + toString({batch_num * 100} + idx) + ".jar",
                      fileSize: toInteger((idx % 100 + 1) * 1024 * 1024),
                      mimeType: "application/java-archive",
                      encoding: "utf-8",

                      scope: CASE idx % 5 WHEN 0 THEN "required" WHEN 1 THEN "optional" WHEN 2 THEN "runtime" WHEN 3 THEN "development" ELSE "test" END,
                      modified: CASE idx % 10 WHEN 0 THEN true ELSE false END,

                      bomRef: "ref-{comp_type}-" + toString({batch_num * 1000} + idx),
                      spdxID: "SPDXRef-{comp_type.upper()}-" + toString({batch_num * 1000} + idx),
                      specVersion: "2.3",
                      serialNumber: "urn:uuid:" + randomUUID(),

                      releaseDate: datetime() - duration({{days: idx * 2}}),
                      buildDate: datetime() - duration({{days: idx * 2 + 1}}),
                      validUntilDate: datetime() + duration({{days: 365 - idx}}),
                      endOfSupportDate: datetime() + duration({{days: 730 - idx}}),

                      confidence: toFloat(0.7 + (idx % 30) * 0.01),
                      trustScore: toFloat(70.0 + (idx % 30)),
                      verificationStatus: CASE idx % 4 WHEN 0 THEN "verified" WHEN 1 THEN "unverified" WHEN 2 THEN "pending" ELSE "verified" END,

                      node_id: randomUUID(),
                      created_by: "AEON_INTEGRATION_WAVE10",
                      created_date: datetime(),
                      last_updated: datetime(),
                      validation_status: "VALIDATED"
                    }})
                    """)
                    self.log_operation(f"software_components_batch_{comp_type}_{batch_num}", {"count": 50})
                    total_created += 50

            # Verify total
            result = session.run("""
            MATCH (sc:SoftwareComponent) WHERE sc.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(sc) as total,
                   count(DISTINCT sc.componentID) as unique_ids,
                   count(DISTINCT sc.purl) as unique_purls
            """)
            stats = result.single()
            self.log_operation("software_components_verification", dict(stats))
            assert stats['total'] == 20000, f"Expected 20000 SoftwareComponents, got {stats['total']}"
            assert stats['unique_ids'] == 20000, "Duplicate componentIDs found"
            assert stats['unique_purls'] == 20000, "Duplicate PURLs found"
            logging.info(f"✅ SoftwareComponent nodes created: {stats['total']}")
            return stats['total']

    def create_packages(self) -> int:
        """Create 10,000 Package nodes in 200 batches"""
        with self.driver.session() as session:
            package_managers = [
                ("npm", 2500, 50),
                ("pip", 2000, 40),
                ("maven", 1500, 30),
                ("nuget", 1500, 30),
                ("cargo", 1000, 20),
                ("go_mod", 1000, 20),
                ("gem", 500, 10)
            ]

            total_created = 0
            for pkg_mgr, target_count, num_batches in package_managers:
                for batch_num in range(1, num_batches + 1):
                    session.run(f"""
                    UNWIND range(1, 50) AS idx
                    CREATE (pkg:Package:SoftwareComponent {{
                      componentID: "{pkg_mgr.upper()}-PKG-" + toString({batch_num * 1000} + idx),
                      purl: "pkg:{pkg_mgr}/" + toLower("{pkg_mgr}") + "-package-" + toString({batch_num * 100} + idx) + "@" + toString((idx % 10) + 1) + ".0.0",
                      cpe: "cpe:2.3:a:{pkg_mgr}:package_" + toString({batch_num * 100} + idx) + ":" + toString((idx % 10) + 1) + ".0.0:*:*:*:*:*:*:*",

                      name: "{pkg_mgr.title()} Package " + toString({batch_num * 100} + idx),
                      version: toString((idx % 10) + 1) + "." + toString(idx % 20) + "." + toString(idx % 50),
                      versionScheme: "semver",
                      componentType: "library",

                      packageManager: "{pkg_mgr}",
                      downloadLocation: "https://registry.{pkg_mgr}.org/package-" + toString({batch_num * 100} + idx),
                      packageURL: "pkg:{pkg_mgr}/package-" + toString({batch_num * 100} + idx),
                      homepage: "https://github.com/vendor/package-" + toString({batch_num * 100} + idx),

                      repository_type: "git",
                      repository_url: "https://github.com/vendor/package-" + toString({batch_num * 100} + idx),
                      repository_branch: "main",
                      repository_commit: "abc" + toString({batch_num * 1000} + idx),

                      checksumAlgorithm: "sha256",
                      checksumValue: "def" + toString({batch_num * 10000} + idx) + "ghi",

                      filesAnalyzed: CASE idx % 2 WHEN 0 THEN true ELSE false END,

                      license: CASE idx % 5 WHEN 0 THEN "MIT" WHEN 1 THEN "Apache-2.0" WHEN 2 THEN "BSD-3-Clause" WHEN 3 THEN "ISC" ELSE "GPL-3.0" END,

                      node_id: randomUUID(),
                      created_by: "AEON_INTEGRATION_WAVE10",
                      created_date: datetime(),
                      validation_status: "VALIDATED"
                    }})
                    """)
                    self.log_operation(f"packages_batch_{pkg_mgr}_{batch_num}", {"count": 50})
                    total_created += 50

            # Verify
            result = session.run("""
            MATCH (pkg:Package) WHERE pkg.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(pkg) as total,
                   count(DISTINCT pkg.componentID) as unique_ids,
                   collect(DISTINCT pkg.packageManager)[0..10] as managers
            """)
            stats = result.single()
            self.log_operation("packages_verification", dict(stats))
            assert stats['total'] == 10000, f"Expected 10000 Packages, got {stats['total']}"
            logging.info(f"✅ Package nodes created: {stats['total']}")
            return stats['total']

    def create_container_images(self) -> int:
        """Create 5,000 ContainerImage nodes in 100 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 101):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (ci:ContainerImage:SoftwareComponent {{
                  componentID: "CONTAINER-IMG-" + toString({batch_num * 1000} + idx),
                  imageID: "sha256:" + toString(randomUUID()),
                  imageName: "app/service-" + toString({batch_num * 100} + idx),
                  imageTag: CASE idx % 5 WHEN 0 THEN "latest" WHEN 1 THEN "v" + toString((idx % 10) + 1) WHEN 2 THEN "stable" WHEN 3 THEN "dev" ELSE "prod" END,
                  imageDigest: "sha256:abc" + toString({batch_num * 10000} + idx) + "def",

                  registry: CASE idx % 4 WHEN 0 THEN "docker.io" WHEN 1 THEN "gcr.io" WHEN 2 THEN "quay.io" ELSE "registry.gitlab.com" END,
                  repository: "vendor/app-" + toString({batch_num}),

                  architecture: CASE idx % 4 WHEN 0 THEN "amd64" WHEN 1 THEN "arm64" WHEN 2 THEN "armv7" ELSE "amd64" END,
                  os: CASE idx % 3 WHEN 0 THEN "linux" WHEN 1 THEN "windows" ELSE "linux" END,
                  osVersion: CASE idx % 3 WHEN 0 THEN "ubuntu-22.04" WHEN 1 THEN "alpine-3.18" ELSE "debian-11" END,

                  size: toInteger((idx % 500 + 100) * 1024 * 1024),
                  virtualSize: toInteger((idx % 600 + 150) * 1024 * 1024),

                  config_user: "appuser",
                  config_exposedPorts: ["80", "443"],
                  config_workingDir: "/app",

                  componentType: "container",
                  name: "Container Image " + toString({batch_num * 100} + idx),
                  version: "v" + toString((idx % 10) + 1) + ".0",

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                self.log_operation(f"container_images_batch_{batch_num}", {"count": 50})

            # Verify
            result = session.run("""
            MATCH (ci:ContainerImage) WHERE ci.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(ci) as total,
                   count(DISTINCT ci.imageID) as unique_ids
            """)
            stats = result.single()
            self.log_operation("container_images_verification", dict(stats))
            assert stats['total'] == 5000, f"Expected 5000 ContainerImages, got {stats['total']}"
            logging.info(f"✅ ContainerImage nodes created: {stats['total']}")
            return stats['total']

    def create_firmware(self) -> int:
        """Create 5,000 Firmware nodes in 100 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 101):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (fw:Firmware:SoftwareComponent {{
                  componentID: "FIRMWARE-" + toString({batch_num * 1000} + idx),
                  name: "Firmware " + toString({batch_num * 100} + idx),
                  version: "v" + toString((idx % 20) + 1) + "." + toString(idx % 50),
                  componentType: "firmware",

                  firmwareType: CASE idx % 5 WHEN 0 THEN "bios" WHEN 1 THEN "uefi" WHEN 2 THEN "embedded" WHEN 3 THEN "bootloader" ELSE "microcode" END,
                  targetDevice: "Device-" + toString(idx % 100),
                  flashSize: toInteger((idx % 32 + 1) * 1024 * 1024),
                  bootloader: "Bootloader v" + toString(idx % 5 + 1),
                  cryptographicSignature: "sig:" + toString(randomUUID()),

                  purl: "pkg:firmware/fw-" + toString({batch_num * 100} + idx) + "@" + toString((idx % 20) + 1),

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                self.log_operation(f"firmware_batch_{batch_num}", {"count": 50})

            # Verify
            result = session.run("""
            MATCH (fw:Firmware) WHERE fw.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(fw) as total,
                   count(DISTINCT fw.componentID) as unique_ids
            """)
            stats = result.single()
            self.log_operation("firmware_verification", dict(stats))
            assert stats['total'] == 5000, f"Expected 5000 Firmware nodes, got {stats['total']}"
            logging.info(f"✅ Firmware nodes created: {stats['total']}")
            return stats['total']

    def create_libraries(self) -> int:
        """Create 10,000 Library nodes in 200 batches"""
        with self.driver.session() as session:
            for batch_num in range(1, 201):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (lib:Library:SoftwareComponent {{
                  componentID: "LIBRARY-" + toString({batch_num * 1000} + idx),
                  name: "Library " + toString({batch_num * 100} + idx),
                  version: toString((idx % 15) + 1) + "." + toString(idx % 30) + "." + toString(idx % 50),
                  componentType: "library",

                  libraryType: CASE idx % 4 WHEN 0 THEN "static" WHEN 1 THEN "dynamic" WHEN 2 THEN "shared" ELSE "header_only" END,
                  apiVersion: toString((idx % 10) + 1) + ".0",
                  abiVersion: toString((idx % 5) + 1),
                  interfaceStability: CASE idx % 4 WHEN 0 THEN "stable" WHEN 1 THEN "unstable" WHEN 2 THEN "deprecated" ELSE "experimental" END,

                  purl: "pkg:lib/library-" + toString({batch_num * 100} + idx) + "@" + toString((idx % 15) + 1),

                  license: CASE idx % 6 WHEN 0 THEN "MIT" WHEN 1 THEN "Apache-2.0" WHEN 2 THEN "LGPL-2.1" WHEN 3 THEN "BSD-2-Clause" WHEN 4 THEN "MPL-2.0" ELSE "ISC" END,

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE10",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                self.log_operation(f"libraries_batch_{batch_num}", {"count": 50})

            # Verify
            result = session.run("""
            MATCH (lib:Library) WHERE lib.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(lib) as total,
                   count(DISTINCT lib.componentID) as unique_ids
            """)
            stats = result.single()
            self.log_operation("libraries_verification", dict(stats))
            assert stats['total'] == 10000, f"Expected 10000 Library nodes, got {stats['total']}"
            logging.info(f"✅ Library nodes created: {stats['total']}")
            return stats['total']

    def execute(self):
        try:
            start_time = datetime.utcnow()
            self.log_operation("wave_10_components_execution_started", {"timestamp": start_time.isoformat()})
            logging.info(f"🎯 Wave 10 Components Execution Started: {start_time.isoformat()}")

            # Create all component types
            sc_count = self.create_software_components()
            pkg_count = self.create_packages()
            ci_count = self.create_container_images()
            fw_count = self.create_firmware()
            lib_count = self.create_libraries()

            total = sc_count + pkg_count + ci_count + fw_count + lib_count

            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()

            logging.info("=" * 80)
            logging.info("🎉 WAVE 10 COMPONENTS COMPLETE")
            logging.info("=" * 80)
            logging.info(f"SoftwareComponent: {sc_count}")
            logging.info(f"Package: {pkg_count}")
            logging.info(f"ContainerImage: {ci_count}")
            logging.info(f"Firmware: {fw_count}")
            logging.info(f"Library: {lib_count}")
            logging.info(f"Total Nodes Created: {total}")
            logging.info(f"Execution Time: {duration:.2f} seconds")
            logging.info(f"Node Creation Rate: {total / duration:.2f} nodes/second")
            logging.info("=" * 80)

        except Exception as e:
            self.log_operation("wave_10_components_execution_error", {"error": str(e)})
            logging.error(f"Wave 10 Components execution failed: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    executor = Wave10ComponentsExecutor()
    executor.execute()
