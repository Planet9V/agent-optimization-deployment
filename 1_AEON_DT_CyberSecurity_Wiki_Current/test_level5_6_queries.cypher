// Test 1: Count InformationEvent nodes
MATCH (ie:InformationEvent)
RETURN count(ie) as TotalInformationEvents;

// Test 2: Count CognitiveBias nodes
MATCH (cb:CognitiveBias)
RETURN count(cb) as TotalCognitiveBiases;

// Test 3: Count Prediction nodes
MATCH (pred:Prediction)
RETURN count(pred) as TotalPredictions;

// Test 4: Sample Information Event structure
MATCH (ie:InformationEvent)
RETURN ie LIMIT 1;

// Test 5: Sample CognitiveBias structure
MATCH (cb:CognitiveBias)
RETURN cb LIMIT 1;

// Test 6: Sample Prediction structure
MATCH (pred:Prediction)
RETURN pred LIMIT 1;

// Test 7: Check relationship types for Level 5/6
CALL db.relationshipTypes() YIELD relationshipType
WHERE relationshipType IN ['TRIGGERS', 'CORRELATES_WITH', 'PREDICTS', 'INFLUENCED_BY', 'SIMILAR_TO', 'BASED_ON']
RETURN relationshipType;
