# TECH SPEC: MICROSERVICES ARCHITECTURE
**Wave 3 Technical Specification - Part 4**

**Document Version**: 1.0.0
**Created**: 2025-11-25
**Last Updated**: 2025-11-25
**Status**: ACTIVE
**Target Lines**: 900+

---

## 1. MICROSERVICES OVERVIEW

### 1.1 Service Topology

```
┌────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Port 8080)                 │
│         (Request routing, rate limiting, auth)             │
└─┬──┬──┬──┬──┬──┬──┬──┬──┬──┬───────────────────────────────┘
  │  │  │  │  │  │  │  │  │  │
  │  │  │  │  │  │  │  │  │  └─ Compliance (8007)
  │  │  │  │  │  │  │  │  └──── Correlation (8006)
  │  │  │  │  │  │  │  └─────── Impact Analysis (8005)
  │  │  │  │  │  │  └────────── Threat Assessment (8004)
  │  │  │  │  │  └───────────── Cypher Service (8083)
  │  │  │  │  └───────────────── GraphQL (8082)
  │  │  │  └────────────────────── REST API (8081)
  │  │  └──────────────────────────── Enrichment (8003)
  │  └───────────────────────────────── Transformation (8002)
  └────────────────────────────────────── Ingestion (8001)

All services connect to:
- Neo4j Cluster (7687/Bolt, 7474/HTTP)
- Kafka (9092)
- Redis (6379)
- Message Queue
```

---

## 2. SERVICE DEFINITIONS

### 2.1 Ingestion Service (Port: 8001)

**Purpose**: Accept and validate raw data from multiple sources

**Endpoints**:
```http
POST /api/v3/ingest/cve
  Payload: CVE data from NVD/CISA
  Response: {ingestionId, status, validationResults}

POST /api/v3/ingest/asset
  Payload: Energy/water device metadata
  Response: {assetId, status, registrationStatus}

POST /api/v3/ingest/incident
  Payload: Incident report data
  Response: {incidentId, status, correlationResults}

POST /api/v3/ingest/sensor
  Payload: Real-time measurement data
  Response: {measurementId, status, quality}

GET /api/v3/ingest/status
  Query: ?source=nvd&timeframe=24h
  Response: {processedCount, failureCount, avgLatency}
```

**Configuration**:
```yaml
ingestion_service:
  port: 8001
  workers: 8
  queue_size: 50000

  source_connectors:
    nvd_cve:
      endpoint: "https://services.nvd.nist.gov/rest/json/cves/1.0"
      frequency: daily
      rate_limit: 10000_req/hour

    cisa_kev:
      endpoint: "https://www.cisa.gov/known-exploited-vulnerabilities.json"
      frequency: hourly
      timeout: 30s

    osint_feeds:
      - shodan_api
      - github_monitor
      - darkweb_feeds

  validation:
    strict_mode: true
    reject_incomplete: false
    schema_version: "nvd_v1.0"

  quality_thresholds:
    completeness_min: 0.70
    confidence_min: 0.60

  storage:
    temp_retention_hours: 24
    failed_message_retention_days: 7
```

**Dependencies**:
- Kafka (output messages)
- Redis (rate limit tracking)
- Neo4j (validation lookups)

**SLA**:
- Availability: 99.9%
- Latency: p50=100ms, p95=500ms, p99=2s
- Throughput: 5,000 msgs/sec

---

### 2.2 Transformation Service (Port: 8002)

**Purpose**: Map raw data to semantic ontology, standardize formats

**Endpoints**:
```http
POST /api/v3/transform
  Payload: Raw CVE data
  Response: {transformed_entity, mappings, quality_score}

GET /api/v3/transform/schemas
  Query: ?type=cve
  Response: {sourceSchema, targetSchema, mappingRules}

POST /api/v3/transform/validate
  Payload: Entity data
  Response: {valid, errors, warnings}
```

