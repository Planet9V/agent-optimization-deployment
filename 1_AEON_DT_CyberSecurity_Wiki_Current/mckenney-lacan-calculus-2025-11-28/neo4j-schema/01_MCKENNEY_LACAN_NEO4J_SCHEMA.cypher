// ============================================================================
// McKenney-Lacan Calculus - Neo4j Graph Schema
// Version: 1.0.0
// Date: 2025-11-30
// Author: AEON Research Division (UAV-Swarm Synthesis)
// Classification: TOP SECRET // NOFORN // AEON EYES ONLY
// ============================================================================
// This schema implements the complete data model for the Psychohistory Engine
// supporting Ising dynamics, Granovetter cascades, Lacanian registers, and
// predictive Early Warning Systems (EWS).
// ============================================================================

// ============================================================================
// SECTION 1: CONSTRAINTS AND INDEXES
// ============================================================================

// Primary Key Constraints
CREATE CONSTRAINT actor_id_unique IF NOT EXISTS FOR (a:Actor) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT asset_id_unique IF NOT EXISTS FOR (a:Asset) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT event_id_unique IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT group_id_unique IF NOT EXISTS FOR (g:Group) REQUIRE g.id IS UNIQUE;
CREATE CONSTRAINT cve_id_unique IF NOT EXISTS FOR (v:Vulnerability) REQUIRE v.cve_id IS UNIQUE;
CREATE CONSTRAINT threat_actor_id_unique IF NOT EXISTS FOR (t:ThreatActor) REQUIRE t.id IS UNIQUE;

// Performance Indexes - Ising Model
CREATE INDEX actor_spin_idx IF NOT EXISTS FOR (a:Actor) ON (a.spin);
CREATE INDEX actor_threshold_idx IF NOT EXISTS FOR (a:Actor) ON (a.threshold);
CREATE INDEX actor_volatility_idx IF NOT EXISTS FOR (a:Actor) ON (a.volatility);

// Performance Indexes - Risk & EWS
CREATE INDEX asset_risk_idx IF NOT EXISTS FOR (a:Asset) ON (a.risk_score);
CREATE INDEX asset_criticality_idx IF NOT EXISTS FOR (a:Asset) ON (a.criticality);
CREATE INDEX actor_ews_variance_idx IF NOT EXISTS FOR (a:Actor) ON (a.ews_variance);
CREATE INDEX actor_ews_autocorr_idx IF NOT EXISTS FOR (a:Actor) ON (a.ews_autocorrelation);

// Performance Indexes - Temporal
CREATE INDEX event_timestamp_idx IF NOT EXISTS FOR (e:Event) ON (e.timestamp);
CREATE INDEX event_type_idx IF NOT EXISTS FOR (e:Event) ON (e.type);

// Performance Indexes - Psychometric
CREATE INDEX actor_lacan_real_idx IF NOT EXISTS FOR (a:Actor) ON (a.lacan_real);
CREATE INDEX actor_disc_d_idx IF NOT EXISTS FOR (a:Actor) ON (a.disc_d);

// Composite Indexes for Common Queries
CREATE INDEX actor_spin_threshold_idx IF NOT EXISTS FOR (a:Actor) ON (a.spin, a.threshold);
CREATE INDEX asset_risk_criticality_idx IF NOT EXISTS FOR (a:Asset) ON (a.risk_score, a.criticality);

// ============================================================================
// SECTION 2: NODE LABELS AND PROPERTY SCHEMAS
// ============================================================================

// ----------------------------------------------------------------------------
// 2.1 ACTOR NODE (Human/Agent Layer - The Ising Particles)
// ----------------------------------------------------------------------------
// Represents humans, AI agents, or organizational entities with psychometric
// properties derived from DISC × OCEAN tensor and Lacanian registers (RSI).

