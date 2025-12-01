#!/usr/bin/env python3
"""
Phase 4: Index Creation - Create 38 optimized indexes for enhanced graph

Index Categories:
- Domain Level: 12 indexes (one per domain)
- Subdomain Level: 15 indexes (key subdomains)
- Functional Role: 8 indexes (cross-domain roles)
- Composite: 3 indexes (common query patterns)

Total: 38 indexes

Pattern: Create indexes sequentially, validate existence
Performance: Measure creation time and index statistics

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


class IndexCreator:
    """Create optimized indexes for enhanced graph database"""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        project_root: Path = None
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.log_file = self.project_root / "logs" / "index_creation.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Load master taxonomy
        taxonomy_path = self.project_root / "master_taxonomy.yaml"
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = yaml.safe_load(f)

        self.index_strategy = self.taxonomy['index_strategy']
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

    def get_existing_indexes(self) -> List[str]:
        """Get list of existing indexes"""
        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")
            existing = []
            for record in result:
                index_name = record.get("name")
                if index_name:
                    existing.append(index_name)
            return existing

    def create_single_label_index(self, name: str, label: str, property: str) -> Dict[str, Any]:
        """Create index on single label and property"""
        start_time = datetime.now()

        with self.driver.session() as session:
            try:
                # Create index
                session.run(f"""
                    CREATE INDEX {name} IF NOT EXISTS
                    FOR (n:{label})
                    ON (n.{property})
                """)

                duration = (datetime.now() - start_time).total_seconds()

                self._log(
                    "create_index",
                    "SUCCESS",
                    {
                        "name": name,
                        "label": label,
                        "property": property,
                        "duration_sec": duration
                    }
                )

                return {
                    "name": name,
                    "label": label,
                    "property": property,
                    "status": "created",
                    "duration": duration
                }

            except Exception as e:
                self._log(
                    "create_index",
                    "FAILED",
                    {
                        "name": name,
                        "label": label,
                        "property": property,
                        "error": str(e)
                    }
                )
                return {
                    "name": name,
                    "label": label,
                    "property": property,
                    "status": "failed",
                    "error": str(e)
                }

    def create_composite_index(self, name: str, labels: List[str], property: str) -> Dict[str, Any]:
        """Create composite index on multiple labels"""
        start_time = datetime.now()

        with self.driver.session() as session:
            try:
                # Create composite index (Neo4j 5.x syntax)
                label_pattern = ':'.join(labels)
                session.run(f"""
                    CREATE INDEX {name} IF NOT EXISTS
                    FOR (n:{label_pattern})
                    ON (n.{property})
                """)

                duration = (datetime.now() - start_time).total_seconds()

                self._log(
                    "create_composite_index",
                    "SUCCESS",
                    {
                        "name": name,
                        "labels": labels,
                        "property": property,
                        "duration_sec": duration
                    }
                )

                return {
                    "name": name,
                    "labels": labels,
                    "property": property,
                    "status": "created",
                    "duration": duration
                }

            except Exception as e:
                self._log(
                    "create_composite_index",
                    "FAILED",
                    {
                        "name": name,
                        "labels": labels,
                        "property": property,
                        "error": str(e)
                    }
                )
                return {
                    "name": name,
                    "labels": labels,
                    "property": property,
                    "status": "failed",
                    "error": str(e)
                }

    def create_all_indexes(self) -> Dict[str, List[Dict]]:
        """Create all indexes from taxonomy configuration"""
        results = {
            "domain": [],
            "subdomain": [],
            "functional_role": [],
            "composite": []
        }

        print("Creating Domain Indexes (12)...")
        print("-" * 80)
        for idx_config in self.index_strategy['domain_indexes']:
            result = self.create_single_label_index(
                idx_config['name'],
                idx_config['label'],
                idx_config['property']
            )
            results['domain'].append(result)
            status = "✅" if result['status'] == "created" else "❌"
            print(f"  {status} {result['name']}: {result['label']}")

        print()
        print("Creating Subdomain Indexes (15)...")
        print("-" * 80)
        for idx_config in self.index_strategy['subdomain_indexes']:
            result = self.create_single_label_index(
                idx_config['name'],
                idx_config['label'],
                idx_config['property']
            )
            results['subdomain'].append(result)
            status = "✅" if result['status'] == "created" else "❌"
            print(f"  {status} {result['name']}: {result['label']}")

        print()
        print("Creating Functional Role Indexes (8)...")
        print("-" * 80)
        for idx_config in self.index_strategy['functional_role_indexes']:
            result = self.create_single_label_index(
                idx_config['name'],
                idx_config['label'],
                idx_config['property']
            )
            results['functional_role'].append(result)
            status = "✅" if result['status'] == "created" else "❌"
            print(f"  {status} {result['name']}: {result['label']}")

        print()
        print("Creating Composite Indexes (3)...")
        print("-" * 80)
        for idx_config in self.index_strategy['composite_indexes']:
            result = self.create_composite_index(
                idx_config['name'],
                idx_config['labels'],
                idx_config['property']
            )
            results['composite'].append(result)
            status = "✅" if result['status'] == "created" else "❌"
            labels_str = ' + '.join(idx_config['labels'])
            print(f"  {status} {result['name']}: {labels_str}")

        return results

    def validate_indexes(self) -> Dict[str, Any]:
        """Validate index creation"""
        existing_indexes = self.get_existing_indexes()

        # Check for expected indexes
        expected_count = 38
        created_count = len(existing_indexes)

        # Count by category
        domain_count = sum(1 for idx in existing_indexes if 'domain' in idx.lower())
        subdomain_count = sum(1 for idx in existing_indexes if any(
            label.lower().replace('_', '') in idx.lower()
            for label in ['water', 'energy', 'adversary', 'malware', 'technique',
                          'software', 'cloud', 'virtualization', 'component',
                          'dependency', 'license', 'surveillance', 'access']
        ))
        role_count = sum(1 for idx in existing_indexes if any(
            role in idx.lower()
            for role in ['asset', 'monitoring', 'control', 'threat', 'detection',
                        'compliance', 'investigation', 'human']
        ))
        composite_count = sum(1 for idx in existing_indexes if any(
            pattern in idx.lower()
            for pattern in ['energy_asset', 'threat_detection', 'sbom_compliance']
        ))

        return {
            "total_indexes": created_count,
            "expected_indexes": expected_count,
            "domain_indexes": domain_count,
            "subdomain_indexes": subdomain_count,
            "role_indexes": role_count,
            "composite_indexes": composite_count,
            "all_created": created_count >= expected_count
        }

    def execute(self) -> bool:
        """Execute index creation workflow"""
        try:
            print("=" * 80)
            print("PHASE 4: INDEX CREATION")
            print("=" * 80)
            print()
            print(f"Total indexes to create: {self.index_strategy['total_indexes']}")
            print(f"  - Domain indexes: {self.index_strategy['categories']['domain_level']}")
            print(f"  - Subdomain indexes: {self.index_strategy['categories']['subdomain_level']}")
            print(f"  - Functional role indexes: {self.index_strategy['categories']['functional_role']}")
            print(f"  - Composite indexes: {self.index_strategy['categories']['composite']}")
            print()

            print("[1/4] Creating pre-index checkpoint...")
            checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Index Creation - Start",
                phase="PHASE_4",
                wave="INDEXES"
            )
            print(f"✅ Checkpoint: {checkpoint_id}")
            print()

            print("[2/4] Creating all indexes...")
            print()
            start_time = datetime.now()
            results = self.create_all_indexes()
            total_duration = (datetime.now() - start_time).total_seconds()

            # Count successes and failures
            total_created = sum(
                sum(1 for r in category_results if r['status'] == 'created')
                for category_results in results.values()
            )
            total_failed = sum(
                sum(1 for r in category_results if r['status'] == 'failed')
                for category_results in results.values()
            )

            print()
            print(f"✅ Index creation complete in {total_duration:.1f} seconds")
            print(f"   Created: {total_created}")
            print(f"   Failed: {total_failed}")
            print()

            print("[3/4] Validating indexes...")
            validation = self.validate_indexes()
            print(f"Total indexes: {validation['total_indexes']}")
            print(f"  Domain: {validation['domain_indexes']}")
            print(f"  Subdomain: {validation['subdomain_indexes']}")
            print(f"  Functional role: {validation['role_indexes']}")
            print(f"  Composite: {validation['composite_indexes']}")
            print()

            print("[4/4] Creating post-index checkpoint...")
            final_checkpoint_id = self.checkpoint_mgr.create_checkpoint(
                operation_name="Index Creation - Complete",
                phase="PHASE_4",
                wave="INDEXES",
                metadata={
                    "validation": validation,
                    "results": {
                        "created": total_created,
                        "failed": total_failed,
                        "duration": total_duration
                    }
                }
            )
            print(f"✅ Final checkpoint: {final_checkpoint_id}")
            print()

            print("=" * 80)
            print("✅ PHASE 4: INDEX CREATION COMPLETE")
            print("=" * 80)
            print()
            print(f"Total indexes: {validation['total_indexes']}")
            print(f"Expected: {validation['expected_indexes']}")
            print(f"Status: {'✅ ALL INDEXES CREATED' if validation['all_created'] else '⚠️  PARTIAL COMPLETION'}")
            print()

            return validation['all_created']

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
    creator = IndexCreator()
    success = creator.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
