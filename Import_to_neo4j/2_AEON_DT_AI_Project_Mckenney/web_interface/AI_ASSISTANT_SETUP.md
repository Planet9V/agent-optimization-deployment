# AI Assistant Setup Guide

## 🤖 AEON AI Assistant Overview

The AI Assistant provides natural language interaction with your AEON document ingestion system, combining:

- **OpenRouter API**: Gemini 2.5 Flash Lite for conversational AI
- **Qdrant RAG**: Vector search for relevant document retrieval
- **Neo4j Queries**: Graph traversal for entity relationships
- **Existing AEON Agents**: Leverages ClassifierAgent, NERAgent capabilities

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Get OpenRouter API Key (FREE)

1. Visit https://openrouter.ai/
2. Sign up with email or GitHub
3. Navigate to **Keys** section
4. Click **Create Key**
5. Copy your API key

### Step 2: Configure Environment

Open the `.env` file:
```bash
nano /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/.env
```

Replace `your_openrouter_api_key_here` with your actual key:
```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxx
```

Save and exit (Ctrl+X, Y, Enter)

### Step 3: Install Dependencies

```bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Start Web Interface

```bash
./launch.sh
```

Navigate to: **http://localhost:8501** → **AI Assistant** page (🤖 in sidebar)

---

## 💬 What Can the AI Assistant Do?

### 📚 Document Queries
```
"Find all documents about Siemens PLCs"
"Show me water sector SCADA documents"
"What documents mention Modbus protocol?"
```

### 🔍 Entity Exploration
```
"What vendors are in the database?"
"List all protocols extracted from documents"
"Show me IEC standards mentioned"
```

### 📊 System Information
```
"How many documents are indexed?"
"What entity types are supported?"
"Show system statistics"
```

### 🛠️ Ingestion Guidance
```
"How do I classify a new document?"
"What file formats are supported?"
"Explain the ingestion pipeline"
```

### 🤝 Interactive Classification
```
"Help me classify this document: [paste text]"
"What sector would this document belong to?"
"Extract entities from this text: [paste text]"
```

---

## 🏗️ Architecture Integration

### Existing AEON Infrastructure Used

**1. ClassifierAgent** (`agents/classifier_agent.py`)
- ML-based document classification
- Confidence scoring
- User feedback learning via Qdrant

**2. NERAgent** (`agents/ner_agent.py`)
- Pattern + Neural hybrid NER
- 8 entity types (VENDOR, PROTOCOL, etc.)
- spaCy + EntityRuler

**3. QdrantMemoryManager** (`utils/qdrant_memory.py`)
- Vector similarity search
- Classification memory
- Agent activity tracking

**4. Neo4jConnector** (`utils/neo4j_connector.py`)
- Document/entity queries
- Graph traversal
- Statistics aggregation

### New AI Assistant Components

**1. AIAssistant** (`web_interface/utils/ai_assistant.py`)
- OpenRouter API integration
- RAG orchestration
- Conversation memory
- Context-aware responses

**2. AI Assistant Page** (`web_interface/pages/5_AI_Assistant.py`)
- Streamlit chat interface
- Session management
- Quick action buttons
- Setup instructions

---

## 🔧 Configuration Options

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your_key_here

# Optional (defaults shown)
OPENROUTER_MODEL=google/gemini-2.5-flash-lite-preview-09-2025
AI_ASSISTANT_ENABLED=true
AI_CONVERSATION_MEMORY=true
AI_MAX_CONTEXT_MESSAGES=10

# Database
NEO4J_URI=bolt://localhost:7687
NEO4J_PASSWORD=neo4j@openspg
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### Model Options

**Default**: `google/gemini-2.5-flash-lite-preview-09-2025`
- Fast and efficient
- Free tier on OpenRouter
- Good for conversational queries

**Alternatives** (change OPENROUTER_MODEL in .env):
```bash
# More powerful
google/gemini-2.0-flash:free
anthropic/claude-3-haiku

# Cost-effective
meta-llama/llama-3.1-8b-instruct:free
```

See https://openrouter.ai/models for all options.

---

## 🧠 How RAG Works

**Retrieval-Augmented Generation** combines:

1. **Vector Search** (Qdrant):
   - User query → embedding (384-dim vector)
   - Find top 5 similar documents
   - Return relevant context

2. **Graph Queries** (Neo4j):
   - Extract keywords from query
   - Find matching entities
   - Retrieve relationships

3. **LLM Generation** (OpenRouter):
   - Combine retrieved context
   - Generate coherent response
   - Cite sources when relevant

### Example Flow

```
User: "Find Siemens PLC documents in water sector"
  ↓
1. Generate embedding of query
2. Search Qdrant for similar documents
3. Query Neo4j for Siemens entities
4. Build context prompt with results
5. Send to Gemini via OpenRouter
6. Return natural language response
  ↓
Assistant: "I found 12 documents about Siemens PLCs in the water sector.
           The most relevant include S7-1500 configuration guides and
           WinCC SCADA integration manuals..."
```

---

## 📊 Conversation Memory

**Stored in Qdrant** (`aeon_conversations` collection):
- Last 10 messages per session
- Embedded for semantic search
- Enables contextual follow-ups

**Benefits**:
- "Show me more details" works correctly
- "What about X vendor?" remembers previous context
- Multi-turn conversations feel natural

---

## 🐛 Troubleshooting

### AI Assistant Not Available

**Check**:
1. API key set in `.env`
2. Qdrant running (optional but recommended)
3. Neo4j running (required)

**Test**:
```bash
# Test Qdrant
curl http://localhost:6333/collections

# Test Neo4j
docker ps | grep openspg-neo4j
```

### "Module not found" Errors

**Fix**:
```bash
cd web_interface
source venv/bin/activate
pip install -r requirements.txt
```

### Slow Responses

**Optimize**:
1. Use faster model (gemini-2.0-flash:free)
2. Reduce AI_MAX_CONTEXT_MESSAGES in .env
3. Enable Qdrant for better RAG performance

### API Rate Limits

OpenRouter free tier limits:
- ~20 requests/minute for Gemini
- Upgrade for higher limits if needed

---

## 📈 Future Enhancements

**Planned for Phase 2**:
- Voice input/output
- Document upload via chat
- Multi-modal (image analysis)
- Batch operations through chat
- Classification review UI
- Advanced analytics queries

---

## 💡 Tips for Best Results

1. **Be specific**: "Find water sector documents" vs "Find documents"
2. **Ask follow-ups**: "Show more details", "What about X?"
3. **Use quick actions**: Buttons provide example queries
4. **Check context**: Expander shows documents used in response
5. **Clear when switching topics**: Use "Clear Conversation" button

---

## 🔐 Security Notes

- API keys stored in `.env` (gitignored)
- No data sent to OpenRouter without user query
- Conversation history stored locally in Qdrant
- Neo4j credentials in environment variables

---

## 📞 Support

**Issues**:
- Check logs: `tail -f streamlit.log`
- Verify Qdrant: http://localhost:6333/dashboard
- Test Neo4j: System Control page

**Documentation**:
- OpenRouter: https://openrouter.ai/docs
- Qdrant: https://qdrant.tech/documentation
- AEON: Parent directory README

---

*AEON AI Assistant - Enhancing Document Ingestion with Conversational AI*
*Version: 1.0 | Integration Complete: 2025-11-03*
