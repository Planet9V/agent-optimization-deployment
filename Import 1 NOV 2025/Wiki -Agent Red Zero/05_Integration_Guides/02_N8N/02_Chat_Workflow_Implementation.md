---
title: n8n Chat Workflow with Memory and Perplexity - Part 2 of 2
category: 05_Integration_Guides/02_N8N
last_updated: 2025-10-25
line_count: 326
status: published
tags: [n8n, workflow, deployment, testing, troubleshooting]
part: 2
total_parts: 2
series: N8N_CHAT_WORKFLOW_SPECIFICATION
---

# n8n Chat Workflow with Memory and Perplexity - Part 2 of 2

**Series**: n8n Chat Workflow Specification
**Navigation**: [Previous Part](./01_Chat_Workflow_Overview.md)

---

## Complete Workflow JSON (Option 1: Simple)

```json
{
  "name": "Simple AI Chat with Memory and Search",
  "nodes": [
    {
      "name": "Chat Interface",
      "type": "@n8n/n8n-nodes-langchain.manualChatTrigger",
      "typeVersion": 1.1,
      "position": [250, 300],
      "parameters": {
        "options": {}
      }
    },
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
    },
    {
      "name": "OpenAI GPT-4",
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
      "typeVersion": 1.2,
      "position": [250, 150],
      "parameters": {
        "model": "gpt-4o-mini",
        "options": {
          "temperature": 0.7,
          "maxTokens": 1000
        }
      },
      "credentials": {
        "openAiApi": {
          "id": "{{ $credentials.openAiApi.id }}",
          "name": "OpenAI API"
        }
      }
    },
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
    },
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
          "id": "{{ $credentials.httpHeaderAuth.id }}",
          "name": "Perplexity API"
        }
      }
    }
  ],
  "connections": {
    "Chat Interface": {
      "main": [
        [
          {
            "node": "AI Chat Agent",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "OpenAI GPT-4": {
      "ai_languageModel": [
        [
          {
            "node": "AI Chat Agent",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "Conversation Memory": {
      "ai_memory": [
        [
          {
            "node": "AI Chat Agent",
            "type": "ai_memory",
            "index": 0
          }
        ]
      ]
    },
    "Perplexity Search": {
      "ai_tool": [
        [
          {
            "node": "AI Chat Agent",
            "type": "ai_tool",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "tags": []
}
```

## Validation Checklist

Based on n8n-mcp validation rules, ensure:

- ✅ **AI Agent has exactly 1 language model connection** (OpenAI GPT-4)
- ✅ **AI Agent has maximum 1 memory connection** (Conversation Memory)
- ✅ **AI Agent promptType is "auto"** (gets input from Chat Trigger)
- ✅ **Chat Trigger → AI Agent main connection exists**
- ✅ **Tool HTTP Request has clear description** for AI to understand when to use it
- ✅ **Memory configuration is appropriate** (Buffer Window for simple, Postgres for production)
- ✅ **System message provides clear instructions** on tool usage and behavior

## Testing Plan

### Test Case 1: Basic Conversation
**User:** "Hello, what can you help me with?"
**Expected:** AI introduces itself and explains capabilities

### Test Case 2: Memory Retention
**User:** "My name is Jim"
**AI:** Acknowledges
**User:** "What's my name?"
**Expected:** AI correctly recalls "Jim" from memory

### Test Case 3: Perplexity Search Activation
**User:** "What are the latest AI developments this week?"
**Expected:** AI uses Perplexity tool, returns recent news with citations

### Test Case 4: Multi-Turn with Context
**User:** "Tell me about Paris"
**AI:** General information about Paris
**User:** "What's the weather there today?"
**Expected:** AI uses Perplexity for current weather in Paris (remembering Paris from context)

### Test Case 5: Fact-Checking
**User:** "Is it true that AI can now solve complex math theorems?"
**Expected:** AI uses Perplexity to fact-check recent AI math achievements

## Deployment Steps

### 1. Prerequisites
- ✅ n8n instance running (port 5678) - CONFIRMED
- ✅ n8n API key configured - CONFIRMED
- ⚠️ OpenAI API key - REQUIRED
- ⚠️ Perplexity API key - REQUIRED

### 2. Create Credentials in n8n

