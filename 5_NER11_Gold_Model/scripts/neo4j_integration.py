#!/usr/bin/env python3
"""
NER11 Gold Standard - Neo4j Integration Module

This module provides seamless integration between the NER11 model
and Neo4j for knowledge graph construction.
"""

import spacy
from neo4j import GraphDatabase
from typing import List, Dict, Tuple, Optional
import logging
from pathlib import Path
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NER11Neo4jIntegrator:
    """
    Integrates NER11 Gold Standard model with Neo4j.
    
    Features:
    - Entity extraction and ingestion
    - Batch processing
    - Relationship inference
    - Metrics tracking
    """
    
    # Entity type to Neo4j label mapping
    LABEL_MAP = {
        "THREAT_ACTOR": "ThreatActor",
        "VULNERABILITY": "Vulnerability",
        "MALWARE": "Malware",
        "OT_DEVICE": "OTDevice",
        "SCADA_SYSTEM": "SCADASystem",
        "ATTACK_VECTOR": "AttackVector",
        "PERSONALITY_TRAIT": "PersonalityTrait",
        "COGNITIVE_BIAS": "CognitiveBias",
        "EMOTIONAL_STATE": "EmotionalState",
        # Add more mappings as needed
    }
    
    def __init__(
        self,
        model_path: str = "./models/model-best",
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password"
    ):
        """
        Initialize the integrator.
        
        Args:
            model_path: Path to NER11 model
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        logger.info(f"Loading NER11 model from {model_path}")
        self.nlp = spacy.load(model_path)
        
        logger.info(f"Connecting to Neo4j at {neo4j_uri}")
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        
        # Metrics
        self.entities_processed = 0
        self.nodes_created = 0
        self.relationships_created = 0
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create Neo4j indexes for performance."""
        with self.driver.session() as session:
            session.run(
                "CREATE INDEX entity_text IF NOT EXISTS FOR (e:Entity) ON (e.text)"
            )
            session.run(
                "CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)"
            )
            logger.info("✓ Neo4j indexes created")
    
    def get_node_label(self, entity_type: str) -> str:
        """Map entity type to Neo4j label."""
        return self.LABEL_MAP.get(entity_type, "Entity")
    
    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract entities from text.
        
        Args:
            text: Input text
            
        Returns:
            List of (entity_text, entity_type) tuples
        """
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        self.entities_processed += len(entities)
        return entities
    
    def ingest_entities(
        self,
        entities: List[Tuple[str, str]],
        source_doc: Optional[str] = None
    ):
        """
        Ingest entities into Neo4j.
        
        Args:
            entities: List of (text, type) tuples
            source_doc: Optional source document ID
        """
        with self.driver.session() as session:
            for text, entity_type in entities:
                label = self.get_node_label(entity_type)
                
                result = session.run("""
                    MERGE (e:%s {text: $text})
                    ON CREATE SET 
                        e.type = $type,
                        e.first_seen = timestamp(),
                        e.count = 1,
                        e.source_doc = $source_doc
                    ON MATCH SET 
                        e.last_seen = timestamp(),
                        e.count = coalesce(e.count, 0) + 1
                    RETURN e
                """ % label, text=text, type=entity_type, source_doc=source_doc)
                
                if result.single():
                    self.nodes_created += 1
    
    def process_and_ingest(
        self,
        text: str,
        source_doc: Optional[str] = None,
        create_relationships: bool = False
    ) -> Dict:
        """
        Extract entities and ingest into Neo4j.
        
        Args:
            text: Input text
            source_doc: Optional source document ID
            create_relationships: Whether to infer relationships
            
        Returns:
            Dictionary with extraction results
        """
        # Extract entities
        entities = self.extract_entities(text)
        
        # Ingest into Neo4j
        self.ingest_entities(entities, source_doc)
        
        # Optionally create relationships
        if create_relationships:
            self._create_cooccurrence_relationships(entities)
        
        return {
            "entity_count": len(entities),
            "entities": entities,
            "nodes_created": self.nodes_created,
            "relationships_created": self.relationships_created
        }
    
    def _create_cooccurrence_relationships(
        self,
        entities: List[Tuple[str, str]]
    ):
        """Create CO_OCCURS relationships between entities."""
        with self.driver.session() as session:
            for i, (text1, type1) in enumerate(entities):
                for text2, type2 in entities[i+1:]:
                    label1 = self.get_node_label(type1)
                    label2 = self.get_node_label(type2)
                    
                    session.run(f"""
                        MATCH (e1:{label1} {{text: $text1}})
                        MATCH (e2:{label2} {{text: $text2}})
                        MERGE (e1)-[r:CO_OCCURS]->(e2)
                        ON CREATE SET r.count = 1
                        ON MATCH SET r.count = coalesce(r.count, 0) + 1
                    """, text1=text1, text2=text2)
                    
                    self.relationships_created += 1
    
    def batch_process_directory(
        self,
        input_dir: str,
        batch_size: int = 100,
        create_relationships: bool = False
    ):
        """
        Process all text files in a directory.
        
        Args:
            input_dir: Directory containing text files
            batch_size: Number of files to process per batch
            create_relationships: Whether to infer relationships
        """
        input_path = Path(input_dir)
        text_files = list(input_path.glob("*.txt"))
        
        logger.info(f"Found {len(text_files)} text files")
        
        for filepath in tqdm(text_files, desc="Processing files"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                self.process_and_ingest(
                    text,
                    source_doc=filepath.name,
                    create_relationships=create_relationships
                )
            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")
        
        self.log_stats()
    
    def log_stats(self):
        """Log processing statistics."""
        logger.info("=" * 50)
        logger.info("Processing Statistics")
        logger.info("=" * 50)
        logger.info(f"Entities Processed: {self.entities_processed}")
        logger.info(f"Nodes Created: {self.nodes_created}")
        logger.info(f"Relationships Created: {self.relationships_created}")
        logger.info("=" * 50)
    
    def close(self):
        """Close Neo4j connection."""
        self.driver.close()
        logger.info("✓ Neo4j connection closed")


def main():
    """CLI interface for Neo4j integration."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="NER11 Gold Standard - Neo4j Integration"
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing text files"
    )
    parser.add_argument(
        "--model-path",
        default="./models/model-best",
        help="Path to NER11 model"
    )
    parser.add_argument(
        "--neo4j-uri",
        default="bolt://localhost:7687",
        help="Neo4j connection URI"
    )
    parser.add_argument(
        "--neo4j-user",
        default="neo4j",
        help="Neo4j username"
    )
    parser.add_argument(
        "--neo4j-password",
        default="password",
        help="Neo4j password"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for processing"
    )
    parser.add_argument(
        "--create-relationships",
        action="store_true",
        help="Create co-occurrence relationships"
    )
    
    args = parser.parse_args()
    
    # Initialize integrator
    integrator = NER11Neo4jIntegrator(
        model_path=args.model_path,
        neo4j_uri=args.neo4j_uri,
        neo4j_user=args.neo4j_user,
        neo4j_password=args.neo4j_password
    )
    
    # Process directory
    integrator.batch_process_directory(
        input_dir=args.input_dir,
        batch_size=args.batch_size,
        create_relationships=args.create_relationships
    )
    
    # Close connection
    integrator.close()


if __name__ == "__main__":
    main()
