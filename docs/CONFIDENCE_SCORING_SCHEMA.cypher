// ═══════════════════════════════════════════════════════════════════════════════
// CONFIDENCE SCORING SCHEMA - Multi-Source Citation Verification System
// ═══════════════════════════════════════════════════════════════════════════════
// File: CONFIDENCE_SCORING_SCHEMA.cypher
// Created: 2025-10-29
// Purpose: Define Neo4j schema for confidence scoring, source credibility tracking,
//          bias detection, and multi-source citation verification
// ═══════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 1: NODE DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// InformationSource - Represents a source of information (social media, news, etc)
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT source_id IF NOT EXISTS FOR (s:InformationSource) REQUIRE s.sourceId IS UNIQUE;
CREATE INDEX source_platform IF NOT EXISTS FOR (s:InformationSource) ON (s.platform);
CREATE INDEX source_type IF NOT EXISTS FOR (s:InformationSource) ON (s.sourceType);
CREATE INDEX source_credibility IF NOT EXISTS FOR (s:InformationSource) ON (s.credibilityScore);

// InformationSource Properties:
// - sourceId: STRING (unique identifier)
// - platform: STRING (twitter, linkedin, reddit, news_site, academic, etc)
// - sourceType: STRING (individual, organization, media_outlet, academic_institution)
// - name: STRING (display name)
// - handle: STRING (username/handle)
// - url: STRING (profile/source URL)
// - credibilityScore: FLOAT (0.0-1.0, current overall credibility)
// - baselineCredibility: FLOAT (0.0-1.0, starting credibility by source type)
// - verificationStatus: STRING (verified, unverified, flagged, banned)
// - followerCount: INTEGER (audience size)
// - accountAge: INTEGER (days since creation)
// - contentVolume: INTEGER (total posts/articles)
// - expertiseDomains: LIST<STRING> (areas of expertise)
// - biasIndicators: MAP (political, commercial, ideological scores)
// - reputationTrend: STRING (improving, stable, declining)
// - lastUpdated: DATETIME
// - createdAt: DATETIME

// ───────────────────────────────────────────────────────────────────────────────
// Claim - Information claim that needs verification
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT claim_id IF NOT EXISTS FOR (c:Claim) REQUIRE c.claimId IS UNIQUE;
CREATE INDEX claim_confidence IF NOT EXISTS FOR (c:Claim) ON (c.confidenceScore);
CREATE INDEX claim_status IF NOT EXISTS FOR (c:Claim) ON (c.verificationStatus);

// Claim Properties:
// - claimId: STRING (unique identifier)
// - content: STRING (the actual claim text)
// - claimType: STRING (factual, opinion, prediction, statistical)
// - domain: STRING (politics, health, finance, technology, etc)
// - confidenceScore: FLOAT (0.0-1.0, overall confidence in claim)
// - verificationStatus: STRING (verified, disputed, unverified, false)
// - firstSeenAt: DATETIME
// - lastUpdatedAt: DATETIME
// - citationCount: INTEGER (number of supporting citations)
// - sourceCount: INTEGER (number of unique sources)
// - consensusLevel: FLOAT (0.0-1.0, agreement across sources)

// ───────────────────────────────────────────────────────────────────────────────
// Citation - A reference to supporting evidence
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT citation_id IF NOT EXISTS FOR (c:Citation) REQUIRE c.citationId IS UNIQUE;
CREATE INDEX citation_credibility IF NOT EXISTS FOR (c:Citation) ON (c.credibilityScore);

// Citation Properties:
// - citationId: STRING (unique identifier)
// - url: STRING (link to evidence)
// - title: STRING (title of referenced content)
// - contentType: STRING (article, study, video, tweet, report)
// - publishDate: DATETIME
// - accessDate: DATETIME
// - credibilityScore: FLOAT (0.0-1.0, citation quality)
// - primaryEvidence: BOOLEAN (direct vs secondary source)
// - peerReviewed: BOOLEAN (for academic sources)
// - archived: BOOLEAN (archived for permanence)
// - archiveUrl: STRING (wayback machine, etc)

// ───────────────────────────────────────────────────────────────────────────────
// BiasIndicator - Detected bias patterns in sources or claims
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT bias_id IF NOT EXISTS FOR (b:BiasIndicator) REQUIRE b.biasId IS UNIQUE;
CREATE INDEX bias_type IF NOT EXISTS FOR (b:BiasIndicator) ON (b.biasType);

// BiasIndicator Properties:
// - biasId: STRING (unique identifier)
// - biasType: STRING (political_left, political_right, commercial, sensational, confirmation)
// - severity: FLOAT (0.0-1.0, how pronounced the bias)
// - confidence: FLOAT (0.0-1.0, confidence in bias detection)
// - detectionMethod: STRING (manual, nlp_analysis, pattern_matching, fact_check)
// - evidence: LIST<STRING> (supporting evidence for bias)
// - detectedAt: DATETIME

// ───────────────────────────────────────────────────────────────────────────────
// FactCheck - Third-party fact-checking result
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT factcheck_id IF NOT EXISTS FOR (f:FactCheck) REQUIRE f.factCheckId IS UNIQUE;

