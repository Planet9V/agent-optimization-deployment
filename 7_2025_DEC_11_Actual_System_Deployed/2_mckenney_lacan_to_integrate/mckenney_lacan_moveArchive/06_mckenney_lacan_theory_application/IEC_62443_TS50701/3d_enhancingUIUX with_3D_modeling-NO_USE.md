**# Architecting the Cognitive SOC: Converging Spatial Computing, Agentic AI, and Graph Theory for Next-Generation Cyber-Physical Defense

## 1. Introduction: The Imperative for Spatial Cognition in Cyber Defense

The contemporary Security Operations Center (SOC) faces an existential crisis of cognitive overload. As the attack surface expands into Industrial Control Systems (ICS), Operational Technology (OT), and ephemeral cloud architectures, the traditional "single pane of glass"—typically realized as a dense, two-dimensional dashboard of text logs and static charts—has reached the limits of human processing efficacy. The data density required to monitor a modern enterprise, particularly one subject to rigorous standards like IEC 62443 or railway specific TS 50701, necessitates a paradigm shift toward Spatial Computing.

This report articulates a comprehensive architectural blueprint for a "Cognitive SOC," a three-dimensional, collaborative command environment. This system is not merely a visualization tool but a fully functional Digital Twin that bridges the gap between the physical reality of infrastructure and the logical reality of threat vectors. By converging React Three Fiber (R3F) for high-fidelity rendering, Conflict-free Replicated Data Types (CRDTs) for real-time state synchronization, and Graph Theory for dynamic threat modeling, we can construct an interface that leverages the human brain's innate spatial reasoning capabilities to reduce Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR).

We analyze the implementation of this architecture across three vertical layers: the Presentation Layer, responsible for the "diegetic" user experience; the Collaboration Layer, ensuring state consistency among distributed analyst teams; and the Intelligence Layer, where autonomous AI agents actively emulate adversaries within a graph-based threat model.

## ---

2. The Physics of Interface: Advanced Spatial Rendering Architectures

The visualization layer of the Cognitive SOC is constructed upon React Three Fiber (R3F), a React renderer for Three.js. Unlike traditional web interfaces where the DOM (Document Object Model) dictates layout, R3F allows us to compose scenes declaratively, treating 3D meshes, lights, and cameras as reactive components. This capability is foundational for creating a Diegetic UI, where interface elements exist within the 3D world—reacting to lighting, physics, and perspective—rather than floating arbitrarily on top of it.

### 2.1 Diegetic User Interfaces and the Geometry of Interaction

A diegetic UI embeds controls and data visualizations directly into the scene geometry. In a cyber-physical context, this means an analyst does not toggle a 2D switch to isolate a compromised server; instead, they interact with the digital representation of the server rack itself. This approach reduces the abstraction gap, allowing the analyst to maintain context between the asset's physical location (e.g., "Zone A, Rack 4") and its logical status (e.g., "Infected").

#### 2.1.1 Spatial Containers and Layout Systems

While Three.js provides the primitives for 3D rendering, managing layout in 3D space is notoriously difficult. We leverage @react-three/uikit, which implements the Yoga layout engine (based on Flexbox) directly within the 3D scene graph. This allows for the construction of responsive 3D panels that adhere to familiar web layout paradigms while existing as distinct meshes in the WebGL context.4

The core components, `<Container>` and `<Fullscreen>`, facilitate the binding of UI panels to the camera's frustum or to specific objects in the scene. A `<Fullscreen>` component, for instance, can calculate the exact pixelSize and distanceToCamera required to render a HUD that feels "attached" to the user's viewport, yet participates in the scene's depth buffer.4 This creates a sense of immersion where the UI layers have physical presence, occluding background elements naturally rather than being composited as a flat overlay.

Table 1: Comparison of UI Rendering Strategies in WebGL

| Strategy       | Technical Implementation                                    | Cognitive Impact                                                                 | Performance Cost                            |
| -------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------- |
| DOM Overlay    | Standard HTML`<div>` floating over `<canvas>`           | High abstraction; disconnect between data and object.                            | Low (Native browser compositing).           |
| Projected 2D   | CSS3DRenderer transforming DOM elements in 3D               | Better spatial context; limited by CSS rendering constraints (no true lighting). | Medium (Heavy DOM manipulation).            |
| Diegetic (FUI) | R3F/Three.js meshes with Flexbox logic (@react-three/uikit) | Maximum immersion; interface reacts to scene lighting and post-processing.       | High (Requires optimization of draw calls). |

#### 2.1.2 Shader-Based Holographics and Signed Distance Fields (SDFs)

To achieve a "Future User Interface" (FUI) aesthetic that signals advanced technological capability, standard texture mapping is insufficient. We employ custom GLSL (OpenGL Shading Language) shaders to generate UI elements procedurally. This technique, utilizing Signed Distance Fields (SDFs), allows for infinite resolution scaling of elements like reticles, connection lines, and health bars without pixelation.5

