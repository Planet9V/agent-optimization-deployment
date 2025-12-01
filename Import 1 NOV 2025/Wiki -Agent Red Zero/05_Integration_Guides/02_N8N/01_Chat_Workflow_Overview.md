---
title: n8n Chat Workflow with Memory and Perplexity - Part 1 of 2
category: 05_Integration_Guides/02_N8N
last_updated: 2025-10-25
line_count: 330
status: published
tags: [n8n, workflow, chat, langchain, memory, perplexity, integration]
part: 1
total_parts: 2
series: N8N_CHAT_WORKFLOW_SPECIFICATION
---

# n8n Chat Workflow with Memory and Perplexity - Part 1 of 2

**Series**: n8n Chat Workflow Specification
**Navigation**: [Next Part](./02_Chat_Workflow_Implementation.md)

---

## Overview
This document specifies a complete chat workflow implementation in n8n with conversational memory and Perplexity AI search integration, based on comprehensive research of n8n's LangChain capabilities.

## Research Summary

### Available n8n Nodes for Chat Workflows

#### 1. **Chat Trigger Nodes**
- **Chat Trigger** (`ChatTrigger.node.js`) - Main entry point for chat interfaces
- **Manual Chat Trigger** (`ManualChatTrigger.node.js`) - Testing and manual execution

#### 2. **Language Model Nodes** (LangChain Package)
- **LM Chat OpenAI** (`@n8n/n8n-nodes-langchain.lmChatOpenAi`) - OpenAI GPT models
- **LM Chat Anthropic** (`@n8n/n8n-nodes-langchain.lmChatAnthropic`) - Claude models
- **LM Chat OpenRouter** (`@n8n/n8n-nodes-langchain.lmChatOpenRouter`) - Multi-provider access
- **OpenAI Assistant** (`OpenAiAssistant.node.js`) - OpenAI Assistants API

#### 3. **Memory Nodes** (Conversational Context)
- **Memory Buffer Window** (`MemoryBufferWindow.node.js`) - In-memory conversation history (simple)
- **Memory Manager** (`MemoryManager.node.js`) - Advanced memory management
- **Memory Postgres Chat** (`MemoryPostgresChat.node.js`) - PostgreSQL persistence
- **Memory Redis Chat** (`MemoryRedisChat.node.js`) - Redis persistence
- **Memory MongoDB Chat** (`MemoryMongoDbChat.node.js`) - MongoDB persistence
- **Memory Zep** (`MemoryZep.node.js`) - Zep long-term memory service
- **Memory Motorhead** (`MemoryMotorhead.node.js`) - Motorhead memory service
- **Memory Xata** (`MemoryXata.node.js`) - Xata serverless database

#### 4. **AI Agent Node**
- **AI Agent** (`@n8n/n8n-nodes-langchain.agent`) - Orchestrates LLM + Tools + Memory
  - Two modes: `auto` (from Chat Trigger) or `define` (custom prompts)
  - Connects to language models, tools, memory, and output parsers
  - Supports streaming for real-time responses

#### 5. **Tool Nodes** (For AI Agent)
- **Tool HTTP Request** (`ToolHttpRequest.node.js`) - HTTP API calls (Perplexity!)
- **Tool Code** (`ToolCode.node.js`) - Custom JavaScript/Python code
- **Tool Vector Store** (`ToolVectorStore.node.js`) - Semantic search/RAG

#### 6. **Supporting Nodes**
- **HTTP Request** (`n8n-nodes-base.httpRequest`) - Standard HTTP calls
- **Output Parser Structured** - Extract structured data from LLM responses
- **Information Extractor** - Extract specific information from text

### Key Architecture Insights from Research

**AI-Specific Connection Flow:**
```
Unlike standard n8n nodes where data flows FROM source TO target,
AI-specific connections flow TO the AI Agent/Chain nodes:

[Chat Trigger] --main--> [AI Agent]           (data input)
[LM Chat OpenAI] --ai_languageModel--> [AI Agent]  (LLM capability)
[Memory Buffer] --ai_memory--> [AI Agent]      (conversational context)
[Tool HTTP] --ai_tool--> [AI Agent]            (search capability)
```

**Memory Connection Rules:**
- AI Agent can have **maximum 1 memory connection** (validated by n8n-mcp)
- Memory persists conversation history across chat sessions
- Memory Buffer Window = simple in-memory (good for prototypes)
- Postgres/Redis/MongoDB = production-grade persistence

**Streaming Configuration:**
- Chat Trigger: `responseMode: "streaming"` for real-time responses
- AI Agent: `streamResponse: true` when using streaming
- **Critical**: Cannot use streaming with certain output parsers

## Workflow Architecture

### Option 1: Simple Chat with In-Memory Context (Recommended for Start)

**Workflow Name:** "Simple AI Chat with Memory and Search"

**Node Flow:**
```
[Manual Chat Trigger]
  ↓ (main)
[AI Agent]
  ← (ai_languageModel) [LM Chat OpenAI]
  ← (ai_memory) [Memory Buffer Window]
  ← (ai_tool) [Tool HTTP Request: Perplexity]
```

**Advantages:**
- ✅ Simple setup, no external database required
- ✅ Fast testing and iteration
- ✅ All-in-one workflow for learning
- ✅ Memory persists during workflow execution

**Limitations:**
- ⚠️ Memory clears when workflow restarts
- ⚠️ Not suitable for production multi-user scenarios

### Option 2: Production Chat with Persistent Memory

**Workflow Name:** "Production AI Chat with Postgres Memory"

**Node Flow:**
```
[Chat Trigger]
  ↓ (main)
[AI Agent]
  ← (ai_languageModel) [LM Chat OpenAI]
  ← (ai_memory) [Memory Postgres Chat]  ← [Postgres DB Connection]
  ← (ai_tool) [Tool HTTP Request: Perplexity]
```