// FactCheck Properties:
// - factCheckId: STRING (unique identifier)
// - factChecker: STRING (snopes, politifact, factcheck_org, etc)
// - rating: STRING (true, mostly_true, mixed, mostly_false, false, unproven)
// - ratingScore: FLOAT (0.0-1.0, normalized rating)
// - url: STRING (fact check article URL)
// - publishedAt: DATETIME
// - summary: STRING (brief explanation)

// ───────────────────────────────────────────────────────────────────────────────
// SourceReputation - Historical reputation tracking
// ───────────────────────────────────────────────────────────────────────────────
CREATE CONSTRAINT reputation_id IF NOT EXISTS FOR (r:SourceReputation) REQUIRE r.reputationId IS UNIQUE;
CREATE INDEX reputation_timestamp IF NOT EXISTS FOR (r:SourceReputation) ON (r.timestamp);

// SourceReputation Properties:
// - reputationId: STRING (unique identifier)
// - timestamp: DATETIME
// - credibilityScore: FLOAT (0.0-1.0, score at this time)
// - accuracyRate: FLOAT (0.0-1.0, historical accuracy)
// - retractionCount: INTEGER (corrections issued)
// - verifiedClaimsCount: INTEGER (claims confirmed true)
// - disputedClaimsCount: INTEGER (claims proven false)
// - changeReason: STRING (why score changed)

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 2: RELATIONSHIP DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// MAKES_CLAIM - Source makes a claim
// ───────────────────────────────────────────────────────────────────────────────
// Properties:
// - claimedAt: DATETIME
// - originalPost: BOOLEAN (true if source originated the claim)
// - confidence: FLOAT (source's stated confidence)
// - context: STRING (additional context provided)

// ───────────────────────────────────────────────────────────────────────────────
// CITES - Claim cites evidence/citation
// ───────────────────────────────────────────────────────────────────────────────
CREATE INDEX cite_weight IF NOT EXISTS FOR ()-[r:CITES]-() ON (r.evidenceWeight);

// Properties:
// - citedAt: DATETIME
// - evidenceWeight: FLOAT (0.0-1.0, strength of this evidence)
// - relevanceScore: FLOAT (0.0-1.0, how relevant to claim)
// - directSupport: BOOLEAN (directly supports vs tangentially related)

// ───────────────────────────────────────────────────────────────────────────────
// CORROBORATES - Source corroborates another source's claim
// ───────────────────────────────────────────────────────────────────────────────
// Properties:
// - corroboratedAt: DATETIME
// - independentVerification: BOOLEAN (independently verified vs repeated)
// - agreementLevel: FLOAT (0.0-1.0, level of agreement)

// ───────────────────────────────────────────────────────────────────────────────
// CONTRADICTS - Source contradicts another claim
// ───────────────────────────────────────────────────────────────────────────────
// Properties:
// - contradictedAt: DATETIME
// - contradictionType: STRING (direct, partial, contextual)
// - evidence: STRING (supporting evidence for contradiction)

// ───────────────────────────────────────────────────────────────────────────────
// HAS_BIAS - Source or claim has bias indicator
// ───────────────────────────────────────────────────────────────────────────────
// Properties:
// - detectedAt: DATETIME
// - impactOnCredibility: FLOAT (-1.0 to 0.0, credibility penalty)

// ───────────────────────────────────────────────────────────────────────────────
// FACT_CHECKED - Claim has been fact-checked
// ───────────────────────────────────────────────────────────────────────────────
// Properties:
// - checkedAt: DATETIME
// - factCheckerCredibility: FLOAT (0.0-1.0, fact-checker's own credibility)

// ───────────────────────────────────────────────────────────────────────────────
// HAS_REPUTATION_HISTORY - Source has historical reputation record
// ───────────────────────────────────────────────────────────────────────────────
// Properties:
// - recordedAt: DATETIME

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 3: BASELINE CREDIBILITY INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════════

// Initialize baseline credibility scores based on source types
// These serve as starting points before reputation adjustments

// Academic institutions and peer-reviewed journals (highest baseline)
// Credibility: 0.90 (can increase to 0.95 or decrease based on performance)

// Established news organizations with editorial standards
// Credibility: 0.75 (varies by specific outlet reputation)

// Verified experts in their field
// Credibility: 0.70 (domain-specific, increases with track record)

// General verified accounts
// Credibility: 0.50 (neutral starting point)

// Unverified accounts with established history
// Credibility: 0.40 (requires building reputation)

// New/unknown accounts
// Credibility: 0.30 (lowest baseline, must prove reliability)

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 4: CONFIDENCE SCORE CALCULATION QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// Query 1: Calculate Initial Confidence Score for a Claim
// ───────────────────────────────────────────────────────────────────────────────
// Factors:
// 1. Source credibility (weighted by # of sources)
// 2. Citation quality and quantity
// 3. Cross-source consensus
// 4. Temporal decay (older sources less credible)
// 5. Fact-check results
// 6. Bias penalties

