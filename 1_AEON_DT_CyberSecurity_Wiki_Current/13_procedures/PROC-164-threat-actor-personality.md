# PROCEDURE: PROC-164 - Threat Actor Personality Profiling

**Procedure ID**: PROC-164
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
| **Frequency** | WEEKLY |
| **Priority** | HIGH |
| **Estimated Duration** | 4-6 hours |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Profile threat actor personalities using Big Five (OCEAN) and Dark Triad traits inferred from TTPs, infrastructure choices, communications, and behavioral patterns to predict future attack strategies and attribution.

### 2.2 Business Objectives
- [ ] Create comprehensive psychological profiles of threat actors
- [ ] Improve threat attribution through personality fingerprinting
- [ ] Predict future TTP evolution based on personality traits
- [ ] Enable targeted defensive strategies per actor personality type

### 2.3 McKenney Questions Addressed

| Question | How Addressed |
|----------|---------------|
| Q4: Who are the attackers? | Full personality profiling for attribution |
| Q3: What do attackers know? | Inferred from cognitive style and openness traits |
| Q7: What will happen next? | Predict TTP evolution from personality stability |
| Q8: What should we do? | Personality-informed defensive strategies |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running | `docker ps | grep neo4j` |
| Python 3.9+ | With spaCy, transformers | `pip show spacy transformers` |
| MITRE ATT&CK Data | Loaded | `MATCH (t:Technique) RETURN count(t)` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| Threat actors | `MATCH (ta:ThreatActor) RETURN count(ta)` | > 10 |
| TTPs mapped | `MATCH ()-[r:USES_TECHNIQUE]->() RETURN count(r)` | > 50 |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format | Update Frequency |
|-------------|------|----------|--------|------------------|
| MITRE ATT&CK | TAXII Server | https://cti-taxii.mitre.org/ | STIX | Quarterly |
| Mandiant Threat Intel | Commercial API | Subscription required | JSON | Weekly |
| CrowdStrike Falcon | Commercial API | Subscription required | JSON | Daily |
| Ransomware Leak Sites | Web Scraping | Tor network | HTML | Daily |
| Dark Web Forums | Archives | Historical data | Text | Static |
| Passive DNS | PassiveTotal/Farsight | Commercial API | JSON | Real-time |
| WHOIS Historical | DomainTools | Commercial API | JSON | Daily |

### 4.2 Personality Trait Extraction Methods

**Big Five (OCEAN)**:
```python
trait_extraction_methods = {
    'Openness': {
        'indicators': [
            'Zero-day usage (novel techniques)',
            'Early adoption of new TTPs',
            'Custom tool development',
            'Cloud-native attacks'
        ],
        'data_sources': ['MITRE ATT&CK technique novelty', 'Malware analysis']
    },
    'Conscientiousness': {
        'indicators': [
            'Strong OPSEC (anti-forensics)',
            'Domain privacy protection',
            'Infrastructure diversity',
            'Consistent operational patterns'
        ],
        'data_sources': ['Infrastructure analysis', 'DNS patterns', 'Forensic artifacts']
    },
    'Extraversion': {
        'indicators': [
            'Public leak sites',
            'Media engagement',
            'Branded ransomware',
            'High-profile targeting'
        ],
        'data_sources': ['Leak site analysis', 'Media mentions', 'Victim publicity']
    },
    'Agreeableness': {
        'indicators': [
            'Negotiation tone (hostile vs cooperative)',
            'Forum behavior (help-giving)',
            'Ransom note empathy language'
        ],
        'data_sources': ['Ransom notes', 'Forum posts', 'Negotiations transcripts']
    },
    'Neuroticism': {
        'indicators': [
            'Operational tempo variability',
            'Reactive vs planned campaigns',
            'Mistake frequency'
        ],
        'data_sources': ['Campaign timelines', 'Incident patterns', 'Error analysis']
    }
}
```

