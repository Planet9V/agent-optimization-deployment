# OpenSPG with Neo4j Community Edition - Complete Workaround Guide

**Issue**: OpenSPG's Java code is hardcoded to execute `CREATE DATABASE` for each new project
**Impact**: Cannot create new knowledge bases through the OpenSPG UI
**Solution**: Use pre-created projects or add new ones via MySQL

---

## 🚨 The Problem

When you try to create a new knowledge base through the OpenSPG UI (http://localhost:8887/#/knowledge/create), OpenSPG executes:

```cypher
CREATE DATABASE <namespace> IF NOT EXISTS
```

**This fails in Neo4j Community Edition**, which only supports a single database named `neo4j`.

### Error Message
```
unknown error
Unsupported administration command: CREATE DATABASE cybersecurity IF NOT EXISTS
```

### Root Cause
The issue is in OpenSPG's Java code at:
```
com.antgroup.openspg.common.util.neo4j.Neo4jGraphUtils.createDatabase()
```

This code is **hardcoded** and cannot be disabled via configuration parameters.

---

## ✅ Solution: Use Pre-Created Projects

### Option 1: Use CybersecurityKB (Already Created)

I've already created a working project for you:

**Project Details:**
- Name: `CybersecurityKB`
- Namespace: `CybersecurityKB`
- Database: `neo4j`
- Status: `VALID`
- Entities: 3,570
- Relationships: 26,134

**How to Access:**

1. Open OpenSPG: http://localhost:8887
2. Go to Knowledge Base List: http://localhost:8887/#/knowledge/list
3. You should see **CybersecurityKB** in the list
4. Click on it to explore the knowledge graph

**What You Can Do:**
- ✅ View entities (CVEs, ATT&CK techniques, malware, CWEs)
- ✅ Browse relationships
- ✅ Create applications using this knowledge base
- ✅ Query the data through OpenSPG UI
- ✅ Use the REST API

**What You CANNOT Do:**
- ❌ Create NEW knowledge bases through the OpenSPG UI
- ❌ Use OpenSPG's "Create Knowledge Base" button

---

## 🔧 Option 2: Add More Projects via MySQL

If you need additional projects with different namespaces, add them directly to MySQL:

### Quick Method: Use the Helper Script

I've created a helper script for you:

```bash
# Add a new project
/tmp/add_openspg_project.sh "ProjectName" "namespace" "Optional description"

# Example: Add a "Cybersecurity" project
/tmp/add_openspg_project.sh "Cybersecurity" "Cybersecurity" "Cybersecurity Knowledge Base"
```

The script will:
1. Insert the project into OpenSPG's MySQL database
2. Configure it to use the `neo4j` database
3. Set status to `VALID`
4. Display the created project

After running the script:
1. Refresh the OpenSPG UI: http://localhost:8887/#/knowledge/list
2. Your new project will appear in the list
3. You can now use it like CybersecurityKB

### Manual Method: Direct SQL

If you prefer to do it manually:

```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e "
INSERT INTO kg_project_info (name, description, status, namespace, config, visibility, tag)
VALUES (
    'YourProjectName',
    'Your project description',
    'VALID',
    'YourNamespace',
    '{\"graphStore\":{\"database\":\"neo4j\",\"uri\":\"neo4j://openspg-neo4j:7687\",\"user\":\"neo4j\",\"password\":\"neo4j@openspg\"}}',
    'PUBLIC',
    'LOCAL'
);

SELECT id, name, namespace, status FROM kg_project_info;
"
```

**Important**: All projects will use:
- Same Neo4j database: `neo4j`
- Namespace-based isolation (e.g., `namespace='Cybersecurity'`)
- Shared graph, but logically separated by namespace property

---

## 📊 Managing Multiple Projects with Namespace Isolation

Since all projects share the `neo4j` database, you need to use **namespace** to separate data:

### Creating Data for a New Project

When you import data for a new project, always set the namespace:

```python
# Example: Import data for "Cybersecurity" project
query = """
MERGE (cve:CVE {id: $id, namespace: 'Cybersecurity'})
SET cve.description = $description
"""
```

### Querying Data by Namespace

```cypher
// Query CybersecurityKB data
MATCH (n {namespace: 'CybersecurityKB'})
RETURN count(n);

// Query Cybersecurity project data
MATCH (n {namespace: 'Cybersecurity'})
RETURN count(n);
```

### Current Namespaces

Check existing namespaces:

```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n) WHERE n.namespace IS NOT NULL RETURN DISTINCT n.namespace, count(*) ORDER BY count(*) DESC;"
```

Expected output:
```
namespace               count
"CybersecurityKB"       3570
```

---

## 🎯 Step-by-Step: Using OpenSPG with CybersecurityKB

### 1. Access the Knowledge Base

Go to: http://localhost:8887/#/knowledge/list

You should see:
```
┌─────────────────────────────────────────┐
│ CybersecurityKB                         │
│ Namespace: CybersecurityKB              │
│ Status: VALID                           │
│ Database: neo4j                         │
└─────────────────────────────────────────┘
```

### 2. Explore the Data

Click on **CybersecurityKB** to:
- Browse entities (3,570 total)
- View relationships (26,134 total)
- See the schema
- Search for specific items

### 3. Create an Application

Go to: http://localhost:8887/#/app/create

Select **CybersecurityKB** as the knowledge base:
- Configure your application name
- Set up LLM integration (if needed)
- Create Q&A applications
- Build custom queries

### 4. Query the Knowledge Graph

Use OpenSPG's query interface to run Cypher queries:

```cypher
// Find critical CVEs
MATCH (cve:CVE {namespace: 'CybersecurityKB'})
WHERE cve.severity = 'CRITICAL'
RETURN cve.cve_id, cve.cvss_score, cve.description
ORDER BY cve.cvss_score DESC
LIMIT 10;

// Find malware techniques
MATCH (malware:Malware {namespace: 'CybersecurityKB'})-[r:RELATED_TO]->(tech:AttackTechnique)
WHERE r.type = 'uses'
RETURN malware.name, tech.external_id, tech.name
LIMIT 20;

// Find CVE to CWE relationships
MATCH (cve:CVE {namespace: 'CybersecurityKB'})-[:EXPLOITS]->(cwe:CWE)
RETURN cve.cve_id, cwe.cwe_id, cwe.name
ORDER BY cve.cvss_score DESC
LIMIT 15;
```

---

## 🔍 Verification Commands

### Check All Projects in OpenSPG

```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e \
  "SELECT id, name, namespace, status FROM kg_project_info;"
```

### Check Neo4j Data by Namespace

```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n {namespace: 'CybersecurityKB'})
   RETURN labels(n)[0] as type, count(*) as count
   ORDER BY count DESC;"
```

### View OpenSPG Configuration

```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e \
  "SELECT config FROM kg_config WHERE config_name = 'KAG Environment Configuration';" \
  | python3 -c "
import sys, json
data = sys.stdin.read()
json_start = data.find('{')
if json_start >= 0:
    config = json.loads(data[json_start:])
    graph_store = config['configTitle']['graph_store']['title']
    for field in graph_store:
        print(f\"{field['ename']}: {field['defaultValue']}\")
"
```

---

## ⚠️ Limitations

### What Doesn't Work

1. **❌ Creating knowledge bases through OpenSPG UI**
   - The "Create Knowledge Base" button will always fail
   - Error: "CREATE DATABASE not supported"

2. **❌ OpenSPG's built-in project wizard**
   - Cannot use the guided setup
   - Must use pre-created projects

3. **❌ Separate Neo4j databases per project**
   - All projects share the `neo4j` database
   - Isolation via `namespace` property only

### What DOES Work

1. **✅ Using pre-created projects**
   - CybersecurityKB works perfectly
   - Additional projects via MySQL insertion work

2. **✅ All OpenSPG features within a project**
   - Browse knowledge graph
   - Create applications
   - Query data
   - REST API access
   - Schema management

3. **✅ Multiple logical projects**
   - Use namespace-based isolation
   - Each namespace acts like a separate project
   - All in the same `neo4j` database

---

## 🚀 Quick Reference

### Use Existing Project
```
URL: http://localhost:8887/#/knowledge/list
Project: CybersecurityKB
Status: Ready to use
```

### Add New Project
```bash
/tmp/add_openspg_project.sh "ProjectName" "Namespace" "Description"
```

### Verify Data
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n {namespace: 'CybersecurityKB'}) RETURN count(*);"
```

### Check Projects
```bash
docker exec openspg-mysql mysql -uroot -popenspg -D openspg -e \
  "SELECT name, namespace, status FROM kg_project_info;"
