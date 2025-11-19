#!/usr/bin/env python3
"""
Store Expert Agent Registry in Qdrant
Stores detailed expert capabilities and metadata
"""

import sys
import os
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = "implementation_docs"

def store_expert_registry():
    """Store expert agent registry with embeddings"""

    # Initialize services
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Ensure collection exists
    try:
        client.get_collection(COLLECTION_NAME)
        print(f"✓ Collection '{COLLECTION_NAME}' exists")
    except Exception:
        print(f"Creating collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"✓ Collection created")

    # Define expert agents
    experts = [
        {
            "name": "Dr. Sarah Chen",
            "role": "Data Scientist",
            "expertise": ["machine learning", "data analysis", "statistical modeling", "Python", "scikit-learn"],
            "specialty": "Advanced analytics and predictive modeling",
            "experience_years": 12,
            "projects_completed": 87,
            "success_rate": 0.94
        },
        {
            "name": "Marcus Rodriguez",
            "role": "Frontend Developer",
            "expertise": ["React", "TypeScript", "UI/UX design", "responsive design", "accessibility"],
            "specialty": "Modern web interfaces and user experience",
            "experience_years": 8,
            "projects_completed": 134,
            "success_rate": 0.91
        },
        {
            "name": "Dr. Emily Watson",
            "role": "Backend Architect",
            "expertise": ["Python", "FastAPI", "microservices", "database design", "API development"],
            "specialty": "Scalable backend systems and APIs",
            "experience_years": 15,
            "projects_completed": 95,
            "success_rate": 0.96
        },
        {
            "name": "James Park",
            "role": "DevOps Engineer",
            "expertise": ["Docker", "Kubernetes", "CI/CD", "cloud infrastructure", "monitoring"],
            "specialty": "Infrastructure automation and deployment",
            "experience_years": 10,
            "projects_completed": 112,
            "success_rate": 0.93
        },
        {
            "name": "Dr. Aisha Patel",
            "role": "Security Specialist",
            "expertise": ["cybersecurity", "penetration testing", "OAuth", "encryption", "compliance"],
            "specialty": "Application security and threat mitigation",
            "experience_years": 11,
            "projects_completed": 68,
            "success_rate": 0.97
        },
        {
            "name": "Tom Anderson",
            "role": "Database Administrator",
            "expertise": ["PostgreSQL", "Neo4j", "Qdrant", "query optimization", "data modeling"],
            "specialty": "Database performance and architecture",
            "experience_years": 14,
            "projects_completed": 89,
            "success_rate": 0.95
        },
        {
            "name": "Lisa Thompson",
            "role": "QA Engineer",
            "expertise": ["testing", "Playwright", "CI/CD", "test automation", "quality assurance"],
            "specialty": "Comprehensive testing and quality control",
            "experience_years": 9,
            "projects_completed": 156,
            "success_rate": 0.92
        },
        {
            "name": "Dr. David Kim",
            "role": "AI Research Scientist",
            "expertise": ["NLP", "embeddings", "vector databases", "semantic search", "AI systems"],
            "specialty": "AI-powered search and knowledge systems",
            "experience_years": 13,
            "projects_completed": 72,
            "success_rate": 0.95
        }
    ]

    print("=" * 80)
    print("EXPERT AGENT REGISTRY STORAGE")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Total Experts: {len(experts)}")
    print()

    # Store each expert
    stored_count = 0
    import hashlib

    for expert in experts:
        # Create description for embedding
        description = (
            f"{expert['name']}, {expert['role']}. "
            f"Expertise: {', '.join(expert['expertise'])}. "
            f"Specialty: {expert['specialty']}. "
            f"{expert['experience_years']} years experience, "
            f"{expert['projects_completed']} projects, "
            f"{expert['success_rate']*100:.1f}% success rate."
        )

        # Generate embedding
        embedding = model.encode(description).tolist()

        # Generate numeric ID from name hash
        name_hash = hashlib.md5(expert['name'].encode()).hexdigest()
        point_id = int(name_hash[:8], 16)  # Use first 8 hex chars as integer

        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "type": "expert_agent",
                "name": expert["name"],
                "role": expert["role"],
                "expertise": expert["expertise"],
                "specialty": expert["specialty"],
                "experience_years": expert["experience_years"],
                "projects_completed": expert["projects_completed"],
                "success_rate": expert["success_rate"],
                "content": description,
                "stored_at": datetime.now().isoformat()
            }
        )

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )

        stored_count += 1
        print(f"✓ Stored: {expert['name']} ({expert['role']})")
        print(f"  Expertise: {', '.join(expert['expertise'][:3])}...")
        print(f"  Embedding dimensions: {len(embedding)}")
        print()

    print("=" * 80)
    print(f"EXPERT REGISTRY STORAGE COMPLETE")
    print(f"Total experts stored: {stored_count}")
    print(f"Collection: implementation_docs")
    print(f"Embedding model: all-MiniLM-L6-v2 (384 dimensions)")
    print("=" * 80)

    return stored_count

if __name__ == "__main__":
    try:
        count = store_expert_registry()
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