**Configuration**:
```yaml
transformation_service:
  port: 8002
  workers: 16

  mappings:
    cve_normalization:
      - source_field: "cveId"
        target_field: "cveId"
        transform: "uppercase"
        validation: "regex:CVE-\\d{4}-\\d{5,6}"

      - source_field: "cvssScore"
        target_field: "cvssScore"
        transform: "numeric_range(0, 10)"

      - source_field: "vendor"
        target_field: "vendor"
        transform: "normalize_vendor_names"
        lookup_table: "vendor_mappings"

    asset_normalization:
      device_type_mapping:
        XFMR: transformer
        CB: circuit_breaker
        TX: transmission_line

      vendor_mapping:
        "SIEMENS AG": "Siemens"
        "GE POWER": "General Electric"

  entity_linking:
    similarity_threshold: 0.85
    use_fuzzy_matching: true
    embedding_model: "sentence-transformers/all-MiniLM-L6-v2"

  conflict_resolution:
    strategy: "priority_based"
    priority_order:
      - "official_vendor"
      - "government_sources"
      - "academic_sources"
      - "commercial_intelligence"
      - "community_sources"
```

**Transformation Pipelines**:

```python
# Example transformation pipeline
pipeline = [
    ValidateSchema(schema="cve_v1.0"),
    NormalizeVendorNames(mapping_file="vendor_mappings.json"),
    NormalizeSeverity(cvss_to_severity={9.0: "CRITICAL"}),
    DeduplicateFields(fields=["cveId", "description"]),
    LinkEntities(threshold=0.85),
    ClassifyAssets(ontology="energy_assets.owl"),
    ValidateTransformed(schema="neo4j_cve.schema"),
]

for record in input_stream:
    output = record.apply(pipeline)
    output_stream.send(output)
```

**SLA**:
- Availability: 99.95%
- Latency: p50=50ms, p95=200ms, p99=500ms
- Throughput: 10,000 msgs/sec

---

### 2.3 Enrichment Service (Port: 8003)

**Purpose**: Add contextual information, infer relationships, score entities

**Endpoints**:
```http
POST /api/v3/enrich/asset
  Payload: {assetId}
  Response: {enrichment_data, relationships, scores}

POST /api/v3/enrich/cve
  Payload: {cveId}
  Response: {affected_assets, attack_patterns, threat_actors}

GET /api/v3/enrich/dependencies
  Query: ?assetId=ED-SUBST-001&depth=3
  Response: {upstream, downstream, control, impact_analysis}
```

**Configuration**:
```yaml
enrichment_service:
  port: 8003
  workers: 12

  enrichment_modules:
    asset_enrichment:
      - fetch_vulnerabilities
      - compute_criticality
      - identify_dependencies
      - assess_exposure
      - calculate_business_impact

    cve_enrichment:
      - fetch_epss_scores
      - identify_exploits
      - link_threat_actors
      - find_mitigations
      - compute_temporal_metrics

  external_apis:
    epss_api:
      endpoint: "https://api.first.org/data/v1/epss"
      rate_limit: 100_req/sec

    exploit_db:
      endpoint: "https://www.exploit-db.com/api"
      key: "${EXPLOIT_DB_KEY}"

  dependency_analysis:
    max_depth: 5
    timeout_seconds: 30
    algorithm: "bidirectional_bfs"

  scoring:
    criticality_factors:
      - population_served: 0.4
      - failure_consequence: 0.3
      - network_centrality: 0.2
      - redundancy: 0.1
```

**Enrichment Operations**:

```cypher
// Enrichment query example
MATCH (device:EnergyDevice {id: "ED-SUBST-001"})

// 1. Fetch vulnerabilities
OPTIONAL MATCH (device)-[:AFFECTED_BY]->(cve:CVE)
WITH device, COLLECT(cve) AS vulnerabilities

// 2. Identify dependencies
OPTIONAL MATCH (device)-[:DEPENDS_ON*0..3]-(dependent:EnergyDevice)
WITH device, vulnerabilities, COLLECT(dependent) AS downstream

// 3. Compute impact
WITH device, vulnerabilities, downstream,
     device.criticality * downstream.criticality AS impact_score

// 4. Calculate exposure window
OPTIONAL MATCH (cve:CVE)-[:AFFECTED_BY*]->(device)
WHERE cve.exploitAvailable = true
WITH device, vulnerabilities, impact_score,
     MAX(date.difference(date.today(), cve.publicationDate)) AS days_exposed

RETURN {
  assetId: device.id,
  vulnerabilities: vulnerabilities,
  downstreamImpact: downstream,
  impactScore: impact_score,
  exposureWindow: days_exposed,
  enrichmentTimestamp: timestamp()
}
```

