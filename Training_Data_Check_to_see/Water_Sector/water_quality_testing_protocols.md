# Water Quality Testing Protocols

## Operational Overview
This document details comprehensive water quality testing protocols for municipal drinking water systems, including SCADA-controlled chemical dosing, continuous monitoring, and laboratory analysis procedures ensuring compliance with EPA Safe Drinking Water Act standards.

## Annotations

### 1. Continuous Chlorine Residual Monitoring
**Context**: Real-time monitoring of free chlorine residual throughout distribution system
**ICS Components**: Hach CL17 chlorine analyzers, SCADA integration modules, flow cells, automatic calibration systems
**Procedure**: Analyzers sample water continuously at 30 strategically located points; SCADA displays real-time values with alarm setpoints at 0.2 mg/L (low) and 4.0 mg/L (high) per EPA requirements
**Safety Critical**: Loss of residual chlorine indicates potential contamination or disinfection failure requiring immediate investigation
**Standards**: EPA Surface Water Treatment Rule requiring minimum 0.2 mg/L residual entering distribution and detectable residual throughout
**Vendors**: Hach chlorine analyzers, YSI residual monitors, Chemtrac analyzers

### 2. Automated Chlorine Injection Control
**Context**: PLC-controlled chlorine gas or sodium hypochlorite injection for primary disinfection
**ICS Components**: Chlorine injector pumps, gas chlorinators, flow-paced controllers, residual feedback loops
**Procedure**: PLC maintains target chlorine dose of 2.0-3.0 mg/L based on source water quality; flow-paced control adjusts dose proportionally; residual feedback trim control maintains 1.0 mg/L target at distribution entry point
**Safety Critical**: Chlorine gas leak detection systems with automatic shutoff and ventilation activation; personnel evacuation procedures
**Standards**: AWWA B301 Hypochlorite standard, EPA Disinfection Profiling requirements
**Vendors**: Capital Controls gas chlorinators, Grundfos DDA dosing pumps, Neptune Chemical Pump Company

### 3. pH Control and Monitoring
**Context**: Continuous pH monitoring and automated adjustment for corrosion control
**ICS Components**: pH sensors, chemical dosing pumps for caustic soda or acid, SCADA trending
**Procedure**: Maintain pH range 7.5-8.5 for optimal corrosion control; automated caustic soda injection when pH drops below 7.5; alarm triggers at pH <7.0 or >9.0 indicating sensor failure or water quality upset
**Safety Critical**: Rapid pH changes can mobilize lead from service lines posing acute health risk
**Standards**: EPA Lead and Copper Rule requiring pH 7.0-10.5 with optimal range 7.5-8.5
**Vendors**: Endress+Hauser Memosens pH sensors, ProMinent Dulcometer controllers

### 4. Turbidity Monitoring - Treatment Effectiveness
**Context**: Continuous monitoring of filtered water turbidity as indicator of treatment effectiveness
**ICS Components**: Hach 1720E turbidity meters, SCADA alarming, automatic sample diversion
**Procedure**: Individual filter turbidity monitored continuously; alarm at 0.3 NTU triggers operator investigation; reading >1.0 NTU initiates automatic filter-to-waste diversion and treatment optimization
**Safety Critical**: Turbidity breakthrough indicates filter failure allowing pathogen passage
**Standards**: EPA Surface Water Treatment Rule requiring turbidity <0.3 NTU in 95% of samples
**Vendors**: Hach turbidity meters, Analytical Technology turbidity analyzers

### 5. Bacteriological Sampling - Total Coliform
**Context**: Regulatory compliance sampling for total coliform and E. coli bacteria
**ICS Components**: LIMS (Laboratory Information Management System), sample tracking barcodes, automated sample routing
**Procedure**: Distribution system sampled at 40 predetermined locations monthly using EPA-approved sampling protocols; samples analyzed within 30 hours using Colilert method or membrane filtration
**Safety Critical**: Any positive coliform sample triggers repeat sampling within 24 hours and public notification if confirmed positive
**Standards**: EPA Total Coliform Rule requiring zero coliform in 95% of monthly samples
**Vendors**: IDEXX Colilert system, Millipore membrane filtration equipment