// USAGE: Calculate confidence for claim with ID 'claim_123'
MATCH (claim:Claim {claimId: 'claim_123'})

// Get all sources making this claim
OPTIONAL MATCH (source:InformationSource)-[makes:MAKES_CLAIM]->(claim)
WITH claim,
     collect(DISTINCT source) AS sources,
     collect(DISTINCT source.credibilityScore) AS sourceCredibilities,
     count(DISTINCT source) AS sourceCount

// Get all citations
OPTIONAL MATCH (claim)-[cites:CITES]->(citation:Citation)
WITH claim, sources, sourceCredibilities, sourceCount,
     collect(DISTINCT citation) AS citations,
     avg(citation.credibilityScore * cites.evidenceWeight) AS avgCitationScore,
     count(DISTINCT citation) AS citationCount

// Get fact-check results
OPTIONAL MATCH (claim)-[checked:FACT_CHECKED]->(fc:FactCheck)
WITH claim, sources, sourceCredibilities, sourceCount,
     citations, avgCitationScore, citationCount,
     avg(fc.ratingScore * checked.factCheckerCredibility) AS avgFactCheckScore,
     count(DISTINCT fc) AS factCheckCount

// Get bias indicators (penalties)
OPTIONAL MATCH (claim)-[hasBias:HAS_BIAS]->(bias:BiasIndicator)
WITH claim, sources, sourceCredibilities, sourceCount,
     citations, avgCitationScore, citationCount,
     avgFactCheckScore, factCheckCount,
     avg(hasBias.impactOnCredibility) AS avgBiasPenalty

// Calculate temporal decay for citations (exponential decay over 365 days)
WITH claim, sources, sourceCredibilities, sourceCount,
     citations, avgCitationScore, citationCount,
     avgFactCheckScore, factCheckCount, avgBiasPenalty,
     [c IN citations |
       CASE
         WHEN c.publishDate IS NOT NULL
         THEN exp(-duration.between(c.publishDate, datetime()).days / 365.0)
         ELSE 0.5
       END
     ] AS temporalDecays

WITH claim, sources, sourceCredibilities, sourceCount,
     avgCitationScore, citationCount,
     avgFactCheckScore, factCheckCount, avgBiasPenalty,
     CASE WHEN size(temporalDecays) > 0 THEN reduce(sum = 0.0, decay IN temporalDecays | sum + decay) / size(temporalDecays) ELSE 0.5 END AS avgTemporalFactor

// Calculate weighted confidence score
WITH claim,
     // Component 1: Source credibility (weight: 0.30)
     CASE
       WHEN sourceCount = 0 THEN 0.0
       ELSE (reduce(sum = 0.0, score IN sourceCredibilities | sum + score) / sourceCount) * 0.30
     END AS sourceComponent,

     // Component 2: Citation quality (weight: 0.25)
     COALESCE(avgCitationScore, 0.0) * 0.25 AS citationComponent,

     // Component 3: Citation quantity bonus (weight: 0.10, logarithmic)
     CASE
       WHEN citationCount = 0 THEN 0.0
       WHEN citationCount >= 10 THEN 0.10
       ELSE log10(citationCount + 1) * 0.10
     END AS citationCountComponent,

     // Component 4: Cross-source consensus (weight: 0.15)
     CASE
       WHEN sourceCount <= 1 THEN 0.0
       WHEN sourceCount >= 5 THEN 0.15
       ELSE (sourceCount / 5.0) * 0.15
     END AS consensusComponent,

     // Component 5: Fact-check validation (weight: 0.15)
     CASE
       WHEN factCheckCount = 0 THEN 0.075  // Neutral if no fact-checks
       ELSE COALESCE(avgFactCheckScore, 0.5) * 0.15
     END AS factCheckComponent,

     // Component 6: Temporal decay (weight: 0.05)
     avgTemporalFactor * 0.05 AS temporalComponent,

     // Bias penalty (applied after)
     COALESCE(avgBiasPenalty, 0.0) AS biasPenalty,

     sourceCount, citationCount, factCheckCount

// Sum all components and apply bias penalty
WITH claim,
     sourceComponent + citationComponent + citationCountComponent +
     consensusComponent + factCheckComponent + temporalComponent AS baseConfidence,
     biasPenalty,
     sourceCount, citationCount, factCheckCount

// Final confidence score (clamped to 0.0-1.0)
SET claim.confidenceScore =
  CASE
    WHEN baseConfidence + biasPenalty > 1.0 THEN 1.0
    WHEN baseConfidence + biasPenalty < 0.0 THEN 0.0
    ELSE baseConfidence + biasPenalty
  END,
  claim.sourceCount = sourceCount,
  claim.citationCount = citationCount,
  claim.lastUpdatedAt = datetime()

RETURN claim.claimId AS claimId,
       claim.confidenceScore AS confidenceScore,
       sourceCount,
       citationCount,
       factCheckCount;

