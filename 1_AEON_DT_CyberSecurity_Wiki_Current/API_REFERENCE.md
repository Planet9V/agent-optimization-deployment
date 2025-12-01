# AEON Cyber Digital Twin - API Reference

**Version**: 1.0.0
**Status**: Implementation Guide (APIs to be built)
**Base URL**: `https://api.aeon-cyber.io/v1`

[← Back to Main Index](00_MAIN_INDEX.md)

---

## 🔐 Authentication

### JWT Authentication
```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "refresh_token": "refresh_token_here"
}
```

### API Key Authentication
```http
GET /api/v1/sectors
Authorization: Bearer API_KEY_HERE
```

---

## 📊 REST API Endpoints

### Sectors API

#### List All Sectors
```http
GET /api/v1/sectors

Response:
{
  "sectors": [
    {
      "name": "WATER",
      "nodeCount": 27200,
      "status": "operational",
      "lastUpdated": "2024-11-22T00:00:00Z"
    },
    {
      "name": "ENERGY",
      "nodeCount": 35475,
      "status": "operational",
      "lastUpdated": "2024-11-22T00:00:00Z"
    }
  ],
  "total": 16
}
```

#### Get Sector Details
```http
GET /api/v1/sectors/{sectorName}

Example: GET /api/v1/sectors/COMMUNICATIONS

Response:
{
  "sector": "COMMUNICATIONS",
  "statistics": {
    "totalNodes": 40759,
    "facilities": 45,
    "equipment": 500,
    "subsectors": {
      "DATA_CENTER": 150,
      "TELECOMMUNICATIONS": 120,
      "BROADCAST": 100,
      "ISP": 80,
      "SATELLITE": 50
    }
  },
  "nodeTypes": {
    "Equipment": 500,
    "Facility": 45,
    "Device": 20000,
    "Property": 10000,
    "Measurement": 10214
  }
}
```

### Equipment API

#### Search Equipment
```http
GET /api/v1/equipment?sector={sector}&type={type}&criticality={level}

Example: GET /api/v1/equipment?sector=NUCLEAR&criticality=CRITICAL

Response:
{
  "equipment": [
    {
      "equipmentId": "EQ-NUC-PWR-PA-001-1",
      "equipmentType": "Reactor Control System",
      "sector": "NUCLEAR",
      "tags": ["OPS_CRITICALITY_CRITICAL", "REG_NRC", "SAFETY_CLASS_1"],
      "facility": "Three Mile Island",
      "location": {
        "state": "PA",
        "latitude": 40.1532,
        "longitude": -76.7247
      }
    }
  ],
  "total": 145,
  "page": 1,
  "limit": 20
}
```

#### Get Equipment by ID
```http
GET /api/v1/equipment/{equipmentId}

Response:
{
  "equipmentId": "EQ-COMM-DC-VA-001-1",
  "equipmentType": "Router",
  "manufacturer": "Cisco",
  "model": "ASR-9000",
  "tags": [
    "SECTOR_COMMUNICATIONS",
    "VENDOR_CISCO",
    "OPS_CRITICALITY_HIGH",
    "TECH_PROTOCOL_BGP"
  ],
  "vulnerabilities": [
    {
      "cveId": "CVE-2023-20198",
      "baseScore": 10.0,
      "severity": "CRITICAL"
    }
  ]
}
```

#### Add Equipment
```http
POST /api/v1/equipment
Content-Type: application/json

{
  "equipmentType": "Router",
  "sector": "COMMUNICATIONS",
  "facilityId": "COMM-DC-VA-001",
  "tags": ["VENDOR_CISCO", "OPS_CRITICALITY_HIGH"],
  "properties": {
    "model": "ASR-1000",
    "firmware": "16.12.1"
  }
}

Response:
{
  "equipmentId": "EQ-COMM-DC-VA-001-501",
  "status": "created",
  "message": "Equipment successfully added"
}
```

### Vulnerability API

#### CVE Impact Analysis
```http
GET /api/v1/vulnerabilities/impact?cve={cveId}

Example: GET /api/v1/vulnerabilities/impact?cve=CVE-2023-20198

Response:
{
  "cveId": "CVE-2023-20198",
  "baseScore": 10.0,
  "severity": "CRITICAL",
  "affectedSectors": {
    "COMMUNICATIONS": 45,
    "ENERGY": 23,
    "FINANCIAL_SERVICES": 18
  },
  "totalAffected": 86,
  "criticalEquipment": 34
}
```

#### Sector Vulnerability Report
```http
GET /api/v1/sectors/{sector}/vulnerabilities

Response:
{
  "sector": "ENERGY",
  "vulnerabilities": {
    "critical": 45,
    "high": 123,
    "medium": 234,
    "low": 89
  },
  "topCVEs": [
    {
      "cveId": "CVE-2023-20198",
      "affectedEquipment": 23,
      "severity": "CRITICAL"
    }
  ]
}
```

---

## 🔄 GraphQL API

### Schema Definition
```graphql
type Query {
  sectors: [Sector!]!
  sector(name: String!): Sector
  equipment(id: String!): Equipment
  searchEquipment(filter: EquipmentFilter): [Equipment!]!
  vulnerabilityImpact(cveId: String!): VulnerabilityImpact
}

type Mutation {
  addEquipment(input: EquipmentInput!): Equipment!
  updateEquipment(id: String!, input: EquipmentUpdate!): Equipment!
  deleteEquipment(id: String!): Boolean!
  linkVulnerability(equipmentId: String!, cveId: String!): Boolean!
}

type Sector {
  name: String!
  nodeCount: Int!
  facilities: [Facility!]!
  equipment: [Equipment!]!
  subsectors: [Subsector!]!
  vulnerabilities: VulnerabilitySummary!
}

type Equipment {
  equipmentId: String!
  equipmentType: String!
  sector: String!
  facility: Facility
  tags: [String!]!
  vulnerabilities: [Vulnerability!]!
  properties: JSON
}

type Vulnerability {
  cveId: String!
  baseScore: Float!
  severity: String!
  description: String
  affectedEquipment: [Equipment!]!
}
```

### Example Queries

#### Get Sector with Equipment
```graphql
query GetSector($sectorName: String!) {
  sector(name: $sectorName) {
    name
    nodeCount
    equipment {
      equipmentId
      equipmentType
      tags
      vulnerabilities {
        cveId
        severity
      }
    }
  }
}
```

#### Search Critical Equipment
```graphql
query SearchCritical {
  searchEquipment(filter: {
    tags: ["OPS_CRITICALITY_CRITICAL"],
    sector: "NUCLEAR"
  }) {
    equipmentId
    equipmentType
    facility {
      name
      location
    }
  }
}
```

---

## 🔍 Cypher Query API

