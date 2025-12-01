# AEON Nexus: Technical Specification - Data Schema & API

**Document ID**: AEON_NEXUS_TECH_SPEC_DATA_SCHEMA
**Parent Doc**: AEON_NEXUS_PRD_EXHAUSTIVE
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## 1. The Graph Schema (Neo4j)

The "Twin" is stored as a Property Graph.

### 1.1 Node Labels
*   **`Actor`**: A character or user (e.g., `Willy`, `Linda`, `Admin`).
    *   *Props*: `name`, `disc_type`, `big5_vector` (List[Float]).
*   **`Event`**: A discrete moment in time (e.g., `Beat_14`).
    *   *Props*: `timestamp`, `sentiment`, `trauma_level`.
*   **`Concept`**: A Lacanian term (e.g., `Objet_a`, `Symbolic`).
    *   *Props*: `definition`, `link_to_paper`.
*   **`Asset`**: A system component (e.g., `Server_01`, `Database`).

### 1.2 Relationship Types
*   **`(:Actor)-[:SPEAKS_TO]->(:Actor)`**: Dialogue flow.
*   **`(:Event)-[:TRIGGERS]->(:Asset)`**: Causality (e.g., Beat 14 crashes Server 01).
*   **`(:Actor)-[:INHABITS]->(:Register)`**: Which Lacanian register is active?
*   **`(:Event)-[:CITES]->(:Paper)`**: Link to the academic corpus.

---

## 2. The API Specification (FastAPI)

The Backend serves as the bridge between the Static CSV and the Dynamic Graph.

### 2.1 Endpoints

#### `GET /api/v1/score/stream` (WebSocket)
*   **Purpose**: Streams the CSV data row-by-row to the Frontend for playback.
*   **Payload**:
    ```json
    {
      "beat": 14,
      "timestamp": 1200,
      "data": {
        "heartbeat": 0.9,
        "mischief": 0.2,
        "gttm_chord": "Dim7"
      }
    }
    ```

#### `GET /api/v1/manifold/geometry/{beat_id}`
*   **Purpose**: Returns the calculated 12D coordinates for the 3D engine.
*   **Logic**:
    1.  Fetch `Actor` state from Neo4j.
    2.  Apply `PsychometricTensor` (PyTorch).
    3.  Return `Vector3` for Three.js.

#### `POST /api/v1/twin/intervene`
*   **Purpose**: The Chef modifies the state.
*   **Payload**: `{"target": "Willy", "action": "REDUCE_TRAUMA", "value": 0.5}`
*   **Effect**: Updates the Neo4j Graph and triggers a re-calculation of the Future Cone.

---

## 3. NER11 Gold Integration Pipeline

How the "Brain" feeds the "Twin".

1.  **Ingest**: Log Line enters system.
2.  **Inference**: `ner11_model.predict(text)`.
3.  **Extraction**:
    *   Entity: `Willy` (Actor)
    *   Entity: `Car` (Asset)
    *   Label: `DEATH_DRIVE` (Concept)
4.  **Graph Update**:
    *   `MERGE (a:Actor {name: "Willy"})`
    *   `MERGE (c:Concept {name: "Death Drive"})`
    *   `CREATE (a)-[:MANIFESTS]->(c)`