// ───────────────────────────────────────────────────────────────────────────────
// Query 2: Update Source Credibility Based on Historical Performance
// ───────────────────────────────────────────────────────────────────────────────
// Adjusts source credibility based on accuracy of past claims

// USAGE: Update credibility for source with ID 'source_123'
MATCH (source:InformationSource {sourceId: 'source_123'})

// Get all claims made by this source
OPTIONAL MATCH (source)-[:MAKES_CLAIM]->(claim:Claim)
WHERE claim.verificationStatus IS NOT NULL

WITH source,
     count(claim) AS totalClaims,
     sum(CASE WHEN claim.verificationStatus = 'verified' THEN 1 ELSE 0 END) AS verifiedClaims,
     sum(CASE WHEN claim.verificationStatus = 'false' THEN 1 ELSE 0 END) AS falseClaims,
     sum(CASE WHEN claim.verificationStatus = 'disputed' THEN 1 ELSE 0 END) AS disputedClaims,
     avg(claim.confidenceScore) AS avgClaimConfidence

// Calculate accuracy rate
WITH source, totalClaims, verifiedClaims, falseClaims, disputedClaims, avgClaimConfidence,
     CASE
       WHEN totalClaims = 0 THEN source.baselineCredibility
       ELSE (verifiedClaims * 1.0 + disputedClaims * 0.5) / totalClaims
     END AS accuracyRate

// Apply learning rate adjustment (slow adaptation to prevent volatility)
WITH source, totalClaims, verifiedClaims, falseClaims, disputedClaims,
     avgClaimConfidence, accuracyRate,
     CASE
       WHEN totalClaims < 10 THEN 0.1   // Very slow learning for new sources
       WHEN totalClaims < 50 THEN 0.2   // Moderate learning
       WHEN totalClaims < 200 THEN 0.3  // Normal learning
       ELSE 0.4                          // Faster learning for established sources
     END AS learningRate

// Calculate new credibility score
WITH source, totalClaims, verifiedClaims, falseClaims, accuracyRate,
     source.credibilityScore * (1 - learningRate) + accuracyRate * learningRate AS newCredibility

// Determine reputation trend
WITH source, totalClaims, verifiedClaims, falseClaims, accuracyRate, newCredibility,
     CASE
       WHEN newCredibility > source.credibilityScore + 0.05 THEN 'improving'
       WHEN newCredibility < source.credibilityScore - 0.05 THEN 'declining'
       ELSE 'stable'
     END AS reputationTrend

// Create historical reputation record
CREATE (rep:SourceReputation {
  reputationId: source.sourceId + '_' + toString(timestamp()),
  timestamp: datetime(),
  credibilityScore: source.credibilityScore,  // Old score
  accuracyRate: accuracyRate,
  verifiedClaimsCount: verifiedClaims,
  disputedClaimsCount: falseClaims,
  retractionCount: 0,  // Would be tracked separately
  changeReason: 'periodic_update'
})

// Link reputation history to source
CREATE (source)-[:HAS_REPUTATION_HISTORY {recordedAt: datetime()}]->(rep)

// Update source credibility
SET source.credibilityScore = newCredibility,
    source.reputationTrend = reputationTrend,
    source.lastUpdated = datetime()

RETURN source.sourceId AS sourceId,
       source.credibilityScore AS newCredibility,
       source.credibilityScore - newCredibility AS credibilityChange,
       reputationTrend,
       accuracyRate,
       totalClaims;

// ───────────────────────────────────────────────────────────────────────────────
// Query 3: Detect and Score Bias in Sources
// ───────────────────────────────────────────────────────────────────────────────
// Analyzes patterns to detect bias in information sources

// USAGE: Detect bias for source 'source_123' based on claim patterns
MATCH (source:InformationSource {sourceId: 'source_123'})

// Analyze claims by domain to detect domain concentration (potential expertise or bias)
OPTIONAL MATCH (source)-[:MAKES_CLAIM]->(claim:Claim)
WITH source,
     count(claim) AS totalClaims,
     collect(claim.domain) AS domains

// Calculate domain concentration (high concentration may indicate bias or expertise)
WITH source, totalClaims, domains,
     [domain IN domains | size([d IN domains WHERE d = domain])] AS domainCounts,
     size([d IN domains WHERE d IS NOT NULL]) AS nonNullDomains

WITH source, totalClaims,
     CASE
       WHEN nonNullDomains = 0 THEN 0.0
       ELSE toFloat(reduce(max = 0, count IN domainCounts | CASE WHEN count > max THEN count ELSE max END)) / nonNullDomains
     END AS domainConcentration

// Analyze claim verification patterns (false claims in specific domains = bias)
OPTIONAL MATCH (source)-[:MAKES_CLAIM]->(claim:Claim)
WHERE claim.verificationStatus IN ['false', 'disputed']
WITH source, totalClaims, domainConcentration,
     collect(claim.domain) AS falseClaimDomains

