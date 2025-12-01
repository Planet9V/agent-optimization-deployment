# TASKMASTER: Transcript Psychometric Extraction (NER11)
## 10-Agent Swarm for Automated Personality Profiling from Communication Data

**File:** TASKMASTER_TRANSCRIPT_PSYCHOMETRICS_v1.0.md
**Created:** 2025-11-26
**Version:** v1.0.0
**Author:** AEON Development Team
**Swarm Size:** 10 specialized agents
**Coordination:** Sequential (pipeline) with parallel sub-tasks
**Status:** ACTIVE

---

## Mission Statement

Deploy a 10-agent swarm to automatically extract psychometric entities (personality traits, cognitive styles, stress indicators, biases, motivations, group roles) from unstructured communication transcripts using NER11 (Named Entity Recognition for Psychometrics). Output structured profiles to Neo4j for AEON psychometric analysis layer.

**Success Criteria:**
1. F1-score ≥ 0.70 on personality trait extraction (validated against ground truth)
2. Process 100+ transcripts/day with <5% error rate
3. Neo4j psychometric profiles updated in real-time (<1 hour latency)
4. Privacy compliance: PII anonymized, consent tracked, audit logs maintained

---

## Agent Architecture Overview

```
TRANSCRIPT INPUT (meeting audio/text, emails, chats)
        ↓
[AGENT 1: Transcript Preprocessor]
        ↓
[AGENT 2: Big Five Linguistic Analyzer]
[AGENT 3: Dark Triad Detector] ─────────────┐
[AGENT 4: Stress Language Identifier]        │ (Parallel)
[AGENT 5: Bias Language Mapper]              │
[AGENT 6: Group Dynamics Extractor] ─────────┘
        ↓
[AGENT 7: Temporal Evolution Tracker]
        ↓
[AGENT 8: Confidence Scorer]
        ↓
[AGENT 9: Neo4j Psychometric Profile Builder]
        ↓
[AGENT 10: Quality Validator]
        ↓
NEO4J PSYCHOMETRIC PROFILES + VALIDATION REPORT
```

---

## AGENT 1: Transcript Preprocessor

### Role
Clean, tokenize, and segment raw transcripts into analysis-ready format.

### Inputs
- Raw transcript files (VTT, SRT, TXT, JSON)
- Audio files (WAV, MP3) → Whisper transcription
- Email threads (MBOX, EML)
- Chat logs (Slack JSON, Teams HTML)

### Processing Steps

**Step 1.1: Format Normalization**
```python
def normalize_transcript(raw_input):
    """Convert diverse formats to standardized JSON."""
    if raw_input.endswith('.vtt'):
        transcript = parse_vtt(raw_input)
    elif raw_input.endswith('.mp3'):
        transcript = whisper.transcribe(raw_input)
    elif raw_input.endswith('.json'):
        transcript = parse_slack_export(raw_input)
    else:
        raise ValueError(f"Unsupported format: {raw_input}")

    return {
        'source': raw_input,
        'format': 'standardized',
        'speakers': identify_speakers(transcript),
        'utterances': segment_by_speaker(transcript),
        'metadata': extract_metadata(raw_input)
    }
```

**Step 1.2: Speaker Diarization**
- Identify unique speakers (SPEAKER_001, SPEAKER_002, ...)
- Assign speaker IDs consistently across sessions (voice fingerprinting)
- Handle multi-speaker overlap and interruptions

**Step 1.3: Tokenization and Linguistic Preprocessing**
```python
from spacy import load

nlp = load("en_core_web_trf")  # Transformer-based model

def linguistic_preprocessing(utterance):
    doc = nlp(utterance)
    return {
        'tokens': [token.text for token in doc],
        'lemmas': [token.lemma_ for token in doc],
        'pos_tags': [token.pos_ for token in doc],
        'dependencies': [(token.text, token.dep_, token.head.text)
                          for token in doc],
        'entities': [(ent.text, ent.label_) for ent in doc.ents]
    }
```

**Step 1.4: Segmentation**
- Semantic segmentation (topic boundaries using TextTiling or BERTopic)
- Temporal segmentation (sliding windows: 30-second, 2-minute, 5-minute)
- Turn-taking analysis (utterance sequences and response patterns)

### Outputs
```json
{
  "transcript_id": "TRANSCRIPT_20251126_001",
  "source_file": "incident_response_meeting_2025_11_26.mp3",
  "date": "2025-11-26T14:30:00Z",
  "duration_minutes": 45,
  "speakers": [
    {
      "speaker_id": "SPEAKER_001",
      "anonymized_id": "ANON_A3F2",
      "turn_count": 23,
      "word_count": 1872
    },
    {
      "speaker_id": "SPEAKER_002",
      "anonymized_id": "ANON_B7K9",
      "turn_count": 18,
      "word_count": 1245
    }
  ],
  "utterances": [
    {
      "speaker_id": "SPEAKER_001",
      "timestamp": "00:01:23",
      "text": "We need to immediately patch the critical vulnerability...",
      "tokens": ["We", "need", "to", "immediately", ...],
      "pos_tags": ["PRON", "VERB", "PART", "ADV", ...],
      "segment": "incident_severity_discussion"
    }
  ],
  "preprocessing_metadata": {
    "total_words": 8247,
    "unique_words": 1523,
    "type_token_ratio": 0.185,
    "avg_sentence_length": 18.3,
    "passive_voice_ratio": 0.12
  }
}
```

### Quality Checks
- Speaker identification confidence ≥ 0.80
- Transcription word error rate (WER) ≤ 10%
- Complete metadata extraction (no missing timestamps)

---

## AGENT 2: Big Five Linguistic Analyzer (OCEAN)

### Role
Extract Big Five personality trait indicators using linguistic markers and LIWC (Linguistic Inquiry and Word Count) patterns.

### Inputs
- Preprocessed transcript (from Agent 1)
- LIWC dictionary (psychometric word categories)
- Personality trait lexicons (Pennebaker, Mairesse et al.)

### Processing Steps

**Step 2.1: LIWC Feature Extraction**
```python
import liwc

liwc_dict = liwc.load_liwc_dictionary("LIWC2015_English.dic")

def extract_liwc_features(text):
    """Calculate LIWC category frequencies."""
    tokens = text.lower().split()
    liwc_counts = {category: 0 for category in liwc_dict.categories()}

    for token in tokens:
        for category in liwc_dict.get_categories(token):
            liwc_counts[category] += 1

    # Normalize by word count
    total_words = len(tokens)
    liwc_frequencies = {
        cat: count / total_words
        for cat, count in liwc_counts.items()
    }

    return liwc_frequencies
```

**Step 2.2: OCEAN Trait Scoring**

**Openness Indicators:**
```python
OPENNESS_MARKERS = {
    'high': {
        'lexical': ['imagine', 'creative', 'innovative', 'curious', 'novel'],
        'liwc_categories': ['insight', 'tentat', 'discrep'],  # Cognitive complexity
        'syntactic': 'high_vocabulary_diversity'
    },
    'low': {
        'lexical': ['conventional', 'traditional', 'practical', 'standard'],
        'liwc_categories': ['certain', 'conj'],  # Concrete thinking
        'syntactic': 'low_vocabulary_diversity'
    }
}

def score_openness(utterances):
    high_score = sum(
        count_markers(u, OPENNESS_MARKERS['high'])
        for u in utterances
    )
    low_score = sum(
        count_markers(u, OPENNESS_MARKERS['low'])
        for u in utterances
    )

    # Normalize to 0-1 scale
    openness_score = (high_score - low_score) / (high_score + low_score + 1e-6)
    openness_score = (openness_score + 1) / 2  # Shift to [0, 1]

    return openness_score
```

**Conscientiousness Indicators:**
```python
CONSCIENTIOUSNESS_MARKERS = {
    'high': {
        'lexical': ['organized', 'planned', 'detailed', 'systematic', 'thorough'],
        'liwc_categories': ['achievement', 'work', 'organize'],
        'syntactic': 'formal_language',
        'temporal': 'future_tense_references'
    },
    'low': {
        'lexical': ['spontaneous', 'flexible', 'improvise', 'casual'],
        'liwc_categories': ['leisure', 'present'],
        'syntactic': 'informal_language'
    }
}
```

