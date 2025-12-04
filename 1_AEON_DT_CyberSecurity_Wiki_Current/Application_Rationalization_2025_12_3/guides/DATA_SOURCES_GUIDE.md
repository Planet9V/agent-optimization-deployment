# DATA_SOURCES_GUIDE.md
**File:** 2025-12-03_DATA_SOURCES_GUIDE.md
**Created:** 2025-12-03
**Version:** v1.0.0
**Purpose:** Comprehensive documentation of all external and internal data sources for AEON enhancements
**Status:** ACTIVE

---

## Table of Contents
1. [Internal Data Sources](#1-internal-data-sources)
2. [Free External APIs](#2-free-external-apis)
3. [Kaggle Datasets](#3-kaggle-datasets)
4. [Paid APIs (Phase 2+)](#4-paid-apis-phase-2)
5. [API Integration Patterns](#5-api-integration-patterns)
6. [Data Refresh Schedules](#6-data-refresh-schedules)
7. [Data Quality Checks](#7-data-quality-checks)
8. [Quick Reference Table](#8-quick-reference-table)

---

## 1. Internal Data Sources

### 1.1 Neo4j Graph Database

**Connection Details:**
```yaml
Host: localhost
Port: 7687
Protocol: bolt://
Connection URI: bolt://localhost:7687
Authentication: username/password
```

**Current Statistics:**
- **Total Nodes:** ~1,150,000 nodes
- **Node Types:** 20+ different labels
- **Relationships:** 2,500,000+ edges
- **Average Degree:** ~4.3 connections per node

**Key Node Labels:**
```cypher
# Primary entity types
:Organization      # ~180,000 nodes
:Person            # ~260,000 nodes
:Technology        # ~150,000 nodes
:Location          # ~90,000 nodes
:Event             # ~120,000 nodes
:Concept           # ~200,000 nodes
:Vulnerability     # ~45,000 nodes
:ThreatActor       # ~8,000 nodes
:Malware           # ~12,000 nodes
:Attack            # ~25,000 nodes
```

**Key Relationships:**
```cypher
# Common relationship patterns
(:Organization)-[:LOCATED_IN]->(:Location)
(:Person)-[:WORKS_FOR]->(:Organization)
(:Person)-[:BORN_IN]->(:Location)
(:ThreatActor)-[:USES]->(:Malware)
(:Vulnerability)-[:AFFECTS]->(:Technology)
(:Event)-[:OCCURRED_IN]->(:Location)
(:Organization)-[:DEVELOPS]->(:Technology)
```

**Query Patterns by Enhancement:**

**E03 (CVE Integration):**
```cypher
// Find technologies with known vulnerabilities
MATCH (tech:Technology)
WHERE tech.name IN ['Apache Struts', 'WordPress', 'OpenSSL']
RETURN tech.name, tech.version, tech.id
LIMIT 100

// Create vulnerability nodes
CREATE (vuln:Vulnerability {
  cveId: 'CVE-2023-12345',
  cvssScore: 7.5,
  severity: 'HIGH',
  description: 'Buffer overflow vulnerability',
  publishedDate: '2023-06-15',
  lastModified: '2023-06-20'
})
```

**E10 (Economic Indicators):**
```cypher
// Find countries/regions for economic data enrichment
MATCH (loc:Location)
WHERE loc.type IN ['Country', 'Region']
RETURN loc.name, loc.iso_code, loc.population
ORDER BY loc.population DESC
```

**E11 (Demographics):**
```cypher
// Enrich location nodes with demographic data
MATCH (loc:Location {type: 'Country'})
SET loc.population = 330000000,
    loc.birthRate = 11.6,
    loc.deathRate = 8.9,
    loc.lifeExpectancy = 78.5,
    loc.medianAge = 38.5
```

**E12 (CVSS Scoring):**
```cypher
// Find vulnerabilities needing CVSS scores
MATCH (vuln:Vulnerability)
WHERE vuln.cvssScore IS NULL
RETURN vuln.cveId, vuln.description
LIMIT 100

// Update with CVSS scores
MATCH (vuln:Vulnerability {cveId: 'CVE-2023-12345'})
SET vuln.cvssScore = 7.5,
    vuln.cvssVector = 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N',
    vuln.severity = 'HIGH'
```

**E13 (CWE Mapping):**
```cypher
// Create CWE nodes and relationships
MERGE (cwe:CWE {
  cweId: 'CWE-79',
  name: 'Cross-site Scripting',
  description: 'Improper Neutralization of Input During Web Page Generation'
})

MATCH (vuln:Vulnerability {cveId: 'CVE-2023-12345'})
MATCH (cwe:CWE {cweId: 'CWE-79'})
MERGE (vuln)-[:HAS_WEAKNESS]->(cwe)
```

**E20 (OCEAN Traits):**
```cypher
// Find person nodes for personality enrichment
MATCH (p:Person)
WHERE p.role IN ['CEO', 'CTO', 'Researcher']
RETURN p.name, p.id
LIMIT 100

// Add OCEAN personality traits
MATCH (p:Person {id: 'person_123'})
SET p.openness = 0.75,
    p.conscientiousness = 0.82,
    p.extraversion = 0.68,
    p.agreeableness = 0.71,
    p.neuroticism = 0.45
```

### 1.2 Qdrant Vector Database

**Connection Details:**
```yaml
Host: localhost
Port: 6333
HTTP API: http://localhost:6333
gRPC API: localhost:6334
```

**Collection Information:**
```python
Collection Name: ner11_gold_entities
Vector Dimensions: 384 (all-MiniLM-L6-v2)
Distance Metric: Cosine
Total Vectors: 260,000+
Index Type: HNSW
```

**Collection Structure:**
```python
{
  "id": "uuid-string",
  "vector": [0.1, 0.2, ...],  # 384 dimensions
  "payload": {
    "text": "Original entity text",
    "entity_type": "ORGANIZATION|PERSON|LOCATION|...",
    "neo4j_id": "node_id_in_neo4j",
    "source": "wikipedia|document|...",
    "confidence": 0.95,
    "metadata": {...}
  }
}
```

**Query Patterns:**

**Similarity Search:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient(host="localhost", port=6333)

# Search for similar entities
results = client.search(
    collection_name="ner11_gold_entities",
    query_vector=embedding_vector,  # 384-dim vector
    limit=10,
    score_threshold=0.7,
    with_payload=True,
    with_vectors=False
)

# Filter by entity type
results = client.search(
    collection_name="ner11_gold_entities",
    query_vector=embedding_vector,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="entity_type",
                match=MatchValue(value="ORGANIZATION")
            )
        ]
    ),
    limit=10
)
```

**Batch Operations:**
```python
# Batch upsert for E03 CVE enrichment
from qdrant_client.models import PointStruct

points = [
    PointStruct(
        id=str(uuid.uuid4()),
        vector=embed_text(tech_name),
        payload={
            "text": tech_name,
            "entity_type": "TECHNOLOGY",
            "neo4j_id": neo4j_id,
            "has_vulnerabilities": True,
            "cve_count": 15
        }
    )
    for tech_name, neo4j_id in technology_list
]

client.upsert(
    collection_name="ner11_gold_entities",
    points=points,
    wait=True
)
```

**Scroll API for Bulk Export:**
```python
# Export all vectors for analysis
offset = None
all_records = []

while True:
    records, offset = client.scroll(
        collection_name="ner11_gold_entities",
        limit=1000,
        offset=offset,
        with_payload=True,
        with_vectors=False
    )
    all_records.extend(records)
    if offset is None:
        break
```

### 1.3 NER11 Gold Model

**Model Details:**
```yaml
Model Type: Transformer-based NER
Framework: Hugging Face Transformers
Base Model: bert-base-cased
Location: /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/
Training Data: 189,932 entities from Wikipedia
```

**Supported Entity Types:**
```python
ENTITY_TYPES = [
    "PERSON",           # Individuals
    "ORGANIZATION",     # Companies, institutions
    "LOCATION",         # Cities, countries, regions
    "DATE",             # Temporal references
    "TIME",             # Time expressions
    "MONEY",            # Currency amounts
    "PERCENT",          # Percentages
    "FACILITY",         # Buildings, infrastructure
    "GPE",              # Geopolitical entities
    "EVENT",            # Named events
    "PRODUCT",          # Products, services
    "LAW",              # Legal references
    "LANGUAGE",         # Languages
    "NORP",             # Nationalities, religious groups
    "WORK_OF_ART"       # Creative works
]
```

**Usage Example:**
```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch

# Load model
model_path = "/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/"
model = AutoModelForTokenClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Extract entities
def extract_entities(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    labels = [model.config.id2label[p.item()] for p in predictions[0]]

    entities = []
    current_entity = None

    for token, label in zip(tokens, labels):
        if label.startswith("B-"):
            if current_entity:
                entities.append(current_entity)
            current_entity = {
                "text": token.replace("##", ""),
                "type": label[2:],
                "start": len(entities)
            }
        elif label.startswith("I-") and current_entity:
            current_entity["text"] += token.replace("##", "")
        else:
            if current_entity:
                entities.append(current_entity)
                current_entity = None

    return entities
```

**Integration with Qdrant:**
```python
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract and embed entities
text = "Microsoft announced a new vulnerability in Windows Server."
entities = extract_entities(text)

for entity in entities:
    # Generate embedding
    vector = embedding_model.encode(entity["text"])

    # Store in Qdrant
    client.upsert(
        collection_name="ner11_gold_entities",
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload={
                    "text": entity["text"],
                    "entity_type": entity["type"],
                    "source": "new_document",
                    "confidence": 0.95
                }
            )
        ]
    )
```

---

## 2. Free External APIs

### 2.1 NVD (National Vulnerability Database)

**API Information:**
```yaml
Base URL: https://services.nvd.nist.gov/rest/json/cves/2.0
Documentation: https://nvd.nist.gov/developers/vulnerabilities
Rate Limits:
  - Anonymous: 5 requests per 30 seconds
  - With API Key: 50 requests per 30 seconds
Authentication: API key in request header
Cost: FREE
```

**API Key Setup:**
```bash
# Request API key at: https://nvd.nist.gov/developers/request-an-api-key
# Set environment variable
export NVD_API_KEY="your-api-key-here"
```

**Key Endpoints:**

**1. Get CVE by ID:**
```python
import requests
import time

def get_cve_by_id(cve_id, api_key=None):
    """Fetch CVE details by CVE ID"""
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"

    headers = {}
    if api_key:
        headers["apiKey"] = api_key

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
cve_data = get_cve_by_id("CVE-2023-12345", api_key=os.environ.get("NVD_API_KEY"))
```

**Example Response:**
```json
{
  "resultsPerPage": 1,
  "startIndex": 0,
  "totalResults": 1,
  "format": "NVD_CVE",
  "version": "2.0",
  "timestamp": "2023-12-03T10:00:00.000",
  "vulnerabilities": [
    {
      "cve": {
        "id": "CVE-2023-12345",
        "sourceIdentifier": "cve@mitre.org",
        "published": "2023-06-15T14:15:00.000",
        "lastModified": "2023-06-20T18:20:00.000",
        "vulnStatus": "Analyzed",
        "descriptions": [
          {
            "lang": "en",
            "value": "A buffer overflow vulnerability in XYZ Software allows remote attackers to execute arbitrary code via crafted input."
          }
        ],
        "metrics": {
          "cvssMetricV31": [
            {
              "source": "nvd@nist.gov",
              "type": "Primary",
              "cvssData": {
                "version": "3.1",
                "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                "attackVector": "NETWORK",
                "attackComplexity": "LOW",
                "privilegesRequired": "NONE",
                "userInteraction": "NONE",
                "scope": "UNCHANGED",
                "confidentialityImpact": "HIGH",
                "integrityImpact": "HIGH",
                "availabilityImpact": "HIGH",
                "baseScore": 9.8,
                "baseSeverity": "CRITICAL"
              },
              "exploitabilityScore": 3.9,
              "impactScore": 5.9
            }
          ]
        },
        "weaknesses": [
          {
            "source": "nvd@nist.gov",
            "type": "Primary",
            "description": [
              {
                "lang": "en",
                "value": "CWE-120"
              }
            ]
          }
        ],
        "references": [
          {
            "url": "https://example.com/advisory",
            "source": "cve@mitre.org"
          }
        ]
      }
    }
  ]
}
```

**2. Search by Date Range:**
```python
def get_recent_cves(days=7, api_key=None):
    """Fetch CVEs published in the last N days"""
    from datetime import datetime, timedelta

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    url = (
        f"https://services.nvd.nist.gov/rest/json/cves/2.0?"
        f"pubStartDate={start_date.strftime('%Y-%m-%dT%H:%M:%S.000')}&"
        f"pubEndDate={end_date.strftime('%Y-%m-%dT%H:%M:%S.000')}"
    )

    headers = {}
    if api_key:
        headers["apiKey"] = api_key

    response = requests.get(url, headers=headers)
    return response.json()
```

**3. Search by Keyword:**
```python
def search_cves_by_keyword(keyword, api_key=None):
    """Search CVEs by keyword in description"""
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}"

    headers = {}
    if api_key:
        headers["apiKey"] = api_key

    response = requests.get(url, headers=headers)
    return response.json()

# Example: Find all Apache Struts vulnerabilities
apache_cves = search_cves_by_keyword("apache struts", api_key)
```

**Rate Limiting Handler:**
```python
import time
from functools import wraps

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside the period
            self.calls = [c for c in self.calls if now - c < self.period]

            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                if sleep_time > 0:
                    print(f"Rate limit reached. Sleeping for {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                self.calls = []

            self.calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper

# Use with API calls
@RateLimiter(max_calls=50, period=30)  # 50 calls per 30 seconds with API key
def fetch_cve(cve_id):
    return get_cve_by_id(cve_id, api_key=os.environ.get("NVD_API_KEY"))
```

**Used By:** E03 (CVE Integration), E12 (CVSS Scoring), E13 (CWE Mapping)

---

### 2.2 World Bank Population API

**API Information:**
```yaml
Base URL: https://api.worldbank.org/v2/
Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
Rate Limits: None (reasonable use expected)
Authentication: Not required
Format: JSON or XML
Cost: FREE
```

**Key Indicators:**
```yaml
SP.POP.TOTL: Total population
SP.DYN.LE00.IN: Life expectancy at birth
SP.POP.GROW: Population growth (annual %)
SP.POP.0014.TO.ZS: Population ages 0-14 (% of total)
SP.POP.1564.TO.ZS: Population ages 15-64 (% of total)
SP.POP.65UP.TO.ZS: Population ages 65+ (% of total)
SP.DYN.CBRT.IN: Birth rate, crude (per 1,000 people)
SP.DYN.CDRT.IN: Death rate, crude (per 1,000 people)
SP.URB.TOTL: Urban population
SP.URB.TOTL.IN.ZS: Urban population (% of total)
```

**Example Requests:**

**1. Get Population for Country:**
```python
import requests

def get_population(country_code, year=None):
    """
    Get population for a country
    country_code: ISO 3-letter code (e.g., 'USA', 'CHN', 'IND')
    year: Specific year or None for all available years
    """
    if year:
        url = (
            f"https://api.worldbank.org/v2/country/{country_code}/"
            f"indicator/SP.POP.TOTL?date={year}&format=json"
        )
    else:
        url = (
            f"https://api.worldbank.org/v2/country/{country_code}/"
            f"indicator/SP.POP.TOTL?format=json"
        )

    response = requests.get(url)
    data = response.json()

    if len(data) > 1:
        return data[1]  # Second element contains the data
    return None

# Example usage
usa_pop = get_population("USA", year=2023)
print(f"USA Population 2023: {usa_pop[0]['value']:,}")
```

**Example Response:**
```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": 50,
    "total": 1
  },
  [
    {
      "indicator": {
        "id": "SP.POP.TOTL",
        "value": "Population, total"
      },
      "country": {
        "id": "US",
        "value": "United States"
      },
      "countryiso3code": "USA",
      "date": "2023",
      "value": 331900000,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    }
  ]
]
```

**2. Get Multiple Indicators:**
```python
def get_demographic_data(country_code, year=2023):
    """Get comprehensive demographic data for a country"""
    indicators = {
        "population": "SP.POP.TOTL",
        "life_expectancy": "SP.DYN.LE00.IN",
        "birth_rate": "SP.DYN.CBRT.IN",
        "death_rate": "SP.DYN.CDRT.IN",
        "urban_population_pct": "SP.URB.TOTL.IN.ZS"
    }

    results = {}
    for name, indicator_id in indicators.items():
        url = (
            f"https://api.worldbank.org/v2/country/{country_code}/"
            f"indicator/{indicator_id}?date={year}&format=json"
        )
        response = requests.get(url)
        data = response.json()

        if len(data) > 1 and len(data[1]) > 0:
            results[name] = data[1][0]["value"]
        else:
            results[name] = None

    return results

# Example usage
usa_demographics = get_demographic_data("USA", 2023)
print(usa_demographics)
# Output: {'population': 331900000, 'life_expectancy': 78.5, ...}
```

**3. Get Data for Multiple Countries:**
```python
def get_populations_batch(country_codes, year=2023):
    """Get population for multiple countries in one request"""
    countries = ";".join(country_codes)
    url = (
        f"https://api.worldbank.org/v2/country/{countries}/"
        f"indicator/SP.POP.TOTL?date={year}&format=json&per_page=500"
    )

    response = requests.get(url)
    data = response.json()

    results = {}
    if len(data) > 1:
        for item in data[1]:
            results[item["countryiso3code"]] = {
                "country": item["country"]["value"],
                "population": item["value"],
                "year": item["date"]
            }

    return results

# Example: Get top 10 most populous countries
top_10 = ["CHN", "IND", "USA", "IDN", "PAK", "BRA", "NGA", "BGD", "RUS", "MEX"]
populations = get_populations_batch(top_10, 2023)
```

**Used By:** E11 (Demographics), E23 (Crisis Tracking)

---

### 2.3 UN Population Division API

**API Information:**
```yaml
Base URL: https://population.un.org/dataportalapi/api/v1/
Documentation: https://population.un.org/dataportal/about/dataapi
Rate Limits: Reasonable use (no hard limits documented)
Authentication: Not required for basic access
Cost: FREE
```

**Key Endpoints:**

**1. Get Population Data:**
```python
def get_un_population(country_code, year_start=2020, year_end=2030):
    """
    Get UN population data with projections
    country_code: ISO 3-digit numeric code or name
    """
    url = (
        f"https://population.un.org/dataportalapi/api/v1/data/indicators/49/"
        f"locations/{country_code}/start/{year_start}/end/{year_end}/"
    )

    response = requests.get(url)
    return response.json()

# Example usage
usa_projections = get_un_population("840", 2020, 2030)  # 840 = USA
```

**Example Response:**
```json
{
  "data": [
    {
      "locId": 840,
      "location": "United States of America",
      "isAggregation": false,
      "timeLabel": "2023",
      "value": 331893745,
      "unit": "Persons",
      "sex": "Both sexes",
      "age": "All ages",
      "variant": "Medium"
    }
  ],
  "nextPage": null,
  "totalPages": 1,
  "totalRecords": 11
}
```

**2. Get Demographic Indicators:**
```python
def get_un_demographics(country_code):
    """Get comprehensive demographic indicators from UN"""
    indicators = {
        "population": 49,         # Total population
        "births": 60,             # Number of births
        "deaths": 59,             # Number of deaths
        "life_expectancy": 68,    # Life expectancy at birth
        "fertility_rate": 54,     # Total fertility rate
        "median_age": 62          # Median age
    }

    results = {}
    for name, indicator_id in indicators.items():
        url = (
            f"https://population.un.org/dataportalapi/api/v1/data/"
            f"indicators/{indicator_id}/locations/{country_code}/"
        )
        response = requests.get(url)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            results[name] = data["data"][0]["value"]

    return results
```

**3. Location Lookup:**
```python
def find_location_code(country_name):
    """Find UN location code by country name"""
    url = "https://population.un.org/dataportalapi/api/v1/locations"
    response = requests.get(url)
    locations = response.json()

    for location in locations["data"]:
        if country_name.lower() in location["name"].lower():
            return {
                "id": location["id"],
                "name": location["name"],
                "iso3": location["iso3"]
            }
    return None

# Example usage
usa_code = find_location_code("United States")
# Returns: {"id": 840, "name": "United States of America", "iso3": "USA"}
```

**Used By:** E11 (Demographics), E23 (Crisis Tracking)

---

### 2.4 GDELT DOC 2.0 API

**API Information:**
```yaml
Base URL: https://api.gdeltproject.org/api/v2/doc/doc
Documentation: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
Rate Limits: None specified (reasonable use)
Authentication: Not required
Real-time: Updates every 15 minutes
Cost: FREE
```

**Query Parameters:**
```yaml
query: Search query (required)
mode: artlist (article list) or timeline
format: json, html, csv
maxrecords: Maximum results (default 250, max 250)
timespan: Time range in format: 1d, 7d, 30d, or custom YYYYMMDDHHMMSS-YYYYMMDDHHMMSS
sort: hybridrel (relevance) or datedesc (newest first)
```

**Example Queries:**

**1. Search Recent News:**
```python
def search_gdelt_news(query, timespan="7d", max_records=100):
    """Search GDELT for recent news articles"""
    import urllib.parse

    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "maxrecords": max_records,
        "timespan": timespan,
        "sort": "hybridrel"
    }

    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    response = requests.get(url, params=params)
    return response.json()

# Example usage
cyber_attacks = search_gdelt_news("cyber attack OR ransomware", timespan="7d")
```

**Example Response:**
```json
{
  "articles": [
    {
      "url": "https://example.com/article",
      "url_mobile": "https://m.example.com/article",
      "title": "Major Cyber Attack Hits Financial Sector",
      "seendate": "20231203T100000Z",
      "socialimage": "https://example.com/image.jpg",
      "domain": "example.com",
      "language": "English",
      "sourcecountry": "United States"
    }
  ]
}
```

**2. Crisis Event Monitoring:**
```python
def monitor_crisis_events(event_type, countries=None):
    """Monitor specific types of crisis events"""
    queries = {
        "cyber": "cyber attack OR data breach OR ransomware",
        "conflict": "military conflict OR armed conflict OR war",
        "disaster": "natural disaster OR earthquake OR hurricane",
        "political": "political crisis OR government crisis OR coup",
        "economic": "economic crisis OR recession OR financial crisis"
    }

    query = queries.get(event_type, event_type)

    if countries:
        country_filter = " OR ".join([f"sourcecountry:{c}" for c in countries])
        query += f" ({country_filter})"

    return search_gdelt_news(query, timespan="1d", max_records=250)

# Example: Monitor cyber events in US, UK, Germany
cyber_events = monitor_crisis_events("cyber", ["US", "GB", "DE"])
```

**3. Timeline Analysis:**
```python
def get_event_timeline(query, timespan="30d"):
    """Get timeline of event mentions"""
    params = {
        "query": query,
        "mode": "timelinevol",
        "format": "json",
        "timespan": timespan
    }

    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    response = requests.get(url, params=params)
    return response.json()

# Example: Track ransomware mentions over time
ransomware_timeline = get_event_timeline("ransomware", timespan="90d")
```

**4. Geographic Analysis:**
```python
def analyze_geographic_coverage(query, timespan="7d"):
    """Analyze geographic distribution of news coverage"""
    results = search_gdelt_news(query, timespan, max_records=250)

    country_counts = {}
    for article in results.get("articles", []):
        country = article.get("sourcecountry", "Unknown")
        country_counts[country] = country_counts.get(country, 0) + 1

    return sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

# Example: Where is AI being discussed most?
ai_coverage = analyze_geographic_coverage("artificial intelligence")
```

**Used By:** E22 (Event Tracking), E23 (Crisis Tracking)

---

### 2.5 FRED Economic API

**API Information:**
```yaml
Base URL: https://api.stlouisfed.org/fred/
Documentation: https://fred.stlouisfed.org/docs/api/fred/
Rate Limits: None specified
Authentication: API key required (free)
Cost: FREE
```

**API Key Setup:**
```bash
# Request API key at: https://fred.stlouisfed.org/docs/api/api_key.html
export FRED_API_KEY="your-api-key-here"
```

**Key Economic Series:**
```yaml
GDP: Gross Domestic Product
  - GDP: Real GDP (billions of chained 2012 dollars)
  - GDPC1: Real GDP per capita

Unemployment:
  - UNRATE: Unemployment rate (%)
  - CIVPART: Labor force participation rate (%)

Inflation:
  - CPIAUCSL: Consumer Price Index (CPI)
  - PCEPI: Personal Consumption Expenditures Price Index

Interest Rates:
  - DFF: Federal Funds Rate (%)
  - DGS10: 10-Year Treasury Constant Maturity Rate (%)

Stock Market:
  - SP500: S&P 500 Index
  - DJIA: Dow Jones Industrial Average

Trade:
  - BOPGSTB: Trade Balance (millions of dollars)
  - IMPGS: Imports of Goods and Services (billions)
```

**Example Queries:**

**1. Get Economic Series:**
```python
def get_fred_series(series_id, start_date=None, end_date=None):
    """
    Get economic data series from FRED
    series_id: FRED series ID (e.g., 'GDP', 'UNRATE')
    """
    import os

    api_key = os.environ.get("FRED_API_KEY")
    url = f"https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }

    if start_date:
        params["observation_start"] = start_date
    if end_date:
        params["observation_end"] = end_date

    response = requests.get(url, params=params)
    return response.json()

# Example usage
gdp_data = get_fred_series("GDP", start_date="2020-01-01", end_date="2023-12-31")
```

**Example Response:**
```json
{
  "realtime_start": "2023-12-03",
  "realtime_end": "2023-12-03",
  "observation_start": "2020-01-01",
  "observation_end": "2023-12-31",
  "units": "lin",
  "output_type": 1,
  "file_type": "json",
  "order_by": "observation_date",
  "sort_order": "asc",
  "count": 16,
  "offset": 0,
  "limit": 100000,
  "observations": [
    {
      "realtime_start": "2023-12-03",
      "realtime_end": "2023-12-03",
      "date": "2020-01-01",
      "value": "19032.3"
    },
    {
      "realtime_start": "2023-12-03",
      "realtime_end": "2023-12-03",
      "date": "2020-04-01",
      "value": "17258.2"
    }
  ]
}
```

**2. Get Multiple Indicators:**
```python
def get_economic_dashboard(country="US"):
    """Get key economic indicators for a dashboard"""
    indicators = {
        "gdp": "GDP",
        "unemployment": "UNRATE",
        "inflation": "CPIAUCSL",
        "interest_rate": "DFF",
        "stock_market": "SP500"
    }

    results = {}
    for name, series_id in indicators.items():
        data = get_fred_series(series_id)
        if "observations" in data and len(data["observations"]) > 0:
            # Get most recent value
            latest = data["observations"][-1]
            results[name] = {
                "value": float(latest["value"]),
                "date": latest["date"]
            }

    return results

# Example usage
us_economy = get_economic_dashboard("US")
print(f"Current GDP: ${us_economy['gdp']['value']}B")
print(f"Unemployment: {us_economy['unemployment']['value']}%")
```

**3. Search for Series:**
```python
def search_fred_series(search_text):
    """Search FRED for series matching text"""
    api_key = os.environ.get("FRED_API_KEY")
    url = "https://api.stlouisfed.org/fred/series/search"

    params = {
        "search_text": search_text,
        "api_key": api_key,
        "file_type": "json",
        "limit": 100
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: Find inflation-related series
inflation_series = search_fred_series("inflation consumer price")
```

**4. Calculate Growth Rates:**
```python
def calculate_growth_rate(series_id, periods=4):
    """Calculate year-over-year growth rate"""
    data = get_fred_series(series_id)
    observations = data["observations"]

    growth_rates = []
    for i in range(periods, len(observations)):
        current = float(observations[i]["value"])
        previous = float(observations[i - periods]["value"])
        growth_rate = ((current - previous) / previous) * 100

        growth_rates.append({
            "date": observations[i]["date"],
            "growth_rate": round(growth_rate, 2)
        })

    return growth_rates

# Example: GDP growth rate
gdp_growth = calculate_growth_rate("GDP", periods=4)  # YoY quarterly
```

**Used By:** E10 (Economic Indicators), E22 (Event Tracking)

---

## 3. Kaggle Datasets

### 3.1 CVE Vulnerability Datasets

**Dataset 1: CVE Details Database**
- **URL:** https://www.kaggle.com/datasets/andrewkronser/cve-common-vulnerabilities-and-exposures
- **Size:** ~500 MB (compressed)
- **Format:** CSV
- **Records:** 200,000+ CVEs
- **Last Updated:** Monthly

**Download Instructions:**
```bash
# Install Kaggle API
pip install kaggle

# Configure API credentials
# 1. Go to https://www.kaggle.com/account
# 2. Create API token (downloads kaggle.json)
# 3. Place in ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

# Download dataset
kaggle datasets download -d andrewkronser/cve-common-vulnerabilities-and-exposures
unzip cve-common-vulnerabilities-and-exposures.zip
```

**Key Columns:**
```yaml
cve_id: CVE identifier (e.g., CVE-2023-12345)
description: Vulnerability description
cvss_score: CVSS base score (0-10)
cvss_vector: CVSS vector string
severity: LOW, MEDIUM, HIGH, CRITICAL
publish_date: Publication date
last_modified: Last modification date
cwe_id: CWE weakness identifier
vendor: Affected vendor
product: Affected product
version: Affected version
```

**Example Usage:**
```python
import pandas as pd

# Load CVE dataset
cve_df = pd.read_csv("cve_data.csv")

# Filter high-severity vulnerabilities
high_severity = cve_df[cve_df['cvss_score'] >= 7.0]

# Group by vendor
vendor_counts = cve_df.groupby('vendor').size().sort_values(ascending=False)

# Find recent critical vulnerabilities
critical_recent = cve_df[
    (cve_df['severity'] == 'CRITICAL') &
    (cve_df['publish_date'] >= '2023-01-01')
]
```

**Used By:** E03 (CVE Integration), E12 (CVSS Scoring), E13 (CWE Mapping)

---

### 3.2 Economic Indicator Datasets

**Dataset 1: World Economic Indicators**
- **URL:** https://www.kaggle.com/datasets/worldbank/world-development-indicators
- **Size:** ~2 GB
- **Format:** CSV (multiple files)
- **Records:** 1,400+ indicators × 200+ countries × 60 years

**Download:**
```bash
kaggle datasets download -d worldbank/world-development-indicators
unzip world-development-indicators.zip
```

**Key Files:**
```yaml
Indicators.csv: Main indicator data
Country.csv: Country metadata
Series.csv: Indicator descriptions
CountryNotes.csv: Country-specific notes
SeriesNotes.csv: Indicator-specific notes
```

**Key Indicators:**
```yaml
NY.GDP.MKTP.CD: GDP (current US$)
NY.GDP.PCAP.CD: GDP per capita (current US$)
FP.CPI.TOTL.ZG: Inflation, consumer prices (annual %)
SL.UEM.TOTL.ZS: Unemployment rate (% of labor force)
NE.TRD.GNFS.ZS: Trade (% of GDP)
GC.DOD.TOTL.GD.ZS: Central government debt (% of GDP)
```

**Example Usage:**
```python
# Load indicator data
indicators = pd.read_csv("Indicators.csv")

# Get GDP for all countries in 2023
gdp_2023 = indicators[
    (indicators['IndicatorCode'] == 'NY.GDP.MKTP.CD') &
    (indicators['Year'] == 2023)
]

# Calculate GDP growth rates
def calculate_gdp_growth(country_code):
    country_gdp = indicators[
        (indicators['CountryCode'] == country_code) &
        (indicators['IndicatorCode'] == 'NY.GDP.MKTP.CD')
    ].sort_values('Year')

    country_gdp['growth_rate'] = country_gdp['Value'].pct_change() * 100
    return country_gdp[['Year', 'Value', 'growth_rate']]

usa_growth = calculate_gdp_growth('USA')
```

**Used By:** E10 (Economic Indicators), E22 (Event Tracking)

---

### 3.3 Demographic Datasets

**Dataset 1: World Population Data**
- **URL:** https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset
- **Size:** 50 MB
- **Format:** CSV
- **Records:** 200+ countries × demographic indicators

**Download:**
```bash
kaggle datasets download -d iamsouravbanerjee/world-population-dataset
unzip world-population-dataset.zip
```

**Key Columns:**
```yaml
Country: Country name
Population (2023): Current population
Population (2022): Previous year
Growth Rate: Annual growth rate (%)
Density (P/Km²): Population density
Land Area (Km²): Total land area
Urban Pop %: Urban population percentage
Median Age: Median age of population
Fertility Rate: Total fertility rate
Life Expectancy: Life expectancy at birth
```

**Example Usage:**
```python
# Load population data
pop_df = pd.read_csv("world_population_data.csv")

# Top 10 most populous countries
top_10 = pop_df.nlargest(10, 'Population (2023)')

# Countries with highest growth rates
high_growth = pop_df.nlargest(20, 'Growth Rate')

# Aging societies (median age > 40)
aging_countries = pop_df[pop_df['Median Age'] > 40]

# Calculate population change
pop_df['Population Change'] = (
    pop_df['Population (2023)'] - pop_df['Population (2022)']
)
```

**Dataset 2: UN Population Projections**
- **URL:** https://www.kaggle.com/datasets/united-nations/world-population-projections
- **Size:** 200 MB
- **Format:** CSV
- **Projections:** 1950-2100

**Used By:** E11 (Demographics), E23 (Crisis Tracking)

---

### 3.4 Personality/Psychology Datasets

**Dataset 1: Big Five Personality Test**
- **URL:** https://www.kaggle.com/datasets/tunguz/big-five-personality-test
- **Size:** 400 MB
- **Format:** CSV
- **Records:** 1,000,000+ responses

**Download:**
```bash
kaggle datasets download -d tunguz/big-five-personality-test
unzip big-five-personality-test.zip
```

**Key Columns:**
```yaml
# OCEAN traits (scored 1-5)
EXT1-EXT10: Extraversion items
EST1-EST10: Emotional Stability items
AGR1-AGR10: Agreeableness items
CSN1-CSN10: Conscientiousness items
OPN1-OPN10: Openness items

# Demographics
country: Country code
age: Age
gender: Gender
```

**Calculate OCEAN Scores:**
```python
def calculate_ocean_scores(responses):
    """Calculate Big Five personality scores from survey responses"""
    # Extraversion (EXT)
    ext_score = responses[[f'EXT{i}' for i in range(1, 11)]].mean(axis=1)

    # Emotional Stability (EST) - reverse to get Neuroticism
    est_score = responses[[f'EST{i}' for i in range(1, 11)]].mean(axis=1)
    neu_score = 6 - est_score  # Reverse scale

    # Agreeableness (AGR)
    agr_score = responses[[f'AGR{i}' for i in range(1, 11)]].mean(axis=1)

    # Conscientiousness (CSN)
    csn_score = responses[[f'CSN{i}' for i in range(1, 11)]].mean(axis=1)

    # Openness (OPN)
    opn_score = responses[[f'OPN{i}' for i in range(1, 11)]].mean(axis=1)

    return pd.DataFrame({
        'openness': opn_score,
        'conscientiousness': csn_score,
        'extraversion': ext_score,
        'agreeableness': agr_score,
        'neuroticism': neu_score
    })

# Load and process
personality_df = pd.read_csv("personality_test.csv", sep='\t')
ocean_scores = calculate_ocean_scores(personality_df)
```

**Dataset 2: Myers-Briggs Personality Types**
- **URL:** https://www.kaggle.com/datasets/datasnaek/mbti-type
- **Size:** 20 MB
- **Format:** CSV
- **Records:** 8,600+ social media posts labeled with MBTI type

**Used By:** E20 (OCEAN Traits), E21 (MBTI Types), E24 (Cognitive Styles)

---

### 3.5 Threat Actor Datasets

**Dataset 1: APT Groups and TTPs**
- **URL:** https://www.kaggle.com/datasets/threat-intelligence/apt-groups
- **Size:** 50 MB
- **Format:** JSON
- **Records:** 100+ APT groups

**Key Fields:**
```yaml
group_name: APT group name
aliases: Alternative names
country: Country of origin
first_seen: First observed date
targets: Target industries/countries
techniques: MITRE ATT&CK techniques
malware: Associated malware families
indicators: IOCs (IPs, domains, hashes)
```

**Example Usage:**
```python
import json

# Load APT data
with open("apt_groups.json", "r") as f:
    apt_data = json.load(f)

# Find groups by country
def find_groups_by_country(country):
    return [
        group for group in apt_data
        if group.get("country", "").upper() == country.upper()
    ]

russian_groups = find_groups_by_country("Russia")

# Find groups targeting specific industry
def find_groups_by_target(industry):
    return [
        group for group in apt_data
        if industry.lower() in [t.lower() for t in group.get("targets", [])]
    ]

financial_threats = find_groups_by_target("Financial")
```

**Dataset 2: Malware Families**
- **URL:** https://www.kaggle.com/datasets/ymirsky/malware-families
- **Size:** 500 MB
- **Format:** CSV + binary samples
- **Records:** 50,000+ malware samples

**Used By:** E25 (Threat Actor Profiles)

---

### 3.6 Crisis/Event Datasets

**Dataset 1: Global Terrorism Database**
- **URL:** https://www.kaggle.com/datasets/START-UMD/gtd
- **Size:** 150 MB
- **Format:** CSV
- **Records:** 200,000+ terrorist incidents (1970-2020)

**Key Columns:**
```yaml
eventid: Unique event ID
iyear, imonth, iday: Date
country_txt: Country name
region_txt: Region
city: City
latitude, longitude: Location
attacktype1_txt: Attack type
targtype1_txt: Target type
gname: Perpetrator group name
nkill: Number killed
nwound: Number wounded
summary: Event description
```

**Example Usage:**
```python
# Load GTD data
gtd = pd.read_csv("globalterrorismdb.csv", encoding='ISO-8859-1')

# Recent attacks by country
recent_attacks = gtd[gtd['iyear'] >= 2015].groupby('country_txt').size()

# Deadliest attacks
deadliest = gtd.nlargest(100, 'nkill')[['iyear', 'country_txt', 'city', 'gname', 'nkill']]

# Attack trends over time
attack_trends = gtd.groupby('iyear').size()
```

**Dataset 2: Armed Conflict Location & Event Data (ACLED)**
- **URL:** https://www.kaggle.com/datasets/acled/acled-conflict-data
- **Size:** 1 GB
- **Format:** CSV
- **Records:** 500,000+ conflict events

**Used By:** E22 (Event Tracking), E23 (Crisis Tracking)

---

## 4. Paid APIs (Phase 2+)

### 4.1 VulnCheck

**Service Information:**
```yaml
Website: https://vulncheck.com
Focus: Real-time vulnerability intelligence
Pricing: Starting at $99/month
Trial: 14-day free trial
```

**Features:**
- **KEV Monitoring:** CISA Known Exploited Vulnerabilities
- **Exploit Database:** Links to public exploits
- **EPSS Scores:** Exploit Prediction Scoring System
- **Faster Updates:** 24-48 hours faster than NVD
- **Enhanced Metadata:** Additional vulnerability context

**When to Upgrade:**
```yaml
Triggers:
  - Real-time threat monitoring required
  - EPSS scores needed for prioritization
  - Exploit availability critical for risk assessment
  - NVD latency causing operational delays
  - Production security tooling deployment

ROI Indicators:
  - Security operations team established
  - Vulnerability management program mature
  - Active threat hunting operations
  - Compliance requirements for rapid response
  - Large-scale infrastructure requiring monitoring
```

**Pricing Tiers:**
```yaml
Starter: $99/month
  - 1,000 API calls/day
  - Basic vulnerability data
  - KEV notifications

Professional: $299/month
  - 10,000 API calls/day
  - EPSS scores
  - Exploit intelligence
  - Priority support

Enterprise: Custom pricing
  - Unlimited API calls
  - Custom integrations
  - Dedicated support
  - Advanced analytics
```

**API Example:**
```python
import requests

def get_vulncheck_data(cve_id, api_key):
    """Fetch vulnerability data from VulnCheck"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    url = f"https://api.vulncheck.com/v1/cve/{cve_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "cve_id": cve_id,
            "epss_score": data.get("epss_score"),
            "has_exploit": data.get("exploit_available"),
            "kev_status": data.get("in_kev"),
            "published": data.get("published_date"),
            "vulncheck_updated": data.get("last_updated")
        }
    return None

# Example usage
vuln_data = get_vulncheck_data("CVE-2023-12345", api_key=os.environ["VULNCHECK_API_KEY"])
```

**Integration Guide:**
```python
# Phase 2 migration plan
def migrate_to_vulncheck():
    """
    Gradually migrate from NVD to VulnCheck
    1. Run both APIs in parallel
    2. Compare data quality and latency
    3. Switch critical systems to VulnCheck
    4. Fully migrate after validation period
    """

    # Hybrid approach during migration
    def fetch_vulnerability_data(cve_id):
        # Try VulnCheck first (faster, more complete)
        vuln_data = get_vulncheck_data(cve_id, VULNCHECK_API_KEY)

        if not vuln_data:
            # Fallback to NVD (free but slower)
            vuln_data = get_cve_by_id(cve_id, NVD_API_KEY)

        return vuln_data
```

---

### 4.2 Commercial Threat Intelligence Feeds

**Option 1: Recorded Future**
```yaml
Website: https://www.recordedfuture.com
Focus: Comprehensive threat intelligence
Pricing: Enterprise (contact sales)
Trial: Available
```

**Features:**
- Real-time threat actor tracking
- Dark web monitoring
- Vulnerability intelligence
- Risk scoring
- Playbook automation

**Option 2: CrowdStrike Falcon Intelligence**
```yaml
Website: https://www.crowdstrike.com
Focus: Adversary intelligence
Pricing: Module-based (contact sales)
Trial: Available
```

**Features:**
- APT tracking
- Malware analysis
- Indicators of compromise (IOCs)
- Attribution intelligence
- Threat hunting tools

**Option 3: Mandiant Threat Intelligence**
```yaml
Website: https://www.mandiant.com
Focus: Advanced threat research
Pricing: Enterprise (contact sales)
Trial: Limited
```

**ROI Analysis:**
```yaml
Cost-Benefit Calculation:

  Monthly Cost: $5,000 - $20,000

  Benefits:
    - Reduced incident response time: 40-60%
    - Proactive threat detection: 50-70%
    - Reduced false positives: 30-50%
    - Enhanced attribution: High confidence
    - Regulatory compliance: Simplified

  Break-even Point:
    - Medium enterprise: 6-12 months
    - Large enterprise: 3-6 months
    - Critical infrastructure: Immediate

  Recommended Timeline:
    Phase 1 (Months 1-6): Free sources + NVD
    Phase 2 (Months 7-12): Add VulnCheck
    Phase 3 (Year 2+): Evaluate commercial feeds
```

**Comparison Matrix:**
```yaml
Recorded Future:
  Strengths: Breadth, automation, risk scoring
  Best For: Large enterprises, financial sector
  Integration: Excellent API, SIEM integrations

CrowdStrike:
  Strengths: Adversary focus, endpoint integration
  Best For: Organizations with CrowdStrike EDR
  Integration: Native platform integration

Mandiant:
  Strengths: Research depth, incident response
  Best For: APT-targeted organizations
  Integration: Google Cloud Security integration
```

---

## 5. API Integration Patterns

### 5.1 Authentication Patterns

**API Key Authentication (NVD, FRED, VulnCheck):**
```python
import os
import requests

class APIKeyAuth:
    """Standard API key authentication"""

    def __init__(self, api_key_env_var):
        self.api_key = os.environ.get(api_key_env_var)
        if not self.api_key:
            raise ValueError(f"Missing environment variable: {api_key_env_var}")

    def get_headers(self):
        """Return headers with API key"""
        return {"apiKey": self.api_key}

    def make_request(self, url, params=None):
        """Make authenticated request"""
        headers = self.get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

# Usage
nvd_auth = APIKeyAuth("NVD_API_KEY")
cve_data = nvd_auth.make_request(
    "https://services.nvd.nist.gov/rest/json/cves/2.0",
    params={"cveId": "CVE-2023-12345"}
)
```

**Bearer Token Authentication (VulnCheck):**
```python
class BearerTokenAuth:
    """Bearer token authentication"""

    def __init__(self, token_env_var):
        self.token = os.environ.get(token_env_var)
        if not self.token:
            raise ValueError(f"Missing environment variable: {token_env_var}")

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def make_request(self, url, method="GET", data=None):
        headers = self.get_headers()

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()
        return response.json()

# Usage
vulncheck_auth = BearerTokenAuth("VULNCHECK_API_KEY")
vuln_data = vulncheck_auth.make_request(
    "https://api.vulncheck.com/v1/cve/CVE-2023-12345"
)
```

**No Authentication (World Bank, GDELT):**
```python
class NoAuth:
    """Public API with no authentication"""

    def make_request(self, url, params=None):
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

# Usage
wb_auth = NoAuth()
pop_data = wb_auth.make_request(
    "https://api.worldbank.org/v2/country/USA/indicator/SP.POP.TOTL",
    params={"format": "json", "date": "2023"}
)
```

---

### 5.2 Rate Limiting Patterns

**Token Bucket Algorithm:**
```python
import time
from collections import deque
from threading import Lock

class RateLimiter:
    """Thread-safe token bucket rate limiter"""

    def __init__(self, max_calls, time_window):
        """
        max_calls: Maximum calls allowed
        time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
        self.lock = Lock()

    def acquire(self):
        """Acquire permission to make API call"""
        with self.lock:
            now = time.time()

            # Remove expired calls
            while self.calls and now - self.calls[0] > self.time_window:
                self.calls.popleft()

            # Check if we can make a call
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True

            # Calculate wait time
            wait_time = self.time_window - (now - self.calls[0])
            if wait_time > 0:
                time.sleep(wait_time)
                self.calls.popleft()
                self.calls.append(time.time())
                return True

    def __call__(self, func):
        """Decorator for rate-limited functions"""
        def wrapper(*args, **kwargs):
            self.acquire()
            return func(*args, **kwargs)
        return wrapper

# Usage
# NVD with API key: 50 requests per 30 seconds
nvd_limiter = RateLimiter(max_calls=50, time_window=30)

@nvd_limiter
def fetch_cve_with_rate_limit(cve_id):
    return get_cve_by_id(cve_id, api_key=os.environ["NVD_API_KEY"])
```

**Adaptive Rate Limiting:**
```python
class AdaptiveRateLimiter:
    """Adapts to API rate limit responses"""

    def __init__(self, initial_rate=10, time_window=60):
        self.current_rate = initial_rate
        self.time_window = time_window
        self.calls = deque()
        self.lock = Lock()

    def handle_rate_limit_error(self, retry_after=None):
        """Adjust rate when rate limit hit"""
        with self.lock:
            # Reduce rate by 50%
            self.current_rate = max(1, self.current_rate // 2)
            print(f"Rate limit hit. Reducing to {self.current_rate} calls per {self.time_window}s")

            # Wait for retry_after if provided
            if retry_after:
                time.sleep(retry_after)

    def handle_success(self):
        """Gradually increase rate on success"""
        with self.lock:
            # Increase rate by 10% every 100 successful calls
            if len(self.calls) % 100 == 0:
                self.current_rate = int(self.current_rate * 1.1)
                print(f"Increasing rate to {self.current_rate} calls per {self.time_window}s")

    def acquire(self):
        with self.lock:
            now = time.time()

            # Remove expired calls
            while self.calls and now - self.calls[0] > self.time_window:
                self.calls.popleft()

            # Wait if necessary
            if len(self.calls) >= self.current_rate:
                wait_time = self.time_window - (now - self.calls[0])
                if wait_time > 0:
                    time.sleep(wait_time)
                self.calls.popleft()

            self.calls.append(time.time())

# Usage
adaptive_limiter = AdaptiveRateLimiter(initial_rate=10, time_window=60)

def fetch_with_adaptive_limiting(cve_id):
    adaptive_limiter.acquire()
    try:
        response = get_cve_by_id(cve_id)
        adaptive_limiter.handle_success()
        return response
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            retry_after = int(e.response.headers.get("Retry-After", 60))
            adaptive_limiter.handle_rate_limit_error(retry_after)
            return fetch_with_adaptive_limiting(cve_id)  # Retry
        raise
```

---

### 5.3 Error Handling Patterns

**Retry with Exponential Backoff:**
```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """Decorator for retrying failed requests"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)

                except requests.exceptions.HTTPError as e:
                    # Don't retry client errors (400-499) except 429
                    if 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                        raise

                    # Retry server errors and rate limits
                    if attempt < max_retries - 1:
                        # Exponential backoff with jitter
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        jitter = random.uniform(0, delay * 0.1)
                        wait_time = delay + jitter

                        print(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.2f}s...")
                        time.sleep(wait_time)
                    else:
                        raise

                except requests.exceptions.RequestException as e:
                    # Network errors - retry with backoff
                    if attempt < max_retries - 1:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        print(f"Network error. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        raise

        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3, base_delay=2)
def fetch_cve_resilient(cve_id):
    return get_cve_by_id(cve_id, api_key=os.environ["NVD_API_KEY"])
```

**Circuit Breaker Pattern:**
```python
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Prevent cascading failures with circuit breaker pattern"""

    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold

        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                print("Circuit breaker: Attempting recovery (HALF_OPEN)")
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN. Service unavailable.")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                print("Circuit breaker: Service recovered (CLOSED)")
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            print(f"Circuit breaker: Too many failures (OPEN)")
            self.state = CircuitState.OPEN

        if self.state == CircuitState.HALF_OPEN:
            print("Circuit breaker: Recovery failed (OPEN)")
            self.state = CircuitState.OPEN
            self.success_count = 0

# Usage
nvd_circuit = CircuitBreaker(failure_threshold=5, timeout=60)

def fetch_cve_with_circuit_breaker(cve_id):
    return nvd_circuit.call(get_cve_by_id, cve_id)
```

---

### 5.4 Caching Strategies

**Simple In-Memory Cache:**
```python
from functools import lru_cache
import hashlib
import json
import time

class CacheEntry:
    def __init__(self, data, ttl):
        self.data = data
        self.expires_at = time.time() + ttl

class SimpleCache:
    """In-memory cache with TTL"""

    def __init__(self, default_ttl=3600):
        self.cache = {}
        self.default_ttl = default_ttl

    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry.expires_at:
                return entry.data
            else:
                del self.cache[key]
        return None

    def set(self, key, data, ttl=None):
        ttl = ttl or self.default_ttl
        self.cache[key] = CacheEntry(data, ttl)

    def clear(self):
        self.cache.clear()

    def __call__(self, ttl=None):
        """Decorator for caching function results"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                key_data = {
                    "func": func.__name__,
                    "args": args,
                    "kwargs": kwargs
                }
                key = hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

                # Check cache
                cached = self.get(key)
                if cached is not None:
                    return cached

                # Call function and cache result
                result = func(*args, **kwargs)
                self.set(key, result, ttl)
                return result
            return wrapper
        return decorator

# Usage
cve_cache = SimpleCache(default_ttl=3600)  # 1 hour cache

@cve_cache(ttl=7200)  # 2 hour cache for this function
def fetch_cve_cached(cve_id):
    print(f"Fetching {cve_id} from API (cache miss)")
    return get_cve_by_id(cve_id, api_key=os.environ["NVD_API_KEY"])

# First call hits API
data1 = fetch_cve_cached("CVE-2023-12345")

# Second call uses cache
data2 = fetch_cve_cached("CVE-2023-12345")
```

**Redis Cache (Production):**
```python
import redis
import json
import pickle

class RedisCache:
    """Redis-based distributed cache"""

    def __init__(self, host="localhost", port=6379, default_ttl=3600):
        self.redis = redis.Redis(host=host, port=port, decode_responses=False)
        self.default_ttl = default_ttl

    def get(self, key):
        data = self.redis.get(key)
        if data:
            return pickle.loads(data)
        return None

    def set(self, key, data, ttl=None):
        ttl = ttl or self.default_ttl
        self.redis.setex(key, ttl, pickle.dumps(data))

    def delete(self, key):
        self.redis.delete(key)

    def clear_pattern(self, pattern):
        """Delete all keys matching pattern"""
        for key in self.redis.scan_iter(match=pattern):
            self.redis.delete(key)

# Usage
redis_cache = RedisCache(host="localhost", port=6379, default_ttl=7200)

def fetch_cve_redis_cached(cve_id):
    cache_key = f"cve:{cve_id}"

    # Check cache
    cached = redis_cache.get(cache_key)
    if cached:
        return cached

    # Fetch from API
    data = get_cve_by_id(cve_id, api_key=os.environ["NVD_API_KEY"])

    # Store in cache
    redis_cache.set(cache_key, data, ttl=7200)

    return data
```

---

### 5.5 Batch Processing Patterns

**Concurrent Batch Processing:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class BatchProcessor:
    """Process items in parallel batches"""

    def __init__(self, max_workers=5, rate_limiter=None):
        self.max_workers = max_workers
        self.rate_limiter = rate_limiter

    def process_batch(self, items, process_func):
        """
        Process items in parallel with optional rate limiting

        items: List of items to process
        process_func: Function to apply to each item
        """
        results = []
        errors = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(self._process_with_rate_limit, process_func, item): item
                for item in items
            }

            # Collect results as they complete
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    errors.append({"item": item, "error": str(e)})

        return results, errors

    def _process_with_rate_limit(self, func, item):
        if self.rate_limiter:
            self.rate_limiter.acquire()
        return func(item)

# Usage
nvd_limiter = RateLimiter(max_calls=50, time_window=30)
processor = BatchProcessor(max_workers=10, rate_limiter=nvd_limiter)

def fetch_single_cve(cve_id):
    return get_cve_by_id(cve_id, api_key=os.environ["NVD_API_KEY"])

# Process 100 CVEs in parallel with rate limiting
cve_ids = [f"CVE-2023-{i:05d}" for i in range(1, 101)]
results, errors = processor.process_batch(cve_ids, fetch_single_cve)

print(f"Successfully processed: {len(results)}")
print(f"Errors: {len(errors)}")
```

**Chunked Batch Processing:**
```python
def process_in_chunks(items, chunk_size, process_func, delay_between_chunks=1):
    """
    Process large lists in smaller chunks with delays

    Useful for very large datasets where processing all at once
    would overwhelm the API or system resources
    """
    results = []
    errors = []

    # Split into chunks
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)} ({len(chunk)} items)")

        # Process chunk
        chunk_results, chunk_errors = process_batch(chunk, process_func)
        results.extend(chunk_results)
        errors.extend(chunk_errors)

        # Delay between chunks (except last one)
        if i < len(chunks) - 1:
            time.sleep(delay_between_chunks)

    return results, errors

# Usage: Process 10,000 CVEs in chunks of 100
all_cve_ids = [f"CVE-2023-{i:05d}" for i in range(1, 10001)]
results, errors = process_in_chunks(
    all_cve_ids,
    chunk_size=100,
    process_func=fetch_single_cve,
    delay_between_chunks=2
)
```

---

## 6. Data Refresh Schedules

### 6.1 Real-time vs Batch Processing

**Real-time Sources (Immediate Updates):**
```yaml
GDELT DOC 2.0:
  Update Frequency: Every 15 minutes
  Latency: ~15-30 minutes
  Use Case: Breaking news, crisis monitoring
  Implementation: Polling or webhook

NVD CVE Feed:
  Update Frequency: Continuous
  Latency: 24-48 hours (official analysis)
  Use Case: Vulnerability monitoring
  Implementation: Daily batch + real-time for critical

VulnCheck (Paid):
  Update Frequency: Continuous
  Latency: 1-4 hours (faster than NVD)
  Use Case: Real-time threat intelligence
  Implementation: Webhook + polling
```

**Batch Sources (Scheduled Updates):**
```yaml
World Bank API:
  Update Frequency: Annually (some quarterly)
  Optimal Refresh: Monthly
  Use Case: Economic indicators
  Implementation: Monthly cron job

UN Population Data:
  Update Frequency: Annually
  Optimal Refresh: Quarterly
  Use Case: Demographic projections
  Implementation: Quarterly batch job

Kaggle Datasets:
  Update Frequency: Varies by dataset
  Optimal Refresh: Weekly/Monthly
  Use Case: Bulk historical data
  Implementation: Manual or scheduled download
```

### 6.2 Recommended Refresh Schedules

**Enhancement-Specific Schedules:**

```python
REFRESH_SCHEDULES = {
    "E03_CVE_Integration": {
        "source": "NVD API",
        "frequency": "daily",
        "cron": "0 2 * * *",  # 2 AM daily
        "priority": "high",
        "incremental": True,  # Only fetch new CVEs
        "full_refresh_interval": "monthly"
    },

    "E10_Economic_Indicators": {
        "source": "World Bank API + FRED",
        "frequency": "monthly",
        "cron": "0 3 1 * *",  # 3 AM on 1st of month
        "priority": "medium",
        "incremental": False,  # Full refresh
        "full_refresh_interval": "monthly"
    },

    "E11_Demographics": {
        "source": "World Bank + UN Population",
        "frequency": "quarterly",
        "cron": "0 4 1 1,4,7,10 *",  # Jan, Apr, Jul, Oct
        "priority": "low",
        "incremental": False,
        "full_refresh_interval": "quarterly"
    },

    "E12_CVSS_Scoring": {
        "source": "NVD API",
        "frequency": "daily",
        "cron": "0 2 30 * * *",  # 2:30 AM daily
        "priority": "high",
        "incremental": True,
        "full_refresh_interval": "monthly"
    },

    "E13_CWE_Mapping": {
        "source": "NVD API",
        "frequency": "daily",
        "cron": "0 3 * * *",  # 3 AM daily
        "priority": "high",
        "incremental": True,
        "full_refresh_interval": "monthly"
    },

    "E20_OCEAN_Traits": {
        "source": "Kaggle Big Five Dataset",
        "frequency": "quarterly",
        "cron": "0 5 1 1,4,7,10 *",
        "priority": "low",
        "incremental": False,
        "full_refresh_interval": "quarterly"
    },

    "E22_Event_Tracking": {
        "source": "GDELT API + FRED",
        "frequency": "hourly",  # Real-time monitoring
        "cron": "0 * * * *",  # Every hour
        "priority": "high",
        "incremental": True,
        "full_refresh_interval": "daily"
    },

    "E23_Crisis_Tracking": {
        "source": "GDELT API + World Bank",
        "frequency": "hourly",  # Real-time monitoring
        "cron": "15 * * * *",  # Every hour at :15
        "priority": "critical",
        "incremental": True,
        "full_refresh_interval": "daily"
    },

    "E25_Threat_Actors": {
        "source": "Kaggle APT Dataset + VulnCheck",
        "frequency": "weekly",
        "cron": "0 6 * * 0",  # 6 AM Sundays
        "priority": "medium",
        "incremental": True,
        "full_refresh_interval": "monthly"
    }
}
```

**Implementation Example:**

```python
import schedule
import time
from datetime import datetime

class DataRefreshScheduler:
    """Schedule and manage data refresh operations"""

    def __init__(self):
        self.schedules = REFRESH_SCHEDULES
        self.last_run = {}

    def setup_schedules(self):
        """Set up all refresh schedules"""
        for enhancement_id, config in self.schedules.items():
            if config["frequency"] == "hourly":
                schedule.every().hour.do(self.refresh_data, enhancement_id)
            elif config["frequency"] == "daily":
                schedule.every().day.at(self.parse_cron_time(config["cron"])).do(
                    self.refresh_data, enhancement_id
                )
            elif config["frequency"] == "weekly":
                day = self.parse_cron_day(config["cron"])
                time_str = self.parse_cron_time(config["cron"])
                schedule.every().week.at(time_str).do(self.refresh_data, enhancement_id)
            elif config["frequency"] == "monthly":
                # Check daily and run on first day of month
                schedule.every().day.at(self.parse_cron_time(config["cron"])).do(
                    self.check_monthly_refresh, enhancement_id
                )

    def refresh_data(self, enhancement_id):
        """Execute data refresh for specific enhancement"""
        config = self.schedules[enhancement_id]

        print(f"[{datetime.now()}] Refreshing {enhancement_id}")
        print(f"  Source: {config['source']}")
        print(f"  Priority: {config['priority']}")
        print(f"  Incremental: {config['incremental']}")

        try:
            if enhancement_id == "E03_CVE_Integration":
                self._refresh_cve_data(incremental=config["incremental"])
            elif enhancement_id == "E10_Economic_Indicators":
                self._refresh_economic_data()
            elif enhancement_id == "E22_Event_Tracking":
                self._refresh_event_data()
            # ... other enhancements

            self.last_run[enhancement_id] = datetime.now()
            print(f"  ✅ Refresh completed successfully")

        except Exception as e:
            print(f"  ❌ Refresh failed: {str(e)}")

    def _refresh_cve_data(self, incremental=True):
        """Refresh CVE data from NVD"""
        if incremental:
            # Only fetch CVEs modified in last 7 days
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            # Fetch recent CVEs
            recent_cves = get_recent_cves(days=7, api_key=os.environ["NVD_API_KEY"])

            # Store in Neo4j
            for cve in recent_cves["vulnerabilities"]:
                store_cve_in_neo4j(cve)
        else:
            # Full refresh - implement pagination
            pass

    def _refresh_economic_data(self):
        """Refresh economic indicators"""
        # Get list of countries from Neo4j
        countries = get_countries_from_neo4j()

        for country in countries:
            # Fetch latest economic data
            econ_data = get_demographic_data(country["iso3"], year=2023)

            # Update Neo4j
            update_country_economic_data(country["id"], econ_data)

    def run(self):
        """Run the scheduler"""
        self.setup_schedules()
        print("Data refresh scheduler started")

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# Usage
scheduler = DataRefreshScheduler()
scheduler.run()
```

### 6.3 Stale Data Handling

**Staleness Detection:**

```python
from datetime import datetime, timedelta

class StaleDataDetector:
    """Detect and handle stale data"""

    # Define staleness thresholds by data type
    STALENESS_THRESHOLDS = {
        "cve_data": timedelta(days=7),
        "economic_indicators": timedelta(days=45),
        "demographics": timedelta(days=180),
        "threat_intelligence": timedelta(days=30),
        "event_data": timedelta(hours=24),
        "crisis_data": timedelta(hours=12)
    }

    def __init__(self, neo4j_driver):
        self.neo4j = neo4j_driver

    def check_data_freshness(self, data_type):
        """Check if data type is stale"""
        threshold = self.STALENESS_THRESHOLDS.get(data_type)
        if not threshold:
            return False, None

        # Query Neo4j for last update timestamp
        query = f"""
        MATCH (n:{data_type.upper()})
        WHERE n.last_updated IS NOT NULL
        RETURN n.last_updated as last_update
        ORDER BY n.last_updated DESC
        LIMIT 1
        """

        result = self.neo4j.run(query).single()
        if not result:
            return True, None  # No data = stale

        last_update = datetime.fromisoformat(result["last_update"])
        age = datetime.now() - last_update

        is_stale = age > threshold
        return is_stale, age

    def get_stale_entities(self, data_type, limit=100):
        """Get entities with stale data"""
        threshold = self.STALENESS_THRESHOLDS.get(data_type)
        if not threshold:
            return []

        cutoff = datetime.now() - threshold

        query = f"""
        MATCH (n:{data_type.upper()})
        WHERE n.last_updated < datetime('{cutoff.isoformat()}')
           OR n.last_updated IS NULL
        RETURN n
        LIMIT {limit}
        """

        return self.neo4j.run(query).data()

    def mark_as_stale(self, node_id, data_type):
        """Mark entity as having stale data"""
        query = f"""
        MATCH (n:{data_type.upper()})
        WHERE id(n) = {node_id}
        SET n.is_stale = true,
            n.stale_since = datetime()
        """
        self.neo4j.run(query)

    def refresh_stale_data(self, data_type, batch_size=100):
        """Refresh all stale data for a type"""
        stale_entities = self.get_stale_entities(data_type, limit=batch_size)

        refreshed = 0
        for entity in stale_entities:
            try:
                if data_type == "cve_data":
                    self._refresh_cve(entity["n"]["cveId"])
                elif data_type == "economic_indicators":
                    self._refresh_economic(entity["n"]["country"])
                # ... other types

                refreshed += 1
            except Exception as e:
                print(f"Failed to refresh {entity}: {e}")

        return refreshed

# Usage
detector = StaleDataDetector(neo4j_driver)

# Check if CVE data is stale
is_stale, age = detector.check_data_freshness("cve_data")
if is_stale:
    print(f"CVE data is stale (age: {age})")
    detector.refresh_stale_data("cve_data", batch_size=100)
```

---

## 7. Data Quality Checks

### 7.1 Validation Rules

**Field-Level Validation:**

```python
from typing import Dict, Any, List
import re

class DataValidator:
    """Validate data quality across all sources"""

    # Validation rules by data type
    VALIDATION_RULES = {
        "cve": {
            "required_fields": ["cveId", "description", "publishedDate"],
            "cvss_range": (0.0, 10.0),
            "severity_values": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "cve_id_pattern": r"^CVE-\d{4}-\d{4,}$"
        },
        "economic": {
            "required_fields": ["country", "indicator", "value", "year"],
            "gdp_range": (0, 100_000_000_000_000),  # $100T max
            "year_range": (1950, 2100),
            "percentage_range": (0, 100)
        },
        "demographic": {
            "required_fields": ["country", "population", "year"],
            "population_range": (0, 10_000_000_000),  # 10B max
            "life_expectancy_range": (20, 120),
            "birth_rate_range": (0, 50),
            "death_rate_range": (0, 50)
        },
        "personality": {
            "required_fields": ["entity_id", "openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"],
            "trait_range": (0.0, 1.0)
        }
    }

    def validate_cve(self, cve_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate CVE data"""
        errors = []
        rules = self.VALIDATION_RULES["cve"]

        # Check required fields
        for field in rules["required_fields"]:
            if field not in cve_data or not cve_data[field]:
                errors.append(f"Missing required field: {field}")

        # Validate CVE ID format
        if "cveId" in cve_data:
            if not re.match(rules["cve_id_pattern"], cve_data["cveId"]):
                errors.append(f"Invalid CVE ID format: {cve_data['cveId']}")

        # Validate CVSS score range
        if "cvssScore" in cve_data:
            score = float(cve_data["cvssScore"])
            min_score, max_score = rules["cvss_range"]
            if not (min_score <= score <= max_score):
                errors.append(f"CVSS score {score} out of range [{min_score}, {max_score}]")

        # Validate severity
        if "severity" in cve_data:
            if cve_data["severity"] not in rules["severity_values"]:
                errors.append(f"Invalid severity: {cve_data['severity']}")

        # Check CVSS and severity consistency
        if "cvssScore" in cve_data and "severity" in cve_data:
            score = float(cve_data["cvssScore"])
            severity = cve_data["severity"]

            expected_severity = self._cvss_to_severity(score)
            if severity != expected_severity:
                errors.append(
                    f"CVSS score {score} inconsistent with severity {severity} "
                    f"(expected {expected_severity})"
                )

        return len(errors) == 0, errors

    def validate_economic_data(self, econ_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate economic indicator data"""
        errors = []
        rules = self.VALIDATION_RULES["economic"]

        # Check required fields
        for field in rules["required_fields"]:
            if field not in econ_data or econ_data[field] is None:
                errors.append(f"Missing required field: {field}")

        # Validate year range
        if "year" in econ_data:
            year = int(econ_data["year"])
            min_year, max_year = rules["year_range"]
            if not (min_year <= year <= max_year):
                errors.append(f"Year {year} out of range [{min_year}, {max_year}]")

        # Validate value ranges based on indicator type
        if "value" in econ_data and "indicator" in econ_data:
            value = float(econ_data["value"])
            indicator = econ_data["indicator"]

            if "GDP" in indicator:
                min_val, max_val = rules["gdp_range"]
                if not (min_val <= value <= max_val):
                    errors.append(f"GDP {value} out of range [{min_val}, {max_val}]")

            elif "%" in indicator or "percent" in indicator.lower():
                min_val, max_val = rules["percentage_range"]
                if not (min_val <= value <= max_val):
                    errors.append(f"Percentage {value} out of range [{min_val}, {max_val}]")

        return len(errors) == 0, errors

    def validate_demographic_data(self, demo_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate demographic data"""
        errors = []
        rules = self.VALIDATION_RULES["demographic"]

        # Check required fields
        for field in rules["required_fields"]:
            if field not in demo_data or demo_data[field] is None:
                errors.append(f"Missing required field: {field}")

        # Validate population range
        if "population" in demo_data:
            pop = float(demo_data["population"])
            min_pop, max_pop = rules["population_range"]
            if not (min_pop <= pop <= max_pop):
                errors.append(f"Population {pop} out of range [{min_pop}, {max_pop}]")

        # Validate life expectancy
        if "lifeExpectancy" in demo_data:
            le = float(demo_data["lifeExpectancy"])
            min_le, max_le = rules["life_expectancy_range"]
            if not (min_le <= le <= max_le):
                errors.append(f"Life expectancy {le} out of range [{min_le}, {max_le}]")

        # Validate birth/death rates
        for rate_field, range_key in [("birthRate", "birth_rate_range"), ("deathRate", "death_rate_range")]:
            if rate_field in demo_data:
                rate = float(demo_data[rate_field])
                min_rate, max_rate = rules[range_key]
                if not (min_rate <= rate <= max_rate):
                    errors.append(f"{rate_field} {rate} out of range [{min_rate}, {max_rate}]")

        return len(errors) == 0, errors

    def validate_personality_data(self, personality_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate OCEAN personality traits"""
        errors = []
        rules = self.VALIDATION_RULES["personality"]

        # Check required fields
        for field in rules["required_fields"]:
            if field not in personality_data or personality_data[field] is None:
                errors.append(f"Missing required field: {field}")

        # Validate trait ranges
        traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        min_val, max_val = rules["trait_range"]

        for trait in traits:
            if trait in personality_data:
                value = float(personality_data[trait])
                if not (min_val <= value <= max_val):
                    errors.append(f"{trait} {value} out of range [{min_val}, {max_val}]")

        return len(errors) == 0, errors

    @staticmethod
    def _cvss_to_severity(cvss_score: float) -> str:
        """Convert CVSS score to severity rating"""
        if cvss_score == 0.0:
            return "NONE"
        elif 0.1 <= cvss_score <= 3.9:
            return "LOW"
        elif 4.0 <= cvss_score <= 6.9:
            return "MEDIUM"
        elif 7.0 <= cvss_score <= 8.9:
            return "HIGH"
        else:
            return "CRITICAL"

# Usage
validator = DataValidator()

# Validate CVE data
cve_data = {
    "cveId": "CVE-2023-12345",
    "description": "Buffer overflow vulnerability",
    "publishedDate": "2023-06-15",
    "cvssScore": 7.5,
    "severity": "HIGH"
}
is_valid, errors = validator.validate_cve(cve_data)
if not is_valid:
    print(f"Validation errors: {errors}")
```

### 7.2 Completeness Checks

**Data Completeness Monitoring:**

```python
class CompletenessChecker:
    """Monitor data completeness across enhancements"""

    def __init__(self, neo4j_driver):
        self.neo4j = neo4j_driver

    def check_cve_completeness(self) -> Dict[str, Any]:
        """Check completeness of CVE data"""
        query = """
        MATCH (v:Vulnerability)
        WITH count(v) as total
        MATCH (v:Vulnerability)
        WHERE v.cvssScore IS NOT NULL
        WITH total, count(v) as with_cvss
        MATCH (v:Vulnerability)
        WHERE v.cweId IS NOT NULL
        WITH total, with_cvss, count(v) as with_cwe
        MATCH (v:Vulnerability)-[:AFFECTS]->(t:Technology)
        WITH total, with_cvss, with_cwe, count(DISTINCT v) as with_technology
        RETURN {
          total: total,
          with_cvss: with_cvss,
          with_cwe: with_cwe,
          with_technology: with_technology,
          cvss_pct: 100.0 * with_cvss / total,
          cwe_pct: 100.0 * with_cwe / total,
          tech_pct: 100.0 * with_technology / total
        } as completeness
        """

        result = self.neo4j.run(query).single()
        return result["completeness"]

    def check_economic_completeness(self) -> Dict[str, Any]:
        """Check completeness of economic data"""
        query = """
        MATCH (loc:Location {type: 'Country'})
        WITH count(loc) as total
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.gdp IS NOT NULL
        WITH total, count(loc) as with_gdp
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.unemployment IS NOT NULL
        WITH total, with_gdp, count(loc) as with_unemployment
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.inflation IS NOT NULL
        RETURN {
          total: total,
          with_gdp: with_gdp,
          with_unemployment: with_unemployment,
          gdp_pct: 100.0 * with_gdp / total,
          unemployment_pct: 100.0 * with_unemployment / total
        } as completeness
        """

        result = self.neo4j.run(query).single()
        return result["completeness"]

    def check_demographic_completeness(self) -> Dict[str, Any]:
        """Check completeness of demographic data"""
        query = """
        MATCH (loc:Location {type: 'Country'})
        WITH count(loc) as total
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.population IS NOT NULL
        WITH total, count(loc) as with_population
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.lifeExpectancy IS NOT NULL
        WITH total, with_population, count(loc) as with_life_exp
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.birthRate IS NOT NULL AND loc.deathRate IS NOT NULL
        RETURN {
          total: total,
          with_population: with_population,
          with_life_exp: with_life_exp,
          population_pct: 100.0 * with_population / total,
          life_exp_pct: 100.0 * with_life_exp / total
        } as completeness
        """

        result = self.neo4j.run(query).single()
        return result["completeness"]

    def generate_completeness_report(self) -> Dict[str, Any]:
        """Generate comprehensive completeness report"""
        return {
            "cve_data": self.check_cve_completeness(),
            "economic_data": self.check_economic_completeness(),
            "demographic_data": self.check_demographic_completeness(),
            "timestamp": datetime.now().isoformat()
        }

# Usage
checker = CompletenessChecker(neo4j_driver)
report = checker.generate_completeness_report()

print("Data Completeness Report")
print("=" * 50)
for data_type, metrics in report.items():
    if data_type != "timestamp":
        print(f"\n{data_type.upper()}:")
        for metric, value in metrics.items():
            if "_pct" in metric:
                print(f"  {metric}: {value:.2f}%")
            else:
                print(f"  {metric}: {value}")
```

### 7.3 Consistency Checks

**Cross-Source Consistency Validation:**

```python
class ConsistencyChecker:
    """Check data consistency across sources"""

    def __init__(self, neo4j_driver):
        self.neo4j = neo4j_driver

    def check_cvss_severity_consistency(self) -> List[Dict[str, Any]]:
        """Check if CVSS scores match severity ratings"""
        query = """
        MATCH (v:Vulnerability)
        WHERE v.cvssScore IS NOT NULL AND v.severity IS NOT NULL
        WITH v,
          CASE
            WHEN v.cvssScore >= 9.0 THEN 'CRITICAL'
            WHEN v.cvssScore >= 7.0 THEN 'HIGH'
            WHEN v.cvssScore >= 4.0 THEN 'MEDIUM'
            WHEN v.cvssScore >= 0.1 THEN 'LOW'
            ELSE 'NONE'
          END as expected_severity
        WHERE v.severity <> expected_severity
        RETURN v.cveId as cve_id,
               v.cvssScore as cvss_score,
               v.severity as actual_severity,
               expected_severity,
               'CVSS/Severity mismatch' as issue
        LIMIT 100
        """

        return self.neo4j.run(query).data()

    def check_population_trends(self) -> List[Dict[str, Any]]:
        """Check for impossible population changes"""
        query = """
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.population IS NOT NULL
           AND loc.populationPreviousYear IS NOT NULL
        WITH loc,
          100.0 * (loc.population - loc.populationPreviousYear) / loc.populationPreviousYear as growth_rate
        WHERE abs(growth_rate) > 10.0  // Flag >10% annual change
        RETURN loc.name as country,
               loc.population as current_population,
               loc.populationPreviousYear as previous_population,
               growth_rate,
               'Unusual population change' as issue
        """

        return self.neo4j.run(query).data()

    def check_economic_outliers(self) -> List[Dict[str, Any]]:
        """Check for economic outliers"""
        query = """
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.gdpPerCapita IS NOT NULL
        WITH avg(loc.gdpPerCapita) as avg_gdp,
             stdev(loc.gdpPerCapita) as std_gdp
        MATCH (loc:Location {type: 'Country'})
        WHERE loc.gdpPerCapita IS NOT NULL
        WITH loc, avg_gdp, std_gdp,
          (loc.gdpPerCapita - avg_gdp) / std_gdp as z_score
        WHERE abs(z_score) > 3  // More than 3 std devs from mean
        RETURN loc.name as country,
               loc.gdpPerCapita as gdp_per_capita,
               z_score,
               'GDP per capita outlier' as issue
        ORDER BY abs(z_score) DESC
        """

        return self.neo4j.run(query).data()

    def check_personality_trait_ranges(self) -> List[Dict[str, Any]]:
        """Check if personality traits are in valid range"""
        query = """
        MATCH (p:Person)
        WHERE p.openness IS NOT NULL
           OR p.conscientiousness IS NOT NULL
           OR p.extraversion IS NOT NULL
           OR p.agreeableness IS NOT NULL
           OR p.neuroticism IS NOT NULL
        WITH p,
          [p.openness, p.conscientiousness, p.extraversion, p.agreeableness, p.neuroticism] as traits
        UNWIND range(0, size(traits)-1) as idx
        WITH p, traits, idx,
          ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'] as trait_names
        WHERE traits[idx] IS NOT NULL
          AND (traits[idx] < 0.0 OR traits[idx] > 1.0)
        RETURN p.name as person,
               trait_names[idx] as trait,
               traits[idx] as value,
               'Trait out of range [0.0, 1.0]' as issue
        """

        return self.neo4j.run(query).data()

    def run_all_consistency_checks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Run all consistency checks"""
        return {
            "cvss_severity_mismatches": self.check_cvss_severity_consistency(),
            "population_anomalies": self.check_population_trends(),
            "economic_outliers": self.check_economic_outliers(),
            "personality_range_violations": self.check_personality_trait_ranges()
        }

# Usage
checker = ConsistencyChecker(neo4j_driver)
issues = checker.run_all_consistency_checks()

print("Data Consistency Issues")
print("=" * 50)
for check_type, problems in issues.items():
    print(f"\n{check_type}: {len(problems)} issues found")
    for problem in problems[:5]:  # Show first 5
        print(f"  {problem}")
```

---

## 8. Quick Reference Table

### API Comparison Matrix

| API | Authentication | Rate Limit | Cost | Update Frequency | Best For | Enhancements |
|-----|----------------|------------|------|------------------|----------|--------------|
| **NVD** | API key (optional) | 5/30s (anon), 50/30s (key) | FREE | Daily | CVE data | E03, E12, E13 |
| **World Bank** | None | Reasonable use | FREE | Annual/Quarterly | Economic indicators | E10, E11 |
| **UN Population** | None | Reasonable use | FREE | Annual | Demographics | E11, E23 |
| **GDELT** | None | Reasonable use | FREE | 15 minutes | News/events | E22, E23 |
| **FRED** | API key (free) | No limit | FREE | Varies by series | Economic data | E10, E22 |
| **VulnCheck** | Bearer token | Tiered | $99-Custom/mo | Real-time | Vuln intel | E03, E12, E13 |

### Enhancement → Data Source Mapping

| Enhancement | Primary Source | Secondary Sources | Refresh Schedule |
|-------------|----------------|-------------------|------------------|
| **E03** CVE Integration | NVD API | Kaggle CVE datasets | Daily |
| **E10** Economic Indicators | FRED, World Bank | Kaggle economic datasets | Monthly |
| **E11** Demographics | World Bank, UN Population | Kaggle demographic datasets | Quarterly |
| **E12** CVSS Scoring | NVD API | VulnCheck (paid) | Daily |
| **E13** CWE Mapping | NVD API | - | Daily |
| **E20** OCEAN Traits | Kaggle Big Five | - | Quarterly |
| **E21** MBTI Types | Kaggle MBTI | - | Quarterly |
| **E22** Event Tracking | GDELT, FRED | Kaggle event datasets | Hourly |
| **E23** Crisis Tracking | GDELT, World Bank | UN, Kaggle conflict data | Hourly |
| **E24** Cognitive Styles | Kaggle psychology datasets | - | Quarterly |
| **E25** Threat Actors | Kaggle APT datasets | VulnCheck (paid) | Weekly |

### Priority Implementation Order

**Phase 1 (Free APIs):**
1. E03 (NVD API)
2. E12 (NVD API)
3. E13 (NVD API)
4. E10 (FRED + World Bank)
5. E22 (GDELT)

**Phase 2 (Kaggle Datasets):**
6. E11 (Demographics)
7. E20 (Personality)
8. E23 (Crisis)
9. E25 (Threat Actors)

**Phase 3 (Paid APIs):**
10. VulnCheck integration for E03, E12, E13
11. Commercial threat feeds for E25

---

## Version History

- **v1.0.0 (2025-12-03):** Initial comprehensive data sources guide
- Documented all internal and external data sources
- Provided API integration patterns and examples
- Established data quality and refresh standards

---

## References & Resources

### Official Documentation
- NVD API: https://nvd.nist.gov/developers
- World Bank API: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
- UN Population: https://population.un.org/dataportal/about/dataapi
- GDELT: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- FRED: https://fred.stlouisfed.org/docs/api/fred/

### Kaggle Datasets
- Browse Datasets: https://www.kaggle.com/datasets
- Kaggle API: https://github.com/Kaggle/kaggle-api

### Paid Services
- VulnCheck: https://vulncheck.com
- Recorded Future: https://www.recordedfuture.com
- CrowdStrike: https://www.crowdstrike.com
- Mandiant: https://www.mandiant.com

---

*Last Updated: 2025-12-03*
*Maintainer: AEON Enhancement Research Team*
*Status: ACTIVE - Comprehensive data source documentation for all AEON enhancements*