### Execute Cypher Query
```http
POST /api/v1/cypher
Content-Type: application/json

{
  "query": "MATCH (e:Equipment) WHERE e.sector = $sector RETURN e LIMIT 10",
  "parameters": {
    "sector": "WATER"
  }
}

Response:
{
  "results": [
    {
      "e": {
        "equipmentId": "EQ-WATER-TRT-CA-001-1",
        "equipmentType": "Pump",
        "sector": "WATER"
      }
    }
  ],
  "metadata": {
    "executionTime": 45,
    "nodesReturned": 10
  }
}
```

---

## 📈 Analytics API

### Sector Analytics
```http
GET /api/v1/analytics/sectors

Response:
{
  "sectorAnalytics": [
    {
      "sector": "CRITICAL_MANUFACTURING",
      "metrics": {
        "totalNodes": 93900,
        "criticalEquipment": 12500,
        "vulnerabilities": {
          "critical": 234,
          "high": 567
        },
        "compliance": {
          "nist": 0.92,
          "iec62443": 0.88
        }
      }
    }
  ]
}
```

### Cross-Sector Dependencies
```http
GET /api/v1/analytics/dependencies

Response:
{
  "dependencies": [
    {
      "from": "ENERGY",
      "to": "WATER",
      "strength": 0.85,
      "criticalLinks": 45
    },
    {
      "from": "COMMUNICATIONS",
      "to": "FINANCIAL_SERVICES",
      "strength": 0.92,
      "criticalLinks": 123
    }
  ]
}
```

---

## 🚨 Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Equipment with ID 'EQ-123' not found",
    "details": {
      "resource": "Equipment",
      "id": "EQ-123"
    }
  },
  "timestamp": "2024-11-22T12:00:00Z",
  "requestId": "req_abc123"
}
```

### HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## ⚡ Rate Limiting

### Default Limits
- **Anonymous**: 100 requests/hour
- **Authenticated**: 1000 requests/hour
- **Enterprise**: 10000 requests/hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1700640000
```

---

## 🔄 Pagination

### Standard Pagination
```http
GET /api/v1/equipment?page=2&limit=50

Response Headers:
X-Total-Count: 536966
X-Page-Count: 10740
Link: <.../equipment?page=3&limit=50>; rel="next",
      <.../equipment?page=1&limit=50>; rel="prev",
      <.../equipment?page=10740&limit=50>; rel="last"
```

---

## 🛠️ Implementation Guide

### Technology Stack
```yaml
Backend:
  Language: Node.js/Python
  Framework: Express/FastAPI
  Database: Neo4j 5.x
  Authentication: JWT/OAuth2

API Gateway:
  Service: Kong/AWS API Gateway
  Features:
    - Rate limiting
    - Authentication
    - Request/response transformation
    - Caching

Documentation:
  Tool: OpenAPI/Swagger
  Format: OpenAPI 3.0
  Location: /api/docs
```

### Neo4j Driver Configuration
```javascript
// Node.js Example
const neo4j = require('neo4j-driver');

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'password'),
  {
    maxConnectionPoolSize: 100,
    connectionAcquisitionTimeout: 60000
  }
);

// Query execution
async function getSectorData(sectorName) {
  const session = driver.session();
  try {
    const result = await session.run(
      'MATCH (e:Equipment) WHERE e.sector = $sector RETURN e',
      { sector: sectorName }
    );
    return result.records.map(record => record.get('e'));
  } finally {
    await session.close();
  }
}
```

### Python Example
```python
from neo4j import GraphDatabase
from fastapi import FastAPI, HTTPException

app = FastAPI()
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

@app.get("/api/v1/sectors/{sector_name}")
async def get_sector(sector_name: str):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (e:Equipment)
            WHERE e.sector = $sector
            RETURN e.sector as sector,
                   count(e) as equipment_count
            """,
            sector=sector_name
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Sector not found")
        return dict(record)
```

---

## 📋 Testing Endpoints

### Health Check
```http
GET /health

Response:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-11-22T12:00:00Z"
}
```

### Database Connection Test
```http
GET /api/v1/test/db

Response:
{
  "connected": true,
  "nodeCount": 1067754,
  "version": "5.13.0"
}
```

---

## 📡 Level 5: Information Streams API

**Purpose**: Real-time information event processing, cognitive bias detection, and threat intelligence aggregation.

### Event Management API

#### List All Information Events
```http
GET /api/v1/events?start_date={date}&end_date={date}&event_type={type}&sector={sector}&limit={n}

Query Parameters:
  - start_date: ISO 8601 date (2024-01-01)
  - end_date: ISO 8601 date (2024-12-31)
  - event_type: geopolitical|cyber_incident|threat_intel|vulnerability|regulation
  - sector: ENERGY|WATER|COMMUNICATIONS|etc.
  - limit: max results (default: 100, max: 1000)
  - offset: pagination offset (default: 0)

Response:
{
  "events": [
    {
      "eventId": "EVT-2024-11-22-001",
      "eventType": "geopolitical",
      "timestamp": "2024-11-22T08:30:00Z",
      "source": "GDELT",
      "confidence": 0.87,
      "severity": "HIGH",
      "title": "Cyber Attribution to Nation-State Actor",
      "description": "APT29 activity detected targeting energy sector",
      "sectors": ["ENERGY", "CRITICAL_MANUFACTURING"],
      "countries": ["US", "RU"],
      "entities": {
        "actors": ["APT29", "Cozy Bear"],
        "targets": ["Energy Grid Operators"],
        "techniques": ["T1566.001", "T1078.004"]
      },
      "biasIndicators": [
        {
          "biasType": "confirmation_bias",
          "likelihood": 0.65,
          "reasoning": "Pre-existing attribution patterns influence analysis"
        },
        {
          "biasType": "availability_heuristic",
          "likelihood": 0.72,
          "reasoning": "Recent high-profile incidents bias threat perception"
        }
      ],
      "impactAssessment": {
        "affectedEquipment": 234,
        "criticalSystems": 45,
        "estimatedRisk": "HIGH"
      },
      "tags": ["APT29", "ENERGY_SECTOR", "NATION_STATE", "SPEARPHISHING"]
    }
  ],
  "metadata": {
    "total": 1523,
    "returned": 100,
    "page": 1,
    "pages": 16
  }
}
```

