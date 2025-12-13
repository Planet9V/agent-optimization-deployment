# Psychometric API Examples - Response Formats

## Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v2/psychometrics/traits` | GET | List all personality traits |
| `/api/v2/psychometrics/traits/{trait_id}` | GET | Get trait details + actors |
| `/api/v2/psychometrics/actors/{actor_id}/profile` | GET | Get actor psychological profile |
| `/api/v2/psychometrics/actors/by-trait/{trait_id}` | GET | Find actors by trait |
| `/api/v2/psychometrics/biases` | GET | List cognitive biases |
| `/api/v2/psychometrics/biases/{bias_id}` | GET | Get bias details |
| `/api/v2/psychometrics/lacanian/registers` | GET | Lacanian framework |
| `/api/v2/psychometrics/dashboard` | GET | System overview |

## Example Responses

### 1. GET /api/v2/psychometrics/traits?limit=3

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/traits?limit=3
```

**Response**:
```json
[
  {
    "trait_id": "trait_001",
    "name": "Machiavellianism",
    "description": "Strategic manipulation and exploitation of others",
    "category": "dark_triad",
    "intensity": 0.8
  },
  {
    "trait_id": "trait_002",
    "name": "Narcissism",
    "description": "Excessive self-focus and need for admiration",
    "category": "dark_triad",
    "intensity": 0.75
  },
  {
    "trait_id": "trait_003",
    "name": "Risk-taking",
    "description": "Propensity for high-risk behavior",
    "category": "behavioral",
    "intensity": 0.9
  }
]
```

### 2. GET /api/v2/psychometrics/traits/trait_001

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/traits/trait_001
```

**Response**:
```json
{
  "trait_id": "trait_001",
  "name": "Machiavellianism",
  "description": "Strategic manipulation and exploitation of others",
  "category": "dark_triad",
  "intensity": 0.8,
  "actors": [
    {
      "actor_id": "APT28",
      "actor_name": "Fancy Bear",
      "relationship_type": "HAS_TRAIT"
    },
    {
      "actor_id": "APT29",
      "actor_name": "Cozy Bear",
      "relationship_type": "HAS_TRAIT"
    }
  ],
  "actor_count": 2
}
```

### 3. GET /api/v2/psychometrics/actors/APT28/profile

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/actors/APT28/profile
```

**Response**:
```json
{
  "actor_id": "APT28",
  "actor_name": "Fancy Bear",
  "traits": [
    {
      "trait_id": "trait_001",
      "trait_name": "Machiavellianism",
      "category": "dark_triad",
      "intensity": 0.85,
      "description": "Strategic manipulation"
    },
    {
      "trait_id": "trait_005",
      "trait_name": "Persistence",
      "category": "behavioral",
      "intensity": 0.9,
      "description": "Sustained campaign focus"
    },
    {
      "trait_id": "trait_012",
      "trait_name": "Technical sophistication",
      "category": "capability",
      "intensity": 0.95,
      "description": "Advanced technical skills"
    }
  ],
  "personality_summary": "Profile based on 3 traits",
  "dominant_traits": [
    "Technical sophistication",
    "Persistence",
    "Machiavellianism"
  ]
}
```

### 4. GET /api/v2/psychometrics/actors/by-trait/trait_001?limit=2

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/actors/by-trait/trait_001?limit=2
```

**Response**:
```json
[
  {
    "actor_id": "APT29",
    "actor_name": "Cozy Bear",
    "description": "Russian state-sponsored threat group",
    "trait_name": "Machiavellianism",
    "trait_intensity": 0.9
  },
  {
    "actor_id": "APT28",
    "actor_name": "Fancy Bear",
    "description": "Russian military intelligence cyber unit",
    "trait_name": "Machiavellianism",
    "trait_intensity": 0.85
  }
]
```

### 5. GET /api/v2/psychometrics/biases?limit=2

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/biases?limit=2
```

**Response**:
```json
[
  {
    "bias_id": "bias_001",
    "name": "Confirmation Bias",
    "description": "Tendency to search for or interpret information that confirms preconceptions",
    "category": "cognitive",
    "severity": "high"
  },
  {
    "bias_id": "bias_002",
    "name": "Anchoring Bias",
    "description": "Over-reliance on initial information when making decisions",
    "category": "decision-making",
    "severity": "medium"
  }
]
```

### 6. GET /api/v2/psychometrics/biases/bias_001

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/biases/bias_001
```

**Response**:
```json
{
  "bias_id": "bias_001",
  "name": "Confirmation Bias",
  "description": "Tendency to search for or interpret information that confirms preconceptions",
  "category": "cognitive",
  "severity": "high",
  "actors": [
    {
      "actor_id": "APT1",
      "actor_name": "Comment Crew"
    }
  ],
  "actor_count": 1
}
```

