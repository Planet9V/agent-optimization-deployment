// ═══════════════════════════════════════════════════════════════
// ENHANCED PSYCHOMETRIC SCHEMA FOR THREAT ACTOR PROFILING
// Extends Layer 4 with Lacanian, Big 5, Discourse Analysis
// File: ENHANCED_PSYCHOMETRIC_SCHEMA.cypher
// Created: 2025-10-29
// Version: v1.0.0
// Author: System Architecture Designer
// Purpose: Comprehensive psychometric profiling for threat actors
// Status: ACTIVE
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// ENHANCED NODE: ThreatActorProfile (Extended Psychometric Properties)
// ───────────────────────────────────────────────────────────────
// Extends existing ThreatActorProfile with comprehensive psychometric dimensions

// EXISTING PROPERTIES (preserved from Layer 4):
//   id, threat_actor_id, intent_primary, intent_secondary, modus_operandi,
//   preferred_tools, preferred_vectors, attack_timing, operational_tempo,
//   risk_tolerance, anti_forensics_capability, psychological_profile

// NEW PROPERTIES - Lacanian Registers (0.0-1.0 scores):
//   lacanian_symbolic_score: float        // Symbolic order: language, law, social norms
//   lacanian_imaginary_score: float       // Imaginary: self-image, ego, ideal-self
//   lacanian_real_score: float            // Real: unrepresentable trauma, drives
//   lacanian_dominant_register: enum [SYMBOLIC, IMAGINARY, REAL, BALANCED]

// NEW PROPERTIES - Big 5 Personality Traits (0.0-1.0 scores):
//   big5_openness: float                  // Openness to experience
//   big5_conscientiousness: float         // Conscientiousness and organization
//   big5_extraversion: float              // Extraversion and social engagement
//   big5_agreeableness: float             // Agreeableness and cooperation
//   big5_neuroticism: float               // Emotional stability/neuroticism

// NEW PROPERTIES - Discourse Positions (confidence scores 0.0-1.0):
//   discourse_master_score: float         // Master: authority, control, commands
//   discourse_university_score: float     // University: knowledge, expertise, systems
//   discourse_hysteric_score: float       // Hysteric: questioning, challenging authority
//   discourse_analyst_score: float        // Analyst: interpretation, hidden meanings
//   discourse_dominant_position: enum [MASTER, UNIVERSITY, HYSTERIC, ANALYST, MIXED]

// NEW PROPERTIES - Psychological Patterns:
//   defense_mechanisms: string[]          // e.g., ["rationalization", "projection", "denial"]
//   transference_patterns: string[]       // e.g., ["authority_defiance", "peer_validation"]
//   cognitive_biases: string[]            // e.g., ["confirmation_bias", "anchoring", "overconfidence"]
//   emotional_triggers: string[]          // e.g., ["perceived_injustice", "status_threat"]

// NEW PROPERTIES - Confidence & Validation:
//   profile_confidence: float (0.0-1.0)   // Overall profile confidence
//   data_sources: string[]                // Sources used for profiling
//   last_updated: datetime                // Profile update timestamp
//   validation_status: enum [UNVALIDATED, PARTIAL, VALIDATED, EXPERT_REVIEWED]
//   analyst_notes: string                 // Human analyst observations

// ───────────────────────────────────────────────────────────────

