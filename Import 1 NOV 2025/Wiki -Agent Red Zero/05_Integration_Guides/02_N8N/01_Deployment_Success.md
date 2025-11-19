---
title: n8n Chat Workflow Deployment Success
category: 05_Integration_Guides/02_N8N
last_updated: 2025-10-25
line_count: 320
status: published
tags: [n8n, deployment, workflow, chatbot, langchain]
---

# n8n Chat Workflow Deployment - SUCCESS ✅

## Deployment Summary

**Status:** ✅ **SUCCESSFULLY DEPLOYED**
**Workflow ID:** `vTKLEeEORD6IHoQ9`
**Workflow Name:** `AI Chat with Memory and Perplexity Search`
**Created:** 2025-10-18 06:59:56 UTC
**Active:** Not yet activated (requires credentials)

## Deployed Nodes

### 1. Chat Interface ✅
- **Type:** `@n8n/n8n-nodes-langchain.manualChatTrigger`
- **Version:** 1.1
- **Node ID:** `22f1ac2c-dac3-4b5f-93b3-bc1ce115fe98`
- **Position:** [250, 300]
- **Status:** Deployed successfully
- **Configuration:** Default manual chat trigger settings

### 2. OpenAI GPT-4 ✅
- **Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- **Version:** 1.2
- **Node ID:** `5bceb071-5c9f-4287-b1bb-c1a373abb18d`
- **Position:** [250, 150]
- **Model:** `gpt-4o-mini`
- **Temperature:** 0.7
- **Max Tokens:** 1000
- **Status:** Deployed successfully
- **⚠️ Requires:** OpenAI API credentials

### 3. Conversation Memory ✅
- **Type:** `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- **Version:** 1.2
- **Node ID:** `488d37de-229c-44ff-936f-4ec79cb99aa8`
- **Position:** [250, 450]
- **Max Messages:** 10 (5 exchanges)
- **Status:** Deployed successfully
- **Storage:** In-memory (non-persistent)

### 4. Perplexity Search ✅
- **Type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
- **Version:** 1.1
- **Node ID:** `60509c5f-ae55-43d7-9bdf-3632c0505d26`
- **Position:** [250, 600]
- **Tool Name:** `perplexity_search`
- **API:** https://api.perplexity.ai/chat/completions
- **Model:** `llama-3.1-sonar-small-128k-online`
- **Status:** Deployed successfully
- **⚠️ Requires:** Perplexity API credentials (HTTP Header Auth)

### 5. AI Chat Agent ✅
- **Type:** `@n8n/n8n-nodes-langchain.agent`
- **Version:** 2.1
- **Node ID:** `42d40e4f-94cd-4918-b1f8-0286351d8fa9`
- **Position:** [450, 300]
- **Prompt Type:** Auto (from Chat Trigger)
- **Max Iterations:** 10
- **System Message:** Configured with tool usage instructions
- **Status:** Deployed successfully

## Connection Topology ✅

All connections successfully configured:

```
[Chat Interface] --main--> [AI Chat Agent]
                              ↑
        [OpenAI GPT-4] --ai_languageModel--┘
        [Conversation Memory] --ai_memory---┘
        [Perplexity Search] --ai_tool-------┘
```

**Connection Details:**
1. ✅ Chat Interface → AI Chat Agent (main)
2. ✅ OpenAI GPT-4 → AI Chat Agent (ai_languageModel)
3. ✅ Conversation Memory → AI Chat Agent (ai_memory)
4. ✅ Perplexity Search → AI Chat Agent (ai_tool)

## Validation Results ✅

All n8n-mcp validation rules passed:

- ✅ AI Agent has exactly 1 language model connection
- ✅ AI Agent has maximum 1 memory connection
- ✅ AI Agent promptType is "auto" (from Chat Trigger)
- ✅ Chat Trigger → AI Agent main connection exists
- ✅ Tool has clear description for AI understanding
- ✅ System message provides tool usage instructions
- ✅ All node types and versions are valid
- ✅ All connection types are correct (main, ai_languageModel, ai_memory, ai_tool)

## Required Next Steps

### Step 1: Configure OpenAI Credentials

1. **Access n8n UI:**
   ```
   URL: http://localhost:5678
   Username: jims67mustang
   Password: Jimmy123$
   ```

2. **Add OpenAI Credential:**
   - Navigate to: Settings → Credentials
   - Click: "Add Credential"
   - Select: "OpenAI API"
   - Enter:
     - **Name:** "OpenAI API"
     - **API Key:** Get from https://platform.openai.com/api-keys
   - Click: "Save"

3. **Assign to Node:**
   - Open workflow: "AI Chat with Memory and Perplexity Search"
   - Click on: "OpenAI GPT-4" node
   - In "Credential to connect with" dropdown: Select your OpenAI credential
   - Click: "Save" (top right)

### Step 2: Configure Perplexity Credentials

1. **Get Perplexity API Key:**
   - Visit: https://www.perplexity.ai/settings/api
   - Create API key if needed
   - Copy the key (format: `pplx-xxxxxxxxxxxxx`)

2. **Add HTTP Header Auth Credential:**
   - Navigate to: Settings → Credentials
   - Click: "Add Credential"
   - Select: "HTTP Header Auth"
   - Enter:
     - **Name:** "Perplexity API"
     - **Header Name:** `Authorization`
     - **Header Value:** `Bearer YOUR_PERPLEXITY_API_KEY`
   - Click: "Save"

3. **Assign to Node:**
   - Open workflow: "AI Chat with Memory and Perplexity Search"
   - Click on: "Perplexity Search" node
   - In "Credential to connect with" dropdown: Select your Perplexity credential
   - Click: "Save" (top right)

### Step 3: Test the Workflow

1. **Open Workflow:**
   - Navigate to: Workflows
   - Click: "AI Chat with Memory and Perplexity Search"

2. **Execute Test:**
   - Click: "Test Workflow" button (top right)
   - In "Chat Interface" input, enter: "Hello, what can you help me with?"
   - Click: "Send"
   - Observe: AI response with capabilities explanation

3. **Test Memory:**
   - Enter: "My name is Jim"
   - Wait for response
   - Enter: "What's my name?"
   - Expected: AI correctly recalls "Jim"

4. **Test Perplexity Search:**
   - Enter: "What are the latest AI developments this week?"
   - Expected: AI uses Perplexity tool, returns recent news with citations
   - Look for: Intermediate steps showing tool calls

5. **Test Multi-Turn Context:**
   - Enter: "Tell me about Paris"
   - Then enter: "What's the weather there today?"
   - Expected: AI understands "there" refers to Paris from context

### Step 4: Activate Workflow (Optional)

Once testing is complete:

1. **Via n8n UI:**
   - Toggle "Active" switch to ON (top right of workflow editor)

2. **Via API:**
   ```bash
   curl -X PATCH http://localhost:5678/api/v1/workflows/vTKLEeEORD6IHoQ9 \
     -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json" \
     -d '{"active": true}'
   ```

## Workflow Access

### n8n UI Access
```
URL: http://localhost:5678
Workflow ID: vTKLEeEORD6IHoQ9
Direct Link: http://localhost:5678/workflow/vTKLEeEORD6IHoQ9
```

### API Access
```bash
# Get workflow details
curl http://localhost:5678/api/v1/workflows/vTKLEeEORD6IHoQ9 \
  -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Execute workflow manually
