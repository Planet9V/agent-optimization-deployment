/**
 * AEON Cyber Digital Twin - TypeScript Data Models
 *
 * Complete type definitions for all operational APIs and data structures.
 * Copy these types directly into your frontend project.
 *
 * Created: 2025-12-02 05:25:00 UTC
 * Version: 1.0.0
 * Status: Production-ready types for 3,889 entities
 */

// ============================================================================
// NER11 ENTITY EXTRACTION API
// ============================================================================

/**
 * 60 NER Labels (Tier 1) - Broad categorical classification
 */
export type NERLabel =
  // Threat Intelligence (15 labels)
  | 'MALWARE' | 'THREAT_ACTOR' | 'ATTACK_TECHNIQUE' | 'CVE' | 'CWE'
  | 'VULNERABILITY' | 'TACTIC' | 'TECHNIQUE' | 'TOOL' | 'INDICATOR'
  | 'CAMPAIGN' | 'APT_GROUP' | 'MITRE_EM3D' | 'THREAT_MODELING' | 'THREAT_PERCEPTION'

  // Infrastructure (12 labels)
  | 'DEVICE' | 'EQUIPMENT' | 'FACILITY' | 'PROTOCOL' | 'NETWORK'
  | 'PHYSICAL' | 'COMPONENT' | 'SOFTWARE_COMPONENT' | 'OPERATING_SYSTEM'
  | 'SYSTEM_ATTRIBUTES' | 'ENGINEERING_PHYSICAL' | 'VENDOR'

  // Organization (8 labels)
  | 'ORGANIZATION' | 'LOCATION' | 'SECTOR' | 'SECTORS' | 'ROLES'
  | 'SECURITY_TEAM' | 'DEMOGRAPHICS' | 'PERSONALITY'

  // Risk & Analysis (10 labels)
  | 'HAZARD_ANALYSIS' | 'IMPACT' | 'ANALYSIS' | 'MEASUREMENT' | 'RAMS'
  | 'IEC_62443' | 'STANDARD' | 'CONTROLS' | 'MITIGATION' | 'DETERMINISTIC_CONTROL'

  // Cognitive/Behavioral (5 labels)
  | 'COGNITIVE_BIAS' | 'LACANIAN' | 'PATTERNS' | 'PROCESS' | 'META'

  // Other (10 labels)
  | 'METADATA' | 'ATTRIBUTES' | 'TEMPLATES' | 'TIME_BASED_TREND'
  | 'OPERATIONAL_MODES' | 'PRIVILEGE_ESCALATION' | 'CYBER_SPECIFICS'
  | 'CORE_ONTOLOGY' | 'CWE_WEAKNESS' | 'MATERIAL';

/**
 * Common Fine-Grained Types (Tier 2) - Specific entity classification
 * Full list of 566 types available in documentation
 */
export type FineGrainedType =
  // Malware types (60+ types)
  | 'RANSOMWARE' | 'TROJAN' | 'WORM' | 'ROOTKIT' | 'RAT' | 'LOADER'
  | 'DROPPER' | 'BACKDOOR' | 'BOTNET' | 'SPYWARE' | 'ADWARE' | 'CRYPTOMINER'

  // Threat actor types (45+ types)
  | 'NATION_STATE' | 'APT_GROUP' | 'HACKTIVIST' | 'CRIME_SYNDICATE'
  | 'INSIDER' | 'SCRIPT_KIDDIE' | 'STATE_SPONSORED' | 'TERRORIST_GROUP'

  // Device types (120+ types)
  | 'PLC' | 'RTU' | 'HMI' | 'DCS' | 'SCADA_SERVER' | 'IED' | 'SENSOR'
  | 'ACTUATOR' | 'RELAY' | 'CIRCUIT_BREAKER' | 'TRANSFORMER' | 'SUBSTATION'

  // Cognitive bias types (25+ types)
  | 'CONFIRMATION_BIAS' | 'NORMALCY_BIAS' | 'AVAILABILITY_HEURISTIC'
  | 'ANCHORING' | 'RECENCY_BIAS' | 'OPTIMISM_BIAS' | 'DUNNING_KRUGER'

  // Protocol types (45+ types)
  | 'MODBUS' | 'DNP3' | 'IEC_61850' | 'PROFINET' | 'ETHERNET_IP'
  | 'BACNET' | 'OPC_UA' | 'S7COMM' | 'CIP' | 'FINS'

  // Software types (30+ types)
  | 'LIBRARY' | 'PACKAGE' | 'FRAMEWORK' | 'APPLICATION' | 'OPERATING_SYSTEM'
  | 'FIRMWARE' | 'DRIVER' | 'KERNEL_MODULE' | 'SERVICE' | 'DAEMON'

  | string;  // Allow any string for extensibility

