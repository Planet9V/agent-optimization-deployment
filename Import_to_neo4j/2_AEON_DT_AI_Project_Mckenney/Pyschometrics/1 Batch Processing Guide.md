[[publishing]]
[[pyschometric[]]]
[[lacan]]
[[news]]

## Batch Processing Guide

```markdown
# Batch Processing Guide

This system processes multiple news articles in two distinct phases:

## Phase 1: Analysis and Knowledge Graph Extraction

1. Place all news articles in the "articles/" directory
2. Run the Phase 1 prompt, providing the list of article filenames
3. The system will create atomic notes in the "atomic_notes/" directory
4. Each atomic note contains comprehensive analysis and knowledge graph elements

## Phase 2: Narrative Composition

1. Ensure all analyses are in the "atomic_notes/" directory
2. Run the Phase 2 prompt, providing the list of analysis filenames
3. The system will create narratives in the "narratives/" directory
4. The system will generate Neo4j Cypher queries in the "cypher_queries/" directory

## Processing Large Batches

For large numbers of articles:
1. Process in smaller batches of 5-10 articles
2. Complete both Phase 1 and Phase 2 for each batch before proceeding
3. Monitor output quality for consistency

## Output Verification

After processing:
1. Verify all atomic notes include knowledge graph elements
2. Check that narratives maintain objectivity
3. Test Cypher queries in Neo4j to ensure proper import
4. Import entity notes into Obsidian to visualize the knowledge graph

## Customization

To customize the process:
1. Modify the artifacts as needed for specific use cases
2. Adjust the templates to include additional sections
3. Update the knowledge graph schema for specialized domains