"""
Relationship Extractor: Automatic relationship detection between entities

Analyzes text to extract relationships between NER entities using:
1. Co-occurrence analysis (entities in same context)
2. Pattern matching (verb phrases indicating relationships)
3. Proximity-based relationships (entities near each other)
4. Semantic relationship inference

File: 07_relationship_extractor.py
Created: 2025-12-02
Version: 1.0.0
Status: PRODUCTION-READY
Author: AEON Architecture Team

Purpose: Extract USES, TARGETS, EXPLOITS, AFFECTS, ATTRIBUTED_TO and other
         relationships automatically from text to build knowledge graph
"""

import re
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass


@dataclass
class ExtractedRelationship:
    """Represents a discovered relationship between two entities."""
    source_entity: str
    source_type: str
    relationship_type: str
    target_entity: str
    target_type: str
    confidence: float
    evidence: str  # Text snippet showing the relationship
    method: str    # How it was detected (pattern, proximity, co-occurrence)


class RelationshipExtractor:
    """
    Extracts relationships between entities from text.

    Methods:
    1. Pattern Matching: "APT29 uses WannaCry" → USES relationship
    2. Proximity: Entities within N words → co-occurrence relationship
    3. Type-based: ThreatActor + Malware in same sentence → likely USES
    4. Verb Phrase Analysis: Extract verb between entities
    """

    def __init__(self):
        """Initialize relationship extractor with patterns."""
        self.relationship_patterns = self._build_relationship_patterns()
        self.proximity_threshold = 50  # characters

    def _build_relationship_patterns(self) -> Dict[str, List[Tuple[re.Pattern, str]]]:
        """
        Build regex patterns for relationship detection.

        Returns dictionary mapping relationship types to (pattern, confidence) tuples.
        """
        patterns = {
            'USES': [
                (re.compile(r'\b(use[sd]?|using|utilized?|employed?|leveraged?|deployed?)\b', re.I), 0.9),
                (re.compile(r'\b(with|via)\b', re.I), 0.7),
            ],

            'TARGETS': [
                (re.compile(r'\b(target(s|ed|ing)?|aimed at|directed at|focused on)\b', re.I), 0.9),
                (re.compile(r'\b(attack(s|ed|ing)?|compromise[sd]?)\b', re.I), 0.85),
                (re.compile(r'\b(affecting|impacting)\b', re.I), 0.75),
            ],

            'EXPLOITS': [
                (re.compile(r'\b(exploit(s|ed|ing)?|leveraged?|took advantage)\b', re.I), 0.95),
                (re.compile(r'\b(abused?|misused?)\b', re.I), 0.85),
            ],

            'AFFECTS': [
                (re.compile(r'\b(affect(s|ed|ing)?|impact(s|ed|ing)?)\b', re.I), 0.9),
                (re.compile(r'\b(vulnerable to|susceptible to)\b', re.I), 0.85),
            ],

            'ATTRIBUTED_TO': [
                (re.compile(r'\b(attributed to|linked to|associated with|tied to)\b', re.I), 0.95),
                (re.compile(r'\b(by|from)\b(?!.*\d)', re.I), 0.7),  # "attack by APT29"
            ],

            'MITIGATES': [
                (re.compile(r'\b(mitigate[sd]?|mitigating|prevent(s|ed|ing)?|protect(s|ed|ing)?)\b', re.I), 0.9),
                (re.compile(r'\b(defend(s|ed|ing)? against|block(s|ed|ing)?)\b', re.I), 0.85),
            ],

            'DETECTS': [
                (re.compile(r'\b(detect(s|ed|ing)?|identified?|discovered?|found)\b', re.I), 0.85),
                (re.compile(r'\b(observed?|noticed?|spotted?)\b', re.I), 0.75),
            ],

            'INDICATES': [
                (re.compile(r'\b(indicate(s|d)?|signal(s|ed)?|suggest(s|ed)?)\b', re.I), 0.85),
                (re.compile(r'\b(show(s|ed)?|reveal(s|ed)?)\b', re.I), 0.75),
            ],
        }

        return patterns

    def extract_relationships_from_text(
        self,
        text: str,
        entities: List[Dict],
        doc_id: str
    ) -> List[ExtractedRelationship]:
        """
        Extract all relationships between entities in text.

        Args:
            text: Full document text
            entities: List of NER entities with positions
            doc_id: Document identifier

        Returns:
            List of ExtractedRelationship objects
        """
        relationships = []

        # Sort entities by position for efficient processing
        sorted_entities = sorted(entities, key=lambda e: e.get('start', 0))

        # Method 1: Pattern-based extraction
        pattern_rels = self._extract_pattern_relationships(text, sorted_entities)
        relationships.extend(pattern_rels)

        # Method 2: Proximity-based (entities near each other)
        proximity_rels = self._extract_proximity_relationships(sorted_entities)
        relationships.extend(proximity_rels)

        # Method 3: Type-based inference
        type_rels = self._infer_type_based_relationships(sorted_entities, text)
        relationships.extend(type_rels)

        # Deduplicate relationships
        unique_rels = self._deduplicate_relationships(relationships)

        return unique_rels

    def _extract_pattern_relationships(
        self,
        text: str,
        entities: List[Dict]
    ) -> List[ExtractedRelationship]:
        """
        Extract relationships using verb phrase patterns.

        Example: "APT29 used WannaCry ransomware"
                 → (APT29, USES, WannaCry)
        """
        relationships = []

        # For each pair of entities
        for i, source in enumerate(entities):
            for target in entities[i+1:i+10]:  # Check next 10 entities
                source_start = source.get('start', 0)
                source_end = source.get('end', 0)
                target_start = target.get('start', 0)
                target_end = target.get('end', 0)

                # Skip if too far apart (>300 chars)
                if target_start - source_end > 300:
                    continue

                # Extract text between entities
                between_text = text[source_end:target_start]

                # Check for relationship patterns
                for rel_type, patterns in self.relationship_patterns.items():
                    for pattern, base_confidence in patterns:
                        if pattern.search(between_text):
                            # Determine if relationship makes sense based on entity types
                            valid, adjusted_confidence = self._validate_relationship_type(
                                source.get('label', ''),
                                target.get('label', ''),
                                rel_type
                            )

                            if valid:
                                relationships.append(ExtractedRelationship(
                                    source_entity=source.get('text', ''),
                                    source_type=source.get('label', ''),
                                    relationship_type=rel_type,
                                    target_entity=target.get('text', ''),
                                    target_type=target.get('label', ''),
                                    confidence=base_confidence * adjusted_confidence,
                                    evidence=text[source_start:target_end],
                                    method='pattern_match'
                                ))
                                break  # Found relationship, stop checking patterns

        return relationships

    def _extract_proximity_relationships(
        self,
        entities: List[Dict]
    ) -> List[ExtractedRelationship]:
        """
        Extract relationships based on entity proximity (co-occurrence).

        Entities within 50 characters likely have a relationship.
        """
        relationships = []

        for i, source in enumerate(entities):
            for target in entities[i+1:i+5]:  # Check next 5 entities
                source_end = source.get('end', 0)
                target_start = target.get('start', 0)
                distance = target_start - source_end

                if 0 < distance < self.proximity_threshold:
                    # Infer relationship type from entity types
                    rel_type = self._infer_relationship_from_types(
                        source.get('label', ''),
                        target.get('label', '')
                    )

                    if rel_type:
                        relationships.append(ExtractedRelationship(
                            source_entity=source.get('text', ''),
                            source_type=source.get('label', ''),
                            relationship_type=rel_type,
                            target_entity=target.get('text', ''),
                            target_type=target.get('label', ''),
                            confidence=0.6,  # Lower confidence for proximity
                            evidence=f"Proximity: {distance} chars apart",
                            method='proximity'
                        ))

        return relationships

    def _infer_type_based_relationships(
        self,
        entities: List[Dict],
        text: str
    ) -> List[ExtractedRelationship]:
        """
        Infer relationships based on entity type combinations.

        Rules:
        - THREAT_ACTOR + MALWARE (same sentence) → USES
        - MALWARE + DEVICE (same sentence) → TARGETS
        - MALWARE + CVE (same sentence) → EXPLOITS
        - CVE + SOFTWARE_COMPONENT → AFFECTS
        """
        relationships = []

        # Group entities by sentence/paragraph
        # Simple heuristic: entities within 200 characters
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                distance = abs(entity2.get('start', 0) - entity1.get('end', 0))

                if distance > 200:
                    continue

                # Check type-based rules
                type1 = entity1.get('label', '')
                type2 = entity2.get('label', '')

                rel_type = None
                confidence = 0.7

                # THREAT_ACTOR → MALWARE
                if type1 == 'THREAT_ACTOR' and type2 == 'MALWARE':
                    rel_type = 'USES'
                    confidence = 0.8

                # MALWARE → DEVICE
                elif type1 == 'MALWARE' and type2 == 'DEVICE':
                    rel_type = 'TARGETS'
                    confidence = 0.75

                # MALWARE → CVE
                elif type1 == 'MALWARE' and type2 == 'CVE':
                    rel_type = 'EXPLOITS'
                    confidence = 0.8

                # CVE → SOFTWARE_COMPONENT
                elif type1 == 'CVE' and type2 == 'SOFTWARE_COMPONENT':
                    rel_type = 'AFFECTS'
                    confidence = 0.85

                # CVE → DEVICE
                elif type1 == 'CVE' and type2 == 'DEVICE':
                    rel_type = 'AFFECTS'
                    confidence = 0.8

                # CONTROLS → VULNERABILITY
                elif type1 == 'CONTROLS' and type2 in ['CVE', 'VULNERABILITY']:
                    rel_type = 'MITIGATES'
                    confidence = 0.8

                # COGNITIVE_BIAS → (incident/event context)
                elif type1 == 'COGNITIVE_BIAS':
                    rel_type = 'CONTRIBUTES_TO'
                    confidence = 0.7

                # DEVICE → PROTOCOL
                elif type1 == 'DEVICE' and type2 == 'PROTOCOL':
                    rel_type = 'USES_PROTOCOL'
                    confidence = 0.75

                if rel_type:
                    # Extract evidence text
                    start = min(entity1.get('start', 0), entity2.get('start', 0))
                    end = max(entity1.get('end', 0), entity2.get('end', 0))
                    evidence = text[start:end] if start < end else ""

                    relationships.append(ExtractedRelationship(
                        source_entity=entity1.get('text', ''),
                        source_type=type1,
                        relationship_type=rel_type,
                        target_entity=entity2.get('text', ''),
                        target_type=type2,
                        confidence=confidence,
                        evidence=evidence[:200],  # Limit evidence length
                        method='type_inference'
                    ))

        return relationships

    def _validate_relationship_type(
        self,
        source_type: str,
        target_type: str,
        rel_type: str
    ) -> Tuple[bool, float]:
        """
        Validate if a relationship type makes sense for given entity types.

        Returns: (is_valid, confidence_multiplier)
        """
        # Define valid relationship combinations
        valid_combinations = {
            'USES': [
                ('THREAT_ACTOR', 'MALWARE'),
                ('THREAT_ACTOR', 'TOOL'),
                ('MALWARE', 'PROTOCOL'),
                ('DEVICE', 'PROTOCOL'),
            ],
            'TARGETS': [
                ('THREAT_ACTOR', 'ORGANIZATION'),
                ('THREAT_ACTOR', 'SECTOR'),
                ('THREAT_ACTOR', 'DEVICE'),
                ('MALWARE', 'DEVICE'),
                ('MALWARE', 'ORGANIZATION'),
                ('ATTACK_TECHNIQUE', 'DEVICE'),
            ],
            'EXPLOITS': [
                ('MALWARE', 'CVE'),
                ('MALWARE', 'VULNERABILITY'),
                ('ATTACK_TECHNIQUE', 'VULNERABILITY'),
                ('THREAT_ACTOR', 'CVE'),
            ],
            'AFFECTS': [
                ('CVE', 'SOFTWARE_COMPONENT'),
                ('CVE', 'DEVICE'),
                ('VULNERABILITY', 'SOFTWARE_COMPONENT'),
                ('VULNERABILITY', 'DEVICE'),
            ],
            'ATTRIBUTED_TO': [
                ('MALWARE', 'THREAT_ACTOR'),
                ('ATTACK_TECHNIQUE', 'THREAT_ACTOR'),
                ('CAMPAIGN', 'THREAT_ACTOR'),
            ],
            'MITIGATES': [
                ('CONTROLS', 'CVE'),
                ('CONTROLS', 'VULNERABILITY'),
                ('CONTROLS', 'ATTACK_TECHNIQUE'),
            ],
        }

        combo = (source_type, target_type)

        if rel_type in valid_combinations:
            if combo in valid_combinations[rel_type]:
                return True, 1.0  # High confidence
            else:
                return False, 0.0  # Invalid combination

        # Default: allow but with lower confidence
        return True, 0.5

    def _infer_relationship_from_types(
        self,
        type1: str,
        type2: str
    ) -> Optional[str]:
        """
        Infer most likely relationship type from entity types alone.
        Used for proximity-based relationships.
        """
        # THREAT_ACTOR + MALWARE → USES
        if type1 == 'THREAT_ACTOR' and type2 == 'MALWARE':
            return 'USES'

        # MALWARE + DEVICE → TARGETS
        if type1 == 'MALWARE' and type2 == 'DEVICE':
            return 'TARGETS'

        # MALWARE + CVE → EXPLOITS
        if type1 == 'MALWARE' and type2 == 'CVE':
            return 'EXPLOITS'

        # CVE + SOFTWARE → AFFECTS
        if type1 == 'CVE' and type2 == 'SOFTWARE_COMPONENT':
            return 'AFFECTS'

        # CONTROLS + CVE → MITIGATES
        if type1 == 'CONTROLS' and type2 in ['CVE', 'VULNERABILITY']:
            return 'MITIGATES'

        # Default: Generic RELATED_TO
        return 'RELATED_TO'

    def _deduplicate_relationships(
        self,
        relationships: List[ExtractedRelationship]
    ) -> List[ExtractedRelationship]:
        """
        Remove duplicate relationships, keeping highest confidence.
        """
        # Key: (source, relationship, target)
        rel_map: Dict[Tuple[str, str, str], ExtractedRelationship] = {}

        for rel in relationships:
            key = (rel.source_entity, rel.relationship_type, rel.target_entity)

            if key not in rel_map or rel.confidence > rel_map[key].confidence:
                rel_map[key] = rel

        return list(rel_map.values())

    def extract_relationships_batch(
        self,
        documents: List[Dict]
    ) -> Dict[str, List[ExtractedRelationship]]:
        """
        Extract relationships from multiple documents.

        Args:
            documents: List of {text: str, entities: List[Dict], doc_id: str}

        Returns:
            Dictionary mapping doc_id to list of relationships
        """
        all_relationships = {}

        for doc in documents:
            relationships = self.extract_relationships_from_text(
                text=doc['text'],
                entities=doc['entities'],
                doc_id=doc.get('doc_id', 'unknown')
            )
            all_relationships[doc['doc_id']] = relationships

        return all_relationships


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def test_relationship_extraction():
    """Test relationship extraction on sample text."""
    extractor = RelationshipExtractor()

    # Sample entities from NER11 output
    entities = [
        {"text": "APT29", "label": "THREAT_ACTOR", "start": 0, "end": 5, "score": 1.0},
        {"text": "WannaCry", "label": "MALWARE", "start": 20, "end": 28, "score": 1.0},
        {"text": "ransomware", "label": "MALWARE", "start": 29, "end": 39, "score": 1.0},
        {"text": "Siemens PLCs", "label": "DEVICE", "start": 60, "end": 72, "score": 1.0},
        {"text": "CVE-2024-12345", "label": "CVE", "start": 100, "end": 114, "score": 1.0},
    ]

    text = "APT29 threat actor used WannaCry ransomware to target Siemens PLCs in energy sector. The attack exploited CVE-2024-12345 vulnerability."

    relationships = extractor.extract_relationships_from_text(text, entities, "test_doc")

    print(f"\n{'='*70}")
    print("RELATIONSHIP EXTRACTION TEST")
    print(f"{'='*70}\n")
    print(f"Extracted {len(relationships)} relationships:\n")

    for i, rel in enumerate(relationships, 1):
        print(f"{i}. {rel.source_entity} ({rel.source_type})")
        print(f"   --[{rel.relationship_type}]-->")
        print(f"   {rel.target_entity} ({rel.target_type})")
        print(f"   Confidence: {rel.confidence:.2f} | Method: {rel.method}")
        print(f"   Evidence: \"{rel.evidence[:80]}...\"")
        print()

    # Expected relationships:
    # 1. APT29 --[USES]--> WannaCry
    # 2. WannaCry --[TARGETS]--> Siemens PLCs
    # 3. WannaCry --[EXPLOITS]--> CVE-2024-12345
    # 4. CVE-2024-12345 --[AFFECTS]--> Siemens PLCs


if __name__ == "__main__":
    test_relationship_extraction()
