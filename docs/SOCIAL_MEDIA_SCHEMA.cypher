// ═══════════════════════════════════════════════════════════════════════════════
// SOCIAL MEDIA INGESTION & BIAS DETECTION SCHEMA
// Neo4j Cypher Schema for Social Media Intelligence Analysis
// ═══════════════════════════════════════════════════════════════════════════════
// Created: 2025-10-29
// Purpose: Graph schema for social media content ingestion, bias detection,
//          narrative tracking, influence networks, and propaganda analysis
// Integration: ThreatActor psychometric profiling, sentiment analysis
// ═══════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════
// 1. NODE DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 1.1 SocialMediaPost - Core Content Node
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT post_id_unique IF NOT EXISTS
FOR (p:SocialMediaPost) REQUIRE p.post_id IS UNIQUE;

CREATE INDEX post_timestamp IF NOT EXISTS
FOR (p:SocialMediaPost) ON (p.timestamp);

CREATE INDEX post_platform IF NOT EXISTS
FOR (p:SocialMediaPost) ON (p.platform);

CREATE FULLTEXT INDEX post_content_search IF NOT EXISTS
FOR (p:SocialMediaPost) ON EACH [p.content, p.translated_content];

// Sample SocialMediaPost node structure
/*
(:SocialMediaPost {
  post_id: "twitter_1234567890",
  platform: "Twitter/X",
  content: "Original post content...",
  translated_content: "English translation if needed",
  language: "en",
  timestamp: datetime("2025-10-29T10:30:00Z"),
  engagement_score: 1250.5,
  reach: 15000,
  likes: 450,
  shares: 85,
  comments: 32,
  verified_account: false,
  account_created: datetime("2018-03-15T00:00:00Z"),
  follower_count: 5420,
  following_count: 892,
  post_type: "original|retweet|quote|reply",
  media_urls: ["https://example.com/image1.jpg"],
  hashtags: ["#election2024", "#democracy"],
  mentions: ["@username1", "@username2"],
  geolocation: point({latitude: 38.8977, longitude: -77.0365}),
  url: "https://twitter.com/user/status/1234567890",
  raw_metadata: '{"additional": "fields"}',
  ingestion_timestamp: datetime(),
  processing_status: "processed|pending|failed"
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.2 BiasIndicator - Detected Bias Patterns
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT bias_id_unique IF NOT EXISTS
FOR (b:BiasIndicator) REQUIRE b.bias_id IS UNIQUE;

CREATE INDEX bias_type IF NOT EXISTS
FOR (b:BiasIndicator) ON (b.bias_type);

CREATE INDEX bias_severity IF NOT EXISTS
FOR (b:BiasIndicator) ON (b.severity);

// Sample BiasIndicator node structure
/*
(:BiasIndicator {
  bias_id: "bias_uuid_123",
  bias_type: "confirmation|selection|framing|anchoring|availability|bandwagon",
  category: "cognitive|emotional|social|political",
  severity: 0.75, // 0.0 = minimal, 1.0 = extreme
  confidence: 0.82,
  detected_at: datetime(),
  description: "Uses selective facts to support predetermined conclusion",
  evidence_snippets: ["snippet1", "snippet2"],
  detection_method: "nlp_pattern|ml_model|rule_based",
  model_version: "bias_detector_v2.3",
  related_fallacies: ["cherry_picking", "hasty_generalization"],
  mitigation_suggestion: "Seek opposing viewpoints and complete data"
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.3 NarrativeThread - Tracked Information Campaigns
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT narrative_id_unique IF NOT EXISTS
FOR (n:NarrativeThread) REQUIRE n.narrative_id IS UNIQUE;

CREATE INDEX narrative_status IF NOT EXISTS
FOR (n:NarrativeThread) ON (n.status);

CREATE INDEX narrative_start_date IF NOT EXISTS
FOR (n:NarrativeThread) ON (n.start_date);

// Sample NarrativeThread node structure
/*
(:NarrativeThread {
  narrative_id: "narrative_election_fraud_2025",
  title: "Election Fraud Claims Campaign",
  description: "Coordinated messaging about alleged election irregularities",
  start_date: datetime("2025-09-15T00:00:00Z"),
  last_activity: datetime(),
  status: "active|declining|dormant|resolved",
  coordination_probability: 0.68,
  post_count: 3847,
  unique_accounts: 892,
  peak_velocity: 450, // posts per hour at peak
  geographic_spread: ["US-Northeast", "US-Southwest"],
  key_hashtags: ["#StopTheSteal", "#ElectionIntegrity"],
  key_phrases: ["widespread fraud", "stolen election"],
  sentiment_trend: [0.2, 0.3, 0.5, 0.7], // negativity over time
  bot_participation_estimate: 0.35,
  state_actor_indicators: ["timing_patterns", "language_consistency"],
  related_events: ["debate_10_25", "rally_10_27"],
  predicted_lifecycle: "7-14 days",
  mitigation_actions: ["fact_check_deployed", "platform_warning_added"]
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.4 SentimentAnalysis - Emotional Content Analysis
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT sentiment_id_unique IF NOT EXISTS
FOR (s:SentimentAnalysis) REQUIRE s.sentiment_id IS UNIQUE;

// Sample SentimentAnalysis node structure
/*
(:SentimentAnalysis {
  sentiment_id: "sentiment_uuid_456",
  overall_polarity: -0.45, // -1.0 = very negative, 1.0 = very positive
  polarity_confidence: 0.88,
  emotions: {
    anger: 0.65,
    fear: 0.42,
    joy: 0.05,
    sadness: 0.32,
    disgust: 0.51,
    surprise: 0.18,
    trust: 0.15
  },
  toxicity_score: 0.58,
  toxicity_categories: ["insult", "identity_attack"],
  subjectivity: 0.75, // 0.0 = objective, 1.0 = subjective
  intensity: 0.68,
  analysis_timestamp: datetime(),
  model_version: "sentiment_v3.1",
  language_detected: "en",
  sarcasm_detected: false,
  emotional_manipulation_indicators: ["fear_mongering", "outrage_amplification"],
  propaganda_techniques: ["loaded_language", "appeal_to_fear"]
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.5 SourceCredibility - Account Reputation & Trust
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT source_id_unique IF NOT EXISTS
FOR (s:SourceCredibility) REQUIRE s.source_id IS UNIQUE;

CREATE INDEX source_trust_score IF NOT EXISTS
FOR (s:SourceCredibility) ON (s.trust_score);

// Sample SourceCredibility node structure
/*
(:SourceCredibility {
  source_id: "source_twitter_user123",
  platform: "Twitter/X",
  account_handle: "@username",
  account_name: "Display Name",
  trust_score: 0.45, // 0.0 = untrusted, 1.0 = highly trusted
  credibility_factors: {
    verification_status: false,
    account_age_days: 2547,
    follower_authenticity: 0.62,
    content_consistency: 0.55,
    fact_check_history: 0.35,
    engagement_authenticity: 0.58,
    network_quality: 0.48
  },
  bot_probability: 0.32,
  bot_indicators: ["posting_pattern", "content_similarity"],
  coordination_flags: ["time_sync_posting", "narrative_alignment"],
  misinformation_history_count: 7,
  fact_check_ratio: 0.15, // fact-checked posts / total posts
  account_type: "individual|organization|media|bot|suspected_bot|state_affiliated",
  state_affiliation_probability: 0.08,
  state_affiliation_country: null,
  influence_score: 0.38,
  audience_demographics: {
    primary_regions: ["US", "UK"],
    age_distribution: "25-45_dominant",
    political_leaning: "right_leaning"
  },
  last_assessment: datetime(),
  risk_level: "low|medium|high|critical"
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.6 PropagationPattern - Viral Spread Analysis
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT propagation_id_unique IF NOT EXISTS
FOR (p:PropagationPattern) REQUIRE p.propagation_id IS UNIQUE;

// Sample PropagationPattern node structure
/*
(:PropagationPattern {
  propagation_id: "propagation_uuid_789",
  pattern_type: "viral|coordinated|organic|amplified|astroturfing",
  spread_velocity: 125.5, // posts per hour
  acceleration: 2.3, // rate of velocity change
  reach_expansion_rate: 1.8,
  network_depth: 6, // degrees of separation
  coordination_score: 0.72,
  coordination_indicators: [
    "synchronized_posting",
    "identical_wording",
    "rapid_sequential_shares"
  ],
  temporal_pattern: "burst|sustained|periodic|irregular",
  geographic_distribution: {
    primary_clusters: ["US-East", "EU-West"],
    spread_direction: "east_to_west",
    anomalous_regions: ["unexpected_asia_spike"]
  },
  amplification_methods: ["bot_networks", "coordinated_hashtags"],
  network_topology: "star|cascade|broadcast|viral",
  key_amplifiers: ["hub_account_1", "hub_account_2"],
  bottleneck_nodes: ["bridge_account_1"],
  predicted_reach_24h: 50000,
  predicted_peak_time: datetime("2025-10-30T14:00:00Z"),
  analysis_timestamp: datetime()
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.7 InfluenceNetwork - Account Relationship Mapping
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT influence_id_unique IF NOT EXISTS
FOR (i:InfluenceNetwork) REQUIRE i.network_id IS UNIQUE;

// Sample InfluenceNetwork node structure
/*
(:InfluenceNetwork {
  network_id: "network_election_influencers",
  network_type: "influence|coordination|amplification|disinformation",
  description: "Coordinated network amplifying election narratives",
  member_count: 245,
  core_members: 18,
  peripheral_members: 227,
  cohesion_score: 0.68,
  centralization: 0.75,
  average_degree: 12.3,
  clustering_coefficient: 0.58,
  network_density: 0.34,
  identified_date: datetime("2025-10-15T00:00:00Z"),
  activity_pattern: "coordinated_bursts",
  coordination_evidence: [
    "synchronized_posting_times",
    "shared_content_patterns",
    "mutual_amplification"
  ],
  influence_reach: 2500000,
  state_actor_probability: 0.42,
  suspected_origin: "unknown|domestic|foreign",
  primary_objectives: ["narrative_shaping", "polarization"],
  mitigation_status: "monitored|flagged|action_taken",
  related_campaigns: ["narrative_election_fraud_2025"]
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.8 PropagandaTechnique - Specific Manipulation Methods
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT propaganda_id_unique IF NOT EXISTS
FOR (p:PropagandaTechnique) REQUIRE p.technique_id IS UNIQUE;

CREATE INDEX propaganda_category IF NOT EXISTS
FOR (p:PropagandaTechnique) ON (p.category);

// Sample PropagandaTechnique node structure
/*
(:PropagandaTechnique {
  technique_id: "technique_uuid_101",
  technique_name: "Appeal to Fear",
  category: "emotional|logical|credibility|propaganda",
  fine_propaganda_category: "appeal_to_fear|loaded_language|name_calling|repetition|flag_waving|causal_oversimplification|appeal_to_authority|slogans|thought_terminating_cliches|whataboutism|straw_man|red_herring|bandwagon",
  description: "Uses fear to manipulate audience reaction",
  detection_confidence: 0.85,
  evidence_text: ["We must act now or face catastrophe", "They will destroy everything"],
  linguistic_markers: ["catastrophe", "destroy", "threat", "danger"],
  psychological_target: "amygdala|emotion|logic|identity",
  effectiveness_estimate: 0.72,
  counter_narrative_available: true,
  detection_method: "fine_grained_propaganda_model_v2",
  detected_at: datetime()
})
*/