**Extraversion Indicators:**
```python
EXTRAVERSION_MARKERS = {
    'high': {
        'lexical': ['we', 'us', 'team', 'together', 'everyone', 'excited'],
        'liwc_categories': ['social', 'posemo', 'we'],
        'pragmatic': 'high_turn_frequency',  # Talks a lot
        'prosodic': 'high_speech_rate'
    },
    'low': {
        'lexical': ['I', 'me', 'alone', 'individual', 'prefer solo'],
        'liwc_categories': ['i', 'sad', 'negemo'],
        'pragmatic': 'low_turn_frequency'
    }
}
```

**Agreeableness Indicators:**
```python
AGREEABLENESS_MARKERS = {
    'high': {
        'lexical': ['understand', 'help', 'support', 'cooperate', 'kind'],
        'liwc_categories': ['social', 'posemo', 'we'],
        'sentiment': 'positive_other_references'
    },
    'low': {
        'lexical': ['compete', 'win', 'challenge', 'disagree', 'critical'],
        'liwc_categories': ['negate', 'anger', 'swear'],
        'sentiment': 'negative_other_references'
    }
}
```

**Neuroticism Indicators:**
```python
NEUROTICISM_MARKERS = {
    'high': {
        'lexical': ['worried', 'anxious', 'stressed', 'afraid', 'uncertain'],
        'liwc_categories': ['anx', 'negemo', 'sad', 'anger'],
        'syntactic': 'high_hedging',  # "maybe", "perhaps"
        'prosodic': 'high_pitch_variability'
    },
    'low': {
        'lexical': ['calm', 'confident', 'stable', 'relaxed', 'certain'],
        'liwc_categories': ['posemo', 'certain'],
        'syntactic': 'low_hedging'
    }
}
```

**Step 2.3: Machine Learning Ensemble**
```python
from sklearn.ensemble import RandomForestRegressor

# Train on labeled corpus (personality + transcripts)
def train_ocean_models(labeled_corpus):
    models = {}
    for trait in ['O', 'C', 'E', 'A', 'N']:
        X = extract_all_features(labeled_corpus)  # LIWC + markers
        y = [person[trait + '_score'] for person in labeled_corpus]

        model = RandomForestRegressor(n_estimators=100, max_depth=10)
        model.fit(X, y)
        models[trait] = model

    return models

# Predict on new transcript
def predict_ocean(transcript, models):
    features = extract_all_features([transcript])
    ocean_scores = {
        trait: models[trait].predict(features)[0]
        for trait in ['O', 'C', 'E', 'A', 'N']
    }
    return ocean_scores
```

### Outputs
```json
{
  "speaker_id": "ANON_A3F2",
  "personality_traits": {
    "openness": {
      "score": 0.72,
      "confidence": 0.85,
      "evidence": [
        {
          "utterance_id": 5,
          "marker": "I'm curious about exploring new detection methods",
          "marker_type": "lexical_openness_high"
        }
      ]
    },
    "conscientiousness": {
      "score": 0.88,
      "confidence": 0.91,
      "evidence": [
        {
          "utterance_id": 12,
          "marker": "Let me detail the systematic approach we'll take",
          "marker_type": "lexical_conscientiousness_high"
        }
      ]
    },
    "extraversion": {"score": 0.45, "confidence": 0.78},
    "agreeableness": {"score": 0.65, "confidence": 0.82},
    "neuroticism": {"score": 0.38, "confidence": 0.79}
  },
  "temporal_stability": 0.83  # Consistency across transcript segments
}
```

### Quality Checks
- Minimum 50 words per speaker (statistical reliability)
- Cross-validation with validated personality assessments (if available)
- Inter-rater agreement for manual annotations ≥ 0.70

---

## AGENT 3: Dark Triad Detector

### Role
Identify Machiavellianism, narcissism, and psychopathy indicators in communication patterns.

### Inputs
- Preprocessed transcript (from Agent 1)
- Dark Triad lexicons (Jones & Paulhus, 2014)
- Manipulation tactics taxonomy

### Processing Steps

**Step 3.1: Machiavellianism Detection**
```python
MACHIAVELLIANISM_MARKERS = {
    'strategic_thinking': [
        'leverage', 'position', 'advantage', 'opportunity', 'timing'
    ],
    'manipulation_language': [
        'you might want to', 'it would be wise', 'consider that',
        'from your perspective'  # False empathy
    ],
    'goal_orientation': [
        'outcome', 'result', 'win', 'achieve', 'success at any cost'
    ],
    'moral_flexibility': [
        'necessary', 'pragmatic', 'realistic', 'end justifies'
    ],
    'social_calculation': [
        'useful', 'beneficial', 'strategic relationship', 'network'
    ]
}

def detect_machiavellianism(utterances):
    score = 0
    evidence = []

    for u in utterances:
        # Pattern 1: Manipulation tactics
        if contains_false_empathy(u) and contains_redirection(u):
            score += 0.15
            evidence.append({
                'pattern': 'manipulation_tactic',
                'utterance': u
            })

        # Pattern 2: Strategic framing
        if contains_strategic_language(u):
            score += 0.10
            evidence.append({
                'pattern': 'strategic_framing',
                'utterance': u
            })

    return {'score': min(score, 1.0), 'evidence': evidence}
```

**Step 3.2: Narcissism Detection**
```python
NARCISSISM_MARKERS = {
    'self_reference_excess': {
        'pattern': 'high_first_person_pronoun_ratio',  # >15% of words
        'liwc_category': 'i'
    },
    'grandiosity': [
        'I am the best', 'my exceptional', 'my superior',
        'no one else', 'only I can'
    ],
    'attention_seeking': {
        'pattern': 'topic_control',  # Redirects conversation to self
        'interruption_rate': 'high'
    },
    'entitlement': [
        'I deserve', 'I should get', 'owe me', 'my right'
    ],
    'lack_of_empathy': {
        'pattern': 'low_other_reference',  # Rarely mentions others' perspectives
        'liwc_categories': ['you', 'they', 'shehe']  # Low frequency
    }
}

def detect_narcissism(speaker_utterances):
    # Calculate self-reference ratio
    total_words = sum(len(u.split()) for u in speaker_utterances)
    first_person_count = sum(
        u.lower().count(' i ') + u.lower().count(' me ') + u.lower().count(' my ')
        for u in speaker_utterances
    )
    self_reference_ratio = first_person_count / total_words

    score = 0
    evidence = []

    # Excessive self-reference (narcissism indicator)
    if self_reference_ratio > 0.15:
        score += 0.25
        evidence.append({
            'pattern': 'excessive_self_reference',
            'ratio': self_reference_ratio
        })

    # Grandiosity language
    grandiosity_count = count_pattern_matches(
        speaker_utterances,
        NARCISSISM_MARKERS['grandiosity']
    )
    if grandiosity_count > 2:
        score += 0.20
        evidence.append({
            'pattern': 'grandiosity',
            'count': grandiosity_count
        })

    return {'score': min(score, 1.0), 'evidence': evidence}
```

**Step 3.3: Psychopathy Detection**
```python
PSYCHOPATHY_MARKERS = {
    'callousness': [
        "don't care", "doesn't matter", "not my problem",
        "whatever", "so what"
    ],
    'impulsivity': [
        "just do it", "right now", "can't wait", "immediately",
        "no time to think"
    ],
    'remorselessness': [
        "had to be done", "necessary action", "no regrets",
        "would do it again"
    ],
    'shallow_affect': {
        'pattern': 'low_emotional_language',
        'liwc_categories': ['posemo', 'negemo'],  # Low frequency
        'emotional_range': 'narrow'
    },
    'blame_externalization': [
        "their fault", "they made me", "forced to",
        "no choice", "circumstances"
    ]
}

def detect_psychopathy(utterances, context='general'):
    score = 0
    evidence = []

    # Callousness detection
    callous_statements = count_pattern_matches(
        utterances,
        PSYCHOPATHY_MARKERS['callousness']
    )
    if callous_statements > 1:
        score += 0.15
        evidence.append({
            'pattern': 'callousness',
            'count': callous_statements
        })

    # Emotional language deficit
    emotional_word_ratio = calculate_emotional_language_ratio(utterances)
    if emotional_word_ratio < 0.02:  # Very low emotional expression
        score += 0.20
        evidence.append({
            'pattern': 'shallow_affect',
            'ratio': emotional_word_ratio
        })

    return {'score': min(score, 1.0), 'evidence': evidence}
```

