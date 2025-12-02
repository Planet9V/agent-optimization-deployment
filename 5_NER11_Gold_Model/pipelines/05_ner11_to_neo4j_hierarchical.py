"""
NER11 to Neo4j Hierarchical Pipeline: Complete Entity Ingestion System

Processes documents through NER11 API, enriches with hierarchical taxonomy,
and ingests into Neo4j v3.1 knowledge graph with relationship extraction.

File: 05_ner11_to_neo4j_hierarchical.py
Created: 2025-12-01
Version: 1.0.0
Status: PRODUCTION-READY
Author: J. McKenney (via AEON Implementation)

TASK: TASKMASTER Task 2.3 - Neo4j Hierarchical Pipeline

Requirements:
1. Import HierarchicalEntityProcessor (Task 1.1)
2. Import NER11ToNeo4jMapper (Task 2.2)
3. Connect to Neo4j (bolt://localhost:7687)
4. Process documents via NER11 API
5. Enrich entities with hierarchical properties
6. Create nodes with MERGE (preserve 1.1M existing)
7. Extract and create relationships
8. Validation: tier2 > tier1, node count preserved

Integration:
- HierarchicalEntityProcessor: 566-type taxonomy enrichment
- NER11ToNeo4jMapper: 60 NER → 16 Neo4j label mapping
- Neo4j v3.1 schema: Hierarchical properties + relationships
- NER11 API: Entity extraction from documents
"""

import os
import sys
import json
import logging
import requests
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

# Import hierarchical processor and mapper
# Import from same directory (pipelines/)
import sys
from pathlib import Path
pipeline_dir = Path(__file__).parent
sys.path.insert(0, str(pipeline_dir))

# Import processor from 00_hierarchical_entity_processor.py
import importlib.util
spec_processor = importlib.util.spec_from_file_location(
    "hierarchical_entity_processor",
    pipeline_dir / "00_hierarchical_entity_processor.py"
)
processor_module = importlib.util.module_from_spec(spec_processor)
spec_processor.loader.exec_module(processor_module)
HierarchicalEntityProcessor = processor_module.HierarchicalEntityProcessor

