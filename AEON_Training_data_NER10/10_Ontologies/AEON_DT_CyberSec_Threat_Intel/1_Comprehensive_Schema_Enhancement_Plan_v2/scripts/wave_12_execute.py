#!/usr/bin/env python3
"""Wave 12 Master Executor: Social Media & Confidence - 4,000 nodes"""
import subprocess, logging, json, sys
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave12MasterExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.scripts_dir = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2/scripts"

    def run_script(self, script_name: str, expected_nodes: int) -> dict:
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
                timeout=300
            )
            duration = (datetime.utcnow() - start_time).total_seconds()

            logging.info(result.stdout)

            return {
                "script": script_name,
                "status": "success",
                "duration": duration,
                "expected_nodes": expected_nodes,
                "rate": expected_nodes / duration if duration > 0 else 0
            }

        except subprocess.CalledProcessError as e:
            logging.error(f"{script_name} failed: {e}")
            logging.error(f"STDOUT: {e.stdout}")
            logging.error(f"STDERR: {e.stderr}")
            raise

    def validate_wave12_nodes(self) -> dict:
        logging.info(f"\n{'='*80}")
        logging.info("🔍 WAVE 12 COMPREHENSIVE VALIDATION")
        logging.info(f"{'='*80}")

        with self.driver.session() as session:
            # Category validation
            categories = {
                "Social Media": ["SocialMediaAccount", "SocialMediaPost"],
                "Threat Social": ["ThreatActorSocialProfile", "SocialNetwork", "BotNetwork"],
                "Confidence": ["ConfidenceScore", "IntelligenceSource", "Evidence"]
            }

            expected_totals = {
                "Social Media": 1000,
                "Threat Social": 1000,
                "Confidence": 2000
            }

            validation_results = {}

            for category, node_types in categories.items():
                labels_str = ", ".join([f"'{label}'" for label in node_types])
                query = f"""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE12'
                  AND any(label IN labels(n) WHERE label IN [{labels_str}])
                RETURN count(n) as count
                """
                result = session.run(query)
                count = result.single()['count']
                expected = expected_totals[category]
                status = "✅" if count == expected else "❌"

                logging.info(f"{status} {category}: {count:,} (expected: {expected:,})")
                validation_results[category] = {
                    "count": count,
                    "expected": expected,
                    "status": "pass" if count == expected else "fail"
                }

            # Total Wave 12 nodes
            logging.info(f"\n{'='*80}")
            result = session.run("""
            MATCH (n) WHERE n.created_by = 'AEON_INTEGRATION_WAVE12'
            RETURN count(n) as total
            """)
            actual_total = result.single()['total']
            expected_total = 4000

            if actual_total == expected_total:
                logging.info(f"✅ WAVE 12 TOTAL: {actual_total:,} nodes (expected: {expected_total:,})")
                validation_results['total_wave12'] = {"status": "pass", "count": actual_total}
            else:
                logging.error(f"❌ WAVE 12 TOTAL MISMATCH: {actual_total:,} (expected: {expected_total:,})")
                validation_results['total_wave12'] = {"status": "fail", "count": actual_total}

            # CVE Preservation
            logging.info(f"\n{'='*80}")
            logging.info("🛡️ CVE PRESERVATION CHECK")
            logging.info(f"{'='*80}")

            result = session.run("MATCH (cve:CVE) RETURN count(cve) as cve_count")
            cve_count = result.single()['cve_count']
            expected_cve = 267487

            if cve_count == expected_cve:
                logging.info(f"✅ CVE PRESERVATION: {cve_count:,} CVE nodes intact")
                validation_results['cve_preservation'] = {"status": "pass", "count": cve_count}
            else:
                logging.error(f"❌ CVE DATA LOSS: {cve_count:,} CVE nodes (expected: {expected_cve:,})")
                validation_results['cve_preservation'] = {"status": "fail", "count": cve_count}

            # Uniqueness validation
            logging.info(f"\n{'='*80}")
            logging.info("🔑 UNIQUENESS VALIDATION")
            logging.info(f"{'='*80}")

            result = session.run("""
            MATCH (n) WHERE n.created_by = 'AEON_INTEGRATION_WAVE12'
            WITH count(n) as total, count(DISTINCT n.node_id) as unique
            RETURN total, unique, total - unique as duplicates
            """)
            stats = result.single()

            if stats['duplicates'] == 0:
                logging.info(f"✅ node_id: All {stats['unique']:,} values unique")
                validation_results['uniqueness'] = {"status": "pass"}
            else:
                logging.error(f"❌ node_id: {stats['duplicates']:,} duplicates found")
                validation_results['uniqueness'] = {"status": "fail"}

            # Confidence score range validation
            logging.info(f"\n{'='*80}")
            logging.info("📊 CONFIDENCE SCORE VALIDATION")
            logging.info(f"{'='*80}")

            result = session.run("""
            MATCH (cs:ConfidenceScore) WHERE cs.created_by = 'AEON_INTEGRATION_WAVE12'
            WITH count(cs) as total,
                 count(CASE WHEN cs.confidenceScore < 0 OR cs.confidenceScore > 1 THEN 1 END) as out_of_range
            RETURN total, out_of_range
            """)
            conf_stats = result.single()

            if conf_stats['out_of_range'] == 0:
                logging.info(f"✅ Confidence scores: All {conf_stats['total']:,} scores in valid range (0-1)")
                validation_results['confidence_range'] = {"status": "pass"}
            else:
                logging.error(f"❌ Confidence scores: {conf_stats['out_of_range']:,} out of range")
                validation_results['confidence_range'] = {"status": "fail"}

            return validation_results

    def execute(self):
        overall_start = datetime.utcnow()

        logging.info("\n")
        logging.info("=" * 80)
        logging.info("🎯 WAVE 12 EXECUTION: SOCIAL MEDIA & CONFIDENCE (4,000 NODES)")
        logging.info("=" * 80)
        logging.info(f"Start Time: {overall_start.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        logging.info("=" * 80)

        scripts = [
            ("wave_12_social_media.py", 1000, "Social Media"),
            ("wave_12_threat_social.py", 1000, "Threat Social"),
            ("wave_12_confidence.py", 2000, "Confidence")
        ]

        execution_stats = []

        try:
            # Execute all scripts
            for script_name, expected_nodes, category in scripts:
                stats = self.run_script(script_name, expected_nodes)
                stats['category'] = category
                execution_stats.append(stats)

            # Comprehensive validation
            validation_results = self.validate_wave12_nodes()

            # Final summary
            overall_duration = (datetime.utcnow() - overall_start).total_seconds()
            total_nodes = sum(s['expected_nodes'] for s in execution_stats)
            overall_rate = total_nodes / overall_duration if overall_duration > 0 else 0

            logging.info(f"\n{'='*80}")
            logging.info("🎉 WAVE 12 EXECUTION COMPLETE")
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
            all_passed = all(
                result.get('status') == 'pass'
                for result in validation_results.values()
                if isinstance(result, dict)
            )

            if all_passed:
                logging.info(f"\n✅ ALL VALIDATIONS PASSED")
            else:
                logging.error(f"\n❌ SOME VALIDATIONS FAILED")

            logging.info(f"{'='*80}\n")

            return 0 if all_passed else 1

        except Exception as e:
            logging.error(f"\n❌ WAVE 12 EXECUTION FAILED: {e}")
            return 1
        finally:
            self.driver.close()

if __name__ == "__main__":
    executor = Wave12MasterExecutor()
    sys.exit(executor.execute())
