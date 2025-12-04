# INTEGRATION PATTERNS - AEON Enhancement Implementation

**Version:** 1.0.0
**Created:** 2025-12-03T20:40:00Z
**Purpose:** Code examples and patterns for implementing AEON enhancements

---

## 1. Neo4j Integration Patterns

### 1.1 Customer Labels (Multi-Tenant Isolation)

```cypher
// Create customer tenant
CREATE (c:Customer {
    customer_id: $customer_id,
    name: $name,
    created_at: datetime(),
    status: 'ACTIVE'
})

// Link asset to customer
MATCH (a:Asset {asset_id: $asset_id})
MATCH (c:Customer {customer_id: $customer_id})
MERGE (a)-[:BELONGS_TO {since: datetime()}]->(c)

// Query with tenant isolation
MATCH (c:Customer {customer_id: $tenant_id})<-[:BELONGS_TO]-(a:Asset)
RETURN a
```

```python
# Python Neo4j driver pattern
from neo4j import GraphDatabase

class TenantIsolatedDriver:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def query_with_tenant(self, query, tenant_id, params=None):
        """Execute query with automatic tenant isolation"""
        with self.driver.session() as session:
            full_params = {"tenant_id": tenant_id, **(params or {})}
            return session.run(query, full_params).data()

    def get_tenant_assets(self, tenant_id):
        query = """
        MATCH (c:Customer {customer_id: $tenant_id})<-[:BELONGS_TO]-(a:Asset)
        RETURN a.asset_id, a.name, a.type
        """
        return self.query_with_tenant(query, tenant_id)
```

### 1.2 E07 IEC 62443 Safety Zones

```cypher
// Define safety zone levels
CREATE CONSTRAINT safety_level_unique IF NOT EXISTS
FOR (s:SafetyLevel) REQUIRE s.level IS UNIQUE

// Create safety levels
UNWIND ['SL0', 'SL1', 'SL2', 'SL3', 'SL4'] AS level
MERGE (s:SafetyLevel {level: level})
SET s.description = CASE level
    WHEN 'SL0' THEN 'No specific requirements'
    WHEN 'SL1' THEN 'Protection against casual violation'
    WHEN 'SL2' THEN 'Protection against intentional violation with simple means'
    WHEN 'SL3' THEN 'Protection against sophisticated attack'
    WHEN 'SL4' THEN 'Protection against state-sponsored attack'
END

// Assign safety level to asset
MATCH (a:Asset {asset_id: $asset_id})
MATCH (s:SafetyLevel {level: $safety_level})
MERGE (a)-[:HAS_SAFETY_LEVEL {
    assigned_at: datetime(),
    assigned_by: $user_id,
    rationale: $rationale
}]->(s)

// Query assets by safety level
MATCH (a:Asset)-[:HAS_SAFETY_LEVEL]->(s:SafetyLevel {level: $min_level})
WHERE s.level >= $min_level
RETURN a.asset_id, a.name, s.level AS safety_level
ORDER BY s.level DESC
```

### 1.3 E03 SBOM Analysis

```cypher
// Create SBOM structure
CREATE (sbom:SBOM {
    sbom_id: $sbom_id,
    format: $format,  // 'CycloneDX' or 'SPDX'
    version: $version,
    created_at: datetime()
})

// Link components
UNWIND $components AS comp
MERGE (c:Component {
    name: comp.name,
    version: comp.version,
    purl: comp.purl
})
MERGE (sbom)-[:CONTAINS {
    scope: comp.scope,
    direct: comp.direct
}]->(c)

// Link CVEs to components
MATCH (c:Component {purl: $purl})
MATCH (cve:CVE {cve_id: $cve_id})
MERGE (c)-[:HAS_VULNERABILITY {
    discovered_at: datetime(),
    source: 'NVD'
}]->(cve)

// Query vulnerable components
MATCH (sbom:SBOM)-[:CONTAINS]->(c:Component)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvss_score >= 7.0
RETURN sbom.sbom_id, c.name, c.version, cve.cve_id, cve.cvss_score
ORDER BY cve.cvss_score DESC
```