### 7. GET /api/v2/psychometrics/lacanian/registers

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/lacanian/registers
```

**Response**:
```json
[
  {
    "register_type": "Real",
    "description": "The traumatic, impossible-to-symbolize dimension of experience - what resists symbolization",
    "traits": ["anxiety", "trauma", "jouissance"],
    "count": 3
  },
  {
    "register_type": "Imaginary",
    "description": "The realm of images, identification, and the ego - the domain of mirror-stage identification",
    "traits": ["narcissism", "rivalry", "identification"],
    "count": 3
  },
  {
    "register_type": "Symbolic",
    "description": "The domain of language, law, and the social order - the structure that governs desire",
    "traits": ["authority", "language", "social_norms"],
    "count": 3
  }
]
```

### 8. GET /api/v2/psychometrics/dashboard

**Request**:
```bash
curl http://localhost:8000/api/v2/psychometrics/dashboard
```

**Response**:
```json
{
  "total_psych_traits": 161,
  "total_personality_traits": 20,
  "total_cognitive_biases": 7,
  "total_actor_profiles": 50,
  "trait_distribution": {
    "dark_triad": 15,
    "behavioral": 42,
    "capability": 38,
    "motivational": 31,
    "social": 35
  },
  "top_traits": [
    {
      "trait": "Persistence",
      "actors": 45
    },
    {
      "trait": "Technical sophistication",
      "actors": 42
    },
    {
      "trait": "Opportunism",
      "actors": 38
    },
    {
      "trait": "Patience",
      "actors": 35
    },
    {
      "trait": "Machiavellianism",
      "actors": 32
    }
  ]
}
```

## Query Parameters

### Pagination
- `limit`: Maximum results to return (default varies by endpoint)
- Example: `?limit=10`

### Filtering
- `category`: Filter by category (traits and biases endpoints)
- Example: `?category=dark_triad`

### Combined
- `?category=behavioral&limit=5`

## Error Responses

### 404 Not Found
```json
{
  "detail": "Trait trait_999 not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Database connection failed"
}
```

## Use Cases

### 1. Threat Actor Profiling
```bash
# Get complete profile
curl http://localhost:8000/api/v2/psychometrics/actors/APT28/profile

# Analyze dominant traits for operational patterns
```

### 2. Trait-Based Actor Discovery
```bash
# Find all actors with specific trait
curl http://localhost:8000/api/v2/psychometrics/actors/by-trait/Machiavellianism

# Cluster actors by psychological similarity
```

### 3. Bias Analysis
```bash
# List all cognitive biases
curl http://localhost:8000/api/v2/psychometrics/biases

# Analyze bias manifestation in actor behavior
curl http://localhost:8000/api/v2/psychometrics/biases/confirmation_bias
```

### 4. Statistical Overview
```bash
# Get dashboard for reporting
curl http://localhost:8000/api/v2/psychometrics/dashboard

# Export for visualization in BI tools
```

### 5. Psychological Framework Analysis
```bash
# Get Lacanian framework
curl http://localhost:8000/api/v2/psychometrics/lacanian/registers

# Map actors to psychoanalytic registers
```

## Integration Examples

### Python Client
```python
import requests

BASE_URL = "http://localhost:8000/api/v2/psychometrics"

# Get actor profile
def get_actor_profile(actor_id):
    response = requests.get(f"{BASE_URL}/actors/{actor_id}/profile")
    return response.json()

# Find actors by trait
def find_actors_by_trait(trait_name, limit=10):
    response = requests.get(
        f"{BASE_URL}/actors/by-trait/{trait_name}",
        params={"limit": limit}
    )
    return response.json()

# Get dashboard stats
def get_dashboard():
    response = requests.get(f"{BASE_URL}/dashboard")
    return response.json()
```

### JavaScript/TypeScript Client
```typescript
const BASE_URL = "http://localhost:8000/api/v2/psychometrics";

// Get trait details
async function getTraitDetails(traitId: string) {
  const response = await fetch(`${BASE_URL}/traits/${traitId}`);
  return response.json();
}

// List all biases
async function listBiases(category?: string) {
  const params = category ? `?category=${category}` : "";
  const response = await fetch(`${BASE_URL}/biases${params}`);
  return response.json();
}
```

### cURL Examples
```bash
# Dashboard
curl http://localhost:8000/api/v2/psychometrics/dashboard | jq

# Traits with filtering
curl "http://localhost:8000/api/v2/psychometrics/traits?category=dark_triad&limit=5" | jq

# Actor profile
curl http://localhost:8000/api/v2/psychometrics/actors/APT28/profile | jq '.dominant_traits'

# Actors by trait
curl http://localhost:8000/api/v2/psychometrics/actors/by-trait/Persistence | jq '.[].actor_name'
```

## Performance Considerations

- **Response times**: < 100ms for most queries (depends on Neo4j)
- **Pagination**: Use `limit` parameter to control response size
- **Caching**: Consider implementing Redis cache for frequently accessed data
- **Indexing**: Ensure Neo4j has indexes on `id` and `name` fields

## Security Notes

- All queries use parameterized Cypher (prevents injection)
- Input validation via Pydantic models
- Consider adding authentication middleware for production
- Rate limiting recommended for public APIs

---

**Generated**: 2025-12-12
**API Version**: v2
**Total Endpoints**: 8
