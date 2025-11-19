---
title: F-Contraction Knowledge Synthesis
category: 06_Advanced_Topics
last_updated: 2025-10-25
line_count: 480
status: published
tags: [neocoder, mcp, documentation]
---

# F-Contraction Knowledge Synthesis

[← Back to Hybrid Reasoning](01_Hybrid_Reasoning.md) | [Next: Vector Integration →](03_Vector_Integration.md)

## Overview

**F-Contraction** is NeoCoder's methodology for synthesizing knowledge from multiple sources while preserving complete attribution and provenance. Unlike simple merging or concatenation, F-Contraction creates new knowledge entities that maintain traceable links to all source material.

## The Problem

Traditional knowledge aggregation faces challenges:

**Simple Merging**: Loses source attribution
```
Source A + Source B = Merged Content
❌ Cannot trace which claims came from which source
```

**Concatenation**: Maintains attribution but creates redundancy
```
Source A | Source B | Source C
❌ Redundant information, no synthesis
❌ Difficult to query holistically
```

**Manual Summarization**: Loses systematization
```
Human creates summary from sources
❌ Not reproducible
❌ Difficult to update as sources change
```

## F-Contraction Approach

F-Contraction (Function-based Contraction) systematically:
1. Extracts knowledge from multiple sources
2. Identifies common patterns and conflicts
3. Creates synthesized entity with merged knowledge
4. Maintains explicit links to all sources
5. Preserves citation chains from sources

```
Source A ─┐
Source B ─┼──> F-Contraction ──> Synthesized Entity
Source C ─┘                           │
                                      ├─[DERIVED_FROM]─> Source A
                                      ├─[DERIVED_FROM]─> Source B
                                      ├─[DERIVED_FROM]─> Source C
                                      ├─[CITED_BY]─> Citation 1 (from Source A)
                                      └─[CITED_BY]─> Citation 2 (from Source B)
```

## Implementation

### Basic F-Contraction

```python
async def f_contraction_synthesis(
    source_ids: list[str],
    preserve_attribution: bool = True
) -> dict:
    """Synthesize knowledge using F-Contraction methodology."""

    # 1. Retrieve source entities
    async with neo4j_session() as session:
        result = await session.run("""
            MATCH (source:KnowledgeEntity)
            WHERE source.id IN $source_ids
            OPTIONAL MATCH (source)-[:CITED_BY]->(citation:Citation)
            RETURN source, collect(citation) as citations
        """, {"source_ids": source_ids})

        sources = [(r["source"], r["citations"]) async for r in result]

    # 2. Extract knowledge from sources
    knowledge_points = []
    all_citations = []

    for source, citations in sources:
        knowledge_points.append({
            "text": source["description"],
            "properties": source["properties"],
            "domain": source["domain"],
            "source_id": source["id"]
        })
        all_citations.extend(citations)

    # 3. Perform synthesis
    # Merge common knowledge, identify conflicts
    synthesized_content = await merge_knowledge_points(knowledge_points)

    # 4. Create synthesized entity
    synth_id = str(uuid.uuid4())
    await session.run("""
        CREATE (synth:KnowledgeEntity {
          id: $id,
          name: $name,
          type: 'synthesized',
          description: $description,
          domain: $domain,
          synthesis_method: 'f_contraction',
          source_count: $source_count,
          created: datetime(),
          properties: $properties
        })
        RETURN synth
    """, {
        "id": synth_id,
        "name": f"Synthesis of {len(sources)} sources",
        "description": synthesized_content["description"],
        "domain": sources[0][0]["domain"],
        "source_count": len(sources),
        "properties": synthesized_content["properties"]
    })

    # 5. Link to sources
    for source, _ in sources:
        await session.run("""
            MATCH (synth:KnowledgeEntity {id: $synth_id})
            MATCH (source:KnowledgeEntity {id: $source_id})
            CREATE (synth)-[:DERIVED_FROM {
              method: 'f_contraction',
              timestamp: datetime()
            }]->(source)
        """, {"synth_id": synth_id, "source_id": source["id"]})

    # 6. Preserve citations
    if preserve_attribution:
        unique_citations = {c["id"]: c for c in all_citations}.values()
        for citation in unique_citations:
            await session.run("""
                MATCH (synth:KnowledgeEntity {id: $synth_id})
                MATCH (citation:Citation {id: $citation_id})
                CREATE (synth)-[:CITED_BY]->(citation)
            """, {"synth_id": synth_id, "citation_id": citation["id"]})

    return {
        "success": True,
        "synthesized_id": synth_id,
        "source_count": len(sources),
        "citations_preserved": len(all_citations)
    }
```

