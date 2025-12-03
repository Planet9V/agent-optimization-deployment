"""
Context Augmentation Module for NER11 Gold Model
=================================================

Addresses the context-dependency issue where the NER11 Gold model (94% F1 score)
requires training-like context to extract entities from short text inputs.

Root Cause:
- Transformer-based NER models learn contextual patterns from training data
- Short inputs like "APT33" or "CVE-2024-1234" lack sufficient context
- Training data consists of longer sentences with domain vocabulary

Solutions Implemented:
1. Context Padding: Add domain-specific context around short inputs
2. Pattern-Based Fallback: Regex patterns for known entity formats
3. Entity Type Hints: Append type hints based on input patterns

Version: 1.0.0
Author: AEON Architecture Team
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class AugmentedEntity:
    """Entity extracted via context augmentation or pattern matching."""
    text: str
    label: str
    start: int
    end: int
    confidence: float
    method: str  # 'pattern', 'augmented', 'original'


# ============================================================================
# PATTERN-BASED ENTITY EXTRACTION (FALLBACK)
# ============================================================================

# Regex patterns for known entity formats
ENTITY_PATTERNS = {
    # CVE IDs - e.g., CVE-2024-12345
    'CVE': [
        (r'\bCVE-\d{4}-\d{4,7}\b', 1.0),
    ],

    # CWE IDs - e.g., CWE-79, CWE-1234
    'CWE': [
        (r'\bCWE-\d{1,4}\b', 1.0),
    ],

    # APT Groups - APT29, APT-33, APT 28
    'APT_GROUP': [
        (r'\bAPT[-\s]?\d{1,3}\b', 0.95),
        (r'\b(?:Fancy Bear|Cozy Bear|Lazarus|Kimsuky|Charming Kitten|OceanLotus|APT29|APT28|APT33|APT38|APT41)\b', 0.9),
    ],

    # MITRE ATT&CK Techniques - T1566, T1566.001
    'TECHNIQUE': [
        (r'\bT\d{4}(?:\.\d{3})?\b', 1.0),
    ],

    # MITRE ATT&CK Tactics - TA0001
    'TACTIC': [
        (r'\bTA\d{4}\b', 1.0),
    ],

    # Malware families (common names)
    'MALWARE': [
        (r'\b(?:Cobalt Strike|Emotet|TrickBot|Mimikatz|BloodHound|Ryuk|WannaCry|NotPetya|Petya|DarkSide|REvil|Conti|LockBit|BlackCat|ALPHV)\b', 0.9),
    ],

    # IEC 62443 references - SR/FR/RE/CR patterns
    'IEC_62443': [
        (r'\b(?:SR|FR|RE|CR)[-\s]?\d{1,2}(?:\.\d{1,2})?\b', 0.85),
        (r'\bIEC\s*62443[-\s]*\d[-\s]*\d\b', 0.95),
        (r'\bSL[-\s]?[1-4]\b', 0.8),  # Security Levels
    ],

    # MITRE EMB3D - TID/MIT patterns
    'MITRE_EM3D': [
        (r'\bTID-\d{3,4}\b', 1.0),
        (r'\bMIT-\d{3,4}\b', 1.0),
    ],

    # Threat actors (named groups)
    'THREAT_ACTOR': [
        (r'\b(?:Sandworm|Turla|Equation Group|Shadow Brokers|FIN7|FIN11|Carbanak|Silence|TA505|Gamaredon|Mustang Panda|Stone Panda|Evil Corp)\b', 0.9),
    ],

    # Operating systems
    'OPERATING_SYSTEM': [
        (r'\b(?:Windows\s*(?:10|11|Server\s*20\d{2})?|Linux|Ubuntu|CentOS|RHEL|macOS|iOS|Android)\b', 0.85),
    ],

    # Protocols
    'PROTOCOL': [
        (r'\b(?:Modbus|OPC[-\s]?UA|DNP3|IEC\s*104|S7comm|EtherNet/IP|PROFINET|BACnet)\b', 0.9),
        (r'\b(?:HTTP|HTTPS|SSH|RDP|SMB|FTP|SFTP|DNS|NTP|SNMP|LDAP|Kerberos)\b', 0.85),
    ],

    # Indicators (IPs, hashes, domains - careful extraction)
    'INDICATOR': [
        # IPv4
        (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 0.7),
        # MD5
        (r'\b[a-fA-F0-9]{32}\b', 0.75),
        # SHA1
        (r'\b[a-fA-F0-9]{40}\b', 0.8),
        # SHA256
        (r'\b[a-fA-F0-9]{64}\b', 0.85),
    ],
}


def extract_pattern_entities(text: str) -> List[AugmentedEntity]:
    """
    Extract entities using regex patterns (fallback for short text).

    Args:
        text: Input text to process

    Returns:
        List of AugmentedEntity objects
    """
    entities = []
    seen_spans = set()

    for label, patterns in ENTITY_PATTERNS.items():
        for pattern, confidence in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                span = (match.start(), match.end())
                if span not in seen_spans:
                    seen_spans.add(span)
                    entities.append(AugmentedEntity(
                        text=match.group(),
                        label=label,
                        start=match.start(),
                        end=match.end(),
                        confidence=confidence,
                        method='pattern'
                    ))

    return entities


# ============================================================================
# CONTEXT AUGMENTATION
# ============================================================================

# Domain-specific context templates for different entity types
CONTEXT_TEMPLATES = {
    # APT group context (based on training data patterns)
    'apt': """
