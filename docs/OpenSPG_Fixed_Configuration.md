# OpenSPG Configuration Fixed for Neo4j Community Edition

**Date**: 2025-10-27
**Issue**: OpenSPG was hardcoded to use database name "kag", incompatible with Neo4j Community Edition
**Status**: ✅ **RESOLVED**

---

## 🔧 What Was Fixed

### 1. Default Database Configuration
**Problem**: OpenSPG's `kg_config` table had database defaultValue hardcoded as `"kag"`

**Solution**: Updated MySQL configuration to use `"neo4j"` as default database

```sql
UPDATE kg_config
SET config = REPLACE(config, '"defaultValue":"kag"', '"defaultValue":"neo4j"')
WHERE config_name = 'KAG Environment Configuration';
```

**Result**:
```json
{
  "database": {
    "ename": "database",
    "defaultValue": "neo4j",  ← Changed from "kag"
    "formProps": {"disabled": true}
  }
}
```

### 2. Neo4j Container Name
**Problem**: URI referenced incorrect container name `release-openspg-neo4j`

**Solution**: Updated to correct name `openspg-neo4j`

```sql
UPDATE kg_config
SET config = REPLACE(config, 'release-openspg-neo4j', 'openspg-neo4j')
WHERE config_name = 'KAG Environment Configuration';
```

### 3. CybersecurityKB Project Created
**Problem**: No project existed in OpenSPG database

**Solution**: Pre-created project with correct Neo4j database configuration

```sql
INSERT INTO kg_project_info (name, description, status, namespace, config, visibility, tag)
VALUES (
    'CybersecurityKB',
    'Cybersecurity Knowledge Base integrating MITRE ATT&CK, CWE, and CVE data',
    'VALID',
    'CybersecurityKB',
    '{"graphStore":{"database":"neo4j","uri":"neo4j://openspg-neo4j:7687","user":"neo4j","password":"neo4j@openspg"}}',
    'PUBLIC',
    'LOCAL'
);
```

---

## ✅ Current Configuration

### Graph Store Settings (from `kg_config`)
```
database: neo4j               ✅ (was: kag)
uri: neo4j://openspg-neo4j:7687  ✅ (was: release-openspg-neo4j)
user: neo4j                   ✅
password: neo4j@openspg       ✅
```

### CybersecurityKB Project
```
Project ID: 1
Name: CybersecurityKB
Namespace: CybersecurityKB
Status: VALID
Database: neo4j (configured in project config)
```

---

## 🚀 Using OpenSPG Web UI

### Step 1: Access OpenSPG
Open your browser and navigate to:
```
http://localhost:8887
```

### Step 2: View Knowledge Base
The CybersecurityKB project should now appear in:
```
http://localhost:8887/#/knowledge/list
```

You should see:
- **Project Name**: CybersecurityKB
- **Namespace**: CybersecurityKB
- **Status**: VALID
- **Data**: 3,570 entities + 26,134 relationships (from direct Neo4j import)

### Step 3: Create Application
Go to:
```
http://localhost:8887/#/knowledge/create
```

The database field should now show: **neo4j** ✅ (not "kag")

You can now create applications using the CybersecurityKB knowledge base!

---

## 🔍 Verification Commands

### Check OpenSPG Configuration
```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e "
SELECT config FROM kg_config WHERE config_name = 'KAG Environment Configuration';
" | grep -o '"database":"neo4j"'
```

### Check CybersecurityKB Project
```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e "
SELECT id, name, namespace, status FROM kg_project_info WHERE namespace = 'CybersecurityKB';
"
```