// ───────────────────────────────────────────────────────────────────────────────
// 1.9 ThreatActor (Reference from OSINT Schema)
// ───────────────────────────────────────────────────────────────────────────────
// This node type is defined in the OSINT schema but referenced here for integration

// ═══════════════════════════════════════════════════════════════════════════════
// 2. RELATIONSHIP DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 2.1 Post Analysis Relationships
// ───────────────────────────────────────────────────────────────────────────────

// SocialMediaPost has detected BiasIndicator
// CREATE (post:SocialMediaPost)-[:HAS_BIAS {
//   detection_confidence: 0.82,
//   detection_timestamp: datetime(),
//   human_verified: false,
//   severity_impact: 0.75
// }]->(bias:BiasIndicator)

CREATE INDEX rel_has_bias_confidence IF NOT EXISTS
FOR ()-[r:HAS_BIAS]-() ON (r.detection_confidence);

// SocialMediaPost analyzed with SentimentAnalysis
// CREATE (post:SocialMediaPost)-[:HAS_SENTIMENT {
//   analysis_timestamp: datetime(),
//   model_confidence: 0.88
// }]->(sentiment:SentimentAnalysis)

// SocialMediaPost exhibits PropagandaTechnique
// CREATE (post:SocialMediaPost)-[:USES_TECHNIQUE {
//   confidence: 0.85,
//   prominence: 0.72, // how prominent in content
//   detected_at: datetime()
// }]->(technique:PropagandaTechnique)