# Import mapper from 04_ner11_to_neo4j_mapper.py
spec_mapper = importlib.util.spec_from_file_location(
    "ner11_to_neo4j_mapper",
    pipeline_dir / "04_ner11_to_neo4j_mapper.py"
)
mapper_module = importlib.util.module_from_spec(spec_mapper)
spec_mapper.loader.exec_module(mapper_module)
NER11ToNeo4jMapper = mapper_module.NER11ToNeo4jMapper
Neo4jSuperLabel = mapper_module.Neo4jSuperLabel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NER11ToNeo4jPipeline:
    """
    Complete pipeline for NER11 entity extraction and Neo4j ingestion.

    Features:
    - Document processing via NER11 API
    - Hierarchical entity enrichment (566 types)
    - Neo4j node creation with MERGE (preserves existing)
    - Relationship extraction and creation
    - Comprehensive validation
    - Batch processing support
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "neo4j@openspg",
        ner11_api_url: str = "http://localhost:8000"
    ):
        """
        Initialize pipeline with Neo4j connection and processors.

        Args:
            neo4j_uri: Neo4j bolt connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            ner11_api_url: NER11 API endpoint URL
        """
        # Initialize processors
        self.hierarchical_processor = HierarchicalEntityProcessor()
        self.mapper = NER11ToNeo4jMapper()

        # Neo4j connection
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

        # NER11 API
        self.ner11_api_url = ner11_api_url

        # Processing statistics
        self.stats = {
            "documents_processed": 0,
            "entities_extracted": 0,
            "entities_enriched": 0,
            "nodes_created": 0,
            "nodes_merged": 0,
            "relationships_created": 0,
            "errors": 0,
            "tier1_entities": 0,
            "tier2_entities": 0
        }

        logger.info(f"Pipeline initialized with Neo4j at {neo4j_uri}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close Neo4j connection"""
        self.close()

    def close(self):
        """Close Neo4j driver connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")

    def extract_entities_from_text(self, text: str) -> List[Dict]:
        """
        Extract entities from text using NER11 API.

        Args:
            text: Input document text

        Returns:
            List of entity dictionaries with {text, label, start, end}
        """
        try:
            response = requests.post(
                f"{self.ner11_api_url}/extract",
                json={"text": text},
                timeout=30
            )
            response.raise_for_status()

            entities = response.json().get("entities", [])
            self.stats["entities_extracted"] += len(entities)

            logger.info(f"Extracted {len(entities)} entities from text")
            return entities

        except requests.exceptions.RequestException as e:
            logger.error(f"NER11 API error: {e}")
            self.stats["errors"] += 1
            return []

    def enrich_entity(self, entity: Dict) -> Dict:
        """
        Enrich entity with hierarchical taxonomy properties.

        Args:
            entity: Entity dict with {text, label, start, end}

        Returns:
            Enriched entity with super_label, tier, hierarchy properties
        """
        ner_label = entity.get("label", "")
        entity_text = entity.get("text", "")

        # Get hierarchical mapping
        taxonomy = self.hierarchical_processor.taxonomy.get(ner_label)

        if not taxonomy:
            # Fallback: try keyword-based classification
            classified = self.hierarchical_processor.classify_entity(
                entity_text,
                ner_label
            )
            taxonomy = classified

        # Get Neo4j mapping
        mapping = self.mapper.get_mapping(ner_label)

        # Build enriched entity
        enriched = {
            **entity,
            "ner_label": ner_label,
            "super_label": taxonomy.get("super_label").value if taxonomy.get("super_label") else None,
            "tier": taxonomy.get("tier", 1),
            "fine_grained_type": taxonomy.get("subtype", ner_label.lower()),
            "specific_instance": entity_text,
            "hierarchy_path": f"{taxonomy.get('super_label').value if taxonomy.get('super_label') else 'Unknown'}/{ner_label}/{entity_text}",
            "discriminator_property": mapping.discriminator_property if mapping else None,
            "discriminator_value": mapping.discriminator_value if mapping else None
        }

        # Add tier-specific properties
        if taxonomy:
            for key, value in taxonomy.items():
                if key not in ["super_label", "tier"]:
                    enriched[key] = value

        # Update stats
        self.stats["entities_enriched"] += 1
        tier = enriched.get("tier", 1)
        if tier == 1:
            self.stats["tier1_entities"] += 1
        elif tier == 2:
            self.stats["tier2_entities"] += 1

        return enriched

    def create_node_in_neo4j(self, entity: Dict) -> bool:
        """
        Create or merge entity node in Neo4j with all hierarchy properties.

        Uses MERGE to preserve existing nodes (critical for 1.1M node preservation).

        Args:
            entity: Enriched entity dictionary

        Returns:
            True if successful, False otherwise
        """
        super_label = entity.get("super_label")
        if not super_label:
            logger.warning(f"No super label for entity: {entity.get('text')}")
            return False

        try:
            with self.driver.session() as session:
                # Build properties for node
                properties = {
                    "name": entity.get("specific_instance", entity.get("text")),
                    "ner_label": entity.get("ner_label"),
                    "fine_grained_type": entity.get("fine_grained_type"),
                    "specific_instance": entity.get("specific_instance"),
                    "hierarchy_path": entity.get("hierarchy_path"),
                    "tier": entity.get("tier", 1)
                }

                # Add discriminator properties
                if entity.get("discriminator_property") and entity.get("discriminator_value"):
                    properties[entity["discriminator_property"]] = entity["discriminator_value"]

                # Add additional enrichment properties
                for key in ["actorType", "malwareFamily", "patternType", "vulnType",
                           "indicatorType", "campaignType", "assetClass", "deviceType",
                           "traitType", "subtype", "metricType", "protocolType",
                           "roleType", "softwareType", "controlType", "eventType"]:
                    if key in entity:
                        properties[key] = entity[key]

                # CRITICAL: Use MERGE to preserve existing nodes
                query = f"""
                MERGE (n:{super_label} {{name: $name}})
                ON CREATE SET
                    n.ner_label = $ner_label,
                    n.fine_grained_type = $fine_grained_type,
                    n.specific_instance = $specific_instance,
                    n.hierarchy_path = $hierarchy_path,
                    n.tier = $tier,
                    n.created_at = datetime()
                ON MATCH SET
                    n.updated_at = datetime()
                """

                # Add dynamic property setting
                for key in properties.keys():
                    if key not in ["name", "ner_label", "fine_grained_type",
                                  "specific_instance", "hierarchy_path", "tier"]:
                        query += f"\nSET n.{key} = ${key}"

                query += "\nRETURN n"

                result = session.run(query, **properties)
                record = result.single()

                if record:
                    self.stats["nodes_merged"] += 1
                    logger.debug(f"Merged node: {super_label}/{entity.get('text')}")
                    return True
                else:
                    logger.warning(f"Node merge returned no record: {entity.get('text')}")
                    return False

        except Neo4jError as e:
            logger.error(f"Neo4j error creating node: {e}")
            self.stats["errors"] += 1
            return False

    def extract_relationships(self, entities: List[Dict], text: str) -> List[Tuple[Dict, str, Dict]]:
        """
        Extract relationships between entities based on patterns and context.

        Args:
            entities: List of enriched entity dictionaries
            text: Original document text for context

        Returns:
            List of (source_entity, relationship_type, target_entity) tuples
        """
        relationships = []

        # Common relationship patterns
        patterns = {
            "EXPLOITS": [
                ("ThreatActor", "Vulnerability"),
                ("Malware", "Vulnerability"),
                ("AttackPattern", "Vulnerability")
            ],
            "USES": [
                ("ThreatActor", "Malware"),
                ("ThreatActor", "AttackPattern"),
                ("Campaign", "Malware"),
                ("Campaign", "AttackPattern")
            ],
            "TARGETS": [
                ("ThreatActor", "Asset"),
                ("ThreatActor", "Organization"),
                ("Malware", "Asset"),
                ("Campaign", "Organization")
            ],
            "AFFECTS": [
                ("Vulnerability", "Software"),
                ("Vulnerability", "Asset"),
                ("Malware", "Software")
            ],
            "ATTRIBUTED_TO": [
                ("Campaign", "ThreatActor"),
                ("Malware", "ThreatActor"),
                ("AttackPattern", "ThreatActor")
            ],
            "MITIGATES": [
                ("Control", "Vulnerability"),
                ("Control", "AttackPattern")
            ],
            "INDICATES": [
                ("Indicator", "Malware"),
                ("Indicator", "ThreatActor"),
                ("Indicator", "AttackPattern")
            ]
        }

        # Extract relationships based on patterns
        for i, source in enumerate(entities):
            source_label = source.get("super_label")
            if not source_label:
                continue

            for j, target in enumerate(entities):
                if i == j:
                    continue

                target_label = target.get("super_label")
                if not target_label:
                    continue

                # Check if this label pair has a known relationship
                for rel_type, label_pairs in patterns.items():
                    if (source_label, target_label) in label_pairs:
                        # Validate proximity in text (entities should be nearby)
                        source_start = source.get("start", 0)
                        target_start = target.get("start", 0)
                        distance = abs(source_start - target_start)

                        # Only create relationship if entities are within 500 characters
                        if distance < 500:
                            relationships.append((source, rel_type, target))

        logger.info(f"Extracted {len(relationships)} relationships from {len(entities)} entities")
        return relationships

    def create_relationship_in_neo4j(
        self,
        source: Dict,
        rel_type: str,
        target: Dict
    ) -> bool:
        """
        Create relationship between two nodes in Neo4j.

        Args:
            source: Source entity dictionary
            rel_type: Relationship type (e.g., "EXPLOITS", "USES")
            target: Target entity dictionary

        Returns:
            True if successful, False otherwise
        """
        source_label = source.get("super_label")
        target_label = target.get("super_label")
        source_name = source.get("specific_instance", source.get("text"))
        target_name = target.get("specific_instance", target.get("text"))

        if not all([source_label, target_label, source_name, target_name]):
            return False

        try:
            with self.driver.session() as session:
                query = f"""
                MATCH (source:{source_label} {{name: $source_name}})
                MATCH (target:{target_label} {{name: $target_name}})
                MERGE (source)-[r:{rel_type}]->(target)
                ON CREATE SET
                    r.created_at = datetime(),
                    r.confidence = 0.8
                ON MATCH SET
                    r.updated_at = datetime()
                RETURN r
                """

                result = session.run(
                    query,
                    source_name=source_name,
                    target_name=target_name
                )

                record = result.single()
                if record:
                    self.stats["relationships_created"] += 1
                    logger.debug(f"Created relationship: {source_name} -{rel_type}-> {target_name}")
                    return True

        except Neo4jError as e:
            logger.error(f"Neo4j error creating relationship: {e}")
            self.stats["errors"] += 1
            return False

        return False

    def process_document(self, text: str, document_id: Optional[str] = None) -> Dict:
        """
        Process complete document: extract entities, enrich, and ingest into Neo4j.

        Args:
            text: Document text to process
            document_id: Optional document identifier

        Returns:
            Processing statistics for this document
        """
        doc_id = document_id or f"doc_{datetime.now().timestamp()}"
        logger.info(f"Processing document: {doc_id}")

        doc_stats = {
            "document_id": doc_id,
            "entities_extracted": 0,
            "nodes_created": 0,
            "relationships_created": 0,
            "errors": 0
        }

        try:
            # Step 1: Extract entities via NER11 API
            entities = self.extract_entities_from_text(text)
            doc_stats["entities_extracted"] = len(entities)

            if not entities:
                logger.warning(f"No entities extracted from document {doc_id}")
                return doc_stats

            # Step 2: Enrich entities with hierarchical taxonomy
            enriched_entities = []
            for entity in entities:
                enriched = self.enrich_entity(entity)
                enriched_entities.append(enriched)

            # Step 3: Create nodes in Neo4j (with MERGE)
            for entity in enriched_entities:
                if self.create_node_in_neo4j(entity):
                    doc_stats["nodes_created"] += 1
                else:
                    doc_stats["errors"] += 1

            # Step 4: Extract and create relationships
            relationships = self.extract_relationships(enriched_entities, text)
            for source, rel_type, target in relationships:
                if self.create_relationship_in_neo4j(source, rel_type, target):
                    doc_stats["relationships_created"] += 1
                else:
                    doc_stats["errors"] += 1

            # Update global stats
            self.stats["documents_processed"] += 1

            logger.info(
                f"Document {doc_id} processed: "
                f"{doc_stats['entities_extracted']} entities, "
                f"{doc_stats['nodes_created']} nodes, "
                f"{doc_stats['relationships_created']} relationships"
            )

        except Exception as e:
            logger.error(f"Error processing document {doc_id}: {e}")
            doc_stats["errors"] += 1
            self.stats["errors"] += 1

        return doc_stats

    def validate_ingestion(self) -> Dict:
        """
        Validate Neo4j ingestion: check node count preservation and tier distribution.

        Critical validations:
        1. Total node count should not decrease (preserve 1,104,066 existing)
        2. Tier 2 entities > Tier 1 entities (hierarchy depth validation)

        Returns:
            Validation report dictionary
        """
        report = {
            "validation_passed": False,
            "total_nodes": 0,
            "baseline_nodes": 1104066,
            "node_count_preserved": False,
            "tier1_count": 0,
            "tier2_count": 0,
            "tier2_greater_than_tier1": False,
            "super_label_distribution": {},
            "errors": []
        }

        try:
            with self.driver.session() as session:
                # Check total node count
                result = session.run("MATCH (n) RETURN count(n) as total")
                record = result.single()
                if record:
                    report["total_nodes"] = record["total"]
                    report["node_count_preserved"] = (
                        report["total_nodes"] >= report["baseline_nodes"]
                    )

                # Check tier distribution
                result = session.run("""
                    MATCH (n)
                    WHERE n.tier IS NOT NULL
                    RETURN n.tier as tier, count(n) as count
                """)
                for record in result:
                    tier = record["tier"]
                    count = record["count"]
                    if tier == 1:
                        report["tier1_count"] = count
                    elif tier == 2:
                        report["tier2_count"] = count

                report["tier2_greater_than_tier1"] = (
                    report["tier2_count"] > report["tier1_count"]
                )

                # Check super label distribution
                result = session.run("""
                    CALL db.labels() YIELD label
                    CALL apoc.cypher.run(
                        'MATCH (n:' + label + ') RETURN count(n) as count',
                        {}
                    ) YIELD value
                    RETURN label, value.count as count
                    ORDER BY count DESC
                """)
                for record in result:
                    label = record["label"]
                    count = record["count"]
                    report["super_label_distribution"][label] = count

                # Overall validation
                report["validation_passed"] = (
                    report["node_count_preserved"] and
                    report["tier2_greater_than_tier1"]
                )

        except Neo4jError as e:
            logger.error(f"Validation error: {e}")
            report["errors"].append(str(e))

        return report

    def get_statistics(self) -> Dict:
        """
        Get current pipeline processing statistics.

        Returns:
            Statistics dictionary
        """
        return {
            **self.stats,
            "validation": self.validate_ingestion()
        }


# ============================================================================
# TESTING AND DEMONSTRATION
# ============================================================================

def test_sample_document():
    """
    Test pipeline with sample cybersecurity document.

    Demonstrates:
    - Entity extraction
    - Hierarchical enrichment
    - Node creation with MERGE
    - Relationship extraction
    - Validation
    """
    print("="*80)
    print("NER11 TO NEO4J HIERARCHICAL PIPELINE - SAMPLE DOCUMENT TEST")
    print("="*80)

    # Sample cybersecurity document
    sample_text = """
    APT29, also known as Cozy Bear, is a Russian advanced persistent threat
    group that has been active since at least 2008. The group is attributed
    to Russia's Foreign Intelligence Service (SVR) and has conducted numerous
    cyber espionage campaigns against government organizations.

    In 2020, APT29 exploited CVE-2020-0688, a remote code execution vulnerability
    in Microsoft Exchange Server. The group used their custom malware, WellMess
    and WellMail, to compromise email servers and exfiltrate sensitive data.

    The campaign targeted organizations in the United States, United Kingdom,
    and Canada. Security analysts recommend implementing multi-factor authentication
    and network segmentation to mitigate these attacks.

    The CISO should review the organization's incident response plan and ensure
    the security team has visibility into all network traffic. Financial impact
    of such breaches can exceed $4.2 million per incident.
    """

    try:
        # Initialize pipeline
        with NER11ToNeo4jPipeline() as pipeline:
            print("\n[STEP 1] Pipeline Initialized")
            print(f"Hierarchical Processor: {len(pipeline.hierarchical_processor.taxonomy)} types")
            print(f"Mapper: {len(pipeline.mapper.mapping_table)} NER labels")

            # Process document
            print("\n[STEP 2] Processing Sample Document")
            doc_stats = pipeline.process_document(sample_text, "sample_apt29_doc")

            print(f"\nDocument Statistics:")
            print(f"  Entities extracted: {doc_stats['entities_extracted']}")
            print(f"  Nodes created/merged: {doc_stats['nodes_created']}")
            print(f"  Relationships created: {doc_stats['relationships_created']}")
            print(f"  Errors: {doc_stats['errors']}")

            # Get pipeline statistics
            print("\n[STEP 3] Pipeline Statistics")
            stats = pipeline.get_statistics()
            print(f"  Documents processed: {stats['documents_processed']}")
            print(f"  Total entities: {stats['entities_extracted']}")
            print(f"  Tier 1 entities: {stats['tier1_entities']}")
            print(f"  Tier 2 entities: {stats['tier2_entities']}")
            print(f"  Nodes merged: {stats['nodes_merged']}")
            print(f"  Relationships: {stats['relationships_created']}")

            # Validation
            print("\n[STEP 4] Validation Results")
            validation = stats['validation']
            print(f"  Total nodes in database: {validation['total_nodes']:,}")
            print(f"  Baseline nodes: {validation['baseline_nodes']:,}")
            print(f"  Node count preserved: {'✅ PASS' if validation['node_count_preserved'] else '❌ FAIL'}")
            print(f"  Tier 2 > Tier 1: {'✅ PASS' if validation['tier2_greater_than_tier1'] else '❌ FAIL'}")
            print(f"  Overall validation: {'✅ PASS' if validation['validation_passed'] else '❌ FAIL'}")

            print("\n" + "="*80)
            if validation['validation_passed']:
                print("✅ PIPELINE TEST SUCCESSFUL")
            else:
                print("⚠️ PIPELINE TEST COMPLETED WITH WARNINGS")
            print("="*80)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run sample document test
    test_sample_document()