A critical design pattern for the SOC is the "Reveal Effect," used to visualize hidden threats or scan progress on an asset. This is implemented via a custom shader that manipulates the alpha channel based on a noise function and a radial gradient.

The fragment shader logic for such an effect involves calculating a distance field from a "scanner" point (e.g., the mouse cursor or a virtual drone). We use Perlin noise (cnoise) to disturb the UV coordinates, creating an organic, fluctuating edge that mimics a digital scan wave.

Mathematical Foundation of the Reveal Shader:

The visibility strength $S$ at any pixel with UV coordinates $v$ and time $t$ is calculated as:

$$
S(v, t) = \text{smoothstep}(r - w, r + w, ||v - c|| + N(v \times f, t))
$$

Where:

* $c$ is the center of the reveal (cursor position).
* $r$ is the radius of the reveal.
* $w$ is the edge softness (feathering).
* $N$ is a 3D noise function (e.g., Simplex or Perlin).
* $f$ is the frequency of the noise (detail level).

This logic allows the UI to dynamically "grow" over a compromised node, revealing the underlying red "infected" texture only where the scan has completed, providing immediate visual feedback on the state of an investigation.7

### 2.2 Material Science in the Digital Realm: Physically Based Glassmorphism

Glassmorphism in a 3D environment is fundamentally different from the CSS backdrop-filter: blur() effect. It requires a physical simulation of light transmission through a dielectric medium. We utilize the MeshTransmissionMaterial from the @react-three/drei library to achieve a "cyber-physical" aesthetic, where UI panels appear as thick, high-tech optical slabs rather than flimsy transparencies.

#### 2.2.1 Configuring Transmission Physics for Cognitive Clarity

The MeshTransmissionMaterial extends the standard MeshPhysicalMaterial by adding a pre-pass render step. The scene behind the object is rendered into a buffer, which is then mapped onto the object's surface with distortions applied based on the material's Index of Refraction (IOR) and Thickness.8

To optimize this material for a SOC dashboard—where legibility of text is paramount—specific parameter tuning is required. High IOR values (like diamond, ~2.4) create excessive distortion that renders text unreadable. We target an IOR close to air (1.0) but slightly elevated to glass (1.1-1.2) to maintain the "glass" feel without compromising utility.

Table 2: Optimal MeshTransmissionMaterial Configuration for FUI Panels

| Property             | Optimal Value Range | Technical Rationale & Cognitive Effect                                                                                                                                                   |
| -------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Transmission         | 0.95 - 1.0          | Maximizes light throughput. Lower values darken the background, which can be useful for modal dialogs but detrimental for HUDs needing situational awareness.                            |
| Roughness            | 0.1 - 0.2           | Introduces microscopic surface irregularities. This diffuses the background buffer, effectively blurring noise to improve the contrast of foreground text (The "Frosted Glass" effect).9 |
| Thickness            | 0.5 - 2.0           | Simulates physical volume. This parameter is crucial for the refraction calculation; without thickness, the IOR calculation has no "medium" to traverse, resulting in a flat look.10     |
| IOR                  | 1.1 - 1.2           | Low refraction minimizes geometric distortion of the background data visualization, preserving the integrity of grids and charts while signaling that the panel is a physical object.10  |
| Chromatic Aberration | 0.02 - 0.05         | Simulates spectral dispersion (prism effect) at the edges. This adds a subtle "cinematic" imperfection that increases perceived realism and visual hierarchy.10                          |
| Backside             | true                | Forces the renderer to compute the back face of the mesh. For volumetric UI slabs, this is essential to seeing the "thickness" of the panel.8                                            |
| Resolution           | 512 or 1024         | Controls the resolution of the transmission buffer. Lower values (e.g., 256) can be used artistically to create a "digital glitch" or retro-computational aesthetic.10                   |

#### 2.2.2 Managing the Transmission Buffer

A significant technical challenge with transmission materials is the "stacking" problem. Because MeshTransmissionMaterial requires a snapshot of the scene behind it to calculate refraction, multiple transmission objects often cannot "see" each other if they share the same render pass or buffer. To resolve this in a complex dashboard where windows might overlap, we must orchestrate the render order or manually manage the buffer property.

By using useFBO (Frame Buffer Object) to manually render the scene to a texture, and passing this texture to the material's buffer prop, we can control exactly what the glass reflects and refracts. This allows for advanced effects, such as a "Safety Zone" bubble that refracts the "Enterprise Zone" background but is itself refracted by a foreground "Alert Modal".8

### 2.3 Cinematic Post-Processing: The Selective Bloom Strategy

To elevate the visual fidelity from "functional" to "cinematic," we implement a post-processing pipeline using @react-three/postprocessing. The objective is to guide the analyst's attention using light, leveraging the Pop-out Effect in visual psychology.

