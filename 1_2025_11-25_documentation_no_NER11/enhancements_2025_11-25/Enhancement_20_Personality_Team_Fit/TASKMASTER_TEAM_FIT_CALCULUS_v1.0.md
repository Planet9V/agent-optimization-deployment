# TASKMASTER: Personality-Team Fit Calculus System
# Version 1.0.0

**File:** TASKMASTER_TEAM_FIT_CALCULUS_v1.0.md
**Created:** 2025-11-26
**Purpose:** 10-agent swarm for mathematical optimization of cybersecurity team composition through personality fit analysis
**Status:** ACTIVE

---

## Mission Statement

Deploy a 10-agent swarm to systematically profile individuals, calculate team fit scores, identify personality gaps, predict conflicts, and recommend optimal hiring decisions to maximize cybersecurity team effectiveness through strategic personality composition.

---

## Agent Architecture

### Agent 1: Individual Psychometric Profiler
**Role:** Administer and score personality assessments (Big Five + Dark Triad + Cognitive Styles + Behavioral)
**Input:** Assessment responses from candidates/employees
**Output:** 16-dimensional personality vector per individual

### Agent 2: Team Centroid Calculator
**Role:** Compute team aggregate statistics (centroid, covariance, diversity)
**Input:** Personality vectors of all team members
**Output:** Team centroid μ_T, covariance matrix Σ_T, diversity index D(T)

### Agent 3: Diversity Index Computer
**Role:** Quantify team personality space coverage and homogeneity
**Input:** Team personality vectors
**Output:** Diversity metrics + coverage maps

### Agent 4: Fit Score Calculator
**Role:** Compute individual-to-function and individual-to-team fit scores
**Input:** Individual personality vector, role requirements, team composition
**Output:** F_function, F_team, F_total scores

### Agent 5: Gap Identifier
**Role:** Detect missing personality types that would strengthen team
**Input:** Team composition, ideal coverage profile
**Output:** Prioritized list of personality gaps

### Agent 6: Conflict Predictor
**Role:** Predict personality clashes between individuals
**Input:** Personality vectors of team members (pairs)
**Output:** Conflict risk scores + high-risk pair identification

### Agent 7: Optimal Hire Recommender
**Role:** Rank candidates by total fit score and recommend hiring decisions
**Input:** Candidate pool, team composition, role requirements
**Output:** Ranked candidate list with hire/no-hire recommendations

### Agent 8: Team Evolution Modeler
**Role:** Simulate how team composition changes affect performance over time
**Input:** Team dynamics, turnover rates, hiring plans
**Output:** Performance trajectory forecasts

### Agent 9: Neo4j Team Graph Builder
**Role:** Construct graph database of people, teams, roles, and relationships
**Input:** All agent outputs
**Output:** Neo4j graph with personality-based relationships

### Agent 10: Quality Validator
**Role:** Validate mathematical rigor, ethical compliance, and actionability
**Input:** All agent outputs
**Output:** Quality scores + validation report

---

## Mathematical Framework

### Personality Space Definition (Agent 1)

#### Big Five (OCEAN) - 5 Dimensions

**Assessment:** NEO-PI-R (240 items) or BFI-2 (60 items)

```
Openness (O) ∈ [0, 1]
  High: Creative, curious, open to experience
  Low: Conventional, practical, routine-oriented

Conscientiousness (C) ∈ [0, 1]
  High: Organized, reliable, goal-directed
  Low: Spontaneous, flexible, careless

Extraversion (E) ∈ [0, 1]
  High: Sociable, assertive, energetic
  Low: Reserved, solitary, quiet

Agreeableness (A) ∈ [0, 1]
  High: Compassionate, cooperative, trusting
  Low: Competitive, challenging, detached

Neuroticism (N) ∈ [0, 1]
  High: Anxious, moody, emotionally reactive
  Low: Stable, calm, resilient
```

#### Dark Triad - 3 Dimensions

**Assessment:** Short Dark Triad (SD3, 27 items)

```
Machiavellianism (Mach) ∈ [0, 1]
  Strategic manipulation, long-term planning
  Security Application: Anticipate attacker tactics

Narcissism (Narc) ∈ [0, 1]
  Grandiosity, need for admiration
  Security Application: Confidence under pressure

Psychopathy (Psych) ∈ [0, 1] (Subclinical only)
  Callousness, fearlessness, impulsivity
  Security Application: Emotional detachment in IR
```

**CRITICAL ETHICAL NOTE:** Only subclinical levels (≤ 60th percentile) acceptable. High Dark Triad (>80th percentile) requires oversight. Use for defensive mindset, not interpersonal manipulation.

#### Cognitive Styles - 4 Dimensions

**Assessment:** Cognitive Style Indicator (CSI, 38 items)

```
Analytical ∈ [0, 1]: Data-driven, systematic thinking
Creative ∈ [0, 1]: Imaginative, lateral thinking
Pragmatic ∈ [0, 1]: Results-oriented, efficient
Relational ∈ [0, 1]: People-focused, empathetic
```

#### Behavioral Dimensions - 4 Dimensions

**Assessment:** Custom questionnaire + structured interview

