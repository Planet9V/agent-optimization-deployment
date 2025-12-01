# CAPEC→ATT&CK Extraction Summary

**Date**: 2025-11-08
**Task**: Extract CAPEC attack patterns with ATT&CK technique mappings from Neo4j

## Extraction Results

### Data Sources
1. **Primary Query**: CAPEC-ATT&CK relationships with full descriptions
   - Database: `openspg-neo4j`
   - Relationship: `[:IMPLEMENTS_TECHNIQUE]`
   - Records extracted: 238 unique pairs

2. **OWASP Context Query**: CAPEC-OWASP-ATT&CK mappings
   - Relationship chain: `[:MAPS_TO_OWASP]` and `[:IMPLEMENTS_TECHNIQUE]`
   - OWASP categories: 10 unique mappings

### Output File

**Location**: `/data/ner_training/v7_capec_attack_owasp.json`

**Statistics**:
- Total entries: 238
- Entries with OWASP context: 15
- Entity types: ATTACK_PATTERN, TECHNIQUE, VULNERABILITY_CLASS
- File size: 5565 lines

### Entity Types

1. **ATTACK_PATTERN**: CAPEC attack patterns
   - Format: `CAPEC-{ID}: {Name}`
   - Example: `CAPEC-112: Brute Force`

2. **TECHNIQUE**: ATT&CK techniques
   - Format: `{ID}: {Name}`
   - Example: `1110: Brute Force`

3. **VULNERABILITY_CLASS**: OWASP categories (when available)
   - Format: `OWASP Category: {Name}`
   - Example: `OWASP Category: Brute force attack`

### Sample Entry

```json
{
  "text": "CAPEC-CAPEC-112: Brute Force. In this attack, some asset (information, functionality, identity, etc.) is protected by a finite secret value. The attacker attempts to gain access to this asset by using trial-and-error to exhaustively explore all the possible secret values in the hope of finding the secret (or a value that is functionally equivalent) that will unlock the asset.. OWASP Category: Brute force attack. Implements ATT&CK Technique 1110: Brute Force. NULL",
  "entities": [
    {
      "start": 0,
      "end": 28,
      "label": "ATTACK_PATTERN",
      "text": "CAPEC-CAPEC-112: Brute Force"
    },
    {
      "start": 375,
      "end": 412,
      "label": "VULNERABILITY_CLASS",
      "text": "OWASP Category: Brute force attack"
    },
    {
      "start": 443,
      "end": 465,
      "label": "TECHNIQUE",
      "text": "1110: Brute Force"
    }
  ],
  "metadata": {
    "source": "neo4j_capec_attack",
    "capec_id": "CAPEC-112",
    "attack_id": "1110",
    "has_owasp": true
  }
}
```

### Processing Pipeline

1. **Extraction**: Neo4j cypher-shell queries
2. **Parsing**: Python script processes raw output
3. **Entity Detection**: Regex-based entity location
4. **JSON Generation**: Structured NER training format
5. **Validation**: Deduplication and quality checks

### Quality Metrics

- ✅ All 238 records have ATTACK_PATTERN entities
- ✅ All 238 records have TECHNIQUE entities
- ✅ 15 records have VULNERABILITY_CLASS entities (OWASP context)
- ✅ No duplicate CAPEC-ATT&CK pairs
- ✅ All entities have valid character offsets

### Next Steps

This dataset is ready for:
1. NER model training
2. Integration with other OXOT datasets (v1-v6)
3. Cross-validation with STIX/TAXII feeds
4. Relationship extraction model training

### Files Generated

- `/data/ner_training/capec_attack_raw.txt` - Raw Neo4j output (primary)
- `/data/ner_training/capec_attack_owasp_raw.txt` - Raw Neo4j output (OWASP)
- `/data/ner_training/v7_capec_attack_owasp.json` - Final NER training data
- `/scripts/process_capec_attack.py` - Processing script

### Memory Hook

**Key**: `swarm/capec_attack/extracted`
**Value**: Dataset location and statistics for downstream tasks