#### 2.3.1 The Luminance Threshold Strategy

Standard bloom effects apply a glow to all pixels exceeding a certain brightness. In a SOC, indiscriminate bloom reduces readability. We require Selective Bloom, where only specific, critical elements (e.g., a node under active attack) emit a glow.

While the library offers a `<SelectiveBloom>` component that requires managing a specific selection array of object references, a more performant and architecturally scalable approach leverages the native luminanceThreshold of the standard `<Bloom>` effect.11

By setting the global luminanceThreshold to 1.0, we ensure that standard colors (which range from 0.0 to 1.0 in RGB) do not glow. To make an object bloom, we push its color values beyond this dynamic range. This requires disabling tone mapping on the specific material (toneMapped={false}) and using high-intensity emissive colors.

Implementation Logic:

* Normal State: Material color is [0.2, 0.5, 1.0] (Blue). toneMapped={true}. Result: No Glow.
* Alert State: Material color is pushed to `` (High-Intensity Red). toneMapped={false}. emissiveIntensity={4.0}. Result: Intense Red Glow that bleeds into surrounding pixels.

This "emissive workflow" decouples the visual effect from the scene graph hierarchy. Any component, anywhere in the application, can trigger a bloom simply by changing its own material properties, without needing registration with a central post-processing pass.12

#### 2.3.2 Color Grading with 3D LUTs