// Example Enhanced ThreatActorProfile for APT29
CREATE (enhanced_profile:ThreatActorProfile {
  // EXISTING PROPERTIES (from Layer 4)
  id: 'profile-apt29-enhanced-001',
  threat_actor_id: 'threat-actor-apt29',
  intent_primary: 'Long-term intelligence collection from government and diplomatic targets',
  intent_secondary: ['Technology transfer', 'Geopolitical intelligence', 'COVID-19 vaccine research theft'],
  modus_operandi: 'Multi-stage intrusion with stealthy persistence mechanisms and legitimate credential abuse',
  preferred_tools: ['SUNBURST', 'Cobalt Strike', 'PowerShell', 'WMI'],
  preferred_vectors: ['Spear-phishing', 'Supply chain compromise', 'Cloud infrastructure exploitation'],
  attack_timing: 'CAMPAIGN',
  operational_tempo: 'SLOW_AND_METHODICAL',
  risk_tolerance: 'LOW',
  anti_forensics_capability: 'ADVANCED',
  psychological_profile: 'Patient, disciplined, state-sponsored operators with long-term strategic objectives.',

  // NEW PROPERTIES - Lacanian Registers
  lacanian_symbolic_score: 0.85,          // High symbolic: operates within state structures, follows protocols
  lacanian_imaginary_score: 0.45,         // Moderate imaginary: professional identity, not ego-driven
  lacanian_real_score: 0.25,              // Low real: minimal chaotic/impulsive behavior
  lacanian_dominant_register: 'SYMBOLIC',

  // NEW PROPERTIES - Big 5 Personality
  big5_openness: 0.72,                    // High openness: innovative TTPs, adaptive strategies
  big5_conscientiousness: 0.88,           // Very high: methodical, organized, disciplined
  big5_extraversion: 0.35,                // Low extraversion: covert operations, minimal public engagement
  big5_agreeableness: 0.25,               // Low agreeableness: adversarial, competitive
  big5_neuroticism: 0.15,                 // Low neuroticism: emotionally stable, patient under pressure

  // NEW PROPERTIES - Discourse Positions
  discourse_master_score: 0.35,           // Moderate master: follows state authority
  discourse_university_score: 0.78,       // High university: systematic knowledge application
  discourse_hysteric_score: 0.15,         // Low hysteric: not questioning authority
  discourse_analyst_score: 0.62,          // High analyst: interpreting intelligence, hidden patterns
  discourse_dominant_position: 'UNIVERSITY',

  // NEW PROPERTIES - Psychological Patterns
  defense_mechanisms: ['intellectualization', 'compartmentalization', 'rationalization'],
  transference_patterns: ['state_authority_alignment', 'professional_identity_reinforcement'],
  cognitive_biases: ['confirmation_bias', 'group_attribution_error', 'planning_fallacy'],
  emotional_triggers: ['national_security_threats', 'geopolitical_competition', 'technological_superiority'],

  // NEW PROPERTIES - Confidence & Validation
  profile_confidence: 0.82,
  data_sources: ['MITRE ATT&CK', 'FBI indictments', 'FireEye threat reports', 'CrowdStrike intelligence'],
  last_updated: datetime('2025-10-29T10:00:00Z'),
  validation_status: 'EXPERT_REVIEWED',
  analyst_notes: 'Profile based on 15+ years of observed behavior, SolarWinds campaign analysis, and declassified intelligence reports.'
});

// ───────────────────────────────────────────────────────────────
// NEW NODE: PsychologicalPattern
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID - UNIQUE CONSTRAINT
//   pattern_type: enum [DEFENSE_MECHANISM, COGNITIVE_BIAS, EMOTIONAL_TRIGGER,
//                       BEHAVIORAL_PATTERN, DECISION_HEURISTIC]
//   name: string (e.g., "Confirmation Bias", "Rationalization")
//   description: string
//   manifestation_indicators: string[]    // Observable behaviors
//   lacanian_register: enum [SYMBOLIC, IMAGINARY, REAL, MULTIPLE]
//   severity_level: enum [LOW, MODERATE, HIGH, CRITICAL]
//   detection_confidence: float (0.0-1.0)
//   evidence: string[]                    // Evidence of this pattern
//   is_shared: boolean (always true)
//   customer_namespace: "shared:psychology"
// ───────────────────────────────────────────────────────────────

CREATE (pattern_rationalization:PsychologicalPattern {
  id: 'psych-pattern-rationalization-001',
  pattern_type: 'DEFENSE_MECHANISM',
  name: 'Rationalization',
  description: 'Justifying malicious actions through logical reasoning or national security arguments',
  manifestation_indicators: [
    'Framing attacks as defensive measures',
    'Citing geopolitical necessity',
    'Minimizing harm to victims',
    'Emphasizing strategic importance'
  ],
  lacanian_register: 'SYMBOLIC',
  severity_level: 'MODERATE',
  detection_confidence: 0.78,
  evidence: [
    'Public statements from state sponsors',
    'Operational patterns showing selective targeting',
    'Post-attribution justifications'
  ],
  is_shared: true,
  customer_namespace: 'shared:psychology'
});

CREATE (pattern_confirmation_bias:PsychologicalPattern {
  id: 'psych-pattern-confirmation-bias-001',
  pattern_type: 'COGNITIVE_BIAS',
  name: 'Confirmation Bias',
  description: 'Tendency to seek and interpret intelligence that confirms pre-existing hypotheses',
  manifestation_indicators: [
    'Repeated targeting of same sectors',
    'Ignoring contradictory intelligence',
    'Pattern persistence despite failures',
    'Selective data collection'
  ],
  lacanian_register: 'IMAGINARY',
  severity_level: 'MODERATE',
  detection_confidence: 0.65,
  evidence: [
    'Campaign continuity analysis',
    'Target selection patterns',
    'Response to defensive measures'
  ],
  is_shared: true,
  customer_namespace: 'shared:psychology'
});

CREATE (pattern_planning_fallacy:PsychologicalPattern {
  id: 'psych-pattern-planning-fallacy-001',
  pattern_type: 'COGNITIVE_BIAS',
  name: 'Planning Fallacy',
  description: 'Underestimating time, costs, and risks while overestimating benefits',
  manifestation_indicators: [
    'Complex campaigns with unrealistic timelines',
    'Inadequate contingency planning',
    'Overconfidence in operational success',
    'Insufficient counter-detection measures'
  ],
  lacanian_register: 'IMAGINARY',
  severity_level: 'LOW',
  detection_confidence: 0.55,
  evidence: [
    'Campaign duration vs. objectives',
    'Detection timeline analysis',
    'Attribution timing patterns'
  ],
  is_shared: true,
  customer_namespace: 'shared:psychology'
});

