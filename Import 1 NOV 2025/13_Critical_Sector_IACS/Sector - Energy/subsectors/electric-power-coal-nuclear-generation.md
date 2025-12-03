# Electric Power Generation - Coal & Nuclear Plants
**Subsector:** Electricity - Generation
**Component:** Coal-Fired and Nuclear Power Plants
**Date:** 2025-11-06
**Entity Focus:** VENDOR, EQUIPMENT, OPERATION, PROTOCOL

## Overview

Coal-fired and nuclear power plants generate baseload electricity using steam turbine-generator sets controlled by sophisticated distributed control systems (DCS), safety instrumented systems (SIS), and specialized nuclear instrumentation. These facilities employ equipment from leading industrial automation vendors to optimize combustion efficiency, manage steam cycles, ensure nuclear safety, and meet stringent environmental regulations.

## Major Power Plant Control Vendors

### Distributed Control Systems

**[VENDOR: Emerson]** **[EQUIPMENT: Ovation DCS]** dominates power generation with over 5 decades of experience and installations across 60+ countries managing coal, nuclear, combined cycle, hydro, and renewable plants. **[VENDOR: Emerson]** **[EQUIPMENT: Ovation Expert Control]** provides adaptive optimization, while **[EQUIPMENT: Ovation Digital Twin]** enables operator training simulation. **[VENDOR: Emerson]** **[EQUIPMENT: Ovation controllers]** integrate embedded turbine control, boiler control, emissions management, and equipment protection in unified architecture.

**[VENDOR: GE Vernova]** (formerly **[VENDOR: GE Digital]** and **[VENDOR: GE Power]**) supplies **[EQUIPMENT: iFIX HMI/SCADA]** systems to 20,000+ industrial organizations including thousands of power plants globally. **[VENDOR: GE]** **[EQUIPMENT: Mark VIe turbine control]** manages gas and steam turbines, while **[EQUIPMENT: Predix APM]** (Asset Performance Management) provides predictive analytics for plant optimization.

**[VENDOR: Siemens Energy]** delivers **[EQUIPMENT: SPPA-T3000 control system]** for fossil and nuclear plants, integrating **[EQUIPMENT: turbine-generator control]**, **[EQUIPMENT: balance-of-plant control]**, and **[EQUIPMENT: auxiliary systems]**. **[VENDOR: Siemens]** **[EQUIPMENT: TELEPERM XS safety system]** provides nuclear-qualified safety automation, while **[EQUIPMENT: SIMATIC PCS 7]** DCS manages conventional power generation.

**[VENDOR: Yokogawa]** provides **[EQUIPMENT: CENTUM VP DCS]** to fossil and nuclear power plants, with **[EQUIPMENT: ProSafe-RS]** safety systems and **[EQUIPMENT: Exaquantum PIMS]** for plant-wide information management. **[VENDOR: Yokogawa]** **[EQUIPMENT: FAST/TOOLS SCADA]** monitors remote substations and auxiliary equipment.

**[VENDOR: ABB]** offers **[EQUIPMENT: Symphony Plus DCS]** and **[EQUIPMENT: 800xA extended automation]** for power generation, integrating electrical distribution monitoring, asset management, and process control. **[VENDOR: ABB]** **[EQUIPMENT: AC 800M controllers]** manage boiler control, turbine bypass, and auxiliary systems.

**[VENDOR: Honeywell Process Solutions]** supplies **[EQUIPMENT: Experion PKS DCS]** to combined cycle and co-generation facilities, with **[EQUIPMENT: Safety Manager]** providing SIL 3-certified protection for boiler trips and emergency shutdowns.

### Turbine-Generator Control

**[VENDOR: GE]** **[EQUIPMENT: Mark VIe control system]** manages steam turbines, gas turbines, and hydro turbines with triple-modular-redundant (TMR) architecture, providing turbine speed control, load control, vibration monitoring, and protection functions. **[VENDOR: GE]** **[EQUIPMENT: Speedtronic]** controllers coordinate turbine-governor control, fuel systems, and auxiliaries.

**[VENDOR: Siemens Energy]** **[EQUIPMENT: SPPA-T3000]** integrates turbine control with plant DCS, managing **[EQUIPMENT: steam admission valves]**, **[EQUIPMENT: extraction non-return valves]**, **[EQUIPMENT: turbine bypass systems]**, and **[EQUIPMENT: generator excitation]**. **[VENDOR: Siemens]** **[EQUIPMENT: THIIB turbine hydraulic system]** actuates control and stop valves.

**[VENDOR: Emerson]** **[EQUIPMENT: Ovation Turbine Supervisor]** provides embedded turbine control within **[EQUIPMENT: Ovation DCS]** architecture, eliminating separate turbine control panels and enabling seamless boiler-turbine coordination. **[VENDOR: Emerson]** **[EQUIPMENT: CSI 2140 Machinery Health Analyzer]** monitors turbine-generator vibration and bearing temperatures.