In recent cybersecurity intelligence reports, threat actors have been conducting sophisticated
cyber espionage operations targeting critical infrastructure. The analysis indicates that
{input} has been attributed to state-sponsored campaigns involving advanced persistent threats.
Security researchers have documented their tactics, techniques, and procedures (TTPs).
""",

    # CVE/vulnerability context
    'cve': """
A critical vulnerability assessment revealed significant security weaknesses in enterprise systems.
The Common Vulnerabilities and Exposures database documents {input} as a notable security flaw
requiring immediate remediation. The vulnerability impacts multiple software components and
has been assigned a high severity score based on exploitability metrics.
""",

    # Malware context
    'malware': """
Threat intelligence teams have identified malicious software being deployed in targeted attacks.
Analysis of the malware sample {input} revealed sophisticated capabilities including persistence
mechanisms, command-and-control communication, and data exfiltration functionality.
The malware family has been linked to multiple cybercrime campaigns.
""",

    # Technique context
    'technique': """
The MITRE ATT&CK framework documents adversary tactics, techniques, and procedures.
Security teams have observed the technique {input} being employed in real-world attacks.
This technique involves specific methods that adversaries use to achieve their objectives
during the cyber kill chain phases from initial access through to impact.
""",

    # ICS/OT context
    'ics': """
Industrial control systems and operational technology environments face unique cybersecurity
challenges. The analysis of {input} reveals implications for SCADA systems, PLCs, and
industrial protocols. IEC 62443 security requirements address protection mechanisms for
manufacturing, energy, and critical infrastructure sectors.
""",

    # Generic cybersecurity context
    'generic': """