CREATE (pattern_geopolitical_competition:PsychologicalPattern {
  id: 'psych-pattern-geopolitical-trigger-001',
  pattern_type: 'EMOTIONAL_TRIGGER',
  name: 'Geopolitical Competition Trigger',
  description: 'Emotional activation from perceived geopolitical threats or competitive disadvantage',
  manifestation_indicators: [
    'Campaign timing correlates with geopolitical events',
    'Targeting aligned with national interests',
    'Escalation during diplomatic tensions',
    'Sector targeting matches strategic priorities'
  ],
  lacanian_register: 'REAL',
  severity_level: 'HIGH',
  detection_confidence: 0.82,
  evidence: [
    'Timeline correlation with international events',
    'Diplomatic incident analysis',
    'Target sector alignment with state interests'
  ],
  is_shared: true,
  customer_namespace: 'shared:psychology'
});

// ───────────────────────────────────────────────────────────────
// NEW NODE: BiasIndicator
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID - UNIQUE CONSTRAINT
//   bias_type: enum [COGNITIVE, ATTRIBUTION, PERCEPTION, DECISION_MAKING, SOCIAL]
//   name: string
//   description: string
//   detection_method: string              // How this bias is detected
//   observable_behaviors: string[]        // Specific behaviors indicating bias
//   confidence_threshold: float           // Minimum confidence for detection
//   false_positive_rate: float            // Known false positive rate
//   mitigation_strategies: string[]       // How to account for this bias
//   is_shared: boolean (always true)
//   customer_namespace: "shared:bias-detection"
// ───────────────────────────────────────────────────────────────

CREATE (bias_overconfidence:BiasIndicator {
  id: 'bias-indicator-overconfidence-001',
  bias_type: 'COGNITIVE',
  name: 'Overconfidence Bias',
  description: 'Excessive confidence in operational capabilities or intelligence assessments',
  detection_method: 'Analysis of campaign complexity vs. actual success rates, operational mistakes patterns',
  observable_behaviors: [
    'Attempting operations beyond demonstrated capability',
    'Minimal contingency planning',
    'Predictable TTPs despite attribution',
    'Insufficient OPSEC in high-risk operations'
  ],
  confidence_threshold: 0.65,
  false_positive_rate: 0.35,
  mitigation_strategies: [
    'Cross-validate with multiple intelligence sources',
    'Consider historical success/failure rates',
    'Account for visibility bias in detected operations',
    'Evaluate undetected operations possibility'
  ],
  is_shared: true,
  customer_namespace: 'shared:bias-detection'
});

CREATE (bias_anchoring:BiasIndicator {
  id: 'bias-indicator-anchoring-001',
  bias_type: 'COGNITIVE',
  name: 'Anchoring Bias',
  description: 'Over-reliance on initial intelligence or first successful TTP',
  detection_method: 'Pattern persistence analysis, TTP evolution rate measurement',
  observable_behaviors: [
    'Continued use of compromised tools',
    'Repeated infrastructure patterns',
    'Consistent targeting methodology',
    'Limited adaptation to defenses'
  ],
  confidence_threshold: 0.70,
  false_positive_rate: 0.25,
  mitigation_strategies: [
    'Track TTP evolution over time',
    'Identify adaptation triggers',
    'Monitor for tool/infrastructure changes',
    'Assess learning curves from failures'
  ],
  is_shared: true,
  customer_namespace: 'shared:bias-detection'
});

CREATE (bias_attribution:BiasIndicator {
  id: 'bias-indicator-group-attribution-001',
  bias_type: 'ATTRIBUTION',
  name: 'Group Attribution Error',
  description: 'Attributing individual operator behaviors to entire threat actor organization',
  detection_method: 'Operator variance analysis, sub-group behavior clustering',
  observable_behaviors: [
    'Inconsistent operational quality',
    'Tool usage variations',
    'Timing pattern differences',
    'Sophistication level variance'
  ],
  confidence_threshold: 0.60,
  false_positive_rate: 0.40,
  mitigation_strategies: [
    'Cluster analysis for sub-groups',
    'Individual operator tracking where possible',
    'Acknowledge organizational heterogeneity',
    'Distinguish unit-level vs. organizational patterns'
  ],
  is_shared: true,
  customer_namespace: 'shared:bias-detection'
});