curl -X POST http://localhost:5678/api/v1/workflows/vTKLEeEORD6IHoQ9/executions \
  -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"data": {"chatInput": "Hello!"}}'
```

## System Message Configuration

The AI Agent is configured with the following system message:

```
You are a helpful AI assistant with access to real-time information via
Perplexity search. When answering questions:

1) Use your knowledge for general information
2) Use the perplexity_search tool for current events or fact-checking
3) Maintain context from conversation history
4) Be concise but thorough
5) Cite sources when using search.
```

This can be customized by editing the "AI Chat Agent" node's "System Message" parameter.

## Cost Estimation

**Expected costs for moderate usage (~1,000 messages/month):**

- **OpenAI GPT-4o-mini:**
  - Input: ~$0.015/month
  - Output: ~$0.06/month
  - Subtotal: ~$0.08/month

- **Perplexity Sonar Small:**
  - ~$0.05/month (assuming 30% of queries trigger search)

**Total: ~$0.13/month for testing (1K messages)**
**Total: ~$1.30/month for light production (10K messages)**

## Troubleshooting

### Issue: "Missing credentials" error
**Solution:** Follow Step 1 and Step 2 above to configure OpenAI and Perplexity credentials

### Issue: "Node execution failed"
**Solution:**
1. Check credential configuration
2. Verify API keys are valid
3. Check API rate limits
4. Review error message in execution log

### Issue: AI doesn't use Perplexity search
**Solution:**
1. Ask questions that require current information (e.g., "What happened in AI this week?")
2. Check "Perplexity Search" node is properly connected to AI Agent
3. Verify credential is assigned to Perplexity node

### Issue: Memory not persisting
**Solution:**
- Memory Buffer Window clears on workflow restart (expected behavior)
- For persistent memory, upgrade to Postgres Memory (see specification doc)

### Issue: Can't access n8n UI
**Solution:**
```bash
# Check n8n is running
docker ps | grep n8n

# Restart if needed
docker restart n8n

# Check logs
docker logs n8n
```

## Upgrade Path: Production Memory

To upgrade to persistent PostgreSQL memory:

1. **Create Memory Postgres Chat node** instead of Buffer Window
2. **Configure PostgreSQL connection:**
   ```
   Host: postgres-shared
   Port: 5432
   Database: agentzero
   User: agentzero
   Password: agentzero123
   ```
3. **Set session management:**
   - Session ID Type: `customKey`
   - Session Key: `={{ $json.sessionId }}`
4. **Replace connection:** Postgres Memory → AI Agent (ai_memory)

## Related Topics

- [Chat Workflow Specification](02_Chat_Workflow_Spec/01_Overview_and_Configuration.md)
- [LangChain Node Reference](07_LangChain_Node_Reference/01_Core_Components.md)
- [MCP Installation Guide](05_Installation_Guide.md)

## Success Metrics

✅ **Workflow Created:** 2025-10-18 06:59:56 UTC
✅ **All 5 Nodes Deployed:** Manual Chat Trigger, OpenAI, Memory, Perplexity, AI Agent
✅ **All 4 Connections Configured:** main, ai_languageModel, ai_memory, ai_tool
✅ **Validation Passed:** All n8n-mcp rules satisfied
✅ **Ready for Testing:** Awaiting credential configuration

## Next Actions

1. ⏳ **Configure OpenAI credentials** (Step 1)
2. ⏳ **Configure Perplexity credentials** (Step 2)
3. ⏳ **Test workflow** (Step 3)
4. ⏳ **Activate workflow** (Step 4 - optional)

---
**Last Updated:** 2025-10-25 | **Lines:** 320/400 | **Status:** published
**Deployment Status:** ✅ SUCCESS
**Workflow ID:** `vTKLEeEORD6IHoQ9`