// ───────────────────────────────────────────────────────────────────────────────
// 2.2 Narrative & Thread Relationships
// ───────────────────────────────────────────────────────────────────────────────

// SocialMediaPost belongs to NarrativeThread
// CREATE (post:SocialMediaPost)-[:BELONGS_TO_NARRATIVE {
//   relevance_score: 0.85,
//   narrative_role: "originator|amplifier|variant|counter",
//   temporal_position: "early|peak|declining",
//   added_at: datetime()
// }]->(narrative:NarrativeThread)

CREATE INDEX rel_narrative_relevance IF NOT EXISTS
FOR ()-[r:BELONGS_TO_NARRATIVE]-() ON (r.relevance_score);

// NarrativeThread evolves from another NarrativeThread
// CREATE (narrative1:NarrativeThread)-[:EVOLVES_INTO {
//   transition_date: datetime(),
//   overlap_period_days: 3,
//   shared_elements: ["hashtags", "key_phrases"]
// }]->(narrative2:NarrativeThread)

// NarrativeThread contradicts another NarrativeThread
// CREATE (narrative1:NarrativeThread)-[:CONTRADICTS {
//   conflict_strength: 0.9,
//   identified_at: datetime(),
//   conflict_type: "factual|framing|source"
// }]->(narrative2:NarrativeThread)

// ───────────────────────────────────────────────────────────────────────────────
// 2.3 Source & Credibility Relationships
// ───────────────────────────────────────────────────────────────────────────────

// SocialMediaPost authored by SourceCredibility
// CREATE (source:SourceCredibility)-[:AUTHORED {
//   post_timestamp: datetime(),
//   account_status_at_time: "active|suspended|flagged",
//   engagement_metrics: {likes: 450, shares: 85}
// }]->(post:SocialMediaPost)

CREATE INDEX rel_authored_timestamp IF NOT EXISTS
FOR ()-[r:AUTHORED]-() ON (r.post_timestamp);

// SourceCredibility part of InfluenceNetwork
// CREATE (source:SourceCredibility)-[:MEMBER_OF_NETWORK {
//   role: "core|peripheral|amplifier|bridge",
//   join_date: datetime(),
//   activity_level: 0.75,
//   influence_rank: 12
// }]->(network:InfluenceNetwork)

// SourceCredibility affiliated with ThreatActor
// CREATE (source:SourceCredibility)-[:AFFILIATED_WITH {
//   confidence: 0.68,
//   affiliation_type: "direct|indirect|suspected",
//   evidence: ["posting_patterns", "content_alignment"],
//   identified_at: datetime()
// }]->(actor:ThreatActor)

// ───────────────────────────────────────────────────────────────────────────────
// 2.4 Propagation & Influence Relationships
// ───────────────────────────────────────────────────────────────────────────────

// SocialMediaPost has PropagationPattern
// CREATE (post:SocialMediaPost)-[:HAS_PROPAGATION {
//   analysis_timestamp: datetime(),
//   propagation_phase: "initiation|growth|peak|decline"
// }]->(pattern:PropagationPattern)

// SocialMediaPost reposted/shared by another SocialMediaPost
// CREATE (original:SocialMediaPost)-[:SHARED_BY {
//   share_type: "retweet|quote|share|cross_post",
//   share_timestamp: datetime(),
//   shares_count: 1,
//   modification_type: "exact|commentary|modified",
//   time_delay_seconds: 3600
// }]->(share:SocialMediaPost)

CREATE INDEX rel_shared_timestamp IF NOT EXISTS
FOR ()-[r:SHARED_BY]-() ON (r.share_timestamp);

// SocialMediaPost replies to another SocialMediaPost
// CREATE (reply:SocialMediaPost)-[:REPLIES_TO {
//   reply_timestamp: datetime(),
//   reply_sentiment: -0.5,
//   reply_type: "agreement|disagreement|question|attack"
// }]->(original:SocialMediaPost)

// SourceCredibility amplifies another SourceCredibility
// CREATE (amplifier:SourceCredibility)-[:AMPLIFIES {
//   amplification_frequency: 0.75, // ratio of shared content
//   relationship_strength: 0.68,
//   start_date: datetime(),
//   mutual_amplification: true
// }]->(amplified:SourceCredibility)

// InfluenceNetwork coordinates with another InfluenceNetwork
// CREATE (network1:InfluenceNetwork)-[:COORDINATES_WITH {
//   coordination_strength: 0.72,
//   shared_narratives: ["narrative_id_1", "narrative_id_2"],
//   coordination_start: datetime(),
//   coordination_evidence: ["timing", "content_overlap"]
// }]->(network2:InfluenceNetwork)

// ───────────────────────────────────────────────────────────────────────────────
// 2.5 ThreatActor Integration Relationships
// ───────────────────────────────────────────────────────────────────────────────

// ThreatActor orchestrates NarrativeThread
// CREATE (actor:ThreatActor)-[:ORCHESTRATES {
//   confidence: 0.78,
//   orchestration_type: "direct|indirect|probable",
//   evidence: ["timing_analysis", "linguistic_fingerprint"],
//   start_date: datetime(),
//   active: true
// }]->(narrative:NarrativeThread)

// ThreatActor controls InfluenceNetwork
// CREATE (actor:ThreatActor)-[:CONTROLS {
//   control_level: 0.85, // 0.0 = influence, 1.0 = direct control
//   control_type: "direct|indirect|suspected",
//   evidence: ["account_analysis", "coordination_patterns"],
//   identified_at: datetime()
// }]->(network:InfluenceNetwork)

