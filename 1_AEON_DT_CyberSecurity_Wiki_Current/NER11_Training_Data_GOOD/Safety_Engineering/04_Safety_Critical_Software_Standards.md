# Safety-Critical Software Standards - Training Data

## DO-178C Avionics Software Certification

1. The [[ARCHITECTURE: DO-178C Software Level A Development]] using [[EQUIPMENT: Qualified Development Tools]] with [[PROTOCOL: Requirements-Based Testing Protocol]] provides [[MITIGATION: Catastrophic Failure Prevention]] against [[ATTACK_PATTERN: Untested Software Path Exploitation]] targeting [[VULNERABILITY: Incomplete Test Coverage]].

2. The [[ARCHITECTURE: Structural Coverage Analysis (DO-178C)]] using [[EQUIPMENT: Code Coverage Analyzer]] and [[PROTOCOL: MC/DC Coverage Protocol]] provides [[MITIGATION: Decision Coverage Verification]] against [[ATTACK_PATTERN: Unexercised Conditional Path Attack]] exploiting [[VULNERABILITY: Insufficient Branch Testing]].

3. The [[ARCHITECTURE: Software Configuration Management (DO-178C)]] using [[EQUIPMENT: Version Control with Audit Trail]] and [[PROTOCOL: Change Impact Analysis Protocol]] provides [[MITIGATION: Traceable Software Baseline]] against [[ATTACK_PATTERN: Unauthorized Code Modification]] targeting [[VULNERABILITY: Uncontrolled Software Changes]].

4. The [[ARCHITECTURE: Tool Qualification (DO-330)]] using [[EQUIPMENT: Qualified Code Generator]] with [[PROTOCOL: Tool Operational Requirements (TOR) Verification]] provides [[MITIGATION: Trusted Tool Output]] against [[ATTACK_PATTERN: Compiler Bug Exploitation]] exploiting [[VULNERABILITY: Unqualified Development Tool]].

5. The [[ARCHITECTURE: Model-Based Development with DO-331]] using [[EQUIPMENT: Qualified Simulink Toolchain]] and [[PROTOCOL: Model Coverage Analysis Protocol]] provides [[MITIGATION: High-Level Verification]] against [[ATTACK_PATTERN: Model-Code Inconsistency Exploitation]] targeting [[VULNERABILITY: Unverified Model-to-Code Translation]].

## IEC 61508 Functional Safety

6. The [[ARCHITECTURE: IEC 61508 Safety Lifecycle]] using [[EQUIPMENT: Lifecycle Management Tool]] with [[PROTOCOL: V-Model Verification and Validation]] provides [[MITIGATION: Systematic Safety Development]] against [[ATTACK_PATTERN: Safety Lifecycle Phase Skip]] exploiting [[VULNERABILITY: Ad-Hoc Safety Process]].

7. The [[ARCHITECTURE: Software Safety Integrity Level (SSIL) Allocation]] using [[EQUIPMENT: Hazard Analysis Tool]] and [[PROTOCOL: Risk Graph Methodology]] provides [[MITIGATION: Appropriate Safety Measures per Risk]] against [[ATTACK_PATTERN: Inadequate Safety Measures]] targeting [[VULNERABILITY: Incorrect SIL Assignment]].

8. The [[ARCHITECTURE: Semi-Formal Verification (IEC 61508)]] using [[EQUIPMENT: Design Assertion Tool]] with [[PROTOCOL: Structured Proof Technique]] provides [[MITIGATION: Design-Level Fault Detection]] against [[ATTACK_PATTERN: Undetected Design Flaw Exploitation]] exploiting [[VULNERABILITY: Informal Design Verification Only]].

9. The [[ARCHITECTURE: Defensive Programming (IEC 61508)]] using [[EQUIPMENT: Static Code Analyzer (MISRA C Checker)]] and [[PROTOCOL: Runtime Error Detection Protocol]] provides [[MITIGATION: Robust Software Design]] against [[ATTACK_PATTERN: Unexpected Input Exploitation]] targeting [[VULNERABILITY: Unvalidated Assumptions in Code]].

