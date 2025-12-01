#!/usr/bin/env python3
"""
CVE Label Enhancement - Add taxonomy labels to 267,487 CVE nodes
Hybrid approach: Preserve all existing CVE data + add domain + subdomain + functional role labels

Total CVE nodes: 267,487
Operation: ADD_LABELS (preserves all existing data)
Labels to add: VULNERABILITY + CVE_Database + Threat_Intelligence

Pattern: SKIP 0 pagination (proven in Phases 1-2)
Batch size: 1000 nodes (optimized for large volume)

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from neo4j import GraphDatabase
    from checkpoint.checkpoint_manager import CheckpointManager
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    sys.exit(1)


class CVELabelEnhancer:
    """Enhance CVE nodes with VULNERABILITY taxonomy labels"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "cve_label_enhancement.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint_mgr = CheckpointManager(neo4j_uri, neo4j_user, neo4j_password)

    def _log(self, operation: str, status: str, details: Dict[str, Any] = None):
        """Log operation"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": status,
            "details": details or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\\n')

    def add_cve_taxonomy_labels(self) -> int:
        """
        Add VULNERABILITY + CVE_Database + Threat_Intelligence labels to all CVE nodes

        Labels to add:
        - VULNERABILITY: Domain label
        - CVE_Database: Subdomain label
        - Threat_Intelligence: Functional role label

        Returns:
            int: Number of CVE nodes enhanced
        """
        total_enhanced = 0
        batch_size = 1000
        start_time = datetime.now()

        print(f"Starting CVE label enhancement at {start_time.strftime('%H:%M:%S')}")
        print(f"Target: 267,487 CVE nodes")
        print(f"Batch size: {batch_size:,} nodes")
        print()

        with self.driver.session() as session:
            while True:
                batch_start = datetime.now()

                result = session.run(f"""
                    MATCH (n:CVE)
                    WHERE NOT n:VULNERABILITY
                    WITH n LIMIT {batch_size}
                    SET n:VULNERABILITY:CVE_Database:Threat_Intelligence
                    RETURN count(n) as enhanced
                """)
                batch_enhanced = result.single()["enhanced"]

                if batch_enhanced == 0:
                    break

                total_enhanced += batch_enhanced
                batch_duration = (datetime.now() - batch_start).total_seconds()

                # Progress reporting every 10 batches
                if total_enhanced % (batch_size * 10) == 0:
                    progress_pct = (total_enhanced / 267487) * 100
                    elapsed = (datetime.now() - start_time).total_seconds()
                    rate = total_enhanced / elapsed if elapsed > 0 else 0
                    eta_seconds = (267487 - total_enhanced) / rate if rate > 0 else 0
                    eta_minutes = eta_seconds / 60

                    print(f"  Progress: {total_enhanced:,} nodes ({progress_pct:.1f}%) | "
                          f"Rate: {rate:.0f} nodes/sec | "
                          f"ETA: {eta_minutes:.1f} min")

                    self._log(
                        "batch_progress",
                        "SUCCESS",
                        {
                            "total_enhanced": total_enhanced,
                            "progress_pct": round(progress_pct, 2),
                            "rate_per_sec": round(rate, 0),
                            "eta_minutes": round(eta_minutes, 1)
                        }
                    )

        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()

        print()
        print(f"Completed at {end_time.strftime('%H:%M:%S')}")
        print(f"Total duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
        print(f"Average rate: {total_enhanced/total_duration:.0f} nodes/second")

        return total_enhanced

    def validate_cve_enhancement(self) -> Dict[str, Any]:
        """
        Validate CVE label enhancement

        Returns:
            Dict with validation metrics
        """
        with self.driver.session() as session:
            # Count total CVE nodes
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            total_cve = result.single()["count"]

            # Count CVE nodes with VULNERABILITY label
            result = session.run("""
                MATCH (n:CVE:VULNERABILITY)
                RETURN count(n) as count
            """)
            cve_vulnerability = result.single()["count"]

            # Count CVE nodes with CVE_Database label
            result = session.run("""
                MATCH (n:CVE:CVE_Database)
                RETURN count(n) as count
            """)
            cve_database = result.single()["count"]

            # Count CVE nodes with Threat_Intelligence label
            result = session.run("""
                MATCH (n:CVE:Threat_Intelligence)
                RETURN count(n) as count
            """)
            cve_threat_intel = result.single()["count"]

            # Count CVE nodes with all three labels
            result = session.run("""
                MATCH (n:CVE:VULNERABILITY:CVE_Database:Threat_Intelligence)
                RETURN count(n) as count
            """)
            cve_complete = result.single()["count"]

        all_complete = (
            total_cve == 267487 and
            cve_complete == 267487
        )

        return {
            "total_cve": total_cve,
            "cve_with_vulnerability": cve_vulnerability,
            "cve_with_database": cve_database,
            "cve_with_threat_intel": cve_threat_intel,
            "cve_complete": cve_complete,
            "all_complete": all_complete,
            "coverage_pct": (cve_complete / total_cve * 100) if total_cve > 0 else 0
        }

    def execute(self) -> bool:
        """Execute CVE label enhancement workflow"""
        try:
            print("=" * 80)
            print("PHASE 3: CVE LABEL ENHANCEMENT")
            print("=" * 80)
            print()
            print("Target: 267,487 CVE nodes")
            print("Labels: VULNERABILITY + CVE_Database + Threat_Intelligence")
            print("Pattern: SKIP 0 pagination with 1000-node batches")
            print()

            print("[1/4] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="CVE Label Enhancement - Start",
                phase="PHASE_3",
                wave="CVE"
            )
            print(f"✅ Checkpoint: {checkpoint_id}")
            print()

            print("[2/4] Adding taxonomy labels to CVE nodes...")
            print("-" * 80)
            cve_enhanced = self.add_cve_taxonomy_labels()
            print(f"✅ Enhanced {cve_enhanced:,} CVE nodes")
            print()

            print("[3/4] Validating CVE enhancement...")
            validation = self.validate_cve_enhancement()
            print(f"Total CVE nodes: {validation['total_cve']:,}")
            print(f"CVE with VULNERABILITY: {validation['cve_with_vulnerability']:,}")
            print(f"CVE with CVE_Database: {validation['cve_with_database']:,}")
            print(f"CVE with Threat_Intelligence: {validation['cve_with_threat_intel']:,}")
            print(f"CVE fully labeled: {validation['cve_complete']:,}")
            print(f"Coverage: {validation['coverage_pct']:.1f}%")
            print()

            if not validation['all_complete']:
                print("⚠️  Warning: Not all CVE nodes fully labeled")
                print(f"   Expected: 267,487")
                print(f"   Actual: {validation['cve_complete']:,}")

            print("[4/4] Creating post-enhancement checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="CVE Label Enhancement - Complete",
                phase="PHASE_3",
                wave="CVE",
                metadata={"validation": validation}
            )
            print(f"✅ Final checkpoint: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ PHASE 3: CVE LABEL ENHANCEMENT COMPLETE")
            print("=" * 80)
            print()
            print(f"Enhanced: {cve_enhanced:,} CVE nodes")
            print(f"Coverage: {validation['coverage_pct']:.1f}%")
            print(f"Status: {'✅ ALL CVE NODES LABELED' if validation['all_complete'] else '⚠️  PARTIAL COMPLETION'}")
            print()

            return validation['all_complete']

        except Exception as e:
            self._log("execute", "FAILED", {"error": str(e)})
            print(f"\\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            self.checkpoint_mgr.close()
            self.driver.close()


def main():
    enhancer = CVELabelEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
