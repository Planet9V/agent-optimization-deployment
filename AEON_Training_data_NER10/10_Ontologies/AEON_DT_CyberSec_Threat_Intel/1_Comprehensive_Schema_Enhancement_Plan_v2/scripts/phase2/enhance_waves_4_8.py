#!/usr/bin/env python3
"""
Waves 4-8 Unified Label Enhancement - Add taxonomy labels to existing nodes
Hybrid approach: Preserve all existing data + add domain + subdomain + functional role labels

Total nodes: 12,768
- Wave 4 (ICS_THREAT_INTEL): 12,233 nodes
- Wave 5 (ICS_FRAMEWORK): 137 nodes
- Wave 6 (THREAT_INTEL_SHARING): 55 nodes
- Wave 7 (BEHAVIORAL): 57 nodes
- Wave 8 (PHYSICAL_SECURITY): 286 nodes

Operation: ADD_LABELS (preserves all existing data)
Pattern: SKIP 0 pagination (proven in Waves 1-3)

Generated: 2025-10-31
Version: 1.0.0
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from neo4j import GraphDatabase
    import yaml
    from checkpoint.checkpoint_manager import CheckpointManager
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    sys.exit(1)


class Waves48LabelEnhancer:
    """Enhance Waves 4-8 with taxonomy labels"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "waves_4_8_enhancement.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

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

    def enhance_wave(
        self,
        wave_num: int,
        wave_name: str,
        created_by: str,
        node_mappings: Dict[str, Dict]
    ) -> Dict[str, int]:
        """
        Enhance a single wave with taxonomy labels

        Args:
            wave_num: Wave number (4-8)
            wave_name: Wave display name
            created_by: Tracking property value
            node_mappings: Node type to label mappings from taxonomy

        Returns:
            Enhancement statistics
        """
        print(f"Processing {wave_name}...")
        print()

        enhancement_stats = {}

        with self.driver.session() as session:
            for node_type, config in node_mappings.items():
                labels_to_add = config['labels']
                expected_count = config['count']

                print(f"  {node_type}:")
                print(f"    Expected: {expected_count:,} nodes")
                print(f"    Adding labels: {', '.join(labels_to_add)}")

                total_enhanced = 0
                batch_size = 100

                # SKIP 0 pattern - process until no nodes remain
                while True:
                    enhance_query = f"""
                        MATCH (n:{node_type})
                        WHERE n.created_by = '{created_by}'
                        AND NOT n:{labels_to_add[0]}
                        WITH n
                        LIMIT {batch_size}
                        SET n:{':'.join(labels_to_add)}
                        RETURN count(n) as enhanced
                    """

                    result = session.run(enhance_query)
                    batch_enhanced = result.single()["enhanced"]

                    if batch_enhanced == 0:
                        break

                    total_enhanced += batch_enhanced

                enhancement_stats[node_type] = {
                    "expected": expected_count,
                    "enhanced": total_enhanced,
                    "labels_added": labels_to_add
                }

                status = "✅" if total_enhanced == expected_count else "⚠️"
                print(f"    {status} Enhanced: {total_enhanced:,} nodes")
                print()

        return enhancement_stats

    def validate_cve_preservation(self) -> bool:
        """Verify CVE baseline unchanged"""
        with self.driver.session() as session:
            result = session.run("MATCH (n:CVE) RETURN count(n) as count")
            cve_count = result.single()["count"]
            preserved = (cve_count == 267487)
            return preserved

    def execute(self) -> bool:
        """Execute Waves 4-8 enhancement"""
        try:
            print("=" * 80)
            print("WAVES 4-8 UNIFIED LABEL ENHANCEMENT")
            print("=" * 80)
            print()

            print("[1/8] Creating pre-enhancement checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Waves 4-8 Label Enhancement - Start",
                phase="PHASE_2",
                wave="WAVES_4_8"
            )
            print(f"✅ Checkpoint: {checkpoint_id}")
            print()

            all_stats = {}

            # Wave 4: ICS_THREAT_INTEL (12,233 nodes)
            print("[2/8] Wave 4: ICS Threat Intelligence (12,233 nodes)")
            print("-" * 80)
            wave4_stats = self.enhance_wave(
                4,
                "ICS Threat Intelligence",
                "AEON_INTEGRATION_WAVE4",
                self.taxonomy['wave_4']['node_type_mappings']
            )
            all_stats['wave_4'] = wave4_stats
            print()

            # Wave 5: ICS_FRAMEWORK (137 nodes)
            print("[3/8] Wave 5: ICS Framework (137 nodes)")
            print("-" * 80)
            wave5_stats = self.enhance_wave(
                5,
                "ICS Framework",
                "AEON_INTEGRATION_WAVE5",
                self.taxonomy['wave_5']['node_type_mappings']
            )
            all_stats['wave_5'] = wave5_stats
            print()

            # Wave 6: THREAT_INTEL_SHARING (55 nodes)
            print("[4/8] Wave 6: Threat Intel Sharing (55 nodes)")
            print("-" * 80)
            wave6_stats = self.enhance_wave(
                6,
                "Threat Intel Sharing",
                "AEON_INTEGRATION_WAVE6",
                self.taxonomy['wave_6']['node_type_mappings']
            )
            all_stats['wave_6'] = wave6_stats
            print()

            # Wave 7: BEHAVIORAL (57 nodes)
            print("[5/8] Wave 7: Behavioral (57 nodes)")
            print("-" * 80)
            wave7_stats = self.enhance_wave(
                7,
                "Behavioral",
                "AEON_INTEGRATION_WAVE7",
                self.taxonomy['wave_7']['node_type_mappings']
            )
            all_stats['wave_7'] = wave7_stats
            print()

            # Wave 8: PHYSICAL_SECURITY (286 nodes)
            print("[6/8] Wave 8: Physical Security (286 nodes)")
            print("-" * 80)
            wave8_stats = self.enhance_wave(
                8,
                "Physical Security",
                "AEON_INTEGRATION_WAVE8",
                self.taxonomy['wave_8']['node_type_mappings']
            )
            all_stats['wave_8'] = wave8_stats
            print()

            # Validation
            print("[7/8] Validating CVE preservation...")
            if not self.validate_cve_preservation():
                print("❌ CRITICAL: CVE preservation failed!")
                return False
            print("✅ CVE baseline preserved (267,487 nodes)")
            print()

            print("[8/8] Creating post-enhancement checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Waves 4-8 Label Enhancement - Complete",
                phase="PHASE_2",
                wave="WAVES_4_8",
                metadata={"enhancement_stats": all_stats}
            )
            print(f"✅ Final checkpoint: {final_checkpoint_id}")
            print()

            # Summary
            print("=" * 80)
            print("✅ WAVES 4-8 LABEL ENHANCEMENT COMPLETE")
            print("=" * 80)
            print()

            for wave_key, stats in all_stats.items():
                wave_total = sum(s['enhanced'] for s in stats.values())
                print(f"{wave_key.upper()}: {wave_total:,} nodes enhanced")

            total_enhanced = sum(
                sum(s['enhanced'] for s in wave_stats.values())
                for wave_stats in all_stats.values()
            )
            print()
            print(f"TOTAL: {total_enhanced:,} nodes enhanced across 5 waves")
            print(f"CVE preservation: ✅ INTACT")
            print()

            return True

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
    enhancer = Waves48LabelEnhancer()
    success = enhancer.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
