# OpenSPG Comprehensive Usage Guide

**File:** OpenSPG_Usage_Guide.md
**Created:** 2025-10-26
**Version:** v1.0.0
**Author:** OpenSPG Documentation Team
**Purpose:** Comprehensive guide for installing, configuring, and using OpenSPG and KAG
**Status:** ACTIVE

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
   - [Docker Installation (Recommended)](#docker-installation-recommended)
   - [Developer Installation](#developer-installation)
   - [Manual/Non-Docker Installation](#manual-non-docker-installation)
4. [Configuration](#configuration)
5. [Getting Started](#getting-started)
6. [Core Concepts](#core-concepts)
7. [Common Workflows](#common-workflows)
8. [API Usage](#api-usage)
9. [Examples and Tutorials](#examples-and-tutorials)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)
12. [References](#references)

---

## Introduction

### What is OpenSPG?

OpenSPG (Semantic-enhanced Programmable Graph) is an open-source Knowledge Graph Engine developed by Ant Group in collaboration with OpenKG. It provides a comprehensive framework for building, managing, and reasoning over domain-specific knowledge graphs.

**Core Capabilities:**
- ✅ Domain model constrained knowledge modeling
- ✅ Facts and logic fused representation
- ✅ Native support for KAG (Knowledge Augmented Generation)
- ✅ Explicit semantic representations
- ✅ Logical rule definitions
- ✅ Pluggable operator frameworks (construction, inference)

### What is KAG?

KAG (Knowledge Augmented Generation) is a logical form-guided reasoning and retrieval framework built on OpenSPG engine and LLMs. It enables:
- 🧠 Logical reasoning over professional domain knowledge bases
- 📚 Factual Q&A solutions
- 🔍 Advanced retrieval beyond traditional vector similarity (RAG)
- 🎯 Multi-hop reasoning with graph-based knowledge

### Key Features

**OpenSPG Framework:**
- **SPG Framework**: Semantic-enhanced Programmable Graph for domain knowledge graphs
- **KNext**: Programmable framework providing scalable, process-oriented, componentized capabilities
- **Multi-Engine Support**: Pluggable adaptation of basic engines and algorithmic services

**KAG Framework:**
- **Knowledge Representation**: DIKW hierarchy friendly to large language models
- **Hybrid Approach**: Schema-free extraction + schema-constrained construction
- **Knowledge-Chunk Indexing**: Cross-references between graph structures and original text
- **Logical Form-Guided Reasoning**: Combines retrieval, graph reasoning, language reasoning, and numerical calculation

---

## System Requirements

### Minimum Requirements

**For Product Users (Docker):**
- **Operating Systems**:
  - macOS 12.6 or later
  - CentOS 7 or later
  - Ubuntu 20.04 or later
  - Windows 10 LTSC 2021 or later
- **Docker**: Latest stable version
- **Docker Compose**: Latest stable version
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 20GB minimum free space

**For Developers (Non-Docker):**
- **Python**: 3.10 or later (3.8+ for some components)
- **Java**: JDK 8 or later (83.6% of codebase)
- **Scala**: 2.12+ (13.9% of codebase)
- **Maven**: Latest stable version
- **Git**: For cloning repositories
- **Conda** (recommended) or Python venv

### Network Requirements

- Internet connection for:
  - Downloading Docker images
  - Installing Python packages
  - Accessing LLM services (OpenAI, etc.)
  - Vectorization services

---

## Installation

### Docker Installation (Recommended)

Docker installation is the easiest way to get started with OpenSPG/KAG.

#### Step 1: Install Docker

**macOS/Windows:**
- Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
- Install and start Docker Desktop

**Linux (Ubuntu/Debian):**
```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

**Linux (CentOS/RHEL):**
```bash
# Install Docker
sudo yum install -y docker docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

#### Step 2: Download Docker Compose Configuration

```bash
# Download the Docker Compose file for Western regions
curl -sSL https://raw.githubusercontent.com/OpenSPG/openspg/refs/heads/master/dev/release/docker-compose-west.yml -o docker-compose-west.yml

# For users in China, use:
# curl -sSL https://raw.githubusercontent.com/OpenSPG/openspg/refs/heads/master/dev/release/docker-compose.yml -o docker-compose.yml
```

#### Step 3: Start OpenSPG Services

```bash
# Start all services in detached mode
docker compose -f docker-compose-west.yml up -d

# Check service status
docker compose -f docker-compose-west.yml ps

# View logs
docker compose -f docker-compose-west.yml logs -f
```

#### Step 4: Access the Interface

1. Open your web browser
2. Navigate to: `http://127.0.0.1:8887`
3. Login with default credentials:
   - **Username**: `openspg`
   - **Password**: `openspg@kag`

#### Docker Services Overview

The Docker Compose setup includes 4 main images:
- **OpenSPG Server**: Core knowledge graph engine
- **KAG Service**: Knowledge augmented generation framework
- **Database**: For persistent storage
- **Web Interface**: Frontend visualization

---

### Developer Installation

For developers who want to work with the source code or customize OpenSPG/KAG.

#### Prerequisites

Install Python 3.10 or later and Git.

#### Installation Steps

**macOS/Linux:**

```bash
# Create and activate conda environment
conda create -n kag-demo python=3.10
conda activate kag-demo

# Clone the KAG repository
git clone https://github.com/OpenSPG/KAG.git
cd KAG

# Install KAG in editable mode
pip install -e .

# Verify installation
python -c "import kag; print(kag.__version__)"
```

**Windows:**

```bash
# Create Python virtual environment
py -m venv kag-demo

# Activate environment
kag-demo\Scripts\activate

# Clone the repository
git clone https://github.com/OpenSPG/KAG.git
cd KAG

# Install KAG
pip install -e .

# Verify installation
python -c "import kag; print(kag.__version__)"
```

#### Install OpenSPG (Optional)

For full OpenSPG development:

```bash
# Clone OpenSPG repository
git clone https://github.com/OpenSPG/openspg.git
cd openspg

# Build with Maven
mvn clean install -DskipTests

# The compiled packages will be in target/ directories
```

---

### Manual/Non-Docker Installation

For advanced users who prefer manual installation without Docker.

#### Step 1: Install System Dependencies

**Python Environment:**
```bash
# Create Python virtual environment
python3.10 -m venv openspg-env
source openspg-env/bin/activate  # On Windows: openspg-env\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

**Java Environment:**
```bash
# Install Java (Ubuntu/Debian)
sudo apt-get install openjdk-11-jdk maven

# Install Java (macOS with Homebrew)
brew install openjdk@11 maven

# Verify installation
java -version
mvn -version
```

#### Step 2: Build OpenSPG from Source

```bash
# Clone OpenSPG
git clone https://github.com/OpenSPG/openspg.git
cd openspg

# Build with Maven
mvn clean package -DskipTests

# The server artifacts will be in server/target/
```

#### Step 3: Install KNext

KNext is OpenSPG's programmable framework.

```bash
# Navigate to Python components
cd python/knext

# Install KNext
pip install -e .

# Verify installation
knext --version
```

#### Step 4: Configure and Run

```bash
# Set up configuration
export OPENSPG_HOME=/path/to/openspg

# Start OpenSPG server
cd server/target
java -jar openspg-server.jar

# The server will start on http://localhost:8887
```

#### Step 5: Install KAG

```bash
# In a separate terminal, install KAG
git clone https://github.com/OpenSPG/KAG.git
cd KAG
pip install -e .
```

---

## Configuration

### KAG Configuration File

KAG uses a `kag_config.yaml` file for configuration. Here's a complete example:

```yaml
# kag_config.yaml

# Project Information
project_id: "my_project"
namespace: "default"

# LLM Configuration
openie_llm:
  type: "openai"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"
  temperature: 0.0
  max_tokens: 2000

chat_llm:
  type: "openai"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"
  temperature: 0.7
  max_tokens: 4000

# Vectorization Configuration
vectorize_model:
  type: "openai"
  model: "text-embedding-3-small"
  api_key: "${OPENAI_API_KEY}"
  dimensions: 1536

# Knowledge Graph Configuration
knowledge_graph:
  host: "127.0.0.1"
  port: 8887
  username: "openspg"
  password: "openspg@kag"

# Builder Configuration
builder:
  batch_size: 100
  workers: 4
  enable_parallel: true

# Reasoner Configuration
reasoner:
  max_hops: 3
  confidence_threshold: 0.7
  reasoning_mode: "hybrid"  # Options: "retrieval", "reasoning", "hybrid"

# Storage Configuration
storage:
  type: "local"  # Options: "local", "s3", "oss"
  path: "./data"
```

### Environment Variables

Set up environment variables for sensitive information:

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
OPENSPG_USERNAME=openspg
OPENSPG_PASSWORD=openspg@kag
OPENSPG_HOST=http://127.0.0.1:8887
EOF

# Load environment variables
source .env  # Linux/macOS
# Or on Windows: set /p=<.env
```

### OpenSPG Server Configuration

The OpenSPG server can be configured through `application.properties`:

```properties
# Server Configuration
server.port=8887
server.context-path=/

# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/openspg
spring.datasource.username=root
spring.datasource.password=your_password

# Knowledge Graph Storage
kg.storage.type=tugraph
kg.storage.host=localhost
kg.storage.port=7687

# Authentication
security.enabled=true
security.default.username=openspg
security.default.password=openspg@kag
```

---

## Getting Started

### Quick Start with Docker

After installing via Docker, follow these steps:

#### 1. Access the Web Interface

```bash
# Ensure services are running
docker compose ps

# Open browser to http://127.0.0.1:8887
# Login: openspg / openspg@kag
```

#### 2. Create Your First Project

Through the web interface:
1. Click "New Project"
2. Enter project name (e.g., "my_first_kg")
3. Select domain template (or start blank)
4. Click "Create"

#### 3. Define Schema

1. Navigate to "Schema" tab
2. Define entity types (e.g., Person, Company)
3. Define relationships (e.g., WorksFor)
4. Add properties to entities
5. Click "Commit Schema"

#### 4. Import Data

1. Go to "Data Import" tab
2. Upload data file (CSV, JSON, or Excel)
3. Map columns to schema entities/properties
4. Click "Start Import"

#### 5. Query and Visualize

1. Navigate to "Query" tab
2. Use natural language or structured query
3. View results in graph or table format

### Quick Start with Developer Mode

For developers working with code:

#### 1. Set Up Project Structure

```bash
# Create project directory
mkdir my_kg_project
cd my_kg_project

# Initialize project structure
knext project create --prj_path .

# This creates:
# ├── builder/         # Knowledge construction
# ├── reasoner/        # Reasoning logic
# ├── schema/          # Schema definitions
# ├── solver/          # Q&A and queries
# └── kag_config.yaml  # Configuration
```

#### 2. Define Schema

Create `schema/MySchema.schema`:

```python
# Define entity types
Entity Person {
    name: String;
    age: Integer;
    email: String;
}

Entity Company {
    name: String;
    industry: String;
    founded_year: Integer;
}

# Define relationships
Relation WorksFor {
    from: Person;
    to: Company;
    properties: {
        position: String;
        start_date: Date;
    }
}
```

#### 3. Commit Schema

```bash
# Commit schema to OpenSPG server
knext schema commit

# Verify schema
knext schema list
```

#### 4. Build Knowledge Graph

Create `builder/indexer.py`:

```python
from kag.builder import KGBuilder
from kag.common.conf import KAG_CONFIG

# Initialize builder
builder = KGBuilder(config=KAG_CONFIG)

# Load data
data = [
    {
        "type": "Person",
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    },
    {
        "type": "Company",
        "name": "Tech Corp",
        "industry": "Technology",
        "founded_year": 2010
    },
    {
        "type": "WorksFor",
        "from": "John Doe",
        "to": "Tech Corp",
        "position": "Software Engineer",
        "start_date": "2020-01-15"
    }
]

# Build knowledge graph
result = builder.build(data)
print(f"Built knowledge graph with {result.entity_count} entities")
```

#### 5. Execute Builder

```bash
cd builder
python indexer.py
cd ..
```

#### 6. Query Knowledge Graph

Create `solver/query.py`:

```python
from kag.solver import KGQueryEngine
from kag.common.conf import KAG_CONFIG

# Initialize query engine
query_engine = KGQueryEngine(config=KAG_CONFIG)

# Execute natural language query
question = "Who works at Tech Corp?"
result = query_engine.query(question)

print(f"Question: {question}")
print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
```

```bash
cd solver
python query.py
cd ..
```

---

## Core Concepts

### 1. SPG (Semantic-enhanced Programmable Graph)

SPG is the foundational framework that combines:
- **Semantic Layer**: Explicit meaning and context
- **Programmable Layer**: Customizable operators and logic
- **Graph Layer**: Networked knowledge representation

### 2. Schema-Constrained Modeling

OpenSPG enforces domain models through schemas:
- **Entity Types**: Define what kinds of things exist
- **Relations**: Define how entities connect
- **Properties**: Define entity attributes
- **Rules**: Define logical constraints

### 3. Knowledge Construction Pipeline

```
Raw Data → Extraction → Linking → Fusion → Storage
    ↓          ↓          ↓        ↓        ↓
 Sources   Entities   Relations  Merge   KG Store
```

### 4. Reasoning Operators

OpenSPG provides three operator types:
- **Planning Operators**: Task decomposition and workflow design
- **Reasoning Operators**: Graph reasoning and semantic inference
- **Retrieval Operators**: Exact match, text search, and calculations

### 5. KNext Framework

KNext is OpenSPG's programmable interface:
- **Projects**: Self-contained KG applications
- **Builders**: Knowledge construction logic
- **Reasoners**: Inference and deduction logic
- **Solvers**: Query and Q&A interfaces

### 6. DIKW Hierarchy in KAG

KAG implements the Data-Information-Knowledge-Wisdom hierarchy:
- **Data**: Raw facts and observations
- **Information**: Processed and contextualized data
- **Knowledge**: Structured understanding with relationships
- **Wisdom**: Actionable insights and reasoning

### 7. Logical Form-Guided Reasoning

KAG uses logical forms to guide reasoning:
1. **Parse** question into logical form
2. **Plan** reasoning steps
3. **Execute** retrieval and inference
4. **Synthesize** answer from results

---

## Common Workflows

### Workflow 1: Building a Domain Knowledge Graph

#### Step 1: Domain Analysis
```bash
# Identify key entities, relationships, and attributes
# Example: Supply Chain Domain
# Entities: Supplier, Product, Factory, Order
# Relations: Supplies, Manufactures, Contains
```

#### Step 2: Schema Design

Create `schema/SupplyChain.schema`:

```python
Entity Supplier {
    supplier_id: String primary;
    name: String;
    country: String;
    reliability_score: Float;
}

Entity Product {
    product_id: String primary;
    name: String;
    category: String;
    unit_price: Float;
}

Entity Factory {
    factory_id: String primary;
    location: String;
    capacity: Integer;
}

Relation Supplies {
    from: Supplier;
    to: Product;
    properties: {
        quantity: Integer;
        delivery_time: Integer;
    }
}

Relation Manufactures {
    from: Factory;
    to: Product;
    properties: {
        daily_output: Integer;
    }
}
```

#### Step 3: Commit Schema

```bash
knext schema commit
```

#### Step 4: Data Preparation

Prepare `builder/data/supply_chain_data.json`:

```json
{
  "suppliers": [
    {
      "supplier_id": "SUP001",
      "name": "Global Parts Inc",
      "country": "USA",
      "reliability_score": 0.95
    }
  ],
  "products": [
    {
      "product_id": "PRD001",
      "name": "Circuit Board A",
      "category": "Electronics",
      "unit_price": 25.50
    }
  ],
  "relations": [
    {
      "type": "Supplies",
      "from": "SUP001",
      "to": "PRD001",
      "quantity": 1000,
      "delivery_time": 7
    }
  ]
}
```

#### Step 5: Build Knowledge Graph

Create `builder/build_supply_chain.py`:

```python
import json
from kag.builder import KGBuilder
from kag.common.conf import KAG_CONFIG

# Load data
with open('data/supply_chain_data.json', 'r') as f:
    data = json.load(f)

# Initialize builder
builder = KGBuilder(config=KAG_CONFIG)

# Build entities
for supplier in data['suppliers']:
    builder.add_entity('Supplier', supplier)

for product in data['products']:
    builder.add_entity('Product', product)

# Build relations
for relation in data['relations']:
    builder.add_relation(
        relation['type'],
        relation['from'],
        relation['to'],
        relation
    )

# Execute build
result = builder.execute()
print(f"Built {result.entity_count} entities and {result.relation_count} relations")
```

```bash
cd builder
python build_supply_chain.py
```

#### Step 6: Query and Analyze

```python
from kag.solver import KGQueryEngine

query_engine = KGQueryEngine()

# Query 1: Find all suppliers of a product
result = query_engine.query("Which suppliers provide Circuit Board A?")
print(result.answer)

# Query 2: Calculate supply chain risk
result = query_engine.query("What is the reliability score of suppliers for product PRD001?")
print(result.answer)
```

---

### Workflow 2: Question Answering with KAG

#### Step 1: Initialize KAG Project

```bash
# Create Q&A project
knext project create --prj_path ./qa_project
cd qa_project
```

#### Step 2: Configure LLM

Update `kag_config.yaml`:

```yaml
openie_llm:
  type: "openai"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"

chat_llm:
  type: "openai"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"
```

#### Step 3: Prepare Knowledge Base

```python
# builder/build_kb.py
from kag.builder import KGBuilder

# Load documents
documents = [
    "The company was founded in 2010 by John Smith.",
    "Our main product is cloud-based analytics software.",
    "We serve over 500 enterprise customers globally."
]

# Build knowledge graph from documents
builder = KGBuilder()
for doc in documents:
    builder.extract_from_text(doc)

builder.execute()
```

#### Step 4: Create Q&A Solver

```python
# solver/qa_system.py
from kag.solver import KAGSolver

# Initialize solver
solver = KAGSolver()

# Define question
question = "When was the company founded and by whom?"

# Get answer with reasoning
result = solver.solve(question)

print(f"Question: {question}")
print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
print(f"Reasoning Path: {result.reasoning_path}")
```

```bash
# Execute Q&A
cd solver
python qa_system.py
```

---

### Workflow 3: Multi-Hop Reasoning

#### Step 1: Build Multi-Layer Knowledge Graph

```python
# Complex knowledge graph with multiple hops
entities = [
    {"type": "Person", "id": "P1", "name": "Alice"},
    {"type": "Person", "id": "P2", "name": "Bob"},
    {"type": "Company", "id": "C1", "name": "Tech Corp"},
    {"type": "Product", "id": "PR1", "name": "AI Platform"}
]

relations = [
    {"type": "WorksFor", "from": "P1", "to": "C1"},
    {"type": "Manages", "from": "P2", "to": "P1"},
    {"type": "Develops", "from": "C1", "to": "PR1"}
]
```

#### Step 2: Configure Reasoner

Update `kag_config.yaml`:

```yaml
reasoner:
  max_hops: 3  # Allow up to 3-hop reasoning
  confidence_threshold: 0.6
  reasoning_mode: "hybrid"
```

#### Step 3: Execute Multi-Hop Query

```python
from kag.solver import KAGSolver

solver = KAGSolver()

# Multi-hop question requiring reasoning
question = "What product does Alice's manager's company develop?"

# This requires 3 hops:
# Alice -> WorksFor -> Tech Corp -> Develops -> AI Platform
# Bob -> Manages -> Alice

result = solver.solve(question)

print(f"Answer: {result.answer}")
print(f"Reasoning Hops: {len(result.reasoning_path)}")
for i, hop in enumerate(result.reasoning_path):
    print(f"  Hop {i+1}: {hop}")
```

---

## API Usage

### Python API

#### 1. Knowledge Graph Builder API

```python
from kag.builder import KGBuilder, Entity, Relation
from kag.common.conf import KAG_CONFIG

# Initialize builder
builder = KGBuilder(config=KAG_CONFIG)

# Add entities
person = Entity(
    type="Person",
    id="P001",
    properties={
        "name": "Jane Doe",
        "age": 28,
        "occupation": "Data Scientist"
    }
)
builder.add_entity(person)

# Add relations
relation = Relation(
    type="WorksFor",
    from_id="P001",
    to_id="C001",
    properties={
        "position": "Senior Data Scientist",
        "start_date": "2022-01-15"
    }
)
builder.add_relation(relation)

# Execute build
result = builder.execute()
print(f"Status: {result.status}")
print(f"Entities: {result.entity_count}")
print(f"Relations: {result.relation_count}")
```

#### 2. Query Engine API

```python
from kag.solver import KGQueryEngine, QueryType

# Initialize query engine
query_engine = KGQueryEngine()

# Execute natural language query
result = query_engine.query(
    question="Who are the data scientists at Tech Corp?",
    query_type=QueryType.ENTITY_SEARCH,
    max_results=10
)

# Process results
for entity in result.entities:
    print(f"Name: {entity.properties['name']}")
    print(f"Position: {entity.properties['occupation']}")
```

#### 3. Reasoner API

```python
from kag.reasoner import KGReasoner, ReasoningStrategy

# Initialize reasoner
reasoner = KGReasoner()

# Execute reasoning with specific strategy
result = reasoner.reason(
    query="Find all products manufactured by suppliers in Asia",
    strategy=ReasoningStrategy.GRAPH_TRAVERSAL,
    max_hops=3
)

print(f"Results: {len(result.entities)}")
for entity in result.entities:
    print(f"  - {entity.properties['name']}")
```

#### 4. KAG Solver API

```python
from kag.solver import KAGSolver, SolverConfig

# Configure solver
config = SolverConfig(
    reasoning_mode="hybrid",
    confidence_threshold=0.7,
    max_hops=3,
    retrieval_k=5
)

# Initialize solver
solver = KAGSolver(config=config)

# Solve complex question
question = "What is the relationship between suppliers and product quality in the supply chain?"
result = solver.solve(question)

print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Sources: {len(result.source_documents)}")
print(f"Reasoning Steps: {len(result.reasoning_path)}")
```

#### 5. Batch Processing API

```python
from kag.builder import BatchBuilder

# Batch process multiple documents
documents = [
    "Document 1 content...",
    "Document 2 content...",
    "Document 3 content..."
]

batch_builder = BatchBuilder(
    batch_size=100,
    workers=4,
    enable_parallel=True
)

# Process in batches
results = batch_builder.process_documents(documents)

print(f"Processed {len(results)} documents")
print(f"Total entities: {sum(r.entity_count for r in results)}")
```

### REST API

OpenSPG server exposes REST APIs for integration.

#### Authentication

```bash
# Get access token
curl -X POST http://127.0.0.1:8887/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "openspg",
    "password": "openspg@kag"
  }'

# Response: {"token": "eyJhbGciOiJIUzI1NiIs..."}
```

#### Create Project

```bash
curl -X POST http://127.0.0.1:8887/api/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyProject",
    "description": "My knowledge graph project",
    "namespace": "default"
  }'
```

#### Upload Schema

```bash
curl -X POST http://127.0.0.1:8887/api/projects/MyProject/schema \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "entities": [
      {
        "type": "Person",
        "properties": [
          {"name": "name", "type": "String"},
          {"name": "age", "type": "Integer"}
        ]
      }
    ]
  }'
```

#### Query Knowledge Graph

```bash
curl -X POST http://127.0.0.1:8887/api/projects/MyProject/query \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Who are the people in the knowledge graph?",
    "max_results": 10
  }'
```

#### Import Data

```bash
curl -X POST http://127.0.0.1:8887/api/projects/MyProject/import \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@data.csv" \
  -F "format=csv" \
  -F "entity_type=Person"
```

---

## Examples and Tutorials

### Example 1: Enterprise Supply Chain KG

**Goal**: Build a supply chain knowledge graph tracking suppliers, products, and factories.

**Files**: Available at `kag/examples/supply_chain/`

**Key Steps**:
1. Define supply chain schema
2. Import supplier and product data
3. Build relationships (supplies, manufactures)
4. Query for supply chain risk analysis
5. Implement reasoner for logistics optimization

**Run Example**:
```bash
cd kag/examples/supply_chain
python builder/indexer.py
python solver/supply_chain_query.py
```

### Example 2: Risk Mining Knowledge Graph

**Goal**: Detect risk patterns in financial transactions.

**Files**: Available at `kag/examples/risk_mining/`

**Key Steps**:
1. Model risk entities (transactions, accounts, alerts)
2. Extract patterns from transaction logs
3. Apply risk detection rules
4. Query for suspicious activity
5. Generate risk reports

**Run Example**:
```bash
cd kag/examples/risk_mining
knext builder execute
knext reasoner execute
```

### Example 3: Medical Knowledge Graph

**Goal**: Build medical knowledge graph for clinical decision support.

**Files**: Available at `kag/examples/medical/`

**Key Steps**:
1. Model medical entities (diseases, symptoms, treatments)
2. Import medical literature and guidelines
3. Link symptoms to diseases
4. Implement diagnostic reasoner
5. Q&A for clinical queries

**Run Example**:
```bash
cd kag/examples/medical
python builder/medical_kg_builder.py
python solver/clinical_qa.py
```

### Example 4: 2Wiki Multi-Hop Q&A

**Goal**: Answer complex questions requiring multi-hop reasoning.

**Dataset**: 2wiki with 6,119 documents (subset with 3 documents for testing)

**Files**: Available at `kag/examples/2wiki/`

**Setup**:
```bash
cd kag/examples/2wiki

# Update LLM configuration in kag_config.yaml
# Update vectorization model configuration
```

**Build Knowledge Graph**:
```bash
cd builder
python indexer.py
cd ..
```

**Run Evaluation**:
```bash
cd solver
python evaFor2wiki.py
# Generates answers and calculates EM (Exact Match) and F1 metrics
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Login Credentials Issue

**Problem**: Don't know the username and password for logging in.

**Solution**:
- Default username: `openspg`
- Default password: `openspg@kag`
- For Docker installation, these are set automatically
- For manual installation, configure in `application.properties`

#### 2. Docker Image Download Failures

**Problem**: Timeout errors when downloading Docker images from default registry.

**Symptoms**:
```
Error: failed to pull image: timeout
```

**Solutions**:

**Option 1**: Use alternative registry (for users in China)
```bash
# Use China-based registry
curl -sSL https://raw.githubusercontent.com/OpenSPG/openspg/refs/heads/master/dev/release/docker-compose.yml -o docker-compose.yml
docker compose -f docker-compose.yml up -d
```

**Option 2**: Configure Docker mirror
```bash
# Add to /etc/docker/daemon.json (Linux)
{
  "registry-mirrors": [
    "https://registry.docker-cn.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}

# Restart Docker
sudo systemctl restart docker
```

**Option 3**: Use proxy
```bash
# Set proxy for Docker
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
docker compose up -d
```

#### 3. Performance Issues with Local Models

**Problem**: Very slow knowledge graph extraction when using local models (processing takes over a day).

**Symptoms**:
- High CPU/RAM usage
- Slow progress on document processing
- Long response times for Q&A

**Solutions**:

**Option 1**: Use cloud-based LLMs
```yaml
# In kag_config.yaml, switch to OpenAI or other cloud providers
openie_llm:
  type: "openai"
  model: "gpt-4-turbo"
  api_key: "${OPENAI_API_KEY}"
```

**Option 2**: Optimize local model settings
```yaml
# Reduce batch size and enable parallel processing
builder:
  batch_size: 50  # Reduce from 100
  workers: 2      # Reduce worker count
  enable_parallel: true
```

**Option 3**: Use smaller dataset for testing
```bash
# Use the 3-document subset instead of full 6,119 documents
cp kag/examples/2wiki/builder/data/2wiki_corpus_sub.json kag/examples/2wiki/builder/data/2wiki_corpus.json
```

**Option 4**: Upgrade hardware
- Minimum: 16GB RAM, 8 CPU cores
- Recommended: 32GB RAM, 16 CPU cores
- Consider GPU acceleration for embedding models

#### 4. Port Already in Use

**Problem**: Port 8887 is already occupied.

**Solution**:

**Option 1**: Stop conflicting service
```bash
# Find process using port 8887
lsof -i :8887  # Linux/macOS
netstat -ano | findstr :8887  # Windows

# Kill the process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows
```

**Option 2**: Change OpenSPG port
```bash
# Edit docker-compose.yml
ports:
  - "8888:8887"  # Map to different host port

# Or in application.properties
server.port=8888
```

#### 5. Python Package Installation Errors

**Problem**: `pip install -e .` fails with dependency conflicts.

**Solutions**:

**Option 1**: Use clean virtual environment
```bash
# Remove old environment
conda env remove -n kag-demo

# Create fresh environment
conda create -n kag-demo python=3.10
conda activate kag-demo
pip install --upgrade pip
pip install -e .
```

**Option 2**: Install dependencies separately
```bash
# Install core dependencies first
pip install torch transformers openai

# Then install KAG
pip install -e . --no-deps
pip install -r requirements.txt
```

#### 6. Schema Commit Failures

**Problem**: `knext schema commit` fails with validation errors.

**Solution**:

**Check 1**: Validate schema syntax
```bash
# Use schema validator
knext schema validate schema/MySchema.schema
```

**Check 2**: Ensure server is running
```bash
# Check server status
curl http://127.0.0.1:8887/api/health

# If down, restart
docker compose restart  # Docker installation
# Or restart server manually
```

**Check 3**: Review schema errors
```bash
# Enable debug logging
export KNEXT_LOG_LEVEL=DEBUG
knext schema commit
```

#### 7. Memory Errors During Build

**Problem**: Out of memory errors when building large knowledge graphs.

**Solutions**:

**Option 1**: Reduce batch size
```yaml
# In kag_config.yaml
builder:
  batch_size: 50  # Reduce from 100
  workers: 2      # Reduce worker count
```

**Option 2**: Process incrementally
```python
# Split data into chunks
chunk_size = 1000
for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    builder.build(chunk)
```

**Option 3**: Increase Docker memory limit
```yaml
# In docker-compose.yml
services:
  openspg:
    deploy:
      resources:
        limits:
          memory: 8G  # Increase from default
```

#### 8. Authentication Errors

**Problem**: API calls return 401 Unauthorized.

**Solution**:

**Check 1**: Verify credentials
```bash
# Test login
curl -X POST http://127.0.0.1:8887/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "openspg", "password": "openspg@kag"}'
```

**Check 2**: Check token expiration
```python
# Tokens expire after 24 hours by default
# Refresh token or re-authenticate
```

**Check 3**: Verify Authorization header
```bash
# Ensure Bearer token format
curl -H "Authorization: Bearer YOUR_TOKEN" ...
```

#### 9. Web Interface Not Loading

**Problem**: Browser shows "Connection refused" or blank page.

**Solutions**:

**Check 1**: Verify all services are running
```bash
docker compose ps
# All services should show "Up" status
```

**Check 2**: Check logs for errors
```bash
docker compose logs -f
```

**Check 3**: Try different browser or clear cache
```bash
# Chrome/Firefox: Clear cache and cookies for localhost
# Try incognito/private mode
```

**Check 4**: Check firewall
```bash
# Linux: Allow port 8887
sudo ufw allow 8887

# Windows: Add firewall rule for port 8887
```

#### 10. EISDIR Error When Reading Directories

**Problem**: `Read()` tool fails with "EISDIR: illegal operation on a directory".

**Solution**:

**❌ Wrong**: Using Read() on directories
```python
Read("/path/to/directory/")  # This causes EISDIR error
```

**✅ Correct**: Use Bash or Glob to explore directories
```python
# First, explore directory with Bash or Glob
Bash("ls -la /path/to/directory/")
Glob("/path/to/directory/**/*.md")

# Then read specific files
Read("/path/to/directory/file1.md")
Read("/path/to/directory/file2.py")
```

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
# Set environment variable
export OPENSPG_DEBUG=true
export KNEXT_LOG_LEVEL=DEBUG

# Run command with debug output
knext --debug builder execute
```

### Getting Help

**Official Resources**:
- GitHub Issues: https://github.com/OpenSPG/openspg/issues
- Documentation: https://openspg.yuque.com/ndx6g9/docs_en
- Discussions: https://github.com/OpenSPG/openspg/discussions

**Community Support**:
- Open an issue on GitHub with:
  - Detailed problem description
  - Steps to reproduce
  - Error messages and logs
  - System information (OS, Python version, etc.)

---

## Best Practices

### 1. Schema Design

**✅ Do**:
- Start with core entities and gradually expand
- Use meaningful, descriptive names for entities and relations
- Define clear property types and constraints
- Document schema design decisions
- Version control your schemas

**❌ Don't**:
- Over-complicate initial schema with too many entities
- Use generic names like "Entity1", "Relation1"
- Mix different granularities in same schema
- Ignore data quality validation rules

**Example Good Schema**:
```python
Entity Customer {
    customer_id: String primary;
    full_name: String required;
    email: Email unique;
    registration_date: Date;
}
```

### 2. Data Quality

**✅ Do**:
- Validate data before import
- Clean and normalize text fields
- Handle missing values explicitly
- Use entity resolution for duplicates
- Maintain data lineage

**❌ Don't**:
- Import raw data without validation
- Ignore duplicate entities
- Skip data quality checks for speed
- Lose track of data sources

**Example Validation**:
```python
def validate_entity(entity):
    assert entity.get('id'), "Entity must have ID"
    assert entity.get('name'), "Entity must have name"
    assert '@' in entity.get('email', '@'), "Invalid email"
    return entity
```

### 3. Performance Optimization

**✅ Do**:
- Batch operations when possible (100-1000 entities per batch)
- Use parallel processing for large datasets
- Enable caching for frequently accessed data
- Monitor and optimize query performance
- Use appropriate indexes

**❌ Don't**:
- Process one entity at a time
- Load entire dataset into memory
- Run complex queries without limits
- Ignore performance metrics

**Example Batch Processing**:
```python
batch_size = 100
for i in range(0, len(entities), batch_size):
    batch = entities[i:i+batch_size]
    builder.add_entities_batch(batch)
```

### 4. Configuration Management

**✅ Do**:
- Use environment variables for sensitive data
- Version control configuration files (excluding secrets)
- Document configuration parameters
- Use different configs for dev/test/prod
- Keep backups of working configurations

**❌ Don't**:
- Hardcode API keys in code
- Commit secrets to version control
- Use production credentials in development
- Leave default passwords unchanged

**Example Configuration**:
```yaml
# kag_config.yaml
openie_llm:
  type: "openai"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"  # From environment
```

### 5. Error Handling

**✅ Do**:
- Implement try-catch for all API calls
- Log errors with context information
- Provide meaningful error messages
- Implement retry logic for transient failures
- Gracefully handle partial failures

**❌ Don't**:
- Silent error suppression
- Generic error messages
- Crash on first error in batch
- Ignore retry opportunities

**Example Error Handling**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def build_entity(entity):
    try:
        return builder.add_entity(entity)
    except Exception as e:
        logger.error(f"Failed to build entity {entity.get('id')}: {e}")
        raise
```

### 6. Testing

**✅ Do**:
- Test schema validation before deployment
- Use small dataset for initial testing
- Implement unit tests for custom operators
- Test edge cases and error conditions
- Validate reasoning results

**❌ Don't**:
- Skip testing on small dataset first
- Test only happy paths
- Assume production data matches test data
- Deploy without validation

**Example Test**:
```python
def test_entity_creation():
    entity = {"type": "Person", "name": "Test User"}
    result = builder.add_entity(entity)
    assert result.status == "success"
    assert result.entity_id is not None
```

### 7. Monitoring and Logging

**✅ Do**:
- Log all critical operations
- Monitor system resource usage
- Track query performance metrics
- Set up alerts for failures
- Regularly review logs

**❌ Don't**:
- Disable logging in production
- Ignore warning messages
- Let log files grow unbounded
- Miss critical error patterns

**Example Logging**:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Building KG with {len(entities)} entities")
logger.warning(f"Low confidence result: {confidence}")
logger.error(f"Build failed: {error}")
```

### 8. Documentation

**✅ Do**:
- Document schema design rationale
- Maintain API usage examples
- Update documentation with code changes
- Include troubleshooting guides
- Document custom operators

**❌ Don't**:
- Assume code is self-documenting
- Let documentation become outdated
- Skip examples for complex features
- Forget to document configuration

### 9. Security

**✅ Do**:
- Use HTTPS for API calls
- Rotate credentials regularly
- Implement role-based access control
- Validate and sanitize all inputs
- Keep dependencies updated

**❌ Don't**:
- Use default passwords
- Share credentials across environments
- Skip input validation
- Ignore security updates

### 10. Deployment

**✅ Do**:
- Use Docker for consistent environments
- Implement health checks
- Plan for zero-downtime updates
- Backup data before upgrades
- Monitor deployment success

**❌ Don't**:
- Deploy without testing
- Skip backup procedures
- Upgrade all components simultaneously
- Deploy on Friday afternoon 😊

---

## References

### Official Resources

1. **GitHub Repositories**:
   - OpenSPG: https://github.com/OpenSPG/openspg
   - KAG: https://github.com/OpenSPG/KAG
   - OneKE: https://github.com/OpenSPG/OneKE
   - KAG-Thinker: https://github.com/OpenSPG/KAG-Thinker

2. **Documentation**:
   - OpenSPG Docs (English): https://openspg.yuque.com/ndx6g9/docs_en
   - User Guide: https://openspg.yuque.com/ndx6g9/docs_en/rs7gr8g4s538b1n7
   - Contribution Guidelines: https://openspg.yuque.com/ndx6g9/docs_en/ae57imdlmnwa5rls

3. **Community**:
   - GitHub Issues: https://github.com/OpenSPG/openspg/issues
   - GitHub Discussions: https://github.com/OpenSPG/openspg/discussions

### Related Technologies

1. **Knowledge Graphs**:
   - OpenKG: http://openkg.cn
   - Knowledge Graph Construction: Various academic papers

2. **Large Language Models**:
   - OpenAI API: https://platform.openai.com/docs
   - Hugging Face Transformers: https://huggingface.co/docs/transformers

3. **Graph Databases**:
   - TuGraph: https://github.com/TuGraph-family/tugraph-db
   - Neo4j: https://neo4j.com/docs

### Academic Papers

1. **SPG Framework**:
   - SPG White Paper (referenced in OpenSPG repository)
   - Semantic-enhanced Programmable Graph papers

2. **Knowledge Graph Construction**:
   - Entity extraction and linking
   - Knowledge fusion and reasoning

3. **Knowledge Augmented Generation**:
   - KAG vs RAG comparison
   - Logical form-guided reasoning

### Tutorials and Guides

1. **Blog Posts**:
   - "KAG: Knowledge Augmented Generation - A Practical Guide better than Rag"
     https://plainenglish.io/blog/kag-knowledge-augmented-generation-a-pratical-guide-better-than-rag

2. **Video Tutorials**:
   - Check OpenSPG GitHub organization for video links
   - Community-contributed tutorials

3. **Example Projects**:
   - Supply Chain KG
   - Risk Mining KG
   - Medical KG
   - 2Wiki Multi-Hop Q&A

### Tools and Libraries

1. **Python Libraries**:
   - `openspg-kag`: https://pypi.org/project/openspg-kag/
   - Related NLP libraries (spaCy, transformers)

2. **Development Tools**:
   - Docker: https://docs.docker.com
   - Python: https://docs.python.org
   - Maven: https://maven.apache.org/guides

### Support Channels

1. **GitHub Issues**: For bug reports and feature requests
2. **GitHub Discussions**: For questions and community help
3. **Documentation**: For official guides and references

---

## Version History

- **v1.0.0** (2025-10-26): Initial comprehensive usage guide
  - Installation instructions (Docker and non-Docker)
  - Configuration guide
  - Core concepts and workflows
  - API usage documentation
  - Examples and tutorials
  - Troubleshooting guide
  - Best practices

---

## Contributing to This Guide

This guide is community-maintained. To contribute:

1. Fork the repository
2. Make improvements or corrections
3. Submit a pull request
4. Include clear description of changes

**Areas for Contribution**:
- Additional examples and use cases
- More troubleshooting scenarios
- Performance optimization tips
- Integration guides with other tools
- Translation to other languages

---

## License

This documentation follows the same license as OpenSPG (Apache 2.0).

---

## Contact

For questions about this guide:
- Open an issue: https://github.com/OpenSPG/openspg/issues
- Discussion forum: https://github.com/OpenSPG/openspg/discussions

---

*Last Updated: 2025-10-26*
*Document Version: 1.0.0*
*OpenSPG Version: Latest*
*KAG Version: v0.8.0+*
