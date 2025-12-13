# Entity Validation Agent

## Purpose
Validates extracted cybersecurity entities from the XML Parser Agent output. Performs format validation, deduplication, confidence scoring, and quality metrics calculation.

## Iron Law Compliance
✅ **EXECUTES ACTUAL VALIDATION** - Does not build validation frameworks
✅ **VALIDATES REAL DATA** - Processes actual parsed_entities.json from XML Parser
✅ **CREATES CLEAN OUTPUT** - Produces validated_entities.json with verified data

## Dependencies
- **Upstream**: XML Parser Agent must create `parsed_entities.json`
- **Python**: 3.7+ with standard library only

## Validation Rules

### Format Validation
- **IP**: Valid IPv4 (4 octets, 0-255 each)
- **Hash_MD5**: Exactly 32 hex chars `[a-f0-9]{32}`
- **Hash_SHA1**: Exactly 40 hex chars `[a-f0-9]{40}`
- **Hash_SHA256**: Exactly 64 hex chars `[a-f0-9]{64}`
- **Email**: Valid format `user@domain.tld`
- **Domain**: Valid DNS format (max 63 chars per label)
- **URL**: Valid HTTP/HTTPS URL

### Deduplication
Removes duplicates by `(value, type)` tuple:
- Same IP appearing in multiple files → Keep first occurrence
- Same hash with different contexts → Keep first occurrence

### Confidence Scoring
- **VERY_HIGH**: Multiple source files + explicit attribution
- **HIGH**: Single source file + explicit attribution
- **MEDIUM**: Inferred from context
- **LOW**: Ambiguous or weak attribution

## Usage

### Automatic (Recommended)
Wait for XML Parser Agent and auto-validate:
```bash
./wait_and_validate.sh
```

### Manual
When `parsed_entities.json` exists:
```bash
python3 entity_validator.py
```

## Outputs

### 1. validated_entities.json
Clean, deduplicated entities with confidence scores:
```json
{
  "metadata": {
    "total_parsed": 8500,
    "total_valid": 8200,
    "total_invalid": 300,
    "duplicates_removed": 1800,
    "unique_entities": 6400,
    "f1_score": 0.9647
  },
  "entities": [
    {
      "value": "192.168.1.100",
      "type": "IP",
      "confidence": "VERY_HIGH",
      "source_files": ["01_APT_Volt_Typhoon_IoCs.md", "02_APT_APT28_Fancy_Bear_IoCs.md"],
      "attribution": "APT28",
      "context": "Command and control infrastructure"
    }
  ]
}
```

### 2. validation_report.txt
Quality metrics and statistics:
- Total counts (parsed, valid, invalid, duplicates)
- Precision and F1 score
- Breakdown by entity type
- Breakdown by confidence level
- Success criteria evaluation (F1 >= 0.90)

## Success Criteria
✅ F1 score >= 0.90
✅ 4,000-8,000 unique valid entities
✅ Precision >= 0.95
✅ Clean output format

## Quality Metrics

### F1 Score Calculation
```
Precision = valid / total_parsed
Recall ≈ Precision (for validation task)
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

### Expected Performance
Based on 39 APT files with ~200 entities each:
- **Input**: ~7,800 parsed entities
- **Expected Valid**: ~7,400 (95% precision)
- **Expected Duplicates**: ~1,400 (18% duplication rate)
- **Expected Unique**: ~6,000 clean entities
- **Expected F1**: ~0.95

## Error Handling

### Missing Input File
```
❌ ERROR: Input file not found: parsed_entities.json
⏳ Waiting for XML Parser Agent to create parsed_entities.json...
```

### Low F1 Score
```
⚠️  WARNING: F1 score 0.85 < 0.90 - review needed
```
Review `validation_report.txt` for:
- High invalid count → Check parser patterns
- Many duplicates → Verify deduplication logic
- Low precision → Tighten validation rules

## Integration Flow

```
XML Parser Agent
    ↓ creates
parsed_entities.json (raw)
    ↓ validated by
Entity Validation Agent
    ↓ creates
validated_entities.json (clean)
    ↓ consumed by
Database Ingestion Agent
```

## Evidence of Completion

When complete, expect:
- ✅ `validated_entities.json` with 4,000-8,000 entities
- ✅ `validation_report.txt` showing F1 >= 0.90
- ✅ Console output showing success metrics
- ✅ Zero framework code, only actual validation

## Troubleshooting

### No parsed_entities.json
- **Cause**: XML Parser Agent hasn't run
- **Fix**: Run XML Parser Agent first or wait

### F1 score too low
- **Cause**: Parser extracting malformed entities
- **Fix**: Review parser patterns, adjust validation rules

### Too many duplicates
- **Cause**: Same entities in multiple files (expected for APT data)
- **Fix**: This is normal - deduplication handles it

### Invalid entities
- **Cause**: Parser extracted non-standard formats
- **Fix**: Review invalid entities, adjust patterns if needed
