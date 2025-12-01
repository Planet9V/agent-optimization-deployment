#!/usr/bin/env python3
"""
Analyze .spacy DocBin files to identify which source documents have zero annotations
This is the ground truth - we'll examine the actual trained data.
"""

import spacy
from spacy.tokens import DocBin
from pathlib import Path
from collections import defaultdict
import json

def analyze_spacy_files():
    """Analyze .spacy files to find documents with zero annotations"""

    base_path = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/ner_training_data")

    # Load blank spaCy model
    nlp = spacy.blank("en")

    results = {
        'train': {'total_docs': 0, 'docs_with_entities': 0, 'docs_without_entities': 0, 'zero_annotation_docs': []},
        'dev': {'total_docs': 0, 'docs_with_entities': 0, 'docs_without_entities': 0, 'zero_annotation_docs': []},
        'test': {'total_docs': 0, 'docs_with_entities': 0, 'docs_without_entities': 0, 'zero_annotation_docs': []}
    }

    entity_stats = defaultdict(int)

    for split_name in ['train', 'dev', 'test']:
        spacy_file = base_path / f"{split_name}.spacy"

        if not spacy_file.exists():
            print(f"⚠️  {spacy_file} not found")
            continue

        print(f"\n{'='*80}")
        print(f"Analyzing {split_name}.spacy")
        print(f"{'='*80}")

        # Load DocBin
        doc_bin = DocBin().from_disk(spacy_file)
        docs = list(doc_bin.get_docs(nlp.vocab))

        results[split_name]['total_docs'] = len(docs)

        print(f"Total documents: {len(docs)}")

        # Analyze each document
        docs_with_zero = []
        for idx, doc in enumerate(docs):
            num_entities = len(doc.ents)

            if num_entities == 0:
                docs_with_zero.append({
                    'index': idx,
                    'text_preview': doc.text[:100] + "..." if len(doc.text) > 100 else doc.text,
                    'text_length': len(doc.text)
                })
                results[split_name]['docs_without_entities'] += 1
            else:
                results[split_name]['docs_with_entities'] += 1

                # Count entity types
                for ent in doc.ents:
                    entity_stats[ent.label_] += 1

        # Store zero annotation docs
        results[split_name]['zero_annotation_docs'] = docs_with_zero

        print(f"Docs WITH entities: {results[split_name]['docs_with_entities']}")
        print(f"Docs WITHOUT entities: {results[split_name]['docs_without_entities']}")

        if docs_with_zero:
            print(f"\nSample documents with ZERO annotations (first 5):")
            for doc_info in docs_with_zero[:5]:
                print(f"   Doc {doc_info['index']}: {doc_info['text_preview']}")

    # Overall statistics
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print(f"{'='*80}")

    total_docs = sum(r['total_docs'] for r in results.values())
    total_with_entities = sum(r['docs_with_entities'] for r in results.values())
    total_without_entities = sum(r['docs_without_entities'] for r in results.values())

    print(f"\nTotal documents across all splits: {total_docs}")
    print(f"Documents WITH entities: {total_with_entities}")
    print(f"Documents WITHOUT entities: {total_without_entities}")
    print(f"Percentage without entities: {(total_without_entities/total_docs*100):.2f}%")

    print(f"\nEntity Type Distribution:")
    for entity_type, count in sorted(entity_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   {entity_type}: {count}")

    # Save results
    output_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/Data Pipeline Builder/SPACY_ANNOTATION_ANALYSIS.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Detailed results saved to: {output_file}")

    # Generate report
    print(f"\n{'='*80}")
    print("KEY FINDING")
    print(f"{'='*80}")

    if total_without_entities > 0:
        print(f"\n⚠️  Found {total_without_entities} documents with ZERO annotations")
        print(f"   These represent {(total_without_entities/total_docs*100):.2f}% of training data")
        print(f"\n   These documents are teaching the model NOT to recognize entities")
        print(f"   (wrong negatives - the core issue causing poor performance)")
    else:
        print(f"\n✅ All documents have at least one entity annotation")
        print(f"   No zero-annotation documents found")

    return results

if __name__ == "__main__":
    analyze_spacy_files()
