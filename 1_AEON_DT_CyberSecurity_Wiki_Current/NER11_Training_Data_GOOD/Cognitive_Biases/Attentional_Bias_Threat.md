# Attentional Bias Toward Threat - Cybersecurity Training

## Cognitive Bias Classification
- **Category:** Attention/Perception Biases
- **Type:** Threat-Related Selective Attention
- **Severity:** MEDIUM-HIGH - Can lead to hypervigilance, burnout, and false positive overload
- **Prevalence:** Very Common in security professionals (70-85%)

## Definition
**Attentional Bias Toward Threat** is the tendency to preferentially allocate attention to threatening, negative, or danger-related stimuli in the environment, even when such stimuli are not objectively more important or probable than neutral stimuli. This bias causes threat-related information to capture and hold attention disproportionately.

## Psychological Mechanism

### Core Cognitive Process
1. **Threat Detection Priority**: Evolutionary advantage to rapidly detect danger
2. **Automatic Attention Capture**: Threatening stimuli processed pre-attentively, automatically drawing focus
3. **Difficulty Disengaging**: Once attention locked on threat, hard to shift to other information
4. **Maintenance of Focus**: Threat maintains attention longer than neutral stimuli

### Neural Basis
- **Amygdala**: Rapid threat detection, emotional salience tagging
- **Anterior Cingulate Cortex**: Conflict monitoring, threat assessment
- **Prefrontal Cortex**: Attentional control, difficulty overriding amygdala-driven attention
- **Vigilance Network**: Sustained attention to potential threats in environment

### Evolutionary Context
- **Survival Value**: Better to detect threat that doesn't exist (false positive) than miss real threat (false negative)
- **Asymmetric Cost**: Cost of missed threat historically greater than cost of false alarm
- **Modern Mismatch**: Evolutionary environment had rare threats; modern security has constant threat information

### Individual Differences
- **Trait Anxiety**: Higher anxiety associated with stronger attentional bias toward threat
- **Professional Role**: Security professionals develop occupational attentional bias
- **PTSD and Trauma**: Prior negative experiences strengthen threat attention
- **Cultural Factors**: Security culture amplifies threat-focused attention

## Cybersecurity Manifestations

### 1. Security Operations Center (SOC) Hypervigilance

#### Threat-Centric Attention Allocation
- **Scenario**: SOC analyst allocates 90% attention to potential threats, 10% to all other information
- **Mechanism**: Threat alerts automatically capture attention regardless of probability or severity
- **Consequence**: Non-threat operational issues ignored, productivity problems unaddressed
- **Example**: Critical system performance degradation missed while investigating low-confidence threats

#### False Positive Bias
- **Scenario**: Analyst interprets ambiguous events as malicious by default
- **Mechanism**: Threat-related interpretation preferred when evidence ambiguous
- **Consequence**: High false positive rate, wasted investigation time, alert fatigue
- **Statistics**: Threat-biased analysts generate 40-60% more false positives than calibrated analysts

#### Minor Anomaly Catastrophization
- **Scenario**: Minor security anomaly interpreted as major breach indicator
- **Mechanism**: Attention magnifies threat significance, minor issues feel catastrophic
- **Consequence**: Excessive escalation, leadership alarm fatigue, "boy who cried wolf" effect
- **Organizational Impact**: Leaders discount security warnings due to frequent false alarms

#### Difficulty Disengaging from Resolved Alerts
- **Scenario**: Analyst continues investigating resolved alert, unable to move on
- **Mechanism**: Threat-captured attention resists disengagement even after resolution
- **Consequence**: Backlog accumulation, unexamined new alerts, delayed detection
- **Cognitive Cost**: Mental effort required to disengage from threat >> effort to detect threat

### 2. Risk Assessment Distortions

#### Threat Overestimation
- **Scenario**: Security team estimates breach probability at 80% when actuarial data shows 8%
- **Mechanism**: Attention bias toward threats makes them appear more probable than reality
- **Consequence**: Excessive security spending, opportunity cost of over-investment
- **Economic Impact**: Security budgets 2-3x appropriate level in threat-biased organizations

#### Worst-Case Scenario Fixation
- **Scenario**: Risk analysis focuses exclusively on catastrophic outcomes
- **Mechanism**: Catastrophic scenarios capture attention, moderate risks ignored
- **Consequence**: Risk mitigation strategies optimized for unlikely worst-case
- **Balance Lost**: Practical risks causing frequent harm receive insufficient attention

