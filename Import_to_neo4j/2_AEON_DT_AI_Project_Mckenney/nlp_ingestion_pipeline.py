#!/usr/bin/env python3
"""
NLP Ingestion Pipeline for Document Processing with Neo4j Integration

Processes multi-format documents (md, txt, pdf, docx, json) with:
- spaCy NLP for entity extraction
- Relationship extraction via dependency parsing
- Table and figure extraction
- Neo4j batch insertion with deduplication
- Progress tracking and resumability
"""

import os
import json
import hashlib
import logging
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from datetime import datetime
from collections import defaultdict

import spacy
from spacy.tokens import Doc, Span
import pandas as pd
from neo4j import GraphDatabase
from tqdm import tqdm
from entity_resolver import EntityResolver

# Document format handlers
try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document as DocxDocument
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentLoader:
    """Multi-format document loader with text extraction"""

    @staticmethod
    def load_text(file_path: str) -> str:
        """Load plain text file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    @staticmethod
    def load_markdown(file_path: str) -> str:
        """Load markdown file preserving structure"""
        return DocumentLoader.load_text(file_path)

    @staticmethod
    def load_json(file_path: str) -> str:
        """Load JSON file and convert to text"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            # Extract text fields from JSON
            text_parts = []
            for key, value in data.items():
                if isinstance(value, str):
                    text_parts.append(f"{key}: {value}")
                elif isinstance(value, (list, dict)):
                    text_parts.append(f"{key}: {json.dumps(value)}")
            return "\n".join(text_parts)
        return json.dumps(data)

    @staticmethod
    def load_pdf(file_path: str) -> str:
        """Load PDF with layout analysis"""
        if not PDF_SUPPORT:
            raise ImportError("pdfplumber not installed. Install with: pip install pdfplumber")

        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"[Page {page_num}]\n{text}")

        return "\n\n".join(text_parts)

    @staticmethod
    def load_docx(file_path: str) -> str:
        """Load DOCX file"""
        if not DOCX_SUPPORT:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")

        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    @classmethod
    def load(cls, file_path: str) -> str:
        """Load document based on file extension"""
        file_path = Path(file_path)
        ext = file_path.suffix.lower()

        loaders = {
            '.txt': cls.load_text,
            '.md': cls.load_markdown,
            '.json': cls.load_json,
            '.pdf': cls.load_pdf,
            '.docx': cls.load_docx,
        }

        loader = loaders.get(ext)
        if not loader:
            raise ValueError(f"Unsupported file format: {ext}")

        return loader(str(file_path))