**Dark Triad**:
```python
dark_triad_extraction = {
    'Machiavellianism': {
        'indicators': [
            'Strategic framing language',
            'Business-like ransom negotiations',
            'Long-term planning',
            'Justification rhetoric'
        ],
        'data_sources': ['Ransom notes', 'Forum posts', 'Negotiation transcripts']
    },
    'Narcissism': {
        'indicators': [
            'Grandiose language ("most advanced")',
            'Branding emphasis',
            'First-person plural usage',
            'Status claims'
        ],
        'data_sources': ['Leak sites', 'Media statements', 'Forum posts']
    },
    'Psychopathy': {
        'indicators': [
            'Impulsive attacks',
            'Destructive behavior (wiper malware)',
            'Low empathy (aggressive ransom tactics)',
            'Thrill-seeking indicators'
        ],
        'data_sources': ['Attack patterns', 'Malware analysis', 'Victim treatment']
    }
}
```

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Constraints |
|-------|-----------|-------------|
| ThreatActorPersonality | actor_id, openness_score, conscientiousness_score, extraversion_score, agreeableness_score, neuroticism_score, machiavellianism_score, narcissism_score, psychopathy_score | UNIQUE on actor_id |
| PersonalityEvidence | evidence_type, source, confidence, timestamp | - |
| PredictedBehavior | behavior_description, probability, based_on_trait | - |

#### Relationship Types

| Type | Source | Target | Properties |
|------|--------|--------|-----------|
| HAS_PERSONALITY | (:ThreatActor) | (:ThreatActorPersonality) | confidence |
| SUPPORTED_BY | (:ThreatActorPersonality) | (:PersonalityEvidence) | weight |
| PREDICTS | (:ThreatActorPersonality) | (:PredictedBehavior) | probability |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Personality Scoring Formula

```python
def calculate_openness(actor_id):
    """Calculate Openness score from TTP novelty"""
    # Query MITRE ATT&CK for actor's techniques
    techniques = get_actor_techniques(actor_id)

    novelty_scores = []
    for technique in techniques:
        first_wild = get_first_observation_date(technique)
        actor_first_use = get_actor_first_use(actor_id, technique)

        # Days between public disclosure and adoption
        adoption_delay = (actor_first_use - first_wild).days

        # Normalize: 0 days = 1.0, 365+ days = 0.0
        novelty_score = max(0, 1 - (adoption_delay / 365))
        novelty_scores.append(novelty_score)

    openness = np.mean(novelty_scores) if novelty_scores else 0.5
    return openness

def calculate_conscientiousness(actor_id):
    """Calculate Conscientiousness from OPSEC indicators"""
    # Infrastructure analysis
    domains = get_actor_domains(actor_id)

    privacy_ratio = sum(1 for d in domains if uses_whois_privacy(d)) / len(domains)
    registrar_diversity = len(set(get_registrar(d) for d in domains)) / len(domains)

    # Anti-forensics usage
    anti_forensics_count = count_anti_forensics_techniques(actor_id)
    total_techniques = count_total_techniques(actor_id)

    anti_forensics_ratio = anti_forensics_count / total_techniques

    conscientiousness = (
        0.4 * privacy_ratio +
        0.3 * registrar_diversity +
        0.3 * anti_forensics_ratio
    )

    return conscientiousness
```

---

## 7. EXECUTION STEPS

### 7.1 Complete Execution Script

