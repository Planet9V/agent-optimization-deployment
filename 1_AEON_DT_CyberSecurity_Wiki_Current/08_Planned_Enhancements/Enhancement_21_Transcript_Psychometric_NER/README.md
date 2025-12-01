# Enhancement 21: Transcript Psychometric Extraction (NER11 Integration)

**File:** Enhancement_21_Transcript_Psychometric_NER/README.md
**Created:** 2025-11-26
**Version:** v1.0.0
**Author:** AEON Development Team
**Purpose:** Extract personality traits, cognitive styles, and psychological markers from text/speech transcripts
**Status:** ACTIVE

---

## Executive Summary

Enhancement 21 implements NER11 (Named Entity Recognition - Psychometric Entities) to extract psychological and behavioral markers from communication transcripts. This system identifies personality traits, cognitive patterns, stress indicators, and group dynamics from written and spoken language, feeding the AEON psychometric analysis layer.

**Core Capability**: Transform unstructured communication into structured psychometric profiles for individuals and groups.

---

## NER11 Psychometric Entity Types

### 1. PERSONALITY_TRAIT (Big Five/OCEAN Model)

**Linguistic Markers for Openness:**
- High: "imagine", "creative", "innovative", "curious", "explore", "abstract", "artistic"
- Low: "conventional", "traditional", "practical", "realistic", "familiar", "standard"

**Linguistic Markers for Conscientiousness:**
- High: "organized", "planned", "detailed", "thorough", "disciplined", "systematic", "precise"
- Low: "spontaneous", "flexible", "casual", "improvise", "whenever", "maybe later"

**Linguistic Markers for Extraversion:**
- High: "we", "team", "together", "everyone", "social", "party", "excited", "energized"
- Low: "I", "alone", "prefer solo", "quiet", "individual", "reserved", "introspective"

**Linguistic Markers for Agreeableness:**
- High: "understand", "help", "support", "cooperate", "compromise", "kind", "empathize"
- Low: "compete", "win", "challenge", "disagree", "push back", "skeptical", "critical"

**Linguistic Markers for Neuroticism:**
- High: "worried", "anxious", "stressed", "afraid", "uncertain", "nervous", "overwhelming"
- Low: "calm", "confident", "stable", "relaxed", "unworried", "steady", "composed"

**NER11 Annotation Schema:**
```xml
<PERSONALITY_TRAIT type="OPENNESS" polarity="high" confidence="0.85">
    "I'm really curious about exploring new approaches to threat detection"
</PERSONALITY_TRAIT>

<PERSONALITY_TRAIT type="CONSCIENTIOUSNESS" polarity="low" confidence="0.72">
    "We'll figure out the details later, let's just get something working"
</PERSONALITY_TRAIT>
```

---

### 2. COGNITIVE_STYLE

**Analytical Style Markers:**
- "data shows", "evidence suggests", "logically", "analyze", "decompose", "systematically"
- "root cause", "correlation", "statistical", "metrics", "measure", "quantify"

**Intuitive Style Markers:**
- "gut feeling", "instinct", "sense", "intuition", "feel like", "seems", "appears"
- "pattern", "holistic", "big picture", "gestalt", "experience tells me"

**Creative Style Markers:**
- "what if", "imagine", "brainstorm", "innovative", "outside the box", "novel"
- "unconventional", "experiment", "try something different"

**Pragmatic Style Markers:**
- "works", "practical", "realistic", "proven", "reliable", "safe bet", "known solution"
- "tested", "conservative", "stick with what works"

**NER11 Schema:**
```xml
<COGNITIVE_STYLE type="ANALYTICAL" confidence="0.91">
    "Let me analyze the attack surface metrics to quantify our exposure"
</COGNITIVE_STYLE>

<COGNITIVE_STYLE type="INTUITIVE" confidence="0.68">
    "Something feels off about this traffic pattern, even though the numbers look normal"
</COGNITIVE_STYLE>
```

---

### 3. COMMUNICATION_PATTERN

**Assertive Pattern Markers:**
- "I believe", "my position", "I recommend", "I'm confident", "clearly", "definitely"
- Direct statements, active voice, first-person declarations

**Passive Pattern Markers:**
- "maybe", "perhaps", "I guess", "sort of", "kind of", "possibly", "might"
- Hedging language, qualifiers, indirect suggestions