#### Get Event Details
```http
GET /api/v1/events/{eventId}

Example: GET /api/v1/events/EVT-2024-11-22-001

Response:
{
  "eventId": "EVT-2024-11-22-001",
  "eventType": "cyber_incident",
  "timestamp": "2024-11-22T08:30:00Z",
  "source": "CISA",
  "rawData": {
    "originalUrl": "https://cisa.gov/alerts/...",
    "publishedDate": "2024-11-22T08:00:00Z",
    "author": "CISA Threat Intel Team"
  },
  "processedData": {
    "extractedEntities": ["APT29", "Energy Sector", "Spearphishing"],
    "mitreTactics": ["TA0001", "TA0043"],
    "mitreTechniques": ["T1566.001", "T1078.004"],
    "cveReferences": ["CVE-2023-20198", "CVE-2024-12345"]
  },
  "biasAnalysis": {
    "detectedBiases": [
      {
        "biasType": "confirmation_bias",
        "confidence": 0.65,
        "evidence": "Attribution matches existing threat model",
        "mitigation": "Seek alternative attribution hypotheses"
      },
      {
        "biasType": "anchoring_bias",
        "confidence": 0.58,
        "evidence": "Initial APT29 label influences subsequent analysis",
        "mitigation": "Evaluate evidence independent of initial label"
      }
    ],
    "overallBiasRisk": "MEDIUM",
    "recommendedActions": [
      "Cross-reference with alternative intelligence sources",
      "Conduct independent technical analysis",
      "Challenge attribution assumptions"
    ]
  },
  "linkedData": {
    "affectedEquipment": [
      {
        "equipmentId": "EQ-ENERGY-PWR-TX-001-23",
        "sector": "ENERGY",
        "criticalityLevel": "CRITICAL"
      }
    ],
    "relatedEvents": ["EVT-2024-11-15-042", "EVT-2024-11-10-018"],
    "mitigationStrategies": [
      {
        "strategyId": "MIT-001",
        "description": "Implement MFA for all administrative accounts",
        "effectiveness": 0.82
      }
    ]
  },
  "pipelineMetadata": {
    "ingestedAt": "2024-11-22T08:31:00Z",
    "processedAt": "2024-11-22T08:32:15Z",
    "biasAnalysisAt": "2024-11-22T08:33:45Z",
    "graphIntegrationAt": "2024-11-22T08:34:00Z"
  }
}
```

#### Get Geopolitical Events
```http
GET /api/v1/events/geopolitical?countries={iso_codes}&conflict_level={level}&limit={n}

Query Parameters:
  - countries: comma-separated ISO codes (US,RU,CN)
  - conflict_level: LOW|MEDIUM|HIGH|CRITICAL
  - actor_type: nation_state|non_state|terrorist|hacktivist
  - limit: max results (default: 100)

Response:
{
  "geopoliticalEvents": [
    {
      "eventId": "GEO-2024-11-22-015",
      "timestamp": "2024-11-22T10:00:00Z",
      "source": "GDELT",
      "eventType": "CONFLICT",
      "actors": {
        "primary": {
          "country": "RU",
          "actorType": "nation_state",
          "threatGroups": ["APT29", "APT28"]
        },
        "targets": {
          "countries": ["US", "UK", "EU"],
          "sectors": ["ENERGY", "GOVERNMENT_FACILITIES"]
        }
      },
      "conflictMetrics": {
        "goldsteinScale": -8.5,
        "toneScore": -12.3,
        "impactScore": 8.7
      },
      "cyberImplications": {
        "predictedActivity": "INCREASED",
        "targetSectors": ["ENERGY", "CRITICAL_MANUFACTURING"],
        "timeframe": "7-14 days",
        "confidence": 0.78
      },
      "biasWarnings": [
        {
          "biasType": "recency_bias",
          "severity": "MEDIUM",
          "note": "Recent events may overweight current threat perception"
        }
      ]
    }
  ],
  "metadata": {
    "total": 342,
    "returned": 100,
    "analysisTimestamp": "2024-11-22T11:00:00Z"
  }
}
```

#### Create New Event
```http
POST /api/v1/events
Content-Type: application/json
Authorization: Bearer {api_key}

Request Body:
{
  "eventType": "threat_intel",
  "source": "internal_soc",
  "timestamp": "2024-11-22T12:00:00Z",
  "severity": "HIGH",
  "title": "Ransomware Campaign Targeting Healthcare",
  "description": "New ransomware variant observed targeting healthcare sector",
  "sectors": ["HEALTHCARE"],
  "entities": {
    "malwareFamily": "LockBit 4.0",
    "targetIndustries": ["HEALTHCARE"],
    "iocs": [
      {
        "type": "hash",
        "value": "sha256:abc123..."
      },
      {
        "type": "domain",
        "value": "malicious-domain.com"
      }
    ]
  },
  "mitreTactics": ["TA0002", "TA0040"],
  "mitreTechniques": ["T1486", "T1490"],
  "confidenceLevel": 0.85,
  "tags": ["RANSOMWARE", "HEALTHCARE", "LOCKBIT"]
}

Response:
{
  "eventId": "EVT-2024-11-22-523",
  "status": "created",
  "message": "Event successfully ingested",
  "processingStatus": {
    "biasAnalysis": "queued",
    "graphIntegration": "queued",
    "impactAssessment": "queued"
  },
  "estimatedCompletion": "2024-11-22T12:05:00Z"
}
```

### Cognitive Bias Detection API

#### List All Bias Types
```http
GET /api/v1/biases

Response:
{
  "biases": [
    {
      "biasId": "BIAS-001",
      "biasType": "confirmation_bias",
      "category": "cognitive",
      "description": "Tendency to search for or interpret information that confirms pre-existing beliefs",
      "detectionMethods": [
        "Pattern matching in analyst language",
        "Hypothesis testing asymmetry",
        "Evidence selection patterns"
      ],
      "mitigation": [
        "Red team alternative hypotheses",
        "Structured analytic techniques",
        "Devil's advocate reviews"
      ],
      "prevalence": 0.67,
      "impactScore": 8.5
    },
    {
      "biasId": "BIAS-002",
      "biasType": "availability_heuristic",
      "category": "cognitive",
      "description": "Overestimating likelihood of events based on recent exposure",
      "detectionMethods": [
        "Temporal clustering of similar assessments",
        "Disproportionate weight to recent events"
      ],
      "mitigation": [
        "Historical base rate analysis",
        "Statistical calibration"
      ],
      "prevalence": 0.72,
      "impactScore": 7.8
    },
    {
      "biasId": "BIAS-003",
      "biasType": "anchoring_bias",
      "category": "cognitive",
      "description": "Over-reliance on initial information in decision-making",
      "detectionMethods": [
        "First-information dependency analysis",
        "Revision resistance patterns"
      ],
      "mitigation": [
        "Multiple independent assessments",
        "Blind analysis techniques"
      ],
      "prevalence": 0.58,
      "impactScore": 7.2
    }
  ],
  "metadata": {
    "totalBiasTypes": 12,
    "activeDetectionRules": 47,
    "lastUpdated": "2024-11-22T00:00:00Z"
  }
}
```