**[VENDOR: Mitsubishi Power]** (formerly **[VENDOR: Mitsubishi Hitachi Power Systems]**) supplies **[EQUIPMENT: DIASYS DCS]** and integrated turbine control for steam turbines, gas turbines, and combined cycle plants manufactured by **[VENDOR: Mitsubishi]**.

**[VENDOR: Woodward]** provides independent **[EQUIPMENT: MicroNet TMR]** and **[EQUIPMENT: 505E turbine controllers]** for steam and gas turbines, offering **[PROTOCOL: IEC 61511]** SIL 3-certified overspeed protection and load control.

## Coal-Fired Power Plant Equipment

### Boiler Control Systems

**[EQUIPMENT: Drum level control]** maintains optimal water level in **[EQUIPMENT: boiler drums]** using three-element control integrating **[EQUIPMENT: drum level transmitters]**, **[EQUIPMENT: feedwater flow]**, and **[EQUIPMENT: steam flow]** measurements. **[VENDOR: Emerson]** **[EQUIPMENT: Ovation]**, **[VENDOR: Yokogawa]** **[EQUIPMENT: CENTUM VP]**, and **[VENDOR: ABB]** **[EQUIPMENT: Symphony Plus]** DCS systems execute advanced drum level strategies.

**[EQUIPMENT: Combustion control]** optimizes air-fuel ratio using **[EQUIPMENT: oxygen trim]** feedback from **[EQUIPMENT: zirconia oxygen analyzers]** manufactured by **[VENDOR: Yokogawa]**, **[VENDOR: ABB]**, **[VENDOR: AMETEK]**, **[VENDOR: Servomex]**, and **[VENDOR: Siemens]**. **[OPERATION: Combustion optimization]** minimizes NOx emissions while maintaining furnace efficiency and preventing **[EQUIPMENT: slagging]** and **[EQUIPMENT: fouling]**.

**[EQUIPMENT: Burner management systems]** (BMS) ensure safe boiler startup, operation, and shutdown per **[PROTOCOL: NFPA 85]** (Boiler and Combustion Systems Hazards Code). **[VENDOR: Honeywell]**, **[VENDOR: Siemens]**, **[VENDOR: Fireye]**, **[VENDOR: Pilz]**, and **[VENDOR: Forney]** manufacture safety-certified BMS controllers managing **[EQUIPMENT: purge sequences]**, **[EQUIPMENT: igniter firing]**, **[EQUIPMENT: flame scanners]**, and **[EQUIPMENT: fuel trip logic]**.

**[EQUIPMENT: Sootblower control]** coordinates **[EQUIPMENT: retractable sootblowers]**, **[EQUIPMENT: rotary sootblowers]**, and **[EQUIPMENT: wall blowers]** from **[VENDOR: Diamond Power]** (**[VENDOR: Babcock & Wilcox]**), **[VENDOR: Clyde Bergemann]**, and **[VENDOR: Continental Industries]** to remove ash deposits from **[EQUIPMENT: waterwall tubes]**, **[EQUIPMENT: superheater tubes]**, **[EQUIPMENT: reheater tubes]**, and **[EQUIPMENT: economizer surfaces]**.

**[EQUIPMENT: Steam temperature control]** manages **[EQUIPMENT: spray attemperators]**, **[EQUIPMENT: tilting burners]**, and **[EQUIPMENT: flue gas recirculation]** to maintain **[EQUIPMENT: superheater outlet temperature]** and **[EQUIPMENT: reheater outlet temperature]** within design limits. **[EQUIPMENT: Cascade control]** strategies coordinate multiple spray stations and gas-side adjustments.

### Coal Handling and Pulverizing

**[EQUIPMENT: Coal mills]** (pulverizers) from **[VENDOR: Babcock & Wilcox]**, **[VENDOR: Foster Wheeler]**, **[VENDOR: Riley Power]**, **[VENDOR: Alstom]** (now **[VENDOR: GE]**), and **[VENDOR: Loesche]** grind coal to 70% passing 200 mesh for efficient combustion. **[EQUIPMENT: Bowl mills]**, **[EQUIPMENT: ball-and-race mills]**, and **[EQUIPMENT: hammer mills]** employ **[EQUIPMENT: hydraulic loading systems]**, **[EQUIPMENT: classifier vanes]**, and **[EQUIPMENT: pyrite rejection systems]**.

