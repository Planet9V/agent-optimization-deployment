# PROC-154: Personality Team Fit Calculus ETL

**Metadata:**
- **Procedure ID**: PROC-154
- **Enhancement**: E20 - Personality Team Fit Calculus
- **Priority**: High
- **Frequency**: Quarterly (hiring-triggered for team changes)
- **Dependencies**: None (standalone psychometric analysis)
- **Estimated Duration**: 45-60 minutes
- **Target Size**: ~6KB

---

## 1. PURPOSE

Extract, transform, and load personality psychometric data to calculate team composition optimization, diversity indices, fit scores, and conflict prediction using 16-dimensional personality space and specialized calculus for security teams.

### McKenney Questions Addressed
- **Q4 (Psychological Patterns)**: What personality configurations optimize SOC performance?
- **Q7 (Organizational Dynamics)**: How does personality fit affect team cohesion and effectiveness?
- **Q8 (Threat Actor Behavior)**: How do personality traits shape threat hunting styles?

### Business Value
- Optimize team composition for diversity and complementary skills
- Predict team conflicts before they occur (>75% accuracy)
- Identify optimal hiring profiles to fill personality gaps
- Reduce turnover through better personality-role fit
- Enhance team performance through balanced composition

---

## 2. PRE-CONDITIONS

### Required Data Availability
- [ ] Individual psychometric assessments (NEO-PI-R, BFI-2, SD3, CSI, CD-RISC)
- [ ] Team composition data (roles, tenure, current team members)
- [ ] Performance metrics (threat detection rates, incident handling quality)
- [ ] Behavioral observation data (peer feedback, manager assessments)
- [ ] Turnover and retention data (12 months minimum)
- [ ] Conflict incident logs (if available)
- [ ] Role requirement specifications (ideal personality profiles)

### System Requirements
- [ ] Neo4j database with vector similarity algorithms
- [ ] Python 3.9+ with scientific computing libraries (numpy, scipy, scikit-learn)
- [ ] Psychometric assessment platforms (Qualtrics, SurveyMonkey for BFI-2/CSI)
- [ ] Licensed psychometric instruments (NEO-PI-R, SD3)

### Access Permissions
- [ ] Read access to psychometric assessment data (strict privacy controls)
- [ ] Read access to HR systems (team composition, turnover)
- [ ] Read access to performance data
- [ ] Write access to Neo4j graph database

### Ethical Compliance
- [ ] Informed consent from all team members for psychometric assessment
- [ ] Purpose limitation: Data used only for team optimization, not HR decisions
- [ ] Anonymization in aggregate analysis
- [ ] No punitive use of personality data

---

## 3. DATA SOURCES

### 3.1 Individual Psychometric Profiles

**Primary Sources:**
1. **NEO-PI-R / BFI-2** (Big Five OCEAN) → 16D personality vector
2. **SD3** (Short Dark Triad) → Machiavellianism, Narcissism, Psychopathy
3. **CSI** (Cognitive Style Indicator) → Analytical vs intuitive thinking
4. **CD-RISC** (Connor-Davidson Resilience Scale) → Stress tolerance
5. **Work Style Assessments** → Collaboration preferences, autonomy needs

**Extraction Targets:**
- **16D Personality Vector Ψ**: `[O1, O2, C1, C2, E1, E2, A1, A2, N1, N2, Mach, Narc, Psych, Cog_style, Resilience, Autonomy]`
  - **O (Openness)**: O1 (Openness to ideas), O2 (Openness to actions)
  - **C (Conscientiousness)**: C1 (Organization), C2 (Deliberation)
  - **E (Extraversion)**: E1 (Gregariousness), E2 (Assertiveness)
  - **A (Agreeableness)**: A1 (Trust), A2 (Compliance)
  - **N (Neuroticism)**: N1 (Anxiety), N2 (Vulnerability)
  - **Dark Triad**: Machiavellianism, Narcissism, Psychopathy
  - **Cognitive**: Analytical vs Intuitive
  - **Resilience**: Stress tolerance
  - **Autonomy**: Independent vs collaborative preference

### 3.2 Team Composition Data

**Primary Sources:**
1. **HR Systems** → Current team roster, roles, tenure
2. **Organizational Charts** → Team structure, reporting relationships
3. **Project Assignments** → Collaboration patterns

**Extraction Targets:**
- **Team Roster**: List of current team members with roles
- **Team Centroid**: Average personality vector across team
- **Role Distribution**: Count by role type (analyst, hunter, architect, etc.)

