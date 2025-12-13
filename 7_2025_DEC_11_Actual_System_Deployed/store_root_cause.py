import requests
import hashlib
from datetime import datetime

# Document content
content = open('20HOP_ROOT_CAUSE.md', 'r').read()

# Create embedding payload
doc_id = hashlib.md5(b"20hop-root-cause-analysis").hexdigest()

payload = {
    "points": [
        {
            "id": doc_id,
            "vector": [0.1] * 1536,  # Placeholder - would use real embeddings in production
            "payload": {
                "collection": "aeon-truth",
                "document_type": "root_cause_analysis",
                "title": "20-Hop Reasoning Root Cause Analysis",
                "created": "2025-12-12T07:40:00Z",
                "findings": [
                    "Combinatorial explosion: 10^20 paths at 20 hops",
                    "Graph fragmentation: 42% orphan nodes (504,007 nodes)",
                    "Performance degradation: Works up to 5 hops, infeasible beyond 10",
                    "No practical use case for > 5 hops"
                ],
                "recommendations": [
                    "Limit all queries to 5-hop maximum",
                    "Clean up 504K orphan nodes",
                    "Use directed path patterns instead of unbounded exploration",
                    "Implement query timeout protection (60 seconds)"
                ],
                "graph_stats": {
                    "total_nodes": 1207069,
                    "total_relationships": 12344852,
                    "orphan_nodes": 504007,
                    "threat_actors": 10599,
                    "avg_relationships_per_node": 10.2
                },
                "performance_data": {
                    "1_hop": "< 1 second",
                    "2_hop": "< 1 second",
                    "3_hop": "< 1 second",
                    "5_hop": "8.7 seconds",
                    "10_hop": "8.1 seconds (degraded results)",
                    "20_hop": "infeasible (combinatorial explosion)"
                },
                "content": content[:50000],  # Store first 50K chars
                "tags": [
                    "root-cause-analysis",
                    "neo4j-performance",
                    "graph-database",
                    "multi-hop-reasoning",
                    "oxot-platform"
                ],
                "status": "CRITICAL_FINDINGS",
                "verified": True,
                "authority": "DIRECT_MEASUREMENT"
            }
        }
    ]
}

# Store in Qdrant
response = requests.put(
    "http://localhost:6333/collections/aeon_truth/points",
    json=payload
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print(f"Document ID: {doc_id}")
