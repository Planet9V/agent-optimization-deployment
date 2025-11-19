---
title: Specialized Tools Reference (Part 1 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 410
status: published
tags: [neocoder, mcp, documentation]
---


# Specialized Tools Reference

[← Back to Code Analysis Tools](03_Code_Analysis_Tools.md) | [Next: Advanced Topics →](../06_Advanced_Topics/01_Hybrid_Reasoning.md)

## Overview

Specialized tools for research synthesis, decision support, data analysis, and advanced Cypher operations across multiple incarnations.

---

## Research Tools (research incarnation)

### add_research_paper

Registers academic paper in knowledge graph.

**Signature**:
```python
async def add_research_paper(
    title: str,
    authors: list[str],
    year: int,
    doi: str | None = None,
    abstract: str | None = None,
    keywords: list[str] | None = None,
    venue: str | None = None
) -> dict
```

**Example**:
```python
paper = await add_research_paper(
    title="Attention Is All You Need",
    authors=["Vaswani", "Shazeer", "Parmar"],
    year=2017,
    doi="10.48550/arXiv.1706.03762",
    keywords=["transformers", "attention", "deep-learning"],
    venue="NeurIPS 2017"
)
```

---

### create_citation

Creates citation relationship between papers.

**Signature**:
```python
async def create_citation(
    source_paper_id: str,
    target_paper_id: str,
    context: str | None = None,
    citation_type: str = "references"
) -> dict
```

**Citation Types**:
- `references` - Source cites target
- `cited_by` - Reverse citation
- `extends` - Builds upon work
- `refutes` - Contradicts findings

---

### synthesize_knowledge (F-Contraction)

Synthesizes knowledge from multiple sources using F-Contraction methodology.

**Signature**:
```python
async def synthesize_knowledge(
    source_ids: list[str],
    synthesis_method: str = "f_contraction",
    preserve_attribution: bool = True,
    output_format: str = "knowledge_graph"
) -> dict
```

**Parameters**:
- `source_ids` - List of source entity UUIDs
- `synthesis_method` - "f_contraction" (default), "merge", "aggregate"
- `preserve_attribution` - Maintain citation tracking
- `output_format` - "knowledge_graph" or "document"

**Returns**:
```json
{
  "success": true,
  "synthesized_entity_id": "uuid",
  "source_count": 5,
  "citations_preserved": true,
  "confidence_score": 0.85
}
```

**F-Contraction Process**:
1. Retrieve source entities
2. Extract common knowledge patterns
3. Merge with conflict resolution
4. Create synthesized entity
5. Link to sources with DERIVED_FROM
6. Preserve original citations

**Example**:
```python
# Synthesize from multiple papers
synthesis = await synthesize_knowledge(
    source_ids=["paper-1", "paper-2", "paper-3"],
    synthesis_method="f_contraction",
    preserve_attribution=True
)

# Result maintains full provenance:
# SynthesizedKnowledge -[:DERIVED_FROM]-> Source1
# SynthesizedKnowledge -[:DERIVED_FROM]-> Source2
# SynthesizedKnowledge -[:CITED_BY]-> OriginalCitation1
```

---

### find_related_research

Finds related papers via citation network.

**Signature**:
```python
async def find_related_research(
    paper_id: str,
    relationship_type: str = "cites",
    max_depth: int = 2
) -> dict
```

**Relationship Types**:
- `cites` - Papers this paper cites
- `cited_by` - Papers that cite this paper
- `co_cited` - Papers cited together
- `co_author` - Same author papers

---

## Decision Support Tools (decision_support incarnation)

### create_decision

Models a decision problem.

**Signature**:
```python
async def create_decision(
    title: str,
    description: str,
    deadline: str | None = None,
    priority: str = "medium"
) -> dict
```

**Priorities**: low, medium, high, critical

---

### add_alternative

Adds decision alternative/option.

**Signature**:
```python
async def add_alternative(
    decision_id: str,
    name: str,
    description: str,
    pros: list[str] | None = None,
    cons: list[str] | None = None
) -> dict
```

**Example**:
```python
alt = await add_alternative(
    decision_id="dec-123",
    name="PostgreSQL",
    description="Relational database",
    pros=["ACID compliance", "mature ecosystem", "JSON support"],
    cons=["scaling complexity", "schema rigidity"]
)
```

---

### add_criterion

Defines evaluation criterion.

**Signature**:
```python
async def add_criterion(
    name: str,
    weight: float,
    description: str,
    measurement: str = "score_1_10"
) -> dict
```

**Parameters**:
- `weight` - Criterion importance (0.0-1.0, sum should equal 1.0)
- `measurement` - "score_1_10", "boolean", "cost", "time"

---

### evaluate_criteria

Scores alternative against criterion.

**Signature**:
```python
async def evaluate_criteria(
    alternative_id: str,
    criterion_id: str,
    score: float,
    notes: str | None = None
) -> dict
```

---

### calculate_decision_scores

Computes weighted scores for all alternatives.

**Signature**:
```python
async def calculate_decision_scores(
    decision_id: str
) -> dict
```

**Returns**:
```json
{
  "success": true,
  "alternatives": [
    {
      "id": "alt-1",
      "name": "PostgreSQL",
      "total_score": 7.8,
      "criterion_scores": {
        "performance": 8.0,
        "scalability": 7.0,
        "cost": 8.5
      }
    }
  ],
  "recommendation": "alt-1"
}
```

---

### track_decision_outcome

Records decision result and actual outcome.

**Signature**:
```python
async def track_decision_outcome(
    decision_id: str,
    chosen_alternative_id: str,
    rationale: str,
    outcome: str | None = None
) -> dict
```

---

## Data Analysis Tools (data_analysis incarnation)

### register_dataset

Tracks dataset in graph.

**Signature**:
```python
async def register_dataset(
    name: str,
    source: str,
    schema: dict,
    row_count: int | None = None,
    format: str = "csv"
) -> dict
```

**Schema Format**:
```json
{
  "columns": ["id", "name", "email", "created_at"],
  "types": ["integer", "string", "string", "datetime"],
  "constraints": ["id unique", "email unique"]
}
```

---

### create_transformation

Defines data transformation.

**Signature**:
```python
async def create_transformation(
    name: str,
    input_dataset_id: str,
    output_dataset_id: str,
    transformation_type: str,
    logic: str,
    parameters: dict | None = None
) -> dict
```

**Transformation Types**:
- `cleaning` - Remove duplicates, handle nulls
- `filtering` - Filter rows
- `aggregation` - Group and aggregate
- `join` - Combine datasets
- `enrichment` - Add derived columns

**Example**:
```python
transform = await create_transformation(
    name="clean_customer_data",
    input_dataset_id="raw-customers",
    output_dataset_id="cleaned-customers",
    transformation_type="cleaning",
    logic="Remove duplicates, fill missing emails",
    parameters={"strategy": "drop_duplicates", "fill_na": "default@example.com"}
)
```

---

### execute_analysis

Runs data analysis workflow.

**Signature**:
```python
async def execute_analysis(
    name: str,
    dataset_id: str,
    analysis_type: str,
    algorithm: str,
    parameters: dict
) -> dict
```

**Analysis Types**:
- `clustering` - K-means, hierarchical
- `classification` - Decision trees, random forest
- `regression` - Linear, polynomial
- `anomaly_detection` - Outlier detection
- `association` - Market basket analysis

**Example**:
```python
analysis = await execute_analysis(
    name="Customer Segmentation",
    dataset_id="cleaned-customers",
    analysis_type="clustering",
    algorithm="k-means",
    parameters={"n_clusters": 5, "random_state": 42}
)
```

---

### track_data_lineage

Queries data provenance and lineage.

**Signature**:
```python
async def track_data_lineage(
    dataset_id: str,
    direction: str = "upstream",
    max_depth: int = 5
) -> dict
```

**Directions**:
- `upstream` - Source datasets
- `downstream` - Derived datasets
- `both` - Full lineage graph

**Returns**:
```json
{
  "success": true,
  "dataset": {...},
  "lineage": {
    "upstream": ["raw_data", "external_source"],
    "downstream": ["aggregated_data", "ml_features"],
    "transformations": [...]
  },
  "graph": {...}
}
```

---