// Example Actor creation:
// CREATE (a:Actor {
//   id: 'ACTOR-001',
//   name: 'Willy Loman',
//   type: 'User',                    // Threat, Defender, User, Executive, Insider
//
//   // === ISING MODEL PROPERTIES ===
//   spin: 1,                         // σ ∈ {-1, +1} (Aligned/Opposed)
//   threshold: 0.3,                  // φ ∈ [0,1] (Granovetter activation threshold)
//   volatility: 0.5,                 // T (Temperature - noise/uncertainty)
//   external_field: 0.0,             // h_i (External pressure/influence)
//
//   // === PSYCHOMETRIC TENSOR (P = DISC ⊗ OCEAN) ===
//   // DISC Quadrant (Row Vector)
//   disc_d: 0.7,                     // Dominance [0,1]
//   disc_i: 0.4,                     // Influence [0,1]
//   disc_s: 0.3,                     // Steadiness [0,1]
//   disc_c: 0.6,                     // Conscientiousness [0,1]
//
//   // Big Five OCEAN (Column Vector)
//   ocean_o: 0.5,                    // Openness/Intellect [0,1]
//   ocean_c: 0.6,                    // Conscientiousness [0,1]
//   ocean_e: 0.4,                    // Extraversion [0,1]
//   ocean_a: 0.7,                    // Agreeableness [0,1]
//   ocean_n: 0.8,                    // Neuroticism [0,1]
//
//   // === LACANIAN REGISTERS (RSI) ===
//   lacan_real: 0.6,                 // R: Trauma, Drive, Zero-day exposure
//   lacan_symbolic: 0.4,             // S: Law, Protocol adherence, Signifier chains
//   lacan_imaginary: 0.5,            // I: Ego, Self-image, GUI/Interface trust
//
//   // === CB5T DERIVED PARAMETERS (for L-GRU Gates) ===
//   stability: 0.55,                 // (C + A + (1-N)) / 3 - Update Gate bias
//   plasticity: 0.45,                // (O + E) / 2 - Reset Gate bias
//
//   // === EARLY WARNING SYSTEM (EWS) METRICS ===
//   ews_variance: 0.12,              // σ² of recent behavior
//   ews_autocorrelation: 0.34,       // ρ(t, t-1) - Critical slowing signal
//   ews_critical_distance: 0.67,     // √|μ| - Distance to bifurcation
//   ews_last_updated: datetime(),    // Timestamp of last EWS calculation
//
//   // === DISCOURSE POSITION (Lacanian Four Discourses) ===
//   discourse_position: 'Agent',     // Agent, Other, Product, Truth
//   discourse_type: 'Hysteric',      // Master, University, Hysteric, Analyst
//
//   // === METADATA ===
//   created_at: datetime(),
//   updated_at: datetime(),
//   source: 'NER11_GOLD',
//   confidence: 0.95
// })

// ----------------------------------------------------------------------------
// 2.2 ASSET NODE (Technological Layer - Network Infrastructure)
// ----------------------------------------------------------------------------
// Represents servers, databases, applications, and network components.
// Used for epidemic R0 calculations via eigenvector centrality.

// Example Asset creation:
// CREATE (a:Asset {
//   id: 'ASSET-001',
//   name: 'PROD-DB-001',
//   type: 'Database',                // Server, Database, Network, Application, Endpoint
//
//   // === CRITICALITY & RISK ===
//   criticality: 0.95,               // Business criticality [0,1]
//   risk_score: 0.72,                // Current risk assessment [0,1]
//
//   // === NETWORK TOPOLOGY METRICS (from GDS) ===
//   eigenvector_centrality: 0.83,    // λ_max contribution (R0 calc)
//   pagerank: 0.024,                 // Importance in network
//   betweenness_centrality: 0.156,   // Bridge/chokepoint score
//   community_id: 12,                // Louvain cluster assignment
//
//   // === EPIDEMIC PARAMETERS ===
//   infection_rate: 0.0,             // β - Currently infected rate
//   recovery_rate: 0.0,              // γ - Patch/remediation rate
//
//   // === EWS METRICS ===
//   ews_variance: 0.08,
//   ews_autocorrelation: 0.22,
//
//   // === METADATA ===
//   ip_address: '10.0.1.50',
//   os: 'Linux',
//   last_scan: datetime(),
//   patch_level: 'Current'
// })

// ----------------------------------------------------------------------------
// 2.3 CONCEPT NODE (Ideological/Memetic Layer)
// ----------------------------------------------------------------------------
// Represents vulnerabilities, attack techniques, policies, and trends.
// These are the "ideas" that propagate through the network.