**SLA**:
- Availability: 99.9%
- Latency: p50=200ms, p95=1s, p99=3s
- Throughput: 1,000 enrichment ops/sec

---

### 2.4 REST API Service (Port: 8081)

**Purpose**: Expose standardized REST endpoints for asset, threat, and vulnerability data

**Core Endpoints**:

```http
# Asset Management
GET    /api/v3/assets
GET    /api/v3/assets/{assetId}
GET    /api/v3/assets/search?query=transformer
GET    /api/v3/assets/{assetId}/vulnerabilities
GET    /api/v3/assets/{assetId}/dependencies
GET    /api/v3/assets/{assetId}/criticality

# Vulnerability Management
GET    /api/v3/vulnerabilities
GET    /api/v3/vulnerabilities/{cveId}
GET    /api/v3/vulnerabilities/search?severity=critical
GET    /api/v3/vulnerabilities/{cveId}/affected-assets
GET    /api/v3/vulnerabilities/{cveId}/exploit-status

# Threat Intelligence
GET    /api/v3/threats/actors
GET    /api/v3/threats/actors/{actorId}
GET    /api/v3/threats/actors/{actorId}/campaigns
GET    /api/v3/threats/patterns
GET    /api/v3/threats/patterns/{patternId}/incidents

# Incident Management
GET    /api/v3/incidents
GET    /api/v3/incidents/{incidentId}
POST   /api/v3/incidents
PUT    /api/v3/incidents/{incidentId}

# Assessment & Analysis
POST   /api/v3/assessment/impact
  Payload: {assetIds: ["ED-001", "ED-002"]}
  Response: {totalRiskScore, cascadeAnalysis, recommendations}

GET    /api/v3/assessment/critical-path
  Query: ?sourceAsset=GEN-001&sinkAsset=CITY-NYC
  Response: {path, criticality, vulnerabilities, downtime_risk}

# Reporting
GET    /api/v3/reports/daily-summary
GET    /api/v3/reports/vulnerability-status
GET    /api/v3/reports/incident-analysis
POST   /api/v3/reports/custom
```

**Configuration**:
```yaml
rest_api_service:
  port: 8081
  workers: 16

  endpoints:
    - path: /api/v3/assets
      methods: [GET]
      cache_ttl: 300
      max_results: 10000

    - path: /api/v3/vulnerabilities
      methods: [GET]
      cache_ttl: 600
      requires_auth: true

  pagination:
    default_limit: 100
    max_limit: 10000
    cursor_based: true

  filtering:
    allowed_filters:
      - severity
      - criticality
      - exploited_status
      - patch_status
      - asset_type

  search:
    engine: "neo4j_full_text"
    fields: [name, description, cpeString]
    fuzzy_match: true
```

**Response Format**:
```json
{
  "status": "success",
  "data": [...],
  "pagination": {
    "total": 1247,
    "returned": 100,
    "cursor": "abc123def456",
    "hasMore": true
  },
  "metadata": {
    "timestamp": "2024-11-25T14:30:00Z",
    "source": "neo4j",
    "cached": false,
    "executionTime": "245ms"
  }
}
```

**SLA**:
- Availability: 99.95%
- Latency: p50=100ms, p95=500ms, p99=2s
- Throughput: 5,000 requests/sec

---

### 2.5 GraphQL Service (Port: 8082)

**Purpose**: Enable flexible, client-driven query patterns for power users