```python
# SBOM Parser Pattern
from cyclonedx.parser import JsonParser
from spdx_tools.spdx.parser import parse_file

class SBOMParser:
    def parse(self, file_path: str, format: str = 'auto'):
        if format == 'auto':
            format = self._detect_format(file_path)

        if format == 'cyclonedx':
            return self._parse_cyclonedx(file_path)
        elif format == 'spdx':
            return self._parse_spdx(file_path)
        else:
            raise ValueError(f"Unknown format: {format}")

    def _parse_cyclonedx(self, file_path):
        with open(file_path) as f:
            parser = JsonParser(f.read())
        bom = parser.parse()
        return [
            {
                'name': comp.name,
                'version': comp.version,
                'purl': str(comp.purl) if comp.purl else None,
                'licenses': [l.id for l in (comp.licenses or [])],
                'hashes': {h.alg: h.value for h in (comp.hashes or [])}
            }
            for comp in bom.components
        ]

    def _parse_spdx(self, file_path):
        doc = parse_file(file_path)
        return [
            {
                'name': pkg.name,
                'version': pkg.version,
                'purl': pkg.external_refs[0].locator if pkg.external_refs else None,
                'licenses': pkg.license_concluded
            }
            for pkg in doc.packages
        ]
```

### 1.4 E12 NOW/NEXT/NEVER Prioritization

```cypher
// NOW/NEXT/NEVER Algorithm
WITH $cve_id AS cve_id
MATCH (cve:CVE {cve_id: cve_id})
OPTIONAL MATCH (cve)<-[:HAS_VULNERABILITY]-(c:Component)<-[:CONTAINS]-(sbom:SBOM)
OPTIONAL MATCH (c)<-[:RUNS_ON]-(a:Asset)-[:HAS_SAFETY_LEVEL]->(s:SafetyLevel)

WITH cve,
     COLLECT(DISTINCT a) AS affected_assets,
     MAX(s.level) AS max_safety_level,
     cve.cvss_score AS cvss,
     cve.exploit_available AS exploitable

// Calculate priority score
WITH cve, affected_assets, max_safety_level, cvss, exploitable,
     (cvss / 10.0) * 0.4 +                              // CVSS weight
     (CASE WHEN exploitable THEN 0.3 ELSE 0 END) +       // Exploit availability
     (CASE max_safety_level
        WHEN 'SL4' THEN 0.3
        WHEN 'SL3' THEN 0.2
        WHEN 'SL2' THEN 0.1
        ELSE 0 END) AS priority_score

// Classify
SET cve.priority_class = CASE
    WHEN priority_score >= 0.7 THEN 'NOW'
    WHEN priority_score >= 0.4 THEN 'NEXT'
    ELSE 'NEVER'
END,
cve.priority_score = priority_score,
cve.affected_asset_count = SIZE(affected_assets),
cve.prioritized_at = datetime()

RETURN cve.cve_id, cve.priority_class, cve.priority_score
```

```python
# NOW/NEXT/NEVER Python Implementation
from dataclasses import dataclass
from enum import Enum

class PriorityClass(Enum):
    NOW = "NOW"
    NEXT = "NEXT"
    NEVER = "NEVER"

@dataclass
class CVEPriority:
    cve_id: str
    cvss_score: float
    exploit_available: bool
    safety_level: str
    affected_assets: int

    def calculate_priority(self) -> tuple[PriorityClass, float]:
        # CVSS contribution (40%)
        cvss_score = (self.cvss_score / 10.0) * 0.4

        # Exploit availability (30%)
        exploit_score = 0.3 if self.exploit_available else 0

        # Safety level contribution (30%)
        safety_weights = {'SL4': 0.3, 'SL3': 0.2, 'SL2': 0.1, 'SL1': 0.05, 'SL0': 0}
        safety_score = safety_weights.get(self.safety_level, 0)

        total_score = cvss_score + exploit_score + safety_score

        if total_score >= 0.7:
            return PriorityClass.NOW, total_score
        elif total_score >= 0.4:
            return PriorityClass.NEXT, total_score
        else:
            return PriorityClass.NEVER, total_score
```

### 1.5 E13 Attack Path Modeling

