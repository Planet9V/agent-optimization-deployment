# WAVE 4 Step 3: OpenSPG Semantic Reasoning & Inference

**Document Version**: 1.0
**Created**: 2025-11-25
**Last Modified**: 2025-11-25
**Status**: ACTIVE
**Purpose**: Semantic relationship inference, knowledge graph construction, and SPG reasoning

---

## Table of Contents

1. [Step 3 Overview](#step-3-overview)
2. [OpenSPG Framework](#openspg-framework)
3. [Semantic Pattern Recognition](#semantic-pattern-recognition)
4. [Relationship Inference Engine](#relationship-inference-engine)
5. [Knowledge Graph Construction](#knowledge-graph-construction)
6. [Reasoning & Validation](#reasoning--validation)
7. [Entity Linking & Resolution](#entity-linking--resolution)
8. [Rule-Based Reasoning](#rule-based-reasoning)
9. [Causal Inference](#causal-inference)
10. [Explainability & Tracing](#explainability--tracing)

---

## Step 3 Overview

### Purpose

Step 3 transforms extracted entities into a rich semantic knowledge graph by inferring relationships, identifying patterns, and applying domain-specific reasoning rules. This step creates the foundation for intelligent analysis and pattern discovery.

### Key Responsibilities

- Identify semantic relationships between entities
- Construct knowledge graph from entity relationships
- Apply domain-specific reasoning rules
- Perform entity linking and disambiguation
- Infer implicit relationships through transitive rules
- Validate semantic consistency
- Generate explainability traces
- Create reasoning provenance

### Expected Inputs

- Extracted entities with types and confidence scores
- Original document text
- Document context and metadata
- Domain specifications

### Expected Outputs

- Entity-relationship graph
- Typed relationships with confidence scores
- Reasoning traces and explanations
- Semantic validation reports
- Graph statistics and metadata

---

## OpenSPG Framework

### SPG Architecture

```
┌───────────────────────────────────────────┐
│      Semantic Property Graph (SPG)        │
├───────────────────────────────────────────┤
│                                           │
│  Entities (Nodes)                         │
│  ├── Properties: {type, value, ...}       │
│  ├── Attributes: {name, description}      │
│  └── Metadata: {confidence, source}       │
│                                           │
│  Relationships (Edges)                    │
│  ├── Type: {semantic_type}                │
│  ├── Direction: {source → target}         │
│  ├── Attributes: {strength, reason}       │
│  └── Reasoning: {rule_applied, confidence}│
│                                           │
│  Schemas                                  │
│  ├── Entity Type Definitions              │
│  ├── Relationship Type Definitions        │
│  ├── Constraint Rules                     │
│  └── Inference Rules                      │
│                                           │
└───────────────────────────────────────────┘
```

### Core Concepts

**Entity Types**: Categorized nodes with properties
**Relationships**: Directed edges with semantics
**Properties**: Key-value attributes on entities/relationships
**Schemas**: Type definitions and constraints
**Reasoning Rules**: Logic for inference

---

## Semantic Pattern Recognition

### Relationship Pattern Types

| Pattern | Description | Example |
|---------|-------------|---------|
| Co-occurrence | Entities appear together | "APT28 used WannaCry malware" |
| Temporal | Time-based relationships | "Attack occurred on 2024-01-15" |
| Causal | Cause-effect relationships | "Vulnerability led to breach" |
| Compositional | Part-whole relationships | "Server is part of Infrastructure" |
| Similarity | Entity similarity/clustering | "Domain A and Domain B are similar" |
| Hierarchical | Type/subtype relationships | "APT28 is a Threat Actor" |

### Pattern Detection Algorithm

```python
# File: backend/services/pattern_detector.py

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
from collections import defaultdict

class RelationshipType(Enum):
    """Types of semantic relationships"""
    USES = "uses"  # Agent uses Tool/Malware
    TARGETS = "targets"  # Attack targets System/Organization
    EXPLOITS = "exploits"  # Attack exploits Vulnerability
    CAUSES = "causes"  # Event causes Impact
    RELATED_TO = "related_to"  # General relationship
    IS_A = "is_a"  # Inheritance
    PART_OF = "part_of"  # Composition
    LOCATED_IN = "located_in"  # Location
    SAME_AS = "same_as"  # Equivalence
    SIMILAR_TO = "similar_to"  # Similarity

@dataclass
class Relationship:
    """Semantic relationship between entities"""
    source_entity: str
    source_type: str
    target_entity: str
    target_type: str
    relationship_type: str
    confidence: float
    strength: float  # 0-1, relationship magnitude
    sentence_context: str
    reasoning_rules: List[str]
    evidence_count: int = 1
    metadata: Dict = None

    def to_dict(self) -> Dict:
        return {
            'source': self.source_entity,
            'source_type': self.source_type,
            'target': self.target_entity,
            'target_type': self.target_type,
            'relationship_type': self.relationship_type,
            'confidence': round(self.confidence, 4),
            'strength': round(self.strength, 4),
            'context': self.sentence_context,
            'rules_applied': self.reasoning_rules,
            'evidence_count': self.evidence_count,
        }

class PatternDetector:
    """Detect semantic patterns and relationships"""

    # Relationship keywords by type
    RELATIONSHIP_PATTERNS = {
        RelationshipType.USES: {
            'keywords': ['uses', 'uses', 'utilized', 'employs', 'deployed'],
            'pattern': r'{source}\s+(uses|utilized|employs|deployed)\s+{target}',
        },
        RelationshipType.TARGETS: {
            'keywords': ['targets', 'attacks', 'compromises', 'affects', 'impacts'],
            'pattern': r'{source}\s+(targets|attacks|compromises|affects)\s+{target}',
        },
        RelationshipType.EXPLOITS: {
            'keywords': ['exploits', 'leverages', 'takes advantage of'],
            'pattern': r'{source}\s+(exploits|leverages)\s+{target}',
        },
        RelationshipType.CAUSES: {
            'keywords': ['causes', 'leads to', 'results in', 'results in'],
            'pattern': r'{source}\s+(causes|leads\s+to|results\s+in)\s+{target}',
        },
    }

    def __init__(self):
        self.detected_relationships = []
        self.rule_engine = RuleEngine()

    def detect_relationships(
        self,
        entities: List[Dict],
        text: str,
        sentences: List[str]
    ) -> List[Relationship]:
        """Detect semantic relationships from text and entities"""

        relationships = []

        # Sentence-level relationship detection
        for sentence in sentences:
            sent_relationships = self._detect_in_sentence(
                sentence,
                entities
            )
            relationships.extend(sent_relationships)

        # Document-level pattern application
        doc_relationships = self._detect_document_patterns(
            entities,
            text
        )
        relationships.extend(doc_relationships)

        # Rule-based inference
        inferred_relationships = self._infer_relationships(
            entities,
            relationships
        )
        relationships.extend(inferred_relationships)

        # Deduplication and confidence scoring
        relationships = self._consolidate_relationships(relationships)

        return relationships

    def _detect_in_sentence(
        self,
        sentence: str,
        entities: List[Dict]
    ) -> List[Relationship]:
        """Detect relationships within a sentence"""

        relationships = []
        sentence_lower = sentence.lower()

        # Try each relationship type
        for rel_type, rel_spec in self.RELATIONSHIP_PATTERNS.items():
            for keyword in rel_spec['keywords']:
                if keyword in sentence_lower:
                    # Find entities in sentence
                    matching_pairs = self._find_entity_pairs(
                        sentence,
                        entities,
                        keyword
                    )

                    for source, target, conf in matching_pairs:
                        relationship = Relationship(
                            source_entity=source['text'],
                            source_type=source['type'],
                            target_entity=target['text'],
                            target_type=target['type'],
                            relationship_type=rel_type.value,
                            confidence=conf,
                            strength=self._calculate_strength(source, target),
                            sentence_context=sentence,
                            reasoning_rules=[f"keyword_pattern:{keyword}"],
                        )
                        relationships.append(relationship)

        return relationships

    def _find_entity_pairs(
        self,
        sentence: str,
        entities: List[Dict],
        keyword: str
    ) -> List[Tuple[Dict, Dict, float]]:
        """Find entity pairs separated by keyword"""

        pairs = []
        sentence_lower = sentence.lower()
        keyword_pos = sentence_lower.find(keyword)

        if keyword_pos == -1:
            return pairs

        # Find entities before and after keyword
        for entity in entities:
            entity_text = entity['text'].lower()
            if entity_text in sentence_lower:
                entity_pos = sentence_lower.find(entity_text)

                for entity2 in entities:
                    if entity == entity2:
                        continue

                    entity2_text = entity2['text'].lower()
                    if entity2_text in sentence_lower:
                        entity2_pos = sentence_lower.find(entity2_text)

                        # Check if entities surround keyword
                        if entity_pos < keyword_pos < entity2_pos:
                            confidence = (entity['confidence'] + entity2['confidence']) / 2.0
                            pairs.append((entity, entity2, confidence))

        return pairs

    def _detect_document_patterns(
        self,
        entities: List[Dict],
        text: str
    ) -> List[Relationship]:
        """Detect document-level patterns"""

        relationships = []

        # Co-occurrence patterns
        cooccurrence_relationships = self._detect_cooccurrence(entities, text)
        relationships.extend(cooccurrence_relationships)

        # Type-based patterns
        type_relationships = self._detect_type_patterns(entities)
        relationships.extend(type_relationships)

        return relationships

    def _detect_cooccurrence(
        self,
        entities: List[Dict],
        text: str
    ) -> List[Relationship]:
        """Detect co-occurrence relationships"""

        relationships = []

        # Paragraph-level co-occurrence
        paragraphs = text.split('\n\n')

        for para in paragraphs:
            para_entities = []

            for entity in entities:
                if entity['text'].lower() in para.lower():
                    para_entities.append(entity)

            # Create relationships between co-occurring entities
            for i, entity1 in enumerate(para_entities):
                for entity2 in para_entities[i+1:]:
                    relationship = Relationship(
                        source_entity=entity1['text'],
                        source_type=entity1['type'],
                        target_entity=entity2['text'],
                        target_type=entity2['type'],
                        relationship_type=RelationshipType.RELATED_TO.value,
                        confidence=0.6,  # Moderate confidence for co-occurrence
                        strength=0.5,
                        sentence_context=para[:100],
                        reasoning_rules=["cooccurrence_pattern"],
                    )
                    relationships.append(relationship)

        return relationships

    def _detect_type_patterns(
        self,
        entities: List[Dict]
    ) -> List[Relationship]:
        """Detect relationships based on entity types"""

        relationships = []

        # Type-based inference rules
        type_rules = {
            ('THREAT_ACTOR', 'MALWARE'): RelationshipType.USES,
            ('THREAT_ACTOR', 'VULNERABILITY'): RelationshipType.EXPLOITS,
            ('ATTACK_VECTOR', 'SYSTEM'): RelationshipType.TARGETS,
            ('VULNERABILITY', 'IMPACT'): RelationshipType.CAUSES,
        }

        for (source_type, target_type), rel_type in type_rules.items():
            source_entities = [e for e in entities if e['type'] == source_type]
            target_entities = [e for e in entities if e['type'] == target_type]

            for source in source_entities:
                for target in target_entities:
                    relationship = Relationship(
                        source_entity=source['text'],
                        source_type=source['type'],
                        target_entity=target['text'],
                        target_type=target['type'],
                        relationship_type=rel_type.value,
                        confidence=0.7,
                        strength=0.6,
                        sentence_context="",
                        reasoning_rules=["type_pattern"],
                    )
                    relationships.append(relationship)

        return relationships

    def _infer_relationships(
        self,
        entities: List[Dict],
        relationships: List[Relationship]
    ) -> List[Relationship]:
        """Infer new relationships using rules"""

        inferred = []

        # Transitive rule: if A uses B and B exploits C, then A can exploit C
        for rel1 in relationships:
            for rel2 in relationships:
                if rel1.target_entity == rel2.source_entity:
                    if rel1.relationship_type == RelationshipType.USES.value and \
                       rel2.relationship_type == RelationshipType.EXPLOITS.value:
                        inferred_rel = Relationship(
                            source_entity=rel1.source_entity,
                            source_type=rel1.source_type,
                            target_entity=rel2.target_entity,
                            target_type=rel2.target_type,
                            relationship_type=RelationshipType.EXPLOITS.value,
                            confidence=rel1.confidence * rel2.confidence * 0.9,  # Decay
                            strength=min(rel1.strength, rel2.strength),
                            sentence_context="",
                            reasoning_rules=["transitive_inference"],
                        )
                        inferred.append(inferred_rel)

        return inferred

    def _consolidate_relationships(
        self,
        relationships: List[Relationship]
    ) -> List[Relationship]:
        """Deduplicate and consolidate relationships"""

        # Group by (source, target, type)
        grouped = defaultdict(list)

        for rel in relationships:
            key = (
                rel.source_entity,
                rel.target_entity,
                rel.relationship_type
            )
            grouped[key].append(rel)

        # Consolidate duplicates
        consolidated = []

        for (source, target, rel_type), rels in grouped.items():
            if rels:
                # Average confidence and strength
                avg_conf = sum(r.confidence for r in rels) / len(rels)
                avg_strength = sum(r.strength for r in rels) / len(rels)
                all_rules = []

                for r in rels:
                    all_rules.extend(r.reasoning_rules)

                consolidated_rel = Relationship(
                    source_entity=source,
                    source_type=rels[0].source_type,
                    target_entity=target,
                    target_type=rels[0].target_type,
                    relationship_type=rel_type,
                    confidence=avg_conf,
                    strength=avg_strength,
                    sentence_context=rels[0].sentence_context,
                    reasoning_rules=list(set(all_rules)),
                    evidence_count=len(rels),
                )
                consolidated.append(consolidated_rel)

        return consolidated

    def _calculate_strength(self, source: Dict, target: Dict) -> float:
        """Calculate relationship strength based on entity confidence"""
        return (source['confidence'] + target['confidence']) / 2.0
```

---

## Relationship Inference Engine

### Rule-Based Inference

```python
# File: backend/services/inference_engine.py

from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
import itertools

@dataclass
class InferenceRule:
    """Rule for relationship inference"""
    name: str
    conditions: List[Tuple[str, str, str]]  # (source_type, rel_type, target_type)
    conclusion: Tuple[str, str]  # (rel_type, confidence_decay)
    description: str

class RuleEngine:
    """Apply inference rules to relationships"""

    def __init__(self):
        self.rules = self._initialize_rules()

    def _initialize_rules(self) -> List[InferenceRule]:
        """Initialize domain-specific inference rules"""

        rules = [
            # Cybersecurity rules
            InferenceRule(
                name="transitive_uses",
                conditions=[
                    ("THREAT_ACTOR", "uses", "TOOL"),
                    ("TOOL", "exploits", "VULNERABILITY"),
                ],
                conclusion=("exploits", 0.85),
                description="If actor uses tool and tool exploits vuln, then actor exploits vuln"
            ),
            InferenceRule(
                name="attack_chain",
                conditions=[
                    ("THREAT_ACTOR", "uses", "MALWARE"),
                    ("MALWARE", "causes", "IMPACT"),
                ],
                conclusion=("causes", 0.90),
                description="If actor uses malware and malware causes impact, then actor causes impact"
            ),
            # Organization rules
            InferenceRule(
                name="person_works_for",
                conditions=[
                    ("PERSON", "related_to", "ORGANIZATION"),
                ],
                conclusion=("works_for", 0.70),
                description="Related person-organization implies works_for"
            ),
            # Geographic rules
            InferenceRule(
                name="location_hierarchy",
                conditions=[
                    ("LOCATION", "part_of", "LOCATION"),
                    ("LOCATION", "located_in", "LOCATION"),
                ],
                conclusion=("part_of", 0.95),
                description="Location parts compose to larger locations"
            ),
        ]

        return rules

    def apply_rules(
        self,
        entities: List[Dict],
        relationships: List[Relationship]
    ) -> List[Relationship]:
        """Apply inference rules to generate new relationships"""

        inferred = []

        for rule in self.rules:
            new_relationships = self._apply_rule(
                rule,
                entities,
                relationships
            )
            inferred.extend(new_relationships)

        return inferred

    def _apply_rule(
        self,
        rule: InferenceRule,
        entities: List[Dict],
        relationships: List[Relationship]
    ) -> List[Relationship]:
        """Apply single rule"""

        new_relationships = []

        # Find matching relationship chains
        for rel_chain in self._find_matching_chains(rule, relationships):
            # Create inferred relationship
            source = rel_chain[0].source_entity
            target = rel_chain[-1].target_entity
            source_type = rel_chain[0].source_type
            target_type = rel_chain[-1].target_type

            # Calculate confidence
            base_confidence = 1.0
            for rel in rel_chain:
                base_confidence *= rel.confidence

            final_confidence = base_confidence * rule.conclusion[1]

            inferred_rel = Relationship(
                source_entity=source,
                source_type=source_type,
                target_entity=target,
                target_type=target_type,
                relationship_type=rule.conclusion[0],
                confidence=min(1.0, final_confidence),
                strength=base_confidence,
                sentence_context="",
                reasoning_rules=[f"inference_rule:{rule.name}"],
            )

            new_relationships.append(inferred_rel)

        return new_relationships

    def _find_matching_chains(
        self,
        rule: InferenceRule,
        relationships: List[Relationship]
    ) -> List[List[Relationship]]:
        """Find chains of relationships matching rule conditions"""

        chains = []

        # For each condition in rule
        matching_rels_per_condition = []

        for source_type, rel_type, target_type in rule.conditions:
            matching = [
                r for r in relationships
                if r.source_type == source_type and
                   r.relationship_type == rel_type and
                   r.target_type == target_type
            ]
            matching_rels_per_condition.append(matching)

        # Find chains that connect (target of one is source of next)
        if matching_rels_per_condition:
            for rel_combo in itertools.product(*matching_rels_per_condition):
                # Check if chain is connected
                connected = True

                for i in range(len(rel_combo) - 1):
                    if rel_combo[i].target_entity != rel_combo[i+1].source_entity:
                        connected = False
                        break

                if connected:
                    chains.append(list(rel_combo))

        return chains
```

---

## Knowledge Graph Construction

### Graph Building

```python
# File: backend/services/knowledge_graph_builder.py

from typing import Dict, List, Set
import networkx as nx
from datetime import datetime

class KnowledgeGraph:
    """Semantic knowledge graph representation"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_properties = {}
        self.edge_properties = {}
        self.metadata = {
            'created': datetime.now().isoformat(),
            'entity_count': 0,
            'relationship_count': 0,
            'densification_ratio': 0.0,
        }

    def add_entity(self, entity_id: str, entity_data: Dict) -> None:
        """Add entity node to graph"""
        self.graph.add_node(
            entity_id,
            **entity_data
        )
        self.node_properties[entity_id] = entity_data
        self.metadata['entity_count'] = len(self.graph.nodes())

    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_data: Dict
    ) -> None:
        """Add relationship edge to graph"""
        self.graph.add_edge(
            source_id,
            target_id,
            **relationship_data
        )
        self.edge_properties[(source_id, target_id)] = relationship_data
        self.metadata['relationship_count'] = len(self.graph.edges())

    def get_entity_neighbors(self, entity_id: str) -> List[str]:
        """Get connected entities"""
        return list(self.graph.neighbors(entity_id))

    def get_shortest_path(self, source_id: str, target_id: str) -> List[str]:
        """Find shortest path between entities"""
        try:
            return nx.shortest_path(self.graph, source_id, target_id)
        except nx.NetworkXNoPath:
            return []

    def get_common_neighbors(self, entity_id1: str, entity_id2: str) -> Set[str]:
        """Find common neighbors"""
        neighbors1 = set(self.graph.neighbors(entity_id1))
        neighbors2 = set(self.graph.neighbors(entity_id2))
        return neighbors1.intersection(neighbors2)

    def get_subgraph(self, entity_ids: List[str]) -> 'KnowledgeGraph':
        """Extract subgraph"""
        subgraph = KnowledgeGraph()
        subgraph.graph = self.graph.subgraph(entity_ids).copy()

        for node_id in entity_ids:
            if node_id in self.node_properties:
                subgraph.node_properties[node_id] = self.node_properties[node_id]

        return subgraph

    def calculate_metrics(self) -> Dict:
        """Calculate graph metrics"""
        metrics = {
            'node_count': len(self.graph.nodes()),
            'edge_count': len(self.graph.edges()),
            'density': nx.density(self.graph),
            'average_clustering': nx.average_clustering(self.graph.to_undirected()),
            'diameter': nx.diameter(self.graph) if nx.is_connected(self.graph.to_undirected()) else None,
            'connected_components': nx.number_connected_components(self.graph.to_undirected()),
        }

        return metrics

    def to_dict(self) -> Dict:
        """Export graph as dictionary"""
        nodes = [
            {
                'id': node,
                **self.graph.nodes[node],
            }
            for node in self.graph.nodes()
        ]

        edges = [
            {
                'source': source,
                'target': target,
                **self.graph.edges[source, target],
            }
            for source, target in self.graph.edges()
        ]

        return {
            'nodes': nodes,
            'edges': edges,
            'metadata': self.metadata,
            'metrics': self.calculate_metrics(),
        }
```

---

## Reasoning & Validation

### Semantic Validation

```python
class SemanticValidator:
    """Validate semantic consistency of relationships"""

    @staticmethod
    def validate_relationship(
        relationship: Relationship,
        entity_types: Dict[str, str]
    ) -> Tuple[bool, List[str]]:
        """Validate relationship semantic consistency"""

        errors = []

        # Check entity types exist
        if relationship.source_entity not in entity_types:
            errors.append(f"Source entity {relationship.source_entity} not found")
        if relationship.target_entity not in entity_types:
            errors.append(f"Target entity {relationship.target_entity} not found")

        # Check relationship type validity
        source_type = entity_types.get(relationship.source_entity, '')
        target_type = entity_types.get(relationship.target_entity, '')

        # Domain-specific validation rules
        valid_type_pairs = {
            'USES': [('THREAT_ACTOR', 'TOOL'), ('THREAT_ACTOR', 'MALWARE')],
            'EXPLOITS': [('THREAT_ACTOR', 'VULNERABILITY'), ('ATTACK_VECTOR', 'VULNERABILITY')],
            'TARGETS': [('THREAT_ACTOR', 'ORGANIZATION'), ('MALWARE', 'SYSTEM')],
        }

        if relationship.relationship_type in valid_type_pairs:
            valid_pairs = valid_type_pairs[relationship.relationship_type]
            if (source_type, target_type) not in valid_pairs:
                errors.append(f"Invalid pair: {source_type} {relationship.relationship_type} {target_type}")

        return len(errors) == 0, errors
```

---

## Entity Linking & Resolution

### Disambiguation

```python
class EntityLinker:
    """Link and disambiguate entities"""

    @staticmethod
    def link_entities(
        entities: List[Dict],
        knowledge_base: Dict
    ) -> List[Dict]:
        """Link entities to knowledge base entries"""

        linked_entities = []

        for entity in entities:
            # Find similar entities in KB
            candidates = EntityLinker._find_candidates(
                entity,
                knowledge_base
            )

            if candidates:
                # Select best match
                best_match = max(
                    candidates,
                    key=lambda x: x['similarity']
                )

                linked_entity = entity.copy()
                linked_entity['kb_id'] = best_match['id']
                linked_entity['kb_match_confidence'] = best_match['similarity']
                linked_entities.append(linked_entity)
            else:
                # No match found
                linked_entities.append(entity)

        return linked_entities

    @staticmethod
    def _find_candidates(
        entity: Dict,
        knowledge_base: Dict,
        threshold: float = 0.7
    ) -> List[Dict]:
        """Find candidate matches in knowledge base"""

        candidates = []

        for kb_entry in knowledge_base.values():
            similarity = EntityLinker._calculate_similarity(
                entity['text'],
                kb_entry['text']
            )

            if similarity >= threshold:
                candidates.append({
                    'id': kb_entry['id'],
                    'text': kb_entry['text'],
                    'type': kb_entry['type'],
                    'similarity': similarity,
                })

        return candidates

    @staticmethod
    def _calculate_similarity(text1: str, text2: str) -> float:
        """Calculate text similarity"""
        from difflib import SequenceMatcher

        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
```

---

## Explainability & Tracing

### Reasoning Traces

```python
@dataclass
class ReasoningTrace:
    """Trace of reasoning steps"""
    relationship: Relationship
    derivation_steps: List[str]
    confidence_score: float
    supporting_evidence: List[str]
    inference_rules_applied: List[str]
    timestamp: datetime

class ExplainabilityGenerator:
    """Generate explanations for inferred relationships"""

    @staticmethod
    def generate_explanation(trace: ReasoningTrace) -> str:
        """Generate human-readable explanation"""

        explanation = f"Relationship: {trace.relationship.source_entity} " + \
                     f"{trace.relationship.relationship_type} " + \
                     f"{trace.relationship.target_entity}\n\n"

        explanation += f"Confidence: {trace.confidence_score:.2%}\n\n"

        explanation += "Reasoning Steps:\n"
        for step in trace.derivation_steps:
            explanation += f"  • {step}\n"

        explanation += "\nRules Applied:\n"
        for rule in trace.inference_rules_applied:
            explanation += f"  • {rule}\n"

        explanation += "\nSupporting Evidence:\n"
        for evidence in trace.supporting_evidence:
            explanation += f"  • {evidence}\n"

        return explanation
```

---

**End of INGESTION_STEP3_OPENSPG_REASONING.md**
*Total Lines: 1,055 | Complete semantic reasoning and knowledge graph construction*
