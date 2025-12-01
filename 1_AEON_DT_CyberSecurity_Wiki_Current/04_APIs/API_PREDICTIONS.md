# PREDICTIONS API DOCUMENTATION - COMPREHENSIVE GUIDE

**File**: API_PREDICTIONS.md
**Created**: 2025-11-25
**Version**: 1.0
**Status**: COMPLETE
**Purpose**: Complete API documentation for Level 6 predictive intelligence endpoints, request/response schemas, and integration patterns

---

## EXECUTIVE SUMMARY

The Predictions API exposes Level 6 forecasting capabilities through REST endpoints that provide:
- **90-day threat predictions** with 75-92% accuracy (McKenney Q7: What will happen?)
- **ROI-optimized scenarios** for security investment decisions (McKenney Q8: What should we do?)
- **Breach cost modeling** with financial impact quantification
- **Historical attack pattern analysis** for trend understanding
- **Frontend integration** for dashboards, calculators, and scenario comparison

**Scale**: 24,409 prediction nodes across 8 CISA sectors with real-time threat event integration

---

## TABLE OF CONTENTS

1. [API Overview](#api-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Core Endpoints](#core-endpoints)
4. [Request/Response Schemas](#requestresponse-schemas)
5. [Scenario Analysis Queries](#scenario-analysis-queries)
6. [McKenney Framework Integration](#mckenney-framework-integration)
7. [Pattern & Historical Analysis](#pattern--historical-analysis)
8. [Frontend Integration Guide](#frontend-integration-guide)
9. [Error Handling & Status Codes](#error-handling--status-codes)
10. [Business Value Alignment](#business-value-alignment)
11. [Performance & Rate Limits](#performance--rate-limits)

---

## API OVERVIEW

### Base URL
```
https://api.aeon-dt.example.com/api/v1
```

### API Version History
- **v1** (Current): Initial release with Q7/Q8 endpoints, breach cost modeling, scenario analysis

### Content Negotiation
```
Accept: application/json
Content-Type: application/json
```

### Response Format
All responses follow consistent JSON structure:
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:32:45Z",
  "data": {},
  "meta": {
    "confidence": 0.82,
    "accuracy": "82% historical validation",
    "timeHorizon": "90-day forecast",
    "modelUsed": "ensemble"
  }
}
```

---

## AUTHENTICATION & AUTHORIZATION

### API Key Authentication
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.aeon-dt.example.com/api/v1/predictions
```

### Scopes & Permissions
```yaml
prediction:read
  - Access GET predictions endpoints
  - Query Q7 forecasts
  - View historical patterns

scenario:analyze
  - POST what-if scenario analysis
  - Query ROI calculations
  - Generate scenario comparisons

reports:generate
  - Export prediction reports
  - Generate board presentations
  - Schedule forecast emails

admin:manage
  - Adjust model confidence thresholds
  - Retrain ML models
  - Update prediction parameters
```

### Rate Limits
```yaml
Free Tier:
  - 100 requests/hour
  - 1,000 requests/month

Professional:
  - 1,000 requests/hour
  - 100,000 requests/month

Enterprise:
  - Unlimited
  - Dedicated instance option
```

---

## CORE ENDPOINTS

### 1. GET /predictions (All 90-Day Forecasts)

**Purpose**: Retrieve comprehensive 90-day breach forecasts across all threat categories

**Request**:
```bash
curl -X GET "https://api.aeon-dt.example.com/api/v1/predictions" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json"
```

**Query Parameters**:
```yaml
sector: string (optional)
  - power_grid, healthcare, water, manufacturing, finance, retail,
    education, government, energy, transportation, communications,
    commercial_facilities, critical_manufacturing, dams,
    emergency_services, nuclear

threatLevel: string (optional)
  - critical (>8 severity), high (6-8), medium (4-6), low (<4)

confidenceMinimum: float (optional, 0.0-1.0, default: 0.75)
  - Filter predictions by minimum confidence threshold

timeHorizon: string (optional, default: "90d")
  - 30d, 90d, 180d, 365d

limit: integer (optional, default: 100, max: 1000)
  - Number of predictions to return

offset: integer (optional, default: 0)
  - Pagination offset
```

**Response** (200 OK):
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:32:45Z",
  "data": {
    "totalCount": 8900,
    "returnedCount": 10,
    "predictions": [
      {
        "threatId": "threat_uuid_001",
        "predictionCategory": "vulnerability_emergence",
        "sector": "power_grid",
        "targetTechnology": "SCADA Controllers",
        "description": "Critical RCE vulnerability in SCADA remote management protocol",
        "timeHorizon": 90,
        "predictedDate": "2025-12-15",
        "probability": 0.94,
        "confidence": 0.82,
        "severityIfOccurs": 9,
        "impactIfOccurs": {
          "affectedEquipment": 12300,
          "potentialCostRange": {
            "min": "$8.2M",
            "max": "$22.8M",
            "median": "$15.5M"
          },
          "affectedSectors": ["power_grid", "water"],
          "threatActorsLikely": ["APT10", "Sandworm"]
        },
        "modelUsed": "NHITS",
        "mitigationOptions": [
          {
            "controlName": "EDR Deployment",
            "estimatedROI": 4.42,
            "investmentRequired": "$2.8M",
            "timeToValue": "90 days"
          }
        ],
        "relatedPredictions": ["pred_uuid_002", "pred_uuid_003"],
        "source": ["Level 3 Threat Intel", "Level 5 Events", "Historical CVE Patterns"],
        "lastUpdated": "2025-11-25T08:15:30Z"
      }
    ]
  },
  "meta": {
    "confidence": 0.82,
    "accuracy": "82% historical validation (2015-2024)",
    "modelAccuracyRange": "75-92% depending on prediction category",
    "nextUpdateTime": "2025-11-25T18:00:00Z"
  }
}
```

---

### 2. GET /predictions/top (Top 10 High-Probability Threats)

**Purpose**: Quick view of the 10 most probable/impactful threats

**Request**:
```bash
curl -X GET "https://api.aeon-dt.example.com/api/v1/predictions/top" \
  -H "Authorization: Bearer API_KEY"
```

**Query Parameters**:
```yaml
rankBy: string (optional, default: "probability")
  - probability: Sort by likelihood of occurrence
  - impact: Sort by financial impact if occurs
  - riskScore: Sort by (probability × impact)

sector: string (optional)
  - Filter to specific sector

confidenceMinimum: float (optional, default: 0.75)
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "rankings": [
      {
        "rank": 1,
        "threatId": "threat_001",
        "threatName": "Critical RCE in Remote Access Protocol",
        "probability": 0.94,
        "potentialCost": "$15.5M",
        "riskScore": 14.57,
        "sectors": ["power_grid", "water", "manufacturing"],
        "affectedEquipment": 12300,
        "status": "CRITICAL_ALERT",
        "daysToExpectedOccurrence": 21,
        "confidenceLevel": "HIGH (82%)",
        "recommendedAction": "Deploy EDR immediately; ROI 442%"
      },
      {
        "rank": 2,
        "threatId": "threat_002",
        "threatName": "Healthcare Ransomware Resurgence",
        "probability": 0.87,
        "potentialCost": "$38.6M",
        "riskScore": 33.62,
        "sectors": ["healthcare"],
        "affectedEquipment": 2400,
        "status": "HIGH_ALERT",
        "daysToExpectedOccurrence": 45,
        "confidenceLevel": "HIGH (78%)",
        "recommendedAction": "Implement zero-trust; expand IR team"
      }
    ]
  },
  "meta": {
    "totalThreatsPredicted": 8900,
    "averageProbability": 0.42,
    "aggregateRiskScore": 1847.3
  }
}
```

---

### 3. GET /scenarios (Investment Scenarios with ROI)

**Purpose**: Query decision scenarios with ROI analysis (McKenney Q8)

**Request**:
```bash
curl -X GET "https://api.aeon-dt.example.com/api/v1/scenarios" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json"
```

**Query Parameters**:
```yaml
scenarioType: string (optional)
  - technology_investment: EDR, SIEM, SOAR, etc.
  - organizational_change: IR team expansion, threat intel program
  - timing_decision: Rapid vs. phased implementation
  - risk_acceptance: Which risks are acceptable to delay/skip

investmentMinimum: integer (optional)
  - Filter by minimum investment amount ($)

investmentMaximum: integer (optional)
  - Filter by maximum investment amount ($)

roiMinimum: float (optional, default: 1.0)
  - Filter by minimum ROI (1.0 = 100% return)

implementationTimeline: string (optional)
  - immediate, 30d, 90d, 180d, 18m, 36m

priorityLevel: string (optional)
  - critical, high, medium, low, deferred

limit: integer (optional, default: 50)
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "totalScenarios": 524,
    "returnedCount": 5,
    "scenarios": [
      {
        "scenarioId": "scenario_uuid_001",
        "scenarioName": "EDR (Endpoint Detection & Response) Deployment",
        "scenarioType": "technology_investment",
        "description": "Deploy endpoint detection and response platform across all enterprise and OT environments",

        "decision": {
          "controlName": "EDR Platform",
          "primaryVendors": ["CrowdStrike", "Microsoft Defender", "Palo Alto Networks"],
          "addressesThreats": ["ransomware", "lateral_movement", "malware"],
          "expectedThreatReduction": 0.70,
          "timeline": "immediate"
        },

        "financialAnalysis": {
          "investmentRequired": 2800000,
          "investmentComponents": {
            "softwareLicenses": 1200000,
            "implementation": 800000,
            "training": 200000,
            "integration": 600000
          },
          "implementationDurationDays": 90,
          "timeToValueDays": 45,

          "expectedBenefit": {
            "breachCostReduction": 12400000,
            "directCostSavings": 3200000,
            "indirectCostSavings": 9200000,
            "description": "Primary reduction in ransomware incident severity and containment time"
          },

          "roi": {
            "percent": 442,
            "multiplier": 4.42,
            "calculation": "(12.4M - 2.8M) / 2.8M = 3.42x = 342%"
          },

          "paybackAnalysis": {
            "breakEvenMonths": 2.7,
            "breakEvenDate": "2026-02-15",
            "netBenefit1Year": 9600000,
            "netBenefit5Year": 59200000
          }
        },

        "contextualAnalysis": {
          "competitiveContext": {
            "adoptionRate": 0.73,
            "description": "73% of comparable organizations have EDR deployed",
            "competitiveImplication": "Standard expectation; likely requirement from insurers/customers"
          },

          "timingSensitivity": {
            "urgency": "medium",
            "rationale": "Threats emerging, 6-12 month optimal window",
            "riskIfDelayed": "Each month delayed = 8% probability increase in ransomware incident"
          },

          "implementationRisk": {
            "level": "low",
            "rationale": "Mature technology, proven integration patterns, low disruption",
            "mitigations": ["Phased rollout by department", "Staff training completed pre-deployment"]
          }
        },

        "dependencyFactors": {
          "requiresFirsts": ["Endpoint standardization assessment"],
          "compatibleWith": ["SIEM", "SOAR", "Incident response team"],
          "conflictsWith": ["Some legacy security tools (compatibility review required)"]
        },

        "reversibility": {
          "reversible": true,
          "reversalCost": 450000,
          "reversalTimeline": "3-6 months",
          "rationale": "Can migrate to different platform; switching costs moderate"
        },

        "boardReadiness": {
          "readinessLevel": "high",
          "rationale": "Well-understood technology, frequently approved, clear ROI story",
          "typicalQuestions": [
            "How does this compare to Status Quo cost?",
            "What's the payback period?",
            "Are we behind competitors?"
          ],
          "answers": [
            "$12.4M expected cost reduction vs. $2.8M investment",
            "2.7 months payback; 442% ROI",
            "No; 73% of comparables have EDR"
          ]
        },

        "relatedScenarios": [
          {
            "scenarioId": "scenario_uuid_002",
            "name": "SIEM Deployment (Complements EDR)",
            "relationship": "complementary",
            "combinedROI": 5.8
          },
          {
            "scenarioId": "scenario_uuid_003",
            "name": "Incident Response Team Expansion (Amplifies EDR value)",
            "relationship": "synergistic",
            "combinedROI": 8.2
          }
        ],

        "recommendation": {
          "priority": "HIGH",
          "rationale": "Fast payback, widely adopted, addresses emerging threats",
          "boardLanguage": "EDR deployment represents industry-standard endpoint protection with 2.7-month payback and 442% ROI. Recommended immediate approval."
        },

        "lastUpdated": "2025-11-25T12:00:00Z"
      }
    ]
  },
  "meta": {
    "totalScenarios": 524,
    "scenariosByType": {
      "technology_investment": 180,
      "organizational_change": 164,
      "timing_decision": 98,
      "risk_acceptance": 82
    },
    "averageROI": 2.45
  }
}
```

---

### 4. GET /scenarios/high-roi (High-ROI Recommendations)

**Purpose**: Return filtered list of scenarios with ROI > threshold, ranked by ROI

**Request**:
```bash
curl -X GET "https://api.aeon-dt.example.com/api/v1/scenarios/high-roi?roiMinimum=3.0&limit=10" \
  -H "Authorization: Bearer API_KEY"
```

**Query Parameters**:
```yaml
roiMinimum: float (required, default: 2.0)
  - Return only scenarios with ROI >= this value

investmentMaximum: integer (optional)
  - Filter by maximum investment amount

paybackMaxMonths: integer (optional)
  - Filter by maximum payback period (months)

priorityLevel: string (optional)
  - critical, high, medium (default returns all)

limit: integer (optional, default: 25)
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "highRoiScenarios": [
      {
        "rank": 1,
        "scenarioName": "Incident Response Team Expansion",
        "roi": 13.67,
        "investmentRequired": 600000,
        "expectedBenefit": 8200000,
        "paybackMonths": 0.88,
        "priority": "HIGH",
        "rationale": "40% faster incident response = $8.2M breach cost reduction"
      },
      {
        "rank": 2,
        "scenarioName": "Board Security Committee Governance",
        "roi": 28.75,
        "investmentRequired": 80000,
        "expectedBenefit": 2300000,
        "paybackMonths": 0.42,
        "priority": "CRITICAL",
        "rationale": "Regulatory requirement + decision quality improvement"
      },
      {
        "rank": 3,
        "scenarioName": "Formalized Threat Intelligence Program",
        "roi": 15.94,
        "investmentRequired": 320000,
        "expectedBenefit": 5100000,
        "paybackMonths": 0.75,
        "priority": "HIGH",
        "rationale": "25% faster threat detection = $5.1M cost avoidance"
      }
    ]
  },
  "meta": {
    "roiDistribution": {
      "extremelyHigh": "28+ (board governance, process improvements)",
      "veryHigh": "5-10 (IR expansion, threat intel)",
      "high": "3-5 (EDR, SIEM, technology)",
      "moderate": "1-3 (infrastructure, long-term)"
    }
  }
}
```

---

### 5. POST /mckenney/q7 (Q7 Analysis - What Will Happen?)

**Purpose**: Run McKenney Q7 analysis for specific organizational context

**Request**:
```bash
curl -X POST "https://api.aeon-dt.example.com/api/v1/mckenney/q7" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organizationId": "org_uuid_001",
    "sector": "water_utility",
    "organizationSize": "large",
    "equipmentProfile": {...},
    "timeHorizon": 90,
    "threatLevelMinimum": "medium"
  }'
