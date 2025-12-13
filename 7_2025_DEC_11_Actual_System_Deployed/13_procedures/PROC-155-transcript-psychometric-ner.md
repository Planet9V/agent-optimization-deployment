# PROCEDURE: PROC-155 - Transcript Psychometric NER Extraction

**Procedure ID**: PROC-155
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON Development Team
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL |
| **Frequency** | DAILY |
| **Priority** | HIGH |
| **Estimated Duration** | 2-4 hours |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Extract psychometric entities (personality traits, stress indicators, cognitive styles, group roles) from meeting transcripts, email communications, and chat logs using NER11 model to populate psychometric tracking in Neo4j.

### 2.2 Business Objectives
- [ ] Enable automated personality trait extraction from organizational communications
- [ ] Build training corpus for psychometric prediction models (E22-E26)
- [ ] Support real-time organizational stress monitoring
- [ ] Feed dyad/triad/organizational analysis enhancements (E17-E20)

### 2.3 McKenney Questions Addressed

| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | N/A - Internal organizational psychometrics |
| Q4: Who are the attackers? | N/A - Defender personality profiling |
| Q5: How do we defend? | Organizational health monitoring improves defense posture |
| Q6: What happened before? | Historical psychometric trends |
| Q7: What will happen next? | Early warning stress indicators predict crises |
| Q8: What should we do? | Evidence-based intervention planning |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps | grep neo4j` |
| Python 3.9+ | Installed with spaCy, transformers | `python --version && pip show spacy` |
| NER11 Model | Trained and available | Check `/models/ner11_psychometric.pkl` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| PersonNode exists | `MATCH (p:Person) RETURN count(p) LIMIT 1` | > 0 |
| Prior procedures complete | PROC-150, PROC-151, PROC-152, PROC-153 | All completed |

### 3.3 Dependencies

| Dependency | Version Required | Verification |
|------------|-----------------|--------------|
| Python | 3.9+ | `python --version` |
| spacy | 3.7+ | `pip show spacy` |
| transformers | 4.30+ | `pip show transformers` |
| neo4j (Python) | 5.x | `pip show neo4j` |

### 3.4 Prior Procedures Required

| Procedure ID | Procedure Name | Must Complete Before |
|--------------|---------------|---------------------|
| PROC-150 | Dyad Analysis | This procedure |
| PROC-151 | Triad Group Dynamics | This procedure |
| PROC-152 | Organizational Blind Spots | This procedure |
| PROC-153 | Personality Team Fit | This procedure |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format | Update Frequency |
|-------------|------|----------|--------|------------------|
| Meeting Transcripts | File | `/data/transcripts/meetings/` | VTT, TXT | Daily |
| Email Archives | Email Server | IMAP/Exchange | EML, MSG | Daily |
| Chat Logs | API | Slack/Teams API | JSON | Hourly |
| Synthetic Data | Generated | `/data/synthetic/` | JSON | On-demand |

### 4.2 Source Details

#### Source 1: Meeting Transcripts

**Connection Information**:
```
Type: File
Path: /data/transcripts/meetings/
Authentication: File system access
File Types: .vtt, .txt, .srt
```

**Expected Volume**: 50-100 transcripts/month, ~5-10 hours of audio transcribed

**Privacy Requirements**:
- Anonymize speaker IDs (SPEAKER_001, SPEAKER_002)
- Redact sensitive technical details
- Encrypt at rest

#### Source 2: Email Communications

**Connection Information**:
```
Type: Email Server (IMAP/Exchange)
Authentication: Service account credentials
Filter: security-team@, incident-response@ mailboxes
Date Range: Last 30 days
```

**Privacy Requirements**:
- Remove email signatures
- Strip forwarded/replied text
- Aggregate analysis only (no individual profiling)

#### Source 3: Slack/Teams Chat Logs

**Connection Information**:
```
Type: API
Slack API: https://slack.com/api/conversations.history
Teams API: https://graph.microsoft.com/v1.0/teams/{id}/channels
Authentication: OAuth2 bearer token
Channels: #incident-response, #soc-alerts, #threat-intel
```

**Rate Limits**: 50 requests/minute (Slack), 100 requests/minute (Teams)

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Container** | openspg-neo4j |
| **Host** | localhost |
| **Port** | 7687 |
| **Database** | neo4j |
| **Schema** | Psychometric Enhancement Schema |

### 5.2 Target Schema

#### Node Types Created/Modified

| Label | Properties | Constraints | Indexes |
|-------|-----------|-------------|---------|
| PsychometricExtraction | text, source, timestamp, speaker_id | UNIQUE on (source, timestamp) | INDEX on timestamp |
| PersonalityTrait | trait_name, score, confidence, extraction_id | - | INDEX on trait_name |
| StressIndicator | indicator_type, intensity, timestamp, context | - | INDEX on timestamp |
| CognitiveStyle | style_type, evidence, confidence | - | INDEX on style_type |
| GroupRole | role_type, person_id, group_context, temporal_stability | - | INDEX on person_id |

#### Relationship Types Created/Modified

| Type | Source | Target | Properties |
|------|--------|--------|-----------|
| HAS_TRAIT | (:Person) | (:PersonalityTrait) | extracted_from, confidence |
| EXHIBITS_STRESS | (:Person) | (:StressIndicator) | timestamp, context |
| USES_COGNITIVE_STYLE | (:Person) | (:CognitiveStyle) | frequency, contexts |
| PLAYS_ROLE | (:Person) | (:GroupRole) | in_group, duration |
| EXTRACTED_FROM | (:PersonalityTrait) | (:PsychometricExtraction) | method, confidence |

---

## 6. TRANSFORMATION LOGIC

### 6.1 NER11 Entity Extraction Pipeline

**Step 1: Text Preprocessing**
```python
def preprocess_transcript(raw_text):
    # Remove timestamps, speaker labels
    # Normalize whitespace
    # Split into speaker turns
    return processed_text