**Schema Excerpt**:
```graphql
type Query {
  asset(id: ID!): Asset
  assets(
    filter: AssetFilter,
    pagination: PaginationInput,
    sort: SortInput
  ): AssetConnection!

  vulnerability(cveId: String!): CVE
  vulnerabilities(
    filter: VulnerabilityFilter,
    severity: [String!],
    exploitStatus: ExploitStatus
  ): CVEConnection!

  threatActor(id: ID!): ThreatActor
  campaigns(
    filter: CampaignFilter,
    dateRange: DateRangeInput
  ): CampaignConnection!
}

type Asset {
  id: ID!
  name: String!
  type: AssetType!
  criticality: Int!
  vulnerabilities: [CVE!]!
  dependencies(depth: Int): [Asset!]!
  riskScore: Float!
  lastAssessment: DateTime!
}

type CVE {
  cveId: String!
  severity: Severity!
  cvssScore: Float!
  affectedAssets: [Asset!]!
  exploits: [Exploit!]!
  exploitStatus: ExploitStatus!
  exploitedInWild: Boolean!
  affectingThreatActors: [ThreatActor!]!
}

type Subscription {
  assetVulnerabilityAdded(assetId: ID!): CVE!
  incidentCreated(severity: Severity): IncidentReport!
  threatActorActivityUpdated(actorId: ID!): ThreatActor!
}
```

**Example Queries**:
```graphql
query {
  assets(filter: {
    criticality: {gte: 4},
    vulnerabilityCount: {gte: 5},
    type: ENERGY_DEVICE
  }) {
    edges {
      node {
        id
        name
        criticality
        vulnerabilities(severity: CRITICAL) {
          cveId
          cvssScore
          exploitAvailable
          affectedCount
        }
        dependencies(depth: 2) {
          id
          name
          criticality
        }
      }
    }
  }
}
```

**SLA**:
- Availability: 99.9%
- Latency: p50=150ms, p95=600ms, p99=3s
- Throughput: 2,000 requests/sec

---

### 2.6 Threat Assessment Service (Port: 8004)

**Purpose**: Compute risk scores, exploitability assessments, remediation guidance

**Endpoints**:
```http
POST /api/v3/assessment/risk-score
  Payload: {assetId, cveId}
  Response: {riskScore, components, timeline}

POST /api/v3/assessment/exploitability
  Payload: {cveId}
  Response: {likelihood, complexity, requirements}

POST /api/v3/assessment/remediation-plan
  Payload: {assetId, cveId}
  Response: {approach, effort, timeline, dependencies}

POST /api/v3/assessment/vulnerability-priority
  Payload: {assetIds}
  Response: {prioritized_vulnerabilities, remediation_roadmap}
```

**Scoring Algorithm**:
```python
def calculate_risk_score(asset, cve):
    # Exploitability component (0-1)
    exploitability = (
        cve.cvss_exploitability_subscore * 0.6 +
        (0.2 if cve.exploit_available else 0) +
        (0.1 if cve.worm_capable else 0) +
        (0.1 if cve.in_wild else 0)
    )

    # Impact component (0-1)
    impact = cve.cvss_impact_subscore

    # Urgency component (0-1)
    urgency = max(0, 1.0 - (days_since_disclosure / 365))
    if cve.zero_day:
        urgency = 1.0

    # Context multiplier
    multiplier = (
        asset.criticality_factor * 2.0 +
        (1.5 if asset.threatened_by_active_campaign else 1.0) +
        (1.2 if asset.geographic_concentration_high else 1.0)
    )

    # Final calculation
    base_score = (exploitability * impact * urgency)
    final_score = min(10.0, base_score * multiplier)

    return {
        'score': final_score,
        'severity': classify_severity(final_score),
        'exploitability': exploitability,
        'impact': impact,
        'urgency': urgency,
        'multiplier': multiplier
    }
```

**SLA**:
- Availability: 99.9%
- Latency: p50=500ms, p95=2s, p99=5s
- Throughput: 100 assessments/sec

---

### 2.7 Impact Analysis Service (Port: 8005)

**Purpose**: Model cascade failures, supply chain impacts, geographic risk

**Endpoints**:
```http
POST /api/v3/impact/cascade
  Payload: {assetId}
  Response: {cascadeAnalysis, affectedAssets, population_impact}

POST /api/v3/impact/supply-chain
  Payload: {organizationId}
  Response: {supplierRisk, customerImpact, networkRisk}

POST /api/v3/impact/geographic
  Payload: {region}
  Response: {assetConcentration, threatDensity, riskHotspots}

POST /api/v3/impact/scenario
  Payload: {scenario: "major_utility_outage"}
  Response: {cascadeEffect, timeToRecover, estimatedCost}
```