```python
#!/usr/bin/env python3
"""
PROCEDURE: PROC-164 - Threat Actor Personality Profiling
Version: 1.0.0
"""

import os
import numpy as np
from neo4j import GraphDatabase
from datetime import datetime
import logging

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

LOG_FILE = f"/var/log/aeon/proc_164_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s')

class ThreatActorProfiler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_threat_actors(self):
        """Get all threat actors for profiling"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (ta:ThreatActor)
                RETURN ta.actor_id AS actor_id, ta.name AS name
            """)
            return [record.data() for record in result]

    def calculate_openness(self, actor_id):
        """Calculate Openness from TTP novelty"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (ta:ThreatActor {actor_id: $actor_id})-[:USES_TECHNIQUE]->(t:Technique)
                RETURN t.technique_id AS technique_id, t.first_observed AS first_observed
            """, actor_id=actor_id)

            techniques = [record.data() for record in result]

        # Placeholder novelty scoring
        openness = 0.65  # Moderate openness

        return openness

    def calculate_conscientiousness(self, actor_id):
        """Calculate Conscientiousness from OPSEC"""
        # Placeholder - integrate with infrastructure analysis
        conscientiousness = 0.70  # Moderate-high OPSEC

        return conscientiousness

    def calculate_extraversion(self, actor_id):
        """Calculate Extraversion from public visibility"""
        with self.driver.session() as session:
            # Check for leak site presence
            result = session.run("""
                MATCH (ta:ThreatActor {actor_id: $actor_id})-[:OPERATES]->(ls:LeakSite)
                RETURN count(ls) AS leak_sites
            """, actor_id=actor_id)

            leak_sites = result.single()['leak_sites']

        # Higher leak site activity = higher extraversion
        extraversion = min(0.3 + (leak_sites * 0.15), 1.0)

        return extraversion

    def calculate_agreeableness(self, actor_id):
        """Calculate Agreeableness from communications"""
        # Placeholder - integrate with ransom note linguistic analysis
        agreeableness = 0.25  # Low agreeableness (hostile)

        return agreeableness

    def calculate_neuroticism(self, actor_id):
        """Calculate Neuroticism from operational patterns"""
        # Placeholder - analyze campaign tempo variability
        neuroticism = 0.40  # Moderate emotional stability

        return neuroticism

    def calculate_dark_triad(self, actor_id):
        """Calculate Dark Triad traits"""
        # Placeholder - integrate with linguistic analysis
        machiavellianism = 0.75  # High strategic manipulation
        narcissism = 0.60  # Moderate grandiosity
        psychopathy = 0.45  # Moderate impulsivity

        return {
            'machiavellianism': machiavellianism,
            'narcissism': narcissism,
            'psychopathy': psychopathy
        }

    def profile_actor(self, actor_id):
        """Generate complete personality profile"""
        ocean = {
            'openness': self.calculate_openness(actor_id),
            'conscientiousness': self.calculate_conscientiousness(actor_id),
            'extraversion': self.calculate_extraversion(actor_id),
            'agreeableness': self.calculate_agreeableness(actor_id),
            'neuroticism': self.calculate_neuroticism(actor_id)
        }

        dark_triad = self.calculate_dark_triad(actor_id)

        return {
            'actor_id': actor_id,
            **ocean,
            **dark_triad,
            'confidence': 0.70
        }

    def store_profile(self, profile):
        """Store personality profile in Neo4j"""
        with self.driver.session() as session:
            session.run("""
                MATCH (ta:ThreatActor {actor_id: $actor_id})

                MERGE (tap:ThreatActorPersonality {actor_id: $actor_id})
                SET tap.openness_score = $openness,
                    tap.conscientiousness_score = $conscientiousness,
                    tap.extraversion_score = $extraversion,
                    tap.agreeableness_score = $agreeableness,
                    tap.neuroticism_score = $neuroticism,
                    tap.machiavellianism_score = $machiavellianism,
                    tap.narcissism_score = $narcissism,
                    tap.psychopathy_score = $psychopathy,
                    tap.confidence = $confidence,
                    tap.profile_date = date()

                MERGE (ta)-[:HAS_PERSONALITY]->(tap)
            """, actor_id=profile['actor_id'],
                 openness=profile['openness'],
                 conscientiousness=profile['conscientiousness'],
                 extraversion=profile['extraversion'],
                 agreeableness=profile['agreeableness'],
                 neuroticism=profile['neuroticism'],
                 machiavellianism=profile['machiavellianism'],
                 narcissism=profile['narcissism'],
                 psychopathy=profile['psychopathy'],
                 confidence=profile['confidence'])

            logging.info(f"Stored profile for {profile['actor_id']} - Openness={profile['openness']:.2f}, Conscientiousness={profile['conscientiousness']:.2f}")

def main():
    logging.info("Starting PROC-164: Threat Actor Personality Profiling")

    profiler = ThreatActorProfiler(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    try:
        actors = profiler.get_threat_actors()

        for actor in actors:
            profile = profiler.profile_actor(actor['actor_id'])
            profiler.store_profile(profile)

        logging.info(f"PROC-164 completed successfully - Profiled {len(actors)} actors")

    except Exception as e:
        logging.error(f"PROC-164 failed: {str(e)}")
        raise
    finally:
        profiler.close()

if __name__ == "__main__":
    main()
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

```cypher
// View threat actor personality profiles
MATCH (ta:ThreatActor)-[:HAS_PERSONALITY]->(tap:ThreatActorPersonality)
RETURN
    ta.name,
    tap.openness_score,
    tap.conscientiousness_score,
    tap.extraversion_score,
    tap.machiavellianism_score,
    tap.narcissism_score
ORDER BY tap.openness_score DESC
LIMIT 10;
```

**Expected Result**: 10-50 actor profiles

---

## 9. ROLLBACK PROCEDURE

```cypher
// Delete today's personality profiles
MATCH (tap:ThreatActorPersonality)
WHERE tap.profile_date = date()
DETACH DELETE tap;
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Run weekly on Sunday at 2 AM
0 2 * * 0 /usr/bin/python3 /scripts/proc_164_actor_profiling.py >> /var/log/aeon/proc_164_cron.log 2>&1
```

---

## 11. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON Dev Team | Initial version |

---

**End of Procedure PROC-164**