```

**Step 2: Entity Recognition**
```python
# NER11 Entity Types
entity_types = {
    'OCEAN_TRAIT': ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'],
    'STRESS_INDICATOR': ['overwhelmed', 'frustrated', 'anxious', 'burned out'],
    'COGNITIVE_STYLE': ['analytical', 'intuitive', 'procedural', 'creative'],
    'GROUP_ROLE': ['leader', 'follower', 'specialist', 'dissenter', 'mediator']
}

def extract_entities(text, ner11_model):
    entities = ner11_model(text)
    return entities
```

**Step 3: Confidence Scoring**
```python
def calculate_confidence(entity, context):
    # Linguistic markers strength
    # Contextual consistency
    # Frequency of occurrence
    confidence = (marker_strength * 0.4 +
                  context_consistency * 0.3 +
                  frequency_score * 0.3)
    return min(confidence, 1.0)
```

### 6.2 Data Validation Rules

| Rule ID | Field | Validation | Action on Failure |
|---------|-------|------------|------------------|
| VAL-001 | speaker_id | NOT NULL | REJECT record |
| VAL-002 | trait_score | Range [0.0-1.0] | CLAMP to range |
| VAL-003 | confidence | >= 0.50 | WARN, include with flag |
| VAL-004 | timestamp | Valid datetime | REJECT record |

---

## 7. EXECUTION STEPS

### 7.1 Complete Execution Script

```python
#!/usr/bin/env python3
"""
PROCEDURE: PROC-155 - Transcript Psychometric NER
Version: 1.0.0
"""

import os
import spacy
from neo4j import GraphDatabase
from datetime import datetime
import logging

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

TRANSCRIPT_DIR = "/data/transcripts/meetings/"
LOG_FILE = f"/var/log/aeon/proc_155_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s')

# Load NER11 model
nlp = spacy.load("/models/ner11_psychometric")