// ───────────────────────────────────────────────────────────────
// NEW NODE: DiscourseDimension
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID - UNIQUE CONSTRAINT
//   position: enum [MASTER, UNIVERSITY, HYSTERIC, ANALYST]
//   description: string
//   characteristic_behaviors: string[]
//   communication_patterns: string[]
//   power_dynamics: string                // How power is exercised/resisted
//   knowledge_relation: string            // Relationship to knowledge/expertise
//   desire_structure: string              // What drives this discourse position
//   typical_threat_actors: string[]       // Example threat actor types
//   is_shared: boolean (always true)
//   customer_namespace: "shared:discourse-analysis"
// ───────────────────────────────────────────────────────────────

CREATE (discourse_master:DiscourseDimension {
  id: 'discourse-master-001',
  position: 'MASTER',
  description: 'Discourse of the Master: Authority, command, control. Operates from position of assumed knowledge and power.',
  characteristic_behaviors: [
    'Directive operational style',
    'Clear command structure',
    'Authoritative decision-making',
    'Minimal justification required'
  ],
  communication_patterns: [
    'Commands rather than requests',
    'Assertion of dominance',
    'Minimal explanation',
    'Expects compliance'
  ],
  power_dynamics: 'Exercises power through authority and command. Assumes right to act without extensive justification.',
  knowledge_relation: 'Claims knowledge without needing to demonstrate it. Knowledge as tool of power.',
  desire_structure: 'Desires recognition of authority and maintenance of power structure.',
  typical_threat_actors: ['State-sponsored APTs with direct government backing', 'Organized crime leadership', 'Hacktivist leaders'],
  is_shared: true,
  customer_namespace: 'shared:discourse-analysis'
});

CREATE (discourse_university:DiscourseDimension {
  id: 'discourse-university-001',
  position: 'UNIVERSITY',
  description: 'Discourse of the University: Knowledge, systems, expertise. Operates through systematic application of knowledge.',
  characteristic_behaviors: [
    'Systematic methodology',
    'Knowledge-based operations',
    'Documented procedures',
    'Evidence-based decision making'
  ],
  communication_patterns: [
    'Technical documentation',
    'Systematic analysis',
    'Framework application',
    'Knowledge sharing within group'
  ],
  power_dynamics: 'Power through expertise and systematic knowledge. Authority derived from competence.',
  knowledge_relation: 'Knowledge as primary tool and objective. Systematic accumulation and application.',
  desire_structure: 'Desires mastery through knowledge, recognition of expertise, systematic understanding.',
  typical_threat_actors: ['APT29', 'APT28', 'Equation Group', 'Advanced research-focused threat actors'],
  is_shared: true,
  customer_namespace: 'shared:discourse-analysis'
});

CREATE (discourse_hysteric:DiscourseDimension {
  id: 'discourse-hysteric-001',
  position: 'HYSTERIC',
  description: 'Discourse of the Hysteric: Questioning, challenging authority, seeking recognition. Operates through resistance.',
  characteristic_behaviors: [
    'Challenges established systems',
    'Questions authority',
    'Seeks attention/recognition',
    'Unpredictable patterns'
  ],
  communication_patterns: [
    'Public statements challenging authority',
    'Manifestos',
    'Attention-seeking behavior',
    'Questions "why" more than "how"'
  ],
  power_dynamics: 'Resists power structures, challenges authority, creates disorder to be recognized.',
  knowledge_relation: 'Questions established knowledge, seeks new understanding, unsatisfied with current answers.',
  desire_structure: 'Desires recognition, validation, to be heard. Wants authority to acknowledge them.',
  typical_threat_actors: ['Anonymous', 'LulzSec', 'Ideologically-driven hacktivists', 'Attention-seeking lone actors'],
  is_shared: true,
  customer_namespace: 'shared:discourse-analysis'
});

CREATE (discourse_analyst:DiscourseDimension {
  id: 'discourse-analyst-001',
  position: 'ANALYST',
  description: 'Discourse of the Analyst: Interpretation, hidden meanings, unconscious motivations. Operates through revealing what is hidden.',
  characteristic_behaviors: [
    'Interpreting intelligence',
    'Seeking hidden patterns',
    'Revealing vulnerabilities',
    'Exploiting unconscious weaknesses'
  ],
  communication_patterns: [
    'Focuses on what is unsaid',
    'Interprets defensive measures',
    'Reads between the lines',
    'Exploits psychological weaknesses'
  ],
  power_dynamics: 'Power through interpretation and revealing hidden truths. Makes the unconscious conscious.',
  knowledge_relation: 'Knowledge of hidden structures, unconscious patterns, psychological vulnerabilities.',
  desire_structure: 'Desires to reveal truth, expose hidden structures, understand psychological dimensions.',
  typical_threat_actors: ['Social engineering specialists', 'Psychological warfare units', 'Advanced profiling teams'],
  is_shared: true,
  customer_namespace: 'shared:discourse-analysis'
});

// ═══════════════════════════════════════════════════════════════
// NEW RELATIONSHIPS - Psychometric Profiling
// ═══════════════════════════════════════════════════════════════

