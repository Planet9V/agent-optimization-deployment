# Standard Operating Procedure for Knowledge Graph Content Extraction

## Purpose
This SOP provides a standardized framework for deconstructing news articles and content snippets into structured knowledge graph components that can be seamlessly integrated into Neo4j and Obsidian graph systems.

## Template Structure

```markdown
---
title: "[Concise Article Title]"
source: "[Original URL]"
author: "[Source Publication/Author]"
published: YYYY-MM-DD
created: YYYY-MM-DD
description: "[1-2 sentence summary of content]"
tags:
  - "[primary topic]"
  - "[secondary topic]"
  - "[relevant domain]"
  - "[key entities]"
  - "clippings"
entities:
  people:
    - "[[Full Name]]"
    - "[[Full Name with Title]]"
  organizations:
    - "[[Organization Name]]"
    - "[[Agency/Institution Name]]"
  locations:
    - "[[City/Region]]"
    - "[[Country]]"
  concepts:
    - "[[Abstract Concept]]"
    - "[[Policy Area]]"
    - "[[Theoretical Framework]]"
relationships:
  - source: "[[Entity A]]"
    relation: "ACTION_VERB"
    target: "[[Entity B]]"
    properties:
      date: "YYYY-MM-DD"
      context: "[additional context]"
  - source: "[[Entity C]]"
    relation: "ACTION_VERB"
    target: "[[This Article]]"
    properties:
      impact: "[descriptor]"
      significance: "[high/medium/low]"
---

# [Full Article Title]

[2-3 sentence comprehensive summary of the content]

## Key Points
- [Concise factual statement]
- [Concise factual statement]
- [Concise factual statement]

## Timeline
- [Date]: [Event]
- [Date]: [Event]
- [Date]: [Event]

## Impact Analysis
- [Quantitative data point]
- [Qualitative assessment]
- [Expert perspective]

## Related [Policies/Stories/Events]
- [[Related Item 1]]
- [[Related Item 2]]
- [[Related Item 3]]

## Media Coverage
- Left-leaning sources ([percentage]%): [Focus/Framing]
- Center sources ([percentage]%): [Focus/Framing]
- Right-leaning sources ([percentage]%): [Focus/Framing]

## Connections
→ [Outgoing relationship to other node]
→ [Outgoing relationship to other node]
← [Incoming relationship from other node]
← [Incoming relationship from other node]
↔ [Bidirectional relationship with other node]
```

## Extraction Process

1. **Initial Content Analysis**
   - Read the full article/snippet
   - Identify the primary topic and key entities
   - Note publication date, source, and author

2. **Entity Extraction**
   - Identify all people mentioned (full names with titles where available)
   - List all organizations, institutions, and agencies
   - Document all locations referenced (cities, regions, countries)
   - Extract abstract concepts, policies, and theoretical frameworks

3. **Relationship Mapping**
   - For each entity pair with a clear relationship:
     - Define the source entity (who/what is acting)
     - Specify the relationship verb in UPPERCASE_SNAKE_CASE
     - Identify the target entity (who/what is being acted upon)
     - Document properties of the relationship (when, how, why)

4. **Temporal Structuring**
   - Create a chronological timeline of events mentioned
   - Note when relationships began, changed, or ended
   - Document publication date and any future dates mentioned

5. **Impact Assessment**
   - Evaluate quantitative impacts (numbers, statistics, measurements)
   - Assess qualitative impacts (descriptions, characterizations)
   - Note expert opinions and predictions

6. **Connection Visualization**
   - Use directional arrows to show relationship flow:
     - → for outgoing relationships from this topic
     - ← for incoming relationships to this topic
     - ↔ for bidirectional relationships

7. **Media Analysis**
   - Document the political leaning of sources covering the topic
   - Note percentage distribution across the spectrum
   - Summarize how different perspectives frame the issue

## Neo4j Integration Notes

- Each entity becomes a node with appropriate labels
- Relationships use the ACTION_VERB as the relationship type
- Properties are attached to both nodes and relationships
- Temporal data is formatted for time-series analysis

## Obsidian Integration Notes

- Use double-bracket notation for all entities
- Maintain consistent naming conventions across all notes
- Include the article itself as a node in relationships
- Use tags for filtering and categorization

## Quality Control Checklist

- [ ] All entities properly identified and categorized
- [ ] Relationships include source, action, target, and properties
- [ ] Timeline events are in chronological order with accurate dates
- [ ] Connections section shows both incoming and outgoing relationships
- [ ] Media coverage analysis includes percentage distribution
- [ ] All links use proper double-bracket Obsidian format
- [ ] Metadata section is complete with all required fields

## Example Transformation

**Original Snippet:**
"President Smith announced new climate regulations yesterday that will require major corporations to reduce emissions by 30% within five years. Industry groups, led by the National Business Association, immediately criticized the move as 'economically devastating,' while environmental organizations praised the decision."

**Transformed Knowledge Graph Components:**

```
entities:
  people:
    - "[[President Smith]]"
  organizations:
    - "[[National Business Association]]"
    - "[[Environmental Organizations]]"
  concepts:
    - "[[Climate Regulations]]"
    - "[[Emissions Reduction]]"

relationships:
  - source: "[[President Smith]]"
    relation: "ANNOUNCED"
    target: "[[Climate Regulations]]"
    properties:
      date: "2025-02-26"
      context: "official statement"
  - source: "[[Climate Regulations]]"
    relation: "REQUIRES"
    target: "[[Major Corporations]]"
    properties:
      requirement: "30% emissions reduction"
      timeframe: "5 years"
  - source: "[[National Business Association]]"
    relation: "CRITICIZED"
    target: "[[Climate Regulations]]"
    properties:
      characterization: "economically devastating"
      timing: "immediate"
```