---
title: N8N Node Reference - Part 2b - Tool Nodes
category: 05_Integration_Guides/02_N8N/Node_Reference
last_updated: 2025-10-25
line_count: 340
status: published
tags: [n8n, langchain, tools, http-requests, vector-store, rag, code, perplexity]
part: 2b
total_parts: 4
---

# n8n LangChain Node Configuration Reference - Part 2b: Tool Nodes

**Navigation:**
- **Previous**: [Part 2a - Memory Nodes](02a_Memory_Nodes.md)
- **Current**: Part 2b - Tool Nodes
- **Next**: [Part 3 - Output Parsers & Best Practices](03_Output_Parsers_Best_Practices.md)

---

Comprehensive reference for n8n LangChain tool nodes that extend AI Agent capabilities.

## Table of Contents
1. [Tool HTTP Request](#tool-http-request)
2. [Tool Code](#tool-code)
3. [Tool Vector Store](#tool-vector-store)

---

## Tool HTTP Request
**Node Type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
**Version:** 1.1
**Purpose:** HTTP API calls as AI tools (Perplexity, custom APIs)

```json
{
  "name": "Perplexity Search",
  "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
  "typeVersion": 1.1,
  "position": [250, 600],
  "parameters": {
    "name": "perplexity_search",
    "description": "Search for current information, recent events, facts, news, or any real-time data. Use this when you need up-to-date information or to fact-check claims. Input should be a clear search query.",
    "method": "POST",
    "url": "https://api.perplexity.ai/chat/completions",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "httpHeaderAuth",
    "sendQuery": false,
    "sendHeaders": false,
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ { \"model\": \"llama-3.1-sonar-small-128k-online\", \"messages\": [{\"role\": \"user\", \"content\": $json.query}], \"max_tokens\": 500, \"temperature\": 0.2, \"return_citations\": true } }}",
    "options": {
      "response": {
        "response": {
          "responseFormat": "json",
          "jsonOutput": "={{ $response.body.choices[0].message.content }}"
        }
      }
    }
  },
  "credentials": {
    "httpHeaderAuth": {
      "id": "perplexity-credential-id",
      "name": "Perplexity API"
    }
  }
}
```

**Critical Parameters:**

**Tool Identification:**
- `name` (string): Tool identifier for AI Agent
  - Use snake_case: `perplexity_search`, `get_weather`, `calculator`
  - AI uses this name when calling the tool
  - Must be unique within workflow

- `description` (string): **MOST IMPORTANT** - Tells AI when to use this tool
  - Be specific about:
    - What the tool does
    - When to use it
    - What input format is expected
  - Example:
    ```
    "Search for current information, recent events, facts, news, or any
    real-time data. Use this when you need up-to-date information or to
    fact-check claims. Input should be a clear search query."
    ```
  - Bad description: `"Search the web"` (too vague)
  - Good description: Above example (specific use cases + input format)

**HTTP Configuration:**
- `method` (enum): HTTP method
  - `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`

- `url` (string): Full API endpoint URL
  - Example: `"https://api.perplexity.ai/chat/completions"`
  - Supports n8n expressions: `"https://api.example.com/{{ $json.endpoint }}"`

- `authentication` (enum): Authentication type
  - `"predefinedCredentialType"` - Use n8n credentials
  - `"defineBelow"` - Manual auth configuration
  - `"none"` - No authentication

- `nodeCredentialType` (string): Credential type when using predefinedCredentialType
  - `"httpHeaderAuth"` - Header-based (Bearer tokens, API keys)
  - `"httpBasicAuth"` - Basic authentication
  - `"httpDigestAuth"` - Digest authentication
  - `"oAuth2Api"` - OAuth 2.0

**Request Body:**
- `sendBody` (boolean): Include request body
  - `true` for POST/PUT/PATCH requests
  - `false` for GET/DELETE

- `specifyBody` (enum): How to define body
  - `"json"` - JSON object (most common for APIs)
  - `"formData"` - Form data
  - `"raw"` - Raw string

- `jsonBody` (string): JSON body as n8n expression
  - Access tool input with `$json.query`
  - Example:
    ```javascript
    ={{ {
      "model": "llama-3.1-sonar-small-128k-online",
      "messages": [{"role": "user", "content": $json.query}],
      "max_tokens": 500,
      "temperature": 0.2,
      "return_citations": true
    } }}
    ```

**Response Handling:**
- `options.response.response.responseFormat` (enum): Expected response format
  - `"json"` - Parse as JSON (most APIs)
  - `"text"` - Plain text
  - `"autodetect"` - Let n8n determine

- `options.response.response.jsonOutput` (string): Extract specific field
  - Extract relevant data from API response
  - Example: `"={{ $response.body.choices[0].message.content }}"`
  - Returns only the extracted value to AI Agent

**Example: Weather API Tool**
```json
{
  "name": "get_weather",
  "description": "Get current weather information for a specific city or location. Input should be a city name or coordinates.",
  "method": "GET",
  "url": "https://api.openweathermap.org/data/2.5/weather",
  "sendQuery": true,
  "queryParameters": {
    "parameters": [
      {
        "name": "q",
        "value": "={{ $json.query }}"
      },
      {
        "name": "appid",
        "value": "{{ $credentials.openWeatherMapApi.apiKey }}"
      },
      {
        "name": "units",
        "value": "metric"
      }
    ]
  },
  "options": {
    "response": {
      "response": {
        "responseFormat": "json",
        "jsonOutput": "={{ { temperature: $response.body.main.temp, condition: $response.body.weather[0].description, humidity: $response.body.main.humidity } }}"
      }
    }
  }
}
```

**Connection Types:**
- **Outgoing:** `ai_tool` → AI Agent

**Use Cases:**
- ✅ Web search (Perplexity, Google Custom Search)
- ✅ Weather data
- ✅ Stock prices and financial data
- ✅ Custom business APIs
- ✅ Database queries via REST API
- ✅ Third-party service integration

**Tool Design Best Practices:**
1. **Clear descriptions** - AI relies entirely on description to understand when to use tool
2. **Specific input format** - Tell AI exactly what format you expect
3. **Response extraction** - Only return relevant data, not entire API response
4. **Error handling** - Consider what happens if API fails
5. **Rate limiting** - Be aware of API rate limits in high-traffic scenarios

---

## Tool Code
**Node Type:** `@n8n/n8n-nodes-langchain.toolCode`
**Version:** 1.0
**Purpose:** Execute custom JavaScript or Python code as AI tool

```json
{
  "name": "calculator",
  "type": "@n8n/n8n-nodes-langchain.toolCode",
  "typeVersion": 1.0,
  "position": [250, 650],
  "parameters": {
    "name": "calculator",
    "description": "Perform mathematical calculations. Input should be a mathematical expression as a string (e.g., '2 + 2', '(5 * 3) / 2', 'Math.sqrt(16)').",
    "language": "javaScript",
    "jsCode": "const result = eval($input);\nreturn { result };",
    "options": {
      "returnAll": false
    }
  }
}
```

**Parameters:**
- `name` (string): Tool identifier
- `description` (string): When and how to use this tool
- `language` (enum): Programming language
  - `"javaScript"` - JavaScript (Node.js)
  - `"python"` - Python 3

**JavaScript Code:**
- `jsCode` (string): JavaScript code to execute
  - Access input with `$input` variable
  - Return object: `return { result: value }`
  - Available libraries: Node.js standard library
  - Example:
    ```javascript
    // Calculator
    const result = eval($input);
    return { result };

    // Data analysis
    const data = JSON.parse($input);
    const average = data.reduce((a, b) => a + b, 0) / data.length;
    return { average, count: data.length };
    ```

**Python Code:**
- `pythonCode` (string): Python code to execute
  - Access input with `input_data` variable
  - Return dictionary: `return {'result': value}`
  - Available libraries: Python standard library + numpy, pandas
  - Example:
    ```python
    # Calculator
    result = eval(input_data)
    return {'result': result}

    # Data processing
    import pandas as pd
    df = pd.DataFrame(input_data)
    return {
      'mean': df['value'].mean(),
      'std': df['value'].std()
    }
    ```

**Security Considerations:**
- ⚠️ **Avoid `eval()` in production** - Use safe parsing instead
- ⚠️ Validate and sanitize all inputs
- ⚠️ Set resource limits for long-running code
- ⚠️ Consider timeout configuration

**Use Cases:**
- ✅ Mathematical calculations
- ✅ Data transformations
- ✅ Custom business logic
- ✅ String manipulation
- ✅ Date/time operations
- ✅ Data analysis and statistics

**Example: Safe Calculator**
```javascript
// Safe calculator without eval
const math = require('mathjs');
try {
  const result = math.evaluate($input);
  return { result };
} catch (error) {
  return { error: 'Invalid mathematical expression' };
}
```

---

## Tool Vector Store
**Node Type:** `@n8n/n8n-nodes-langchain.toolVectorStore`
**Version:** 1.0
**Purpose:** Semantic search over document embeddings (RAG)

```json
{
  "name": "document_search",
  "type": "@n8n/n8n-nodes-langchain.toolVectorStore",
  "typeVersion": 1.0,
  "position": [250, 700],
  "parameters": {
    "name": "document_search",
    "description": "Search internal company documents and knowledge base for information about products, policies, procedures, and technical documentation. Input should be a search query describing what information you need.",
    "vectorStoreType": "pinecone",
    "topK": 3,
    "options": {
      "includeMetadata": true
    }
  },
  "credentials": {
    "pineconeApi": {
      "id": "pinecone-credential-id",
      "name": "Pinecone Vector DB"
    }
  }
}
```

**Parameters:**
- `name`, `description`: Same as other tools

- `vectorStoreType` (enum): Vector database backend
  - `"pinecone"` - Pinecone (managed, scalable)
  - `"qdrant"` - Qdrant (open-source, self-hosted)
  - `"supabase"` - Supabase (PostgreSQL + pgvector)
  - `"memory"` - In-memory (for testing)

- `topK` (number): Number of similar documents to return
  - Default: `3`
  - Range: `1-20`
  - Higher values = more context but slower

- `options.includeMetadata` (boolean): Include document metadata
  - `true` - Return source, page numbers, etc.
  - `false` - Only return document text

**Vector Database Configuration:**

**Qdrant (Recommended for AgentZero):**
```
Host: qdrant
Port: 6333
Collection: documents
Distance Metric: Cosine
Vector Size: 1536 (OpenAI ada-002)
```

**Use Cases:**
- ✅ RAG (Retrieval Augmented Generation)
- ✅ Internal knowledge base search
- ✅ Product documentation lookup
- ✅ Policy and procedure queries
- ✅ Technical troubleshooting from docs

**Complete RAG Example:**
```
[Document Loader] → [Text Splitter] → [Embeddings OpenAI] → [Vector Store Qdrant]
                                                                       ↓ (ai_tool)
[Chat Trigger] → [AI Agent] ← ────────────────────────── [Tool Vector Store]
```

---

**Navigation:**
- **Previous**: [Part 2a - Memory Nodes](02a_Memory_Nodes.md)
- **Current**: Part 2b - Tool Nodes
- **Next**: [Part 3 - Output Parsers & Best Practices](03_Output_Parsers_Best_Practices.md)

---
**Document Version:** 1.0 (Part 2b of 4)
**Last Updated:** 2025-10-25
**Lines:** 340 / 500 limit