To unify the disparate assets in the scene (some imported from CAD, others generated procedurally), we apply a Lookup Table (LUT). Common in film production, LUTs map input colors to a target palette. By loading a .cube file into a custom effect pass, we can force the entire render output to adhere to a specific aesthetic, such as "Cyberpunk Teal" or a high-contrast "Silver Blue" palette (e.g., matching DHS Blue #005288 to a cinematic equivalent).14 This ensures visual consistency across the application, crucial for long-duration monitoring where visual fatigue is a risk.

## ---

3. The Collaborative Fabric: Real-Time State Synchronization

A modern SOC is inherently collaborative; a single incident often requires the coordinated efforts of network analysts, threat hunters, and compliance officers. The interface must therefore support multi-user presence and state synchronization. We utilize Yjs, a high-performance CRDT library, bridged to Valtio for local state management.

### 3.1 The Yjs-Valtio Bridge Pattern

Directly binding React components to Yjs types (Maps, Arrays) can lead to verbose boilerplate and excessive re-renders. Valtio, a proxy-based state manager, acts as the ideal intermediary. We establish a two-way binding where the Valtio proxy serves as the mutable "local" state, which is automatically synchronized with the Yjs "shared" state.17

Architecture of the Bridge:

1. Y.Doc: The CRDT source of truth. It handles vector clocks, conflict resolution, and network propagation via y-websocket or y-webrtc.
2. Y.Map / Y.Array: The shared types representing the scene graph (e.g., nodes, connections, alerts).
3. Valtio Proxy: A reactive JavaScript object that mirrors the Yjs structure. Changes to this proxy are intercepted and applied to the Yjs types.
4. React Component: Subscribes to the Valtio proxy using the useSnapshot() hook. This ensures the component only re-renders when the specific properties it accesses are modified.18

This architecture allows developers to write standard mutable JavaScript (e.g., state.nodes[id].status = 'compromised') while the underlying bridge handles the complexity of propagating that change to all connected clients.20

### 3.2 Granular Undo/Redo in Multi-User Environments

Implementing Undo/Redo in a shared 3D environment is non-trivial. A global undo stack would revert actions performed by other users, causing confusion and potential data loss. We must implement Selective Undo Management using Y.UndoManager with tracked origins.21

Transaction Origins:

Every change in Yjs is associated with an origin. By default, this is null. To isolate a user's action history, we assign a unique clientID or sessionID to the origin of every transaction initiated by the local interface.

JavaScript

// Initialization of the UndoManager
const undoManager = new Y.UndoManager(yText, {
  trackedOrigins: newSet() // Only track changes originating from this client
});

// Applying a change with origin tagging
doc.transact(() => {
  yText.insert(0, 'Log entry...');
}, localClientID);

When a user moves a node in the 3D space, the transaction is tagged with their ID. The UndoManager inspects this tag and adds the operation to the stack only if it matches the local user's ID. This ensures that pressing Ctrl+Z reverses only the local user's most recent action, even if five other analysts are simultaneously modifying the graph.22

### 3.3 Ephemeral State and Awareness: The 3D Cursor

In a 2D document, presence is a caret. In a 3D SOC, presence is a Frustum or a 3D Cursor. We utilize the Yjs Awareness Protocol to broadcast ephemeral state that does not need to be persisted in the document history (e.g., mouse position, camera rotation, selection state).24

Data Structure for 3D Awareness:

* User Identity: { name: "Analyst A", color: "#FF0000" }
* 3D Position: { x: 10.5, y: 2.0, z: -5.0 } (World coordinates of the raycaster intersection with the scene geometry).
* View Matrix: The camera's position and rotation quaternion.

This data is broadcast via the awareness instance attached to the connection provider. In the R3F scene, we subscribe to these updates and render a custom `<CursorMesh>` or `<CameraFrustumHelper>` at the remote user's coordinates. This provides immediate visual feedback: if Analyst B is inspecting a specific firewall node, Analyst A sees their color-coded cursor hovering over it and their camera frustum pointing towards it, facilitating non-verbal coordination.24

## ---

4. Semantic Digital Twins: Graph-Based Threat Modeling

The visual and collaborative layers must sit atop a rigorous data model. We define the "Digital Twin" not just as a visual replica, but as a semantic graph representing the security posture of the infrastructure. We integrate MulVAL for attack graph generation and Neo4j for graph persistence.

### 4.1 From Vulnerability Scans to Logic Graphs with MulVAL

MulVAL (Multihost, Multistage Vulnerability Analysis) utilizes Datalog clauses to model the interaction of network configurations and vulnerabilities. Unlike simple vulnerability scanners that produce lists of CVEs, MulVAL reasons about reachability. It determines if a vulnerability on Machine A can actually be exploited by an attacker on Machine B given the firewall rules between them.27

#### 4.1.1 The MulVAL Pipeline and Data Ingestion

To integrate MulVAL into a modern data pipeline, we must automate the processing of its output. The MulVAL engine runs an XSB Prolog reasoner that consumes input files (OVAL scans, HACL rules) and produces a logical attack graph.

When executed with the -l flag, MulVAL outputs two critical CSV files: VERTICES.CSV and ARCS.CSV. These files contain the raw graph structure but lack explicit headers, requiring a predefined schema for ingestion.29

Table 3: Inferred Schema for MulVAL VERTICES.CSV

| Column Index | Field Name  | Data Type | Description                                                 |
| ------------ | ----------- | --------- | ----------------------------------------------------------- |
| 0            | node_id     | Integer   | Unique identifier for the attack graph node.                |
| 1            | description | String    | Human-readable text (e.g., "execCode(internet, root)").     |
| 2            | type        | String    | Node type: OR (Goal), AND (Derivation), LEAF (Fact/Config). |
| 3            | probability | Float     | (Optional) Probability metric if CVSS scoring is enabled.   |
| 4            | metric      | Float     | (Optional) Risk metric associated with the node.            |

Table 4: Inferred Schema for MulVAL ARCS.CSV

| Column Index | Field Name | Data Type | Description                                                  |
| ------------ | ---------- | --------- | ------------------------------------------------------------ |
| 0            | source_id  | Integer   | ID of the parent node (Precondition).                        |
| 1            | target_id  | Integer   | ID of the child node (Consequence).                          |
| 2            | rule_label | String    | The interaction rule (e.g., remote_exploit, network_access). |

### 4.2 Graph Persistence: Neo4j Ingestion Strategy

Neo4j serves as the persistence layer for the Digital Twin. We use the Cypher query language to transform the static CSV outputs into a queryable property graph. The ingestion process must map the MulVAL node types to Neo4j labels to facilitate efficient querying.31

Cypher Ingestion Script:

Cypher

// Ingest Vertices
LOAD CSV FROM 'file:///VERTICES.CSV' AS row
CREATE (:AttackNode {
    mulval_id: toInteger(row),
    description: row[1],
    type: row[2],
    probability: toFloat(row[3])
});

// Ingest Arcs (Relationships)
LOAD CSV FROM 'file:///ARCS.CSV' AS row
MATCH (source:AttackNode { mulval_id: toInteger(row) })
MATCH (target:AttackNode { mulval_id: toInteger(row[1]) })
CREATE (source)- }]->(target);

Once ingested, the graph allows for sophisticated analysis. We can calculate Betweenness Centrality to identify nodes that appear in the highest number of attack paths—these are the "choke points" where a defensive intervention (e.g., patching or firewalling) would yield the highest return on investment.32

### 4.3 Modeling Industrial Security: The IEC 62443 Schema

For industrial environments, the graph schema must be enriched with concepts from IEC 62443 (specifically Part 3-2): Zones, Conduits, and Security Levels (SL). This standard mandates the segmentation of the network to limit the blast radius of an attack.34

Extended Graph Schema:

* Nodes: :Asset (PLC, Server), :Zone (Safety System, Enterprise), :Conduit (VPN, Switch).
* Relationships:
* (:Asset)-->(:Zone)
* (:Zone)-->(:Conduit)-->(:Zone)
* Properties:
* SL_T (Target Security Level): Integer 1-4.
* SL_A (Achieved Security Level): Integer 1-4.
* SecRAC (Security Related Application Conditions): JSON string containing constraints.