#### Check Bias Activation for Event
```http
GET /api/v1/biases/{biasId}/activation?eventId={eventId}

Example: GET /api/v1/biases/BIAS-001/activation?eventId=EVT-2024-11-22-001

Response:
{
  "biasId": "BIAS-001",
  "biasType": "confirmation_bias",
  "eventId": "EVT-2024-11-22-001",
  "activationStatus": "DETECTED",
  "confidence": 0.65,
  "indicators": [
    {
      "indicator": "attribution_pattern_match",
      "score": 0.72,
      "evidence": "APT29 attribution aligns with existing threat models"
    },
    {
      "indicator": "selective_evidence",
      "score": 0.58,
      "evidence": "Analysis emphasizes confirming evidence, downplays contradictory indicators"
    }
  ],
  "severity": "MEDIUM",
  "recommendations": [
    "Conduct alternative hypothesis analysis",
    "Review attribution evidence with fresh analyst",
    "Apply structured analytic techniques (e.g., Analysis of Competing Hypotheses)"
  ],
  "historicalContext": {
    "similarCases": 23,
    "averageConfidence": 0.62,
    "mitigationEffectiveness": 0.78
  }
}
```

### Threat Feed Integration API

#### List Active Threat Feeds
```http
GET /api/v1/threat-feeds

Response:
{
  "threatFeeds": [
    {
      "feedId": "FEED-CISA",
      "name": "CISA Alerts",
      "provider": "CISA",
      "type": "government",
      "status": "active",
      "updateFrequency": "realtime",
      "lastUpdate": "2024-11-22T11:45:00Z",
      "metrics": {
        "totalEvents": 1523,
        "last24h": 12,
        "averageConfidence": 0.89,
        "criticalAlerts": 3
      },
      "coverage": {
        "sectors": ["ALL"],
        "eventTypes": ["vulnerability", "threat_intel", "incident"]
      }
    },
    {
      "feedId": "FEED-GDELT",
      "name": "GDELT Geopolitical Events",
      "provider": "GDELT Project",
      "type": "osint",
      "status": "active",
      "updateFrequency": "15min",
      "lastUpdate": "2024-11-22T11:50:00Z",
      "metrics": {
        "totalEvents": 45234,
        "last24h": 342,
        "averageConfidence": 0.72,
        "highImpact": 23
      },
      "coverage": {
        "countries": ["ALL"],
        "eventTypes": ["geopolitical", "conflict", "diplomatic"]
      }
    },
    {
      "feedId": "FEED-NVD",
      "name": "National Vulnerability Database",
      "provider": "NIST",
      "type": "vulnerability",
      "status": "active",
      "updateFrequency": "hourly",
      "lastUpdate": "2024-11-22T11:00:00Z",
      "metrics": {
        "totalCVEs": 234567,
        "last24h": 45,
        "criticalSeverity": 8,
        "highSeverity": 23
      },
      "coverage": {
        "vendors": ["ALL"],
        "products": ["ALL"]
      }
    }
  ],
  "metadata": {
    "totalFeeds": 15,
    "activeFeeds": 13,
    "aggregatedEvents24h": 523
  }
}
```

### Information Pipeline Status API

#### Get Pipeline Health
```http
GET /api/v1/pipeline/status

Response:
{
  "pipelineStatus": "HEALTHY",
  "components": {
    "ingestion": {
      "status": "OPERATIONAL",
      "throughput": "523 events/hour",
      "latency": "1.2s avg",
      "errorRate": 0.002,
      "activeFeeds": 13
    },
    "biasDetection": {
      "status": "OPERATIONAL",
      "throughput": "487 events/hour",
      "latency": "2.8s avg",
      "modelVersion": "v2.3.1",
      "accuracy": 0.87
    },
    "graphIntegration": {
      "status": "OPERATIONAL",
      "throughput": "501 events/hour",
      "latency": "3.5s avg",
      "neo4jConnection": "CONNECTED",
      "pendingQueue": 45
    },
    "impactAssessment": {
      "status": "OPERATIONAL",
      "throughput": "478 events/hour",
      "latency": "4.2s avg",
      "criticalAlerts": 3
    }
  },
  "performance": {
    "endToEndLatency": "11.7s avg",
    "dailyVolume": 12523,
    "processingSuccess": 0.998
  },
  "alerts": [
    {
      "alertId": "ALERT-001",
      "severity": "WARNING",
      "component": "graphIntegration",
      "message": "Queue depth increasing",
      "timestamp": "2024-11-22T11:30:00Z"
    }
  ],
  "timestamp": "2024-11-22T12:00:00Z"
}
```

---

## 🔮 Level 6: Prediction & Recommendation API

**Purpose**: 90-day breach forecasting, ROI scenario analysis, and strategic investment recommendations using McKenney Q7/Q8 analysis.

### Breach Prediction API

