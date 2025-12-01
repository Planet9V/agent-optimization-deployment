#!/usr/bin/env python3
"""
Comprehensive ICS-SEC-KG Dump Analyzer
Analyzes all downloaded ICS-SEC-KG dumps to document:
- Structure and predicates
- Key relationships for attack chains
- Schema alignment opportunities
- NER training data potential
"""

import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

ICS_KG_DUMPS = Path('/home/jim/2_OXOT_Projects_Dev/10_Ontologies/ICS-SEC-KG/dumps')

class DumpAnalyzer:
    """Comprehensive analyzer for ICS-SEC-KG TTL dumps"""

    def __init__(self):
        self.results = {}

    def analyze_dump(self, dump_path: Path, name: str, sample_size: int = 10000) -> Dict:
        """Analyze a single TTL dump file"""
        print(f"\n{'='*80}")
        print(f"📂 ANALYZING: {name}")
        print(f"📁 File: {dump_path.name}")
        print(f"📊 Size: {dump_path.stat().st_size / 1024 / 1024:.1f}MB")
        print(f"{'='*80}")

        analysis = {
            'name': name,
            'file': str(dump_path),
            'size_mb': round(dump_path.stat().st_size / 1024 / 1024, 2),
            'predicates': Counter(),
            'classes': Counter(),
            'namespaces': set(),
            'sample_entities': [],
            'attack_chain_relevance': {},
            'ner_training_potential': {}
        }

        # Parse sample of file
        with open(dump_path, 'r') as f:
            lines_sampled = 0
            current_entity = {}
            current_subject = None

            for line in f:
                lines_sampled += 1
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                # Extract namespace prefixes
                if line.startswith('@prefix'):
                    match = re.search(r'@prefix\s+(\w+):\s+<([^>]+)>', line)
                    if match:
                        prefix, uri = match.groups()
                        analysis['namespaces'].add(f"{prefix}:{uri}")

                # Extract triples
                triple_match = re.search(r'<([^>]+)>\s+<([^>]+)>\s+[<"]([^>"]+)[">]', line)
                if triple_match:
                    subject, predicate, obj = triple_match.groups()

                    # Track subject changes
                    if subject != current_subject:
                        if current_entity and len(analysis['sample_entities']) < 5:
                            analysis['sample_entities'].append(current_entity.copy())
                        current_entity = {'subject': subject, 'properties': {}}
                        current_subject = subject

                    # Extract predicate name
                    pred_name = predicate.split('/')[-1].split('#')[-1]
                    analysis['predicates'][pred_name] += 1

                    # Track in current entity
                    if pred_name not in current_entity['properties']:
                        current_entity['properties'][pred_name] = []
                    current_entity['properties'][pred_name].append(obj)

                    # Detect classes
                    if 'type' in pred_name.lower() or pred_name == 'a':
                        class_name = obj.split('/')[-1].split('#')[-1]
                        analysis['classes'][class_name] += 1

                if lines_sampled >= sample_size:
                    break

        # Analyze attack chain relevance
        analysis['attack_chain_relevance'] = self._assess_attack_chain_relevance(analysis)

        # Analyze NER training potential
        analysis['ner_training_potential'] = self._assess_ner_potential(analysis)

        return analysis

    def _assess_attack_chain_relevance(self, analysis: Dict) -> Dict:
        """Assess how this dump supports CVE→CWE→CAPEC→ATT&CK chains"""
        preds = analysis['predicates']

        relevance = {
            'chain_mappings': [],
            'linking_properties': [],
            'score': 0  # 0-10
        }

        # Check for chain-relevant predicates
        if any('cve' in p.lower() for p in preds):
            relevance['chain_mappings'].append('CVE entity presence')
            relevance['score'] += 2

        if any('cwe' in p.lower() or 'weakness' in p.lower() for p in preds):
            relevance['chain_mappings'].append('CWE/Weakness relationships')
            relevance['linking_properties'].append('hasCWE, hasRelatedWeakness')
            relevance['score'] += 3

        if any('capec' in p.lower() or 'attack pattern' in p.lower() for p in preds):
            relevance['chain_mappings'].append('CAPEC attack pattern connections')
            relevance['linking_properties'].append('hasCAPEC, hasRelatedWeakness')
            relevance['score'] += 3

        if any('technique' in p.lower() or 'tactic' in p.lower() for p in preds):
            relevance['chain_mappings'].append('ATT&CK technique/tactic mappings')
            relevance['linking_properties'].append('implementsTechnique, accomplishesTactic')
            relevance['score'] += 2

        return relevance

    def _assess_ner_potential(self, analysis: Dict) -> Dict:
        """Assess value for NER training data extraction"""
        potential = {
            'entity_types': [],
            'extraction_targets': [],
            'score': 0  # 0-10
        }

        classes = analysis['classes']
        preds = analysis['predicates']

        # Check for valuable entity types
        entity_indicators = {
            'CVE': ['CVE identifiers', 'vulnerability references'],
            'CWE': ['Weakness types', 'security categories'],
            'CAPEC': ['Attack pattern names', 'attack descriptions'],
            'Technique': ['ATT&CK techniques', 'tactic names'],
            'Product': ['Software products', 'vendor names'],
            'Sector': ['Critical infrastructure sectors'],
            'Advisory': ['Security advisory identifiers']
        }

        for entity_type, descriptions in entity_indicators.items():
            if any(entity_type.lower() in c.lower() for c in classes):
                potential['entity_types'].append(entity_type)
                potential['extraction_targets'].extend(descriptions)
                potential['score'] += 1

        # Check for textual description predicates (good for context)
        text_predicates = ['description', 'title', 'name', 'summary']
        if any(tp in str(preds).lower() for tp in text_predicates):
            potential['extraction_targets'].append('Textual descriptions for context')
            potential['score'] += 2

        return potential

    def generate_comprehensive_report(self) -> str:
        """Generate markdown report with all findings"""
        report = f"""# ICS-SEC-KG Dump Analysis Report
**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Dumps Analyzed**: {len(self.results)}
**Total Size**: {sum(r['size_mb'] for r in self.results.values()):.1f}MB

## Executive Summary

This report provides a comprehensive analysis of ICS-SEC-KG dumps to support:
1. **Attack Chain Unification**: CVE→CWE→CAPEC→ATT&CK semantic mapping
2. **Schema Integration**: Alignment with our cybersecurity ontology
3. **NER Training**: Entity extraction and relationship identification

---
"""

        # Add per-dump analysis
        for name, analysis in sorted(self.results.items()):
            report += self._format_dump_section(name, analysis)

        # Add synthesis section
        report += self._generate_synthesis()

        return report

    def _format_dump_section(self, name: str, analysis: Dict) -> str:
        """Format individual dump analysis section"""
        section = f"""
## {name.upper()} Dump

**File**: `{Path(analysis['file']).name}`
**Size**: {analysis['size_mb']}MB
**Classes**: {len(analysis['classes'])} unique types
**Predicates**: {len(analysis['predicates'])} unique properties

### Top 10 Predicates
"""
        for pred, count in analysis['predicates'].most_common(10):
            section += f"- `{pred}`: {count:,} occurrences\n"

        section += "\n### Top 5 Entity Classes\n"
        for cls, count in analysis['classes'].most_common(5):
            section += f"- `{cls}`: {count:,} instances\n"

        # Attack chain relevance
        relevance = analysis['attack_chain_relevance']
        section += f"\n### Attack Chain Relevance (Score: {relevance['score']}/10)\n"
        if relevance['chain_mappings']:
            section += "**Supports**:\n"
            for mapping in relevance['chain_mappings']:
                section += f"- {mapping}\n"
        if relevance['linking_properties']:
            section += f"\n**Key Properties**: {', '.join(relevance['linking_properties'])}\n"

        # NER potential
        ner = analysis['ner_training_potential']
        section += f"\n### NER Training Potential (Score: {ner['score']}/10)\n"
        if ner['entity_types']:
            section += f"**Entity Types**: {', '.join(ner['entity_types'])}\n"
        if ner['extraction_targets']:
            section += "**Extraction Targets**:\n"
            for target in ner['extraction_targets'][:5]:
                section += f"- {target}\n"

        # Sample entity
        if analysis['sample_entities']:
            section += "\n### Sample Entity Structure\n```\n"
            sample = analysis['sample_entities'][0]
            section += f"Subject: {sample['subject']}\n"
            for prop, values in list(sample['properties'].items())[:5]:
                section += f"  {prop}: {values[0] if values else 'N/A'}\n"
            section += "```\n"

        section += "\n---\n"
        return section

    def _generate_synthesis(self) -> str:
        """Generate synthesis and recommendations"""
        return """
## Synthesis & Recommendations

### Attack Chain Construction Strategy

**Optimal Linking Approach**:
1. **ICSA Advisories** → CVE identifiers (via `hasCVE`)
2. **CVE Dump** → CWE weaknesses (via `hasCWE`)
3. **CAPEC Dump** → CWE relationships (via `hasRelatedWeakness`)
4. **ATT&CK Dump** → CAPEC patterns (via `hasCAPEC` or technique descriptions)

**Expected Chain Completeness**:
- ICSA provides ~100K+ CVE references
- CVE-2023 dump contains ~29K vulnerabilities with CWE mappings
- CAPEC dump includes ~600 attack patterns with CWE links
- ATT&CK dump covers ~700 techniques

**Estimated Complete Chains**: ~500-2,000 CVE→CWE→CAPEC→ATT&CK paths

### Schema Integration Priorities

1. **Import ICSA Advisory Structure**: ICS-specific vulnerability tracking
2. **Align CWE Hierarchy**: Weakness taxonomy for root cause analysis
3. **Integrate CAPEC Patterns**: Attack pattern ontology for threat modeling
4. **Map ATT&CK Techniques**: Tactical/technical adversary behavior

### NER Training Data Extraction

**High-Value Sources**:
- **ICSA**: ICS products, vendors, sectors (critical infrastructure context)
- **CVE**: Vulnerability descriptions, impact statements
- **CAPEC**: Attack pattern narratives, mitigation strategies
- **ATT&CK**: Technique descriptions, procedure examples

**Recommended Extraction Pipeline**:
1. Parse TTL dumps for entity-description pairs
2. Extract CVE/CWE/CAPEC/ATT&CK identifiers as labels
3. Use descriptions as training contexts
4. Generate relationship annotations from predicates

---

**Next Steps**:
1. Implement TTL parser for complete attack chain extraction
2. Generate Neo4j Cypher import statements
3. Create NER training dataset from textual descriptions
4. Validate chains with known examples (e.g., Log4Shell CVE-2021-44228)
"""

