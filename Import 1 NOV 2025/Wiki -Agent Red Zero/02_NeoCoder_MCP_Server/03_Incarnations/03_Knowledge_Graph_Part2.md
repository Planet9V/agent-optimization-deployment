---
title: 03_Knowledge_Graph_Part1 (Part 2 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 44
status: published
tags: [neocoder, mcp, documentation]
---

## Best Practices

### Entity Design

**Naming Conventions**:
- Use clear, descriptive entity names
- Maintain consistent naming across domain
- Use properties for aliases and variations
- Tag entities for discovery

**Type System**:
- Define standard entity types (concept, fact, process, etc.)
- Use consistent typing across knowledge base
- Document custom entity types
- Enforce type constraints where applicable

### Relationship Modeling

**Relationship Types**:
- Use established relationship vocabulary
- Define relationship semantics clearly
- Add properties for relationship metadata
- Avoid creating redundant relationship types

**Graph Structure**:
- Keep hierarchies manageable (max 5-7 levels)
- Create bidirectional relationships where appropriate
- Avoid circular dependencies
- Use strength/confidence properties

### Knowledge Quality

**Citation Tracking**:
- Always cite knowledge sources
- Track citation credibility
- Link entities to supporting evidence
- Identify contradictions

**Maintenance**:
- Review and update entities regularly
- Archive outdated knowledge
- Resolve contradictions
- Validate relationship integrity