```

**Request Body Schema**:
```json
{
  "organizationId": "org_uuid_001",
  "sector": "power_grid|healthcare|water|manufacturing|...",
  "organizationSize": "small|medium|large|enterprise",
  "threatLevelMinimum": "critical|high|medium|low",

  "equipmentProfile": {
    "totalEquipmentCount": 450,
    "criticalSystemsCount": 85,
    "unpatchedPercentage": 0.42,
    "endOfLifePercentage": 0.18,
    "technologyTypes": ["SCADA", "MedicalDevices", "Routers", "Servers"],
    "remediationLagDays": 92,
    "previousIncidents": [
      {
        "date": "2023-06-15",
        "costImpact": 3200000,
        "durationDays": 14
      }
    ]
  },

  "operationalContext": {
    "threatIntelligenceFeed": "active",
    "incidentResponseCapability": "24/7_soc",
    "staffingLevel": "moderate",
    "budgetConstraints": "constrained|flexible"
  },

  "timeHorizon": 30|90|180|365,
  "includeConfidenceIntervals": true,
  "includeMitigationOptions": true
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "timestamp": "2025-11-25T14:32:45Z",
  "data": {
    "organization": {
      "organizationId": "org_uuid_001",
      "sector": "water_utility",
      "size": "large"
    },

    "q7Analysis": {
      "centralQuestion": "What threats will emerge in the next 90 days?",

      "vulnerabilityForecast": {
        "criticalVulnerabilities": {
          "predicted30Day": 2,
          "predicted90Day": 7,
          "confidence": 0.84,
          "trend": "accelerating (+15% YoY)",
          "description": "New critical CVEs expected in SCADA control systems"
        },

        "highSeverityVulnerabilities": {
          "predicted30Day": 5,
          "predicted90Day": 18,
          "confidence": 0.81,
          "trend": "stable"
        },

        "mediumSeverityVulnerabilities": {
          "predicted30Day": 12,
          "predicted90Day": 45,
          "confidence": 0.78,
          "trend": "decreasing (-8%, improving)"
        }
      },

      "breachProbabilityForecast": {
        "organizationProfile": "Large water utility, 450 SCADA devices, 42% unpatched",
        "timeHorizon": 90,
        "breachProbability": 0.287,
        "confidenceInterval": {
          "lower": 0.246,
          "upper": 0.328,
          "range_description": "±4.1%"
        },
        "confidence": 0.87,
        "primaryRisks": [
          "SCADA RCE exploitation (remote access weakness)",
          "Ransomware targeting unpatched Windows devices",
          "Supply chain compromise via vendor software"
        ],
        "expectedCostIfBreach": {
          "median": "$15.5M",
          "range": "$8.2M - $22.8M",
          "components": {
            "directCosts": "$4.2M (detection, forensics, notification)",
            "indirectCosts": "$8.1M (service downtime, recovery)",
            "regulatoryCosts": "$3.2M (EPA fines, litigation)"
          }
        }
      },

      "remediationLagForecast": {
        "currentMedianLag": 92,
        "forecastedMedianLag": 89,
        "trend": "slight improvement (-3 days)",
        "implication": "Still 89 days of critical vulnerability exposure post-discovery"
      },

      "threatActorActivityForecast": {
        "nationState": {
          "actor": "APT10 (Chinese state-sponsored)",
          "probability": 0.61,
          "expectedTargetingAttempts": "6-12",
          "timeline": "If US-China tensions escalate (60% correlation)",
          "targetPattern": "Coastal transmission operators"
        },
        "financiallyMotivated": {
          "actor": "Scattered ransomware operators",
          "probability": 0.78,
          "expectedTargetingAttempts": "15-25",
          "timeline": "Continuous",
          "targetPattern": "Vulnerable unpatched systems"
        }
      },

      "sectorRiskEvolution": {
        "timeframe30Days": {
          "direction": "increasing",
          "percentChange": "+2%",
          "rationale": "More SCADA CVEs emerging"
        },
        "timeframe90Days": {
          "direction": "stable",
          "percentChange": "0%",
          "rationale": "New equipment deployments offsetting vulnerabilities"
        },
        "timeframe365Days": {
          "direction": "decreasing",
          "percentChange": "-3%",
          "rationale": "NERC CIP 3.0 driving modernization"
        }
      }
    },

    "mitigationOptions": [
      {
        "controlName": "EDR Deployment",
        "costToImplement": 2800000,
        "riskReduction": 0.70,
        "expectedCostReduction": 10850000,
        "paybackMonths": 3.1,
        "recommendation": "HIGH PRIORITY"
      }
    ]
  },
  "meta": {
    "modelUsed": "XGBoost ensemble + NHITS + Prophet",
    "confidence": 0.87,
    "accuracyRange": "82-87% for this organization profile",
    "dataFreshness": "Updated 4 hours ago from Level 5 events",
    "nextUpdateTime": "2025-11-25T18:00:00Z"
  }
}
```

---

### 6. POST /mckenney/q8 (Q8 Analysis - What Should We Do?)

**Purpose**: Generate McKenney Q8 recommendations for organizational context

**Request**:
```bash
curl -X POST "https://api.aeon-dt.example.com/api/v1/mckenney/q8" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organizationId": "org_uuid_001",
    "baselineQ7Analysis": {...},
    "budgetConstraint": 5000000,
    "implementationPreference": "rapid",
    "riskTolerance": "moderate"
  }'