// Calculate false claim concentration by domain
WITH source, totalClaims, domainConcentration, falseClaimDomains,
     CASE
       WHEN size(falseClaimDomains) = 0 THEN 0.0
       WHEN size(falseClaimDomains) = 1 THEN 1.0
       ELSE toFloat(reduce(max = 0, domain IN falseClaimDomains |
              size([d IN falseClaimDomains WHERE d = domain]) + max)) / size(falseClaimDomains)
     END AS falseClaimConcentration

// Determine bias severity based on patterns
WITH source, totalClaims, domainConcentration, falseClaimConcentration,
     CASE
       WHEN domainConcentration > 0.7 AND falseClaimConcentration > 0.6 THEN 0.8  // High bias
       WHEN domainConcentration > 0.6 AND falseClaimConcentration > 0.4 THEN 0.6  // Moderate bias
       WHEN domainConcentration > 0.5 OR falseClaimConcentration > 0.3 THEN 0.4   // Low bias
       ELSE 0.2  // Minimal bias
     END AS biasSeverity

// Create or update bias indicator if severity is significant
WHERE biasSeverity > 0.3

MERGE (bias:BiasIndicator {
  biasId: source.sourceId + '_confirmation_bias',
  biasType: 'confirmation',
  severity: biasSeverity,
  confidence: 0.7,  // Medium confidence in detection
  detectionMethod: 'pattern_matching',
  detectedAt: datetime()
})

// Link bias to source
MERGE (source)-[r:HAS_BIAS]->(bias)
SET r.detectedAt = datetime(),
    r.impactOnCredibility = -0.1 * biasSeverity  // Credibility penalty

RETURN source.sourceId AS sourceId,
       biasSeverity AS detectedBiasSeverity,
       domainConcentration,
       falseClaimConcentration;

// ───────────────────────────────────────────────────────────────────────────────
// Query 4: Cross-Reference Validation (Multi-Source Verification)
// ───────────────────────────────────────────────────────────────────────────────
// Identifies claims supported by multiple independent sources

// USAGE: Find claims with strong cross-source consensus
MATCH (claim:Claim)
WHERE claim.sourceCount >= 2

// Get all sources making this claim
MATCH (source:InformationSource)-[makes:MAKES_CLAIM]->(claim)

// Calculate source diversity metrics
WITH claim,
     collect(DISTINCT source) AS sources,
     collect(DISTINCT source.platform) AS platforms,
     collect(DISTINCT source.sourceType) AS sourceTypes,
     avg(source.credibilityScore) AS avgSourceCredibility,
     count(DISTINCT source) AS sourceCount

// Check for corroboration between sources
OPTIONAL MATCH (source1:InformationSource)-[:MAKES_CLAIM]->(claim)
              <-[:MAKES_CLAIM]-(source2:InformationSource)
WHERE source1.sourceId < source2.sourceId  // Avoid duplicate pairs
  AND NOT (source1)-[:CORROBORATES]->()-[:MAKES_CLAIM]->(claim)

// Create corroboration relationships
FOREACH (ignoreMe IN CASE WHEN sourceCount >= 2 THEN [1] ELSE [] END |
  MERGE (source1)-[corr:CORROBORATES {
    corroboratedAt: datetime(),
    independentVerification: source1.platform <> source2.platform,
    agreementLevel: 1.0
  }]->(source2)
)

// Calculate consensus score
WITH claim, sources, platforms, sourceTypes,
     avgSourceCredibility, sourceCount,
     size(platforms) AS platformDiversity,
     size(sourceTypes) AS sourceTypeDiversity

// Calculate consensus level (0.0-1.0)
WITH claim,
     CASE
       WHEN sourceCount = 1 THEN 0.0
       WHEN sourceCount >= 5 AND platformDiversity >= 3 THEN 1.0
       WHEN sourceCount >= 3 AND platformDiversity >= 2 THEN 0.8
       WHEN sourceCount >= 2 THEN 0.5
       ELSE 0.3
     END AS consensusLevel,
     avgSourceCredibility,
     sourceCount,
     platformDiversity,
     sourceTypeDiversity

// Update claim consensus properties
SET claim.consensusLevel = consensusLevel,
    claim.lastUpdatedAt = datetime()

// Boost confidence for high consensus
WITH claim, consensusLevel, avgSourceCredibility, sourceCount
WHERE consensusLevel >= 0.7
SET claim.confidenceScore =
  CASE
    WHEN claim.confidenceScore + (consensusLevel * 0.15) > 1.0 THEN 1.0
    ELSE claim.confidenceScore + (consensusLevel * 0.15)
  END

RETURN claim.claimId AS claimId,
       claim.confidenceScore AS boostedConfidence,
       consensusLevel,
       avgSourceCredibility,
       sourceCount;

// ───────────────────────────────────────────────────────────────────────────────
// Query 5: Temporal Credibility Decay for Citations
// ───────────────────────────────────────────────────────────────────────────────
// Updates citation credibility based on age (older = less relevant)

// USAGE: Apply temporal decay to all citations older than 30 days
MATCH (citation:Citation)
WHERE citation.publishDate IS NOT NULL
  AND duration.between(citation.publishDate, datetime()).days > 30