// Example Concept creation:
// CREATE (c:Concept {
//   id: 'CONCEPT-001',
//   name: 'Zero Trust Architecture',
//   type: 'Policy',                  // Vulnerability, Attack, Policy, Trend, Malware
//
//   // === SENTIMENT & PROPAGATION ===
//   sentiment: 0.8,                  // [-1,1] (Negative to Positive)
//   hype_cycle_phase: 0.6,           // [0,1] (Trigger -> Plateau)
//   adoption_rate: 0.35,             // Fraction of adopters
//
//   // === ENTROPY & INFORMATION ===
//   entropy: 2.3,                    // Information entropy (bits)
//   virality_r0: 1.4,                // Memetic reproduction number
//
//   // === MITRE MAPPING (if applicable) ===
//   mitre_id: null,
//   mitre_tactic: null,
//
//   // === METADATA ===
//   first_observed: datetime(),
//   last_mentioned: datetime(),
//   source_count: 47
// })

// ----------------------------------------------------------------------------
// 2.4 EVENT NODE (Temporal Layer - The Score Notes)
// ----------------------------------------------------------------------------
// Represents discrete events in time - attacks, detections, responses.
// Mapped to musical notation (Pitch, Duration, Volume, Timbre).

// Example Event creation:
// CREATE (e:Event {
//   id: 'EVENT-001',
//   timestamp: datetime('2025-11-30T10:15:00Z'),
//   type: 'Attack',                  // Attack, Detection, Response, Cascade, Bifurcation
//
//   // === SEVERITY & IMPACT ===
//   severity: 0.85,                  // [0,1]
//   impact_score: 0.72,
//
//   // === MUSICAL CALCULUS NOTATION ===
//   // Note N = (P, D, V, T) - Pitch, Duration, Volume, Timbre
//   musical_pitch: 72,               // MIDI note (C5 = high severity)
//   musical_duration: 0.5,           // Quarter note = 0.25, Half = 0.5
//   musical_volume: 100,             // Velocity [0-127]
//   musical_timbre: 'Brass',         // Instrument family (from DISC)
//
//   // === LACANIAN REGISTER ===
//   register: 'Real',                // Real, Symbolic, Imaginary
//
//   // === CASCADE TRACKING ===
//   cascade_id: 'CASCADE-001',       // If part of a cascade
//   cascade_order: 1,                // Position in cascade sequence
//
//   // === METADATA ===
//   source: 'SIEM',
//   raw_log: '...'
// })

// ----------------------------------------------------------------------------
// 2.5 GROUP NODE (Collective Layer - Monad/Dyad/Triad/Team)
// ----------------------------------------------------------------------------
// Represents collections of actors with emergent properties.

// Example Group creation:
// CREATE (g:Group {
//   id: 'GROUP-001',
//   name: 'Security Operations Team',
//   type: 'Team',                    // Monad, Dyad, Triad, Team, Organization, Nation
//
//   // === COLLECTIVE ISING PROPERTIES ===
//   magnetization: 0.72,             // m = Σσ/N (Group alignment)
//   susceptibility: 0.34,            // χ = ∂m/∂h (Response to external field)
//
//   // === GROUP DYNAMICS ===
//   cohesion: 0.85,                  // Internal coupling strength
//   diversity_index: 0.67,           // Cognitive diversity (node similarity)
//
//   // === SCHELLING SEGREGATION ===
//   segregation_index: 0.23,         // Unlike-neighbors ratio
//   happiness_score: 0.89,           // 1 - segregation if < tolerance
//
//   // === SIZE & STRUCTURE ===
//   member_count: 8,
//   hierarchy_depth: 2,
//
//   // === METADATA ===
//   formed_at: datetime(),
//   last_interaction: datetime()
// })

// ----------------------------------------------------------------------------
// 2.6 VULNERABILITY NODE (CVE/Exploit Layer)
// ----------------------------------------------------------------------------
// Specific vulnerability instances with epidemic parameters.

// Example Vulnerability creation:
// CREATE (v:Vulnerability {
//   cve_id: 'CVE-2025-12345',
//   name: 'Critical RCE in Widget Framework',
//
//   // === CVSS SCORES ===
//   cvss_base: 9.8,
//   cvss_temporal: 9.2,
//   cvss_environmental: 8.5,
//
//   // === EPIDEMIC PARAMETERS ===
//   infection_rate: 0.15,            // β - Exploitation rate
//   recovery_rate: 0.02,             // γ - Patch deployment rate
//
//   // === CALCULATED R0 ===
//   // R0 = (β/γ) × λ_max(A) - computed via Cypher
//   estimated_r0: 3.2,
//
//   // === EXTERNAL FIELD ===
//   field_strength: -0.8,            // h < 0 = Strong negative pressure
//
//   // === TIMELINE ===
//   disclosed: datetime(),
//   exploited_wild: datetime(),
//   patch_available: datetime(),
//
//   // === METADATA ===
//   cwe_id: 'CWE-94',
//   affected_products: ['Widget Framework 1.x', 'Widget Framework 2.x'],
//   epss_score: 0.87
// })