```cypher
// Create attack path relationship types
// EXPLOITS, LEADS_TO, ENABLES_ACCESS

// Find shortest attack path to critical asset
MATCH path = shortestPath(
    (entry:Asset {type: 'INTERNET_FACING'})-[:CONNECTS_TO|EXPLOITS|LEADS_TO*..10]->(target:Asset {critical: true})
)
WHERE ALL(r IN relationships(path) WHERE
    r.type = 'CONNECTS_TO' OR
    EXISTS((startNode(r))-[:HAS_VULNERABILITY]->(:CVE))
)
RETURN path,
       LENGTH(path) AS path_length,
       [n IN nodes(path) | n.name] AS path_nodes

// Calculate attack path risk score
MATCH (a:Asset)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE a.asset_id IN $path_asset_ids
WITH SUM(cve.cvss_score) AS total_cvss,
     COUNT(cve) AS vuln_count,
     MAX(cve.cvss_score) AS max_cvss
RETURN total_cvss, vuln_count, max_cvss,
       (max_cvss / 10.0) * 0.5 + (vuln_count / 10.0) * 0.3 + (total_cvss / 100.0) * 0.2 AS path_risk_score
```

---

## 2. Qdrant Integration Patterns

### 2.1 Vector Upsert Pattern

```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

class QdrantEntityStore:
    def __init__(self, url="localhost:6333", collection="ner11_gold_entities"):
        self.client = QdrantClient(url=url)
        self.collection = collection

    def ensure_collection(self, vector_size=384):
        """Create collection if it doesn't exist"""
        collections = self.client.get_collections().collections
        if self.collection not in [c.name for c in collections]:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )

    def upsert_entity(self, entity_id: str, embedding: list, payload: dict):
        """Upsert single entity with embedding"""
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=entity_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )

    def batch_upsert(self, entities: list[dict], batch_size=100):
        """Batch upsert entities"""
        for i in range(0, len(entities), batch_size):
            batch = entities[i:i+batch_size]
            points = [
                PointStruct(
                    id=e['id'],
                    vector=e['embedding'],
                    payload=e['payload']
                )
                for e in batch
            ]
            self.client.upsert(collection_name=self.collection, points=points)
```

### 2.2 Similarity Search Pattern

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

class EntitySearcher:
    def __init__(self, qdrant_store: QdrantEntityStore):
        self.store = qdrant_store

    def search_similar(self, query_embedding: list, limit=10, entity_type=None):
        """Search for similar entities"""
        query_filter = None
        if entity_type:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="entity_type",
                        match=MatchValue(value=entity_type)
                    )
                ]
            )

        results = self.store.client.search(
            collection_name=self.store.collection,
            query_vector=query_embedding,
            limit=limit,
            query_filter=query_filter
        )

        return [
            {
                'id': r.id,
                'score': r.score,
                'payload': r.payload
            }
            for r in results
        ]

    def search_by_text(self, text: str, embedding_model, limit=10):
        """Search by text using embedding model"""
        embedding = embedding_model.encode(text).tolist()
        return self.search_similar(embedding, limit)
```

### 2.3 Customer-Isolated Vector Store Pattern

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny, PointStruct

@dataclass
class CustomerVectorContext:
    """Customer context for Qdrant vector operations."""
    customer_id: str
    include_system: bool = True
    access_level: str = "read"

    def get_customer_ids(self) -> List[str]:
        """Get list of customer IDs to include in search."""
        if self.include_system:
            return [self.customer_id, "SYSTEM"]
        return [self.customer_id]


class CustomerIsolatedVectorStore:
    """
    Qdrant vector store with automatic customer isolation.
    All operations automatically filter by customer_id in payload.
    """

    def __init__(self, url: str = "localhost:6333", collection: str = "ner11_gold_entities"):
        self.client = QdrantClient(url=url)
        self.collection = collection
        self._context: Optional[CustomerVectorContext] = None

    def set_context(self, context: CustomerVectorContext) -> None:
        """Set customer context for all operations."""
        self._context = context

    def _build_customer_filter(self, additional: Optional[List] = None) -> Filter:
        """Build Qdrant filter with customer isolation."""
        customer_ids = self._context.get_customer_ids()
        must_conditions = [
            FieldCondition(key="customer_id", match=MatchAny(any=customer_ids))
        ]
        if additional:
            must_conditions.extend(additional)
        return Filter(must=must_conditions)

    def search_similar(self, query_embedding: List[float], limit: int = 10) -> List[Dict]:
        """Search with automatic customer isolation."""
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=limit,
            query_filter=self._build_customer_filter()
        )
        return [{'id': r.id, 'score': r.score, 'payload': r.payload} for r in results]

    def upsert_entity(self, entity_id: str, embedding: List[float], payload: Dict) -> None:
        """Upsert with automatic customer_id assignment."""
        payload['customer_id'] = self._context.customer_id
        self.client.upsert(
            collection_name=self.collection,
            points=[PointStruct(id=entity_id, vector=embedding, payload=payload)]
        )


# Factory pattern for getting customer-isolated stores
class CustomerVectorStoreFactory:
    _instances: Dict[str, CustomerIsolatedVectorStore] = {}

    @classmethod
    def get_store(cls, customer_id: str, url: str = "localhost:6333",
                  collection: str = "ner11_gold_entities") -> CustomerIsolatedVectorStore:
        cache_key = f"{url}:{collection}"
        if cache_key not in cls._instances:
            cls._instances[cache_key] = CustomerIsolatedVectorStore(url=url, collection=collection)
        store = cls._instances[cache_key]
        store.set_context(CustomerVectorContext(customer_id=customer_id))
        return store
```