### 6. Disinfection Byproducts Monitoring - TTHM and HAA5
**Context**: Quarterly monitoring for trihalomethanes (TTHM) and haloacetic acids (HAA5)
**ICS Components**: Automated samplers, chain-of-custody documentation, certified laboratory analysis
**Procedure**: Four locations sampled quarterly representing maximum residence time in distribution system; samples shipped overnight to EPA-certified laboratory for gas chromatography analysis
**Safety Critical**: TTHM levels >80 μg/L or HAA5 >60 μg/L trigger system modifications to reduce disinfection byproduct formation
**Standards**: EPA Stage 2 Disinfectants and Disinfection Byproducts Rule
**Vendors**: Teledyne Tekmar AutoMate-Q40 sample preparation, Agilent GC-MS systems

### 7. Fluoride Addition and Monitoring
**Context**: Controlled fluoride addition for dental health protection
**ICS Components**: Fluoride chemical feeders, online fluoride analyzers, dosing verification systems
**Procedure**: Target fluoride concentration 0.7 mg/L maintained through automated hydrofluorosilicic acid injection; continuous analyzer monitors actual concentration with alarm setpoints at 0.5 mg/L (low) and 1.2 mg/L (high)
**Safety Critical**: Fluoride overfeed above 4.0 mg/L causes dental fluorosis health concerns
**Standards**: CDC Fluoridation Guidelines recommending 0.7 mg/L optimal level
**Vendors**: Blue-White Industries fluoride chemical feeders, Hach fluoride analyzers

### 8. Lead and Copper Compliance Monitoring
**Context**: Triennial monitoring at high-risk residential locations for lead and copper corrosion
**ICS Components**: Sample kit distribution tracking, certified laboratory analysis, GIS mapping
**Procedure**: 60 Tier 1 high-risk homes sampled every three years using first-draw sampling protocol; samples analyzed by ICP-MS for lead and copper concentrations
**Safety Critical**: 90th percentile lead >15 μg/L or copper >1.3 mg/L triggers corrosion control treatment and public education requirements
**Standards**: EPA Lead and Copper Rule
**Vendors**: Brooks Rand automated sampling systems, PerkinElmer ICP-MS instruments

### 9. Chlorine Demand Testing - Raw Water Characterization
**Context**: Laboratory testing to determine chlorine dose requirements for source water
**ICS Components**: Bench-scale chlorine demand apparatus, laboratory SCADA integration
**Procedure**: Weekly jar test procedure applies varying chlorine doses to raw water samples; plots chlorine demand curve; determines breakpoint chlorination dose for SCADA setpoint adjustment
**Safety Critical**: Inadequate chlorine dose allows pathogen survival; excessive dose increases disinfection byproducts
**Standards**: APHA Standard Methods 2350B Chlorine Demand
**Vendors**: Hach laboratory chlorine test kits

### 10. Continuous TOC (Total Organic Carbon) Monitoring
**Context**: Real-time monitoring of organic precursors for disinfection byproduct formation
**ICS Components**: Sievers online TOC analyzers, SCADA trending, enhanced coagulation control
**Procedure**: Continuous TOC monitoring at treatment plant inlet and outlet; SCADA trends identify seasonal variations; coagulant dose automatically adjusted to achieve enhanced TOC removal when levels exceed 2.0 mg/L
**Safety Critical**: High TOC levels combine with chlorine to form regulated carcinogenic disinfection byproducts
**Standards**: EPA Enhanced Coagulation requirements under Stage 2 DBP Rule
**Vendors**: GE Sievers M9 TOC analyzers, Shimadzu TOC analyzers

### 11. SCADA-Integrated Particle Counting
**Context**: Real-time particle counts as early warning for filter breakthrough
**ICS Components**: Met One particle counters, SCADA integration, statistical process control
**Procedure**: Continuous particle counting in 2-100 μm range on each filter effluent; statistical process control algorithms detect trends indicating filter degradation before turbidity increase
**Safety Critical**: Particle count increase precedes turbidity breakthrough by 12-24 hours allowing preventive action
**Standards**: Partnership for Safe Water optimization goals
**Vendors**: Met One online particle counters, HACH 3000 series

### 12. Nitrate/Nitrite Monitoring - Agricultural Areas
**Context**: Monitoring for agricultural fertilizer contamination in vulnerable source waters
**ICS Components**: Ion-selective electrode analyzers, automated sampling, SCADA alarming
**Procedure**: Continuous or 4-hour composite sampling at treatment plant inlet; SCADA alarm triggers at 8 mg/L nitrate approaching 10 mg/L MCL; sustained high levels require alternative source activation
**Safety Critical**: Nitrate >10 mg/L causes methemoglobinemia (blue baby syndrome) in infants
**Standards**: EPA Maximum Contaminant Level for Nitrate at 10 mg/L as N
**Vendors**: Hach Nitratax sc nitrate probe, Endress+Hauser Liquiline analyzers