// ThreatActorProfile → PsychologicalPattern (profile exhibits psychological pattern)
CREATE (enhanced_profile)-[:EXHIBITS_PATTERN {
  confidence: 0.78,
  detection_date: datetime('2025-01-15T10:00:00Z'),
  evidence_sources: ['SolarWinds analysis', 'Operation Cloud Hopper'],
  analyst_confidence: 0.82
}]->(pattern_rationalization);

CREATE (enhanced_profile)-[:EXHIBITS_PATTERN {
  confidence: 0.65,
  detection_date: datetime('2024-11-20T10:00:00Z'),
  evidence_sources: ['Target sector analysis', 'Campaign continuity study'],
  analyst_confidence: 0.70
}]->(pattern_confirmation_bias);

CREATE (enhanced_profile)-[:EXHIBITS_PATTERN {
  confidence: 0.55,
  detection_date: datetime('2024-09-10T10:00:00Z'),
  evidence_sources: ['Campaign timeline analysis'],
  analyst_confidence: 0.60
}]->(pattern_planning_fallacy);

CREATE (enhanced_profile)-[:EXHIBITS_PATTERN {
  confidence: 0.82,
  detection_date: datetime('2025-03-01T10:00:00Z'),
  evidence_sources: ['Geopolitical event correlation', 'Targeting alignment analysis'],
  analyst_confidence: 0.85
}]->(pattern_geopolitical_competition);

// ThreatActorProfile → BiasIndicator (profile shows bias indicator)
CREATE (enhanced_profile)-[:SHOWS_BIAS {
  confidence: 0.70,
  impact_level: 'MODERATE',
  detection_method: 'TTP evolution rate analysis',
  false_positive_probability: 0.25
}]->(bias_anchoring);

CREATE (enhanced_profile)-[:SHOWS_BIAS {
  confidence: 0.60,
  impact_level: 'HIGH',
  detection_method: 'Operator variance clustering',
  false_positive_probability: 0.40
}]->(bias_attribution);

// ThreatActorProfile → DiscourseDimension (profile operates in discourse position)
CREATE (enhanced_profile)-[:OPERATES_IN_DISCOURSE {
  primary_position: true,
  confidence: 0.78,
  evidence: ['Systematic methodology', 'Knowledge-based operations', 'Technical documentation'],
  last_assessed: datetime('2025-10-29T10:00:00Z')
}]->(discourse_university);

CREATE (enhanced_profile)-[:OPERATES_IN_DISCOURSE {
  primary_position: false,
  confidence: 0.62,
  evidence: ['Intelligence interpretation', 'Pattern recognition', 'Psychological profiling of targets'],
  last_assessed: datetime('2025-10-29T10:00:00Z')
}]->(discourse_analyst);

// PsychologicalPattern → BiasIndicator (pattern influenced by bias)
CREATE (pattern_confirmation_bias)-[:INFLUENCED_BY_BIAS {
  influence_strength: 'HIGH',
  mechanism: 'Cognitive bias directly manifests in observable pattern'
}]->(bias_anchoring);

CREATE (pattern_planning_fallacy)-[:INFLUENCED_BY_BIAS {
  influence_strength: 'DIRECT',
  mechanism: 'Bias is the pattern itself'
}]->(bias_overconfidence);

// ═══════════════════════════════════════════════════════════════
// CONSTRAINTS AND INDEXES
// ═══════════════════════════════════════════════════════════════

// Unique constraints
CREATE CONSTRAINT unique_threat_actor_profile_id IF NOT EXISTS
FOR (p:ThreatActorProfile) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT unique_psychological_pattern_id IF NOT EXISTS
FOR (p:PsychologicalPattern) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT unique_bias_indicator_id IF NOT EXISTS
FOR (b:BiasIndicator) REQUIRE b.id IS UNIQUE;

CREATE CONSTRAINT unique_discourse_dimension_id IF NOT EXISTS
FOR (d:DiscourseDimension) REQUIRE d.id IS UNIQUE;

// Performance indexes
CREATE INDEX profile_lacanian_register IF NOT EXISTS
FOR (p:ThreatActorProfile) ON (p.lacanian_dominant_register);

CREATE INDEX profile_discourse_position IF NOT EXISTS
FOR (p:ThreatActorProfile) ON (p.discourse_dominant_position);

CREATE INDEX profile_confidence IF NOT EXISTS
FOR (p:ThreatActorProfile) ON (p.profile_confidence);

CREATE INDEX pattern_type IF NOT EXISTS
FOR (p:PsychologicalPattern) ON (p.pattern_type);

CREATE INDEX bias_type IF NOT EXISTS
FOR (b:BiasIndicator) ON (b.bias_type);

CREATE INDEX discourse_position IF NOT EXISTS
FOR (d:DiscourseDimension) ON (d.position);

