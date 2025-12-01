// 4. CREATE CAPEC→OWASP RELATIONSHIPS
// Total: 39 relationships
// ========================================


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MERGE (owasp:OWASPCategory {name: "Buffer Overflow via Environment Variables"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MERGE (owasp:OWASPCategory {name: "Buffer overflow attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-101'})
MERGE (owasp:OWASPCategory {name: "Server-Side Includes (SSI) Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-103'})
MERGE (owasp:OWASPCategory {name: "Clickjacking"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-107'})
MERGE (owasp:OWASPCategory {name: "Cross Site Tracing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-112'})
MERGE (owasp:OWASPCategory {name: "Brute force attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-125'})
MERGE (owasp:OWASPCategory {name: "Traffic flood"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-126'})
MERGE (owasp:OWASPCategory {name: "Path Traversal"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-135'})
MERGE (owasp:OWASPCategory {name: "Format string attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-136'})
MERGE (owasp:OWASPCategory {name: "LDAP Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-141'})
MERGE (owasp:OWASPCategory {name: "Cache Poisoning"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-148'})
MERGE (owasp:OWASPCategory {name: "Content Spoofing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-168'})
MERGE (owasp:OWASPCategory {name: "Windows alternate data stream"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-176'})
MERGE (owasp:OWASPCategory {name: "Setting Manipulation"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-240'})
MERGE (owasp:OWASPCategory {name: "Resource Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-242'})
MERGE (owasp:OWASPCategory {name: "Code Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-248'})
MERGE (owasp:OWASPCategory {name: "Command Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-268'})
MERGE (owasp:OWASPCategory {name: "Log Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-460'})
MERGE (owasp:OWASPCategory {name: "Web Parameter Tampering"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-492'})
MERGE (owasp:OWASPCategory {name: "Regular expression Denial of Service - ReDoS"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MERGE (owasp:OWASPCategory {name: "Embedding Null Code"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-587'})
MERGE (owasp:OWASPCategory {name: "Cross Frame Scripting"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-588'})
MERGE (owasp:OWASPCategory {name: "Reflected DOM Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MERGE (owasp:OWASPCategory {name: "Session Prediction"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-593'})
MERGE (owasp:OWASPCategory {name: "Session hijacking attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MERGE (owasp:OWASPCategory {name: "Credential stuffing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-61'})
MERGE (owasp:OWASPCategory {name: "Session fixation"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-62'})
MERGE (owasp:OWASPCategory {name: "Cross Site Request Forgery (CSRF)"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-63'})
MERGE (owasp:OWASPCategory {name: "Cross Site Scripting (XSS)"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-642'})
MERGE (owasp:OWASPCategory {name: "Binary planting"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-66'})
MERGE (owasp:OWASPCategory {name: "SQL Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-662'})
MERGE (owasp:OWASPCategory {name: "Man-in-the-browser attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MERGE (owasp:OWASPCategory {name: "Blind SQL Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MERGE (owasp:OWASPCategory {name: "Unicode Encoding"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MERGE (owasp:OWASPCategory {name: "Blind XPath Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MERGE (owasp:OWASPCategory {name: "XPATH Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-87'})
MERGE (owasp:OWASPCategory {name: "Forced browsing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MERGE (owasp:OWASPCategory {name: "Man-in-the-middle attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-97'})
MERGE (owasp:OWASPCategory {name: "Cryptanalysis"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";