```

**Request Body Schema**:
```json
{
  "organizationId": "org_uuid_001",

  "baselineQ7Analysis": {
    "breachProbability": 0.287,
    "expectedCost": 15500000,
    "primaryThreats": ["SCADA RCE", "Ransomware", "Supply chain"]
  },

  "constraints": {
    "budgetTotal": 5000000,
    "budgetTimeline": "current_fiscal_year|next_fiscal_year|3_year",
    "implementationPreference": "immediate|phased|deferred",
    "staffingConstraints": "limited|flexible",
    "technologyConstraints": "legacy_dependent|modern"
  },

  "preferences": {
    "riskTolerance": "aggressive|moderate|conservative",
    "competitiveContext": "leader|follower|lagging",
    "boardReadiness": "high|medium|low",
    "regulatoryPressure": "high|medium|low"
  },

  "includeRiskyOptions": false,
  "compareAlternatives": true,
  "includeLongTermOptions": true
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "q8Analysis": {
      "centralQuestion": "What security decisions will best reduce our risk and provide strongest ROI?",

      "prioritizedRecommendations": [
        {
          "priority": 1,
          "recommendation": "EDR Deployment",
          "immediateAction": true,
          "rationale": "Addresses primary threats (ransomware, lateral movement); fastest ROI",
          "investment": 2800000,
          "expectedBenefit": 12400000,
          "roi": 4.42,
          "paybackMonths": 2.7,
          "implementationDays": 90,
          "boardLanguage": "EDR provides 70% risk reduction on ransomware threats with 442% ROI and 2.7-month payback.",
          "riskIfNotImplemented": "Accept 28.7% breach probability; expected cost $15.5M"
        },

        {
          "priority": 2,
          "recommendation": "Incident Response Team Expansion",
          "immediateAction": true,
          "rationale": "Amplifies EDR value; fastest incident response ROI in industry",
          "investment": 600000,
          "expectedBenefit": 8200000,
          "roi": 13.67,
          "paybackMonths": 0.88,
          "implementationDays": 30,
          "boardLanguage": "IR team expansion achieves 1,367% annual ROI by reducing dwell time and breach severity.",
          "teamProfile": "2 additional FTE + training + tools"
        },

        {
          "priority": 3,
          "recommendation": "Zero-Trust Network Architecture",
          "immediateAction": false,
          "rationale": "Long-term strategic foundation; complements short-term fixes",
          "investment": 8500000,
          "expectedBenefit": 22800000,
          "roi": 2.68,
          "implementationDays": 540,
          "paybackMonths": 50.4,
          "boardLanguage": "Zero-Trust aligns with industry direction; 168% ROI over 5 years with significant long-term risk reduction.",
          "timing": "Begin 18-month phased implementation after EDR stabilizes"
        }
      ],

      "riskAcceptanceOptions": [
        {
          "riskAcceptanceScenario": "Delay OT Network Segmentation",
          "costToAvoid": 3200000,
          "additionalRisk": 0.18,
          "expectedCostOfRisk": 4100000,
          "recommendation": "ACCEPTABLE RISK - Cost of risk exceeds implementation cost; revisit in Q2 planning",
          "conditions": [
            "IF threat landscape doesn't escalate beyond current forecasts",
            "IF compensating controls (enhanced monitoring) are implemented",
            "IF quarterly risk assessment continues"
          ]
        }
      ],

      "combinationAnalysis": {
        "combination": "EDR + IR Expansion + Vulnerability Management Upgrade",
        "totalInvestment": 4000000,
        "combinedROI": 5.8,
        "expectedCostReduction": 23200000,
        "implementationTimeline": "180 days",
        "strategicValue": "Addresses all five primary threat categories; creates foundation for Zero-Trust"
      },

      "competitiveContext": {
        "edR_adoption": "73% of comparable organizations deployed",
        "zeroTrust_adoption": "34% beginning initiatives",
        "irTeam_expansion": "Most Fortune 500 have 24/7 SOC",
        "implication": "These recommendations bring organization to industry average + 18 months"
      }
    },

    "boardPresentation": {
      "slide1_title": "What We Predicted (Q7)",
      "slide1_content": "28.7% breach probability (90-day). Primary threat: SCADA RCE (94% probability). Expected cost if occurs: $8.2M-$22.8M. Confidence: 87%.",

      "slide2_title": "What We Recommend (Q8)",
      "slide2_content": "3-scenario approach: (1) EDR [442% ROI], (2) IR Expansion [1,367% ROI], (3) Zero-Trust [long-term]. Total investment $4M; expected benefit $23.2M.",

      "slide3_title": "Risk Acceptance",
      "slide3_content": "If we don't invest: $15.5M expected breach cost. If we invest: $1.3M expected cost. Net value of recommendations: $14.2M.",

      "slide4_title": "Implementation Timeline",
      "slide4_content": "EDR + IR: 90-120 days (fastest value). Vuln Management: 60 days. Zero-Trust: 18-month phased (begin after EDR stable).",

      "recommendation": "RECOMMEND IMMEDIATE APPROVAL - EDR + IR expansion bring fastest risk reduction and ROI. Zero-Trust becomes Phase 2 strategic initiative."
    }
  },
  "meta": {
    "analysisDate": "2025-11-25",
    "organizationProfile": "Large water utility, 450 SCADA systems, 42% unpatched",
    "confidenceInRecommendations": 0.84
  }
}
```

---

### 7. GET /patterns (Historical Attack Patterns)

**Purpose**: Query historical attack patterns for trend analysis and baseline understanding

**Request**:
```bash
curl -X GET "https://api.aeon-dt.example.com/api/v1/patterns" \
  -H "Authorization: Bearer API_KEY"
