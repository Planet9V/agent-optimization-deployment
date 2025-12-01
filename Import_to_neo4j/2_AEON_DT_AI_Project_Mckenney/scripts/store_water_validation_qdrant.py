#!/usr/bin/env python3
"""Store Water sector validation results in Qdrant."""

import json
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

def main():
    print("Storing Water sector validation results in Qdrant...")

    # Load validation results
    results_file = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/water/validation/validation_results.json")

    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Initialize Qdrant client
    client = QdrantClient(host="localhost", port=6333)

    # Collection name
    collection_name = "sector_validation_results"

    # Check if collection exists, create if not
    try:
        client.get_collection(collection_name)
        print(f"Collection '{collection_name}' exists")
    except Exception:
        print(f"Creating collection '{collection_name}'")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    # Create summary payload
    payload = {
        "sector": "water",
        "validation_date": "2025-11-05",
        "status": "FAILED",
        "f1_score": results["avg_f1_score"],
        "threshold": results["threshold"],
        "passed": results["passed"],
        "test_sections": results["test_sections"],
        "total_patterns": results["total_patterns"],
        "category_results": results["category_results"],
        "data_quality_issues": results["data_quality_issues"],
        "comparison_to_dams": results["comparison_to_dams"],
        "key_findings": {
            "best_category": "scada",
            "best_f1": 0.933,
            "worst_category": "operations",
            "worst_f1": 0.545,
            "missing_categories": ["security", "standards"],
            "duplicate_content": True,
            "source_documents": 2,
            "precision": 1.0,
            "recall_avg": 0.681
        },
        "recommendations": [
            "Obtain 10-15 diverse Water sector documents",
            "Eliminate duplicate content from test set",
            "Add security and standards test materials",
            "Review and improve operations patterns (54.5% F1)",
            "Retest with improved source materials",
            "Target F1 >= 85% on retest"
        ],
        "root_causes": [
            "Limited source diversity (2 docs vs 15+ for Dams)",
            "Duplicate content between source documents",
            "Missing critical categories (security, standards)",
            ".docx format conversion issues",
            "Narrow operational content (Fine Screens only)"
        ]
    }

    # Create a simple embedding (dummy vector for metadata storage)
    # In production, this would be a semantic embedding of the validation summary
    dummy_vector = [0.1] * 384

    # Create point
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=dummy_vector,
        payload=payload
    )

    # Upsert point
    client.upsert(
        collection_name=collection_name,
        points=[point]
    )

    print()
    print("=" * 80)
    print("STORED IN QDRANT")
    print("=" * 80)
    print(f"Collection: {collection_name}")
    print(f"Sector: water")
    print(f"F1 Score: {results['avg_f1_score']:.3f}")
    print(f"Status: {'PASSED' if results['passed'] else 'FAILED'}")
    print(f"Patterns: {results['total_patterns']}")
    print(f"Test Sections: {results['test_sections']}")
    print()
    print("Data Quality Issues:")
    for issue in results["data_quality_issues"]:
        print(f"  - {issue}")
    print()
    print("Comparison to Dams:")
    print(f"  Dams F1:  {results['comparison_to_dams']['dams_f1']:.3f}")
    print(f"  Water F1: {results['comparison_to_dams']['water_f1']:.3f}")
    print(f"  Delta:    {results['comparison_to_dams']['difference']:+.3f}")
    print()

if __name__ == "__main__":
    main()
