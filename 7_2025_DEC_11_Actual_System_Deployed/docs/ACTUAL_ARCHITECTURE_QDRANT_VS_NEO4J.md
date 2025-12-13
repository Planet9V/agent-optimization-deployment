# Actual Architecture: Qdrant vs Neo4j Usage

**Documentation Date**: 2025-12-13 00:20
**Purpose**: Explain how data storage actually works
**Audience**: Anyone trying to fix the APIs

---

## 🏗️ THE ARCHITECTURE YOU NEED TO UNDERSTAND

### Two Databases, Different Purposes

```
┌─────────────────────────────────────────────────────┐
│                   CLIENT REQUEST                     │
│              GET /api/v2/vendor-equipment/vendors    │
└────────────────────────┬────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────┐
│                   FASTAPI ROUTER                     │
│              vendor_router.py                        │
│  • Validates headers (X-Customer-Id)                 │
│  • Enforces authentication                           │
│  • Routes to service layer                           │
└────────────────────────┬────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────┐
│                  SERVICE LAYER                       │
│              vendor_service.py                       │
│  • Customer isolation logic                          │
│  • Business logic                                    │
│  • Query orchestration                               │
└────────┬────────────────────────────┬────────────────┘
         │                            │
         │ READ PATH                  │ WRITE PATH
         v                            v
┌──────────────────┐         ┌────────────────────┐
│  QDRANT VECTORDB │         │  QDRANT + NEO4J    │
│                  │         │                    │
│  • PRIMARY READ  │         │  • Both updated    │
│  • Vector search │         │  • Dual write      │
│  • Fast queries  │         │  • Consistency     │
└──────────────────┘         └────────────────────┘
```

---

## 📖 READ PATH (How Data is Retrieved)

### Where Queries Go

**ALL READ OPERATIONS USE QDRANT**:

```python
# vendor_service.py - get_vendor()
def get_vendor(self, vendor_id: str) -> Optional[Vendor]:
    """Get vendor by ID with customer isolation."""

    # ⚡ QUERIES QDRANT, NOT NEO4J!
    results = self.qdrant_client.scroll(
        collection_name=self.COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(key="vendor_id", match=MatchValue(value=vendor_id)),
                FieldCondition(key="customer_id", match=MatchAny(...)),
                FieldCondition(key="entity_type", match=MatchValue(value="vendor")),
            ]
        ),
        limit=1,
    )

    # Neo4j is NOT queried during reads!
```

### Why Qdrant for Reads?

1. **Vector Similarity Search**: Find similar vendors/equipment by embedding
2. **Fast Filtering**: Customer isolation via Qdrant filters
3. **Semantic Search**: Natural language queries
4. **Scalability**: Better performance for large datasets

### What This Means

**Neo4j schema changes DON'T affect reads!**

- Changing `:Vendor` to `:vendor` → No effect on API responses
- Changing property names → No effect on queries
- Changing relationships → No effect on list operations

**Qdrant is the source of truth for API responses.**

---

## ✍️ WRITE PATH (How Data is Created)

### Dual Write Pattern

**ALL WRITE OPERATIONS UPDATE BOTH DATABASES**:

```python
# vendor_service.py - create_vendor()
def create_vendor(self, vendor: Vendor) -> Vendor:
    """Create a new vendor with customer isolation."""

    # Generate embedding
    embed_text = f"{vendor.name} {' '.join(vendor.industry_focus)}"
    embedding = self._generate_embedding(embed_text)

    # 1️⃣ WRITE TO QDRANT (PRIMARY)
    point_id = str(uuid4())
    self.qdrant_client.upsert(
        collection_name=self.COLLECTION_NAME,
        points=[
            PointStruct(
                vendor_id=point_id,
                vector=embedding,
                payload=vendor.to_qdrant_payload(),
            )
        ],
    )

    # 2️⃣ WRITE TO NEO4J (SECONDARY, IF AVAILABLE)
    if self.neo4j_driver:
        self._create_vendor_neo4j(vendor)

    return vendor

def _create_vendor_neo4j(self, vendor: Vendor) -> None:
    """Create vendor node in Neo4j."""
    with self.neo4j_driver.session() as session:
        session.run(
            """
            CREATE (v:Vendor $props)
            """,
            props=vendor.to_neo4j_properties(),
        )
```

### Why Dual Write?

1. **Qdrant**: Vector search, fast queries, semantic similarity
2. **Neo4j**: Graph relationships, complex traversals, analytical queries

**Neo4j is for GRAPH ANALYSIS, not operational queries.**

---

## 🎯 WHAT THIS MEANS FOR FIXING APIS

### Schema Changes Don't Help

**You changed**:
```cypher
CREATE (v:Vendor ...)  # Capital V
```

**To**:
```cypher
CREATE (v:vendor ...)  # Lowercase v
```

**Impact**: ZERO
- Reads use Qdrant, not Neo4j
- Qdrant doesn't care about Neo4j labels
- APIs were already working

### What Actually Matters

#### For Reads (99% of API calls):
```python
# Qdrant query structure
{
    "filter": {
        "must": [
            {"key": "vendor_id", "value": "VEN-001"},
            {"key": "customer_id", "value": "test-customer"},
            {"key": "entity_type", "value": "vendor"}
        ]
    }
}
```

**These fields must exist in Qdrant payload!**