**Aggressive Pattern Markers:**
- "you must", "you should have", "obviously", "clearly you", "I told you", "wrong"
- Blame language, imperatives directed at others, absolutes

**Collaborative Pattern Markers:**
- "we", "let's", "together", "what do you think", "build on", "combine", "our"
- Team-oriented, inclusive language, open questions

**NER11 Schema:**
```xml
<COMMUNICATION_PATTERN type="AGGRESSIVE" confidence="0.87">
    "You clearly didn't follow the security protocol I outlined last week"
</COMMUNICATION_PATTERN>

<COMMUNICATION_PATTERN type="COLLABORATIVE" confidence="0.93">
    "Let's combine your threat intelligence with our detection capabilities"
</COMMUNICATION_PATTERN>
```

---

### 4. STRESS_INDICATOR

**Urgency Stress Markers:**
- "ASAP", "urgent", "immediately", "critical", "now", "emergency", "rush"
- Multiple exclamation marks, all caps, time pressure language

**Anxiety Stress Markers:**
- "worried", "concerned", "afraid", "don't know", "uncertain", "overwhelmed"
- Hedging increases, question marks multiply, seeking reassurance

**Deflection Stress Markers:**
- "not my fault", "I wasn't told", "someone else", "I don't know about that"
- Blame shifting, responsibility avoidance, information denial

**Cognitive Load Markers:**
- Sentence fragments, incomplete thoughts, topic jumping, repetition
- "um", "uh", "well", "so", pause indicators in transcripts

**NER11 Schema:**
```xml
<STRESS_INDICATOR type="URGENCY" intensity="HIGH" confidence="0.89">
    "CRITICAL: We need to patch this NOW before the vulnerability is exploited!!!"
</STRESS_INDICATOR>

<STRESS_INDICATOR type="COGNITIVE_LOAD" intensity="MEDIUM" confidence="0.76">
    "So, um, the firewall is... well, we need to check... I think maybe..."
</STRESS_INDICATOR>
```

---

### 5. BIAS_MARKER

**Confirmation Bias Markers:**
- "as expected", "proves what I thought", "knew it all along", "typical"
- Seeking information that confirms, ignoring contradictory evidence

**Anchoring Bias Markers:**
- "first thought", "initial impression", "still think", "based on my original"
- Over-reliance on first piece of information

**Availability Bias Markers:**
- "recent breach", "just saw", "happened last week", "everyone's talking about"
- Over-weighting recent or memorable events

**Sunk Cost Bias Markers:**
- "already invested", "too much work", "can't give up now", "after all this time"
- Continuing failed approach due to prior investment

**Attribution Bias Markers:**
- "they always", "he never", "typical of them", "that's just how she is"
- Internal attributions for others' failures, external for own failures

**NER11 Schema:**
```xml
<BIAS_MARKER type="CONFIRMATION" confidence="0.81">
    "This breach proves what I've been saying all along about outsourcing security"
</BIAS_MARKER>

<BIAS_MARKER type="SUNK_COST" confidence="0.74">
    "We've already invested 6 months in this SIEM, we can't switch now"
</BIAS_MARKER>
```

---

### 6. MOTIVATION_SIGNAL (Jouissance Indicators)

**Achievement Motivation:**
- "succeed", "accomplish", "goal", "target", "complete", "win", "best"
- Focus on outcomes, results, metrics

**Power Motivation:**
- "control", "manage", "direct", "lead", "authority", "decision", "my team"
- Focus on influence, status, hierarchy

**Affiliation Motivation:**
- "belong", "team", "together", "relationship", "trust", "friendship", "support"
- Focus on connection, harmony, acceptance

**Autonomy Motivation:**
- "independent", "my way", "freedom", "own decision", "self-directed", "choice"
- Focus on independence, self-direction

**Security Motivation:**
- "safe", "protected", "stable", "certain", "guaranteed", "risk-free", "proven"
- Focus on predictability, safety, comfort

**NER11 Schema:**
```xml
<MOTIVATION_SIGNAL type="POWER" intensity="HIGH" confidence="0.88">
    "I need to be the one making the final decision on our security architecture"
</MOTIVATION_SIGNAL>

<MOTIVATION_SIGNAL type="AFFILIATION" intensity="MEDIUM" confidence="0.79">
    "Most important is that we maintain team trust throughout this incident response"
</MOTIVATION_SIGNAL>
```

---

