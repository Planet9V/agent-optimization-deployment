# Page Concept: The Hybrid Engine
**"Structure Meets Meaning"**

## 1. Core Concept
A high-tech visualization of the **"Split-Brain" Architecture** (Neo4j + Qdrant). It solves the problem of how to ingest 566 complex entity types into a rigid graph schema without breaking it.

## 2. Visual Design (The "Synapse")
*   **Style**: Cyberpunk, glowing data streams splitting and converging.
*   **Central Metaphor**: The Left Brain (Neo4j - Logic/Structure) and Right Brain (Qdrant - Intuition/Context).

## 3. The Visualization

### 3.1 The Data Stream
*   **Visual**: A massive pipe of raw JSON data flowing from the NER11 Model.
*   **Content**: "566 Entity Types", "Rich Context", "Unstructured Text".

### 3.2 The Split (The Prism)
*   **Visual**: The stream hits a "Prism" (The ETL Pipeline) and splits into two beams.
    1.  **Beam A (Structure)**: Thin, precise laser. Hits **Neo4j**.
        *   *Action*: Maps "PLC" to "Asset". Maps "Normalcy Bias" to "RiskFactor".
        *   *Result*: Fast, traversable Graph.
    2.  **Beam B (Context)**: Wide, holographic beam. Hits **Qdrant**.
        *   *Action*: Stores the full text, the nuance, the embeddings.
        *   *Result*: Searchable, semantic Vector Store.

### 3.3 The Synthesis (The Query)
*   **Visual**: A Chat Bot (Agent) asking a question: *"Why did the operator ignore the warning?"*
*   **Action**:
    1.  Agent queries **Qdrant** -> Finds "Normalcy Bias" (Context).
    2.  Agent queries **Neo4j** -> Finds "Water Plant A" (Structure).
    3.  **Result**: "The operator at Water Plant A ignored the warning due to Normalcy Bias."

## 4. Technical Implementation
*   **Data Source**: `05_HYBRID_ARCHITECTURE_DESIGN.md`.
*   **Visuals**: Particle systems for data flow, split-screen comparison.

## 5. Business Value
*   **"Innovation"**: Shows we are using cutting-edge Vector + Graph technology (RAG).
*   **"Scalability"**: Explains how we handle massive complexity without performance loss.
*   **"Future-Proof"**: Ready for AI Agents and LLMs.