10. The [[ARCHITECTURE: Software Safety Assessment (IEC 61508 Part 3)]] using [[EQUIPMENT: Independent Safety Auditor]] with [[PROTOCOL: Compliance Checklist Verification]] provides [[MITIGATION: Third-Party Safety Validation]] against [[ATTACK_PATTERN: Self-Assessment Bias]] exploiting [[VULNERABILITY: Inadequate Independent Review]].

## ISO 26262 Automotive Functional Safety

11. The [[ARCHITECTURE: ISO 26262 Automotive Safety Lifecycle]] using [[EQUIPMENT: Requirements Management Database]] and [[PROTOCOL: Safety Requirement Traceability Protocol]] provides [[MITIGATION: Complete Safety Requirement Coverage]] against [[ATTACK_PATTERN: Missing Safety Requirement Exploitation]] targeting [[VULNERABILITY: Incomplete Safety Specification]].

12. The [[ARCHITECTURE: ASIL Decomposition Strategy]] using [[EQUIPMENT: Redundant ECUs with Independence]] and [[PROTOCOL: ASIL Decomposition Verification Protocol]] provides [[MITIGATION: Reduced Single-Component ASIL Rating]] against [[ATTACK_PATTERN: Single Point Failure in High-ASIL System]] exploiting [[VULNERABILITY: Undecomposed ASIL Assignment]].

13. The [[ARCHITECTURE: Dependent Failure Analysis (DFA)]] using [[EQUIPMENT: Failure Mode Correlation Tool]] with [[PROTOCOL: Common Cause Failure Analysis]] provides [[MITIGATION: Independence Verification of Redundant Channels]] against [[ATTACK_PATTERN: Common Mode Failure Exploitation]] targeting [[VULNERABILITY: Unanalyzed Dependent Failures]].

14. The [[ARCHITECTURE: Software Unit Testing (ISO 26262-6)]] using [[EQUIPMENT: Unit Test Framework (e.g., Google Test)]] and [[PROTOCOL: 100% Statement Coverage Requirement for ASIL D]] provides [[MITIGATION: Comprehensive Unit-Level Validation]] against [[ATTACK_PATTERN: Unit-Level Bug Exploitation]] exploiting [[VULNERABILITY: Insufficient Unit Test Coverage]].

15. The [[ARCHITECTURE: Software Integration Testing (ISO 26262-6)]] using [[EQUIPMENT: Hardware-Software Integration Test Bench]] with [[PROTOCOL: Back-to-Back Testing Protocol]] provides [[MITIGATION: Interface Defect Detection]] against [[ATTACK_PATTERN: Integration-Induced Failure]] targeting [[VULNERABILITY: Unvalidated Component Interactions]].

## IEC 62304 Medical Device Software

16. The [[ARCHITECTURE: IEC 62304 Software Safety Classification]] using [[EQUIPMENT: Hazard Analysis for Medical Devices]] and [[PROTOCOL: Risk-Based Class Assignment Protocol]] provides [[MITIGATION: Appropriate Development Rigor]] against [[ATTACK_PATTERN: Under-Classification Attack]] exploiting [[VULNERABILITY: Incorrect Safety Class Assignment]].

17. The [[ARCHITECTURE: Software Development Plan (IEC 62304 Clause 5.1)]] using [[EQUIPMENT: Development Process Documentation]] with [[PROTOCOL: Activity and Task Definition Protocol]] provides [[MITIGATION: Planned and Controlled Development]] against [[ATTACK_PATTERN: Ad-Hoc Development Vulnerability Injection]] targeting [[VULNERABILITY: Unstructured Development Process]].

18. The [[ARCHITECTURE: Software Risk Management (IEC 62304 Clause 7)]] using [[EQUIPMENT: Risk Management File]] and [[PROTOCOL: ISO 14971 Integration Protocol]] provides [[MITIGATION: Identified and Mitigated Software Risks]] against [[ATTACK_PATTERN: Unidentified Risk Exploitation]] exploiting [[VULNERABILITY: Inadequate Risk Analysis]].

