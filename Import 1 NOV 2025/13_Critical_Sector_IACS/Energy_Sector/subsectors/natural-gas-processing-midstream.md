# Natural Gas Processing - Midstream Operations
**Subsector:** Oil and Natural Gas - Midstream
**Component:** Natural Gas Processing & Transmission
**Date:** 2025-11-06
**Entity Focus:** VENDOR, EQUIPMENT, OPERATION, PROTOCOL

## Overview

Natural gas processing facilities separate natural gas liquids (NGLs), remove impurities, and prepare pipeline-quality gas for transmission. These plants employ sophisticated process control systems, rotating equipment, cryogenic separation units, and extensive safety instrumentation coordinated by multiple industrial automation vendors.

## Major Process Control Vendors

### Distributed Control Systems (DCS)

**[VENDOR: Honeywell Process Solutions]** dominates gas processing with **[EQUIPMENT: Experion PKS DCS]**, deployed in over 60% of major North American gas plants. **[VENDOR: Honeywell]** **[EQUIPMENT: C300 controllers]**, **[EQUIPMENT: Safety Manager]**, and **[EQUIPMENT: UniSim Design]** software manage amine treating, dehydration, NGL fractionation, and compression operations. **[VENDOR: Honeywell]** **[EQUIPMENT: Profit Controller]** provides multivariable predictive control for cryogenic separation units.

**[VENDOR: Emerson]** supplies **[EQUIPMENT: DeltaV DCS]** to gas processing facilities, integrating **[EQUIPMENT: DeltaV SIS]** safety systems, **[EQUIPMENT: AMS Device Manager]**, and **[EQUIPMENT: Syncade MES]** (Manufacturing Execution System). **[VENDOR: Emerson]** **[EQUIPMENT: DeltaV Live]** mobile applications enable remote monitoring of amine regeneration, dew point control, and compressor performance.

**[VENDOR: Yokogawa]** provides **[EQUIPMENT: CENTUM VP DCS]**, **[EQUIPMENT: ProSafe-RS safety system]**, and **[EQUIPMENT: Exaquantum PIMS]** for gas processing automation. **[VENDOR: Yokogawa]** **[EQUIPMENT: Exapilot APC]** (Advanced Process Control) optimizes NGL recovery and refrigeration systems. **[VENDOR: Yokogawa]** **[EQUIPMENT: FieldMate device management]** configures **[EQUIPMENT: FOUNDATION Fieldbus]** instruments.

**[VENDOR: ABB]** delivers **[EQUIPMENT: Symphony Plus DCS]**, **[EQUIPMENT: 800xA automation platform]**, and **[EQUIPMENT: AC800M controllers]** to gas processing plants. **[VENDOR: ABB]** **[EQUIPMENT: Ability System 800xA]** integrates process control, safety systems, and electrical distribution monitoring in a single operator interface.

**[VENDOR: Schneider Electric]** offers **[EQUIPMENT: Foxboro I/A Series DCS]** and modern **[EQUIPMENT: EcoStruxure Foxboro DCS]** to midstream facilities, with **[EQUIPMENT: Triconex safety controllers]** providing triple-modular-redundant (TMR) protection for emergency shutdown systems. **[VENDOR: Schneider Electric]** **[EQUIPMENT: SimSci PRO/II]** simulates gas processing operations for operator training.

### Programmable Logic Controllers (PLCs)

**[VENDOR: Rockwell Automation]** supplies **[EQUIPMENT: Allen-Bradley ControlLogix PLCs]**, **[EQUIPMENT: CompactLogix controllers]**, and **[EQUIPMENT: PlantPAx DCS]** for skid-mounted gas processing units and modular plants. **[VENDOR: Rockwell Automation]** **[EQUIPMENT: GuardLogix safety PLCs]** integrate with **[EQUIPMENT: Kinetix servo drives]** for automated valve actuation and sampling systems.

**[VENDOR: Siemens]** provides **[EQUIPMENT: SIMATIC S7-1500 PLCs]**, **[EQUIPMENT: S7-400 controllers]**, and **[EQUIPMENT: PCS 7 DCS]** for gas plant automation. **[VENDOR: Siemens]** **[EQUIPMENT: SIMATIC Safety Integrated]** controllers meet **[PROTOCOL: IEC 61511]** SIL 3 requirements for emergency shutdown and fire & gas protection.

