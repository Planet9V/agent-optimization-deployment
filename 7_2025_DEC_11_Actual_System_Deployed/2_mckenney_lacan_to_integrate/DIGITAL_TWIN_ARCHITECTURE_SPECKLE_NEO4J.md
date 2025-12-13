# AEON Digital Twin: "Body & Brain" Architecture
**Target System**: Full AEON Cyber Digital Twin Application (Backend/Core)
**Status**: Specification / Roadmap

> [!NOTE]
> This document defines the architecture for the *future* full-scale Digital Twin application. The current Informational Website will focus on high-end aesthetics and Diegetic UI experimentation.

---

## 1. The Core Concept: "Body & Brain"
A true Digital Twin requires both a physical representation (Body) and highly coupled logic/state (Brain).

### The Body: Speckle Systems (BIM/CAD)
*   **Role**: The "Source of Truth" for physical geometry.
*   **Data Stored**:
    *   Vertices/Faces (The mesh).
    *   BIM Metadata (Revit parameters, Rhino layers).
    *   Version History (Commit streams).
*   **Tech Stack**: Speckle Server, `@speckle/viewer`, `@speckle/objectloader`.

### The Brain: Neo4j + E30 Engine
*   **Role**: The "Source of Truth" for behavior, relationships, and assessment.
*   **Data Stored**:
    *   **Nodes**: `(:Asset)`, `(:Threat)`, `(:Vulnerability)`, `(:PsychometricState)`.
    *   **Relationships**: `(:Asset)-[:LOCATED_IN]->(:Room)`, `(:Threat)-[:TARGETS]->(:Asset)`.
    *   **State**: Real-time health, Dissonance scores, Threat levels.

---

## 2. The Bridge: Synchronization Pipeline

The system relies on a **One-Way Sync** from Body to Brain for structure, and **Real-Time Query** from Brain to Body for status.

### A. Phase 1: Ingestion (The "Birth" of a Twin)
1.  **Architect** uploads a model to **Speckle** (e.g., via Revit Plugin).
2.  **Speckle Server** generates a `Commit Created` webhook.
3.  **AEON E30 Engine** (Endpoint: `/api/webhooks/speckle`) receives the payload.
4.  **E30 Processor**:
    *    traverse the Speckle Object Tree (using `Speckle API`).
    *   For every physical object (Window, Door, Sensor):
        *   **MATCH**: Check if `(:Asset {speckleId: "..."})` exists in Neo4j.
        *   **MERGE**: If not, create it.
        *   **UPDATE**: Update properties (Name, Type) from BIM data.
5.  **Result**: The Graph Database now has a Node for every physical object in the 3D model.

### B. Phase 2: Simulation (The "Life" of a Twin)
1.  **Simulation Engine** (Psychometrics) runs on the Neo4j Graph.
2.  It calculates `Dissonance` for the `(:Asset)` nodes based on their relationships.
3.  It updates the Node properties in Neo4j: `SET a.dissonance = 0.85`.

### C. Phase 3: Visualization (The Frontend)
1.  **Browser** loads the 3D Model from **Speckle** (Geometry).
2.  **Color Mapping**:
    *   Browser queries Backend: `GET /api/assets/status` -> returns Map `{ "speckleId_123": { color: "red", dissonance: 0.85 } }`.
    *   React Three Fiber applies these colors to the Speckle Mesh instances.
    *   **Result**: The user sees the 3D building glowing Red where Dissonance is high.

---

## 3. Implementation Roadmap
1.  [ ] **Speckle Server**: Deploy instance or use Speckle.xyz.
2.  [ ] **Neo4j Connector**: Write TypeScript Service (`services/speckle-sync.ts`) to handle Webhooks.
3.  [ ] **Schema Mapping**: Define how IFC Types map to Neo4j Labels (e.g., `IfcWall` -> `(:Wall)`).
4.  [ ] **Frontend**: Build the "Hybrid Viewer" using `@react-three/fiber` + `@speckle/viewer`.

---
**Summary**: This architecture ensures we are not duplicating "File Data" in our Database, nor "Logic Data" in our Files. We respect the strengths of both platforms.
