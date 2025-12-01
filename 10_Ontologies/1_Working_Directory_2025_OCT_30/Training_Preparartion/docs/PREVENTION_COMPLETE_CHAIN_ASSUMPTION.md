# Prevention Guide: Complete Chain Assumption in NER Training

## Executive Summary

This document captures the critical lesson learned during NER V7 development: **never assume complete attack chains exist in cybersecurity knowledge graphs**. It provides a checklist for future projects to avoid repeating this mistake and describes alternative approaches for handling sparse graph data.

## The Mistake

### What We Assumed (Incorrectly)

```
Assumption: Most CVEs have complete attack chains
Expected: CVE → CWE → CAPEC → ATTACK for majority of records
Reality: <1% of CVEs have complete chains
```

### Why This Assumption Was Costly

1. **Wasted Development Time**: 2 weeks building extraction pipelines for non-existent data
2. **False Validation**: Initial tests on hand-picked examples succeeded, masking the problem
3. **Training Failure**: Insufficient training data (<50 examples) for NER model
4. **Semantic Mismatch Discovery**: Only found 0.3% CWE semantic overlap after investigating training failures

### The CWE Semantic Mismatch Problem

When we discovered complete chains were rare, we investigated why CVE→CWE relationships are so difficult to extract:

```
CVE descriptions: "Buffer overflow in libpng 1.6.37 via crafted PNG file"
CWE descriptions: "Buffer copy without checking size of input"
Semantic overlap: 0.3% (only "buffer" and "overflow" overlap)
```

**Key Insight**: CVE and CWE text live in different semantic spaces:
- CVEs describe specific implementations
- CWEs describe abstract security concepts
- Text similarity approaches fail

## Warning Signs You're Making This Assumption

### Red Flags Checklist

**Before Starting NER Training**:

- [ ] You haven't run a coverage analysis of your knowledge graph
- [ ] You're planning to extract entity chains >2 hops deep
- [ ] You haven't calculated semantic overlap between entity types
- [ ] Your training data depends on complete relationship paths
- [ ] You haven't validated that most records have the relationships you need

### Early Detection Queries

#### 1. Check Relationship Coverage

```cypher
// Analyze relationship completeness
MATCH (cve:CVE)
OPTIONAL MATCH (cve)-[:HAS_WEAKNESS]->(cwe:CWE)
OPTIONAL MATCH (cwe)-[:EXPLOITED_BY]->(capec:CAPEC)
OPTIONAL MATCH (capec)-[:MAPS_TO]->(attack:ATTACK)
RETURN
  count(cve) AS total_cves,
  count(cwe) AS has_cwe,
  count(capec) AS has_capec,
  count(attack) AS has_attack,
  count(cwe) * 100.0 / count(cve) AS cwe_coverage_pct,
  count(capec) * 100.0 / count(cve) AS capec_coverage_pct,
  count(attack) * 100.0 / count(cve) AS attack_coverage_pct
```

**Danger Zone**: If any coverage <5%, complete chains are likely rare.

#### 2. Check Complete Chain Availability

```cypher
// Count complete vs partial chains
MATCH (cve:CVE)
OPTIONAL MATCH path1 = (cve)-[:HAS_WEAKNESS]->(cwe:CWE)
OPTIONAL MATCH path2 = (cve)-[:HAS_WEAKNESS]->(:CWE)-[:EXPLOITED_BY]->(:CAPEC)
OPTIONAL MATCH path3 = (cve)-[:HAS_WEAKNESS]->(:CWE)-[:EXPLOITED_BY]->(:CAPEC)-[:MAPS_TO]->(:ATTACK)
RETURN
  count(path1) AS partial_chains_1,
  count(path2) AS partial_chains_2,
  count(path3) AS complete_chains,
  count(path3) * 100.0 / count(cve) AS complete_chain_percentage
```

**Warning**: If complete_chain_percentage <1%, stop and reconsider your approach.

#### 3. Check Semantic Overlap

```cypher
// Analyze text similarity between entity types
MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)
WITH cve, cwe,
     [w IN split(toLower(cve.description), ' ') WHERE size(w) > 4] AS cve_words,
     [w IN split(toLower(cwe.description), ' ') WHERE size(w) > 4] AS cwe_words
WITH cve, cwe, cve_words, cwe_words,
     [w IN cve_words WHERE w IN cwe_words] AS overlap
RETURN
  avg(size(overlap) * 100.0 / size(cve_words)) AS avg_overlap_pct,
  count(*) AS sample_size
```

