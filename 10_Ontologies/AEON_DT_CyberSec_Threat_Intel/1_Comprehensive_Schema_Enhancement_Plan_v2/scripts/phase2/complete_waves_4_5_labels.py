#!/usr/bin/env python3
"""
Wave 4-5 Label Completion - Add missing domain labels

Wave 4: 5,180 nodes need ICS_THREAT_INTEL label
Wave 5: 137 nodes need ICS_FRAMEWORK label

Operation: ADD_LABELS to all nodes based on created_by tracking
Pattern: SKIP 0 pagination (proven in Waves 1-3)

Generated: 2025-10-31
Version: 1.0.1
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


class Wave45LabelCompleter:
    """Complete Wave 4-5 with missing domain labels"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "waves_4_5_completion.jsonl"
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

    def add_wave4_domain_labels(self) -> int:
        """Add ICS_THREAT_INTEL label to all Wave 4 nodes"""
        total_enhanced = 0
        batch_size = 500

        with self.driver.session() as session:
            while True:
                result = session.run(f"""
                    MATCH (n)
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE4'
                    AND NOT n:ICS_THREAT_INTEL
                    WITH n LIMIT {batch_size}
                    SET n:ICS_THREAT_INTEL
                    RETURN count(n) as enhanced
                """)
                batch_enhanced = result.single()["enhanced"]

                if batch_enhanced == 0:
                    break

                total_enhanced += batch_enhanced
                print(f"  Progress: {total_enhanced:,} nodes labeled...")

        return total_enhanced

    def add_wave5_domain_labels(self) -> int:
        """Add ICS_FRAMEWORK label to all Wave 5 nodes"""
        total_enhanced = 0
        batch_size = 100

        with self.driver.session() as session:
            while True:
                result = session.run(f"""
                    MATCH (n)
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE5'
                    AND NOT n:ICS_FRAMEWORK
                    WITH n LIMIT {batch_size}
                    SET n:ICS_FRAMEWORK
                    RETURN count(n) as enhanced
                """)
                batch_enhanced = result.single()["enhanced"]

                if batch_enhanced == 0:
                    break

                total_enhanced += batch_enhanced
                print(f"  Progress: {total_enhanced:,} nodes labeled...")

        return total_enhanced

    def validate_cve_preservation(self) -> bool:
        """Verify CVE baseline unchanged"""
        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]
            preserved = (cve_count == 267487)
            return preserved

    def validate_completion(self) -> Dict[str, Any]:
        """Validate Wave 4-5 completion"""
        with self.driver.session() as session:
            # Wave 4 validation
            result = session.run("""
                MATCH (n:ICS_THREAT_INTEL)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE4'
                RETURN count(n) as count
            """)
            wave4_labeled = result.single()["count"]

            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE4'
                RETURN count(n) as count
            """)
            wave4_total = result.single()["count"]

            # Wave 5 validation
            result = session.run("""
                MATCH (n:ICS_FRAMEWORK)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE5'
                RETURN count(n) as count
            """)
            wave5_labeled = result.single()["count"]

            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE5'
                RETURN count(n) as count
            """)
            wave5_total = result.single()["count"]

            # CVE check
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        return {
            "wave4_labeled": wave4_labeled,
            "wave4_total": wave4_total,
            "wave4_complete": wave4_labeled == wave4_total,
            "wave5_labeled": wave5_labeled,
            "wave5_total": wave5_total,
            "wave5_complete": wave5_labeled == wave5_total,
            "cve_count": cve_count,
            "cve_preserved": cve_count == 267487
        }

    def execute(self) -> bool:
        """Execute Wave 4-5 label completion"""
        try:
            print("=" * 80)
            print("WAVE 4-5 LABEL COMPLETION")
            print("=" * 80)
            print()

            print("[1/5] Creating pre-completion checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 4-5 Label Completion - Start",
                phase="PHASE_2",
                wave="WAVES_4_5"
            )
            print(f"✅ Checkpoint: {checkpoint_id}")
            print()

            print("[2/5] Adding ICS_THREAT_INTEL label to Wave 4 nodes...")
            wave4_enhanced = self.add_wave4_domain_labels()
            print(f"✅ Enhanced {wave4_enhanced:,} Wave 4 nodes")
            print()

            print("[3/5] Adding ICS_FRAMEWORK label to Wave 5 nodes...")
            wave5_enhanced = self.add_wave5_domain_labels()
            print(f"✅ Enhanced {wave5_enhanced:,} Wave 5 nodes")
            print()

            print("[4/5] Validating completion...")
            validation = self.validate_completion()
            print(f"Wave 4: {validation['wave4_labeled']:,}/{validation['wave4_total']:,} labeled")
            print(f"Wave 5: {validation['wave5_labeled']:,}/{validation['wave5_total']:,} labeled")
            print(f"CVE preserved: {validation['cve_preserved']}")
            print()

            if not validation['cve_preserved']:
                print("❌ CRITICAL: CVE preservation failed!")
                return False

            print("[5/5] Creating post-completion checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 4-5 Label Completion - Complete",
                phase="PHASE_2",
                wave="WAVES_4_5",
                metadata={"validation": validation}
            )
            print(f"✅ Final checkpoint: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 4-5 LABEL COMPLETION SUCCESSFUL")
            print("=" * 80)
            print()
            print(f"Wave 4: {validation['wave4_labeled']:,} nodes ({'✅ COMPLETE' if validation['wave4_complete'] else '❌ INCOMPLETE'})")
            print(f"Wave 5: {validation['wave5_labeled']:,} nodes ({'✅ COMPLETE' if validation['wave5_complete'] else '❌ INCOMPLETE'})")
            print(f"CVE preservation: {'✅ INTACT' if validation['cve_preserved'] else '❌ FAILED'}")
            print()

            return validation['wave4_complete'] and validation['wave5_complete'] and validation['cve_preserved']

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
    completer = Wave45LabelCompleter()
    success = completer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