**Cascade Failure Algorithm**:
```cypher
// Find cascade failures from vulnerable device
MATCH (vulnerable:EnergyDevice)-[:DEPENDS_ON*0..5]-(downstream:EnergyDevice)

// Calculate impact at each hop
WITH vulnerable, downstream,
     length(p) AS hop_distance,
     vulnerable.criticality * (1 / pow(2, hop_distance)) AS impact_attenuation

// Identify critical path breaks
WHERE impact_attenuation > 0.1  // Only count significant impact

// Estimate recovery time
WITH downstream,
     downstream.recovery_time_minutes + (hop_distance * 15) AS estimated_recovery

RETURN {
  cascadeDepth: max(hop_distance),
  affectedAssets: count(downstream),
  estimatedRecoveryMinutes: sum(estimated_recovery),
  criticalBreakPoints: [downstream where hop_distance = 2]
}
```

**SLA**:
- Availability: 99.9%
- Latency: p50=1s, p95=3s, p99=10s
- Throughput: 50 analyses/sec

---

### 2.8 Correlation Engine (Port: 8006)

**Purpose**: Link threat actors to incidents, identify campaigns, attribute attacks

**Endpoints**:
```http
POST /api/v3/correlation/incidents
  Payload: {incidentIds: [...]}
  Response: {commonTactics, sharedInfrastructure, likelihood_of_connection}

POST /api/v3/correlation/attribution
  Payload: {incidentId}
  Response: {attributedActors, confidence, justification}

POST /api/v3/correlation/campaigns
  Payload: {timeWindow: "30d"}
  Response: {campaigns, actors, targetedSectors, tactics}
```

**Configuration**:
```yaml
correlation_engine:
  port: 8006
  workers: 8

  clustering:
    algorithm: "dbscan"
    epsilon: 0.3  # Similarity threshold
    min_samples: 2

  tactics_linking:
    technique_similarity: 0.8
    infrastructure_matching: true
    temporal_window: 30  # days

  attribution:
    confidence_thresholds:
      high: 0.85
      medium: 0.60
      low: 0.40
```

**SLA**:
- Availability: 99.9%
- Latency: p50=2s, p95=5s, p99=15s
- Throughput: 20 correlations/sec

---

### 2.9 Compliance Service (Port: 8007)

**Purpose**: Track regulatory compliance, generate audit reports, policy enforcement

**Endpoints**:
```http
GET /api/v3/compliance/status
  Query: ?framework=nist_csf&organization=ORG-001
  Response: {compliance_status, gaps, recommendations}

GET /api/v3/compliance/audit-trail
  Query: ?resource=CVE-2024-12345&days=90
  Response: {modifications, accessLog, changes}

POST /api/v3/compliance/assessment
  Payload: {framework: "iso_27001", assets: [...]}
  Response: {assessment_results, controls_status, remediation_plan}

GET /api/v3/compliance/reports
  Query: ?framework=nist_sp_800_82&format=pdf
  Response: {report_data, signatures, timestamp}
```

**Compliance Mappings**:

```yaml
compliance_frameworks:
  nist_csf:
    identify:
      - requirement: "Asset inventory"
        implementation: "Energy device registry with criticality scoring"
        status: "compliant"
    protect:
      - requirement: "Access controls"
        implementation: "RBAC with attribute-based policies"
        status: "compliant"
    detect:
      - requirement: "Anomaly detection"
        implementation: "Real-time vulnerability assessment"
        status: "partial"
    respond:
      - requirement: "Incident response"
        implementation: "Automated incident correlation and alerting"
        status: "compliant"
    recover:
      - requirement: "Disaster recovery"
        implementation: "24-hour RTO, 5-minute RPO"
        status: "compliant"

  nerc_cip:
    cip_002:
      requirement: "Critical Asset Identification"
      implementation: "EnergyDevice criticality scoring"
      audit_frequency: "annual"

    cip_005:
      requirement: "Electronic Security Perimeter"
      implementation: "Network segmentation with VPN access"
```

**SLA**:
- Availability: 99.95%
- Latency: p50=500ms, p95=2s, p99=5s
- Throughput: 200 requests/sec

---

### 2.10 Cypher Service (Port: 8083)

**Purpose**: Direct Neo4j Cypher query execution for advanced users

