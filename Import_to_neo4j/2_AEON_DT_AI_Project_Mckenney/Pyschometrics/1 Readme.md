[[publishing]]
[[pyschometric[]]]
[[lacan]]
[[news]]

# Psychoanalytic Knowledge Graph System for News Analysis

## Overview

This system transforms news articles into comprehensive analyses and engaging narratives while extracting structured knowledge graph elements for visualization and database integration. It employs psychoanalytic frameworks, bias analysis, and connection mapping to reveal deeper patterns and relationships within news content.

The system operates as a two-phase batch process:
1. **Analysis Phase**: Extracts knowledge and creates structured atomic notes
2. **Composition Phase**: Transforms analyses into engaging narratives and database queries

## Directory Structure

```
project/
├── prompts/                      # Core system prompts
│   ├── phase1_analysis_prompt.txt
│   └── phase2_narrative_prompt.txt
│
├── artifacts/                    # Reference frameworks and templates
│   ├── artifact_1_psychoanalytic_framework.txt
│   ├── artifact_2_bias_analysis_framework.txt
│   ├── artifact_3_analysis_template.txt
│   ├── artifact_4_objectivity_checklist.txt
│   ├── artifact_5_countertransference_guide.txt
│   ├── artifact_6_narrative_techniques.txt
│   ├── artifact_7_narrative_template.txt
│   ├── artifact_8_reader_engagement.txt
│   ├── artifact_9_knowledge_graph_schema.txt
│   ├── artifact_10_neo4j_cypher_template.txt
│   ├── artifact_11_obsidian_integration_guide.txt
│   ├── artifact_12_connection_exploration_framework.txt
│   └── artifact_13_connection_visualization_techniques.txt
│
├── articles/                     # Input news articles
│   ├── article1.txt
│   ├── article2.txt
│   └── article3.txt
│
├── atomic_notes/                 # Phase 1 outputs
│   # Analysis files generated from articles
│
├── narratives/                   # Phase 2 narrative outputs
│   # Narrative files generated from analyses
│
├── cypher_queries/               # Phase 2 database outputs
│   # Neo4j query files generated from analyses
│
├── entity_notes/                 # Knowledge graph entity notes
│   # Individual entity files for Obsidian
│
├── examples/                     # Example inputs and outputs
│   ├── example_article.txt
│   ├── example_analysis.md
│   ├── example_narrative.md
│   ├── example_knowledge_graph.md
│   ├── example_cypher_queries.txt
│   └── example_connection_map.md
│
└── batch_processing_guide.md     # Detailed implementation guide
```

## Quick Start Guide

### 1. Setup

1. Clone or download this repository
2. Place news articles in the `articles/` directory
3. Ensure all artifact files are in the `artifacts/` directory

### 2. Run Phase 1: Analysis

1. Open the `prompts/phase1_analysis_prompt.txt` file
2. Replace `[LIST OF ARTICLE FILENAMES IN articles/ DIRECTORY]` with your actual article filenames
3. Submit the prompt to a capable AI assistant
4. The AI will process each article and create atomic notes in the `atomic_notes/` directory

### 3. Run Phase 2: Composition

1. Open the `prompts/phase2_narrative_prompt.txt` file
2. Replace `[LIST OF ANALYSIS FILENAMES IN atomic_notes/ DIRECTORY]` with your actual analysis filenames
3. Submit the prompt to a capable AI assistant
4. The AI will process each analysis and create narratives in the `narratives/` directory and Cypher queries in the `cypher_queries/` directory

### 4. Knowledge Graph Integration

1. Import entity notes into Obsidian following the `artifact_11_obsidian_integration_guide.txt`
2. Import Cypher queries into Neo4j following standard database procedures

## System Components

### Core Prompts

- **Phase 1 Prompt**: Orchestrates the analysis process, including psychoanalytic analysis, bias analysis, and knowledge graph extraction
- **Phase 2 Prompt**: Orchestrates the composition process, transforming analyses into engaging narratives and database queries

### Key Artifacts

- **Psychoanalytic Framework**: Lacanian registers, discourse positions, and psychological patterns
- **Bias Analysis Framework**: Publication context, framing devices, inclusion/exclusion patterns
- **Knowledge Graph Schema**: Entity types, relationship types, and properties for graph databases
- **Connection Exploration Framework**: Political, historical, psychological, and media ecosystem connections
- **Templates**: Structured formats for analyses, narratives, and database queries

### Outputs

- **Atomic Notes**: Comprehensive analyses with psychoanalytic dimensions and knowledge graph elements
- **Narratives**: Engaging, balanced content that presents multiple perspectives
- **Cypher Queries**: Database import statements for Neo4j integration
- **Entity Notes**: Individual files for each significant entity in the knowledge graph

## Detailed Implementation Guide

For complete implementation instructions, see the `batch_processing_guide.md` file.

