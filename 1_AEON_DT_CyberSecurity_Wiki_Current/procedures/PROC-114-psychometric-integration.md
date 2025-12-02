# PROCEDURE: [PROC-114] Psychometric Integration for Threat Actor Profiling

**Procedure ID**: PROC-114
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL |
| **Frequency** | QUARTERLY |
| **Priority** | MEDIUM |
| **Estimated Duration** | 3-5 hours |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Ingest 53 personality framework files (Big Five, MBTI, Dark Triad, DISC, Enneagram) to create PersonalityProfile and PersonalityTrait nodes, establish EXHIBITS_TRAIT relationships to ThreatActor nodes, and enable psychometric-based threat actor behavioral prediction and insider threat detection.

### 2.2 Business Objectives
- [x] Ingest 53 personality framework training files
- [x] Create PersonalityProfile nodes (200-300 expected)
- [x] Link personality traits to ThreatActor behavioral patterns
- [x] Enable social engineering vulnerability assessment
- [x] Support insider threat psychological profiling

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q4: Who are the attackers? | Psychological profiling of threat actors |
| Q5: How do we defend? | Identify social engineering vulnerabilities |
| Q6: What happened before? | Behavioral pattern analysis from past incidents |
| Q8: What should we do? | Targeted security awareness training |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps | grep neo4j` |
| Training Data | Files accessible | `ls -l /path/to/psychometric/*.md | wc -l` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| ThreatActor nodes exist | `MATCH (ta:ThreatActor) RETURN count(ta)` | >= 50 |
| Campaign nodes exist | `MATCH (c:Campaign) RETURN count(c)` | >= 100 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name |
|--------------|---------------|
| PROC-001 | Schema Migration |
| PROC-111 | APT Threat Intelligence Ingestion |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format |
|-------------|------|----------|--------|
| Psychometric Training Files | File Collection | `/home/jim/2_OXOT_Projects_Dev/psychometric_frameworks/` | Markdown with annotations |

### 4.2 Personality Framework Files (53 total)

**Big Five (OCEAN) - 5 files**:
- Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism

**MBTI - 16 files**:
- INTJ, ENTJ, INTP, ENTP, INFJ, ENFJ, INFP, ENFP, ISTJ, ESTJ, ISFJ, ESFJ, ISTP, ESTP, ISFP, ESFP

**Dark Triad - 3 files**:
- Narcissism, Machiavellianism, Psychopathy

**DISC - 4 files**:
- Dominance, Influence, Steadiness, Conscientiousness

**Enneagram - 9 files**:
- Type 1 through Type 9

**Other Frameworks - 16 files**:
- CliftonStrengths, Hogan Assessment, Peterson Big Five, etc.

### 4.3 Training Data Schema
```markdown
# MBTI: INTJ (Architect)

**Personality Type**: INTJ
**Full Name**: Introverted, Intuitive, Thinking, Judging
**Nickname**: The Architect, The Mastermind

## Core Traits
- <TRAIT>Strategic thinking</TRAIT>
- <TRAIT>Long-term planning</TRAIT>
- <TRAIT>Independent decision-making</TRAIT>

## Threat Actor Correlations
- <THREAT_PATTERN>Advanced persistent threats (APT)</THREAT_PATTERN>
- <MOTIVATION>Intellectual challenge, ideological conviction</MOTIVATION>
- <ATTACK_STYLE>Methodical, patient, sophisticated</ATTACK_STYLE>
```

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Container** | openspg-neo4j |
| **Port** | 7687 (Bolt) |
| **Volume** | active_neo4j_data |

### 5.2 Target Schema

**Node Types**:
| Label | Properties | Constraints |
|-------|-----------|-------------|
| PersonalityFramework | name, description, category | UNIQUE on name |
| PersonalityProfile | profile_id, framework, type_name | UNIQUE on (framework, type_name) |
| PersonalityTrait | name, description, category | UNIQUE on name |
| SocialEngineeringVulnerability | vulnerability_type, description | UNIQUE on vulnerability_type |

**Relationships**:
| Type | Source | Target |
|------|--------|--------|
| PART_OF | (:PersonalityProfile) | (:PersonalityFramework) |
| EXHIBITS_TRAIT | (:PersonalityProfile) | (:PersonalityTrait) |
| EXHIBITS_PROFILE | (:ThreatActor) | (:PersonalityProfile) |
| VULNERABLE_TO | (:PersonalityProfile) | (:SocialEngineeringVulnerability) |
| EXPLOITS_VULNERABILITY | (:ThreatActor) | (:SocialEngineeringVulnerability) |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules

| Source Field | Target Property | Transformation |
|--------------|-----------------|----------------|
| `<TRAIT>` | PersonalityTrait.name | Direct extract |
| `<THREAT_PATTERN>` | Behavioral pattern | Link to ThreatActor |
| `<MOTIVATION>` | ThreatActor.motivation | Append to existing |
| Framework file name | PersonalityProfile.framework | Extract framework type |

### 6.2 Framework Type Detection

| File Pattern | Framework |
|-------------|----------|
| `*MBTI*.md` | MBTI |
| `*Big_Five*.md` | Big Five (OCEAN) |
| `*Dark_Triad*.md` | Dark Triad |
| `*DISC*.md` | DISC |
| `*Enneagram*.md` | Enneagram |

### 6.3 Validation Rules

| Rule | Field | Validation | Action |
|------|-------|------------|--------|
| VAL-001 | Framework | Known framework | WARN if unknown |
| VAL-002 | TRAIT | Min 3 chars | SKIP |
| VAL-003 | Profile | Unique combo | MERGE on conflict |

---

## 7. EXECUTION STEPS

### Step 1: Verify Training Data
```bash
# Placeholder path - adjust to actual location
PSYCH_DATA_PATH="/home/jim/2_OXOT_Projects_Dev/psychometric_frameworks"
ls -1 "$PSYCH_DATA_PATH"/*.md | wc -l  # Should be 53
```

### Step 2: Create Schema Constraints
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
CREATE CONSTRAINT personality_framework_name_unique IF NOT EXISTS FOR (pf:PersonalityFramework) REQUIRE pf.name IS UNIQUE;
CREATE CONSTRAINT personality_profile_unique IF NOT EXISTS FOR (pp:PersonalityProfile) REQUIRE (pp.framework, pp.type_name) IS UNIQUE;
CREATE CONSTRAINT personality_trait_name_unique IF NOT EXISTS FOR (pt:PersonalityTrait) REQUIRE pt.name IS UNIQUE;
CREATE CONSTRAINT social_eng_vuln_type_unique IF NOT EXISTS FOR (sev:SocialEngineeringVulnerability) REQUIRE sev.vulnerability_type IS UNIQUE;
EOF
```

### Step 3: Run Psychometric Ingestion Script
```bash
python3 << 'SCRIPT'
import re
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))
data_path = "/home/jim/2_OXOT_Projects_Dev/psychometric_frameworks"

def extract_tags(content, tag_name):
    pattern = f"<{tag_name}>(.*?)</{tag_name}>"
    return re.findall(pattern, content, re.IGNORECASE)

def detect_framework(filename):
    """Detect personality framework from filename"""
    filename_lower = filename.lower()
    if 'mbti' in filename_lower or 'myers' in filename_lower:
        return 'MBTI'
    elif 'big_five' in filename_lower or 'ocean' in filename_lower:
        return 'Big Five'
    elif 'dark_triad' in filename_lower or 'narcissism' in filename_lower or 'machiavellianism' in filename_lower or 'psychopathy' in filename_lower:
        return 'Dark Triad'
    elif 'disc' in filename_lower:
        return 'DISC'
    elif 'enneagram' in filename_lower:
        return 'Enneagram'
    else:
        return 'Other'

def ingest_psychometric_file(session, filepath):
    """Ingest single personality framework file"""
    filename = os.path.basename(filepath)
    framework = detect_framework(filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract personality type name from header
    match = re.search(r'#\s+([^:\n]+):', content)
    type_name = match.group(1).strip() if match else os.path.splitext(filename)[0]

    # Extract traits
    traits = extract_tags(content, 'TRAIT')
    threat_patterns = extract_tags(content, 'THREAT_PATTERN')
    motivations = extract_tags(content, 'MOTIVATION')
    vulnerabilities = extract_tags(content, 'VULNERABILITY')

    # Create PersonalityFramework
    session.run("""
        MERGE (pf:PersonalityFramework {name: $framework})
        ON CREATE SET pf.created_at = datetime()
    """, framework=framework)

    # Create PersonalityProfile
    session.run("""
        MERGE (pp:PersonalityProfile {framework: $framework, type_name: $type_name})
        ON CREATE SET pp.profile_id = randomUUID(),
                      pp.source_file = $filename,
                      pp.created_at = datetime()
        WITH pp
        MATCH (pf:PersonalityFramework {name: $framework})
        MERGE (pp)-[:PART_OF]->(pf)
    """, framework=framework, type_name=type_name, filename=filename)

    # Create PersonalityTraits and link
    for trait in set(traits):
        session.run("""
            MERGE (pt:PersonalityTrait {name: $trait})
            ON CREATE SET pt.framework = $framework,
                          pt.created_at = datetime()
            WITH pt
            MATCH (pp:PersonalityProfile {framework: $framework, type_name: $type_name})
            MERGE (pp)-[:EXHIBITS_TRAIT]->(pt)
        """, trait=trait, framework=framework, type_name=type_name)

    # Create SocialEngineeringVulnerabilities
    for vuln in set(vulnerabilities):
        session.run("""
            MERGE (sev:SocialEngineeringVulnerability {vulnerability_type: $vuln})
            ON CREATE SET sev.created_at = datetime()
            WITH sev
            MATCH (pp:PersonalityProfile {framework: $framework, type_name: $type_name})
            MERGE (pp)-[:VULNERABLE_TO]->(sev)
        """, vuln=vuln, framework=framework, type_name=type_name)

    # Link threat patterns to existing ThreatActors (best effort)
    for pattern in threat_patterns:
        # Example: "APT" pattern links to threat actors with "APT" in name
        session.run("""
            MATCH (pp:PersonalityProfile {framework: $framework, type_name: $type_name})
            MATCH (ta:ThreatActor)
            WHERE ta.name =~ $pattern_regex
            MERGE (ta)-[:EXHIBITS_PROFILE {confidence: 0.6}]->(pp)
        """, framework=framework, type_name=type_name, pattern_regex=f".*{re.escape(pattern)}.*")

# Process all psychometric files
try:
    md_files = [f for f in os.listdir(data_path) if f.endswith('.md')]

    with driver.session() as session:
        for idx, filename in enumerate(md_files, 1):
            print(f"Processing {idx}/{len(md_files)}: {filename}")
            filepath = os.path.join(data_path, filename)
            ingest_psychometric_file(session, filepath)

    print(f"Psychometric integration complete: {len(md_files)} files processed")

except FileNotFoundError:
    print(f"Psychometric data directory not found: {data_path}")
    print("Note: Adjust data_path to actual location of psychometric training files")

driver.close()
SCRIPT
```

### Step 4: Verify Results
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
MATCH (pf:PersonalityFramework) RETURN pf.name, count{(pp:PersonalityProfile)-[:PART_OF]->(pf)} AS profiles;
MATCH (pp:PersonalityProfile) RETURN count(pp) AS total_profiles;
MATCH (pt:PersonalityTrait) RETURN count(pt) AS total_traits;
MATCH (ta:ThreatActor)-[r:EXHIBITS_PROFILE]->(pp:PersonalityProfile) RETURN count(r) AS actor_profiles;
EOF
```

---

## 8. POST-EXECUTION VERIFICATION

### Verify Framework Coverage
```cypher
MATCH (pf:PersonalityFramework)
RETURN pf.name AS framework,
       count{(pp:PersonalityProfile)-[:PART_OF]->(pf)} AS profile_count
ORDER BY profile_count DESC;
```

**Expected Results**:
- MBTI: 16
- Enneagram: 9
- Big Five: 5
- DISC: 4
- Dark Triad: 3

### Verify Threat Actor Profiling
```cypher
MATCH (ta:ThreatActor)-[r:EXHIBITS_PROFILE]->(pp:PersonalityProfile)
RETURN ta.name, pp.framework, pp.type_name, r.confidence
ORDER BY ta.name
LIMIT 20;
```

### Test Social Engineering Vulnerability Analysis
```cypher
MATCH path = (pp:PersonalityProfile)-[:VULNERABLE_TO]->(sev:SocialEngineeringVulnerability)
             <-[:EXPLOITS_VULNERABILITY]-(ta:ThreatActor)
RETURN pp.type_name, sev.vulnerability_type, ta.name
LIMIT 10;
```

### Success Criteria

| Criterion | Threshold | Actual |
|-----------|-----------|--------|
| PersonalityFrameworks | >= 5 | ___ |
| PersonalityProfiles | >= 40 | ___ |
| PersonalityTraits | >= 100 | ___ |
| EXHIBITS_PROFILE links | >= 20 | ___ |

---

## 9. ROLLBACK PROCEDURE

### Remove All Psychometric Data
```cypher
MATCH (pf:PersonalityFramework)
DETACH DELETE pf;

MATCH (pp:PersonalityProfile)
DETACH DELETE pp;

MATCH (pt:PersonalityTrait)
DETACH DELETE pt;

MATCH (sev:SocialEngineeringVulnerability)
DETACH DELETE sev;
```

### Verify Rollback
```cypher
MATCH (n)
WHERE n:PersonalityFramework OR n:PersonalityProfile OR n:PersonalityTrait
RETURN count(n);
// Expected: 0
```

---

## 10. SCHEDULING & AUTOMATION

### Cron Schedule
```cron
# Quarterly on 1st of Jan/Apr/Jul/Oct at 6 AM
0 6 1 1,4,7,10 * /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_114_psychometric_integration.sh >> /var/log/aeon/proc_114.log 2>&1
```

---

## 11. MONITORING & ALERTING

### Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Execution duration | Log | > 6 hours | ERROR |
| PersonalityProfiles | Neo4j | < 35 | WARN |
| Framework coverage | Neo4j | < 5 frameworks | ERROR |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL System | Initial procedure for E04 Psychometric Integration |

---

## 13. APPENDICES

### Appendix A: Academic References

**Big Five (OCEAN)**:
- McCrae, R. R., & Costa, P. T. (2008). The five-factor theory of personality. *Handbook of Personality*.

**MBTI**:
- Myers, I. B., et al. (1998). *MBTI manual: A guide to the development and use of the Myers-Briggs Type Indicator*.

**Dark Triad**:
- Paulhus, D. L., & Williams, K. M. (2002). The dark triad of personality. *Journal of Research in Personality*.

### Appendix B: Related Documentation
- Enhancement 04 README: `/enhancements/Enhancement_04_Psychometric_Integration/README.md`
- DATA_SOURCES.md: `/enhancements/Enhancement_04_Psychometric_Integration/DATA_SOURCES.md`

---

**End of Procedure PROC-114**
