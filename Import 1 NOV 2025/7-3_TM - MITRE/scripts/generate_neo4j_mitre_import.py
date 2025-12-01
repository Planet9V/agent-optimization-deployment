#!/usr/bin/env python3
"""
Neo4j Cypher Import Generator for MITRE ATT&CK Phase 2
Creates Cypher scripts for importing MITRE entities with bi-directional relationships.

Entity Types:
- AttackTechnique (from attack-pattern)
- Mitigation (from course-of-action)
- ThreatActor (from intrusion-set)
- Software (from malware/tool)
- DataSource (from x-mitre-data-source)

Relationship Types (Bi-directional):
- USES / USED_BY
- MITIGATES / MITIGATED_BY
- DETECTS / DETECTED_BY
- ATTRIBUTED_TO / ATTRIBUTES
- SUBTECHNIQUE_OF / PARENT_OF
"""

import json
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict

class Neo4jMitreImporter:
    """Generate Neo4j Cypher import scripts for MITRE ATT&CK"""

    def __init__(self, stix_file: str):
        self.stix_file = Path(stix_file)
        self.data = self._load_stix_data()
        self.entity_stats = defaultdict(int)
        self.relationship_stats = defaultdict(int)

    def _load_stix_data(self) -> dict:
        """Load MITRE ATT&CK STIX JSON data"""
        with open(self.stix_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _escape_string(self, text: str) -> str:
        """Escape string for Cypher query"""
        if not text:
            return ""
        return text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

    def _get_technique_id(self, technique: dict) -> str:
        """Extract MITRE ATT&CK ID"""
        for ref in technique.get('external_references', []):
            if ref.get('source_name') == 'mitre-attack':
                return ref.get('external_id', '')
        return ''

    def _get_tactic_names(self, technique: dict) -> List[str]:
        """Extract tactic names"""
        tactics = []
        for phase in technique.get('kill_chain_phases', []):
            tactic = phase.get('phase_name', '').replace('-', '_').upper()
            if tactic:
                tactics.append(tactic)
        return tactics

    def generate_technique_import(self) -> str:
        """Generate Cypher for AttackTechnique nodes"""
        techniques = [obj for obj in self.data.get('objects', [])
                      if obj.get('type') == 'attack-pattern']

        cypher_lines = []
        cypher_lines.append("// ========================================")
        cypher_lines.append("// MITRE ATT&CK Techniques Import")
        cypher_lines.append("// ========================================\n")

        cypher_lines.append("// Create AttackTechnique nodes")
        cypher_lines.append("CREATE CONSTRAINT IF NOT EXISTS FOR (t:AttackTechnique) REQUIRE t.id IS UNIQUE;")
        cypher_lines.append("CREATE INDEX IF NOT EXISTS FOR (t:AttackTechnique) ON (t.name);\n")

        batch_size = 100
        for i in range(0, len(techniques), batch_size):
            batch = techniques[i:i+batch_size]
            cypher_lines.append(f"// Batch {i//batch_size + 1}: Techniques {i+1} to {i+len(batch)}")
            cypher_lines.append("UNWIND [")

            for idx, tech in enumerate(batch):
                name = self._escape_string(tech.get('name', ''))
                tech_id = self._get_technique_id(tech)
                description = self._escape_string(tech.get('description', '')[:500])  # Truncate
                tactics = self._get_tactic_names(tech)
                is_subtechnique = '.' in tech_id
                modified = tech.get('modified', '')

                cypher_lines.append(f"  {{")
                cypher_lines.append(f"    id: '{tech_id}',")
                cypher_lines.append(f"    name: '{name}',")
                cypher_lines.append(f"    description: '{description}',")
                cypher_lines.append(f"    tactics: {tactics},")
                cypher_lines.append(f"    is_subtechnique: {str(is_subtechnique).lower()},")
                cypher_lines.append(f"    modified: '{modified}',")
                cypher_lines.append(f"    stix_id: '{tech.get('id', '')}'")
                cypher_lines.append(f"  }}" + ("," if idx < len(batch) - 1 else ""))

                self.entity_stats['AttackTechnique'] += 1

            cypher_lines.append("] AS tech")
            cypher_lines.append("MERGE (t:AttackTechnique {id: tech.id})")
            cypher_lines.append("SET t.name = tech.name,")
            cypher_lines.append("    t.description = tech.description,")
            cypher_lines.append("    t.tactics = tech.tactics,")
            cypher_lines.append("    t.is_subtechnique = tech.is_subtechnique,")
            cypher_lines.append("    t.modified = tech.modified,")
            cypher_lines.append("    t.stix_id = tech.stix_id;\n")

        return "\n".join(cypher_lines)

    def generate_mitigation_import(self) -> str:
        """Generate Cypher for Mitigation nodes"""
        mitigations = [obj for obj in self.data.get('objects', [])
                       if obj.get('type') == 'course-of-action']

        cypher_lines = []
        cypher_lines.append("// ========================================")
        cypher_lines.append("// MITRE ATT&CK Mitigations Import")
        cypher_lines.append("// ========================================\n")

        cypher_lines.append("// Create Mitigation nodes")
        cypher_lines.append("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Mitigation) REQUIRE m.id IS UNIQUE;")
        cypher_lines.append("CREATE INDEX IF NOT EXISTS FOR (m:Mitigation) ON (m.name);\n")

        cypher_lines.append("UNWIND [")
        for idx, mit in enumerate(mitigations):
            name = self._escape_string(mit.get('name', ''))
            mit_id = self._get_technique_id(mit)
            description = self._escape_string(mit.get('description', '')[:500])

            cypher_lines.append(f"  {{")
            cypher_lines.append(f"    id: '{mit_id}',")
            cypher_lines.append(f"    name: '{name}',")
            cypher_lines.append(f"    description: '{description}',")
            cypher_lines.append(f"    stix_id: '{mit.get('id', '')}'")
            cypher_lines.append(f"  }}" + ("," if idx < len(mitigations) - 1 else ""))

            self.entity_stats['Mitigation'] += 1

        cypher_lines.append("] AS mit")
        cypher_lines.append("MERGE (m:Mitigation {id: mit.id})")
        cypher_lines.append("SET m.name = mit.name,")
        cypher_lines.append("    m.description = mit.description,")
        cypher_lines.append("    m.stix_id = mit.stix_id;\n")

        return "\n".join(cypher_lines)

    def generate_actor_import(self) -> str:
        """Generate Cypher for ThreatActor nodes"""
        actors = [obj for obj in self.data.get('objects', [])
                  if obj.get('type') == 'intrusion-set']

        cypher_lines = []
        cypher_lines.append("// ========================================")
        cypher_lines.append("// MITRE ATT&CK Threat Actors Import")
        cypher_lines.append("// ========================================\n")

        cypher_lines.append("// Create ThreatActor nodes")
        cypher_lines.append("CREATE CONSTRAINT IF NOT EXISTS FOR (a:ThreatActor) REQUIRE a.stix_id IS UNIQUE;")
        cypher_lines.append("CREATE INDEX IF NOT EXISTS FOR (a:ThreatActor) ON (a.name);\n")

        cypher_lines.append("UNWIND [")
        for idx, actor in enumerate(actors):
            name = self._escape_string(actor.get('name', ''))
            description = self._escape_string(actor.get('description', '')[:500])
            aliases = actor.get('aliases', [])

            cypher_lines.append(f"  {{")
            cypher_lines.append(f"    name: '{name}',")
            cypher_lines.append(f"    description: '{description}',")
            cypher_lines.append(f"    aliases: {aliases},")
            cypher_lines.append(f"    stix_id: '{actor.get('id', '')}'")
            cypher_lines.append(f"  }}" + ("," if idx < len(actors) - 1 else ""))

            self.entity_stats['ThreatActor'] += 1

        cypher_lines.append("] AS actor")
        cypher_lines.append("MERGE (a:ThreatActor {stix_id: actor.stix_id})")
        cypher_lines.append("SET a.name = actor.name,")
        cypher_lines.append("    a.description = actor.description,")
        cypher_lines.append("    a.aliases = actor.aliases;\n")

        return "\n".join(cypher_lines)

    def generate_software_import(self) -> str:
        """Generate Cypher for Software nodes (malware + tools)"""
        software = [obj for obj in self.data.get('objects', [])
                    if obj.get('type') in ('malware', 'tool')]

        cypher_lines = []
        cypher_lines.append("// ========================================")
        cypher_lines.append("// MITRE ATT&CK Software Import")
        cypher_lines.append("// ========================================\n")

        cypher_lines.append("// Create Software nodes")
        cypher_lines.append("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Software) REQUIRE s.stix_id IS UNIQUE;")
        cypher_lines.append("CREATE INDEX IF NOT EXISTS FOR (s:Software) ON (s.name);\n")

        cypher_lines.append("UNWIND [")
        for idx, sw in enumerate(software):
            name = self._escape_string(sw.get('name', ''))
            sw_type = sw.get('type', '')
            description = self._escape_string(sw.get('description', '')[:500])

            cypher_lines.append(f"  {{")
            cypher_lines.append(f"    name: '{name}',")
            cypher_lines.append(f"    type: '{sw_type}',")
            cypher_lines.append(f"    description: '{description}',")
            cypher_lines.append(f"    stix_id: '{sw.get('id', '')}'")
            cypher_lines.append(f"  }}" + ("," if idx < len(software) - 1 else ""))

            self.entity_stats['Software'] += 1

        cypher_lines.append("] AS sw")
        cypher_lines.append("MERGE (s:Software {stix_id: sw.stix_id})")
        cypher_lines.append("SET s.name = sw.name,")
        cypher_lines.append("    s.type = sw.type,")
        cypher_lines.append("    s.description = sw.description;\n")

        return "\n".join(cypher_lines)

    def generate_relationship_import(self) -> str:
        """Generate Cypher for bi-directional relationships"""
        relationships = [obj for obj in self.data.get('objects', [])
                         if obj.get('type') == 'relationship']

        cypher_lines = []
        cypher_lines.append("// ========================================")
        cypher_lines.append("// MITRE ATT&CK Relationships (Bi-directional)")
        cypher_lines.append("// ========================================\n")

        # Group by relationship type
        rel_groups = defaultdict(list)
        for rel in relationships:
            rel_type = rel.get('relationship_type', '')
            rel_groups[rel_type].append(rel)

        # Generate Cypher for each relationship type
        for rel_type, rels in rel_groups.items():
            cypher_lines.append(f"// {rel_type.upper()} relationships")

            # Map MITRE types to bi-directional Neo4j types
            if rel_type == 'uses':
                forward_rel = 'USES'
                backward_rel = 'USED_BY'
            elif rel_type == 'mitigates':
                forward_rel = 'MITIGATES'
                backward_rel = 'MITIGATED_BY'
            elif rel_type == 'detects':
                forward_rel = 'DETECTS'
                backward_rel = 'DETECTED_BY'
            elif rel_type == 'attributed-to':
                forward_rel = 'ATTRIBUTED_TO'
                backward_rel = 'ATTRIBUTES'
            elif rel_type == 'subtechnique-of':
                forward_rel = 'SUBTECHNIQUE_OF'
                backward_rel = 'PARENT_OF'
            else:
                forward_rel = rel_type.upper().replace('-', '_')
                backward_rel = f"{forward_rel}_REV"

            cypher_lines.append("UNWIND [")
            for idx, rel in enumerate(rels):
                source_ref = rel.get('source_ref', '')
                target_ref = rel.get('target_ref', '')
                description = self._escape_string(rel.get('description', '')[:200])

                cypher_lines.append(f"  {{")
                cypher_lines.append(f"    source: '{source_ref}',")
                cypher_lines.append(f"    target: '{target_ref}',")
                cypher_lines.append(f"    description: '{description}'")
                cypher_lines.append(f"  }}" + ("," if idx < len(rels) - 1 else ""))

                self.relationship_stats[forward_rel] += 1
                self.relationship_stats[backward_rel] += 1

            cypher_lines.append("] AS rel")
            cypher_lines.append("MATCH (source {stix_id: rel.source})")
            cypher_lines.append("MATCH (target {stix_id: rel.target})")
            cypher_lines.append(f"MERGE (source)-[r1:{forward_rel}]->(target)")
            cypher_lines.append("SET r1.description = rel.description")
            cypher_lines.append(f"MERGE (target)-[r2:{backward_rel}]->(source)")
            cypher_lines.append("SET r2.description = rel.description;\n")

        return "\n".join(cypher_lines)

    def generate_complete_import_script(self, output_file: str):
        """Generate complete Neo4j import script"""
        print("=" * 80)
        print("Generating Neo4j Cypher Import Scripts...")
        print("=" * 80)

        cypher_script = []
        cypher_script.append("// ========================================")
        cypher_script.append("// MITRE ATT&CK Phase 2 - Neo4j Import Script")
        cypher_script.append("// Generated for bi-directional relationship support")
        cypher_script.append("// ========================================\n")

        # Entity imports
        print("\nGenerating entity imports...")
        cypher_script.append(self.generate_technique_import())
        cypher_script.append(self.generate_mitigation_import())
        cypher_script.append(self.generate_actor_import())
        cypher_script.append(self.generate_software_import())

        # Relationship imports
        print("Generating relationship imports...")
        cypher_script.append(self.generate_relationship_import())

        # Write to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cypher_script))

        print(f"\n✓ Import script saved to: {output_path}")
        print(f"  File size: {output_path.stat().st_size / 1024:.2f} KB")

        # Print statistics
        print("\n" + "=" * 80)
        print("Import Statistics")
        print("=" * 80)
        print("\nEntity Counts:")
        for entity_type, count in sorted(self.entity_stats.items()):
            print(f"  {entity_type}: {count}")

        print("\nRelationship Counts (includes bi-directional):")
        for rel_type, count in sorted(self.relationship_stats.items()):
            print(f"  {rel_type}: {count}")


def main():
    """Main execution"""

    stix_file = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/MITRE-ATT-CK-STIX/enterprise-attack/enterprise-attack-17.0.json"
    output_file = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE/scripts/neo4j_mitre_import.cypher"

    print("=" * 80)
    print("Neo4j MITRE ATT&CK Import Generator - Phase 2")
    print("=" * 80)
    print(f"\nSource: {stix_file}")
    print(f"Output: {output_file}")
    print(f"\nFeatures:")
    print("  - Bi-directional relationships (USES ↔ USED_BY)")
    print("  - Full entity coverage (Techniques, Mitigations, Actors, Software)")
    print("  - Batch import optimization")
    print("  - STIX ID preservation for future updates\n")

    importer = Neo4jMitreImporter(stix_file)
    importer.generate_complete_import_script(output_file)

    print("\n" + "=" * 80)
    print("Next Steps")
    print("=" * 80)
    print("\n1. Start Neo4j database")
    print("2. Execute import script:")
    print(f"   cat {output_file} | cypher-shell -u neo4j -p password")
    print("3. Verify import:")
    print("   MATCH (t:AttackTechnique) RETURN count(t)")
    print("   MATCH ()-[r:USES]->() RETURN count(r)")
    print("4. Test bi-directional queries:")
    print("   MATCH (a)-[:USES]->(t:AttackTechnique) RETURN a.name, t.name LIMIT 5")
    print("   MATCH (t:AttackTechnique)<-[:USED_BY]-(a) RETURN t.name, a.name LIMIT 5")
    print("\n")


if __name__ == "__main__":
    main()