```
Risk_Tolerance ∈ [0, 1]: Willingness to act under uncertainty
Stress_Resilience ∈ [0, 1]: Ability to function under pressure
Attention_to_Detail ∈ [0, 1]: Thoroughness, completeness
Autonomy ∈ [0, 1]: Preference for independent vs collaborative work
```

#### Complete Personality Vector

```
p = [O, C, E, A, N, Mach, Narc, Psych, Analytical, Creative, Pragmatic, Relational, Risk_Tol, Stress_Res, Attention, Autonomy]

Dimensionality: n = 16

Normalization: Each component ∈ [0, 1] via percentile ranking against population norms
```

---

### Agent 1 Implementation: Psychometric Profiler

**Input Schema:**
```json
{
  "person_id": "CAND-2025-042",
  "assessment_responses": {
    "big_five": {
      "neo_pi_r_responses": [3, 4, 2, 5, ...],  // 240 Likert scale responses
      "scoring": "standard"
    },
    "dark_triad": {
      "sd3_responses": [2, 3, 4, ...],  // 27 Likert scale responses
      "scoring": "sum_scores"
    },
    "cognitive_styles": {
      "csi_responses": [1, 5, 3, ...],  // 38 responses
      "scoring": "factor_analysis"
    },
    "behavioral": {
      "risk_tolerance_score": 0.65,
      "stress_resilience_score": 0.82,
      "attention_detail_score": 0.91,
      "autonomy_score": 0.58
    }
  }
}
```

**Processing Logic:**
```python
import numpy as np
from scipy.stats import percentileofscore

def score_big_five(responses, scoring_key='neo_pi_r'):
    """
    Score Big Five traits from NEO-PI-R or BFI-2 responses.
    """
    # NEO-PI-R: 48 items per trait (240 total)
    # Scoring: Sum responses for each trait, convert to percentile

    traits = ['O', 'C', 'E', 'A', 'N']
    scores = {}

    for i, trait in enumerate(traits):
        # Extract items for this trait (48 items each)
        trait_items = responses[i*48:(i+1)*48]

        # Sum Likert scores (1-5)
        raw_score = sum(trait_items)

        # Convert to percentile using population norms
        # (norms from Costa & McCrae, 1992)
        percentile = percentileofscore(population_norms[trait], raw_score) / 100.0

        scores[trait] = percentile

    return scores

def score_dark_triad(responses):
    """
    Score Dark Triad from SD3 responses.
    """
    # SD3: 9 items per trait (27 total)
    # Mach items: 1-9, Narc items: 10-18, Psych items: 19-27

    mach_score = sum(responses[0:9]) / (9 * 5)  # Normalize to [0,1]
    narc_score = sum(responses[9:18]) / (9 * 5)
    psych_score = sum(responses[18:27]) / (9 * 5)

    # Convert to percentiles
    mach_percentile = percentileofscore(population_norms['Mach'], mach_score * 45) / 100.0
    narc_percentile = percentileofscore(population_norms['Narc'], narc_score * 45) / 100.0
    psych_percentile = percentileofscore(population_norms['Psych'], psych_score * 45) / 100.0

    return {
        'Mach': mach_percentile,
        'Narc': narc_percentile,
        'Psych': psych_percentile
    }

def score_cognitive_styles(responses):
    """
    Score cognitive styles via factor analysis.
    """
    # CSI produces 4 factors: Analytical, Creative, Pragmatic, Relational
    # Use pre-computed factor loadings

    factor_scores = np.dot(csi_factor_loadings, responses)

    # Normalize to [0, 1]
    normalized = (factor_scores - csi_means) / csi_stds
    percentiles = norm.cdf(normalized)  # Convert to percentiles

    return {
        'Analytical': percentiles[0],
        'Creative': percentiles[1],
        'Pragmatic': percentiles[2],
        'Relational': percentiles[3]
    }

def create_personality_vector(assessment_data):
    """
    Combine all assessments into single 16-dimensional vector.
    """
    big_five = score_big_five(assessment_data['big_five']['neo_pi_r_responses'])
    dark_triad = score_dark_triad(assessment_data['dark_triad']['sd3_responses'])
    cognitive = score_cognitive_styles(assessment_data['cognitive_styles']['csi_responses'])
    behavioral = assessment_data['behavioral']

    vector = [
        big_five['O'], big_five['C'], big_five['E'], big_five['A'], big_five['N'],
        dark_triad['Mach'], dark_triad['Narc'], dark_triad['Psych'],
        cognitive['Analytical'], cognitive['Creative'], cognitive['Pragmatic'], cognitive['Relational'],
        behavioral['risk_tolerance_score'], behavioral['stress_resilience_score'],
        behavioral['attention_detail_score'], behavioral['autonomy_score']
    ]

    return np.array(vector)
```

