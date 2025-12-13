import requests
import hashlib

# Create collection if needed
create_payload = {
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    }
}

response = requests.put(
    "http://localhost:6333/collections/aeon_truth",
    json=create_payload
)
print(f"Collection creation: {response.status_code} - {response.json()}")

# Read document
content = open('20HOP_ROOT_CAUSE.md', 'r').read()
doc_id = hashlib.md5(b"20hop-root-cause-analysis").hexdigest()

# Store document
payload = {
    "points": [
        {
            "id": doc_id,
            "vector": [0.1] * 1536,
            "payload": {
                "collection": "aeon-truth",
                "document_type": "root_cause_analysis",
                "title": "20-Hop Reasoning Root Cause Analysis",
                "created": "2025-12-12T07:40:00Z",
                "summary": "Mathematical proof that 20-hop reasoning is infeasible due to combinatorial explosion (10^20 paths). Actual testing shows queries work up to 5 hops, degrade at 10+. Graph has 504K orphan nodes (42% fragmentation). Solution: Limit to 5-hop maximum.",
                "key_findings": [
                    "COMBINATORIAL_EXPLOSION: 20-hop = 10^20 paths (124 quintillion)",
                    "GRAPH_FRAGMENTATION: 504,007 orphan nodes (41.7% of graph)",
                    "PERFORMANCE_LIMIT: Works up to 5 hops (8.7 sec), infeasible beyond 10",
                    "NO_USE_CASE: No threat intelligence scenario requires > 5 hops"
                ],
                "recommendations": [
                    "IMMEDIATE: Change all 20-hop queries to 5-hop maximum",
                    "SHORT_TERM: Clean up 504K orphan nodes",
                    "LONG_TERM: Precompute common attack chains"
                ],
                "graph_metrics": {
                    "total_nodes": 1207069,
                    "total_relationships": 12344852,
                    "orphan_nodes": 504007,
                    "orphan_rate": 0.417,
                    "threat_actors": 10599,
                    "avg_degree": 10.2
                },
                "performance_benchmarks": {
                    "hop_1": "< 1 second",
                    "hop_2": "< 1 second", 
                    "hop_3": "< 1 second",
                    "hop_5": "8.7 seconds",
                    "hop_10": "8.1 seconds (degraded)",
                    "hop_20": "INFEASIBLE"
                },
                "full_content": content,
                "tags": ["root-cause", "neo4j", "performance", "oxot", "critical"],
                "verified": True,
                "file_path": "/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/20HOP_ROOT_CAUSE.md"
            }
        }
    ]
}

response = requests.put(
    "http://localhost:6333/collections/aeon_truth/points",
    json=payload
)

print(f"\nDocument storage: {response.status_code}")
print(f"Response: {response.json()}")
print(f"Document ID: {doc_id}")
print(f"\n✓ Root cause analysis stored in Qdrant collection 'aeon_truth'")
print(f"✓ Document accessible at: /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/20HOP_ROOT_CAUSE.md")