19. The [[ARCHITECTURE: Software Problem Resolution (IEC 62304 Clause 9)]] using [[EQUIPMENT: Problem Tracking System]] with [[PROTOCOL: Root Cause Analysis Protocol]] provides [[MITIGATION: Systematic Defect Correction]] against [[ATTACK_PATTERN: Recurring Defect Pattern]] targeting [[VULNERABILITY: Superficial Bug Fixes Without Root Cause Analysis]].

20. The [[ARCHITECTURE: Software Maintenance (IEC 62304 Clause 6)]] using [[EQUIPMENT: Change Control Board]] and [[PROTOCOL: Regression Testing Protocol]] provides [[MITIGATION: Controlled Post-Release Modifications]] against [[ATTACK_PATTERN: Unvalidated Patch Injection]] exploiting [[VULNERABILITY: Uncontrolled Software Updates]].

## EN 50128 Railway Software

21. The [[ARCHITECTURE: EN 50128 Software Safety Integrity Level (SIL)]] using [[EQUIPMENT: Railway Hazard Analysis Tool]] and [[PROTOCOL: CENELEC SIL Allocation Protocol]] provides [[MITIGATION: Railway-Specific Safety Rigor]] against [[ATTACK_PATTERN: Signaling Failure Exploitation]] targeting [[VULNERABILITY: Inadequate Railway Safety Measures]].

22. The [[ARCHITECTURE: Diverse Programming (EN 50128 SIL 3/4)]] using [[EQUIPMENT: Independent Implementation Teams]] with [[PROTOCOL: Cross-Verification Protocol]] provides [[MITIGATION: Design Diversity Against Common Errors]] against [[ATTACK_PATTERN: Common Implementation Flaw]] exploiting [[VULNERABILITY: Single Implementation Path]].

23. The [[ARCHITECTURE: Formal Methods (EN 50128 Table A.3)]] using [[EQUIPMENT: Formal Specification Language (e.g., Z, VDM)]] and [[PROTOCOL: Formal Proof of Safety Properties]] provides [[MITIGATION: Mathematically Proven Correctness]] against [[ATTACK_PATTERN: Logical Design Flaw Exploitation]] targeting [[VULNERABILITY: Informal Specification Only]].

24. The [[ARCHITECTURE: Modular Approach (EN 50128 Clause 7.2)]] using [[EQUIPMENT: Strongly Typed Programming Language (Ada)]] with [[PROTOCOL: Interface Specification Protocol]] provides [[MITIGATION: Verified Module Boundaries]] against [[ATTACK_PATTERN: Interface Assumption Violation]] exploiting [[VULNERABILITY: Unclear Module Dependencies]].

25. The [[ARCHITECTURE: Software Validation (EN 50128 Clause 7.5)]] using [[EQUIPMENT: Independent Validation Team]] and [[PROTOCOL: Black-Box Testing Against SRS]] provides [[MITIGATION: Unbiased Requirements Verification]] against [[ATTACK_PATTERN: Validation Bias Attack]] targeting [[VULNERABILITY: Developer-Led Validation Only]].

## MISRA Coding Standards

26. The [[ARCHITECTURE: MISRA C:2012 Compliance]] using [[EQUIPMENT: Static Analysis Tool (e.g., PRQA QA·C)]] with [[PROTOCOL: Mandatory Rules Enforcement]] provides [[MITIGATION: Eliminated Undefined Behavior]] against [[ATTACK_PATTERN: Undefined Behavior Exploitation]] targeting [[VULNERABILITY: Non-Portable or Unsafe C Constructs]].

27. The [[ARCHITECTURE: MISRA C++ 2008 Compliance]] using [[EQUIPMENT: C++ Static Analyzer]] and [[PROTOCOL: Restricted Language Subset Protocol]] provides [[MITIGATION: Predictable Object-Oriented Code]] against [[ATTACK_PATTERN: C++ Feature Misuse Attack]] exploiting [[VULNERABILITY: Unsafe C++ Features in Safety Code]].

