# Enhancement 21: Data Sources for Transcript Psychometric Extraction

**File:** Enhancement_21_Transcript_Psychometric_NER/DATA_SOURCES.md
**Created:** 2025-11-26
**Version:** v1.0.0
**Author:** AEON Development Team
**Purpose:** Comprehensive data source catalog for NER11 psychometric entity extraction
**Status:** ACTIVE

---

## Executive Summary

This document catalogs all potential data sources for training and deploying the NER11 psychometric extraction system. Data sources are categorized by type, accessibility, and ethical considerations.

**Target Corpus Size:** 10,000+ transcripts across diverse contexts
**Minimum Viable Corpus:** 1,000 transcripts with validated annotations

---

## 1. Meeting Transcripts

### 1.1 Security Operations Center (SOC) Meetings

**Data Type:** Incident response planning, threat briefings, post-mortem reviews
**Volume:** 50-100 meetings/month (5-10 hours of audio)
**Access:** Internal organizational data (permission required)

**Psychometric Value:**
- High-stress communication patterns during incidents
- Leadership emergence under pressure
- Group dynamics in crisis situations
- Cognitive load indicators during complex problem-solving

**Collection Method:**
```python
# Automated meeting recording pipeline
sources = {
    "zoom_recordings": "/recordings/soc_meetings/",
    "teams_recordings": "/recordings/teams_security/",
    "transcript_format": "vtt",
    "speakers_identified": True,
    "timestamp_precision": "second"
}
```

**Privacy Considerations:**
- Obtain consent from all participants
- Anonymize speaker IDs (SPEAKER_001, SPEAKER_002)
- Redact sensitive technical details (IP addresses, credentials)
- Store encrypted at rest

---

### 1.2 Leadership Strategy Meetings

**Data Type:** Quarterly planning, budget discussions, risk assessments
**Volume:** 10-20 meetings/quarter (2-5 hours of audio)
**Access:** Executive permission required

**Psychometric Value:**
- Long-term personality trait stability
- Decision-making styles under uncertainty
- Power dynamics and influence patterns
- Strategic vs. tactical thinking indicators

**Privacy Considerations:**
- Higher sensitivity due to strategic information
- Board-level approval may be required
- Anonymization critical
- Potential embargo period before analysis

---

### 1.3 Synthetic Meeting Data

**Data Type:** GPT-4 generated transcripts with specified personality profiles
**Volume:** Unlimited (generate on demand)
**Access:** Fully controlled

**Generation Prompt Template:**
```
Generate a 30-minute incident response meeting transcript with 4 speakers:
- SPEAKER_001: High conscientiousness, analytical cognitive style, leader role
- SPEAKER_002: High neuroticism, stressed, follower role
- SPEAKER_003: Low agreeableness, aggressive communication, dissenter role
- SPEAKER_004: High openness, creative cognitive style, specialist role

Context: Zero-day vulnerability discovered in production system.
Include realistic technical discussion, stress indicators, and group dynamics.
```

**Validation Challenge:**
- Synthetic data may lack authentic stress patterns
- Group dynamics may be overly stereotyped
- Use for initial training only, validate on real data

---

## 2. Email Communications

### 2.1 Security Team Email Threads

**Data Type:** Incident notifications, policy discussions, vendor communications
**Volume:** 1,000-2,000 emails/month
**Access:** Email server export (IT and legal approval)

**Psychometric Value:**
- Asynchronous communication patterns
- Formality vs. informality shifts under stress
- Persistent personality traits across contexts
- Bias markers in decision justifications

**Collection Method:**
```python
# Email corpus builder
from imaplib import IMAP4_SSL
from email.parser import BytesParser

sources = {
    "mailboxes": ["security-team@", "incident-response@"],
    "date_range": "2024-01-01 to 2025-11-26",
    "filter_keywords": ["incident", "vulnerability", "breach", "risk"],
    "exclude_automated": True  # Filter out automated notifications
}
```

**Preprocessing Requirements:**
- Remove email signatures
- Strip forwarded/replied text markers
- Preserve timestamp sequences
- Maintain thread structure

---

### 2.2 Post-Incident Review Email Chains

**Data Type:** Lessons learned discussions, blame attribution, improvement proposals
**Volume:** 50-100 email threads/year
**Access:** Incident response archive

**Psychometric Value:**
- Attribution bias markers (who gets blamed)
- Defensive vs. constructive communication
- Organizational learning culture indicators
- Stress recovery patterns

**Ethical Considerations:**
- Post-incident reviews may involve personnel criticism
- High sensitivity for individual careers
- Aggregate analysis only (no individual profiling)

---

## 3. Chat Logs (Slack, Teams, IRC)

### 3.1 Real-Time Incident Response Channels

**Data Type:** Fast-paced technical troubleshooting during active incidents
**Volume:** 5,000-10,000 messages/month (during incidents)
**Access:** Workspace admin API access

**Psychometric Value:**
- High-frequency stress indicators
- Cognitive load under time pressure
- Communication pattern shifts (normal → crisis)
- Leadership emergence in real-time