class TextPreprocessor:
    """Text cleaning and normalization"""

    @staticmethod
    def clean(text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")

        return text.strip()


class EntityExtractor:
    """Extract entities using spaCy NLP with custom patterns"""

    # Cybersecurity-specific entity types
    CUSTOM_ENTITIES = {
        'CVE': r'CVE-\d{4}-\d{4,}',
        'CAPEC': r'CAPEC-\d+',
        'CWE': r'CWE-\d+',
        'TECHNIQUE': r'T\d{4}(?:\.\d{3})?',  # ATT&CK techniques
        'IP_ADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'HASH': r'\b[a-fA-F0-9]{32,64}\b',
        'URL': r'https?://[^\s]+',
    }

    def __init__(self, nlp):
        self.nlp = nlp

    def extract(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text"""
        doc = self.nlp(text)
        entities = []

        # Standard NER entities
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'type': 'NER'
            })

        # Custom pattern matching for cybersecurity entities
        for entity_type, pattern in self.CUSTOM_ENTITIES.items():
            for match in re.finditer(pattern, text):
                entities.append({
                    'text': match.group(),
                    'label': entity_type,
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'PATTERN'
                })

        return entities


class RelationshipExtractor:
    """Extract relationships using dependency parsing"""

    def __init__(self, nlp):
        self.nlp = nlp

    def extract(self, text: str) -> List[Dict[str, Any]]:
        """Extract subject-verb-object triples and other relationships"""
        doc = self.nlp(text)
        relationships = []

        for sent in doc.sents:
            # Extract SVO triples
            for token in sent:
                if token.pos_ == "VERB":
                    subjects = [child for child in token.children if child.dep_ in ("nsubj", "nsubjpass")]
                    objects = [child for child in token.children if child.dep_ in ("dobj", "pobj", "attr")]

                    for subject in subjects:
                        for obj in objects:
                            relationships.append({
                                'subject': subject.text,
                                'subject_lemma': subject.lemma_,
                                'predicate': token.text,
                                'predicate_lemma': token.lemma_,
                                'object': obj.text,
                                'object_lemma': obj.lemma_,
                                'sentence': sent.text,
                                'type': 'SVO'
                            })

            # Extract prepositional relationships
            for token in sent:
                if token.dep_ == "prep":
                    head = token.head
                    obj = [child for child in token.children if child.dep_ == "pobj"]
                    if obj:
                        relationships.append({
                            'subject': head.text,
                            'predicate': token.text,
                            'object': obj[0].text,
                            'sentence': sent.text,
                            'type': 'PREP'
                        })

        return relationships


class TableExtractor:
    """Extract tables from text and documents"""

    @staticmethod
    def extract_markdown_tables(text: str) -> List[pd.DataFrame]:
        """Extract tables from markdown text"""
        tables = []

        # Find markdown tables - improved pattern
        # Match: | header | header | \n | --- | --- | \n | data | data |
        lines = text.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Check if line looks like a table header
            if line.startswith('|') and line.endswith('|') and line.count('|') >= 3:
                # Check next line for separator
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    # Separator line has dashes
                    if next_line.startswith('|') and '-' in next_line:
                        # Parse header
                        headers = [h.strip() for h in line.split('|')[1:-1]]

                        # Parse data rows
                        data = []
                        j = i + 2
                        while j < len(lines):
                            row_line = lines[j].strip()
                            if row_line.startswith('|') and row_line.endswith('|'):
                                cells = [c.strip() for c in row_line.split('|')[1:-1]]
                                if len(cells) == len(headers):
                                    data.append(cells)
                                    j += 1
                                else:
                                    break
                            else:
                                break

                        # Create DataFrame
                        if data:
                            try:
                                df = pd.DataFrame(data, columns=headers)
                                tables.append(df)
                            except Exception as e:
                                logger.warning(f"Failed to parse table: {e}")

                        i = j - 1

            i += 1

        return tables


class MetadataTracker:
    """Track document metadata with SHA256 hashing for deduplication"""

    @staticmethod
    def compute_hash(text: str) -> str:
        """Compute SHA256 hash of text"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    def create_metadata(file_path: str, text: str) -> Dict[str, Any]:
        """Create metadata dictionary for document"""
        file_path = Path(file_path)

        return {
            'file_path': str(file_path.absolute()),
            'file_name': file_path.name,
            'file_ext': file_path.suffix,
            'file_size': file_path.stat().st_size if file_path.exists() else 0,
            'sha256': MetadataTracker.compute_hash(text),
            'processed_at': datetime.now().isoformat(),
            'char_count': len(text),
            'line_count': text.count('\n') + 1,
        }


class Neo4jBatchInserter:
    """Batch insert data into Neo4j with deduplication"""

    def __init__(self, uri: str, user: str, password: str, batch_size: int = 100):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.batch_size = batch_size
        self._setup_constraints()

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    def _setup_constraints(self):
        """Create Neo4j constraints and indexes"""
        with self.driver.session() as session:
            # NOTE: Neo4j Community Edition limitations:
            # - NODE KEY constraints require Enterprise Edition
            # - Composite unique constraints not supported
            # - Solution: MERGE with (text, label) + composite index for performance
            constraints = [
                "CREATE CONSTRAINT metadata_sha256 IF NOT EXISTS FOR (m:Metadata) REQUIRE m.sha256 IS UNIQUE",
                "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
                "CREATE INDEX entity_text IF NOT EXISTS FOR (e:Entity) ON (e.text)",
                "CREATE INDEX entity_label IF NOT EXISTS FOR (e:Entity) ON (e.label)",
                "CREATE INDEX entity_composite IF NOT EXISTS FOR (e:Entity) ON (e.text, e.label)",
                "CREATE INDEX relationship_doc_id IF NOT EXISTS FOR ()-[r:RELATIONSHIP]-() ON (r.doc_id)",
                "CREATE FULLTEXT INDEX document_fulltext IF NOT EXISTS FOR (d:Document) ON EACH [d.content]",
            ]

            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    logger.debug(f"Constraint/index already exists or failed: {e}")

    def check_document_exists(self, sha256: str) -> bool:
        """
        Check if document already processed AND has relationships.
        This ensures incomplete processing from buggy runs gets retried.
        """
        with self.driver.session() as session:
            # First check if Metadata exists
            metadata_result = session.run(
                "MATCH (m:Metadata {sha256: $sha256}) RETURN count(m) as count",
                sha256=sha256
            )
            metadata_exists = metadata_result.single()['count'] > 0

            if not metadata_exists:
                return False

            # If Metadata exists, verify document has relationships
            # Find the document ID associated with this SHA256
            doc_result = session.run(
                """
                MATCH (m:Metadata {sha256: $sha256})-[:METADATA_FOR]->(d:Document)
                RETURN d.id as doc_id
                """,
                sha256=sha256
            )

            doc_record = doc_result.single()
            if not doc_record:
                # Metadata exists but no document link - incomplete processing
                return False

            doc_id = doc_record['doc_id']

            # Check if this document has any relationships
            rel_result = session.run(
                """
                MATCH ()-[r:RELATIONSHIP {doc_id: $doc_id}]->()
                RETURN count(r) as count
                """,
                doc_id=doc_id
            )

            rel_count = rel_result.single()['count']

            # Only consider document "processed" if it has relationships
            return rel_count > 0

    def insert_document(self, metadata: Dict[str, Any], text: str) -> str:
        """Insert document with metadata"""
        with self.driver.session() as session:
            result = session.run("""
                CREATE (d:Document {
                    id: randomUUID(),
                    content: $content,
                    char_count: $char_count,
                    line_count: $line_count
                })
                MERGE (m:Metadata {sha256: $sha256})
                ON CREATE SET
                    m.file_path = $file_path,
                    m.file_name = $file_name,
                    m.file_ext = $file_ext,
                    m.file_size = $file_size,
                    m.processed_at = $processed_at
                ON MATCH SET
                    m.processed_at = $processed_at
                CREATE (m)-[:METADATA_FOR]->(d)
                RETURN d.id as doc_id
            """,
                content=text[:10000],  # Store first 10k chars
                char_count=metadata['char_count'],
                line_count=metadata['line_count'],
                sha256=metadata['sha256'],
                file_path=metadata['file_path'],
                file_name=metadata['file_name'],
                file_ext=metadata['file_ext'],
                file_size=metadata['file_size'],
                processed_at=metadata['processed_at']
            )
            return result.single()['doc_id']

    def insert_entities_batch(self, doc_id: str, entities: List[Dict[str, Any]]):
        """Batch insert entities"""
        if not entities:
            return

        # Batch entities
        for i in range(0, len(entities), self.batch_size):
            batch = entities[i:i + self.batch_size]

            with self.driver.session() as session:
                session.run("""
                    MATCH (d:Document {id: $doc_id})
                    UNWIND $entities as entity
                    MERGE (e:Entity {text: entity.text, label: entity.label})
                    ON CREATE SET
                        e.created_at = datetime(),
                        e.count = 1
                    ON MATCH SET
                        e.count = coalesce(e.count, 0) + 1
                    CREATE (d)-[:CONTAINS_ENTITY {
                        start: entity.start,
                        end: entity.end,
                        type: entity.type
                    }]->(e)
                """,
                    doc_id=doc_id,
                    entities=batch
                )

    def insert_relationships_batch(self, doc_id: str, relationships: List[Dict[str, Any]]):
        """Batch insert relationships"""
        if not relationships:
            return

        for i in range(0, len(relationships), self.batch_size):
            batch = relationships[i:i + self.batch_size]

            with self.driver.session() as session:
                session.run("""
                    MATCH (d:Document {id: $doc_id})
                    UNWIND $relationships as rel
                    MERGE (s:Entity {text: rel.subject, label: coalesce(rel.subject_label, 'UNKNOWN')})
                    ON CREATE SET s.text = rel.subject, s.label = coalesce(rel.subject_label, 'UNKNOWN')
                    MERGE (o:Entity {text: rel.object, label: coalesce(rel.object_label, 'UNKNOWN')})
                    ON CREATE SET o.text = rel.object, o.label = coalesce(rel.object_label, 'UNKNOWN')
                    CREATE (s)-[r:RELATIONSHIP {
                        predicate: rel.predicate,
                        type: rel.type,
                        sentence: rel.sentence,
                        doc_id: $doc_id
                    }]->(o)
                """,
                    doc_id=doc_id,
                    relationships=batch
                )


class NLPIngestionPipeline:
    """Main NLP ingestion pipeline orchestrator"""

    def __init__(
        self,
        neo4j_uri: str,
        neo4j_user: str,
        neo4j_password: str,
        spacy_model: str = "en_core_web_lg",
        batch_size: int = 100,
        progress_file: str = ".ingestion_progress.json"
    ):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.batch_size = batch_size
        self.progress_file = progress_file

        # Load spaCy model
        logger.info(f"Loading spaCy model: {spacy_model}")
        self.nlp = spacy.load(spacy_model)

        # Initialize components
        self.loader = DocumentLoader()
        self.preprocessor = TextPreprocessor()
        self.entity_extractor = EntityExtractor(self.nlp)
        self.relationship_extractor = RelationshipExtractor(self.nlp)
        self.table_extractor = TableExtractor()
        self.metadata_tracker = MetadataTracker()
        self.neo4j_inserter = Neo4jBatchInserter(neo4j_uri, neo4j_user, neo4j_password, batch_size)

        # Load progress
        self.processed_files = self._load_progress()

    def _load_progress(self) -> Set[str]:
        """Load processing progress from file"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                return set(data.get('processed_files', []))
            except Exception as e:
                logger.warning(f"Failed to load progress: {e}")
        return set()

    def _save_progress(self):
        """Save processing progress to file"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump({
                    'processed_files': list(self.processed_files),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save progress: {e}")

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process single document through full pipeline"""
        try:
            # Load document
            logger.info(f"Loading: {file_path}")
            text = self.loader.load(file_path)

            # Clean text
            text = self.preprocessor.clean(text)

            # Create metadata
            metadata = self.metadata_tracker.create_metadata(file_path, text)

            # Check for duplicates
            if self.neo4j_inserter.check_document_exists(metadata['sha256']):
                logger.info(f"Document already processed (duplicate): {file_path}")
                return {'status': 'duplicate', 'sha256': metadata['sha256']}

            # Insert document
            doc_id = self.neo4j_inserter.insert_document(metadata, text)
            logger.info(f"Document inserted: {doc_id}")

            # Extract entities
            logger.info("Extracting entities...")
            entities = self.entity_extractor.extract(text)
            self.neo4j_inserter.insert_entities_batch(doc_id, entities)
            logger.info(f"Inserted {len(entities)} entities")

            # Resolve entity duplicates and variations
            try:
                entity_resolver = EntityResolver(self.neo4j_inserter.driver)
                resolution_stats = entity_resolver.resolve_all_entities(doc_id)
                logger.info(f"Entity resolution: {resolution_stats}")
            except Exception as e:
                logger.error(f"Entity resolution failed for {doc_id}: {e}")
                # Don't fail document processing on resolution errors

            # Extract relationships
            logger.info("Extracting relationships...")
            relationships = self.relationship_extractor.extract(text)
            self.neo4j_inserter.insert_relationships_batch(doc_id, relationships)
            logger.info(f"Inserted {len(relationships)} relationships")

            # Extract tables
            tables = self.table_extractor.extract_markdown_tables(text)
            logger.info(f"Extracted {len(tables)} tables")

            return {
                'status': 'success',
                'doc_id': doc_id,
                'sha256': metadata['sha256'],
                'entities': len(entities),
                'relationships': len(relationships),
                'tables': len(tables)
            }

        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            return {'status': 'error', 'error': str(e)}

    def process_directory(self, directory: str, file_pattern: str = "*.*"):
        """Process all documents in directory"""
        directory = Path(directory)
        files = sorted(directory.glob(file_pattern))

        logger.info(f"Found {len(files)} files to process")

        results = {
            'total': len(files),
            'processed': 0,
            'duplicates': 0,
            'errors': 0,
            'skipped': 0
        }

        with tqdm(total=len(files), desc="Processing documents") as pbar:
            for file_path in files:
                file_path_str = str(file_path.absolute())

                # Skip if already processed
                if file_path_str in self.processed_files:
                    results['skipped'] += 1
                    pbar.update(1)
                    continue

                # Process document
                result = self.process_document(file_path_str)

                if result['status'] == 'success':
                    results['processed'] += 1
                    self.processed_files.add(file_path_str)
                elif result['status'] == 'duplicate':
                    results['duplicates'] += 1
                    self.processed_files.add(file_path_str)
                else:
                    results['errors'] += 1

                # Save progress periodically
                if (results['processed'] + results['duplicates']) % 10 == 0:
                    self._save_progress()

                pbar.update(1)

        # Final progress save
        self._save_progress()

        logger.info(f"Processing complete: {results}")
        return results

    def close(self):
        """Close connections and cleanup"""
        self.neo4j_inserter.close()
        self._save_progress()


def main():
    """Main entry point for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(description="NLP Ingestion Pipeline for Document Processing")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--neo4j-uri", default="bolt://localhost:7687", help="Neo4j URI")
    parser.add_argument("--neo4j-user", default="neo4j", help="Neo4j username")
    parser.add_argument("--neo4j-password", required=True, help="Neo4j password")
    parser.add_argument("--spacy-model", default="en_core_web_lg", help="spaCy model name")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size for Neo4j inserts")
    parser.add_argument("--pattern", default="**/*.md", help="File pattern for directory processing")

    args = parser.parse_args()

    # Create pipeline
    pipeline = NLPIngestionPipeline(
        neo4j_uri=args.neo4j_uri,
        neo4j_user=args.neo4j_user,
        neo4j_password=args.neo4j_password,
        spacy_model=args.spacy_model,
        batch_size=args.batch_size
    )

    try:
        input_path = Path(args.input)

        if input_path.is_file():
            # Process single file
            result = pipeline.process_document(str(input_path))
            print(json.dumps(result, indent=2))
        elif input_path.is_dir():
            # Process directory
            results = pipeline.process_directory(str(input_path), args.pattern)
            print(json.dumps(results, indent=2))
        else:
            logger.error(f"Input path does not exist: {args.input}")
            return 1

        return 0

    finally:
        pipeline.close()


if __name__ == "__main__":
    exit(main())