28. The [[ARCHITECTURE: MISRA Compliance Deviation Management]] using [[EQUIPMENT: Deviation Request System]] with [[PROTOCOL: Justification and Alternative Measure Protocol]] provides [[MITIGATION: Controlled Rule Exceptions]] against [[ATTACK_PATTERN: Blanket Rule Disablement]] targeting [[VULNERABILITY: Unjustified MISRA Non-Compliance]].

29. The [[ARCHITECTURE: MISRA Compliance Verification]] using [[EQUIPMENT: Multi-Tool Analysis Strategy]] and [[PROTOCOL: Tool Consensus Validation]] provides [[MITIGATION: High Confidence in Rule Checking]] against [[ATTACK_PATTERN: Static Analysis Tool Blind Spot]] exploiting [[VULNERABILITY: Single-Tool Analysis Limitations]].

30. The [[ARCHITECTURE: MISRA Guideline Implementation]] using [[EQUIPMENT: Enforced Coding Templates]] with [[PROTOCOL: Automated Guideline Check Protocol]] provides [[MITIGATION: Proactive Coding Standard Adherence]] against [[ATTACK_PATTERN: Gradual Standards Erosion]] targeting [[VULNERABILITY: Voluntary Compliance Only]].

## Software Verification and Validation

31. The [[ARCHITECTURE: Independent Verification and Validation (IV&V)]] using [[EQUIPMENT: Third-Party V&V Team]] and [[PROTOCOL: IEEE 1012 Standard Process]] provides [[MITIGATION: Unbiased Defect Detection]] against [[ATTACK_PATTERN: Developer Blind Spot Exploitation]] targeting [[VULNERABILITY: Self-Verification Limitations]].

32. The [[ARCHITECTURE: Back-to-Back Testing]] using [[EQUIPMENT: Certified Model Reference]] with [[PROTOCOL: Automated Output Comparison Protocol]] provides [[MITIGATION: Implementation Consistency Verification]] against [[ATTACK_PATTERN: Subtle Implementation Deviation]] exploiting [[VULNERABILITY: Undetected Model-Code Mismatch]].

33. The [[ARCHITECTURE: Requirements-Based Testing (RBT)]] using [[EQUIPMENT: Requirements Traceability Matrix]] and [[PROTOCOL: Bidirectional Traceability Protocol]] provides [[MITIGATION: Complete Requirements Coverage]] against [[ATTACK_PATTERN: Untested Requirement Exploitation]] targeting [[VULNERABILITY: Incomplete Test-to-Requirement Mapping]].

34. The [[ARCHITECTURE: Boundary Value Analysis]] using [[EQUIPMENT: Equivalence Class Partitioning Tool]] with [[PROTOCOL: Edge Case Test Generation]] provides [[MITIGATION: Input Validation Defect Detection]] against [[ATTACK_PATTERN: Boundary Condition Exploitation]] exploiting [[VULNERABILITY: Insufficient Edge Case Testing]].

35. The [[ARCHITECTURE: Robustness Testing]] using [[EQUIPMENT: Fault Injection Test Framework]] and [[PROTOCOL: Abnormal Input Test Protocol]] provides [[MITIGATION: Graceful Degradation Under Stress]] against [[ATTACK_PATTERN: Malformed Input Attack]] targeting [[VULNERABILITY: Unvalidated Error Handling Paths]].

## Software Safety Analysis

36. The [[ARCHITECTURE: Software Fault Tree Analysis (SFTA)]] using [[EQUIPMENT: Fault Tree Construction Tool]] with [[PROTOCOL: Top-Down Software Failure Analysis]] provides [[MITIGATION: Quantified Software Failure Probability]] against [[ATTACK_PATTERN: Unforeseen Software Failure Combination]] exploiting [[VULNERABILITY: Unanalyzed Software Failure Modes]].