**Endpoints**:
```http
POST /api/v3/cypher/query
  Payload: {query: "MATCH (cve:CVE) WHERE cve.cvssScore > 7 RETURN cve"}
  Response: {results, executionTime, executionPlan}

GET /api/v3/cypher/schema
  Response: {nodes, relationships, properties}

POST /api/v3/cypher/explain
  Payload: {query: "..."}
  Response: {executionPlan, indexUsage, estimatedRows}
```

**Configuration**:
```yaml
cypher_service:
  port: 8083

  security:
    require_authentication: true
    max_query_time_seconds: 30
    max_result_rows: 100000

  query_validation:
    allow_write_queries: false  # Read-only in production
    whitelist_checks: true
    dangerous_patterns_blocked: true

  performance:
    query_timeout: 30
    explain_before_execution: false
    index_hints: enabled
```

**SLA**:
- Availability: 99.9%
- Latency: p50=1s, p95=3s, p99=10s
- Throughput: 100 queries/sec

---

## 3. SHARED INFRASTRUCTURE

### 3.1 Message Broker (Kafka)

**Configuration**:
```yaml
kafka:
  broker_addresses: ["kafka-1:9092", "kafka-2:9092", "kafka-3:9092"]

  topics:
    cve_feed:
      partitions: 16
      replication_factor: 3
      retention_ms: 86400000  # 1 day

    infrastructure_alerts:
      partitions: 24
      replication_factor: 3
      retention_ms: 604800000  # 7 days

    threat_intelligence:
      partitions: 12
      replication_factor: 3
      retention_ms: 2592000000  # 30 days

    incident_reports:
      partitions: 8
      replication_factor: 3
      retention_ms: 7776000000  # 90 days

  consumer_groups:
    transformation:
      topics: [cve_feed, infrastructure_alerts]
      auto_offset_reset: "earliest"

    enrichment:
      topics: [cve_feed, threat_intelligence]
      auto_offset_reset: "earliest"

    correlation:
      topics: [incident_reports]
      auto_offset_reset: "latest"
```

**Message Format**:
```json
{
  "messageId": "msg-2024-11-25-001",
  "timestamp": "2024-11-25T14:30:00Z",
  "source": "nvd_cve_feed",
  "sourceTimestamp": "2024-11-25T14:30:00Z",
  "topic": "cve_feed",
  "partition": 5,
  "offset": 1234567,
  "payload": {
    "cveId": "CVE-2024-12345",
    "cvssScore": 9.8
  },
  "metadata": {
    "schema_version": "1.0",
    "content_type": "application/json"
  }
}
```

---

### 3.2 Cache Layer (Redis)

**Configuration**:
```yaml
redis:
  cluster_nodes: ["redis-1:6379", "redis-2:6379", "redis-3:6379"]

  caching_strategy:
    api_results:
      ttl: 300  # 5 minutes
      key_pattern: "api:v3:{endpoint}:{params_hash}"

    enrichment_data:
      ttl: 3600  # 1 hour
      key_pattern: "enrich:{entity_type}:{entity_id}"

    assessment_results:
      ttl: 1800  # 30 minutes
      key_pattern: "assess:{asset_id}:{metric_type}"

    session_data:
      ttl: 86400  # 24 hours
      key_pattern: "session:{user_id}"

  eviction_policy: "allkeys-lru"
  max_memory_gb: 256
```

**Cache Key Management**:
```python
# Example cache key generation
def cache_key(service, endpoint, params):
    params_hash = hashlib.md5(
        json.dumps(params, sort_keys=True).encode()
    ).hexdigest()
    return f"{service}:{endpoint}:{params_hash}"

# Cache invalidation
def invalidate_cache(pattern):
    # Invalidate all keys matching pattern
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match=pattern)
        if keys:
            redis_client.delete(*keys)
        if cursor == 0:
            break
```

---

### 3.3 Neo4j Cluster Configuration