---

# Batch Processing Guide

## Overview

This guide provides detailed instructions for implementing the Psychoanalytic Knowledge Graph System as a batch process. The system processes multiple news articles in two distinct phases, creating structured analyses, engaging narratives, and knowledge graph components.

## Prerequisites

- A capable AI assistant with access to the system prompts and artifacts
- News articles in text format
- Basic understanding of knowledge graphs (for advanced usage)
- Obsidian and/or Neo4j (for visualization and database integration)

## Phase 1: Analysis and Knowledge Graph Extraction

### Preparation

1. Place all news articles in the `articles/` directory
2. Create a list of the article filenames
3. Ensure all artifacts are in the `artifacts/` directory

### Execution

1. Open the `prompts/phase1_analysis_prompt.txt` file
2. Replace `[LIST OF ARTICLE FILENAMES IN articles/ DIRECTORY]` with your actual article filenames
3. Submit the prompt to a capable AI assistant
4. The AI will process each article sequentially

### Output

For each article, the system will:
- Create an atomic note with comprehensive analysis
- Extract knowledge graph elements (entities, relationships, properties)
- Map connection networks across multiple dimensions
- Save the analysis to the `atomic_notes/` directory

### Verification

After Phase 1 completes:
1. Check that all articles have corresponding analysis files
2. Verify that each analysis includes knowledge graph elements
3. Ensure connection networks are mapped comprehensively
4. Confirm that all analyses meet objectivity standards

## Phase 2: Narrative Composition and Database Integration

### Preparation

1. Ensure all analyses are in the `atomic_notes/` directory
2. Create a list of the analysis filenames
3. Create the `narratives/` and `cypher_queries/` directories if they don't exist

### Execution

1. Open the `prompts/phase2_narrative_prompt.txt` file
2. Replace `[LIST OF ANALYSIS FILENAMES IN atomic_notes/ DIRECTORY]` with your actual analysis filenames
3. Submit the prompt to a capable AI assistant
4. The AI will process each analysis sequentially

### Output

For each analysis, the system will:
- Create an engaging narrative composition
- Generate Neo4j Cypher queries for database import
- Save the narrative to the `narratives/` directory
- Save the Cypher queries to the `cypher_queries/` directory

### Verification

After Phase 2 completes:
1. Check that all analyses have corresponding narrative and query files
2. Verify that narratives maintain objectivity while being engaging
3. Test Cypher queries to ensure they're properly formatted
4. Confirm that knowledge graph elements are consistently represented

## Processing Large Batches

For large numbers of articles:

1. Process in smaller batches of 5-10 articles
2. Complete both Phase 1 and Phase 2 for each batch before proceeding
3. Monitor output quality for consistency
4. Consider using specialized prompts for specific content types

## Knowledge Graph Integration

### Obsidian Integration

1. Import entity notes into Obsidian
2. Configure graph view settings according to `artifact_11_obsidian_integration_guide.txt`
3. Use the following plugins for enhanced functionality:
   - Dataview
   - Graph Analysis
   - Obsidian Git
   - Templater

### Neo4j Integration

1. Start your Neo4j database
2. Open the Neo4j Browser
3. Copy the contents of each Cypher query file
4. Execute the queries in the Neo4j Browser
5. Verify that nodes and relationships are created correctly

## Customization Options

### Content-Specific Analysis

For specialized content types, consider modifying:
- The psychoanalytic framework for different theoretical approaches
- The connection exploration framework for domain-specific relationships
- The knowledge graph schema for specialized entity and relationship types

### Output Format Adjustments

To customize output formats:
- Modify the analysis template for different analytical structures
- Adjust the narrative template for different storytelling approaches
- Update the Cypher template for different database schemas

## Troubleshooting

### Common Issues

- **Incomplete Analysis**: If analyses are missing sections, check that the analysis prompt references all required artifacts
- **Inconsistent Knowledge Graph**: If entity references are inconsistent, verify the knowledge graph schema is being properly applied
- **Objectivity Concerns**: If bias appears in outputs, ensure the objectivity checklist is being rigorously applied

### Quality Improvement

To improve output quality:
- Provide more detailed article context when available
- Request specific focus on areas that need deeper analysis
- Use the specialized prompts for particular content types
- Implement iterative refinement for complex topics

## Examples

The `examples/` directory contains sample inputs and outputs to demonstrate the system's capabilities:

- `example_article.txt`: A sample news article
- `example_analysis.md`: A comprehensive analysis with knowledge graph elements
- `example_narrative.md`: An engaging narrative based on the analysis
- `example_knowledge_graph.md`: A visualization of the extracted knowledge graph
- `example_cypher_queries.txt`: Neo4j queries generated from the analysis
- `example_connection_map.md`: A detailed map of connections across multiple dimensions

These examples provide reference points for expected output quality and format.