**Usage Example:**
```python
# Get customer-isolated store
store = CustomerVectorStoreFactory.get_store(
    customer_id="CUST-001",
    url="localhost:6333",
    collection="ner11_gold_entities"
)

# Search - automatically filters by CUST-001 and SYSTEM
results = store.search_similar(query_embedding, limit=10)

# Upsert - automatically adds customer_id to payload
store.upsert_entity(
    entity_id="entity-123",
    embedding=embedding_vector,
    payload={"entity_type": "CVE", "name": "CVE-2024-0001"}
)
```

### 2.4 NER30 Semantic Search API with Customer Isolation

```python
from fastapi import APIRouter, Header, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny


class CustomerSemanticSearchRequest(BaseModel):
    """Request for customer-isolated semantic search."""
    query: str = Field(..., description="Search query text")
    limit: int = Field(default=10, ge=1, le=100)
    customer_id: str = Field(..., description="Customer ID for isolation")
    label_filter: Optional[str] = Field(default=None, description="Tier 1: NER label")
    fine_grained_filter: Optional[str] = Field(default=None, description="Tier 2: type")
    include_system: bool = Field(default=True, description="Include SYSTEM entities")


class CustomerIsolatedSemanticService:
    """
    NER30 semantic search with automatic customer isolation.

    All searches are filtered by customer_id to ensure multi-tenant isolation.
    SYSTEM entities (CVEs, CWEs, CAPECs) are optionally included.
    """

    def __init__(self, qdrant_url: str, collection: str, embedding_model):
        self.client = QdrantClient(url=qdrant_url)
        self.collection = collection
        self.embedding_model = embedding_model

    def _build_customer_filter(
        self,
        customer_id: str,
        include_system: bool = True,
        additional_filters: List = None
    ) -> Filter:
        """Build Qdrant filter with customer isolation."""
        customer_ids = [customer_id, "SYSTEM"] if include_system else [customer_id]

        must_conditions = [
            FieldCondition(key="customer_id", match=MatchAny(any=customer_ids))
        ]

        if additional_filters:
            must_conditions.extend(additional_filters)

        return Filter(must=must_conditions)

    def search(self, request: CustomerSemanticSearchRequest) -> Dict[str, Any]:
        """Execute customer-isolated semantic search."""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([request.query])[0].tolist()

        # Build filter with customer isolation
        query_filter = self._build_customer_filter(
            customer_id=request.customer_id,
            include_system=request.include_system,
        )

        # Execute search
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=request.limit,
        )

        return {
            "results": [
                {
                    "score": r.score,
                    "entity": r.payload.get("entity"),
                    "customer_id": r.payload.get("customer_id"),
                    "is_system": r.payload.get("customer_id") == "SYSTEM",
                }
                for r in results
            ],
            "customer_id": request.customer_id,
            "total_results": len(results),
        }


# FastAPI Router
router = APIRouter(prefix="/api/v2/search", tags=["semantic-search"])

@router.post("/semantic")
async def semantic_search(
    request: CustomerSemanticSearchRequest,
    x_customer_id: str = Header(..., description="Customer ID"),
):
    """Customer-isolated semantic search endpoint."""
    # Verify customer_id matches header (security check)
    if request.customer_id != x_customer_id:
        raise HTTPException(status_code=403, detail="Customer ID mismatch")

    service = get_semantic_service()  # Dependency injection
    return service.search(request)
```

