#!/usr/bin/env python3
"""
ICS-SEC-KG OWL Ontology Parser
Extracts CVE→CWE→CAPEC→ATT&CK semantic mappings from ICS-SEC-KG ontology
Week 1 Proof-of-Concept: Attack Chain Unification
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
from neo4j import GraphDatabase

# OWL Ontology paths
ICS_KG_DIR = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/ICS-SEC-KG/src/main/resources/owl')

# Neo4j connection
NEO4J_URI = 'bolt://localhost:7687'
NEO4J_AUTH = ('neo4j', 'neo4j@openspg')

class ICSSecKGParser:
    """Parse ICS-SEC-KG OWL ontology for attack chain mappings"""

    def __init__(self):
        self.cve_to_cwe: Dict[str, Set[str]] = defaultdict(set)
        self.capec_to_cwe: Dict[str, Set[str]] = defaultdict(set)
        self.attack_to_capec: Dict[str, Set[str]] = defaultdict(set)
        self.attack_to_tactic: Dict[str, Set[str]] = defaultdict(set)

        # Statistics
        self.stats = {
            'cve_cwe_mappings': 0,
            'capec_cwe_mappings': 0,
            'attack_capec_mappings': 0,
            'complete_chains': 0,
            'unique_cves': set(),
            'unique_cwes': set(),
            'unique_capecs': set(),
            'unique_attacks': set()
        }

    def parse_turtle_file(self, file_path: Path) -> List[Tuple[str, str, str]]:
        """
        Parse Turtle/TTL file to extract RDF triples
        Returns: List of (subject, predicate, object) tuples
        """
        triples = []
        content = file_path.read_text()

        # Remove comments and blank lines
        lines = [line.split('#')[0].strip() for line in content.split('\n')]
        content_clean = ' '.join(line for line in lines if line)

        # Extract triples (simplified parser - handles basic turtle syntax)
        # Pattern: <subject> <predicate> <object> .
        triple_pattern = r'<([^>]+)>\s+<([^>]+)>\s+<([^>]+)>\s*[;.]'
        matches = re.finditer(triple_pattern, content_clean)

        for match in matches:
            subject = match.group(1)
            predicate = match.group(2)
            obj = match.group(3)
            triples.append((subject, predicate, obj))

        return triples

    def extract_id_from_uri(self, uri: str) -> str:
        """Extract identifier from URI (e.g., CVE-2021-44228 from full URI)"""
        # Common patterns
        if 'cve' in uri.lower():
            match = re.search(r'(CVE-\d{4}-\d+)', uri, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        if 'cwe' in uri.lower():
            match = re.search(r'(CWE-\d+)', uri, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        if 'capec' in uri.lower():
            match = re.search(r'(CAPEC-\d+)', uri, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        if 'attack' in uri.lower():
            match = re.search(r'(T\d{4}(?:\.\d{3})?)', uri, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        # Fallback: return last part of URI
        return uri.split('/')[-1].split('#')[-1]

    def parse_cve_cwe_mappings(self, integrated_ttl: Path):
        """Parse CVE→CWE mappings from integrated.ttl"""
        print(f"📖 Parsing CVE→CWE mappings from {integrated_ttl.name}...")

        triples = self.parse_turtle_file(integrated_ttl)

        for subject, predicate, obj in triples:
            # Look for cve:hasCWE relationships
            if 'hasCWE' in predicate:
                cve_id = self.extract_id_from_uri(subject)
                cwe_id = self.extract_id_from_uri(obj)

                if cve_id.startswith('CVE') and cwe_id.startswith('CWE'):
                    self.cve_to_cwe[cve_id].add(cwe_id)
                    self.stats['cve_cwe_mappings'] += 1
                    self.stats['unique_cves'].add(cve_id)
                    self.stats['unique_cwes'].add(cwe_id)

        print(f"✅ Found {self.stats['cve_cwe_mappings']} CVE→CWE mappings")
        print(f"   Unique CVEs: {len(self.stats['unique_cves'])}")
        print(f"   Unique CWEs: {len(self.stats['unique_cwes'])}")

    def parse_capec_cwe_mappings(self, integrated_ttl: Path):
        """Parse CAPEC→CWE mappings from integrated.ttl"""
        print(f"\n📖 Parsing CAPEC→CWE mappings from {integrated_ttl.name}...")

        triples = self.parse_turtle_file(integrated_ttl)

        for subject, predicate, obj in triples:
            # Look for capec:hasRelatedWeakness relationships
            if 'hasRelatedWeakness' in predicate:
                capec_id = self.extract_id_from_uri(subject)
                cwe_id = self.extract_id_from_uri(obj)

                if capec_id.startswith('CAPEC') and cwe_id.startswith('CWE'):
                    self.capec_to_cwe[capec_id].add(cwe_id)
                    self.stats['capec_cwe_mappings'] += 1
                    self.stats['unique_capecs'].add(capec_id)
                    self.stats['unique_cwes'].add(cwe_id)

        print(f"✅ Found {self.stats['capec_cwe_mappings']} CAPEC→CWE mappings")
        print(f"   Unique CAPECs: {len(self.stats['unique_capecs'])}")

    def parse_attack_capec_mappings(self, integrated_ttl: Path):
        """Parse ATT&CK→CAPEC mappings from integrated.ttl"""
        print(f"\n📖 Parsing ATT&CK→CAPEC mappings from {integrated_ttl.name}...")

        triples = self.parse_turtle_file(integrated_ttl)

        for subject, predicate, obj in triples:
            # Look for attack:hasCAPEC relationships
            if 'hasCAPEC' in predicate:
                attack_id = self.extract_id_from_uri(subject)
                capec_id = self.extract_id_from_uri(obj)

                if attack_id.startswith('T') and capec_id.startswith('CAPEC'):
                    self.attack_to_capec[attack_id].add(capec_id)
                    self.stats['attack_capec_mappings'] += 1
                    self.stats['unique_attacks'].add(attack_id)
                    self.stats['unique_capecs'].add(capec_id)

            # Also capture ATT&CK→Tactic relationships
            if 'accomplishesTactic' in predicate:
                attack_id = self.extract_id_from_uri(subject)
                tactic_id = self.extract_id_from_uri(obj)

                if attack_id.startswith('T'):
                    self.attack_to_tactic[attack_id].add(tactic_id)

        print(f"✅ Found {self.stats['attack_capec_mappings']} ATT&CK→CAPEC mappings")
        print(f"   Unique ATT&CK Techniques: {len(self.stats['unique_attacks'])}")

    def compute_complete_chains(self) -> List[Dict]:
        """
        Compute complete CVE→CWE→CAPEC→ATT&CK chains
        Returns list of complete chain dicts
        """
        print("\n🔗 Computing complete attack chains...")
        complete_chains = []

        for cve_id, cwe_set in self.cve_to_cwe.items():
            for cwe_id in cwe_set:
                # Find CAPECs that connect to this CWE
                for capec_id, capec_cwe_set in self.capec_to_cwe.items():
                    if cwe_id in capec_cwe_set:
                        # Find ATT&CK techniques that use this CAPEC
                        for attack_id, attack_capec_set in self.attack_to_capec.items():
                            if capec_id in attack_capec_set:
                                # Complete chain found!
                                tactics = self.attack_to_tactic.get(attack_id, set())

                                chain = {
                                    'cve_id': cve_id,
                                    'cwe_id': cwe_id,
                                    'capec_id': capec_id,
                                    'attack_id': attack_id,
                                    'tactics': list(tactics)
                                }
                                complete_chains.append(chain)
                                self.stats['complete_chains'] += 1

        print(f"✅ Found {len(complete_chains)} complete CVE→CWE→CAPEC→ATT&CK chains")
        return complete_chains

    def generate_neo4j_cypher(self, chains: List[Dict], output_file: Path):
        """Generate Neo4j Cypher import statements"""
        print(f"\n📝 Generating Neo4j Cypher import script...")

        cypher_statements = []

        # Header
        cypher_statements.append("// ICS-SEC-KG Attack Chain Import")
        cypher_statements.append("// Generated from ICS-SEC-KG OWL Ontology")
        cypher_statements.append("// Week 1 Proof-of-Concept: Complete CVE→ATT&CK Chains\n")

        # Create indexes
        cypher_statements.append("// Create indexes for performance")
        cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:CVE) ON (n.id);")
        cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:CWE) ON (n.id);")
        cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:CAPEC) ON (n.capecId);")
        cypher_statements.append("CREATE INDEX IF NOT EXISTS FOR (n:AttackTechnique) ON (n.techniqueId);\n")

        # Import chains
        cypher_statements.append(f"// Import {len(chains)} complete attack chains")

        for i, chain in enumerate(chains[:100], 1):  # Limit to 100 for proof-of-concept
            cve_id = chain['cve_id']
            cwe_id = chain['cwe_id']
            capec_id = chain['capec_id']
            attack_id = chain['attack_id']

            cypher = f"""
