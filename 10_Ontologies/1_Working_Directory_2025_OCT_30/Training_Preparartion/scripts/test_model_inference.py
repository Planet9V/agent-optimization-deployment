#!/usr/bin/env python3
"""
Quick inference test for v6 NER model
Tests on real critical infrastructure documents
"""
import spacy
from pathlib import Path
from collections import defaultdict
import json

def test_inference(model_path: str, test_doc_path: str):
    """Test model on a real document"""

    print("=" * 80)
    print("V6 NER MODEL INFERENCE TEST")
    print("=" * 80)

    # Load model
    print(f"\n📦 Loading model from: {model_path}")
    nlp = spacy.load(model_path)
    print(f"✅ Model loaded: {len(nlp.pipe_names)} components")

    # Read test document
    print(f"\n📄 Reading test document: {test_doc_path}")
    with open(test_doc_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"✅ Document loaded: {len(text)} characters, ~{len(text.split())} words")

    # Process document
    print(f"\n🔍 Processing document...")
    doc = nlp(text)

    # Collect entities by type
    entities_by_type = defaultdict(list)
    for ent in doc.ents:
        entities_by_type[ent.label_].append(ent.text)

    # Display results
    print(f"\n📊 EXTRACTION RESULTS")
    print("=" * 80)
    print(f"Total entities found: {len(doc.ents)}")
    print(f"Unique entity types: {len(entities_by_type)}")
    print()

    # Show by category
    categories = {
        "Critical Infrastructure": ["VENDOR", "EQUIPMENT", "PROTOCOL", "OPERATION", "ARCHITECTURE", "SUPPLIER"],
        "Cybersecurity": ["SECURITY", "VULNERABILITY", "WEAKNESS", "MITIGATION"],
        "Threat Intelligence": ["THREAT_MODEL", "TACTIC", "TECHNIQUE", "ATTACK_PATTERN", "INDICATOR"],
        "Attribution": ["THREAT_ACTOR", "CAMPAIGN"],
        "Technical Components": ["SOFTWARE_COMPONENT", "HARDWARE_COMPONENT"],
        "Human Factors": ["PERSONALITY_TRAIT", "COGNITIVE_BIAS", "INSIDER_INDICATOR", "SOCIAL_ENGINEERING", "ATTACK_VECTOR"]
    }

    for category, entity_types in categories.items():
        category_entities = {et: entities_by_type.get(et, []) for et in entity_types if et in entities_by_type}
        if category_entities:
            print(f"\n🏷️  {category.upper()}")
            print("-" * 80)
            for entity_type, entities in sorted(category_entities.items(), key=lambda x: -len(x[1])):
                unique_entities = list(dict.fromkeys(entities))  # Preserve order, remove duplicates
                print(f"  {entity_type:20s} ({len(entities):3d}): {', '.join(unique_entities[:5])}")
                if len(unique_entities) > 5:
                    print(f"{' ' * 27}...and {len(unique_entities) - 5} more")

    # Show sample extractions with context
    print(f"\n\n📝 SAMPLE EXTRACTIONS WITH CONTEXT")
    print("=" * 80)

    # Get top entity types by count
    top_types = sorted(entities_by_type.items(), key=lambda x: -len(x[1]))[:5]

    for entity_type, entities in top_types[:3]:  # Show top 3 types
        print(f"\n{entity_type}:")
        # Show first 3 unique entities with context
        seen = set()
        count = 0
        for ent in doc.ents:
            if ent.label_ == entity_type and ent.text not in seen and count < 3:
                seen.add(ent.text)
                count += 1
                # Get surrounding context
                start = max(0, ent.start_char - 50)
                end = min(len(text), ent.end_char + 50)
                context = text[start:end].replace('\n', ' ')
                # Highlight entity
                context = context.replace(ent.text, f"**{ent.text}**")
                print(f"  • ...{context}...")

    # Performance by category
    print(f"\n\n📈 EXPECTED PERFORMANCE BY CATEGORY")
    print("=" * 80)

    performance_tiers = {
        "Excellent (F1 ≥ 90%)": {
            "count": 19,
            "examples": ["SECURITY (98.17%)", "TACTIC (98.75%)", "TECHNIQUE (94.62%)",
                        "EQUIPMENT (91.09%)", "PROTOCOL (92.64%)"]
        },
        "Good (F1 80-89%)": {
            "count": 1,
            "examples": ["ATTACK_PATTERN (81.63%)"]
        },
        "Use with Caution (F1 < 50%)": {
            "count": 3,
            "examples": ["VENDOR (36.14%)", "VULNERABILITY (31.25%)", "INDICATOR (25.99%)"]
        }
    }

    for tier, info in performance_tiers.items():
        print(f"\n{tier}: {info['count']} entity types")
        for example in info['examples']:
            print(f"  • {example}")

    print("\n" + "=" * 80)
    print("✅ INFERENCE TEST COMPLETE")
    print("=" * 80)

    # Save results
    results = {
        "document": str(test_doc_path),
        "total_entities": len(doc.ents),
        "unique_types": len(entities_by_type),
        "entities_by_type": {k: len(v) for k, v in entities_by_type.items()},
        "sample_entities": {k: list(dict.fromkeys(v))[:10] for k, v in entities_by_type.items()}
    }

    return results

if __name__ == "__main__":
    # Find model
    model_path = Path("ner_model")

    # Find a test document
    test_docs = list(Path("Energy_Sector").glob("*.md"))
    if not test_docs:
        # Try other sectors
        for sector in ["Communications_Sector", "Chemical_Sector", "Healthcare_Sector"]:
            test_docs = list(Path(sector).glob("*.md"))
            if test_docs:
                break

    if not test_docs:
        print("❌ No test documents found!")
        exit(1)

    test_doc = test_docs[0]

    # Run test
    results = test_inference(str(model_path), str(test_doc))

    # Save results
    with open("inference_test_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: inference_test_results.json")
