# CVE-CWE NER Training Data Extraction Summary

**Date**: 2025-11-08
**Dataset Version**: 7.0
**Source**: Neo4j OpenSPG Database (CVE-CWE Relationships)

## Extraction Results

### Dataset Statistics

- **Total NER Examples**: 690
- **Unique CWE Types**: 111
- **Entity Annotations**: 3,051 total
- **File Size**: 841.9 KB
- **Output Format**: JSON (spaCy-compatible)

### Entity Distribution

| Entity Type    | Count | Description                          |
|----------------|-------|--------------------------------------|
| VERSION        | 1,574 | Software versions, SP numbers, R numbers |
| WEAKNESS       | 1,016 | CWE identifiers and references       |
| SOFTWARE       |   219 | Products, systems, drivers            |
| PROTOCOL       |   213 | Network protocols (HTTP, SSL, etc.)   |
| VULNERABILITY  |    29 | CVE references within descriptions    |

### Database Query

```cypher
MATCH (cve:CVE)-[:HAS_WEAKNESS|IS_WEAKNESS_TYPE]->(cwe)
WHERE cve.description IS NOT NULL
  AND cwe.name IS NOT NULL
  AND NOT cwe.name CONTAINS 'DEPRECATED'
WITH cwe.cwe_id AS cwe_type,
     COLLECT({cve: cve, cwe: cwe})[0..30] AS pairs
UNWIND pairs AS pair
RETURN pair.cve.id + '|||||' +
       pair.cve.description + '|||||' +
       pair.cwe.cwe_id + '|||||' +
       pair.cwe.name + '|||||' +
       substring(pair.cwe.description, 0, 300) AS record
LIMIT 1000;
```

**Notes**:
- Pipe-delimited format (`|||||`) used to avoid CSV escaping issues
- Sampled 30 CVE examples per CWE type for diversity
- Limited to first 1,000 records from Neo4j (690 passed quality filters)

### Data Quality Filters

Applied during processing:
1. **Description Length**: Minimum 50 characters
2. **Entity Minimum**: At least 2 entities per example
3. **Deprecated Filtering**: Excluded deprecated CWE categories
4. **Deduplication**: Ensured unique CVE-CWE pairings

### Sample CWE Coverage

The dataset includes diverse CWE types such as:
- CWE-275: Permission Issues
- CWE-352: Cross-Site Request Forgery
- CWE-287: Authentication Bypass
- CWE-78: OS Command Injection
- CWE-190: Integer Overflow
- CWE-787: Out-of-Bounds Write
- And 105 more unique weakness types...

### Entity Recognition Patterns

**SOFTWARE Detection**:
- Microsoft Windows (all versions)
- Apache, Oracle, Cisco products
- VLC Media Player, Zope, Plone
- Industrial systems (Modicon, SoMachine)
- Kernel components (win32k.sys)

**PROTOCOL Detection**:
- HTTP, HTTPS, FTP, SSH, SSL/TLS
- TCP, UDP, IP, ICMP
- DNS, SMTP, POP3, IMAP
- Ethernet variants

**VERSION Detection**:
- Semantic versions (1.2.3.4)
- Service Packs (SP2, SP3)
- Release numbers (R2, R3)
- Firmware versions (V1.10.0.0)

### Output Format

```json
{
  "dataset_info": {
    "name": "CVE-CWE NER Training Dataset",
    "version": "7.0",
    "total_examples": 690,
    "unique_cwe_types": 111,
    "entity_types": ["VULNERABILITY", "WEAKNESS", "SOFTWARE", "PROTOCOL", "VERSION"]
  },
  "examples": [
    {
      "text": "CVE description... This vulnerability is classified as CWE-XXX (Category).",
      "entities": [
        {"start": 0, "end": 10, "label": "SOFTWARE", "text": "win32k.sys"},
        ...
      ],
      "metadata": {
        "cve_id": "CVE-2011-0676",
        "cwe_id": "CWE-2",
        "cwe_name": "7PK - Environment",
        "entity_count": 8,
        "entity_types": ["SOFTWARE", "VERSION", "WEAKNESS"]
      }
    }
  ]
}
```

### File Locations

- **Raw Data**: `data/ner_training/raw_cve_cwe_pipe.txt`
- **Processed Dataset**: `data/ner_training/v7_cve_cwe_mappings.json`
- **Processing Script**: `scripts/process_pipe_delimited.py`

### Usage

This dataset is designed for training spaCy NER models to recognize cybersecurity entities in vulnerability descriptions. The annotations follow spaCy's training format with character-level entity spans.

**Next Steps**:
1. Convert to spaCy DocBin format for training
2. Split into train/validation/test sets (70/15/15)
3. Train custom NER model with cybersecurity focus
4. Evaluate on held-out CVE descriptions

### Memory Hook Registration

Registered in Claude-Flow memory:
- **Task ID**: `cve_cwe_extraction`
- **Memory Key**: `swarm/cve_cwe/extracted`
- **Status**: Complete
- **Timestamp**: 2025-11-08T18:11:17Z

---

**Extraction Method**: Direct Neo4j query → Pipe-delimited format → Python regex entity extraction → JSON output
**Quality**: High-quality annotations with diverse CWE coverage and rich entity types
**Completeness**: 690 examples from 64,224 total CVE-CWE relationships (representative sample)
