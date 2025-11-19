#!/usr/bin/env python3
"""
Wave 12 Subdomain Enhancement - Add missing subdomain labels

Discovery found 800 nodes missing subdomain labels:
- ConfidenceScore (800) → Intelligence_Analysis

Operation: ADD_LABELS (preserves all existing data)
Pattern: SKIP 0 pagination (proven in Phases 1-5)

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


class Wave12SubdomainEnhancer:
    """Add missing subdomain labels to Wave 12 Deep Discovery & Intelligence Analysis nodes"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "wave_12_subdomain_enhancement.jsonl"
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
            f.write(json.dumps(log_entry) + '\n')

    def enhance_confidence_scores(self) -> int:
        """Add Intelligence_Analysis subdomain to ConfidenceScore nodes"""
        total_enhanced = 0
        batch_size = 100

        with self.driver.session() as session:
            while True:
                result = session.run("""
                    MATCH (n:ConfidenceScore)
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE12'
                    AND NOT n:Intelligence_Analysis
                    WITH n LIMIT $batch_size
                    SET n:Intelligence_Analysis
                    RETURN count(n) as enhanced
                """, batch_size=batch_size)

                batch_enhanced = result.single()["enhanced"]

                if batch_enhanced == 0:
                    break

                total_enhanced += batch_enhanced
                print(f"  Enhanced {batch_enhanced} nodes (total: {total_enhanced})")

        return total_enhanced

    def validate_cve_preservation(self) -> bool:
        """Verify CVE baseline unchanged"""
        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]
            return cve_count == 267487

    def validate_completion(self) -> Dict[str, Any]:
        """Validate Wave 12 subdomain enhancement"""
        with self.driver.session() as session:
            # Total Wave 12 nodes
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE12'
                RETURN count(n) as total
            """)
            total_nodes = result.single()["total"]

            # Nodes with subdomain
            result = session.run("""
                MATCH (n)
                WHERE n.created_by = 'AEON_INTEGRATION_WAVE12'
                AND (n:Social_Media_Intelligence OR n:Threat_Actor_Analysis OR n:Intelligence_Analysis)
                RETURN count(n) as with_subdomain
            """)
            with_subdomain = result.single()["with_subdomain"]

            # Subdomain breakdown
            subdomains = {}
            for subdomain in ["Social_Media_Intelligence", "Threat_Actor_Analysis", "Intelligence_Analysis"]:
                result = session.run(f"""
                    MATCH (n:{subdomain})
                    WHERE n.created_by = 'AEON_INTEGRATION_WAVE12'
                    RETURN count(n) as count
                """)
                subdomains[subdomain] = result.single()["count"]

            # CVE check
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]

        return {
            "total_nodes": total_nodes,
            "with_subdomain": with_subdomain,
            "subdomains": subdomains,
            "coverage_pct": (with_subdomain / total_nodes * 100) if total_nodes > 0 else 0,
            "cve_count": cve_count,
            "cve_preserved": cve_count == 267487,
            "complete": with_subdomain == total_nodes
        }

    def execute(self) -> bool:
        """Execute Wave 12 subdomain enhancement"""
        try:
            print("=" * 80)
            print("WAVE 12: SUBDOMAIN LABEL ENHANCEMENT")
            print("=" * 80)
            print()
            print("Target: 800 nodes missing subdomain labels")
            print("Operation: Add Intelligence_Analysis subdomain to ConfidenceScore nodes")
            print()

            print("[1/5] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 12 Subdomain Enhancement - Start",
                phase="PHASE_5",
                wave="WAVE12"
            )
            print(f"✅ Checkpoint: {checkpoint_id}")
            print()

            print("[2/5] Adding Intelligence_Analysis subdomain to ConfidenceScore nodes...")
            enhanced_count = self.enhance_confidence_scores()
            print(f"✅ Enhanced {enhanced_count:,} ConfidenceScore nodes")
            print()

            print("[3/5] Validating enhancement...")
            validation = self.validate_completion()
            print(f"Total nodes: {validation['total_nodes']:,}")
            print(f"With subdomain: {validation['with_subdomain']:,} ({validation['coverage_pct']:.1f}%)")
            print()
            print("Subdomain distribution:")
            for subdomain, count in validation['subdomains'].items():
                print(f"  • {subdomain}: {count:,} nodes")
            print()

            if not validation['cve_preserved']:
                print("❌ CRITICAL: CVE preservation failed!")
                return False

            print(f"CVE Preservation: ✅ INTACT ({validation['cve_count']:,} nodes)")
            print()

            print("[4/5] Creating post-enhancement checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Wave 12 Subdomain Enhancement - Complete",
                phase="PHASE_5",
                wave="WAVE12",
                metadata={
                    "enhanced_count": enhanced_count,
                    "validation": validation
                }
            )
            print(f"✅ Final checkpoint: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ WAVE 12 SUBDOMAIN ENHANCEMENT COMPLETE")
            print("=" * 80)
            print()
            print(f"Total enhanced: {enhanced_count:,} nodes")
            print(f"Coverage: {validation['coverage_pct']:.1f}%")
            print(f"Status: {'✅ 100% COMPLETE' if validation['complete'] else '⚠️  PARTIAL'}")
            print()

            return validation['complete'] and validation['cve_preserved']

        except Exception as e:
            self._log("execute", "FAILED", {"error": str(e)})
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            self.checkpoint_mgr.close()
            self.driver.close()


def main():
    enhancer = Wave12SubdomainEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
