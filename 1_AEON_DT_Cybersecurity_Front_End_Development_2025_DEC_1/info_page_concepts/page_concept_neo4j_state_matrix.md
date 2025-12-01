# Page Concept: The Neo4j State Matrix
**"The Structure of the Unconscious"**

## 1. Core Concept
A deep-dive visualization of the **Neo4j Graph Database**, the "State Matrix" of the system. This page allows users to see the raw topology of the network, inspect individual nodes (Assets, Actors, Concepts), and watch **Cypher Algorithms** (PageRank, Louvain) execute in real-time.

## 2. Visual Design (The "Neural Lattice")
*   **The Graph**: A massive, force-directed graph (3D).
    *   **Nodes**: Glowing spheres. Size = Eigenvector Centrality. Color = Community (Louvain).
    *   **Edges**: Glowing lines. Thickness = Bandwidth/Influence ($J_{ij}$).
*   **The "Lens"**: A circular cursor that acts as a magnifying glass/X-ray, revealing node properties when hovered.

## 3. Key Features & Interactions

### 3.1 Real-Time Cypher Terminal
*   **Visual**: A floating terminal window.
*   **Interaction**: As the user navigates the graph, the *actual Cypher query* generating the view is typed out in the terminal.
    *   `MATCH (n:Asset)-[r:CONNECTS_TO]->(m) WHERE n.risk > 0.8 RETURN n, r, m`
*   **Educational**: Teaches the user how the "Physics" is translated into "Query".

### 3.2 Algorithm Visualizer
*   **Control**: Buttons to trigger GDS algorithms.
    *   **"Run Louvain"**: The graph re-colors itself based on detected communities.
    *   **"Run PageRank"**: The nodes resize based on importance.
    *   **"Show Shortest Path"**: A glowing lightning bolt connects two selected nodes.

### 3.3 The "Hamiltonian Heatmap"
*   **Visual**: Toggle a "Heatmap Mode".
*   **Effect**: The graph is overlaid with a color gradient representing the **Local Energy** ($H_i$).
    *   **Hot Spots (Red)**: High tension/risk (Misaligned Spins).
    *   **Cold Spots (Blue)**: Stable/Secure regions.

## 4. Technical Implementation
*   **Data Source**: `07_NEO4J_IMPLEMENTATION_OF_PSYCHOHISTORY.md`.
*   **Backend**: Direct Bolt connection to Neo4j (read-only).
*   **Visualization**:
    *   **3d-force-graph**: For the physics-based graph rendering.
    *   **Neo4j Bloom** style aesthetics.

## 5. Business Value
*   **"Transparency"**: Shows that the "AI" isn't a black box; it's a structured, queryable database.
*   **"Insight"**: Reveals hidden structures (e.g., "Why is the Marketing server connected to the SCADA network?").
*   **"Power"**: Demonstrates the scale and complexity of the data AEON handles.
