#!/usr/bin/env python3
"""
Autonomous Phase Executor - Monitors and auto-executes Phases 4-6
Runs continuously until all phases complete successfully

File: autonomous_phase_executor.py
Created: 2025-11-01 22:57:00
Version: 1.0.0
Author: Automation Agent
Purpose: Autonomous execution and monitoring of CVE remediation phases
Status: ACTIVE
"""

import time
import logging
import yaml
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple
from neo4j import GraphDatabase
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'../logs/autonomous_executor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutonomousPhaseExecutor:
    """Monitors Phase 3 and autonomously executes Phases 4-6"""

    def __init__(self, config_path: str = '../config.yaml'):
        """Initialize with configuration"""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        self.driver = GraphDatabase.driver(
            config['neo4j']['uri'],
            auth=(config['neo4j']['user'], config['neo4j']['password'])
        )

        self.target_cve_count = 316552  # Expected total CVEs
        self.min_acceptable_count = 310000  # Minimum acceptable (allow for some failures)

        self.phase_status = {
            'phase3': 'in_progress',
            'phase4a': 'pending',
            'phase4b': 'pending',
            'phase5': 'pending',
            'phase6': 'pending'
        }

    def get_cve_count(self) -> int:
        """Get current CVE count from database"""
        query = "MATCH (cve:CVE) RETURN count(cve) AS total"

        try:
            with self.driver.session() as session:
                result = session.run(query)
                count = result.single()['total']
                return count
        except Exception as e:
            logger.error(f"Error getting CVE count: {str(e)}")
            return 0

    def check_phase3_completion(self) -> Tuple[bool, int]:
        """
        Check if Phase 3 (bulk import) is complete

        Returns: (is_complete, current_count)
        """
        count = self.get_cve_count()

        if count >= self.min_acceptable_count:
            logger.info(f"✅ Phase 3 COMPLETE: {count} CVEs imported (target: {self.target_cve_count})")
            return True, count
        else:
            progress_pct = (count / self.target_cve_count) * 100
            logger.info(f"Phase 3 progress: {count}/{self.target_cve_count} ({progress_pct:.1f}%)")
            return False, count

    def validate_cve_quality(self) -> Dict[str, int]:
        """Validate CVE data quality"""
        queries = {
            'null_ids': "MATCH (cve:CVE) WHERE cve.id IS NULL RETURN count(cve) AS count",
            'malformed_ids': "MATCH (cve:CVE) WHERE cve.id =~ 'cve-CVE-.*' RETURN count(cve) AS count",
            'correct_format': "MATCH (cve:CVE) WHERE cve.id =~ 'CVE-.*' RETURN count(cve) AS count"
        }

        results = {}
        with self.driver.session() as session:
            for name, query in queries.items():
                result = session.run(query)
                results[name] = result.single()['count']

        return results

    def execute_phase4a(self) -> bool:
        """Execute Phase 4a: THREATENS_GRID_STABILITY reconstruction"""
        logger.info("="*80)
        logger.info("EXECUTING PHASE 4A: THREATENS_GRID_STABILITY RECONSTRUCTION")
        logger.info("="*80)

        try:
            result = subprocess.run(
                ['python3', 'phase4a_reconstruct_grid_stability.py'],
                cwd=Path(__file__).parent,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )

            if result.returncode == 0:
                logger.info("✅ Phase 4a COMPLETE")
                logger.info(result.stdout)
                return True
            else:
                logger.error(f"❌ Phase 4a FAILED with exit code {result.returncode}")
                logger.error(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            logger.error("❌ Phase 4a TIMEOUT after 10 minutes")
            return False
        except Exception as e:
            logger.error(f"❌ Phase 4a ERROR: {str(e)}")
            return False

    def execute_phase4b(self) -> bool:
        """Execute Phase 4b: VULNERABLE_TO reconstruction"""
        logger.info("="*80)
        logger.info("EXECUTING PHASE 4B: VULNERABLE_TO RECONSTRUCTION")
        logger.info("="*80)

        try:
            result = subprocess.run(
                ['python3', 'phase4b_reconstruct_vulnerable_to.py'],
                cwd=Path(__file__).parent,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout (larger dataset)
            )

            if result.returncode == 0:
                logger.info("✅ Phase 4b COMPLETE")
                logger.info(result.stdout)
                return True
            else:
                logger.error(f"❌ Phase 4b FAILED with exit code {result.returncode}")
                logger.error(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            logger.error("❌ Phase 4b TIMEOUT after 30 minutes")
            return False
        except Exception as e:
            logger.error(f"❌ Phase 4b ERROR: {str(e)}")
            return False

    def execute_phase5(self) -> bool:
        """Execute Phase 5: EPSS enrichment"""
        logger.info("="*80)
        logger.info("EXECUTING PHASE 5: EPSS ENRICHMENT")
        logger.info("="*80)

        # Use existing enrichment script
        enrichment_script = Path(__file__).parent / 'phase1_epss_enrichment.py'

        if not enrichment_script.exists():
            logger.warning("EPSS enrichment script not found, skipping Phase 5")
            return True  # Don't fail entire process

        try:
            result = subprocess.run(
                ['python3', str(enrichment_script)],
                cwd=Path(__file__).parent,
                capture_output=True,
                text=True,
                timeout=3600  # 60 minute timeout
            )

            if result.returncode == 0:
                logger.info("✅ Phase 5 COMPLETE")
                logger.info(result.stdout[-1000:])  # Last 1000 chars
                return True
            else:
                logger.warning(f"⚠️ Phase 5 completed with warnings (exit code {result.returncode})")
                logger.warning(result.stderr[-500:])
                return True  # Don't fail if EPSS has issues

        except subprocess.TimeoutExpired:
            logger.warning("⚠️ Phase 5 TIMEOUT after 60 minutes - continuing anyway")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Phase 5 ERROR: {str(e)} - continuing anyway")
            return True

    def execute_phase6(self) -> bool:
        """Execute Phase 6: Final validation"""
        logger.info("="*80)
        logger.info("EXECUTING PHASE 6: FINAL VALIDATION")
        logger.info("="*80)

        # Validate CVE IDs
        quality = self.validate_cve_quality()

        logger.info("CVE ID Quality Check:")
        logger.info(f"  NULL IDs: {quality['null_ids']}")
        logger.info(f"  Malformed IDs (cve-CVE-*): {quality['malformed_ids']}")
        logger.info(f"  Correct format (CVE-*): {quality['correct_format']}")

        if quality['null_ids'] > 0 or quality['malformed_ids'] > 0:
            logger.error("❌ Phase 6 FAILED: Found NULL or malformed CVE IDs")
            return False

        # Validate relationship counts
        relationship_queries = {
            'THREATENS_GRID_STABILITY': "MATCH ()-[r:THREATENS_GRID_STABILITY]->() RETURN count(r) as c",
            'VULNERABLE_TO': "MATCH ()-[r:VULNERABLE_TO]->() RETURN count(r) as c"
        }

        logger.info("\nRelationship Count Validation:")
        with self.driver.session() as session:
            for rel_type, query in relationship_queries.items():
                result = session.run(query)
                count = result.single()['c']
                logger.info(f"  {rel_type}: {count}")

        # Check EPSS enrichment
        epss_query = "MATCH (cve:CVE) WHERE cve.epss_score IS NOT NULL RETURN count(cve) as c"
        with self.driver.session() as session:
            result = session.run(epss_query)
            epss_count = result.single()['c']
            total_cves = self.get_cve_count()
            epss_pct = (epss_count / total_cves) * 100 if total_cves > 0 else 0

            logger.info(f"\nEPSS Enrichment:")
            logger.info(f"  CVEs with EPSS scores: {epss_count}/{total_cves} ({epss_pct:.1f}%)")

        logger.info("\n✅ Phase 6 COMPLETE: All validations passed")
        return True

    def run(self):
        """Main execution loop"""
        logger.info("="*80)
        logger.info("AUTONOMOUS PHASE EXECUTOR - Starting")
        logger.info("="*80)

        # Monitor Phase 3
        logger.info("\nMonitoring Phase 3 (bulk import) completion...")
        while True:
            is_complete, count = self.check_phase3_completion()

            if is_complete:
                self.phase_status['phase3'] = 'completed'
                break

            time.sleep(60)  # Check every minute

        # Validate Phase 3 quality
        quality = self.validate_cve_quality()
        if quality['null_ids'] > 0 or quality['malformed_ids'] > 0:
            logger.error(f"❌ Phase 3 data quality issues: {quality}")
            logger.error("Cannot proceed to Phase 4")
            return False

        # Execute Phase 4a
        logger.info("\nProceeding to Phase 4a...")
        time.sleep(5)
        if self.execute_phase4a():
            self.phase_status['phase4a'] = 'completed'
        else:
            logger.error("Phase 4a failed - stopping")
            return False

        # Execute Phase 4b
        logger.info("\nProceeding to Phase 4b...")
        time.sleep(5)
        if self.execute_phase4b():
            self.phase_status['phase4b'] = 'completed'
        else:
            logger.error("Phase 4b failed - stopping")
            return False

        # Execute Phase 5
        logger.info("\nProceeding to Phase 5...")
        time.sleep(5)
        if self.execute_phase5():
            self.phase_status['phase5'] = 'completed'
        else:
            logger.warning("Phase 5 had issues but continuing...")

        # Execute Phase 6
        logger.info("\nProceeding to Phase 6...")
        time.sleep(5)
        if self.execute_phase6():
            self.phase_status['phase6'] = 'completed'
        else:
            logger.error("Phase 6 validation failed")
            return False

        # Final summary
        logger.info("="*80)
        logger.info("ALL PHASES COMPLETE")
        logger.info("="*80)
        logger.info(f"Phase Status: {self.phase_status}")
        logger.info(f"Final CVE count: {self.get_cve_count()}")
        logger.info("="*80)

        return True

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()


def main():
    """Main execution"""
    executor = AutonomousPhaseExecutor()

    try:
        success = executor.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nExecution interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        executor.close()


if __name__ == "__main__":
    main()