// ----------------------------------------------------------------------------
// 2.7 THREAT_ACTOR NODE (Adversary Layer)
// ----------------------------------------------------------------------------
// Known threat actors with behavioral profiles.

// Example ThreatActor creation:
// CREATE (t:ThreatActor {
//   id: 'TA-APT28',
//   name: 'APT28',
//   aliases: ['Fancy Bear', 'Sofacy', 'Pawn Storm'],
//
//   // === ISING PROPERTIES ===
//   spin: -1,                        // Adversarial alignment
//
//   // === PSYCHOMETRIC PROFILE (estimated) ===
//   disc_d: 0.9,                     // High Dominance
//   disc_i: 0.3,                     // Low Influence (secretive)
//   disc_s: 0.2,                     // Low Steadiness (adaptive)
//   disc_c: 0.8,                     // High Conscientiousness (methodical)
//
//   // === CAPABILITY & INTENT ===
//   sophistication: 0.95,
//   resources: 'Nation-State',
//   motivation: 'Espionage',
//
//   // === MITRE MAPPING ===
//   primary_tactics: ['Initial Access', 'Credential Access', 'Exfiltration'],
//
//   // === ACTIVITY ===
//   first_seen: datetime('2004-01-01'),
//   last_activity: datetime(),
//   active: true
// })

// ============================================================================
// SECTION 3: RELATIONSHIP TYPES
// ============================================================================

// ----------------------------------------------------------------------------
// 3.1 INFLUENCES - Social/Psychological Coupling (J_ij)
// ----------------------------------------------------------------------------
// Represents influence relationships between actors.
// The coupling constant J determines ferromagnetic (J>0) or
// antiferromagnetic (J<0) interactions in the Ising model.

// Example:
// MATCH (a:Actor {id: 'ACTOR-001'}), (b:Actor {id: 'ACTOR-002'})
// CREATE (a)-[:INFLUENCES {
//   weight: 0.75,                    // General influence strength [0,1]
//   J_coupling: 0.6,                 // Ising coupling constant
//   trust: 0.8,                      // Trust level [0,1]
//
//   // === INFLUENCE TYPE ===
//   type: 'Professional',            // Professional, Personal, Hierarchical, Adversarial
//   direction: 'Bidirectional',      // Unidirectional, Bidirectional
//
//   // === COMMUNICATION METRICS ===
//   interaction_frequency: 15,       // Interactions per week
//   last_interaction: datetime(),
//
//   // === DISCOURSE DYNAMICS ===
//   discourse_flow: 'Agent->Other',  // Lacanian discourse direction
//
//   // === METADATA ===
//   established: datetime(),
//   source: 'HR_SYSTEM'
// }]->(b)

// ----------------------------------------------------------------------------
// 3.2 CONNECTS_TO - Network Topology
// ----------------------------------------------------------------------------
// Physical or logical network connections between assets.

// Example:
// MATCH (a:Asset {id: 'ASSET-001'}), (b:Asset {id: 'ASSET-002'})
// CREATE (a)-[:CONNECTS_TO {
//   weight: 1.0,                     // Connection strength
//   bandwidth: 1000,                 // Mbps
//   latency: 2,                      // ms
//
//   // === PROTOCOL ===
//   protocol: 'TCP',
//   port: 5432,
//   encrypted: true,
//
//   // === TOPOLOGY TYPE ===
//   type: 'Internal',                // Internal, DMZ, External, VPN
//
//   // === METADATA ===
//   established: datetime()
// }]->(b)

// ----------------------------------------------------------------------------
// 3.3 MEMBER_OF - Group Membership
// ----------------------------------------------------------------------------
// Actor membership in groups (for collective dynamics).

// Example:
// MATCH (a:Actor {id: 'ACTOR-001'}), (g:Group {id: 'GROUP-001'})
// CREATE (a)-[:MEMBER_OF {
//   role: 'Analyst',
//   join_date: datetime(),
//
//   // === POSITION IN GROUP ===
//   hierarchy_level: 2,
//   influence_in_group: 0.6,
//
//   // === ACTIVITY ===
//   active: true,
//   participation_rate: 0.85
// }]->(g)

