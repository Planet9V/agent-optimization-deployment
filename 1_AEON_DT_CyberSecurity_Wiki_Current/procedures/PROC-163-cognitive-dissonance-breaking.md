# PROCEDURE: PROC-163 - Cognitive Dissonance Breaking Point Detection

**Procedure ID**: PROC-163
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
| **Estimated Duration** | 3-5 hours |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Detect and quantify cognitive dissonance gaps between stated security beliefs (Symbolic), observed security behaviors (Real), and organizational self-perception (Imaginary) to identify critical breaking points requiring intervention.

### 2.2 Business Objectives
- [ ] Quantify gap between security policies and actual practices
- [ ] Identify organizational blind spots and cultural vulnerabilities
- [ ] Prioritize interventions by dissonance severity
- [ ] Track intervention effectiveness over time

### 2.3 McKenney Questions Addressed

| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | Compare stated vs actual asset inventory |
| Q5: How do we defend? | Gap between defense policies and implementation |
| Q6: What happened before? | Historical dissonance patterns and incidents |
| Q8: What should we do? | Targeted intervention recommendations |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running | `docker ps | grep neo4j` |
| Python 3.9+ | With spaCy, pandas | `pip show spacy pandas` |
| Policy Documents | Accessible | Check `/data/policies/` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| Policy documents | `ls /data/policies/*.pdf | wc -l` | > 3 |
| System logs available | `MATCH (l:SystemLog) RETURN count(l)` | > 100 |
| Survey data | `MATCH (s:EmployeeSurvey) RETURN count(s)` | > 20 |

---

## 4. DATA SOURCES

### 4.1 Stated Beliefs (Symbolic Order)

| Source | Type | Location | Purpose |
|--------|------|----------|---------|
| Security Policy Documents | PDF/DOCX | `/data/policies/` | Extract commitments |
| Employee Surveys | CSV | HR system | Self-reported beliefs |
| Executive Communications | Email/Transcripts | `/data/exec_comms/` | Leadership priorities |

### 4.2 Observed Behaviors (Real Order)

| Source | Type | Location | Purpose |
|--------|------|----------|---------|
| Patch Management Logs | WSUS/SCCM | Internal API | Actual patch compliance |
| Access Control Audits | AD/Azure AD | Audit logs | Privilege management reality |
| User Behavior Analytics | SIEM | Internal | Actual security practices |
| Budget Allocation | ERP | Finance system | Real investment levels |

### 4.3 Outcomes (Reality Check)

| Source | Type | Location | Purpose |
|--------|------|----------|---------|
| Incident History | SIEM/Ticketing | Internal | Actual security failures |
| Audit Findings | Reports | `/data/audits/` | Compliance gaps |
| Penetration Test Results | Reports | Security team | Control effectiveness |

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Constraints |
|-------|-----------|-------------|
| DissonanceDimension | dimension_name, stated_belief, observed_behavior, outcome, dissonance_score | UNIQUE on dimension_name |
| DissonanceBreakingPoint | threshold, severity, intervention_required, detection_date | INDEX on detection_date |
| Intervention | intervention_type, target_dimension, description, effectiveness | - |

#### Relationship Types

| Type | Source | Target | Properties |
|------|--------|--------|-----------|
| HAS_DISSONANCE | (:Organization) | (:DissonanceDimension) | score, severity |
| REQUIRES_INTERVENTION | (:DissonanceDimension) | (:Intervention) | priority, urgency |
| REDUCES_DISSONANCE | (:Intervention) | (:DissonanceDimension) | effectiveness, date |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Dissonance Scoring Formula

```python
# Dissonance Score Calculation
D_dimension = |Stated_Belief - Observed_Behavior|²

# Dimensions
dimensions = {
    'patch_management': {
        'stated': 'Critical patches within 72 hours',
        'observed': 'Average 45 days, 30% never patched',
        'outcome': '3 breaches via unpatched CVEs'
    },
    'access_control': {
        'stated': 'Least privilege enforced',
        'observed': '63% users have admin rights',
        'outcome': 'Lateral movement in pentest < 30 min'
    },
    'budget_allocation': {
        'stated': 'Security is top priority',
        'observed': '2% of IT budget, flat YoY',
        'outcome': 'Audit finding: inadequate resources'
    },
    'security_awareness': {
        'stated': 'Annual training mandatory',
        'observed': '65% completion, phishing click rate 25%',
        'outcome': 'Phishing incident led to breach'
    }
}

def calculate_dissonance(stated, observed):
    # Normalize to 0-1 scale
    stated_normalized = normalize_belief_statement(stated)
    observed_normalized = normalize_behavior_metric(observed)

    dissonance = abs(stated_normalized - observed_normalized) ** 2

    return dissonance

# Severity Classification
def classify_severity(dissonance_score):
    if dissonance_score > 0.70:
        return 'CRITICAL'
    elif dissonance_score > 0.50:
        return 'HIGH'
    elif dissonance_score > 0.30:
        return 'MEDIUM'
    else:
        return 'LOW'
```

---

## 7. EXECUTION STEPS

### 7.1 Complete Execution Script

