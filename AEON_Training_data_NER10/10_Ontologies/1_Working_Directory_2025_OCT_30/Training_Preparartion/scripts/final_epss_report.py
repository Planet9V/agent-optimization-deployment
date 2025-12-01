#!/usr/bin/env python3
"""Generate final EPSS enrichment report"""

from neo4j import GraphDatabase
from datetime import datetime

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def generate_report():
    print("=" * 80)
    print("FIRST.ORG EPSS ENRICHMENT - FINAL REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print("")
    
    with driver.session() as session:
        # Overall statistics
        query = """
        MATCH (c:CVE)
        RETURN
            count(c) AS total_cves,
            count(c.epss_score) AS with_epss,
            count(CASE WHEN c.epss_score IS NULL THEN 1 END) AS without_epss
        """
        result = session.run(query)
        stats = result.single()
        
        total = stats['total_cves']
        with_epss = stats['with_epss']
        without_epss = stats['without_epss']
        coverage_pct = (with_epss / total * 100) if total > 0 else 0
        
        print("COVERAGE STATISTICS:")
        print(f"  Total CVEs in database:     {total:>10,}")
        print(f"  CVEs with EPSS scores:      {with_epss:>10,}")
        print(f"  CVEs without EPSS scores:   {without_epss:>10,}")
        print(f"  EPSS Coverage:              {coverage_pct:>9.2f}%")
        print("")
        
        # Priority distribution
        query = """
        MATCH (c:CVE)
        WHERE c.epss_score IS NOT NULL
        RETURN
            count(CASE WHEN c.priority_tier = 'NOW' THEN 1 END) AS priority_now,
            count(CASE WHEN c.priority_tier = 'NEXT' THEN 1 END) AS priority_next,
            count(CASE WHEN c.priority_tier = 'NEVER' THEN 1 END) AS priority_never,
            count(CASE WHEN c.priority_tier IS NULL THEN 1 END) AS no_priority
        """
        result = session.run(query)
        priority = result.single()
        
        print("PRIORITY TIER DISTRIBUTION:")
        print(f"  NOW (EPSS ≥ 0.7):           {priority['priority_now']:>10,} ({priority['priority_now']/with_epss*100:>5.2f}%)")
        print(f"  NEXT (0.3 ≤ EPSS < 0.7):    {priority['priority_next']:>10,} ({priority['priority_next']/with_epss*100:>5.2f}%)")
        print(f"  NEVER (EPSS < 0.3):         {priority['priority_never']:>10,} ({priority['priority_never']/with_epss*100:>5.2f}%)")
        if priority['no_priority'] > 0:
            print(f"  No priority assigned:       {priority['no_priority']:>10,}")
        print("")
        
        # EPSS score statistics
        query = """
        MATCH (c:CVE)
        WHERE c.epss_score IS NOT NULL
        RETURN
            min(c.epss_score) AS min_score,
            max(c.epss_score) AS max_score,
            avg(c.epss_score) AS avg_score,
            percentileCont(c.epss_score, 0.25) AS q1_score,
            percentileCont(c.epss_score, 0.50) AS median_score,
            percentileCont(c.epss_score, 0.75) AS q3_score,
            percentileCont(c.epss_score, 0.90) AS p90_score,
            percentileCont(c.epss_score, 0.95) AS p95_score,
            percentileCont(c.epss_score, 0.99) AS p99_score
        """
        result = session.run(query)
        scores = result.single()
        
        print("EPSS SCORE STATISTICS:")
        print(f"  Minimum:                    {scores['min_score']:>10.6f}")
        print(f"  25th Percentile (Q1):       {scores['q1_score']:>10.6f}")
        print(f"  Median (Q2):                {scores['median_score']:>10.6f}")
        print(f"  75th Percentile (Q3):       {scores['q3_score']:>10.6f}")
        print(f"  90th Percentile:            {scores['p90_score']:>10.6f}")
        print(f"  95th Percentile:            {scores['p95_score']:>10.6f}")
        print(f"  99th Percentile:            {scores['p99_score']:>10.6f}")
        print(f"  Maximum:                    {scores['max_score']:>10.6f}")
        print(f"  Average:                    {scores['avg_score']:>10.6f}")
        print("")
        
        # Top 10 highest EPSS scores
        query = """
        MATCH (c:CVE)
        WHERE c.epss_score IS NOT NULL
        RETURN c.id AS cve_id, c.epss_score AS epss_score, c.priority_tier AS priority
        ORDER BY c.epss_score DESC
        LIMIT 10
        """
        result = session.run(query)
        top_cves = list(result)
        
        print("TOP 10 HIGHEST EPSS SCORES:")
        for i, record in enumerate(top_cves, 1):
            print(f"  {i:>2}. {record['cve_id']:<20} EPSS: {record['epss_score']:.6f}  [{record['priority']}]")
        print("")
        
        # EPSS update statistics
        query = """
        MATCH (c:CVE)
        WHERE c.epss_updated IS NOT NULL
        RETURN
            min(c.epss_updated) AS oldest_update,
            max(c.epss_updated) AS newest_update,
            count(DISTINCT c.epss_date) AS unique_dates
        """
        result = session.run(query)
        updates = result.single()
        
        print("EPSS UPDATE INFORMATION:")
        if updates['oldest_update']:
            print(f"  Oldest EPSS update:         {updates['oldest_update']}")
            print(f"  Newest EPSS update:         {updates['newest_update']}")
            print(f"  Unique EPSS dates:          {updates['unique_dates']}")
        print("")
        
        # Training readiness assessment
        print("TRAINING READINESS ASSESSMENT:")
        print(f"  ✓ EPSS coverage: {coverage_pct:.2f}% (target: 100%)")
        
        if coverage_pct >= 95:
            print(f"  ✓ Coverage threshold met (≥95%)")
        else:
            print(f"  ✗ Coverage threshold NOT met (<95%)")
        
        if priority['priority_now'] > 0:
            print(f"  ✓ HIGH priority CVEs identified: {priority['priority_now']:,}")
        
        if priority['priority_next'] > 0:
            print(f"  ✓ MEDIUM priority CVEs identified: {priority['priority_next']:,}")
        
        print("")
        print("RECOMMENDATION:")
        if coverage_pct >= 94:
            print("  Database is READY for prioritized NER training.")
            print("  Recommended approach:")
            print("    1. Train on NOW tier first (highest impact)")
            print("    2. Expand to NEXT tier for comprehensive coverage")
            print("    3. Use NEVER tier for background training if needed")
        else:
            print(f"  WARNING: {without_epss:,} CVEs missing EPSS scores")
            print("  Recommend investigating missing CVEs before training")
        
    print("")
    print("=" * 80)

if __name__ == "__main__":
    generate_report()
    driver.close()