// ----------------------------------------------------------------------------
// 3.4 TARGETS - Attack Relationship
// ----------------------------------------------------------------------------
// Threat actor targeting relationship.

// Example:
// MATCH (t:ThreatActor {id: 'TA-APT28'}), (a:Asset {id: 'ASSET-001'})
// CREATE (t)-[:TARGETS {
//   confidence: 0.85,
//   timestamp: datetime(),
//
//   // === ATTACK DETAILS ===
//   technique: 'T1566.001',          // MITRE technique
//   campaign_id: 'CAMP-001',
//
//   // === STATUS ===
//   status: 'Active',                // Active, Historical, Suspected
//   success: null                    // null = ongoing, true/false = completed
// }]->(a)

// ----------------------------------------------------------------------------
// 3.5 ADOPTS - Behavior/Concept Adoption
// ----------------------------------------------------------------------------
// Actor adoption of concepts (for memetic propagation).

// Example:
// MATCH (a:Actor {id: 'ACTOR-001'}), (c:Concept {id: 'CONCEPT-001'})
// CREATE (a)-[:ADOPTS {
//   timestamp: datetime(),
//   conviction: 0.8,                 // Strength of adoption [0,1]
//
//   // === GRANOVETTER CASCADE ===
//   triggered_by_fraction: 0.35,     // What fraction triggered adoption
//   cascade_id: 'CASCADE-001',
//   cascade_order: 5,
//
//   // === METADATA ===
//   source: 'Training',              // Training, Peer, Policy, Incident
//   reversible: true
// }]->(c)

// ----------------------------------------------------------------------------
// 3.6 TRIGGERED - Cascade Chain
// ----------------------------------------------------------------------------
// Links events in a cascade sequence.

// Example:
// MATCH (e1:Event {id: 'EVENT-001'}), (e2:Event {id: 'EVENT-002'})
// CREATE (e1)-[:TRIGGERED {
//   delay: 120,                      // Seconds between events
//   cascade_id: 'CASCADE-001',
//
//   // === CAUSALITY ===
//   probability: 0.92,               // P(e2|e1)
//   mechanism: 'Network Propagation' // How it spread
// }]->(e2)

// ----------------------------------------------------------------------------
// 3.7 AFFECTS - Vulnerability Impact
// ----------------------------------------------------------------------------
// Vulnerability affecting asset.

// Example:
// MATCH (v:Vulnerability {cve_id: 'CVE-2025-12345'}), (a:Asset {id: 'ASSET-001'})
// CREATE (v)-[:AFFECTS {
//   confirmed: true,
//
//   // === IMPACT MODIFIERS ===
//   exploitability: 0.9,
//   impact_modifier: 0.85,           // Local environmental factor
//
//   // === REMEDIATION ===
//   patched: false,
//   compensating_controls: ['WAF', 'IDS'],
//
//   // === METADATA ===
//   discovered: datetime(),
//   scanner: 'Nessus'
// }]->(a)

// ----------------------------------------------------------------------------
// 3.8 PARTICIPATED_IN - Actor Event Participation
// ----------------------------------------------------------------------------
// Links actors to events they were involved in.

// Example:
// MATCH (a:Actor {id: 'ACTOR-001'}), (e:Event {id: 'EVENT-001'})
// CREATE (a)-[:PARTICIPATED_IN {
//   role: 'Victim',                  // Victim, Attacker, Responder, Witness
//
//   // === IMPACT ON ACTOR ===
//   spin_change: 0,                  // Did event flip their spin?
//   trauma_score: 0.3,               // Contribution to lacan_real
//
//   // === METADATA ===
//   timestamp: datetime()
// }]->(e)

// ============================================================================
// SECTION 4: GDS GRAPH PROJECTIONS
// ============================================================================

// 4.1 Social Network Projection (for Ising/Granovetter)
// CALL gds.graph.project(
//   'social_network',
//   'Actor',
//   {
//     INFLUENCES: {
//       orientation: 'UNDIRECTED',
//       properties: ['J_coupling', 'weight', 'trust']
//     }
//   },
//   {
//     nodeProperties: ['spin', 'threshold', 'volatility', 'external_field']
//   }
// )