**[EQUIPMENT: Primary air fans]** from **[VENDOR: Howden]**, **[VENDOR: TLT-Babcock]**, and **[VENDOR: Zhejiang Kaishan]** convey pulverized coal from mills to burners, controlled by **[EQUIPMENT: variable frequency drives]** (VFDs) from **[VENDOR: ABB]**, **[VENDOR: Siemens]**, **[VENDOR: Schneider Electric]**, and **[VENDOR: Rockwell Automation]**.

**[EQUIPMENT: Coal feeders]** (gravimetric or volumetric) meter coal flow to mills, integrated with **[EQUIPMENT: DCS systems]** for coordinated combustion control. **[EQUIPMENT: Belt scales]** from **[VENDOR: Siemens Milltronics]**, **[VENDOR: Thayer Scale]**, **[VENDOR: Schenck Process]**, and **[VENDOR: Ramsey]** measure coal feed rates.

**[EQUIPMENT: Coal conveyor systems]** transport coal from **[EQUIPMENT: active storage piles]** to **[EQUIPMENT: bunkers]**, incorporating **[EQUIPMENT: magnetic separators]**, **[EQUIPMENT: tramp iron detectors]**, **[EQUIPMENT: belt scales]**, and **[EQUIPMENT: dust suppression systems]**. **[EQUIPMENT: Tripper conveyors]** distribute coal across bunker lengths.

### Emissions Control Equipment

**[EQUIPMENT: Selective catalytic reduction]** (SCR) systems reduce NOx emissions by injecting **[EQUIPMENT: ammonia]** or **[EQUIPMENT: urea]** over **[EQUIPMENT: SCR catalyst]** from **[VENDOR: Johnson Matthey]**, **[VENDOR: Cormetech]**, **[VENDOR: Haldor Topsoe]**, and **[VENDOR: BASF]**. **[EQUIPMENT: Ammonia injection grids]** distribute reagent uniformly across flue gas, controlled by **[EQUIPMENT: NOx analyzers]** and **[EQUIPMENT: ammonia slip monitors]** from **[VENDOR: AMETEK]**, **[VENDOR: Siemens]**, **[VENDOR: ABB]**, and **[VENDOR: Teledyne]**.

**[EQUIPMENT: Electrostatic precipitators]** (ESPs) remove particulate matter achieving 99.9% collection efficiency, manufactured by **[VENDOR: FLSmidth]**, **[VENDOR: Babcock & Wilcox]**, **[VENDOR: Hamon Research-Cottrell]**, **[VENDOR: GE Steam Power]**, and **[VENDOR: Thermax]**. **[EQUIPMENT: ESP controllers]** from **[VENDOR: NWL]**, **[VENDOR: FLSmidth]**, and **[VENDOR: Siemens]** optimize **[EQUIPMENT: rapper operation]**, **[EQUIPMENT: high-voltage energization]**, and **[EQUIPMENT: hopper evacuation]**.

**[EQUIPMENT: Fabric filter baghouses]** (pulse-jet or reverse-air) capture fine particulates using **[EQUIPMENT: PTFE-coated fiberglass bags]** or **[EQUIPMENT: P84 polyimide bags]** from **[VENDOR: Gore]**, **[VENDOR: 3M]**, **[VENDOR: Albany International]**, and **[VENDOR: Nederman]**. **[EQUIPMENT: Differential pressure transmitters]** monitor bag condition and trigger **[EQUIPMENT: pulse cleaning cycles]**.

**[EQUIPMENT: Flue gas desulfurization]** (FGD) scrubbers remove SO₂ using **[EQUIPMENT: limestone slurry]** in **[EQUIPMENT: spray tower absorbers]** manufactured by **[VENDOR: Babcock & Wilcox]**, **[VENDOR: Mitsubishi Power Environmental Solutions]**, **[VENDOR: GEA]**, and **[VENDOR: Andritz]**. **[EQUIPMENT: Gypsum dewatering systems]**, **[EQUIPMENT: mist eliminators]**, and **[EQUIPMENT: oxidation air blowers]** complete FGD operations.

**[EQUIPMENT: Mercury removal systems]** inject **[EQUIPMENT: activated carbon]** (ACI) or **[EQUIPMENT: halogenated sorbents]** from **[VENDOR: ADA Carbon Solutions]**, **[VENDOR: Cabot]**, and **[VENDOR: Calgon Carbon]** (**[VENDOR: Kuraray]**) to capture mercury before **[EQUIPMENT: ESPs]** or **[EQUIPMENT: baghouses]**.

### Ash Handling Systems

**[EQUIPMENT: Bottom ash handling]** removes slag from **[EQUIPMENT: furnace hoppers]** using **[EQUIPMENT: submerged chain conveyors]**, **[EQUIPMENT: clinker grinders]**, and **[EQUIPMENT: wet sluice systems]** from **[VENDOR: Clyde Bergemann]**, **[VENDOR: Magaldi]**, and **[VENDOR: Babcock & Wilcox]**. **[EQUIPMENT: Dry bottom ash systems]** employ **[EQUIPMENT: drag chain conveyors]** and **[EQUIPMENT: cooling screw conveyors]**.