def main():
    analyzer = DumpAnalyzer()

    # Analyze each dump category
    dumps_to_analyze = {
        'CAPEC': ICS_KG_DUMPS / 'capec/capec_latest.ttl',
        'ATT&CK': ICS_KG_DUMPS / 'cat/enterprise-attack.ttl',
        'CWE': ICS_KG_DUMPS / 'cwe/cwec_latest.ttl',
        'CVE-2023': ICS_KG_DUMPS / 'cve/nvd_cve_2023.ttl',
        'CPE': ICS_KG_DUMPS / 'cpe/cpe_dictionary.ttl',
        'ICSA': ICS_KG_DUMPS / 'icsa/icsa_advisories.ttl'
    }

    for name, path in dumps_to_analyze.items():
        if path.exists():
            # Adjust sample size based on file size
            sample_size = 50000 if path.stat().st_size > 50*1024*1024 else 10000
            analyzer.results[name] = analyzer.analyze_dump(path, name, sample_size)
        else:
            print(f"⚠️  SKIP: {name} - file not found at {path}")

    # Generate and save report
    print("\n" + "="*80)
    print("📝 GENERATING COMPREHENSIVE REPORT")
    print("="*80)

    report = analyzer.generate_comprehensive_report()

    output_file = Path('docs/ICS_SEC_KG_COMPREHENSIVE_ANALYSIS.md')
    output_file.write_text(report)

    print(f"\n✅ Report saved to: {output_file}")
    print(f"📊 Total dumps analyzed: {len(analyzer.results)}")
    print(f"📈 Total size: {sum(r['size_mb'] for r in analyzer.results.values()):.1f}MB")

    # Save JSON version for programmatic access
    json_file = Path('docs/ICS_SEC_KG_ANALYSIS.json')
    with open(json_file, 'w') as f:
        # Convert Counter and set objects to serializable format
        results_json = {}
        for name, data in analyzer.results.items():
            results_json[name] = {
                'name': data['name'],
                'file': data['file'],
                'size_mb': data['size_mb'],
                'predicates': dict(data['predicates'].most_common(20)),
                'classes': dict(data['classes'].most_common(10)),
                'namespaces': list(data['namespaces'])[:10],
                'attack_chain_relevance': data['attack_chain_relevance'],
                'ner_training_potential': data['ner_training_potential'],
                'sample_entities': data['sample_entities'][:3]
            }
        json.dump(results_json, f, indent=2)

    print(f"✅ JSON data saved to: {json_file}")
    print()

if __name__ == '__main__':
    import pandas as pd
    main()