37. The [[ARCHITECTURE: Software Failure Modes and Effects Analysis (SFMEA)]] using [[EQUIPMENT: Bottom-Up SFMEA Tool]] and [[PROTOCOL: Effect Propagation Analysis]] provides [[MITIGATION: Comprehensive Software Fault Impact Assessment]] against [[ATTACK_PATTERN: Unexpected Failure Propagation]] targeting [[VULNERABILITY: Unanalyzed Failure Effect Chains]].

38. The [[ARCHITECTURE: Common Cause Failure (CCF) Analysis]] using [[EQUIPMENT: Diversity Analysis Tool]] with [[PROTOCOL: Beta-Factor Methodology]] provides [[MITIGATION: Quantified Redundancy Effectiveness]] against [[ATTACK_PATTERN: Simultaneous Redundant Channel Failure]] exploiting [[VULNERABILITY: Unanalyzed Common Vulnerabilities]].

39. The [[ARCHITECTURE: Software Reliability Prediction]] using [[EQUIPMENT: Reliability Growth Model Tool]] and [[PROTOCOL: Defect Discovery Rate Analysis]] provides [[MITIGATION: Quantitative Reliability Estimate]] against [[ATTACK_PATTERN: Premature Release with Latent Defects]] targeting [[VULNERABILITY: Unknown Residual Defect Rate]].

40. The [[ARCHITECTURE: Petri Net Analysis for Software Safety]] using [[EQUIPMENT: Timed Petri Net Simulator]] with [[PROTOCOL: Reachability and Liveness Analysis]] provides [[MITIGATION: Verified Absence of Deadlocks and Livelocks]] against [[ATTACK_PATTERN: Deliberate System Deadlock Induction]] exploiting [[VULNERABILITY: Unverified Concurrency Properties]].

## Certification and Compliance

41. The [[ARCHITECTURE: Safety Case Development (GSN)]] using [[EQUIPMENT: Goal Structuring Notation Tool]] and [[PROTOCOL: Argument Pattern Library]] provides [[MITIGATION: Structured Safety Argumentation]] against [[ATTACK_PATTERN: Weak Safety Justification Attack]] targeting [[VULNERABILITY: Informal or Incomplete Safety Case]].

42. The [[ARCHITECTURE: Certification Liaison Management]] using [[EQUIPMENT: Certification Evidence Repository]] with [[PROTOCOL: Authority Engagement Protocol]] provides [[MITIGATION: Streamlined Certification Process]] against [[ATTACK_PATTERN: Certification Evidence Gap Exploitation]] exploiting [[VULNERABILITY: Insufficient Regulatory Engagement]].

43. The [[ARCHITECTURE: Software Quality Assurance (SQA)]] using [[EQUIPMENT: Independent SQA Function]] and [[PROTOCOL: Process Audit and Compliance Check]] provides [[MITIGATION: Verified Process Adherence]] against [[ATTACK_PATTERN: Process Shortcut Under Schedule Pressure]] targeting [[VULNERABILITY: Unmonitored Process Compliance]].

44. The [[ARCHITECTURE: Configuration Status Accounting]] using [[EQUIPMENT: Automated Build and Release System]] with [[PROTOCOL: Immutable Artifact Repository]] provides [[MITIGATION: Traceable Software Baseline]] against [[ATTACK_PATTERN: Binary Manipulation Before Deployment]] exploiting [[VULNERABILITY: Unverified Build Artifacts]].

45. The [[ARCHITECTURE: Post-Certification Maintenance Control]] using [[EQUIPMENT: Change Classification Tool]] and [[PROTOCOL: Recertification Trigger Analysis]] provides [[MITIGATION: Maintained Certification Status]] against [[ATTACK_PATTERN: Certification Invalidation via Uncontrolled Change]] targeting [[VULNERABILITY: Unmanaged Post-Certification Modifications]].

## Cross-Entity Annotation Summary
- ARCHITECTURE: 45 unique safety-critical software architectures
- EQUIPMENT: 45 safety software development tools
- PROTOCOL: 45 software safety standards protocols
- MITIGATION: 45 software safety risk mitigations
- ATTACK_PATTERN: 45 software safety attack scenarios
- VULNERABILITY: 45 software safety vulnerabilities
