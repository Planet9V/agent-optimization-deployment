# Psychometric Assessment APIs

**Total Endpoints:** 8

**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [GET /api/v2/psychometrics/traits](#get--api-v2-psychometrics-traits): List Traits
2. [GET /api/v2/psychometrics/traits/{trait_id}](#get--api-v2-psychometrics-traits-trait_id): Get Trait Details
3. [GET /api/v2/psychometrics/actors/{actor_id}/profile](#get--api-v2-psychometrics-actors-actor_id-profile): Get Actor Profile
4. [GET /api/v2/psychometrics/actors/by-trait/{trait_id}](#get--api-v2-psychometrics-actors-by-trait-trait_id): Get Actors By Trait
5. [GET /api/v2/psychometrics/biases](#get--api-v2-psychometrics-biases): List Biases
6. [GET /api/v2/psychometrics/biases/{bias_id}](#get--api-v2-psychometrics-biases-bias_id): Get Bias Details
7. [GET /api/v2/psychometrics/lacanian/registers](#get--api-v2-psychometrics-lacanian-registers): Get Lacanian Registers
8. [GET /api/v2/psychometrics/dashboard](#get--api-v2-psychometrics-dashboard): Get Dashboard

---

# Endpoint Details


## GET /api/v2/psychometrics/traits

**Summary:** List Traits

**Operation ID:** `list_traits_api_v2_psychometrics_traits_get`

**Description:**
List all psychological traits

Returns all PsychTrait nodes with optional filtering

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | string/null | ⬜ No | query | Filter by category |
| `limit` | integer | ⬜ No | query | Maximum number of results |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "trait_id": "<trait_id>",
  "name": "<name>"
}]
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/traits"
```

---

## GET /api/v2/psychometrics/traits/{trait_id}

**Summary:** Get Trait Details

**Operation ID:** `get_trait_details_api_v2_psychometrics_traits__trait_id__get`

**Description:**
Get detailed information about a specific trait

Includes related actors and trait relationships

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `trait_id` | string | ✅ Yes | path |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/traits/{trait_id}"
```

---

## GET /api/v2/psychometrics/actors/{actor_id}/profile

**Summary:** Get Actor Profile

**Operation ID:** `get_actor_profile_api_v2_psychometrics_actors__actor_id__profile_get`

**Description:**
Get psychological profile for a threat actor

Returns all traits associated with the actor

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `actor_id` | string | ✅ Yes | path |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "actor_id": "<actor_id>",
  "actor_name": "<actor_name>",
  "traits": [],
  "dominant_traits": []
}
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/actors/{actor_id}/profile"
```

---

## GET /api/v2/psychometrics/actors/by-trait/{trait_id}

**Summary:** Get Actors By Trait

**Operation ID:** `get_actors_by_trait_api_v2_psychometrics_actors_by_trait__trait_id__get`

**Description:**
Get all actors exhibiting a specific trait

Returns threat actors associated with the given trait

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `trait_id` | string | ✅ Yes | path |  |
| `limit` | integer | ⬜ No | query | Maximum number of results |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{}]
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/actors/by-trait/{trait_id}"
```

---

## GET /api/v2/psychometrics/biases

**Summary:** List Biases

**Operation ID:** `list_biases_api_v2_psychometrics_biases_get`

**Description:**
List all cognitive biases

Returns all Cognitive_Bias nodes with optional filtering

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | string/null | ⬜ No | query | Filter by category |
| `limit` | integer | ⬜ No | query | Maximum number of results |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "bias_id": "<bias_id>",
  "name": "<name>"
}]
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/biases"
```

---

## GET /api/v2/psychometrics/biases/{bias_id}

**Summary:** Get Bias Details

**Operation ID:** `get_bias_details_api_v2_psychometrics_biases__bias_id__get`

**Description:**
Get detailed information about a specific cognitive bias

Includes related actors and examples

### Parameters

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bias_id` | string | ✅ Yes | path |  |

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{}
```

### 404 - Not found
### 422 - Validation Error

**Response Body:**
```json
{
  "detail": []
}
```


### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/biases/{bias_id}"
```

---

## GET /api/v2/psychometrics/lacanian/registers

**Summary:** Get Lacanian Registers

**Operation ID:** `get_lacanian_registers_api_v2_psychometrics_lacanian_registers_get`

**Description:**
Get Lacanian psychoanalytic framework registers

Returns the three registers: Real, Imaginary, Symbolic with associated traits

### Parameters

No parameters required.

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
[{
  "register_type": "<register_type>",
  "description": "<description>",
  "traits": [],
  "count": 1
}]
```

### 404 - Not found

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/lacanian/registers"
```

---

## GET /api/v2/psychometrics/dashboard

**Summary:** Get Dashboard

**Operation ID:** `get_dashboard_api_v2_psychometrics_dashboard_get`

**Description:**
Get psychometric dashboard statistics

Returns comprehensive overview of all psychometric data

### Parameters

No parameters required.

### Request Body

No request body required.

### Responses

### 200 - Successful Response

**Response Body:**
```json
{
  "total_psych_traits": 1,
  "total_personality_traits": 1,
  "total_cognitive_biases": 1,
  "total_actor_profiles": 1,
  "top_traits": []
}
```

### 404 - Not found

### Example Request

```bash
curl -X GET "http://localhost:8000/api/v2/psychometrics/dashboard"
```

---