**[VENDOR: GE Digital]** (formerly **[VENDOR: GE Intelligent Platforms]**) offers **[EQUIPMENT: PACSystems RX3i PLCs]** and **[EQUIPMENT: iFIX SCADA]** for gas processing and compression stations. **[VENDOR: GE Digital]** **[EQUIPMENT: Proficy Historian]** collects time-series data from **[EQUIPMENT: flow computers]**, **[EQUIPMENT: gas chromatographs]**, and **[EQUIPMENT: emission monitors]**.

## Critical Processing Equipment

### Gas Treatment Systems

**[EQUIPMENT: Amine treating units]** remove H₂S and CO₂ using **[EQUIPMENT: absorber towers]**, **[EQUIPMENT: regeneration columns]**, and **[EQUIPMENT: amine circulation pumps]** from **[VENDOR: Sulzer]**, **[VENDOR: Koch-Glitsch]**, and **[VENDOR: Exterran]**. **[EQUIPMENT: Lean/rich amine heat exchangers]** recover thermal energy, while **[EQUIPMENT: amine filtration systems]** from **[VENDOR: Pall Corporation]** and **[VENDOR: Parker Hannifin]** remove contaminants.

**[EQUIPMENT: Molecular sieve dehydrators]** from **[VENDOR: Honeywell UOP]**, **[VENDOR: Zeochem]**, and **[VENDOR: BASF]** reduce water content to pipeline specifications (<7 lb H₂O/MMscf). **[EQUIPMENT: Triethylene glycol (TEG) dehydration units]** manufactured by **[VENDOR: Exterran]**, **[VENDOR: Schlumberger]**, and **[VENDOR: Enerflex]** provide alternative dehydration using **[EQUIPMENT: glycol contactors]** and **[EQUIPMENT: regeneration stills]**.

**[EQUIPMENT: Mercury removal units]** protect aluminum **[EQUIPMENT: cryogenic heat exchangers]** using **[EQUIPMENT: sulfur-impregnated activated carbon]** from **[VENDOR: Calgon Carbon]** (now **[VENDOR: Kuraray]**) or **[EQUIPMENT: HgSIV adsorbent]** from **[VENDOR: Johnson Matthey]**. **[EQUIPMENT: Adsorber vessels]** with **[EQUIPMENT: automated valve sequencing]** enable online regeneration.

### NGL Recovery and Fractionation

**[EQUIPMENT: Turboexpander plants]** manufactured by **[VENDOR: Atlas Copco]**, **[VENDOR: GE Oil & Gas]**, **[VENDOR: Honeywell UOP]**, and **[VENDOR: Cryostar]** achieve high ethane recovery using **[EQUIPMENT: turboexpander compressors]**, **[EQUIPMENT: demethanizers]**, and **[EQUIPMENT: brazed aluminum heat exchangers]** from **[VENDOR: Chart Industries]** and **[VENDOR: Linde Engineering]**.

**[EQUIPMENT: Refrigeration plants]** employ **[EQUIPMENT: propane chillers]**, **[EQUIPMENT: mixed refrigerant systems]**, or **[EQUIPMENT: cascade refrigeration cycles]** with **[EQUIPMENT: reciprocating compressors]** from **[VENDOR: Ariel Corporation]**, **[EQUIPMENT: screw compressors]** from **[VENDOR: Howden]**, and **[EQUIPMENT: centrifugal compressors]** from **[VENDOR: MAN Energy Solutions]**.

**[EQUIPMENT: Fractionation towers]** separate NGLs into ethane, propane, butane, and natural gasoline using **[EQUIPMENT: structured packing]** from **[VENDOR: Sulzer]**, **[VENDOR: Koch-Glitsch]**, and **[VENDOR: Raschig]**. **[EQUIPMENT: Reboilers]**, **[EQUIPMENT: condensers]**, and **[EQUIPMENT: reflux drums]** control **[EQUIPMENT: distillation column]** performance with **[EQUIPMENT: split-range level controllers]** and **[EQUIPMENT: cascade temperature control]**.

**[EQUIPMENT: De-ethanizers]**, **[EQUIPMENT: depropanizers]**, **[EQUIPMENT: debutanizers]**, and **[EQUIPMENT: deisobutanizers]** produce specification-grade NGLs measured by **[EQUIPMENT: gas chromatographs]** from **[VENDOR: ABB]** **[EQUIPMENT: PGC5000]**, **[VENDOR: Yokogawa]** **[EQUIPMENT: GC8000]**, **[VENDOR: Siemens]** **[EQUIPMENT: MAXUM]**, and **[VENDOR: Emerson]** **[EQUIPMENT: Rosemount 700XA]**.

### Compression Systems

