```
OBSIDIAN INTEGRATION GUIDE:

1. NODE FORMATTING

   A. ENTITY NODES
      - Use consistent double-bracket format: [[Type: Name]]
      - Example: [[Person: Donald Trump]], [[Organization: Pentagon]]
      - Create separate notes for each significant entity
      - Include frontmatter with properties for each entity note
   
   B. FRONTMATTER TEMPLATE
      ```
      ---
      type: person/organization/concept/policy/location/event
      name: "Full Name"
      aliases: ["Alternative Name", "Abbreviation"]
      tags: [relevant, tags, domain]
      created: YYYY-MM-DD
      ---
      ```

2. RELATIONSHIP DOCUMENTATION

   A. IN ENTITY NOTES
      - Include "Relationships" section in each entity note
      - Format: "- [[Related Entity]] - RELATIONSHIP_TYPE (context)"
      - Example: "- [[Organization: Pentagon]] - IMPLEMENTS [[Policy: Transgender Service Policy]] (2025-02-27)"
   
   B. BIDIRECTIONAL LINKING
      - Ensure relationships are documented in both entity notes
      - Use consistent relationship terminology in both directions
      - Example: "IMPLEMENTS" in one direction, "IMPLEMENTED_BY" in the other

3. GRAPH VISUALIZATION

   A. RECOMMENDED SETTINGS
      - Group nodes by type (person, organization, etc.)
      - Color-code by domain or significance
      - Filter by relationship types for focused views
      - Use local graphs for entity-specific relationships
   
   B. CUSTOM CSS SNIPPETS
      ```css
      .graph-view.color-fill-tag {
        color: var(--text-normal);
        font-size: 8px;
      }
      .graph-view.color-fill-person {
        color: #FFC0CB;
      }
      .graph-view.color-fill-organization {
        color: #ADD8E6;
      }
      .graph-view.color-fill-concept {
        color: #90EE90;
      }
      .graph-view.color-fill-policy {
        color: #FFD700;
      }
      ```

4. QUERIES AND FILTERS

   A. DATAVIEW QUERIES
      ```dataview
      TABLE type, tags
      FROM "entities"
      SORT type ASC
      ```
      
      ```dataview
      LIST relationships
      FROM [[Entity Name]]
      ```
   
   B. RECOMMENDED PLUGINS
      - Dataview: For querying and displaying relationship data
      - Graph Analysis: For advanced graph visualization
      - Obsidian Git: For version control of knowledge graph
      - Templater: For consistent entity note creation
```