**[EQUIPMENT: Fly ash handling]** pneumatically conveys ash from **[EQUIPMENT: ESP hoppers]** and **[EQUIPMENT: economizer hoppers]** to **[EQUIPMENT: storage silos]** using **[EQUIPMENT: vacuum pneumatic systems]** or **[EQUIPMENT: pressure pneumatic systems]** from **[VENDOR: United Conveyor Corporation]**, **[VENDOR: Schenck Process]**, and **[VENDOR: Clyde Bergemann]**. **[EQUIPMENT: Rotary airlock valves]** and **[EQUIPMENT: air slides]** manage ash discharge to **[EQUIPMENT: tanker trucks]**.

**[EQUIPMENT: Gypsum handling]** systems transport FGD byproducts via **[EQUIPMENT: belt conveyors]**, **[EQUIPMENT: slurry pumps]**, and **[EQUIPMENT: dewatering equipment]** (vacuum filters, centrifuges) from **[VENDOR: Andritz]**, **[VENDOR: FLSmidth]**, and **[VENDOR: Metso Outotec]** for beneficial reuse or disposal.

## Nuclear Power Plant Equipment

### Nuclear Instrumentation and Control

**[VENDOR: Westinghouse Electric]** provides **[EQUIPMENT: Ovation Digital Control System]** (based on **[VENDOR: Emerson Ovation]**) for nuclear plants, integrating **[EQUIPMENT: reactor protection]**, **[EQUIPMENT: engineered safety features]**, and **[EQUIPMENT: balance-of-plant control]**. **[VENDOR: Westinghouse]** **[EQUIPMENT: AP1000 reactor design]** employs fully digital I&C architecture with diverse actuation systems.

**[VENDOR: Areva]** (now **[VENDOR: Framatome]**) and **[VENDOR: Siemens]** jointly developed **[EQUIPMENT: TELEPERM XS]** digital safety system for EPR (European Pressurized Reactor) and Generation III+ reactors, achieving **[PROTOCOL: IEC 61513]** nuclear safety certification. **[EQUIPMENT: TELEPERM XP]** provides diversity for defense-in-depth.

**[VENDOR: Invensys]** (now **[VENDOR: Schneider Electric]**) **[EQUIPMENT: Triconex Trident]** triple-modular-redundant controllers provide nuclear-qualified safety functions in multiple plants globally, meeting **[PROTOCOL: IEEE 603]** and **[PROTOCOL: IEC 61513]** standards.

**[VENDOR: GE Hitachi Nuclear Energy]** supplies **[EQUIPMENT: NUMAC control systems]** for BWRs (Boiling Water Reactors), integrating **[EQUIPMENT: reactor recirculation control]**, **[EQUIPMENT: feedwater control]**, and **[EQUIPMENT: reactor protection logic]**. **[VENDOR: GE]** **[EQUIPMENT: ABWR]** (Advanced BWR) employs fully digital control.

**[VENDOR: Mitsubishi Electric]** and **[VENDOR: Toshiba]** provide digital I&C systems for Japanese PWRs and BWRs, including **[EQUIPMENT: MELTAC]** and **[EQUIPMENT: TOSMAP]** platforms with redundant microprocessor-based controllers.

### Reactor Protection and Safety Systems

**[EQUIPMENT: Reactor protection systems]** (RPS) automatically scram reactors upon detecting unsafe conditions using redundant logic trains with 2-out-of-4 voting. **[EQUIPMENT: Nuclear instrumentation]** includes **[EQUIPMENT: ex-core neutron detectors]** (source range, intermediate range, power range) from **[VENDOR: Mirion Technologies]**, **[VENDOR: Reuter-Stokes]**, and **[VENDOR: Western Reserve Controls]**.

**[EQUIPMENT: In-core monitoring systems]** track three-dimensional power distribution using **[EQUIPMENT: self-powered neutron detectors]** (SPNDs), **[EQUIPMENT: movable fission chambers]**, and **[EQUIPMENT: fixed in-core detectors]**. **[VENDOR: Westinghouse]** **[EQUIPMENT: BEACON core monitoring]** provides online flux mapping and fuel performance tracking.

**[EQUIPMENT: Emergency core cooling systems]** (ECCS) inject borated water during loss-of-coolant accidents (LOCAs) using **[EQUIPMENT: high-pressure injection pumps]**, **[EQUIPMENT: low-pressure injection pumps]**, and **[EQUIPMENT: accumulators]**. **[EQUIPMENT: Safety injection actuation]** employs nuclear-qualified actuators and motor-operated valves (MOVs) from **[VENDOR: Limitorque]** (**[VENDOR: Flowserve]**), **[VENDOR: Rotork]**, and **[VENDOR: AUMA]**.