// 4.2 Asset Network Projection (for R0 calculation)
// CALL gds.graph.project(
//   'asset_network',
//   'Asset',
//   {
//     CONNECTS_TO: {
//       orientation: 'UNDIRECTED',
//       properties: ['weight', 'bandwidth']
//     }
//   },
//   {
//     nodeProperties: ['criticality', 'risk_score']
//   }
// )

// 4.3 Full Psychohistory Projection (multi-node types)
// CALL gds.graph.project(
//   'psychohistory_full',
//   ['Actor', 'Asset', 'Concept', 'Group'],
//   {
//     INFLUENCES: {properties: ['J_coupling']},
//     CONNECTS_TO: {properties: ['weight']},
//     MEMBER_OF: {properties: ['influence_in_group']},
//     ADOPTS: {properties: ['conviction']}
//   }
// )

// ============================================================================
// SECTION 5: SAMPLE DATA FOR TESTING
// ============================================================================

// Create sample Actors (Willy Loman scenario adapted to cyber)
CREATE (willy:Actor {
  id: 'ACTOR-WILLY',
  name: 'Willy Loman',
  type: 'User',
  spin: -1,
  threshold: 0.2,
  volatility: 0.9,
  external_field: -0.5,
  disc_d: 0.3,
  disc_i: 0.7,
  disc_s: 0.2,
  disc_c: 0.4,
  ocean_o: 0.2,
  ocean_c: 0.3,
  ocean_e: 0.6,
  ocean_a: 0.5,
  ocean_n: 0.95,
  lacan_real: 0.9,
  lacan_symbolic: 0.3,
  lacan_imaginary: 0.8,
  stability: 0.28,
  plasticity: 0.4,
  ews_variance: 0.45,
  ews_autocorrelation: 0.78,
  ews_critical_distance: 0.15,
  discourse_position: 'Agent',
  discourse_type: 'Hysteric',
  created_at: datetime()
});

CREATE (linda:Actor {
  id: 'ACTOR-LINDA',
  name: 'Linda Loman',
  type: 'User',
  spin: 1,
  threshold: 0.8,
  volatility: 0.3,
  external_field: 0.2,
  disc_d: 0.2,
  disc_i: 0.5,
  disc_s: 0.9,
  disc_c: 0.8,
  ocean_o: 0.4,
  ocean_c: 0.85,
  ocean_e: 0.5,
  ocean_a: 0.95,
  ocean_n: 0.4,
  lacan_real: 0.3,
  lacan_symbolic: 0.8,
  lacan_imaginary: 0.6,
  stability: 0.8,
  plasticity: 0.45,
  ews_variance: 0.08,
  ews_autocorrelation: 0.12,
  ews_critical_distance: 0.85,
  discourse_position: 'Other',
  discourse_type: 'Master',
  created_at: datetime()
});

// Create influence relationship
MATCH (w:Actor {id: 'ACTOR-WILLY'}), (l:Actor {id: 'ACTOR-LINDA'})
CREATE (w)-[:INFLUENCES {
  weight: 0.9,
  J_coupling: 0.7,
  trust: 0.95,
  type: 'Personal',
  direction: 'Bidirectional',
  interaction_frequency: 100,
  last_interaction: datetime(),
  discourse_flow: 'Agent->Other'
}]->(l);

CREATE (l)-[:INFLUENCES {
  weight: 0.85,
  J_coupling: 0.6,
  trust: 0.98,
  type: 'Personal',
  direction: 'Bidirectional',
  interaction_frequency: 100,
  last_interaction: datetime(),
  discourse_flow: 'Other->Agent'
}]->(w);

// Create sample Event (The Crash)
CREATE (crash:Event {
  id: 'EVENT-CRASH',
  timestamp: datetime(),
  type: 'Bifurcation',
  severity: 0.95,
  impact_score: 0.9,
  musical_pitch: 84,
  musical_duration: 1.0,
  musical_volume: 120,
  musical_timbre: 'Percussion',
  register: 'Real'
});

// Link Actor to Event
MATCH (w:Actor {id: 'ACTOR-WILLY'}), (c:Event {id: 'EVENT-CRASH'})
CREATE (w)-[:PARTICIPATED_IN {
  role: 'Subject',
  spin_change: 0,
  trauma_score: 0.9,
  timestamp: datetime()
}]->(c);

// ============================================================================
// END OF SCHEMA DEFINITION
// ============================================================================
