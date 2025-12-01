#!/usr/bin/env python3
"""
Batch Document Loader for Cybersecurity Threat Intelligence
Parallel processing with Neo4j integration and Claude-Flow coordination
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Optional
import argparse
from datetime import datetime
from multiprocessing import Pool, cpu_count
from functools import partial
import sys

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    logging.warning("tqdm not installed. Install with: pip install tqdm")

# Import our processing modules
sys.path.append(str(Path(__file__).parent))
from pdf_processor import PDFProcessor
from word_processor import WordProcessor
from nlp_entity_extractor import EntityExtractor
from relationship_extractor import RelationshipExtractor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchDocumentLoader:
    """Batch process documents with parallel execution and Neo4j integration"""

    def __init__(self,
                 num_workers: Optional[int] = None,
                 neo4j_enabled: bool = False,
                 neo4j_uri: Optional[str] = None,
                 neo4j_user: Optional[str] = None,
                 neo4j_password: Optional[str] = None,
                 claude_flow_enabled: bool = False):
        """
        Initialize batch document loader

        Args:
            num_workers: Number of parallel workers (default: CPU count)
            neo4j_enabled: Enable Neo4j database integration
            neo4j_uri: Neo4j database URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
            claude_flow_enabled: Enable Claude-Flow coordination
        """
        self.num_workers = num_workers or cpu_count()
        self.neo4j_enabled = neo4j_enabled
        self.claude_flow_enabled = claude_flow_enabled

        logger.info(f"Initialized with {self.num_workers} workers")

        # Initialize processors
        self.pdf_processor = PDFProcessor()
        self.word_processor = WordProcessor()
        self.entity_extractor = EntityExtractor()
        self.relationship_extractor = RelationshipExtractor()

        # Initialize Neo4j driver if enabled
        if neo4j_enabled:
            try:
                from neo4j import GraphDatabase
                self.neo4j_driver = GraphDatabase.driver(
                    neo4j_uri or "bolt://localhost:7687",
                    auth=(neo4j_user or "neo4j", neo4j_password or "password")
                )
                logger.info("Neo4j connection established")
            except ImportError:
                logger.error("neo4j package not installed. Install with: pip install neo4j")
                self.neo4j_enabled = False
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                self.neo4j_enabled = False

    def process_single_document(self, file_path: Path) -> Dict:
        """
        Process a single document

        Args:
            file_path: Path to document file

        Returns:
            Processing result dictionary
        """
        try:
            logger.info(f"Processing: {file_path.name}")

            # Determine file type and process accordingly
            if file_path.suffix.lower() == '.pdf':
                doc_data = self.pdf_processor.process_pdf(file_path)
                text = self._extract_text_from_pdf_result(doc_data)

            elif file_path.suffix.lower() in ['.docx', '.doc']:
                doc_data = self.word_processor.process_document(file_path)
                text = self._extract_text_from_word_result(doc_data)

            elif file_path.suffix.lower() in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                doc_data = {'text': text}

            else:
                return {
                    'file': str(file_path),
                    'status': 'skipped',
                    'reason': f'Unsupported file type: {file_path.suffix}'
                }

            # Extract entities
            entities = self.entity_extractor.extract_entities(text)

            # Extract relationships
            relationships = self.relationship_extractor.extract_all_relationships(text)

            result = {
                'file': str(file_path),
                'status': 'success',
                'document_data': doc_data,
                'entities': entities,
                'relationships': relationships,
                'processed_at': datetime.now().isoformat()
            }

            # Import to Neo4j if enabled
            if self.neo4j_enabled:
                self._import_to_neo4j(result)

            return result

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return {
                'file': str(file_path),
                'status': 'error',
                'error': str(e)
            }

    def batch_process(self,
                     input_dir: Path,
                     output_dir: Path,
                     file_patterns: List[str] = ['*.pdf', '*.docx', '*.txt']) -> Dict:
        """
        Process multiple documents in parallel

        Args:
            input_dir: Directory containing documents
            output_dir: Output directory for results
            file_patterns: File patterns to process

        Returns:
            Summary dictionary
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Collect all files
        all_files = []
        for pattern in file_patterns:
            all_files.extend(input_dir.glob(pattern))

        # Filter out temporary files
        all_files = [f for f in all_files if not f.name.startswith('~$')]

        logger.info(f"Found {len(all_files)} documents to process")

        # Execute Claude-Flow pre-task hook
        if self.claude_flow_enabled:
            self._claude_flow_pre_task(len(all_files))

        # Process in parallel
        results = []

        if TQDM_AVAILABLE:
            with Pool(self.num_workers) as pool:
                results = list(tqdm(
                    pool.imap(self.process_single_document, all_files),
                    total=len(all_files),
                    desc="Processing documents"
                ))
        else:
            with Pool(self.num_workers) as pool:
                results = pool.map(self.process_single_document, all_files)

        # Save individual results
        for result in results:
            if result['status'] == 'success':
                file_path = Path(result['file'])
                output_file = output_dir / f"{file_path.stem}.json"

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

        # Generate summary
        summary = self._generate_summary(results)

        # Save summary
        summary_file = output_dir / 'batch_processing_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        logger.info(f"Batch processing complete. Summary saved to {summary_file}")

        # Execute Claude-Flow post-task hook
        if self.claude_flow_enabled:
            self._claude_flow_post_task(summary)

        return summary

    def _extract_text_from_pdf_result(self, pdf_data: Dict) -> str:
        """Extract text from PDF processing result"""
        if 'text' in pdf_data:
            if pdf_data['text'].get('type') == 'page_chunks':
                return '\n\n'.join([page['text'] for page in pdf_data['text']['pages']])
            else:
                return pdf_data['text'].get('text', '')
        return ''

    def _extract_text_from_word_result(self, word_data: Dict) -> str:
        """Extract text from Word processing result"""
        text_parts = []

        if 'structure' in word_data and 'sections' in word_data['structure']:
            for section in word_data['structure']['sections']:
                text_parts.append(section.get('title', ''))

                for content in section.get('content', []):
                    if content['type'] == 'paragraph':
                        text_parts.append(content['text'])

                for subsection in section.get('subsections', []):
                    text_parts.append(subsection.get('title', ''))
                    for content in subsection.get('content', []):
                        if content['type'] == 'paragraph':
                            text_parts.append(content['text'])

        return '\n\n'.join(text_parts)

    def _import_to_neo4j(self, result: Dict):
        """
        Import document data to Neo4j

        Args:
            result: Document processing result
        """
        if not self.neo4j_enabled:
            return

        try:
            with self.neo4j_driver.session() as session:
                # Create document node
                doc_name = Path(result['file']).stem

                session.run(
                    """
                    MERGE (d:Document {name: $name})
                    SET d.file_path = $file_path,
                        d.processed_at = $processed_at
                    """,
                    name=doc_name,
                    file_path=result['file'],
                    processed_at=result['processed_at']
                )

                # Import entities
                entities = result.get('entities', {})
                for entity_type, entity_list in entities.items():
                    for entity in entity_list:
                        session.run(
                            f"""
                            MERGE (e:Entity {{name: $name, type: $type}})
                            MERGE (d:Document {{name: $doc_name}})
                            MERGE (d)-[:CONTAINS]->(e)
                            """,
                            name=entity['text'],
                            type=entity_type,
                            doc_name=doc_name
                        )

                # Import relationships
                graph_rels = result.get('relationships', {}).get('graph_relationships', [])
                for rel in graph_rels:
                    session.run(
                        f"""
                        MERGE (from:Entity {{name: $from_node, type: $from_type}})
                        MERGE (to:Entity {{name: $to_node, type: $to_type}})
                        MERGE (from)-[r:{rel['relationship_type']} {{confidence: $confidence}}]->(to)
                        """,
                        from_node=rel['from_node'],
                        from_type=rel['from_type'],
                        to_node=rel['to_node'],
                        to_type=rel['to_type'],
                        confidence=rel['confidence']
                    )

            logger.info(f"Imported {result['file']} to Neo4j")

        except Exception as e:
            logger.error(f"Error importing to Neo4j: {e}")

    def _generate_summary(self, results: List[Dict]) -> Dict:
        """
        Generate processing summary

        Args:
            results: List of processing results

        Returns:
            Summary dictionary
        """
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = sum(1 for r in results if r['status'] == 'error')
        skipped_count = sum(1 for r in results if r['status'] == 'skipped')

        # Count entities and relationships
        total_entities = 0
        total_relationships = 0

        for result in results:
            if result['status'] == 'success':
                entities = result.get('entities', {})
                total_entities += sum(len(entity_list) for entity_list in entities.values())

                relationships = result.get('relationships', {})
                total_relationships += relationships.get('total_relationships', 0)

        return {
            'total_documents': len(results),
            'successful': success_count,
            'errors': error_count,
            'skipped': skipped_count,
            'total_entities_extracted': total_entities,
            'total_relationships_extracted': total_relationships,
            'processed_at': datetime.now().isoformat(),
            'results': results
        }

    def _claude_flow_pre_task(self, num_documents: int):
        """Execute Claude-Flow pre-task hook"""
        try:
            import subprocess
            subprocess.run([
                'npx', 'claude-flow@alpha', 'hooks', 'pre-task',
                '--description', f'Batch processing {num_documents} documents'
            ], check=False)
        except Exception as e:
            logger.warning(f"Claude-Flow pre-task hook failed: {e}")

    def _claude_flow_post_task(self, summary: Dict):
        """Execute Claude-Flow post-task hook"""
        try:
            import subprocess
            subprocess.run([
                'npx', 'claude-flow@alpha', 'hooks', 'post-task',
                '--task-id', 'batch_document_processing',
                '--metrics', json.dumps(summary)
            ], check=False)
        except Exception as e:
            logger.warning(f"Claude-Flow post-task hook failed: {e}")

    def __del__(self):
        """Cleanup Neo4j connection"""
        if hasattr(self, 'neo4j_driver') and self.neo4j_driver:
            self.neo4j_driver.close()