**Output Schema:**
```json
{
  "person_id": "CAND-2025-042",
  "personality_vector": [0.45, 0.82, 0.28, 0.65, 0.22, 0.35, 0.30, 0.18,
                         0.85, 0.38, 0.72, 0.48, 0.65, 0.82, 0.91, 0.58],
  "trait_breakdown": {
    "big_five": {"O": 0.45, "C": 0.82, "E": 0.28, "A": 0.65, "N": 0.22},
    "dark_triad": {"Mach": 0.35, "Narc": 0.30, "Psych": 0.18},
    "cognitive": {"Analytical": 0.85, "Creative": 0.38, "Pragmatic": 0.72, "Relational": 0.48},
    "behavioral": {"Risk_Tol": 0.65, "Stress_Res": 0.82, "Attention": 0.91, "Autonomy": 0.58}
  },
  "interpretation": {
    "strengths": ["Very high Conscientiousness", "High Stress Resilience", "Exceptional Attention to Detail"],
    "considerations": ["Low Extraversion (prefers solo work)", "Moderate Openness (balanced creativity/routine)"],
    "red_flags": []
  },
  "assessment_date": "2025-11-26",
  "assessor_notes": "Candidate shows excellent fit for SOC analyst role: high conscientiousness and attention to detail."
}
```

---

### Agent 2 Implementation: Team Centroid Calculator

**Input Schema:**
```json
{
  "team_id": "TEAM-SOC-001",
  "team_members": [
    {
      "person_id": "EMP-SEC-001",
      "personality_vector": [0.42, 0.79, 0.25, ...]
    },
    {
      "person_id": "EMP-SEC-002",
      "personality_vector": [0.38, 0.81, 0.33, ...]
    },
    ...
  ]
}
```

**Processing Logic:**
```python
def calculate_team_centroid(team_members):
    """
    Compute team average personality vector (centroid).
    """
    vectors = [member['personality_vector'] for member in team_members]
    vectors = np.array(vectors)

    centroid = np.mean(vectors, axis=0)

    return centroid

def calculate_covariance_matrix(team_members):
    """
    Compute team personality covariance matrix.
    """
    vectors = [member['personality_vector'] for member in team_members]
    vectors = np.array(vectors)

    # Center data
    centered = vectors - np.mean(vectors, axis=0)

    # Covariance matrix
    cov_matrix = np.cov(centered, rowvar=False)

    return cov_matrix

def calculate_diversity_index(team_members):
    """
    Compute team diversity as average distance from centroid.
    """
    vectors = [member['personality_vector'] for member in team_members]
    vectors = np.array(vectors)

    centroid = np.mean(vectors, axis=0)

    # Average Euclidean distance from centroid
    distances = [np.linalg.norm(v - centroid) for v in vectors]
    diversity = np.mean(distances)

    # Alternative: Determinant of covariance (volume in personality space)
    cov_matrix = calculate_covariance_matrix(team_members)
    diversity_det = np.linalg.det(cov_matrix) ** (1/len(centroid))

    return {
        'diversity_euclidean': diversity,
        'diversity_det': diversity_det
    }
```

**Output Schema:**
```json
{
  "team_id": "TEAM-SOC-001",
  "team_size": 7,
  "team_centroid": [0.42, 0.81, 0.28, 0.63, 0.27, 0.36, 0.32, 0.21,
                    0.83, 0.41, 0.71, 0.49, 0.43, 0.84, 0.89, 0.61],
  "covariance_matrix": [[0.012, -0.003, ...], [...], ...],
  "diversity_index": {
    "euclidean": 0.18,
    "determinant": 0.0023
  },
  "interpretation": {
    "homogeneity_level": "High (low diversity)",
    "strongest_alignment": "Conscientiousness (low variance σ=0.03)",
    "greatest_variation": "Openness (high variance σ=0.12)",
    "notes": "Team is highly homogeneous in core traits (C, N, Attention) which is good for SOC consistency, but lacks diversity in Openness which may limit innovation."
  }
}
```

---

### Agent 4 Implementation: Fit Score Calculator

**Role Ideal Profiles (Predefined):**
```python
ROLE_PROFILES = {
    'SOC_Analyst': np.array([0.40, 0.75, 0.30, 0.60, 0.25, 0.35, 0.30, 0.20,
                             0.80, 0.40, 0.70, 0.50, 0.40, 0.80, 0.90, 0.60]),

    'Threat_Hunter': np.array([0.85, 0.70, 0.40, 0.50, 0.30, 0.50, 0.40, 0.30,
                               0.75, 0.90, 0.60, 0.40, 0.65, 0.70, 0.85, 0.85]),

    'IR_Lead': np.array([0.55, 0.85, 0.65, 0.60, 0.20, 0.45, 0.50, 0.25,
                         0.80, 0.50, 0.85, 0.70, 0.70, 0.90, 0.80, 0.50]),

    'Red_Team': np.array([0.90, 0.65, 0.50, 0.30, 0.25, 0.70, 0.55, 0.50,
                          0.75, 0.95, 0.60, 0.30, 0.85, 0.75, 0.70, 0.80]),

    'Threat_Intel': np.array([0.75, 0.75, 0.25, 0.50, 0.30, 0.40, 0.35, 0.25,
                              0.90, 0.60, 0.65, 0.40, 0.30, 0.70, 0.90, 0.70]),

    'Security_Architect': np.array([0.70, 0.85, 0.45, 0.55, 0.25, 0.50, 0.45, 0.30,
                                    0.85, 0.70, 0.80, 0.60, 0.50, 0.75, 0.95, 0.65])
}
```