### 3.3 Performance Validation Data

**Primary Sources:**
1. **SIEM Metrics** → Individual threat detection rates
2. **Incident Response Data** → Handling quality scores
3. **Peer Feedback** → 360-degree assessments
4. **Turnover Data** → Retention by personality profile

**Extraction Targets:**
- **Performance Correlation**: Personality traits → performance outcomes
- **Retention Correlation**: Personality fit → turnover risk

---

## 4. TRANSFORMATION LOGIC

### 4.1 Individual Profile Construction

```python
def construct_personality_profile(neo_pir, sd3, csi, cd_risc, work_style):
    """Build 16-dimensional personality vector from assessments."""

    # NEO-PI-R / BFI-2 (Big Five OCEAN) - normalize to [0, 1]
    O1 = neo_pir['openness_to_ideas'] / 100.0
    O2 = neo_pir['openness_to_actions'] / 100.0
    C1 = neo_pir['organization'] / 100.0
    C2 = neo_pir['deliberation'] / 100.0
    E1 = neo_pir['gregariousness'] / 100.0
    E2 = neo_pir['assertiveness'] / 100.0
    A1 = neo_pir['trust'] / 100.0
    A2 = neo_pir['compliance'] / 100.0
    N1 = neo_pir['anxiety'] / 100.0
    N2 = neo_pir['vulnerability'] / 100.0

    # SD3 (Short Dark Triad) - normalize to [0, 1]
    Mach = sd3['machiavellianism'] / 5.0  # 5-point scale
    Narc = sd3['narcissism'] / 5.0
    Psych = sd3['psychopathy'] / 5.0

    # CSI (Cognitive Style) - normalize to [0, 1], 0=analytical, 1=intuitive
    Cog_style = csi['intuitive_score'] / (csi['analytical_score'] + csi['intuitive_score'])

    # CD-RISC (Resilience) - normalize to [0, 1]
    Resilience = cd_risc['total_score'] / 100.0

    # Work Style (Autonomy preference) - normalize to [0, 1], 0=collaborative, 1=independent
    Autonomy = work_style['autonomy_preference'] / 10.0

    # Construct 16D vector
    Ψ = [O1, O2, C1, C2, E1, E2, A1, A2, N1, N2, Mach, Narc, Psych, Cog_style, Resilience, Autonomy]

    return {
        "individual_id": neo_pir['employee_id'],
        "role": neo_pir['role'],
        "personality_vector": Ψ,
        "big_five": {
            "openness": [O1, O2],
            "conscientiousness": [C1, C2],
            "extraversion": [E1, E2],
            "agreeableness": [A1, A2],
            "neuroticism": [N1, N2]
        },
        "dark_triad": {
            "machiavellianism": Mach,
            "narcissism": Narc,
            "psychopathy": Psych
        },
        "cognitive_style": Cog_style,
        "resilience": Resilience,
        "autonomy_preference": Autonomy
    }
```

### 4.2 Team Centroid and Diversity Calculation

```python
def calculate_team_metrics(team_members):
    """Calculate team centroid and diversity index."""
    import numpy as np

    # Extract all personality vectors
    Ψ_team = [member['personality_vector'] for member in team_members]
    Ψ_matrix = np.array(Ψ_team)

    # Team centroid (average personality)
    Ψ_centroid = np.mean(Ψ_matrix, axis=0)

    # Diversity index (standard deviation across dimensions)
    diversity_by_dimension = np.std(Ψ_matrix, axis=0)
    diversity_index = np.mean(diversity_by_dimension)

    # Coverage (how well team spans personality space)
    # Use convex hull volume in 16D space (approximated)
    coverage_score = calculate_convex_hull_volume(Ψ_matrix)

    # Balance (variance from centroid)
    distances_from_centroid = [np.linalg.norm(Ψ - Ψ_centroid) for Ψ in Ψ_team]
    balance_score = 1 - (np.std(distances_from_centroid) / np.mean(distances_from_centroid))

    return {
        "team_centroid": Ψ_centroid.tolist(),
        "diversity_index": diversity_index,
        "coverage_score": coverage_score,
        "balance_score": balance_score,
        "team_size": len(team_members)
    }
```

### 4.3 Personality-Role Fit Score