**Usage Example:**
```bash
# Search with customer isolation
curl -X POST "http://localhost:8000/api/v2/search/semantic" \
  -H "X-Customer-ID: CUST-001" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ransomware attack",
    "customer_id": "CUST-001",
    "limit": 10,
    "include_system": true,
    "label_filter": "MALWARE"
  }'
```

---

## 3. External API Integration Patterns

### 3.1 NVD API Pattern

```python
import requests
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential
import time

class NVDClient:
    BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers['apiKey'] = api_key

    @property
    def rate_limit(self):
        return 50 if self.api_key else 5

    @sleep_and_retry
    @limits(calls=5, period=30)  # Conservative default
    def _rate_limited_request(self, params):
        return self.session.get(self.BASE_URL, params=params)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=60))
    def fetch_cves(self, keyword=None, cpe_name=None, cvss_severity=None,
                   start_index=0, results_per_page=100):
        """Fetch CVEs with optional filters"""
        params = {
            'startIndex': start_index,
            'resultsPerPage': results_per_page
        }

        if keyword:
            params['keywordSearch'] = keyword
        if cpe_name:
            params['cpeName'] = cpe_name
        if cvss_severity:
            params['cvssV3Severity'] = cvss_severity

        response = self._rate_limited_request(params)
        response.raise_for_status()
        return response.json()

    def fetch_all_cves(self, **kwargs):
        """Iterate through all pages of CVEs"""
        start_index = 0
        total_results = None

        while total_results is None or start_index < total_results:
            data = self.fetch_cves(start_index=start_index, **kwargs)
            total_results = data.get('totalResults', 0)

            for vuln in data.get('vulnerabilities', []):
                yield vuln

            start_index += len(data.get('vulnerabilities', []))
            time.sleep(0.5)  # Additional rate limiting
```

### 3.2 World Bank API Pattern

```python
import requests

class WorldBankClient:
    BASE_URL = "https://api.worldbank.org/v2"

    def fetch_indicator(self, indicator: str, country: str = "all",
                        date_range: str = None):
        """Fetch World Bank indicator data"""
        url = f"{self.BASE_URL}/country/{country}/indicator/{indicator}"
        params = {
            'format': 'json',
            'per_page': 1000
        }
        if date_range:
            params['date'] = date_range

        response = requests.get(url, params=params)
        response.raise_for_status()

        # World Bank returns [metadata, data]
        result = response.json()
        if len(result) > 1:
            return result[1]
        return []

    def get_population(self, country: str = "all", year: int = None):
        """Get population data"""
        date_range = str(year) if year else None
        return self.fetch_indicator("SP.POP.TOTL", country, date_range)

    def get_gdp(self, country: str = "all", year: int = None):
        """Get GDP data"""
        date_range = str(year) if year else None
        return self.fetch_indicator("NY.GDP.MKTP.CD", country, date_range)
```

### 3.3 Rate Limiting Middleware

```python
import time
from collections import deque
from threading import Lock

class TokenBucketRateLimiter:
    """Token bucket rate limiter"""

    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = Lock()

    def acquire(self, tokens=1):
        """Acquire tokens, blocking if necessary"""
        with self.lock:
            now = time.time()
            # Add tokens based on elapsed time
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if tokens <= self.tokens:
                self.tokens -= tokens
                return True

            # Calculate wait time
            wait_time = (tokens - self.tokens) / self.rate
            time.sleep(wait_time)
            self.tokens = 0
            self.last_update = time.time()
            return True

class AdaptiveRateLimiter:
    """Adapts rate based on API responses"""

    def __init__(self, initial_rate=5, min_rate=1, max_rate=50):
        self.rate = initial_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.limiter = TokenBucketRateLimiter(initial_rate, initial_rate)
        self.errors = deque(maxlen=10)

    def record_success(self):
        self.errors.append(False)
        if all(not e for e in self.errors) and len(self.errors) >= 5:
            self._increase_rate()

    def record_error(self, is_rate_limit=False):
        self.errors.append(True)
        if is_rate_limit:
            self._decrease_rate()

    def _increase_rate(self):
        new_rate = min(self.max_rate, self.rate * 1.2)
        if new_rate != self.rate:
            self.rate = new_rate
            self.limiter = TokenBucketRateLimiter(self.rate, int(self.rate))

    def _decrease_rate(self):
        new_rate = max(self.min_rate, self.rate * 0.5)
        if new_rate != self.rate:
            self.rate = new_rate
            self.limiter = TokenBucketRateLimiter(self.rate, int(self.rate))
```

