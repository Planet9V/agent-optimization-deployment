#!/usr/bin/env python3
"""
Pre-annotation Script for Batch 2 - Technical Entity Extraction
Processes 25 incident reports for 10 technical entity types
"""

import spacy
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Entity patterns and keywords
ENTITY_PATTERNS = {
    "INCIDENT_CHARACTERISTIC": {
        "attack_types": [
            "ransomware", "phishing", "ddos", "malware", "trojan", "backdoor",
            "supply chain attack", "zero-day", "credential stuffing", "brute force",
            "sql injection", "xss", "remote code execution", "privilege escalation"
        ],
        "impact_indicators": [
            "data breach", "service disruption", "financial loss", "reputation damage",
            "operational shutdown", "data exfiltration", "system compromise"
        ],
        "time_patterns": [
            r"(\d+)\s+(days?|hours?|minutes?|months?|weeks?)\s+(to detect|undetected|dwell time)",
            r"detection\s+lag[:\s]+(\d+)\s+(days?|hours?|months?)",
            r"response\s+time[:\s]+(\d+)\s+(hours?|minutes?)"
        ]
    },

    "THREAT_VECTOR": {
        "apt_groups": [
            "apt28", "apt29", "apt41", "lazarus", "sandworm", "volt typhoon",
            "fancy bear", "cozy bear", "turla", "fin7", "carbanak", "apt32",
            "oceanlotus", "salt typhoon", "lockbit", "blackbasta", "royal", "cuba"
        ],
        "ransomware_families": [
            "lockbit", "blackbasta", "royal", "cuba", "conti", "ryuk", "revil",
            "emotet", "trickbot", "qakbot", "icedid", "cobalt strike"
        ],
        "attack_vectors": [
            "insider threat", "supply chain", "third-party", "vendor compromise",
            "natural disaster", "physical breach", "social engineering"
        ]
    },

    "ATTACKER_MOTIVATION": {
        "mice_framework": {
            "money": ["financial gain", "ransom", "extortion", "cryptocurrency", "profit"],
            "ideology": ["political", "activism", "hacktivism", "nation-state", "geopolitical"],
            "coercion": ["blackmail", "extortion", "intimidation", "pressure", "threat"],
            "ego": ["reputation", "notoriety", "bragging rights", "challenge", "recognition"]
        }
    },

    "HISTORICAL_PATTERN": {
        "trend_indicators": [
            "increasing", "decreasing", "escalating", "de-escalating", "recurring",
            "breakthrough", "novel", "unprecedented", "similar to", "reminiscent of"
        ],
        "temporal_markers": [
            r"(\d{4})\s+incident", r"since\s+(\d{4})", r"between\s+(\d{4})\s+and\s+(\d{4})",
            r"(q[1-4])\s+(\d{4})", r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})"
        ]
    },

    "FUTURE_THREAT": {
        "projection_indicators": [
            "expected", "predicted", "forecasted", "anticipated", "likely",
            "emerging", "trending", "growing", "increasing threat", "future risk"
        ],
        "confidence_levels": [
            "high confidence", "medium confidence", "low confidence",
            "very likely", "likely", "possible", "unlikely"
        ],
        "timeframes": [
            r"(next|within)\s+(\d+)\s+(year|month|quarter)",
            r"by\s+(\d{4})", r"(\d{4})\s+forecast"
        ]
    },

    "ORGANIZATIONAL_CONTEXT": {
        "sectors": [
            "energy", "healthcare", "finance", "banking", "critical infrastructure",
            "transportation", "telecommunications", "defense", "manufacturing",
            "retail", "government", "education", "technology"
        ],
        "size_indicators": [
            "enterprise", "sme", "small business", "large organization",
            "fortune 500", "multinational", "startup"
        ],
        "maturity_levels": [
            "mature", "immature", "developing", "advanced", "basic",
            "sophisticated", "nascent", "established"
        ]
    },

    "STAKEHOLDER_ROLE": {
        "roles": [
            "ciso", "cto", "cfo", "ceo", "board member", "it manager",
            "security analyst", "incident responder", "soc analyst", "threat hunter",
            "compliance officer", "risk manager", "auditor"
        ]
    },

    "DECISION_FACTOR": {
        "budget_indicators": [
            "budget", "cost", "investment", "funding", "resources",
            "roi", "return on investment", "cost-benefit"
        ],
        "risk_indicators": [
            "risk tolerance", "risk appetite", "risk acceptance", "risk aversion",
            "risk-based", "risk assessment"
        ],
        "compliance_indicators": [
            "compliance", "regulatory", "gdpr", "hipaa", "pci-dss",
            "sox", "nist", "iso 27001", "iec 62443"
        ],
        "political_indicators": [
            "political", "stakeholder pressure", "board mandate",
            "organizational politics", "executive decision"
        ]
    },

    "DETECTION_METHOD": {
        "behavioral_analysis": [
            "behavioral analysis", "anomaly detection", "behavioral monitoring",
            "ueba", "user behavior analytics", "baseline deviation"
        ],
        "signature_based": [
            "signature", "pattern matching", "rule-based", "known indicators",
            "ioc matching", "hash comparison"
        ],
        "anomaly_detection": [
            "anomaly", "outlier", "deviation", "abnormal", "unusual activity",
            "statistical analysis"
        ],
        "threat_intelligence": [
            "threat intelligence", "intel feed", "indicator sharing",
            "ioc feed", "threat data", "intelligence-driven"
        ]
    },

    "MITIGATION_ACTION": {
        "technical": [
            "patch", "update", "firewall rule", "segmentation", "isolation",
            "encryption", "mfa", "multi-factor", "access control", "authentication"
        ],
        "organizational": [
            "policy", "procedure", "training", "awareness", "governance",
            "incident response plan", "business continuity", "disaster recovery"
        ],
        "strategic": [
            "risk acceptance", "risk transfer", "insurance", "third-party assessment",
            "vendor management", "strategic planning"
        ],
        "behavioral": [
            "user training", "security awareness", "phishing simulation",
            "security culture", "human factor", "behavioral change"
        ]
    }
}