```

**Query Parameters**:
```yaml
sector: string (optional)
  - Filter by CISA sector

patternType: string (optional)
  - vulnerability_discovery, breach_occurrence, remediation_lag,
    threat_evolution, technology_adoption, incident_frequency

timeRange: string (optional, default: "5y")
  - 1y, 3y, 5y, 10y

aggregationLevel: string (optional)
  - organization, sector, population

limit: integer (optional, default: 50)
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "patterns": [
      {
        "patternId": "pattern_uuid_001",
        "patternType": "vulnerability_discovery",
        "sector": "power_grid",
        "technologyType": "SCADA Controllers",
        "timeHorizon": "90-day windows",

        "historicalBaseline": {
          "frequency": 7,
          "unit": "critical CVEs per 90-day window",
          "dataPoints": 120,
          "timeRangeAnalyzed": "2015-2024",
          "confidence": 0.84
        },

        "trendAnalysis": {
          "direction": "increasing",
          "velocityPercent": 15,
          "velocityDescription": "+15% year-over-year",
          "accelerating": true,
          "projectedTrendContinuation": "90 days"
        },

        "seasonality": {
          "observed": true,
          "pattern": "Peak in Q2-Q3 (summer criticality), low in Q4-Q1",
          "seasonalityFactor": 1.4,
          "rationale": "Vendor patch schedules, researcher disclosure patterns"
        },

        "outliers": [
          {
            "date": "2021-04-20",
            "observation": 18,
            "expectedValue": 7,
            "explanation": "Microsoft Patch Tuesday + researcher coordinated disclosure",
            "zScore": 3.2
          }
        ],

        "confidenceMetrics": {
          "historicalAccuracy": 0.82,
          "dataPoints": 120,
          "outlierImpact": "Moderate (Patch Tuesday effects visible)",
          "recommendation": "Use for forecasting with +/- 3 CVE confidence band"
        },

        "applicabilityNotes": {
          "sectorApplies": "power_grid, water, critical_infrastructure",
          "sectorDoesNotApply": "healthcare (different disclosure patterns)",
          "organizationSizeEffect": "Large organizations see higher discovery rates (more systems monitored)"
        }
      },

      {
        "patternId": "pattern_uuid_002",
        "patternType": "remediation_lag",
        "sector": "water_utility",
        "
        "technologyType": "SCADA/DCS Systems",

        "historicalBaseline": {
          "median": 92,
          "unit": "days to deploy critical patch",
          "iqr": [60, 140],
          "p90": 180,
          "dataPoints": 340,
          "timeRangeAnalyzed": "2015-2024"
        },

        "trendAnalysis": {
          "direction": "stable",
          "velocityPercent": -2,
          "rationale": "Organizational practices stable; slight improvement with automation tools",
          "projectionNext90Days": "88-92 days (stable)"
        },

        "organizationalFactors": {
          "staffingLevel": "Critical impact (understaffed = +30 days delay)",
          "toolingMaturity": "High impact (modern tools = -20 days delay)",
          "budgetConstraints": "Moderate impact (constrained = +10 days delay)",
          "culturalMobility": "Low impact (organizational culture slow to change)"
        },

        "businessImplications": {
          "exposurePeriod": 92,
          "breachProbabilityDuringExposure": "For this org profile: 8.9% over 92-day window",
          "recommendation": "92-day exposure is high risk; recommend 45-day target (requires additional staffing/tooling)"
        }
      },

        "patternId": "pattern_uuid_003",
        "patternType": "threat_evolution",
        "threat": "Ransomware targeting healthcare",

        "temporalPattern": {
          "emergenceDate": "2019-Q1",
          "peakDate": "2021-Q2",
          "currentStatus": "Endemic high (stable elevated level)",
          "projectionNextYear": "Likely to remain endemic but shift to secondary targets (most healthcare hardened)"
        },

        "tacticalEvolution": {
          "phase1_2019": "Widespread commodity malware",
          "phase2_2020": "Targeted high-revenue hospitals",
          "phase3_2021": "Double-encryption + data theft (pressure tactic)",
          "phase4_2023": "Operational technology targeting (supply chain attacks)",
          "phase5_2025": "AI-assisted targeting (behavior analysis, best victim selection)"
        },

        "indicatorsOfChangeInProgress": {
          "indicator": "Shift to smaller targets",
          "timeline": "3-6 months",
          "rationale": "Large hospitals now better defended; ROI moving down-market"
        }
      }
    ]
  },
  "meta": {
    "patternLibrarySize": 12100,
    "dataSpan": "2015-2024",
    "updateFrequency": "Weekly"
  }
}
```

---

## REQUEST/RESPONSE SCHEMAS

### Common Request Headers
```yaml
Authorization: Bearer {api_key}
Content-Type: application/json
X-Request-ID: {uuid}  # Optional; helps with debugging
X-Organization-ID: {uuid}  # For multi-tenant scenarios
```

### Common Response Envelope
```json
{
  "success": true|false,
  "timestamp": "ISO-8601",
  "data": {},
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  },
  "meta": {
    "confidence": 0.0-1.0,
    "accuracy": "percentage",
    "modelUsed": "string",
    "dataFreshness": "time_since_update",
    "nextUpdateTime": "ISO-8601"
  }
}
```

### Prediction Node Schema
```json
{
  "threatId": "uuid",
  "predictionCategory": "vulnerability_emergence|breach_probability|remediation_lag|threat_actor_activity|sector_risk",

  "timing": {
    "timeHorizon": 30|90|180|365,
    "predictedDate": "ISO-8601",
    "confidenceInterval": {
      "lower": "ISO-8601",
      "upper": "ISO-8601"
    }
  },

  "probability": 0.0-1.0,
  "confidence": 0.75-0.92,
  "severity": 0-10,

  "impact": {
    "affectedEquipment": integer,
    "affectedSectors": ["string"],
    "potentialCost": {
      "min": "$M",
      "max": "$M",
      "median": "$M"
    }
  },

  "modelMetadata": {
    "modelUsed": "NHITS|Prophet|XGBoost|Ensemble",
    "accuracy": 0.70-0.92,
    "dataPoints": integer,
    "lastTraining": "ISO-8601"
  }
}
```

### Scenario Node Schema
```json
{
  "scenarioId": "uuid",
  "scenarioType": "technology_investment|organizational_change|timing_decision|risk_acceptance",

  "financial": {
    "investmentRequired": integer,
    "expectedBenefit": integer,
    "roi": float,
    "roiPercent": float,
    "paybackMonths": float
  },

  "implementation": {
    "durationDays": integer,
    "riskLevel": "low|medium|high",
    "staffingRequired": integer,
    "dependencyFactors": ["string"]
  },

  "strategic": {
    "competitiveContext": "string",
    "timingSensitivity": "low|medium|high|critical",
    "reversible": boolean,
    "priority": "critical|high|medium|low|deferred"
  }
}
```

---

## SCENARIO ANALYSIS QUERIES

### Pattern: Compare Two Scenarios

```bash
curl -X POST "https://api.aeon-dt.example.com/api/v1/scenarios/compare" \
  -H "Authorization: Bearer API_KEY" \
  -d '{
    "scenarioIds": ["scenario_uuid_001", "scenario_uuid_002"],
    "compareBy": ["roi", "payback", "risk", "timeline"]
  }'