#### Black Swan Obsession
- **Scenario**: Security planning dominated by concern about unprecedented novel attacks
- **Mechanism**: Novel threats more attention-grabbing than common known threats
- **Consequence**: Under-protection against common threats, over-preparation for rare events
- **Reality: 85-90% of successful attacks use well-known techniques, not novel methods

#### Negative News Amplification
- **Scenario**: Security team absorbs every breach report, believes all are relevant to organization
- **Mechanism**: Threat-related news captures attention disproportionately
- **Consequence**: Continuous crisis mentality, burnout, inability to prioritize
- **Media Effect**: Infosec media business model amplifies threats, feeds attentional bias

### 3. Incident Response Challenges

#### Threat Attribution Bias
- **Scenario**: Ambiguous incident evidence preferentially interpreted as malicious rather than accidental
- **Mechanism**: Threat-focused attention seeks threat explanations over benign alternatives
- **Consequence**: Normal system failures investigated as security incidents
- **Resource Waste**: 30-50% of incident investigations determine non-malicious cause

#### Scope Expansion Tendency
- **Scenario**: IR team continuously expands investigation scope looking for additional threats
- **Mechanism**: Threat attention bias resists declaring "all clear," keeps searching
- **Consequence**: Incidents never conclusively closed, resources trapped in investigation loops
- **Closure Difficulty**: Psychological difficulty declaring "no further threats found"

#### Paranoia Spiral
- **Scenario**: Finding one threat indicator leads to belief that "everything is compromised"
- **Mechanism**: Initial threat detection primes attention for more threats
- **Consequence**: Investigation scope becomes organization-wide without justification
- **Example**: Single compromised endpoint leads to full network forensics despite no lateral movement evidence

#### Post-Incident Hyper-Awareness
- **Scenario**: After incident resolution, team sees threats in all subsequent activity
- **Mechanism**: Recent threat experience sensitizes attention to threat stimuli
- **Consequence**: False positive surge post-incident, investigation overload
- **Duration**: Heightened threat attention persists 4-8 weeks post-incident

### 4. Security Tool Development and Configuration

#### Detection Rule Sensitivity Bias
- **Scenario**: Detection rules tuned to maximize threat detection regardless of false positive rate
- **Mechanism**: Rule developers focused on threat detection, less attentive to FP impact
- **Consequence**: Unsustainably high alert volume, SOC overwhelmed
- **Tuning Challenge**: Difficult to balance detection vs precision when threat-focused

#### Logging Everything Syndrome
- **Scenario**: Organization logs every possible event "in case it's needed for investigation"
- **Mechanism**: Threat attention creates "can't have too much data" mindset
- **Consequence**: Storage costs, performance impacts, analysis paralysis
- **Data Reality**: 95%+ of collected logs never examined

#### Security Control Maximalism
- **Scenario**: Organization deploys every available security control regardless of relevance
- **Mechanism**: Each control addresses potential threat, attention makes all seem necessary
- **Consequence**: Complex fragile security architecture, operational friction, shadow IT
- **Usability: Excessive controls drive users to workarounds, reducing actual security

#### Alert Threshold Paranoia
- **Scenario**: Detection thresholds set extremely low to "catch everything"
- **Mechanism**: Threat attention overweights false negative risk, underweights false positive cost
- **Consequence**: Alert storms, analyst burnout, critical alerts lost in noise
- **Optimization**: Must consciously resist threat bias to achieve effective thresholds

### 5. Communication and Reporting

#### Threat-Centric Reporting
- **Scenario**: Security reports to leadership emphasize threats, downplay successful defenses
- **Mechanism**: Attention naturally drawn to threats when constructing narrative
- **Consequence**: Leadership perceives security program as failing despite success
- **Funding Impact**: Paradoxically, successful security may lose funding due to threat-focused reporting

#### Vendor FUD Susceptibility
- **Scenario**: Security team falls for vendor "Fear, Uncertainty, Doubt" marketing
- **Mechanism**: Threat attention makes FUD compelling despite lack of evidence
- **Consequence**: Unnecessary tool purchases, budget waste, vendor lock-in
- **Industry Problem**: Vendor marketing deliberately exploits threat attention bias