**Advantages:**
- ✅ Persistent memory across sessions
- ✅ Multi-user support with session IDs
- ✅ Production-ready scalability
- ✅ Can query conversation history

**Requirements:**
- PostgreSQL database (already available in docker-compose.yml!)
- Database connection configuration

## Detailed Node Configuration

### 1. Manual Chat Trigger Configuration
```json
{
  "name": "Chat Interface",
  "type": "@n8n/n8n-nodes-langchain.manualChatTrigger",
  "typeVersion": 1.1,
  "position": [250, 300],
  "parameters": {
    "options": {}
  }
}
```

### 2. AI Agent Configuration
```json
{
  "name": "AI Chat Agent",
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 2.1,
  "position": [450, 300],
  "parameters": {
    "promptType": "auto",
    "text": "",
    "hasOutputParser": false,
    "options": {
      "systemMessage": "You are a helpful AI assistant with access to real-time information via Perplexity search. When answering questions:\n\n1. Use your knowledge for general information\n2. Use the Perplexity search tool for current events, recent data, or fact-checking\n3. Maintain context from previous messages in the conversation\n4. Be concise but thorough\n5. Cite sources when using search results\n\nRemember the conversation history and reference it when relevant.",
      "maxIterations": 10,
      "returnIntermediateSteps": true
    }
  }
}
```

**Critical AI Agent Properties:**
- `promptType: "auto"` - Gets input from Chat Trigger automatically
- `systemMessage` - Defines agent behavior and tool usage instructions
- `maxIterations: 10` - Allows multi-step reasoning (tool call → analyze → answer)
- `returnIntermediateSteps` - Shows thinking process (useful for debugging)

### 3. LM Chat OpenAI Configuration
```json
{
  "name": "OpenAI GPT-4",
  "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
  "typeVersion": 1.2,
  "position": [250, 150],
  "parameters": {
    "model": "gpt-4o-mini",
    "options": {
      "temperature": 0.7,
      "maxTokens": 1000,
      "topP": 1
    }
  },
  "credentials": {
    "openAiApi": {
      "id": "openai-credentials-id",
      "name": "OpenAI API"
    }
  }
}
```

**Model Selection:**
- `gpt-4o-mini` - Fast, cost-effective, good quality (recommended)
- `gpt-4o` - Maximum capability, higher cost
- `gpt-3.5-turbo` - Budget option

**Alternative: Use OpenRouter for Multi-Provider Access**
```json
{
  "name": "OpenRouter (Multi-Model)",
  "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
  "typeVersion": 1.0,
  "parameters": {
    "model": "perplexity/llama-3.1-sonar-small-128k-online",
    "options": {
      "temperature": 0.7
    }
  },
  "credentials": {
    "openRouterApi": {
      "id": "openrouter-credentials-id",
      "name": "OpenRouter API"
    }
  }
}
```

**Note:** OpenRouter gives access to Perplexity models directly via LLM, but we'll use Tool HTTP Request for explicit search control.

### 4. Memory Buffer Window Configuration (Option 1)
```json
{
  "name": "Conversation Memory",
  "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
  "typeVersion": 1.2,
  "position": [250, 450],
  "parameters": {
    "options": {
      "maxMessages": 10,
      "returnMessages": true
    }
  }
}
```

**Memory Properties:**
- `maxMessages: 10` - Keeps last 10 messages (5 exchanges)
- `returnMessages: true` - Returns full message objects with metadata
- In-memory storage - fast but non-persistent

### 4-ALT. Memory Postgres Chat Configuration (Option 2)
```json
{
  "name": "Postgres Conversation Memory",
  "type": "@n8n/n8n-nodes-langchain.memoryPostgresChat",
  "typeVersion": 1.0,
  "position": [250, 450],
  "parameters": {
    "tableName": "chat_memory",
    "sessionIdType": "customKey",
    "sessionKey": "={{ $json.sessionId }}",
    "options": {
      "maxMessages": 20
    }
  },
  "credentials": {
    "postgres": {
      "id": "postgres-credentials-id",
      "name": "PostgreSQL AgentZero"
    }
  }
}
```

**Postgres Memory Advantages:**
- Persistent across workflow restarts
- Multi-session support via `sessionId`
- Can query conversation history directly in PostgreSQL
- Production-ready scaling

**Database Connection:**
```
Host: postgres-shared
Port: 5432
Database: agentzero
User: agentzero
Password: agentzero123
```

### 5. Tool HTTP Request: Perplexity Search Configuration
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
      "id": "perplexity-credentials-id",
      "name": "Perplexity API"
    }
  }
}
```

**Perplexity Tool Configuration Explanation:**
- `name: "perplexity_search"` - Tool identifier for AI Agent
- `description` - Instructions for when AI should use this tool
- `model: "llama-3.1-sonar-small-128k-online"` - Perplexity's online search model
- `return_citations: true` - Include source URLs in responses
- `temperature: 0.2` - Lower temperature for factual accuracy
- `jsonOutput` - Extracts answer from Perplexity response

**Perplexity API Credentials:**
```
Type: HTTP Header Auth
Header Name: Authorization
Header Value: Bearer YOUR_PERPLEXITY_API_KEY
```

**Get Perplexity API Key:** https://www.perplexity.ai/settings/api

**Perplexity Pricing (as of 2025):**
- Sonar Small Online: $0.20 per 1M tokens (very affordable)
- Sonar Large Online: $1.00 per 1M tokens

---

**Navigation**: [Next Part](./02_Chat_Workflow_Implementation.md)
**Line Range**: 1-330 of 656 total lines