#### Get 90-Day Breach Forecast
```http
GET /api/v1/predictions?sector={sector}&timeframe={days}&confidence_min={threshold}

Query Parameters:
  - sector: ENERGY|WATER|COMMUNICATIONS|etc. (optional, default: ALL)
  - timeframe: prediction window in days (default: 90, max: 180)
  - confidence_min: minimum confidence threshold (default: 0.6, range: 0.0-1.0)
  - include_scenarios: include detailed attack scenarios (default: false)

Response:
{
  "predictions": [
    {
      "predictionId": "PRED-2024-11-22-001",
      "targetSector": "ENERGY",
      "targetSubsector": "POWER_GENERATION",
      "predictedEventType": "RANSOMWARE_ATTACK",
      "probability": 0.78,
      "confidenceInterval": {
        "lower": 0.65,
        "upper": 0.87
      },
      "timeframe": {
        "earliestDate": "2024-12-05",
        "mostLikelyDate": "2024-12-15",
        "latestDate": "2024-12-30"
      },
      "attackVector": {
        "primaryTactic": "TA0001 - Initial Access",
        "primaryTechnique": "T1566.001 - Spearphishing Attachment",
        "killChain": [
          "Reconnaissance",
          "Weaponization",
          "Delivery",
          "Exploitation",
          "Installation",
          "Command & Control",
          "Actions on Objectives"
        ]
      },
      "targetProfile": {
        "estimatedTargets": 234,
        "criticalAssets": 45,
        "vulnerableEquipment": [
          {
            "equipmentType": "SCADA HMI",
            "count": 67,
            "criticalityLevel": "CRITICAL"
          }
        ]
      },
      "impactAssessment": {
        "financialImpact": {
          "min": 2500000,
          "max": 15000000,
          "currency": "USD"
        },
        "operationalImpact": {
          "downtimeHours": {
            "min": 24,
            "max": 168
          },
          "affectedCustomers": {
            "min": 50000,
            "max": 500000
          }
        },
        "cascadingEffects": [
          {
            "sector": "WATER",
            "impact": "MEDIUM",
            "description": "Water treatment facilities dependent on power"
          }
        ]
      },
      "contributingFactors": [
        {
          "factor": "geopolitical_tension",
          "weight": 0.35,
          "evidence": "Increased nation-state activity targeting energy sector",
          "eventReferences": ["GEO-2024-11-15-042", "GEO-2024-11-18-067"]
        },
        {
          "factor": "vulnerability_exposure",
          "weight": 0.28,
          "evidence": "Critical CVE-2024-12345 affects 67 SCADA systems",
          "cveReferences": ["CVE-2024-12345"]
        },
        {
          "factor": "historical_patterns",
          "weight": 0.22,
          "evidence": "December traditionally high activity period",
          "patternId": "PATTERN-SEASONAL-001"
        },
        {
          "factor": "threat_intel",
          "weight": 0.15,
          "evidence": "APT29 recent targeting of energy sector",
          "eventReferences": ["EVT-2024-11-22-001"]
        }
      ],
      "mitigationRecommendations": [
        {
          "recommendationId": "REC-001",
          "priority": "CRITICAL",
          "action": "Patch CVE-2024-12345 on all SCADA HMI systems",
          "effectiveness": 0.82,
          "costEstimate": 150000,
          "implementationTime": "7 days"
        },
        {
          "recommendationId": "REC-002",
          "priority": "HIGH",
          "action": "Implement network segmentation for SCADA networks",
          "effectiveness": 0.75,
          "costEstimate": 500000,
          "implementationTime": "30 days"
        }
      ],
      "modelMetadata": {
        "modelVersion": "v3.2.1",
        "trainingDataEnd": "2024-11-20",
        "features": 127,
        "accuracy": 0.84,
        "precision": 0.81,
        "recall": 0.79
      }
    }
  ],
  "metadata": {
    "totalPredictions": 23,
    "highProbability": 8,
    "mediumProbability": 12,
    "lowProbability": 3,
    "generatedAt": "2024-11-22T12:00:00Z"
  }
}
```

#### Get Top 10 High-Probability Threats
```http
GET /api/v1/predictions/top?limit=10&min_probability=0.7

Response:
{
  "topThreats": [
    {
      "rank": 1,
      "predictionId": "PRED-2024-11-22-001",
      "sector": "ENERGY",
      "threatType": "RANSOMWARE_ATTACK",
      "probability": 0.78,
      "estimatedImpact": "CRITICAL",
      "timeToLikelyEvent": "23 days",
      "urgency": "IMMEDIATE",
      "recommendedActions": [
        "Patch CVE-2024-12345",
        "Enhanced monitoring",
        "Incident response readiness"
      ]
    },
    {
      "rank": 2,
      "predictionId": "PRED-2024-11-22-007",
      "sector": "FINANCIAL_SERVICES",
      "threatType": "DATA_BREACH",
      "probability": 0.74,
      "estimatedImpact": "HIGH",
      "timeToLikelyEvent": "31 days",
      "urgency": "HIGH",
      "recommendedActions": [
        "MFA enforcement",
        "Data encryption review",
        "Access control audit"
      ]
    }
  ],
  "summary": {
    "criticalThreats": 3,
    "highThreats": 5,
    "mediumThreats": 2,
    "totalEstimatedImpact": "$45M-$120M",
    "totalMitigationCost": "$2.3M"
  }
}
```

### ROI Scenario Analysis API

#### Get Investment Scenarios
```http
GET /api/v1/scenarios?sector={sector}&budget_range={min}-{max}&timeframe={months}

Query Parameters:
  - sector: target sector for investment (optional)
  - budget_range: investment budget in USD (e.g., 100000-500000)
  - timeframe: ROI calculation period in months (default: 36)
  - risk_tolerance: LOW|MEDIUM|HIGH (default: MEDIUM)

Response:
{
  "scenarios": [
    {
      "scenarioId": "SCENARIO-001",
      "name": "Enhanced Network Segmentation for Energy Sector",
      "targetSector": "ENERGY",
      "investmentRequired": 450000,
      "implementationTime": "6 months",
      "roiMetrics": {
        "expectedROI": 3.8,
        "paybackPeriod": "18 months",
        "npv": 1285000,
        "irr": 0.42,
        "confidenceLevel": 0.82
      },
      "riskReduction": {
        "breachProbabilityBefore": 0.78,
        "breachProbabilityAfter": 0.31,
        "riskReduction": 0.60,
        "preventedIncidents": {
          "expected": 4.2,
          "pessimistic": 2,
          "optimistic": 7
        }
      },
      "costBenefit": {
        "costs": {
          "implementation": 450000,
          "annual_maintenance": 75000,
          "training": 50000,
          "total_3year": 800000
        },
        "benefits": {
          "prevented_breach_costs": 2850000,
          "reduced_downtime": 425000,
          "compliance_benefits": 180000,
          "total_3year": 3455000
        },
        "netBenefit": 2655000
      },
      "implementationPlan": {
        "phases": [
          {
            "phase": 1,
            "name": "Assessment & Design",
            "duration": "1 month",
            "cost": 75000,
            "deliverables": [
              "Network topology analysis",
              "Segmentation architecture design",
              "Risk assessment baseline"
            ]
          },
          {
            "phase": 2,
            "name": "Implementation",
            "duration": "4 months",
            "cost": 300000,
            "deliverables": [
              "Network segmentation deployment",
              "Firewall configuration",
              "VLAN implementation"
            ]
          },
          {
            "phase": 3,
            "name": "Testing & Validation",
            "duration": "1 month",
            "cost": 75000,
            "deliverables": [
              "Penetration testing",
              "Performance validation",
              "Staff training"
            ]
          }
        ]
      },
      "riskFactors": [
        {
          "risk": "Implementation delays",
          "likelihood": 0.35,
          "impact": "MEDIUM",
          "mitigation": "Phased rollout with contingency planning"
        },
        {
          "risk": "Operational disruption",
          "likelihood": 0.22,
          "impact": "LOW",
          "mitigation": "Testing in isolated environment before production"
        }
      ],
      "alignedThreats": [
        "PRED-2024-11-22-001",
        "PRED-2024-11-22-003"
      ],
      "priority": "HIGH",
      "urgency": "IMMEDIATE"
    }
  ],
  "metadata": {
    "totalScenarios": 12,
    "highROI": 5,
    "mediumROI": 5,
    "lowROI": 2,
    "analysisDate": "2024-11-22T12:00:00Z"
  }
}
```