The 3D interface utilizes this schema to render volumetric boundaries. A :Zone node in Neo4j translates to a translucent sphere or bounding box in R3F, enclosing all :Asset nodes connected to it. The color of the zone boundary can dynamically reflect the delta between SL_T and SL_A; if the Achieved level is lower than the Target, the zone pulses red, visually indicating a compliance gap.36

## ---

5. Autonomous Adversary Emulation: The AI Agent Layer

Static attack graphs provide a snapshot of potential risk. To create a dynamic, reactive SOC, we integrate Autonomous AI Agents capable of simulating adversaries and validating defenses in real-time. We utilize LangChain and LangGraph to orchestrate these agents, allowing them to reason about the network topology and execute simulated attacks.

### 5.1 LLM-Driven Red Teaming Architecture

Red Teaming with Large Language Models (LLMs) involves simulating an adversarial actor to probe system defenses. In our architecture, the "System" is the Digital Twin and its connected simulation APIs (Cyber Range). We define a Red Team Agent using LangGraph, which models the agent's cognition as a state machine.38

LangGraph State Schema:

Python

class AgentState(TypedDict):
    messages: Annotated, operator.add]
    knowledge_graph: Dict  # Internal map of discovered assets
    current_objective: str
    tools_available: List[str]
    history: List[str]

The Agent Workflow:

1. Objective Setting: The agent is initialized with a goal (e.g., "Compromise the Historian Database in Zone 2").
2. Observation: The agent uses tools to query the Neo4j graph, simulating reconnaissance (e.g., "What assets are connected to my current entry point?").
3. Reasoning: The LLM (e.g., GPT-4 or a fine-tuned Llama 3) analyzes the graph data to identify a viable attack path (e.g., "Asset X has CVE-2023-XYZ and connects to the target").
4. Action: The agent executes an "exploit" tool, which updates the graph state (e.g., creating a `` relationship).40

### 5.2 Custom Tools for Graph Interaction

To enable the agent to interact with the Neo4j Digital Twin, we must construct custom tools using the @tool decorator in LangChain. These tools abstract the complexity of Cypher queries, allowing the LLM to interact with the database using natural language or structured parameters.42

Example: query_attack_path Tool

Python

from langchain.tools import tool
from neo4j import GraphDatabase

@tool
defquery_attack_path(source: str, target: str) -> str:
    """
    Finds the shortest attack path between two assets in the Digital Twin.
    Args:
        source: The name or ID of the starting asset.
        target: The name or ID of the target asset.
    """
    query = """
    MATCH (start:Asset {name: $source}), (end:Asset {name: $target})
    MATCH p = shortestPath((start)-->(end))
    RETURN p
    """
    #... execution logic using Neo4j driver...
    return format_path_for_llm(result)

By exposing such tools, the agent can "see" the network topology. It can query for high-value targets ("Crown Jewels") or look for nodes with specific vulnerabilities, effectively navigating the MulVAL graph to plan its attack.32

### 5.3 Integrating Threat Intelligence (STIX/TAXII)

To ensure the simulation reflects reality, the agent's behavior must be grounded in real-world Threat Intelligence. We ingest STIX 2.1 objects (Attack Patterns, Campaigns, Malware) via TAXII feeds (e.g., MITRE ATT&CK Enterprise or ICS matrices).

Ingestion Workflow:

1. A background service polls a TAXII server (e.g., MITRE CTID or a commercial feed).
2. STIX objects of type attack-pattern and malware are ingested into Neo4j.
3. These nodes are linked to the MulVAL interaction rules. For example, a MulVAL rule remote_exploit might be linked to the STIX pattern T1210 (Exploitation of Remote Services).

Persona-Based Emulation:

The Red Team Agent can be prompted to adopt a specific Threat Actor Persona (e.g., "Act as APT29"). The agent then queries the graph for attack-pattern nodes associated with that actor (via the uses relationship in STIX). It restricts its behavior to only those TTPs (Tactics, Techniques, and Procedures) known to be used by APT29. This ensures that the stress tests validated by the SOC are not just theoretical worst-case scenarios, but historically accurate simulations of specific threat groups.44

## ---

6. Convergence: The Cognitive Dashboard Application

The convergence of spatial computing, real-time collaboration, and graph-based AI results in the Cognitive SOC Dashboard. This is a unified application where the 3D view is the primary interface for both monitoring and active defense.

### 6.1 Full Stack Architecture

1. Presentation Layer (Client):

* Runtime: React (Vite ecosystem).
* 3D Engine: React Three Fiber (Three.js).
* UI Framework: @react-three/uikit handling spatial layout.
* Visuals: Custom shaders (HUDs, Reveal) and Post-processing (Selective Bloom, LUTs).
* State: Valtio proxies synced to Yjs.

2. Middleware Layer (Orchestration):

