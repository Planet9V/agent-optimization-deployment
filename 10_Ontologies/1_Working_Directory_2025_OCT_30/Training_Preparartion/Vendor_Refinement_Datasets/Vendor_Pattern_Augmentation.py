#!/usr/bin/env python3
"""
Vendor Pattern Augmentation for ICS/OT NER Training

Purpose: Improve VENDOR entity recognition from 31.16% F1 to 75%+ by incorporating
comprehensive vendor name variations into training data augmentation patterns.

Usage:
    python Vendor_Pattern_Augmentation.py --input dataset.json --output augmented_dataset.json

Author: Training Data Augmentation System
Date: 2025-11-05
Version: 1.0
"""

import json
import re
import random
from pathlib import Path
from typing import List, Dict, Set, Tuple
import argparse


class VendorPatternAugmenter:
    """
    Augments training data with comprehensive vendor name variations
    to improve NER model performance on VENDOR entities.
    """

    def __init__(self, variations_path: str, aliases_path: str):
        """
        Initialize with vendor variation databases.

        Args:
            variations_path: Path to Vendor_Name_Variations.json
            aliases_path: Path to Vendor_Aliases_Database.csv
        """
        self.variations = self._load_variations(variations_path)
        self.aliases = self._load_aliases(aliases_path)
        self.canonical_to_variations = self._build_lookup()

    def _load_variations(self, path: str) -> Dict[str, List[str]]:
        """Load vendor variations from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_aliases(self, path: str) -> List[Dict[str, str]]:
        """Load vendor aliases from CSV file."""
        import csv
        aliases = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                aliases.append(row)
        return aliases

    def _build_lookup(self) -> Dict[str, Set[str]]:
        """Build reverse lookup from any variant to all variants."""
        lookup = {}
        for canonical, variants in self.variations.items():
            all_variants = set([canonical] + variants)
            for variant in all_variants:
                lookup[variant.lower()] = all_variants
        return lookup

    def augment_pattern(self, text: str, entities: List[Dict]) -> List[Tuple[str, List[Dict]]]:
        """
        Generate augmented versions of text with vendor name variations.

        Args:
            text: Original text
            entities: Original entity annotations

        Returns:
            List of (augmented_text, augmented_entities) tuples
        """
        augmented_samples = []

        # Find all vendor entities in the text
        vendor_entities = [e for e in entities if e.get('label') == 'VENDOR']

        if not vendor_entities:
            return [(text, entities)]

        # For each vendor entity, create variations
        for vendor_entity in vendor_entities:
            start = vendor_entity['start']
            end = vendor_entity['end']
            original_vendor = text[start:end]

            # Find all possible variations
            variations = self._get_variations(original_vendor)

            # Create augmented samples with different variations
            for variation in variations[:5]:  # Limit to 5 variations per vendor
                if variation.lower() == original_vendor.lower():
                    continue

                new_text = text[:start] + variation + text[end:]
                new_entities = self._adjust_entities(entities, start, end, len(variation))
                augmented_samples.append((new_text, new_entities))

        return augmented_samples

    def _get_variations(self, vendor_name: str) -> List[str]:
        """Get all variations for a given vendor name."""
        normalized = vendor_name.lower().strip()

        # Direct lookup
        if normalized in self.canonical_to_variations:
            return list(self.canonical_to_variations[normalized])

        # Fuzzy matching - check if any variant contains or is contained
        matches = set()
        for variant, all_variants in self.canonical_to_variations.items():
            if normalized in variant or variant in normalized:
                matches.update(all_variants)

        return list(matches) if matches else [vendor_name]

    def _adjust_entities(self, entities: List[Dict], old_start: int, old_end: int,
                        new_length: int) -> List[Dict]:
        """Adjust entity positions after text substitution."""
        old_length = old_end - old_start
        length_diff = new_length - old_length

        adjusted = []
        for entity in entities:
            new_entity = entity.copy()

            if entity['start'] == old_start and entity['end'] == old_end:
                # This is the modified entity
                new_entity['end'] = old_start + new_length
            elif entity['start'] > old_end:
                # Entity comes after modified section
                new_entity['start'] += length_diff
                new_entity['end'] += length_diff

            adjusted.append(new_entity)

        return adjusted

    def create_vendor_patterns(self) -> List[str]:
        """
        Create comprehensive regex patterns for vendor matching.

        Returns:
            List of regex patterns for vendor recognition
        """
        patterns = []

        # Collect all vendor names and their variations
        all_vendors = set()
        for canonical, variants in self.variations.items():
            all_vendors.add(canonical)
            all_vendors.update(variants)

        # Group by common patterns

        # Pattern 1: Company suffixes
        suffixes = [
            r'\s+(?:Inc\.?|Corporation|Corp\.?|Ltd\.?|Limited|LLC|GmbH|AG|SE|SA|plc)',
            r'\s+(?:Technologies|Solutions|Systems|Electric|Electronics|Automation)',
            r'\s+(?:International|Global|Group|Holdings|Industries)'
        ]

        # Pattern 2: Product/brand names within companies
        product_patterns = [
            r'(?:SICAM|SIPROTEC|Trainguard|Simis|SIMATIC)',  # Siemens products
            r'(?:REL\d{3}|TEC|Ability)',  # ABB products
            r'(?:MiCOM|MarkVIe|Predix|iFIX)',  # GE products
            r'(?:Atlas|Urbalis|SmartLock|Mastria)',  # Alstom products
            r'(?:ControlLogix|CompactLogix|FactoryTalk)',  # Rockwell products
        ]

        # Pattern 3: Common vendor words
        vendor_keywords = [
            r'(?:Siemens|ABB|General\s+Electric|Schneider|Honeywell)',
            r'(?:Emerson|Yokogawa|Rockwell|Mitsubishi|Hitachi)',
            r'(?:Alstom|Thales|Bombardier|Wabtec|Stadler)',
            r'(?:Motorola|Harris|L3Harris|Cisco|Dell|HP)',
        ]

        # Pattern 4: Acronyms and abbreviations
        acronyms = [
            r'\b(?:GE|ABB|SEL|HPE|JCI|HID|FIS|SAP|CAF|BAE)\b',
        ]

        # Combine patterns
        patterns.extend(suffixes)
        patterns.extend(product_patterns)
        patterns.extend(vendor_keywords)
        patterns.extend(acronyms)

        # Pattern 5: Full vendor name list (high-confidence matches)
        sorted_vendors = sorted(all_vendors, key=len, reverse=True)  # Longest first
        for vendor in sorted_vendors:
            # Escape special regex characters
            escaped = re.escape(vendor)
            patterns.append(r'\b' + escaped + r'\b')

        return patterns

    def validate_recall(self, test_samples: List[Tuple[str, List[str]]]) -> float:
        """
        Validate recall on test samples.

        Args:
            test_samples: List of (text, expected_vendors) tuples

        Returns:
            Recall score (0.0 to 1.0)
        """
        patterns = self.create_vendor_patterns()
        combined_pattern = '|'.join(patterns)
        regex = re.compile(combined_pattern, re.IGNORECASE)

        true_positives = 0
        false_negatives = 0

        for text, expected_vendors in test_samples:
            found_vendors = set()
            for match in regex.finditer(text):
                found_vendors.add(match.group().lower())

            for expected in expected_vendors:
                expected_lower = expected.lower()
                # Check if any found vendor matches or is a variation
                matched = False
                for found in found_vendors:
                    if found in expected_lower or expected_lower in found:
                        matched = True
                        break

                if matched:
                    true_positives += 1
                else:
                    false_negatives += 1

        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        return recall

    def augment_dataset(self, dataset: List[Dict], augmentation_factor: int = 3) -> List[Dict]:
        """
        Augment entire dataset with vendor variations.

        Args:
            dataset: Original dataset with text and entities
            augmentation_factor: How many augmented samples to create per original

        Returns:
            Augmented dataset
        """
        augmented = []

        for sample in dataset:
            text = sample['text']
            entities = sample.get('entities', [])

            # Add original sample
            augmented.append(sample)

            # Generate augmented variations
            variations = self.augment_pattern(text, entities)

            # Add random subset of variations
            selected = random.sample(variations, min(augmentation_factor, len(variations)))
            for aug_text, aug_entities in selected:
                augmented.append({
                    'text': aug_text,
                    'entities': aug_entities,
                    'augmented': True,
                    'original_id': sample.get('id', None)
                })

        return augmented


def create_test_samples() -> List[Tuple[str, List[str]]]:
    """Create test samples for validation."""
    return [
        ("Siemens SICAM RTU deployed at power station", ["Siemens", "SICAM"]),
        ("ABB REL670 protection relay malfunction", ["ABB", "REL670"]),
        ("GE MarkVIe turbine control system", ["GE", "MarkVIe"]),
        ("Schneider Electric EcoStruxure platform", ["Schneider Electric", "EcoStruxure"]),
        ("Honeywell Process Solutions DCS upgrade", ["Honeywell Process Solutions"]),
        ("Emerson DeltaV control system", ["Emerson", "DeltaV"]),
        ("Yokogawa CENTUM VP installed", ["Yokogawa", "CENTUM VP"]),
        ("Rockwell Allen-Bradley ControlLogix PLC", ["Rockwell", "Allen-Bradley", "ControlLogix"]),
        ("Alstom Urbalis 400 CBTC system", ["Alstom", "Urbalis 400"]),
        ("Siemens Mobility Trainguard MT signaling", ["Siemens Mobility", "Trainguard MT"]),
        ("FIS Systematics core banking platform", ["FIS", "Systematics"]),
        ("Motorola MOTOTRBO digital radios", ["Motorola", "MOTOTRBO"]),
        ("L3Harris APX radios deployed", ["L3Harris", "APX"]),
        ("Cisco Catalyst switches installed", ["Cisco", "Catalyst"]),
        ("Dell PowerEdge servers upgraded", ["Dell", "PowerEdge"]),
        ("HPE Aruba wireless network", ["HPE", "Aruba"]),
        ("Johnson Controls C•CURE access control", ["Johnson Controls", "C•CURE"]),
        ("HID iCLASS SE credentials", ["HID", "iCLASS SE"]),
        ("Genetec Security Center PSIM", ["Genetec", "Security Center"]),
        ("Milestone XProtect VMS platform", ["Milestone", "XProtect"]),
    ]


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Vendor Pattern Augmentation for NER Training')
    parser.add_argument('--variations', default='Vendor_Name_Variations.json',
                       help='Path to vendor variations JSON file')
    parser.add_argument('--aliases', default='Vendor_Aliases_Database.csv',
                       help='Path to vendor aliases CSV file')
    parser.add_argument('--input', help='Input dataset JSON file')
    parser.add_argument('--output', help='Output augmented dataset JSON file')
    parser.add_argument('--test', action='store_true', help='Run validation test')
    parser.add_argument('--augmentation-factor', type=int, default=3,
                       help='Number of augmented samples per original')

    args = parser.parse_args()

    # Initialize augmenter
    augmenter = VendorPatternAugmenter(args.variations, args.aliases)

    if args.test:
        # Run validation test
        print("Running validation test on sample data...")
        test_samples = create_test_samples()
        recall = augmenter.validate_recall(test_samples)
        print(f"Recall on test samples: {recall:.2%}")

        if recall >= 0.95:
            print("✓ SUCCESS: Recall target of 95%+ achieved!")
        else:
            print(f"⚠ WARNING: Recall {recall:.2%} below 95% target")

        # Display sample patterns
        print("\nSample regex patterns generated:")
        patterns = augmenter.create_vendor_patterns()[:10]
        for i, pattern in enumerate(patterns, 1):
            print(f"{i}. {pattern}")

    elif args.input and args.output:
        # Augment dataset
        print(f"Loading dataset from {args.input}...")
        with open(args.input, 'r', encoding='utf-8') as f:
            dataset = json.load(f)

        print(f"Original dataset size: {len(dataset)} samples")
        print(f"Augmenting with factor {args.augmentation_factor}...")

        augmented_dataset = augmenter.augment_dataset(dataset, args.augmentation_factor)

        print(f"Augmented dataset size: {len(augmented_dataset)} samples")
        print(f"Increase: {len(augmented_dataset) - len(dataset)} new samples")

        print(f"Saving augmented dataset to {args.output}...")
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(augmented_dataset, f, indent=2, ensure_ascii=False)

        print("✓ Dataset augmentation complete!")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