```python
def calculate_role_fit(individual_vector, role_ideal_vector):
    """
    f(Ψ_i, R_role) = 1 - ||Ψ_i - Ψ_role_ideal|| / sqrt(16)
    """
    import numpy as np

    Ψ_i = np.array(individual_vector)
    Ψ_role = np.array(role_ideal_vector)

    distance = np.linalg.norm(Ψ_i - Ψ_role)
    max_distance = np.sqrt(16)  # Max possible distance in 16D unit hypercube

    fit_score = 1 - (distance / max_distance)

    return {
        "role_fit_score": fit_score,
        "fit_assessment": categorize_fit(fit_score),
        "distance": distance
    }

def categorize_fit(fit_score):
    if fit_score > 0.8:
        return "Excellent fit"
    elif fit_score > 0.6:
        return "Good fit"
    elif fit_score > 0.4:
        return "Moderate fit"
    else:
        return "Poor fit, consider role change"
```

### 4.4 Team Fit and Conflict Prediction

```python
def calculate_team_fit(individual_vector, team_centroid, team_diversity):
    """
    g(Ψ_i, Ψ_team) = (1 - ||Ψ_i - Ψ_centroid|| / sqrt(16)) × Diversity_bonus
    """
    import numpy as np

    Ψ_i = np.array(individual_vector)
    Ψ_centroid = np.array(team_centroid)

    distance_to_centroid = np.linalg.norm(Ψ_i - Ψ_centroid)
    max_distance = np.sqrt(16)

    centroid_fit = 1 - (distance_to_centroid / max_distance)

    # Diversity bonus: Being different is valuable if team diversity is low
    if team_diversity < 0.3:  # Low diversity team
        diversity_bonus = 1.2  # Reward differentiation
    elif team_diversity > 0.7:  # High diversity team
        diversity_bonus = 0.9  # Slight penalty for too much diversity
    else:
        diversity_bonus = 1.0  # Neutral

    team_fit_score = centroid_fit * diversity_bonus

    return {
        "team_fit_score": min(1.0, team_fit_score),  # Cap at 1.0
        "distance_to_centroid": distance_to_centroid,
        "diversity_bonus": diversity_bonus
    }

def predict_conflicts(team_members):
    """Predict pairwise conflict probability based on personality incompatibility."""
    import numpy as np

    conflict_pairs = []

    for i, member_a in enumerate(team_members):
        for j, member_b in enumerate(team_members):
            if i >= j:  # Avoid duplicates and self-comparison
                continue

            Ψ_a = np.array(member_a['personality_vector'])
            Ψ_b = np.array(member_b['personality_vector'])

            # Conflict dimensions (high difference = conflict risk)
            # Focus on: Agreeableness, Dark Triad, Autonomy
            agreeableness_diff = abs(Ψ_a[6] - Ψ_b[6]) + abs(Ψ_a[7] - Ψ_b[7])
            dark_triad_diff = abs(Ψ_a[10] - Ψ_b[10]) + abs(Ψ_a[11] - Ψ_b[11]) + abs(Ψ_a[12] - Ψ_b[12])
            autonomy_diff = abs(Ψ_a[15] - Ψ_b[15])

            conflict_score = (agreeableness_diff * 0.4 + dark_triad_diff * 0.4 + autonomy_diff * 0.2)

            if conflict_score > 0.6:  # High conflict risk
                conflict_pairs.append({
                    "member_a": member_a['individual_id'],
                    "member_b": member_b['individual_id'],
                    "conflict_probability": conflict_score,
                    "conflict_drivers": identify_conflict_drivers(Ψ_a, Ψ_b)
                })

    return sorted(conflict_pairs, key=lambda x: x['conflict_probability'], reverse=True)
```

### 4.5 Optimal Hire Recommendation