/**
 * POST /ner request
 */
export interface NERRequest {
  text: string;  // Max 100,000 characters
}

/**
 * Extracted entity from NER11 API
 */
export interface NEREntity {
  text: string;       // Extracted entity text
  label: NERLabel;    // One of 60 NER labels
  start: number;      // Character position start
  end: number;        // Character position end
  score: number;      // Confidence 0.0-1.0 (typically 0.9-1.0)
}

/**
 * POST /ner response
 */
export interface NERResponse {
  entities: NEREntity[];
  doc_length: number;  // Number of characters in input
}

// ============================================================================
// SEMANTIC SEARCH API
// ============================================================================

/**
 * POST /search/semantic request
 */
export interface SemanticSearchRequest {
  query: string;                    // Search query text (required, 1-1000 chars)
  limit?: number;                   // Max results (1-100, default 10)
  label_filter?: NERLabel;          // Tier 1 filter (optional)
  fine_grained_filter?: FineGrainedType;  // Tier 2 filter (optional, MOST POWERFUL)
  confidence_threshold?: number;    // Min NER confidence (0.0-1.0, default 0.0)
}

/**
 * Search result from semantic search
 */
export interface SemanticSearchResult {
  score: number;                    // Similarity score 0.0-1.0
  entity: string;                   // Entity text
  ner_label: NERLabel;             // Tier 1 classification
  fine_grained_type: FineGrainedType;  // Tier 2 classification
  hierarchy_path: string;           // Full path (e.g., "MALWARE/RANSOMWARE/WannaCry")
  confidence: number;               // NER extraction confidence
  doc_id: string;                   // Source document identifier
}

/**
 * POST /search/semantic response
 */
export interface SemanticSearchResponse {
  results: SemanticSearchResult[];
  total_found: number;
  query: string;
}

// ============================================================================
// HYBRID SEARCH API
// ============================================================================

/**
 * Relationship types in Neo4j knowledge graph
 */
export type RelationshipType =
  // Attack relationships
  | 'EXPLOITS'        // Malware exploits vulnerabilities
  | 'USES'            // Threat actors use malware/tools
  | 'TARGETS'         // Attacks target assets
  | 'AFFECTS'         // Vulnerabilities affect software/devices
  | 'ATTRIBUTED_TO'   // Attacks attributed to threat actors

  // Defense relationships
  | 'MITIGATES'       // Controls mitigate vulnerabilities
  | 'PROTECTS'        // Controls protect assets
  | 'DETECTS'         // Indicators detect threats

  // Analysis relationships
  | 'INDICATES'       // Indicators signal threats
  | 'EXHIBITS'        // Users exhibit cognitive biases
  | 'CONTRIBUTES_TO'  // Biases contribute to incidents

  // Structural relationships
  | 'BELONGS_TO' | 'LOCATED_AT' | 'PART_OF' | 'HAS_VULNERABILITY'
  | 'RUNS' | 'DEPENDS_ON' | 'CONNECTS_TO'

  | string;  // Allow any relationship type

/**
 * POST /search/hybrid request
 */
export interface HybridSearchRequest {
  query: string;                        // Search query (required, 1-1000 chars)
  limit?: number;                       // Max semantic results (1-100, default 10)
  expand_graph?: boolean;               // Enable Neo4j graph expansion (default true)
  hop_depth?: number;                   // Graph traversal depth 1-3 (default 2)
  label_filter?: NERLabel;              // Tier 1 filter
  fine_grained_filter?: FineGrainedType;  // Tier 2 filter
  confidence_threshold?: number;        // Min confidence (0.0-1.0, default 0.0)
  relationship_types?: RelationshipType[];  // Filter relationship types
}

/**
 * Related entity from graph expansion
 */
export interface RelatedEntity {
  name: string;                         // Entity name
  label: string;                        // Neo4j label (ThreatActor, Malware, Asset, etc.)
  ner_label: NERLabel;                 // Tier 1
  fine_grained_type: FineGrainedType;  // Tier 2
  hierarchy_path: string;               // Full hierarchical path
  hop_distance: number;                 // Distance from source (1-3)
  relationship: RelationshipType;       // Relationship type
  relationship_direction: 'outgoing' | 'incoming';  // Direction of relationship
}

/**
 * Graph context for an entity
 */
export interface GraphContext {
  node_exists: boolean;                 // Entity exists in Neo4j
  outgoing_relationships: number;       // Count of outgoing edges
  incoming_relationships: number;       // Count of incoming edges
  labels: string[];                     // Neo4j labels on the node
  properties: Record<string, any>;      // Node properties
}

