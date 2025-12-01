---
title: Other Incarnations (Part 1 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 427
status: published
tags: [neocoder, mcp, documentation]
---


# Other Incarnations

[← Back to Code Analysis](04_Code_Analysis.md) | [Next: Workflows →](../04_Workflows/01_Template_Overview.md)

## Overview

This page covers four specialized incarnations: **Research**, **Decision Support**, **Data Analysis**, and **Complex System**. Each provides domain-specific tools and schema for their respective workflows.

---

## Research Incarnation

**Incarnation Type**: `research`
**Version**: 1.0.0
**Primary Use Cases**: Literature review, citation tracking, research synthesis, F-Contraction knowledge synthesis

### Capabilities

- **Literature Management**: Track research papers, articles, and sources
- **Citation Networks**: Map citation relationships and influence
- **Knowledge Synthesis**: F-Contraction methodology for merging knowledge with attribution
- **Author Tracking**: Manage author information and collaboration networks
- **Research Workflows**: Organize literature review and synthesis processes

### Schema

**ResearchPaper**:
```cypher
CREATE (paper:ResearchPaper {
  id: randomUUID(),
  title: 'Attention Is All You Need',
  authors: ['Vaswani', 'Shazeer', 'Parmar', 'Uszkoreit'],
  year: 2017,
  doi: '10.48550/arXiv.1706.03762',
  abstract: 'We propose a new simple network architecture...',
  keywords: ['transformers', 'attention', 'neural-networks'],
  citations: 50000,
  venue: 'NeurIPS 2017'
})
```

**Citation**:
```cypher
CREATE (citation:Citation {
  id: randomUUID(),
  source: 'Attention Is All You Need',
  target: 'Neural Machine Translation by Jointly Learning to Align',
  context: 'attention mechanism',
  section: 'related_work',
  page: 3
})
```

**Author**:
```cypher
CREATE (author:Author {
  id: randomUUID(),
  name: 'Ashish Vaswani',
  affiliation: 'Google Brain',
  h_index: 45,
  research_areas: ['deep-learning', 'nlp']
})
```

### Key Tools

**add_research_paper**:
```python
async def add_research_paper(
    title: str,
    authors: list[str],
    year: int,
    doi: str = None,
    abstract: str = None,
    keywords: list[str] = None
) -> dict
```

**create_citation**:
```python
async def create_citation(
    source_paper_id: str,
    target_paper_id: str,
    context: str = None,
    citation_type: str = "references"
) -> dict
```

**synthesize_knowledge** (F-Contraction):
```python
async def synthesize_knowledge(
    source_ids: list[str],
    synthesis_method: str = "f_contraction",
    preserve_attribution: bool = True
) -> dict
```

**find_related_research**:
```python
async def find_related_research(
    paper_id: str,
    relationship_type: str = "cites",
    max_depth: int = 2
) -> dict
```

### F-Contraction Synthesis

**F-Contraction** is NeoCoder's knowledge synthesis methodology that merges information from multiple sources while preserving attribution:

```python
# 1. Collect research papers on a topic
papers = await query_cypher("""
    MATCH (p:ResearchPaper)
    WHERE 'transformers' IN p.keywords
    RETURN collect(p.id) as paper_ids
""")

# 2. Synthesize knowledge with F-Contraction
synthesis = await synthesize_knowledge(
    source_ids=papers["paper_ids"],
    synthesis_method="f_contraction",
    preserve_attribution=True
)

# Result maintains citation graph:
# Synthesized Knowledge → DERIVED_FROM → Source Papers
# Each claim → SUPPORTED_BY → Original Citations
```

### Workflows

**Literature Review**:
```python
# 1. Add papers
paper1 = await add_research_paper(
    title="Attention Is All You Need",
    authors=["Vaswani et al."],
    year=2017
)

# 2. Map citations
await create_citation(
    source_paper_id=paper1["paper_id"],
    target_paper_id=paper2["paper_id"],
    context="attention mechanism"
)

# 3. Find related work
related = await find_related_research(
    paper_id=paper1["paper_id"],
    relationship_type="cited_by",
    max_depth=2
)

# 4. Synthesize findings
synthesis = await synthesize_knowledge(
    source_ids=[paper1["paper_id"], paper2["paper_id"]],
    synthesis_method="f_contraction"
)
```

---

## Decision Support Incarnation

**Incarnation Type**: `decision_support`
**Version**: 1.0.0
**Primary Use Cases**: Multi-criteria decision analysis, alternative evaluation, decision tracking

### Capabilities

- **Decision Modeling**: Structure decision problems in graph
- **Alternative Evaluation**: Track and compare options
- **Criteria Weighting**: Multi-criteria decision analysis (MCDA)
- **Decision History**: Audit trail of decisions and outcomes
- **Impact Analysis**: Evaluate decision consequences

### Schema

**Decision**:
```cypher
CREATE (decision:Decision {
  id: randomUUID(),
  title: 'Select Database Technology',
  description: 'Choose between SQL and NoSQL for project',
  status: 'pending',
  created: datetime(),
  deadline: datetime('2024-02-01'),
  priority: 'high'
})
```

**Alternative**:
```cypher
CREATE (alt:Alternative {
  id: randomUUID(),
  name: 'PostgreSQL',
  description: 'Relational database with JSON support',
  pros: ['ACID compliance', 'mature ecosystem'],
  cons: ['scaling complexity', 'schema rigidity']
})
```

**Criterion**:
```cypher
CREATE (criterion:Criterion {
  id: randomUUID(),
  name: 'Scalability',
  weight: 0.3,
  description: 'Ability to handle growth',
  measurement: 'score_1_10'
})
```

### Key Tools

**create_decision**:
```python
async def create_decision(
    title: str,
    description: str,
    deadline: str = None,
    priority: str = "medium"
) -> dict
```

**add_alternative**:
```python
async def add_alternative(
    decision_id: str,
    name: str,
    description: str,
    pros: list[str] = None,
    cons: list[str] = None
) -> dict
```

**evaluate_criteria**:
```python
async def evaluate_criteria(
    alternative_id: str,
    criterion_id: str,
    score: float,
    notes: str = None
) -> dict
```

**track_decision_outcome**:
```python
async def track_decision_outcome(
    decision_id: str,
    chosen_alternative_id: str,
    rationale: str,
    outcome: str = None
) -> dict
```

### Workflows

**Decision Analysis**:
```python
# 1. Create decision
decision = await create_decision(
    title="Select Database",
    description="Choose DB for new project"
)

# 2. Add alternatives
pg = await add_alternative(decision["decision_id"], "PostgreSQL", "SQL DB")
mongo = await add_alternative(decision["decision_id"], "MongoDB", "NoSQL DB")

# 3. Define criteria with weights
perf = await add_criterion("Performance", weight=0.4)
scale = await add_criterion("Scalability", weight=0.3)
cost = await add_criterion("Cost", weight=0.3)

# 4. Evaluate alternatives
await evaluate_criteria(pg["alternative_id"], perf["criterion_id"], score=8)
await evaluate_criteria(mongo["alternative_id"], perf["criterion_id"], score=7)

# 5. Calculate weighted scores and make decision
scores = await calculate_decision_scores(decision["decision_id"])
await track_decision_outcome(decision["decision_id"], chosen_alt_id, rationale)
```

---

## Data Analysis Incarnation

**Incarnation Type**: `data_analysis`
**Version**: 1.0.0
**Primary Use Cases**: Data pipeline tracking, analysis workflows, dataset versioning, data lineage

### Capabilities

- **Dataset Management**: Track data sources and versions
- **Transformation Tracking**: Map data transformations
- **Analysis Workflows**: Organize analysis pipelines
- **Data Lineage**: Query data provenance
- **Quality Monitoring**: Track data quality metrics

### Schema

**Dataset**:
```cypher
CREATE (dataset:Dataset {
  id: randomUUID(),
  name: 'customer_data_v2',
  source: 'production_db',
  schema: {columns: ['id', 'name', 'email']},
  row_count: 150000,
  created: datetime(),
  format: 'parquet'
})
```

**Transformation**:
```cypher
CREATE (transform:Transformation {
  id: randomUUID(),
  name: 'clean_customer_data',
  type: 'cleaning',
  logic: 'Remove duplicates and null values',
  parameters: {strategy: 'drop_duplicates'},
  created: datetime()
})
```

**Analysis**:
```cypher
CREATE (analysis:Analysis {
  id: randomUUID(),
  name: 'Customer Segmentation',
  type: 'clustering',
  algorithm: 'k-means',
  parameters: {n_clusters: 5},
  results: {silhouette_score: 0.65},
  created: datetime()
})
```

### Key Tools

**register_dataset**:
```python
async def register_dataset(
    name: str,
    source: str,
    schema: dict,
    row_count: int = None,
    format: str = "csv"
) -> dict
```

**create_transformation**:
```python
async def create_transformation(
    name: str,
    input_dataset_id: str,
    output_dataset_id: str,
    transformation_type: str,
    logic: str
) -> dict
```

**execute_analysis**:
```python
async def execute_analysis(
    name: str,
    dataset_id: str,
    analysis_type: str,
    algorithm: str,
    parameters: dict
) -> dict
```

**track_data_lineage**:
```python
async def track_data_lineage(
    dataset_id: str,
    direction: str = "upstream",
    max_depth: int = 5
) -> dict
```

### Workflows

**Data Pipeline**:
```python
# 1. Register raw dataset
raw = await register_dataset(
    name="raw_customers",
    source="production_db",
    schema={"columns": ["id", "name", "email", "signup_date"]},
    row_count=150000
)

# 2. Create transformation
cleaned = await register_dataset(name="cleaned_customers", source="pipeline")
transform = await create_transformation(
    name="clean_data",
    input_dataset_id=raw["dataset_id"],
    output_dataset_id=cleaned["dataset_id"],
    transformation_type="cleaning",
    logic="Remove duplicates and nulls"
)

# 3. Execute analysis
analysis = await execute_analysis(
    name="Customer Segmentation",
    dataset_id=cleaned["dataset_id"],
    analysis_type="clustering",
    algorithm="k-means",
    parameters={"n_clusters": 5}
)

# 4. Track lineage
lineage = await track_data_lineage(
    dataset_id=cleaned["dataset_id"],
    direction="both"
)
```

---