**OpenAI Credentials:**
1. n8n UI → Settings → Credentials → Add Credential
2. Select "OpenAI API"
3. Enter API Key from https://platform.openai.com/api-keys
4. Save

**Perplexity Credentials:**
1. n8n UI → Settings → Credentials → Add Credential
2. Select "HTTP Header Auth"
3. Name: "Perplexity API"
4. Header Name: "Authorization"
5. Header Value: "Bearer YOUR_PERPLEXITY_API_KEY"
6. Save

### 3. Create Workflow
```bash
# Using n8n API
curl -X POST http://n8n:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: YOUR_N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @simple_chat_workflow.json
```

### 4. Activate Workflow
```bash
# Activate the workflow
curl -X PATCH http://n8n:5678/api/v1/workflows/{workflowId} \
  -H "X-N8N-API-KEY: YOUR_N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true}'
```

### 5. Test via n8n UI
1. Open workflow in n8n UI
2. Click "Test Workflow"
3. Enter chat message in Manual Chat Trigger
4. Observe AI Agent processing and responses

## Advanced Enhancements

### Enhancement 1: Add RAG (Retrieval Augmented Generation)
Add **Tool Vector Store** node for document-based knowledge:
- Load documents into vector store
- AI can search documents when needed
- Combines with Perplexity for comprehensive knowledge

### Enhancement 2: Add Structured Output
Add **Output Parser Structured** for:
- Extract structured data from conversations
- Save to database
- Trigger automated actions

### Enhancement 3: Multi-User Session Management
Upgrade to **Memory Postgres Chat** with:
- User session IDs from webhook headers
- Per-user conversation persistence
- Conversation history API

### Enhancement 4: Webhook Integration
Replace Manual Chat Trigger with:
- **Webhook Trigger** for external applications
- **Chat Trigger** for n8n chat widget integration
- REST API endpoints for mobile apps

## Cost Estimation

**Monthly costs for moderate usage (~10,000 messages/month):**

- **OpenAI GPT-4o-mini**: ~$15/month
  - $0.150 per 1M input tokens
  - $0.600 per 1M output tokens
  - Average ~150 tokens per exchange

- **Perplexity Sonar Small Online**: ~$5/month
  - $0.20 per 1M tokens
  - Used only when search needed (~30% of queries)

- **PostgreSQL**: $0 (self-hosted in Docker)
- **n8n**: $0 (self-hosted in Docker)

**Total: ~$20/month for production usage**

## Troubleshooting

### Issue: AI Agent doesn't use Perplexity search
**Solution:** Improve tool description to be more specific about when to use it

### Issue: Memory not persisting
**Solution:** Check Memory Buffer Window is connected with `ai_memory` connection type, not `main`

### Issue: "No language model connected" error
**Solution:** Ensure OpenAI node is connected via `ai_languageModel` connection (not `main`)

### Issue: Perplexity tool returns errors
**Solution:**
1. Verify API key in HTTP Header Auth credentials
2. Check `jsonBody` expression syntax
3. Test Perplexity API directly with curl first

### Issue: Conversation context lost
**Solution:**
1. Check Memory node maxMessages is high enough
2. For production, switch to Postgres memory for persistence
3. Verify AI Agent systemMessage instructs to use conversation history

## References

- **n8n LangChain Documentation**: https://docs.n8n.io/integrations/langchain/
- **Perplexity API Docs**: https://docs.perplexity.ai/
- **OpenAI API Docs**: https://platform.openai.com/docs
- **n8n-mcp Repository**: https://github.com/czlonkowski/n8n-mcp
- **n8n Workflow Templates**: https://n8n.io/workflows/

## Next Steps

1. ✅ **Specification Complete** - This document
2. ⏳ **Create workflow JSON file** - Export to file for import
3. ⏳ **Set up credentials** - OpenAI and Perplexity API keys
4. ⏳ **Deploy workflow** - Upload to n8n via API
5. ⏳ **Test and validate** - Run all test cases
6. ⏳ **Monitor and optimize** - Track usage and costs

---

**Navigation**: [Previous Part](./01_Chat_Workflow_Overview.md)
**Line Range**: 331-656 of 656 total lines

**Document Version:** 1.0
**Created:** 2025-10-18
**Last Updated:** 2025-10-25
**Status:** Ready for Implementation
