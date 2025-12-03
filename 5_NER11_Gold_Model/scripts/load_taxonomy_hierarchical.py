#!/usr/bin/env python3
"""
Hierarchical Taxonomy Loader for CAPEC, CWE, and EMB3D

Loads security taxonomies into Neo4j with proper hierarchical schema and
stores embeddings in Qdrant for semantic search.

Usage:
    python3 scripts/load_taxonomy_hierarchical.py --all
    python3 scripts/load_taxonomy_hierarchical.py --capec --cwe
    python3 scripts/load_taxonomy_hierarchical.py --emb3d --force

Author: NER11 Gold Model Team
Date: 2025-12-02
"""

import sys
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
TAXONOMY_COLLECTION = "taxonomy_embeddings"

# File paths
BASE_PATH = Path(__file__).parent.parent / "training_data/custom_data/source_files"
CAPEC_PATH = BASE_PATH / "Vulnerabilities/capec_latest/capec_v3.9.xml"
CWE_PATH = BASE_PATH / "Vulnerabilities/cwec_latest.xml/cwec_v4.18.xml"
EMB3D_PATH = BASE_PATH / "Vulnerabilities/emb3d-stix-2.0.1.json"

# Alternative EMB3D path
EMB3D_ALT_PATH = BASE_PATH / "EMB3D Technique/emb3d-stix-2.0.1.json"

# XML Namespaces
CAPEC_NS = {'capec': 'http://capec.mitre.org/capec-3'}
CWE_NS = {'cwe': 'http://cwe.mitre.org/cwe-7'}