/**
 * Hybrid search result (semantic + graph)
 */
export interface HybridSearchResult {
  score: number;                        // Adjusted score (semantic + graph boost)
  entity: string;
  ner_label: NERLabel;
  fine_grained_type: FineGrainedType;
  hierarchy_path: string;
  confidence: number;
  doc_id: string;
  related_entities: RelatedEntity[];    // Graph expansion results
  graph_context: GraphContext;          // Graph metadata
}

/**
 * POST /search/hybrid response
 */
export interface HybridSearchResponse {
  results: HybridSearchResult[];
  query: string;
  total_results: number;
  search_type: 'hybrid';
  qdrant_time_ms: number;               // Semantic search time
  neo4j_time_ms: number;                // Graph expansion time
  total_time_ms: number;                // Total response time
  filters_applied: Record<string, any>;
}

// ============================================================================
// NEO4J KNOWLEDGE GRAPH
// ============================================================================

/**
 * Neo4j Super Labels (16 labels from E27 framework)
 */
export type Neo4jSuperLabel =
  // Threat Intelligence
  | 'ThreatActor' | 'AttackPattern' | 'Vulnerability' | 'Malware'
  | 'Indicator' | 'Campaign' | 'Control'

  // Infrastructure
  | 'Asset' | 'Organization' | 'Location' | 'Protocol' | 'Software'

  // Psychometric
  | 'PsychTrait' | 'Role'

  // Economic & Events
  | 'EconomicMetric' | 'Event';

/**
 * Hierarchical node properties (E30 enhancement)
 */
export interface HierarchicalNodeProperties {
  id: string;                      // UUID
  name: string;                    // Entity name
  ner_label: NERLabel;            // Tier 1
  fine_grained_type: FineGrainedType;  // Tier 2
  specific_instance: string;      // Tier 3
  hierarchy_path: string;         // Full path
  hierarchy_level: number;        // 1, 2, or 3
  confidence: number;             // NER confidence
  created_at: string;             // ISO timestamp
  updated_at?: string;            // ISO timestamp
}

/**
 * Malware node (example of label-specific properties)
 */
export interface MalwareNode extends HierarchicalNodeProperties {
  malwareFamily?: string;
  platform?: string;              // windows, linux, macos, cross-platform
  capabilities?: string[];        // persistence, lateral_movement, etc.
}

/**
 * Threat Actor node
 */
export interface ThreatActorNode extends HierarchicalNodeProperties {
  actorType?: string;             // nation-state, cybercrime, hacktivist
  sophistication?: string;        // low, medium, high, advanced
  motivation?: string;            // financial, espionage, sabotage
  country?: string;
}

/**
 * Asset node (ICS/IT devices)
 */
export interface AssetNode extends HierarchicalNodeProperties {
  assetClass?: string;
  deviceType?: string;
  vendor?: string;
  model?: string;
  firmware_version?: string;
}

/**
 * Vulnerability node
 */
export interface VulnerabilityNode extends HierarchicalNodeProperties {
  cve_id?: string;
  cvss_score?: number;
  severity?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  published_date?: string;
}

/**
 * Cognitive Bias node
 */
export interface PsychTraitNode extends HierarchicalNodeProperties {
  traitType?: string;
  subtype?: string;
  description?: string;
}

// ============================================================================
// QDRANT VECTOR DATABASE
// ============================================================================

/**
 * Qdrant collection configuration
 */
export interface QdrantCollection {
  name: 'ner11_entities_hierarchical';
  vector_size: 384;
  distance: 'Cosine';
  points_count: number;  // Currently 3,889
}

/**
 * Qdrant payload (entity metadata)
 */
export interface QdrantPayload {
  entity: string;
  ner_label: NERLabel;
  fine_grained_type: FineGrainedType;
  specific_instance: string;
  hierarchy_path: string;
  hierarchy_level: number;
  confidence: number;
  classification_confidence: number;
  doc_id: string;
  created_at: string;
}

/**
 * Qdrant point (vector + payload)
 */
export interface QdrantPoint {
  id: number | string;
  vector: number[];           // 384-dimensional embedding
  payload: QdrantPayload;
}

// ============================================================================
// HELPER TYPES
// ============================================================================

/**
 * API Response wrapper
 */
export interface APIResponse<T> {
  data: T;
  status: number;
  message?: string;
}

/**
 * Error response
 */
export interface APIError {
  detail: string;
  status_code: number;
}

/**
 * Pagination params (for future APIs)
 */
export interface PaginationParams {
  page?: number;
  per_page?: number;
  offset?: number;
  limit?: number;
}

/**
 * Sort params (for future APIs)
 */
export interface SortParams {
  sort_by?: string;
  order?: 'asc' | 'desc';
}