### Outputs
```json
{
  "speaker_id": "ANON_B7K9",
  "dark_triad": {
    "machiavellianism": {
      "score": 0.42,
      "confidence": 0.68,
      "evidence": [
        {
          "pattern": "manipulation_tactic",
          "utterance": "You might want to consider that this approach benefits everyone",
          "analysis": "False empathy combined with strategic redirection"
        }
      ]
    },
    "narcissism": {
      "score": 0.23,
      "confidence": 0.71,
      "evidence": [
        {
          "pattern": "self_reference_excess",
          "ratio": 0.17,
          "threshold": 0.15
        }
      ]
    },
    "psychopathy": {
      "score": 0.11,
      "confidence": 0.59,
      "evidence": []
    }
  },
  "risk_assessment": "LOW",  # Dark Triad scores below concern thresholds
  "recommended_monitoring": false
}
```

### Quality Checks
- Avoid false positives (confident communication ≠ narcissism)
- Context-aware interpretation (incident stress ≠ psychopathy)
- Minimum 200 words per speaker for Dark Triad assessment

---

## AGENT 4: Stress Language Identifier

### Role
Detect and quantify stress indicators in communication: urgency, anxiety, deflection, cognitive load.

### Inputs
- Preprocessed transcript (from Agent 1)
- Context metadata (meeting type: incident vs. planning)

### Processing Steps

**Step 4.1: Urgency Stress Detection**
```python
URGENCY_MARKERS = {
    'time_pressure': ['ASAP', 'urgent', 'immediately', 'critical', 'now', 'rush'],
    'emphasis': {
        'all_caps': ['NOW', 'CRITICAL', 'URGENT'],
        'exclamation_marks': 'multiple',  # "!!!" or more
        'repetition': ['hurry hurry', 'now now now']
    },
    'direct_commands': ['must', 'need to', 'have to', 'get this done']
}

def detect_urgency_stress(utterance):
    intensity = 0
    markers = []

    # Time pressure language
    urgency_word_count = count_pattern_matches(
        [utterance],
        URGENCY_MARKERS['time_pressure']
    )
    intensity += urgency_word_count * 0.15

    # Emphasis patterns
    if utterance.isupper() or has_multiple_caps(utterance):
        intensity += 0.25
        markers.append('ALL_CAPS')

    exclamation_count = utterance.count('!')
    if exclamation_count >= 2:
        intensity += exclamation_count * 0.10
        markers.append(f'EXCLAMATIONS_{exclamation_count}')

    return {
        'intensity': min(intensity, 1.0),
        'category': 'URGENCY',
        'markers': markers
    }
```

**Step 4.2: Anxiety Stress Detection**
```python
ANXIETY_MARKERS = {
    'worry_language': ['worried', 'concerned', 'afraid', 'nervous', 'anxious'],
    'uncertainty': ['don\'t know', 'unsure', 'not certain', 'unclear', 'confused'],
    'hedging': ['maybe', 'perhaps', 'possibly', 'might', 'could'],
    'reassurance_seeking': ['right?', 'correct?', 'you think?', 'is that okay?'],
    'catastrophizing': ['disaster', 'terrible', 'worst case', 'catastrophic']
}

def detect_anxiety_stress(utterances, speaker_id):
    # Calculate hedging ratio
    total_sentences = len(utterances)
    hedging_count = sum(
        count_pattern_matches([u], ANXIETY_MARKERS['hedging'])
        for u in utterances
    )
    hedging_ratio = hedging_count / total_sentences

    # Worry language frequency
    worry_count = sum(
        count_pattern_matches([u], ANXIETY_MARKERS['worry_language'])
        for u in utterances
    )

    intensity = 0
    if hedging_ratio > 0.30:  # >30% of sentences contain hedging
        intensity += 0.20

    if worry_count > 3:
        intensity += 0.25

    return {
        'intensity': min(intensity, 1.0),
        'category': 'ANXIETY',
        'hedging_ratio': hedging_ratio,
        'worry_count': worry_count
    }
```

**Step 4.3: Deflection Stress Detection**
```python
DEFLECTION_MARKERS = {
    'blame_shifting': ['not my fault', 'I wasn\'t told', 'someone else', 'they did'],
    'responsibility_avoidance': ['not my job', 'wasn\'t assigned', 'out of scope'],
    'information_denial': ['I don\'t know about that', 'news to me', 'first I\'m hearing'],
    'topic_avoidance': ['can we talk about', 'let\'s focus on', 'more important']
}

def detect_deflection_stress(utterances, conversational_context):
    deflection_count = 0
    evidence = []

    for u in utterances:
        if contains_blame_shift(u):
            deflection_count += 1
            evidence.append({
                'type': 'blame_shifting',
                'utterance': u
            })

        if contains_responsibility_avoidance(u):
            deflection_count += 1
            evidence.append({
                'type': 'responsibility_avoidance',
                'utterance': u
            })

    # Context matters: Deflection during incident response is high-stress indicator
    intensity = deflection_count * 0.20
    if conversational_context == 'incident_response':
        intensity *= 1.5  # Amplify in high-stakes context

    return {
        'intensity': min(intensity, 1.0),
        'category': 'DEFLECTION',
        'deflection_count': deflection_count,
        'evidence': evidence
    }
```

**Step 4.4: Cognitive Load Detection**
```python
COGNITIVE_LOAD_MARKERS = {
    'disfluency': ['um', 'uh', 'er', 'ah'],
    'sentence_fragments': 'incomplete_thoughts',
    'repetition': 'word_or_phrase_repetition',
    'topic_jumping': 'rapid_topic_changes',
    'speech_errors': ['I mean', 'wait', 'sorry', 'what I meant']
}

def detect_cognitive_load(utterances, timestamps):
    # Disfluency rate
    total_words = sum(len(u.split()) for u in utterances)
    disfluency_count = sum(
        count_pattern_matches([u], COGNITIVE_LOAD_MARKERS['disfluency'])
        for u in utterances
    )
    disfluency_rate = disfluency_count / total_words

    # Sentence fragmentation
    complete_sentences = sum(
        1 for u in utterances if is_complete_sentence(u)
    )
    fragmentation_ratio = 1 - (complete_sentences / len(utterances))

    # Topic coherence
    topic_jumps = count_topic_changes(utterances, threshold=0.3)

    intensity = 0
    if disfluency_rate > 0.05:  # >5% of words are disfluencies
        intensity += 0.25

    if fragmentation_ratio > 0.40:  # >40% incomplete sentences
        intensity += 0.20

    if topic_jumps > len(utterances) * 0.30:  # Frequent topic changes
        intensity += 0.20

    return {
        'intensity': min(intensity, 1.0),
        'category': 'COGNITIVE_LOAD',
        'disfluency_rate': disfluency_rate,
        'fragmentation_ratio': fragmentation_ratio,
        'topic_jumps': topic_jumps
    }
```

### Outputs
```json
{
  "speaker_id": "ANON_C5R1",
  "stress_indicators": [
    {
      "type": "URGENCY",
      "intensity": 0.75,
      "confidence": 0.89,
      "timestamp": "00:12:45",
      "context": "zero_day_disclosure",
      "evidence": {
        "utterance": "We MUST patch this IMMEDIATELY before it's exploited!!!",
        "markers": ["ALL_CAPS", "EXCLAMATIONS_3", "time_pressure_high"]
      }
    },
    {
      "type": "COGNITIVE_LOAD",
      "intensity": 0.58,
      "confidence": 0.76,
      "timestamp": "00:18:30",
      "evidence": {
        "disfluency_rate": 0.08,
        "fragmentation_ratio": 0.45,
        "utterance_sample": "So, um, the firewall is... well, we need to, uh..."
      }
    }
  ],
  "aggregate_stress_score": 0.67,
  "stress_trend": "INCREASING",  # Compared to speaker's baseline
  "risk_flag": "MONITOR"
}
```