* Collaboration Server: Node.js running y-websocket for CRDT sync and Awareness broadcast.
* Agent Service: Python (FastAPI) hosting LangGraph agents. This service exposes REST endpoints or WebSockets for the frontend to dispatch agents and receive simulation updates.

3. Data Layer (Persistence):

* Graph Database: Neo4j, storing the Digital Twin (Assets, Zones, Conduits) and the Attack Graph (MulVAL output).
* Knowledge Base: Vector store (e.g., Pinecone or Weaviate) for RAG (Retrieval Augmented Generation), allowing agents to search unstructured documentation like SRACs (Safety Related Application Conditions).

### 6.2 Case Study Implementation: Railway Security (TS 50701)

In a railway security context, the system provides a specialized view compliant with CLC/TS 50701.

* Zoning Visualization: The 3D view renders the "Train Control Network" (Zone A) and "Passenger Wi-Fi" (Zone B) as distinct volumetric regions using MeshTransmissionMaterial.
* Conduit Inspection: The connection between zones is rendered as a glowing 3D cable. Hovering over this conduit reveals its SL-A (Achieved Security Level) and any detected traffic anomalies.
* SRAC Management: When an analyst clicks a signaling asset, a glassmorphic panel expands. This panel displays the Safety Related Application Conditions (SRACs)—critical constraints exported from the safety case (e.g., "Patching this PLC requires manual override of the failsafe"). This data is pulled from the Neo4j graph, where the Asset node is linked to an SRAC document node.34
* Active Defense Simulation: The analyst drags a "Red Team Agent" icon onto the "Passenger Wi-Fi" zone. The agent (running in LangGraph) attempts to traverse the conduit to the control network. The attack path is visualized in real-time: edges turn red as the agent discovers them. If the agent succeeds, the conduit glows intensely, signaling a violation of the zone boundary and prompting immediate remediation.

## 7. Future Outlook

The trajectory of this architecture points toward fully immersive Spatial Computing interfaces (e.g., Apple Vision Pro, Meta Quest). The use of R3F and WebXR allows this application to be ported to VR/AR with minimal refactoring, enabling analysts to literally "walk" through the attack graph. Furthermore, the role of agents will evolve from simulation to active defense. Future iterations will empower agents to autonomously reconfigure firewalls—modifying the Digital Twin, which then pushes configurations to the physical infrastructure via Infrastructure-as-Code pipelines—closing the OODA loop (Observe, Orient, Decide, Act) at machine speed.

This report outlines a rigorous, technically validated path to building such a system, moving beyond proof-of-concept into a robust, operational tool for defending the critical cyber-physical infrastructure of the future.

#### Works cited

