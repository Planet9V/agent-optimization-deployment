# Neo4j Community Edition Configuration for KAG

## The Issue

Neo4j Community Edition does **NOT** support `CREATE DATABASE` commands. This is an Enterprise-only feature.

Your OpenSPG deployment uses Neo4j Community, so you must use the default `neo4j` database.

## ✅ Correct Configuration

### Option 1: KAG Project Configuration (Recommended)

When creating your cybersecurity knowledge base project, use this configuration:

**File:** `CybersecurityKB/kag_config.yaml`

```yaml
project:
  biz_scene: default
  host_addr: http://127.0.0.1:8887
  id: "1"
  language: en
  namespace: CybersecurityKB  # This is your project namespace, NOT a database name

# OpenSPG handles Neo4j connection internally
# It automatically uses the default 'neo4j' database
# No database creation needed!
```

### Option 2: Direct Neo4j Connection (Advanced)

If you're connecting directly to Neo4j (not through OpenSPG), use:

```python
from neo4j import GraphDatabase

# Connect to the default database
driver = GraphDatabase.driver(
    "neo4j://localhost:7687",
    auth=("neo4j", "neo4j@openspg"),
    database="neo4j"  # Always use 'neo4j' in Community Edition
)
```

### Option 3: OpenSPG Server Configuration

The OpenSPG server configuration is already correct in your `docker-compose.yml`:

```yaml
openspg-server:
  command: [
    "--cloudext.graphstore.url=neo4j://openspg-neo4j:7687?user=neo4j&password=neo4j@openspg&database=neo4j"
  ]
```

This is already using `database=neo4j` ✅

## 🎯 How KAG Handles Namespaces

KAG uses **namespaces** (not separate databases) for isolation:

```
Single Neo4j Database: neo4j
├── Namespace: CybersecurityKB
│   ├── Nodes with property: namespace=CybersecurityKB
│   └── Relationships within this namespace
├── Namespace: AnotherProject
│   ├── Nodes with property: namespace=AnotherProject
│   └── Relationships within this namespace
└── Shared nodes (if configured)
```

**Benefits:**
- ✅ Works with Neo4j Community Edition
- ✅ Multiple projects in one database
- ✅ Isolated by namespace property
- ✅ Can share threat intelligence across projects

## 🔍 Verify Your Configuration

```bash
# Check Neo4j default database
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL dbms.listConfig() YIELD name, value
   WHERE name = 'initial.dbms.default_database'
   RETURN value"

# Expected output: neo4j

# Check existing data
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN DISTINCT labels(n), count(*)"
```

## 🚀 For Your Cybersecurity KB Implementation

**You don't need to change anything!**

Just follow the implementation plan and use:

```yaml
project:
  namespace: CybersecurityKB  # Your project identifier
  host_addr: http://127.0.0.1:8887  # OpenSPG handles Neo4j connection
```

KAG will automatically:
1. Connect to OpenSPG server
2. OpenSPG connects to Neo4j default database
3. Store all your data with `namespace: CybersecurityKB` property
4. Keep your cybersecurity data isolated from other projects

## ❌ What NOT to Do

```python
# ❌ DON'T try to create databases in Community Edition
CREATE DATABASE cybersecurity  # This will fail!

# ❌ DON'T try to switch databases
:use cybersecurity  # Not available in Community

# ❌ DON'T modify docker-compose.yml database setting
# It's already correct: database=neo4j
```

## ✅ What TO Do

```yaml
# ✅ Use namespace for isolation
project:
  namespace: CybersecurityKB

# ✅ Let OpenSPG handle Neo4j connection
host_addr: http://127.0.0.1:8887

# ✅ Query by namespace
MATCH (n {namespace: 'CybersecurityKB'}) RETURN n LIMIT 25
```

## 📋 Summary

**Where to configure:** Your KAG project's `kag_config.yaml` file

**What to set:** Just the `namespace` field - OpenSPG handles the rest

**Database to use:** Always `neo4j` (the default) - already configured

**No changes needed to:**
- ❌ docker-compose.yml (already correct)
- ❌ OpenSPG server config (already correct)
- ❌ Neo4j config (already correct)

**Your implementation plan is already configured correctly for Neo4j Community Edition!**