### Knowledge Merging Logic

```python
async def merge_knowledge_points(
    knowledge_points: list[dict]
) -> dict:
    """Merge knowledge points with conflict resolution."""

    # Extract common themes
    all_text = " ".join([kp["text"] for kp in knowledge_points])

    # Identify conflicts
    conflicts = []
    properties = {}

    for key in set().union(*[kp["properties"].keys() for kp in knowledge_points]):
        values = [
            kp["properties"].get(key)
            for kp in knowledge_points
            if key in kp["properties"]
        ]

        # Check for conflicts
        unique_values = set(values)
        if len(unique_values) > 1:
            conflicts.append({
                "property": key,
                "values": list(unique_values),
                "resolution": "multiple_values"
            })
            properties[key] = list(unique_values)  # Store all values
        else:
            properties[key] = values[0]

    # Generate synthesized description
    synthesized_desc = await generate_synthesis_description(
        all_text,
        conflicts
    )

    return {
        "description": synthesized_desc,
        "properties": properties,
        "conflicts": conflicts
    }
```

## Advanced Patterns

### Weighted F-Contraction

Weight sources by credibility or recency:

```python
async def weighted_f_contraction(
    source_data: list[dict]  # [{"id": "...", "weight": 0.8}, ...]
) -> dict:
    """F-Contraction with source weighting."""

    # Weight knowledge points by source credibility
    weighted_points = []

    for item in source_data:
        source = await get_entity_by_id(item["id"])
        weighted_points.append({
            "text": source["description"],
            "weight": item["weight"],
            "source_id": item["id"]
        })

    # Merge with weight consideration
    synthesized = await weighted_merge(weighted_points)

    # Create synthesis with weight metadata
    synth_id = await create_synthesis_entity(
        synthesized,
        metadata={"weights": {s["source_id"]: s["weight"] for s in source_data}}
    )

    return {"synthesized_id": synth_id}
```

### Temporal F-Contraction

Synthesize across time with version tracking:

```python
async def temporal_f_contraction(
    entity_id: str,
    time_range: dict
) -> dict:
    """Synthesize entity evolution over time."""

    # Get all versions in time range
    versions = await neo4j_session.run("""
        MATCH (current:KnowledgeEntity {id: $id})
        OPTIONAL MATCH (current)-[:SUPERSEDES*]->(older:KnowledgeEntity)
        WHERE older.created >= $start_time
          AND older.created <= $end_time
        RETURN collect(older) + [current] as versions
    """, {
        "id": entity_id,
        "start_time": time_range["start"],
        "end_time": time_range["end"]
    })

    version_ids = [v["id"] for v in versions.single()["versions"]]

    # Synthesize across temporal versions
    temporal_synthesis = await f_contraction_synthesis(
        source_ids=version_ids,
        preserve_attribution=True
    )

    # Add temporal metadata
    await neo4j_session.run("""
        MATCH (synth:KnowledgeEntity {id: $synth_id})
        SET synth.temporal_synthesis = true,
            synth.time_range = $time_range
    """, {
        "synth_id": temporal_synthesis["synthesized_id"],
        "time_range": time_range
    })

    return temporal_synthesis
```

### Cross-Domain F-Contraction

Synthesize knowledge across different domains:

```python
async def cross_domain_f_contraction(
    source_ids: list[str],
    target_domain: str
) -> dict:
    """Synthesize knowledge from multiple domains."""

    # Retrieve sources from different domains
    sources = await get_entities_by_ids(source_ids)

    # Identify domain mappings
    domain_mappings = {}
    for source in sources:
        source_domain = source["domain"]
        if source_domain not in domain_mappings:
            domain_mappings[source_domain] = []
        domain_mappings[source_domain].append(source["id"])

    # Perform synthesis with domain context
    synthesis = await f_contraction_synthesis(source_ids)

    # Add cross-domain metadata
    await neo4j_session.run("""
        MATCH (synth:KnowledgeEntity {id: $synth_id})
        SET synth.cross_domain = true,
            synth.source_domains = $domains,
            synth.target_domain = $target_domain
    """, {
        "synth_id": synthesis["synthesized_id"],
        "domains": list(domain_mappings.keys()),
        "target_domain": target_domain
    })

    return synthesis
```

## Use Cases

### 1. Literature Review Synthesis