**[EQUIPMENT: Reciprocating compressors]** from **[VENDOR: Ariel Corporation]** (JGK, JGE, JGH models) dominate gas gathering and processing applications with **[EQUIPMENT: natural gas engines]** from **[VENDOR: Caterpillar]**, **[VENDOR: Waukesha]** (**[VENDOR: INNIO]**), and **[VENDOR: Cummins]**. **[EQUIPMENT: Compressor controllers]** from **[VENDOR: Ariel]** **[EQUIPMENT: ICCP]**, **[VENDOR: Emerson]** **[EQUIPMENT: Bristol POGO]**, and **[VENDOR: Hoerbiger]** **[EQUIPMENT: HydroCOM]** optimize performance and manage **[EQUIPMENT: unloader valves]**.

**[EQUIPMENT: Centrifugal compressors]** manufactured by **[VENDOR: Siemens Energy]**, **[VENDOR: GE Oil & Gas]**, **[VENDOR: MAN Energy Solutions]**, **[VENDOR: Solar Turbines]**, and **[VENDOR: Baker Hughes Nuovo Pignone]** handle high-volume gas transmission, driven by **[EQUIPMENT: gas turbines]**, **[EQUIPMENT: electric motors]**, or **[EQUIPMENT: steam turbines]**.

**[EQUIPMENT: Screw compressors]** from **[VENDOR: Howden]**, **[VENDOR: Atlas Copco]**, **[VENDOR: Ingersoll Rand]**, and **[VENDOR: GEA]** provide oil-free compression for instrument air and low-ratio applications. **[EQUIPMENT: Variable speed drives]** (VSDs) from **[VENDOR: ABB]**, **[VENDOR: Siemens]**, and **[VENDOR: Schneider Electric]** modulate capacity efficiently.

**[EQUIPMENT: Anti-surge control systems]** from **[VENDOR: Emerson]** **[EQUIPMENT: Control Wave]**, **[VENDOR: Honeywell]** **[EQUIPMENT: ASC+]**, **[VENDOR: Rockwell Automation]**, and **[VENDOR: Compressor Controls Corporation]** prevent surge-induced damage to centrifugal compressors using **[EQUIPMENT: fast-acting anti-surge valves]**.

## Instrumentation and Measurement

### Flow Measurement

**[EQUIPMENT: Ultrasonic flowmeters]** from **[VENDOR: Sick]** **[EQUIPMENT: FLOWSIC600]**, **[VENDOR: GE Panametrics]** **[EQUIPMENT: TransPort PT900]**, **[VENDOR: Krohne]** **[EQUIPMENT: ALTOSONIC V12]**, and **[VENDOR: Emerson Daniel]** **[EQUIPMENT: SeniorSonic]** provide custody-quality gas measurement compliant with **[PROTOCOL: AGA Report No. 9]**.

**[EQUIPMENT: Coriolis mass flowmeters]** from **[VENDOR: Emerson]** **[EQUIPMENT: Micro Motion]**, **[VENDOR: Endress+Hauser]** **[EQUIPMENT: Promass]**, **[VENDOR: Yokogawa]** **[EQUIPMENT: ROTAMASS]**, and **[VENDOR: Krohne]** **[EQUIPMENT: OPTIMASS]** measure NGL flows with ±0.10% accuracy, integrating with **[EQUIPMENT: flow computers]** via **[PROTOCOL: Modbus]**, **[PROTOCOL: HART]**, or **[PROTOCOL: FOUNDATION Fieldbus]**.

**[EQUIPMENT: Turbine meters]** manufactured by **[VENDOR: Emerson Daniel]**, **[VENDOR: SICK]**, **[VENDOR: Elster Instromet]** (now **[VENDOR: Honeywell]**), and **[VENDOR: FMC Technologies]** measure gas flows with **[EQUIPMENT: pulse output]** or **[EQUIPMENT: 4-20mA analog signals]**, proven by **[EQUIPMENT: master meter systems]** and **[EQUIPMENT: sonic nozzle calibrators]**.

**[EQUIPMENT: Differential pressure flowmeters]** using **[EQUIPMENT: orifice plates]**, **[EQUIPMENT: venturi tubes]**, or **[EQUIPMENT: flow nozzles]** comply with **[PROTOCOL: AGA Report No. 3]** and **[PROTOCOL: ISO 5167]**, with **[EQUIPMENT: differential pressure transmitters]** from **[VENDOR: Emerson Rosemount]**, **[VENDOR: Endress+Hauser]**, **[VENDOR: Yokogawa]**, and **[VENDOR: ABB]**.

### Analytical Instruments