---

## 4. ETL Pipeline Patterns

### 4.1 Batch Processing Pattern

```python
from typing import Generator, TypeVar, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

T = TypeVar('T')

def process_in_batches(items: list[T], batch_size: int = 100) -> Generator[list[T], None, None]:
    """Yield successive batches from items list"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def parallel_batch_process(items: list[T], process_fn: Callable[[T], any],
                           batch_size: int = 100, max_workers: int = 4):
    """Process items in parallel batches"""
    results = []
    errors = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for batch in process_in_batches(items, batch_size):
            futures = {executor.submit(process_fn, item): item for item in batch}

            for future in as_completed(futures):
                item = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Error processing {item}: {e}")
                    errors.append((item, e))

    return results, errors
```

### 4.2 Idempotent Operations Pattern

```python
class IdempotentNeo4jOperations:
    """Idempotent Neo4j operations using MERGE"""

    def __init__(self, driver):
        self.driver = driver

    def upsert_entity(self, label: str, id_field: str, id_value: str, properties: dict):
        """Idempotent entity upsert using MERGE"""
        query = f"""
        MERGE (n:{label} {{{id_field}: $id_value}})
        SET n += $properties
        SET n.updated_at = datetime()
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, id_value=id_value, properties=properties)
            return result.single()

    def upsert_relationship(self, source_label: str, source_id: str,
                           target_label: str, target_id: str,
                           rel_type: str, properties: dict = None):
        """Idempotent relationship upsert"""
        query = f"""
        MATCH (source:{source_label} {{id: $source_id}})
        MATCH (target:{target_label} {{id: $target_id}})
        MERGE (source)-[r:{rel_type}]->(target)
        SET r += $properties
        SET r.updated_at = datetime()
        RETURN r
        """
        with self.driver.session() as session:
            result = session.run(query,
                                source_id=source_id,
                                target_id=target_id,
                                properties=properties or {})
            return result.single()
```

### 4.3 Transaction Management Pattern

```python
from contextlib import contextmanager
from neo4j import Transaction

class TransactionalOperations:
    def __init__(self, driver):
        self.driver = driver

    @contextmanager
    def transaction(self):
        """Context manager for Neo4j transactions with automatic rollback on error"""
        session = self.driver.session()
        tx = session.begin_transaction()
        try:
            yield tx
            tx.commit()
        except Exception as e:
            tx.rollback()
            raise
        finally:
            session.close()

    def execute_batch_in_transaction(self, operations: list[tuple[str, dict]]):
        """Execute multiple operations in single transaction"""
        with self.transaction() as tx:
            results = []
            for query, params in operations:
                result = tx.run(query, params)
                results.append(result.data())
            return results
```

---

## 5. Test Integration Patterns

### 5.1 Neo4j Test Fixture

```python
import pytest
from neo4j import GraphDatabase
from testcontainers.neo4j import Neo4jContainer

@pytest.fixture(scope="session")
def neo4j_container():
    """Start Neo4j container for testing"""
    with Neo4jContainer("neo4j:5.9") as neo4j:
        yield neo4j

@pytest.fixture(scope="function")
def neo4j_session(neo4j_container):
    """Create test session with cleanup"""
    driver = GraphDatabase.driver(
        neo4j_container.get_connection_url(),
        auth=("neo4j", neo4j_container.NEO4J_PASSWORD)
    )
    session = driver.session()

    yield session

    # Cleanup test data
    session.run("MATCH (n) DETACH DELETE n")
    session.close()
    driver.close()

@pytest.fixture
def sample_customer(neo4j_session):
    """Create sample customer for testing"""
    result = neo4j_session.run("""
        CREATE (c:Customer {
            customer_id: 'TEST-001',
            name: 'Test Customer',
            created_at: datetime()
        })
        RETURN c
    """)
    return result.single()['c']
```

