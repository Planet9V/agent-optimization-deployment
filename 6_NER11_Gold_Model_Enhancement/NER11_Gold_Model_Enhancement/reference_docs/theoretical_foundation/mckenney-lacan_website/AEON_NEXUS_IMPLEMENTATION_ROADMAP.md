# AEON Nexus: Implementation Roadmap

**Document ID**: AEON_NEXUS_IMPLEMENTATION_ROADMAP
**Parent Doc**: AEON_NEXUS_PRD_EXHAUSTIVE
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## Phase 1: The Foundation (Weeks 1-2)
**Goal**: A running Next.js app with a blank 3D canvas and a connected Neo4j instance.

1.  **Repo Setup**: Initialize `aeon-nexus` with Next.js 15 + TypeScript.
2.  **3D Boilerplate**: Install `react-three-fiber` and render a spinning cube to verify WebGL.
3.  **Graph Setup**: Spin up a Neo4j AuraDB instance and connect via `neo4j-driver`.
4.  **CSV Parser**: Implement a server-side parser for `GRAND_UNIFIED_SCORE.csv`.

## Phase 2: The Symphony (Weeks 3-4)
**Goal**: The "Guitar Hero" timeline works, and the audio plays in sync.

1.  **Tone.js Setup**: Create the `InstrumentRack` (Heartbeat, Mischief, Harmony).
2.  **Timeline Component**: Build the 2D Canvas timeline with scrolling lanes.
3.  **Sync Engine**: Implement the `useFrame` loop in R3F to drive the audio transport.
4.  **Sonification**: Map the CSV data to the synth triggers.

## Phase 3: The Intelligence (Weeks 5-6)
**Goal**: The 3D Manifold reflects the data, and the Graph is live.

1.  **Manifold Geometry**: Implement the `PsychometricManifold` mesh with the custom shader.
2.  **Data Binding**: Connect the CSV stream to the Shader Uniforms ($R \to uTrauma$).
3.  **NER Integration**: Connect the `ner11_model` to the ingestion pipeline.
4.  **Graph Visualization**: Implement `react-force-graph-3d` for the Topology view.

## Phase 4: The Polish (Weeks 7-8)
**Goal**: "Groundbreaking" Aesthetics and Performance.

1.  **Post-Processing**: Add Bloom, Chromatic Aberration, and Depth of Field.
2.  **Optimization**: Implement `InstancedMesh` for the timeline notes (1000+ objects).
3.  **Trauma Shader**: Fine-tune the noise functions for maximum visceral impact.
4.  **Launch**: Deploy to Vercel Edge Network.

---

## Phase 5: The Primer (Weeks 9-10)
**Goal**: The "Mathematical Playground" is live with 10 interactive visualizations.

1.  **Tensor Slicer**: Implement 3D volumetric rendering for the Rank-3 Tensor.
2.  **Knot Lab**: Use `d3-force` or custom physics to simulate the Borromean Rings.
3.  **Riemann Surface**: Create a parametric surface geometry that deforms with "Mass" input.
4.  **Stochastic Sim**: Run a client-side Monte Carlo simulation (WebWorker) for the Future Cone.
5.  **Integration**: Link each Primer visualization to its corresponding Markdown volume in the Graph.

---

## Critical Path Dependencies

1.  **NER11 Gold Model**: Must be fully trained and exported to ONNX for fast inference.
2.  **Grand Unified Score**: The CSV must be finalized (Done).
3.  **Academic Corpus**: All 65+ Markdown files must be indexed in the Graph.