// Calculate temporal decay factor (exponential decay)
WITH citation,
     duration.between(citation.publishDate, datetime()).days AS ageInDays,
     // Half-life of 365 days (citation loses half credibility per year)
     exp(-ln(2) * duration.between(citation.publishDate, datetime()).days / 365.0) AS decayFactor

// Apply decay to credibility score (never below 0.1 baseline)
WITH citation, ageInDays, decayFactor,
     CASE
       WHEN citation.credibilityScore * decayFactor < 0.1 THEN 0.1
       ELSE citation.credibilityScore * decayFactor
     END AS newCredibility

// Update citation credibility
SET citation.credibilityScore = newCredibility

// Update related claims' confidence scores
WITH citation
MATCH (claim:Claim)-[cites:CITES]->(citation)
WITH claim,
     collect(citation.credibilityScore) AS citationScores,
     count(citation) AS citationCount

// Recalculate claim confidence with updated citation scores
SET claim.confidenceScore =
  CASE
    WHEN citationCount = 0 THEN claim.confidenceScore
    ELSE claim.confidenceScore * 0.7 + (reduce(sum = 0.0, score IN citationScores | sum + score) / citationCount) * 0.3
  END,
  claim.lastUpdatedAt = datetime()

RETURN claim.claimId AS claimId,
       claim.confidenceScore AS updatedConfidence,
       citationCount;

// ───────────────────────────────────────────────────────────────────────────────
// Query 6: Source Reputation Tracking Over Time
// ───────────────────────────────────────────────────────────────────────────────
// Retrieves historical reputation data for trend analysis

// USAGE: Get reputation history for source 'source_123' over last 90 days
MATCH (source:InformationSource {sourceId: 'source_123'})
       -[:HAS_REPUTATION_HISTORY]->(rep:SourceReputation)
WHERE rep.timestamp >= datetime() - duration({days: 90})

// Order by timestamp to show trend
WITH source, rep
ORDER BY rep.timestamp DESC

RETURN source.sourceId AS sourceId,
       source.credibilityScore AS currentCredibility,
       collect({
         timestamp: rep.timestamp,
         credibilityScore: rep.credibilityScore,
         accuracyRate: rep.accuracyRate,
         verifiedClaimsCount: rep.verifiedClaimsCount,
         disputedClaimsCount: rep.disputedClaimsCount,
         changeReason: rep.changeReason
       }) AS reputationHistory,
       source.reputationTrend AS currentTrend;

// ───────────────────────────────────────────────────────────────────────────────
// Query 7: Identify Contradictory Claims
// ───────────────────────────────────────────────────────────────────────────────
// Finds claims that contradict each other for conflict resolution

// USAGE: Find contradictions for a specific domain (e.g., 'health')
MATCH (claim1:Claim {domain: 'health'})
MATCH (claim2:Claim {domain: 'health'})
WHERE claim1.claimId < claim2.claimId  // Avoid duplicate pairs
  AND claim1.content <> claim2.content

// Check for factual contradiction indicators (would use NLP in production)
// For now, use fact-check results as proxy
MATCH (claim1)-[:FACT_CHECKED]->(fc1:FactCheck)
MATCH (claim2)-[:FACT_CHECKED]->(fc2:FactCheck)
WHERE (fc1.rating = 'true' AND fc2.rating = 'false') OR
      (fc1.rating = 'false' AND fc2.rating = 'true')

// Create contradiction relationship
MERGE (claim1)-[contra:CONTRADICTS {
  contradictedAt: datetime(),
  contradictionType: 'direct',
  evidence: 'fact_check_disagreement'
}]->(claim2)

// Flag both claims for review
SET claim1.verificationStatus = 'disputed',
    claim2.verificationStatus = 'disputed'

// Reduce confidence for both claims
SET claim1.confidenceScore = claim1.confidenceScore * 0.7,
    claim2.confidenceScore = claim2.confidenceScore * 0.7

RETURN claim1.claimId AS claim1Id,
       claim1.content AS claim1Content,
       claim1.confidenceScore AS claim1Confidence,
       claim2.claimId AS claim2Id,
       claim2.content AS claim2Content,
       claim2.confidenceScore AS claim2Confidence;

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 5: BATCH OPERATIONS FOR PERFORMANCE
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// Batch Update: Recalculate All Claim Confidence Scores
// ───────────────────────────────────────────────────────────────────────────────
// Run periodically to update all claims based on latest data