// ============================================================================
// REACT HOOK TYPES
// ============================================================================

/**
 * Semantic search hook state
 */
export interface UseSemanticSearchState {
  results: SemanticSearchResult[];
  loading: boolean;
  error: string | null;
  search: (query: string, options?: Partial<SemanticSearchRequest>) => Promise<SemanticSearchResult[]>;
}

/**
 * Hybrid search hook state
 */
export interface UseHybridSearchState {
  results: HybridSearchResult[];
  loading: boolean;
  error: string | null;
  performance: {
    qdrant: number;
    neo4j: number;
    total: number;
  } | null;
  search: (query: string, options?: Partial<HybridSearchRequest>) => Promise<HybridSearchResult[]>;
}

/**
 * Neo4j hook state
 */
export interface UseNeo4jState {
  driver: any | null;  // neo4j.Driver
  connected: boolean;
  error: string | null;
  runQuery: (cypher: string, params?: Record<string, any>) => Promise<any[]>;
}

// ============================================================================
// UI COMPONENT PROPS
// ============================================================================

/**
 * Entity card component props
 */
export interface EntityCardProps {
  entity: SemanticSearchResult | HybridSearchResult;
  onClick?: (entity: string) => void;
  showGraph?: boolean;
}

/**
 * Search bar component props
 */
export interface SearchBarProps {
  onSearch: (query: string, filters?: SearchFilters) => void;
  loading?: boolean;
  placeholder?: string;
}

/**
 * Search filters
 */
export interface SearchFilters {
  label_filter?: NERLabel;
  fine_grained_filter?: FineGrainedType;
  confidence_threshold?: number;
}

/**
 * Graph visualization props
 */
export interface GraphVisualizationProps {
  entity: HybridSearchResult;
  width?: number;
  height?: number;
  onNodeClick?: (node: RelatedEntity) => void;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

/**
 * Hierarchy path parser result
 */
export interface ParsedHierarchyPath {
  tier1: string;      // NER label
  tier2: string;      // Fine-grained type
  tier3: string;      // Specific instance
  full: string;       // Full path
}

/**
 * Entity statistics
 */
export interface EntityStatistics {
  total_entities: number;
  tier1_labels: number;
  tier2_types: number;
  tier3_instances: number;
  most_common_type: string;
  most_common_label: string;
}

/**
 * Search performance metrics
 */
export interface SearchPerformance {
  query: string;
  results_count: number;
  response_time_ms: number;
  qdrant_time_ms?: number;
  neo4j_time_ms?: number;
  timestamp: string;
}

// ============================================================================
// EXAMPLE USAGE
// ============================================================================

/*
// Import in your React component:
import {
  NERRequest,
  NERResponse,
  SemanticSearchRequest,
  SemanticSearchResponse,
  HybridSearchRequest,
  HybridSearchResponse,
  UseSemanticSearchState
} from './DATA_MODELS';

// Use with axios:
const response = await axios.post<NERResponse>(
  'http://localhost:8000/ner',
  { text: 'APT29 ransomware' } as NERRequest
);

const entities: NEREntity[] = response.data.entities;

// Use with React hooks:
const { results, loading, search }: UseSemanticSearchState = useSemanticSearch();

await search('ransomware', {
  fine_grained_filter: 'RANSOMWARE'
});

// results is now typed as SemanticSearchResult[]
results.forEach(r => {
  console.log(r.entity, r.fine_grained_type);  // Full IntelliSense!
});
*/

// ============================================================================
// EXPORT ALL TYPES
// ============================================================================

export type {
  // NER11 Types
  NERLabel,
  FineGrainedType,
  NERRequest,
  NEREntity,
  NERResponse,

  // Search Types
  SemanticSearchRequest,
  SemanticSearchResult,
  SemanticSearchResponse,
  HybridSearchRequest,
  HybridSearchResult,
  HybridSearchResponse,
  RelatedEntity,
  GraphContext,

  // Neo4j Types
  Neo4jSuperLabel,
  HierarchicalNodeProperties,
  MalwareNode,
  ThreatActorNode,
  AssetNode,
  VulnerabilityNode,
  PsychTraitNode,

  // Qdrant Types
  QdrantCollection,
  QdrantPayload,
  QdrantPoint,

  // Helper Types
  APIResponse,
  APIError,
  PaginationParams,
  SortParams,

  // Hook Types
  UseSemanticSearchState,
  UseHybridSearchState,
  UseNeo4jState,

  // Component Types
  EntityCardProps,
  SearchBarProps,
  SearchFilters,
  GraphVisualizationProps,

  // Utility Types
  ParsedHierarchyPath,
  EntityStatistics,
  SearchPerformance
};