**Collection Method:**
```python
# Slack API export
from slack_sdk import WebClient

channels = [
    "incident-response",
    "soc-alerts",
    "threat-intel",
    "security-engineering"
]

for channel in channels:
    history = client.conversations_history(
        channel=channel_id,
        oldest="2024-01-01",
        limit=1000
    )
    # Process and anonymize
```

**Temporal Patterns:**
- Message frequency spikes during incidents
- Response time distributions (urgency indicators)
- After-hours activity (burnout risk)

---

### 3.2 Persistent Discussion Channels

**Data Type:** Non-urgent security discussions, tool recommendations, knowledge sharing
**Volume:** 2,000-5,000 messages/month (steady-state)
**Access:** Workspace admin API access

**Psychometric Value:**
- Baseline personality traits (non-stressed)
- Group cohesion and collaboration patterns
- Expertise domains and specialist roles
- Communication norms and culture

---

## 4. Interview Transcripts

### 4.1 Post-Incident Interviews

**Data Type:** One-on-one interviews with incident responders
**Volume:** 20-50 interviews/year (30-60 minutes each)
**Access:** HR and legal approval required

**Psychometric Value:**
- Detailed stress narratives
- Reflective cognitive styles
- Attribution patterns (self vs. others)
- Organizational culture indicators

**Interview Protocol:**
```
1. Timeline reconstruction (cognitive recall)
2. Decision-making rationale (reasoning style)
3. Emotional responses (stress indicators)
4. Lessons learned (learning orientation)
5. Organizational support (affiliation needs)
```

**Validation Use:**
- Gold standard for detailed psychometric analysis
- Correlate with validated personality assessments
- Small sample size but high quality

---

### 4.2 Security Awareness Training Interviews

**Data Type:** Employee responses to security scenarios
**Volume:** 100-500 interviews/year (10-15 minutes each)
**Access:** Training program data

**Psychometric Value:**
- Security culture indicators
- Risk perception patterns
- Compliance motivation
- Cognitive biases in threat assessment

---

## 5. Threat Actor Forum Posts

### 5.1 Public Underground Forums

**Data Type:** Discussions on breached data, exploit techniques, victim targeting
**Volume:** 10,000-50,000 posts/month (across major forums)
**Access:** Public OSINT (no ethical restrictions)

**Psychometric Value:**
- Dark Triad traits (Machiavellianism, narcissism, psychopathy)
- In-group/out-group dynamics (hacker culture)
- Motivations (financial, ideological, thrill-seeking)
- Status-seeking behavior

**Forums to Monitor:**
```
Public/Semi-Public:
- RaidForums (defunct but archived)
- BreachForums
- XSS.is
- Exploit.in
- Reddit: r/netsec, r/AskNetsec (ethical hackers)

Fully Public:
- HackerOne disclosure discussions
- Security researcher Twitter threads
- YouTube security content creator comments
```

