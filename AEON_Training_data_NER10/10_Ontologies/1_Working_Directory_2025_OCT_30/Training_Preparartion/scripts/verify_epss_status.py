#!/usr/bin/env python3
"""Verify EPSS enrichment status"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def check_status():
    queries = {
        "Total CVEs": "MATCH (c:CVE) RETURN count(c) AS count",
        "CVEs with valid IDs": "MATCH (c:CVE) WHERE c.cve_id IS NOT NULL RETURN count(c) AS count",
        "CVEs with NULL IDs": "MATCH (c:CVE) WHERE c.cve_id IS NULL RETURN count(c) AS count",
        "CVEs with EPSS": "MATCH (c:CVE) WHERE c.epss_score IS NOT NULL RETURN count(c) AS count",
        "CVEs without EPSS (all)": "MATCH (c:CVE) WHERE c.epss_score IS NULL RETURN count(c) AS count",
        "CVEs without EPSS (valid ID)": "MATCH (c:CVE) WHERE c.epss_score IS NULL AND c.cve_id IS NOT NULL RETURN count(c) AS count",
        "Priority NOW": "MATCH (c:CVE) WHERE c.priority_tier = 'NOW' RETURN count(c) AS count",
        "Priority NEXT": "MATCH (c:CVE) WHERE c.priority_tier = 'NEXT' RETURN count(c) AS count",
        "Priority NEVER": "MATCH (c:CVE) WHERE c.priority_tier = 'NEVER' RETURN count(c) AS count",
    }
    
    print("=" * 60)
    print("EPSS ENRICHMENT STATUS VERIFICATION")
    print("=" * 60)
    
    with driver.session() as session:
        for label, query in queries.items():
            result = session.run(query)
            count = result.single()['count']
            print(f"{label:.<40} {count:>10,}")
    
    # Get EPSS score statistics
    stats_query = """
    MATCH (c:CVE)
    WHERE c.epss_score IS NOT NULL
    RETURN
        min(c.epss_score) AS min_score,
        max(c.epss_score) AS max_score,
        avg(c.epss_score) AS avg_score,
        percentileCont(c.epss_score, 0.5) AS median_score
    """
    
    with driver.session() as session:
        result = session.run(stats_query)
        stats = result.single()
        print("")
        print("EPSS SCORE STATISTICS:")
        print(f"  Minimum: {stats['min_score']:.6f}")
        print(f"  Maximum: {stats['max_score']:.6f}")
        print(f"  Average: {stats['avg_score']:.6f}")
        print(f"  Median: {stats['median_score']:.6f}")
    
    # Sample CVEs without EPSS
    sample_query = """
    MATCH (c:CVE)
    WHERE c.epss_score IS NULL AND c.cve_id IS NOT NULL
    RETURN c.cve_id AS cve_id
    LIMIT 10
    """
    
    with driver.session() as session:
        result = session.run(sample_query)
        samples = [record['cve_id'] for record in result]
        if samples:
            print("")
            print("SAMPLE CVEs WITHOUT EPSS (first 10):")
            for cve_id in samples:
                print(f"  - {cve_id}")
    
    print("=" * 60)

if __name__ == "__main__":
    check_status()
    driver.close()
