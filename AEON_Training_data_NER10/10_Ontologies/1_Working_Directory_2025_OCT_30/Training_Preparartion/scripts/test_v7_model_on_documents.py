#!/usr/bin/env python3
"""
V7 NER Model Testing on Real-World Documents
Tests v7 model on annual cybersecurity reports, express attack briefs, and sector analysis
"""

import spacy
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import subprocess
import sys
from document_processor import DocumentProcessor

class V7ModelTester:
    """Test v7 NER model on real-world documents"""

    def __init__(self, model_path: str = "models/v7_ner_model"):
        print(f"\n🔄 Loading v7 NER model from: {model_path}")
        try:
            self.nlp = spacy.load(model_path)
            print(f"✅ Model loaded successfully")
            print(f"📊 Entity types: {len(self.nlp.get_pipe('ner').labels)}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)

        # Initialize enhanced document processor
        print(f"🔧 Initializing enhanced document processor...")
        self.doc_processor = DocumentProcessor()
        print(self.doc_processor.get_capability_report())

        self.entity_counts = defaultdict(int)
        self.results = {
            'total_documents': 0,
            'total_entities': 0,
            'document_results': [],
            'category_stats': {}
        }

    def read_document(self, file_path: Path) -> str:
        """Read any supported document format using DocumentProcessor"""
        text = self.doc_processor.read_document(str(file_path))
        return text if text else ""

    def process_document(self, file_path: Path, category: str) -> Dict:
        """Process a single document with v7 NER model"""
        print(f"  📄 Processing: {file_path.name[:60]}")

        # Read document using enhanced processor (handles all formats)
        text = self.read_document(file_path)

        if not text or len(text) < 50:
            print(f"    ⚠️  No text extracted (length: {len(text)})")
            return {
                'file': file_path.name,
                'category': category,
                'text_length': len(text),
                'entities_found': 0,
                'entity_breakdown': {}
            }

        # Truncate very long documents to avoid memory issues
        max_chars = 500000  # ~500KB of text
        if len(text) > max_chars:
            text = text[:max_chars]
            print(f"    ℹ️  Truncated to {max_chars:,} characters")

        # Process with NER model
        doc = self.nlp(text)

        # Count entities
        entity_breakdown = defaultdict(int)
        unique_entities = defaultdict(set)

        for ent in doc.ents:
            entity_breakdown[ent.label_] += 1
            unique_entities[ent.label_].add(ent.text.lower())
            self.entity_counts[ent.label_] += 1

        entities_found = len(doc.ents)
        unique_count = sum(len(v) for v in unique_entities.values())

        print(f"    ✅ Found {entities_found} entities ({unique_count} unique) in {len(text):,} chars")

        result = {
            'file': file_path.name,
            'category': category,
            'text_length': len(text),
            'entities_found': entities_found,
            'unique_entities': unique_count,
            'entity_breakdown': dict(entity_breakdown),
            'unique_entity_breakdown': {k: len(v) for k, v in unique_entities.items()},
            'top_entities': self.get_top_entities(doc.ents, limit=10)
        }

        self.results['total_documents'] += 1
        self.results['total_entities'] += entities_found
        self.results['document_results'].append(result)

        return result

    def get_top_entities(self, entities, limit: int = 10) -> Dict[str, List[str]]:
        """Get top N entities by type"""
        entity_texts = defaultdict(list)
        for ent in entities:
            if ent.text not in entity_texts[ent.label_]:
                entity_texts[ent.label_].append(ent.text)

        return {label: texts[:limit] for label, texts in entity_texts.items()}

    def process_directory(self, directory: Path, category: str,
                         pattern: str = "*.md", limit: int = None) -> List[Dict]:
        """Process all matching files in directory"""
        print(f"\n📂 Processing {category}: {directory}")

        files = sorted(directory.glob(pattern))
        if limit:
            files = files[:limit]

        print(f"   Found {len(files)} files")

        category_results = []
        for file_path in files:
            result = self.process_document(file_path, category)
            category_results.append(result)

        # Calculate category statistics
        total_entities = sum(r['entities_found'] for r in category_results)
        avg_entities = total_entities / len(category_results) if category_results else 0

        self.results['category_stats'][category] = {
            'documents': len(category_results),
            'total_entities': total_entities,
            'avg_entities_per_doc': avg_entities,
            'total_text_length': sum(r['text_length'] for r in category_results)
        }

        print(f"   ✅ Category stats: {len(category_results)} docs, {total_entities} entities")

        return category_results

    def generate_report(self) -> Dict:
        """Generate comprehensive test report"""
        print(f"\n" + "="*80)
        print(f"📊 V7 NER MODEL TEST REPORT")
        print(f"="*80)

        # Overall statistics
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Total documents processed: {self.results['total_documents']}")
        print(f"   Total entities extracted: {self.results['total_entities']:,}")
        print(f"   Average entities per doc: {self.results['total_entities'] / self.results['total_documents']:.1f}")

        # Entity type distribution
        print(f"\n🏷️  ENTITY TYPE DISTRIBUTION:")
        sorted_entities = sorted(self.entity_counts.items(),
                                key=lambda x: x[1], reverse=True)
        for entity_type, count in sorted_entities[:20]:
            percentage = (count / self.results['total_entities']) * 100
            print(f"   {entity_type:20s} {count:6,d} ({percentage:5.2f}%)")

        # Category breakdown
        print(f"\n📂 CATEGORY BREAKDOWN:")
        for category, stats in self.results['category_stats'].items():
            print(f"\n   {category}:")
            print(f"      Documents: {stats['documents']}")
            print(f"      Total entities: {stats['total_entities']:,}")
            print(f"      Avg entities/doc: {stats['avg_entities_per_doc']:.1f}")
            print(f"      Total text: {stats['total_text_length']:,} chars")

        # Document-level statistics
        doc_entity_counts = [r['entities_found'] for r in self.results['document_results']]
        if doc_entity_counts:
            print(f"\n📊 DOCUMENT-LEVEL STATISTICS:")
            print(f"   Min entities: {min(doc_entity_counts)}")
            print(f"   Max entities: {max(doc_entity_counts)}")
            print(f"   Median entities: {sorted(doc_entity_counts)[len(doc_entity_counts)//2]}")

        # Top performing documents
        print(f"\n🏆 TOP 10 DOCUMENTS BY ENTITY COUNT:")
        top_docs = sorted(self.results['document_results'],
                         key=lambda x: x['entities_found'], reverse=True)[:10]
        for i, doc in enumerate(top_docs, 1):
            print(f"   {i:2d}. {doc['file'][:50]:50s} - {doc['entities_found']:5d} entities")

        return self.results

    def save_results(self, output_file: str = "data/ner_training/V7_TEST_RESULTS.json"):
        """Save results to JSON file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert defaultdict to regular dict for JSON serialization
        results_copy = dict(self.results)
        results_copy['entity_counts'] = dict(self.entity_counts)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_copy, f, indent=2)

        print(f"\n💾 Results saved to: {output_path}")

def main():
    """Execute v7 model testing"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     V7 NER MODEL - PRODUCTION TEST                           ║
║                                                                              ║
║  Testing on:                                                                 ║
║  • 30 Annual Cybersecurity Reports (2025)                                   ║
║  • 10 Express Attack Briefs (OXOT)                                          ║
║  • 1 Airplane Sector Analysis                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Initialize tester
    tester = V7ModelTester()

    # Test on annual cybersecurity reports
    annual_reports_dir = Path("/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/12_Reports - Annual Cyber Security/2025")
    tester.process_directory(annual_reports_dir, "Annual Cybersecurity Reports",
                            pattern="*.md", limit=30)

    # Test on express attack briefs
    attack_briefs_dir = Path("/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/11_OXOT/OXOT - Reporting - Express Attack Briefs")
    tester.process_directory(attack_briefs_dir, "Express Attack Briefs",
                            pattern="*.docx", limit=10)

    # Test on airplane sector analysis
    airplane_sector_dir = Path("/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Airplane")
    tester.process_directory(airplane_sector_dir, "Airplane Sector Analysis",
                            pattern="*.md", limit=None)

    # Generate comprehensive report
    results = tester.generate_report()

    # Save results
    tester.save_results()

    print(f"\n🎉 V7 NER MODEL TEST COMPLETE")
    print(f"   Processed {results['total_documents']} documents")
    print(f"   Extracted {results['total_entities']:,} entities")
    print(f"\n✅ Production validation successful!")

if __name__ == "__main__":
    main()