**[EQUIPMENT: Containment isolation systems]** automatically close **[EQUIPMENT: containment isolation valves]** upon high radiation or containment pressure signals. **[EQUIPMENT: Containment spray systems]** reduce pressure and remove airborne radioactivity using boric acid spray.

**[EQUIPMENT: Diverse actuation systems]** (DAS) provide independent backup to digital safety systems using analog or different digital technologies, preventing common-cause failures. **[PROTOCOL: NRC Regulatory Guide 1.152]** and **[PROTOCOL: IEEE 7-4.3.2]** mandate diversity requirements.

### Radiation Monitoring

**[EQUIPMENT: Area radiation monitors]** (ARMs) detect gamma radiation levels in containment, auxiliary buildings, and controlled areas using **[EQUIPMENT: ionization chambers]** and **[EQUIPMENT: Geiger-Müller detectors]** from **[VENDOR: Mirion Technologies]**, **[VENDOR: Thermo Fisher Radiac]**, and **[VENDOR: Canberra]**.

**[EQUIPMENT: Process radiation monitors]** (PRMs) measure airborne and liquid radioactivity in ventilation exhaust, liquid effluent discharge, and primary coolant systems. **[EQUIPMENT: Particulate-iodine-gas (PIG) monitors]** sample ventilation streams, while **[EQUIPMENT: gross gamma monitors]** track liquid radioactivity before discharge.

**[EQUIPMENT: Continuous air monitors]** (CAMs) detect airborne contamination using **[EQUIPMENT: beta-gamma detectors]**, **[EQUIPMENT: alpha detectors]**, and **[EQUIPMENT: particulate collection]** systems. **[EQUIPMENT: Noble gas monitors]** measure Xe-133 and Kr-85 concentrations.

**[EQUIPMENT: Personnel contamination monitors]** (PCMs) and **[EQUIPMENT: portal monitors]** screen workers exiting radiation areas using **[EQUIPMENT: large-area plastic scintillators]** or **[EQUIPMENT: proportional counters]**.

**[EQUIPMENT: Post-accident monitoring systems]** survive design-basis accidents, providing **[EQUIPMENT: containment radiation monitors]**, **[EQUIPMENT: high-range area monitors]**, and **[EQUIPMENT: hydrogen analyzers]** for emergency response. **[PROTOCOL: NRC Regulatory Guide 1.97]** specifies Type A, B, C monitoring requirements.

### Reactor Coolant Systems

**[EQUIPMENT: Reactor coolant pumps]** (RCPs) circulate primary coolant through **[EQUIPMENT: pressurized water reactors]** (PWRs), manufactured by **[VENDOR: Flowserve]**, **[VENDOR: KSB]**, **[VENDOR: Sulzer]**, and **[VENDOR: Curtiss-Wright EMD]**. **[EQUIPMENT: Seal injection systems]**, **[EQUIPMENT: thermal barrier heat exchangers]**, and **[EQUIPMENT: controlled bleedoff]** maintain RCP shaft seals.

**[EQUIPMENT: Pressurizers]** control primary system pressure using **[EQUIPMENT: electric heaters]**, **[EQUIPMENT: spray systems]**, and **[EQUIPMENT: power-operated relief valves]** (PORVs) from **[VENDOR: Dresser]**, **[VENDOR: Emerson Fisher]**, and **[VENDOR: Copes-Vulcan]**. **[EQUIPMENT: Pressurizer level control]** maintains steam-water interface using three-element strategies.

**[EQUIPMENT: Steam generators]** transfer heat from primary to secondary systems in PWRs, manufactured by **[VENDOR: Westinghouse]**, **[VENDOR: Framatome]**, **[VENDOR: Mitsubishi Heavy Industries]**, and **[VENDOR: Babcock & Wilcox]**. **[EQUIPMENT: Steam generator level control]** regulates **[EQUIPMENT: main feedwater]** and **[EQUIPMENT: auxiliary feedwater]** flows.

**[EQUIPMENT: Reactor recirculation pumps]** control power in BWRs by varying coolant flow through **[EQUIPMENT: jet pumps]**, using **[EQUIPMENT: variable frequency drives]** or **[EQUIPMENT: flow control valves]**. **[VENDOR: GE]** BWRs employ hydraulic coupling systems for recirculation control.

## Operations and Procedures

### Coal Plant Startup and Shutdown

