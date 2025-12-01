# Document Processing Scripts for Cybersecurity Threat Intelligence

Automated document processing pipeline for extracting entities, relationships, and structured data from cybersecurity documents.

## Scripts Overview

### 1. nlp_entity_extractor.py
Extract entities using spaCy NLP with custom cybersecurity patterns.

**Features:**
- Named entity recognition (ORG, PRODUCT, GPE, etc.)
- Custom patterns: CVE, CWE, CAPEC, IP addresses, hashes, URLs
- Dependency parsing for relationships
- Co-occurrence analysis
- Confidence scoring
- Entity deduplication

**Usage:**
```bash
# Single file
python nlp_entity_extractor.py document.txt -o entities.json

# With relationships and co-occurrences
python nlp_entity_extractor.py document.txt --relationships --co-occurrences

# Directory processing
python nlp_entity_extractor.py /path/to/docs/ -o results.json

# Use larger spaCy model
python nlp_entity_extractor.py document.txt -m en_core_web_lg
```

### 2. pdf_processor.py
Extract text, tables, and metadata from PDF documents.

**Features:**
- Text extraction with page-level chunking
- Table extraction and structuring
- Figure/diagram detection
- Metadata extraction (title, author, dates)
- OCR fallback for scanned PDFs

**Usage:**
```bash
# Single PDF
python pdf_processor.py document.pdf -o tmp/

# Batch processing
python pdf_processor.py /path/to/pdfs/ -o tmp/results/

# With OCR for scanned PDFs
python pdf_processor.py scanned.pdf --ocr

# Skip tables and figures
python pdf_processor.py document.pdf --no-tables --no-figures
```

### 3. word_processor.py
Extract structured content from Word documents.

**Features:**
- Heading hierarchy preservation
- Table extraction
- Style and formatting preservation
- Metadata extraction
- Comments extraction (optional)

**Usage:**
```bash
# Single document
python word_processor.py document.docx -o tmp/

# Batch processing
python word_processor.py /path/to/docs/ -o tmp/results/

# Extract comments
python word_processor.py document.docx --comments

# Skip tables
python word_processor.py document.docx --no-tables
```

### 4. relationship_extractor.py
Extract relationships between entities using NLP and pattern matching.

**Features:**
- Dependency parsing for verb relationships
- Pattern matching for cybersecurity relationships (exploits, mitigates, affects, etc.)
- Co-occurrence analysis
- Confidence scoring
- Graph-ready relationship suggestions

**Usage:**
```bash
# Extract relationships
python relationship_extractor.py document.txt -o relationships.json

# Adjust co-occurrence window
python relationship_extractor.py document.txt --window 100

# Use larger model
python relationship_extractor.py document.txt -m en_core_web_lg
```

### 5. batch_document_loader.py
Parallel batch processing with Neo4j integration.

**Features:**
- Parallel processing using multiprocessing
- Progress tracking with tqdm
- Error recovery and retry logic
- Neo4j batch import
- Claude-Flow coordination hooks
- Comprehensive processing reports

**Usage:**
```bash
# Basic batch processing
python batch_document_loader.py /path/to/documents/ -o tmp/results/

# With Neo4j import
python batch_document_loader.py /path/to/docs/ --neo4j \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-password your_password

# With Claude-Flow coordination
python batch_document_loader.py /path/to/docs/ --claude-flow

# Specify file patterns
python batch_document_loader.py /path/to/docs/ --patterns "*.pdf" "*.docx"

# Control parallel workers
python batch_document_loader.py /path/to/docs/ -w 8
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Optional: Download larger model for better accuracy
python -m spacy download en_core_web_lg

# Optional: Install OCR support
pip install pytesseract Pillow
sudo apt-get install tesseract-ocr  # Linux
brew install tesseract  # macOS
```

## Configuration

Create a config file at `config/document_processing.yaml`:

```yaml
# Document Processing Configuration

nlp:
  model: en_core_web_sm  # or en_core_web_lg
  batch_size: 100
  confidence_threshold: 0.7

pdf:
  ocr_enabled: false
  extract_tables: true
  extract_figures: true
  page_chunks: true

word:
  extract_tables: true
  extract_comments: false
  preserve_formatting: true

relationships:
  co_occurrence_window: 50
  min_confidence: 0.3
  extract_patterns: true
  extract_dependencies: true

batch:
  num_workers: null  # null = auto (CPU count)
  retry_attempts: 3
  timeout_seconds: 300

neo4j:
  uri: bolt://localhost:7687
  user: neo4j
  password: your_password
  batch_size: 1000

claude_flow:
  enabled: false
  hooks: true
```

## Output Structure

### Entity Extraction Output
```json
{
  "entities": {
    "CVE": [
      {"text": "CVE-2023-12345", "start": 10, "end": 24, "confidence": 1.0}
    ],
    "ORG": [
      {"text": "Microsoft", "start": 50, "end": 59, "confidence": 0.9}
    ]
  },
  "relationships": [
    {
      "subject": "Threat Actor",
      "relation": "exploits",
      "object": "CVE-2023-12345",
      "confidence": 0.8
    }
  ]
}
```

### PDF Processing Output
```json
{
  "metadata": {
    "title": "Threat Intelligence Report",
    "author": "Security Team",
    "num_pages": 25
  },
  "text": {
    "type": "page_chunks",
    "pages": [
      {"page_number": 1, "text": "..."}
    ]
  },
  "tables": [...],
  "figures": [...]
}
```

## Integration with Neo4j

The batch loader can automatically import extracted data into Neo4j:

**Graph Schema:**
- `Document` nodes with file metadata
- `Entity` nodes with type and text
- `(Document)-[:CONTAINS]->(Entity)` relationships
- Custom relationship types: `EXPLOITS`, `MITIGATES`, `AFFECTS`, etc.

**Example Cypher Queries:**

```cypher
// Find all CVEs in documents
MATCH (d:Document)-[:CONTAINS]->(e:Entity {type: 'CVE'})
RETURN d.name, e.name

// Find exploitation relationships
MATCH (attacker:Entity)-[:EXPLOITS]->(vuln:Entity)
RETURN attacker.name, vuln.name

// Find mitigation strategies
MATCH (control:Entity)-[:MITIGATES]->(threat:Entity)
RETURN control.name, threat.name
```

## Claude-Flow Integration

When `--claude-flow` is enabled:

1. **Pre-Task Hook**: Registers batch processing task
2. **Progress Tracking**: Updates processing status
3. **Post-Task Hook**: Reports metrics and results
4. **Memory Storage**: Stores processing results for cross-session access

## Performance

- **Parallel Processing**: 4-8x faster with multiprocessing
- **Entity Extraction**: ~500-1000 docs/hour (depending on size)
- **PDF Processing**: ~100-200 pages/minute
- **Neo4j Import**: ~1000 entities/second

## Error Handling

All scripts include:
- Comprehensive error logging
- Retry logic for transient failures
- Graceful degradation
- Detailed error reporting
- Processing status tracking

## Logging

Logs are saved to `/logs/processing/`:
- `document_processing.log` - Main processing log
- `entity_extraction.log` - Entity extraction details
- `neo4j_import.log` - Database import logs
- `errors.log` - Error details

## Testing

```bash
# Test entity extraction
python nlp_entity_extractor.py ../test_data/sample.txt

# Test PDF processing
python pdf_processor.py ../test_data/sample.pdf

# Test batch processing (small batch)
python batch_document_loader.py ../test_data/ -w 2
```

## Troubleshooting

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Neo4j connection failed:**
- Check Neo4j is running: `sudo systemctl status neo4j`
- Verify credentials and URI
- Check firewall settings

**OCR not working:**
```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr
pip install pytesseract Pillow
```

**Memory issues with large documents:**
- Reduce batch size in config
- Use fewer parallel workers
- Process documents in smaller chunks

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints for new functions
3. Include docstrings with examples
4. Add unit tests for new features
5. Update this README for new capabilities

## License

MIT License - See LICENSE file for details