```python
# Collect research papers
papers = await query_knowledge_graph("""
    MATCH (p:ResearchPaper)
    WHERE 'transformers' IN p.keywords
    RETURN collect(p.id) as paper_ids
""")

# Synthesize findings
synthesis = await f_contraction_synthesis(
    source_ids=papers["paper_ids"],
    preserve_attribution=True
)

# Result: Single synthesized entity with:
# - Combined findings from all papers
# - Links to each source paper
# - Preserved citations from all papers
```

### 2. Code Documentation Generation

```python
# Find related code files
files = await query_knowledge_graph("""
    MATCH (f:File)-[:DEFINES]->(e:CodeEntity)
    WHERE e.name CONTAINS 'Auth'
    RETURN collect(e.id) as entity_ids
""")

# Synthesize documentation
doc_synthesis = await f_contraction_synthesis(
    source_ids=files["entity_ids"]
)

# Result: Comprehensive documentation with:
# - Combined code entity information
# - Links to source files
# - Preserved docstrings and comments
```

### 3. Knowledge Base Evolution

```python
# Get multiple versions of an entity
versions = await get_entity_versions(entity_id="concept-uuid")

# Synthesize evolution
evolution = await temporal_f_contraction(
    entity_id="concept-uuid",
    time_range={"start": "2023-01-01", "end": "2024-01-01"}
)

# Result: Evolution summary with:
# - Changes over time
# - Links to all versions
# - Conflict resolution between versions
```

## Querying Synthesized Knowledge

### Find Synthesis Sources

```cypher
-- Get all sources for a synthesis
MATCH (synth:KnowledgeEntity {id: $synth_id})
MATCH (synth)-[:DERIVED_FROM]->(source:KnowledgeEntity)
RETURN source.name, source.description
ORDER BY source.created
```

### Trace Citation Chain

```cypher
-- Get all citations through synthesis
MATCH (synth:KnowledgeEntity {id: $synth_id})
MATCH (synth)-[:CITED_BY]->(citation:Citation)
OPTIONAL MATCH (synth)-[:DERIVED_FROM]->(source)
                -[:CITED_BY]->(source_citation:Citation)
RETURN collect(DISTINCT citation) as direct_citations,
       collect(DISTINCT source_citation) as source_citations
```

### Find Related Syntheses

```cypher
-- Find other syntheses using same sources
MATCH (synth1:KnowledgeEntity {id: $synth_id})
MATCH (synth1)-[:DERIVED_FROM]->(shared_source)
            <-[:DERIVED_FROM]-(synth2:KnowledgeEntity)
WHERE synth1 <> synth2
RETURN synth2, count(shared_source) as shared_sources
ORDER BY shared_sources DESC
```

## Best Practices

### Source Selection

**Choose compatible sources**:
```python
# Good: Same domain, compatible content
sources = ["paper-1-ai", "paper-2-ai", "paper-3-ai"]
synthesis = await f_contraction_synthesis(sources)

# Avoid: Incompatible domains without cross-domain handling
sources = ["biology-paper", "physics-paper"]  # May need cross-domain approach
```

### Attribution Preservation

**Always track sources**:
```python
# Good: Full attribution
synthesis = await f_contraction_synthesis(
    source_ids=sources,
    preserve_attribution=True  # Preserve all citations
)

# Avoid: Lost attribution
synthesis = simple_merge(sources)  # Citations lost
```

### Conflict Resolution

**Document conflicts explicitly**:
```python
# Store conflicts in synthesis
synthesis_props = {
    "conflicts": [
        {
            "property": "year_introduced",
            "values": [2017, 2018],
            "sources": ["paper-1", "paper-2"]
        }
    ]
}
```

### Update Strategy

**Keep synthesis current**:
```python
# When source updates, re-synthesize
async def update_synthesis_on_source_change(synth_id: str):
    # Get current sources
    sources = await get_synthesis_sources(synth_id)

    # Re-run synthesis
    new_synth = await f_contraction_synthesis([s["id"] for s in sources])

    # Link to previous synthesis
    await link_synthesis_versions(old_id=synth_id, new_id=new_synth["synthesized_id"])
```

## Related Documentation

- [Hybrid Reasoning](01_Hybrid_Reasoning.md) - Overall architecture
- [Research Tools](../05_Tools_Reference/04_Specialized_Tools.md) - Synthesis tools
- [Knowledge Graph](../03_Incarnations/03_Knowledge_Graph.md) - Entity management
- [Graph Structure](../02_Core_Concepts/03_Graph_Structure.md) - Schema details

---
*Last Updated: 2025-10-24 | [Report Issues](https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow/issues)*
