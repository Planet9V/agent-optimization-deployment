#!/bin/bash
# Example usage scripts for NLP Ingestion Pipeline

# Activate virtual environment
source venv/bin/activate

# Example 1: Process single markdown file
echo "Example 1: Single file processing"
python nlp_ingestion_pipeline.py document.md \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-password your_password

# Example 2: Process directory of markdown files
echo "Example 2: Directory processing (markdown only)"
python nlp_ingestion_pipeline.py /path/to/documents \
  --neo4j-password your_password \
  --pattern "**/*.md"

# Example 3: Process multiple file types
echo "Example 3: Multi-format processing"
python nlp_ingestion_pipeline.py /path/to/documents \
  --neo4j-password your_password \
  --pattern "**/*.{md,txt,pdf,docx}"

# Example 4: High-performance processing with larger batches
echo "Example 4: High-performance configuration"
python nlp_ingestion_pipeline.py /path/to/documents \
  --neo4j-password your_password \
  --batch-size 200 \
  --spacy-model en_core_web_trf

# Example 5: Process specific subdirectory
echo "Example 5: Subdirectory processing"
python nlp_ingestion_pipeline.py /path/to/documents/reports \
  --neo4j-password your_password \
  --pattern "*.md"

# Example 6: Resume interrupted processing
echo "Example 6: Resume processing (automatically skips processed files)"
python nlp_ingestion_pipeline.py /path/to/documents \
  --neo4j-password your_password

# Example 7: Fresh processing (clear progress first)
echo "Example 7: Fresh processing"
rm -f .ingestion_progress.json
python nlp_ingestion_pipeline.py /path/to/documents \
  --neo4j-password your_password
