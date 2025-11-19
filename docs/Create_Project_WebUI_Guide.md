# Creating CybersecurityKB Project via OpenSPG Web UI

## Issue: Neo4j Community Edition Limitation

When using `knext project create` or `knext project restore`, OpenSPG tries to execute `CREATE DATABASE` which fails in Neo4j Community Edition.

**Solution:** Create the project through the OpenSPG Web UI, which handles Community Edition correctly.

---

## Step-by-Step Instructions

### Step 1: Access OpenSPG Web UI

1. Open your browser
2. Navigate to: **http://localhost:8887**
3. Login credentials:
   - Username: `openspg`
   - Password: `openspg@kag`

### Step 2: Create New Project

1. Click **"Create Project"** or **"New Knowledge Base"** button
2. Fill in project details:
   - **Project Name**: `CybersecurityKB`
   - **Description**: `Cybersecurity Knowledge Base using Unified Cybersecurity Ontology`
   - **Language**: `English`
   - **Business Scene**: `cybersecurity`

3. Click **"Create"** or **"Confirm"**

### Step 3: Configure Project Settings

Once created, go to project settings and verify/update:

1. **Graph Store Configuration**:
   - Should automatically use the default Neo4j database
   - No manual configuration needed

2. **LLM Configuration** (if prompted):
   - **Provider**: OpenAI
   - **Model**: gpt-4o
   - **API Key**: [Your OpenAI key]
   - **Base URL**: https://api.openai.com/v1

3. **Embedding Configuration** (if prompted):
   - **Provider**: OpenAI
   - **Model**: text-embedding-3-large
   - **API Key**: [Your OpenAI key]
   - **Dimensions**: 3072

### Step 4: Link to Your Local Project

After creating via Web UI, link it to your local project directory:

```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB

# The project now exists in OpenSPG's MySQL database
# Your local files will sync with it when you run builder/solver
```

### Step 5: Verify Project Creation

Check that the project was created successfully:

```bash
# Via CLI
cd /home/jim/2_OXOT_Projects_Dev/KAG
source venv/bin/activate
knext project list

# Via Neo4j (should NOT create new database)
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL dbms.listConfig() YIELD name, value
   WHERE name CONTAINS 'database'
   RETURN name, value"

# Should still show only 'neo4j' database
```

---

## Alternative: Manual Project Registration (Advanced)

If the Web UI doesn't work, you can manually register the project in MySQL:

```bash
# Connect to MySQL
docker exec -it openspg-mysql mysql -u root -popenspg openspg

# Insert project record
INSERT INTO kg_project (
  id, name, namespace, description, language, biz_scene,
  gmt_create, gmt_modified, status
) VALUES (
  1, 'CybersecurityKB', 'CybersecurityKB',
  'Cybersecurity Knowledge Base', 'en', 'cybersecurity',
  NOW(), NOW(), 'ACTIVE'
);

# Exit MySQL
EXIT;
```

Then your local project should be recognized.

---

## Why This Happens

**Root Cause:** OpenSPG was designed for Neo4j Enterprise, which supports multiple databases.

**OpenSPG's Behavior:**
- When creating a project via API/CLI: Tries `CREATE DATABASE <project_namespace>`
- When creating via Web UI: Uses default database with namespace isolation

**Neo4j Community Edition:**
- Only supports ONE database (default: `neo4j`)
- Uses node properties for isolation: `{namespace: 'CybersecurityKB'}`

---

## After Project Creation

Once the project is created (via Web UI or manually), you can proceed with:

### Phase 3: Create Schema

```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB
source ../../../venv/bin/activate

# Create schema file (Phase 3)
vim schema/CybersecurityKB.schema

# Commit schema
knext schema commit
```

### Phase 4-5: Build Knowledge Graph

```bash
# Import data (Phase 4-5)
cd builder
python indexer.py
```

### Phase 6: Query and Test

```bash
# Run queries (Phase 6)
cd ../solver
python qa.py
```

---

## Verification

After creating the project, verify it's using the correct database:

```bash
# Check project in OpenSPG
curl -s http://localhost:8887/api/v1/project/list | jq

# Check Neo4j database (should still be 'neo4j')
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "SHOW DATABASES"

# Should only show: neo4j, system
```

---

## Next Steps

After successfully creating the project:

✅ **Phase 2 Complete** - Project created and registered
➡️ **Phase 3** - Create OpenSPG schema from UCO ontology
➡️ **Phase 4** - Prepare and import cybersecurity data
➡️ **Phase 5** - Build knowledge graph
➡️ **Phase 6** - Query and test reasoning capabilities
