"""
NER11 Gold Standard - Basic Usage Example

This example demonstrates basic entity extraction using the NER11 model.
"""

import spacy

# Load the model
print("Loading NER11 Gold Standard model...")
nlp = spacy.load("../models/model-best")
print(f"✓ Model loaded ({len(nlp.get_pipe('ner').labels)} entity types)\n")

# Sample text
text = """
The APT29 threat actor group, also known as Cozy Bear, exploited 
CVE-2023-12345, a critical zero-day vulnerability in the Siemens S7-1200 
programmable logic controller (PLC). The attack campaign targeted critical 
infrastructure in the energy sector across multiple European countries.

The malware, dubbed "EnergyBear", established persistence through a 
scheduled task and communicated with a command-and-control server using 
encrypted DNS tunneling. The attack exhibited characteristics of advanced 
persistent threat (APT) operations, including:

- Sophisticated social engineering tactics
- Multi-stage payload delivery
- Lateral movement through OT networks
- Data exfiltration via covert channels

Security researchers observed elevated levels of anxiety and stress among 
the incident response team, consistent with high-stakes cyber incidents. 
The psychological impact included increased cognitive load and decision 
fatigue, particularly during the initial triage phase.
"""

# Process text
print("Processing text...\n")
doc = nlp(text)

# Extract and display entities
print(f"Extracted {len(doc.ents)} entities:\n")
print(f"{'Entity Text':<40} {'Entity Type':<30} {'Position'}")
print("=" * 90)

for ent in doc.ents:
    print(f"{ent.text:<40} {ent.label_:<30} ({ent.start_char}, {ent.end_char})")

# Group by entity type
print("\n\nEntities by Category:\n")
print("=" * 90)

from collections import defaultdict
entities_by_type = defaultdict(list)

for ent in doc.ents:
    entities_by_type[ent.label_].append(ent.text)

for entity_type, entities in sorted(entities_by_type.items()):
    print(f"\n{entity_type}:")
    for entity in entities:
        print(f"  - {entity}")

print("\n" + "=" * 90)
print("✓ Processing complete!")