**Red Flag**: If avg_overlap_pct <1%, text-based extraction will likely fail.

## Validation Checklist for Future Projects

### Phase 1: Pre-Planning Validation (Before Writing Code)

```yaml
data_validation:
  - action: "Run relationship coverage queries"
    pass_criteria: "Primary relationship >80% coverage"
    fail_criteria: "Primary relationship <50% coverage"

  - action: "Analyze semantic overlap between entity types"
    pass_criteria: "Semantic overlap >5%"
    fail_criteria: "Semantic overlap <1%"

  - action: "Count complete vs partial chains"
    pass_criteria: "Complete chains >10% of data"
    fail_criteria: "Complete chains <1% of data"

  - action: "Review sample of entity pairs manually"
    pass_criteria: "Text similarity evident in majority"
    fail_criteria: "Text similarity rare or absent"
```

### Phase 2: Planning Validation (After Approach Design)

```yaml
approach_validation:
  - action: "Identify minimum required relationships"
    pass_criteria: "Can train on partial chains"
    fail_criteria: "Requires complete chains"

  - action: "Calculate expected training data size"
    pass_criteria: ">1000 training examples"
    fail_criteria: "<100 training examples"

  - action: "Design fallback approach for sparse data"
    pass_criteria: "Partial chain training planned"
    fail_criteria: "No fallback strategy"

  - action: "Validate extraction queries on sample data"
    pass_criteria: "Queries return expected data"
    fail_criteria: "Queries return sparse results"
```

### Phase 3: Implementation Validation (During Development)

```yaml
development_validation:
  - action: "Run extraction on small sample (100 records)"
    pass_criteria: ">80 records have required data"
    fail_criteria: "<20 records have required data"

  - action: "Verify training data format correctness"
    pass_criteria: "All required fields present"
    fail_criteria: "Missing critical fields"

  - action: "Check for semantic overlap in sample"
    pass_criteria: "Overlap matches expectations"
    fail_criteria: "Overlap much lower than expected"

  - action: "Train on small sample to validate approach"
    pass_criteria: "Model learns on sample data"
    fail_criteria: "Model fails to converge"
```

## Alternative Approaches Decision Matrix

### When to Use Each Approach

| Scenario | Data Characteristics | Recommended Approach | Avoid |
|----------|---------------------|---------------------|--------|
| **Abundant Complete Chains** | >10% complete chains | Standard multi-hop NER | Partial chain training |
| **Sparse Complete Chains** | 1-10% complete chains | Partial chain training + augmentation | Assuming completeness |
| **Very Sparse Chains** | <1% complete chains | Partial chain training (NER V7 approach) | Multi-hop extraction |
| **High Semantic Overlap** | >10% text similarity | Text-similarity based extraction | Relationship-only training |
| **Low Semantic Overlap** | <1% text similarity | Relationship-based training (NER V7) | Text-similarity extraction |
| **Mixed Density** | Variable chain completeness | Adaptive training with weights | One-size-fits-all |

### Approach Selection Flowchart

```
START: Need to extract entity chains from knowledge graph
  ↓
[Check relationship coverage]
  ↓
Coverage >80% for all hops?
  ├─ YES → [Check semantic overlap]
  │           ↓
  │         Overlap >10%?
  │           ├─ YES → Use standard multi-hop NER
  │           └─ NO → [Check training data size]
  │                      ↓
  │                    >10,000 examples?
  │                      ├─ YES → Use relationship-aware NER
  │                      └─ NO → Use few-shot learning
  │
  └─ NO → [Check if primary hop >80%]
            ↓
          Primary hop >80%?
            ├─ YES → Use partial chain training (NER V7)
            └─ NO → [Alternative data sources?]
                       ├─ YES → Augment with external data
                       └─ NO → Reconsider if NER is appropriate
```

## Prevention Strategies

### 1. Always Run Coverage Analysis First