1. pmndrs/uikit: user interfaces for react-three-fiber - GitHub, accessed December 8, 2025, [https://github.com/pmndrs/uikit](https://github.com/pmndrs/uikit)
2. A brief intro to WebGL shaders - Builder.io, accessed December 8, 2025, [https://www.builder.io/blog/webgl-shaders](https://www.builder.io/blog/webgl-shaders)
3. Introduction to Shaders - Wawa Sensei, accessed December 8, 2025, [https://wawasensei.dev/courses/react-three-fiber/lessons/shaders-introduction](https://wawasensei.dev/courses/react-three-fiber/lessons/shaders-introduction)
4. How to Code a Shader Based Reveal Effect with React Three Fiber & GLSL | Codrops, accessed December 8, 2025, [https://tympanus.net/codrops/2024/12/02/how-to-code-a-shader-based-reveal-effect-with-react-three-fiber-glsl/](https://tympanus.net/codrops/2024/12/02/how-to-code-a-shader-based-reveal-effect-with-react-three-fiber-glsl/)
5. MeshTransmissionMaterial - React-Three-Drei, accessed December 8, 2025, [https://drei.docs.pmnd.rs/shaders/mesh-transmission-material](https://drei.docs.pmnd.rs/shaders/mesh-transmission-material)
6. Creating the Effect of Transparent Glass and Plastic in Three.js - Codrops, accessed December 8, 2025, [https://tympanus.net/codrops/2021/10/27/creating-the-effect-of-transparent-glass-and-plastic-in-three-js/](https://tympanus.net/codrops/2021/10/27/creating-the-effect-of-transparent-glass-and-plastic-in-three-js/)
7. Playing with Light and Refraction in Three.js: Warping 3D Text Inside a Glass Torus, accessed December 8, 2025, [https://tympanus.net/codrops/2025/03/13/warping-3d-text-inside-a-glass-torus/](https://tympanus.net/codrops/2025/03/13/warping-3d-text-inside-a-glass-torus/)
8. SelectiveBloom - React Postprocessing, accessed December 8, 2025, [https://react-postprocessing.docs.pmnd.rs/effects/selective-bloom](https://react-postprocessing.docs.pmnd.rs/effects/selective-bloom)
9. Three Fibre: BLOOM - How to set different intensity for different objects? : r/threejs - Reddit, accessed December 8, 2025, [https://www.reddit.com/r/threejs/comments/1ei5q98/three_fibre_bloom_how_to_set_different_intensity/](https://www.reddit.com/r/threejs/comments/1ei5q98/three_fibre_bloom_how_to_set_different_intensity/)
10. Bloom - React Postprocessing, accessed December 8, 2025, [https://react-postprocessing.docs.pmnd.rs/effects/bloom](https://react-postprocessing.docs.pmnd.rs/effects/bloom)
11. Post processing - Wawa Sensei, accessed December 8, 2025, [https://wawasensei.dev/courses/react-three-fiber/lessons/post-processing](https://wawasensei.dev/courses/react-three-fiber/lessons/post-processing)
12. An In-Depth Look at Color Grading Techniques in Three.js Post-Processing - MoldStud, accessed December 8, 2025, [https://moldstud.com/articles/p-an-in-depth-look-at-color-grading-techniques-in-threejs-post-processing](https://moldstud.com/articles/p-an-in-depth-look-at-color-grading-techniques-in-threejs-post-processing)
13. DHS Color Palette - Homeland Security, accessed December 8, 2025, [https://www.dhs.gov/xlibrary/dhsweb/_site/color-palette.html](https://www.dhs.gov/xlibrary/dhsweb/_site/color-palette.html)
14. Tutorial: Building a Collaborative Editing App with Yjs, valtio, and React - DEV Community, accessed December 8, 2025, [https://dev.to/route06/tutorial-building-a-collaborative-editing-app-with-yjs-valtio-and-react-1mcl](https://dev.to/route06/tutorial-building-a-collaborative-editing-app-with-yjs-valtio-and-react-1mcl)
15. valtio-yjs makes yjs state easy - GitHub, accessed December 8, 2025, [https://github.com/valtiojs/valtio-yjs](https://github.com/valtiojs/valtio-yjs)
16. State management in React using Valtio | by Usetech - Medium, accessed December 8, 2025, [https://medium.com/@usetech/state-management-in-react-using-valtio-8609fbcf0ad7](https://medium.com/@usetech/state-management-in-react-using-valtio-8609fbcf0ad7)
17. valtio-yjs - NPM, accessed December 8, 2025, [https://www.npmjs.com/package/valtio-yjs](https://www.npmjs.com/package/valtio-yjs)
18. Y.UndoManager - Yjs Docs, accessed December 8, 2025, [https://beta.yjs.dev/docs/api/undo-manager/](https://beta.yjs.dev/docs/api/undo-manager/)
19. How is UndoManager being used? - Yjs Community, accessed December 8, 2025, [https://discuss.yjs.dev/t/how-is-undomanager-being-used/1851](https://discuss.yjs.dev/t/how-is-undomanager-being-used/1851)
20. Y.UndoManager - Yjs Docs, accessed December 8, 2025, [https://docs.yjs.dev/api/undo-manager](https://docs.yjs.dev/api/undo-manager)
21. Getting Started with Yjs: The Fastest Way to Add Real-Time Collaboration to Your App, accessed December 8, 2025, [https://jewelhuq.medium.com/getting-started-with-yjs-the-fastest-way-to-add-real-time-collaboration-to-your-app-33a946540c73](https://jewelhuq.medium.com/getting-started-with-yjs-the-fastest-way-to-add-real-time-collaboration-to-your-app-33a946540c73)
22. Awareness & Presence - Yjs Docs, accessed December 8, 2025, [https://docs.yjs.dev/getting-started/adding-awareness](https://docs.yjs.dev/getting-started/adding-awareness)
23. Awareness | Hocuspocus Docs - Tiptap, accessed December 8, 2025, [https://tiptap.dev/docs/hocuspocus/guides/awareness](https://tiptap.dev/docs/hocuspocus/guides/awareness)
24. Attack Graph Generation Algorithm Implementation - IS MUNI, accessed December 8, 2025, [https://is.muni.cz/th/sjrvw/Attack_graph_generation_algorithm_implementation.pdf](https://is.muni.cz/th/sjrvw/Attack_graph_generation_algorithm_implementation.pdf)
25. MulVAL: A Logic-based Network Security Analyzer ∗ - USENIX, accessed December 8, 2025, [https://www.usenix.org/event/sec05/tech/full_papers/ou/ou.pdf](https://www.usenix.org/event/sec05/tech/full_papers/ou/ou.pdf)
26. risksense/mulval: A logic-based enterprise network security analyzer - GitHub, accessed December 8, 2025, [https://github.com/risksense/mulval](https://github.com/risksense/mulval)
27. CSV format for source data files | Aerospike Documentation, accessed December 8, 2025, [https://aerospike.com/docs/graph/develop/data-loading/csv-format/](https://aerospike.com/docs/graph/develop/data-loading/csv-format/)
28. Tutorial: Import data from a relational database into Neo4j - Getting Started, accessed December 8, 2025, [https://neo4j.com/docs/getting-started/data-import/import-relational-and-etl/](https://neo4j.com/docs/getting-started/data-import/import-relational-and-etl/)
29. cybersecurity/documentation/cybersecurity.adoc at main · neo4j-graph-examples/cybersecurity - GitHub, accessed December 8, 2025, [https://github.com/neo4j-graph-examples/cybersecurity/blob/main/documentation/cybersecurity.adoc](https://github.com/neo4j-graph-examples/cybersecurity/blob/main/documentation/cybersecurity.adoc)
30. Graphs for Cybersecurity: Knowledge Graph as Digital Twin - Neo4j, accessed December 8, 2025, [https://neo4j.com/blog/security/graphs-cybersecurity-knowledge-graph-digital-twin/](https://neo4j.com/blog/security/graphs-cybersecurity-knowledge-graph-digital-twin/)
31. Navigating TS 50701: Unpacking the Impact of the Cybersecurity Standard for Rail - Cylus, accessed December 8, 2025, [https://www.cylus.com/post/navigating-ts-50701-unpacking-the-impact-of-the-cybersecurity-standard-for-rail](https://www.cylus.com/post/navigating-ts-50701-unpacking-the-impact-of-the-cybersecurity-standard-for-rail)
32. Understanding ISA/IEC 62443: A Guide for OT Security Teams - Dragos, accessed December 8, 2025, [https://www.dragos.com/blog/isa-iec-62443-concepts](https://www.dragos.com/blog/isa-iec-62443-concepts)
33. Effective ICS Cybersecurity Using the IEC 62443 Standard - Fortinet, accessed December 8, 2025, [https://www.fortinet.com/content/dam/fortinet/assets/analyst-reports/report-sans-cybersecurity-iec-62443.pdf](https://www.fortinet.com/content/dam/fortinet/assets/analyst-reports/report-sans-cybersecurity-iec-62443.pdf)
34. OT Data Governance: NIST 800-82 & ISA-62443 for Secure Data Sharing, accessed December 8, 2025, [https://blog.dreamfactory.com/ot-data-governance-nist-800-82-isa-62443-for-secure-data-sharing](https://blog.dreamfactory.com/ot-data-governance-nist-800-82-isa-62443-for-secure-data-sharing)
35. LLM red teaming guide (open source) - Promptfoo, accessed December 8, 2025, [https://www.promptfoo.dev/docs/red-team/](https://www.promptfoo.dev/docs/red-team/)
36. What Is LLM Red Teaming? | DeepTeam, accessed December 8, 2025, [https://trydeepteam.com/docs/what-is-llm-red-teaming](https://trydeepteam.com/docs/what-is-llm-red-teaming)
37. RedCodeAgent: Automatic Red-teaming Agent against Diverse Code Agents - arXiv, accessed December 8, 2025, [https://arxiv.org/html/2510.02609v1](https://arxiv.org/html/2510.02609v1)
38. From Sands to Mansions: Simulating Full Attack Chain with LLM-Organized Knowledge - arXiv, accessed December 8, 2025, [https://arxiv.org/html/2407.16928v2](https://arxiv.org/html/2407.16928v2)
39. Tools - Docs by LangChain, accessed December 8, 2025, [https://docs.langchain.com/oss/python/langchain/tools](https://docs.langchain.com/oss/python/langchain/tools)
40. Beyond Built-in Tools: Creating Custom LangChain Tools for Real-World Applications | by Andrzej K. – Code & Tech Explorer - Medium, accessed December 8, 2025, [https://medium.com/@ako74programmer/beyond-built-in-tools-creating-custom-langchain-tools-for-real-world-applications-bc7dc2777c04](https://medium.com/@ako74programmer/beyond-built-in-tools-creating-custom-langchain-tools-for-real-world-applications-bc7dc2777c04)
41. OTX is a Free STIX/TAXII Feed - LevelBlue, accessed December 8, 2025, [https://levelblue.com/blogs/security-essentials/otx-is-now-a-free-stix-taxii-server](https://levelblue.com/blogs/security-essentials/otx-is-now-a-free-stix-taxii-server)
42. What is the Role of STIX/TAXII in Threat Intelligence Sharing? - Cyware, accessed December 8, 2025, [https://www.cyware.com/blog/what-is-the-role-of-stix-taxii-in-threat-intelligence-sharing](https://www.cyware.com/blog/what-is-the-role-of-stix-taxii-in-threat-intelligence-sharing)
43. Railway Safety: Understanding SRACs | PDF | Risk - Scribd, accessed December 8, 2025, [https://www.scribd.com/document/755836407/The-importance-of-SRACs-in-a-Railway-RAMS-Study](https://www.scribd.com/document/755836407/The-importance-of-SRACs-in-a-Railway-RAMS-Study)

**
