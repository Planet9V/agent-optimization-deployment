# Neo4j Pipeline Integration Guide

## Overview
This guide explains how to integrate the NER11 Gold Standard API with a Neo4j database to build a Knowledge Graph.

## Prerequisites
- Running NER11 Gold API container (`http://localhost:8000`)
- Running Neo4j Database (`bolt://localhost:7687`)
- Python 3.8+
- `neo4j` and `requests` python packages

## Integration Script

Create a script `ingest_to_neo4j.py`:

```python
import requests
from neo4j import GraphDatabase

# Configuration
API_URL = "http://localhost:8000/ner"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

class KnowledgeGraphBuilder:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def process_document(self, doc_id, text):
        # 1. Extract Entities via API
        response = requests.post(API_URL, json={"text": text})
        if response.status_code != 200:
            print(f"Error extracting entities: {response.text}")
            return

        data = response.json()
        entities = data['entities']

        # 2. Ingest into Neo4j
        with self.driver.session() as session:
            session.write_transaction(self._create_graph, doc_id, text, entities)

    @staticmethod
    def _create_graph(tx, doc_id, text, entities):
        # Create Document Node
        tx.run("MERGE (d:Document {id: $doc_id}) SET d.text = $text", 
               doc_id=doc_id, text=text)
        
        for ent in entities:
            # Create Entity Node & Relationship
            tx.run("""
                MERGE (e:Entity {name: $name, type: $label})
                MERGE (d:Document {id: $doc_id})
                MERGE (d)-[:MENTIONS {score: $score}]->(e)
            """, name=ent['text'], label=ent['label'], 
                 doc_id=doc_id, score=ent['score'])
            print(f"Linked '{ent['text']}' ({ent['label']}) to Document {doc_id}")

if __name__ == "__main__":
    kg = KnowledgeGraphBuilder()
    
    sample_text = "The Lazarus Group targeted the SWIFT network using custom malware."
    kg.process_document("doc_001", sample_text)
    
    kg.close()
```

## Pipeline Architecture

1.  **Ingestion**: Documents are fed into the script.
2.  **Extraction**: Text is sent to the NER11 API container.
3.  **Graph Construction**: Extracted entities are written to Neo4j as nodes, linked to the source document.

## Schema
- **Nodes**: `Document`, `Entity`
- **Relationships**: `(:Document)-[:MENTIONS]->(:Entity)`
- **Properties**: `Entity.type` (e.g., THREAT_ACTOR, MALWARE) matches NER11 labels.