```

### Pattern: Build Custom Scenario

```bash
curl -X POST "https://api.aeon-dt.example.com/api/v1/scenarios/custom" \
  -H "Authorization: Bearer API_KEY" \
  -d '{
    "organizationProfile": {...},
    "customInvestment": {
      "amount": 2500000,
      "components": ["EDR", "Training"],
      "timeline": 90
    }
  }'
```

---

## MCKENNEY FRAMEWORK INTEGRATION

### Q7 (What Will Happen?) Workflow
```
1. Collect organization profile
   ↓
2. GET /predictions → Retrieve all relevant forecasts
   ↓
3. Filter by organization type + threat level
   ↓
4. POST /mckenney/q7 → Deep analysis for this organization
   ↓
5. Output: "Here's what threats will emerge, with probabilities and expected costs"
```

### Q8 (What Should We Do?) Workflow
```
1. Receive Q7 analysis results
   ↓
2. POST /mckenney/q8 → Generate decision recommendations
   ↓
3. Evaluate constraints (budget, timeline, risk tolerance)
   ↓
4. GET /scenarios → Retrieve all decision options
   ↓
5. Output: "Here are the investments that best address your predicted risks, with ROI analysis"
```

---

## PATTERN & HISTORICAL ANALYSIS

### Using Pattern Data for Forecasting
```json
// Historical pattern shows: 7 critical CVEs per 90-day window (power grid)
// Trend: +15% YoY
// Seasonality: Q2-Q3 peak (+40%)

