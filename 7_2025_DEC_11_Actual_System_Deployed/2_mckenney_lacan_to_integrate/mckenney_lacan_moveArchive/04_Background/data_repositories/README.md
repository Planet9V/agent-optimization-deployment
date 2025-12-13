# Demographic Data Repositories for Knowledge Graph

This directory contains tools and resources for collecting, normalizing, and structuring demographic data for ingestion into the McKenney-Lacan Knowledge Graph.

## Directory Structure

- **world_bank/**: Contains tools for fetching World Bank data.
  - `fetch_world_bank_data.py`: Script to fetch and normalize data.
  - `data/`: Output directory for World Bank JSON artifacts.
- **us_census/**: Placeholders and documentation for US Census Bureau data integration.
- **kaggle_datasets/**: Documentation and storage for manually downloaded Kaggle datasets.
- `requirements.txt`: Shared Python dependencies.

## Unified Data Schema

To ensure compatibility with our Knowledge Graph (e.g., Qdrant, Neo4j), all data is normalized into the following entity structure:

```json
{
  "id": "wb:USA",                  // Unique Identifier (Source Prefix + Original ID)
  "type": "GeographicRegion",      // Node Label
  "name": "United States",         // Human-readable Name
  "parent_id": null,               // For hierarchy (e.g., State -> Country)
  "attributes": [
    {
      "metric": "population_total",
      "value": 333287557,
      "year": 2022,
      "source": "World Bank (SP.POP.TOTL)",
      "timestamp": 1709543210.123
    }
  ]
}
```

## How to Collect Data

### World Bank
Navigate to `world_bank/` and follow the instructions in the script or run:
```bash
python world_bank/fetch_world_bank_data.py
```

### US Census & Kaggle
See the `README.md` files in their respective directories for specific setup and download instructions.