#### Crisis Communication Defaults
- **Scenario**: All security communications framed as urgent threats
- **Mechanism**: Threat attention makes neutral tone feel inappropriately casual
- **Consequence**: Communication fatigue, important warnings dismissed
- **Calibration: Must consciously vary communication urgency to preserve impact

#### Breach Disclosure Amplification
- **Scenario**: Organization's breach disclosure emphasizes threat sophistication over containment success
- **Mechanism**: Threat aspects of incident capture attention during disclosure writing
- **Consequence**: Reputational damage worse than justified, customer overreaction
- **Strategy: Requires conscious effort to balance threat disclosure with response effectiveness

### 6. Career and Professional Development

#### Threat Intelligence Career Trap
- **Scenario**: Security professionals specialize in threat intelligence, lose broader security perspective
- **Mechanism**: Threat-focused role amplifies existing attention bias
- **Consequence**: Career limited to threat-focused roles, difficulty transitioning to security engineering
- **Balance: Must consciously develop non-threat-focused skills

#### Certification Bias Toward Offensive Security
- **Scenario**: Security professionals pursue offensive security certs (pentesting, red team) over defensive
- **Mechanism**: Offensive security culturally associated with threats, captures attention
- **Consequence**: Industry shortage of defensive security expertise
- **Market Reality**: 80% of security jobs are defensive, but offensive training more popular

#### Conference and Training Selection
- **Scenario**: Professionals attend threat-focused conferences, ignore security architecture/engineering
- **Mechanism**: "Advanced Persistent Threats" conference more attention-grabbing than "Secure Configuration Management"
- **Consequence**: Professional development overweights threats vs foundational security
- **Skill Gap**: Threat knowledge without engineering capability limits effectiveness

#### News Consumption Patterns
- **Scenario**: Security professionals compulsively consume breach reports and threat news
- **Mechanism**: Threat-related news more attention-grabbing than security success stories
- **Consequence**: Distorted view of threat landscape, burnout from negative information diet
- **Mental Health**: Constant threat information consumption contributes to anxiety and burnout

## Alert Fatigue Connection

### Attention Capture Without Significance
- **Mechanism**: All alerts capture threat-focused attention regardless of actual risk
- **Effect**: Cognitive resources depleted by low-significance threat stimuli
- **Consequence**: High-significance threats receive insufficient attention despite capturing initial focus
- **Paradox: Threat attention bias contributes to missing genuine threats

### Disengagement Difficulty
- **Mechanism**: Threat attention resists disengagement, even after alert resolution
- **Effect**: Analysts spend excessive time on resolved alerts
- **Consequence**: Backlog grows as new alerts arrive faster than disengagement from old ones
- **Management: Requires conscious disengagement protocols to overcome natural tendency

### Hypervigilance Exhaustion
- **Mechanism**: Continuous threat-focused attention is cognitively demanding
- **Effect**: Mental fatigue from sustained hypervigilance
- **Consequence**: Attention capacity depleted, paradoxically reducing threat detection
- **Burnout: Threat attention bias is major contributor to SOC analyst burnout

### False Positive Interpretation Bias
- **Mechanism**: Ambiguous alerts interpreted as threats due to attention bias
- **Effect**: False positive rate higher than tool design specifications
- **Consequence**: Alert volume amplified by interpretation bias
- **Compounding: Tool FP rate multiplied by human interpretation bias

## Insider Threat Detection Implications

### Hypervigilance Toward Employees
- **Scenario**: Security team interprets normal employee behavior as threatening
- **Mechanism**: Insider threat awareness creates attentional bias toward employee actions
- **Consequence**: Hostile surveillance culture, employee privacy violations, false accusations
- **Legal Risk**: Excessive monitoring and false accusations create liability

### Difficulty Disengaging from Insider Suspicions
- **Scenario**: Once employee flagged as potential insider threat, impossible to clear suspicion
- **Mechanism**: Threat attention makes disconfirming evidence psychologically invisible
- **Consequence**: Innocent employees subjected to ongoing investigation
- **Career Damage**: Suspicion follows employee even after exoneration

### Privileged User Paranoia
- **Scenario**: All privileged user activity viewed with suspicion
- **Mechanism**: Privileged access combined with insider threat attention creates constant suspicion
- **Consequence**: Adversarial relationship between security and IT administration
- **Operational Friction**: Security monitoring impedes legitimate administrative work