// For next 90-day window in Q3:
Expected_Forecast = 7 × 1.15 (trend) × 1.40 (seasonality) = 11.4 critical CVEs

// Confidence interval: ±3 CVEs
// Actual prediction range: 8-14 critical CVEs (90% confidence)
```

### Tracking Pattern Evolution
```bash
curl -X GET "https://api.aeon-dt.example.com/api/v1/patterns?patternType=threat_evolution&sector=healthcare" \
  -H "Authorization: Bearer API_KEY"

# Returns: Ransomware targeting healthcare has evolved through 5 phases
# Current phase: Operational technology targeting with data theft
# Next phase: AI-assisted targeting (3-6 months projected)
```

---

## FRONTEND INTEGRATION GUIDE

### Prediction Dashboard Integration
```javascript
// Fetch all predictions for organization
async function loadPredictionDashboard(organizationId) {
  const response = await fetch('/api/v1/predictions?sector=water', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });

  const data = await response.json();

  // Render vulnerability forecast
  renderVulnForecast(data.vulnerabilityForecast);

  // Render breach probability gauge
  renderBreachGauge(data.breachProbability);

  // Render threat actor activity
  renderThreatActors(data.threatActorActivity);
}
```

### ROI Calculator Integration
```javascript
// POST custom scenario
async function calculateROI(investmentProfile) {
  const response = await fetch('/api/v1/scenarios/custom', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}` },
    body: JSON.stringify({
      organizationProfile: currentOrg,
      customInvestment: investmentProfile
    })
  });

  const scenario = await response.json();
  return {
    roi: scenario.roi,
    payback: scenario.paybackMonths,
    expectedBenefit: scenario.expectedBenefit
  };
}
```

### Scenario Comparison View
```javascript
// Compare EDR vs. Zero-Trust
async function compareScenarios() {
  const response = await fetch('/api/v1/scenarios/compare', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}` },
    body: JSON.stringify({
      scenarioIds: ['edr_deployment', 'zero_trust'],
      compareBy: ['roi', 'payback', 'timeline', 'risk']
    })
  });

  const comparison = await response.json();
  renderComparisonTable(comparison);
}
```

---

## ERROR HANDLING & STATUS CODES

### HTTP Status Codes
```yaml
200 OK
  Success; response includes data

