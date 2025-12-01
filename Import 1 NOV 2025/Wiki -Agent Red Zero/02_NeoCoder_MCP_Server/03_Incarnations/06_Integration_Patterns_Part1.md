---
title: Integration Patterns (Part 1 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 456
status: published
tags: [neocoder, mcp, documentation]
---


# Integration Patterns

[← Back to Other Incarnations](05_Other_Incarnations.md) | [Next: Creating Incarnations →](07_Creating_Incarnations.md)

## Overview

Cross-incarnation integration patterns enable sophisticated workflows that combine capabilities from multiple incarnations. This guide demonstrates proven patterns for coordinating work across incarnations, sharing data between schemas, and building complex multi-incarnation pipelines.

## Pattern Categories

### Sequential Patterns
Execute incarnations in sequence, with each phase building on previous results

### Parallel Patterns
Run multiple incarnations concurrently on independent data

### Hierarchical Patterns
Organize incarnations in parent-child relationships for complex workflows

### Hybrid Patterns
Combine sequential and parallel execution for optimal performance

## Core Integration Patterns

### Pattern 1: Code-to-Knowledge Pipeline

**Use Case**: Analyze codebase structure and create knowledge graph representation

**Incarnations**: `code_analysis` → `knowledge_graph`

**Workflow**:
```python
# Phase 1: Code Analysis Incarnation
await switch_incarnation("code_analysis")

# Analyze project structure
analysis = await analyze_code_structure(
    file_path="src/auth/login.py",
    analysis_depth=3,
    include_ast=True
)

# Extract entities (classes, functions, imports)
code_entities = await get_code_entities(
    file_path="src/auth/login.py"
)

# Phase 2: Knowledge Graph Incarnation
await switch_incarnation("knowledge_graph")

# Create knowledge entities from code analysis
for entity in code_entities:
    await create_knowledge_entity(
        name=entity["name"],
        entity_type="technology",
        description=f"{entity['type']} in authentication system",
        domain="software_engineering",
        properties={
            "code_entity_id": entity["id"],
            "file_path": "src/auth/login.py",
            "complexity": entity.get("complexity", 0)
        }
    )

# Create relationships based on code dependencies
for dependency in analysis["dependencies"]:
    await create_relationship(
        source_id=dependency["from_id"],
        target_id=dependency["to_id"],
        relationship_type="DEPENDS_ON",
        description=f"Code dependency: {dependency['type']}"
    )
```

**Benefits**:
- Code structure preserved in knowledge graph
- Enables semantic queries on code relationships
- Documents technical architecture in graph form

### Pattern 2: Research-to-Knowledge Synthesis

**Use Case**: Process research papers and synthesize knowledge entities

**Incarnations**: `research` → `knowledge_graph`

**Workflow**:
```python
# Phase 1: Research Incarnation
await switch_incarnation("research")

# Add research papers
papers = [
    {"title": "Hybrid Reasoning Systems", "authors": ["Smith", "Jones"], "year": 2023},
    {"title": "Graph Neural Networks", "authors": ["Lee", "Chen"], "year": 2024}
]

paper_ids = []
for paper in papers:
    result = await add_research_paper(
        title=paper["title"],
        authors=paper["authors"],
        year=paper["year"]
    )
    paper_ids.append(result["paper_id"])

# Perform F-Contraction synthesis
synthesis = await f_contraction_synthesis(
    source_ids=paper_ids,
    preserve_attribution=True
)

# Phase 2: Knowledge Graph Incarnation
await switch_incarnation("knowledge_graph")

# Create knowledge entity from synthesis
await create_knowledge_entity(
    name=synthesis["topic"],
    entity_type="concept",
    description=synthesis["synthesized_content"],
    domain="research",
    properties={
        "synthesis_id": synthesis["id"],
        "source_count": len(paper_ids),
        "confidence": synthesis["confidence_score"]
    }
)

# Link to original research citations
for paper_id in paper_ids:
    await create_relationship(
        source_id=synthesis["entity_id"],
        target_id=paper_id,
        relationship_type="DERIVED_FROM",
        description="Synthesized from research paper"
    )
```

**Benefits**:
- Research insights preserved with full attribution
- Citation networks integrated with knowledge graph
- F-Contraction synthesis maintains source traceability

### Pattern 3: Decision-Supported Development

**Use Case**: Use decision analysis to guide development choices

**Incarnations**: `decision_support` → `coding`

**Workflow**:
```python
# Phase 1: Decision Support Incarnation
await switch_incarnation("decision_support")

# Model architecture decision
decision = await create_decision(
    name="Choose Database Technology",
    description="Select database for authentication service",
    decision_type="technical_architecture"
)

# Add alternatives
alternatives = [
    {"name": "PostgreSQL", "description": "Relational database"},
    {"name": "MongoDB", "description": "Document database"},
    {"name": "Neo4j", "description": "Graph database"}
]

for alt in alternatives:
    await add_alternative(
        decision_id=decision["id"],
        name=alt["name"],
        description=alt["description"]
    )

# Evaluate against criteria
criteria = ["scalability", "query_performance", "data_model_fit"]
await evaluate_criteria(
    decision_id=decision["id"],
    criteria_weights={
        "scalability": 0.3,
        "query_performance": 0.4,
        "data_model_fit": 0.3
    }
)

# Get recommended alternative
recommendation = await get_decision_recommendation(decision["id"])
chosen = recommendation["recommended_alternative"]

# Phase 2: Coding Incarnation
await switch_incarnation("coding")

# Create project with chosen technology
project = await create_project(
    name="AuthService",
    root_path="/src/auth-service",
    metadata={
        "database": chosen["name"],
        "decision_id": decision["id"],
        "rationale": recommendation["rationale"]
    }
)

# Execute setup workflow for chosen database
await execute_workflow(
    template_keyword="SETUP_DATABASE",
    parameters={
        "project_id": project["id"],
        "database_type": chosen["name"].lower()
    }
)
```

**Benefits**:
- Systematic decision-making documented in graph
- Architecture choices linked to project metadata
- Decision rationale preserved for future reference

### Pattern 4: Data-Driven System Modeling

**Use Case**: Analyze data pipeline and model as complex system

**Incarnations**: `data_analysis` → `complex_system`

**Workflow**:
```python
# Phase 1: Data Analysis Incarnation
await switch_incarnation("data_analysis")

# Register datasets
source_dataset = await register_dataset(
    name="User Events",
    source="kafka://events",
    schema={"user_id": "string", "event_type": "string", "timestamp": "datetime"}
)

# Define transformations
transform1 = await create_transformation(
    name="Aggregate Events",
    input_dataset_id=source_dataset["id"],
    transformation_type="aggregation",
    parameters={"window": "1hour", "group_by": "user_id"}
)

# Execute analysis
analysis = await execute_analysis(
    dataset_id=source_dataset["id"],
    analysis_type="pipeline_performance"
)

# Phase 2: Complex System Incarnation
await switch_incarnation("complex_system")

# Create system components from data pipeline
for stage in analysis["pipeline_stages"]:
    await create_system_component(
        name=stage["name"],
        component_type="data_processor",
        properties={
            "throughput": stage["throughput"],
            "latency": stage["latency"],
            "error_rate": stage["error_rate"]
        }
    )

# Model interactions
for interaction in analysis["stage_interactions"]:
    await define_interaction(
        source_component=interaction["from"],
        target_component=interaction["to"],
        interaction_type="data_flow",
        properties={
            "volume": interaction["volume"],
            "frequency": interaction["frequency"]
        }
    )

# Run system simulation
simulation = await run_simulation(
    scenario="peak_load",
    parameters={"load_multiplier": 3}
)
```

**Benefits**:
- Data pipeline modeled as system dynamics
- Performance bottlenecks identified through simulation
- System-level optimization opportunities revealed

## Advanced Integration Patterns

### Pattern 5: Full-Stack Development Pipeline

**Incarnations**: `coding` → `code_analysis` → `knowledge_graph` → `decision_support`

**Use Case**: Complete development workflow with analysis and documentation

```python
# 1. Coding: Create project structure
await switch_incarnation("coding")
project = await create_project(name="APIGateway", root_path="/src/gateway")

# 2. Code Analysis: Analyze implementation
await switch_incarnation("code_analysis")
analysis = await analyze_code_structure(file_path="src/gateway/router.py")

# 3. Knowledge Graph: Document architecture
await switch_incarnation("knowledge_graph")
await create_knowledge_entity(
    name="API Gateway Architecture",
    type="architecture",
    properties={"complexity": analysis["metrics"]["complexity"]}
)

# 4. Decision Support: Track technical decisions
await switch_incarnation("decision_support")
await create_decision(
    name="Choose Routing Strategy",
    alternatives=["path_based", "header_based", "weighted"]
)
```

### Pattern 6: Research-Informed Development

**Incarnations**: `research` → `knowledge_graph` → `coding` → `code_analysis`

**Use Case**: Implement algorithms from research papers

```python
# 1. Research: Find and synthesize papers on algorithm
await switch_incarnation("research")
papers = await search_research_papers(query="graph traversal algorithms")
synthesis = await f_contraction_synthesis(source_ids=[p["id"] for p in papers])

# 2. Knowledge Graph: Model algorithm concepts
await switch_incarnation("knowledge_graph")
algorithm_entity = await create_knowledge_entity(
    name="Optimized Graph Traversal",
    description=synthesis["content"],
    domain="algorithms"
)

# 3. Coding: Implement algorithm
await switch_incarnation("coding")
project = await create_project(name="GraphLib", root_path="/src/graphlib")
await add_file_to_project(project["id"], "src/traversal.py")

# 4. Code Analysis: Verify implementation complexity
await switch_incarnation("code_analysis")
impl_analysis = await analyze_code_structure(file_path="src/traversal.py")
# Compare implementation complexity to theoretical expectations
```

### Pattern 7: Continuous Knowledge Evolution

**Incarnations**: Cyclical between `knowledge_graph`, `research`, and `code_analysis`

**Use Case**: Maintain up-to-date knowledge base from multiple sources

```python
async def knowledge_evolution_cycle():
    """Run continuous knowledge update cycle."""

    # Monitor new code
    await switch_incarnation("code_analysis")
    new_code_entities = await get_recent_code_entities(days=7)

    # Check for research updates
    await switch_incarnation("research")
    new_papers = await check_new_research(topics=["AI", "databases"])

    # Update knowledge graph
    await switch_incarnation("knowledge_graph")

    # Integrate code insights
    for entity in new_code_entities:
        await update_knowledge_from_code(entity)

    # Integrate research insights
    for paper in new_papers:
        await update_knowledge_from_research(paper)

    # Identify knowledge gaps
    gaps = await identify_knowledge_gaps()

    # Return to research to fill gaps
    if gaps:
        await switch_incarnation("research")
        await search_research_to_fill_gaps(gaps)
```

## Data Sharing Patterns

### Cross-Schema Queries

**Direct Cypher Queries**:
```cypher
-- Query across coding and knowledge_graph schemas
MATCH (project:Project {name: 'AuthService'})
MATCH (project)-[:HAS_FILE]->(file:File)
MATCH (file)-[:DEFINES]->(code_entity:CodeEntity)
MATCH (knowledge:KnowledgeEntity {domain: 'authentication'})
MATCH path = (code_entity)-[*1..2]-(knowledge)
RETURN project, file, code_entity, knowledge, path
```

### Entity Linking

**Pattern**: Create RELATES_TO relationships across incarnation schemas

```python
# Link code entity to knowledge entity
async def link_code_to_knowledge(code_entity_id: str, knowledge_entity_id: str):
    """Create cross-incarnation relationship."""
    query = """
    MATCH (code:CodeEntity {id: $code_id})
    MATCH (knowledge:KnowledgeEntity {id: $knowledge_id})
    CREATE (code)-[:IMPLEMENTS]->(knowledge)
    RETURN code, knowledge
    """

    async with driver.session() as session:
        result = await session.run(query, {
            "code_id": code_entity_id,
            "knowledge_id": knowledge_entity_id
        })
        return result.single()
```

### Metadata Propagation

**Pattern**: Share metadata through common property namespaces

```python
# Common metadata structure across incarnations
common_metadata = {
    "project_id": "proj-123",  # Links to coding incarnation
    "domain": "authentication",  # Links to knowledge_graph
    "decision_id": "dec-456",  # Links to decision_support
    "created_by": "claude",
    "created_at": datetime.now().isoformat()
}

# Apply to entities in any incarnation
await create_knowledge_entity(
    name="Auth System",
    properties=common_metadata
)

await create_code_entity(
    name="LoginHandler",
    properties=common_metadata
)
```