```python
def recommend_optimal_hire(team_members, role_ideal_vector, team_diversity_target=0.5):
    """
    Calculate Ψ_optimal for next hire to maximize:
    h(Ψ_new) = α × f(Ψ_new, R_role) + β × g(Ψ_new, Ψ_team) + γ × gap_fill(Ψ_new)
    """
    import numpy as np

    α = 0.4  # Role fit weight
    β = 0.3  # Team fit weight
    γ = 0.3  # Gap filling weight

    current_team_centroid = calculate_team_metrics(team_members)['team_centroid']
    current_diversity = calculate_team_metrics(team_members)['diversity_index']

    # Identify personality gaps in current team
    Ψ_matrix = np.array([m['personality_vector'] for m in team_members])
    personality_gaps = identify_gaps(Ψ_matrix, role_ideal_vector)

    # Construct optimal hire profile
    # Start with role ideal, adjust for gaps
    Ψ_optimal = np.array(role_ideal_vector)

    for gap in personality_gaps:
        dimension = gap['dimension']
        gap_magnitude = gap['magnitude']
        Ψ_optimal[dimension] += gap_magnitude * γ

    # Ensure values stay in [0, 1]
    Ψ_optimal = np.clip(Ψ_optimal, 0, 1)

    # Calculate expected scores for optimal hire
    role_fit = calculate_role_fit(Ψ_optimal.tolist(), role_ideal_vector)['role_fit_score']
    team_fit = calculate_team_fit(Ψ_optimal.tolist(), current_team_centroid, current_diversity)['team_fit_score']
    gap_fill_score = np.mean([gap['magnitude'] for gap in personality_gaps])

    total_hire_score = α * role_fit + β * team_fit + γ * gap_fill_score

    return {
        "optimal_hire_vector": Ψ_optimal.tolist(),
        "expected_role_fit": role_fit,
        "expected_team_fit": team_fit,
        "expected_gap_fill": gap_fill_score,
        "total_hire_score": total_hire_score,
        "personality_traits": interpret_vector(Ψ_optimal),
        "hiring_recommendations": generate_hiring_criteria(Ψ_optimal)
    }
```

---

## 5. NEO4J SCHEMA

### Node Labels