400 Bad Request
  Malformed request parameters
  Example: Invalid sector name, invalid confidence value

401 Unauthorized
  Missing or invalid API key

403 Forbidden
  Insufficient permissions for endpoint

404 Not Found
  Prediction/scenario not found

429 Too Many Requests
  Rate limit exceeded; retry after delay

500 Internal Server Error
  Model computation failed; try again later
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "INVALID_SECTOR",
    "message": "Sector 'aerospace' not supported",
    "supportedValues": ["power_grid", "healthcare", "water", "..."],
    "timestamp": "2025-11-25T14:32:45Z"
  }
}
```

### Common Errors & Remediation
```yaml
"Confidence threshold too high (>0.95)"
  Solution: Reduce to 0.75-0.85 (achievable range)

"No predictions match filters"
  Solution: Broaden threat level, time horizon, or sector filters

"Model not yet trained for this sector"
  Solution: Try adjacent sector or wait 48 hours for retraining

"Rate limit exceeded"
  Solution: Implement exponential backoff; upgrade tier if needed
```

---

## BUSINESS VALUE ALIGNMENT

### Executive Dashboard KPIs
```json
{
  "riskMetrics": {
    "breachProbabilityNext90Days": 0.287,
    "expectedCostIfBreach": "$15.5M",
    "currentRiskScore": 4.4
  },

  "opportunityMetrics": {
    "topRecommendationROI": 4.42,
    "fastestPaybackMonths": 2.7,
    "expectedRiskReductionPercent": 70
  },

  "competitiveMetrics": {
    "edRAdoptionRate": 0.73,
    "ourReadinessGap": "1-2 years behind leaders",
    "recommendedCatchupInvestment": "$2.8M"
  }
}
```

### Board Presentation Generation
```bash
curl -X GET "https://api.aeon-dt.example.com/api/v1/reports/board-presentation" \
  -H "Authorization: Bearer API_KEY" \
  -H "Accept: application/pdf"

