# Case Study 2: Till Eulenspiegel (Anomaly Detection)

**Document ID**: CASE_STUDY_2_TILL_EULENSPIEGEL_ANOMALY
**Version**: 1.0 (Application)
**Date**: 2025-11-28
**Author**: AEON Research Division (Swarm 3 - The Conductors)
**Classification**: TOP SECRET // NOFORN // AEON EYES ONLY

---

## 1. The Scenario

A Chaos Engineering bot ("Till") is deployed to randomly restart services in Production. The SOC must distinguish between Till's "Pranks" and a real attack.

---

## 2. The Score Analysis

### 2.1 The Eulenspiegel Motif (The Prank)
*   **Context**: Till announces his presence.
*   **Key**: F Major (Playful).
*   **Instrumentation**:
    *   **Horn (Till)**: A rising, chromatic line. "Once upon a time..."

**Score Fragment**:
```csv
Beat,Time,Actor,Instrument,Pitch,Duration,Volume,Event,Lacan
1.0,12:00,TillBot,Horn,F4,0.5,mf,"Chaos Experiment Started",Imaginary (Play)
1.5,12:00,TillBot,Horn,A4,0.5,mf,"Target: Payment Service",Imaginary
2.0,12:00,TillBot,Horn,C5,0.5,mf,"Action: Restart",Imaginary
```

### 2.2 The Market Scene (The Disruption)
*   **Context**: The Payment Service restarts. Transactions fail. The "Market" (Users) is disrupted.
*   **Key**: D Minor (Chaos).
*   **Instrumentation**:
    *   **Woodwinds (Users)**: Chattering, confused.
    *   **Percussion (Errors)**: Clattering pots and pans (500 Errors).

**Score Fragment**:
```csv
Beat,Time,Actor,Instrument,Pitch,Duration,Volume,Event,Lacan
10.0,12:01,User_A,Flute,E5,0.25,f,"Transaction Failed!",Real (Gap)
10.25,12:01,User_B,Oboe,E5,0.25,f,"Cart Empty?",Real
10.5,12:01,Syslog,Snare,C4,0.1,ff,"HTTP 500",Symbolic (Error)
10.6,12:01,Syslog,Snare,C4,0.1,ff,"HTTP 500",Symbolic
```

### 2.3 The Judgment (The False Positive)
*   **Context**: The SOC sees the errors and declares an incident.
*   **Key**: F Minor (Judgment).
*   **Instrumentation**:
    *   **Trombone (SOC)**: Heavy, authoritative chords. "Death to the sinner!"

**Score Fragment**:
```csv
Beat,Time,Actor,Instrument,Pitch,Duration,Volume,Event,Lacan
20.0,12:05,SOC_Analyst,Trombone,F2,2.0,ff,"INCIDENT DECLARED",Symbolic (Law)
22.0,12:05,TillBot,Clarinet,D6,0.5,p,"It was just a prank!",Imaginary (Mockery)
```

---

## 3. Conclusion

The Calculus reveals that the "Timbre" of Till (Horn) is distinct from the "Timbre" of a real attacker (Synthesizer). By training the SOC to recognize the **Eulenspiegel Motif**, we reduce False Positives.