# CVE and vulnerability patterns
CVE_PATTERN = r"CVE-\d{4}-\d{4,7}"
APT_PATTERN = r"APT[\s-]?\d{1,3}"
IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
HASH_PATTERN = r"\b[a-fA-F0-9]{32,64}\b"

class PreAnnotator:
    def __init__(self):
        self.stats = defaultdict(int)
        self.confidence_scores = []

    def extract_entities(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract all 10 entity types from text"""
        entities = []
        doc = nlp(text)

        # 1. Baseline entities from spaCy
        entities.extend(self._extract_spacy_entities(doc, filename))

        # 2. Technical patterns (CVE, APT, IPs)
        entities.extend(self._extract_technical_patterns(text, filename))

        # 3. Incident characteristics
        entities.extend(self._extract_incident_characteristics(text, filename))

        # 4. Threat vectors
        entities.extend(self._extract_threat_vectors(text, filename))

        # 5. Attacker motivations
        entities.extend(self._extract_attacker_motivations(text, filename))

        # 6. Historical patterns
        entities.extend(self._extract_historical_patterns(text, filename))

        # 7. Future threats
        entities.extend(self._extract_future_threats(text, filename))

        # 8. Organizational context
        entities.extend(self._extract_organizational_context(text, filename))

        # 9. Stakeholder roles
        entities.extend(self._extract_stakeholder_roles(text, filename))

        # 10. Decision factors
        entities.extend(self._extract_decision_factors(text, filename))

        # 11. Detection methods
        entities.extend(self._extract_detection_methods(text, filename))

        # 12. Mitigation actions
        entities.extend(self._extract_mitigation_actions(text, filename))

        return entities

    def _extract_spacy_entities(self, doc, filename: str) -> List[Dict[str, Any]]:
        """Extract baseline ORG, PERSON, DATE entities"""
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON", "DATE", "GPE", "LOC"]:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "confidence": 0.85,
                    "source": "spacy_baseline",
                    "filename": filename
                })
                self.stats[f"spacy_{ent.label_}"] += 1
        return entities

    def _extract_technical_patterns(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract CVE, APT, IP, hash patterns"""
        entities = []

        # CVE patterns
        for match in re.finditer(CVE_PATTERN, text):
            entities.append({
                "text": match.group(0),
                "label": "VULNERABILITY_ID",
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.95,
                "source": "regex_cve",
                "filename": filename
            })
            self.stats["cve_patterns"] += 1

        # APT patterns
        for match in re.finditer(APT_PATTERN, text, re.IGNORECASE):
            entities.append({
                "text": match.group(0),
                "label": "THREAT_ACTOR",
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.90,
                "source": "regex_apt",
                "filename": filename
            })
            self.stats["apt_patterns"] += 1

        # IP addresses
        for match in re.finditer(IP_PATTERN, text):
            entities.append({
                "text": match.group(0),
                "label": "IP_ADDRESS",
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.90,
                "source": "regex_ip",
                "filename": filename
            })
            self.stats["ip_addresses"] += 1

        return entities

    def _extract_incident_characteristics(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract incident characteristics"""
        entities = []
        text_lower = text.lower()

        # Attack types
        for attack_type in ENTITY_PATTERNS["INCIDENT_CHARACTERISTIC"]["attack_types"]:
            if attack_type in text_lower:
                # Find actual position in original text
                pos = text_lower.find(attack_type)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(attack_type)],
                        "label": "ATTACK_TYPE",
                        "start": pos,
                        "end": pos + len(attack_type),
                        "confidence": 0.80,
                        "source": "keyword_attack_type",
                        "filename": filename
                    })
                    self.stats["attack_types"] += 1

        # Impact indicators
        for impact in ENTITY_PATTERNS["INCIDENT_CHARACTERISTIC"]["impact_indicators"]:
            if impact in text_lower:
                pos = text_lower.find(impact)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(impact)],
                        "label": "INCIDENT_IMPACT",
                        "start": pos,
                        "end": pos + len(impact),
                        "confidence": 0.75,
                        "source": "keyword_impact",
                        "filename": filename
                    })
                    self.stats["impact_indicators"] += 1

        # Time patterns
        for pattern in ENTITY_PATTERNS["INCIDENT_CHARACTERISTIC"]["time_patterns"]:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    "text": match.group(0),
                    "label": "DETECTION_TIMING",
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.85,
                    "source": "regex_timing",
                    "filename": filename
                })
                self.stats["detection_timing"] += 1

        return entities

    def _extract_threat_vectors(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract threat vectors"""
        entities = []
        text_lower = text.lower()

        # APT groups
        for apt in ENTITY_PATTERNS["THREAT_VECTOR"]["apt_groups"]:
            if apt in text_lower:
                pos = text_lower.find(apt)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(apt)],
                        "label": "APT_GROUP",
                        "start": pos,
                        "end": pos + len(apt),
                        "confidence": 0.90,
                        "source": "keyword_apt",
                        "filename": filename
                    })
                    self.stats["apt_groups"] += 1

        # Ransomware families
        for ransomware in ENTITY_PATTERNS["THREAT_VECTOR"]["ransomware_families"]:
            if ransomware in text_lower:
                pos = text_lower.find(ransomware)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(ransomware)],
                        "label": "RANSOMWARE_FAMILY",
                        "start": pos,
                        "end": pos + len(ransomware),
                        "confidence": 0.90,
                        "source": "keyword_ransomware",
                        "filename": filename
                    })
                    self.stats["ransomware_families"] += 1

        # Attack vectors
        for vector in ENTITY_PATTERNS["THREAT_VECTOR"]["attack_vectors"]:
            if vector in text_lower:
                pos = text_lower.find(vector)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(vector)],
                        "label": "ATTACK_VECTOR",
                        "start": pos,
                        "end": pos + len(vector),
                        "confidence": 0.75,
                        "source": "keyword_vector",
                        "filename": filename
                    })
                    self.stats["attack_vectors"] += 1

        return entities

    def _extract_attacker_motivations(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract attacker motivations using MICE framework"""
        entities = []
        text_lower = text.lower()

        for category, keywords in ENTITY_PATTERNS["ATTACKER_MOTIVATION"]["mice_framework"].items():
            for keyword in keywords:
                if keyword in text_lower:
                    pos = text_lower.find(keyword)
                    if pos != -1:
                        entities.append({
                            "text": text[pos:pos+len(keyword)],
                            "label": f"MOTIVATION_{category.upper()}",
                            "start": pos,
                            "end": pos + len(keyword),
                            "confidence": 0.70,
                            "source": "mice_framework",
                            "metadata": {"mice_category": category},
                            "filename": filename
                        })
                        self.stats[f"motivation_{category}"] += 1

        return entities

    def _extract_historical_patterns(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract historical patterns and trends"""
        entities = []
        text_lower = text.lower()

        # Trend indicators
        for indicator in ENTITY_PATTERNS["HISTORICAL_PATTERN"]["trend_indicators"]:
            if indicator in text_lower:
                pos = text_lower.find(indicator)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(indicator)],
                        "label": "TREND_INDICATOR",
                        "start": pos,
                        "end": pos + len(indicator),
                        "confidence": 0.70,
                        "source": "keyword_trend",
                        "filename": filename
                    })
                    self.stats["trend_indicators"] += 1

        # Temporal markers
        for pattern in ENTITY_PATTERNS["HISTORICAL_PATTERN"]["temporal_markers"]:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    "text": match.group(0),
                    "label": "TEMPORAL_REFERENCE",
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.85,
                    "source": "regex_temporal",
                    "filename": filename
                })
                self.stats["temporal_markers"] += 1

        return entities

    def _extract_future_threats(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract future threat projections"""
        entities = []
        text_lower = text.lower()

        # Projection indicators
        for indicator in ENTITY_PATTERNS["FUTURE_THREAT"]["projection_indicators"]:
            if indicator in text_lower:
                pos = text_lower.find(indicator)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(indicator)],
                        "label": "THREAT_PROJECTION",
                        "start": pos,
                        "end": pos + len(indicator),
                        "confidence": 0.65,
                        "source": "keyword_projection",
                        "filename": filename
                    })
                    self.stats["threat_projections"] += 1

        # Confidence levels
        for confidence in ENTITY_PATTERNS["FUTURE_THREAT"]["confidence_levels"]:
            if confidence in text_lower:
                pos = text_lower.find(confidence)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(confidence)],
                        "label": "CONFIDENCE_LEVEL",
                        "start": pos,
                        "end": pos + len(confidence),
                        "confidence": 0.80,
                        "source": "keyword_confidence",
                        "filename": filename
                    })
                    self.stats["confidence_levels"] += 1

        # Timeframes
        for pattern in ENTITY_PATTERNS["FUTURE_THREAT"]["timeframes"]:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    "text": match.group(0),
                    "label": "THREAT_TIMEFRAME",
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.75,
                    "source": "regex_timeframe",
                    "filename": filename
                })
                self.stats["threat_timeframes"] += 1

        return entities

    def _extract_organizational_context(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract organizational context"""
        entities = []
        text_lower = text.lower()

        # Sectors
        for sector in ENTITY_PATTERNS["ORGANIZATIONAL_CONTEXT"]["sectors"]:
            if sector in text_lower:
                pos = text_lower.find(sector)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(sector)],
                        "label": "ORGANIZATION_SECTOR",
                        "start": pos,
                        "end": pos + len(sector),
                        "confidence": 0.80,
                        "source": "keyword_sector",
                        "filename": filename
                    })
                    self.stats["org_sectors"] += 1

        # Size indicators
        for size in ENTITY_PATTERNS["ORGANIZATIONAL_CONTEXT"]["size_indicators"]:
            if size in text_lower:
                pos = text_lower.find(size)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(size)],
                        "label": "ORGANIZATION_SIZE",
                        "start": pos,
                        "end": pos + len(size),
                        "confidence": 0.70,
                        "source": "keyword_size",
                        "filename": filename
                    })
                    self.stats["org_sizes"] += 1

        # Maturity levels
        for maturity in ENTITY_PATTERNS["ORGANIZATIONAL_CONTEXT"]["maturity_levels"]:
            if maturity in text_lower:
                pos = text_lower.find(maturity)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(maturity)],
                        "label": "SECURITY_MATURITY",
                        "start": pos,
                        "end": pos + len(maturity),
                        "confidence": 0.70,
                        "source": "keyword_maturity",
                        "filename": filename
                    })
                    self.stats["security_maturity"] += 1

        return entities

    def _extract_stakeholder_roles(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract stakeholder roles"""
        entities = []
        text_lower = text.lower()

        for role in ENTITY_PATTERNS["STAKEHOLDER_ROLE"]["roles"]:
            if role in text_lower:
                pos = text_lower.find(role)
                if pos != -1:
                    entities.append({
                        "text": text[pos:pos+len(role)],
                        "label": "STAKEHOLDER_ROLE",
                        "start": pos,
                        "end": pos + len(role),
                        "confidence": 0.85,
                        "source": "keyword_role",
                        "filename": filename
                    })
                    self.stats["stakeholder_roles"] += 1

        return entities

    def _extract_decision_factors(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract decision factors"""
        entities = []
        text_lower = text.lower()

        factor_types = [
            ("budget_indicators", "BUDGET_FACTOR"),
            ("risk_indicators", "RISK_FACTOR"),
            ("compliance_indicators", "COMPLIANCE_FACTOR"),
            ("political_indicators", "POLITICAL_FACTOR")
        ]

        for factor_key, label in factor_types:
            for indicator in ENTITY_PATTERNS["DECISION_FACTOR"][factor_key]:
                if indicator in text_lower:
                    pos = text_lower.find(indicator)
                    if pos != -1:
                        entities.append({
                            "text": text[pos:pos+len(indicator)],
                            "label": label,
                            "start": pos,
                            "end": pos + len(indicator),
                            "confidence": 0.75,
                            "source": f"keyword_{factor_key}",
                            "filename": filename
                        })
                        self.stats[factor_key] += 1

        return entities

    def _extract_detection_methods(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract detection methods"""
        entities = []
        text_lower = text.lower()

        method_types = [
            ("behavioral_analysis", "DETECTION_BEHAVIORAL"),
            ("signature_based", "DETECTION_SIGNATURE"),
            ("anomaly_detection", "DETECTION_ANOMALY"),
            ("threat_intelligence", "DETECTION_INTELLIGENCE")
        ]

        for method_key, label in method_types:
            for method in ENTITY_PATTERNS["DETECTION_METHOD"][method_key]:
                if method in text_lower:
                    pos = text_lower.find(method)
                    if pos != -1:
                        entities.append({
                            "text": text[pos:pos+len(method)],
                            "label": label,
                            "start": pos,
                            "end": pos + len(method),
                            "confidence": 0.80,
                            "source": f"keyword_{method_key}",
                            "filename": filename
                        })
                        self.stats[method_key] += 1

        return entities

    def _extract_mitigation_actions(self, text: str, filename: str) -> List[Dict[str, Any]]:
        """Extract mitigation actions"""
        entities = []
        text_lower = text.lower()

        action_types = [
            ("technical", "MITIGATION_TECHNICAL"),
            ("organizational", "MITIGATION_ORGANIZATIONAL"),
            ("strategic", "MITIGATION_STRATEGIC"),
            ("behavioral", "MITIGATION_BEHAVIORAL")
        ]

        for action_key, label in action_types:
            for action in ENTITY_PATTERNS["MITIGATION_ACTION"][action_key]:
                if action in text_lower:
                    pos = text_lower.find(action)
                    if pos != -1:
                        entities.append({
                            "text": text[pos:pos+len(action)],
                            "label": label,
                            "start": pos,
                            "end": pos + len(action),
                            "confidence": 0.75,
                            "source": f"keyword_{action_key}",
                            "filename": filename
                        })
                        self.stats[f"mitigation_{action_key}"] += 1

        return entities

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file and return annotations"""
        text = file_path.read_text(encoding='utf-8', errors='ignore')
        entities = self.extract_entities(text, file_path.name)

        return {
            "filename": file_path.name,
            "filepath": str(file_path),
            "text_length": len(text),
            "entity_count": len(entities),
            "entities": entities,
            "timestamp": datetime.now().isoformat()
        }

    def process_batch(self, files: List[Path], output_path: Path):
        """Process batch of files and save to JSONL"""
        all_results = []

        print(f"Processing {len(files)} files...")
        for i, file_path in enumerate(files, 1):
            print(f"  [{i}/{len(files)}] Processing: {file_path.name}")
            result = self.process_file(file_path)
            all_results.append(result)

            # Track confidence scores
            for entity in result["entities"]:
                self.confidence_scores.append(entity["confidence"])

        # Write JSONL output
        with output_path.open('w', encoding='utf-8') as f:
            for result in all_results:
                f.write(json.dumps(result) + '\n')

        # Generate statistics
        return self._generate_statistics(all_results, output_path)

    def _generate_statistics(self, results: List[Dict], output_path: Path) -> Dict:
        """Generate processing statistics"""
        total_entities = sum(r["entity_count"] for r in results)
        avg_confidence = sum(self.confidence_scores) / len(self.confidence_scores) if self.confidence_scores else 0

        stats = {
            "total_files": len(results),
            "total_entities": total_entities,
            "average_entities_per_file": total_entities / len(results) if results else 0,
            "average_confidence": avg_confidence,
            "entity_type_counts": dict(self.stats),
            "output_file": str(output_path),
            "processing_timestamp": datetime.now().isoformat()
        }

        # Save stats
        stats_path = output_path.parent / f"{output_path.stem}_stats.json"
        with stats_path.open('w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        return stats


def main():
    # Define paths
    source_dir = Path("/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training")
    output_path = Path("/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/15_NER10_Approach/annotation/batch2_preannotated.jsonl")

    # Get first 25 .md files
    all_files = sorted(source_dir.glob("*.md"))
    target_files = all_files[:25]

    print(f"Found {len(all_files)} total files")
    print(f"Processing first {len(target_files)} files")
    print(f"Output: {output_path}")
    print()

    # Process batch
    annotator = PreAnnotator()
    stats = annotator.process_batch(target_files, output_path)

    # Print summary
    print("\n" + "="*60)
    print("BATCH 2 PRE-ANNOTATION COMPLETE")
    print("="*60)
    print(f"Files processed: {stats['total_files']}")
    print(f"Total entities: {stats['total_entities']}")
    print(f"Avg entities/file: {stats['average_entities_per_file']:.1f}")
    print(f"Avg confidence: {stats['average_confidence']:.2f}")
    print(f"\nOutput: {stats['output_file']}")
    print(f"Stats: {output_path.parent / f'{output_path.stem}_stats.json'}")

    # Top entity types
    print("\nTop 10 Entity Types:")
    sorted_types = sorted(stats['entity_type_counts'].items(), key=lambda x: x[1], reverse=True)
    for entity_type, count in sorted_types[:10]:
        print(f"  {entity_type}: {count}")

    # Validation check
    if stats['total_entities'] >= 550:
        print(f"\n✓ TARGET MET: {stats['total_entities']} entities (target: 550-750)")
    else:
        print(f"\n⚠ BELOW TARGET: {stats['total_entities']} entities (target: 550-750)")


if __name__ == "__main__":
    main()
