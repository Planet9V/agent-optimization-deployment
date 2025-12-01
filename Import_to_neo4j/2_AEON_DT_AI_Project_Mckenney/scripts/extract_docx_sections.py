#!/usr/bin/env python3
"""Extract representative sections from Water sector .docx files for validation testing."""

import sys
import os
from pathlib import Path
from docx import Document
import json

def extract_sections(docx_path, min_words=100):
    """Extract text sections from a .docx file."""
    doc = Document(docx_path)
    sections = []
    current_section = {"title": "", "content": "", "paragraphs": []}

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Check if this is a heading (section title)
        if para.style.name.startswith('Heading'):
            # Save previous section if it has content
            if current_section["paragraphs"]:
                current_section["content"] = "\n".join(current_section["paragraphs"])
                word_count = len(current_section["content"].split())
                if word_count >= min_words:
                    sections.append(current_section.copy())

            # Start new section
            current_section = {"title": text, "content": "", "paragraphs": []}
        else:
            current_section["paragraphs"].append(text)

    # Add final section
    if current_section["paragraphs"]:
        current_section["content"] = "\n".join(current_section["paragraphs"])
        word_count = len(current_section["content"].split())
        if word_count >= min_words:
            sections.append(current_section.copy())

    return sections

def categorize_section(section):
    """Categorize a section based on content keywords."""
    content_lower = (section["title"] + " " + section["content"]).lower()

    categories = {
        "equipment": ["equipment", "pump", "valve", "sensor", "meter", "filter", "treatment", "chlorine", "disinfection"],
        "operations": ["operation", "treatment", "process", "distribution", "wastewater", "drinking water", "supply"],
        "security": ["security", "cybersecurity", "threat", "vulnerability", "attack", "protection", "authentication"],
        "scada": ["scada", "control", "plc", "hmi", "rtu", "automation", "supervisory"],
        "standards": ["standard", "regulation", "compliance", "certification", "iso", "nist", "requirement"],
        "vendors": ["vendor", "manufacturer", "supplier", "provider", "company", "product"]
    }

    scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in content_lower)
        scores[category] = score

    # Return category with highest score
    return max(scores.items(), key=lambda x: x[1])[0] if max(scores.values()) > 0 else "general"

def main():
    # Document paths
    doc1_path = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Water Management/IACS_Water Management Equipment Manufacturing.md.docx"
    doc2_path = "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/13_Critical_Sector_IACS/Sector - Water Management/Water Management Equipment Manufacturing Overview.docx"

    print("Extracting sections from Water sector documents...")
    print(f"Document 1: {Path(doc1_path).name} ({Path(doc1_path).stat().st_size / 1024:.1f} KB)")
    print(f"Document 2: {Path(doc2_path).name} ({Path(doc2_path).stat().st_size / 1024:.1f} KB)")
    print()

    # Extract sections from both documents
    sections1 = extract_sections(doc1_path)
    sections2 = extract_sections(doc2_path)

    print(f"Extracted {len(sections1)} sections from Document 1")
    print(f"Extracted {len(sections2)} sections from Document 2")
    print()

    # Categorize all sections
    all_sections = []
    for i, section in enumerate(sections1):
        section["source"] = "IACS_Water Management Equipment Manufacturing.md.docx"
        section["section_id"] = f"doc1_sec{i+1}"
        section["category"] = categorize_section(section)
        section["word_count"] = len(section["content"].split())
        all_sections.append(section)

    for i, section in enumerate(sections2):
        section["source"] = "Water Management Equipment Manufacturing Overview.docx"
        section["section_id"] = f"doc2_sec{i+1}"
        section["category"] = categorize_section(section)
        section["word_count"] = len(section["content"].split())
        all_sections.append(section)

    # Group by category
    by_category = {}
    for section in all_sections:
        cat = section["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(section)

    print("Sections by category:")
    for cat, secs in sorted(by_category.items()):
        print(f"  {cat}: {len(secs)} sections")
    print()

    # Select 9 representative sections
    target_distribution = {
        "equipment": 2,
        "operations": 2,
        "security": 1,
        "scada": 2,
        "standards": 1,
        "vendors": 1
    }

    selected_sections = []
    for category, count in target_distribution.items():
        if category in by_category:
            # Sort by word count (prefer longer, more substantial sections)
            category_sections = sorted(by_category[category], key=lambda x: x["word_count"], reverse=True)
            selected = category_sections[:count]
            selected_sections.extend(selected)
            print(f"Selected {len(selected)} {category} sections")
        else:
            print(f"WARNING: No sections found for category '{category}'")

    print(f"\nTotal selected sections: {len(selected_sections)}")
    print()

    # Create output directory
    output_dir = Path("/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Critical_Infrastructure_Sectors_Patterns/water/validation/test_sections")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save sections as text files for NER processing
    manifest = []
    for i, section in enumerate(selected_sections, 1):
        filename = f"section_{i:02d}_{section['category']}.txt"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {section['title']}\n\n")
            f.write(section['content'])

        manifest.append({
            "id": i,
            "filename": filename,
            "category": section["category"],
            "source_document": section["source"],
            "section_id": section["section_id"],
            "title": section["title"],
            "word_count": section["word_count"]
        })

        print(f"Section {i}: {section['category']}")
        print(f"  Source: {section['source']}")
        print(f"  Title: {section['title'][:60]}...")
        print(f"  Words: {section['word_count']}")
        print()

    # Save manifest
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"Saved {len(selected_sections)} test sections to: {output_dir}")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
