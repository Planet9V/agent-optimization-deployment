#!/usr/bin/env python3
"""Wave 10 Master Executor: SBOM Integration - 140,000 nodes"""
import subprocess, logging, json, sys
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave10MasterExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.scripts_dir = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2/scripts"
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_10_master_execution.jsonl"

    def log_operation(self, operation: str, details: dict):
        log_entry = {"timestamp": datetime.utcnow().isoformat(), "operation": operation, "details": details}
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        logging.info(f"{operation}: {details}")

    def run_script(self, script_name: str, expected_nodes: int) -> dict:
        """Execute a Wave 10 script and return statistics"""
        script_path = f"{self.scripts_dir}/{script_name}"
        logging.info(f"\n{'='*80}")
        logging.info(f"🚀 Executing: {script_name}")
        logging.info(f"{'='*80}")
        
        start_time = datetime.utcnow()
        try:
            result = subprocess.run(
                ['python3', script_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=600
            )
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            logging.info(result.stdout)
            if result.stderr:
                logging.warning(f"STDERR: {result.stderr}")
            
            stats = {
                "script": script_name,
                "status": "success",
                "duration": duration,
                "expected_nodes": expected_nodes,
                "rate": expected_nodes / duration if duration > 0 else 0
            }
            self.log_operation(f"{script_name}_completed", stats)
            return stats
            
        except subprocess.TimeoutExpired:
            error_msg = f"{script_name} timed out after 600 seconds"
            logging.error(error_msg)
            self.log_operation(f"{script_name}_timeout", {"error": error_msg})
            raise
        except subprocess.CalledProcessError as e:
            error_msg = f"{script_name} failed with return code {e.returncode}"
            logging.error(error_msg)
            logging.error(f"STDOUT: {e.stdout}")
            logging.error(f"STDERR: {e.stderr}")
            self.log_operation(f"{script_name}_failed", {"error": error_msg, "stdout": e.stdout, "stderr": e.stderr})
            raise

    def validate_wave10_nodes(self) -> dict:
        """Comprehensive validation of all Wave 10 nodes"""
        logging.info(f"\n{'='*80}")
        logging.info("🔍 WAVE 10 COMPREHENSIVE VALIDATION")
        logging.info(f"{'='*80}")
        
        with self.driver.session() as session:
            # 1. Category-level validation
            categories = {
                "Software Components": ["SoftwareComponent", "Package", "ContainerImage", "Firmware", "Library"],
                "Dependencies": ["Dependency", "DependencyTree", "DependencyPath"],
                "Build Information": ["BuildSystem", "Build", "BuildTool", "Artifact"],
                "Licenses": ["SoftwareLicense", "LicenseCompliance", "LicensePolicy"],
                "Provenance": ["Provenance", "Attestation", "VulnerabilityAttestation"]
            }
            
            expected_totals = {
                "Software Components": 50000,
                "Dependencies": 40000,
                "Build Information": 20000,
                "Licenses": 15000,
                "Provenance": 15000
            }
            
            validation_results = {}
            total_nodes = 0
            
            for category, node_types in categories.items():
                labels_str = ", ".join([f"'{label}'" for label in node_types])
                query = f"""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE10'
                  AND any(label IN labels(n) WHERE label IN [{labels_str}])
                RETURN count(n) as count
                """
                result = session.run(query)
                count = result.single()['count']
                total_nodes += count
                
                expected = expected_totals[category]
                status = "✅" if count == expected else "❌"
                
                logging.info(f"{status} {category}: {count:,} (expected: {expected:,})")
                validation_results[category] = {
                    "count": count,
                    "expected": expected,
                    "status": "pass" if count == expected else "fail"
                }
            
            # 2. Total Wave 10 nodes validation
            logging.info(f"\n{'='*80}")
            result = session.run("""
            MATCH (n) WHERE n.created_by = 'AEON_INTEGRATION_WAVE10'
            RETURN count(n) as total
            """)
            actual_total = result.single()['total']
            expected_total = 140000
            
            if actual_total == expected_total:
                logging.info(f"✅ WAVE 10 TOTAL: {actual_total:,} nodes (expected: {expected_total:,})")
                validation_results['total_wave10'] = {"status": "pass", "count": actual_total}
            else:
                logging.error(f"❌ WAVE 10 TOTAL MISMATCH: {actual_total:,} (expected: {expected_total:,})")
                validation_results['total_wave10'] = {"status": "fail", "count": actual_total, "expected": expected_total}
            
            # 3. Per-type node counts
            logging.info(f"\n{'='*80}")
            logging.info("📊 PER-TYPE NODE COUNTS")
            logging.info(f"{'='*80}")
            
            expected_per_type = {
                "SoftwareComponent": 20000, "Package": 10000, "ContainerImage": 5000, "Firmware": 5000, "Library": 10000,
                "Dependency": 30000, "DependencyTree": 8000, "DependencyPath": 2000,
                "BuildSystem": 5000, "Build": 8000, "BuildTool": 2000, "Artifact": 5000,
                "SoftwareLicense": 8000, "LicenseCompliance": 5000, "LicensePolicy": 2000,
                "Provenance": 8000, "Attestation": 5000, "VulnerabilityAttestation": 2000
            }
            
            type_validation = {}
            for node_type, expected in expected_per_type.items():
                result = session.run(f"""
                MATCH (n:{node_type}) WHERE n.created_by = 'AEON_INTEGRATION_WAVE10'
                RETURN count(n) as count
                """)
                count = result.single()['count']
                status = "✅" if count == expected else "❌"
                logging.info(f"{status} {node_type}: {count:,} (expected: {expected:,})")
                type_validation[node_type] = {"count": count, "expected": expected, "status": "pass" if count == expected else "fail"}
            
            validation_results['per_type'] = type_validation
            
            # 4. CVE Preservation Check
            logging.info(f"\n{'='*80}")
            logging.info("🛡️ CVE PRESERVATION CHECK")
            logging.info(f"{'='*80}")
            
            result = session.run("MATCH (cve:CVE) RETURN count(cve) as cve_count")
            cve_count = result.single()['cve_count']
            expected_cve = 267487
            
            if cve_count == expected_cve:
                logging.info(f"✅ CVE PRESERVATION: {cve_count:,} CVE nodes intact (expected: {expected_cve:,})")
                validation_results['cve_preservation'] = {"status": "pass", "count": cve_count}
            else:
                logging.error(f"❌ CVE DATA LOSS: {cve_count:,} CVE nodes (expected: {expected_cve:,})")
                validation_results['cve_preservation'] = {"status": "fail", "count": cve_count, "expected": expected_cve}
            
            # 5. Uniqueness Validation
            logging.info(f"\n{'='*80}")
            logging.info("🔑 UNIQUENESS VALIDATION")
            logging.info(f"{'='*80}")
            
            uniqueness_checks = [
                ("node_id", "n.node_id"),
                ("componentID", "n.componentID", "SoftwareComponent"),
                ("purl", "n.purl", "SoftwareComponent"),
                ("dependencyID", "n.dependencyID", "Dependency"),
                ("buildID", "n.buildID", "Build"),
                ("licenseID", "n.licenseID", "SoftwareLicense"),
                ("provenanceID", "n.provenanceID", "Provenance")
            ]
            
            uniqueness_results = {}
            for check in uniqueness_checks:
                field = check[0]
                property = check[1]
                label = check[2] if len(check) > 2 else None
                
                if label:
                    query = f"""
                    MATCH (n:{label}) WHERE n.created_by = 'AEON_INTEGRATION_WAVE10'
                    WITH count(n) as total, count(DISTINCT {property}) as unique
                    RETURN total, unique, total - unique as duplicates
                    """
                else:
                    query = f"""
                    MATCH (n) WHERE n.created_by = 'AEON_INTEGRATION_WAVE10'
                    WITH count(n) as total, count(DISTINCT {property}) as unique
                    RETURN total, unique, total - unique as duplicates
                    """
                
                result = session.run(query)
                stats = result.single()
                duplicates = stats['duplicates']
                
                if duplicates == 0:
                    logging.info(f"✅ {field}: All {stats['unique']:,} values unique")
                    uniqueness_results[field] = {"status": "pass", "unique": stats['unique']}
                else:
                    logging.error(f"❌ {field}: {duplicates:,} duplicates found")
                    uniqueness_results[field] = {"status": "fail", "duplicates": duplicates}
            
            validation_results['uniqueness'] = uniqueness_results
            
            return validation_results

    def execute(self):
        """Execute all Wave 10 scripts with comprehensive validation"""
        overall_start = datetime.utcnow()
        
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("🎯 WAVE 10 EXECUTION: SBOM INTEGRATION (140,000 NODES)")
        logging.info("=" * 80)
        logging.info(f"Start Time: {overall_start.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        logging.info("=" * 80)
        
        scripts = [
            ("wave_10_components.py", 50000, "Software Components"),
            ("wave_10_dependencies.py", 40000, "Dependencies"),
            ("wave_10_build.py", 20000, "Build Information"),
            ("wave_10_licenses.py", 15000, "Licenses"),
            ("wave_10_provenance.py", 15000, "Provenance & Attestation")
        ]
        
        execution_stats = []
        
        try:
            # Execute all scripts
            for script_name, expected_nodes, category in scripts:
                stats = self.run_script(script_name, expected_nodes)
                stats['category'] = category
                execution_stats.append(stats)
            
            # Comprehensive validation
            validation_results = self.validate_wave10_nodes()
            
            # Final summary
            overall_duration = (datetime.utcnow() - overall_start).total_seconds()
            total_nodes = sum(s['expected_nodes'] for s in execution_stats)
            overall_rate = total_nodes / overall_duration if overall_duration > 0 else 0
            
            logging.info(f"\n{'='*80}")
            logging.info("🎉 WAVE 10 EXECUTION COMPLETE")
            logging.info(f"{'='*80}")
            logging.info(f"Total Nodes Created: {total_nodes:,}")
            logging.info(f"Total Execution Time: {overall_duration:.2f}s")
            logging.info(f"Overall Creation Rate: {overall_rate:.2f} nodes/second")
            logging.info(f"{'='*80}")
            
            # Per-script performance
            logging.info("\n📊 PER-SCRIPT PERFORMANCE:")
            for stats in execution_stats:
                logging.info(f"  • {stats['category']}: {stats['duration']:.2f}s ({stats['rate']:.2f} nodes/s)")
            
            # Validation summary
            all_passed = True
            for category, result in validation_results.items():
                if isinstance(result, dict) and result.get('status') == 'fail':
                    all_passed = False
                    break
            
            if all_passed:
                logging.info(f"\n✅ ALL VALIDATIONS PASSED")
            else:
                logging.error(f"\n❌ SOME VALIDATIONS FAILED - Review logs above")
            
            logging.info(f"{'='*80}\n")
            
            self.log_operation("wave_10_master_complete", {
                "total_nodes": total_nodes,
                "duration": overall_duration,
                "rate": overall_rate,
                "validation_status": "pass" if all_passed else "fail",
                "scripts_executed": len(execution_stats)
            })
            
            return 0 if all_passed else 1
            
        except Exception as e:
            logging.error(f"\n❌ WAVE 10 EXECUTION FAILED: {e}")
            self.log_operation("wave_10_master_failed", {"error": str(e)})
            return 1
        finally:
            self.driver.close()

if __name__ == "__main__":
    executor = Wave10MasterExecutor()
    sys.exit(executor.execute())