// ThreatActor exploits BiasIndicator
// CREATE (actor:ThreatActor)-[:EXPLOITS_BIAS {
//   exploitation_frequency: 0.68,
//   effectiveness: 0.75,
//   target_audience: "demographic_segment",
//   observed_campaigns: ["campaign_1", "campaign_2"]
// }]->(bias:BiasIndicator)

// ═══════════════════════════════════════════════════════════════════════════════
// 3. SAMPLE DATA CREATION QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 3.1 Create Sample Social Media Posts
// ───────────────────────────────────────────────────────────────────────────────

// Example: Election fraud narrative post
CREATE (post1:SocialMediaPost {
  post_id: "twitter_sample_001",
  platform: "Twitter/X",
  content: "BREAKING: Thousands of 'irregularities' found in ballot counting! This election is being STOLEN! #StopTheSteal #ElectionFraud",
  language: "en",
  timestamp: datetime("2025-10-29T08:15:00Z"),
  engagement_score: 3450.0,
  reach: 45000,
  likes: 1200,
  shares: 450,
  comments: 180,
  verified_account: false,
  follower_count: 8900,
  post_type: "original",
  hashtags: ["#StopTheSteal", "#ElectionFraud"],
  ingestion_timestamp: datetime(),
  processing_status: "processed"
});

// Example: Counter-narrative post
CREATE (post2:SocialMediaPost {
  post_id: "twitter_sample_002",
  platform: "Twitter/X",
  content: "Election officials confirm no widespread irregularities. All standard procedures followed. Please rely on verified sources. #FactCheck #ElectionIntegrity",
  language: "en",
  timestamp: datetime("2025-10-29T09:30:00Z"),
  engagement_score: 1850.0,
  reach: 22000,
  likes: 680,
  shares: 120,
  comments: 95,
  verified_account: true,
  follower_count: 125000,
  post_type: "original",
  hashtags: ["#FactCheck", "#ElectionIntegrity"],
  ingestion_timestamp: datetime(),
  processing_status: "processed"
});

// ───────────────────────────────────────────────────────────────────────────────
// 3.2 Create Sample Bias Indicators
// ───────────────────────────────────────────────────────────────────────────────

CREATE (bias1:BiasIndicator {
  bias_id: "bias_confirmation_001",
  bias_type: "confirmation",
  category: "cognitive",
  severity: 0.82,
  confidence: 0.88,
  detected_at: datetime(),
  description: "Presents selective information supporting predetermined conclusion about election fraud",
  evidence_snippets: ["Thousands of 'irregularities'", "election is being STOLEN"],
  detection_method: "nlp_pattern",
  related_fallacies: ["cherry_picking", "hasty_generalization"]
});

CREATE (bias2:BiasIndicator {
  bias_id: "bias_framing_001",
  bias_type: "framing",
  category: "emotional",
  severity: 0.75,
  confidence: 0.85,
  detected_at: datetime(),
  description: "Uses emotionally charged framing to present information",
  evidence_snippets: ["BREAKING", "STOLEN"],
  detection_method: "ml_model"
});

// ───────────────────────────────────────────────────────────────────────────────
// 3.3 Create Sample Narrative Thread
// ───────────────────────────────────────────────────────────────────────────────

CREATE (narrative1:NarrativeThread {
  narrative_id: "narrative_election_fraud_sample",
  title: "Election Fraud Claims - 2025",
  description: "Coordinated campaign alleging widespread election irregularities",
  start_date: datetime("2025-10-25T00:00:00Z"),
  last_activity: datetime(),
  status: "active",
  coordination_probability: 0.75,
  post_count: 4200,
  unique_accounts: 950,
  peak_velocity: 520,
  key_hashtags: ["#StopTheSteal", "#ElectionFraud"],
  bot_participation_estimate: 0.42,
  state_actor_indicators: ["timing_patterns", "coordinated_hashtags"]
});

// ───────────────────────────────────────────────────────────────────────────────
// 3.4 Create Sample Sentiment Analysis
// ───────────────────────────────────────────────────────────────────────────────

CREATE (sentiment1:SentimentAnalysis {
  sentiment_id: "sentiment_sample_001",
  overall_polarity: -0.68,
  polarity_confidence: 0.91,
  emotions: {
    anger: 0.78,
    fear: 0.62,
    joy: 0.02,
    sadness: 0.18,
    disgust: 0.45,
    surprise: 0.35,
    trust: 0.08
  },
  toxicity_score: 0.64,
  toxicity_categories: ["inflammatory"],
  subjectivity: 0.85,
  intensity: 0.82,
  analysis_timestamp: datetime(),
  emotional_manipulation_indicators: ["fear_mongering", "outrage_amplification"],
  propaganda_techniques: ["loaded_language", "appeal_to_fear"]
});

// ───────────────────────────────────────────────────────────────────────────────
// 3.5 Create Sample Source Credibility
// ───────────────────────────────────────────────────────────────────────────────

CREATE (source1:SourceCredibility {
  source_id: "source_twitter_sample_001",
  platform: "Twitter/X",
  account_handle: "@concernedcitizen2025",
  trust_score: 0.28,
  credibility_factors: {
    verification_status: false,
    account_age_days: 45,
    follower_authenticity: 0.42,
    fact_check_history: 0.15
  },
  bot_probability: 0.58,
  bot_indicators: ["posting_pattern", "content_similarity"],
  coordination_flags: ["time_sync_posting"],
  misinformation_history_count: 12,
  account_type: "suspected_bot",
  influence_score: 0.52,
  risk_level: "high"
});

CREATE (source2:SourceCredibility {
  source_id: "source_twitter_sample_002",
  platform: "Twitter/X",
  account_handle: "@verifiedelectionnews",
  trust_score: 0.88,
  credibility_factors: {
    verification_status: true,
    account_age_days: 2800,
    follower_authenticity: 0.92,
    fact_check_history: 0.95
  },
  bot_probability: 0.05,
  account_type: "media",
  influence_score: 0.85,
  risk_level: "low"
});

// ───────────────────────────────────────────────────────────────────────────────
// 3.6 Create Sample Propaganda Technique
// ───────────────────────────────────────────────────────────────────────────────