### 7. GROUP_ROLE

**Leader Role Markers:**
- "we should", "let's", "I recommend", "our direction", "team goal", first to speak
- Direction-setting, decision-making, vision statements

**Follower Role Markers:**
- "agree with", "sounds good", "I'll do that", "as you said", "following up"
- Agreement, implementation focus, deferring to others

**Dissenter Role Markers:**
- "but", "however", "what about", "have we considered", "disagree", "alternative"
- Questioning, challenging, presenting alternatives

**Harmonizer Role Markers:**
- "both sides", "common ground", "compromise", "balance", "understand both"
- Conflict reduction, synthesis, mediation

**Specialist Role Markers:**
- Technical jargon, deep domain knowledge, "technically", "actually", corrections
- Expertise demonstration, detail focus, precision

**NER11 Schema:**
```xml
<GROUP_ROLE type="DISSENTER" confidence="0.86">
    "Have we considered the performance impact of this security control?"
</GROUP_ROLE>

<GROUP_ROLE type="LEADER" confidence="0.92">
    "Our team's priority is containing this incident within 24 hours"
</GROUP_ROLE>
```

---

## Linguistic Feature Engineering

### Feature Categories

**1. Lexical Features:**
- Word frequencies (LIWC categories)
- Part-of-speech distributions
- Vocabulary richness (type-token ratio)
- Sentiment polarity scores

**2. Syntactic Features:**
- Sentence length distribution
- Complexity measures (embedded clauses)
- Passive vs. active voice ratio
- Question vs. statement ratio

**3. Pragmatic Features:**
- Turn-taking patterns
- Interruption frequency
- Response latency
- Topic control

**4. Temporal Features:**
- Speech rate (words per minute)
- Pause patterns
- Disfluency markers
- Response time to questions

---

## Integration with AEON Psychometric Layer

### Data Flow Architecture

```
TEXT/SPEECH TRANSCRIPTS
        ↓
[Preprocessing & Tokenization]
        ↓
[NER11 Entity Extraction]
        ↓
[Feature Engineering]
        ↓
[Confidence Scoring]
        ↓
[Temporal Aggregation]
        ↓
NEO4J PSYCHOMETRIC PROFILES
        ↓
[AEON Analysis Layer]
```

### Neo4j Schema Integration

```cypher
// Individual psychometric profile node
CREATE (p:PsychometricProfile {
    subject_id: "PERSON_12345",
    timestamp: datetime(),
    data_source: "incident_response_transcript_2025_11_26"
})

// Personality trait nodes
CREATE (t:PersonalityTrait {
    trait: "OPENNESS",
    score: 0.72,
    confidence: 0.85,
    evidence_count: 15
})

// Link profile to traits
CREATE (p)-[:HAS_TRAIT {
    temporal_stability: 0.88,
    first_observed: datetime("2025-01-15"),
    last_updated: datetime("2025-11-26")
}]->(t)

// Stress indicator nodes
CREATE (s:StressIndicator {
    type: "URGENCY",
    intensity: "HIGH",
    timestamp: datetime(),
    context: "zero_day_disclosure"
})

CREATE (p)-[:EXHIBITS_STRESS {
    frequency: 0.23,
    duration_minutes: 45
}]->(s)

// Group role relationships
CREATE (p)-[:PLAYS_ROLE {
    role: "DISSENTER",
    in_context: "security_architecture_meeting",
    frequency: 0.15
}]->(g:Group {name: "Security Team"})
```

---

## Training Data Requirements

### Labeled Transcript Corpus Needed

**Minimum Dataset:**
- 500+ meeting transcripts (incident response, planning, reviews)
- 200+ email threads (security team communications)
- 100+ chat logs (Slack, Teams, IRC)
- 50+ interview transcripts (post-incident reviews)

**Annotation Requirements:**
- 2-3 annotators per transcript (inter-annotator agreement check)
- OCEAN scores from validated assessments (ground truth)
- Temporal labels (crisis vs. steady-state)
- Context tags (technical discussion, conflict, planning)

**Data Sources:**
1. Synthetic transcripts (GPT-4 generated with specified profiles)
2. Public datasets (EMNLP, ACL workshops on personality detection)
3. Organizational data (anonymized, IRB-approved)
4. Threat actor forum posts (public OSINT)

---

## Model Architecture

### Transformer-Based NER11 Pipeline