### 5.2 Mock API Pattern

```python
import responses
import pytest

@pytest.fixture
def mock_nvd_api():
    """Mock NVD API responses"""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://services.nvd.nist.gov/rest/json/cves/2.0",
            json={
                "resultsPerPage": 1,
                "startIndex": 0,
                "totalResults": 1,
                "vulnerabilities": [
                    {
                        "cve": {
                            "id": "CVE-2024-0001",
                            "descriptions": [
                                {"lang": "en", "value": "Test vulnerability"}
                            ],
                            "metrics": {
                                "cvssMetricV31": [{
                                    "cvssData": {"baseScore": 7.5}
                                }]
                            }
                        }
                    }
                ]
            },
            status=200
        )
        yield rsps

def test_nvd_fetch(mock_nvd_api):
    """Test NVD API integration"""
    client = NVDClient()
    result = client.fetch_cves(keyword="test")

    assert result['totalResults'] == 1
    assert result['vulnerabilities'][0]['cve']['id'] == 'CVE-2024-0001'
```

### 5.3 Qdrant Test Fixture

```python
import pytest
from qdrant_client import QdrantClient
from testcontainers.core.generic import GenericContainer

@pytest.fixture(scope="session")
def qdrant_container():
    """Start Qdrant container for testing"""
    container = GenericContainer("qdrant/qdrant:v1.7.0")
    container.with_exposed_ports(6333, 6334)
    container.start()

    yield container

    container.stop()

@pytest.fixture(scope="function")
def qdrant_client(qdrant_container):
    """Create Qdrant client for testing"""
    host = qdrant_container.get_container_host_ip()
    port = qdrant_container.get_exposed_port(6333)

    client = QdrantClient(host=host, port=port)

    # Create test collection
    client.create_collection(
        collection_name="test_entities",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

    yield client

    # Cleanup
    client.delete_collection("test_entities")
```

---

## 6. Error Recovery Patterns

### 6.1 Circuit Breaker Pattern

```python
import time
from enum import Enum
from threading import Lock

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
        self.lock = Lock()

    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            self._record_failure()
            raise

    def _record_success(self):
        with self.lock:
            self.failures = 0
            self.state = CircuitState.CLOSED

    def _record_failure(self):
        with self.lock:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = CircuitState.OPEN
```

### 6.2 Retry with Backoff Pattern

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import logging

logger = logging.getLogger(__name__)

class RetryableAPIClient:
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def fetch_with_retry(self, url):
        """Fetch URL with exponential backoff retry"""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
```

---

## 7. Performance Patterns

### 7.1 Caching Pattern

```python
from functools import lru_cache
import redis
import json
import hashlib