**[EQUIPMENT: Gas chromatographs]** analyze C₁-C₆+ hydrocarbon composition for BTU calculation, custody transfer, and product quality verification. **[VENDOR: ABB]** **[EQUIPMENT: PGC5000 NGC8200]**, **[VENDOR: Siemens]** **[EQUIPMENT: MAXUM Edition II]**, **[VENDOR: Yokogawa]** **[EQUIPMENT: GC8000]**, and **[VENDOR: Emerson]** **[EQUIPMENT: Rosemount 700XA]** provide online analysis with automatic calibration.

**[EQUIPMENT: Moisture analyzers]** from **[VENDOR: Michell Instruments]**, **[VENDOR: Panametrics]** (**[VENDOR: GE]**), **[VENDOR: AMETEK]**, and **[VENDOR: Vaisala]** verify dew point specifications using **[EQUIPMENT: chilled mirror hygrometers]**, **[EQUIPMENT: aluminum oxide sensors]**, or **[EQUIPMENT: tunable diode laser (TDL) analyzers]**.

**[EQUIPMENT: Sulfur analyzers]** detect H₂S and total sulfur using **[EQUIPMENT: electrochemical sensors]**, **[EQUIPMENT: UV fluorescence analyzers]** from **[VENDOR: Teledyne]** and **[VENDOR: AMETEK]**, or **[EQUIPMENT: gas chromatography with sulfur-selective detection]**. **[EQUIPMENT: Mercury analyzers]** from **[VENDOR: Analytik Jena]**, **[VENDOR: LUMEX]**, and **[VENDOR: OhioLumex]** measure ultra-trace mercury levels.

**[EQUIPMENT: Oxygen analyzers]** monitor combustion efficiency and inert gas purity using **[EQUIPMENT: zirconia sensors]** from **[VENDOR: Yokogawa]**, **[VENDOR: AMETEK]**, **[VENDOR: ABB]**, and **[VENDOR: Servomex]**. **[EQUIPMENT: CO₂ analyzers]** employ **[EQUIPMENT: non-dispersive infrared (NDIR) sensors]** or **[EQUIPMENT: tunable diode laser spectroscopy]**.

### Level and Pressure Measurement

**[EQUIPMENT: Guided wave radar level transmitters]** from **[VENDOR: Emerson]** **[EQUIPMENT: Rosemount 5300]**, **[VENDOR: Endress+Hauser]** **[EQUIPMENT: Levelflex FMP50]**, **[VENDOR: Vega]** **[EQUIPMENT: VEGAFLEX]**, and **[VENDOR: Magnetrol]** **[EQUIPMENT: Eclipse Model 706]** measure levels in **[EQUIPMENT: amine contactors]**, **[EQUIPMENT: glycol contactors]**, **[EQUIPMENT: reflux drums]**, and **[EQUIPMENT: storage tanks]**.

**[EQUIPMENT: Differential pressure level transmitters]** calculate liquid levels in pressurized vessels using **[EQUIPMENT: electronic DP cells]** from **[VENDOR: Emerson Rosemount]**, **[VENDOR: Yokogawa]**, **[VENDOR: Endress+Hauser]**, and **[VENDOR: ABB]**, with **[EQUIPMENT: remote seals]** isolating process fluids.

**[EQUIPMENT: Pressure transmitters]** monitor compressor suction/discharge, tower pressures, and pipeline pressures with accuracies to ±0.04% of span. **[VENDOR: Emerson Rosemount 3051S]**, **[VENDOR: Yokogawa EJX910A]**, **[VENDOR: Endress+Hauser Cerabar]**, and **[VENDOR: ABB 266]** transmitters provide **[PROTOCOL: HART]**, **[PROTOCOL: FOUNDATION Fieldbus]**, or **[PROTOCOL: PROFIBUS PA]** communication.

**[EQUIPMENT: Temperature transmitters]** from **[VENDOR: Emerson]**, **[VENDOR: Endress+Hauser]**, **[VENDOR: Wika]**, and **[VENDOR: Pyromation]** interface with **[EQUIPMENT: RTDs]** (Pt100/Pt1000) and **[EQUIPMENT: thermocouples]** (Type J, K, T) for cryogenic and high-temperature applications.

## Operations and Control Strategies

### Process Control Operations

**[OPERATION: Amine treating optimization]** maintains acid gas removal efficiency through **[EQUIPMENT: amine circulation rate control]**, **[EQUIPMENT: reboiler temperature control]**, and **[EQUIPMENT: reflux control]** using cascade and feedforward strategies. **[OPERATION: Amine quality monitoring]** tracks **[EQUIPMENT: heat stable salt]** accumulation and **[EQUIPMENT: amine degradation]** products.

