---
title: N8N Node Reference - Part 3 - Output Parsers & Best Practices
category: 05_Integration_Guides/02_N8N/Node_Reference
last_updated: 2025-10-25
line_count: 347
status: published
tags: [n8n, langchain, output-parsers, connections, best-practices, validation]
part: 3
total_parts: 3
---

# n8n LangChain Node Configuration Reference - Part 3: Output Parsers & Best Practices

**Navigation:**
- **Previous**: [Part 2 - Memory & Tool Nodes](02_Memory_Tool_Nodes.md)
- **Current**: Part 3 - Output Parsers & Best Practices
- **Overview**: [Part 1 - Core Nodes](01_Core_Nodes.md)

---

Comprehensive reference for n8n LangChain output parsers, connection types, and best practices.

## Table of Contents - Part 3
1. [Output Parsers](#output-parsers)
2. [Connection Types Reference](#connection-types-reference)
3. [Best Practices Summary](#best-practices-summary)

---

## Output Parsers

### Output Parser Structured
**Node Type:** `@n8n/n8n-nodes-langchain.outputParserStructured`
**Version:** 1.0
**Purpose:** Extract structured data from LLM responses

```json
{
  "name": "Extract Contact Info",
  "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
  "typeVersion": 1.0,
  "position": [650, 300],
  "parameters": {
    "jsonSchema": "{\n  \"type\": \"object\",\n  \"properties\": {\n    \"name\": {\"type\": \"string\"},\n    \"email\": {\"type\": \"string\", \"format\": \"email\"},\n    \"phone\": {\"type\": \"string\"},\n    \"company\": {\"type\": \"string\"}\n  },\n  \"required\": [\"name\", \"email\"]\n}",
    "options": {
      "returnAsString": false
    }
  }
}
```

**Parameters:**
- `jsonSchema` (string): JSON Schema defining expected output structure
  - Standard JSON Schema format
  - Specify types, required fields, formats
  - LLM will structure response to match schema

**Example Schemas:**

**Contact Information:**
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "email": {"type": "string", "format": "email"},
    "phone": {"type": "string"},
    "company": {"type": "string"}
  },
  "required": ["name", "email"]
}
```

**Product Analysis:**
```json
{
  "type": "object",
  "properties": {
    "product_name": {"type": "string"},
    "category": {"type": "string", "enum": ["electronics", "clothing", "food", "other"]},
    "price": {"type": "number"},
    "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
    "key_features": {"type": "array", "items": {"type": "string"}},
    "rating": {"type": "number", "minimum": 0, "maximum": 5}
  },
  "required": ["product_name", "category", "sentiment"]
}
```

**Connection Types:**
- **Outgoing:** `ai_outputParser` → AI Agent
- **Important:** Set `hasOutputParser: true` on AI Agent

**Use Cases:**
- ✅ Data extraction from conversations
- ✅ Form filling from natural language
- ✅ Structured logging of chat interactions
- ✅ Database insertion from AI responses
- ✅ API call preparation from LLM output

**Limitations:**
- ⚠️ May not work with streaming mode
- ⚠️ Adds latency (LLM must format output)
- ⚠️ Schema must be clear and unambiguous

---

## Connection Types Reference

### Overview of n8n LangChain Connection Types

**Standard n8n Connections:**
- `main`: Data flow between regular nodes (left to right)

**AI-Specific Connections** (flow INTO AI nodes, not from them):
- `ai_languageModel`: Language model capability
- `ai_memory`: Conversation context
- `ai_tool`: Tool/function capabilities
- `ai_outputParser`: Output formatting
- `ai_embedding`: Text embedding models
- `ai_vectorStore`: Vector database connections
- `ai_retriever`: Document retrieval
- `ai_documentLoader`: Document ingestion
- `ai_textSplitter`: Text chunking

### Connection Flow Diagram

```
Standard Flow:
[Node A] --main--> [Node B] --main--> [Node C]

AI Agent Flow:
[Chat Trigger] --main--> [AI Agent] --main--> [Output Node]
                             ↑
        [OpenAI] --ai_languageModel--┘
        [Memory] --ai_memory----------┘
        [Tool 1] --ai_tool------------┘
        [Tool 2] --ai_tool------------┘
        [Parser] --ai_outputParser----┘
```

### Connection Rules by Node Type

**AI Agent:**
- **Incoming:**
  - `main`: 1 required (from Chat Trigger or data source)
  - `ai_languageModel`: 1-2 required (2 if needsFallback)
  - `ai_memory`: 0-1 optional
  - `ai_tool`: 0-many optional
  - `ai_outputParser`: 0-1 optional
- **Outgoing:**
  - `main`: To next node in workflow

**Chat Trigger:**
- **Incoming:** None (entry point)
- **Outgoing:**
  - `main`: 1 to AI Agent

**Language Models:**
- **Incoming:** None (capability provider)
- **Outgoing:**
  - `ai_languageModel`: To AI Agent/Chain

**Memory Nodes:**
- **Incoming:** None (capability provider)
- **Outgoing:**
  - `ai_memory`: To AI Agent/Chain

**Tool Nodes:**
- **Incoming:** None (capability provider)
- **Outgoing:**
  - `ai_tool`: To AI Agent

---

## Best Practices Summary

### Node Configuration Best Practices

**1. Tool Descriptions:**
- Be extremely specific about when to use the tool
- Describe expected input format
- Give examples of appropriate use cases
- Mention when NOT to use the tool

**2. System Messages:**
- Clearly define agent role and capabilities
- List available tools and when to use them
- Set response style and formatting expectations
- Include ethical guidelines and limitations

**3. Memory Management:**
- Use Buffer Window for development/testing
- Use Postgres/Redis for production
- Set appropriate maxMessages based on use case
- Implement session ID strategy for multi-user systems

**4. Cost Optimization:**
- Use gpt-4o-mini for most tasks
- Set appropriate maxTokens limits
- Use temperature: 0 for factual queries
- Limit maxIterations to prevent excessive tool calls
- Consider caching for frequently accessed data

**5. Error Handling:**
- Validate tool inputs before API calls
- Handle API failures gracefully
- Set appropriate timeouts
- Log errors for debugging

**6. Security:**
- Never expose credentials in node parameters
- Validate all user inputs
- Implement rate limiting
- Use appropriate authentication methods
- Audit tool permissions

### Node Selection Guide

**Choose AI Agent when:**
- ✅ Need multi-step reasoning
- ✅ Require tool usage
- ✅ Building conversational interfaces
- ✅ Implementing RAG systems

**Choose Memory Buffer Window when:**
- ✅ Prototyping and testing
- ✅ Single-user conversations
- ✅ Short-term memory needs

**Choose Memory Postgres when:**
- ✅ Production applications
- ✅ Multi-user systems
- ✅ Need conversation history
- ✅ Persistent memory required

**Choose Tool HTTP Request when:**
- ✅ Integrating with REST APIs
- ✅ Need real-time data (weather, stocks, news)
- ✅ Search capabilities (Perplexity, Google)

**Choose Tool Code when:**
- ✅ Custom business logic
- ✅ Mathematical calculations
- ✅ Data transformations
- ✅ Complex string operations

**Choose Tool Vector Store when:**
- ✅ Document search and retrieval
- ✅ RAG implementations
- ✅ Knowledge base queries
- ✅ Semantic similarity search

### Workflow Validation Checklist

**Before deploying n8n workflows:**

**Connection Validation:**
- ✅ AI Agent has exactly 1 language model (or 2 with fallback)
- ✅ Maximum 1 memory connection per agent
- ✅ Maximum 1 output parser per agent
- ✅ All AI connections use correct connection types
- ✅ Chat Trigger connected via `main` to AI Agent

**Configuration Validation:**
- ✅ `promptType: "auto"` when using Chat Trigger
- ✅ `hasOutputParser: true` when Output Parser connected
- ✅ `streamResponse` matches Chat Trigger `responseMode`
- ✅ Tool descriptions are clear and specific
- ✅ System message includes tool usage instructions

**Memory Validation:**
- ✅ Session ID strategy defined for multi-user systems
- ✅ `maxMessages` appropriate for use case
- ✅ Database credentials configured for persistent memory
- ✅ TTL settings appropriate for Redis memory

**Tool Validation:**
- ✅ Tool names use snake_case format
- ✅ Tool descriptions specify input format
- ✅ HTTP tools have proper authentication
- ✅ Response extraction configured correctly
- ✅ Error handling implemented for API calls

**Performance Validation:**
- ✅ `maxIterations` set to prevent runaway costs
- ✅ `maxTokens` limits configured appropriately
- ✅ Temperature settings match use case requirements
- ✅ Timeout values reasonable for expected response times

### Common Configuration Errors

**Error: "Language model connection required"**
- Cause: AI Agent missing `ai_languageModel` connection
- Fix: Connect OpenAI, Anthropic, or OpenRouter node to AI Agent

**Error: "Multiple memory connections not allowed"**
- Cause: >1 memory node connected to AI Agent
- Fix: Use only 1 memory node per agent

**Error: "Streaming mode mismatch"**
- Cause: Chat Trigger `responseMode: "streaming"` but Agent `streamResponse: false`
- Fix: Set both to matching streaming configuration

**Error: "Output parser required"**
- Cause: `hasOutputParser: true` but no parser connected
- Fix: Connect Output Parser node or set `hasOutputParser: false`

**Error: "Invalid session ID"**
- Cause: Memory node `sessionKey` expression returns undefined
- Fix: Verify `$json.sessionId` exists in input data

**Error: "Tool description missing"**
- Cause: Tool node missing or has empty description
- Fix: Add clear, specific description of when to use tool

### Integration Examples

**Basic Chat with Memory:**
```
[Chat Trigger] → [AI Agent] → [Response Output]
                      ↑
  [OpenAI GPT-4] ────┘
  [Postgres Memory] ─┘
```

**Multi-Tool Research Agent:**
```
[Chat Trigger] → [AI Agent] → [Response Output]
                      ↑
  [OpenAI GPT-4] ────┤
  [Postgres Memory] ─┤
  [Perplexity Tool] ─┤
  [Calculator Tool] ─┤
  [Vector Store Tool]┘
```

**RAG System:**
```
[Document Loader] → [Text Splitter] → [Embeddings] → [Qdrant Store]
                                                            ↓ (ai_tool)
[Chat Trigger] → [AI Agent] ← ────────────────── [Vector Store Tool]
                      ↑
  [OpenAI GPT-4] ────┘
  [Postgres Memory] ─┘
```

**Structured Output Extraction:**
```
[Chat Trigger] → [AI Agent] → [Database Insert]
                      ↑
  [OpenAI GPT-4] ────┤
  [Output Parser] ───┘ (hasOutputParser: true)
```

---

**Navigation:**
- **Previous**: [Part 2 - Memory & Tool Nodes](02_Memory_Tool_Nodes.md)
- **Current**: Part 3 - Output Parsers & Best Practices
- **Overview**: [Part 1 - Core Nodes](01_Core_Nodes.md)

---
**Document Version:** 1.0 (Part 3 of 3)
**Last Updated:** 2025-10-25
**Lines:** 347 / 500 limit
**Total Nodes Documented:** 15+
**Configuration Examples:** 25+