class CacheManager:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour

    def cache_key(self, prefix: str, *args, **kwargs):
        """Generate cache key from arguments"""
        data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        hash_val = hashlib.md5(data.encode()).hexdigest()
        return f"{prefix}:{hash_val}"

    def get(self, key: str):
        """Get cached value"""
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: any, ttl: int = None):
        """Set cached value with TTL"""
        self.redis.setex(key, ttl or self.default_ttl, json.dumps(value))

    def cached(self, prefix: str, ttl: int = None):
        """Decorator for caching function results"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                key = self.cache_key(prefix, *args, **kwargs)
                cached = self.get(key)
                if cached is not None:
                    return cached

                result = func(*args, **kwargs)
                self.set(key, result, ttl)
                return result
            return wrapper
        return decorator

# Usage
cache = CacheManager()

@cache.cached("cve_details", ttl=3600)
def get_cve_details(cve_id: str):
    return nvd_client.fetch_cve(cve_id)
```

### 7.2 Connection Pooling Pattern

```python
from neo4j import GraphDatabase
from contextlib import contextmanager

class Neo4jConnectionPool:
    _instance = None

    def __new__(cls, uri, user, password, max_connections=50):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.driver = GraphDatabase.driver(
                uri,
                auth=(user, password),
                max_connection_pool_size=max_connections
            )
        return cls._instance

    @contextmanager
    def session(self):
        """Get session from pool"""
        session = self.driver.session()
        try:
            yield session
        finally:
            session.close()

    def close(self):
        """Close driver and all connections"""
        self.driver.close()
        Neo4jConnectionPool._instance = None
```

---

## 8. Enhancement-Specific Patterns

### 8.1 E10 Economic Impact Calculation

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class EconomicImpact:
    asset_value: Decimal
    cvss_score: float
    exploit_probability: float
    downtime_hours: float
    hourly_cost: Decimal

    def calculate_risk_value(self) -> Decimal:
        """Calculate economic risk value"""
        # Annual Loss Expectancy (ALE) = SLE × ARO
        # Single Loss Expectancy (SLE)
        sle = self.asset_value * Decimal(str(self.cvss_score / 10.0))

        # Annualized Rate of Occurrence (ARO)
        aro = Decimal(str(self.exploit_probability * 12))  # Monthly probability

        ale = sle * aro

        # Add downtime cost
        downtime_cost = self.hourly_cost * Decimal(str(self.downtime_hours))

        return ale + (downtime_cost * aro)

    def calculate_remediation_roi(self, remediation_cost: Decimal) -> float:
        """Calculate ROI of remediation"""
        risk_value = self.calculate_risk_value()
        if remediation_cost == 0:
            return float('inf')
        return float((risk_value - remediation_cost) / remediation_cost * 100)
```

### 8.2 E21 Transcript Psychometric NER

```python
import spacy
from transformers import pipeline

class PsychometricNER:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.sentiment = pipeline("sentiment-analysis")

        # Custom psychometric patterns
        self.psychometric_patterns = {
            'AUTHORITY': ['should', 'must', 'have to', 'need to'],
            'UNCERTAINTY': ['maybe', 'perhaps', 'might', 'possibly'],
            'AGGRESSION': ['attack', 'destroy', 'eliminate', 'crush'],
            'COOPERATION': ['together', 'collaborate', 'share', 'help']
        }

    def analyze_transcript(self, text: str) -> dict:
        """Extract psychometric signals from transcript"""
        doc = self.nlp(text)

        # Standard NER
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Psychometric patterns
        psych_signals = {}
        for category, patterns in self.psychometric_patterns.items():
            count = sum(1 for p in patterns if p.lower() in text.lower())
            psych_signals[category] = count

        # Sentiment
        sentiment = self.sentiment(text[:512])[0]  # Truncate for model

        return {
            'entities': entities,
            'psychometric_signals': psych_signals,
            'sentiment': sentiment,
            'word_count': len(doc),
            'sentence_count': len(list(doc.sents))
        }
```

### 8.3 E25 Threat Actor Personality Profile

```python
@dataclass
class ThreatActorProfile:
    actor_id: str
    name: str
    aliases: list[str]
    motivation: str  # FINANCIAL, IDEOLOGICAL, STATE_SPONSORED, etc.
    sophistication: str  # LOW, MEDIUM, HIGH, ADVANCED
    target_sectors: list[str]
    known_ttps: list[str]  # MITRE ATT&CK TTPs

    # Personality traits (Big Five model)
    openness: float  # 0-1
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

    def risk_score(self) -> float:
        """Calculate threat actor risk score"""
        sophistication_weights = {
            'LOW': 0.2, 'MEDIUM': 0.4, 'HIGH': 0.7, 'ADVANCED': 1.0
        }

        base_score = sophistication_weights.get(self.sophistication, 0.5)

        # Adjust for personality traits
        aggression_factor = (1 - self.agreeableness) * 0.3
        persistence_factor = self.conscientiousness * 0.2
        unpredictability = self.neuroticism * 0.1

        return min(1.0, base_score + aggression_factor + persistence_factor + unpredictability)
```

---

## Links

- [00_TASKMASTER_MASTER_INDEX.md](../taskmaster/00_TASKMASTER_MASTER_INDEX.md) - Master navigation
- [DATA_SOURCES_GUIDE.md](DATA_SOURCES_GUIDE.md) - API and data source details
- [../tests/UNIT_TEST_TEMPLATE.md](../tests/UNIT_TEST_TEMPLATE.md) - Unit test patterns
- [../tests/INTEGRATION_TEST_TEMPLATE.md](../tests/INTEGRATION_TEST_TEMPLATE.md) - Integration test patterns

---

**Generated by Claude-Flow mesh swarm analysis**
**Swarm ID:** swarm_1764814789507_ywsdg0lld