CREATE (propaganda1:PropagandaTechnique {
  technique_id: "technique_appeal_fear_001",
  technique_name: "Appeal to Fear",
  category: "emotional",
  fine_propaganda_category: "appeal_to_fear",
  description: "Uses fear of election fraud to manipulate audience",
  detection_confidence: 0.88,
  evidence_text: ["election is being STOLEN", "irregularities"],
  linguistic_markers: ["STOLEN", "BREAKING"],
  psychological_target: "amygdala",
  effectiveness_estimate: 0.76,
  detected_at: datetime()
});

CREATE (propaganda2:PropagandaTechnique {
  technique_id: "technique_loaded_language_001",
  technique_name: "Loaded Language",
  category: "emotional",
  fine_propaganda_category: "loaded_language",
  description: "Uses emotionally charged words to influence opinion",
  detection_confidence: 0.92,
  evidence_text: ["BREAKING", "STOLEN", "irregularities"],
  linguistic_markers: ["BREAKING", "STOLEN"],
  detected_at: datetime()
});

// ───────────────────────────────────────────────────────────────────────────────
// 3.7 Create Sample Influence Network
// ───────────────────────────────────────────────────────────────────────────────

CREATE (network1:InfluenceNetwork {
  network_id: "network_election_fraud_amplifiers",
  network_type: "amplification",
  description: "Coordinated network amplifying election fraud narratives",
  member_count: 280,
  core_members: 22,
  cohesion_score: 0.72,
  coordination_evidence: ["synchronized_posting_times", "shared_hashtags"],
  state_actor_probability: 0.48,
  primary_objectives: ["narrative_shaping", "polarization"],
  mitigation_status: "monitored"
});

// ───────────────────────────────────────────────────────────────────────────────
// 3.8 Create Relationships Between Sample Nodes
// ───────────────────────────────────────────────────────────────────────────────

// Connect post to biases
MATCH (post:SocialMediaPost {post_id: "twitter_sample_001"}),
      (bias1:BiasIndicator {bias_id: "bias_confirmation_001"}),
      (bias2:BiasIndicator {bias_id: "bias_framing_001"})
CREATE (post)-[:HAS_BIAS {
  detection_confidence: 0.88,
  detection_timestamp: datetime(),
  severity_impact: 0.82
}]->(bias1),
(post)-[:HAS_BIAS {
  detection_confidence: 0.85,
  detection_timestamp: datetime(),
  severity_impact: 0.75
}]->(bias2);

// Connect post to sentiment
MATCH (post:SocialMediaPost {post_id: "twitter_sample_001"}),
      (sentiment:SentimentAnalysis {sentiment_id: "sentiment_sample_001"})
CREATE (post)-[:HAS_SENTIMENT {
  analysis_timestamp: datetime(),
  model_confidence: 0.91
}]->(sentiment);

// Connect post to propaganda techniques
MATCH (post:SocialMediaPost {post_id: "twitter_sample_001"}),
      (propaganda1:PropagandaTechnique {technique_id: "technique_appeal_fear_001"}),
      (propaganda2:PropagandaTechnique {technique_id: "technique_loaded_language_001"})
CREATE (post)-[:USES_TECHNIQUE {
  confidence: 0.88,
  prominence: 0.76,
  detected_at: datetime()
}]->(propaganda1),
(post)-[:USES_TECHNIQUE {
  confidence: 0.92,
  prominence: 0.82,
  detected_at: datetime()
}]->(propaganda2);

// Connect post to narrative
MATCH (post:SocialMediaPost {post_id: "twitter_sample_001"}),
      (narrative:NarrativeThread {narrative_id: "narrative_election_fraud_sample"})
CREATE (post)-[:BELONGS_TO_NARRATIVE {
  relevance_score: 0.95,
  narrative_role: "amplifier",
  temporal_position: "peak",
  added_at: datetime()
}]->(narrative);

// Connect source to post
MATCH (source:SourceCredibility {source_id: "source_twitter_sample_001"}),
      (post:SocialMediaPost {post_id: "twitter_sample_001"})
CREATE (source)-[:AUTHORED {
  post_timestamp: post.timestamp,
  account_status_at_time: "active"
}]->(post);

// Connect source to network
MATCH (source:SourceCredibility {source_id: "source_twitter_sample_001"}),
      (network:InfluenceNetwork {network_id: "network_election_fraud_amplifiers"})
CREATE (source)-[:MEMBER_OF_NETWORK {
  role: "amplifier",
  join_date: datetime("2025-10-26T00:00:00Z"),
  activity_level: 0.82,
  influence_rank: 15
}]->(network);

// ═══════════════════════════════════════════════════════════════════════════════
// 4. ANALYTICAL QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 4.1 Detect High-Risk Coordinated Campaigns
// ───────────────────────────────────────────────────────────────────────────────

// Find active narratives with high coordination and state actor indicators
// MATCH (narrative:NarrativeThread)
// WHERE narrative.status = 'active'
//   AND narrative.coordination_probability > 0.7
//   AND narrative.state_actor_indicators IS NOT NULL
//   AND size(narrative.state_actor_indicators) > 0
// RETURN narrative.narrative_id AS campaign_id,
//        narrative.title,
//        narrative.coordination_probability,
//        narrative.post_count,
//        narrative.unique_accounts,
//        narrative.state_actor_indicators,
//        narrative.bot_participation_estimate
// ORDER BY narrative.coordination_probability DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 4.2 Identify Influence Network Hubs
// ───────────────────────────────────────────────────────────────────────────────

// Find core members of influence networks with high amplification
// MATCH (source:SourceCredibility)-[member:MEMBER_OF_NETWORK]->(network:InfluenceNetwork)
// WHERE member.role = 'core' OR member.role = 'amplifier'
//   AND source.influence_score > 0.5
// OPTIONAL MATCH (source)-[:AMPLIFIES]->(amplified:SourceCredibility)
// WITH source, network, count(amplified) AS amplification_count
// WHERE amplification_count > 10
// RETURN source.account_handle,
//        source.trust_score,
//        source.bot_probability,
//        network.network_id,
//        amplification_count,
//        source.risk_level
// ORDER BY amplification_count DESC
// LIMIT 20;

// ───────────────────────────────────────────────────────────────────────────────
// 4.3 Track Propaganda Technique Prevalence
// ───────────────────────────────────────────────────────────────────────────────