```python
# Conceptual architecture
class PsychometricNER11:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
        self.model = BertForTokenClassification.from_pretrained(
            "bert-base-cased",
            num_labels=len(NER11_TAG_SET)
        )
        self.post_processor = ConfidenceScorer()

    def extract_entities(self, transcript: str) -> List[PsychometricEntity]:
        tokens = self.tokenizer(transcript, return_tensors="pt")
        outputs = self.model(**tokens)
        predictions = torch.argmax(outputs.logits, dim=-1)

        entities = self.decode_predictions(predictions)
        scored_entities = self.post_processor.score(entities, transcript)

        return scored_entities
```

### NER11 Tag Set (BIO Format)

```
B-PERS_OPEN_HIGH    I-PERS_OPEN_HIGH
B-PERS_CONS_LOW     I-PERS_CONS_LOW
B-COGN_ANALYTICAL   I-COGN_ANALYTICAL
B-COMM_AGGRESSIVE   I-COMM_AGGRESSIVE
B-STRESS_URGENCY    I-STRESS_URGENCY
B-BIAS_CONFIRMATION I-BIAS_CONFIRMATION
B-MOTIV_POWER       I-MOTIV_POWER
B-ROLE_LEADER       I-ROLE_LEADER
O (Outside any entity)
```

---

## Validation Metrics

### NER Performance Metrics
- Precision: % of predicted entities that are correct
- Recall: % of actual entities that are detected
- F1-Score: Harmonic mean of precision and recall
- Entity-level accuracy: Exact match rate

**Target Performance:**
- Personality traits: F1 ≥ 0.75
- Cognitive styles: F1 ≥ 0.70
- Communication patterns: F1 ≥ 0.80
- Stress indicators: F1 ≥ 0.65
- Bias markers: F1 ≥ 0.60
- Motivation signals: F1 ≥ 0.55
- Group roles: F1 ≥ 0.70

### Psychometric Validation
- Correlation with validated assessments (Big Five inventories)
- Test-retest reliability over time
- Convergent validity (similar methods should correlate)
- Discriminant validity (different constructs should not correlate)

---

## Privacy and Ethics

### Data Protection Measures
1. **Anonymization:** Remove PII before NER11 processing
2. **Aggregation:** Report only group-level statistics publicly
3. **Consent:** Obtain informed consent for transcript analysis
4. **Purpose Limitation:** Use only for stated security purposes
5. **Right to Erasure:** Allow individuals to request data deletion

### Ethical Guidelines
- **No Discrimination:** Psychometric data cannot be used for hiring/firing
- **Transparency:** Individuals aware of analysis
- **Fairness:** Models tested for demographic bias
- **Accountability:** Human review of high-stakes decisions
- **Reversibility:** Ability to challenge automated assessments

---

## Implementation Roadmap

### Phase 1: Prototype (Months 1-3)
- Develop synthetic training data
- Train baseline BERT-based NER11 model
- Build Neo4j schema for psychometric profiles
- Validate on 100 test transcripts

### Phase 2: Validation (Months 4-6)
- Collect real transcript data (IRB-approved)
- Annotate with validated personality assessments
- Retrain model on real data
- Achieve F1 ≥ 0.70 on held-out test set

### Phase 3: Integration (Months 7-9)
- Integrate with AEON psychometric layer
- Build real-time transcript processing pipeline
- Deploy in pilot security operations center (SOC)
- Monitor performance and collect feedback

### Phase 4: Production (Months 10-12)
- Scale to full organizational deployment
- Continuous learning from new transcripts
- A/B testing against human analyst assessments
- Publish validation study results

---

## References

**Personality Psychology:**
- McCrae & Costa (1997). "Personality trait structure as a human universal."
- Goldberg (1993). "The structure of phenotypic personality traits."

**Computational Linguistics:**
- Pennebaker et al. (2015). "LIWC2015: Linguistic Inquiry and Word Count."
- Mairesse et al. (2007). "Using Linguistic Cues for the Automatic Recognition of Personality."

**Named Entity Recognition:**
- Devlin et al. (2019). "BERT: Pre-training of Deep Bidirectional Transformers."
- Akbik et al. (2018). "Contextual String Embeddings for Sequence Labeling."

---

**End of Enhancement 21 README**
**Next Steps:** Review TASKMASTER_TRANSCRIPT_PSYCHOMETRICS_v1.0.md for implementation details.