### Quality Checks
- Context-aware interpretation (incident ≠ baseline stress)
- Baseline establishment (speaker's normal stress level)
- False positive mitigation (excited ≠ stressed)

---

## AGENT 5: Bias Language Mapper

### Role
Identify cognitive biases expressed through language: confirmation, anchoring, availability, sunk cost, attribution.

### Inputs
- Preprocessed transcript (from Agent 1)
- Decision context (planning, incident response, retrospective)

### Processing Steps

**Step 5.1: Confirmation Bias Detection**
```python
CONFIRMATION_BIAS_MARKERS = {
    'expectation_language': ['as expected', 'knew it', 'told you so', 'typical'],
    'selective_evidence': {
        'pattern': 'ignoring_contradictory_evidence',
        'indicators': ['but ignoring', 'dismissing', 'not considering']
    },
    'premature_closure': ['obviously', 'clearly', 'without a doubt', 'definitely']
}

def detect_confirmation_bias(utterances, decision_context):
    evidence = []
    score = 0

    for u in utterances:
        # "As expected" language
        if contains_expectation_language(u):
            score += 0.15
            evidence.append({
                'type': 'expectation_confirmation',
                'utterance': u
            })

        # Premature closure (not exploring alternatives)
        if contains_certainty_language(u) and not_enough_evidence(decision_context):
            score += 0.20
            evidence.append({
                'type': 'premature_closure',
                'utterance': u,
                'analysis': 'High certainty with insufficient evidence'
            })

    return {
        'bias': 'CONFIRMATION',
        'score': min(score, 1.0),
        'confidence': 0.72,
        'evidence': evidence
    }
```

**Step 5.2: Anchoring Bias Detection**
```python
ANCHORING_BIAS_MARKERS = {
    'first_impression': ['first thought', 'initial impression', 'originally'],
    'persistence': ['still think', 'maintain', 'stick with original'],
    'insufficient_adjustment': {
        'pattern': 'over_reliance_on_initial_value',
        'context': 'estimation_or_pricing'
    }
}

def detect_anchoring_bias(utterances, temporal_sequence):
    evidence = []
    score = 0

    # Find initial position stated
    initial_position = identify_first_position(utterances)

    # Check if position unchanged despite new information
    if initial_position and position_unchanged(utterances, initial_position):
        new_info_presented = count_new_information_introduced(temporal_sequence)
        if new_info_presented >= 3:  # Significant new info ignored
            score += 0.30
            evidence.append({
                'type': 'anchoring_persistence',
                'initial_position': initial_position,
                'new_info_ignored': new_info_presented
            })

    return {
        'bias': 'ANCHORING',
        'score': min(score, 1.0),
        'confidence': 0.68,
        'evidence': evidence
    }
```

**Step 5.3: Availability Bias Detection**
```python
AVAILABILITY_BIAS_MARKERS = {
    'recency': ['just happened', 'recent', 'last week', 'saw yesterday'],
    'salience': ['everyone\'s talking about', 'all over the news', 'famous case'],
    'personal_experience': ['happened to me', 'I remember when', 'in my experience']
}

def detect_availability_bias(utterances):
    evidence = []
    score = 0

    for u in utterances:
        # Over-weighting recent events
        if contains_recency_language(u) and used_as_primary_evidence(u):
            score += 0.20
            evidence.append({
                'type': 'recency_overweight',
                'utterance': u
            })

        # Over-weighting salient/memorable events
        if contains_salience_language(u):
            score += 0.15
            evidence.append({
                'type': 'salience_overweight',
                'utterance': u
            })

    return {
        'bias': 'AVAILABILITY',
        'score': min(score, 1.0),
        'confidence': 0.75,
        'evidence': evidence
    }
```

**Step 5.4: Sunk Cost Bias Detection**
```python
SUNK_COST_BIAS_MARKERS = {
    'investment_language': ['already invested', 'spent so much', 'put in time/money'],
    'loss_aversion': ['waste', 'for nothing', 'can\'t give up now'],
    'emotional_attachment': ['after all this work', 'too much effort', 'can\'t quit']
}

def detect_sunk_cost_bias(utterances, decision_context):
    evidence = []
    score = 0

    # Check if past investment used to justify future commitment
    for u in utterances:
        if contains_sunk_cost_justification(u) and decision_context == 'continuation':
            score += 0.25
            evidence.append({
                'type': 'sunk_cost_fallacy',
                'utterance': u,
                'analysis': 'Past investment used to justify continued investment'
            })

    return {
        'bias': 'SUNK_COST',
        'score': min(score, 1.0),
        'confidence': 0.79,
        'evidence': evidence
    }
```

**Step 5.5: Attribution Bias Detection**
```python
ATTRIBUTION_BIAS_MARKERS = {
    'internal_attribution_others': [
        'they always', 'he never', 'typical of them', 'just how she is'
    ],
    'external_attribution_self': [
        'circumstances', 'bad luck', 'forced to', 'had no choice'
    ],
    'dispositional_language': ['personality', 'nature', 'type of person']
}

def detect_attribution_bias(utterances):
    evidence = []
    score = 0

    self_references = [u for u in utterances if is_self_reference(u)]
    other_references = [u for u in utterances if is_other_reference(u)]

    # Internal attribution for others' failures
    others_internal = count_pattern_matches(
        other_references,
        ATTRIBUTION_BIAS_MARKERS['internal_attribution_others']
    )

    # External attribution for own failures
    self_external = count_pattern_matches(
        self_references,
        ATTRIBUTION_BIAS_MARKERS['external_attribution_self']
    )

    if others_internal > 0 and self_external > 0:
        score += 0.30
        evidence.append({
            'type': 'fundamental_attribution_error',
            'pattern': 'Internal attribution for others, external for self'
        })

    return {
        'bias': 'ATTRIBUTION',
        'score': min(score, 1.0),
        'confidence': 0.71,
        'evidence': evidence
    }
```

### Outputs
```json
{
  "speaker_id": "ANON_D2W8",
  "cognitive_biases": [
    {
      "bias_type": "CONFIRMATION",
      "score": 0.68,
      "confidence": 0.81,
      "evidence": [
        {
          "utterance": "This breach proves what I've been saying all along about cloud security",
          "analysis": "Using single instance to confirm pre-existing belief"
        }
      ],
      "risk_assessment": "MEDIUM",
      "recommendation": "Seek disconfirming evidence"
    },
    {
      "bias_type": "SUNK_COST",
      "score": 0.52,
      "confidence": 0.74,
      "evidence": [
        {
          "utterance": "We've invested 8 months in this SIEM, we can't switch now",
          "analysis": "Past investment used to justify continued commitment despite issues"
        }
      ],
      "risk_assessment": "MEDIUM",
      "recommendation": "Evaluate based on future value, not past investment"
    }
  ],
  "aggregate_bias_score": 0.60,
  "decision_quality_flag": "REVIEW_RECOMMENDED"
}
```

### Quality Checks
- Context-aware interpretation (strategic persistence ≠ sunk cost bias)
- Severity assessment (minor biases vs. decision-critical)
- Validation against decision outcomes (when available)

---

## AGENT 6: Group Dynamics Extractor

### Role
Identify group roles and interaction patterns: leader, follower, dissenter, harmonizer, specialist.

### Inputs
- Preprocessed transcript with speaker interactions (from Agent 1)
- Turn-taking sequences
- Social network analysis of conversation flow

### Processing Steps

**Step 6.1: Leader Role Detection**
```python
LEADER_MARKERS = {
    'direction_setting': ['we should', 'let\'s', 'our direction', 'team goal'],
    'decision_making': ['I recommend', 'we\'ll do', 'the plan is'],
    'vision_statements': ['our mission', 'long-term', 'objective'],
    'interaction_patterns': {
        'speaks_first': 'high_frequency',
        'interruption_privilege': 'high',
        'response_rate': 'others_respond_to_leader_frequently'
    }
}

def detect_leader_role(speaker_id, all_utterances, interaction_graph):
    score = 0
    evidence = []

    # First-to-speak frequency
    first_utterance_count = count_first_utterances(speaker_id, all_utterances)
    if first_utterance_count > len(all_utterances) * 0.30:  # Speaks first >30% of time
        score += 0.25
        evidence.append('speaks_first_frequently')

    # Direction-setting language
    direction_count = count_pattern_matches(
        get_speaker_utterances(speaker_id, all_utterances),
        LEADER_MARKERS['direction_setting']
    )
    if direction_count > 3:
        score += 0.20
        evidence.append('direction_setting_language')

    # Centrality in interaction network
    centrality = calculate_betweenness_centrality(speaker_id, interaction_graph)
    if centrality > 0.40:  # High centrality (information gatekeeper)
        score += 0.25
        evidence.append(f'high_centrality_{centrality:.2f}')

    return {
        'role': 'LEADER',
        'score': min(score, 1.0),
        'confidence': 0.86,
        'evidence': evidence
    }
```

**Step 6.2: Follower Role Detection**
```python
FOLLOWER_MARKERS = {
    'agreement': ['agree', 'sounds good', 'makes sense', 'yes'],
    'implementation_focus': ['I\'ll do that', 'will implement', 'following up'],
    'deferring': ['as you said', 'as mentioned', 'per your direction'],
    'interaction_patterns': {
        'responds_to_others': 'high',
        'initiates_topics': 'low',
        'seeks_approval': 'high'
    }
}

def detect_follower_role(speaker_id, all_utterances, interaction_graph):
    score = 0
    evidence = []

    speaker_utt = get_speaker_utterances(speaker_id, all_utterances)

    # Agreement language frequency
    agreement_ratio = count_pattern_matches(
        speaker_utt,
        FOLLOWER_MARKERS['agreement']
    ) / len(speaker_utt)

    if agreement_ratio > 0.40:
        score += 0.30
        evidence.append(f'high_agreement_ratio_{agreement_ratio:.2f}')

    # Low topic initiation
    topics_initiated = count_new_topics_by_speaker(speaker_id, all_utterances)
    if topics_initiated < 2:
        score += 0.25
        evidence.append('low_topic_initiation')

    return {
        'role': 'FOLLOWER',
        'score': min(score, 1.0),
        'confidence': 0.79,
        'evidence': evidence
    }
```

**Step 6.3: Dissenter Role Detection**
```python
DISSENTER_MARKERS = {
    'disagreement': ['but', 'however', 'disagree', 'not sure about'],
    'questioning': ['what about', 'have we considered', 'why', 'how'],
    'alternatives': ['alternative', 'different approach', 'instead'],
    'challenge': ['challenge that', 'push back', 'not convinced']
}

def detect_dissenter_role(speaker_id, all_utterances):
    score = 0
    evidence = []

    speaker_utt = get_speaker_utterances(speaker_id, all_utterances)

    # Disagreement language
    disagreement_count = count_pattern_matches(
        speaker_utt,
        DISSENTER_MARKERS['disagreement'] + DISSENTER_MARKERS['challenge']
    )

    if disagreement_count > len(speaker_utt) * 0.20:  # >20% of utterances
        score += 0.30
        evidence.append(f'high_disagreement_{disagreement_count}')

    # Question frequency (critical questioning)
    question_count = sum(1 for u in speaker_utt if '?' in u)
    question_ratio = question_count / len(speaker_utt)

    if question_ratio > 0.35:
        score += 0.25
        evidence.append(f'high_questioning_{question_ratio:.2f}')

    return {
        'role': 'DISSENTER',
        'score': min(score, 1.0),
        'confidence': 0.82,
        'evidence': evidence
    }
```

**Step 6.4: Harmonizer Role Detection**
```python
HARMONIZER_MARKERS = {
    'synthesis': ['both sides', 'common ground', 'balance', 'integrate'],
    'mediation': ['let\'s hear', 'understand both', 'see the point'],
    'conflict_reduction': ['compromise', 'middle way', 'agree on'],
    'positive_framing': ['opportunity', 'build on', 'combine']
}

def detect_harmonizer_role(speaker_id, all_utterances, conflict_episodes):
    score = 0
    evidence = []

    speaker_utt = get_speaker_utterances(speaker_id, all_utterances)

    # Synthesis language
    synthesis_count = count_pattern_matches(
        speaker_utt,
        HARMONIZER_MARKERS['synthesis']
    )

    if synthesis_count > 2:
        score += 0.25
        evidence.append('synthesis_language')

    # Intervention during conflict
    conflict_utterances = get_utterances_during_conflict(speaker_id, conflict_episodes)
    if len(conflict_utterances) > 0:
        mediation_attempts = count_pattern_matches(
            conflict_utterances,
            HARMONIZER_MARKERS['mediation']
        )
        if mediation_attempts > 0:
            score += 0.30
            evidence.append('conflict_mediation')

    return {
        'role': 'HARMONIZER',
        'score': min(score, 1.0),
        'confidence': 0.76,
        'evidence': evidence
    }
```

**Step 6.5: Specialist Role Detection**
```python
SPECIALIST_MARKERS = {
    'technical_jargon': 'high_domain_vocabulary',
    'precision': ['technically', 'specifically', 'accurately', 'precisely'],
    'corrections': ['actually', 'correction', 'to clarify'],
    'deep_knowledge': 'detailed_explanations',
    'expertise_signaling': ['in my experience', 'professionally', 'based on research']
}

def detect_specialist_role(speaker_id, all_utterances, domain_vocabulary):
    score = 0
    evidence = []

    speaker_utt = get_speaker_utterances(speaker_id, all_utterances)

    # Technical vocabulary density
    tech_vocab_count = count_domain_terms(speaker_utt, domain_vocabulary)
    tech_vocab_density = tech_vocab_count / sum(len(u.split()) for u in speaker_utt)

    if tech_vocab_density > 0.10:  # >10% domain-specific terms
        score += 0.30
        evidence.append(f'high_tech_vocab_{tech_vocab_density:.2f}')

    # Correction behavior (expertise assertion)
    correction_count = count_pattern_matches(
        speaker_utt,
        SPECIALIST_MARKERS['corrections']
    )

    if correction_count > 2:
        score += 0.25
        evidence.append('expertise_corrections')

    return {
        'role': 'SPECIALIST',
        'score': min(score, 1.0),
        'confidence': 0.84,
        'evidence': evidence
    }
```

### Outputs
```json
{
  "group_dynamics": {
    "participants": [
      {
        "speaker_id": "ANON_A3F2",
        "roles": [
          {
            "role": "LEADER",
            "score": 0.88,
            "confidence": 0.91,
            "evidence": ["speaks_first_frequently", "direction_setting", "high_centrality_0.67"]
          },
          {
            "role": "SPECIALIST",
            "score": 0.72,
            "confidence": 0.85,
            "evidence": ["high_tech_vocab_0.14", "expertise_corrections"]
          }
        ],
        "primary_role": "LEADER"
      },
      {
        "speaker_id": "ANON_B7K9",
        "roles": [
          {
            "role": "DISSENTER",
            "score": 0.79,
            "confidence": 0.86,
            "evidence": ["high_disagreement_8", "high_questioning_0.42"]
          }
        ],
        "primary_role": "DISSENTER"
      }
    ],
    "interaction_network": {
      "edges": [
        {"from": "ANON_A3F2", "to": "ANON_B7K9", "weight": 12, "type": "response"},
        {"from": "ANON_B7K9", "to": "ANON_A3F2", "weight": 9, "type": "challenge"}
      ],
      "centrality_scores": {
        "ANON_A3F2": 0.67,
        "ANON_B7K9": 0.45
      }
    },
    "group_health_indicators": {
      "role_diversity": 0.85,  # Healthy variety of roles
      "conflict_level": "MODERATE",  # Dissenter present but not excessive
      "cohesion": 0.72
    }
  }
}
```

### Quality Checks
- Role stability across multiple meetings (consistency)
- Network centrality validation (matches observed influence)
- Context-aware role interpretation (incident vs. planning meetings)

---

## AGENT 7: Temporal Evolution Tracker

### Role
Monitor personality trait changes over time, detect trends, and identify crisis-related shifts.

### Inputs
- Historical psychometric profiles (all previous extractions for each speaker)
- Current transcript analysis (from Agents 2-6)
- Timeline metadata (normal operations vs. crisis periods)

### Processing Steps

**Step 7.1: Longitudinal Trait Tracking**
```python
def track_personality_evolution(speaker_id, current_profile, historical_profiles):
    """Compare current traits against historical baseline."""

    traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    evolution = {}

    for trait in traits:
        historical_scores = [
            p[trait]['score'] for p in historical_profiles
            if trait in p
        ]

        if len(historical_scores) < 3:
            # Insufficient history for trend analysis
            evolution[trait] = {
                'trend': 'INSUFFICIENT_DATA',
                'stability': None
            }
            continue

        # Calculate baseline (historical mean)
        baseline = np.mean(historical_scores)
        baseline_std = np.std(historical_scores)

        current_score = current_profile[trait]['score']

        # Deviation from baseline
        z_score = (current_score - baseline) / (baseline_std + 1e-6)

        # Trend analysis (linear regression)
        timestamps = [p['timestamp'] for p in historical_profiles]
        trend_slope, _ = np.polyfit(timestamps, historical_scores, 1)

        evolution[trait] = {
            'current_score': current_score,
            'baseline': baseline,
            'deviation_z': z_score,
            'trend': 'INCREASING' if trend_slope > 0.01 else 'DECREASING' if trend_slope < -0.01 else 'STABLE',
            'stability': 1 / (baseline_std + 1e-6),  # Lower std = more stable
            'alert': abs(z_score) > 2.0  # >2 std from baseline
        }

    return evolution
```

**Step 7.2: Crisis-Related Shifts Detection**
```python
def detect_crisis_related_shifts(speaker_id, timeline):
    """Identify personality changes correlated with crisis events."""

    crisis_periods = identify_crisis_periods(timeline)
    normal_periods = identify_normal_periods(timeline)

    crisis_profiles = get_profiles_during(speaker_id, crisis_periods)
    normal_profiles = get_profiles_during(speaker_id, normal_periods)

    shifts = {}

    for trait in ['neuroticism', 'conscientiousness', 'agreeableness']:
        crisis_mean = np.mean([p[trait]['score'] for p in crisis_profiles])
        normal_mean = np.mean([p[trait]['score'] for p in normal_profiles])

        shift_magnitude = crisis_mean - normal_mean
        shift_direction = 'INCREASE' if shift_magnitude > 0 else 'DECREASE'

        # Statistical significance (t-test)
        t_stat, p_value = stats.ttest_ind(
            [p[trait]['score'] for p in crisis_profiles],
            [p[trait]['score'] for p in normal_profiles]
        )

        shifts[trait] = {
            'crisis_mean': crisis_mean,
            'normal_mean': normal_mean,
            'shift_magnitude': abs(shift_magnitude),
            'direction': shift_direction,
            'statistically_significant': p_value < 0.05,
            'interpretation': interpret_crisis_shift(trait, shift_direction)
        }

    return shifts

def interpret_crisis_shift(trait, direction):
    """Provide contextual interpretation of personality shifts during crisis."""
    interpretations = {
        ('neuroticism', 'INCREASE'): 'Expected stress response',
        ('neuroticism', 'DECREASE'): 'Possible emotional numbing or avoidance',
        ('conscientiousness', 'INCREASE'): 'Adaptive heightened vigilance',
        ('conscientiousness', 'DECREASE'): 'Potential burnout or overwhelm',
        ('agreeableness', 'DECREASE'): 'Conflict escalation under pressure'
    }
    return interpretations.get((trait, direction), 'Requires further analysis')
```

**Step 7.3: Stress Accumulation Modeling**
```python
def model_stress_accumulation(speaker_id, historical_stress_indicators):
    """Model cumulative stress over time using exponential decay."""

    # Stress accumulation with decay (recent stress weighs more)
    decay_rate = 0.05  # Daily decay rate

    cumulative_stress = 0
    stress_timeline = []

    for timestamp, stress_score in sorted(historical_stress_indicators):
        # Decay previous stress
        days_since_last = (timestamp - stress_timeline[-1]['timestamp']).days if stress_timeline else 0
        cumulative_stress *= np.exp(-decay_rate * days_since_last)

        # Add current stress
        cumulative_stress += stress_score

        stress_timeline.append({
            'timestamp': timestamp,
            'cumulative_stress': cumulative_stress,
            'instant_stress': stress_score
        })

    # Forecast future stress (assuming current rate continues)
    current_rate = (stress_timeline[-1]['cumulative_stress'] -
                    stress_timeline[-7]['cumulative_stress']) / 7  # Weekly rate

    forecast_30d = cumulative_stress + current_rate * 30

    return {
        'current_cumulative_stress': cumulative_stress,
        'trend': 'INCREASING' if current_rate > 0 else 'DECREASING',
        'forecast_30d': forecast_30d,
        'risk_level': 'HIGH' if forecast_30d > 0.70 else 'MEDIUM' if forecast_30d > 0.50 else 'LOW'
    }
```

### Outputs
```json
{
  "speaker_id": "ANON_A3F2",
  "temporal_analysis": {
    "data_span": {
      "first_profile": "2024-06-15",
      "last_profile": "2025-11-26",
      "total_profiles": 47
    },
    "personality_evolution": {
      "neuroticism": {
        "current_score": 0.68,
        "baseline": 0.42,
        "deviation_z": 2.3,
        "trend": "INCREASING",
        "stability": 0.65,
        "alert": true,
        "interpretation": "Significant stress accumulation detected"
      },
      "conscientiousness": {
        "current_score": 0.88,
        "baseline": 0.85,
        "deviation_z": 0.4,
        "trend": "STABLE",
        "stability": 0.92,
        "alert": false
      }
    },
    "crisis_related_shifts": {
      "last_crisis_period": "2025-09-10 to 2025-09-25",
      "neuroticism": {
        "crisis_mean": 0.71,
        "normal_mean": 0.41,
        "shift_magnitude": 0.30,
        "direction": "INCREASE",
        "statistically_significant": true,
        "interpretation": "Expected stress response"
      }
    },
    "stress_accumulation": {
      "current_cumulative_stress": 0.65,
      "trend": "INCREASING",
      "forecast_30d": 0.73,
      "risk_level": "HIGH",
      "recommendation": "Intervention recommended (stress mitigation)"
    }
  }
}
```

### Quality Checks
- Minimum 10 historical profiles for trend analysis
- Control for context (crisis vs. normal periods)
- Statistical significance testing for shifts

---

## AGENT 8: Confidence Scorer

### Role
Assess reliability of all psychometric extractions and flag low-confidence results.

### Inputs
- All entity extractions (from Agents 2-6)
- Data quality metadata (word count, speaker identification confidence)
- Ground truth validations (when available)

### Processing Steps

**Step 8.1: Entity-Level Confidence Scoring**
```python
def score_entity_confidence(entity, utterance_context):
    """Calculate confidence score for individual psychometric entity."""

    confidence_factors = {}

    # Factor 1: Linguistic evidence strength
    marker_count = len(entity['evidence'])
    confidence_factors['evidence_strength'] = min(marker_count / 3, 1.0)  # Saturates at 3+ markers

    # Factor 2: Context appropriateness
    if entity_appropriate_for_context(entity, utterance_context):
        confidence_factors['context_match'] = 1.0
    else:
        confidence_factors['context_match'] = 0.5

    # Factor 3: Inter-annotator agreement (if multi-model ensemble)
    if hasattr(entity, 'model_agreement'):
        confidence_factors['model_agreement'] = entity['model_agreement']
    else:
        confidence_factors['model_agreement'] = 0.80  # Default assumption

    # Factor 4: Utterance quality
    utterance_quality = assess_utterance_quality(utterance_context)
    confidence_factors['utterance_quality'] = utterance_quality

    # Weighted combination
    weights = {
        'evidence_strength': 0.30,
        'context_match': 0.25,
        'model_agreement': 0.25,
        'utterance_quality': 0.20
    }

    confidence = sum(
        confidence_factors[factor] * weights[factor]
        for factor in weights
    )

    return confidence

def assess_utterance_quality(utterance_context):
    """Evaluate quality of utterance for reliable extraction."""
    quality_score = 1.0

    # Penalize very short utterances
    if len(utterance_context.split()) < 10:
        quality_score *= 0.60

    # Penalize high disfluency
    if utterance_context.count('um') + utterance_context.count('uh') > 3:
        quality_score *= 0.80

    # Reward complete sentences
    if utterance_context.endswith(('.', '!', '?')):
        quality_score *= 1.05

    return min(quality_score, 1.0)
```

**Step 8.2: Speaker-Level Confidence Aggregation**
```python
def aggregate_speaker_confidence(speaker_profile):
    """Aggregate confidence across all traits for a speaker."""

    trait_confidences = []

    for trait in speaker_profile['personality_traits']:
        entity_confidences = [
            e['confidence'] for e in speaker_profile['personality_traits'][trait]['evidence']
        ]
        trait_confidence = np.mean(entity_confidences) if entity_confidences else 0.50

        trait_confidences.append(trait_confidence)

    # Overall speaker profile confidence
    overall_confidence = np.mean(trait_confidences)

    # Data sufficiency factor
    word_count = speaker_profile['metadata']['word_count']
    if word_count < 100:
        overall_confidence *= 0.60  # Penalize insufficient data
    elif word_count < 300:
        overall_confidence *= 0.80

    return {
        'overall_confidence': overall_confidence,
        'trait_confidences': {
            trait: trait_confidences[i]
            for i, trait in enumerate(speaker_profile['personality_traits'])
        },
        'reliability_flag': 'HIGH' if overall_confidence > 0.80 else 'MEDIUM' if overall_confidence > 0.60 else 'LOW'
    }
```

**Step 8.3: Validation Against Ground Truth (When Available)**
```python
def validate_against_ground_truth(extracted_profiles, ground_truth_assessments):
    """Compare extractions with validated personality assessments."""

    validation_results = {}

    for speaker_id in extracted_profiles:
        if speaker_id not in ground_truth_assessments:
            validation_results[speaker_id] = {'status': 'NO_GROUND_TRUTH'}
            continue

        extracted = extracted_profiles[speaker_id]
        ground_truth = ground_truth_assessments[speaker_id]

        correlations = {}
        for trait in ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']:
            extracted_score = extracted[trait]['score']
            ground_truth_score = ground_truth[trait]

            # Absolute error
            error = abs(extracted_score - ground_truth_score)

            correlations[trait] = {
                'extracted': extracted_score,
                'ground_truth': ground_truth_score,
                'error': error,
                'within_tolerance': error < 0.15  # ±0.15 tolerance on 0-1 scale
            }

        # Overall validation
        mean_error = np.mean([correlations[t]['error'] for t in correlations])

        validation_results[speaker_id] = {
            'status': 'VALIDATED',
            'mean_error': mean_error,
            'trait_level_validation': correlations,
            'pass': mean_error < 0.15
        }

    return validation_results
```

### Outputs
```json
{
  "confidence_assessment": {
    "speaker_profiles": [
      {
        "speaker_id": "ANON_A3F2",
        "overall_confidence": 0.87,
        "reliability_flag": "HIGH",
        "trait_confidences": {
          "openness": 0.85,
          "conscientiousness": 0.91,
          "extraversion": 0.82,
          "agreeableness": 0.84,
          "neuroticism": 0.89
        },
        "data_sufficiency": {
          "word_count": 1872,
          "sufficient": true
        },
        "validation": {
          "status": "VALIDATED",
          "mean_error": 0.09,
          "pass": true
        }
      },
      {
        "speaker_id": "ANON_B7K9",
        "overall_confidence": 0.68,
        "reliability_flag": "MEDIUM",
        "trait_confidences": {
          "openness": 0.72,
          "conscientiousness": 0.65,
          "extraversion": 0.61,
          "agreeableness": 0.70,
          "neuroticism": 0.71
        },
        "data_sufficiency": {
          "word_count": 421,
          "sufficient": false,
          "recommendation": "Collect additional data"
        },
        "validation": {
          "status": "NO_GROUND_TRUTH"
        }
      }
    ],
    "overall_transcript_confidence": 0.78,
    "quality_gates_passed": true
  }
}
```

### Quality Checks
- Minimum confidence threshold (0.60) for profile usage
- Flag profiles requiring additional data collection
- Continuous learning from validated cases

---

## AGENT 9: Neo4j Psychometric Profile Builder

### Role
Structure all extracted psychometric data into Neo4j graph database for AEON integration.

### Inputs
- All agent outputs (Agents 1-8)
- Neo4j connection credentials
- AEON schema definitions

### Processing Steps

**Step 9.1: Person Node Creation/Update**
```cypher
// Create or update person node
MERGE (p:Person {anonymized_id: $anonymized_id})
ON CREATE SET
  p.first_observed = datetime(),
  p.data_source = 'NER11_TRANSCRIPT_EXTRACTION'
ON MATCH SET
  p.last_updated = datetime()

RETURN p
```

**Step 9.2: Psychometric Profile Node Creation**
```cypher
// Create psychometric profile snapshot
CREATE (prof:PsychometricProfile {
  profile_id: $profile_id,
  timestamp: datetime($transcript_date),
  data_source: $transcript_source,
  confidence: $overall_confidence
})

// Link to person
MATCH (p:Person {anonymized_id: $anonymized_id})
CREATE (p)-[:HAS_PROFILE {
  temporal_order: $order,
  context: $context  // 'crisis', 'normal', 'planning'
}]->(prof)
```

**Step 9.3: Personality Trait Nodes**
```cypher
// Create Big Five trait nodes
UNWIND $traits AS trait
MERGE (t:PersonalityTrait {
  trait_name: trait.name,
  trait_category: 'BIG_FIVE'
})

MATCH (prof:PsychometricProfile {profile_id: $profile_id})
CREATE (prof)-[:EXHIBITS_TRAIT {
  score: trait.score,
  confidence: trait.confidence,
  evidence_count: trait.evidence_count,
  deviation_from_baseline: trait.z_score
}]->(t)
```

**Step 9.4: Dark Triad Trait Nodes**
```cypher
// Create Dark Triad trait nodes
UNWIND $dark_triad AS trait
MERGE (dt:DarkTriadTrait {
  trait_name: trait.name
})

MATCH (prof:PsychometricProfile {profile_id: $profile_id})
CREATE (prof)-[:EXHIBITS_DARK_TRAIT {
  score: trait.score,
  confidence: trait.confidence,
  risk_level: trait.risk_level
}]->(dt)
```

**Step 9.5: Stress Indicator Nodes**
```cypher
// Create stress indicator nodes
UNWIND $stress_indicators AS stress
CREATE (s:StressIndicator {
  indicator_id: randomUUID(),
  type: stress.type,  // URGENCY, ANXIETY, DEFLECTION, COGNITIVE_LOAD
  intensity: stress.intensity,
  timestamp: datetime(stress.timestamp),
  context: stress.context
})

MATCH (prof:PsychometricProfile {profile_id: $profile_id})
CREATE (prof)-[:EXHIBITS_STRESS {
  confidence: stress.confidence
}]->(s)

// Link stress to utterance evidence
CREATE (s)-[:EVIDENCED_BY {
  utterance: stress.utterance,
  markers: stress.markers
}]->(:Evidence {text: stress.utterance})
```

**Step 9.6: Cognitive Bias Nodes**
```cypher
// Create cognitive bias nodes
UNWIND $biases AS bias
MERGE (b:CognitiveBias {
  bias_type: bias.type
})

MATCH (prof:PsychometricProfile {profile_id: $profile_id})
CREATE (prof)-[:EXHIBITS_BIAS {
  score: bias.score,
  confidence: bias.confidence,
  risk_assessment: bias.risk_assessment
}]->(b)

// Link to decision context (if applicable)
FOREACH (decision IN bias.decision_contexts |
  MERGE (d:Decision {decision_id: decision.id})
  CREATE (b)-[:INFLUENCED_DECISION {
    impact: decision.bias_impact
  }]->(d)
)
```

**Step 9.7: Group Role Nodes**
```cypher
// Create group role relationships
UNWIND $roles AS role
MERGE (r:GroupRole {
  role_name: role.name
})

MATCH (prof:PsychometricProfile {profile_id: $profile_id})
CREATE (prof)-[:PLAYS_ROLE {
  score: role.score,
  confidence: role.confidence,
  context: role.context,
  frequency: role.frequency
}]->(r)

// Link to group/meeting
MATCH (m:Meeting {meeting_id: $meeting_id})
CREATE (prof)-[:PARTICIPATED_IN]->(m)
```

**Step 9.8: Temporal Evolution Relationships**
```cypher
// Create temporal sequence relationships
MATCH (p:Person {anonymized_id: $anonymized_id})-[:HAS_PROFILE]->(prof:PsychometricProfile)
WITH prof ORDER BY prof.timestamp
WITH collect(prof) AS profiles

UNWIND range(0, size(profiles)-2) AS idx
WITH profiles[idx] AS current, profiles[idx+1] AS next
CREATE (current)-[:PRECEDES {
  time_delta_days: duration.between(current.timestamp, next.timestamp).days
}]->(next)
```

**Step 9.9: Integration with AEON Layers**
```cypher
// Link to AEON Cyber Events (if applicable)
MATCH (prof:PsychometricProfile {profile_id: $profile_id})
MATCH (event:CyberEvent {event_id: $event_id})
WHERE duration.between(event.timestamp, prof.timestamp).days IN range(-7, 7)
CREATE (prof)-[:DURING_EVENT {
  temporal_proximity: 'CONCURRENT'
}]->(event)

// Link to AEON Threat Actors (for threat actor profiling)
MATCH (prof:PsychometricProfile {profile_id: $profile_id})
MATCH (actor:ThreatActor {actor_id: $actor_id})
CREATE (actor)-[:HAS_PSYCHOMETRIC_PROFILE]->(prof)
```

### Outputs
Neo4j graph structure:
```
Person
  ├─[:HAS_PROFILE]→ PsychometricProfile_1 (2024-06-15)
  │   ├─[:EXHIBITS_TRAIT]→ Openness (0.72)
  │   ├─[:EXHIBITS_TRAIT]→ Conscientiousness (0.88)
  │   ├─[:EXHIBITS_STRESS]→ StressIndicator (URGENCY, 0.75)
  │   ├─[:EXHIBITS_BIAS]→ ConfirmationBias (0.68)
  │   ├─[:PLAYS_ROLE]→ LeaderRole (0.88)
  │   └─[:PARTICIPATED_IN]→ Meeting_001
  │
  ├─[:HAS_PROFILE]→ PsychometricProfile_2 (2024-07-20)
  │   └─[:PRECEDES]→ PsychometricProfile_1
  │
  └─[:HAS_PROFILE]→ PsychometricProfile_3 (2025-11-26)
      └─[:PRECEDES]→ PsychometricProfile_2
```

### Quality Checks
- Schema validation (all required fields present)
- Relationship integrity (no orphaned nodes)
- Temporal consistency (profiles ordered correctly)

---

## AGENT 10: Quality Validator

### Role
Final validation of entire pipeline output, ensuring accuracy, completeness, and privacy compliance.

### Inputs
- Neo4j psychometric profiles (from Agent 9)
- Original transcript (from Agent 1)
- Confidence scores (from Agent 8)

### Validation Checks

**Check 1: Data Completeness**
```python
def validate_completeness(profile):
    """Ensure all required fields are present."""
    required_fields = [
        'anonymized_id',
        'personality_traits',
        'stress_indicators',
        'cognitive_biases',
        'group_roles',
        'confidence_scores'
    ]

    missing_fields = [
        field for field in required_fields
        if field not in profile or profile[field] is None
    ]

    return {
        'complete': len(missing_fields) == 0,
        'missing_fields': missing_fields
    }
```

**Check 2: Privacy Compliance**
```python
def validate_privacy_compliance(profile, transcript):
    """Ensure no PII leaked into profile."""

    pii_patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        'name': NER_PERSON_DETECTION  # Use NER model
    }

    violations = []

    # Check profile fields for PII
    profile_text = json.dumps(profile)
    for pii_type, pattern in pii_patterns.items():
        if re.search(pattern, profile_text):
            violations.append({
                'type': pii_type,
                'field': 'profile',
                'severity': 'HIGH'
            })

    # Verify anonymization in transcript
    if 'SPEAKER_00' not in transcript and 'ANON_' not in transcript:
        violations.append({
            'type': 'speaker_identification',
            'field': 'transcript',
            'severity': 'CRITICAL'
        })

    return {
        'compliant': len(violations) == 0,
        'violations': violations
    }
```

**Check 3: Accuracy Validation (Sample-Based)**
```python
def validate_accuracy_sample(profiles, sample_size=10):
    """Manually validate random sample of extractions."""

    sample_profiles = random.sample(profiles, min(sample_size, len(profiles)))

    validation_results = []

    for profile in sample_profiles:
        # Human expert review
        expert_review = request_human_validation(profile)

        accuracy_score = calculate_agreement(
            profile['personality_traits'],
            expert_review['personality_traits']
        )

        validation_results.append({
            'profile_id': profile['profile_id'],
            'accuracy_score': accuracy_score,
            'expert_confidence': expert_review['confidence'],
            'discrepancies': identify_discrepancies(profile, expert_review)
        })

    overall_accuracy = np.mean([r['accuracy_score'] for r in validation_results])

    return {
        'overall_accuracy': overall_accuracy,
        'validation_results': validation_results,
        'pass': overall_accuracy > 0.75
    }
```

**Check 4: Neo4j Graph Integrity**
```cypher
// Check for orphaned nodes
MATCH (n)
WHERE NOT (n)--()
RETURN count(n) AS orphaned_nodes

// Check for missing confidence scores
MATCH (prof:PsychometricProfile)
WHERE NOT EXISTS(prof.confidence)
RETURN count(prof) AS profiles_missing_confidence

// Check for temporal inconsistencies
MATCH (p1:PsychometricProfile)-[:PRECEDES]->(p2:PsychometricProfile)
WHERE p1.timestamp > p2.timestamp
RETURN count(*) AS temporal_inconsistencies
```

### Final Validation Report
```json
{
  "validation_report": {
    "timestamp": "2025-11-26T16:45:00Z",
    "transcript_id": "TRANSCRIPT_20251126_001",
    "checks_performed": 4,
    "checks_passed": 4,
    "status": "PASS",
    "details": {
      "completeness": {
        "status": "PASS",
        "missing_fields": []
      },
      "privacy_compliance": {
        "status": "PASS",
        "violations": []
      },
      "accuracy_sample": {
        "status": "PASS",
        "overall_accuracy": 0.82,
        "sample_size": 10
      },
      "graph_integrity": {
        "status": "PASS",
        "orphaned_nodes": 0,
        "missing_confidence_scores": 0,
        "temporal_inconsistencies": 0
      }
    },
    "recommendations": [
      "Deploy to production",
      "Monitor accuracy metrics on live data",
      "Schedule quarterly ground truth validation"
    ]
  }
}
```

---

## Swarm Coordination & Execution

### Parallel Execution Strategy
- Agents 2-6 execute in parallel (independent psychometric analyses)
- Agent 7 requires historical data (can start while 2-6 running, complete after)
- Agents 1, 8, 9, 10 execute sequentially (dependencies)

### Error Handling
- Agent failure → log error, continue with available data
- Low confidence → flag profile, do not block pipeline
- Privacy violation → HALT, do not write to Neo4j

### Performance Targets
- Process 100 transcripts/day (batched overnight)
- Average processing time: 3-5 minutes per transcript
- Neo4j write latency: <10 seconds per profile

---

## Deployment & Monitoring

### Production Checklist
- [ ] BERT-based NER11 model trained and validated (F1 ≥ 0.70)
- [ ] Neo4j schema deployed and tested
- [ ] Privacy compliance audited (legal approval)
- [ ] Confidence thresholds calibrated
- [ ] Ground truth validation pipeline established
- [ ] Agent swarm orchestration tested (end-to-end)

### Continuous Monitoring
- Daily accuracy checks (sample-based validation)
- Weekly privacy audits (PII detection scans)
- Monthly model retraining (new transcript data)
- Quarterly ground truth validation studies

---

**End of TASKMASTER: Transcript Psychometric Extraction (NER11)**
**Next Steps:** Deploy 10-agent swarm and begin pilot extraction on 100 test transcripts.
