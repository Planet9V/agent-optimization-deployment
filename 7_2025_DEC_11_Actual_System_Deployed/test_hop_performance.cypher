// Test 1-hop performance
PROFILE MATCH (ta:ThreatActor)-[r]-(n)
RETURN ta.name, type(r), labels(n)[0] LIMIT 10;

// Test 2-hop performance
PROFILE MATCH path = (ta:ThreatActor)-[*1..2]-(n)
RETURN length(path), ta.name, labels(n)[0] LIMIT 10;

// Test 3-hop performance
PROFILE MATCH path = (ta:ThreatActor)-[*1..3]-(n)
RETURN length(path) LIMIT 10;

// Test 5-hop performance
PROFILE MATCH path = (ta:ThreatActor)-[*1..5]-(n)
RETURN length(path) LIMIT 10;

// Graph health checks
MATCH (n) WHERE NOT (n)--() 
RETURN count(n) as orphan_nodes;

CALL db.relationshipTypes() YIELD relationshipType
RETURN relationshipType, count(*) as usage;

CALL db.indexes() YIELD name, type, labelsOrTypes, properties
RETURN name, type, labelsOrTypes, properties;

// Relationship distribution
MATCH ()-[r]->() 
RETURN type(r) as rel_type, count(r) as count 
ORDER BY count DESC LIMIT 20;

// Check for APOC
RETURN apoc.version() as apoc_version;