**Function Fit Calculation:**
```python
def cosine_similarity(v1, v2):
    """Compute cosine similarity between two vectors."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def calculate_function_fit(person_vector, role):
    """
    Compute how well person aligns with ideal role profile.
    """
    role_ideal = ROLE_PROFILES[role]

    fit = cosine_similarity(person_vector, role_ideal)

    return fit

def calculate_team_fit(person_vector, team_members, weights={'alignment': 0.4, 'gap_filling': 0.4, 'conflict': 0.2}):
    """
    Compute how well person fits into existing team.
    """
    team_vectors = [m['personality_vector'] for m in team_members]
    team_centroid = np.mean(team_vectors, axis=0)

    # Component 1: Alignment with team centroid
    alignment = cosine_similarity(person_vector, team_centroid)

    # Component 2: Gap filling (increase diversity)
    current_diversity = calculate_diversity_index(team_members)['euclidean']
    new_team = team_members + [{'personality_vector': person_vector}]
    new_diversity = calculate_diversity_index(new_team)['euclidean']

    gap_filling = (new_diversity - current_diversity) / current_diversity if current_diversity > 0 else 0.0

    # Component 3: Conflict risk
    conflict_risks = [conflict_risk_pairwise(person_vector, m['personality_vector']) for m in team_members]
    avg_conflict = np.mean(conflict_risks)

    # Combined team fit
    team_fit = (weights['alignment'] * alignment +
                weights['gap_filling'] * (1 + gap_filling) -
                weights['conflict'] * avg_conflict)

    return {
        'team_fit_total': team_fit,
        'alignment': alignment,
        'gap_filling': gap_filling,
        'conflict_risk': avg_conflict
    }

def conflict_risk_pairwise(p1, p2):
    """
    Predict conflict risk between two individuals.
    """
    # Extract traits from vectors
    # Indices: O=0, C=1, E=2, A=3, N=4, Mach=5, Narc=6, Psych=7, ...

    # Neuroticism clash (both high N → conflict)
    neuroticism_clash = p1[4] * p2[4]

    # Agreeableness clash (both low A → conflict)
    agreeableness_clash = (1 - p1[3]) * (1 - p2[3])

    # Extraversion mismatch (one intro, one extro)
    extraversion_mismatch = abs(p1[2] - p2[2])

    # Dark Triad clashes
    mach_clash = max(0, p1[5] + p2[5] - 1.2)  # Both Machiavellian
    narc_clash = max(0, p1[6] + p2[6] - 1.4)  # Both Narcissistic (dominance struggle)
    psych_clash = max(0, p1[7] * p2[7] - 0.3)  # Both callous

    dt_clash = mach_clash + narc_clash + psych_clash

    # Weighted combination
    conflict_risk = (0.3 * neuroticism_clash +
                     0.3 * agreeableness_clash +
                     0.2 * extraversion_mismatch +
                     0.2 * dt_clash)

    return conflict_risk

def calculate_total_fit(person_vector, role, team_members, weights={'function': 0.6, 'team': 0.4}):
    """
    Compute total fit score combining function and team fit.
    """
    function_fit = calculate_function_fit(person_vector, role)
    team_fit_components = calculate_team_fit(person_vector, team_members)
    team_fit = team_fit_components['team_fit_total']

    total_fit = weights['function'] * function_fit + weights['team'] * team_fit

    return {
        'total_fit': total_fit,
        'function_fit': function_fit,
        'team_fit': team_fit,
        'team_fit_components': team_fit_components,
        'interpretation': interpret_fit_score(total_fit)
    }

def interpret_fit_score(score):
    """Interpret fit score for hiring decision."""
    if score > 0.7:
        return "Strong Hire (Excellent Fit)"
    elif score > 0.5:
        return "Moderate Hire (Good Fit, interview further)"
    elif score > 0.3:
        return "Weak Hire (Marginal Fit, only if exceptional technical skills)"
    else:
        return "Do Not Hire (Poor Fit)"
```

**Output Schema:**
```json
{
  "person_id": "CAND-2025-042",
  "role": "SOC_Analyst",
  "team_id": "TEAM-SOC-001",
  "fit_scores": {
    "total_fit": 0.895,
    "function_fit": 0.982,
    "team_fit": 0.766,
    "team_fit_components": {
      "alignment": 0.975,
      "gap_filling": -0.02,
      "conflict_risk": 0.08
    }
  },
  "interpretation": "Strong Hire (Excellent Fit)",
  "detailed_analysis": {
    "strengths": [
      "Near-perfect alignment with SOC analyst ideal profile (0.982)",
      "Very similar to existing team (0.975 alignment)",
      "Low conflict risk with current team members (0.08)"
    ],
    "considerations": [
      "Slightly reduces team diversity (-2%), may want to prioritize diversity in next hire",
      "Very homogeneous team overall, consider adding creative problem-solver in future"
    ],
    "recommendation": "Strong hire. Candidate will integrate seamlessly and perform well in SOC analyst role."
  }
}
```

---

### Agent 5 Implementation: Gap Identifier