// Composite indexes for common queries
CREATE INDEX profile_big5_conscientiousness IF NOT EXISTS
FOR (p:ThreatActorProfile) ON (p.big5_conscientiousness);

CREATE INDEX profile_big5_openness IF NOT EXISTS
FOR (p:ThreatActorProfile) ON (p.big5_openness);

CREATE INDEX pattern_severity IF NOT EXISTS
FOR (p:PsychologicalPattern) ON (p.severity_level);

// ═══════════════════════════════════════════════════════════════
// MIGRATION PATH FROM EXISTING SCHEMA
// ═══════════════════════════════════════════════════════════════

// Step 1: Extend existing ThreatActorProfile nodes with new properties
MATCH (p:ThreatActorProfile)
WHERE NOT EXISTS(p.lacanian_symbolic_score)
SET p.lacanian_symbolic_score = 0.5,
    p.lacanian_imaginary_score = 0.5,
    p.lacanian_real_score = 0.5,
    p.lacanian_dominant_register = 'BALANCED',
    p.big5_openness = 0.5,
    p.big5_conscientiousness = 0.5,
    p.big5_extraversion = 0.5,
    p.big5_agreeableness = 0.5,
    p.big5_neuroticism = 0.5,
    p.discourse_master_score = 0.25,
    p.discourse_university_score = 0.25,
    p.discourse_hysteric_score = 0.25,
    p.discourse_analyst_score = 0.25,
    p.discourse_dominant_position = 'MIXED',
    p.defense_mechanisms = [],
    p.transference_patterns = [],
    p.cognitive_biases = [],
    p.emotional_triggers = [],
    p.profile_confidence = 0.5,
    p.data_sources = ['migration_from_layer_4'],
    p.last_updated = datetime(),
    p.validation_status = 'UNVALIDATED',
    p.analyst_notes = 'Migrated from Layer 4 schema - requires expert review';

// Step 2: Create baseline PsychologicalPattern nodes (shown above)
// Already completed in this schema

// Step 3: Create baseline BiasIndicator nodes (shown above)
// Already completed in this schema

// Step 4: Create DiscourseDimension taxonomy (shown above)
// Already completed in this schema

// Step 5: Establish relationships based on existing psychological_profile text
// This requires manual analysis or NLP processing of existing profiles

// Example automated relationship creation based on keywords
MATCH (p:ThreatActorProfile)
WHERE p.psychological_profile CONTAINS 'methodical'
   OR p.psychological_profile CONTAINS 'systematic'
   OR p.psychological_profile CONTAINS 'disciplined'
MATCH (d:DiscourseDimension {position: 'UNIVERSITY'})
MERGE (p)-[:OPERATES_IN_DISCOURSE {
  primary_position: true,
  confidence: 0.60,
  evidence: ['keyword_analysis'],
  last_assessed: datetime()
}]->(d);

// ═══════════════════════════════════════════════════════════════
// QUERY EXAMPLES - Enhanced Psychometric Analysis
// ═══════════════════════════════════════════════════════════════

// Example 1: Find threat actors with high conscientiousness and university discourse
MATCH (ta:ThreatActor)-[:HAS_PROFILE]->(p:ThreatActorProfile)
WHERE p.big5_conscientiousness >= 0.75
  AND p.discourse_dominant_position = 'UNIVERSITY'
  AND p.profile_confidence >= 0.70
RETURN ta.name AS threat_actor,
       p.big5_conscientiousness AS conscientiousness,
       p.lacanian_dominant_register AS lacanian_register,
       p.operational_tempo AS tempo,
       p.profile_confidence AS confidence
ORDER BY p.big5_conscientiousness DESC;

// Example 2: Identify threat actors with similar psychometric profiles
MATCH (p1:ThreatActorProfile)-[:OPERATES_IN_DISCOURSE]->(d:DiscourseDimension)
MATCH (p2:ThreatActorProfile)-[:OPERATES_IN_DISCOURSE]->(d)
WHERE p1.id <> p2.id
  AND abs(p1.big5_conscientiousness - p2.big5_conscientiousness) < 0.15
  AND abs(p1.big5_openness - p2.big5_openness) < 0.15
  AND p1.lacanian_dominant_register = p2.lacanian_dominant_register
RETURN p1.id AS profile1,
       p2.id AS profile2,
       d.position AS shared_discourse,
       abs(p1.big5_conscientiousness - p2.big5_conscientiousness) AS conscientiousness_diff,
       abs(p1.big5_openness - p2.big5_openness) AS openness_diff
ORDER BY conscientiousness_diff + openness_diff ASC
LIMIT 10;

// Example 3: Find psychological patterns most associated with specific threat actors
MATCH (ta:ThreatActor)-[:HAS_PROFILE]->(p:ThreatActorProfile)
      -[r:EXHIBITS_PATTERN]->(pattern:PsychologicalPattern)