### 13. Alkalinity and Hardness Testing - Corrosion Control
**Context**: Regular laboratory testing to optimize corrosion control treatment
**ICS Components**: Laboratory autotitrators, LIMS integration, Langelier Index calculators
**Procedure**: Daily alkalinity and hardness testing using automated titration; results input to SCADA for calculation of Langelier Saturation Index (LSI); chemical dosing adjusted to maintain LSI near zero for optimal corrosion control
**Safety Critical**: Corrosive water (negative LSI) mobilizes lead from service lines and copper from plumbing
**Standards**: AWWA C400 corrosion control standards
**Vendors**: Hach autotitrators, Mettler Toledo titration systems

### 14. Cryptosporidium and Giardia Monitoring - LT2ESWTR
**Context**: Monthly microscopic analysis for protozoan parasites in source water
**ICS Components**: Sampling equipment, certified laboratory microscopy, risk assessment calculations
**Procedure**: 24-month initial monitoring program followed by reduced frequency based on source water risk; samples concentrated using EPA Method 1623, analyzed by immunofluorescence microscopy
**Safety Critical**: Detection triggers requirements for additional treatment barriers (UV, membrane filtration, or ozone)
**Standards**: EPA Long Term 2 Enhanced Surface Water Treatment Rule
**Vendors**: IDEXX Filta-Max sampling systems, Waterborne Inc. analysis services

### 15. Cyanotoxin Monitoring - HAB Management
**Context**: Monitoring for harmful algal bloom toxins from source water
**ICS Components**: Automated samplers, ELISA test kits, LC-MS/MS laboratory confirmation
**Procedure**: Weekly screening during algal bloom season (May-October) using ELISA rapid test kits; positive results confirmed by mass spectrometry; levels >1.6 μg/L microcystin trigger enhanced treatment
**Safety Critical**: Cyanotoxins cause liver damage and neurological effects; conventional treatment may not remove toxins effectively
**Standards**: EPA Health Advisory Level for Microcystin-LR at 1.6 μg/L for adults
**Vendors**: Abraxis ELISA test kits, Agilent LC-MS/MS systems

### 16. SCADA-Controlled Coagulant Dosing
**Context**: Automated jar test optimization and coagulant dose control
**ICS Components**: Streaming current detectors, coagulant dosing pumps, PLC optimization algorithms
**Procedure**: Streaming current monitor provides real-time feedback on coagulation effectiveness; PLC adjusts alum or ferric chloride dose to maintain optimal charge neutralization; SCADA logs dose vs. raw water turbidity correlation
**Safety Critical**: Underdosing allows particle breakthrough; overdosing wastes chemicals and impacts finished water quality
**Standards**: AWWA B408 Liquid Alum standard
**Vendors**: Chemtrac PC3000 streaming current monitor, Milton Roy chemical pumps

### 17. UV Disinfection Monitoring and Control
**Context**: UV system operation for primary or secondary disinfection and Cryptosporidium inactivation
**ICS Components**: UV intensity sensors, lamp status monitors, validated dose calculations, SCADA integration
**Procedure**: UV dose calculated continuously based on flow rate, UV transmittance, and lamp intensity; minimum 40 mJ/cm² dose maintained per EPA UV Manual; low UV alarm triggers automatic chlorine boost
**Safety Critical**: Inadequate UV dose allows Cryptosporidium passage causing potential gastroenteritis outbreaks
**Standards**: EPA UV Disinfection Guidance Manual (UVDGM)
**Vendors**: Trojan Technologies UV systems, Xylem Wedeco UV systems

### 18. Phosphate Corrosion Inhibitor Control
**Context**: Automated orthophosphate addition for lead corrosion control
**ICS Components**: Phosphate dosing pumps, orthophosphate analyzers, SCADA trending
**Procedure**: Maintain 1.0-2.0 mg/L orthophosphate residual in distribution system through automated zinc orthophosphate or sodium phosphate injection; continuous analyzer monitors actual concentration
**Safety Critical**: Phosphate forms protective scales on lead service lines preventing lead dissolution
**Standards**: EPA Lead and Copper Rule corrosion control treatment optimization
**Vendors**: Hach PhosphaX phosphate analyzer, Grundfos dosing systems