**Ideal Coverage Profile:**
```python
IDEAL_COVERAGE = {
    'SOC_Team': {
        'high_conscientiousness': 0.90,  # 90% of team should have C > 0.7
        'low_neuroticism': 0.80,          # 80% should have N < 0.3
        'moderate_openness': 0.60,        # 60% should have O in [0.4, 0.7]
        'high_attention_detail': 0.95,    # 95% should have Attention > 0.8
        'high_stress_resilience': 0.85,   # 85% should have Stress_Res > 0.7
        'creative_minority': 0.20         # 20% should have Creative > 0.7 (innovation)
    },
    'IR_Team': {
        'very_high_conscientiousness': 0.95,
        'very_low_neuroticism': 0.90,
        'high_stress_resilience': 0.95,
        'pragmatic_majority': 0.80,
        'relational_communicators': 0.50,
        'diverse_openness': 0.40
    },
    'Red_Team': {
        'very_high_openness': 0.90,
        'very_high_creative': 0.85,
        'moderate_dark_triad': 0.60,
        'high_risk_tolerance': 0.85,
        'high_autonomy': 0.80,
        'low_agreeableness': 0.50
    }
}
```

**Gap Detection Algorithm:**
```python
def identify_personality_gaps(team_members, team_type):
    """
    Compare team's actual coverage to ideal coverage profile.
    """
    ideal = IDEAL_COVERAGE[team_type]
    actual_coverage = compute_team_coverage(team_members)

    gaps = []

    for criterion, ideal_percentage in ideal.items():
        actual_percentage = actual_coverage.get(criterion, 0.0)

        if actual_percentage < ideal_percentage:
            gap_size = ideal_percentage - actual_percentage
            priority = gap_size / ideal_percentage  # Fractional gap

            gaps.append({
                'criterion': criterion,
                'ideal': ideal_percentage,
                'actual': actual_percentage,
                'gap_size': gap_size,
                'priority': priority,
                'recommendation': generate_gap_recommendation(criterion, gap_size)
            })

    # Sort by priority
    gaps.sort(key=lambda x: x['priority'], reverse=True)

    return gaps

def compute_team_coverage(team_members):
    """
    Compute percentage of team meeting various personality criteria.
    """
    n = len(team_members)
    coverage = {}

    # Extract all personality vectors
    vectors = [m['personality_vector'] for m in team_members]
    vectors = np.array(vectors)

    # High Conscientiousness (C > 0.7)
    coverage['high_conscientiousness'] = sum([v[1] > 0.7 for v in vectors]) / n

    # Low Neuroticism (N < 0.3)
    coverage['low_neuroticism'] = sum([v[4] < 0.3 for v in vectors]) / n

    # Moderate Openness (O in [0.4, 0.7])
    coverage['moderate_openness'] = sum([0.4 <= v[0] <= 0.7 for v in vectors]) / n

    # High Attention to Detail (Attention > 0.8)
    coverage['high_attention_detail'] = sum([v[14] > 0.8 for v in vectors]) / n

    # High Stress Resilience (Stress_Res > 0.7)
    coverage['high_stress_resilience'] = sum([v[13] > 0.7 for v in vectors]) / n

    # Creative Minority (Creative > 0.7)
    coverage['creative_minority'] = sum([v[9] > 0.7 for v in vectors]) / n

    # ... (additional criteria)

    return coverage

def generate_gap_recommendation(criterion, gap_size):
    """
    Generate actionable recommendation based on gap type.
    """
    recommendations = {
        'high_conscientiousness': f"Priority: Hire individuals with Conscientiousness > 0.7 (gap: {gap_size:.1%}). Focus on detail-oriented candidates with track record of thorough work.",

        'low_neuroticism': f"Priority: Hire emotionally stable individuals with Neuroticism < 0.3 (gap: {gap_size:.1%}). Stress resilience critical for SOC role.",

        'creative_minority': f"Priority: Add creative problem-solver with Creative > 0.7 (gap: {gap_size:.1%}). Will bring innovation and novel threat detection to team.",

        'high_stress_resilience': f"Priority: Hire candidates with proven high-pressure performance (Stress_Res > 0.7, gap: {gap_size:.1%}). Consider former military, first responders, or high-stress roles.",

        # ... (more recommendations)
    }

    return recommendations.get(criterion, f"Address gap in {criterion} ({gap_size:.1%})")
```

**Output Schema:**
```json
{
  "team_id": "TEAM-SOC-001",
  "team_type": "SOC_Team",
  "gaps_identified": [
    {
      "criterion": "creative_minority",
      "ideal": 0.20,
      "actual": 0.0,
      "gap_size": 0.20,
      "priority": 1.0,
      "recommendation": "Priority: Add creative problem-solver with Creative > 0.7 (gap: 20.0%). Will bring innovation and novel threat detection to team."
    },
    {
      "criterion": "moderate_openness",
      "ideal": 0.60,
      "actual": 0.43,
      "gap_size": 0.17,
      "priority": 0.28,
      "recommendation": "Priority: Hire individuals with Openness in [0.4, 0.7] (gap: 17.0%). Balance routine work with pattern recognition."
    },
    {
      "criterion": "low_neuroticism",
      "ideal": 0.80,
      "actual": 0.71,
      "gap_size": 0.09,
      "priority": 0.11,
      "recommendation": "Priority: Hire emotionally stable individuals with Neuroticism < 0.3 (gap: 9.0%). Stress resilience critical for SOC role."
    }
  ],
  "summary": {
    "total_gaps": 3,
    "highest_priority": "creative_minority",
    "next_hire_profile": "Threat hunter or senior SOC analyst with high Openness (>0.7) and Creative (>0.7) to bring innovation to team"
  }
}
```

