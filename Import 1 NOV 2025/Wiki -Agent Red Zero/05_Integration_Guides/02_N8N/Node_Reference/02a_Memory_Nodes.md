---
title: N8N Node Reference - Part 2a - Memory Nodes
category: 05_Integration_Guides/02_N8N/Node_Reference
last_updated: 2025-10-25
line_count: 295
status: published
tags: [n8n, langchain, memory, postgres, redis, buffer, chat-history]
part: 2a
total_parts: 4
---

# n8n LangChain Node Configuration Reference - Part 2a: Memory Nodes

**Navigation:**
- **Previous**: [Part 1 - Core Nodes](01_Core_Nodes.md)
- **Current**: Part 2a - Memory Nodes
- **Next**: [Part 2b - Tool Nodes](02b_Tool_Nodes.md)

---

Comprehensive reference for n8n LangChain memory nodes with configuration details and best practices.

## Table of Contents
1. [Memory Buffer Window](#memory-buffer-window)
2. [Memory Postgres Chat](#memory-postgres-chat)
3. [Memory Redis Chat](#memory-redis-chat)
4. [Memory Manager](#memory-manager)

---

## Memory Buffer Window
**Node Type:** `@n8n/n8n-nodes-langchain.memoryBufferWindow`
**Version:** 1.2
**Purpose:** In-memory conversation history (non-persistent)

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

**Parameters:**
- `options.maxMessages` (number): Number of messages to keep
  - Default: `10` (5 user + 5 assistant messages)
  - Range: `1-100`
  - Higher values = more context but slower/costlier

- `options.returnMessages` (boolean): Return message objects or strings
  - `true` - Return full message objects with role and metadata (recommended)
  - `false` - Return simple string concatenation

**Memory Structure:**
```json
[
  {
    "role": "user",
    "content": "What's the weather?",
    "timestamp": "2025-10-18T10:00:00Z"
  },
  {
    "role": "assistant",
    "content": "I'll search for current weather...",
    "timestamp": "2025-10-18T10:00:02Z"
  }
]
```

**Connection Types:**
- **Outgoing:** `ai_memory` → AI Agent or Chain nodes

**Use Cases:**
- ✅ Development and testing
- ✅ Single-session conversations
- ✅ Prototypes and demos

**Limitations:**
- ⚠️ Memory clears when workflow restarts
- ⚠️ Not suitable for production multi-user systems
- ⚠️ Cannot persist across n8n restarts

---

## Memory Postgres Chat
**Node Type:** `@n8n/n8n-nodes-langchain.memoryPostgresChat`
**Version:** 1.0
**Purpose:** PostgreSQL-backed persistent memory

```json
{
  "name": "Postgres Memory",
  "type": "@n8n/n8n-nodes-langchain.memoryPostgresChat",
  "typeVersion": 1.0,
  "position": [250, 450],
  "parameters": {
    "tableName": "chat_memory",
    "sessionIdType": "customKey",
    "sessionKey": "={{ $json.sessionId }}",
    "options": {
      "maxMessages": 20,
      "returnMessages": true
    }
  },
  "credentials": {
    "postgres": {
      "id": "postgres-credential-id",
      "name": "PostgreSQL"
    }
  }
}
```

**Parameters:**
- `tableName` (string): PostgreSQL table name for storing messages
  - Default: `"chat_memory"`
  - Table auto-created if not exists

- `sessionIdType` (enum): How to identify conversation sessions
  - `"fromInput"` - Use sessionId from input data (recommended)
  - `"customKey"` - Define custom expression in `sessionKey`
  - `"workflowId"` - Use workflow ID (all conversations share memory)

- `sessionKey` (string): n8n expression for session ID
  - Example: `"={{ $json.sessionId }}"` (from Chat Trigger)
  - Example: `"={{ $json.userId }}"` (user-specific conversations)
  - Example: `"user_{{ $json.email }}"` (email-based sessions)

- `options.maxMessages` (number): Messages to load from database
  - Default: `20`
  - Range: `1-1000`
  - Loads most recent N messages for context

- `options.returnMessages` (boolean): Same as Buffer Window

**Database Schema:**
```sql
CREATE TABLE chat_memory (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(255) NOT NULL,
  message_type VARCHAR(50) NOT NULL,  -- 'user' or 'assistant'
  content TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_session_id (session_id),
  INDEX idx_created_at (created_at)
);
```

**Credentials (PostgreSQL):**
```
Host: postgres-shared
Port: 5432
Database: agentzero
User: agentzero
Password: agentzero123
SSL: false (for local Docker)
```

**Connection Types:**
- **Outgoing:** `ai_memory` → AI Agent

**Use Cases:**
- ✅ Production chat applications
- ✅ Multi-user conversation persistence
- ✅ Conversation history analysis
- ✅ Session resumption after restarts

**Advantages:**
- ✅ Persistent across workflow/n8n restarts
- ✅ Per-user conversation isolation
- ✅ Queryable conversation history
- ✅ Scalable for high-volume applications

**Querying Conversation History:**
```sql
-- Get all conversations for a user
SELECT * FROM chat_memory
WHERE session_id = 'user_jim@example.com'
ORDER BY created_at DESC;

-- Get conversation summary
SELECT
  session_id,
  COUNT(*) as message_count,
  MIN(created_at) as first_message,
  MAX(created_at) as last_message
FROM chat_memory
GROUP BY session_id;
```

---

## Memory Redis Chat
**Node Type:** `@n8n/n8n-nodes-langchain.memoryRedisChat`
**Version:** 1.0
**Purpose:** Redis-backed high-performance memory

```json
{
  "name": "Redis Memory",
  "type": "@n8n/n8n-nodes-langchain.memoryRedisChat",
  "typeVersion": 1.0,
  "position": [250, 450],
  "parameters": {
    "sessionIdType": "customKey",
    "sessionKey": "={{ $json.sessionId }}",
    "options": {
      "maxMessages": 15,
      "ttl": 86400
    }
  },
  "credentials": {
    "redis": {
      "id": "redis-credential-id",
      "name": "Redis"
    }
  }
}
```

**Additional Parameters:**
- `options.ttl` (number): Time-to-live in seconds
  - Default: `86400` (24 hours)
  - Memory auto-expires after TTL
  - Useful for temporary sessions

**Advantages over Postgres:**
- ✅ Faster read/write performance
- ✅ Lower latency for real-time chat
- ✅ Built-in TTL for automatic cleanup
- ✅ Simpler data structure (key-value)

**Use Cases:**
- ✅ High-traffic chat applications
- ✅ Real-time customer support
- ✅ Temporary conversation sessions
- ✅ Cache-like memory patterns

---

## Memory Manager
**Node Type:** `@n8n/n8n-nodes-langchain.memoryManager`
**Version:** 1.0
**Purpose:** Advanced memory with summarization and filtering

```json
{
  "name": "Smart Memory Manager",
  "type": "@n8n/n8n-nodes-langchain.memoryManager",
  "typeVersion": 1.0,
  "position": [250, 450],
  "parameters": {
    "options": {
      "maxTokenLimit": 2000,
      "summarizationThreshold": 0.8,
      "importanceScoring": true
    }
  }
}
```

**Advanced Parameters:**
- `maxTokenLimit` (number): Maximum tokens in memory context
  - Automatically summarizes when exceeded
  - Prevents context window overflow

- `summarizationThreshold` (number, 0-1): When to trigger summarization
  - `0.8` = Summarize at 80% of maxTokenLimit
  - Uses LLM to create concise summaries

- `importanceScoring` (boolean): Score message importance
  - Filter less relevant messages
  - Prioritize key information

**Use Cases:**
- ✅ Long conversations (>100 messages)
- ✅ Cost optimization (reduce context tokens)
- ✅ Intelligent memory management
- ✅ Summary-based context retention

---

**Navigation:**
- **Previous**: [Part 1 - Core Nodes](01_Core_Nodes.md)
- **Current**: Part 2a - Memory Nodes
- **Next**: [Part 2b - Tool Nodes](02b_Tool_Nodes.md)

---
**Document Version:** 1.0 (Part 2a of 4)
**Last Updated:** 2025-10-25
**Lines:** 295 / 500 limit
