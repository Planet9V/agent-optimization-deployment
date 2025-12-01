#!/usr/bin/env python3
"""
Relationship Extractor for Cybersecurity Threat Intelligence
Extracts relationships between entities using NLP and pattern matching
"""

import logging
from pathlib import Path
from typing import Dict, List, Tuple, Set
import json
import argparse
from collections import defaultdict
import re

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logging.warning("spaCy not installed. Install with: pip install spacy")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RelationshipExtractor:
    """Extract relationships between entities from cybersecurity documents"""

    # Relationship patterns specific to cybersecurity
    RELATIONSHIP_PATTERNS = {
        'exploits': [
            r'(\w+)\s+exploits?\s+(\w+)',
            r'(\w+)\s+takes? advantage of\s+(\w+)',
            r'(\w+)\s+leverages?\s+(\w+)'
        ],
        'mitigates': [
            r'(\w+)\s+mitigates?\s+(\w+)',
            r'(\w+)\s+prevents?\s+(\w+)',
            r'(\w+)\s+protects? against\s+(\w+)',
            r'(\w+)\s+defends? against\s+(\w+)'
        ],
        'affects': [
            r'(\w+)\s+affects?\s+(\w+)',
            r'(\w+)\s+impacts?\s+(\w+)',
            r'(\w+)\s+compromises?\s+(\w+)',
            r'(\w+)\s+targets?\s+(\w+)'
        ],
        'uses': [
            r'(\w+)\s+uses?\s+(\w+)',
            r'(\w+)\s+employs?\s+(\w+)',
            r'(\w+)\s+utilizes?\s+(\w+)'
        ],
        'causes': [
            r'(\w+)\s+causes?\s+(\w+)',
            r'(\w+)\s+leads? to\s+(\w+)',
            r'(\w+)\s+results? in\s+(\w+)'
        ]
    }

    def __init__(self, model_name: str = 'en_core_web_sm'):
        """
        Initialize relationship extractor

        Args:
            model_name: spaCy model to use
        """
        if not SPACY_AVAILABLE:
            raise ImportError("spaCy is required. Install with: pip install spacy")

        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"Loaded spaCy model: {model_name}")
        except OSError:
            logger.warning(f"Model {model_name} not found. Downloading...")
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', model_name])
            self.nlp = spacy.load(model_name)

        # Compile patterns
        self.compiled_patterns = {}
        for rel_type, patterns in self.RELATIONSHIP_PATTERNS.items():
            self.compiled_patterns[rel_type] = [re.compile(p, re.IGNORECASE) for p in patterns]

    def extract_dependency_relationships(self, text: str) -> List[Dict]:
        """
        Extract relationships using dependency parsing

        Args:
            text: Input text to process

        Returns:
            List of relationship dictionaries
        """
        doc = self.nlp(text)
        relationships = []

        # Build entity map
        entity_map = {ent.text: ent.label_ for ent in doc.ents}

        for sent in doc.sents:
            # Find verb-based relationships
            for token in sent:
                if token.pos_ == 'VERB':
                    # Get subjects and objects
                    subjects = []
                    objects = []

                    for child in token.children:
                        if child.dep_ in ('nsubj', 'nsubjpass'):
                            subjects.append(child)
                        elif child.dep_ in ('dobj', 'pobj', 'attr', 'oprd'):
                            objects.append(child)
                        elif child.dep_ == 'prep':
                            # Check for objects of prepositions
                            for prep_child in child.children:
                                if prep_child.dep_ == 'pobj':
                                    objects.append(prep_child)

                    # Create relationships
                    for subj in subjects:
                        for obj in objects:
                            # Get full noun phrases
                            subj_text = self._get_noun_phrase(subj)
                            obj_text = self._get_noun_phrase(obj)

                            # Calculate confidence based on distance and entity types
                            distance = abs(obj.i - subj.i)
                            confidence = max(0.3, 1.0 - (distance / 20))

                            # Boost confidence if both are named entities
                            if subj_text in entity_map and obj_text in entity_map:
                                confidence = min(1.0, confidence + 0.2)

                            relationships.append({
                                'subject': subj_text,
                                'subject_type': entity_map.get(subj_text, 'UNKNOWN'),
                                'relation': token.lemma_,
                                'object': obj_text,
                                'object_type': entity_map.get(obj_text, 'UNKNOWN'),
                                'sentence': sent.text,
                                'confidence': round(confidence, 2),
                                'method': 'dependency_parsing'
                            })

        return relationships

    def extract_pattern_relationships(self, text: str) -> List[Dict]:
        """
        Extract relationships using pattern matching

        Args:
            text: Input text to process

        Returns:
            List of relationship dictionaries
        """
        relationships = []

        for rel_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(text)

                for match in matches:
                    subject = match.group(1).strip()
                    obj = match.group(2).strip()

                    # Get context (sentence containing the match)
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end]

                    relationships.append({
                        'subject': subject,
                        'relation': rel_type,
                        'object': obj,
                        'context': context,
                        'confidence': 0.8,  # Pattern matches have high confidence
                        'method': 'pattern_matching'
                    })

        return relationships

    def extract_co_occurrence_relationships(self, text: str, window_size: int = 50) -> List[Dict]:
        """
        Extract relationships based on entity co-occurrence

        Args:
            text: Input text to process
            window_size: Character window for co-occurrence

        Returns:
            List of co-occurrence relationships
        """
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]

        relationships = []

        for i, (ent1_text, ent1_type, ent1_start, ent1_end) in enumerate(entities):
            for ent2_text, ent2_type, ent2_start, ent2_end in entities[i+1:]:
                # Check if within window
                distance = ent2_start - ent1_end

                if distance <= window_size:
                    # Calculate confidence based on proximity
                    confidence = max(0.3, 1.0 - (distance / window_size))

                    # Get context
                    context_start = max(0, ent1_start - 50)
                    context_end = min(len(text), ent2_end + 50)
                    context = text[context_start:context_end]

                    relationships.append({
                        'entity1': ent1_text,
                        'entity1_type': ent1_type,
                        'entity2': ent2_text,
                        'entity2_type': ent2_type,
                        'distance': distance,
                        'confidence': round(confidence, 2),
                        'context': context,
                        'method': 'co_occurrence'
                    })
                else:
                    break  # Entities are sorted by position

        return relationships

    def suggest_graph_relationships(self, relationships: List[Dict]) -> List[Dict]:
        """
        Suggest relationships suitable for graph database import

        Args:
            relationships: List of extracted relationships

        Returns:
            List of graph-ready relationship dictionaries
        """
        graph_relationships = []

        for rel in relationships:
            # Convert to graph format
            if 'subject' in rel and 'object' in rel:
                graph_rel = {
                    'from_node': rel['subject'],
                    'from_type': rel.get('subject_type', 'UNKNOWN'),
                    'relationship_type': rel['relation'].upper().replace(' ', '_'),
                    'to_node': rel['object'],
                    'to_type': rel.get('object_type', 'UNKNOWN'),
                    'confidence': rel['confidence'],
                    'source_method': rel['method']
                }
                graph_relationships.append(graph_rel)

            elif 'entity1' in rel and 'entity2' in rel:
                # Co-occurrence relationship
                graph_rel = {
                    'from_node': rel['entity1'],
                    'from_type': rel['entity1_type'],
                    'relationship_type': 'CO_OCCURS_WITH',
                    'to_node': rel['entity2'],
                    'to_type': rel['entity2_type'],
                    'confidence': rel['confidence'],
                    'distance': rel['distance'],
                    'source_method': rel['method']
                }
                graph_relationships.append(graph_rel)

        return graph_relationships

    def extract_all_relationships(self, text: str) -> Dict:
        """
        Extract relationships using all available methods

        Args:
            text: Input text to process

        Returns:
            Dictionary containing all relationship types
        """
        logger.info("Extracting relationships from text...")

        # Extract using different methods
        dependency_rels = self.extract_dependency_relationships(text)
        logger.info(f"Found {len(dependency_rels)} dependency relationships")

        pattern_rels = self.extract_pattern_relationships(text)
        logger.info(f"Found {len(pattern_rels)} pattern relationships")

        co_occurrence_rels = self.extract_co_occurrence_relationships(text)
        logger.info(f"Found {len(co_occurrence_rels)} co-occurrence relationships")

        # Combine all relationships
        all_relationships = dependency_rels + pattern_rels + co_occurrence_rels

        # Generate graph suggestions
        graph_relationships = self.suggest_graph_relationships(all_relationships)
        logger.info(f"Generated {len(graph_relationships)} graph relationships")

        return {
            'dependency_relationships': dependency_rels,
            'pattern_relationships': pattern_rels,
            'co_occurrence_relationships': co_occurrence_rels,
            'graph_relationships': graph_relationships,
            'total_relationships': len(all_relationships)
        }

    def _get_noun_phrase(self, token) -> str:
        """
        Get the full noun phrase for a token

        Args:
            token: spaCy token

        Returns:
            Full noun phrase as string
        """
        # Get all children that are part of the noun phrase
        phrase_tokens = [token]

        for child in token.children:
            if child.dep_ in ('compound', 'amod', 'det', 'poss'):
                phrase_tokens.append(child)

        # Sort by position and join
        phrase_tokens.sort(key=lambda t: t.i)
        return ' '.join([t.text for t in phrase_tokens])


def main():
    """CLI interface for relationship extraction"""
    parser = argparse.ArgumentParser(description='Extract relationships from cybersecurity documents')
    parser.add_argument('input', help='Input text file')
    parser.add_argument('-o', '--output', help='Output JSON file', default='relationships.json')
    parser.add_argument('-m', '--model', help='spaCy model', default='en_core_web_sm')
    parser.add_argument('--window', type=int, help='Co-occurrence window size', default=50)

    args = parser.parse_args()

    # Initialize extractor
    extractor = RelationshipExtractor(model_name=args.model)

    # Read input
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract relationships
    results = extractor.extract_all_relationships(text)

    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Results saved to {args.output}")
    logger.info(f"Total relationships extracted: {results['total_relationships']}")
    logger.info(f"Graph relationships: {len(results['graph_relationships'])}")


if __name__ == '__main__':
    main()