// Find most common propaganda techniques in active narratives
// MATCH (post:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative:NarrativeThread)
// WHERE narrative.status = 'active'
// MATCH (post)-[uses:USES_TECHNIQUE]->(technique:PropagandaTechnique)
// RETURN technique.technique_name,
//        technique.fine_propaganda_category,
//        count(post) AS usage_count,
//        avg(uses.confidence) AS avg_confidence,
//        avg(technique.effectiveness_estimate) AS avg_effectiveness
// ORDER BY usage_count DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 4.4 Analyze Narrative Evolution Chains
// ───────────────────────────────────────────────────────────────────────────────

// Trace how narratives evolve over time
// MATCH path = (n1:NarrativeThread)-[:EVOLVES_INTO*1..3]->(n2:NarrativeThread)
// WHERE n1.start_date < datetime().subtractDays(30)
// RETURN n1.title AS origin_narrative,
//        n2.title AS evolved_narrative,
//        length(path) AS evolution_depth,
//        n1.start_date AS origin_date,
//        n2.start_date AS evolution_date,
//        n2.status AS current_status;

// ───────────────────────────────────────────────────────────────────────────────
// 4.5 Detect Coordinated Timing Patterns
// ───────────────────────────────────────────────────────────────────────────────

// Find posts with suspicious temporal clustering (within 5 minutes)
// MATCH (post1:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative:NarrativeThread)
// MATCH (post2:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative)
// WHERE post1.post_id <> post2.post_id
//   AND duration.between(post1.timestamp, post2.timestamp).seconds < 300
// WITH narrative,
//      collect(DISTINCT post1.post_id) AS synchronized_posts,
//      count(DISTINCT post1.post_id) AS sync_count
// WHERE sync_count > 10
// RETURN narrative.narrative_id,
//        narrative.title,
//        sync_count,
//        synchronized_posts[0..5] AS sample_posts
// ORDER BY sync_count DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 4.6 Source Credibility vs Narrative Participation
// ───────────────────────────────────────────────────────────────────────────────

// Analyze low-credibility sources driving high-risk narratives
// MATCH (source:SourceCredibility)-[:AUTHORED]->(post:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative:NarrativeThread)
// WHERE source.trust_score < 0.4
//   AND source.bot_probability > 0.5
//   AND narrative.coordination_probability > 0.6
// WITH source, narrative, count(post) AS post_count
// RETURN source.account_handle,
//        source.trust_score,
//        source.bot_probability,
//        source.risk_level,
//        narrative.title,
//        post_count
// ORDER BY post_count DESC
// LIMIT 50;

// ───────────────────────────────────────────────────────────────────────────────
// 4.7 Sentiment Trajectory Analysis
// ───────────────────────────────────────────────────────────────────────────────

// Track sentiment changes within a narrative over time
// MATCH (post:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative:NarrativeThread)
// MATCH (post)-[:HAS_SENTIMENT]->(sentiment:SentimentAnalysis)
// WHERE narrative.narrative_id = 'narrative_election_fraud_sample'
// RETURN date(post.timestamp) AS post_date,
//        avg(sentiment.overall_polarity) AS avg_polarity,
//        avg(sentiment.emotions.anger) AS avg_anger,
//        avg(sentiment.emotions.fear) AS avg_fear,
//        avg(sentiment.toxicity_score) AS avg_toxicity,
//        count(post) AS post_count
// ORDER BY post_date;

// ───────────────────────────────────────────────────────────────────────────────
// 4.8 Bias Exploitation Patterns by ThreatActor
// ───────────────────────────────────────────────────────────────────────────────

// Find which biases are most exploited by threat actors
// MATCH (actor:ThreatActor)-[exploits:EXPLOITS_BIAS]->(bias:BiasIndicator)
// MATCH (post:SocialMediaPost)-[:HAS_BIAS]->(bias)
// RETURN actor.name AS threat_actor,
//        bias.bias_type,
//        bias.category,
//        exploits.exploitation_frequency,
//        exploits.effectiveness,
//        count(post) AS post_count
// ORDER BY exploits.effectiveness DESC, post_count DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 4.9 Cross-Platform Coordination Detection
// ───────────────────────────────────────────────────────────────────────────────

// Detect similar content across different platforms (requires content similarity)
// MATCH (post1:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative:NarrativeThread)
// MATCH (post2:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative)
// WHERE post1.platform <> post2.platform
//   AND post1.post_id <> post2.post_id
//   AND abs(duration.between(post1.timestamp, post2.timestamp).seconds) < 3600
// WITH narrative,
//      collect(DISTINCT post1.platform) AS platforms,
//      count(DISTINCT post1.post_id) AS cross_platform_count
// WHERE size(platforms) > 1
// RETURN narrative.narrative_id,
//        narrative.title,
//        platforms,
//        cross_platform_count
// ORDER BY cross_platform_count DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 4.10 Viral Cascade Analysis
// ───────────────────────────────────────────────────────────────────────────────

// Trace how posts spread through sharing relationships
// MATCH path = (original:SocialMediaPost)-[:SHARED_BY*1..5]->(shares:SocialMediaPost)
// WHERE original.post_id = 'twitter_sample_001'
// RETURN original.post_id AS original_post,
//        original.engagement_score AS original_engagement,
//        length(path) AS cascade_depth,
//        count(shares) AS total_shares,
//        sum(shares.engagement_score) AS cascade_engagement
// ORDER BY cascade_depth DESC;

// ═══════════════════════════════════════════════════════════════════════════════
// 5. INTEGRATION WITH THREATACTOR PSYCHOMETRICS
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 5.1 Link Narratives to ThreatActor Psychological Profiles
// ───────────────────────────────────────────────────────────────────────────────

// Find narratives orchestrated by threat actors with specific psychological traits
// MATCH (actor:ThreatActor)-[orchestrates:ORCHESTRATES]->(narrative:NarrativeThread)
// OPTIONAL MATCH (actor)-[:HAS_PSYCHOLOGICAL_PROFILE]->(profile:PsychologicalProfile)
// WHERE profile.dark_triad_traits.machiavellianism > 0.7
//    OR profile.cognitive_patterns.deceptive_thinking > 0.7
// RETURN actor.name,
//        actor.category,
//        narrative.title,
//        orchestrates.confidence,
//        profile.dark_triad_traits.machiavellianism AS machiavellianism,
//        profile.cognitive_patterns.deceptive_thinking AS deception_level,
//        narrative.coordination_probability
// ORDER BY orchestrates.confidence DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 5.2 Match Propaganda Techniques to Actor Behavioral Patterns
// ───────────────────────────────────────────────────────────────────────────────