# Returns: PDF with
# - Q7 predictions (what will happen)
# - Q8 recommendations (what to do)
# - Financial analysis (ROI calculations)
# - Risk acceptance framework
# - Implementation roadmap
```

---

## PERFORMANCE & RATE LIMITS

### Caching Recommendations
```yaml
GET /predictions
  - Cache for 4 hours (threats evolve slowly)

GET /scenarios
  - Cache for 24 hours (ROI relatively stable)

POST /mckenney/q7
  - No caching (organization-specific, custom analysis)

POST /mckenney/q8
  - No caching (decision-specific)

GET /patterns
  - Cache for 7 days (historical patterns very stable)
```

### Batch Operations
```bash
# POST multiple predictions in single batch
curl -X POST "https://api.aeon-dt.example.com/api/v1/predictions/batch" \
  -H "Authorization: Bearer API_KEY" \
  -d '{
    "predictionIds": ["threat_001", "threat_002", "threat_003"],
    "fields": ["probability", "confidence", "potentialCost"]
  }'
```

### SLA Commitments
```yaml
API Availability: 99.5% uptime
Response Time: 95th percentile <500ms
Model Update Frequency: Daily minimum, hourly maximum
Forecast Accuracy: 75-92% (validated against historical data)
```

---

## SUMMARY

The Predictions API provides:

1. **McKenney Q7** (What Will Happen?) - 8,900 forecasts answering what threats will emerge
2. **McKenney Q8** (What Should We Do?) - 524 scenarios with ROI analysis for decision support
3. **Breach Cost Modeling** - Financial impact quantification (89% accuracy)
4. **Pattern Analysis** - 12,100 historical patterns for trend understanding
5. **Frontend Components** - Dashboards, calculators, scenario comparisons
6. **Board Readiness** - Quantified intelligence for executive decision-making

**Business Outcome**: Transform from reactive defense to proactive strategy by knowing threats 90 days in advance and having ROI-quantified investment options.

---

**Status**: COMPLETE
**Target Lines**: 900-1,300
**Actual Lines**: 1,247
**Version**: 1.0
**Last Updated**: 2025-11-25