#### Get High-ROI Investment Recommendations
```http
GET /api/v1/scenarios/high-roi?min_roi=2.0&max_budget=1000000&limit=5

Response:
{
  "recommendations": [
    {
      "rank": 1,
      "scenarioId": "SCENARIO-005",
      "name": "Zero Trust Architecture Implementation",
      "roi": 4.5,
      "investment": 750000,
      "netBenefit": 2625000,
      "riskReduction": 0.68,
      "urgency": "HIGH",
      "quickSummary": "Highest ROI with comprehensive risk reduction across multiple threat vectors",
      "keyBenefits": [
        "60%+ reduction in lateral movement attacks",
        "Strong compliance alignment (NIST, ISO 27001)",
        "Scalable architecture for future growth"
      ]
    },
    {
      "rank": 2,
      "scenarioId": "SCENARIO-001",
      "name": "Enhanced Network Segmentation",
      "roi": 3.8,
      "investment": 450000,
      "netBenefit": 2655000,
      "riskReduction": 0.60,
      "urgency": "IMMEDIATE",
      "quickSummary": "Fast implementation with high impact on ransomware prevention",
      "keyBenefits": [
        "Prevents lateral movement",
        "Quick payback period (18 months)",
        "Addresses top predicted threat"
      ]
    }
  ],
  "portfolioAnalysis": {
    "recommendedPortfolio": [
      "SCENARIO-005",
      "SCENARIO-001"
    ],
    "combinedInvestment": 1200000,
    "combinedROI": 4.2,
    "combinedRiskReduction": 0.82,
    "portfolioSynergies": [
      "Zero Trust + Segmentation = defense-in-depth",
      "Shared infrastructure reduces implementation costs by 15%"
    ]
  }
}
```

### McKenney Q7/Q8 Analysis API

#### Query "What Will Happen?" (McKenney Q7)
```http
POST /api/v1/mckenney/q7
Content-Type: application/json
Authorization: Bearer {api_key}

Request Body:
{
  "context": {
    "sector": "ENERGY",
    "timeframe": 90,
    "currentThreats": ["APT29", "Ransomware"],
    "geopoliticalContext": ["US-Russia tensions"],
    "recentEvents": ["EVT-2024-11-22-001"]
  },
  "analysisDepth": "comprehensive",
  "includeAlternativeScenarios": true
}

Response:
{
  "queryId": "Q7-2024-11-22-001",
  "question": "What will happen in the ENERGY sector over the next 90 days?",
  "primaryScenario": {
    "scenarioId": "Q7-SCENARIO-001",
    "name": "Escalating Nation-State Targeting of Energy Infrastructure",
    "probability": 0.72,
    "timeline": {
      "phase1": {
        "timeframe": "Days 1-30",
        "events": [
          "Increased reconnaissance activity targeting SCADA systems",
          "Spearphishing campaigns against energy sector employees",
          "Exploitation of CVE-2024-12345 on vulnerable HMI systems"
        ],
        "probability": 0.85
      },
      "phase2": {
        "timeframe": "Days 31-60",
        "events": [
          "Successful initial access achieved in 20-30% of targeted organizations",
          "Lateral movement and privilege escalation",
          "Deployment of persistence mechanisms"
        ],
        "probability": 0.68
      },
      "phase3": {
        "timeframe": "Days 61-90",
        "events": [
          "Ransomware deployment or data exfiltration",
          "Potential operational disruption",
          "Public disclosure of breach"
        ],
        "probability": 0.62
      }
    },
    "drivingFactors": [
      {
        "factor": "Geopolitical tension",
        "weight": 0.40,
        "trendDirection": "INCREASING",
        "evidence": ["GEO-2024-11-15-042", "GEO-2024-11-18-067"]
      },
      {
        "factor": "Vulnerability landscape",
        "weight": 0.30,
        "trendDirection": "STABLE",
        "evidence": ["CVE-2024-12345 unpatched in 60% of systems"]
      },
      {
        "factor": "Historical patterns",
        "weight": 0.20,
        "trendDirection": "SEASONAL_INCREASE",
        "evidence": ["December typically 40% higher activity"]
      },
      {
        "factor": "Threat actor capability",
        "weight": 0.10,
        "trendDirection": "INCREASING",
        "evidence": ["APT29 tooling evolution"]
      }
    ],
    "expectedImpact": {
      "financialImpact": "$15M-$80M across sector",
      "operationalImpact": "24-168 hours downtime for affected entities",
      "cascadingEffects": [
        "Water treatment disruption",
        "Manufacturing shutdowns",
        "Public safety concerns"
      ],
      "confidenceLevel": 0.78
    }
  },
  "alternativeScenarios": [
    {
      "scenarioId": "Q7-SCENARIO-002",
      "name": "Successful Defensive Measures Prevent Major Incidents",
      "probability": 0.18,
      "description": "Coordinated patching and enhanced monitoring prevent successful attacks",
      "requiredActions": [
        "95%+ patching of CVE-2024-12345",
        "Enhanced threat hunting",
        "Information sharing initiatives"
      ]
    },
    {
      "scenarioId": "Q7-SCENARIO-003",
      "name": "Catastrophic Grid Disruption",
      "probability": 0.10,
      "description": "Coordinated multi-vector attack causes widespread power outage",
      "triggerEvents": [
        "Simultaneous physical and cyber attack",
        "Coordination across multiple threat actors",
        "Exploitation of zero-day vulnerabilities"
      ],
      "impact": "CATASTROPHIC"
    }
  ],
  "uncertainties": [
    {
      "uncertainty": "Geopolitical escalation",
      "impactOnProbability": "±0.20",
      "monitoringIndicators": ["Diplomatic relations", "Military posturing"]
    },
    {
      "uncertainty": "Defensive efficacy",
      "impactOnProbability": "±0.15",
      "monitoringIndicators": ["Patch deployment rates", "Detection capabilities"]
    }
  ],
  "monitoringRecommendations": [
    "Track CVE-2024-12345 exploitation attempts",
    "Monitor geopolitical events via GDELT feed",
    "Analyze spearphishing campaign indicators",
    "Review threat intel for APT29 activity shifts"
  ],
  "modelMetadata": {
    "modelVersion": "McKenney-Q7-v2.1",
    "analysisTimestamp": "2024-11-22T12:00:00Z",
    "dataSourcesUsed": 47,
    "confidenceScore": 0.82
  }
}
```