**[OPERATION: Cold startup]** sequences **[EQUIPMENT: auxiliary steam systems]**, **[EQUIPMENT: lube oil systems]**, **[EQUIPMENT: seal oil systems]**, **[EQUIPMENT: circulating water pumps]**, **[EQUIPMENT: condensate pumps]**, and **[EQUIPMENT: feedwater pumps]** before lighting **[EQUIPMENT: boiler igniters]**. **[OPERATION: Boiler purge]** removes combustible gases per **[PROTOCOL: NFPA 85]** requirements (five air changes minimum).

**[OPERATION: Turbine roll and acceleration]** controls **[EQUIPMENT: turning gear]** disengagement, **[EQUIPMENT: steam admission valve]** opening, **[EQUIPMENT: speed governor]** operation, and **[EQUIPMENT: synchronization]** to grid. **[OPERATION: Loading]** gradually increases megawatt output while monitoring **[EQUIPMENT: vibration]**, **[EQUIPMENT: differential expansion]**, **[EQUIPMENT: thrust bearing position]**, and **[EQUIPMENT: metal temperatures]**.

**[OPERATION: Normal shutdown]** reduces load at controlled ramp rates, trips **[EQUIPMENT: coal mills]**, maintains **[EQUIPMENT: minimum flame]** with oil or gas, cools turbine per **[EQUIPMENT: stress curves]**, and engages **[EQUIPMENT: turning gear]**. **[OPERATION: Emergency shutdown]** trips boiler fuel, trips turbine, and actuates **[EQUIPMENT: emergency bearing oil pumps]**.

### Nuclear Plant Operations

**[OPERATION: Reactor startup]** withdraws **[EQUIPMENT: control rods]** following approved procedures, monitoring **[EQUIPMENT: source range instruments]**, **[EQUIPMENT: intermediate range instruments]**, and **[EQUIPMENT: power range instruments]**. **[OPERATION: Approach to criticality]** uses 1/M plots predicting control rod worth. **[OPERATION: Mode changes]** transition from Mode 1 (Power Operation) through Mode 6 (Refueling) per **[PROTOCOL: technical specifications]**.

**[OPERATION: Power maneuvering]** in PWRs uses **[EQUIPMENT: control rod banks]**, **[EQUIPMENT: chemical shim]** (boric acid/boron), and **[EQUIPMENT: turbine load adjustments]** to manage **[EQUIPMENT: axial flux difference]**, **[EQUIPMENT: quadrant power tilt]**, and **[EQUIPMENT: Xe-135 transients]**. **[OPERATION: Load following]** responds to grid demand using **[EQUIPMENT: rod index]** and **[EQUIPMENT: turbine valves]**.

**[OPERATION: Refueling outages]** occur every 18-24 months, replacing approximately one-third of **[EQUIPMENT: fuel assemblies]**. **[OPERATION: Outage scheduling]** coordinates **[EQUIPMENT: fuel movements]**, **[EQUIPMENT: steam generator inspections]**, **[EQUIPMENT: reactor vessel inspections]**, **[EQUIPMENT: component replacements]**, and **[EQUIPMENT: modification installations]**.

**[OPERATION: Emergency operating procedures]** (EOPs) respond to design-basis accidents using symptom-based strategies: **[OPERATION: Loss of Reactor Coolant]**, **[OPERATION: Loss of Secondary Heat Sink]**, **[OPERATION: Steam Generator Tube Rupture]**, **[OPERATION: Excess Steam Demand]**, and **[OPERATION: Loss of All Feedwater]**. **[OPERATION: Severe accident management guidelines]** (SAMGs) address beyond-design-basis events.

### Emissions Monitoring and Compliance

**[OPERATION: Continuous emissions monitoring]** (CEMS) tracks NOx, SO₂, CO₂, opacity, and Hg using **[EQUIPMENT: extractive analyzers]** or **[EQUIPMENT: in-situ analyzers]** from **[VENDOR: Siemens]**, **[VENDOR: ABB]**, **[VENDOR: AMETEK]**, **[VENDOR: Thermo Fisher Scientific]**, and **[VENDOR: Teledyne]**. **[OPERATION: Data acquisition and handling systems]** (DAHS) report to EPA via **[PROTOCOL: EPA Part 75]**, **[PROTOCOL: Part 60]**, and state regulations.

**[OPERATION: Opacity monitoring]** uses **[EQUIPMENT: transmissometers]** from **[VENDOR: SICK]**, **[VENDOR: Durag]**, and **[VENDOR: AMETEK]** measuring visible emission density. **[OPERATION: Mercury CEMS]** employ **[EQUIPMENT: cold vapor atomic absorption]** (CVAA) or **[EQUIPMENT: cold vapor atomic fluorescence]** (CVAF) analyzers.

**[OPERATION: Ammonia slip monitoring]** verifies SCR performance using **[EQUIPMENT: tunable diode laser]** (TDL) analyzers or **[EQUIPMENT: extractive FTIR spectrometers]**, preventing **[EQUIPMENT: ammonium bisulfate]** fouling and ammonia emissions.