```python
#!/usr/bin/env python3
"""
Coverage analysis template - run BEFORE designing extraction approach
"""

from neo4j import GraphDatabase

class CoverageAnalyzer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def analyze_relationships(self, entity_types, relationships):
        """Analyze relationship coverage across entity types"""
        query = """
        MATCH (start:{start_label})
        {optional_matches}
        RETURN
          count(start) AS total,
          {counts}
        """

        # Build dynamic query based on entity types
        optional_matches = []
        counts = []

        for i, (src, rel, tgt) in enumerate(relationships):
            var = f"r{i}"
            optional_matches.append(
                f"OPTIONAL MATCH (start)-[:{rel}]->({var}:{tgt})"
            )
            counts.append(f"count({var}) AS has_{rel.lower()}")

        # Format query
        query = query.format(
            start_label=entity_types[0],
            optional_matches="\n".join(optional_matches),
            counts=",\n".join(counts)
        )

        with self.driver.session() as session:
            result = session.run(query)
            return result.single()

# Usage
analyzer = CoverageAnalyzer("bolt://localhost:7687", "neo4j", "password")
relationships = [
    ("CVE", "HAS_WEAKNESS", "CWE"),
    ("CWE", "EXPLOITED_BY", "CAPEC"),
    ("CAPEC", "MAPS_TO", "ATTACK")
]
coverage = analyzer.analyze_relationships(["CVE"], relationships)

print(f"Total CVEs: {coverage['total']}")
print(f"Has CWE: {coverage['has_has_weakness']} ({coverage['has_has_weakness']/coverage['total']*100:.1f}%)")
print(f"Has CAPEC: {coverage['has_exploited_by']} ({coverage['has_exploited_by']/coverage['total']*100:.1f}%)")
print(f"Has ATTACK: {coverage['has_maps_to']} ({coverage['has_maps_to']/coverage['total']*100:.1f}%)")

# Decision logic
if coverage['has_maps_to'] / coverage['total'] < 0.01:
    print("⚠️  WARNING: Complete chains <1% - DO NOT assume completeness!")
    print("✅ RECOMMENDATION: Use partial chain training approach")
```

### 2. Validate Semantic Overlap Early

```python
#!/usr/bin/env python3
"""
Semantic overlap analysis - run BEFORE text-similarity extraction
"""

def calculate_semantic_overlap(entity_pairs, sample_size=100):
    """Calculate semantic overlap between entity descriptions"""
    import random
    from collections import Counter

    sample = random.sample(entity_pairs, min(sample_size, len(entity_pairs)))

    overlaps = []
    word_pairs = []

    for pair in sample:
        source_words = set(pair["source_desc"].lower().split())
        target_words = set(pair["target_desc"].lower().split())

        # Filter words >4 characters
        source_words = {w for w in source_words if len(w) > 4}
        target_words = {w for w in target_words if len(w) > 4}

        if len(source_words) > 0:
            overlap = len(source_words & target_words)
            overlap_pct = overlap / len(source_words)
            overlaps.append(overlap_pct)

            if overlap > 0:
                word_pairs.append((
                    list(source_words & target_words),
                    pair["source_id"],
                    pair["target_id"]
                ))

    avg_overlap = sum(overlaps) / len(overlaps) if overlaps else 0

    print(f"Average semantic overlap: {avg_overlap*100:.2f}%")
    print(f"Sample size: {len(overlaps)}")
    print(f"\nTop 5 overlapping word pairs:")
    for words, src, tgt in sorted(word_pairs, key=lambda x: len(x[0]), reverse=True)[:5]:
        print(f"  {src} → {tgt}: {words}")

    # Decision logic
    if avg_overlap < 0.01:
        print("\n⚠️  WARNING: Semantic overlap <1% - text similarity unlikely to work!")
        print("✅ RECOMMENDATION: Use relationship-based training, not text similarity")
    elif avg_overlap < 0.05:
        print("\n⚠️  WARNING: Low semantic overlap - text similarity may struggle")
        print("✅ RECOMMENDATION: Consider hybrid relationship + text approach")
    else:
        print("\n✅ Good semantic overlap - text similarity approaches viable")

    return avg_overlap

# Usage
overlap = calculate_semantic_overlap(cve_cwe_pairs, sample_size=100)
```

### 3. Design with Partial Chains in Mind

