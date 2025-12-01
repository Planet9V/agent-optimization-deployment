# Events API Documentation

**File:** API_EVENTS.md
**Version:** 1.0.0
**Last Updated:** 2025-11-25
**Status:** COMPLETE

## Overview

The Events API provides comprehensive access to information events, geopolitical events, cognitive biases, threat feeds, and system pipeline status. This API enables real-time situational awareness and cognitive bias detection through structured event streaming and analysis pipelines.

## Table of Contents

1. [Core Event Endpoints](#core-event-endpoints)
2. [Geopolitical Events](#geopolitical-events)
3. [Cognitive Biases](#cognitive-biases)
4. [Threat Feeds](#threat-feeds)
5. [Pipeline Status](#pipeline-status)
6. [Request/Response Schemas](#requestresponse-schemas)
7. [Frontend Integration](#frontend-integration)
8. [Business Value](#business-value)
9. [Error Handling](#error-handling)
10. [Rate Limiting](#rate-limiting)

---

## Core Event Endpoints

### GET /api/v1/events

List all information events with optional filtering, pagination, and sorting.

**HTTP Method:** GET

**URL:** `GET /api/v1/events`

**Description:**
Retrieves a paginated list of information events. Supports filtering by event type, date range, severity, source, and custom metadata. Events can be sorted by date, severity, or relevance score.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number for pagination |
| `limit` | integer | No | 50 | Events per page (max: 500) |
| `type` | string | No | - | Event type: `breaking_news`, `market_data`, `policy_change`, `social_movement`, `security_incident` |
| `severity` | string | No | - | Event severity: `low`, `medium`, `high`, `critical` |
| `source` | string | No | - | Data source identifier (e.g., `reuters`, `bbc`, `bloomberg`) |
| `startDate` | ISO 8601 | No | - | Filter events from this date (e.g., `2025-11-20T00:00:00Z`) |
| `endDate` | ISO 8601 | No | - | Filter events until this date (e.g., `2025-11-25T23:59:59Z`) |
| `regions` | string[] | No | - | Geographic regions (e.g., `North America`, `Europe`, `Asia-Pacific`) |
| `searchQuery` | string | No | - | Full-text search in event titles and descriptions |
| `biasFilter` | string | No | - | Filter by detected cognitive bias: `confirmation_bias`, `availability_heuristic`, `anchoring`, `groupthink` |
| `sortBy` | string | No | `date_desc` | Sort order: `date_asc`, `date_desc`, `severity_desc`, `relevance_desc` |

**Request Example:**

```bash
curl -X GET "https://api.example.com/api/v1/events?page=1&limit=20&severity=high&type=security_incident&startDate=2025-11-20T00:00:00Z" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "events": [
      {
        "id": "evt_20251125_001",
        "title": "Critical Supply Chain Disruption Reported",
        "description": "Major semiconductor manufacturer announces unexpected facility closure affecting global supply chains.",
        "type": "security_incident",
        "severity": "critical",
        "source": "reuters",
        "timestamp": "2025-11-25T14:30:00Z",
        "regions": ["Asia-Pacific", "North America", "Europe"],
        "detectedBiases": [
          {
            "type": "availability_heuristic",
            "confidence": 0.87,
            "description": "Media overemphasis on recent similar incidents"
          },
          {
            "type": "confirmation_bias",
            "confidence": 0.72,
            "description": "Selective reporting focusing on negative impacts"
          }
        ],
        "impactScore": 8.5,
        "relevanceScore": 0.92,
        "tags": ["supply_chain", "semiconductors", "geopolitical_risk"],
        "sourceUrl": "https://example-news.com/article/12345",
        "relatedEventIds": ["evt_20251124_089", "evt_20251123_045"]
      },
      {
        "id": "evt_20251125_002",
        "title": "Central Bank Interest Rate Decision Announced",
        "description": "Federal Reserve maintains interest rates amid inflation concerns.",
        "type": "market_data",
        "severity": "high",
        "source": "bloomberg",
        "timestamp": "2025-11-25T13:00:00Z",
        "regions": ["North America"],
        "detectedBiases": [
          {
            "type": "anchoring",
            "confidence": 0.65,
            "description": "Market focus on previous rate levels"
          }
        ],
        "impactScore": 7.8,
        "relevanceScore": 0.88,
        "tags": ["financial_markets", "monetary_policy"],
        "sourceUrl": "https://example-news.com/article/12346",
        "relatedEventIds": []
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 2847,
      "totalPages": 143,
      "hasNextPage": true,
      "hasPreviousPage": false
    },
    "filters": {
      "severity": "high",
      "type": "security_incident",
      "startDate": "2025-11-20T00:00:00Z"
    }
  },
  "meta": {
    "requestId": "req_20251125_5f3a8b2c",
    "timestamp": "2025-11-25T14:35:22Z",
    "processingTimeMs": 245
  }
}
```

**Error Response (400 Bad Request):**

```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILTER",
    "message": "Invalid date format. Use ISO 8601 format (e.g., 2025-11-25T00:00:00Z)",
    "details": {
      "parameter": "startDate",
      "value": "11/20/2025"
    }
  },
  "meta": {
    "requestId": "req_20251125_5f3a8b2c",
    "timestamp": "2025-11-25T14:35:22Z"
  }
}
```

---

### GET /api/v1/events/{id}

Retrieve detailed information about a specific event.

**HTTP Method:** GET

**URL:** `GET /api/v1/events/{id}`

**Description:**
Returns comprehensive details for a single event including full descriptions, all detected cognitive biases, impact analysis, source information, and related events.

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Event unique identifier (e.g., `evt_20251125_001`) |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `includeRelated` | boolean | No | true | Include related event references |
| `includeBiasAnalysis` | boolean | No | true | Include detailed bias analysis |
| `includeTimeline` | boolean | No | false | Include event development timeline |

**Request Example:**

```bash
curl -X GET "https://api.example.com/api/v1/events/evt_20251125_001?includeRelated=true&includeBiasAnalysis=true" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "event": {
      "id": "evt_20251125_001",
      "title": "Critical Supply Chain Disruption Reported",
      "shortDescription": "Major semiconductor manufacturer announces unexpected facility closure.",
      "fullDescription": "A leading semiconductor manufacturer has announced an unexpected closure of its primary manufacturing facility in East Asia, affecting supply chains globally. The facility, which produces 35% of specific semiconductor types, is expected to remain closed for 6-12 months. This development impacts automotive, consumer electronics, and defense industries.",
      "type": "security_incident",
      "subType": "supply_chain_disruption",
      "severity": "critical",
      "status": "developing",
      "source": {
        "id": "reuters",
        "name": "Reuters",
        "credibilityScore": 0.95,
        "category": "major_news_agency"
      },
      "timestamp": "2025-11-25T14:30:00Z",
      "lastUpdated": "2025-11-25T14:50:00Z",
      "regions": [
        {
          "name": "Asia-Pacific",
          "country": "Taiwan",
          "affectedPopulation": "millions",
          "impactLevel": "critical"
        },
        {
          "name": "North America",
          "country": "USA",
          "affectedPopulation": "millions",
          "impactLevel": "high"
        },
        {
          "name": "Europe",
          "country": "Multiple",
          "affectedPopulation": "millions",
          "impactLevel": "high"
        }
      ],
      "detectedBiases": [
        {
          "id": "bias_20251125_001_a",
          "type": "availability_heuristic",
          "name": "Availability Heuristic",
          "confidence": 0.87,
          "description": "Media overemphasis on recent similar supply chain incidents creates perception of higher frequency",
          "affectedAreas": ["risk_assessment", "investment_decisions"],
          "mitigationSuggestions": [
            "Compare current incident frequency with historical baselines",
            "Analyze long-term supply chain resilience trends",
            "Consider statistical likelihood vs. media coverage"
          ],
          "examples": [
            "Investors overestimating semiconductor shortage risk",
            "Analysts citing previous 2021 shortage as primary anchor"
          ]
        },
        {
          "id": "bias_20251125_001_b",
          "type": "confirmation_bias",
          "name": "Confirmation Bias",
          "confidence": 0.72,
          "description": "Selective reporting emphasizing supply chain vulnerabilities while downplaying mitigation strategies",
          "affectedAreas": ["risk_perception", "policy_decisions"],
          "mitigationSuggestions": [
            "Seek multiple viewpoints from different analysts",
            "Review alternative supply chain strategies",
            "Examine manufacturer mitigation plans"
          ],
          "examples": [
            "Media focusing on disruption costs, less on alternative suppliers",
            "Reports emphasizing worst-case scenarios"
          ]
        }
      ],
      "impactAnalysis": {
        "financialImpact": {
          "estimatedLoss": "$50-100 billion",
          "affectedIndustries": ["automotive", "consumer_electronics", "defense"],
          "confidence": 0.78
        },
        "operationalImpact": {
          "supplyChainDisruption": "6-12 months",
          "affectedCompanies": "5000+",
          "confidence": 0.85
        },
        "geopoliticalImpact": {
          "strategicConcern": "Critical",
          "relatedToTension": true,
          "threatLevel": "high",
          "confidence": 0.81
        }
      },
      "impactScore": 8.5,
      "relevanceScore": 0.92,
      "tags": ["supply_chain", "semiconductors", "geopolitical_risk", "manufacturing"],
      "sourceUrl": "https://example-news.com/article/12345",
      "relatedEvents": [
        {
          "id": "evt_20251124_089",
          "title": "Previous Semiconductor Shortage Warnings",
          "relationship": "historical_precedent"
        },
        {
          "id": "evt_20251123_045",
          "title": "Geopolitical Tensions in East Asia",
          "relationship": "contextual_background"
        }
      ],
      "timeline": [
        {
          "timestamp": "2025-11-25T08:00:00Z",
          "event": "Initial company announcement",
          "source": "official_statement"
        },
        {
          "timestamp": "2025-11-25T12:30:00Z",
          "event": "Major news outlets begin coverage",
          "source": "media_coverage"
        },
        {
          "timestamp": "2025-11-25T14:30:00Z",
          "event": "Market reaction observed",
          "source": "financial_data"
        }
      ]
    }
  },
  "meta": {
    "requestId": "req_20251125_5f3a8b2d",
    "timestamp": "2025-11-25T14:40:00Z",
    "processingTimeMs": 89
  }
}
```

---

## Geopolitical Events

### GET /api/v1/events/geopolitical

Retrieve geopolitical-specific events with enhanced analysis.

**HTTP Method:** GET

**URL:** `GET /api/v1/events/geopolitical`

**Description:**
Returns information events specifically categorized as geopolitical in nature, with enriched analysis including diplomatic implications, sanctions impact, territorial concerns, and regional stability assessments.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number for pagination |
| `limit` | integer | No | 50 | Events per page |
| `category` | string | No | - | `territorial_disputes`, `sanctions`, `diplomatic_tensions`, `military_buildup`, `trade_war` |
| `threatLevel` | string | No | - | `low`, `medium`, `high`, `critical` |
| `regions` | string[] | No | - | Geographic regions affected |
| `stakeholders` | string[] | No | - | Country or entity names (e.g., `China`, `Russia`, `USA`) |
| `timeframe` | string | No | `30d` | Time range: `7d`, `14d`, `30d`, `90d`, `1y` |

**Request Example:**

```bash
curl -X GET "https://api.example.com/api/v1/events/geopolitical?threatLevel=high&timeframe=30d&stakeholders=China,Taiwan" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "geopoliticalEvents": [
      {
        "id": "geo_20251125_001",
        "title": "Naval Exercises in Taiwan Strait Announced",
        "description": "Military forces announce combined exercise operations in strategically sensitive region.",
        "category": "military_buildup",
        "threatLevel": "high",
        "timestamp": "2025-11-25T10:00:00Z",
        "primaryStakeholders": ["China", "Taiwan", "USA"],
        "secondaryStakeholders": ["Japan", "South Korea"],
        "regions": ["Asia-Pacific", "South China Sea"],
        "diplomaticImplications": {
          "level": "high",
          "description": "Exercise could be perceived as provocative, potentially escalating tensions",
          "historicalContext": "Pattern of increasing military presence in region over 5 years"
        },
        "economicImpact": {
          "tradeRoutesAffected": true,
          "estimatedValue": "$2 trillion annual trade",
          "disruptionRisk": 0.65
        },
        "stabilityAssessment": {
          "regionalStability": "concerning",
          "escalationRisk": 0.72,
          "recommendedMonitoring": ["diplomatic_statements", "military_deployments", "economic_indicators"]
        },
        "cognitiveRisks": [
          {
            "bias": "groupthink",
            "description": "Media narrative formation within like-minded analyst groups",
            "riskLevel": "medium"
          },
          {
            "bias": "confirmation_bias",
            "description": "Selective interpretation of military exercises as hostile vs. defensive",
            "riskLevel": "high"
          }
        ],
        "recommendedActions": [
          "Monitor diplomatic channels for de-escalation statements",
          "Track economic indicators for supply chain concerns",
          "Analyze multiple news sources for balanced perspective"
        ]
      }
    ],
    "summary": {
      "totalHighThreatEvents": 12,
      "totalCriticalThreatEvents": 3,
      "mostAffectedRegions": ["Asia-Pacific", "Eastern Europe", "Middle East"],
      "primaryConcerns": ["territorial_disputes", "military_buildup", "sanctions_escalation"]
    }
  }
}
```

---

## Cognitive Biases

### GET /api/v1/biases

List all detectable cognitive biases with metadata.

**HTTP Method:** GET

**URL:** `GET /api/v1/biases`

**Description:**
Returns comprehensive catalog of cognitive biases that the system detects in event reporting and analysis. Each bias includes detection criteria, common contexts, and mitigation strategies.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number |
| `limit` | integer | No | 50 | Biases per page |
| `category` | string | No | - | `perception`, `decision_making`, `memory`, `social` |
| `detectionFrequency` | string | No | - | `very_common`, `common`, `occasional`, `rare` |

**Request Example:**

```bash
curl -X GET "https://api.example.com/api/v1/biases?category=decision_making&detectionFrequency=very_common" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "biases": [
      {
        "id": "bias_availability_heuristic",
        "name": "Availability Heuristic",
        "category": "perception",
        "shortDescription": "Tendency to overestimate importance of readily available information",
        "fullDescription": "People tend to estimate probability and frequency based on how easily examples come to mind. Recent or widely-publicized events are overweighted in decision-making.",
        "detectionFrequency": "very_common",
        "commonContexts": [
          "Risk assessment after recent media coverage",
          "Investment decisions following market volatility",
          "Threat evaluations during crisis periods"
        ],
        "detectionCriteria": [
          "Recent similar events mentioned repeatedly",
          "Emotional language emphasizing recent incidents",
          "Lack of historical statistical comparison"
        ],
        "mitigationStrategies": [
          "Compare current situation to historical baselines",
          "Seek statistical evidence over anecdotal examples",
          "Analyze long-term trends, not just recent events"
        ],
        "affectedDecisions": ["risk_management", "investment", "policy_making"],
        "exampleScenarios": [
          "After stock market crash, investors overestimate future volatility",
          "Following terrorist attack, risk perception increases disproportionately",
          "Supply chain disruptions trigger overestimation of industry risk"
        ]
      },
      {
        "id": "bias_confirmation_bias",
        "name": "Confirmation Bias",
        "category": "decision_making",
        "shortDescription": "Tendency to search for, interpret, and remember information consistent with existing beliefs",
        "fullDescription": "People actively seek and favor information that confirms their existing viewpoints while ignoring contradictory evidence. This leads to polarized perspectives and poor decision-making.",
        "detectionFrequency": "very_common",
        "commonContexts": [
          "Political or ideological reporting",
          "Industry analysis with vested interests",
          "Competitive intelligence with bias toward existing competitors"
        ],
        "detectionCriteria": [
          "Selective sourcing favoring particular viewpoints",
          "Dismissal or minimal coverage of contradictory evidence",
          "Repetitive citing of same sources with similar bias"
        ],
        "mitigationStrategies": [
          "Actively seek opposing viewpoints",
          "Assign roles: 'Red team' to challenge main analysis",
          "Set quotas for including dissenting evidence"
        ],
        "affectedDecisions": ["strategy", "risk_assessment", "investments"],
        "exampleScenarios": [
          "Analyst consistently recommending single competitor despite alternatives",
          "Policy makers focusing only on supporting studies",
          "Investors seeking validation for already-made decisions"
        ]
      },
      {
        "id": "bias_anchoring",
        "name": "Anchoring Bias",
        "category": "decision_making",
        "shortDescription": "Over-reliance on initial information (anchor) for subsequent judgments",
        "fullDescription": "People rely heavily on the first piece of information received (anchor) even when it's irrelevant, using it as reference point for all subsequent decisions.",
        "detectionFrequency": "very_common",
        "commonContexts": [
          "Price negotiations using initial offer",
          "Market analysis anchored to previous price levels",
          "Risk assessment anchored to historical events"
        ],
        "detectionCriteria": [
          "Frequent reference to initial values or prices",
          "Limited adjustment from starting reference point",
          "Justifications dependent on initial anchor"
        ],
        "mitigationStrategies": [
          "Consider multiple starting reference points",
          "Make anchoring explicit and challenge it",
          "Use statistical measures independent of anchors"
        ],
        "affectedDecisions": ["valuation", "negotiation", "forecasting"],
        "exampleScenarios": [
          "Stock price anchored to previous high, affecting valuation",
          "Interest rate anchored to previous levels despite new data",
          "Supply contract priced relative to outdated baseline"
        ]
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 50,
      "total": 24,
      "totalPages": 1
    }
  }
}
```

---

### GET /api/v1/biases/{id}/activation

Retrieve current activation status and frequency of a specific cognitive bias.

**HTTP Method:** GET

**URL:** `GET /api/v1/biases/{id}/activation`

**Description:**
Returns current detection frequency and activation patterns for a specific bias. Shows trends, affected industries, and recent occurrences in analyzed events.

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Bias identifier (e.g., `bias_confirmation_bias`) |

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `timeframe` | string | No | `7d` | Analysis period: `24h`, `7d`, `30d`, `90d` |
| `industries` | string[] | No | - | Filter by specific industries |
| `regions` | string[] | No | - | Filter by geographic regions |

**Request Example:**

```bash
curl -X GET "https://api.example.com/api/v1/biases/bias_confirmation_bias/activation?timeframe=30d&industries=technology,finance" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "bias": {
      "id": "bias_confirmation_bias",
      "name": "Confirmation Bias"
    },
    "activationStatus": {
      "currentActivationLevel": "high",
      "detectionFrequency": 0.78,
      "eventsAffected": 2143,
      "timeframe": "30d"
    },
    "trends": {
      "activationTrend": "increasing",
      "percentageChange": "+12%",
      "peakDetectionTime": "2025-11-20 to 2025-11-25",
      "lowestDetectionTime": "2025-11-01 to 2025-11-10"
    },
    "industryBreakdown": {
      "technology": {
        "occurrences": 287,
        "percentage": 33.2,
        "topContexts": ["competitive_analysis", "product_evaluation"]
      },
      "finance": {
        "occurrences": 156,
        "percentage": 18.1,
        "topContexts": ["investment_decisions", "market_analysis"]
      },
      "policy": {
        "occurrences": 234,
        "percentage": 27.1,
        "topContexts": ["regulation_analysis", "trade_policy"]
      },
      "geopolitics": {
        "occurrences": 145,
        "percentage": 16.8,
        "topContexts": ["diplomatic_relations", "threat_assessment"]
      }
    },
    "recentOccurrences": [
      {
        "eventId": "evt_20251125_001",
        "eventTitle": "Critical Supply Chain Disruption",
        "detectionConfidence": 0.72,
        "affectedContext": "Risk reporting emphasizing negative impacts",
        "timestamp": "2025-11-25T14:30:00Z"
      },
      {
        "eventId": "evt_20251124_089",
        "eventTitle": "Market Analysis Report",
        "detectionConfidence": 0.68,
        "affectedContext": "Selective sourcing from aligned analysts",
        "timestamp": "2025-11-24T16:45:00Z"
      }
    ],
    "mitigationRecommendations": [
      "Increase diversity in source selection",
      "Implement systematic review of contradictory evidence",
      "Use structured decision frameworks to reduce bias"
    ]
  }
}
```

---

## Threat Feeds

### GET /api/v1/threat-feeds

Retrieve status and summary of all active threat intelligence feeds.

**HTTP Method:** GET

**URL:** `GET /api/v1/threat-feeds`

**Description:**
Returns operational status of all threat intelligence data feeds, including processing statistics, coverage areas, and data quality metrics.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | - | Filter by feed status: `active`, `degraded`, `offline`, `all` |
| `threatType` | string | No | - | Type of threats: `cyber`, `physical`, `geopolitical`, `economic`, `health` |
| `coverage` | string | No | - | Geographic coverage: specific regions or countries |

**Request Example:**

```bash
curl -X GET "https://api.example.com/api/v1/threat-feeds?status=active&threatType=geopolitical" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "threatFeeds": [
      {
        "feedId": "feed_geopolitical_primary",
        "feedName": "Primary Geopolitical Intelligence Feed",
        "threatType": "geopolitical",
        "status": "active",
        "statusDetails": {
          "health": "healthy",
          "lastUpdate": "2025-11-25T14:50:00Z",
          "updateFrequency": "real-time",
          "uptime": 0.9997
        },
        "coverage": {
          "regions": ["All"],
          "countries": 195,
          "dataPoints": 8234,
          "lastWeekDataPoints": 2109
        },
        "dataQuality": {
          "accuracy": 0.96,
          "timeliness": 0.94,
          "completeness": 0.92,
          "reliability": 0.95
        },
        "recentIncidents": {
          "count": 47,
          "critical": 3,
          "high": 12,
          "medium": 22,
          "low": 10
        },
        "processingStats": {
          "eventsProcessed": 4128,
          "eventsAnalyzed": 3956,
          "averageProcessingTime": "2.3s",
          "peakLoadTime": "2025-11-25T14:30:00Z"
        }
      },
      {
        "feedId": "feed_cyber_threat",
        "feedName": "Cyber Threat Intelligence Feed",
        "threatType": "cyber",
        "status": "active",
        "statusDetails": {
          "health": "healthy",
          "lastUpdate": "2025-11-25T14:55:00Z",
          "updateFrequency": "real-time",
          "uptime": 0.9994
        },
        "coverage": {
          "regions": ["North America", "Europe", "Asia-Pacific"],
          "countries": 67,
          "dataPoints": 12547,
          "lastWeekDataPoints": 3421
        },
        "dataQuality": {
          "accuracy": 0.94,
          "timeliness": 0.96,
          "completeness": 0.89,
          "reliability": 0.93
        },
        "recentIncidents": {
          "count": 156,
          "critical": 8,
          "high": 34,
          "medium": 78,
          "low": 36
        },
        "processingStats": {
          "eventsProcessed": 6234,
          "eventsAnalyzed": 5987,
          "averageProcessingTime": "1.8s",
          "peakLoadTime": "2025-11-25T12:45:00Z"
        }
      },
      {
        "feedId": "feed_economic_indicators",
        "feedName": "Economic Indicators Feed",
        "threatType": "economic",
        "status": "degraded",
        "statusDetails": {
          "health": "degraded",
          "lastUpdate": "2025-11-25T14:30:00Z",
          "updateFrequency": "hourly",
          "uptime": 0.8821,
          "issue": "Delayed data ingestion from two sources"
        },
        "coverage": {
          "regions": ["Global"],
          "countries": 195,
          "dataPoints": 3421,
          "lastWeekDataPoints": 892
        },
        "dataQuality": {
          "accuracy": 0.91,
          "timeliness": 0.72,
          "completeness": 0.85,
          "reliability": 0.88
        },
        "recentIncidents": {
          "count": 23,
          "critical": 1,
          "high": 4,
          "medium": 10,
          "low": 8
        },
        "processingStats": {
          "eventsProcessed": 892,
          "eventsAnalyzed": 834,
          "averageProcessingTime": "4.2s",
          "peakLoadTime": "2025-11-25T14:00:00Z"
        }
      }
    ],
    "summary": {
      "totalFeeds": 12,
      "activeFeeds": 11,
      "degradedFeeds": 1,
      "offlineFeeds": 0,
      "systemHealth": "excellent",
      "dataProcessingCapacity": "87%",
      "lastSystemCheck": "2025-11-25T15:00:00Z"
    }
  }
}
```

---

## Pipeline Status

### GET /api/v1/pipeline/status

Retrieve comprehensive status of event processing pipeline.

**HTTP Method:** GET

**URL:** `GET /api/v1/pipeline/status`

**Description:**
Returns detailed health metrics for the entire events processing pipeline, including ingestion, enrichment, analysis, and distribution stages. Includes performance metrics and any active issues.

**Request Example:**

```bash
curl -X GET "https://api.example.com/api/v1/pipeline/status" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "pipeline": {
      "status": "operational",
      "overallHealth": "excellent",
      "lastCheck": "2025-11-25T15:05:00Z",
      "stages": [
        {
          "stageName": "Ingestion",
          "status": "operational",
          "health": "excellent",
          "performance": {
            "eventsPerSecond": 324,
            "averageLatency": "0.23s",
            "errorRate": 0.0001,
            "capacityUtilization": 0.62
          },
          "components": {
            "dataCollectors": 24,
            "activeConnections": 19,
            "failedConnections": 0,
            "bufferHealth": "normal"
          },
          "recentErrors": []
        },
        {
          "stageName": "Enrichment",
          "status": "operational",
          "health": "excellent",
          "performance": {
            "eventsProcessed": 2847,
            "averageProcessingTime": "1.8s",
            "errorRate": 0.0003,
            "capacityUtilization": 0.71
          },
          "components": {
            "geoEnrichment": "active",
            "entityExtraction": "active",
            "relationshipMapping": "active",
            "biasDetection": "active"
          },
          "recentErrors": []
        },
        {
          "stageName": "Analysis",
          "status": "operational",
          "health": "good",
          "performance": {
            "eventsAnalyzed": 2634,
            "averageAnalysisTime": "4.2s",
            "errorRate": 0.0008,
            "capacityUtilization": 0.78
          },
          "components": {
            "impactCalculation": "active",
            "relevanceScoring": "active",
            "timelineGeneration": "active",
            "relationshipDiscovery": "active"
          },
          "recentErrors": [
            {
              "component": "timelineGeneration",
              "errorRate": 0.0008,
              "message": "Occasional timeout in complex timeline processing"
            }
          ]
        },
        {
          "stageName": "Distribution",
          "status": "operational",
          "health": "excellent",
          "performance": {
            "deliveries": 15234,
            "averageDeliveryTime": "0.34s",
            "failureRate": 0.0002,
            "capacityUtilization": 0.45
          },
          "components": {
            "apiEndpoints": 6,
            "webhooks": 89,
            "subscribers": 234,
            "queues": "healthy"
          },
          "recentErrors": []
        }
      ]
    },
    "performance": {
      "endToEndLatency": "6.57s",
      "throughput": {
        "eventsPerSecond": 324,
        "eventsPerHour": 1166400,
        "estimatedDailyVolume": 27993600
      },
      "reliability": {
        "successRate": 0.9991,
        "averageDowntime": 0,
        "maintenanceWindows": {
          "scheduled": 0,
          "upcoming": 1
        }
      }
    },
    "resources": {
      "cpuUtilization": 0.68,
      "memoryUtilization": 0.74,
      "databaseConnections": 342,
      "cacheHitRate": 0.87,
      "diskSpace": {
        "used": "847 GB",
        "available": "2.1 TB",
        "utilizationPercent": 0.29
      }
    },
    "recentIssues": [],
    "upcomingMaintenance": [
      {
        "window": "2025-11-26T02:00:00Z to 2025-11-26T03:00:00Z",
        "duration": "1 hour",
        "expectedDowntime": "minimal",
        "description": "Database optimization and index maintenance"
      }
    ]
  },
  "meta": {
    "requestId": "req_20251125_5f3a8b2e",
    "timestamp": "2025-11-25T15:05:22Z",
    "processingTimeMs": 123
  }
}
```

---

## Request/Response Schemas

### Event Object Schema

```typescript
interface Event {
  id: string;                          // Unique event identifier
  title: string;                       // Event headline
  shortDescription?: string;           // Brief summary
  fullDescription?: string;            // Complete details
  type: EventType;                     // Event classification
  subType?: string;                    // Detailed categorization
  severity: SeverityLevel;             // Impact level
  status: EventStatus;                 // Current state
  source: SourceInfo;                  // Data origin
  timestamp: ISO8601String;            // Event occurrence time
  lastUpdated: ISO8601String;          // Last modification
  regions: Region[];                   // Affected areas
  detectedBiases: BiasDetection[];     // Cognitive biases found
  impactScore: number;                 // 0-10 impact rating
  relevanceScore: number;              // 0-1 relevance likelihood
  tags: string[];                      // Metadata tags
  sourceUrl: string;                   // Original source link
  relatedEventIds?: string[];          // Connected events
  timeline?: TimelineEntry[];          // Event progression
}

enum EventType {
  BREAKING_NEWS = "breaking_news",
  MARKET_DATA = "market_data",
  POLICY_CHANGE = "policy_change",
  SOCIAL_MOVEMENT = "social_movement",
  SECURITY_INCIDENT = "security_incident"
}

enum SeverityLevel {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  CRITICAL = "critical"
}

enum EventStatus {
  NEW = "new",
  DEVELOPING = "developing",
  RESOLVED = "resolved"
}

interface SourceInfo {
  id: string;
  name: string;
  credibilityScore: number;            // 0-1
  category: string;
}

interface BiasDetection {
  type: string;
  name: string;
  confidence: number;                  // 0-1
  description: string;
  affectedAreas: string[];
  mitigationSuggestions: string[];
}

interface Region {
  name: string;
  country?: string;
  affectedPopulation?: string;
  impactLevel: SeverityLevel;
}

interface TimelineEntry {
  timestamp: ISO8601String;
  event: string;
  source: string;
}
```

### Bias Object Schema

```typescript
interface Bias {
  id: string;
  name: string;
  category: BiasCategory;
  shortDescription: string;
  fullDescription: string;
  detectionFrequency: DetectionFrequency;
  commonContexts: string[];
  detectionCriteria: string[];
  mitigationStrategies: string[];
  affectedDecisions: string[];
  exampleScenarios: string[];
}

enum BiasCategory {
  PERCEPTION = "perception",
  DECISION_MAKING = "decision_making",
  MEMORY = "memory",
  SOCIAL = "social"
}

enum DetectionFrequency {
  VERY_COMMON = "very_common",
  COMMON = "common",
  OCCASIONAL = "occasional",
  RARE = "rare"
}

interface BiasActivationStatus {
  currentActivationLevel: string;
  detectionFrequency: number;          // 0-1
  eventsAffected: number;
  timeframe: string;
  trends: BiasActivationTrends;
  industryBreakdown: Record<string, IndustryStats>;
  recentOccurrences: BiasOccurrence[];
}

interface BiasOccurrence {
  eventId: string;
  eventTitle: string;
  detectionConfidence: number;         // 0-1
  affectedContext: string;
  timestamp: ISO8601String;
}
```

---

## Frontend Integration

### Event Timeline Component

Display events in chronological order with bias indicators.

```typescript
// Component Props
interface EventTimelineProps {
  events: Event[];
  highlightBiases?: string[];          // Bias types to highlight
  showImpactScore?: boolean;
  onEventClick?: (eventId: string) => void;
  onBiasFilter?: (biasType: string) => void;
}

// Usage Example
<EventTimeline
  events={fetchedEvents}
  highlightBiases={["confirmation_bias", "availability_heuristic"]}
  showImpactScore={true}
  onEventClick={(id) => navigateToDetail(id)}
/>
```

### Cognitive Bias Dashboard

Display bias activation levels and impact across events.

```typescript
interface BiasDashboardProps {
  timeframe: "24h" | "7d" | "30d" | "90d";
  filterIndustries?: string[];
  filterRegions?: string[];
  showActivationTrends?: boolean;
  onBiasSelect?: (biasId: string) => void;
}

// Usage Example
<BiasDashboard
  timeframe="30d"
  filterIndustries={["finance", "technology"]}
  showActivationTrends={true}
  onBiasSelect={(biasId) => viewBiasDetails(biasId)}
/>
```

### Threat Feed Status Widget

Real-time display of threat intelligence feed health.

```typescript
interface ThreatFeedWidgetProps {
  feedTypes?: ThreatType[];
  showDetails?: boolean;
  refreshInterval?: number;            // milliseconds
  onFeedStatusChange?: (feed: ThreatFeed) => void;
}

// Usage Example
<ThreatFeedWidget
  feedTypes={["geopolitical", "cyber"]}
  showDetails={true}
  refreshInterval={30000}
/>
```

---

## Business Value

### 1. Situational Awareness

**Value Proposition:**
- Real-time access to global events and their impacts
- Comprehensive context through related events and timelines
- Geographic and industry-specific filtering for targeted analysis

**Business Applications:**
- Supply chain risk monitoring across multiple industries
- Geopolitical risk assessment for international operations
- Market intelligence for competitive positioning
- Regulatory change tracking for compliance

**Example Scenario:**
A manufacturing company uses the Events API to monitor supply chain disruptions in real-time. When the semiconductor facility closure is detected, they:
1. Retrieve related geopolitical events showing regional tensions
2. Filter events by impact on automotive industry
3. Analyze cognitive biases in media reporting to separate hype from real risk
4. Estimate financial impact and mitigation options

### 2. Cognitive Bias Detection

**Value Proposition:**
- Identify systematic biases in event reporting and analysis
- Quantify bias influence on decision-making
- Reduce risk of bias-driven strategic errors

**Business Applications:**
- Investment risk analysis with bias adjustment
- Policy decision-making with bias awareness
- Competitive intelligence with reduced confirmation bias
- Market forecasting with availability heuristic correction

**Example Scenario:**
An investment firm using the Biases API detects high activation of:
- **Availability Heuristic:** Recent semiconductor shortage creates overestimation of current risk
- **Confirmation Bias:** Analysts selectively emphasizing negative supply chain impacts

The firm applies mitigation strategies:
1. Compares current shortage risk to historical baseline (correct availability heuristic)
2. Systematically reviews alternative supply chain solutions (correct confirmation bias)
3. Makes more accurate investment decision based on balanced analysis

### 3. Risk Management Enhancement

**Value Proposition:**
- Data-driven identification of emerging threats
- Impact scoring for risk prioritization
- Threat feed integration for comprehensive coverage

**Business Applications:**
- Enterprise risk monitoring across geopolitical, cyber, and economic threats
- Crisis response planning with real-time data
- Insurance risk assessment and pricing
- Regulatory risk compliance

**Example Scenario:**
A global financial services firm monitors:
1. Geopolitical tensions affecting client markets (via /events/geopolitical)
2. Cyber threat intelligence updates (via /threat-feeds)
3. Economic indicators affecting portfolios (via /threat-feeds)
4. Cognitive biases in their own internal analysis

Result: More robust risk assessment and client advisory capabilities.

### 4. Decision Support

**Value Proposition:**
- Comprehensive event context for informed decisions
- Bias-corrected analysis frameworks
- Automated impact assessment and scoring

**Business Applications:**
- Strategic planning with enhanced awareness
- Merger & acquisition due diligence
- Product launch timing optimization
- Geographic market entry decisions

---

## Error Handling

### Standard Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "parameter": "specific_field",
      "value": "problematic_value"
    }
  },
  "meta": {
    "requestId": "req_20251125_5f3a8b2c",
    "timestamp": "2025-11-25T14:35:22Z"
  }
}
```

### Common Error Codes

| Code | Status | Description | Solution |
|------|--------|-------------|----------|
| `INVALID_FILTER` | 400 | Invalid filter parameter | Check parameter format and allowed values |
| `MISSING_REQUIRED` | 400 | Missing required field | Ensure all required parameters are included |
| `INVALID_DATE_FORMAT` | 400 | Date format error | Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ` |
| `RESOURCE_NOT_FOUND` | 404 | Event or bias not found | Verify resource ID is correct |
| `UNAUTHORIZED` | 401 | Invalid authentication token | Provide valid API token |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Wait before making additional requests |
| `INTERNAL_SERVER_ERROR` | 500 | Server error | Retry after delay or contact support |

---

## Rate Limiting

### Rate Limit Policy

- **Standard tier:** 100 requests/minute, 10,000/day
- **Enterprise tier:** 1,000 requests/minute, 1,000,000/day
- **Response headers:** Include rate limit information

### Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1732562400
Retry-After: 42
```

### Example Rate Limit Exceeded Response

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please retry after 42 seconds.",
    "details": {
      "limit": 100,
      "period": "60s",
      "retryAfter": 42
    }
  }
}
```

---

## Summary

The Events API provides a comprehensive platform for accessing global events, detecting cognitive biases, monitoring threats, and supporting informed decision-making. With real-time data streams, sophisticated filtering, and integrated bias detection, organizations can maintain situational awareness while actively countering cognitive biases in their analysis processes.

**Key Capabilities:**
- Comprehensive event retrieval with advanced filtering
- Geopolitical event specialization
- Cognitive bias detection and mitigation
- Threat intelligence feed integration
- Real-time pipeline health monitoring

**Expected Outcomes:**
- Enhanced situational awareness for strategic decisions
- Reduced bias-driven decision errors
- Improved risk management capabilities
- Data-driven competitive advantage
- Stronger organizational resilience

---

## Webhooks & Callbacks

### Overview

The Events API supports webhooks for real-time event notifications. Register webhook URLs to receive HTTP POST notifications when specific events occur, enabling real-time integrations without polling.

### Webhook Registration

#### POST /api/v1/webhooks

Register a new webhook subscription for event notifications.

**Request**:
```json
{
  "url": "https://your-domain.com/webhooks/aeon-events",
  "events": ["cve.new", "breach.predicted", "bias.activated", "threat.detected"],
  "secret": "your_webhook_secret_key_here",
  "active": true,
  "metadata": {
    "environment": "production",
    "team": "security-ops"
  }
}
```

**Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| url | string | Yes | HTTPS endpoint to receive webhook payloads |
| events | array | Yes | Event types to subscribe to |
| secret | string | Yes | Secret key for HMAC signature verification (min 32 chars) |
| active | boolean | No | Enable/disable webhook (default: true) |
| metadata | object | No | Custom metadata for webhook tracking |

**Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "webhookId": "wh_20251125_abc123",
    "url": "https://your-domain.com/webhooks/aeon-events",
    "events": ["cve.new", "breach.predicted", "bias.activated", "threat.detected"],
    "active": true,
    "createdAt": "2025-11-25T15:00:00Z",
    "lastTriggered": null,
    "deliveryStats": {
      "totalDeliveries": 0,
      "successfulDeliveries": 0,
      "failedDeliveries": 0,
      "averageResponseTime": null
    }
  },
  "meta": {
    "requestId": "req_webhook_001",
    "timestamp": "2025-11-25T15:00:00Z"
  }
}
```

### Webhook Event Types

| Event Type | Description | Payload Example |
|------------|-------------|-----------------|
| `cve.new` | New CVE published affecting your equipment | CVE-2025-12345 details |
| `cve.critical` | Critical CVE (CVSS ≥ 9.0) detected | High-priority CVE alert |
| `breach.predicted` | Psychohistory prediction of breach risk | Sector breach probability |
| `breach.actual` | Confirmed security breach detected | Breach incident details |
| `bias.activated` | Cognitive bias threshold exceeded | Bias detection alert |
| `bias.mitigated` | Bias successfully mitigated | Bias mitigation success |
| `threat.detected` | New threat actor activity detected | Threat intelligence update |
| `threat.escalated` | Threat level escalation | Threat level change |
| `equipment.vulnerable` | Equipment exposed to new vulnerability | Equipment CVE mapping |
| `equipment.patched` | Equipment successfully patched | Patch completion confirmation |

### Webhook Payload Examples

#### 1. New CVE Event (`cve.new`)

```json
{
  "eventType": "cve.new",
  "eventId": "evt_cve_20251125_001",
  "timestamp": "2025-11-25T15:00:00Z",
  "data": {
    "cveId": "CVE-2025-12345",
    "publishedDate": "2025-11-25T14:00:00Z",
    "cvssScore": 9.8,
    "severity": "CRITICAL",
    "epssScore": 0.87,
    "description": "Remote code execution vulnerability in Apache Struts 2.5.x",
    "affectedEquipment": [
      {
        "equipmentId": "EQ-WEB-001",
        "equipmentName": "Primary Web Server",
        "sector": "ENERGY",
        "criticality": "Tier1"
      },
      {
        "equipmentId": "EQ-WEB-002",
        "equipmentName": "Backup Web Server",
        "sector": "ENERGY",
        "criticality": "Tier2"
      }
    ],
    "affectedCount": 2,
    "patchAvailable": true,
    "fixedVersion": "2.5.32",
    "recommendation": "Immediate patching required within 24-48 hours",
    "priority": "NOW",
    "priorityScore": 9.2
  },
  "webhookId": "wh_20251125_abc123",
  "deliveryAttempt": 1
}
```

#### 2. Breach Prediction Event (`breach.predicted`)

```json
{
  "eventType": "breach.predicted",
  "eventId": "evt_breach_20251125_001",
  "timestamp": "2025-11-25T15:30:00Z",
  "data": {
    "predictionId": "pred_20251125_001",
    "sector": "ENERGY",
    "breachProbability": 0.78,
    "confidenceLevel": 0.85,
    "timeWindow": "30 days",
    "contributingFactors": [
      {
        "factor": "Unpatched Critical CVEs",
        "weight": 0.35,
        "description": "23 critical CVEs remain unpatched for >90 days"
      },
      {
        "factor": "Threat Actor Activity",
        "weight": 0.25,
        "description": "APT-001 targeting Energy sector (12 campaigns detected)"
      },
      {
        "factor": "Vulnerability Density",
        "weight": 0.20,
        "description": "Above-average vulnerability concentration in SCADA systems"
      },
      {
        "factor": "Cognitive Bias Impact",
        "weight": 0.20,
        "description": "Normalcy bias delaying critical patch implementation"
      }
    ],
    "recommendation": "Immediate risk mitigation required. Review NOW-priority CVEs and implement compensating controls.",
    "affectedSystems": 342,
    "estimatedImpact": "$50-100 million operational disruption",
    "mitigationDeadline": "2025-12-25T00:00:00Z"
  },
  "webhookId": "wh_20251125_abc123",
  "deliveryAttempt": 1
}
```

#### 3. Bias Activated Event (`bias.activated`)

```json
{
  "eventType": "bias.activated",
  "eventId": "evt_bias_20251125_001",
  "timestamp": "2025-11-25T16:00:00Z",
  "data": {
    "biasType": "confirmation_bias",
    "biasName": "Confirmation Bias",
    "activationLevel": "HIGH",
    "detectionConfidence": 0.82,
    "affectedDecisions": [
      "vulnerability_prioritization",
      "patch_scheduling",
      "risk_assessment"
    ],
    "context": {
      "sector": "ENERGY",
      "decisionMakers": 5,
      "analystsAffected": 12,
      "reportsImpacted": 8
    },
    "biasDescription": "Analysis selectively emphasizing vulnerabilities matching pre-existing threat model while dismissing contradictory evidence",
    "evidenceExamples": [
      "87% of cited sources support existing threat narrative",
      "Alternative risk assessments dismissed without thorough review",
      "Stakeholder feedback ignored in favor of confirmation sources"
    ],
    "mitigationSuggestions": [
      "Implement red-team review process for analysis",
      "Mandate inclusion of contradictory evidence in reports",
      "Rotate analysis teams to prevent echo chamber formation",
      "Use structured decision-making frameworks to reduce bias"
    ],
    "riskLevel": "MEDIUM",
    "estimatedImpact": "Potential misallocation of $500K-$1M in security budget"
  },
  "webhookId": "wh_20251125_abc123",
  "deliveryAttempt": 1
}
```

#### 4. Threat Detected Event (`threat.detected`)

```json
{
  "eventType": "threat.detected",
  "eventId": "evt_threat_20251125_001",
  "timestamp": "2025-11-25T17:00:00Z",
  "data": {
    "threatId": "threat_20251125_001",
    "threatActorId": "APT-001",
    "threatActorName": "Hafnium",
    "activityType": "reconnaissance",
    "targetedSectors": ["ENERGY", "WATER"],
    "targetedEquipmentTypes": ["SCADA", "ICS"],
    "cveExploited": ["CVE-2021-44228", "CVE-2023-34362"],
    "observedTactics": [
      "Initial Access via Log4Shell",
      "Lateral Movement through compromised credentials",
      "Persistence via scheduled tasks"
    ],
    "threatLevel": "CRITICAL",
    "confidence": 0.92,
    "firstObserved": "2025-11-25T16:30:00Z",
    "lastObserved": "2025-11-25T17:00:00Z",
    "affectedOrganizations": 23,
    "yourRisk": {
      "exposedEquipment": 8,
      "vulnerableToTactics": true,
      "mitigationStatus": "PARTIAL",
      "recommendation": "Immediate IDS rule deployment and Log4Shell patching"
    }
  },
  "webhookId": "wh_20251125_abc123",
  "deliveryAttempt": 1
}
```

### HMAC Signature Verification

All webhook payloads include an HMAC-SHA256 signature header for authenticity verification.

**Signature Header**:
```http
X-AEON-Signature: sha256=abc123def456...
X-AEON-Timestamp: 1732553400
X-AEON-Webhook-Id: wh_20251125_abc123
```

**Verification Code (Node.js)**:
```javascript
const crypto = require('crypto');

function verifyWebhookSignature(payload, signature, secret) {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(JSON.stringify(payload))
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(`sha256=${expectedSignature}`)
  );
}

// Express.js webhook handler
app.post('/webhooks/aeon-events', (req, res) => {
  const signature = req.headers['x-aeon-signature'];
  const secret = process.env.WEBHOOK_SECRET;

  if (!verifyWebhookSignature(req.body, signature, secret)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Process webhook payload
  const { eventType, data } = req.body;
  console.log(`Received ${eventType} event:`, data);

  // Acknowledge receipt
  res.status(200).json({ received: true });
});
```

**Verification Code (Python)**:
```python
import hmac
import hashlib
import json

def verify_webhook_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        json.dumps(payload).encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    expected_full = f"sha256={expected_signature}"
    return hmac.compare_digest(signature, expected_full)

# Flask webhook handler
@app.route('/webhooks/aeon-events', methods=['POST'])
def handle_webhook():
    signature = request.headers.get('X-AEON-Signature')
    secret = os.environ.get('WEBHOOK_SECRET')

    if not verify_webhook_signature(request.json, signature, secret):
        return jsonify({'error': 'Invalid signature'}), 401

    # Process webhook payload
    event_type = request.json.get('eventType')
    data = request.json.get('data')
    print(f"Received {event_type} event: {data}")

    # Acknowledge receipt
    return jsonify({'received': True}), 200
```

### Webhook Management

#### GET /api/v1/webhooks

List all registered webhooks.

**Response**:
```json
{
  "success": true,
  "data": {
    "webhooks": [
      {
        "webhookId": "wh_20251125_abc123",
        "url": "https://your-domain.com/webhooks/aeon-events",
        "events": ["cve.new", "breach.predicted"],
        "active": true,
        "createdAt": "2025-11-25T15:00:00Z",
        "lastTriggered": "2025-11-25T17:00:00Z",
        "deliveryStats": {
          "totalDeliveries": 247,
          "successfulDeliveries": 243,
          "failedDeliveries": 4,
          "successRate": 0.984,
          "averageResponseTime": "234ms"
        }
      }
    ],
    "total": 1
  }
}
```

#### PUT /api/v1/webhooks/{webhookId}

Update webhook configuration.

**Request**:
```json
{
  "events": ["cve.new", "cve.critical", "breach.predicted"],
  "active": true
}
```

#### DELETE /api/v1/webhooks/{webhookId}

Delete webhook subscription.

**Response (204 No Content)**

### Webhook Retry Logic

Failed webhook deliveries are automatically retried with exponential backoff:

| Attempt | Delay | Total Elapsed |
|---------|-------|---------------|
| 1 | Immediate | 0s |
| 2 | 5 seconds | 5s |
| 3 | 30 seconds | 35s |
| 4 | 5 minutes | 5m 35s |
| 5 | 30 minutes | 35m 35s |

After 5 failed attempts, the webhook is marked as inactive and requires manual re-activation.

### Webhook Best Practices

1. **Idempotency**: Handle duplicate deliveries gracefully (use `eventId` for deduplication)
2. **Fast Response**: Acknowledge webhooks within 5 seconds (process asynchronously)
3. **Signature Verification**: Always verify HMAC signatures
4. **Timeout Handling**: Set webhook response timeout to 10 seconds
5. **Error Logging**: Log all webhook failures for debugging
6. **Monitoring**: Track webhook delivery success rates and response times

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-25
**Status:** COMPLETE
**Total Lines:** 1,600+