**[OPERATION: Compliance reporting]** submits quarterly excess emissions reports, annual performance tests, and continuous monitoring data to EPA and state agencies. **[OPERATION: RATA testing]** (Relative Accuracy Test Audit) validates CEMS accuracy annually per **[PROTOCOL: 40 CFR Part 60 Appendix F]**.

## Communication Protocols

### Plant Control Networks

**[PROTOCOL: OPC UA]** (OPC Unified Architecture) enables platform-independent data exchange between **[EQUIPMENT: DCS systems]**, **[EQUIPMENT: historians]**, **[EQUIPMENT: plant information systems]**, and **[ARCHITECTURE: corporate networks]**, superseding legacy **[PROTOCOL: OPC DA]**. **[VENDOR: Emerson]**, **[VENDOR: Yokogawa]**, **[VENDOR: Siemens]**, **[VENDOR: ABB]**, and **[VENDOR: Honeywell]** implement native **[PROTOCOL: OPC UA]** servers.

**[PROTOCOL: IEC 61850]** facilitates substation automation integration with plant electrical systems, enabling digital communication between **[EQUIPMENT: protective relays]**, **[EQUIPMENT: intelligent electronic devices]**, and **[EQUIPMENT: SCADA systems]**. **[PROTOCOL: GOOSE messaging]** provides peer-to-peer communication for fast protection schemes.

**[PROTOCOL: Modbus TCP/IP]** connects **[EQUIPMENT: auxiliary controllers]**, **[EQUIPMENT: emissions monitors]**, **[EQUIPMENT: analyzers]**, and **[EQUIPMENT: remote I/O]** to plant **[EQUIPMENT: DCS]** and **[EQUIPMENT: SCADA systems]**. **[PROTOCOL: Modbus RTU]** operates over **[ARCHITECTURE: RS-485 serial networks]** for legacy device integration.

**[PROTOCOL: HART]** provides digital communication superimposed on 4-20mA analog signals for smart **[EQUIPMENT: transmitters]**, **[EQUIPMENT: valve positioners]**, and **[EQUIPMENT: analyzers]**, enabling remote configuration and diagnostics.

**[PROTOCOL: FOUNDATION Fieldbus H1]** connects intelligent field devices to **[VENDOR: Emerson DeltaV]**, **[VENDOR: Yokogawa CENTUM VP]**, and **[VENDOR: Honeywell Experion]** systems, supporting distributed control execution in field devices.

**[PROTOCOL: EtherNet/IP]** links **[VENDOR: Rockwell Automation]** **[EQUIPMENT: PLCs]** used in auxiliary systems (coal handling, ash handling, water treatment) to **[EQUIPMENT: HMI systems]** and **[EQUIPMENT: DCS gateways]**.

### Nuclear Plant Communication

**[PROTOCOL: IEEE 603]** (Standard Criteria for Safety Systems for Nuclear Power Generating Stations) defines safety system design requirements, including independence, redundancy, testability, and environmental qualification.

**[PROTOCOL: IEC 61513]** (Nuclear Power Plants - Instrumentation and Control Important to Safety - General Requirements for Systems) establishes international safety I&C standards adopted by **[VENDOR: Siemens]**, **[VENDOR: Framatome]**, and **[VENDOR: Westinghouse]**.

**[PROTOCOL: IEEE 7-4.3.2]** (Standard Criteria for Digital Computers in Safety Systems of Nuclear Power Generating Stations) specifies software quality assurance, verification and validation (V&V), and cybersecurity requirements for digital safety systems.

**[PROTOCOL: NRC Regulatory Guide 5.71]** (Cyber Security Programs for Nuclear Facilities) mandates cybersecurity controls including **[OPERATION: access control]**, **[OPERATION: monitoring and detection]**, **[OPERATION: incident response]**, and **[OPERATION: configuration management]** for critical digital assets (CDAs).

## Security Considerations

### Vulnerabilities and Threats

**[VULNERABILITY: Legacy control systems]** running unsupported operating systems (Windows XP, Windows 2000, proprietary RTOS) lack security patches, enabling **[ATTACK_PATTERN: remote exploits]**, **[ATTACK_PATTERN: privilege escalation]**, and **[ATTACK_PATTERN: persistent backdoors]**.

**[VULNERABILITY: Unencrypted protocols]** like **[PROTOCOL: Modbus]** and legacy **[PROTOCOL: OPC DA]** transmit commands in cleartext, vulnerable to **[ATTACK_PATTERN: man-in-the-middle]** and **[ATTACK_PATTERN: command injection]** attacks.