WHERE ta.sophistication IN ['STRATEGIC', 'EXPERT']
  AND r.confidence >= 0.70
RETURN pattern.name AS pattern,
       pattern.pattern_type AS type,
       count(DISTINCT ta) AS threat_actor_count,
       avg(r.confidence) AS avg_confidence,
       collect(DISTINCT ta.name) AS threat_actors
ORDER BY threat_actor_count DESC, avg_confidence DESC;

// Example 4: Detect bias patterns across threat actor profiles
MATCH (p:ThreatActorProfile)-[r:SHOWS_BIAS]->(b:BiasIndicator)
WHERE r.confidence >= 0.60
RETURN b.name AS bias,
       b.bias_type AS type,
       count(DISTINCT p) AS profile_count,
       avg(r.confidence) AS avg_confidence,
       avg(b.false_positive_rate) AS avg_false_positive_rate
ORDER BY profile_count DESC;

// Example 5: Find Lacanian register patterns by sophistication level
MATCH (ta:ThreatActor)-[:HAS_PROFILE]->(p:ThreatActorProfile)
WHERE p.profile_confidence >= 0.70
RETURN ta.sophistication AS sophistication,
       p.lacanian_dominant_register AS dominant_register,
       count(*) AS count,
       avg(p.lacanian_symbolic_score) AS avg_symbolic,
       avg(p.lacanian_imaginary_score) AS avg_imaginary,
       avg(p.lacanian_real_score) AS avg_real
ORDER BY sophistication, count DESC;

// Example 6: Analyze discourse positions by primary motivation
MATCH (ta:ThreatActor)-[:HAS_PROFILE]->(p:ThreatActorProfile)
      -[:OPERATES_IN_DISCOURSE {primary_position: true}]->(d:DiscourseDimension)
WHERE p.profile_confidence >= 0.70
RETURN ta.primary_motivation AS motivation,
       d.position AS discourse_position,
       count(*) AS count,
       collect(DISTINCT ta.name)[0..5] AS example_actors
ORDER BY motivation, count DESC;

// Example 7: Find threat actors with high real register (chaotic/impulsive)
MATCH (ta:ThreatActor)-[:HAS_PROFILE]->(p:ThreatActorProfile)
WHERE p.lacanian_real_score >= 0.60
  AND p.profile_confidence >= 0.60
RETURN ta.name AS threat_actor,
       ta.sophistication AS sophistication,
       p.lacanian_real_score AS real_score,
       p.operational_tempo AS tempo,
       p.risk_tolerance AS risk_tolerance,
       p.emotional_triggers AS triggers
ORDER BY p.lacanian_real_score DESC;

// Example 8: Complete psychometric profile with all dimensions
MATCH (ta:ThreatActor {name: 'APT29'})-[:HAS_PROFILE]->(p:ThreatActorProfile)
OPTIONAL MATCH (p)-[r1:EXHIBITS_PATTERN]->(pattern:PsychologicalPattern)
OPTIONAL MATCH (p)-[r2:SHOWS_BIAS]->(bias:BiasIndicator)
OPTIONAL MATCH (p)-[r3:OPERATES_IN_DISCOURSE]->(discourse:DiscourseDimension)
RETURN ta.name AS threat_actor,
       // Lacanian dimensions
       {
         symbolic: p.lacanian_symbolic_score,
         imaginary: p.lacanian_imaginary_score,
         real: p.lacanian_real_score,
         dominant: p.lacanian_dominant_register
       } AS lacanian_profile,
       // Big 5 dimensions
       {
         openness: p.big5_openness,
         conscientiousness: p.big5_conscientiousness,
         extraversion: p.big5_extraversion,
         agreeableness: p.big5_agreeableness,
         neuroticism: p.big5_neuroticism
       } AS big5_profile,
       // Discourse positions
       collect(DISTINCT {
         position: discourse.position,
         confidence: r3.confidence,
         is_primary: r3.primary_position
       }) AS discourse_positions,
       // Psychological patterns
       collect(DISTINCT {
         pattern: pattern.name,
         type: pattern.pattern_type,
         confidence: r1.confidence
       }) AS patterns,
       // Biases
       collect(DISTINCT {
         bias: bias.name,
         type: bias.bias_type,
         confidence: r2.confidence
       }) AS biases,
       // Meta information
       p.profile_confidence AS overall_confidence,
       p.validation_status AS validation_status;

// Example 9: Find defense mechanism patterns by sophistication
MATCH (ta:ThreatActor)-[:HAS_PROFILE]->(p:ThreatActorProfile)
WHERE size(p.defense_mechanisms) > 0
  AND p.profile_confidence >= 0.60
UNWIND p.defense_mechanisms AS mechanism
RETURN ta.sophistication AS sophistication,
       mechanism AS defense_mechanism,
       count(*) AS frequency,
       collect(DISTINCT ta.name)[0..3] AS example_actors