---

### Agent 7 Implementation: Optimal Hire Recommender

**Greedy Hiring Algorithm:**
```python
def rank_candidates(candidates, team, role, team_type):
    """
    Rank candidates by total fit score and recommend hiring decisions.
    """
    candidate_scores = []

    for candidate in candidates:
        # Calculate fit scores
        fit_results = calculate_total_fit(
            person_vector=candidate['personality_vector'],
            role=role,
            team_members=team
        )

        # Compute gap-filling contribution
        gaps = identify_personality_gaps(team, team_type)
        gap_filling_bonus = compute_gap_filling_bonus(candidate, gaps)

        # Adjusted score
        adjusted_score = fit_results['total_fit'] + 0.1 * gap_filling_bonus  # 10% bonus for filling gaps

        candidate_scores.append({
            'candidate_id': candidate['person_id'],
            'total_fit': fit_results['total_fit'],
            'function_fit': fit_results['function_fit'],
            'team_fit': fit_results['team_fit'],
            'gap_filling_bonus': gap_filling_bonus,
            'adjusted_score': adjusted_score,
            'recommendation': make_hire_recommendation(adjusted_score, fit_results, candidate)
        })

    # Sort by adjusted score
    candidate_scores.sort(key=lambda x: x['adjusted_score'], reverse=True)

    return candidate_scores

def compute_gap_filling_bonus(candidate, gaps):
    """
    Compute bonus score if candidate fills priority gaps.
    """
    bonus = 0.0
    vector = candidate['personality_vector']

    for gap in gaps:
        if gap['criterion'] == 'creative_minority' and vector[9] > 0.7:  # Creative > 0.7
            bonus += gap['priority'] * 0.5  # 50% of priority as bonus

        elif gap['criterion'] == 'low_neuroticism' and vector[4] < 0.3:  # N < 0.3
            bonus += gap['priority'] * 0.4

        elif gap['criterion'] == 'high_conscientiousness' and vector[1] > 0.7:  # C > 0.7
            bonus += gap['priority'] * 0.3

        # ... (more gap criteria)

    return min(bonus, 0.3)  # Cap bonus at 0.3 (don't let gaps dominate)

def make_hire_recommendation(score, fit_results, candidate):
    """
    Generate hiring recommendation with rationale.
    """
    if score > 0.75:
        return {
            'decision': 'STRONG HIRE',
            'rationale': f"Excellent fit (score: {score:.3f}). Candidate aligns well with role requirements and team dynamics. Recommend fast-track.",
            'priority': 'High'
        }
    elif score > 0.60:
        return {
            'decision': 'HIRE',
            'rationale': f"Good fit (score: {score:.3f}). Candidate meets requirements. Recommend proceeding with offer.",
            'priority': 'Medium'
        }
    elif score > 0.45:
        return {
            'decision': 'MAYBE',
            'rationale': f"Moderate fit (score: {score:.3f}). Interview further to assess culture fit and technical depth before decision.",
            'priority': 'Low'
        }
    else:
        return {
            'decision': 'DO NOT HIRE',
            'rationale': f"Poor fit (score: {score:.3f}). Personality mismatch with role or team. High risk of burnout or conflict.",
            'priority': 'None'
        }
```

**Output Schema:**
```json
{
  "role": "SOC_Analyst",
  "team_id": "TEAM-SOC-001",
  "candidate_pool_size": 15,
  "ranked_candidates": [
    {
      "rank": 1,
      "candidate_id": "CAND-2025-042",
      "total_fit": 0.895,
      "function_fit": 0.982,
      "team_fit": 0.766,
      "gap_filling_bonus": 0.0,
      "adjusted_score": 0.895,
      "recommendation": {
        "decision": "STRONG HIRE",
        "rationale": "Excellent fit (score: 0.895). Candidate aligns well with role requirements and team dynamics. Recommend fast-track.",
        "priority": "High"
      }
    },
    {
      "rank": 2,
      "candidate_id": "CAND-2025-038",
      "total_fit": 0.812,
      "function_fit": 0.891,
      "team_fit": 0.698,
      "gap_filling_bonus": 0.15,
      "adjusted_score": 0.827,
      "recommendation": {
        "decision": "STRONG HIRE",
        "rationale": "Excellent fit with gap-filling bonus. Candidate brings high Openness (0.82) to fill creative minority gap. Dual benefit: good SOC analyst + innovation contributor.",
        "priority": "High"
      }
    },
    ...
  ],
  "summary": {
    "strong_hires": 3,
    "hires": 5,
    "maybes": 4,
    "do_not_hire": 3,
    "top_recommendation": "CAND-2025-042 (score: 0.895) followed by CAND-2025-038 (adjusted score: 0.827 with gap-filling bonus)"
  }
}
```

---

## Execution Workflow

### Phase 1: Assessment Administration (Week 1)

**Activities:**
- Administer psychometric assessments to candidates and existing team
- Big Five (NEO-PI-R or BFI-2): ~45 min
- Dark Triad (SD3): ~10 min
- Cognitive Styles (CSI): ~15 min
- Behavioral questionnaire: ~10 min
- Total: ~80 minutes per person

**Agent Actions:**
- Agent 1: Score all assessments, create personality vectors
- Validate assessment completion and quality