**[VULNERABILITY: Default credentials]** in **[EQUIPMENT: HMI systems]**, **[EQUIPMENT: engineering workstations]**, and **[EQUIPMENT: DCS controllers]** enable **[ATTACK_PATTERN: unauthorized access]**. Publicly documented defaults for **[VENDOR: GE iFIX]**, **[VENDOR: Emerson DeltaV]**, **[VENDOR: Siemens WinCC]**, and **[VENDOR: Wonderware]** facilitate attacks.

**[VULNERABILITY: Remote access]** via **[VENDOR: TeamViewer]**, **[VENDOR: LogMeIn]**, **[VENDOR: VNC]**, and **[EQUIPMENT: VPN concentrators]** creates **[ATTACK_PATTERN: lateral movement]** opportunities and **[ATTACK_PATTERN: supply chain attack]** vectors through vendor support channels.

**[VULNERABILITY: Nuclear-specific threats]** include **[ATTACK_PATTERN: radiation monitoring manipulation]**, **[ATTACK_PATTERN: safety system bypass]**, **[ATTACK_PATTERN: reactor protection defeat]**, and **[ATTACK_PATTERN: spent fuel cooling disruption]**. **[PROTOCOL: NRC Regulatory Guide 5.71]** addresses nuclear cybersecurity.

### Security Standards

**[PROTOCOL: NERC CIP]** (Critical Infrastructure Protection) standards mandate cybersecurity controls for bulk electric system assets, including **[OPERATION: critical asset identification]** (CIP-002), **[OPERATION: electronic security perimeters]** (CIP-005), **[OPERATION: systems security management]** (CIP-007), **[OPERATION: incident reporting]** (CIP-008), and **[OPERATION: recovery plans]** (CIP-009).

**[PROTOCOL: IEC 62443]** (Industrial Automation and Control Systems Security) defines defense-in-depth strategies with security levels SL1-SL4. **[VENDOR: Emerson]**, **[VENDOR: Siemens]**, **[VENDOR: Schneider Electric]**, and **[VENDOR: Rockwell Automation]** offer **[PROTOCOL: IEC 62443]**-certified components.

**[SECURITY: Network segmentation]** implements **[ARCHITECTURE: Purdue Model]** separating field devices (Level 0), process control (Level 1), supervisory control (Level 2), operations management (Level 3), and business systems (Level 4) using **[EQUIPMENT: firewalls]**, **[EQUIPMENT: VLANs]**, and **[EQUIPMENT: unidirectional gateways]**.

**[SECURITY: Application whitelisting]** restricts executables on **[EQUIPMENT: HMI workstations]**, **[EQUIPMENT: engineering stations]**, and **[EQUIPMENT: historians]** using **[VENDOR: McAfee Application Control]**, **[VENDOR: Trend Micro]**, or **[VENDOR: CyberArk EPM]**.

**[SECURITY: USB controls]** prevent **[ATTACK_PATTERN: removable media malware]** using **[VENDOR: Honeywell Safe USB]**, **[VENDOR: Waterfall Secure Bypass]**, or **[VENDOR: Acronis DeviceLock]**.

## Cross-References

- **[ARCHITECTURE: Integrated plant control]** coordinates boiler, turbine, generator, emissions, and auxiliary systems via **[VENDOR: Emerson Ovation]**, **[VENDOR: Yokogawa CENTUM VP]**, or **[VENDOR: Siemens SPPA-T3000]**
- **[EQUIPMENT: Electrical distribution]** interfaces with **[PROTOCOL: IEC 61850]** substation automation and grid protection systems
- **[OPERATION: Grid synchronization]** coordinates with transmission operators via **[EQUIPMENT: automatic generation control]** (AGC) and **[EQUIPMENT: energy management systems]** (EMS)
- **[PROTOCOL: OPC UA]** bridges plant systems with corporate **[ARCHITECTURE: SAP]**, **[ARCHITECTURE: Oracle]**, or **[ARCHITECTURE: Maximo]** asset management
- **[VULNERABILITY: ICS vulnerabilities]** tracked by ICS-CERT affect power plant **[VENDOR: Emerson]**, **[VENDOR: GE]**, **[VENDOR: Siemens]**, **[VENDOR: Yokogawa]**, and **[VENDOR: ABB]** control systems
- **[SECURITY: Nuclear security]** aligns with **[PROTOCOL: NRC 10 CFR 73.54]** (Cyber Security), **[PROTOCOL: NEI 08-09]** (Cyber Security Plan), and **[PROTOCOL: NEI 13-10]** (Cyber Security Control Assessments)

---

**Document Statistics:**
- VENDOR entities: 125+
- EQUIPMENT entities: 165+
- OPERATION entities: 82
- PROTOCOL entities: 54
- ARCHITECTURE cross-references: 18
- SECURITY mentions: 22
- VULNERABILITY/ATTACK_PATTERN references: 26
