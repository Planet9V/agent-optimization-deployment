#!/usr/bin/env python3
"""
Comprehensive Taxonomy Loader for AEON Cyber Digital Twin
Loads all security taxonomy data with proper Neo4j schema and Qdrant embeddings.

Data Sources:
- CAPEC v3.9 (Attack Patterns)
- CWE v4.18 (Weaknesses)
- EMB3D STIX 2.0.1 (Embedded Device Threats)
- MITRE ATT&CK Enterprise (835 techniques)
- MITRE ATT&CK Mobile (190 techniques)
- MITRE ATT&CK ICS (95 techniques)
- VulnCheck KEV (Known Exploited Vulnerabilities)
- EPSS Scores (303,657 CVE exploitability scores)

Neo4j Schema:
- Node Labels: CAPEC, CWE, EMB3D_Threat, EMB3D_Mitigation, EMB3D_Property,
               ATT&CK_Technique, ATT&CK_Tactic, VulnCheck_KEV, CVE, EPSS
- Relationships: CHILD_OF, BELONGS_TO, EXPLOITS, MITIGATES, USES_TECHNIQUE,
                 HAS_EPSS, TARGETS, MAPPED_TO, RELATED_TO

Usage:
    python3 scripts/load_comprehensive_taxonomy.py --all
    python3 scripts/load_comprehensive_taxonomy.py --capec --cwe --emb3d
    python3 scripts/load_comprehensive_taxonomy.py --mitre --vulncheck --epss
"""

import sys
import argparse
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from neo4j import GraphDatabase

# Optional: Qdrant for embeddings
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, Distance, VectorParams
    from sentence_transformers import SentenceTransformer
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    print("Warning: Qdrant/SentenceTransformer not available, skipping embeddings")

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "taxonomy_embeddings"

# Base path for data files
BASE_PATH = Path("/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/NVS Full CVE CAPEC CWE EMBED")

# XML Namespaces
CAPEC_NS = {'capec': 'http://capec.mitre.org/capec-3'}
CWE_NS = {'cwe': 'http://cwe.mitre.org/cwe-7'}