```python
#!/usr/bin/env python3
"""
Partial chain training framework - handles incomplete chains gracefully
"""

class PartialChainTrainingDataGenerator:
    def __init__(self, required_relationships, optional_relationships):
        """
        required_relationships: List of relationships that MUST exist
        optional_relationships: List of relationships used when available
        """
        self.required = required_relationships
        self.optional = optional_relationships

    def extract_training_examples(self, graph_data):
        """Extract training examples, accepting partial chains"""
        examples = []

        for record in graph_data:
            # Validate required relationships exist
            if not all(rel in record for rel in self.required):
                continue  # Skip if required relationships missing

            # Build training example
            example = {
                "required_entities": {
                    rel: record[rel] for rel in self.required
                },
                "optional_entities": {
                    rel: record.get(rel, None) for rel in self.optional
                },
                "completeness": self._calculate_completeness(record)
            }

            examples.append(example)

        return examples

    def _calculate_completeness(self, record):
        """Calculate what percentage of optional relationships are present"""
        present = sum(1 for rel in self.optional if rel in record and record[rel])
        return present / len(self.optional) if self.optional else 1.0

    def train_with_weights(self, examples, model):
        """Train model with weights based on chain completeness"""
        for example in examples:
            # Weight by completeness
            weight = 0.5 + 0.5 * example["completeness"]
            model.train(example, sample_weight=weight)

# Usage
generator = PartialChainTrainingDataGenerator(
    required_relationships=["CVE", "CWE"],
    optional_relationships=["CAPEC", "ATTACK"]
)

examples = generator.extract_training_examples(graph_data)
print(f"Extracted {len(examples)} training examples")
print(f"Average completeness: {sum(e['completeness'] for e in examples)/len(examples):.2%}")
```

## Lessons Learned Summary

### What We Did Wrong

1. **Assumed data completeness** without verification
2. **Didn't run coverage analysis** before designing approach
3. **Ignored semantic overlap** as a critical factor
4. **Built for rare edge cases** (complete chains) instead of common cases (partial chains)
5. **Validated on hand-picked examples** that were unrepresentative

### What We Should Have Done

1. **Run coverage analysis first** - understand data reality before planning
2. **Calculate semantic overlap** - validate extraction approach feasibility
3. **Design for partial chains** - make incomplete data the default assumption
4. **Validate on random samples** - ensure representative evaluation
5. **Plan fallback approaches** - have alternatives ready when assumptions fail

### Key Takeaways

**GOLDEN RULE**: In knowledge graph NER training, always assume sparsity until proven otherwise.

**Validation Requirements**:
- ✅ Run relationship coverage analysis BEFORE planning
- ✅ Calculate semantic overlap BEFORE extraction design
- ✅ Test on random samples, not hand-picked examples
- ✅ Design partial chain training as default approach
- ✅ Plan for <1% complete chains, hope for more

**Decision Framework**:
```
IF complete_chains <1%:
    → Use partial chain training (NER V7 approach)

IF semantic_overlap <1%:
    → Use relationship-based training, not text similarity

IF training_data <1000:
    → Reconsider if NER is appropriate
    → Consider few-shot learning or rule-based extraction
```

## References

- **NER V7 Approach Evaluation**: `../evaluation/NER_V7_APPROACH_EVALUATION.json`
- **Partial Chain Training Methodology**: `WIKI_PARTIAL_CHAIN_TRAINING.md`
- **Schema Documentation**: `SCHEMA_UPDATE_NER_V7.md`
- **Implementation Guide**: `HOWTO_GENERATE_NER_TRAINING.md`
- **Cypher Queries**: `CYPHER_QUERIES_NER_V7.md`

## Conclusion

The complete chain assumption mistake cost 2 weeks of development time but taught a valuable lesson: **always validate data assumptions before building extraction pipelines**. By following this prevention guide, future projects can avoid this pitfall and choose appropriate approaches based on actual data characteristics, not assumptions.

The partial chain training approach (NER V7) successfully addressed the sparse data problem by:
1. Accepting incomplete chains as valid training examples
2. Focusing on relationship learning rather than text similarity
3. Leveraging abundant CVE→CWE pairs instead of rare complete chains
4. Achieving 73% improvement in CWE entity F1 score

This prevention guide ensures these lessons are applied systematically in future work.
