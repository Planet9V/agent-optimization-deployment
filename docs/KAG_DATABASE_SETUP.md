# Creating a KAG Database on OpenSPG Neo4j

## Overview

KAG (Knowledge Augmented Generation) creates knowledge bases in OpenSPG that use Neo4j for graph storage. Each KAG "project" is essentially a knowledge base with its own schema, data, and configuration.

## Your Current Setup

- **OpenSPG Server**: http://localhost:8887
- **Neo4j Database**: openspg-neo4j (neo4j://localhost:7687)
- **Neo4j Credentials**: neo4j / neo4j@openspg
- **KAG Installed**: Version 0.8.0 in `/home/jim/2_OXOT_Projects_Dev/venv`

## Step-by-Step Guide

### 1. Activate KAG Environment

```bash
cd /home/jim/2_OXOT_Projects_Dev
source venv/bin/activate
```

### 2. Create Configuration File

Create a configuration file for your KAG project:

```bash
cat > my_kag_config.yaml << 'EOF'
#------------project configuration start----------------#
openie_llm: &openie_llm
  type: maas
  base_url: https://api.deepseek.com
  api_key: YOUR_DEEPSEEK_API_KEY
  model: deepseek-chat
  enable_check: false

chat_llm: &chat_llm
  type: maas
  base_url: https://api.deepseek.com
  api_key: YOUR_DEEPSEEK_API_KEY
  model: deepseek-chat
  enable_check: false

vectorize_model: &vectorize_model
  api_key: YOUR_SILICONFLOW_API_KEY
  base_url: https://api.siliconflow.cn/v1/
  model: BAAI/bge-m3
  type: openai
  vector_dimensions: 1024
  enable_check: false
vectorizer: *vectorize_model

log:
  level: INFO

project:
  biz_scene: default
  host_addr: http://127.0.0.1:8887
  id: "1"
  language: en
  namespace: MyFirstKAG
#------------project configuration end----------------#

#------------kag-builder configuration start----------------#
kag_builder_pipeline:
  chain:
    type: unstructured_builder_chain
    extractor:
      type: schema_free_extractor
      llm: *openie_llm
      ner_prompt:
        type: default_ner
      std_prompt:
        type: default_std
      triple_prompt:
        type: default_triple
    reader:
      type: dict_reader
    post_processor:
      type: kag_post_processor
    splitter:
      type: length_splitter
      split_length: 100000
      window_length: 0
    vectorizer:
      type: batch_vectorizer
      vectorize_model: *vectorize_model
    writer:
      type: kg_writer
  num_threads_per_chain: 1
  num_chains: 16
  scanner:
    type: dict_scanner
#------------kag-builder configuration end----------------#

#------------kag-solver configuration start----------------#
search_api: &search_api
  type: openspg_search_api

graph_api: &graph_api
  type: openspg_graph_api

exact_kg_retriever: &exact_kg_retriever
  type: default_exact_kg_retriever
  el_num: 5
  llm_client: *chat_llm
  search_api: *search_api
  graph_api: *graph_api

fuzzy_kg_retriever: &fuzzy_kg_retriever
  type: default_fuzzy_kg_retriever
  el_num: 5
  vectorize_model: *vectorize_model
  llm_client: *chat_llm
  search_api: *search_api
  graph_api: *graph_api

chunk_retriever: &chunk_retriever
  type: default_chunk_retriever
  llm_client: *chat_llm
  recall_num: 10
  rerank_topk: 10

kag_solver_pipeline:
  memory:
    type: default_memory
    llm_client: *chat_llm
  max_iterations: 3
  reasoner:
    type: default_reasoner
    llm_client: *chat_llm
    lf_planner:
      type: default_lf_planner
      llm_client: *chat_llm
      vectorize_model: *vectorize_model
    lf_executor:
      type: default_lf_executor
      llm_client: *chat_llm
      force_chunk_retriever: true
      exact_kg_retriever: *exact_kg_retriever
      fuzzy_kg_retriever: *fuzzy_kg_retriever
      chunk_retriever: *chunk_retriever
      merger:
        type: default_lf_sub_query_res_merger
        vectorize_model: *vectorize_model
        chunk_retriever: *chunk_retriever
  generator:
    type: default_generator
    llm_client: *chat_llm
  reflector:
    type: default_reflector
    llm_client: *chat_llm
#------------kag-solver configuration end----------------#
EOF
```

**Important**: Replace `YOUR_DEEPSEEK_API_KEY` and `YOUR_SILICONFLOW_API_KEY` with your actual API keys.

### 3. Create the KAG Project

```bash
cd /home/jim/2_OXOT_Projects_Dev
knext project create --config_path ./my_kag_config.yaml
```

This will create a directory named `MyFirstKAG` with the following structure:

```
MyFirstKAG/
├── builder/
│   ├── __init__.py
│   ├── data/
│   ├── indexer.py
│   └── prompt/
├── kag_config.yaml
├── reasoner/
├── schema/
│   ├── MyFirstKAG.schema
│   └── __init__.py
└── solver/
    ├── __init__.py
    ├── data/
    └── prompt/
```

### 4. Define Your Schema (Optional)

Edit the schema file to define your knowledge graph structure:

```bash
cd MyFirstKAG
vim schema/MyFirstKAG.schema
```

Example schema:
```
namespace MyFirstKAG

# Define entity types
entity Person {
  name: string
  age: int
}

entity Company {
  name: string
  industry: string
}

# Define relationships
relation WorksFor(Person, Company) {
  position: string
  startDate: date
}
```

Commit the schema:
```bash
knext schema commit
```

### 5. Prepare Your Data

Create a data file for indexing. KAG supports JSON format:

```bash
cat > builder/data/sample_data.json << 'EOF'
[
  {
    "id": "doc_1",
    "name": "About Tesla",
    "content": "Tesla, Inc. is an American electric vehicle and clean energy company. Elon Musk is the CEO of Tesla. The company was founded in 2003."
  },
  {
    "id": "doc_2",
    "name": "SpaceX Overview",
    "content": "SpaceX is an American spacecraft manufacturer and launch service provider. Elon Musk founded SpaceX in 2002."
  }
]
EOF
```

### 6. Build the Knowledge Graph

Create or edit `builder/indexer.py`:

```python
import os
import logging
from kag.common.registry import import_modules_from_path
from kag.builder.runner import BuilderChainRunner

logger = logging.getLogger(__name__)

def buildKB(file_path):
    from kag.common.conf import KAG_CONFIG

    runner = BuilderChainRunner.from_config(
        KAG_CONFIG.all_config["kag_builder_pipeline"]
    )
    runner.invoke(file_path)

    logger.info(f"\n\nbuildKB successfully for {file_path}\n\n")

if __name__ == "__main__":
    import_modules_from_path(".")
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, "data/sample_data.json")

    buildKB(file_path)
```

Run the indexer:

```bash
cd builder
python indexer.py
```

This will:
- Extract entities, relationships, and knowledge units from your documents
- Store them in Neo4j (openspg-neo4j)
- Create vector embeddings for semantic search
- Generate checkpoint files for resumable processing

### 7. Verify in Neo4j

Check your knowledge graph in Neo4j Browser:

```bash
# Open in browser: http://localhost:7474
# Login: neo4j / neo4j@openspg

# Run Cypher query to see your data:
MATCH (n) RETURN n LIMIT 25
```

### 8. Query Your Knowledge Base

Create a query script `solver/qa.py`:

```python
import logging
from kag.solver.logic.solver_pipeline import SolverPipeline
from kag.common.conf import KAG_CONFIG
from kag.common.registry import import_modules_from_path

logger = logging.getLogger(__name__)

class MyKAGQuery:
    def __init__(self):
        pass

    def qa(self, query):
        resp = SolverPipeline.from_config(
            KAG_CONFIG.all_config["kag_solver_pipeline"]
        )
        answer, traceLog = resp.run(query)

        logger.info(f"\n\nAnswer for '{query}': {answer}\n\n")
        return answer, traceLog

if __name__ == "__main__":
    import_modules_from_path("./prompt")
    kag = MyKAGQuery()

    # Ask questions about your knowledge base
    kag.qa("Who is the CEO of Tesla?")
    kag.qa("When was SpaceX founded?")
```

Run queries:

```bash
cd solver
python qa.py
```

## How It Works

### Knowledge Storage in Neo4j

KAG stores knowledge in your `openspg-neo4j` database with:

1. **Entity Nodes**: Extracted entities (Person, Company, etc.)
2. **Relationship Edges**: Connections between entities
3. **Chunk Nodes**: Original text chunks linked to entities
4. **Vector Embeddings**: For semantic similarity search

### Database Structure

```
Neo4j Database: neo4j (default)
├── Entities (labeled by type: Person, Company, etc.)
├── Relations (typed edges between entities)
├── Chunks (text blocks with vector embeddings)
├── KnowledgeUnits (semantic knowledge pieces)
└── Indexes (for fast retrieval)
```

### Shared Volume Usage

Your KAG project can use the shared volume for data exchange:

```bash
# Copy documents to shared volume for processing
docker cp my_documents.json openspg-server:/shared/

# Reference from KAG builder
file_path = "/shared/my_documents.json"
buildKB(file_path)
```

## Multiple Knowledge Bases

You can create multiple KAG projects (knowledge bases) in the same OpenSPG/Neo4j instance:

```bash
# Create another project with different namespace
knext project create --config_path ./another_config.yaml
# namespace: AnotherKAG
```

Each project uses a different namespace in Neo4j for isolation.

## Useful Commands

```bash
# List all projects
knext project list

# Update project configuration
cd MyFirstKAG
knext project update --proj_path .

# Delete project
knext project delete --namespace MyFirstKAG

# Check build progress
wc -l builder/ckpt/kag_checkpoint_0_1.ckpt
```

## Troubleshooting

### Issue: "Connection refused to OpenSPG server"
**Solution**: Ensure OpenSPG services are running:
```bash
cd /home/jim/2_OXOT_Projects_Dev
docker-compose ps
```

### Issue: "API key error"
**Solution**: Update API keys in `kag_config.yaml`:
```yaml
api_key: YOUR_ACTUAL_API_KEY
```

### Issue: "Neo4j connection failed"
**Solution**: Verify Neo4j credentials and connectivity:
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"
```

## Next Steps

1. **Use Real Data**: Replace sample data with your actual documents
2. **Customize Schema**: Define domain-specific entities and relationships
3. **Tune Parameters**: Adjust LLM models, chunk sizes, retrieval parameters
4. **Production Deployment**: Configure proper API keys and resource limits
5. **Integration**: Use KAG API in your applications

## References

- KAG Documentation: https://openspg.yuque.com/ndx6g9/cwh47i
- OpenSPG Schema Guide: https://openspg.yuque.com/ndx6g9/cwh47i/fiq6zum3qtzr7cne
- KAG GitHub: https://github.com/OpenSPG/KAG
