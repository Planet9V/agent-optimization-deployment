#!/bin/bash

# KAG Project Creation Script
# Creates a new KAG knowledge base on OpenSPG Neo4j

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================"
echo "KAG Project Creation Wizard"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    cd /home/jim/2_OXOT_Projects_Dev
    source venv/bin/activate
fi

# Get project name
read -p "Enter project name (e.g., MyKnowledgeBase): " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}Project name is required${NC}"
    exit 1
fi

# Get API keys
echo ""
echo "You need API keys for:"
echo "  1. LLM (e.g., DeepSeek, OpenAI, Qwen)"
echo "  2. Embedding model (e.g., SiliconFlow)"
echo ""

read -p "Enter LLM provider (deepseek/openai/qwen) [deepseek]: " LLM_PROVIDER
LLM_PROVIDER=${LLM_PROVIDER:-deepseek}

case $LLM_PROVIDER in
    deepseek)
        LLM_BASE_URL="https://api.deepseek.com"
        LLM_MODEL="deepseek-chat"
        ;;
    openai)
        LLM_BASE_URL="https://api.openai.com/v1"
        LLM_MODEL="gpt-4"
        ;;
    qwen)
        LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1/"
        LLM_MODEL="qwen2.5-72b-instruct"
        ;;
    *)
        echo -e "${RED}Invalid provider${NC}"
        exit 1
        ;;
esac

read -p "Enter LLM API key: " LLM_API_KEY
if [ -z "$LLM_API_KEY" ]; then
    echo -e "${RED}API key is required${NC}"
    exit 1
fi

read -p "Enter embedding model API key [same as LLM]: " EMBED_API_KEY
EMBED_API_KEY=${EMBED_API_KEY:-$LLM_API_KEY}

# Create config file
CONFIG_FILE="${PROJECT_NAME}_config.yaml"

echo ""
echo -e "${YELLOW}Creating configuration file: $CONFIG_FILE${NC}"

cat > "$CONFIG_FILE" << EOF
#------------project configuration start----------------#
openie_llm: &openie_llm
  type: maas
  base_url: $LLM_BASE_URL
  api_key: $LLM_API_KEY
  model: $LLM_MODEL
  enable_check: false

chat_llm: &chat_llm
  type: maas
  base_url: $LLM_BASE_URL
  api_key: $LLM_API_KEY
  model: $LLM_MODEL
  enable_check: false

vectorize_model: &vectorize_model
  api_key: $EMBED_API_KEY
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
  namespace: $PROJECT_NAME
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

echo -e "${GREEN}✓ Configuration file created${NC}"

# Create the project
echo ""
echo -e "${YELLOW}Creating KAG project...${NC}"

cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples

if knext project create --config_path "../../$CONFIG_FILE"; then
    echo -e "${GREEN}✓ Project created successfully${NC}"
else
    echo -e "${RED}✗ Project creation failed${NC}"
    exit 1
fi

# Create sample data
echo ""
echo -e "${YELLOW}Creating sample data...${NC}"

mkdir -p "$PROJECT_NAME/builder/data"

cat > "$PROJECT_NAME/builder/data/sample_data.json" << 'EOFDATA'
[
  {
    "id": "doc_1",
    "name": "OpenSPG Overview",
    "content": "OpenSPG is a knowledge graph engine developed by Ant Group. It provides semantic-enhanced programmable graph capabilities for building professional domain knowledge bases."
  },
  {
    "id": "doc_2",
    "name": "KAG Framework",
    "content": "KAG (Knowledge Augmented Generation) is a framework built on OpenSPG that enables LLM-enhanced question answering with logical reasoning capabilities. KAG supports multi-hop reasoning and factual question answering."
  },
  {
    "id": "doc_3",
    "name": "Neo4j Integration",
    "content": "OpenSPG uses Neo4j as the default graph database for storing knowledge graphs. Neo4j provides ACID transactions, Cypher query language, and excellent performance for graph traversals."
  }
]
EOFDATA

echo -e "${GREEN}✓ Sample data created${NC}"

# Create indexer script
cat > "$PROJECT_NAME/builder/indexer.py" << 'EOFINDEX'
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
EOFINDEX

echo -e "${GREEN}✓ Indexer script created${NC}"

# Create query script
cat > "$PROJECT_NAME/solver/qa.py" << 'EOFQA'
import logging
from kag.solver.logic.solver_pipeline import SolverPipeline
from kag.common.conf import KAG_CONFIG
from kag.common.registry import import_modules_from_path

logger = logging.getLogger(__name__)

class KAGQuery:
    def __init__(self):
        pass

    def qa(self, query):
        resp = SolverPipeline.from_config(
            KAG_CONFIG.all_config["kag_solver_pipeline"]
        )
        answer, traceLog = resp.run(query)

        logger.info(f"\n\nAnswer for '{query}': {answer}\n\n")
        print(f"\nQ: {query}")
        print(f"A: {answer}\n")
        return answer, traceLog

if __name__ == "__main__":
    import_modules_from_path("./prompt")
    kag = KAGQuery()

    # Sample queries
    queries = [
        "What is OpenSPG?",
        "What database does OpenSPG use?",
        "What capabilities does KAG provide?"
    ]

    for query in queries:
        kag.qa(query)
        print("-" * 80)
EOFQA

echo -e "${GREEN}✓ Query script created${NC}"

# Summary
echo ""
echo "========================================"
echo -e "${GREEN}Project Setup Complete!${NC}"
echo "========================================"
echo ""
echo "Project directory: /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/$PROJECT_NAME"
echo ""
echo "Next steps:"
echo "  1. Build the knowledge graph:"
echo "     cd $PROJECT_NAME/builder"
echo "     python indexer.py"
echo ""
echo "  2. Query your knowledge base:"
echo "     cd $PROJECT_NAME/solver"
echo "     python qa.py"
echo ""
echo "  3. Check in Neo4j Browser:"
echo "     http://localhost:7474"
echo "     Login: neo4j / neo4j@openspg"
echo "     Query: MATCH (n) RETURN n LIMIT 25"
echo ""
echo "Documentation: /home/jim/2_OXOT_Projects_Dev/docs/KAG_DATABASE_SETUP.md"
echo ""
