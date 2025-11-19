# Quick Start Guide - NLP Ingestion Pipeline

Get up and running with the NLP ingestion pipeline in 5 minutes.

## Prerequisites

- Python 3.8+
- Neo4j 5.0+ running on `bolt://localhost:7687`
- Documents to process (MD, TXT, PDF, DOCX, JSON)

## Installation (2 minutes)

```bash
# Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney

# Activate virtual environment (already created)
source venv/bin/activate

# Verify installation
python -c "import spacy; print('spaCy:', spacy.__version__)"
python -c "import neo4j; print('Neo4j:', neo4j.__version__)"
```

## Run Demo (1 minute)

See the pipeline in action without Neo4j:

```bash
python demo.py
```

**Expected output**:
- 41 entities extracted (CVEs, organizations, people, locations)
- 23 relationships extracted (SVO triples, prepositional)
- 1 table extracted with 3 rows
- Complete analysis summary

## Run Tests (1 minute)

Verify everything works:

```bash
python test_pipeline.py
```

**Expected**: All 6 tests pass ✅

## Process Your Documents (1 minute)

### Option 1: Single File

```bash
python nlp_ingestion_pipeline.py your_document.md \
  --neo4j-password YOUR_PASSWORD
```

### Option 2: Directory

```bash
python nlp_ingestion_pipeline.py /path/to/your/documents \
  --neo4j-password YOUR_PASSWORD \
  --pattern "**/*.md"
```

### Option 3: Multiple Formats

```bash
python nlp_ingestion_pipeline.py /path/to/documents \
  --neo4j-password YOUR_PASSWORD \
  --pattern "**/*.{md,txt,pdf,docx}"
```

## Verify Results in Neo4j

```bash
# Connect to Neo4j
cypher-shell -u neo4j -p YOUR_PASSWORD

# Count documents
MATCH (d:Document) RETURN count(d);

# List top entities
MATCH (e:Entity)
RETURN e.label, e.text, e.count
ORDER BY e.count DESC
LIMIT 10;

# View sample relationships
MATCH (s:Entity)-[r:RELATIONSHIP]->(o:Entity)
RETURN s.text, r.predicate, o.text
LIMIT 5;
```

## Common Commands

### Resume Processing
```bash
# Automatically skips already-processed files
python nlp_ingestion_pipeline.py /path/to/documents --neo4j-password PWD
```

### Fresh Start
```bash
# Clear progress and reprocess everything
rm .ingestion_progress.json
python nlp_ingestion_pipeline.py /path/to/documents --neo4j-password PWD
```

### High-Performance Mode
```bash
# Use transformer model and larger batches
python nlp_ingestion_pipeline.py /path/to/documents \
  --neo4j-password PWD \
  --spacy-model en_core_web_trf \
  --batch-size 200
```

### Process Specific File Types
```bash
# Only markdown files
python nlp_ingestion_pipeline.py /path/to/docs --neo4j-password PWD --pattern "**/*.md"

# Only PDFs
python nlp_ingestion_pipeline.py /path/to/docs --neo4j-password PWD --pattern "**/*.pdf"

# All supported formats
python nlp_ingestion_pipeline.py /path/to/docs --neo4j-password PWD --pattern "**/*.{md,txt,pdf,docx,json}"
```

## What Gets Extracted?

### Entities
- **People**: John Smith, Dr. Sarah Chen
- **Organizations**: Microsoft, Google, Apache
- **Locations**: New York, California
- **CVEs**: CVE-2024-1234
- **CAPECs**: CAPEC-63
- **CWEs**: CWE-89
- **ATT&CK Techniques**: T1190
- **IP Addresses**: 192.168.1.100
- **Hashes**: MD5, SHA1, SHA256
- **URLs**: https://example.com

### Relationships
- **SVO Triples**: "vulnerability allows execution"
- **Prepositional**: "attack from China"
- **Context**: Full sentence preserved

### Tables
- Markdown tables converted to structured data
- Preserved in Neo4j for querying

### Metadata
- SHA256 hash (deduplication)
- File path, name, size
- Processing timestamp
- Character/line counts

## Useful Neo4j Queries

### Find All CVEs
```cypher
MATCH (e:Entity {label: 'CVE'})
RETURN e.text, e.count
ORDER BY e.count DESC;
```

### Search Documents
```cypher
CALL db.index.fulltext.queryNodes('document_fulltext', 'vulnerability exploit')
YIELD node, score
RETURN node.content, score
LIMIT 5;
```

### Entity Co-occurrence
```cypher
MATCH (d:Document)-[:CONTAINS_ENTITY]->(e1:Entity),
      (d)-[:CONTAINS_ENTITY]->(e2:Entity)
WHERE e1.label = 'CVE' AND e2.label = 'ORG'
RETURN e1.text, collect(DISTINCT e2.text) as organizations
LIMIT 10;
```

### Relationship Exploration
```cypher
MATCH (s:Entity)-[r:RELATIONSHIP]->(o:Entity)
WHERE s.label = 'ORG' AND o.label = 'PRODUCT'
RETURN s.text, r.predicate, o.text, r.sentence
LIMIT 10;
```

## Troubleshooting

### "No module named 'spacy'"
```bash
source venv/bin/activate  # You forgot to activate the venv
```

### "Can't find model 'en_core_web_lg'"
```bash
python -m spacy download en_core_web_lg
```

### "Connection refused to bolt://localhost:7687"
```bash
# Check if Neo4j is running
systemctl status neo4j
# Or start it
systemctl start neo4j
```

### "ImportError: pdfplumber"
```bash
pip install pdfplumber
```

### Processing Too Slow
```bash
# Use smaller spaCy model
python nlp_ingestion_pipeline.py docs/ \
  --spacy-model en_core_web_sm \
  --neo4j-password PWD
```

### Out of Memory
```bash
# Reduce batch size
python nlp_ingestion_pipeline.py docs/ \
  --batch-size 50 \
  --neo4j-password PWD
```

## Performance Expectations

- **Speed**: 10-20 documents/minute (depends on size and format)
- **Entities**: 20-100 per document (varies by content)
- **Relationships**: 10-50 per document
- **Memory**: ~500MB for spaCy model + processing overhead
- **Neo4j**: Scales to millions of entities/relationships

## Next Steps

1. **Process Your Corpus**: Run pipeline on your 932 documents
2. **Explore Graph**: Use Neo4j Browser to visualize relationships
3. **Query Data**: Write Cypher queries for your use case
4. **Integrate**: Connect to your application via Neo4j driver
5. **Customize**: Add custom entity patterns or relationship extractors

## Support

- **Documentation**: See README.md for complete details
- **Examples**: Check example_usage.sh for more commands
- **Testing**: Run test_pipeline.py to verify functionality
- **Demo**: Run demo.py to see capabilities

## Files in Project

```
nlp_ingestion_pipeline.py  # Main pipeline (1,100 lines)
test_pipeline.py           # Test suite
demo.py                    # Interactive demo
requirements.txt           # Dependencies
README.md                  # Full documentation
QUICKSTART.md              # This file
PROJECT_SUMMARY.md         # Complete project overview
example_usage.sh           # Usage examples
```

---

**You're ready to go!** Process your documents and explore the graph.