class PsychometricExtractor:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def extract_from_transcript(self, transcript_path):
        """Extract psychometric entities from transcript"""
        logging.info(f"Processing: {transcript_path}")

        with open(transcript_path, 'r') as f:
            text = f.read()

        # Preprocess
        processed_text = self.preprocess(text)

        # Extract entities
        doc = nlp(processed_text)

        # Store in Neo4j
        with self.driver.session() as session:
            for ent in doc.ents:
                if ent.label_ in ['OCEAN_TRAIT', 'STRESS_INDICATOR', 'COGNITIVE_STYLE', 'GROUP_ROLE']:
                    session.write_transaction(self._create_entity, ent, transcript_path)

        logging.info(f"Completed: {transcript_path} - {len(doc.ents)} entities")

    def preprocess(self, text):
        """Clean and normalize transcript text"""
        # Remove timestamps
        import re
        text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text

    @staticmethod
    def _create_entity(tx, entity, source):
        """Create psychometric entity in Neo4j"""
        query = """
        MERGE (pe:PsychometricExtraction {
            source: $source,
            timestamp: datetime()
        })
        CREATE (trait:PersonalityTrait {
            trait_name: $trait,
            score: $score,
            confidence: $confidence,
            extraction_id: randomUUID()
        })
        CREATE (trait)-[:EXTRACTED_FROM]->(pe)
        """

        # Calculate score from entity attributes
        score = entity._.trait_score if hasattr(entity._, 'trait_score') else 0.5
        confidence = entity._.confidence if hasattr(entity._, 'confidence') else 0.65

        tx.run(query, source=source, trait=entity.text, score=score, confidence=confidence)

def main():
    logging.info("Starting PROC-155: Transcript Psychometric NER")

    extractor = PsychometricExtractor(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    try:
        # Process all transcripts in directory
        for filename in os.listdir(TRANSCRIPT_DIR):
            if filename.endswith(('.vtt', '.txt', '.srt')):
                transcript_path = os.path.join(TRANSCRIPT_DIR, filename)
                extractor.extract_from_transcript(transcript_path)

        logging.info("PROC-155 completed successfully")

    except Exception as e:
        logging.error(f"PROC-155 failed: {str(e)}")
        raise
    finally:
        extractor.close()

if __name__ == "__main__":
    main()
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Entity Extraction

```cypher
// Count extracted personality traits
MATCH (pt:PersonalityTrait)
WHERE pt.extraction_id IS NOT NULL
RETURN count(pt) AS total_traits;
```

**Expected Result**: > 100 (depending on transcript volume)

#### Verify Confidence Scores

```cypher
// Check confidence distribution
MATCH (pt:PersonalityTrait)
RETURN
    pt.trait_name,
    avg(pt.confidence) AS avg_confidence,
    min(pt.confidence) AS min_confidence,
    max(pt.confidence) AS max_confidence
ORDER BY avg_confidence DESC;
```

**Expected Result**: avg_confidence > 0.60

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Transcripts processed | Count | >= 50 | [To fill] |
| Entities extracted | Count | >= 500 | [To fill] |
| Avg confidence | Score | >= 0.60 | [To fill] |
| Error rate | % | < 5% | [To fill] |

---

## 9. ROLLBACK PROCEDURE

### 9.1 Rollback Steps

#### Step 1: Identify Affected Data

```cypher
// Find entities created by this run
MATCH (pe:PsychometricExtraction)
WHERE pe.timestamp > datetime('2025-11-26T00:00:00')
MATCH (trait)-[:EXTRACTED_FROM]->(pe)
RETURN count(trait) AS entities_to_delete;
```

#### Step 2: Remove Extracted Data

```cypher
// Delete extraction run
MATCH (pe:PsychometricExtraction)
WHERE pe.timestamp > datetime('2025-11-26T00:00:00')
MATCH (trait)-[:EXTRACTED_FROM]->(pe)
DETACH DELETE trait, pe;
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Run daily at 1 AM
0 1 * * * /usr/bin/python3 /scripts/proc_155_ner_extraction.py >> /var/log/aeon/proc_155_cron.log 2>&1
```

---

## 11. MONITORING & ALERTING

### 11.1 Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Extraction duration | Log | > 240 min | WARN |
| Entities extracted | Log | < 100 | ERROR |
| Avg confidence | Neo4j | < 0.50 | WARN |
| Failed transcripts | Log | > 5% | ERROR |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON Dev Team | Initial version |

---

**End of Procedure PROC-155**