def main():
    """CLI interface for batch document loading"""
    parser = argparse.ArgumentParser(description='Batch process documents for threat intelligence')
    parser.add_argument('input_dir', help='Input directory containing documents')
    parser.add_argument('-o', '--output', help='Output directory', default='tmp/batch_results')
    parser.add_argument('-w', '--workers', type=int, help='Number of parallel workers')
    parser.add_argument('--neo4j', action='store_true', help='Enable Neo4j import')
    parser.add_argument('--neo4j-uri', help='Neo4j URI', default='bolt://localhost:7687')
    parser.add_argument('--neo4j-user', help='Neo4j username', default='neo4j')
    parser.add_argument('--neo4j-password', help='Neo4j password')
    parser.add_argument('--claude-flow', action='store_true', help='Enable Claude-Flow coordination')
    parser.add_argument('--patterns', nargs='+', help='File patterns to process',
                       default=['*.pdf', '*.docx', '*.txt'])

    args = parser.parse_args()

    # Initialize loader
    loader = BatchDocumentLoader(
        num_workers=args.workers,
        neo4j_enabled=args.neo4j,
        neo4j_uri=args.neo4j_uri,
        neo4j_user=args.neo4j_user,
        neo4j_password=args.neo4j_password,
        claude_flow_enabled=args.claude_flow
    )

    # Process documents
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output)

    if not input_dir.is_dir():
        logger.error(f"Input directory not found: {input_dir}")
        return

    summary = loader.batch_process(input_dir, output_dir, file_patterns=args.patterns)

    # Print summary
    print("\n" + "="*60)
    print("BATCH PROCESSING SUMMARY")
    print("="*60)
    print(f"Total documents: {summary['total_documents']}")
    print(f"Successful: {summary['successful']}")
    print(f"Errors: {summary['errors']}")
    print(f"Skipped: {summary['skipped']}")
    print(f"Total entities: {summary['total_entities_extracted']}")
    print(f"Total relationships: {summary['total_relationships_extracted']}")
    print("="*60)


if __name__ == '__main__':
    main()