// Correlate propaganda techniques with threat actor behavioral signatures
// MATCH (actor:ThreatActor)-[:CONTROLS]->(network:InfluenceNetwork)
// MATCH (source:SourceCredibility)-[:MEMBER_OF_NETWORK]->(network)
// MATCH (source)-[:AUTHORED]->(post:SocialMediaPost)
// MATCH (post)-[uses:USES_TECHNIQUE]->(technique:PropagandaTechnique)
// OPTIONAL MATCH (actor)-[:HAS_BEHAVIORAL_PATTERN]->(behavior:BehavioralPattern)
// WHERE behavior.communication_style.persuasion_tactics IS NOT NULL
// RETURN actor.name,
//        technique.technique_name,
//        technique.category,
//        count(post) AS technique_usage,
//        avg(uses.confidence) AS avg_confidence,
//        behavior.communication_style.persuasion_tactics AS behavioral_tactics
// ORDER BY technique_usage DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 5.3 Cognitive Bias Exploitation vs Personality Traits
// ───────────────────────────────────────────────────────────────────────────────

// Map which cognitive biases actors exploit based on their personality profiles
// MATCH (actor:ThreatActor)-[exploits:EXPLOITS_BIAS]->(bias:BiasIndicator)
// OPTIONAL MATCH (actor)-[:HAS_PSYCHOLOGICAL_PROFILE]->(profile:PsychologicalProfile)
// WHERE profile.personality_traits.openness < 0.3
//    OR profile.cognitive_patterns.confirmation_bias > 0.7
// RETURN actor.name,
//        bias.bias_type,
//        bias.category,
//        exploits.exploitation_frequency,
//        exploits.effectiveness,
//        profile.personality_traits.openness AS openness,
//        profile.cognitive_patterns.confirmation_bias AS actor_confirmation_bias
// ORDER BY exploits.effectiveness DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 5.4 Sentiment Manipulation by Actor Motivation
// ───────────────────────────────────────────────────────────────────────────────

// Analyze sentiment patterns in content linked to actors with specific motivations
// MATCH (actor:ThreatActor)-[:ORCHESTRATES]->(narrative:NarrativeThread)
// MATCH (post:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative)
// MATCH (post)-[:HAS_SENTIMENT]->(sentiment:SentimentAnalysis)
// OPTIONAL MATCH (actor)-[:HAS_MOTIVATION]->(motivation:Motivation)
// WHERE motivation.primary_category IN ['political', 'ideological']
// RETURN actor.name,
//        motivation.primary_category AS motivation_type,
//        narrative.title,
//        avg(sentiment.overall_polarity) AS avg_polarity,
//        avg(sentiment.emotions.anger) AS avg_anger,
//        avg(sentiment.emotions.fear) AS avg_fear,
//        avg(sentiment.toxicity_score) AS avg_toxicity,
//        count(post) AS post_count
// ORDER BY avg_toxicity DESC;

// ═══════════════════════════════════════════════════════════════════════════════
// 6. MAINTENANCE & OPTIMIZATION QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 6.1 Archive Old Posts (Data Retention)
// ───────────────────────────────────────────────────────────────────────────────

// Archive posts older than 90 days (detach relationships, mark for archival)
// MATCH (post:SocialMediaPost)
// WHERE post.timestamp < datetime().subtractDays(90)
//   AND NOT (post:Archived)
// SET post:Archived, post.archived_at = datetime()
// RETURN count(post) AS archived_count;

// ───────────────────────────────────────────────────────────────────────────────
// 6.2 Update Narrative Status
// ───────────────────────────────────────────────────────────────────────────────

// Mark narratives as dormant if no activity in 14 days
// MATCH (narrative:NarrativeThread)
// WHERE narrative.status = 'active'
//   AND narrative.last_activity < datetime().subtractDays(14)
// SET narrative.status = 'dormant', narrative.dormant_date = datetime()
// RETURN count(narrative) AS narratives_marked_dormant;

// ───────────────────────────────────────────────────────────────────────────────
// 6.3 Recompute Source Credibility Scores
// ───────────────────────────────────────────────────────────────────────────────

// Recalculate trust scores based on recent activity (placeholder logic)
// MATCH (source:SourceCredibility)-[:AUTHORED]->(post:SocialMediaPost)
// WHERE post.timestamp > datetime().subtractDays(30)
// OPTIONAL MATCH (post)-[:HAS_BIAS]->(bias:BiasIndicator)
// WITH source,
//      count(post) AS recent_posts,
//      count(bias) AS bias_count,
//      avg(bias.severity) AS avg_bias_severity
// SET source.trust_score = 1.0 - (bias_count * 1.0 / recent_posts) * avg_bias_severity,
//     source.last_assessment = datetime()
// RETURN source.source_id, source.trust_score;

// ───────────────────────────────────────────────────────────────────────────────
// 6.4 Performance Optimization - Index Usage Check
// ───────────────────────────────────────────────────────────────────────────────

// Query to verify index usage (run with PROFILE or EXPLAIN)
// EXPLAIN
// MATCH (post:SocialMediaPost)
// WHERE post.timestamp > datetime().subtractDays(7)
//   AND post.platform = 'Twitter/X'
// RETURN post.post_id, post.engagement_score
// ORDER BY post.engagement_score DESC
// LIMIT 100;

// ═══════════════════════════════════════════════════════════════════════════════
// 7. ADVANCED ANALYTICAL PATTERNS
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 7.1 Community Detection in Influence Networks
// ───────────────────────────────────────────────────────────────────────────────

// Identify tightly connected subgraphs (requires Graph Data Science library)
// CALL gds.louvain.stream({
//   nodeProjection: 'SourceCredibility',
//   relationshipProjection: 'AMPLIFIES'
// })
// YIELD nodeId, communityId
// RETURN gds.util.asNode(nodeId).account_handle AS account,
//        communityId,
//        gds.util.asNode(nodeId).trust_score AS trust_score
// ORDER BY communityId, trust_score DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 7.2 PageRank for Influence Scoring
// ───────────────────────────────────────────────────────────────────────────────

