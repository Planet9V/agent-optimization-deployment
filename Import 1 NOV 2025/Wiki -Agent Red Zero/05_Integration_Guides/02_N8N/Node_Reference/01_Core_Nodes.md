---
title: N8N Node Reference - Part 1 - Core Nodes
category: 05_Integration_Guides/02_N8N/Node_Reference
last_updated: 2025-10-25
line_count: 437
status: published
tags: [n8n, langchain, chat-triggers, ai-agent, language-models, openai, anthropic, openrouter]
part: 1
total_parts: 3
---

# n8n LangChain Node Configuration Reference - Part 1: Core Nodes

**Navigation:**
- **Current**: Part 1 - Core Nodes (Chat Triggers, AI Agent, Language Models)
- **Next**: [Part 2 - Memory & Tool Nodes](02_Memory_Tool_Nodes.md)
- **Overview**: [Part 3 - Output Parsers & Best Practices](03_Output_Parsers_Best_Practices.md)

---

Comprehensive reference for n8n LangChain core nodes with exact configuration details, parameter specifications, and usage patterns.

## Table of Contents - Part 1
1. [Chat Trigger Nodes](#chat-trigger-nodes)
2. [AI Agent & Orchestration](#ai-agent--orchestration)
3. [Language Model Nodes](#language-model-nodes)

---

## Chat Trigger Nodes

### Manual Chat Trigger
**Node Type:** `@n8n/n8n-nodes-langchain.manualChatTrigger`
**Version:** 1.1
**Purpose:** Testing and manual chat interaction

```json
{
  "name": "Manual Chat",
  "type": "@n8n/n8n-nodes-langchain.manualChatTrigger",
  "typeVersion": 1.1,
  "position": [250, 300],
  "parameters": {
    "options": {}
  }
}
```

**Parameters:**
- `options` (object, optional): Additional configuration options
  - Currently no specific options documented

**Output:** Emits chat messages with structure:
```json
{
  "chatInput": "user message text",
  "sessionId": "unique-session-id",
  "action": "sendMessage"
}
```

**Connection Types:**
- **Outgoing:** `main` → AI Agent or Chain nodes

**Use Cases:**
- ✅ Development and testing
- ✅ Manual workflow execution
- ✅ Debugging chat flows

---

### Chat Trigger
**Node Type:** `@n8n/n8n-nodes-langchain.chatTrigger`
**Version:** 1.0
**Purpose:** Production chat interface with streaming support

```json
{
  "name": "Chat Interface",
  "type": "@n8n/n8n-nodes-langchain.chatTrigger",
  "typeVersion": 1.0,
  "position": [250, 300],
  "parameters": {
    "public": false,
    "options": {
      "responseMode": "lastNode",
      "welcomeMessage": "Hello! How can I help you today?",
      "inputPlaceholder": "Type your message...",
      "allowFileUploads": false,
      "allowedFileTypes": []
    }
  }
}
```

**Parameters:**
- `public` (boolean): Make chat interface publicly accessible
- `options.responseMode` (string): How to handle responses
  - `"lastNode"` - Return output from last node (default)
  - `"streaming"` - Stream responses in real-time
- `options.welcomeMessage` (string): Initial greeting message
- `options.inputPlaceholder` (string): Input field placeholder text
- `options.allowFileUploads` (boolean): Enable file uploads in chat
- `options.allowedFileTypes` (array): Allowed file extensions (e.g., `["pdf", "txt"]`)

**Streaming Configuration:**
```json
{
  "options": {
    "responseMode": "streaming"
  }
}
```

**Critical Validation Rules:**
- ⚠️ When `responseMode: "streaming"`, AI Agent must have `streamResponse: true`
- ⚠️ Streaming mode incompatible with certain Output Parsers
- ⚠️ Must connect to AI Agent with `promptType: "auto"`

**Use Cases:**
- ✅ Production chat interfaces
- ✅ Customer support bots
- ✅ Real-time conversational AI

---

## AI Agent & Orchestration

### AI Agent
**Node Type:** `@n8n/n8n-nodes-langchain.agent`
**Version:** 2.1 (latest), also 2.0, 1.9, 1.8, 1.7
**Purpose:** Orchestrate LLM + Tools + Memory for complex reasoning

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
      "systemMessage": "You are a helpful assistant.",
      "maxIterations": 10,
      "returnIntermediateSteps": true,
      "streamResponse": false,
      "needsFallback": false
    }
  }
}
```

**Parameters:**

**Core Configuration:**
- `promptType` (enum): How AI receives user input
  - `"auto"` - Automatically from Chat Trigger (uses `$json.chatInput`)
  - `"define"` - Custom prompt defined in `text` parameter
- `text` (string): Custom prompt when `promptType: "define"`
  - Supports n8n expressions: `={{ $json.query }}`
- `hasOutputParser` (boolean): Whether Output Parser is connected
  - Set to `true` when connecting Output Parser node

**System Configuration (`options`):**
- `systemMessage` (string): Agent's role, capabilities, and behavior
  - **Critical**: Defines how agent uses tools, memory, and responds
  - Include tool usage instructions here
  - Example:
    ```
    You are an AI assistant with access to:
    1. Web search via Perplexity (use for current events)
    2. Vector database (use for internal documents)
    3. Conversation memory (reference previous messages)

    Always cite sources when using search results.
    ```

- `maxIterations` (number): Maximum tool calls per response
  - Default: `10`
  - Range: `1-100`
  - Higher values allow multi-step reasoning (search → analyze → search → answer)
  - Lower values prevent excessive API costs

- `returnIntermediateSteps` (boolean): Include reasoning process in output
  - `true` - Show all tool calls and reasoning steps (useful for debugging)
  - `false` - Return only final answer (cleaner for production)

- `streamResponse` (boolean): Enable response streaming
  - `true` - Stream tokens as they're generated (for Chat Trigger streaming)
  - `false` - Return complete response at once (default)
  - **Must match Chat Trigger `responseMode: "streaming"`**

- `needsFallback` (boolean): Use fallback LLM if primary fails
  - `true` - Requires 2 language model connections
  - `false` - Single LLM only (default)
  - Available in typeVersion 2.1+

**Connection Requirements:**

**Required Connections:**
1. **Incoming Data:** `main` connection from Chat Trigger or other nodes
2. **Language Model:** `ai_languageModel` connection from LLM node
   - **Exactly 1 required** (or 2 if `needsFallback: true`)

**Optional Connections:**
3. **Memory:** `ai_memory` connection from Memory node
   - **Maximum 1 allowed**
   - Provides conversation history context
4. **Tools:** `ai_tool` connections from Tool nodes
   - **0 to many** tool connections
   - Each tool adds a capability to the agent
5. **Output Parser:** `ai_outputParser` connection from Parser node
   - **Maximum 1 allowed**
   - Requires `hasOutputParser: true`

**Validation Rules (enforced by n8n-mcp):**
- ✅ Must have exactly 1 language model (or 2 with fallback)
- ✅ Maximum 1 memory connection
- ✅ Maximum 1 output parser connection
- ✅ If `promptType: "auto"`, must have incoming connection from Chat Trigger
- ✅ If `hasOutputParser: true`, must have ai_outputParser connection
- ✅ If `needsFallback: true`, must have 2 language model connections
- ⚠️ Streaming mode requires matching configuration on Chat Trigger

**Output Structure:**
```json
{
  "output": "Final answer from agent",
  "intermediateSteps": [
    {
      "action": "Tool call details",
      "observation": "Tool result"
    }
  ]
}
```

**Use Cases:**
- ✅ Multi-step reasoning and problem solving
- ✅ Tool-augmented conversations
- ✅ RAG (Retrieval Augmented Generation)
- ✅ Complex task automation with AI

**Advanced Example (Multi-Tool Agent):**
```json
{
  "name": "Research Assistant",
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 2.1,
  "parameters": {
    "promptType": "auto",
    "hasOutputParser": false,
    "options": {
      "systemMessage": "You are a research assistant with access to:\n\n1. **Web Search** (perplexity_search): For current events, news, recent developments\n2. **Document Search** (vector_search): For internal company documents and knowledge base\n3. **Calculator** (calculator): For precise calculations\n4. **Code Executor** (python_code): For data analysis and computation\n\nAlways:\n- Choose the right tool for each task\n- Cite sources when using search\n- Show your work for calculations\n- Maintain conversation context",
      "maxIterations": 15,
      "returnIntermediateSteps": true,
      "streamResponse": false
    }
  }
}
```

---

## Language Model Nodes

### LM Chat OpenAI
**Node Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi`
**Version:** 1.2 (latest), also 1.1, 1.0
**Purpose:** OpenAI GPT models (ChatGPT, GPT-4)

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
      "topP": 1,
      "frequencyPenalty": 0,
      "presencePenalty": 0,
      "timeout": 60000
    }
  },
  "credentials": {
    "openAiApi": {
      "id": "credential-id-here",
      "name": "OpenAI API"
    }
  }
}
```

**Parameters:**

**Model Selection (`model`):**
- `"gpt-4o"` - Latest GPT-4 Omni (multimodal, high capability)
  - Cost: $2.50 per 1M input tokens, $10 per 1M output tokens
- `"gpt-4o-mini"` - Fast, cost-effective GPT-4 (recommended)
  - Cost: $0.150 per 1M input tokens, $0.600 per 1M output tokens
- `"gpt-4-turbo"` - Previous generation GPT-4
- `"gpt-3.5-turbo"` - Budget option, good for simple tasks
  - Cost: $0.50 per 1M input tokens, $1.50 per 1M output tokens
- `"gpt-4"` - Original GPT-4 (slower, more expensive)

**Generation Options (`options`):**
- `temperature` (number, 0-2): Creativity vs determinism
  - `0` - Deterministic, focused (for factual tasks)
  - `0.7` - Balanced creativity (default, recommended)
  - `1.0-2.0` - High creativity (for creative writing)

- `maxTokens` (number): Maximum response length
  - Range: `1-4096` (model dependent)
  - Default: `1000`
  - GPT-4o max: `16384`
  - **Note:** 1 token ≈ 4 characters

- `topP` (number, 0-1): Nucleus sampling
  - `1` - Consider all tokens (default)
  - `0.1` - Only top 10% probable tokens
  - Alternative to temperature

- `frequencyPenalty` (number, 0-2): Reduce repetition
  - `0` - No penalty (default)
  - `0.5-1.0` - Moderate reduction of repeating phrases
  - `2.0` - Strong penalty against repetition

- `presencePenalty` (number, 0-2): Encourage topic diversity
  - `0` - No penalty (default)
  - `0.5-1.0` - Moderate encouragement to discuss new topics
  - `2.0` - Strong penalty for repeating topics

- `timeout` (number): API request timeout in milliseconds
  - Default: `60000` (60 seconds)
  - Increase for long responses

**Credentials:**
- **Type:** OpenAI API
- **API Key:** From https://platform.openai.com/api-keys
- **Organization ID:** Optional, for team accounts

**Connection Types:**
- **Outgoing:** `ai_languageModel` → AI Agent or Chain nodes

**Cost Optimization Tips:**
- ✅ Use `gpt-4o-mini` for most tasks (85% cheaper than gpt-4o)
- ✅ Set appropriate `maxTokens` to avoid excessive usage
- ✅ Use `temperature: 0` for factual queries (faster, cheaper)
- ✅ Cache system messages when possible

---

### LM Chat Anthropic
**Node Type:** `@n8n/n8n-nodes-langchain.lmChatAnthropic`
**Version:** 1.0
**Purpose:** Anthropic Claude models

```json
{
  "name": "Claude 3",
  "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic",
  "typeVersion": 1.0,
  "position": [250, 150],
  "parameters": {
    "model": "claude-3-5-sonnet-20241022",
    "options": {
      "temperature": 0.7,
      "maxTokens": 2000,
      "topP": 1,
      "topK": 40
    }
  },
  "credentials": {
    "anthropicApi": {
      "id": "credential-id-here",
      "name": "Anthropic API"
    }
  }
}
```

**Model Selection:**
- `"claude-3-5-sonnet-20241022"` - Latest Claude 3.5 Sonnet (best balance)
  - Cost: $3 per 1M input tokens, $15 per 1M output tokens
- `"claude-3-opus-20240229"` - Highest capability
  - Cost: $15 per 1M input tokens, $75 per 1M output tokens
- `"claude-3-haiku-20240307"` - Fastest, cheapest
  - Cost: $0.25 per 1M input tokens, $1.25 per 1M output tokens

**Parameters:**
- `temperature`, `maxTokens`, `topP` - Same as OpenAI
- `topK` (number): Top-K sampling
  - Range: `1-500`
  - Default: `40`
  - Only consider top K most likely tokens

**Advantages of Claude:**
- ✅ Longer context windows (200K tokens)
- ✅ Strong reasoning capabilities
- ✅ Better at following complex instructions
- ✅ More honest about limitations

---

### LM Chat OpenRouter
**Node Type:** `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
**Version:** 1.0
**Purpose:** Access to multiple LLM providers via OpenRouter

