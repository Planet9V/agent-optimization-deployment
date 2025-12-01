#!/usr/bin/env python3
"""
Pre-annotation script for Batch 1: 25 Cognitive Bias files
Extracts 8 psychological entity types with confidence scoring
"""

import json
import re
import os
from pathlib import Path
from typing import List, Dict, Tuple
import spacy

# Load spaCy model for basic NER and context
nlp = spacy.load("en_core_web_lg")

# Entity type patterns based on Phase 1 research
ENTITY_PATTERNS = {
    "COGNITIVE_BIAS": {
        "keywords": [
            "availability heuristic", "confirmation bias", "normalcy bias", "anchoring bias",
            "hindsight bias", "ingroup bias", "base rate fallacy", "sunk cost fallacy",
            "framing effect", "status quo bias", "representativeness heuristic",
            "overconfidence bias", "attentional bias", "authority bias", "bandwagon effect",
            "change blindness", "cocktail party effect", "conjunction fallacy", "cryptomnesia"
        ],
        "context_words": ["bias", "heuristic", "fallacy", "cognitive error", "mental shortcut"]
    },
    "EMOTION": {
        "keywords": [
            "anxiety", "panic", "denial", "complacency", "confidence", "fear", "anger",
            "frustration", "stress", "worry", "concern", "alarm", "calm", "relief",
            "overconfidence", "underconfidence", "paranoia", "apathy", "skepticism"
        ],
        "context_words": ["feel", "emotion", "emotional", "psychological state", "mindset"]
    },
    "THREAT_PERCEPTION": {
        "real": ["actual threat", "real danger", "physical breach", "active attack", "verified threat"],
        "imaginary": ["perceived threat", "phantom risk", "imagined danger", "false alarm", "exaggerated risk"],
        "symbolic": ["policy violation", "compliance failure", "cultural norm", "authority challenge"]
    },
    "DEFENSE_MECHANISM": {
        "keywords": [
            "denial", "projection", "rationalization", "displacement", "intellectualization",
            "reaction formation", "compartmentalization", "minimization", "blame shifting",
            "excuse making", "justification", "avoidance", "repression"
        ],
        "context_words": ["cope", "defend", "protect self", "psychological defense"]
    },
    "SECURITY_CULTURE": {
        "keywords": [
            "risk-aware", "security-conscious", "compliant", "innovative", "legacy-bound",
            "reactive", "proactive", "security mindset", "organizational culture",
            "security posture", "risk appetite", "threat awareness"
        ],
        "context_words": ["culture", "organizational", "team approach", "company mindset"]
    },
    "BEHAVIORAL_INDICATOR": {
        "keywords": [
            "hesitation", "confidence", "contradiction", "conviction", "certainty",
            "doubt", "resistance", "acceptance", "compliance", "defiance",
            "pattern", "habit", "routine", "deviation", "anomaly"
        ],
        "context_words": ["behavior", "action", "response", "reaction", "conduct"]
    },
    "COMMUNICATION_PATTERN": {
        "keywords": [
            "transparent", "hidden", "exaggerated", "minimized", "clear", "ambiguous",
            "direct", "indirect", "open", "closed", "honest", "deceptive",
            "overcommunicate", "undercommunicate", "withhold information"
        ],
        "context_words": ["communication", "reporting", "disclosure", "message", "information sharing"]
    },
    "LACANIAN_AXIS": {
        "real": ["material breach", "actual loss", "physical damage", "concrete threat"],
        "imaginary": ["reputation risk", "perceived weakness", "image threat", "ego threat"],
        "symbolic": ["policy breach", "authority challenge", "norm violation", "compliance failure"]
    }
}

# Confidence scoring rules
def calculate_confidence(match_type: str, context_strength: int, entity_clarity: int) -> float:
    """Calculate confidence score (0.0-1.0) based on match quality"""
    base_scores = {
        "exact_keyword": 0.90,
        "partial_keyword": 0.75,
        "context_match": 0.65,
        "pattern_match": 0.70
    }

    confidence = base_scores.get(match_type, 0.60)

    # Adjust based on context strength (0-10)
    confidence += (context_strength / 100)

    # Adjust based on entity clarity (0-10)
    confidence += (entity_clarity / 100)

    return min(1.0, max(0.0, confidence))