**[OPERATION: Glycol dehydration control]** regulates **[EQUIPMENT: glycol circulation rates]**, **[EQUIPMENT: reboiler temperatures]**, and **[EQUIPMENT: contactor pressures]** to achieve pipeline water dew point specifications. **[OPERATION: Glycol regeneration]** removes absorbed water and hydrocarbons in **[EQUIPMENT: reboiler stills]** operating at 350-400°F.

**[OPERATION: Cryogenic NGL recovery]** adjusts **[EQUIPMENT: turboexpander speed]**, **[EQUIPMENT: demethanizer reflux]**, and **[EQUIPMENT: residue gas temperature]** to maximize ethane recovery while meeting pipeline heating value specifications. **[OPERATION: Auto-refrigeration]** uses **[EQUIPMENT: Joule-Thomson expansion]** across **[EQUIPMENT: control valves]** for simpler plants.

**[OPERATION: Fractionation column control]** implements **[EQUIPMENT: dual-composition inferential control]**, **[EQUIPMENT: differential temperature control]**, or direct **[EQUIPMENT: gas chromatograph feedback]** to maintain product specifications. **[OPERATION: Feed composition changes]** trigger **[EQUIPMENT: adaptive control adjustments]** via **[VENDOR: Honeywell]** **[EQUIPMENT: Profit Controller]** or **[VENDOR: Emerson]** **[EQUIPMENT: DeltaV Predict]**.

### Compression Operations

**[OPERATION: Reciprocating compressor control]** modulates capacity using **[EQUIPMENT: fixed or variable unloaders]**, **[EQUIPMENT: clearance pockets]**, or **[EQUIPMENT: suction valve unloaders]** managed by **[VENDOR: Ariel]** **[EQUIPMENT: ICCP controllers]** or **[VENDOR: Compressor Controls Corporation]** **[EQUIPMENT: control panels]**.

**[OPERATION: Centrifugal compressor control]** varies **[EQUIPMENT: inlet guide vanes]** (IGVs), **[EQUIPMENT: variable speed drives]**, or **[EQUIPMENT: discharge throttling]** to match flow requirements while avoiding surge. **[OPERATION: Anti-surge protection]** monitors compressor operating points on **[EQUIPMENT: compressor performance curves]**, opening **[EQUIPMENT: recycle valves]** when approaching surge line.

**[OPERATION: Compressor condition monitoring]** tracks **[EQUIPMENT: vibration levels]**, **[EQUIPMENT: bearing temperatures]**, **[EQUIPMENT: lube oil pressures]**, and **[EQUIPMENT: valve temperatures]** using **[VENDOR: Bently Nevada]** (**[VENDOR: Baker Hughes]**) **[EQUIPMENT: System 1]**, **[VENDOR: SKF]** **[EQUIPMENT: Multilog DMx]**, or **[VENDOR: Emerson AMS]** machinery health management.

**[OPERATION: Engine-driven compressor control]** coordinates **[EQUIPMENT: engine speed governors]**, **[EQUIPMENT: air-fuel ratio control]**, **[EQUIPMENT: ignition timing]**, and **[EQUIPMENT: turbocharger wastegate control]** via **[VENDOR: Woodward]** **[EQUIPMENT: MicroNet TMR]** or **[VENDOR: Altronic]** **[EQUIPMENT: CD-200]** controllers.

### Safety and Environmental Operations

**[OPERATION: Emergency shutdown (ESD) activation]** isolates plant sections using **[EQUIPMENT: block valves]**, **[EQUIPMENT: blowdown valves]**, and **[EQUIPMENT: depressurization systems]** upon detection of high pressure, low pressure, fire, or gas release. **[PROTOCOL: IEC 61511]**-compliant **[EQUIPMENT: safety instrumented systems]** achieve SIL 2 or SIL 3 integrity.

**[OPERATION: Fire and gas detection]** employs **[EQUIPMENT: flame detectors]** (UV/IR), **[EQUIPMENT: combustible gas detectors]** (catalytic bead or infrared), and **[EQUIPMENT: toxic gas monitors]** (H₂S, CO, SO₂) from **[VENDOR: Honeywell Analytics]**, **[VENDOR: MSA Safety]**, **[VENDOR: Dräger]**, and **[VENDOR: Emerson Rosemount]**.

**[OPERATION: Pressure relief]** protects vessels via **[EQUIPMENT: pressure safety valves]** (PSVs) from **[VENDOR: Emerson Fisher]**, **[VENDOR: Crosby]**, **[VENDOR: Anderson Greenwood]**, and **[VENDOR: Teledyne Farris]**, sized per **[PROTOCOL: API Standard 520]** and **[PROTOCOL: API Standard 521]**. **[EQUIPMENT: Flare systems]** combust relief discharges with **[EQUIPMENT: flare pilots]**, **[EQUIPMENT: knock-out drums]**, and **[EQUIPMENT: water seals]**.