**Collection Challenges:**
- Pseudonymous identities (can't validate with ground truth)
- Cultural language barriers (Russian, Chinese forums)
- Deception and misinformation (operational security)

**Research Value:**
- Comparative psychometrics (defenders vs. attackers)
- Early warning indicators (frustration → escalation)
- Network analysis (who influences whom)

---

### 5.2 Dark Web Marketplaces

**Data Type:** Vendor-buyer negotiations, dispute resolutions, reviews
**Volume:** 1,000-5,000 transactions/month (visible subset)
**Access:** Tor-based scraping (legal gray area)

**Psychometric Value:**
- Trust and reputation dynamics
- Risk tolerance indicators
- Negotiation styles
- Conflict resolution patterns

**Legal Considerations:**
- Passive observation generally legal
- Active participation illegal (sting operations only)
- Data retention policies unclear
- Consult legal counsel before collection

---

## 6. Public Datasets

### 6.1 Academic Personality Text Corpora

**Source:** Essays, social media posts, blogs with validated personality labels
**Examples:**
- **Essays Dataset:** 2,468 essays with Big Five scores (Pennebaker & King, 1999)
- **myPersonality Dataset:** 75,000+ Facebook posts with personality labels (Kosinski et al., 2013)
- **Pandora Dataset:** Reddit posts with MBTI labels (Mitchell et al., 2015)

**Access:** Publicly available for research
**License:** Cite original publications

**Adaptation Required:**
- Domain shift: Social media ≠ professional communication
- Fine-tuning needed for cybersecurity context
- Transfer learning approach

---

### 6.2 Stress and Emotion Corpora

**Source:** Speech transcripts with emotional/stress annotations
**Examples:**
- **IEMOCAP:** 12 hours of emotional speech (Busso et al., 2008)
- **AVEC:** Audio-visual depression corpus (Valstar et al., 2013)
- **DaIKT:** Daily stress and cognitive load corpus (Sano et al., 2018)

**Psychometric Value:**
- Stress indicator baselines
- Emotion-cognition interactions
- Vocal features for multimodal analysis

---

## 7. Organizational Health Metrics

### 7.1 Psychometric Assessment Results

**Data Type:** Big Five, MBTI, DiSC, Hogan assessments (if conducted)
**Volume:** Depends on organizational assessment programs
**Access:** HR data (strict privacy protections)

**Usage:**
- Ground truth labels for validation
- Correlate NER11 extractions with validated scores
- Test-retest reliability over time

**Ethical Requirements:**
- Individual consent mandatory
- Aggregate reporting only
- Research use disclosure during assessment

---

### 7.2 Performance Reviews and Feedback

**Data Type:** Supervisor comments, peer feedback, self-assessments
**Volume:** Annual or semi-annual per employee
**Access:** HR data (extreme sensitivity)

**Psychometric Value:**
- Behavioral indicators over time
- Bias in performance attribution
- Correlation with communication patterns

**Use Case:**
- Validate group role extractions (leader, specialist)
- Detect bias in evaluation language

**Ethical Restrictions:**
- Strictly research use, never operational decisions
- Anonymization essential
- Institutional Review Board (IRB) approval mandatory

---

## 8. Synthetic Data Generation

### 8.1 LLM-Generated Transcripts

**Method:** GPT-4, Claude, or Llama3 with personality-conditioned prompts
**Volume:** Unlimited (cost-limited)
**Quality:** Variable (requires validation)

**Generation Pipeline:**
```python
# Synthetic transcript generator
from openai import OpenAI

def generate_transcript(personality_profiles, context, duration_minutes):
    prompt = f"""
    Generate a {duration_minutes}-minute meeting transcript about {context}.

    Speakers:
    {format_personality_profiles(personality_profiles)}

    Requirements:
    - Realistic turn-taking
    - Context-appropriate technical language
    - Stress indicators proportional to context severity
    - Group dynamics consistent with personality profiles
    """

    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
```

**Validation:**
- Human expert review for realism
- Compare NER11 extractions to intended profiles
- Measure correlation with real data extractions

---

### 8.2 Agent-Based Simulation

**Method:** Multi-agent conversational simulations with personality engines
**Advantages:**
- Controlled personality parameters
- Systematic exploration of personality combinations
- Large-scale data generation

**Architecture:**
```python
class PersonalityAgent:
    def __init__(self, big_five_scores, cognitive_style, role):
        self.personality = big_five_scores
        self.style = cognitive_style
        self.role = role
        self.message_generator = LLMBackbone()

    def respond(self, conversation_context, stress_level):
        # Generate response consistent with personality
        response = self.message_generator.generate(
            context=conversation_context,
            personality=self.personality,
            stress=stress_level
        )
        return response

# Simulate 4-person meeting with varied personalities
agents = [
    PersonalityAgent(OCEAN(0.8, 0.9, 0.3, 0.7, 0.2), "analytical", "leader"),
    PersonalityAgent(OCEAN(0.4, 0.5, 0.6, 0.8, 0.7), "intuitive", "follower"),
    # ...
]

transcript = simulate_meeting(agents, context="incident", duration=30)
```

---

## Data Quality Standards

### Minimum Corpus Requirements

**For Training NER11 Model:**
- 1,000+ transcripts with personality ground truth
- 5,000+ transcripts without ground truth (semi-supervised)
- 100+ transcripts with expert annotation (validation set)

**For Production Deployment:**
- 10,000+ transcripts covering diverse contexts
- Continuous learning from new transcripts
- Quarterly model retraining

### Annotation Quality

**Inter-Annotator Agreement:**
- Cohen's Kappa ≥ 0.70 for entity boundaries
- Pearson r ≥ 0.75 for personality trait scores

**Ground Truth Validation:**
- Validate 10% of corpus with professional assessments
- Correlate NER11 extractions with validated scores
- Achieve r ≥ 0.60 for Big Five traits

---

## Data Access Governance

### Access Control Tiers

**Tier 1 (Public Data):**
- No restrictions: Academic datasets, public forums, synthetic data

**Tier 2 (Organizational Data - Aggregated):**
- Security team approval required
- Anonymized meeting transcripts
- Aggregated chat logs
- No individual identification possible

**Tier 3 (Organizational Data - Individual):**
- HR and Legal approval required
- IRB approval for research use
- Individual consent obtained
- Email threads, performance reviews
- Strict anonymization and purpose limitation

**Tier 4 (Restricted Data):**
- Executive and Board approval required
- Leadership strategy meetings
- Personnel investigations
- Extreme sensitivity

---

## References

**Personality Datasets:**
- Pennebaker & King (1999). "Linguistic styles: Language use as an individual difference."
- Kosinski et al. (2013). "Private traits and attributes are predictable from digital records."

**Ethics Guidelines:**
- ACM Code of Ethics (2018)
- Belmont Report (1979) - Human subjects research principles
- GDPR Article 9 - Special categories of personal data

---

**End of Enhancement 21 Data Sources**
**Next Steps:** Develop data collection pipelines with appropriate privacy protections.
