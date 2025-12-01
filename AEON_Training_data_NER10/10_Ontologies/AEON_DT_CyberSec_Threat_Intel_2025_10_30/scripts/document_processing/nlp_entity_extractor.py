#!/usr/bin/env python3
"""
NLP Entity Extractor for Cybersecurity Threat Intelligence
Extracts entities using spaCy with custom patterns for CVE, CWE, CAPEC identifiers
"""

import spacy
import re
import logging
from typing import List, Dict, Tuple, Set
from collections import defaultdict
from pathlib import Path
import json
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EntityExtractor:
    """Extract entities from cybersecurity documents using NLP"""

    # Custom patterns for cybersecurity identifiers
    PATTERNS = {
        'CVE': r'CVE-\d{4}-\d{4,7}',
        'CWE': r'CWE-\d{1,5}',
        'CAPEC': r'CAPEC-\d{1,5}',
        'IP_ADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'HASH_MD5': r'\b[a-fA-F0-9]{32}\b',
        'HASH_SHA1': r'\b[a-fA-F0-9]{40}\b',
        'HASH_SHA256': r'\b[a-fA-F0-9]{64}\b',
        'URL': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    }

    def __init__(self, model_name: str = 'en_core_web_sm'):
        """
        Initialize entity extractor

        Args:
            model_name: spaCy model to use (en_core_web_sm, en_core_web_md, en_core_web_lg)
        """
        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"Loaded spaCy model: {model_name}")
        except OSError:
            logger.warning(f"Model {model_name} not found. Downloading...")
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', model_name])
            self.nlp = spacy.load(model_name)

        # Compile regex patterns
        self.compiled_patterns = {
            name: re.compile(pattern)
            for name, pattern in self.PATTERNS.items()
        }

    def extract_entities(self, text: str, include_confidence: bool = True) -> Dict[str, List[Dict]]:
        """
        Extract all entities from text

        Args:
            text: Input text to process
            include_confidence: Include confidence scores

        Returns:
            Dictionary of entity types to lists of entity dictionaries
        """
        entities = defaultdict(list)

        # Extract spaCy entities
        doc = self.nlp(text)

        for ent in doc.ents:
            entity_data = {
                'text': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'label': ent.label_
            }

            if include_confidence:
                # Calculate confidence based on entity length and context
                entity_data['confidence'] = self._calculate_confidence(ent, doc)

            entities[ent.label_].append(entity_data)

        # Extract custom cybersecurity patterns
        for pattern_name, pattern in self.compiled_patterns.items():
            matches = pattern.finditer(text)
            for match in matches:
                entity_data = {
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'label': pattern_name
                }

                if include_confidence:
                    entity_data['confidence'] = 1.0  # Pattern matches have high confidence

                entities[pattern_name].append(entity_data)

        # Deduplicate entities
        entities = self._deduplicate_entities(entities)

        return dict(entities)

    def extract_relationships(self, text: str) -> List[Dict]:
        """
        Extract relationships between entities using dependency parsing

        Args:
            text: Input text to process

        Returns:
            List of relationship dictionaries
        """
        doc = self.nlp(text)
        relationships = []

        # Find entities
        entities = {ent.text: ent.label_ for ent in doc.ents}

        # Parse dependencies to find relationships
        for sent in doc.sents:
            for token in sent:
                # Look for verb relationships connecting entities
                if token.pos_ == 'VERB':
                    subjects = [child for child in token.children if child.dep_ in ('nsubj', 'nsubjpass')]
                    objects = [child for child in token.children if child.dep_ in ('dobj', 'pobj', 'attr')]

                    for subj in subjects:
                        for obj in objects:
                            subj_text = subj.text
                            obj_text = obj.text

                            # Check if subject or object are entities
                            if subj_text in entities or obj_text in entities:
                                relationships.append({
                                    'subject': subj_text,
                                    'subject_type': entities.get(subj_text, 'UNKNOWN'),
                                    'relation': token.lemma_,
                                    'object': obj_text,
                                    'object_type': entities.get(obj_text, 'UNKNOWN'),
                                    'sentence': sent.text,
                                    'confidence': 0.7
                                })

        return relationships

    def extract_co_occurrences(self, text: str, window_size: int = 50) -> List[Dict]:
        """
        Extract entity co-occurrences within a sliding window

        Args:
            text: Input text to process
            window_size: Character window for co-occurrence

        Returns:
            List of co-occurrence dictionaries
        """
        entities = self.extract_entities(text, include_confidence=False)

        # Flatten all entities with positions
        all_entities = []
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                all_entities.append({
                    'text': entity['text'],
                    'type': entity_type,
                    'start': entity['start'],
                    'end': entity['end']
                })

        # Sort by position
        all_entities.sort(key=lambda x: x['start'])

        # Find co-occurrences
        co_occurrences = []
        for i, entity1 in enumerate(all_entities):
            for entity2 in all_entities[i+1:]:
                # Check if within window
                distance = entity2['start'] - entity1['end']
                if distance <= window_size:
                    co_occurrences.append({
                        'entity1': entity1['text'],
                        'entity1_type': entity1['type'],
                        'entity2': entity2['text'],
                        'entity2_type': entity2['type'],
                        'distance': distance,
                        'confidence': max(0.3, 1.0 - (distance / window_size))
                    })
                else:
                    break  # Entities are sorted, so we can break

        return co_occurrences

    def _calculate_confidence(self, entity, doc) -> float:
        """
        Calculate confidence score for an entity

        Args:
            entity: spaCy entity object
            doc: spaCy doc object

        Returns:
            Confidence score between 0 and 1
        """
        confidence = 0.5  # Base confidence

        # Longer entities are more reliable
        if len(entity.text) > 10:
            confidence += 0.2
        elif len(entity.text) > 5:
            confidence += 0.1

        # Entities with proper capitalization
        if entity.text[0].isupper():
            confidence += 0.1

        # Organizations and products are more reliable in technical documents
        if entity.label_ in ('ORG', 'PRODUCT'):
            confidence += 0.2

        return min(1.0, confidence)

    def _deduplicate_entities(self, entities: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """
        Remove duplicate entities

        Args:
            entities: Dictionary of entity lists

        Returns:
            Deduplicated entity dictionary
        """
        deduplicated = defaultdict(list)

        for entity_type, entity_list in entities.items():
            seen = set()
            for entity in entity_list:
                # Create unique key based on text and position
                key = (entity['text'].lower(), entity['start'])
                if key not in seen:
                    seen.add(key)
                    deduplicated[entity_type].append(entity)

        return deduplicated

    def process_batch(self, texts: List[str]) -> List[Dict]:
        """
        Process multiple texts in batch

        Args:
            texts: List of text strings to process

        Returns:
            List of entity extraction results
        """
        results = []

        for i, text in enumerate(texts):
            logger.info(f"Processing document {i+1}/{len(texts)}")
            try:
                entities = self.extract_entities(text)
                relationships = self.extract_relationships(text)
                co_occurrences = self.extract_co_occurrences(text)

                results.append({
                    'document_id': i,
                    'entities': entities,
                    'relationships': relationships,
                    'co_occurrences': co_occurrences,
                    'status': 'success'
                })
            except Exception as e:
                logger.error(f"Error processing document {i}: {e}")
                results.append({
                    'document_id': i,
                    'status': 'error',
                    'error': str(e)
                })

        return results


def main():
    """CLI interface for entity extraction"""
    parser = argparse.ArgumentParser(description='Extract entities from cybersecurity documents')
    parser.add_argument('input', help='Input text file or directory')
    parser.add_argument('-o', '--output', help='Output JSON file', default='entities.json')
    parser.add_argument('-m', '--model', help='spaCy model', default='en_core_web_sm')
    parser.add_argument('--relationships', action='store_true', help='Extract relationships')
    parser.add_argument('--co-occurrences', action='store_true', help='Extract co-occurrences')

    args = parser.parse_args()

    # Initialize extractor
    extractor = EntityExtractor(model_name=args.model)

    # Read input
    input_path = Path(args.input)
    if input_path.is_file():
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Extract entities
        entities = extractor.extract_entities(text)

        result = {'entities': entities}

        if args.relationships:
            result['relationships'] = extractor.extract_relationships(text)

        if args.co_occurrences:
            result['co_occurrences'] = extractor.extract_co_occurrences(text)

        # Save results
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"Results saved to {args.output}")
        logger.info(f"Extracted {sum(len(v) for v in entities.values())} entities")

    elif input_path.is_dir():
        # Process all text files in directory
        texts = []
        for txt_file in input_path.glob('*.txt'):
            with open(txt_file, 'r', encoding='utf-8') as f:
                texts.append(f.read())

        results = extractor.process_batch(texts)

        # Save results
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        logger.info(f"Processed {len(texts)} documents. Results saved to {args.output}")

    else:
        logger.error(f"Invalid input path: {input_path}")


if __name__ == '__main__':
    main()