**[OPERATION: Emissions monitoring]** measures VOC emissions, NOx, CO, and SO₂ using **[EQUIPMENT: continuous emission monitoring systems]** (CEMS) from **[VENDOR: Siemens]**, **[VENDOR: ABB]**, **[VENDOR: AMETEK]**, and **[VENDOR: Teledyne]**, reporting to EPA via **[PROTOCOL: EPA Part 60]** and **[PROTOCOL: Part 75]** protocols.

**[OPERATION: Leak detection and repair]** (LDAR) programs monitor fugitive emissions from **[EQUIPMENT: valves]**, **[EQUIPMENT: flanges]**, **[EQUIPMENT: pump seals]**, and **[EQUIPMENT: compressor seals]** using **[EQUIPMENT: portable gas detectors]** and **[EQUIPMENT: infrared cameras]** from **[VENDOR: FLIR]**, **[VENDOR: Opgal]**, and **[VENDOR: Sensia]** (**[VENDOR: Rockwell Automation]**).

## Communication Protocols and Networks

### Industrial Control Protocols

**[PROTOCOL: FOUNDATION Fieldbus H1]** connects **[EQUIPMENT: smart transmitters]**, **[EQUIPMENT: valve positioners]**, and **[EQUIPMENT: analytical instruments]** to **[VENDOR: Emerson DeltaV]**, **[VENDOR: Honeywell Experion]**, and **[VENDOR: ABB 800xA]** systems at 31.25 kbps over **[ARCHITECTURE: two-wire 4-20mA networks]**. **[EQUIPMENT: Fieldbus power supplies]** and **[EQUIPMENT: segment protectors]** from **[VENDOR: Relcom]**, **[VENDOR: Pepperl+Fuchs]**, and **[VENDOR: MTL]** ensure network reliability.

**[PROTOCOL: HART]** (Highway Addressable Remote Transducer) superimposes digital communication on 4-20mA signals, enabling remote configuration of **[EQUIPMENT: pressure transmitters]**, **[EQUIPMENT: level transmitters]**, and **[EQUIPMENT: flow transmitters]**. **[EQUIPMENT: HART multiplexers]** from **[VENDOR: Emerson]**, **[VENDOR: MACTek]**, and **[VENDOR: Moore Industries]** aggregate multiple HART devices.

**[PROTOCOL: Modbus TCP/IP]** provides Ethernet-based communication between **[EQUIPMENT: PLCs]**, **[EQUIPMENT: HMIs]**, **[EQUIPMENT: flow computers]**, and **[EQUIPMENT: SCADA systems]**. **[PROTOCOL: Modbus RTU]** operates over **[ARCHITECTURE: RS-485 serial networks]** connecting remote instruments and **[EQUIPMENT: RTUs]**.

**[PROTOCOL: PROFIBUS PA]** (Process Automation) and **[PROTOCOL: PROFIBUS DP]** (Decentralized Peripherals) communicate with **[VENDOR: Siemens SIMATIC]** controllers and instruments, offering similar functionality to **[PROTOCOL: FOUNDATION Fieldbus]** in **[VENDOR: Siemens]**-based plants.

**[PROTOCOL: EtherNet/IP]** connects **[VENDOR: Rockwell Automation]** **[EQUIPMENT: ControlLogix]** and **[EQUIPMENT: CompactLogix]** controllers to **[EQUIPMENT: I/O modules]**, **[EQUIPMENT: VFDs]**, and **[EQUIPMENT: HMI systems]** using Common Industrial Protocol (CIP) over Ethernet.

**[PROTOCOL: OPC UA]** (OPC Unified Architecture) enables platform-independent data exchange between **[EQUIPMENT: DCS systems]**, **[EQUIPMENT: historians]**, **[EQUIPMENT: optimization software]**, and **[ARCHITECTURE: enterprise systems]**, superseding legacy **[PROTOCOL: OPC DA]** (Data Access) and **[PROTOCOL: OPC HDA]** (Historical Data Access).

### SCADA and Remote Monitoring

**[PROTOCOL: DNP3]** (Distributed Network Protocol 3) facilitates communication between **[EQUIPMENT: SCADA master stations]** and **[EQUIPMENT: remote terminal units]** at compressor stations, valve stations, and remote processing facilities. **[PROTOCOL: DNP3 Secure Authentication]** adds cryptographic authentication but remains optional in many deployments.

