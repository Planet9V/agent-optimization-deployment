"""
Example usage of QdrantMemoryManager
Demonstrates all key features
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from memory.qdrant_memory_manager import QdrantMemoryManager


def main():
    """Demonstrate QdrantMemoryManager functionality"""

    # Initialize memory manager (will use in-memory fallback if Qdrant unavailable)
    print("Initializing QdrantMemoryManager...")
    memory = QdrantMemoryManager(host="localhost", port=6333)

    # Get initial statistics
    print("\n=== Initial Statistics ===")
    stats = memory.get_statistics()
    print(f"Mode: {stats['mode']}")
    print(f"Qdrant Available: {stats['qdrant_available']}")
    print(f"Embeddings Available: {stats['embeddings_available']}")

    # 1. Track agent activities
    print("\n=== Tracking Agent Activities ===")

    activity_id_1 = memory.track_agent_activity(
        agent_name="ClassificationAgent",
        activity_type="document_classification",
        data={
            "file": "contractor_contract_001.pdf",
            "sector": "General Contractor",
            "subsector": "Commercial Construction",
            "confidence": 0.92
        },
        metadata={"model_version": "1.0", "processing_time": 1.2}
    )
    print(f"Tracked activity: {activity_id_1}")

    activity_id_2 = memory.track_agent_activity(
        agent_name="ValidationAgent",
        activity_type="quality_check",
        data={
            "files_checked": 50,
            "errors_found": 2,
            "warnings": 5
        }
    )
    print(f"Tracked activity: {activity_id_2}")

    # 2. Store checkpoints
    print("\n=== Storing Checkpoints ===")

    checkpoint_id = memory.store_checkpoint(
        checkpoint_name="processing_batch_1",
        state_data={
            "total_files": 100,
            "processed_files": 50,
            "current_file": "document_051.pdf",
            "errors": [],
            "started_at": "2025-11-02T10:00:00"
        },
        metadata={"batch_number": 1, "priority": "high"}
    )
    print(f"Stored checkpoint: {checkpoint_id}")

    # 3. Retrieve checkpoint
    print("\n=== Retrieving Checkpoint ===")

    retrieved_checkpoint = memory.retrieve_checkpoint("processing_batch_1")
    if retrieved_checkpoint:
        print(f"Retrieved checkpoint: {retrieved_checkpoint['checkpoint_name']}")
        print(f"State data: {retrieved_checkpoint['state_data']}")

    # 4. Store classification decisions with user feedback
    print("\n=== Storing Classification Decisions ===")

    decision_id_1 = memory.store_classification_decision(
        file_path="documents/contract_abc.pdf",
        sector="General Contractor",
        subsector="Commercial Construction",
        confidence=0.88,
        user_feedback="Correct - this is indeed commercial construction",
        metadata={"corrected": False, "review_required": False}
    )
    print(f"Stored decision: {decision_id_1}")

    decision_id_2 = memory.store_classification_decision(
        file_path="documents/subcontractor_xyz.pdf",
        sector="Subcontractor",
        subsector="Electrical",
        confidence=0.65,
        user_feedback="Incorrect - should be HVAC not Electrical",
        metadata={"corrected": True, "correct_subsector": "HVAC"}
    )
    print(f"Stored decision: {decision_id_2}")

    # 5. Get agent history
    print("\n=== Agent History ===")

    classification_history = memory.get_agent_history("ClassificationAgent", limit=10)
    print(f"ClassificationAgent history: {len(classification_history)} activities")
    for activity in classification_history:
        print(f"  - {activity['activity_type']} at {activity['timestamp']}")

    validation_history = memory.get_agent_history("ValidationAgent", limit=10)
    print(f"ValidationAgent history: {len(validation_history)} activities")

    # 6. Store document embeddings (if embeddings available)
    print("\n=== Document Embeddings ===")

    if memory.embedding_model:
        # Generate embedding for a sample document
        sample_text = "This is a commercial construction contract for office building"
        embedding = memory._generate_embedding(sample_text)

        if embedding:
            success = memory.store_document_embedding(
                document_id="doc_001",
                embedding=embedding,
                metadata={
                    "filename": "contract_abc.pdf",
                    "sector": "General Contractor",
                    "text_preview": sample_text[:100]
                }
            )
            print(f"Stored document embedding: {success}")

            # Search for similar documents
            similar_docs = memory.search_similar_documents(embedding, top_k=3)
            print(f"Found {len(similar_docs)} similar documents")
    else:
        print("Embeddings not available - skipping document embedding features")

    # 7. Track multiple activities for workflow
    print("\n=== Workflow Tracking ===")

    workflow_steps = [
        ("PreprocessAgent", "document_extraction", {"pages": 10}),
        ("ClassificationAgent", "sector_classification", {"result": "GC"}),
        ("ValidationAgent", "confidence_check", {"passed": True}),
        ("StorageAgent", "database_insert", {"records": 1})
    ]

    for agent, activity_type, data in workflow_steps:
        activity_id = memory.track_agent_activity(agent, activity_type, data)
        print(f"  {agent} -> {activity_type}: {activity_id}")

    # 8. Final statistics
    print("\n=== Final Statistics ===")

    final_stats = memory.get_statistics()
    if "in_memory_counts" in final_stats:
        print("In-memory storage counts:")
        for collection, count in final_stats["in_memory_counts"].items():
            print(f"  {collection}: {count}")
    elif "collections" in final_stats:
        print("Qdrant collections:")
        for collection, info in final_stats["collections"].items():
            print(f"  {collection}: {info['points_count']} points")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