---

### Phase 2: Team Analysis (Week 1-2)

**Parallel Agent Execution:**

**Agent 2 (Team Centroid Calculator):**
- Compute team centroids for all teams
- Calculate covariance matrices
- Output: Team aggregate statistics

**Agent 3 (Diversity Index Computer):**
- Compute diversity indices (Euclidean, determinant)
- Generate personality space coverage maps
- Output: Diversity metrics

**Agent 5 (Gap Identifier):**
- Compare actual vs ideal coverage profiles
- Prioritize gaps by severity
- Output: Gap analysis reports

**Agent 6 (Conflict Predictor):**
- Compute pairwise conflict risks
- Identify high-risk pairs
- Output: Conflict risk matrix

---

### Phase 3: Candidate Evaluation (Week 2)

**For Each Candidate:**

**Agent 1:** Score assessments → personality vector

**Agent 4:** Calculate fit scores:
- Function fit (candidate vs role ideal)
- Team fit (candidate vs team dynamics)
- Total fit (weighted combination)

**Agent 5:** Assess gap-filling potential

**Agent 7:** Generate hiring recommendation

---

### Phase 4: Synthesis and Recommendations (Week 2-3)

**Agent 7 (Optimal Hire Recommender):**
- Rank all candidates by adjusted fit scores
- Generate hiring decision matrix
- Produce detailed rationale for each decision

**Agent 8 (Team Evolution Modeler):**
- Simulate team performance with different hiring scenarios
- Forecast team effectiveness over time
- Output: "What-if" analysis for hiring decisions

**Agent 9 (Neo4j Graph Builder):**
- Construct comprehensive personality graph
- Link people, teams, roles, conflicts, gaps
- Enable interactive exploration and queries

**Agent 10 (Quality Validator):**
- Validate mathematical rigor
- Check ethical compliance (Dark Triad usage, privacy, bias)
- Verify actionability of recommendations
- Output: Quality assurance report

---

### Phase 5: Reporting (Week 3)

**Executive Summary Generation:**
```markdown
# Team Fit Analysis Report: SOC Team Alpha

**Analysis Period:** 2025-11-01 to 2025-11-26
**Team:** TEAM-SOC-001 (7 members)
**Role:** SOC Analyst (3 openings)
**Candidate Pool:** 15 candidates

## Team Health Assessment

**Current Team Profile:**
- Centroid: High Conscientiousness (0.81), Low Neuroticism (0.27), Moderate Openness (0.42)
- Diversity: Low (D = 0.18) - Homogeneous team, good for consistency
- Conflict Risk: Low (avg 0.12) - Stable team dynamics
- Function Alignment: Strong (avg 0.87) - Team well-suited for SOC work

**Gaps Identified:**
1. **Creative Minority (Priority 1.0):** No team members with high Creativity (>0.7). Risk: May miss novel attack patterns.
2. **Moderate Openness (Priority 0.28):** Only 43% have balanced Openness. May need more pattern recognition capability.
3. **Low Neuroticism (Priority 0.11):** 71% meet threshold, target is 80%. Minor stress resilience gap.

## Hiring Recommendations

**Top 3 Candidates:**

1. **CAND-2025-042 (Score: 0.895)**
   - **Decision:** STRONG HIRE (Fast-track)
   - **Function Fit:** 0.982 (Near-perfect SOC analyst profile)
   - **Team Fit:** 0.766 (Seamless integration)
   - **Profile:** High C (0.82), Low N (0.22), Exceptional Attention (0.93)
   - **Notes:** Will maintain team's core strengths, but does not fill creativity gap

2. **CAND-2025-038 (Adjusted Score: 0.827)**
   - **Decision:** STRONG HIRE (Gap-filler)
   - **Function Fit:** 0.891 (Excellent SOC analyst)
   - **Team Fit:** 0.698 (Good integration)
   - **Gap-Filling Bonus:** +0.15 (High Openness 0.82, Creative 0.76)
   - **Profile:** High O (0.82), High C (0.79), Creative thinker
   - **Notes:** Dual benefit: strong SOC analyst + fills creativity gap. **Recommend hiring first to address priority gap.**

3. **CAND-2025-051 (Score: 0.768)**
   - **Decision:** HIRE
   - **Function Fit:** 0.852
   - **Team Fit:** 0.642
   - **Profile:** Very High C (0.91), Ultra-High Attention (0.98), Low N (0.18)
   - **Notes:** Exceptional detail-orientation, will excel at thorough investigations

**Hiring Strategy:**
- **Immediate:** Offer to CAND-2025-038 (fills creativity gap + strong analyst)
- **Next:** Offer to CAND-2025-042 (maintains team excellence)
- **Third Position:** Offer to CAND-2025-051 (forensic/deep-dive specialist)

**Expected Team Impact:**
- Team diversity will increase from 0.18 → 0.24 (+33%)
- Creativity coverage: 0% → 10% (1 of 10 members)
- Avg function fit: 0.87 → 0.89
- Conflict risk: 0.12 → 0.14 (slight increase, acceptable)

## Long-Term Recommendations

1. **Succession Planning:** Identify high-performers for promotion to SOC lead, threat hunter roles
2. **Training:** Provide creative thinking workshops to existing team (partial gap mitigation)
3. **Next Hiring Cycle:** Continue prioritizing diversity in Openness and Creative thinking
4. **Team Dynamics:** Monitor CAND-2025-038 integration (higher Openness may require adjustment period)
```