```json
{
  "name": "OpenRouter Multi-Model",
  "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
  "typeVersion": 1.0,
  "position": [250, 150],
  "parameters": {
    "model": "perplexity/llama-3.1-sonar-small-128k-online",
    "options": {
      "temperature": 0.7,
      "maxTokens": 1000
    }
  },
  "credentials": {
    "openRouterApi": {
      "id": "credential-id-here",
      "name": "OpenRouter API"
    }
  }
}
```

**Popular Models via OpenRouter:**
- `"anthropic/claude-3.5-sonnet"` - Claude 3.5 Sonnet
- `"openai/gpt-4o"` - GPT-4 Omni
- `"google/gemini-pro-1.5"` - Google Gemini
- `"perplexity/llama-3.1-sonar-small-128k-online"` - Perplexity Sonar (online search built-in!)
- `"meta-llama/llama-3.1-70b-instruct"` - Llama 3.1 70B
- `"mistralai/mistral-large"` - Mistral Large

**Advantages:**
- ✅ Single API for multiple providers
- ✅ Automatic failover between models
- ✅ Cost comparison across providers
- ✅ Access to Perplexity models with built-in search

**Credentials:**
- **API Key:** From https://openrouter.ai/keys
- **Cost:** Pay-as-you-go, varies by model

---

**Navigation:**
- **Current**: Part 1 - Core Nodes (Chat Triggers, AI Agent, Language Models)
- **Next**: [Part 2 - Memory & Tool Nodes](02_Memory_Tool_Nodes.md)
- **Overview**: [Part 3 - Output Parsers & Best Practices](03_Output_Parsers_Best_Practices.md)

---
**Document Version:** 1.0 (Part 1 of 3)
**Last Updated:** 2025-10-25
**Lines:** 437 / 500 limit