class ComprehensiveTaxonomyLoader:
    """Loads all security taxonomy data into Neo4j and Qdrant."""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 skip_embeddings: bool = False):
        self.driver = GraphDatabase.driver(
            neo4j_uri, auth=(neo4j_user, neo4j_password)
        )
        print(f"Connected to Neo4j at {neo4j_uri}")

        self.skip_embeddings = skip_embeddings or not QDRANT_AVAILABLE

        if not self.skip_embeddings:
            self.qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            self._ensure_collection()
            print("Loading embedding model...")
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print("Embedding model loaded")

        self.stats = {
            "capec": {"nodes": 0, "relationships": 0},
            "cwe": {"nodes": 0, "relationships": 0},
            "emb3d": {"nodes": 0, "relationships": 0},
            "attack_enterprise": {"nodes": 0, "relationships": 0},
            "attack_mobile": {"nodes": 0, "relationships": 0},
            "attack_ics": {"nodes": 0, "relationships": 0},
            "vulncheck": {"nodes": 0, "relationships": 0},
            "epss": {"nodes": 0, "relationships": 0},
            "cross_links": 0,
            "embeddings": 0
        }

    def _ensure_collection(self):
        """Ensure Qdrant collection exists."""
        try:
            self.qdrant.get_collection(COLLECTION_NAME)
        except:
            self.qdrant.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"Created Qdrant collection: {COLLECTION_NAME}")

    def close(self):
        self.driver.close()

    def _store_embedding(self, text: str, label: str, entity_id: str, metadata: Dict = None):
        """Store embedding in Qdrant."""
        if self.skip_embeddings:
            return
        try:
            embedding = self.embedding_model.encode(text).tolist()
            point_id = hash(f"{label}_{entity_id}") % (2**63)
            payload = {
                "text": text[:500],
                "label": label,
                "entity_id": entity_id,
                "created_at": datetime.utcnow().isoformat()
            }
            if metadata:
                payload.update(metadata)
            self.qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[PointStruct(id=point_id, vector=embedding, payload=payload)]
            )
            self.stats["embeddings"] += 1
        except Exception as e:
            pass  # Silent fail for embeddings

    # ============== CAPEC LOADER ==============
    def load_capec(self, force: bool = False) -> Dict:
        """Load CAPEC attack patterns from XML."""
        capec_file = BASE_PATH / "capec_latest" / "capec_v3.9.xml"
        if not capec_file.exists():
            print(f"CAPEC file not found: {capec_file}")
            return self.stats["capec"]

        print(f"\n{'='*60}")
        print("LOADING CAPEC v3.9 ATTACK PATTERNS")
        print(f"{'='*60}")

        tree = ET.parse(capec_file)
        root = tree.getroot()

        # Create indexes
        with self.driver.session() as session:
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:CAPEC) ON (c.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:CAPEC_Category) ON (c.id)")

        # Load attack patterns
        patterns = root.findall('.//capec:Attack_Pattern', CAPEC_NS)
        print(f"Found {len(patterns)} attack patterns")

        with self.driver.session() as session:
            for pattern in patterns:
                capec_id = f"CAPEC-{pattern.get('ID')}"
                name = pattern.get('Name', '')
                status = pattern.get('Status', '')

                desc_elem = pattern.find('.//capec:Description', CAPEC_NS)
                description = self._get_text_content(desc_elem) if desc_elem is not None else ''

                # Get likelihood and severity
                likelihood = pattern.find('.//capec:Likelihood_Of_Attack', CAPEC_NS)
                likelihood_text = likelihood.text if likelihood is not None else ''
                severity = pattern.find('.//capec:Typical_Severity', CAPEC_NS)
                severity_text = severity.text if severity is not None else ''

                session.run("""
                    MERGE (c:CAPEC {id: $id})
                    SET c.name = $name,
                        c.status = $status,
                        c.description = $desc,
                        c.likelihood = $likelihood,
                        c.severity = $severity,
                        c.taxonomy = 'CAPEC',
                        c.version = 'v3.9',
                        c.updated_at = timestamp()
                """, id=capec_id, name=name, status=status, desc=description[:2000],
                    likelihood=likelihood_text, severity=severity_text)
                self.stats["capec"]["nodes"] += 1

                # Store embedding
                self._store_embedding(f"{name}. {description}", "CAPEC", capec_id)

                # Create hierarchy from Related_Attack_Patterns
                related = pattern.findall('.//capec:Related_Attack_Pattern', CAPEC_NS)
                for rel in related:
                    nature = rel.get('Nature', '')
                    target_id = f"CAPEC-{rel.get('CAPEC_ID')}"
                    if nature == 'ChildOf':
                        session.run("""
                            MATCH (child:CAPEC {id: $child_id})
                            MERGE (parent:CAPEC {id: $parent_id})
                            MERGE (child)-[:CHILD_OF]->(parent)
                        """, child_id=capec_id, parent_id=target_id)
                        self.stats["capec"]["relationships"] += 1

                # Link to CWEs
                cwes = pattern.findall('.//capec:Related_Weakness', CAPEC_NS)
                for cwe in cwes:
                    cwe_id = f"CWE-{cwe.get('CWE_ID')}"
                    session.run("""
                        MATCH (c:CAPEC {id: $capec_id})
                        MERGE (w:CWE {id: $cwe_id})
                        MERGE (c)-[:EXPLOITS]->(w)
                    """, capec_id=capec_id, cwe_id=cwe_id)
                    self.stats["cross_links"] += 1

        # Load categories
        categories = root.findall('.//capec:Category', CAPEC_NS)
        print(f"Found {len(categories)} categories")

        with self.driver.session() as session:
            for cat in categories:
                cat_id = f"CAPEC-CAT-{cat.get('ID')}"
                name = cat.get('Name', '')
                status = cat.get('Status', '')

                summary = cat.find('.//capec:Summary', CAPEC_NS)
                summary_text = self._get_text_content(summary) if summary is not None else ''

                session.run("""
                    MERGE (c:CAPEC_Category {id: $id})
                    SET c.name = $name,
                        c.status = $status,
                        c.summary = $summary,
                        c.taxonomy = 'CAPEC',
                        c.updated_at = timestamp()
                """, id=cat_id, name=name, status=status, summary=summary_text[:2000])
                self.stats["capec"]["nodes"] += 1

                # Link members
                members = cat.findall('.//capec:Member_Of', CAPEC_NS)
                for member in members:
                    pattern_id = f"CAPEC-{member.get('CAPEC_ID')}"
                    session.run("""
                        MATCH (p:CAPEC {id: $pattern_id})
                        MATCH (c:CAPEC_Category {id: $cat_id})
                        MERGE (p)-[:BELONGS_TO]->(c)
                    """, pattern_id=pattern_id, cat_id=cat_id)
                    self.stats["capec"]["relationships"] += 1

        print(f"CAPEC: {self.stats['capec']['nodes']} nodes, {self.stats['capec']['relationships']} relationships")
        return self.stats["capec"]

    # ============== CWE LOADER ==============
    def load_cwe(self, force: bool = False) -> Dict:
        """Load CWE weaknesses from XML."""
        cwe_file = BASE_PATH / "cwec_v4.18.xml"
        if not cwe_file.exists():
            print(f"CWE file not found: {cwe_file}")
            return self.stats["cwe"]

        print(f"\n{'='*60}")
        print("LOADING CWE v4.18 WEAKNESSES")
        print(f"{'='*60}")

        tree = ET.parse(cwe_file)
        root = tree.getroot()

        # Create indexes
        with self.driver.session() as session:
            session.run("CREATE INDEX IF NOT EXISTS FOR (w:CWE) ON (w.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:CWE_Category) ON (c.id)")

        # Load weaknesses
        weaknesses = root.findall('.//cwe:Weakness', CWE_NS)
        print(f"Found {len(weaknesses)} weaknesses")

        with self.driver.session() as session:
            for weakness in weaknesses:
                cwe_id = f"CWE-{weakness.get('ID')}"
                name = weakness.get('Name', '')
                abstraction = weakness.get('Abstraction', '')
                status = weakness.get('Status', '')

                desc = weakness.find('.//cwe:Description', CWE_NS)
                description = desc.text if desc is not None and desc.text else ''

                session.run("""
                    MERGE (w:CWE {id: $id})
                    SET w.name = $name,
                        w.abstraction = $abstraction,
                        w.status = $status,
                        w.description = $desc,
                        w.taxonomy = 'CWE',
                        w.version = 'v4.18',
                        w.updated_at = timestamp()
                """, id=cwe_id, name=name, abstraction=abstraction,
                    status=status, desc=description[:2000])
                self.stats["cwe"]["nodes"] += 1

                # Store embedding
                self._store_embedding(f"{name}. {description}", "CWE", cwe_id)

                # Create hierarchy
                related = weakness.findall('.//cwe:Related_Weakness', CWE_NS)
                for rel in related:
                    nature = rel.get('Nature', '')
                    target_id = f"CWE-{rel.get('CWE_ID')}"
                    if nature == 'ChildOf':
                        session.run("""
                            MATCH (child:CWE {id: $child_id})
                            MERGE (parent:CWE {id: $parent_id})
                            MERGE (child)-[:CHILD_OF]->(parent)
                        """, child_id=cwe_id, parent_id=target_id)
                        self.stats["cwe"]["relationships"] += 1

        # Load categories
        categories = root.findall('.//cwe:Category', CWE_NS)
        print(f"Found {len(categories)} categories")

        with self.driver.session() as session:
            for cat in categories:
                cat_id = f"CWE-CAT-{cat.get('ID')}"
                name = cat.get('Name', '')
                status = cat.get('Status', '')

                summary = cat.find('.//cwe:Summary', CWE_NS)
                summary_text = summary.text if summary is not None and summary.text else ''

                session.run("""
                    MERGE (c:CWE_Category {id: $id})
                    SET c.name = $name,
                        c.status = $status,
                        c.summary = $summary,
                        c.taxonomy = 'CWE',
                        c.updated_at = timestamp()
                """, id=cat_id, name=name, status=status, summary=summary_text[:2000])
                self.stats["cwe"]["nodes"] += 1

                # Link members
                members = cat.findall('.//cwe:Has_Member', CWE_NS)
                for member in members:
                    weakness_id = f"CWE-{member.get('CWE_ID')}"
                    session.run("""
                        MATCH (w:CWE {id: $weakness_id})
                        MATCH (c:CWE_Category {id: $cat_id})
                        MERGE (w)-[:BELONGS_TO]->(c)
                    """, weakness_id=weakness_id, cat_id=cat_id)
                    self.stats["cwe"]["relationships"] += 1

        print(f"CWE: {self.stats['cwe']['nodes']} nodes, {self.stats['cwe']['relationships']} relationships")
        return self.stats["cwe"]

    # ============== EMB3D LOADER ==============
    def load_emb3d(self, force: bool = False) -> Dict:
        """Load EMB3D embedded device threats from STIX JSON."""
        emb3d_file = BASE_PATH / "emb3d-stix-2.0.1.json"
        if not emb3d_file.exists():
            print(f"EMB3D file not found: {emb3d_file}")
            return self.stats["emb3d"]

        print(f"\n{'='*60}")
        print("LOADING EMB3D STIX 2.0.1")
        print(f"{'='*60}")

        with open(emb3d_file, 'r') as f:
            data = json.load(f)

        objects = data.get('objects', [])

        # Create indexes
        with self.driver.session() as session:
            session.run("CREATE INDEX IF NOT EXISTS FOR (t:EMB3D_Threat) ON (t.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (m:EMB3D_Mitigation) ON (m.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (p:EMB3D_Property) ON (p.id)")

        # Categorize objects
        threats = [o for o in objects if o.get('type') == 'attack-pattern']
        mitigations = [o for o in objects if o.get('type') == 'course-of-action']
        properties = [o for o in objects if o.get('type') == 'x-emb3d-property']
        relationships = [o for o in objects if o.get('type') == 'relationship']

        print(f"Found: {len(threats)} threats, {len(mitigations)} mitigations, {len(properties)} properties")

        with self.driver.session() as session:
            # Load threats
            for threat in threats:
                stix_id = threat.get('id', '')
                name = threat.get('name', '')
                description = threat.get('description', '')

                # Extract EMB3D ID from external references
                emb3d_id = stix_id
                for ref in threat.get('external_references', []):
                    if ref.get('source_name') == 'EMB3D':
                        emb3d_id = ref.get('external_id', stix_id)
                        break

                session.run("""
                    MERGE (t:EMB3D_Threat {id: $id})
                    SET t.stix_id = $stix_id,
                        t.name = $name,
                        t.description = $desc,
                        t.taxonomy = 'EMB3D',
                        t.updated_at = timestamp()
                """, id=emb3d_id, stix_id=stix_id, name=name, desc=description[:2000])
                self.stats["emb3d"]["nodes"] += 1

                self._store_embedding(f"{name}. {description}", "EMB3D_Threat", emb3d_id)

            # Load mitigations
            for mitigation in mitigations:
                stix_id = mitigation.get('id', '')
                name = mitigation.get('name', '')
                description = mitigation.get('description', '')

                emb3d_id = stix_id
                for ref in mitigation.get('external_references', []):
                    if ref.get('source_name') == 'EMB3D':
                        emb3d_id = ref.get('external_id', stix_id)
                        break

                session.run("""
                    MERGE (m:EMB3D_Mitigation {id: $id})
                    SET m.stix_id = $stix_id,
                        m.name = $name,
                        m.description = $desc,
                        m.taxonomy = 'EMB3D',
                        m.updated_at = timestamp()
                """, id=emb3d_id, stix_id=stix_id, name=name, desc=description[:2000])
                self.stats["emb3d"]["nodes"] += 1

            # Load properties
            for prop in properties:
                stix_id = prop.get('id', '')
                name = prop.get('name', '')
                description = prop.get('description', '')

                session.run("""
                    MERGE (p:EMB3D_Property {id: $id})
                    SET p.name = $name,
                        p.description = $desc,
                        p.taxonomy = 'EMB3D',
                        p.updated_at = timestamp()
                """, id=stix_id, name=name, desc=description[:2000])
                self.stats["emb3d"]["nodes"] += 1

            # Create relationships
            for rel in relationships:
                source = rel.get('source_ref', '')
                target = rel.get('target_ref', '')
                rel_type = rel.get('relationship_type', 'related-to')

                # Map relationship type to Neo4j
                neo4j_rel = 'RELATED_TO'
                if rel_type == 'mitigates':
                    neo4j_rel = 'MITIGATES'
                elif rel_type == 'uses':
                    neo4j_rel = 'USES'
                elif rel_type == 'targets':
                    neo4j_rel = 'TARGETS'

                session.run(f"""
                    MATCH (s) WHERE s.stix_id = $source OR s.id = $source
                    MATCH (t) WHERE t.stix_id = $target OR t.id = $target
                    MERGE (s)-[:{neo4j_rel}]->(t)
                """, source=source, target=target)
                self.stats["emb3d"]["relationships"] += 1

        print(f"EMB3D: {self.stats['emb3d']['nodes']} nodes, {self.stats['emb3d']['relationships']} relationships")
        return self.stats["emb3d"]

    # ============== MITRE ATT&CK LOADER ==============
    def load_mitre_attack(self, domain: str = "enterprise", force: bool = False) -> Dict:
        """Load MITRE ATT&CK data from STIX JSON."""
        domain_map = {
            "enterprise": ("enterprise-attack.json", "attack_enterprise"),
            "mobile": ("mobile-attack.json", "attack_mobile"),
            "ics": ("ics-attack.json", "attack_ics")
        }

        if domain not in domain_map:
            print(f"Unknown ATT&CK domain: {domain}")
            return {}

        filename, stat_key = domain_map[domain]
        attack_file = BASE_PATH / filename

        if not attack_file.exists():
            print(f"ATT&CK file not found: {attack_file}")
            return self.stats[stat_key]

        print(f"\n{'='*60}")
        print(f"LOADING MITRE ATT&CK {domain.upper()}")
        print(f"{'='*60}")

        with open(attack_file, 'r') as f:
            data = json.load(f)

        objects = data.get('objects', [])

        # Create indexes
        with self.driver.session() as session:
            session.run("CREATE INDEX IF NOT EXISTS FOR (t:ATTACK_Technique) ON (t.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (t:ATTACK_Tactic) ON (t.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (g:ATTACK_Group) ON (g.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (s:ATTACK_Software) ON (s.id)")

        techniques = [o for o in objects if o.get('type') == 'attack-pattern']
        tactics = [o for o in objects if o.get('type') == 'x-mitre-tactic']
        groups = [o for o in objects if o.get('type') == 'intrusion-set']
        software = [o for o in objects if o.get('type') == 'malware' or o.get('type') == 'tool']
        relationships = [o for o in objects if o.get('type') == 'relationship']

        print(f"Found: {len(techniques)} techniques, {len(tactics)} tactics, {len(groups)} groups")

        with self.driver.session() as session:
            # Load tactics
            for tactic in tactics:
                stix_id = tactic.get('id', '')
                name = tactic.get('name', '')
                description = tactic.get('description', '')
                shortname = tactic.get('x_mitre_shortname', '')

                attack_id = ''
                for ref in tactic.get('external_references', []):
                    if ref.get('source_name') == 'mitre-attack':
                        attack_id = ref.get('external_id', '')
                        break

                session.run("""
                    MERGE (t:ATTACK_Tactic {id: $id})
                    SET t.stix_id = $stix_id,
                        t.name = $name,
                        t.shortname = $shortname,
                        t.description = $desc,
                        t.domain = $domain,
                        t.taxonomy = 'MITRE_ATTACK',
                        t.updated_at = timestamp()
                """, id=attack_id or stix_id, stix_id=stix_id, name=name,
                    shortname=shortname, desc=description[:2000], domain=domain)
                self.stats[stat_key]["nodes"] += 1

            # Load techniques
            for technique in techniques:
                stix_id = technique.get('id', '')
                name = technique.get('name', '')
                description = technique.get('description', '')

                # Check for revoked/deprecated
                if technique.get('revoked') or technique.get('x_mitre_deprecated'):
                    continue

                attack_id = ''
                for ref in technique.get('external_references', []):
                    if ref.get('source_name') == 'mitre-attack':
                        attack_id = ref.get('external_id', '')
                        break

                # Get kill chain phases (tactics)
                kill_chain = technique.get('kill_chain_phases', [])
                phase_names = [p.get('phase_name', '') for p in kill_chain]

                # Determine if sub-technique
                is_subtechnique = technique.get('x_mitre_is_subtechnique', False)

                session.run("""
                    MERGE (t:ATTACK_Technique {id: $id})
                    SET t.stix_id = $stix_id,
                        t.name = $name,
                        t.description = $desc,
                        t.domain = $domain,
                        t.is_subtechnique = $is_sub,
                        t.tactics = $tactics,
                        t.taxonomy = 'MITRE_ATTACK',
                        t.updated_at = timestamp()
                """, id=attack_id or stix_id, stix_id=stix_id, name=name,
                    desc=description[:2000], domain=domain, is_sub=is_subtechnique,
                    tactics=phase_names)
                self.stats[stat_key]["nodes"] += 1

                self._store_embedding(f"{attack_id} {name}. {description}", "ATTACK_Technique", attack_id or stix_id)

                # Link to tactics
                for phase in phase_names:
                    session.run("""
                        MATCH (tech:ATTACK_Technique {id: $tech_id})
                        MATCH (tac:ATTACK_Tactic) WHERE tac.shortname = $phase
                        MERGE (tech)-[:USES_TACTIC]->(tac)
                    """, tech_id=attack_id or stix_id, phase=phase)
                    self.stats[stat_key]["relationships"] += 1

            # Load groups
            for group in groups:
                stix_id = group.get('id', '')
                name = group.get('name', '')
                description = group.get('description', '')
                aliases = group.get('aliases', [])

                attack_id = ''
                for ref in group.get('external_references', []):
                    if ref.get('source_name') == 'mitre-attack':
                        attack_id = ref.get('external_id', '')
                        break

                session.run("""
                    MERGE (g:ATTACK_Group {id: $id})
                    SET g.stix_id = $stix_id,
                        g.name = $name,
                        g.description = $desc,
                        g.aliases = $aliases,
                        g.domain = $domain,
                        g.taxonomy = 'MITRE_ATTACK',
                        g.updated_at = timestamp()
                """, id=attack_id or stix_id, stix_id=stix_id, name=name,
                    desc=description[:2000], aliases=aliases, domain=domain)
                self.stats[stat_key]["nodes"] += 1

            # Process relationships
            for rel in relationships:
                source = rel.get('source_ref', '')
                target = rel.get('target_ref', '')
                rel_type = rel.get('relationship_type', '')

                if rel_type == 'uses':
                    session.run("""
                        MATCH (s) WHERE s.stix_id = $source
                        MATCH (t) WHERE t.stix_id = $target
                        MERGE (s)-[:USES]->(t)
                    """, source=source, target=target)
                    self.stats[stat_key]["relationships"] += 1
                elif rel_type == 'subtechnique-of':
                    session.run("""
                        MATCH (child:ATTACK_Technique) WHERE child.stix_id = $source
                        MATCH (parent:ATTACK_Technique) WHERE parent.stix_id = $target
                        MERGE (child)-[:SUBTECHNIQUE_OF]->(parent)
                    """, source=source, target=target)
                    self.stats[stat_key]["relationships"] += 1
                elif rel_type == 'mitigates':
                    session.run("""
                        MATCH (m) WHERE m.stix_id = $source
                        MATCH (t:ATTACK_Technique) WHERE t.stix_id = $target
                        MERGE (m)-[:MITIGATES]->(t)
                    """, source=source, target=target)
                    self.stats[stat_key]["relationships"] += 1

        print(f"ATT&CK {domain}: {self.stats[stat_key]['nodes']} nodes, {self.stats[stat_key]['relationships']} relationships")
        return self.stats[stat_key]

    # ============== VULNCHECK KEV LOADER ==============
    def load_vulncheck(self, force: bool = False) -> Dict:
        """Load VulnCheck Known Exploited Vulnerabilities."""
        kev_file = BASE_PATH / "vulncheck-kev.json"
        if not kev_file.exists():
            print(f"VulnCheck file not found: {kev_file}")
            return self.stats["vulncheck"]

        print(f"\n{'='*60}")
        print("LOADING VULNCHECK KEV")
        print(f"{'='*60}")

        with open(kev_file, 'r') as f:
            data = json.load(f)

        print(f"Found {len(data)} KEV entries")

        # Create indexes
        with self.driver.session() as session:
            session.run("CREATE INDEX IF NOT EXISTS FOR (k:VulnCheck_KEV) ON (k.cve)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:CVE) ON (c.id)")

        with self.driver.session() as session:
            for entry in data:
                cves = entry.get('cve', [])
                vendor = entry.get('vendorProject', '')
                product = entry.get('product', '')
                vuln_name = entry.get('vulnerabilityName', '')
                description = entry.get('shortDescription', '')
                ransomware = entry.get('knownRansomwareCampaignUse', 'Unknown')
                required_action = entry.get('required_action', '')
                cwes = entry.get('cwes', [])

                for cve_id in cves:
                    # Create KEV entry
                    session.run("""
                        MERGE (k:VulnCheck_KEV {cve: $cve})
                        SET k.vendor = $vendor,
                            k.product = $product,
                            k.vulnerability_name = $vuln_name,
                            k.description = $desc,
                            k.ransomware_use = $ransomware,
                            k.required_action = $action,
                            k.taxonomy = 'VulnCheck',
                            k.updated_at = timestamp()
                    """, cve=cve_id, vendor=vendor, product=product,
                        vuln_name=vuln_name, desc=description[:2000],
                        ransomware=ransomware, action=required_action[:500])
                    self.stats["vulncheck"]["nodes"] += 1

                    # Create CVE node and link
                    session.run("""
                        MERGE (c:CVE {id: $cve})
                        SET c.is_kev = true,
                            c.kev_vendor = $vendor,
                            c.kev_product = $product
                        WITH c
                        MATCH (k:VulnCheck_KEV {cve: $cve})
                        MERGE (c)-[:IN_KEV]->(k)
                    """, cve=cve_id, vendor=vendor, product=product)
                    self.stats["vulncheck"]["relationships"] += 1

                    # Link to CWEs
                    for cwe_id in cwes:
                        if cwe_id:
                            session.run("""
                                MATCH (c:CVE {id: $cve})
                                MERGE (w:CWE {id: $cwe})
                                MERGE (c)-[:HAS_WEAKNESS]->(w)
                            """, cve=cve_id, cwe=cwe_id)
                            self.stats["cross_links"] += 1

        print(f"VulnCheck: {self.stats['vulncheck']['nodes']} nodes, {self.stats['vulncheck']['relationships']} relationships")
        return self.stats["vulncheck"]

    # ============== EPSS LOADER ==============
    def load_epss(self, force: bool = False) -> Dict:
        """Load EPSS exploitability scores."""
        epss_file = BASE_PATH / "epss_scores-2025-12-02.csv"
        if not epss_file.exists():
            print(f"EPSS file not found: {epss_file}")
            return self.stats["epss"]

        print(f"\n{'='*60}")
        print("LOADING EPSS SCORES")
        print(f"{'='*60}")

        # Create indexes
        with self.driver.session() as session:
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:CVE) ON (c.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (e:EPSS) ON (e.cve)")

        # Count lines first
        with open(epss_file, 'r') as f:
            total_lines = sum(1 for _ in f) - 2  # Subtract header lines

        print(f"Processing {total_lines:,} EPSS scores...")

        batch_size = 5000
        batch = []
        count = 0

        with open(epss_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip model version line
            next(reader)  # Skip header

            for row in reader:
                if len(row) >= 3:
                    cve_id = row[0]
                    epss_score = float(row[1])
                    percentile = float(row[2])

                    batch.append({
                        'cve': cve_id,
                        'epss': epss_score,
                        'percentile': percentile
                    })

                    if len(batch) >= batch_size:
                        self._process_epss_batch(batch)
                        count += len(batch)
                        if count % 50000 == 0:
                            print(f"   Processed {count:,}/{total_lines:,} ({100*count/total_lines:.1f}%)")
                        batch = []

            # Process remaining
            if batch:
                self._process_epss_batch(batch)
                count += len(batch)

        self.stats["epss"]["nodes"] = count
        print(f"EPSS: {self.stats['epss']['nodes']:,} scores loaded")
        return self.stats["epss"]

    def _process_epss_batch(self, batch: List[Dict]):
        """Process a batch of EPSS scores."""
        with self.driver.session() as session:
            session.run("""
                UNWIND $batch AS row
                MERGE (c:CVE {id: row.cve})
                SET c.epss_score = row.epss,
                    c.epss_percentile = row.percentile,
                    c.epss_date = '2025-12-02',
                    c.updated_at = timestamp()
            """, batch=batch)

    # ============== CROSS-TAXONOMY LINKS ==============
    def create_cross_taxonomy_links(self) -> Dict:
        """Create relationships between different taxonomies."""
        print(f"\n{'='*60}")
        print("CREATING CROSS-TAXONOMY RELATIONSHIPS")
        print(f"{'='*60}")

        with self.driver.session() as session:
            # CAPEC → ATT&CK via name similarity
            result = session.run("""
                MATCH (c:CAPEC)
                MATCH (t:ATTACK_Technique)
                WHERE toLower(c.name) CONTAINS toLower(t.name)
                   OR toLower(t.name) CONTAINS toLower(c.name)
                MERGE (c)-[:MAPPED_TO {method: 'name_similarity'}]->(t)
                RETURN count(*) as count
            """)
            capec_attack = result.single()["count"]
            print(f"   CAPEC → ATT&CK: {capec_attack} mappings")
            self.stats["cross_links"] += capec_attack

            # EMB3D → ATT&CK ICS
            result = session.run("""
                MATCH (e:EMB3D_Threat)
                MATCH (t:ATTACK_Technique {domain: 'ics'})
                WHERE toLower(e.name) CONTAINS toLower(t.name)
                   OR toLower(t.name) CONTAINS toLower(e.name)
                MERGE (e)-[:MAPPED_TO {method: 'name_similarity'}]->(t)
                RETURN count(*) as count
            """)
            emb3d_ics = result.single()["count"]
            print(f"   EMB3D → ATT&CK ICS: {emb3d_ics} mappings")
            self.stats["cross_links"] += emb3d_ics

            # Link high-EPSS CVEs to KEV
            result = session.run("""
                MATCH (c:CVE)
                WHERE c.epss_score > 0.5 AND c.is_kev IS NULL
                SET c.high_epss = true
                RETURN count(*) as count
            """)
            high_epss = result.single()["count"]
            print(f"   High-EPSS CVEs flagged: {high_epss}")

        return {"cross_links": self.stats["cross_links"]}

    # ============== VERIFICATION ==============
    def verify_schema(self) -> Dict:
        """Verify schema integrity."""
        print(f"\n{'='*60}")
        print("SCHEMA VERIFICATION")
        print(f"{'='*60}")

        with self.driver.session() as session:
            # Count nodes by label (filter out labels with dots to avoid syntax errors)
            result = session.run("""
                CALL db.labels() YIELD label
                WHERE NOT label CONTAINS "."
                CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN count(n) as count', {})
                    YIELD value
                RETURN label, value.count as count
                ORDER BY value.count DESC
            """)

            print("\nNode counts by label:")
            for record in result:
                print(f"   {record['label']}: {record['count']:,}")

            # Count relationships (filter out relationship types with dots)
            result = session.run("""
                CALL db.relationshipTypes() YIELD relationshipType
                WHERE NOT relationshipType CONTAINS "."
                CALL apoc.cypher.run('MATCH ()-[r:' + relationshipType + ']->() RETURN count(r) as count', {})
                    YIELD value
                RETURN relationshipType, value.count as count
                ORDER BY value.count DESC
                LIMIT 20
            """)

            print("\nRelationship counts:")
            for record in result:
                print(f"   {record['relationshipType']}: {record['count']:,}")

            # Check hierarchical integrity
            result = session.run("""
                MATCH (c:CAPEC)-[:CHILD_OF*]->(root:CAPEC)
                WHERE NOT (root)-[:CHILD_OF]->()
                RETURN count(DISTINCT c) as hierarchical_capec
            """)
            hierarchical = result.single()
            print(f"\nHierarchical CAPEC nodes: {hierarchical['hierarchical_capec']:,}")

        return {"verified": True}

    def _get_text_content(self, elem) -> str:
        """Extract text content from XML element, handling nested elements."""
        if elem is None:
            return ''
        text_parts = []
        if elem.text:
            text_parts.append(elem.text)
        for child in elem:
            if child.text:
                text_parts.append(child.text)
            if child.tail:
                text_parts.append(child.tail)
        return ' '.join(text_parts).strip()

    def print_summary(self):
        """Print loading summary."""
        print(f"\n{'='*60}")
        print("COMPREHENSIVE TAXONOMY LOADING SUMMARY")
        print(f"{'='*60}")

        total_nodes = 0
        total_rels = 0

        for source, data in self.stats.items():
            if isinstance(data, dict) and 'nodes' in data:
                print(f"{source.upper()}: {data['nodes']:,} nodes, {data['relationships']:,} relationships")
                total_nodes += data['nodes']
                total_rels += data['relationships']

        print(f"\nCross-taxonomy links: {self.stats['cross_links']:,}")
        print(f"Embeddings stored: {self.stats['embeddings']:,}")
        print(f"\nTOTAL: {total_nodes:,} nodes, {total_rels:,} relationships")


def main():
    parser = argparse.ArgumentParser(description="Comprehensive Taxonomy Loader")
    parser.add_argument("--all", action="store_true", help="Load all taxonomies")
    parser.add_argument("--capec", action="store_true", help="Load CAPEC")
    parser.add_argument("--cwe", action="store_true", help="Load CWE")
    parser.add_argument("--emb3d", action="store_true", help="Load EMB3D")
    parser.add_argument("--mitre", action="store_true", help="Load all MITRE ATT&CK")
    parser.add_argument("--enterprise", action="store_true", help="Load ATT&CK Enterprise")
    parser.add_argument("--mobile", action="store_true", help="Load ATT&CK Mobile")
    parser.add_argument("--ics", action="store_true", help="Load ATT&CK ICS")
    parser.add_argument("--vulncheck", action="store_true", help="Load VulnCheck KEV")
    parser.add_argument("--epss", action="store_true", help="Load EPSS scores")
    parser.add_argument("--cross-links", action="store_true", help="Create cross-taxonomy links")
    parser.add_argument("--verify", action="store_true", help="Verify schema")
    parser.add_argument("--force", action="store_true", help="Force reload")
    parser.add_argument("--skip-embeddings", action="store_true", help="Skip Qdrant embeddings")

    args = parser.parse_args()

    # If no args specified, show help
    if not any([args.all, args.capec, args.cwe, args.emb3d, args.mitre,
                args.enterprise, args.mobile, args.ics, args.vulncheck,
                args.epss, args.cross_links, args.verify]):
        parser.print_help()
        return

    print("="*60)
    print("COMPREHENSIVE TAXONOMY LOADER FOR AEON CYBER DIGITAL TWIN")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*60)

    loader = ComprehensiveTaxonomyLoader(
        NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD,
        skip_embeddings=args.skip_embeddings
    )

    try:
        if args.all or args.capec:
            loader.load_capec(args.force)

        if args.all or args.cwe:
            loader.load_cwe(args.force)

        if args.all or args.emb3d:
            loader.load_emb3d(args.force)

        if args.all or args.mitre or args.enterprise:
            loader.load_mitre_attack("enterprise", args.force)

        if args.all or args.mitre or args.mobile:
            loader.load_mitre_attack("mobile", args.force)

        if args.all or args.mitre or args.ics:
            loader.load_mitre_attack("ics", args.force)

        if args.all or args.vulncheck:
            loader.load_vulncheck(args.force)

        if args.all or args.epss:
            loader.load_epss(args.force)

        if args.all or args.cross_links:
            loader.create_cross_taxonomy_links()

        if args.all or args.verify:
            loader.verify_schema()

        loader.print_summary()

    finally:
        loader.close()

    print(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