def extract_entities(text: str, filename: str) -> List[Dict]:
    """Extract all 8 entity types from text with confidence scores"""
    entities = []
    doc = nlp(text)

    # 1. COGNITIVE_BIAS extraction
    for bias in ENTITY_PATTERNS["COGNITIVE_BIAS"]["keywords"]:
        pattern = re.compile(rf'\b{re.escape(bias)}\b', re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = match.span()
            # Check context
            context = text[max(0, start-50):min(len(text), end+50)]
            context_strength = sum(1 for word in ENTITY_PATTERNS["COGNITIVE_BIAS"]["context_words"]
                                  if word in context.lower())

            entities.append({
                "start": start,
                "end": end,
                "label": "COGNITIVE_BIAS",
                "type": bias,
                "text": match.group(),
                "confidence": calculate_confidence("exact_keyword", context_strength * 2, 8)
            })

    # 2. EMOTION extraction
    for emotion in ENTITY_PATTERNS["EMOTION"]["keywords"]:
        pattern = re.compile(rf'\b{re.escape(emotion)}\b', re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = match.span()
            context = text[max(0, start-50):min(len(text), end+50)]
            context_strength = sum(1 for word in ENTITY_PATTERNS["EMOTION"]["context_words"]
                                  if word in context.lower())

            entities.append({
                "start": start,
                "end": end,
                "label": "EMOTION",
                "type": emotion,
                "text": match.group(),
                "confidence": calculate_confidence("exact_keyword", context_strength * 2, 7)
            })

    # 3. THREAT_PERCEPTION extraction (Lacanian framework)
    for perception_type, keywords in ENTITY_PATTERNS["THREAT_PERCEPTION"].items():
        for keyword in keywords:
            pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                start, end = match.span()
                entities.append({
                    "start": start,
                    "end": end,
                    "label": "THREAT_PERCEPTION",
                    "type": perception_type,
                    "text": match.group(),
                    "confidence": calculate_confidence("exact_keyword", 5, 7)
                })

    # 4. DEFENSE_MECHANISM extraction
    for mechanism in ENTITY_PATTERNS["DEFENSE_MECHANISM"]["keywords"]:
        pattern = re.compile(rf'\b{re.escape(mechanism)}\b', re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = match.span()
            context = text[max(0, start-50):min(len(text), end+50)]
            context_strength = sum(1 for word in ENTITY_PATTERNS["DEFENSE_MECHANISM"]["context_words"]
                                  if word in context.lower())

            entities.append({
                "start": start,
                "end": end,
                "label": "DEFENSE_MECHANISM",
                "type": mechanism,
                "text": match.group(),
                "confidence": calculate_confidence("exact_keyword", context_strength * 2, 6)
            })

    # 5. SECURITY_CULTURE extraction
    for culture in ENTITY_PATTERNS["SECURITY_CULTURE"]["keywords"]:
        pattern = re.compile(rf'\b{re.escape(culture)}\b', re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = match.span()
            context = text[max(0, start-50):min(len(text), end+50)]
            context_strength = sum(1 for word in ENTITY_PATTERNS["SECURITY_CULTURE"]["context_words"]
                                  if word in context.lower())

            entities.append({
                "start": start,
                "end": end,
                "label": "SECURITY_CULTURE",
                "type": culture,
                "text": match.group(),
                "confidence": calculate_confidence("exact_keyword", context_strength * 2, 7)
            })

    # 6. BEHAVIORAL_INDICATOR extraction
    for indicator in ENTITY_PATTERNS["BEHAVIORAL_INDICATOR"]["keywords"]:
        pattern = re.compile(rf'\b{re.escape(indicator)}\b', re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = match.span()
            context = text[max(0, start-50):min(len(text), end+50)]
            context_strength = sum(1 for word in ENTITY_PATTERNS["BEHAVIORAL_INDICATOR"]["context_words"]
                                  if word in context.lower())

            entities.append({
                "start": start,
                "end": end,
                "label": "BEHAVIORAL_INDICATOR",
                "type": indicator,
                "text": match.group(),
                "confidence": calculate_confidence("exact_keyword", context_strength * 2, 6)
            })

    # 7. COMMUNICATION_PATTERN extraction
    for pattern_type in ENTITY_PATTERNS["COMMUNICATION_PATTERN"]["keywords"]:
        pattern = re.compile(rf'\b{re.escape(pattern_type)}\b', re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = match.span()
            context = text[max(0, start-50):min(len(text), end+50)]
            context_strength = sum(1 for word in ENTITY_PATTERNS["COMMUNICATION_PATTERN"]["context_words"]
                                  if word in context.lower())

            entities.append({
                "start": start,
                "end": end,
                "label": "COMMUNICATION_PATTERN",
                "type": pattern_type,
                "text": match.group(),
                "confidence": calculate_confidence("exact_keyword", context_strength * 2, 6)
            })

    # 8. LACANIAN_AXIS extraction (specific framework)
    for axis_type, keywords in ENTITY_PATTERNS["LACANIAN_AXIS"].items():
        for keyword in keywords:
            pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                start, end = match.span()
                entities.append({
                    "start": start,
                    "end": end,
                    "label": "LACANIAN_AXIS",
                    "type": axis_type,
                    "text": match.group(),
                    "confidence": calculate_confidence("exact_keyword", 6, 8)
                })

    # Remove duplicate spans (keep highest confidence)
    entities = remove_duplicate_spans(entities)

    return entities


def remove_duplicate_spans(entities: List[Dict]) -> List[Dict]:
    """Remove overlapping spans, keeping highest confidence"""
    if not entities:
        return []

    # Sort by start position, then by confidence (descending)
    sorted_entities = sorted(entities, key=lambda x: (x['start'], -x['confidence']))

    filtered = []
    last_end = -1

    for entity in sorted_entities:
        if entity['start'] >= last_end:
            filtered.append(entity)
            last_end = entity['end']

    return filtered


def process_file(filepath: Path) -> Dict:
    """Process a single file and return Prodigy JSONL entry"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    entities = extract_entities(text, filepath.name)

    # Convert to Prodigy format
    spans = [{
        "start": e["start"],
        "end": e["end"],
        "label": e["label"],
        "type": e["type"],
        "confidence": e["confidence"]
    } for e in entities]

    # Flag low-confidence entities for human review
    low_confidence_count = sum(1 for s in spans if s["confidence"] < 0.70)

    return {
        "text": text,
        "spans": spans,
        "meta": {
            "file": filepath.name,
            "batch": 1,
            "entity_count": len(spans),
            "low_confidence_count": low_confidence_count,
            "needs_review": low_confidence_count > 0
        }
    }


def main():
    # Setup paths
    input_dir = Path("/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cognitive_Biases")
    output_file = Path("/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/15_NER10_Approach/annotation/batch1_preannotated.jsonl")

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Get first 25 .md files (excluding COMPLETION_REPORT.md)
    md_files = sorted([f for f in input_dir.glob("*.md") if f.name != "COMPLETION_REPORT.md"])[:25]

    print(f"Processing {len(md_files)} files...")

    total_entities = 0
    total_low_confidence = 0

    # Process each file and write to JSONL
    with open(output_file, 'w', encoding='utf-8') as out:
        for i, filepath in enumerate(md_files, 1):
            print(f"  [{i:2d}/25] {filepath.name}...", end=" ")

            try:
                entry = process_file(filepath)
                out.write(json.dumps(entry) + "\n")

                total_entities += entry["meta"]["entity_count"]
                total_low_confidence += entry["meta"]["low_confidence_count"]

                print(f"✓ {entry['meta']['entity_count']} entities ({entry['meta']['low_confidence_count']} flagged)")

            except Exception as e:
                print(f"✗ ERROR: {e}")

    # Summary report
    print(f"\n{'='*60}")
    print(f"PRE-ANNOTATION COMPLETE")
    print(f"{'='*60}")
    print(f"Files processed:      {len(md_files)}")
    print(f"Total entities:       {total_entities}")
    print(f"Low confidence:       {total_low_confidence}")
    print(f"Needs review:         {total_low_confidence > 0}")
    print(f"Output file:          {output_file}")
    print(f"{'='*60}")

    # Validation check
    if 550 <= total_entities <= 750:
        print(f"✓ Entity count within target range (550-750)")
    else:
        print(f"⚠ Entity count outside target range: {total_entities}")


if __name__ == "__main__":
    main()