Cybersecurity analysts have documented threat actors, vulnerabilities, and attack methodologies
impacting organizations globally. The subject of analysis {input} relates to documented
security incidents, threat intelligence, and defensive recommendations. Security operations
centers monitor for indicators of compromise associated with these threats.
""",
}


def detect_input_type(text: str) -> str:
    """
    Detect the type of input to select appropriate context template.

    Args:
        text: Input text

    Returns:
        Context template key ('apt', 'cve', 'malware', 'technique', 'ics', 'generic')
    """
    text_lower = text.lower()

    # APT/threat actor patterns
    if re.search(r'\bapt[-\s]?\d', text_lower) or any(ta in text_lower for ta in
        ['fancy bear', 'cozy bear', 'lazarus', 'kimsuky', 'turla', 'sandworm']):
        return 'apt'

    # CVE/vulnerability patterns
    if re.search(r'\bcve-\d{4}', text_lower) or 'vulnerability' in text_lower:
        return 'cve'

    # Malware patterns
    if any(mw in text_lower for mw in
        ['cobalt strike', 'emotet', 'trickbot', 'ransomware', 'malware', 'trojan']):
        return 'malware'

    # Technique patterns
    if re.search(r'\bt\d{4}', text_lower) or 'technique' in text_lower:
        return 'technique'

    # ICS/OT patterns
    if any(ics in text_lower for ics in
        ['scada', 'plc', 'ics', 'ot ', 'modbus', 'opc', 'iec 62443', 'dnp3']):
        return 'ics'

    return 'generic'


def augment_short_text(text: str, min_length: int = 50) -> Tuple[str, int, int]:
    """
    Augment short text with domain-specific context to improve NER extraction.

    Args:
        text: Original input text
        min_length: Minimum character length to trigger augmentation

    Returns:
        Tuple of (augmented_text, original_start, original_end)
        - augmented_text: Text with context padding
        - original_start: Start position of original text in augmented output
        - original_end: End position of original text in augmented output
    """
    # Only augment short text
    if len(text) >= min_length:
        return text, 0, len(text)

    # Detect input type and select template
    input_type = detect_input_type(text)
    template = CONTEXT_TEMPLATES.get(input_type, CONTEXT_TEMPLATES['generic'])

    # Build augmented text
    augmented = template.format(input=text)

    # Find where the original input appears in the augmented text
    original_start = augmented.find(text)
    original_end = original_start + len(text)

    return augmented, original_start, original_end


def adjust_entity_positions(
    entities: List[Dict],
    original_start: int,
    original_end: int,
    original_text: str
) -> List[Dict]:
    """
    Adjust entity positions back to original text coordinates.

    Filters entities to only those that appear in the original text segment
    and adjusts their positions accordingly.

    Args:
        entities: Entities extracted from augmented text
        original_start: Start of original text in augmented output
        original_end: End of original text in augmented output
        original_text: The original input text

    Returns:
        List of entities with adjusted positions (only from original text region)
    """
    adjusted = []

    for ent in entities:
        ent_start = ent.get('start', 0)
        ent_end = ent.get('end', 0)

        # Check if entity falls within original text region
        if ent_start >= original_start and ent_end <= original_end:
            # Adjust coordinates to original text
            adjusted.append({
                **ent,
                'start': ent_start - original_start,
                'end': ent_end - original_start,
            })

    return adjusted


# ============================================================================
# COMBINED EXTRACTION
# ============================================================================

def extract_with_augmentation(
    text: str,
    nlp_model,
    use_patterns: bool = True,
    use_augmentation: bool = True,
    min_augment_length: int = 50
) -> List[Dict]:
    """
    Extract entities using combined approach:
    1. Pattern-based extraction (high-confidence for known formats)
    2. Context augmentation for short text
    3. Standard NER model extraction

    Args:
        text: Input text
        nlp_model: spaCy NLP model
        use_patterns: Enable pattern-based fallback
        use_augmentation: Enable context augmentation
        min_augment_length: Minimum length to trigger augmentation

    Returns:
        List of entity dictionaries with text, label, start, end, confidence, method
    """
    all_entities = []
    seen_spans = set()

    # Step 1: Pattern-based extraction (always reliable)
    if use_patterns:
        pattern_entities = extract_pattern_entities(text)
        for ent in pattern_entities:
            span_key = (ent.start, ent.end, ent.label)
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                all_entities.append({
                    'text': ent.text,
                    'label': ent.label,
                    'start': ent.start,
                    'end': ent.end,
                    'confidence': ent.confidence,
                    'method': 'pattern'
                })

    # Step 2: NER model extraction (with augmentation if needed)
    if nlp_model:
        is_short = len(text) < min_augment_length

        if is_short and use_augmentation:
            # Augment short text
            augmented_text, orig_start, orig_end = augment_short_text(text, min_augment_length)
            doc = nlp_model(augmented_text)

            # Extract and adjust positions
            model_entities = [
                {'text': ent.text, 'label': ent.label_, 'start': ent.start_char, 'end': ent.end_char}
                for ent in doc.ents
            ]
            model_entities = adjust_entity_positions(model_entities, orig_start, orig_end, text)

            for ent in model_entities:
                span_key = (ent['start'], ent['end'], ent['label'])
                if span_key not in seen_spans:
                    seen_spans.add(span_key)
                    all_entities.append({
                        **ent,
                        'confidence': 0.85,  # Slightly lower for augmented
                        'method': 'augmented'
                    })
        else:
            # Standard extraction
            doc = nlp_model(text)
            for ent in doc.ents:
                span_key = (ent.start_char, ent.end_char, ent.label_)
                if span_key not in seen_spans:
                    seen_spans.add(span_key)
                    all_entities.append({
                        'text': ent.text,
                        'label': ent.label_,
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'confidence': 0.95,
                        'method': 'model'
                    })

    # Sort by position
    all_entities.sort(key=lambda x: x['start'])

    return all_entities


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Test pattern extraction
    test_cases = [
        "APT29",
        "CVE-2024-12345",
        "APT33 launched attacks using Cobalt Strike",
        "T1566.001 phishing technique",
        "CWE-79 XSS vulnerability",
        "IEC 62443-3-3 SR 1.1",
    ]

    print("=" * 60)
    print("PATTERN-BASED EXTRACTION TEST")
    print("=" * 60)

    for test in test_cases:
        entities = extract_pattern_entities(test)
        print(f"\nInput: '{test}'")
        if entities:
            for ent in entities:
                print(f"  → {ent.text} ({ent.label}) [confidence: {ent.confidence}]")
        else:
            print("  → No entities found")

    print("\n" + "=" * 60)
    print("CONTEXT AUGMENTATION TEST")
    print("=" * 60)

    for test in test_cases[:3]:
        aug_text, start, end = augment_short_text(test)
        print(f"\nInput: '{test}'")
        print(f"Type: {detect_input_type(test)}")
        print(f"Augmented length: {len(aug_text)} chars")
        print(f"Original position: [{start}:{end}]")
