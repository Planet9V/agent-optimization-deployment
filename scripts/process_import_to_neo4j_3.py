#!/usr/bin/env python3
"""
Document Processing Pipeline for import_to_neo4j_3
Handles deduplication, entity extraction, and Neo4j import
"""

import hashlib
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from neo4j import GraphDatabase
import json

# Python-docx for Word docs
try:
    from docx import Document as DocxDocument
except ImportError:
    print("Installing python-docx...")
    import subprocess
    subprocess.run(["pip3", "install", "python-docx"], check=True)
    from docx import Document as DocxDocument


class DocumentProcessor:
    """Process documents with deduplication and entity extraction"""

    def __init__(self):
        self.neo4j_uri = 'bolt://localhost:7687'
        self.neo4j_user = 'neo4j'
        self.neo4j_password = 'neo4j@openspg'
        self.db_path = '/home/jim/2_OXOT_Projects_Dev/import_to_neo4j_2/document_library.db'

        self.driver = GraphDatabase.driver(
            self.neo4j_uri,
            auth=(self.neo4j_user, self.neo4j_password)
        )

        # Statistics
        self.stats = {
            'total_files': 0,
            'new_files': 0,
            'duplicates': 0,
            'errors': 0,
            'entities_extracted': 0,
            'by_category': {}
        }

        # Entity patterns
        self.patterns = {
            'CVE': re.compile(r'CVE-\d{4}-\d{4,7}', re.IGNORECASE),
            'CWE': re.compile(r'CWE-\d+', re.IGNORECASE),
            'ThreatActor': re.compile(r'\b(?:APT\d+|Volt\s+Typhoon|Sandworm|Lazarus|Cozy\s+Bear|FrostyGoop|Voltzite|CyberAv3ngers|DragonForce|RansomHub|BlackCat|Stormous|Rhysida|LockBit|Qilin|Royal|Akira|Play|Scattered\s+Spider|Cl0p)\b', re.IGNORECASE),
            'Malware': re.compile(r'\b(?:ransomware|backdoor|trojan|worm|spyware|rootkit|keylogger|botnet)\b', re.IGNORECASE),
        }

    def calculate_hash(self, content: str) -> str:
        """Calculate SHA256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def read_markdown(self, filepath: Path) -> str:
        """Read markdown file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""

    def read_docx(self, filepath: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = DocxDocument(filepath)
            text_parts = []
            for para in doc.paragraphs:
                text_parts.append(para.text)
            return '\n'.join(text_parts)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""

    def extract_content(self, filepath: Path) -> Tuple[str, str]:
        """Extract content and calculate hash"""
        if filepath.suffix == '.md':
            content = self.read_markdown(filepath)
        elif filepath.suffix == '.docx':
            content = self.read_docx(filepath)
        else:
            content = ""

        file_hash = self.calculate_hash(content)
        return content, file_hash

    def check_duplicate_neo4j(self, file_hash: str) -> bool:
        """Check if document exists in Neo4j by hash"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (d:Document {file_hash: $hash}) RETURN count(d) as count",
                hash=file_hash
            )
            count = result.single()['count']
            return count > 0

    def check_duplicate_sqlite(self, file_hash: str) -> bool:
        """Check if document exists in SQLite by hash"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM document_library WHERE sha256_hash = ?",
            (file_hash,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def extract_entities(self, content: str) -> Dict[str, Set[str]]:
        """Extract entities from content"""
        entities = {
            'CVE': set(),
            'CWE': set(),
            'ThreatActor': set(),
            'Malware': set()
        }

        for entity_type, pattern in self.patterns.items():
            matches = pattern.findall(content)
            entities[entity_type].update(m.upper() if entity_type in ['CVE', 'CWE'] else m for m in matches)

        return entities

    def import_to_neo4j(self, filepath: Path, content: str, file_hash: str, entities: Dict[str, Set[str]]) -> str:
        """Import document to Neo4j and link entities"""
        with self.driver.session() as session:
            # Create Document node
            result = session.run("""
                CREATE (d:Document {
                    file_path: $path,
                    file_hash: $hash,
                    file_type: $type,
                    file_size: $size,
                    import_date: datetime(),
                    last_modified: datetime(),
                    entity_count: $entity_count
                })
                RETURN elementId(d) as doc_id
            """,
                path=str(filepath),
                hash=file_hash,
                type=filepath.suffix[1:],
                size=len(content),
                entity_count=sum(len(v) for v in entities.values())
            )

            doc_id = result.single()['doc_id']

            # Link entities
            for entity_type, entity_names in entities.items():
                for entity_name in entity_names:
                    # Create or match entity
                    session.run(f"""
                        MERGE (e:{entity_type} {{name: $name}})
                        WITH e
                        MATCH (d:Document) WHERE elementId(d) = $doc_id
                        MERGE (d)-[:MENTIONS]->(e)
                    """,
                        name=entity_name,
                        doc_id=doc_id
                    )

            return doc_id

    def import_to_sqlite(self, filepath: Path, file_hash: str, neo4j_doc_id: str, entities: Dict[str, Set[str]]):
        """Import document to SQLite library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO document_library (
                file_name, sha256_hash, file_path, ingestion_timestamp,
                file_size, format, neo4j_doc_id, entity_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            filepath.name,
            file_hash,
            str(filepath),
            datetime.now().isoformat(),
            filepath.stat().st_size,
            filepath.suffix[1:],
            neo4j_doc_id,
            sum(len(v) for v in entities.values())
        ))

        conn.commit()
        conn.close()

    def process_file(self, filepath: Path, category: str) -> Tuple[bool, str]:
        """Process a single file"""
        self.stats['total_files'] += 1

        # Extract content and hash
        content, file_hash = self.extract_content(filepath)
        if not content:
            self.stats['errors'] += 1
            return False, "Failed to extract content"

        # Check duplicates
        if self.check_duplicate_neo4j(file_hash) or self.check_duplicate_sqlite(file_hash):
            self.stats['duplicates'] += 1
            return False, f"Duplicate (hash: {file_hash[:16]}...)"

        # Extract entities
        entities = self.extract_entities(content)
        total_entities = sum(len(v) for v in entities.values())
        self.stats['entities_extracted'] += total_entities

        # Import to Neo4j
        try:
            neo4j_doc_id = self.import_to_neo4j(filepath, content, file_hash, entities)

            # Import to SQLite
            self.import_to_sqlite(filepath, file_hash, neo4j_doc_id, entities)

            self.stats['new_files'] += 1
            self.stats['by_category'][category] = self.stats['by_category'].get(category, 0) + 1

            return True, f"Imported ({total_entities} entities: {', '.join(f'{k}={len(v)}' for k, v in entities.items() if v)})"
        except Exception as e:
            self.stats['errors'] += 1
            return False, f"Import error: {e}"

    def process_directory(self, base_path: Path) -> Dict[str, List[Dict]]:
        """Process all files in directory structure"""
        results = {}

        # Define categories
        categories = {
            '11_SBOM_Analysis': [],
            '4_AEON_Digital_Twin_Cyber_Threats': [],
            '4_AEON_Digital_Twin_Cyber_Threats/Pyschoanalytics': [],
            'Express Attack Briefs': [],
            'Crisis Management Competitors': []
        }

        # Collect files by category
        for filepath in sorted(base_path.rglob('*')):
            if not filepath.is_file() or filepath.suffix not in ['.md', '.docx']:
                continue

            # Determine category
            rel_path = filepath.relative_to(base_path)
            category = None

            if '11_SBOM_Analysis' in str(rel_path):
                category = '11_SBOM_Analysis'
            elif 'Pyschoanalytics' in str(rel_path):
                category = '4_AEON_Digital_Twin_Cyber_Threats/Pyschoanalytics'
            elif '4_AEON_Digital_Twin_Cyber_Threats' in str(rel_path):
                category = '4_AEON_Digital_Twin_Cyber_Threats'
            elif 'Express Attack Briefs' in str(rel_path):
                category = 'Express Attack Briefs'
            elif 'Crisis Management Competitors' in str(rel_path):
                category = 'Crisis Management Competitors'

            if category:
                categories[category].append(filepath)

        # Process each category
        for category, files in categories.items():
            print(f"\n{'='*80}")
            print(f"Processing: {category} ({len(files)} files)")
            print('='*80)

            category_results = []
            for filepath in files:
                success, message = self.process_file(filepath, category)
                status = "✓" if success else "✗"
                print(f"  {status} {filepath.name[:60]:<60} | {message}")

                category_results.append({
                    'file': filepath.name,
                    'path': str(filepath),
                    'success': success,
                    'message': message
                })

            results[category] = category_results

        return results

    def generate_report(self, results: Dict[str, List[Dict]]) -> str:
        """Generate processing report"""
        report = []
        report.append("\n" + "="*80)
        report.append("DOCUMENT PROCESSING REPORT")
        report.append("="*80)
        report.append(f"\nProcessing Date: {datetime.now().isoformat()}")
        report.append(f"\nSummary Statistics:")
        report.append(f"  Total Files Scanned: {self.stats['total_files']}")
        report.append(f"  New Files Processed: {self.stats['new_files']}")
        report.append(f"  Duplicates Skipped: {self.stats['duplicates']}")
        report.append(f"  Errors: {self.stats['errors']}")
        report.append(f"  Total Entities Extracted: {self.stats['entities_extracted']}")

        report.append(f"\nBy Category:")
        for category, count in sorted(self.stats['by_category'].items()):
            report.append(f"  {category}: {count} new files")

        # Get Neo4j growth
        with self.driver.session() as session:
            result = session.run("MATCH (d:Document) RETURN count(d) as count")
            doc_count = result.single()['count']

            result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = result.single()['count']

            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            total_rels = result.single()['count']

        report.append(f"\nNeo4j Final State:")
        report.append(f"  Total Documents: {doc_count}")
        report.append(f"  Total Nodes: {total_nodes}")
        report.append(f"  Total Relationships: {total_rels}")

        report.append(f"\nDetailed Results by Category:")
        for category, file_results in results.items():
            report.append(f"\n{category}:")
            report.append(f"  Files: {len(file_results)}")
            new = sum(1 for r in file_results if r['success'])
            dups = sum(1 for r in file_results if 'Duplicate' in r['message'])
            report.append(f"  New: {new}, Duplicates: {dups}")

        return '\n'.join(report)

    def close(self):
        """Close connections"""
        self.driver.close()


def main():
    """Main processing function"""
    base_path = Path('/home/jim/2_OXOT_Projects_Dev/import_to_neo4j_3')

    processor = DocumentProcessor()

    try:
        # Process all files
        results = processor.process_directory(base_path)

        # Generate report
        report = processor.generate_report(results)
        print(report)

        # Save report
        report_path = Path('/home/jim/2_OXOT_Projects_Dev/docs/import_to_neo4j_3_processing_report.txt')
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        print(f"\n✓ Report saved to: {report_path}")

    finally:
        processor.close()


if __name__ == '__main__':
    main()