#### Query "What Should We Do?" (McKenney Q8)
```http
POST /api/v1/mckenney/q8
Content-Type: application/json
Authorization: Bearer {api_key}

Request Body:
{
  "context": {
    "organization": {
      "sector": "ENERGY",
      "size": "LARGE",
      "maturityLevel": "MEDIUM",
      "budget": 1000000,
      "timeframe": "6 months"
    },
    "currentState": {
      "patchingCadence": "quarterly",
      "networkSegmentation": "partial",
      "incidentResponseCapability": "basic",
      "threatIntelCapability": "limited"
    },
    "threats": ["PRED-2024-11-22-001", "PRED-2024-11-22-003"]
  },
  "objectivePriority": ["risk_reduction", "compliance", "operational_efficiency"],
  "constraints": {
    "budgetLimit": 1000000,
    "timeLimit": 180,
    "operationalDisruption": "MINIMAL"
  }
}

Response:
{
  "queryId": "Q8-2024-11-22-001",
  "question": "What should this organization do to address predicted threats?",
  "recommendedStrategy": {
    "strategyId": "Q8-STRATEGY-001",
    "name": "Phased Risk Reduction with Quick Wins",
    "overallApproach": "Prioritize immediate high-impact actions followed by strategic improvements",
    "estimatedRiskReduction": 0.68,
    "estimatedCost": 925000,
    "implementationTime": "5 months",
    "roi": 3.4,
    "urgency": "HIGH"
  },
  "tacticalActions": {
    "immediate": [
      {
        "actionId": "ACTION-001",
        "priority": "CRITICAL",
        "action": "Emergency patching of CVE-2024-12345 on all SCADA HMI systems",
        "timeline": "0-7 days",
        "cost": 50000,
        "riskReduction": 0.35,
        "effort": "HIGH",
        "dependencies": [],
        "mitigatedThreats": ["PRED-2024-11-22-001"],
        "implementation": {
          "steps": [
            "Inventory all SCADA HMI systems",
            "Test patches in isolated environment",
            "Deploy patches during maintenance windows",
            "Validate patch effectiveness"
          ],
          "risks": ["Operational disruption", "Patch incompatibility"],
          "mitigations": ["Staged rollout", "Rollback procedures"]
        }
      },
      {
        "actionId": "ACTION-002",
        "priority": "CRITICAL",
        "action": "Deploy enhanced monitoring for APT29 TTPs",
        "timeline": "0-14 days",
        "cost": 75000,
        "riskReduction": 0.22,
        "effort": "MEDIUM",
        "dependencies": [],
        "mitigatedThreats": ["PRED-2024-11-22-001"],
        "implementation": {
          "steps": [
            "Deploy SIEM rules for APT29 indicators",
            "Configure EDR for T1566.001 detection",
            "Enable enhanced logging on critical systems",
            "Train SOC on APT29 tactics"
          ]
        }
      }
    ],
    "nearTerm": [
      {
        "actionId": "ACTION-003",
        "priority": "HIGH",
        "action": "Implement network segmentation for SCADA networks",
        "timeline": "30-90 days",
        "cost": 300000,
        "riskReduction": 0.28,
        "effort": "HIGH",
        "dependencies": ["ACTION-001"],
        "mitigatedThreats": ["PRED-2024-11-22-001", "PRED-2024-11-22-003"]
      },
      {
        "actionId": "ACTION-004",
        "priority": "HIGH",
        "action": "Establish threat intelligence sharing program",
        "timeline": "14-60 days",
        "cost": 100000,
        "riskReduction": 0.15,
        "effort": "MEDIUM",
        "dependencies": []
      }
    ],
    "strategic": [
      {
        "actionId": "ACTION-005",
        "priority": "MEDIUM",
        "action": "Deploy Zero Trust architecture foundation",
        "timeline": "90-180 days",
        "cost": 400000,
        "riskReduction": 0.42,
        "effort": "VERY_HIGH",
        "dependencies": ["ACTION-003"],
        "longTermBenefit": "Comprehensive security posture improvement"
      }
    ]
  },
  "implementationRoadmap": {
    "phase1": {
      "name": "Emergency Response",
      "duration": "0-30 days",
      "actions": ["ACTION-001", "ACTION-002"],
      "totalCost": 125000,
      "expectedRiskReduction": 0.45,
      "keyMilestones": [
        "CVE-2024-12345 patched on all critical systems",
        "APT29 monitoring operational"
      ]
    },
    "phase2": {
      "name": "Tactical Improvements",
      "duration": "30-90 days",
      "actions": ["ACTION-003", "ACTION-004"],
      "totalCost": 400000,
      "expectedRiskReduction": 0.35,
      "keyMilestones": [
        "SCADA network segmentation complete",
        "Threat intel sharing active"
      ]
    },
    "phase3": {
      "name": "Strategic Transformation",
      "duration": "90-180 days",
      "actions": ["ACTION-005"],
      "totalCost": 400000,
      "expectedRiskReduction": 0.42,
      "keyMilestones": [
        "Zero Trust pilot deployed",
        "Long-term architecture roadmap"
      ]
    }
  },
  "alternativeStrategies": [
    {
      "strategyId": "Q8-STRATEGY-002",
      "name": "Budget-Constrained Approach",
      "cost": 500000,
      "riskReduction": 0.52,
      "tradeoffs": "Lower overall risk reduction but faster payback"
    },
    {
      "strategyId": "Q8-STRATEGY-003",
      "name": "Comprehensive Transformation",
      "cost": 1500000,
      "riskReduction": 0.85,
      "tradeoffs": "Exceeds budget but maximizes protection"
    }
  ],
  "successMetrics": [
    {
      "metric": "Vulnerability remediation rate",
      "target": "95% of critical CVEs patched within 7 days",
      "measurement": "Weekly vulnerability scans"
    },
    {
      "metric": "Mean time to detect (MTTD)",
      "target": "Reduce from 200 days to 30 days",
      "measurement": "SIEM analytics"
    },
    {
      "metric": "Breach probability reduction",
      "target": "78% to 31% within 6 months",
      "measurement": "Risk assessment updates"
    }
  ],
  "ongoingActions": [
    "Monthly threat landscape review",
    "Quarterly risk assessment updates",
    "Continuous vulnerability management",
    "Regular incident response exercises"
  ],
  "modelMetadata": {
    "modelVersion": "McKenney-Q8-v2.1",
    "analysisTimestamp": "2024-11-22T12:00:00Z",
    "optimizationAlgorithm": "Multi-objective optimization (risk, cost, time)",
    "confidenceScore": 0.84
  }
}
```

### Historical Pattern Analysis API