class TaxonomyLoader:
    """Loads security taxonomies with hierarchical relationships."""

    def __init__(self, force_reload: bool = False):
        """Initialize connections."""
        self.force_reload = force_reload

        # Neo4j connection
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
        print(f"✅ Connected to Neo4j at {NEO4J_URI}")

        # Qdrant connection
        self.qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        self._ensure_qdrant_collection()
        print(f"✅ Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")

        # Embedding model
        print("📦 Loading embedding model...")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        # Statistics
        self.stats = {
            "capec_nodes": 0,
            "capec_relationships": 0,
            "cwe_nodes": 0,
            "cwe_relationships": 0,
            "emb3d_nodes": 0,
            "emb3d_relationships": 0,
            "cross_taxonomy": 0,
            "embeddings": 0
        }

    def _ensure_qdrant_collection(self):
        """Ensure Qdrant collection exists."""
        collections = [c.name for c in self.qdrant.get_collections().collections]
        if TAXONOMY_COLLECTION not in collections:
            self.qdrant.create_collection(
                collection_name=TAXONOMY_COLLECTION,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"   Created Qdrant collection: {TAXONOMY_COLLECTION}")

    def close(self):
        """Close connections."""
        self.driver.close()

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        return self.embedding_model.encode(text).tolist()

    def _store_embedding(self, node_id: str, node_type: str, text: str, metadata: Dict):
        """Store embedding in Qdrant."""
        try:
            embedding = self._generate_embedding(text)
            point_id = hash(f"{node_type}_{node_id}") % (2**63)

            self.qdrant.upsert(
                collection_name=TAXONOMY_COLLECTION,
                points=[PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "node_id": node_id,
                        "node_type": node_type,
                        "text": text[:500],  # Truncate for storage
                        **metadata,
                        "created_at": datetime.utcnow().isoformat()
                    }
                )]
            )
            self.stats["embeddings"] += 1
        except Exception as e:
            pass  # Silent fail for embeddings

    # =========================================================================
    # CAPEC LOADING
    # =========================================================================

    def load_capec(self) -> Dict:
        """Load CAPEC attack patterns with hierarchical relationships."""
        print("\n" + "="*60)
        print("📦 LOADING CAPEC (Attack Patterns)")
        print("="*60)

        if not CAPEC_PATH.exists():
            print(f"❌ CAPEC file not found: {CAPEC_PATH}")
            return {"error": "file_not_found"}

        tree = ET.parse(CAPEC_PATH)
        root = tree.getroot()

        with self.driver.session() as session:
            # Clear existing if force reload
            if self.force_reload:
                session.run("MATCH (n:CAPEC) DETACH DELETE n")
                session.run("MATCH (n:CAPECCategory) DETACH DELETE n")
                print("   🗑️  Cleared existing CAPEC nodes")

            # Create indexes
            session.run("CREATE INDEX capec_id IF NOT EXISTS FOR (c:CAPEC) ON (c.id)")
            session.run("CREATE INDEX capec_cat_id IF NOT EXISTS FOR (c:CAPECCategory) ON (c.id)")

            # Load Attack Patterns
            patterns = root.findall('.//capec:Attack_Pattern', CAPEC_NS)
            print(f"   Processing {len(patterns)} attack patterns...")

            for pattern in patterns:
                capec_id = f"CAPEC-{pattern.get('ID')}"
                name = pattern.get('Name', '')
                status = pattern.get('Status', '')

                # Get description
                desc_elem = pattern.find('capec:Description', CAPEC_NS)
                description = desc_elem.text if desc_elem is not None and desc_elem.text else ""

                # Get severity/likelihood
                likelihood = pattern.find('.//capec:Likelihood_Of_Attack', CAPEC_NS)
                likelihood_val = likelihood.text if likelihood is not None else None

                severity = pattern.find('.//capec:Typical_Severity', CAPEC_NS)
                severity_val = severity.text if severity is not None else None

                # Create CAPEC node
                session.run("""
                    MERGE (c:CAPEC {id: $id})
                    SET c.name = $name,
                        c.description = $description,
                        c.status = $status,
                        c.likelihood = $likelihood,
                        c.severity = $severity,
                        c.source = 'MITRE',
                        c.version = '3.9',
                        c.updated_at = timestamp()
                """, id=capec_id, name=name, description=description[:2000],
                    status=status, likelihood=likelihood_val, severity=severity_val)
                self.stats["capec_nodes"] += 1

                # Store embedding
                embed_text = f"{capec_id} {name} {description[:500]}"
                self._store_embedding(capec_id, "CAPEC", embed_text, {
                    "name": name,
                    "severity": severity_val or "Unknown"
                })

                # Link to CWEs
                weaknesses = pattern.findall('.//capec:Related_Weakness', CAPEC_NS)
                for weakness in weaknesses:
                    cwe_id = f"CWE-{weakness.get('CWE_ID')}"
                    session.run("""
                        MATCH (c:CAPEC {id: $capec_id})
                        MERGE (w:CWE {id: $cwe_id})
                        MERGE (c)-[r:EXPLOITS]->(w)
                        SET r.source = 'CAPEC'
                    """, capec_id=capec_id, cwe_id=cwe_id)
                    self.stats["cross_taxonomy"] += 1

                # Create hierarchical relationships
                related = pattern.findall('.//capec:Related_Attack_Pattern', CAPEC_NS)
                for rel in related:
                    rel_id = f"CAPEC-{rel.get('CAPEC_ID')}"
                    nature = rel.get('Nature', 'RelatedTo')

                    if nature == 'ChildOf':
                        session.run("""
                            MATCH (child:CAPEC {id: $child_id})
                            MERGE (parent:CAPEC {id: $parent_id})
                            MERGE (child)-[r:CHILD_OF]->(parent)
                        """, child_id=capec_id, parent_id=rel_id)
                    elif nature == 'ParentOf':
                        session.run("""
                            MATCH (parent:CAPEC {id: $parent_id})
                            MERGE (child:CAPEC {id: $child_id})
                            MERGE (child)-[r:CHILD_OF]->(parent)
                        """, parent_id=capec_id, child_id=rel_id)
                    else:
                        session.run("""
                            MATCH (c1:CAPEC {id: $id1})
                            MERGE (c2:CAPEC {id: $id2})
                            MERGE (c1)-[r:RELATED_TO {nature: $nature}]->(c2)
                        """, id1=capec_id, id2=rel_id, nature=nature)
                    self.stats["capec_relationships"] += 1

            # Load Categories
            categories = root.findall('.//capec:Category', CAPEC_NS)
            print(f"   Processing {len(categories)} categories...")

            for cat in categories:
                cat_id = f"CAPEC-CAT-{cat.get('ID')}"
                name = cat.get('Name', '')

                session.run("""
                    MERGE (c:CAPECCategory {id: $id})
                    SET c.name = $name,
                        c.source = 'MITRE',
                        c.updated_at = timestamp()
                """, id=cat_id, name=name)
                self.stats["capec_nodes"] += 1

                # Link patterns to categories
                members = cat.findall('.//capec:Has_Member', CAPEC_NS)
                for member in members:
                    member_id = f"CAPEC-{member.get('CAPEC_ID')}"
                    session.run("""
                        MATCH (c:CAPECCategory {id: $cat_id})
                        MATCH (p:CAPEC {id: $pattern_id})
                        MERGE (p)-[r:BELONGS_TO]->(c)
                    """, cat_id=cat_id, pattern_id=member_id)
                    self.stats["capec_relationships"] += 1

        print(f"   ✅ CAPEC loaded: {self.stats['capec_nodes']} nodes, {self.stats['capec_relationships']} relationships")
        return {"nodes": self.stats['capec_nodes'], "relationships": self.stats['capec_relationships']}

    # =========================================================================
    # CWE LOADING
    # =========================================================================

    def load_cwe(self) -> Dict:
        """Load CWE weaknesses with hierarchical relationships."""
        print("\n" + "="*60)
        print("📦 LOADING CWE (Weaknesses)")
        print("="*60)

        if not CWE_PATH.exists():
            print(f"❌ CWE file not found: {CWE_PATH}")
            return {"error": "file_not_found"}

        tree = ET.parse(CWE_PATH)
        root = tree.getroot()

        with self.driver.session() as session:
            # Clear existing if force reload
            if self.force_reload:
                session.run("MATCH (n:CWE) DETACH DELETE n")
                session.run("MATCH (n:CWECategory) DETACH DELETE n")
                print("   🗑️  Cleared existing CWE nodes")

            # Create indexes
            session.run("CREATE INDEX cwe_id IF NOT EXISTS FOR (c:CWE) ON (c.id)")
            session.run("CREATE INDEX cwe_cat_id IF NOT EXISTS FOR (c:CWECategory) ON (c.id)")

            # Load Weaknesses
            weaknesses = root.findall('.//cwe:Weakness', CWE_NS)
            print(f"   Processing {len(weaknesses)} weaknesses...")

            for weakness in weaknesses:
                cwe_id = f"CWE-{weakness.get('ID')}"
                name = weakness.get('Name', '')
                abstraction = weakness.get('Abstraction', '')
                status = weakness.get('Status', '')

                # Get description
                desc_elem = weakness.find('.//cwe:Description', CWE_NS)
                description = desc_elem.text if desc_elem is not None and desc_elem.text else ""

                # Get extended description
                ext_desc = weakness.find('.//cwe:Extended_Description', CWE_NS)
                extended = ""
                if ext_desc is not None:
                    # May contain nested XML
                    extended = ET.tostring(ext_desc, encoding='unicode', method='text')[:500]

                # Create CWE node
                session.run("""
                    MERGE (c:CWE {id: $id})
                    SET c.name = $name,
                        c.description = $description,
                        c.extended_description = $extended,
                        c.abstraction = $abstraction,
                        c.status = $status,
                        c.source = 'MITRE',
                        c.version = '4.18',
                        c.updated_at = timestamp()
                """, id=cwe_id, name=name, description=description[:2000],
                    extended=extended, abstraction=abstraction, status=status)
                self.stats["cwe_nodes"] += 1

                # Store embedding
                embed_text = f"{cwe_id} {name} {description[:500]}"
                self._store_embedding(cwe_id, "CWE", embed_text, {
                    "name": name,
                    "abstraction": abstraction
                })

                # Link to CAPECs
                capec_refs = weakness.findall('.//cwe:Related_Attack_Pattern', CWE_NS)
                for ref in capec_refs:
                    capec_id = f"CAPEC-{ref.get('CAPEC_ID')}"
                    session.run("""
                        MATCH (w:CWE {id: $cwe_id})
                        MERGE (c:CAPEC {id: $capec_id})
                        MERGE (c)-[r:EXPLOITS]->(w)
                        SET r.source = 'CWE'
                    """, cwe_id=cwe_id, capec_id=capec_id)
                    self.stats["cross_taxonomy"] += 1

                # Create hierarchical relationships
                related = weakness.findall('.//cwe:Related_Weakness', CWE_NS)
                for rel in related:
                    rel_id = f"CWE-{rel.get('CWE_ID')}"
                    nature = rel.get('Nature', 'RelatedTo')

                    if nature == 'ChildOf':
                        session.run("""
                            MATCH (child:CWE {id: $child_id})
                            MERGE (parent:CWE {id: $parent_id})
                            MERGE (child)-[r:CHILD_OF]->(parent)
                        """, child_id=cwe_id, parent_id=rel_id)
                    elif nature == 'ParentOf':
                        session.run("""
                            MATCH (parent:CWE {id: $parent_id})
                            MERGE (child:CWE {id: $child_id})
                            MERGE (child)-[r:CHILD_OF]->(parent)
                        """, parent_id=cwe_id, child_id=rel_id)
                    elif nature in ('PeerOf', 'CanPrecede', 'CanFollow', 'Requires', 'CanAlsoBe'):
                        session.run("""
                            MATCH (w1:CWE {id: $id1})
                            MERGE (w2:CWE {id: $id2})
                            MERGE (w1)-[r:RELATED_TO {nature: $nature}]->(w2)
                        """, id1=cwe_id, id2=rel_id, nature=nature)
                    self.stats["cwe_relationships"] += 1

            # Load Categories
            categories = root.findall('.//cwe:Category', CWE_NS)
            print(f"   Processing {len(categories)} categories...")

            for cat in categories:
                cat_id = f"CWE-CAT-{cat.get('ID')}"
                name = cat.get('Name', '')

                session.run("""
                    MERGE (c:CWECategory {id: $id})
                    SET c.name = $name,
                        c.source = 'MITRE',
                        c.updated_at = timestamp()
                """, id=cat_id, name=name)
                self.stats["cwe_nodes"] += 1

                # Link weaknesses to categories
                members = cat.findall('.//cwe:Has_Member', CWE_NS)
                for member in members:
                    member_id = f"CWE-{member.get('CWE_ID')}"
                    session.run("""
                        MATCH (c:CWECategory {id: $cat_id})
                        MATCH (w:CWE {id: $weakness_id})
                        MERGE (w)-[r:BELONGS_TO]->(c)
                    """, cat_id=cat_id, weakness_id=member_id)
                    self.stats["cwe_relationships"] += 1

        print(f"   ✅ CWE loaded: {self.stats['cwe_nodes']} nodes, {self.stats['cwe_relationships']} relationships")
        return {"nodes": self.stats['cwe_nodes'], "relationships": self.stats['cwe_relationships']}

    # =========================================================================
    # EMB3D LOADING
    # =========================================================================

    def load_emb3d(self) -> Dict:
        """Load EMB3D embedded threats from STIX format."""
        print("\n" + "="*60)
        print("📦 LOADING EMB3D (Embedded Device Threats)")
        print("="*60)

        # Try primary path, then alternate
        emb3d_path = EMB3D_PATH if EMB3D_PATH.exists() else EMB3D_ALT_PATH

        if not emb3d_path.exists():
            print(f"❌ EMB3D file not found: {emb3d_path}")
            return {"error": "file_not_found"}

        print(f"   Loading from: {emb3d_path}")

        with open(emb3d_path, 'r') as f:
            stix_bundle = json.load(f)

        objects = stix_bundle.get('objects', [])
        print(f"   Found {len(objects)} STIX objects")

        with self.driver.session() as session:
            # Clear existing if force reload
            if self.force_reload:
                session.run("MATCH (n:EMB3D) DETACH DELETE n")
                session.run("MATCH (n:EMB3DMitigation) DETACH DELETE n")
                session.run("MATCH (n:EMB3DProperty) DETACH DELETE n")
                print("   🗑️  Cleared existing EMB3D nodes")

            # Create indexes
            session.run("CREATE INDEX emb3d_id IF NOT EXISTS FOR (e:EMB3D) ON (e.id)")
            session.run("CREATE INDEX emb3d_stix_id IF NOT EXISTS FOR (e:EMB3D) ON (e.stix_id)")

            # Process objects by type
            id_map = {}  # STIX ID to simple ID mapping

            for obj in objects:
                obj_type = obj.get('type', '')
                stix_id = obj.get('id', '')
                name = obj.get('name', '')
                description = obj.get('description', '')

                if obj_type == 'vulnerability':
                    # EMB3D Threat/Vulnerability
                    emb3d_id = obj.get('external_references', [{}])[0].get('external_id', stix_id)
                    id_map[stix_id] = emb3d_id

                    session.run("""
                        MERGE (e:EMB3D {id: $id})
                        SET e.stix_id = $stix_id,
                            e.name = $name,
                            e.description = $description,
                            e.type = 'threat',
                            e.source = 'EMB3D',
                            e.version = '2.0.1',
                            e.updated_at = timestamp()
                    """, id=emb3d_id, stix_id=stix_id, name=name, description=description[:2000])
                    self.stats["emb3d_nodes"] += 1

                    # Store embedding
                    embed_text = f"EMB3D {emb3d_id} {name} {description[:500]}"
                    self._store_embedding(emb3d_id, "EMB3D", embed_text, {
                        "name": name,
                        "threat_type": "embedded_device"
                    })

                elif obj_type == 'course-of-action':
                    # EMB3D Mitigation
                    mit_id = obj.get('external_references', [{}])[0].get('external_id', stix_id)
                    id_map[stix_id] = mit_id

                    session.run("""
                        MERGE (m:EMB3DMitigation {id: $id})
                        SET m.stix_id = $stix_id,
                            m.name = $name,
                            m.description = $description,
                            m.source = 'EMB3D',
                            m.updated_at = timestamp()
                    """, id=mit_id, stix_id=stix_id, name=name, description=description[:2000])
                    self.stats["emb3d_nodes"] += 1

                elif obj_type == 'x-mitre-emb3d-property':
                    # EMB3D Property (device characteristics)
                    prop_id = obj.get('x_mitre_emb3d_property_id', stix_id)
                    id_map[stix_id] = prop_id

                    session.run("""
                        MERGE (p:EMB3DProperty {id: $id})
                        SET p.stix_id = $stix_id,
                            p.name = $name,
                            p.description = $description,
                            p.source = 'EMB3D',
                            p.updated_at = timestamp()
                    """, id=prop_id, stix_id=stix_id, name=name, description=description[:2000])
                    self.stats["emb3d_nodes"] += 1

            # Process relationships
            print("   Processing relationships...")
            for obj in objects:
                if obj.get('type') == 'relationship':
                    source_ref = obj.get('source_ref', '')
                    target_ref = obj.get('target_ref', '')
                    rel_type = obj.get('relationship_type', 'related-to')

                    source_id = id_map.get(source_ref, source_ref)
                    target_id = id_map.get(target_ref, target_ref)

                    # Determine node types from STIX ID patterns
                    if 'vulnerability' in source_ref:
                        source_label = 'EMB3D'
                    elif 'course-of-action' in source_ref:
                        source_label = 'EMB3DMitigation'
                    elif 'x-mitre-emb3d-property' in source_ref:
                        source_label = 'EMB3DProperty'
                    else:
                        continue

                    if 'vulnerability' in target_ref:
                        target_label = 'EMB3D'
                    elif 'course-of-action' in target_ref:
                        target_label = 'EMB3DMitigation'
                    elif 'x-mitre-emb3d-property' in target_ref:
                        target_label = 'EMB3DProperty'
                    else:
                        continue

                    # Create relationship based on type
                    rel_cypher = rel_type.upper().replace('-', '_')
                    try:
                        session.run(f"""
                            MATCH (s:{source_label} {{stix_id: $source_stix}})
                            MATCH (t:{target_label} {{stix_id: $target_stix}})
                            MERGE (s)-[r:{rel_cypher}]->(t)
                        """, source_stix=source_ref, target_stix=target_ref)
                        self.stats["emb3d_relationships"] += 1
                    except:
                        pass  # Skip invalid relationships

        print(f"   ✅ EMB3D loaded: {self.stats['emb3d_nodes']} nodes, {self.stats['emb3d_relationships']} relationships")
        return {"nodes": self.stats['emb3d_nodes'], "relationships": self.stats['emb3d_relationships']}

    # =========================================================================
    # CROSS-TAXONOMY LINKING
    # =========================================================================

    def create_cross_links(self) -> Dict:
        """Create cross-taxonomy relationships between CAPEC, CWE, and EMB3D."""
        print("\n" + "="*60)
        print("🔗 CREATING CROSS-TAXONOMY LINKS")
        print("="*60)

        with self.driver.session() as session:
            # Link EMB3D threats to CWEs based on name/description similarity
            # (EMB3D doesn't have explicit CWE references, so we link by concept)

            # Link EMB3D to CAPEC Attack Patterns by similar concepts
            result = session.run("""
                MATCH (e:EMB3D)
                MATCH (c:CAPEC)
                WHERE toLower(e.description) CONTAINS toLower(c.name)
                   OR toLower(c.description) CONTAINS toLower(e.name)
                MERGE (e)-[r:RELATES_TO]->(c)
                SET r.source = 'semantic_match'
                RETURN count(r) as links
            """)
            record = result.single()
            emb3d_capec = record["links"] if record else 0

            # Verify existing CAPEC <-> CWE links
            result = session.run("""
                MATCH (c:CAPEC)-[r:EXPLOITS]->(w:CWE)
                RETURN count(r) as links
            """)
            record = result.single()
            capec_cwe = record["links"] if record else 0

            print(f"   ✅ CAPEC ↔ CWE links: {capec_cwe}")
            print(f"   ✅ EMB3D ↔ CAPEC links: {emb3d_capec}")

            # Create CVE links to CWE (from existing CVEs)
            result = session.run("""
                MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
                RETURN count(r) as links
            """)
            record = result.single()
            cve_cwe = record["links"] if record else 0
            print(f"   ✅ CVE → CWE links: {cve_cwe}")

        return {
            "capec_cwe": capec_cwe,
            "emb3d_capec": emb3d_capec,
            "cve_cwe": cve_cwe
        }

    def verify_schema(self) -> Dict:
        """Verify hierarchical schema is properly loaded."""
        print("\n" + "="*60)
        print("🔍 VERIFYING HIERARCHICAL SCHEMA")
        print("="*60)

        with self.driver.session() as session:
            # Count nodes by type
            result = session.run("""
                MATCH (n)
                WHERE n:CAPEC OR n:CWE OR n:EMB3D OR n:EMB3DMitigation OR n:EMB3DProperty
                   OR n:CAPECCategory OR n:CWECategory
                RETURN labels(n)[0] as label, count(*) as count
                ORDER BY count DESC
            """)

            node_counts = {}
            for record in result:
                node_counts[record["label"]] = record["count"]

            # Count relationship types
            result = session.run("""
                MATCH ()-[r]->()
                WHERE type(r) IN ['CHILD_OF', 'BELONGS_TO', 'EXPLOITS', 'RELATED_TO',
                                   'MITIGATES', 'RELATES_TO', 'HAS_WEAKNESS']
                RETURN type(r) as type, count(*) as count
                ORDER BY count DESC
            """)

            rel_counts = {}
            for record in result:
                rel_counts[record["type"]] = record["count"]

            # Print summary
            print("\n📊 Node Counts:")
            for label, count in sorted(node_counts.items()):
                print(f"   {label}: {count:,}")

            print("\n📊 Relationship Counts:")
            for rel_type, count in sorted(rel_counts.items()):
                print(f"   {rel_type}: {count:,}")

            # Check hierarchies exist
            result = session.run("""
                MATCH path = (c:CAPEC)-[:CHILD_OF*1..5]->(parent:CAPEC)
                RETURN count(path) as hierarchy_depth
            """)
            capec_hierarchy = result.single()["hierarchy_depth"]

            result = session.run("""
                MATCH path = (w:CWE)-[:CHILD_OF*1..5]->(parent:CWE)
                RETURN count(path) as hierarchy_depth
            """)
            cwe_hierarchy = result.single()["hierarchy_depth"]

            print(f"\n📊 Hierarchy Verification:")
            print(f"   CAPEC hierarchy paths: {capec_hierarchy:,}")
            print(f"   CWE hierarchy paths: {cwe_hierarchy:,}")

            valid = (
                node_counts.get("CAPEC", 0) > 500 and
                node_counts.get("CWE", 0) > 500 and
                node_counts.get("EMB3D", 0) > 0 and
                capec_hierarchy > 0 and
                cwe_hierarchy > 0
            )

            if valid:
                print("\n✅ SCHEMA VALIDATION: PASSED")
            else:
                print("\n⚠️  SCHEMA VALIDATION: INCOMPLETE")

            return {
                "nodes": node_counts,
                "relationships": rel_counts,
                "capec_hierarchy": capec_hierarchy,
                "cwe_hierarchy": cwe_hierarchy,
                "valid": valid
            }

    def print_summary(self):
        """Print final summary."""
        print("\n" + "="*60)
        print("📊 TAXONOMY LOADING SUMMARY")
        print("="*60)
        print(f"CAPEC Nodes: {self.stats['capec_nodes']:,}")
        print(f"CAPEC Relationships: {self.stats['capec_relationships']:,}")
        print(f"CWE Nodes: {self.stats['cwe_nodes']:,}")
        print(f"CWE Relationships: {self.stats['cwe_relationships']:,}")
        print(f"EMB3D Nodes: {self.stats['emb3d_nodes']:,}")
        print(f"EMB3D Relationships: {self.stats['emb3d_relationships']:,}")
        print(f"Cross-Taxonomy Links: {self.stats['cross_taxonomy']:,}")
        print(f"Qdrant Embeddings: {self.stats['embeddings']:,}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description="Load Security Taxonomies")
    parser.add_argument("--all", action="store_true", help="Load all taxonomies")
    parser.add_argument("--capec", action="store_true", help="Load CAPEC")
    parser.add_argument("--cwe", action="store_true", help="Load CWE")
    parser.add_argument("--emb3d", action="store_true", help="Load EMB3D")
    parser.add_argument("--verify", action="store_true", help="Verify schema only")
    parser.add_argument("--force", action="store_true", help="Force reload (clear existing)")

    args = parser.parse_args()

    # Default to --all if no specific taxonomy selected
    if not any([args.all, args.capec, args.cwe, args.emb3d, args.verify]):
        args.all = True

    print("="*60)
    print("🏗️  HIERARCHICAL TAXONOMY LOADER")
    print(f"    Date: {datetime.now().isoformat()}")
    print(f"    Force Reload: {args.force}")
    print("="*60)

    loader = TaxonomyLoader(force_reload=args.force)

    try:
        if args.verify:
            loader.verify_schema()
        else:
            if args.all or args.capec:
                loader.load_capec()

            if args.all or args.cwe:
                loader.load_cwe()

            if args.all or args.emb3d:
                loader.load_emb3d()

            loader.create_cross_links()
            loader.verify_schema()
            loader.print_summary()

    finally:
        loader.close()

    print("\n✅ TAXONOMY LOADING COMPLETE")


if __name__ == "__main__":
    main()