### Behavioral Analytics Bias
- **Scenario**: UEBA anomaly alerts interpreted as malicious by default
- **Mechanism**: Threat attention predisposes toward malicious interpretation of behavioral anomalies
- **Consequence**: High false positive rate, investigation overload
- **Calibration: Must consciously consider benign explanations for anomalies

## Training and Mitigation Strategies

### 1. Attention Balance Training

#### Neutral Information Practice
- **Method**: Training exercises requiring attention to neutral and positive security information
- **Application**: Review reports of security successes, not just breaches
- **Goal**: Develop capacity to attend to non-threatening security information
- **Benefit: 20-30% reduction in false positive rate after attention balance training

#### Positive Security Framing
- **Practice**: Consciously identify successful defenses and positive outcomes
- **Example**: "This week we successfully detected and blocked 47 attacks"
- **Mechanism**: Trains attention toward positive security outcomes
- **Culture: Builds more sustainable security culture than pure threat focus

#### Cognitive Reappraisal Training
- **Method**: Practice reinterpreting ambiguous events in non-threatening ways
- **Exercise**: Given ambiguous log entry, generate benign explanations
- **Benefit: Reduces automatic threat interpretation of ambiguous information
- **Application**: Real-time reappraisal during alert investigation

#### Attention Flexibility Drills
- **Exercise**: Practice rapidly shifting attention between threat and non-threat information
- **Goal**: Improve ability to disengage from threats when appropriate
- **Measurement**: Track time to disengage from resolved alerts
- **Improvement: 30-50% faster disengagement after 4-6 weeks training

### 2. Risk Calibration

#### Statistical Risk Literacy
- **Training**: Teach accurate interpretation of threat probabilities
- **Content**: Base rate neglect, denominator blindness, probability vs possibility
- **Application**: Compare subjective threat probability estimates to actuarial data
- **Outcome**: 40-60% improvement in risk estimation accuracy

#### Comparative Risk Analysis
- **Method**: Compare security risks to other business risks with known probabilities
- **Benefit: Provides perspective on absolute and relative security risk
- **Example**: "This threat has 1% annual probability; major product failure has 8% probability"
- **Calibration: Prevents treating all possible threats as high-probability

#### Historical Base Rate Review
- **Practice**: Regular review of actual incident rates in organization and industry
- **Data: "Last year we had 3 incidents from 10,000 alerts investigated"
- **Calibration: Grounds threat perception in organizational reality
- **Frequency: Quarterly base rate review sessions recommended

#### Scenario-Based Probability Training
- **Method**: Present scenarios requiring probability estimates, provide feedback
- **Learning**: Repeated practice with feedback improves calibration
- **Application**: Use real organizational incident data for scenarios
- **Measurement**: Track calibration improvement over time

### 3. Mindfulness and Meta-Awareness

#### Threat Attention Meta-Awareness
- **Practice**: Notice when attention captured by threat, consciously evaluate if appropriate
- **Self-Monitoring**: "My attention is locked on this threat - is it justified?"
- **Intervention**: Conscious disengagement when threat attention disproportionate
- **Evidence: Mindfulness training reduces threat attention bias by 25-40%

#### Body-Based Awareness
- **Recognition**: Threat attention accompanied by physiological arousal (elevated heart rate, muscle tension)
- **Practice**: Notice physical signs of threat response, use as meta-awareness cue
- **Intervention**: Physiological calming techniques to reduce threat attention
- **Example**: Deep breathing before investigating alerts to reduce threat bias

#### Anxiety Management Training
- **Recognition**: Trait anxiety amplifies threat attention bias
- **Intervention**: Clinical interventions for anxiety (CBT, exposure therapy, medication)
- **Application**: Occupational health programs for security professionals
- **Benefit: Reducing underlying anxiety reduces threat attention bias

#### Work-Life Boundary Maintenance
- **Practice**: Strict boundaries between work (threat-focused) and personal time
- **Benefit: Prevents threat attention from dominating entire life
- **Mental Health**: Critical for preventing burnout and maintaining perspective
- **Policy: Organizational support for disconnection from security information

### 4. Organizational and Process Interventions

#### Positive Security Metrics
- **Approach**: Track and report successful defenses, not just detected threats
- **Metrics**: "Attacks blocked," "vulnerabilities remediated," "% assets compliant"
- **Benefit: Directs attention toward security successes
- **Leadership: Management attention follows measured metrics