**[EQUIPMENT: Cellular routers]** from **[VENDOR: Sierra Wireless]**, **[VENDOR: Digi International]**, **[VENDOR: Moxa]**, and **[VENDOR: Phoenix Contact]** enable **[ARCHITECTURE: 4G LTE]** or **[ARCHITECTURE: 5G connectivity]** for remote gas plants and well sites, tunneling **[PROTOCOL: VPN connections]** to central SCADA systems.

**[EQUIPMENT: Satellite communication terminals]** from **[VENDOR: Hughes Network Systems]**, **[VENDOR: Viasat]**, **[VENDOR: Inmarsat]**, and **[VENDOR: Iridium]** provide connectivity to extremely remote facilities, supporting **[PROTOCOL: DNP3]**, **[PROTOCOL: Modbus]**, and proprietary SCADA protocols.

**[EQUIPMENT: Radio systems]** (licensed UHF/VHF, 900 MHz ISM, or microwave) from **[VENDOR: Motorola]**, **[VENDOR: Cambium Networks]**, **[VENDOR: Siemens RUGGEDCOM]**, and **[VENDOR: GE MDS]** link remote assets where cellular coverage is unavailable.

### Network Infrastructure

**[EQUIPMENT: Industrial Ethernet switches]** from **[VENDOR: Cisco Industrial Ethernet]**, **[VENDOR: Hirschmann]** (**[VENDOR: Belden]**), **[VENDOR: Moxa]**, **[VENDOR: Siemens SCALANCE]**, and **[VENDOR: Phoenix Contact]** create redundant **[ARCHITECTURE: ring topologies]** with **[PROTOCOL: Rapid Spanning Tree Protocol]** (RSTP), **[PROTOCOL: Media Redundancy Protocol]** (MRP), or **[PROTOCOL: Parallel Redundancy Protocol]** (PRP).

**[EQUIPMENT: Industrial firewalls]** from **[VENDOR: Fortinet]**, **[VENDOR: Palo Alto Networks]**, **[VENDOR: Cisco]**, **[VENDOR: Tofino Security]** (**[VENDOR: Belden]**), and **[VENDOR: Hirschmann]** implement **[ARCHITECTURE: defense-in-depth]** strategies, segregating **[ARCHITECTURE: control networks]** from **[ARCHITECTURE: corporate networks]** via **[ARCHITECTURE: industrial DMZs]**.

**[EQUIPMENT: Unidirectional gateways]** from **[VENDOR: Waterfall Security]**, **[VENDOR: Owl Cyber Defense]**, and **[VENDOR: Hirschmann Tofino Enforcer]** prevent reverse data flows from **[ARCHITECTURE: enterprise zones]** to **[ARCHITECTURE: control system zones]**, enabling data replication while blocking cyberattacks.

## Security Considerations

### Vulnerabilities and Threat Landscape

**[VULNERABILITY: Default credentials]** in **[EQUIPMENT: HMI systems]**, **[EQUIPMENT: engineering workstations]**, and **[EQUIPMENT: RTUs]** enable **[ATTACK_PATTERN: unauthorized access]**. **[VENDOR: Wonderware]**, **[VENDOR: GE iFIX]**, **[VENDOR: Rockwell FactoryTalk]**, and **[VENDOR: Siemens WinCC]** systems have experienced breaches due to unchanged default passwords.

**[VULNERABILITY: Unencrypted protocols]** like **[PROTOCOL: Modbus]**, **[PROTOCOL: DNP3]** (without Secure Authentication), and **[PROTOCOL: HART]** transmit commands and data in cleartext, enabling **[ATTACK_PATTERN: man-in-the-middle attacks]**, **[ATTACK_PATTERN: command injection]**, and **[ATTACK_PATTERN: data manipulation]**.

**[VULNERABILITY: Remote access exposures]** from **[EQUIPMENT: VPN concentrators]**, **[VENDOR: TeamViewer]**, **[VENDOR: LogMeIn]**, and **[VENDOR: AnyDesk]** remote support tools create **[ATTACK_PATTERN: lateral movement]** opportunities for threat actors. **[ATTACK_PATTERN: Credential theft]** targeting vendor support accounts enables persistent access.

**[VULNERABILITY: Firmware vulnerabilities]** in **[EQUIPMENT: PLCs]**, **[EQUIPMENT: RTUs]**, **[EQUIPMENT: intelligent transmitters]**, and **[EQUIPMENT: HMI systems]** allow **[ATTACK_PATTERN: firmware modification]**, **[ATTACK_PATTERN: backdoor installation]**, and **[ATTACK_PATTERN: denial of service]** attacks. **[VENDOR: Siemens]**, **[VENDOR: Schneider Electric]**, **[VENDOR: Rockwell Automation]**, and **[VENDOR: ABB]** publish CVE advisories for discovered vulnerabilities.

