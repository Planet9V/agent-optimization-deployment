#!/usr/bin/env python3
"""
Enhanced Entity & Relationship Extraction for Neo4j
Processes documents to extract cybersecurity entities and their relationships
"""

import spacy
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from document_processor import DocumentProcessor
import re

class EntityRelationshipExtractor:
    """Extract entities and relationships for Neo4j graph construction"""

    def __init__(self, model_path: str = "models/v7_ner_model"):
        print(f"\n🔄 Loading v7 NER model from: {model_path}")
        self.nlp = spacy.load(model_path)
        self.doc_processor = DocumentProcessor()

        # Relationship patterns
        self.relationship_patterns = self._build_relationship_patterns()

        # Results storage
        self.entities = []
        self.relationships = []
        self.attack_paths = []
        self.cypher_statements = []

    def _build_relationship_patterns(self) -> Dict:
        """Define patterns for extracting relationships"""
        return {
            'EXPLOITS': [
                r'exploit[s]?\s+(?:the\s+)?(\w+)',
                r'vulnerable\s+to\s+(\w+)',
                r'affected\s+by\s+(\w+)',
                r'targeting\s+(\w+)',
            ],
            'USES': [
                r'use[s]?\s+(\w+)',
                r'leverage[s]?\s+(\w+)',
                r'deploy[s]?\s+(\w+)',
                r'utiliz[es]+\s+(\w+)',
            ],
            'TARGETS': [
                r'target[s]?\s+(\w+)',
                r'attack[s]?\s+(\w+)',
                r'compromise[s]?\s+(\w+)',
                r'affect[s]?\s+(\w+)',
            ],
            'ENABLES': [
                r'enable[s]?\s+(\w+)',
                r'allow[s]?\s+(\w+)',
                r'facilitate[s]?\s+(\w+)',
                r'lead[s]?\s+to\s+(\w+)',
            ],
            'MITIGATES': [
                r'mitigate[s]?\s+(\w+)',
                r'prevent[s]?\s+(\w+)',
                r'block[s]?\s+(\w+)',
                r'defend[s]?\s+against\s+(\w+)',
            ],
        }

    def extract_entities(self, text: str, doc_name: str) -> List[Dict]:
        """Extract entities from text"""
        doc = self.nlp(text)
        entities = []

        for ent in doc.ents:
            entity = {
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'source_doc': doc_name
            }
            entities.append(entity)

        return entities

    def extract_relationships(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Extract relationships between entities"""
        relationships = []

        # Create entity lookup by position
        entity_positions = [(e['start'], e['end'], e) for e in entities]
        entity_positions.sort()

        # Find relationships using patterns
        for rel_type, patterns in self.relationship_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    # Find nearby entities
                    match_pos = match.start()
                    window_start = max(0, match_pos - 200)
                    window_end = min(len(text), match_pos + 200)

                    # Find entities in window
                    nearby_entities = [
                        e for start, end, e in entity_positions
                        if window_start <= start <= window_end
                    ]

                    # Create relationships between nearby entities
                    if len(nearby_entities) >= 2:
                        for i in range(len(nearby_entities) - 1):
                            source = nearby_entities[i]
                            target = nearby_entities[i + 1]

                            relationship = {
                                'source': source['text'],
                                'source_type': source['label'],
                                'relationship': rel_type,
                                'target': target['text'],
                                'target_type': target['label'],
                                'context': text[window_start:window_end].strip()
                            }
                            relationships.append(relationship)

        return relationships

    def extract_attack_chains(self, entities: List[Dict], relationships: List[Dict]) -> List[Dict]:
        """Identify attack chains from relationships"""
        attack_chains = []

        # Build graph from relationships
        graph = defaultdict(list)
        for rel in relationships:
            if rel['relationship'] in ['EXPLOITS', 'USES', 'ENABLES', 'TARGETS']:
                graph[rel['source']].append((rel['relationship'], rel['target']))

        # Find chains (simple path detection)
        visited = set()
        for source in graph:
            if source not in visited:
                chain = self._build_chain(source, graph, visited)
                if len(chain) > 1:
                    attack_chains.append({
                        'chain': chain,
                        'length': len(chain),
                        'start': chain[0]['node'],
                        'end': chain[-1]['node']
                    })

        return attack_chains

    def _build_chain(self, start: str, graph: Dict, visited: Set, chain: List = None) -> List[Dict]:
        """Recursively build attack chain"""
        if chain is None:
            chain = []

        chain.append({'node': start, 'step': len(chain)})
        visited.add(start)

        if start in graph and len(chain) < 10:  # Max chain length
            for rel_type, target in graph[start]:
                if target not in visited:
                    chain.append({'relationship': rel_type})
                    self._build_chain(target, graph, visited, chain)
                    break  # Follow first path only

        return chain

    def generate_cypher_statements(self, entities: List[Dict], relationships: List[Dict],
                                   doc_name: str) -> List[str]:
        """Generate Cypher CREATE statements for Neo4j"""
        cypher = []

        # Create document node
        cypher.append(f"""
// Document Node
CREATE (doc:Document {{
    name: "{doc_name}",
    type: "Express_Attack_Brief",
    processed_date: date()
}})
""")

        # Create entity nodes (deduplicated)
        entity_map = {}
        for ent in entities:
            ent_key = f"{ent['label']}:{ent['text']}"
            if ent_key not in entity_map:
                entity_map[ent_key] = ent

                # Sanitize text for Cypher
                safe_text = ent['text'].replace('"', '\\"').replace('\n', ' ')[:100]

                cypher.append(f"""
// Entity: {ent['label']}
MERGE (e_{len(cypher)}:{ent['label']} {{
    name: "{safe_text}",
    type: "{ent['label']}"
}})
WITH e_{len(cypher)}
MATCH (doc:Document {{name: "{doc_name}"}})
CREATE (e_{len(cypher)})-[:MENTIONED_IN]->(doc)
""")

        # Create relationships
        for i, rel in enumerate(relationships):
            safe_source = rel['source'].replace('"', '\\"')[:50]
            safe_target = rel['target'].replace('"', '\\"')[:50]

            cypher.append(f"""
// Relationship: {rel['relationship']}
MATCH (source:{rel['source_type']} {{name: "{safe_source}"}})
MATCH (target:{rel['target_type']} {{name: "{safe_target}"}})
MERGE (source)-[:{rel['relationship']}]->(target)
""")

        return cypher

    def process_document(self, file_path: Path) -> Dict:
        """Process single document and extract everything"""
        print(f"\n📄 Processing: {file_path.name}")

        # Extract text
        text = self.doc_processor.read_document(str(file_path))
        if not text or len(text) < 100:
            print(f"  ⚠️  Insufficient text extracted")
            return None

        print(f"  ✅ Extracted {len(text):,} characters")

        # Extract entities
        entities = self.extract_entities(text, file_path.name)
        print(f"  🏷️  Found {len(entities)} entities")

        # Extract relationships
        relationships = self.extract_relationships(text, entities)
        print(f"  🔗 Found {len(relationships)} relationships")

        # Extract attack chains
        attack_chains = self.extract_attack_chains(entities, relationships)
        print(f"  ⛓️  Identified {len(attack_chains)} attack chains")

        # Generate Cypher
        cypher = self.generate_cypher_statements(entities, relationships, file_path.name)
        print(f"  📊 Generated {len(cypher)} Cypher statements")

        return {
            'document': file_path.name,
            'text_length': len(text),
            'entity_count': len(entities),
            'relationship_count': len(relationships),
            'attack_chain_count': len(attack_chains),
            'entities': entities,
            'relationships': relationships,
            'attack_chains': attack_chains,
            'cypher_statements': cypher
        }

    def process_directory(self, directory: Path, pattern: str = "*.docx") -> Dict:
        """Process all documents in directory"""
        files = sorted(directory.glob(pattern))
        print(f"\n📂 Found {len(files)} files matching {pattern}")

        results = {
            'total_documents': 0,
            'total_entities': 0,
            'total_relationships': 0,
            'total_attack_chains': 0,
            'documents': []
        }

        for file_path in files:
            result = self.process_document(file_path)
            if result:
                results['documents'].append(result)
                results['total_documents'] += 1
                results['total_entities'] += result['entity_count']
                results['total_relationships'] += result['relationship_count']
                results['total_attack_chains'] += result['attack_chain_count']

        return results

    def generate_summary_report(self, results: Dict) -> str:
        """Generate comprehensive summary report"""
        report = []
        report.append("\n" + "="*80)
        report.append("🔍 ENTITY & RELATIONSHIP EXTRACTION REPORT")
        report.append("="*80)

        # Overall stats
        report.append(f"\n📊 OVERALL STATISTICS:")
        report.append(f"   Documents Processed:    {results['total_documents']}")
        report.append(f"   Total Entities:         {results['total_entities']}")
        report.append(f"   Total Relationships:    {results['total_relationships']}")
        report.append(f"   Total Attack Chains:    {results['total_attack_chains']}")

        # Entity type distribution
        entity_types = defaultdict(int)
        for doc in results['documents']:
            for ent in doc['entities']:
                entity_types[ent['label']] += 1

        report.append(f"\n🏷️  ENTITY TYPE DISTRIBUTION:")
        for ent_type, count in sorted(entity_types.items(), key=lambda x: x[1], reverse=True):
            pct = (count / results['total_entities'] * 100) if results['total_entities'] > 0 else 0
            report.append(f"   {ent_type:20s} {count:6d} ({pct:5.2f}%)")

        # Relationship type distribution
        rel_types = defaultdict(int)
        for doc in results['documents']:
            for rel in doc['relationships']:
                rel_types[rel['relationship']] += 1

        report.append(f"\n🔗 RELATIONSHIP TYPE DISTRIBUTION:")
        for rel_type, count in sorted(rel_types.items(), key=lambda x: x[1], reverse=True):
            pct = (count / results['total_relationships'] * 100) if results['total_relationships'] > 0 else 0
            report.append(f"   {rel_type:20s} {count:6d} ({pct:5.2f}%)")

        # Top attack chains
        all_chains = []
        for doc in results['documents']:
            for chain in doc['attack_chains']:
                all_chains.append((doc['document'], chain))

        if all_chains:
            report.append(f"\n⛓️  TOP 10 ATTACK CHAINS:")
            sorted_chains = sorted(all_chains, key=lambda x: x[1]['length'], reverse=True)[:10]
            for i, (doc_name, chain) in enumerate(sorted_chains, 1):
                report.append(f"   {i:2d}. {doc_name[:40]:40s} - {chain['length']} steps")
                report.append(f"       {chain['start']} → {chain['end']}")

        # Document breakdown
        report.append(f"\n📄 DOCUMENT BREAKDOWN:")
        for doc in results['documents']:
            report.append(f"\n   {doc['document']}:")
            report.append(f"      Entities: {doc['entity_count']}")
            report.append(f"      Relationships: {doc['relationship_count']}")
            report.append(f"      Attack Chains: {doc['attack_chain_count']}")
            report.append(f"      Cypher Statements: {len(doc['cypher_statements'])}")

        return '\n'.join(report)

    def save_results(self, results: Dict, output_file: Path):
        """Save results to JSON"""
        # Remove large cypher statements for cleaner JSON
        clean_results = {
            'total_documents': results['total_documents'],
            'total_entities': results['total_entities'],
            'total_relationships': results['total_relationships'],
            'total_attack_chains': results['total_attack_chains'],
            'documents': []
        }

        for doc in results['documents']:
            clean_doc = {
                'document': doc['document'],
                'entity_count': doc['entity_count'],
                'relationship_count': doc['relationship_count'],
                'attack_chain_count': doc['attack_chain_count'],
                'entities': doc['entities'][:20],  # First 20 only
                'relationships': doc['relationships'][:20],  # First 20 only
                'attack_chains': doc['attack_chains'][:5]  # First 5 only
            }
            clean_results['documents'].append(clean_doc)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(clean_results, f, indent=2)

        print(f"\n💾 Results saved to: {output_file}")

    def save_cypher_statements(self, results: Dict, output_file: Path):
        """Save all Cypher statements to file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("// ============================================\n")
            f.write("// Neo4j Cypher Statements\n")
            f.write("// Express Attack Briefs Entity & Relationship Import\n")
            f.write("// ============================================\n\n")

            for doc in results['documents']:
                f.write(f"\n// ========== {doc['document']} ==========\n\n")
                for statement in doc['cypher_statements']:
                    f.write(statement)
                    f.write("\n")

        print(f"💾 Cypher statements saved to: {output_file}")


def main():
    """Main execution"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           ENTITY & RELATIONSHIP EXTRACTION FOR NEO4J                         ║
║                                                                              ║
║  Processing Express Attack Briefs:                                           ║
║  • Extract cybersecurity entities (CVE, CWE, CAPEC)                         ║
║  • Identify relationships between entities                                   ║
║  • Build attack chains and paths                                             ║
║  • Generate Neo4j Cypher statements                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Initialize extractor
    extractor = EntityRelationshipExtractor()

    # Process Express Attack Briefs
    briefs_dir = Path("/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/11_OXOT/OXOT - Reporting - Express Attack Briefs")
    results = extractor.process_directory(briefs_dir, "*.docx")

    # Generate and print report
    report = extractor.generate_summary_report(results)
    print(report)

    # Save results
    output_dir = Path("data/neo4j_import")
    output_dir.mkdir(parents=True, exist_ok=True)

    extractor.save_results(results, output_dir / "express_briefs_entities_relationships.json")
    extractor.save_cypher_statements(results, output_dir / "express_briefs_import.cypher")

    print(f"\n✅ Processing complete!")
    print(f"   📊 View results: data/neo4j_import/express_briefs_entities_relationships.json")
    print(f"   📜 View Cypher: data/neo4j_import/express_briefs_import.cypher")

    # Example queries
    print(f"\n" + "="*80)
    print("🔍 EXAMPLE NEO4J QUERIES YOU COULD RUN:")
    print("="*80)

    example_queries = """
// 1. Find all attack chains targeting critical infrastructure
MATCH path = (v:VULNERABILITY)-[:EXPLOITS]->(cwe:CWE)-[:ENABLES]->(capec:CAPEC)
WHERE capec.name CONTAINS "infrastructure"
RETURN path

// 2. Identify threat actors and their techniques
MATCH (actor:THREAT_ACTOR)-[:USES]->(capec:CAPEC)-[:EXPLOITS]->(vuln:VULNERABILITY)
RETURN actor.name, collect(capec.name) as techniques, count(vuln) as vulnerabilities

// 3. Find multi-stage attack paths
MATCH path = (start)-[*3..5]->(end)
WHERE start:VULNERABILITY AND end:CAPEC
RETURN path
LIMIT 10

// 4. Cross-document threat intelligence
MATCH (e:Entity)-[:MENTIONED_IN]->(d:Document)
WITH e, count(d) as doc_count
WHERE doc_count > 3
RETURN e.type, e.name, doc_count
ORDER BY doc_count DESC

// 5. Find common vulnerabilities across briefs
MATCH (v:VULNERABILITY)-[:MENTIONED_IN]->(d:Document)
WITH v, collect(d.name) as documents
WHERE size(documents) > 1
RETURN v.name, documents
"""

    print(example_queries)

    print("\n🎯 Next Steps:")
    print("   1. Review generated Cypher statements")
    print("   2. Load into Neo4j: cypher-shell < data/neo4j_import/express_briefs_import.cypher")
    print("   3. Run example queries to explore attack paths")
    print("   4. Build custom queries for your threat intelligence needs")


if __name__ == "__main__":
    main()