#### Role Rotation
- **Practice**: Rotate security professionals through threat and non-threat roles
- **Benefit: Develops balanced attention and prevents threat obsession
- **Example**: Rotate between SOC analysis and security engineering every 6-12 months
- **Career Development**: Builds broader skills, reduces burnout

#### Neutral Case Review
- **Practice**: Regular review of correctly-dismissed alerts and benign anomalies
- **Learning**: Trains attention toward neutral interpretations
- **Benefit: Improves ability to recognize false positives
- **Implementation**: Weekly review of 10 resolved false positive alerts

#### Structured Disengagement Protocols
- **Policy**: Formal procedures for closing alerts and investigations
- **Purpose**: Overcomes natural difficulty disengaging from threats
- **Content**: Specific criteria for declaring "threat resolved"
- **Enforcement: Managerial oversight of investigation closure

### 5. Communication and Reporting Standards

#### Balanced Reporting Requirements
- **Standard**: Security reports must include successes, not just threats
- **Ratio: Target 50/50 balance between threat information and positive security outcomes
- **Leadership: Presents realistic picture of security posture
- **Morale: Balanced reporting supports team morale and leadership confidence

#### Threat Communication Guidelines
- **Policy**: Calibrate communication urgency to actual risk
- **Levels**: Critical, High, Medium, Low with explicit criteria
- **Discipline: Resist threat attention bias toward over-stating urgency
- **Credibility: Preserves impact of genuinely critical communications

#### Vendor Claim Skepticism
- **Training**: Teach critical evaluation of vendor threat claims
- **Questions**: "What's the actual prevalence? How does this compare to other risks?"
- **Policy: Require independent validation of vendor threat assertions
- **Budget Protection**: Reduces unnecessary spending driven by FUD

### 6. Technology-Assisted Debiasing

#### Objective Risk Scoring
- **Technology**: Algorithmic risk scores based on statistical models
- **Benefit: Compensates for human threat attention bias
- **Implementation**: Present objective risk score prominently alongside subjective assessment
- **Calibration: Over time, human assessments converge toward objective scores

#### False Positive Rate Tracking
- **System**: Automatic tracking of analyst false positive rates
- **Feedback**: Individual feedback on FP rate compared to team baseline
- **Awareness**: Makes threat interpretation bias visible
- **Improvement: FP rates decrease 20-40% when analysts see their own bias metrics

#### Attention Distribution Monitoring
- **Technology**: Track how analysts allocate time across alert types/priorities
- **Analysis**: Identify disproportionate attention to threats vs other work
- **Intervention**: Prompt analysts when attention distribution becomes unbalanced
- **Example**: "You've spent 90% of time on low-priority alerts today"

#### Forced Neutral Consideration
- **Tool Design**: Analyst must document benign explanation before concluding threat
- **Mechanism**: Slows threat interpretation, forces consideration of alternatives
- **Effect: 30-50% reduction in false positive conclusions
- **Implementation: Built into SIEM investigation workflow

## Detection and Debiasing

### Personal Recognition Strategies
- **Physical Cues**: Notice elevated arousal (heart rate, tension) indicating threat attention activated
- **Time Tracking**: Monitor how long focusing on single threat without progress
- **Question Assumptions**: "Am I seeing threats because they're there, or because I'm looking for them?"
- **Seek Disconfirmation**: Actively look for evidence that situation is NOT threatening

### Team-Based Mitigation
- **Diverse Roles**: Mix threat-focused and engineering-focused team members
- **Alternative Viewpoints**: Encourage team members to suggest benign explanations
- **Collective Calibration**: Team discussions about whether threat assessments balanced
- **Buddy Systems**: Partner high-threat-attention analysts with low-threat-attention analysts

### Organizational Interventions
- **Balanced Metrics**: Measure and report both threats and successful defenses
- **Role Diversity**: Ensure security team includes non-threat-focused roles
- **Cultural Calibration**: Leadership actively promotes balanced perspective
- **Support Programs**: Mental health resources for security professionals

## Research Evidence

### Key Studies
1. **Bar-Haim et al. (2007)**: Meta-analysis showing threat-related attentional bias across anxiety disorders
2. **Cisler & Koster (2010)**: Attentional bias involves both facilitated attention to threat and difficulty disengaging
3. **MacLeod et al. (2002)**: Attentional bias training can reduce anxiety and modify attention patterns
4. **Mogg & Bradley (1998)**: Threat attention bias stronger for anxiety-relevant threats

