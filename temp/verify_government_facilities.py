#!/usr/bin/env python3
"""Verify GOVERNMENT_FACILITIES deployment"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

queries = {
    "Total GOVERNMENT_FACILITIES nodes": "MATCH (n:GOVERNMENT_FACILITIES) RETURN count(n) as count",
    "GovernmentDevice": "MATCH (n:GovernmentDevice) RETURN count(n) as count",
    "GovernmentMeasurement": "MATCH (n:GovernmentMeasurement) RETURN count(n) as count",
    "GovernmentProperty": "MATCH (n:GovernmentProperty) RETURN count(n) as count",
    "GovernmentProcess": "MATCH (n:GovernmentProcess) RETURN count(n) as count",
    "GovernmentControl": "MATCH (n:GovernmentControl) RETURN count(n) as count",
    "GovernmentAlert": "MATCH (n:GovernmentAlert) RETURN count(n) as count",
    "GovernmentZone": "MATCH (n:GovernmentZone) RETURN count(n) as count",
    "MajorAsset": "MATCH (n:MajorAsset) RETURN count(n) as count",
    "Total relationships": "MATCH (n:GOVERNMENT_FACILITIES)-[r]-() RETURN count(DISTINCT r) as count",
    "Federal_Facilities": "MATCH (n:GOVERNMENT_FACILITIES {subsector: 'Federal_Facilities'}) RETURN count(n) as count",
    "State_Local_Facilities": "MATCH (n:GOVERNMENT_FACILITIES {subsector: 'State_Local_Facilities'}) RETURN count(n) as count",
    "Courts_Legislative": "MATCH (n:GOVERNMENT_FACILITIES {subsector: 'Courts_Legislative'}) RETURN count(n) as count"
}

print("=" * 80)
print("GOVERNMENT_FACILITIES DEPLOYMENT VERIFICATION")
print("=" * 80)

with driver.session() as session:
    for metric, query in queries.items():
        result = session.run(query)
        count = result.single()["count"]
        print(f"{metric:40s}: {count:>10,}")

driver.close()
print("=" * 80)
