# CybersecurityKB Quick Start Guide

**Status**: ✅ Fully Operational
**Last Updated**: 2025-01-26

---

## 🚀 Quick Access

### Python Query Interface
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/solver
python3 query_interface.py
```

### Neo4j Browser
Open: http://localhost:7474
- Username: `neo4j`
- Password: `neo4j@openspg`
- Database: `neo4j`

### Cypher Queries
```bash
docker exec -it openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j
```

---

## 📊 What's Inside

**Total**: 3,470 entities | 26,000+ relationships

- 1,379 CWE Weaknesses
- 823 ATT&CK Techniques
- 667 Malware
- 268 Mitigations
- 181 Threat Actors
- 91 Tools
- 47 Campaigns
- 14 Tactics

---

## 🔍 Common Queries

### Find credential access techniques
```cypher
MATCH (at:AttackTechnique {namespace: 'CybersecurityKB'})
WHERE at.tactic = 'credential-access'
RETURN at.external_id, at.name
ORDER BY at.name
LIMIT 10;
```

### Find threat actor techniques
```cypher
MATCH (ta:ThreatActor {namespace: 'CybersecurityKB'})-[r:RELATED_TO]->(at:AttackTechnique)
WHERE ta.name CONTAINS 'APT' AND r.type = 'uses'
RETURN ta.name, collect(at.name)[..10] as techniques
LIMIT 5;
```

### Find most effective mitigations
```cypher
MATCH (coa:CourseOfAction {namespace: 'CybersecurityKB'})-[r:RELATED_TO]->(at:AttackTechnique)
WHERE r.type = 'mitigates'
RETURN coa.name, count(at) as techniques_covered
ORDER BY techniques_covered DESC
LIMIT 10;
```

---

## 🐍 Python API Examples

```python
from solver.query_interface import CybersecurityKB

kb = CybersecurityKB()

# Statistics
stats = kb.get_statistics()
print(f"Total: {stats['total']} entities")

# Find techniques
cred_techniques = kb.find_techniques_by_tactic('credential-access')
for t in cred_techniques[:5]:
    print(f"{t['technique_id']}: {t['name']}")

# Threat actor analysis
threat = kb.get_threat_actor_techniques('APT28')
if threat:
    print(f"{threat['threat_actor']}: {len(threat['techniques'])} techniques")

# Top mitigations
mitigations = kb.get_most_effective_mitigations(limit=5)
for m in mitigations:
    print(f"{m['mitigation']}: {m['techniques_covered']} techniques")

kb.close()
```

---

## 📁 File Locations

### Import Scripts
```
/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder/
├── import_attack.py  # ATT&CK import
├── import_cwe.py     # CWE import
└── import_cve.py     # CVE import (NVD API)
```

### Query Tools
```
/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/solver/
├── cybersecurity_queries.cypher  # 50+ example queries
└── query_interface.py            # Python API
```

### Schema
```
/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/schema/
└── create_neo4j_schema.cypher    # Schema definition
```

### Documentation
```
/home/jim/2_OXOT_Projects_Dev/docs/
├── CybersecurityKB_Complete.md           # Full documentation
├── Phase3_Schema_Verification.md         # Schema details
├── Neo4j_Direct_Approach.md              # Implementation approach
└── Cybersecurity_KB_Implementation_Plan.md  # Original plan
```

---

## 🔄 Re-import Data

### Update ATT&CK Data
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder

# Download latest
curl -L -o data/raw/enterprise-attack.json \
  "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# Import
python3 import_attack.py
```

### Update CWE Data
```bash
# Download latest
curl -L -o data/raw/cwe-list.xml \
  "https://cwe.mitre.org/data/xml/cwec_latest.xml.zip"

# Extract
python3 -c "
import zipfile
with zipfile.ZipFile('data/raw/cwe-list.xml', 'r') as z:
    z.extractall('data/raw/')
"

# Import
python3 import_cwe.py
```

### Import Recent CVEs
```bash
# Requires NVD API key in import_cve.py
python3 import_cve.py --days 30 --max-results 200
```

---

## 🎯 Top Insights

### Most Used Techniques
1. T1105 - Ingress Tool Transfer (483 uses)
2. T1082 - System Information Discovery (421 uses)
3. T1071.001 - Web Protocols (391 uses)

### Best Mitigations
1. User Account Management (117 techniques)
2. Privileged Account Management (111 techniques)
3. Audit (106 techniques)

### Tactics Coverage
- Defense Evasion: 223 techniques
- Persistence: 121 techniques
- Credential Access: 74 techniques

---

## 🛠️ Troubleshooting

### Connection Issues
```bash
# Check Neo4j status
docker ps | grep openspg-neo4j

# Check Neo4j logs
docker logs openspg-neo4j
```

### Query Performance
All indexes are in place. For slow queries:
- Add `LIMIT` clauses
- Use `EXPLAIN` to analyze query plans
- Check index usage with `PROFILE`

### Memory Issues
Neo4j configured with:
- Heap: 2G-4G
- Page Cache: 2G

---

## 📚 Documentation

- **Full Guide**: `/docs/CybersecurityKB_Complete.md`
- **Schema Details**: `/docs/Phase3_Schema_Verification.md`
- **Query Examples**: `/solver/cybersecurity_queries.cypher`
- **Python API**: `/solver/query_interface.py`

---

## ✅ Verification

```bash
# Count entities
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n {namespace: 'CybersecurityKB'}) RETURN count(*) as total;"

# Expected: 3470

# Check indexes
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "SHOW INDEXES WHERE name STARTS WITH 'cybersec' YIELD name RETURN count(name) as index_count;"

# Expected: 58
```

---

**Status**: System operational and ready for use! 🚀