// Calculate PageRank-based influence scores
// CALL gds.pageRank.stream({
//   nodeProjection: 'SourceCredibility',
//   relationshipProjection: 'AMPLIFIES'
// })
// YIELD nodeId, score
// RETURN gds.util.asNode(nodeId).account_handle AS account,
//        score AS influence_pagerank,
//        gds.util.asNode(nodeId).follower_count AS followers
// ORDER BY score DESC
// LIMIT 20;

// ───────────────────────────────────────────────────────────────────────────────
// 7.3 Shortest Path Between Threat Actor and Target Post
// ───────────────────────────────────────────────────────────────────────────────

// Find how threat actors influence specific posts through network paths
// MATCH path = shortestPath(
//   (actor:ThreatActor)-[*..7]-(post:SocialMediaPost {post_id: 'twitter_sample_001'})
// )
// RETURN actor.name,
//        [node in nodes(path) | labels(node)[0] + ':' + coalesce(node.name, node.post_id, node.narrative_id, node.network_id)] AS path_description,
//        length(path) AS path_length;

// ───────────────────────────────────────────────────────────────────────────────
// 7.4 Temporal Correlation Analysis
// ───────────────────────────────────────────────────────────────────────────────

// Find narratives that spike simultaneously (potential coordination)
// MATCH (n1:NarrativeThread), (n2:NarrativeThread)
// WHERE n1.narrative_id <> n2.narrative_id
//   AND n1.status = 'active' AND n2.status = 'active'
//   AND abs(duration.between(n1.start_date, n2.start_date).days) < 2
// OPTIONAL MATCH (n1)<-[:BELONGS_TO_NARRATIVE]-(post1:SocialMediaPost)
// OPTIONAL MATCH (n2)<-[:BELONGS_TO_NARRATIVE]-(post2:SocialMediaPost)
// WITH n1, n2,
//      collect(DISTINCT post1.hashtags) AS hashtags1,
//      collect(DISTINCT post2.hashtags) AS hashtags2
// WITH n1, n2,
//      [tag in hashtags1 WHERE tag in hashtags2] AS shared_hashtags
// WHERE size(shared_hashtags) > 0
// RETURN n1.title AS narrative1,
//        n2.title AS narrative2,
//        shared_hashtags,
//        size(shared_hashtags) AS shared_count
// ORDER BY shared_count DESC;

// ═══════════════════════════════════════════════════════════════════════════════
// 8. REAL-TIME MONITORING QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// 8.1 Recent High-Engagement Posts with High Bias
// ───────────────────────────────────────────────────────────────────────────────

// Find recent viral posts with significant bias indicators
// MATCH (post:SocialMediaPost)-[has_bias:HAS_BIAS]->(bias:BiasIndicator)
// WHERE post.timestamp > datetime().subtractHours(24)
//   AND post.engagement_score > 1000
//   AND bias.severity > 0.7
// RETURN post.post_id,
//        post.platform,
//        post.content[0..100] AS content_preview,
//        post.engagement_score,
//        collect(bias.bias_type) AS detected_biases,
//        max(bias.severity) AS max_bias_severity
// ORDER BY post.engagement_score DESC
// LIMIT 20;

// ───────────────────────────────────────────────────────────────────────────────
// 8.2 Emerging Narratives Detection
// ───────────────────────────────────────────────────────────────────────────────

// Detect new narrative threads in the last 48 hours
// MATCH (narrative:NarrativeThread)
// WHERE narrative.start_date > datetime().subtractDays(2)
//   AND narrative.post_count > 50
// OPTIONAL MATCH (post:SocialMediaPost)-[:BELONGS_TO_NARRATIVE]->(narrative)
// OPTIONAL MATCH (post)-[:HAS_SENTIMENT]->(sentiment:SentimentAnalysis)
// RETURN narrative.narrative_id,
//        narrative.title,
//        narrative.start_date,
//        narrative.post_count,
//        narrative.unique_accounts,
//        narrative.coordination_probability,
//        avg(sentiment.overall_polarity) AS avg_sentiment
// ORDER BY narrative.post_count DESC;

// ───────────────────────────────────────────────────────────────────────────────
// 8.3 Bot Network Activity Surge Detection
// ───────────────────────────────────────────────────────────────────────────────

// Find sudden increases in bot activity within networks
// MATCH (source:SourceCredibility)-[:MEMBER_OF_NETWORK]->(network:InfluenceNetwork)
// WHERE source.bot_probability > 0.6
// MATCH (source)-[:AUTHORED]->(post:SocialMediaPost)
// WHERE post.timestamp > datetime().subtractHours(6)
// WITH network, count(post) AS recent_bot_posts, collect(DISTINCT source.source_id) AS bot_sources
// WHERE recent_bot_posts > 20
// RETURN network.network_id,
//        network.network_type,
//        recent_bot_posts,
//        size(bot_sources) AS active_bots,
//        network.state_actor_probability
// ORDER BY recent_bot_posts DESC;

// ═══════════════════════════════════════════════════════════════════════════════
// END OF SCHEMA
// ═══════════════════════════════════════════════════════════════════════════════

// USAGE INSTRUCTIONS:
// 1. Execute constraint and index creation queries first
// 2. Use sample data creation queries to test schema
// 3. Adapt analytical queries to your specific use cases
// 4. Integrate with ThreatActor schema from OSINT_SCHEMA.cypher
// 5. Use Graph Data Science library for advanced community detection
// 6. Implement real-time ingestion pipelines to populate SocialMediaPost nodes
// 7. Schedule periodic maintenance queries (archival, score updates)
// 8. Monitor emerging narratives and high-risk coordination patterns
// 9. Correlate social media activity with threat actor psychometric profiles
// 10. Deploy fact-checking and mitigation workflows based on query results

// INTEGRATION POINTS:
// - ThreatActor nodes from OSINT schema
// - PsychologicalProfile, BehavioralPattern, Motivation nodes for deep analysis
// - External NLP/ML pipelines for bias detection, sentiment analysis
// - Real-time ingestion from Twitter API, Facebook Graph API, Reddit API
// - Visualization dashboards (Neo4j Bloom, custom D3.js graphs)
// - Alerting systems for high-risk narrative emergence