### Occupational Research
- **Healthcare: Doctors show attentional bias toward disease symptoms, overdiagnose
- **Law Enforcement**: Police officers show attentional bias toward threats, increasing use of force
- **Aviation: Pilot threat attention bias can cause misinterpretation of normal system alerts
- **Military: Combat veterans show persistent threat attention bias (PTSD symptom)

### Cybersecurity-Specific Findings
- **False Positive Rates**: Threat-anxious analysts generate 40-60% more false positives
- **Investigation Time**: High-threat-attention analysts spend 2-3x longer on resolved alerts
- **Burnout Correlation**: Stronger threat attention bias predicts earlier burnout (r = 0.65)
- **Risk Overestimation**: Security professionals overestimate breach probability by 5-10x

## Related Cognitive Biases

### Negativity Bias
- **Relationship**: General tendency to attend to negative information amplifies threat attention
- **Effect**: Threat attention is specific case of broader negativity bias
- **Combined: Both biases must be addressed for balanced attention

### Confirmation Bias
- **Relationship**: Threat attention provides initial hypothesis, confirmation bias sustains it
- **Mechanism**: Attention focuses on threats → seek confirmatory evidence → ignore disconfirming evidence
- **Cycle: Creates reinforcing loop maintaining threat interpretation

### Availability Heuristic
- **Relationship**: Attended threats become mentally available, judged as more probable
- **Effect**: Threat attention increases subjective probability estimates
- **Risk Assessment: Combined effect severely distorts risk perception

## Practical Exercises

### Exercise 1: Ambiguous Alert Interpretation
- **Setup**: Present ambiguous security alert
- **Task: Generate both threatening and benign explanations
- **Compare: Observe tendency to prefer threatening explanations
- **Practice: Deliberately develop benign explanations
- **Learning: Awareness of threat interpretation bias

### Exercise 2: Attention Tracking
- **Setup**: Monitor security environment for one shift
- **Measurement**: Track time allocation across threat vs non-threat activities
- **Analysis: Compare actual vs optimal attention distribution
- **Adjustment: Consciously rebalance attention in subsequent shifts

### Exercise 3: Positive Security Identification
- **Task: Review day's activities, identify successful defenses and positive outcomes
- **Challenge**: Most security professionals struggle to identify positives
- **Practice: Daily practice identifying and reporting successes
- **Outcome: Develops attention toward positive security information

### Exercise 4: Disengagement Training
- **Setup**: Investigate alert, then practice rapid disengagement upon resolution
- **Measurement: Track time from "resolved" to moving to next task
- **Goal: Reduce disengagement time by 50%
- **Benefit: Improves efficiency, reduces backlog accumulation

## Conclusion

Attentional bias toward threat is evolutionarily-rooted cognitive pattern that served survival purposes in ancestral environments but creates significant challenges in modern cybersecurity contexts. While some degree of threat sensitivity is necessary for security work, uncalibrated threat attention leads to:
- Hypervigilance and burnout
- False positive overload
- Distorted risk perception
- Inefficient resource allocation
- Hostile work culture

Effective management requires multi-layered approach:
1. **Individual Training**: Attention balance, cognitive reappraisal, mindfulness
2. **Process Design**: Structured protocols overcoming natural threat attention
3. **Organizational Culture**: Balanced metrics and positive security emphasis
4. **Technology Support**: Algorithmic debiasing and attention monitoring
5. **Mental Health**: Support for security professionals managing threat attention

The goal is not elimination of threat attention - which would be dangerous - but calibration to appropriate levels. Security professionals must maintain vigilance while avoiding the cognitive and emotional costs of excessive threat focus.

**Key Takeaway**: Threats naturally capture attention more than they deserve. Sustainable effective security requires conscious effort to maintain balanced attention, attending to security successes, engineering work, and non-threatening information alongside genuine threats.

---

**File Metadata:**
- **Bias Category:** Attention/Perception
- **Severity:** MEDIUM-HIGH
- **Target Audience:** SOC Analysts, Security Managers, Incident Responders, All Security Professionals
- **Training Duration:** 90-120 minutes
- **Prerequisites:** Basic understanding of psychology and anxiety
- **Assessment:** Attention distribution tracking, false positive rate measurement, risk calibration exercises