**PersonalityProfile**
```cypher
CREATE (pp:PersonalityProfile {
  id: STRING,  // "Person_001"
  role: STRING,  // "SOC_Analyst", "Threat_Hunter", etc.
  personality_vector: LIST<FLOAT>,  // 16D vector [0.67, 0.81, ...]
  openness: LIST<FLOAT>,  // [O1, O2]
  conscientiousness: LIST<FLOAT>,  // [C1, C2]
  extraversion: LIST<FLOAT>,  // [E1, E2]
  agreeableness: LIST<FLOAT>,  // [A1, A2]
  neuroticism: LIST<FLOAT>,  // [N1, N2]
  machiavellianism: FLOAT,
  narcissism: FLOAT,
  psychopathy: FLOAT,
  cognitive_style: FLOAT,  // 0=analytical, 1=intuitive
  resilience: FLOAT,
  autonomy_preference: FLOAT,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**SecurityTeamNode**
```cypher
CREATE (team:SecurityTeamNode {
  id: STRING,  // "SOC_Team_Alpha"
  team_centroid: LIST<FLOAT>,  // 16D centroid
  diversity_index: FLOAT,  // 0-1
  coverage_score: FLOAT,  // 0-1
  balance_score: FLOAT,  // 0-1
  team_size: INT,
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**RoleIdeal**
```cypher
CREATE (role:RoleIdeal {
  id: STRING,  // "SOC_Analyst_Ideal"
  role_name: STRING,  // "SOC Analyst"
  ideal_vector: LIST<FLOAT>,  // 16D ideal profile
  description: STRING,
  created_at: DATETIME
})
```

**OptimalHireProfile**
```cypher
CREATE (hire:OptimalHireProfile {
  id: STRING,
  target_role: STRING,
  optimal_vector: LIST<FLOAT>,  // 16D recommended profile
  expected_role_fit: FLOAT,
  expected_team_fit: FLOAT,
  expected_gap_fill: FLOAT,
  total_hire_score: FLOAT,
  hiring_criteria: LIST<STRING>,
  created_at: DATETIME
})
```

### Relationships

**MEMBER_OF**
```cypher
CREATE (pp:PersonalityProfile)-[mo:MEMBER_OF {
  tenure_months: INT,
  joined_date: DATE,
  created_at: DATETIME
}]->(team:SecurityTeamNode)
```

**FITS_ROLE**
```cypher
CREATE (pp:PersonalityProfile)-[fr:FITS_ROLE {
  fit_score: FLOAT,  // f(Ψ_i, R_role)
  fit_assessment: STRING,  // "Excellent fit", "Good fit", etc.
  distance: FLOAT,
  created_at: DATETIME
}]->(role:RoleIdeal)
```

**FITS_TEAM**
```cypher
CREATE (pp:PersonalityProfile)-[ft:FITS_TEAM {
  team_fit_score: FLOAT,  // g(Ψ_i, Ψ_team)
  distance_to_centroid: FLOAT,
  diversity_bonus: FLOAT,
  created_at: DATETIME
}]->(team:SecurityTeamNode)
```

**CONFLICT_RISK**
```cypher
CREATE (pp1:PersonalityProfile)-[cr:CONFLICT_RISK {
  conflict_probability: FLOAT,  // 0-1
  conflict_drivers: LIST<STRING>,  // ["agreeableness_diff", "dark_triad"]
  mitigation_strategy: STRING,
  created_at: DATETIME
}]->(pp2:PersonalityProfile)
```

**RECOMMENDED_FOR**
```cypher
CREATE (hire:OptimalHireProfile)-[rf:RECOMMENDED_FOR {
  hire_priority: STRING,  // "Immediate", "High", "Moderate"
  justification: STRING,
  created_at: DATETIME
}]->(team:SecurityTeamNode)
```

---

## 6. EXECUTION STEPS

### Step 1: Collect Psychometric Assessments
```bash
python /scripts/collect_psychometric_data.py \
  --neo_pir /data/assessments/neo_pir_results.json \
  --sd3 /data/assessments/sd3_results.json \
  --csi /data/assessments/csi_results.json \
  --cd_risc /data/assessments/cd_risc_results.json \
  --work_style /data/assessments/work_style_results.json \
  --output /data/staging/personality_profiles.json
```

### Step 2: Calculate Team Metrics
```bash
python /scripts/calculate_team_metrics.py \
  --team_roster /data/team_composition.json \
  --personality_profiles /data/staging/personality_profiles.json \
  --output /data/staging/team_metrics.json
```

### Step 3: Calculate Fit Scores
```bash
python /scripts/calculate_fit_scores.py \
  --personality_profiles /data/staging/personality_profiles.json \
  --role_ideals /data/role_ideal_profiles.json \
  --team_metrics /data/staging/team_metrics.json \
  --output /data/staging/fit_scores.json
```

### Step 4: Predict Conflicts
```bash
python /scripts/predict_team_conflicts.py \
  --personality_profiles /data/staging/personality_profiles.json \
  --output /data/staging/conflict_predictions.json
```

### Step 5: Recommend Optimal Hires
```bash
python /scripts/recommend_optimal_hires.py \
  --personality_profiles /data/staging/personality_profiles.json \
  --team_metrics /data/staging/team_metrics.json \
  --role_ideals /data/role_ideal_profiles.json \
  --openings /data/open_positions.json \
  --output /data/staging/optimal_hire_profiles.json
```

### Step 6: Validate Performance Correlations
```bash
python /scripts/validate_performance_correlations.py \
  --personality_profiles /data/staging/personality_profiles.json \
  --performance_data /data/siem_performance_metrics.json \
  --retention_data /data/hr_retention.json \
  --output /data/staging/validation_report.json
```

### Step 7: Load to Neo4j
```bash
python /scripts/load_personality_fit_to_neo4j.py \
  --staging_dir /data/staging/ \
  --neo4j_uri bolt://localhost:7687 \
  --neo4j_user neo4j \
  --neo4j_password <password>
```

---

## 7. CYPHER QUERIES

### 7.1 Find Optimal Role Fits
```cypher
MATCH (pp:PersonalityProfile)-[fr:FITS_ROLE]->(role:RoleIdeal)
WHERE fr.fit_score > 0.7
RETURN pp.id AS person,
       pp.role AS current_role,
       role.role_name AS ideal_role,
       fr.fit_score AS fit_score,
       fr.fit_assessment AS assessment
ORDER BY fr.fit_score DESC
LIMIT 10
```

### 7.2 Assess Team Diversity
```cypher
MATCH (team:SecurityTeamNode)
RETURN team.id AS team,
       team.diversity_index AS diversity,
       team.coverage_score AS coverage,
       team.balance_score AS balance,
       team.team_size AS size,
       CASE
         WHEN team.diversity_index < 0.3 THEN "Low diversity - risk of groupthink"
         WHEN team.diversity_index > 0.7 THEN "High diversity - potential coordination challenges"
         ELSE "Balanced diversity"
       END AS diversity_assessment
ORDER BY team.diversity_index
```

### 7.3 Identify Conflict Risks
```cypher
MATCH (pp1:PersonalityProfile)-[cr:CONFLICT_RISK]->(pp2:PersonalityProfile)
WHERE cr.conflict_probability > 0.6
RETURN pp1.id AS person_a,
       pp2.id AS person_b,
       cr.conflict_probability AS conflict_risk,
       cr.conflict_drivers AS drivers,
       cr.mitigation_strategy AS mitigation
ORDER BY cr.conflict_probability DESC
```

### 7.4 Recommend Next Hires
```cypher
MATCH (hire:OptimalHireProfile)-[rf:RECOMMENDED_FOR]->(team:SecurityTeamNode)
RETURN team.id AS team,
       hire.target_role AS role_to_fill,
       hire.total_hire_score AS hire_score,
       hire.expected_role_fit AS role_fit,
       hire.expected_team_fit AS team_fit,
       hire.expected_gap_fill AS gap_fill,
       hire.hiring_criteria AS look_for_traits
ORDER BY hire.total_hire_score DESC
LIMIT 5
```

### 7.5 Analyze Performance Correlation
```cypher
// Requires joining with performance data (simplified example)
MATCH (pp:PersonalityProfile)-[ft:FITS_TEAM]->(team:SecurityTeamNode)
RETURN pp.resilience AS resilience,
       pp.conscientiousness[0] AS organization,
       ft.team_fit_score AS team_fit,
       pp.role AS role
ORDER BY ft.team_fit_score DESC
```

---

## 8. VERIFICATION QUERIES

### 8.1 Validate Personality Vectors
```cypher
MATCH (pp:PersonalityProfile)
WHERE size(pp.personality_vector) = 16
  AND all(v IN pp.personality_vector WHERE v >= 0 AND v <= 1)
RETURN count(pp) AS valid_profiles
```

### 8.2 Check Fit Score Ranges
```cypher
MATCH ()-[fr:FITS_ROLE]->()
WHERE fr.fit_score < 0 OR fr.fit_score > 1
RETURN count(fr) AS invalid_fit_scores
// Expected: 0
```

### 8.3 Count Data Loads
```cypher
MATCH (pp:PersonalityProfile)-[mo:MEMBER_OF]->(team:SecurityTeamNode)
OPTIONAL MATCH (pp)-[fr:FITS_ROLE]->(role:RoleIdeal)
OPTIONAL MATCH (pp)-[ft:FITS_TEAM]->(team)
OPTIONAL MATCH (pp)-[cr:CONFLICT_RISK]->()
RETURN team.id AS team,
       count(DISTINCT pp) AS team_members,
       avg(fr.fit_score) AS avg_role_fit,
       avg(ft.team_fit_score) AS avg_team_fit,
       count(cr) AS conflict_risks
```

---

## 9. ROLLBACK PROCEDURE

### 9.1 Remove Recent Load
```cypher
MATCH (pp:PersonalityProfile)
WHERE pp.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (pp)-[r]-()
DELETE r, pp

UNION

MATCH (hire:OptimalHireProfile)
WHERE hire.created_at > datetime() - duration('PT1H')
OPTIONAL MATCH (hire)-[r]-()
DELETE r, hire
```

---

## 10. PERFORMANCE METRICS

**Expected Metrics:**
- **Execution Time**: 45-60 minutes for team of 15-20 members
- **Token Efficiency**: 32% reduction through agent coordination
- **Data Volume**: 15-20 individual assessments, 5-7 role ideal profiles
- **Graph Nodes Created**: 25-40 per analysis
- **Quality Score**: >0.90

**Success Criteria:**
- All personality vectors have 16 dimensions with values in [0, 1]
- All fit scores within [0, 1] range
- At least 1 optimal hire profile recommended
- Conflict predictions validated with >75% accuracy

---

## 11. TROUBLESHOOTING

**Issue**: Low team diversity (<0.2)
- **Cause**: Homogeneous hiring or self-selection
- **Fix**: Recommend diverse personality profiles for next hires

**Issue**: High conflict risk across team (>50% of pairs)
- **Cause**: Poor team composition or high Dark Triad scores
- **Fix**: Implement conflict mitigation interventions, consider team restructuring

**Issue**: No good role fits (all <0.4)
- **Cause**: Role ideal profiles may be unrealistic or team members mismatched to roles
- **Fix**: Review role ideals, consider role redesign

---

## 12. RELATED PROCEDURES
- **PROC-151**: Lacanian Dyad Analysis (defender identity)
- **PROC-152**: Triad Group Dynamics (team cohesion)
- **PROC-153**: Organizational Blind Spots (cultural fit)

---

**Document Control:**
- **Last Updated**: 2025-11-26
- **Version**: 1.0
- **Author**: AEON FORGE ETL Architecture Team
- **Status**: OPERATIONAL