// USAGE: Batch update all claims (run daily/weekly)
CALL apoc.periodic.iterate(
  "MATCH (claim:Claim) RETURN claim",
  "
  // Get source credibility
  OPTIONAL MATCH (source:InformationSource)-[:MAKES_CLAIM]->(claim)
  WITH claim, avg(source.credibilityScore) AS avgSourceCredibility, count(source) AS sourceCount

  // Get citation quality
  OPTIONAL MATCH (claim)-[cites:CITES]->(citation:Citation)
  WITH claim, avgSourceCredibility, sourceCount,
       avg(citation.credibilityScore * cites.evidenceWeight) AS avgCitationScore,
       count(citation) AS citationCount

  // Get fact-check results
  OPTIONAL MATCH (claim)-[checked:FACT_CHECKED]->(fc:FactCheck)
  WITH claim, avgSourceCredibility, sourceCount, avgCitationScore, citationCount,
       avg(fc.ratingScore * checked.factCheckerCredibility) AS avgFactCheckScore

  // Calculate confidence components
  WITH claim,
       COALESCE(avgSourceCredibility, 0.3) * 0.30 AS sourceComponent,
       COALESCE(avgCitationScore, 0.0) * 0.25 AS citationComponent,
       CASE WHEN citationCount >= 10 THEN 0.10 ELSE log10(citationCount + 1) * 0.10 END AS citationCountComponent,
       CASE WHEN sourceCount >= 5 THEN 0.15 ELSE (sourceCount / 5.0) * 0.15 END AS consensusComponent,
       COALESCE(avgFactCheckScore, 0.5) * 0.15 AS factCheckComponent

  // Update confidence score
  SET claim.confidenceScore =
    CASE
      WHEN sourceComponent + citationComponent + citationCountComponent + consensusComponent + factCheckComponent > 1.0
      THEN 1.0
      ELSE sourceComponent + citationComponent + citationCountComponent + consensusComponent + factCheckComponent
    END,
    claim.lastUpdatedAt = datetime()
  ",
  {batchSize: 1000, parallel: true}
);

// ───────────────────────────────────────────────────────────────────────────────
// Batch Update: Apply Temporal Decay to All Citations
// ───────────────────────────────────────────────────────────────────────────────
// Run daily to decay citation credibility based on age

// USAGE: Batch apply temporal decay (run daily)
CALL apoc.periodic.iterate(
  "MATCH (citation:Citation) WHERE citation.publishDate IS NOT NULL RETURN citation",
  "
  WITH citation,
       exp(-ln(2) * duration.between(citation.publishDate, datetime()).days / 365.0) AS decayFactor
  SET citation.credibilityScore =
    CASE
      WHEN citation.credibilityScore * decayFactor < 0.1 THEN 0.1
      ELSE citation.credibilityScore * decayFactor
    END
  ",
  {batchSize: 5000, parallel: true}
);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 6: EXAMPLE DATA CREATION (FOR TESTING)
// ═══════════════════════════════════════════════════════════════════════════════

// Example: Create a verified news source
CREATE (source1:InformationSource {
  sourceId: 'source_nyt_001',
  platform: 'news_site',
  sourceType: 'media_outlet',
  name: 'The New York Times',
  handle: 'nytimes',
  url: 'https://www.nytimes.com',
  credibilityScore: 0.85,
  baselineCredibility: 0.75,
  verificationStatus: 'verified',
  followerCount: 10000000,
  accountAge: 5000,
  contentVolume: 50000,
  expertiseDomains: ['politics', 'business', 'world', 'health'],
  biasIndicators: {political: -0.1, commercial: 0.0, ideological: -0.05},
  reputationTrend: 'stable',
  lastUpdated: datetime(),
  createdAt: datetime()
});

// Example: Create an academic source
CREATE (source2:InformationSource {
  sourceId: 'source_harvard_med',
  platform: 'academic',
  sourceType: 'academic_institution',
  name: 'Harvard Medical School',
  handle: 'harvardmed',
  url: 'https://hms.harvard.edu',
  credibilityScore: 0.95,
  baselineCredibility: 0.90,
  verificationStatus: 'verified',
  followerCount: 500000,
  accountAge: 3650,
  contentVolume: 5000,
  expertiseDomains: ['health', 'medicine', 'research'],
  biasIndicators: {political: 0.0, commercial: 0.0, ideological: 0.0},
  reputationTrend: 'stable',
  lastUpdated: datetime(),
  createdAt: datetime()
});

// Example: Create an unverified social media source
CREATE (source3:InformationSource {
  sourceId: 'source_twitter_123',
  platform: 'twitter',
  sourceType: 'individual',
  name: 'Random User',
  handle: '@randomuser123',
  url: 'https://twitter.com/randomuser123',
  credibilityScore: 0.30,
  baselineCredibility: 0.30,
  verificationStatus: 'unverified',
  followerCount: 500,
  accountAge: 60,
  contentVolume: 200,
  expertiseDomains: [],
  biasIndicators: {political: 0.3, commercial: 0.0, ideological: 0.2},
  reputationTrend: 'stable',
  lastUpdated: datetime(),
  createdAt: datetime()
});

// Example: Create a claim
CREATE (claim1:Claim {
  claimId: 'claim_vax_001',
  content: 'mRNA vaccines are effective against COVID-19',
  claimType: 'factual',
  domain: 'health',
  confidenceScore: 0.0,  // Will be calculated
  verificationStatus: 'unverified',
  firstSeenAt: datetime(),
  lastUpdatedAt: datetime(),
  citationCount: 0,
  sourceCount: 0,
  consensusLevel: 0.0
});

