[[publishing]]
[[pyschometric[]]]
[[lacan]]
[[news]]
[[kb schmea]]

```
KNOWLEDGE GRAPH SCHEMA:

1. NODE TYPES AND PROPERTIES

   A. ENTITY NODES
      - People
        Properties: name, role, organization, significance
        Format: [[Person: Full Name]]
        
      - Organizations
        Properties: name, type, scope, significance
        Format: [[Organization: Full Name]]
        
      - Locations
        Properties: name, type, geographic_context
        Format: [[Location: Full Name]]
        
      - Concepts
        Properties: name, domain, definition
        Format: [[Concept: Full Name]]
        
      - Events
        Properties: name, date, significance
        Format: [[Event: Full Name]]
        
      - Policies
        Properties: name, issuing_entity, date, status
        Format: [[Policy: Full Name]]

   B. DOCUMENT NODES
      - Articles
        Properties: title, author, publication, date, url
        Format: [[Article: Title]]
        
      - Analysis
        Properties: title, creation_date, source_article
        Format: [[Analysis: Title]]
        
      - Narratives
        Properties: title, creation_date, source_analysis
        Format: [[Narrative: Title]]

2. RELATIONSHIP TYPES

   A. ENTITY RELATIONSHIPS
      - IMPLEMENTS (Entity → Policy)
      - AUTHORIZES (Entity → Policy/Action)
      - AFFECTS (Policy/Action → Entity)
      - OPPOSES (Entity → Policy/Action)
      - SUPPORTS (Entity → Policy/Action)
      - REGULATES (Entity → Entity)
      - BELONGS_TO (Entity → Entity)
      - LOCATED_IN (Entity → Location)
      - PRECEDES (Entity → Entity)
      - SUCCEEDS (Entity → Entity)
      
   B. CONCEPTUAL RELATIONSHIPS
      - RELATES_TO (Concept → Concept)
      - INSTANCE_OF (Entity → Concept)
      - CONTRADICTS (Concept → Concept)
      - SUPPORTS (Concept → Concept)
      - PART_OF (Concept → Concept)
      
   C. DOCUMENT RELATIONSHIPS
      - ANALYZES (Analysis → Article)
      - MENTIONS (Article → Entity)
      - REFERENCES (Document → Document)
      - CITES (Document → Entity)
      
   D. PSYCHOANALYTIC RELATIONSHIPS
      - FUNCTIONS_AS_SYMBOLIC (Entity → Concept)
      - MIRRORS (Entity → Entity)
      - REPRESENTS_REAL (Entity/Event → Concept)
      - EMPLOYS_DEFENSE (Entity → Concept)
      - TRANSFERS (Entity → Entity)
      - REPEATS_PATTERN (Event → Event)

3. RELATIONSHIP PROPERTIES
   - date: When the relationship began or occurred
   - context: Situational context of the relationship
   - strength: Strong/Moderate/Weak connection
   - evidence: Textual evidence supporting the relationship
   - power_dynamic: Dominant/Subordinate/Equal
   - certainty: High/Medium/Low confidence in relationship

4. GRAPH STRUCTURE REQUIREMENTS

   A. BIDIRECTIONAL LINKING
      - All entities must use consistent double-bracket format
      - Relationships must be explicitly stated in both directions
      - Each entity should link to relevant concepts
      
   B. METADATA TAGGING
      - All nodes must have appropriate tags for filtering
      - Tags should include domain, type, and significance
      - Consistent tag hierarchy should be maintained
      
   C. GRAPH VISUALIZATION SUPPORT
      - Node types should have consistent prefixes
      - Relationship types should use UPPERCASE_SNAKE_CASE
      - Properties should use camelCase
```