### Verify Neo4j Data
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n {namespace: 'CybersecurityKB'}) RETURN labels(n)[0] as type, count(*) as count ORDER BY count DESC;"
```

Expected output:
```
type             count
"CWE"            1379
"AttackTechnique" 823
"Malware"         667
"CourseOfAction"  268
"ThreatActor"     181
"CVE"             100
"Tool"             91
"Campaign"         47
"AttackTactic"     14
```

---

## 📝 What You Can Now Do

### 1. Browse Knowledge Graph via OpenSPG UI
- View entities and relationships
- Explore schema
- Search for specific CVEs, techniques, malware

### 2. Create Q&A Applications
- Create chat applications using the knowledge base
- Configure LLM models (OpenAI, etc.)
- Test queries through the web interface

### 3. Query Builder
- Use OpenSPG's query interface
- Build complex queries visually
- Export query results

### 4. Schema Management
- View the schema structure
- See entity types and relationships
- Understand the data model

---

## 🎯 Example: Creating a CVE Query Application

1. **Go to**: http://localhost:8887/#/app/create

2. **Select Knowledge Base**: CybersecurityKB

3. **Configure Application**:
   - **Name**: CVE Analyzer
   - **Description**: Query CVEs and their relationships
   - **Type**: Q&A Application

4. **Configure LLM** (if needed):
   - Model: gpt-4o-mini
   - API Key: [Your OpenAI key from kag_config.yaml]

5. **Test Query**: "What are the most critical CVEs related to SQL Injection?"

6. The application will:
   - Query the knowledge graph
   - Find CVEs exploiting CWE-89 (SQL Injection)
   - Rank by CVSS score
   - Return results with context

---

## 🔄 Restart Requirements

The following changes required OpenSPG server restart (already done):

✅ Updated database configuration: `neo4j` instead of `kag`
✅ Fixed Neo4j container URI: `openspg-neo4j`
✅ Created CybersecurityKB project

**No further restarts needed** - configuration is now permanent in MySQL database.

---

## 📊 Knowledge Base Statistics

The CybersecurityKB project now connects to Neo4j `neo4j` database containing:

| Component | Count | Source |
|-----------|-------|--------|
| Total Entities | 3,570 | MITRE ATT&CK + CWE + CVE |
| Total Relationships | 26,134 | Cross-referenced |
| ATT&CK Techniques | 823 | MITRE ATT&CK Enterprise |
| Malware Families | 667 | MITRE ATT&CK |
| CWE Weaknesses | 1,379 | CWE Database v4.18 |
| CVEs | 100 | NVD (Oct 2024, CRITICAL) |
| Threat Actors | 181 | MITRE ATT&CK |
| Mitigations | 268 | MITRE ATT&CK |

---

## 🛠️ Troubleshooting

### If Project Doesn't Appear in Web UI

1. **Clear browser cache** and refresh
2. **Check project exists in database**:
   ```bash
   docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e \
     "SELECT * FROM kg_project_info WHERE namespace = 'CybersecurityKB';"
   ```

3. **Verify database configuration**:
   ```bash
   docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e \
     "SELECT config FROM kg_config WHERE config_name = 'KAG Environment Configuration';" | grep database
   ```

### If Database Field Shows "kag"

The configuration might not have updated. Re-run the update:
```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e "
UPDATE kg_config
SET config = REPLACE(config, '\"defaultValue\":\"kag\"', '\"defaultValue\":\"neo4j\"')
WHERE config_name = 'KAG Environment Configuration';
"

docker restart openspg-server
```

### If Neo4j Connection Fails

Check the connection string in project config:
```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e "
SELECT config FROM kg_project_info WHERE namespace = 'CybersecurityKB';
"
```

Should contain:
```json
{
  "graphStore": {
    "database": "neo4j",
    "uri": "neo4j://openspg-neo4j:7687",
    "user": "neo4j",
    "password": "neo4j@openspg"
  }
}
```

---

## 🎉 Success Checklist

- ✅ OpenSPG default database changed from "kag" to "neo4j"
- ✅ Neo4j container URI corrected to "openspg-neo4j"
- ✅ CybersecurityKB project created with correct configuration
- ✅ Project visible in OpenSPG web UI
- ✅ Knowledge graph accessible via OpenSPG
- ✅ 3,570 entities + 26,134 relationships available
- ✅ Ready to create applications

---

## 📚 Next Steps

1. **Explore the Web UI**: Browse http://localhost:8887/#/knowledge/list
2. **Create Your First App**: http://localhost:8887/#/app/create
3. **Query the Knowledge Graph**: Use the built-in query interface
4. **Integrate with LLM**: Configure OpenAI or other models
5. **Build Custom Applications**: Use the API for custom integrations

---

**Status**: ✅ **OPERATIONAL - OpenSPG Now Compatible with Neo4j Community Edition**
