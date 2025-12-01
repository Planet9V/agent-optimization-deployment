# KAG Quick Reference Guide

## Environment Setup

```bash
# Activate KAG environment
cd /home/jim/2_OXOT_Projects_Dev
source venv/bin/activate

# Verify KAG installation
python -c "import kag; print(f'KAG version: {kag.__version__}')"
```

## Create New KAG Project

### Using Interactive Script (Recommended)
```bash
cd /home/jim/2_OXOT_Projects_Dev
./scripts/create_kag_project.sh
```

### Manual Creation
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples

# Create project
knext project create --config_path ./my_config.yaml

# Update existing project
cd MyProject
knext project update --proj_path .
```

## Project Management

```bash
# List all projects
knext project list

# Delete project
knext project delete --namespace MyProject

# Check project structure
cd MyProject
tree -L 2
```

## Building Knowledge Graph

```bash
cd MyProject/builder

# Create/edit data file
vim data/my_data.json

# Run builder
python indexer.py

# Check progress
wc -l ckpt/kag_checkpoint_0_1.ckpt

# View extraction results
less ckpt/kag_checkpoint_0_1.ckpt
```

## Schema Management

```bash
cd MyProject

# Edit schema
vim schema/MyProject.schema

# Commit schema to OpenSPG
knext schema commit

# View schema in Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL db.schema.visualization()"
```

## Querying Knowledge Base

```bash
cd MyProject/solver

# Create query script
vim qa.py

# Run queries
python qa.py
```

### Sample Query Script
```python
from kag.solver.logic.solver_pipeline import SolverPipeline
from kag.common.conf import KAG_CONFIG

class KAGQuery:
    def qa(self, query):
        solver = SolverPipeline.from_config(
            KAG_CONFIG.all_config["kag_solver_pipeline"]
        )
        answer, trace = solver.run(query)
        return answer

# Usage
kag = KAGQuery()
answer = kag.qa("Your question here?")
print(answer)
```

## Neo4j Verification

```bash
# Query Neo4j from command line
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN labels(n) as Type, count(*) as Count"

# Check relationships
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH ()-[r]->() RETURN type(r) as RelationType, count(*) as Count"

# Export graph data
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100" > graph_export.txt
```

## Data Formats

### JSON Input Format
```json
[
  {
    "id": "unique_doc_id",
    "name": "Document Title",
    "content": "Full text content of the document..."
  }
]
```

### CSV Input Format
Requires custom scanner implementation in `builder/` directory.

## Common Tasks

### Add New Documents
```bash
cd MyProject/builder

# Add documents to data/
cp ~/new_documents.json data/

# Update indexer.py with new file path
vim indexer.py

# Run builder
python indexer.py
```

### Update Configuration
```bash
cd MyProject

# Edit configuration
vim kag_config.yaml

# Update to server
knext project update --proj_path .
```

### Backup Knowledge Graph
```bash
# Backup Neo4j data
docker exec openspg-neo4j neo4j-admin database dump neo4j \
  --to-path=/shared/backup_$(date +%Y%m%d).dump

# Copy to host
docker cp openspg-neo4j:/shared/backup_20251026.dump ./backups/
```

### Restore Knowledge Graph
```bash
# Copy backup to container
docker cp ./backups/backup_20251026.dump openspg-neo4j:/shared/

# Stop services
cd /home/jim/2_OXOT_Projects_Dev
docker-compose stop openspg-server

# Restore database
docker exec openspg-neo4j neo4j-admin database load neo4j \
  --from-path=/shared/backup_20251026.dump --overwrite-destination

# Restart services
docker-compose start openspg-server
```

## Troubleshooting

### Check Service Status
```bash
cd /home/jim/2_OXOT_Projects_Dev
docker-compose ps
docker-compose logs -f openspg-server
```

### Test OpenSPG Connection
```bash
curl -f http://localhost:8887/health
```

### Test Neo4j Connection
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"
```

### Clear Checkpoints
```bash
cd MyProject/builder
rm -rf ckpt/
```

### Reset Project Data
```bash
# This will delete all data in Neo4j for this namespace
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) WHERE n.namespace = 'MyProject' DETACH DELETE n"
```

## Configuration Templates

### Minimal Config (Local LLM)
```yaml
project:
  host_addr: http://127.0.0.1:8887
  namespace: MyProject
  language: en

chat_llm:
  type: maas
  base_url: http://localhost:11434/v1  # Ollama
  model: llama2
  api_key: dummy
```

### Production Config (Cloud LLM)
```yaml
chat_llm:
  type: maas
  base_url: https://api.openai.com/v1
  model: gpt-4
  api_key: ${OPENAI_API_KEY}

vectorize_model:
  type: openai
  base_url: https://api.openai.com/v1
  model: text-embedding-3-large
  api_key: ${OPENAI_API_KEY}
  vector_dimensions: 3072
```

## Performance Tips

### Optimize Builder Performance
- Increase `num_chains` for parallel processing (default: 16)
- Adjust `split_length` for document chunking (default: 100000)
- Use `num_threads_per_chain` for multi-threading (default: 1)

### Optimize Query Performance
- Tune `recall_num` and `rerank_topk` in retrievers
- Adjust `el_num` (entity linking number) for accuracy/speed tradeoff
- Use `force_chunk_retriever: false` for pure graph reasoning

### Monitor Resource Usage
```bash
# Check container resources
docker stats openspg-server openspg-neo4j

# Check Neo4j memory
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL dbms.queryJmx('java.lang:type=Memory') YIELD attributes"
```

## Integration Examples

### Python Application
```python
from kag.solver.logic.solver_pipeline import SolverPipeline
from kag.common.conf import KAG_PROJECT_CONF

# Initialize
KAG_PROJECT_CONF.init_from_file("path/to/kag_config.yaml")
solver = SolverPipeline.from_config(
    KAG_PROJECT_CONF.all_config["kag_solver_pipeline"]
)

# Query
answer, trace = solver.run("Your question?")
```

### REST API Wrapper
```python
from flask import Flask, request, jsonify
from kag.solver.logic.solver_pipeline import SolverPipeline

app = Flask(__name__)
solver = SolverPipeline.from_config(config)

@app.route("/query", methods=["POST"])
def query():
    question = request.json["question"]
    answer, _ = solver.run(question)
    return jsonify({"answer": answer})
```

## Useful Commands Summary

```bash
# Environment
source venv/bin/activate

# Project
knext project create --config_path config.yaml
knext project list
knext schema commit

# Build
cd builder && python indexer.py

# Query
cd solver && python qa.py

# Verify
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) RETURN n LIMIT 25"
```

## Resources

- **Documentation**: /home/jim/2_OXOT_Projects_Dev/docs/KAG_DATABASE_SETUP.md
- **OpenSPG UI**: http://localhost:8887
- **Neo4j Browser**: http://localhost:7474
- **KAG GitHub**: https://github.com/OpenSPG/KAG
- **OpenSPG Docs**: https://openspg.yuque.com/ndx6g9/cwh47i

## Next Steps

1. **Create your first project**: Run `./scripts/create_kag_project.sh`
2. **Build knowledge graph**: Add your documents and run the builder
3. **Test queries**: Try Q&A with your knowledge base
4. **Explore in Neo4j**: Visualize your knowledge graph
5. **Integrate**: Use KAG in your applications