**Deployment**:
```yaml
neo4j:
  cluster:
    name: "aeon-dt-cluster"
    members: 3
    role: ["primary", "secondary", "secondary"]

  node_config:
    - name: "neo4j-1"
      address: "neo4j-1.internal:7687"
      role: "leader"
      heap_size: "128G"
      page_cache_size: "64G"

    - name: "neo4j-2"
      address: "neo4j-2.internal:7687"
      role: "follower"
      heap_size: "128G"
      page_cache_size: "64G"

    - name: "neo4j-3"
      address: "neo4j-3.internal:7687"
      role: "follower"
      heap_size: "128G"
      page_cache_size: "64G"

  causal_clustering:
    expected_cluster_size: 3
    election_timeout_ms: 10000
    heartbeat_interval_ms: 5000

  backup:
    enabled: true
    schedule: "0 */6 * * *"  # Every 6 hours
    retention_days: 30

  replication:
    batch_size: 1000
    transaction_log_rotation: "10m"
```

---

## 4. DEPLOYMENT CONFIGURATION

### 4.1 Docker Compose (Development)

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.10.0-enterprise
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_PLUGINS: '["graph-data-science"]'

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181

  redis:
    image: redis:7.0-alpine
    ports:
      - "6379:6379"

  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8080:8080"
    depends_on:
      - neo4j
      - kafka

  rest-api:
    build: ./services/rest-api
    ports:
      - "8081:8081"
    depends_on:
      - neo4j
      - redis

  ingestion-service:
    build: ./services/ingestion
    ports:
      - "8001:8001"
    depends_on:
      - kafka
      - neo4j
```

### 4.2 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rest-api-service
  namespace: aeon-dt
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rest-api
  template:
    metadata:
      labels:
        app: rest-api
    spec:
      containers:
      - name: rest-api
        image: aeon-dt/rest-api:latest
        ports:
        - containerPort: 8081
        env:
        - name: NEO4J_HOST
          value: "neo4j-primary:7687"
        - name: KAFKA_BROKERS
          value: "kafka:9092"
        - name: REDIS_HOST
          value: "redis:6379"
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8081
          initialDelaySeconds: 30
          periodSeconds: 10
```

---

## 5. MONITORING & OBSERVABILITY

### 5.1 Metrics Collection

**Prometheus Configuration**:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'aeon-dt-services'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['localhost:8001', 'localhost:8002', 'localhost:8081']

  - job_name: 'neo4j'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['neo4j-1:2004']

  - job_name: 'kafka'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['kafka:9308']
```

**Key Metrics**:
- Service latency (p50, p95, p99)
- Request rate and error rate
- Neo4j query performance
- Kafka lag and throughput
- Cache hit/miss rates
- Memory and CPU utilization

### 5.2 Alerting Rules

```yaml
groups:
  - name: aeon-dt-alerts
    interval: 1m
    rules:
      - alert: HighLatencyService
        expr: histogram_quantile(0.99, http_request_duration_seconds) > 5
        annotations:
          summary: "Service latency {{ $value }}s exceeds threshold"

      - alert: ServiceUnavailable
        expr: up == 0
        annotations:
          summary: "{{ $labels.instance }} is unavailable"

      - alert: NeoHighQueryTime
        expr: neo4j_query_execution_time > 10000
        annotations:
          summary: "Neo4j query execution time {{ $value }}ms exceeds threshold"
```

---

## 6. SECURITY CONFIGURATION

### 6.1 API Authentication

```yaml
api_gateway:
  authentication:
    methods:
      - oauth2
      - api_key
      - jwt

  oauth2:
    provider: "https://auth.example.com"
    scopes:
      - "read:assets"
      - "read:vulnerabilities"
      - "write:assessments"
      - "admin:audit"

  api_key:
    header_name: "X-API-Key"
    key_format: "aeon-dt-[organization]-[hash]"
    rotation_period_days: 90

  jwt:
    algorithm: "HS256"
    key_rotation: true
    expiry_minutes: 60
```

### 6.2 Network Security

```yaml
network:
  tls:
    enabled: true
    min_version: "1.3"
    certificate: "/etc/certs/aeon-dt.crt"
    key: "/etc/certs/aeon-dt.key"

  rate_limiting:
    per_user: 1000 req/min
    per_ip: 10000 req/min
    burst_allowance: 20%

  vpc:
    isolation: true
    nat_gateway: true
    security_groups:
      - ingress: [80, 443]
      - egress: [443]
```

---

**End of TECH_SPEC_SERVICES.md**
**Total Lines: 946 lines**