ORDER BY sophistication, frequency DESC;

// Example 10: Multi-hop query: Software → CVE → ThreatActor → Psychometric Profile
MATCH path = (s:Software {customer_namespace: 'customer:EnterpriseCorp'})
  -[:HAS_VULNERABILITY]->(cve:CVE)
  -[:HAS_EXPLOIT]->(e:Exploit)
  -[:USED_BY_THREAT_ACTOR]->(ta:ThreatActor)
  -[:HAS_PROFILE]->(p:ThreatActorProfile)
WHERE cve.cvssV3BaseScore >= 9.0
  AND p.profile_confidence >= 0.70
OPTIONAL MATCH (p)-[:EXHIBITS_PATTERN]->(pattern:PsychologicalPattern)
WHERE pattern.severity_level IN ['HIGH', 'CRITICAL']
RETURN s.name AS vulnerable_software,
       cve.cveId AS critical_vulnerability,
       ta.name AS threat_actor,
       ta.sophistication AS sophistication,
       {
         lacanian: p.lacanian_dominant_register,
         discourse: p.discourse_dominant_position,
         conscientiousness: p.big5_conscientiousness,
         risk_tolerance: p.risk_tolerance
       } AS psychometric_summary,
       collect(DISTINCT pattern.name) AS critical_patterns,
       length(path) AS attack_chain_hops;

// ═══════════════════════════════════════════════════════════════
// VALIDATION AND QUALITY METRICS
// ═══════════════════════════════════════════════════════════════

// Profile confidence distribution
MATCH (p:ThreatActorProfile)
RETURN
  CASE
    WHEN p.profile_confidence >= 0.8 THEN 'HIGH (0.8-1.0)'
    WHEN p.profile_confidence >= 0.6 THEN 'MEDIUM (0.6-0.8)'
    ELSE 'LOW (< 0.6)'
  END AS confidence_level,
  count(*) AS profile_count,
  avg(p.profile_confidence) AS avg_confidence
ORDER BY avg_confidence DESC;

// Lacanian register distribution
MATCH (p:ThreatActorProfile)
WHERE p.profile_confidence >= 0.60
RETURN p.lacanian_dominant_register AS dominant_register,
       count(*) AS count,
       avg(p.lacanian_symbolic_score) AS avg_symbolic,
       avg(p.lacanian_imaginary_score) AS avg_imaginary,
       avg(p.lacanian_real_score) AS avg_real
ORDER BY count DESC;

// Discourse position distribution
MATCH (p:ThreatActorProfile)
WHERE p.profile_confidence >= 0.60
RETURN p.discourse_dominant_position AS dominant_position,
       count(*) AS count,
       avg(p.discourse_master_score) AS avg_master,
       avg(p.discourse_university_score) AS avg_university,
       avg(p.discourse_hysteric_score) AS avg_hysteric,
       avg(p.discourse_analyst_score) AS avg_analyst
ORDER BY count DESC;

// Big 5 trait correlations with sophistication
MATCH (ta:ThreatActor)-[:HAS_PROFILE]->(p:ThreatActorProfile)
WHERE p.profile_confidence >= 0.70
RETURN ta.sophistication AS sophistication,
       avg(p.big5_openness) AS avg_openness,
       avg(p.big5_conscientiousness) AS avg_conscientiousness,
       avg(p.big5_extraversion) AS avg_extraversion,
       avg(p.big5_agreeableness) AS avg_agreeableness,
       avg(p.big5_neuroticism) AS avg_neuroticism,
       count(*) AS sample_size
ORDER BY
  CASE ta.sophistication
    WHEN 'STRATEGIC' THEN 5
    WHEN 'INNOVATOR' THEN 4
    WHEN 'EXPERT' THEN 3
    WHEN 'PRACTITIONER' THEN 2
    ELSE 1
  END DESC;

// Most common psychological patterns
MATCH (p:ThreatActorProfile)-[r:EXHIBITS_PATTERN]->(pattern:PsychologicalPattern)
WHERE r.confidence >= 0.60
RETURN pattern.name AS pattern,
       pattern.pattern_type AS type,
       pattern.lacanian_register AS register,
       count(*) AS occurrence_count,
       avg(r.confidence) AS avg_confidence
ORDER BY occurrence_count DESC
LIMIT 20;

// Bias indicator prevalence
MATCH (p:ThreatActorProfile)-[r:SHOWS_BIAS]->(b:BiasIndicator)
WHERE r.confidence >= 0.60
RETURN b.name AS bias,
       b.bias_type AS type,
       count(*) AS profile_count,
       avg(r.confidence) AS avg_confidence,
       avg(b.false_positive_rate) AS avg_false_positive
ORDER BY profile_count DESC;

// ═══════════════════════════════════════════════════════════════
// END OF ENHANCED PSYCHOMETRIC SCHEMA
// ═══════════════════════════════════════════════════════════════