// Example: Create citations
CREATE (citation1:Citation {
  citationId: 'cite_nejm_001',
  url: 'https://www.nejm.org/doi/full/10.1056/NEJMoa2034577',
  title: 'Safety and Efficacy of the BNT162b2 mRNA Covid-19 Vaccine',
  contentType: 'study',
  publishDate: datetime('2020-12-31T00:00:00Z'),
  accessDate: datetime(),
  credibilityScore: 0.95,
  primaryEvidence: true,
  peerReviewed: true,
  archived: true,
  archiveUrl: 'https://web.archive.org/web/...'
});

CREATE (citation2:Citation {
  citationId: 'cite_cdc_001',
  url: 'https://www.cdc.gov/coronavirus/vaccines',
  title: 'COVID-19 Vaccines',
  contentType: 'report',
  publishDate: datetime('2021-01-15T00:00:00Z'),
  accessDate: datetime(),
  credibilityScore: 0.90,
  primaryEvidence: true,
  peerReviewed: false,
  archived: true,
  archiveUrl: 'https://web.archive.org/web/...'
});

// Example: Create fact-check
CREATE (fc1:FactCheck {
  factCheckId: 'fc_snopes_001',
  factChecker: 'snopes',
  rating: 'true',
  ratingScore: 1.0,
  url: 'https://www.snopes.com/fact-check/mrna-vaccine-effectiveness/',
  publishedAt: datetime('2021-02-01T00:00:00Z'),
  summary: 'Multiple peer-reviewed studies confirm mRNA vaccine effectiveness'
});

// Example: Create bias indicator
CREATE (bias1:BiasIndicator {
  biasId: 'bias_twitter_123_political',
  biasType: 'political_right',
  severity: 0.6,
  confidence: 0.7,
  detectionMethod: 'nlp_analysis',
  evidence: ['Frequent use of partisan language', 'Selective fact sharing'],
  detectedAt: datetime()
});

// Example: Link sources to claim
MATCH (s1:InformationSource {sourceId: 'source_harvard_med'})
MATCH (c1:Claim {claimId: 'claim_vax_001'})
CREATE (s1)-[:MAKES_CLAIM {
  claimedAt: datetime(),
  originalPost: true,
  confidence: 1.0,
  context: 'Based on clinical trial data'
}]->(c1);

// Example: Link citations to claim
MATCH (c1:Claim {claimId: 'claim_vax_001'})
MATCH (cite1:Citation {citationId: 'cite_nejm_001'})
MATCH (cite2:Citation {citationId: 'cite_cdc_001'})
CREATE (c1)-[:CITES {
  citedAt: datetime(),
  evidenceWeight: 1.0,
  relevanceScore: 1.0,
  directSupport: true
}]->(cite1);

CREATE (c1)-[:CITES {
  citedAt: datetime(),
  evidenceWeight: 0.9,
  relevanceScore: 0.95,
  directSupport: true
}]->(cite2);

// Example: Link fact-check to claim
MATCH (c1:Claim {claimId: 'claim_vax_001'})
MATCH (fc1:FactCheck {factCheckId: 'fc_snopes_001'})
CREATE (c1)-[:FACT_CHECKED {
  checkedAt: datetime(),
  factCheckerCredibility: 0.85
}]->(fc1);

// Example: Link bias to source
MATCH (s3:InformationSource {sourceId: 'source_twitter_123'})
MATCH (b1:BiasIndicator {biasId: 'bias_twitter_123_political'})
CREATE (s3)-[:HAS_BIAS {
  detectedAt: datetime(),
  impactOnCredibility: -0.15
}]->(b1);

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION 7: UTILITY QUERIES
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// Get Top Credible Sources
// ───────────────────────────────────────────────────────────────────────────────
MATCH (source:InformationSource)
WHERE source.credibilityScore > 0.8
RETURN source.name AS name,
       source.credibilityScore AS credibility,
       source.reputationTrend AS trend,
       source.sourceType AS type
ORDER BY source.credibilityScore DESC
LIMIT 10;

// ───────────────────────────────────────────────────────────────────────────────
// Get High Confidence Claims by Domain
// ───────────────────────────────────────────────────────────────────────────────
MATCH (claim:Claim)
WHERE claim.confidenceScore > 0.7
  AND claim.domain = 'health'
RETURN claim.content AS content,
       claim.confidenceScore AS confidence,
       claim.sourceCount AS sources,
       claim.citationCount AS citations,
       claim.verificationStatus AS status
ORDER BY claim.confidenceScore DESC
LIMIT 20;

// ───────────────────────────────────────────────────────────────────────────────
// Identify Sources with Declining Reputation
// ───────────────────────────────────────────────────────────────────────────────
MATCH (source:InformationSource)
WHERE source.reputationTrend = 'declining'
RETURN source.name AS name,
       source.credibilityScore AS currentCredibility,
       source.sourceType AS type,
       source.platform AS platform
ORDER BY source.credibilityScore ASC;

// ═══════════════════════════════════════════════════════════════════════════════
// END OF CONFIDENCE SCORING SCHEMA
// ═══════════════════════════════════════════════════════════════════════════════