```

---

## 📚 Related Documentation

- **OpenSPG Configuration Fix**: `/docs/OpenSPG_Fixed_Configuration.md`
- **Knowledge Base Summary**: `/docs/CybersecurityKB_Complete_Summary.md`
- **Query Examples**: `/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/solver/query_examples.cypher`

---

## 💡 Tips

### Tip 1: Refresh Browser After Adding Projects
After adding a new project via MySQL, refresh the OpenSPG UI to see it appear.

### Tip 2: Use Namespace Consistently
Always include `namespace: 'YourNamespace'` in your Cypher queries to avoid cross-contamination.

### Tip 3: Import Data with Namespace
When importing new data, always set the namespace property:
```python
tx.run("MERGE (n:Entity {id: $id, namespace: $namespace})",
       id=entity_id, namespace='YourNamespace')
```

### Tip 4: Export and Reimport if Needed
If you need true database isolation, you can:
1. Export data from one namespace
2. Set up Neo4j Enterprise Edition
3. Import into separate databases

But for most use cases, namespace isolation is sufficient.

---

## ✅ Success Checklist

- ✅ CybersecurityKB project visible in OpenSPG UI
- ✅ Can browse 3,570 entities
- ✅ Can create applications
- ✅ Can query the knowledge graph
- ✅ Database field shows "neo4j" (not "kag")
- ✅ Understand limitation: Cannot create NEW knowledge bases via UI
- ✅ Know how to add projects via MySQL if needed

---

**Status**: ✅ **OPERATIONAL - OpenSPG works with Neo4j Community Edition using pre-created projects**

**Workaround**: Don't use the "Create Knowledge Base" button - use pre-created projects instead