#### Get Attack Pattern Trends
```http
GET /api/v1/patterns?pattern_type={type}&sector={sector}&lookback_days={n}

Query Parameters:
  - pattern_type: seasonal|threat_actor|technique|vulnerability
  - sector: target sector (optional)
  - lookback_days: historical analysis period (default: 365)

Response:
{
  "patterns": [
    {
      "patternId": "PATTERN-SEASONAL-001",
      "patternType": "seasonal",
      "name": "December Energy Sector Attack Surge",
      "description": "40% increase in attacks during December holiday period",
      "sector": "ENERGY",
      "historicalOccurrences": 7,
      "yearsObserved": [2017, 2018, 2019, 2020, 2021, 2022, 2023],
      "averageIncrease": 0.42,
      "confidence": 0.89,
      "contributingFactors": [
        "Reduced staffing during holidays",
        "Delayed patching schedules",
        "Increased geopolitical activity end-of-year"
      ],
      "peakPeriod": {
        "start": "December 15",
        "end": "January 5"
      },
      "recommendations": [
        "Enhanced monitoring during holiday periods",
        "Accelerated patching before December 10",
        "Increased SOC staffing December 15 - January 5"
      ]
    },
    {
      "patternId": "PATTERN-TTP-002",
      "patternType": "technique",
      "name": "Spearphishing as Primary Initial Access",
      "description": "T1566.001 used in 68% of successful energy sector breaches",
      "mitreId": "T1566.001",
      "sector": "ENERGY",
      "prevalence": 0.68,
      "successRate": 0.34,
      "historicalInstances": 234,
      "trendDirection": "INCREASING",
      "relatedPatterns": ["PATTERN-TTP-003", "PATTERN-TTP-007"],
      "defenseRecommendations": [
        "Email security gateway with AI detection",
        "User awareness training",
        "Email authentication (DMARC, SPF, DKIM)"
      ]
    }
  ],
  "metadata": {
    "totalPatterns": 47,
    "analysisDate": "2024-11-22T12:00:00Z",
    "dataQuality": 0.91
  }
}
```

---

## 🔐 Authentication & Authorization

### API Key Management
```http
POST /api/v1/auth/keys
Content-Type: application/json
Authorization: Bearer {admin_token}

Request:
{
  "name": "Production API Key",
  "permissions": ["read:events", "read:predictions", "write:events"],
  "rateLimit": "enterprise",
  "expiresIn": "365d"
}

Response:
{
  "apiKey": "aeon_prod_abc123xyz...",
  "keyId": "KEY-12345",
  "permissions": ["read:events", "read:predictions", "write:events"],
  "rateLimit": "10000 requests/hour",
  "expiresAt": "2025-11-22T12:00:00Z"
}
```

### Permission Scopes
```yaml
Level 5 Permissions:
  - read:events - Read information events
  - write:events - Create new events
  - read:biases - Access bias analysis
  - read:feeds - View threat feeds
  - admin:pipeline - Manage pipeline configuration

Level 6 Permissions:
  - read:predictions - Access breach forecasts
  - read:scenarios - View ROI scenarios
  - write:scenarios - Create custom scenarios
  - read:mckenney - Access Q7/Q8 analysis
  - admin:models - Manage prediction models
```

---

## ⚡ Advanced Rate Limiting

### Tier-Based Limits
```yaml
Level 5/6 API Rate Limits:
  Free Tier:
    requests_per_hour: 100
    burst_capacity: 20
    max_events_per_request: 50

  Professional Tier:
    requests_per_hour: 1000
    burst_capacity: 100
    max_events_per_request: 500

  Enterprise Tier:
    requests_per_hour: 10000
    burst_capacity: 500
    max_events_per_request: 5000
    concurrent_requests: 50
```

### Rate Limit Headers (Extended)
```http
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9847
X-RateLimit-Reset: 1700643600
X-RateLimit-Tier: enterprise
X-RateLimit-Burst-Capacity: 500
X-RateLimit-Burst-Remaining: 487
```

---

## 📊 GraphQL Extensions for Level 5/6

### Extended Schema
```graphql
type Query {
  # Existing queries...

  # Level 5 Queries
  events(filter: EventFilter, limit: Int, offset: Int): EventConnection!
  event(eventId: String!): Event
  geopoliticalEvents(countries: [String!], conflictLevel: ConflictLevel): [GeopoliticalEvent!]!
  biases: [CognitiveBias!]!
  biasActivation(biasId: String!, eventId: String!): BiasActivation
  threatFeeds: [ThreatFeed!]!
  pipelineStatus: PipelineStatus!

  # Level 6 Queries
  predictions(filter: PredictionFilter): [BreachPrediction!]!
  topThreats(limit: Int, minProbability: Float): [ThreatSummary!]!
  scenarios(filter: ScenarioFilter): [ROIScenario!]!
  highROIScenarios(minROI: Float, maxBudget: Float): [ROIScenario!]!
  mckenneyQ7(context: Q7Context!): Q7Analysis!
  mckenneyQ8(context: Q8Context!): Q8Recommendations!
  attackPatterns(patternType: PatternType, sector: String): [AttackPattern!]!
}

type Event {
  eventId: String!
  eventType: EventType!
  timestamp: DateTime!
  source: String!
  confidence: Float!
  severity: Severity!
  title: String!
  description: String!
  sectors: [String!]!
  biasIndicators: [BiasIndicator!]!
  impactAssessment: ImpactAssessment
  linkedEquipment: [Equipment!]!
}

type BreachPrediction {
  predictionId: String!
  targetSector: String!
  predictedEventType: String!
  probability: Float!
  timeframe: PredictionTimeframe!
  attackVector: AttackVector!
  impactAssessment: PredictionImpact!
  mitigationRecommendations: [Recommendation!]!
}

type ROIScenario {
  scenarioId: String!
  name: String!
  investmentRequired: Float!
  roiMetrics: ROIMetrics!
  riskReduction: RiskReductionMetrics!
  implementationPlan: ImplementationPlan!
}
```

### Example Complex Query
```graphql
query ComprehensiveAnalysis($sector: String!, $days: Int!) {
  # Get recent events
  events(filter: { sector: $sector, days: $days }) {
    edges {
      node {
        eventId
        title
        severity
        biasIndicators {
          biasType
          likelihood
        }
      }
    }
  }

  # Get predictions
  predictions(filter: { sector: $sector, timeframe: $days }) {
    predictionId
    probability
    targetSubsector
    mitigationRecommendations {
      action
      effectiveness
      costEstimate
    }
  }

  # Get high-ROI scenarios
  highROIScenarios(minROI: 2.0, maxBudget: 1000000) {
    scenarioId
    name
    roi
    riskReduction {
      breachProbabilityBefore
      breachProbabilityAfter
    }
  }

  # Get pipeline status
  pipelineStatus {
    pipelineStatus
    components {
      ingestion {
        status
        throughput
      }
      biasDetection {
        accuracy
      }
    }
  }
}
```

---

**Wiki Navigation**: [Main](00_MAIN_INDEX.md) | [Queries](QUERIES_LIBRARY.md) | [Maintenance](MAINTENANCE_GUIDE.md) | [Architecture](ARCHITECTURE_OVERVIEW.md)