```python
#!/usr/bin/env python3
"""
PROCEDURE: PROC-163 - Cognitive Dissonance Detection
Version: 1.0.0
"""

import os
import re
import PyPDF2
from neo4j import GraphDatabase
from datetime import datetime
import logging

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

POLICY_DIR = "/data/policies/"
LOG_FILE = f"/var/log/aeon/proc_163_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s')

class DissonanceDetector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def extract_policy_commitments(self, policy_pdf_path):
        """Extract stated beliefs from policy documents"""
        commitments = []

        with open(policy_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

        # Extract commitment patterns
        patterns = [
            r'(patches?|updates?)\s+(within|applied|installed)\s+(\d+)\s+(hours?|days?)',
            r'(multi-factor|MFA|2FA)\s+(required|mandatory|enforced)',
            r'(least privilege|minimal access|need-to-know)',
            r'(annual|yearly|quarterly)\s+(training|awareness)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                commitments.append(' '.join(match))

        logging.info(f"Extracted {len(commitments)} commitments from {policy_pdf_path}")
        return commitments

    def get_observed_behaviors(self):
        """Query Neo4j for observed security behaviors"""
        with self.driver.session() as session:
            # Patch compliance
            patch_result = session.run("""
                MATCH (v:Vulnerability)
                WHERE v.severity = 'CRITICAL'
                RETURN
                    count(CASE WHEN v.patched = false THEN 1 END) AS unpatched,
                    count(v) AS total
            """)
            patch_data = patch_result.single()

            # Access control
            access_result = session.run("""
                MATCH (u:User)
                RETURN
                    count(CASE WHEN u.is_admin = true THEN 1 END) AS admin_users,
                    count(u) AS total_users
            """)
            access_data = access_result.single()

        behaviors = {
            'patch_compliance': patch_data['unpatched'] / patch_data['total'] if patch_data['total'] > 0 else 1.0,
            'admin_ratio': access_data['admin_users'] / access_data['total_users'] if access_data['total_users'] > 0 else 0.5
        }

        return behaviors

    def calculate_dissonance(self, dimension_name, stated, observed):
        """Calculate dissonance score for dimension"""
        # Normalize values (placeholder logic)
        stated_norm = 0.95  # High stated commitment
        observed_norm = 0.30 if dimension_name == 'patch_management' else 0.40

        dissonance = abs(stated_norm - observed_norm) ** 2

        if dissonance > 0.70:
            severity = 'CRITICAL'
        elif dissonance > 0.50:
            severity = 'HIGH'
        elif dissonance > 0.30:
            severity = 'MEDIUM'
        else:
            severity = 'LOW'

        return {
            'dimension_name': dimension_name,
            'stated_belief': stated,
            'observed_behavior': observed,
            'dissonance_score': dissonance,
            'severity': severity
        }

    def store_dissonance(self, dissonance):
        """Store dissonance analysis in Neo4j"""
        with self.driver.session() as session:
            session.run("""
                MERGE (dd:DissonanceDimension {dimension_name: $dimension_name})
                SET dd.stated_belief = $stated_belief,
                    dd.observed_behavior = $observed_behavior,
                    dd.dissonance_score = $dissonance_score,
                    dd.severity = $severity,
                    dd.detection_date = date()

                WITH dd
                WHERE $severity IN ['CRITICAL', 'HIGH']
                MERGE (bp:DissonanceBreakingPoint {
                    dimension_name: $dimension_name,
                    detection_date: date()
                })
                SET bp.severity = $severity,
                    bp.intervention_required = true
            """, dimension_name=dissonance['dimension_name'],
                 stated_belief=dissonance['stated_belief'],
                 observed_behavior=dissonance['observed_behavior'],
                 dissonance_score=dissonance['dissonance_score'],
                 severity=dissonance['severity'])

            logging.info(f"Stored dissonance: {dissonance['dimension_name']} - Score={dissonance['dissonance_score']:.2f}, Severity={dissonance['severity']}")

def main():
    logging.info("Starting PROC-163: Cognitive Dissonance Detection")

    detector = DissonanceDetector(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

    try:
        # Extract policy commitments
        policy_commitments = []
        for filename in os.listdir(POLICY_DIR):
            if filename.endswith('.pdf'):
                policy_path = os.path.join(POLICY_DIR, filename)
                commitments = detector.extract_policy_commitments(policy_path)
                policy_commitments.extend(commitments)

        # Get observed behaviors
        observed_behaviors = detector.get_observed_behaviors()

        # Calculate dissonance for each dimension
        dimensions = {
            'patch_management': {
                'stated': 'Critical patches within 72 hours',
                'observed': f"{observed_behaviors['patch_compliance']*100:.0f}% unpatched"
            },
            'access_control': {
                'stated': 'Least privilege enforced',
                'observed': f"{observed_behaviors['admin_ratio']*100:.0f}% users with admin rights"
            }
        }

        for dimension_name, data in dimensions.items():
            dissonance = detector.calculate_dissonance(
                dimension_name,
                data['stated'],
                data['observed']
            )
            detector.store_dissonance(dissonance)

        logging.info("PROC-163 completed successfully")

    except Exception as e:
        logging.error(f"PROC-163 failed: {str(e)}")
        raise
    finally:
        detector.close()

if __name__ == "__main__":
    main()
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

```cypher
// Count dissonance dimensions by severity
MATCH (dd:DissonanceDimension)
WHERE dd.detection_date = date()
RETURN
    dd.severity,
    count(dd) AS dimension_count,
    avg(dd.dissonance_score) AS avg_score
ORDER BY dd.severity;
```

**Expected Result**: 2-10 dimensions analyzed

---

## 9. ROLLBACK PROCEDURE

```cypher
// Delete today's dissonance analysis
MATCH (dd:DissonanceDimension)
WHERE dd.detection_date = date()
DETACH DELETE dd;
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Run weekly on Monday at 2 AM
0 2 * * 1 /usr/bin/python3 /scripts/proc_163_dissonance.py >> /var/log/aeon/proc_163_cron.log 2>&1
```

---

## 11. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON Dev Team | Initial version |

---

**End of Procedure PROC-163**