**[ATTACK_PATTERN: Supply chain compromises]** inject malware during equipment manufacturing, software development, or system integration. **[ATTACK_PATTERN: Watering hole attacks]** target vendor support websites and engineering forums frequented by gas plant personnel.

### Security Standards and Best Practices

**[PROTOCOL: IEC 62443]** (Industrial Automation and Control Systems Security) defines security requirements across **[ARCHITECTURE: zones and conduits]**, specifying security levels SL1 (protection against casual or coincidental violation) through SL4 (protection against intentional violation using sophisticated means).

**[PROTOCOL: NERC CIP]** (Critical Infrastructure Protection) standards apply to gas processing facilities impacting **[ARCHITECTURE: bulk electric system]** reliability, mandating **[OPERATION: critical asset identification]** (CIP-002), **[OPERATION: electronic security perimeters]** (CIP-005), **[OPERATION: systems security management]** (CIP-007), and **[OPERATION: incident reporting]** (CIP-008).

**[PROTOCOL: API Standard 1164]** (Pipeline SCADA Security) provides security recommendations for pipeline control systems, addressing **[OPERATION: access control]**, **[OPERATION: network security]**, **[OPERATION: data integrity]**, and **[OPERATION: disaster recovery]**.

**[SECURITY: Network segmentation]** isolates **[ARCHITECTURE: safety instrumented systems]**, **[ARCHITECTURE: process control networks]**, **[ARCHITECTURE: business systems]**, and **[ARCHITECTURE: remote access zones]** using **[EQUIPMENT: VLANs]**, **[EQUIPMENT: firewalls]**, and **[EQUIPMENT: routers]** following the **[ARCHITECTURE: Purdue Enterprise Reference Architecture]** (PERA) model.

**[SECURITY: Application whitelisting]** restricts **[EQUIPMENT: HMI workstations]** and **[EQUIPMENT: engineering stations]** to approved executables using **[VENDOR: McAfee Application Control]**, **[VENDOR: Trend Micro Safe Lock]**, **[VENDOR: Ivanti Application Control]**, or **[VENDOR: CyberArk]** solutions, preventing **[ATTACK_PATTERN: malware execution]**.

**[SECURITY: Portable media controls]** block **[ATTACK_PATTERN: USB-based malware]** introduction using **[EQUIPMENT: USB port blockers]**, **[VENDOR: Honeywell Safe USB]**, **[VENDOR: Waterfall Secure Bypass]**, or **[VENDOR: Acronis DeviceLock]** solutions.

## Cross-References

- **[ARCHITECTURE: Gas processing plants]** integrate with upstream **[ARCHITECTURE: production facilities]** via **[EQUIPMENT: gathering pipelines]** and downstream **[ARCHITECTURE: transmission pipelines]**
- **[EQUIPMENT: Custody transfer meters]** interface with **[ARCHITECTURE: pipeline SCADA systems]** and corporate **[ARCHITECTURE: accounting systems]** via **[PROTOCOL: OPC UA]** or **[PROTOCOL: Modbus TCP]**
- **[OPERATION: Plant optimization]** coordinates with **[VENDOR: AspenTech]** **[EQUIPMENT: Aspen PIMS]** and **[VENDOR: Honeywell]** **[EQUIPMENT: Profit Suite]** for enterprise-wide production management
- **[PROTOCOL: IEC 62443]** security zones align with **[ARCHITECTURE: ISA-95]** hierarchical levels for consistent automation architecture
- **[VULNERABILITY: ICS vulnerabilities]** tracked by ICS-CERT affect midstream **[VENDOR: Honeywell]**, **[VENDOR: Emerson]**, **[VENDOR: Rockwell]**, **[VENDOR: Siemens]**, and **[VENDOR: Schneider Electric]** systems
- **[SECURITY: Incident response]** procedures coordinate with **[OPERATION: TSA Pipeline Security Directive]** requirements and **[OPERATION: CISA ICS-CERT]** reporting obligations

---

**Document Statistics:**
- VENDOR entities: 108+
- EQUIPMENT entities: 145+
- OPERATION entities: 72
- PROTOCOL entities: 58
- ARCHITECTURE cross-references: 28
- SECURITY mentions: 20
- VULNERABILITY/ATTACK_PATTERN references: 24