### 19. Seasonal Temperature Monitoring and Adaptation
**Context**: Adjusting treatment processes based on seasonal water temperature variations
**ICS Components**: Temperature sensors, SCADA trend analysis, seasonal control strategies
**Procedure**: Winter operations (water <10°C) increase coagulant dose by 20% to compensate for reduced reaction kinetics; summer operations (water >20°C) increase chlorine contact time to account for increased bacterial activity
**Safety Critical**: Temperature affects chemical reaction rates, microbial growth, and disinfection effectiveness
**Standards**: AWWA M37 Operational Control of Coagulation and Filtration Processes
**Vendors**: Standard temperature sensors integrated with SCADA

### 20. Operator Rounds and Manual Testing Verification
**Context**: Human verification of automated SCADA systems through regular operator rounds
**ICS Components**: Portable test kits, calibration standards, paper logs, mobile data entry
**Procedure**: Operators conduct four daily rounds verifying SCADA chlorine, pH, and turbidity readings using calibrated portable instruments; discrepancies >10% trigger sensor cleaning or calibration
**Safety Critical**: Automated systems can fail without detection if operator verification is not performed
**Standards**: State operator certification requirements for routine operations
**Vendors**: Hach pocket colorimeter II, Oakton portable meters

### 21. Water Quality Event Detection - CANARY
**Context**: Statistical algorithms detecting anomalous water quality patterns indicating contamination
**ICS Components**: CANARY software, multiparameter sensors, SCADA integration, event classification algorithms
**Procedure**: CANARY software analyzes real-time data streams from 20+ sensors using change-point detection algorithms; anomalies trigger investigation protocols within 15 minutes
**Safety Critical**: Early contamination detection enables rapid response preventing widespread exposure
**Standards**: EPA Water Security Initiative protocols
**Vendors**: EPA CANARY software (free), Halo Wlsystgent Insight platforms

### 22. Disinfectant Switchover Operations - Chlorine to Chloramine
**Context**: Seasonal conversion from free chlorine to chloramines for distribution system disinfection
**ICS Components**: Ammonia dosing systems, chlorine-to-ammonia ratio controllers, breakpoint prevention
**Procedure**: Ammonia addition ramped up gradually over 48 hours while maintaining chlorine dose; target 4:1 chlorine:ammonia weight ratio for monochloramine formation; comprehensive distribution sampling verifies stable chloramine residual
**Safety Critical**: Improper chlorine:ammonia ratio can form dichloramine causing taste/odor complaints or inadequate disinfection
**Standards**: EPA Chloramines fact sheet and AWWA chloramination practices
**Vendors**: Capital Controls ammonia systems, Evoqua chloramine control packages

### 23. Regulatory Compliance Reporting - SDWIS
**Context**: Automated data export and regulatory report generation
**ICS Components**: SCADA historians, report generation software, electronic regulatory submission systems
**Procedure**: Monthly compliance reports auto-generated from SCADA data historians; regulatory parameters (chlorine residual, turbidity, bacteriological results) exported to EPA Safe Drinking Water Information System
**Safety Critical**: Failure to report violations can result in regulatory penalties and loss of public trust
**Standards**: EPA SDWIS Federal Reporting Services requirements
**Vendors**: OSIsoft PI to SDWIS interfaces, custom SCADA reporting modules

### 24. Quality Assurance and Quality Control (QA/QC)
**Context**: Ongoing validation of laboratory and online analyzer accuracy
**ICS Components**: Certified reference standards, proficiency testing samples, calibration schedules, QC tracking
**Procedure**: Laboratory participates in quarterly proficiency testing programs; online analyzers verified weekly with certified standards; all results tracked in LIMS with automatic flagging of out-of-range QC samples
**Safety Critical**: Inaccurate measurements can lead to improper treatment decisions or false compliance status
**Standards**: EPA QA/QC requirements for drinking water analysis, NELAC certification standards
**Vendors**: NSI Lab Solutions proficiency testing, ERA Environmental PT programs

## Laboratory Equipment Integration
Modern water quality laboratories integrate with SCADA systems enabling real-time data sharing between laboratory analysis and treatment plant operations for optimal process control.

## Emergency Response Protocols
All positive bacteriological results, regulatory exceedances, or water quality anomalies trigger immediate notification protocols to operations management, regulatory agencies, and public health authorities as required.