---

## Validation & Testing

### Synthetic Test Cases

**Test Case 1: Perfect Fit Candidate**
- Input: Candidate with personality vector identical to role ideal
- Expected: F_function = 1.0, F_total > 0.9
- Validation: Ensures algorithm recognizes ideal candidates

**Test Case 2: Poor Fit Candidate (High Neuroticism for SOC)**
- Input: Candidate with N = 0.85 (very high stress sensitivity)
- Expected: F_function < 0.3, recommendation = "Do Not Hire"
- Validation: Ensures red flags are detected

**Test Case 3: Gap-Filling Candidate**
- Input: Homogeneous team + candidate with orthogonal personality
- Expected: High gap_filling bonus, increased team diversity
- Validation: Ensures diversity is rewarded

**Test Case 4: Conflict Risk Detection**
- Input: Two candidates with high Dark Triad scores
- Expected: Elevated conflict_risk (>0.3)
- Validation: Ensures personality clashes are predicted

---

## Performance Metrics

| Agent | Processing Time | Accuracy Target | Output Volume |
|-------|----------------|-----------------|---------------|
| Agent 1 (Profiler) | <5 min/person | >95% scoring accuracy | 1 vector per person |
| Agent 2 (Centroid) | <1 min/team | 100% numerical accuracy | 1 centroid per team |
| Agent 3 (Diversity) | <2 min/team | >95% consistency | 2 indices per team |
| Agent 4 (Fit Score) | <30 sec/candidate | >90% predictive validity | 3 scores per candidate |
| Agent 5 (Gap Identifier) | <3 min/team | >85% gap detection | ~5-10 gaps per team |
| Agent 6 (Conflict) | <5 min/team | >80% conflict prediction | n×(n-1)/2 pairs |
| Agent 7 (Hire Recommender) | <10 min/pool | >85% hire success rate | Ranked list |
| Agent 8 (Evolution) | <15 min/scenario | >75% forecast accuracy | Simulation results |
| Agent 9 (Neo4j) | <10 min | 100% schema compliance | Full graph |
| Agent 10 (Validator) | <5 min | 100% coverage | Quality report |

**Total Execution Time:** <1 hour for typical hiring scenario (15 candidates, 1 team)

---

## Deployment Instructions

### Prerequisites

```bash
# Python environment
python3.9+
pip install numpy scipy pandas scikit-learn neo4j-driver

# Psychometric scoring libraries
pip install personality-assessments  # Hypothetical package with NEO-PI-R, SD3 scoring

# Neo4j database
neo4j-community-5.x or neo4j-aura
```

### Configuration

```yaml
# config.yaml
team_fit_calculus:
  # Fit score weights
  weights:
    function_fit: 0.6
    team_fit: 0.4
    alignment: 0.4
    gap_filling: 0.4
    conflict: 0.2

  # Conflict risk parameters
  conflict_weights:
    neuroticism: 0.3
    agreeableness: 0.3
    extraversion: 0.2
    dark_triad: 0.2

  # Decision thresholds
  thresholds:
    strong_hire: 0.75
    hire: 0.60
    maybe: 0.45
    do_not_hire: 0.45

  # Ethical safeguards
  dark_triad_max: 0.80  # Maximum acceptable percentile
  diversity_min: 0.15   # Minimum team diversity (prevent homogeneity)

  # Neo4j connection
  neo4j:
    uri: "bolt://localhost:7687"
    user: "neo4j"
    password: "<secure_password>"
    database: "team_fit"
```

### Execution

```bash
# Run complete team fit analysis
python taskmaster_team_fit_calculus.py \
  --config config.yaml \
  --team-data /path/to/team_data.json \
  --candidate-data /path/to/candidates.json \
  --output-dir /path/to/results \
  --neo4j-import

# Run specific agent only
python taskmaster_team_fit_calculus.py \
  --agent fit_score_calculator \
  --input candidate_001.json \
  --output fit_scores.json

# Generate hiring report
python generate_hiring_report.py \
  --neo4j-uri bolt://localhost:7687 \
  --format [markdown|pdf|html] \
  --output hiring_report.pdf
```

---

## Ethical Oversight

### Review Checklist

- [ ] **Dark Triad Usage:** All scores ≤ 80th percentile? Oversight plan for elevated scores?
- [ ] **Diversity:** Diversity explicitly rewarded in objective function?
- [ ] **Protected Classes:** No correlation between personality requirements and protected characteristics?
- [ ] **Transparency:** Candidates informed about assessment use?
- [ ] **Feedback:** Candidates receive assessment results?
- [ ] **Privacy:** Data retention policy compliant (≤1 year post-hiring decision)?
- [ ] **Voluntary:** Assessment participation optional (not mandatory)?
- [ ] **Validation:** Correlation between fit scores and actual performance tracked?
- [ ] **Bias Audit:** Regular audit for disparate impact on demographic groups?

---

**End of TASKMASTER: Team Fit Calculus System v1.0**

*For theoretical foundation, see README.md*
*For data source specifications, see DATA_SOURCES.md*