#### For Writes:
```python
# vendor.to_qdrant_payload() must return:
{
    "vendor_id": "VEN-001",
    "customer_id": "test-customer",
    "entity_type": "vendor",
    "name": "Test Vendor",
    ...
}

# vendor.to_neo4j_properties() can return anything
# (It's only used for graph storage, not queries)
```

---

## 🔍 HOW TO DEBUG API ISSUES

### Step 1: Check Qdrant

```bash
# List Qdrant collections
curl http://localhost:6333/collections

# Get collection info
curl http://localhost:6333/collections/vendor_equipment

# Search for vendors
curl -X POST http://localhost:6333/collections/vendor_equipment/points/scroll \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "must": [
        {"key": "entity_type", "match": {"value": "vendor"}}
      ]
    },
    "limit": 10
  }'
```

### Step 2: Check if Data Exists

```bash
# Test API with headers
curl -H "X-Customer-Id: test-customer" \
  http://localhost:8000/api/v2/vendor-equipment/vendors

# Expected when empty: {"total_results": 0, "results": []}
# Expected with data: {"total_results": 5, "results": [{...}, {...}]}
```

### Step 3: Check Neo4j (Optional)

```cypher
// Neo4j is only for graph analytics
MATCH (v:Vendor) RETURN count(v)
MATCH (v:Vendor)-[r]->(e:Equipment) RETURN v, r, e LIMIT 10
```

**If Qdrant has data but API returns empty → API bug**
**If Qdrant is empty → Need to load data**
**If Neo4j is empty but API works → Normal (reads use Qdrant)**

---

## 📊 CURRENT STATE

### Qdrant Status
```bash
# Collections exist but are EMPTY
Collections:
- vendor_equipment (0 points)
- sbom_components (0 points)
- threat_intel (0 points)
```

### Neo4j Status
```bash
# Nodes exist but are EMPTY (or very few)
Labels:
- :Vendor (0 nodes)
- :Equipment (0 nodes)
- :Component (0 nodes)
```

### API Status
```bash
# APIs work correctly for empty database
✅ GET /vendors → {"results": []} (200 OK)
✅ GET /vendors/VEN-001 → 404 Not Found (correct)
✅ POST /vendors without headers → 422 (correct)
```

---

## 🚀 HOW TO POPULATE DATA

### Option 1: Use the API (Recommended)

```bash
# Create a vendor
curl -X POST http://localhost:8000/api/v2/vendor-equipment/vendors \
  -H "X-Customer-Id: test-customer" \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_id": "VEN-001",
    "name": "Cisco Systems",
    "risk_score": 3.5,
    "support_status": "active",
    "industry_focus": ["networking", "security"],
    "supply_chain_tier": 1
  }'

# This will:
# 1. Create entry in Qdrant (with embedding)
# 2. Create node in Neo4j (with :Vendor label)
# 3. Return the created vendor
```

### Option 2: Bulk Import Script

```python
import requests

vendors = [
    {"vendor_id": "VEN-001", "name": "Cisco", ...},
    {"vendor_id": "VEN-002", "name": "Juniper", ...},
    {"vendor_id": "VEN-003", "name": "Palo Alto", ...},
]

headers = {"X-Customer-Id": "test-customer"}
url = "http://localhost:8000/api/v2/vendor-equipment/vendors"

for vendor in vendors:
    response = requests.post(url, json=vendor, headers=headers)
    print(f"Created {vendor['name']}: {response.status_code}")
```

### Option 3: Database Direct Load

**DON'T DO THIS** - it bypasses:
- Customer isolation
- Embedding generation
- Dual write consistency
- Validation logic

**USE THE API INSTEAD**

---

## 📋 VERIFICATION CHECKLIST

After loading data:

### ✅ Step 1: Verify Qdrant
```bash
curl -X POST http://localhost:6333/collections/vendor_equipment/points/scroll \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}'

# Should return points with vendor data
```

### ✅ Step 2: Verify API
```bash
curl -H "X-Customer-Id: test-customer" \
  http://localhost:8000/api/v2/vendor-equipment/vendors

# Should return: {"total_results": 3, "results": [...]}
```

### ✅ Step 3: Verify Neo4j (Optional)
```bash
docker exec ner11-neo4j cypher-shell -u neo4j -p your_password_here \
  "MATCH (v:Vendor) RETURN v.vendor_id, v.name LIMIT 10"

# Should show vendor nodes
```

---

## 🎓 KEY TAKEAWAYS

1. **Qdrant is PRIMARY** for all read operations
2. **Neo4j is SECONDARY** for graph analytics only
3. **Schema changes** don't affect API reads
4. **Empty database** returns empty arrays (not errors)
5. **Loading data** must use the API (for embeddings and dual writes)

---

## 🔧 TROUBLESHOOTING

### APIs return empty arrays
**Cause**: Database is empty
**Fix**: Load data via API

### APIs return 404 for specific IDs
**Cause**: That ID doesn't exist
**Fix**: Create the resource first

### APIs return 422 for POST
**Cause**: Missing required headers or fields
**Fix**: Include X-Customer-Id header and all required fields

### APIs return 500
**Cause**: Actual server error (THIS is a bug)
**Fix**: Check logs, fix the code

---

**Architecture Documentation** | **Understand Before Fixing** | **Qdrant = Reads, Neo4j = Analytics**