// Chain {i}: {cve_id} → {cwe_id} → {capec_id} → {attack_id}
MERGE (cve:CVE {{id: '{cve_id}'}})
MERGE (cwe:CWE {{id: '{cwe_id}'}})
MERGE (capec:CAPEC {{capecId: '{capec_id}'}})
MERGE (attack:AttackTechnique {{techniqueId: '{attack_id}'}})

MERGE (cve)-[:HAS_CWE]->(cwe)
MERGE (cwe)-[:ENABLES_ATTACK_PATTERN]->(capec)
MERGE (capec)-[:USES_TECHNIQUE]->(attack)

SET cve.source = 'ICS-SEC-KG',
    cve.chain_complete = true,
    cve.imported_date = datetime();
"""
            cypher_statements.append(cypher)

        # Write to file
        output_file.write_text('\n'.join(cypher_statements))
        print(f"✅ Generated Cypher script: {output_file}")
        print(f"   Statements: {len(cypher_statements)}")
        print(f"   Chains included: {min(100, len(chains))}")

    def generate_analysis_report(self, chains: List[Dict], output_file: Path):
        """Generate comprehensive analysis report"""
        print(f"\n📊 Generating analysis report...")

        report = {
            'analysis_date': '2025-11-08',
            'source': 'ICS-SEC-KG OWL Ontology',
            'ontology_path': str(ICS_KG_DIR),

            'statistics': {
                'total_cve_cwe_mappings': self.stats['cve_cwe_mappings'],
                'total_capec_cwe_mappings': self.stats['capec_cwe_mappings'],
                'total_attack_capec_mappings': self.stats['attack_capec_mappings'],
                'complete_chains_found': len(chains),

                'unique_entities': {
                    'cves': len(self.stats['unique_cves']),
                    'cwes': len(self.stats['unique_cwes']),
                    'capecs': len(self.stats['unique_capecs']),
                    'attack_techniques': len(self.stats['unique_attacks'])
                }
            },

            'sample_chains': chains[:10],

            'coverage_analysis': {
                'cve_with_complete_chains': len(set(c['cve_id'] for c in chains)),
                'attack_techniques_reachable': len(set(c['attack_id'] for c in chains)),
                'capecs_in_chains': len(set(c['capec_id'] for c in chains))
            }
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"✅ Generated report: {output_file}")

        return report

def main():
    print("="*80)
    print("ICS-SEC-KG OWL ONTOLOGY PARSER")
    print("Week 1 Proof-of-Concept: Attack Chain Unification")
    print("="*80)
    print()

    parser = ICSSecKGParser()

    # Parse integrated ontology
    integrated_ttl = ICS_KG_DIR / 'integrated.ttl'

    if not integrated_ttl.exists():
        print(f"❌ ERROR: {integrated_ttl} not found")
        return

    # Step 1: Parse all mappings
    parser.parse_cve_cwe_mappings(integrated_ttl)
    parser.parse_capec_cwe_mappings(integrated_ttl)
    parser.parse_attack_capec_mappings(integrated_ttl)

    # Step 2: Compute complete chains
    chains = parser.compute_complete_chains()

    # Step 3: Generate outputs
    output_dir = Path('docs')
    output_dir.mkdir(exist_ok=True)

    cypher_file = output_dir / 'ICS_SEC_KG_ATTACK_CHAINS.cypher'
    report_file = output_dir / 'ICS_SEC_KG_PARSER_REPORT.json'

    parser.generate_neo4j_cypher(chains, cypher_file)
    report = parser.generate_analysis_report(chains, report_file)

    # Step 4: Summary
    print("\n" + "="*80)
    print("📈 PARSING SUMMARY")
    print("="*80)
    print(f"✅ CVE→CWE mappings:       {report['statistics']['total_cve_cwe_mappings']:,}")
    print(f"✅ CAPEC→CWE mappings:     {report['statistics']['total_capec_cwe_mappings']:,}")
    print(f"✅ ATT&CK→CAPEC mappings:  {report['statistics']['total_attack_capec_mappings']:,}")
    print(f"✅ Complete chains found:  {report['statistics']['complete_chains_found']:,}")
    print()
    print(f"📊 Coverage Analysis:")
    print(f"   CVEs with complete chains: {report['coverage_analysis']['cve_with_complete_chains']}")
    print(f"   ATT&CK techniques reachable: {report['coverage_analysis']['attack_techniques_reachable']}")
    print()
    print(f"📁 Output Files:")
    print(f"   Cypher script: {cypher_file}")
    print(f"   Analysis report: {report_file}")
    print()

if __name__ == '__main__':
    main()
