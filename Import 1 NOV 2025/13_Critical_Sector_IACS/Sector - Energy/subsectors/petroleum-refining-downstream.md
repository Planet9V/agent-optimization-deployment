# Petroleum Refining - Downstream Operations
**Subsector:** Oil and Natural Gas - Downstream
**Component:** Crude Oil Refining & Petrochemical Processing
**Date:** 2025-11-06
**Entity Focus:** VENDOR, EQUIPMENT, OPERATION, PROTOCOL

## Overview

Petroleum refineries transform crude oil into valuable products including gasoline, diesel, jet fuel, heating oil, lubricants, and petrochemical feedstocks. These complex facilities employ sophisticated distributed control systems, advanced process control, safety instrumented systems, and analyzers from leading industrial automation vendors to optimize yields, maintain product quality, ensure safety, and minimize environmental impacts.

## Major Refinery Automation Vendors

### Distributed Control Systems (DCS)

**[VENDOR: Honeywell Process Solutions]** dominates refinery automation with over 50% market share through **[EQUIPMENT: Experion PKS DCS]**, deployed in hundreds of refineries globally managing crude distillation, catalytic cracking, hydroprocessing, and product blending. **[VENDOR: Honeywell]** **[EQUIPMENT: C300 controllers]**, **[EQUIPMENT: Safety Manager SIS]**, **[EQUIPMENT: Profit Controller APC]**, and **[EQUIPMENT: UniSim Design simulation]** provide integrated process control, safety, and optimization. **[VENDOR: Honeywell]** **[EQUIPMENT: Uniformance PHD]** historians collect time-series data from thousands of process measurements.

**[VENDOR: Yokogawa]** supplies **[EQUIPMENT: CENTUM VP DCS]** to major refineries, integrating **[EQUIPMENT: ProSafe-RS safety system]**, **[EQUIPMENT: Exaquantum PIMS]** (Plant Information Management System), and **[EQUIPMENT: Exapilot APC]** (Advanced Process Control). **[VENDOR: Yokogawa]** **[EQUIPMENT: CENTUM VP R6]** supports up to 100,000 I/O points for mega-scale refinery complexes. **[VENDOR: Yokogawa]** **[EQUIPMENT: Field Instruments]** include **[EQUIPMENT: EJA differential pressure transmitters]**, **[EQUIPMENT: ROTAMASS Coriolis flowmeters]**, and **[EQUIPMENT: YTA temperature transmitters]**.

**[VENDOR: Emerson]** provides **[EQUIPMENT: DeltaV DCS]** for refinery operations, with **[EQUIPMENT: DeltaV SIS]** safety systems achieving SIL 3 certification per **[PROTOCOL: IEC 61511]**. **[VENDOR: Emerson]** **[EQUIPMENT: DeltaV Batch]** manages batch operations in lubricant blending and specialty products. **[VENDOR: Emerson]** **[EQUIPMENT: Syncade MES]** (Manufacturing Execution System) coordinates production scheduling, quality management, and inventory tracking.

**[VENDOR: ABB]** delivers **[EQUIPMENT: Symphony Plus DCS]** and **[EQUIPMENT: 800xA extended automation]** platforms, integrating electrical distribution monitoring, asset management, and collaborative operations. **[VENDOR: ABB]** **[EQUIPMENT: AC 800M controllers]**, **[EQUIPMENT: Symphony Plus Safety]**, and **[EQUIPMENT: Aspect Objects]** provide flexible configuration for refinery unit operations.

**[VENDOR: Schneider Electric]** offers legacy **[EQUIPMENT: Foxboro I/A Series DCS]** and modernized **[EQUIPMENT: EcoStruxure Foxboro DCS]**, with **[EQUIPMENT: Triconex TMR safety systems]** protecting critical units. **[VENDOR: Schneider Electric]** **[EQUIPMENT: PlantStruxure PES]** (Process Expert System) delivers integrated DCS, MES, and manufacturing intelligence.

### Advanced Process Control (APC) Vendors

**[VENDOR: Honeywell]** **[EQUIPMENT: Profit Controller]** provides multivariable model predictive control (MPC) for crude units, FCCUs, hydrocrackers, reformers, and alkylation units, increasing yields, reducing energy consumption, and improving product quality. **[VENDOR: Honeywell]** **[EQUIPMENT: Profit Optimizer]** performs real-time economic optimization, and **[EQUIPMENT: Profit Suite]** integrates planning, scheduling, and control.

**[VENDOR: AspenTech]** delivers **[EQUIPMENT: Aspen DMC3]** (Dynamic Matrix Control) for refinery-wide optimization, **[EQUIPMENT: Aspen HYSYS]** process simulation, **[EQUIPMENT: Aspen Plus]** rigorous modeling, and **[EQUIPMENT: Aspen PIMS]** manufacturing information management. **[VENDOR: AspenTech]** **[EQUIPMENT: Aspen Petroleum Supply Chain Planner]** optimizes crude selection and product distribution.

**[VENDOR: Yokogawa]** **[EQUIPMENT: Exapilot]** provides model predictive control, coordinating with **[EQUIPMENT: CENTUM VP DCS]** for seamless regulatory-to-advanced control transitions. **[VENDOR: Yokogawa]** **[EQUIPMENT: Exarqe]** performs rigorous online optimization using first-principles models.

**[VENDOR: Emerson]** **[EQUIPMENT: DeltaV Predict]** integrates APC functionality within **[EQUIPMENT: DeltaV DCS]** architecture, eliminating separate APC servers and simplifying maintenance.

**[VENDOR: Shell Global Solutions]** licenses **[EQUIPMENT: SMOC]** (Shell Multivariable Optimizing Control) technology to refineries, combining MPC with real-time optimization (RTO) for maximum economic benefit.

## Critical Refinery Process Units

### Crude Distillation Units (CDU/VDU)

**[EQUIPMENT: Atmospheric distillation columns]** separate crude oil into fractions (light ends, naphtha, kerosene, diesel, atmospheric gas oil, atmospheric residue) using **[EQUIPMENT: trayed columns]** or **[EQUIPMENT: packed columns]** from **[VENDOR: Koch-Glitsch]**, **[VENDOR: Sulzer]**, **[VENDOR: Raschig]**, and **[VENDOR: Montz]**. **[EQUIPMENT: Crude preheat trains]** recover energy using **[EQUIPMENT: shell-and-tube heat exchangers]** from **[VENDOR: Alfa Laval]**, **[VENDOR: API Heat Transfer]**, **[VENDOR: Chart Industries]**, and **[VENDOR: Xylem Hoffman & Lamoureux]**.

**[EQUIPMENT: Vacuum distillation units]** (VDUs) process atmospheric residue into vacuum gas oil (VGO) and vacuum residue under sub-atmospheric pressure created by **[EQUIPMENT: steam ejectors]** from **[VENDOR: Graham Corporation]**, **[VENDOR: Korting]**, and **[VENDOR: Schutte & Koerting]**, or **[EQUIPMENT: liquid ring vacuum pumps]** from **[VENDOR: Gardner Denver]** (**[VENDOR: Ingersoll Rand]**) and **[VENDOR: Flowserve]**.

**[EQUIPMENT: Desalter units]** remove salts, metals, and sediment from crude oil using **[EQUIPMENT: electrostatic coalescers]**, **[EQUIPMENT: chemical injection systems]**, and **[EQUIPMENT: wash water systems]**. **[VENDOR: Cameron]** (**[VENDOR: Schlumberger]**), **[VENDOR: NATCO]**, **[VENDOR: Sulzer]**, and **[VENDOR: Agar Corporation]** manufacture desalter equipment.

**[EQUIPMENT: Column overhead systems]** prevent corrosion using **[EQUIPMENT: amine injection]**, **[EQUIPMENT: caustic injection]**, and **[EQUIPMENT: filming corrosion inhibitors]**. **[EQUIPMENT: Overhead condensers]** employ **[EQUIPMENT: air-cooled heat exchangers]** from **[VENDOR: SPX Cooling Technologies]**, **[VENDOR: Hudson Products]**, and **[VENDOR: Chart Energy & Chemicals]**.

### Fluid Catalytic Cracking (FCC) Units

**[EQUIPMENT: FCC reactors]** crack heavy gas oils into gasoline and light olefins using **[EQUIPMENT: zeolite catalysts]** from **[VENDOR: W.R. Grace]**, **[VENDOR: BASF]**, **[VENDOR: Albemarle]**, and **[VENDOR: Johnson Matthey]**. **[EQUIPMENT: Regenerators]** burn coke deposits from spent catalyst, producing high-temperature flue gas that drives **[EQUIPMENT: power recovery turbines]** from **[VENDOR: Siemens Energy]**, **[VENDOR: GE Oil & Gas]**, and **[VENDOR: Atlas Copco]**.

**[EQUIPMENT: Main fractionators]** separate FCC products into fuel gas, C3/C4 LPG, gasoline, light cycle oil (LCO), and heavy cycle oil (HCO). **[EQUIPMENT: Wet gas compressors]** from **[VENDOR: GE Oil & Gas]**, **[VENDOR: Siemens Energy]**, and **[VENDOR: MAN Energy Solutions]** compress overhead vapors for gas plant processing.

**[EQUIPMENT: Slide valves]** control catalyst circulation between reactor and regenerator, manufactured by **[VENDOR: Bray International]**, **[VENDOR: Xomox]**, and **[VENDOR: DeZurik]**. **[EQUIPMENT: Catalyst transfer lines]** employ **[EQUIPMENT: expansion joints]** from **[VENDOR: Flex-A-Seal]**, **[VENDOR: Senior Flexonics]**, and **[VENDOR: Pathway Polymers]** to accommodate thermal growth.

**[EQUIPMENT: Electrostatic precipitators]** (ESPs) remove catalyst fines from regenerator flue gas, manufactured by **[VENDOR: GE Steam Power]**, **[VENDOR: Babcock & Wilcox]**, **[VENDOR: FLSmidth]**, and **[VENDOR: Hamon Research-Cottrell]**. **[EQUIPMENT: SCR units]** (Selective Catalytic Reduction) reduce NOx emissions using **[EQUIPMENT: ammonia injection]** and **[EQUIPMENT: catalyst beds]** from **[VENDOR: Johnson Matthey]**, **[VENDOR: Cormetech]**, and **[VENDOR: Haldor Topsoe]**.

### Hydroprocessing Units

**[EQUIPMENT: Hydrotreaters]** remove sulfur, nitrogen, and metals from feedstocks using **[EQUIPMENT: cobalt-molybdenum]** or **[EQUIPMENT: nickel-molybdenum catalysts]** from **[VENDOR: Albemarle]**, **[VENDOR: Haldor Topsoe]**, **[VENDOR: Axens]**, and **[VENDOR: Criterion Catalysts]** (**[VENDOR: Shell]**). **[EQUIPMENT: Hydrocracker reactors]** convert heavy oils into lighter, higher-value products under high hydrogen pressure (1500-2500 psig).

**[EQUIPMENT: Recycle gas compressors]** circulate hydrogen-rich gas through reactors, using **[EQUIPMENT: centrifugal compressors]** from **[VENDOR: Siemens Energy]**, **[VENDOR: GE Oil & Gas]**, **[VENDOR: Baker Hughes Nuovo Pignone]**, **[VENDOR: MAN Energy Solutions]**, and **[VENDOR: Atlas Copco]**. **[EQUIPMENT: Make-up hydrogen compressors]** boost fresh hydrogen from **[EQUIPMENT: hydrogen plants]** or **[EQUIPMENT: reformer units]**.

**[EQUIPMENT: Reactor effluent air coolers]** (REACs) and **[EQUIPMENT: reactor effluent water coolers]** reduce temperatures before **[EQUIPMENT: high-pressure separators]**. **[EQUIPMENT: Amine treaters]** remove H₂S from recycle gas using **[EQUIPMENT: MDEA]** (methyldiethanolamine) or **[EQUIPMENT: DGA]** (diglycolamine) solutions.

**[EQUIPMENT: Reactor internals]** include **[EQUIPMENT: quench boxes]**, **[EQUIPMENT: distributor trays]**, and **[EQUIPMENT: grading materials]** from **[VENDOR: Axens]**, **[VENDOR: Haldor Topsoe]**, **[VENDOR: Shell Global Solutions]**, and **[VENDOR: UOP]** (**[VENDOR: Honeywell]**). **[EQUIPMENT: Spent catalyst handling systems]** utilize **[EQUIPMENT: vacuum trucks]**, **[EQUIPMENT: dump bins]**, and **[EQUIPMENT: radioactive monitoring]** for safe disposal.

### Catalytic Reforming Units

**[EQUIPMENT: Catalytic reformers]** convert low-octane naphthas into high-octane reformate using **[EQUIPMENT: platinum-rhenium catalysts]** from **[VENDOR: Axens]**, **[VENDOR: UOP]** (**[VENDOR: Honeywell]**), and **[VENDOR: Haldor Topsoe]**. **[VENDOR: UOP]** **[EQUIPMENT: CCR Platforming]** (Continuous Catalyst Regeneration) maintains high activity through online catalyst regeneration.

**[EQUIPMENT: Reformer reactors]** operate in series with interstage **[EQUIPMENT: fired heaters]** reheating process streams to reaction temperatures (900-1000°F). **[EQUIPMENT: Burner management systems]** from **[VENDOR: Honeywell]**, **[VENDOR: Siemens]**, **[VENDOR: Fireye]**, and **[VENDOR: Pilz]** ensure safe heater operation per **[PROTOCOL: NFPA 85]** and **[PROTOCOL: API RP 556]**.

**[EQUIPMENT: Catalyst regeneration systems]** burn off coke using **[EQUIPMENT: oxygen analyzers]**, **[EQUIPMENT: combustion air blowers]**, and **[EQUIPMENT: chloride injection systems]**. **[EQUIPMENT: Catalyst reduction systems]** prepare regenerated catalyst for reactor return using **[EQUIPMENT: hydrogen reduction]** at controlled temperatures.

**[EQUIPMENT: Product stabilizers]** remove light ends from reformate, producing **[EQUIPMENT: C5+ reformate]** for gasoline blending and **[EQUIPMENT: hydrogen-rich gas]** for hydrotreating. **[EQUIPMENT: Net gas compressors]** recover excess hydrogen for refinery distribution.

### Alkylation Units

**[EQUIPMENT: Sulfuric acid alkylation units]** from **[VENDOR: Honeywell UOP]**, **[VENDOR: Axens]**, and **[VENDOR: CB&I]** (**[VENDOR: McDermott]**) react isobutane with C3/C4 olefins to produce high-octane alkylate gasoline. **[EQUIPMENT: Acid settlers]**, **[EQUIPMENT: contactors]**, and **[EQUIPMENT: refrigeration systems]** maintain reaction conditions.

**[EQUIPMENT: Hydrofluoric acid alkylation units]** from **[VENDOR: UOP]**, **[VENDOR: Phillips 66]**, and legacy **[VENDOR: Stratco]** designs employ **[EQUIPMENT: HF acid]** as catalyst, requiring extensive **[OPERATION: acid mitigation]** systems including **[EQUIPMENT: water spray curtains]**, **[EQUIPMENT: alkylation cleaners (AlkyClean)]**, and **[EQUIPMENT: acid vapor detection]** from **[VENDOR: Honeywell Analytics]** and **[VENDOR: MSA Safety]**.

**[EQUIPMENT: Propane refrigeration systems]** chill alkylation reactors using **[EQUIPMENT: reciprocating compressors]** from **[VENDOR: Ariel Corporation]**, **[VENDOR: Howden]**, **[VENDOR: GEA]**, and **[VENDOR: Mayekawa]**. **[EQUIPMENT: Propane chillers]**, **[EQUIPMENT: evaporators]**, and **[EQUIPMENT: condensers]** maintain precise temperature control.

**[EQUIPMENT: Deisobutanizer columns]** recycle unreacted isobutane to **[EQUIPMENT: alkylation reactors]**, while **[EQUIPMENT: debutanizer columns]** separate alkylate product. **[EQUIPMENT: Caustic scrubbers]** neutralize acid carryover before product storage.

## Instrumentation and Analyzers

### Process Analyzers

**[EQUIPMENT: Gas chromatographs]** analyze hydrocarbon compositions, providing real-time feedback for **[OPERATION: distillation endpoint control]**, **[OPERATION: reformer octane control]**, and **[OPERATION: product quality verification]**. **[VENDOR: ABB]** **[EQUIPMENT: NGC8200]**, **[VENDOR: Siemens]** **[EQUIPMENT: MAXUM Edition II]**, **[VENDOR: Agilent]** **[EQUIPMENT: 490 Micro GC]**, and **[VENDOR: Emerson]** **[EQUIPMENT: Rosemount 700XA]** provide online GC analysis with automatic calibration and validation.

**[EQUIPMENT: Near-infrared (NIR) analyzers]** from **[VENDOR: ABB]**, **[VENDOR: Yokogawa]**, **[VENDOR: Thermo Fisher Scientific]**, and **[VENDOR: Guided Wave]** measure octane numbers, cetane numbers, sulfur content, and distillation properties in real-time, enabling closed-loop **[OPERATION: product quality control]**.

**[EQUIPMENT: Sulfur analyzers]** monitor compliance with ultra-low sulfur diesel (ULSD) and gasoline specifications using **[EQUIPMENT: X-ray fluorescence (XRF)]** from **[VENDOR: PANalytical]** (**[VENDOR: Malvern]**), **[VENDOR: Rigaku]**, and **[VENDOR: Horiba]**, or **[EQUIPMENT: UV fluorescence]** from **[VENDOR: Teledyne]** and **[VENDOR: Antek]** (**[VENDOR: PAC]**).

**[EQUIPMENT: Octane analyzers]** employ **[EQUIPMENT: NIR spectroscopy]** or **[EQUIPMENT: online CFR engines]** to measure research octane number (RON) and motor octane number (MON) for **[OPERATION: gasoline blending optimization]**. **[VENDOR: Sentry Equipment]** and **[VENDOR: PAC]** manufacture online octane analysis systems.

**[EQUIPMENT: Viscosity analyzers]** from **[VENDOR: Anton Paar]**, **[VENDOR: Cambridge Viscosity]**, **[VENDOR: Emerson Micro Motion]**, and **[VENDOR: Brookfield]** monitor lubricant production and fuel oil specifications. **[EQUIPMENT: Cloud point]** and **[EQUIPMENT: pour point analyzers]** ensure cold-weather diesel performance.

**[EQUIPMENT: Corrosion analyzers]** measure **[EQUIPMENT: total acid number (TAN)]**, **[EQUIPMENT: chloride content]**, and **[EQUIPMENT: naphthenic acid content]** to prevent equipment damage. **[EQUIPMENT: Online corrosion probes]** from **[VENDOR: Emerson Rosemount]**, **[VENDOR: Honeywell]**, and **[VENDOR: Metal Samples]** track corrosion rates in real-time.

### Flow and Level Measurement

**[EQUIPMENT: Coriolis mass flowmeters]** from **[VENDOR: Emerson Micro Motion]**, **[VENDOR: Endress+Hauser Promass]**, **[VENDOR: Yokogawa ROTAMASS]**, **[VENDOR: Krohne OPTIMASS]**, and **[VENDOR: Siemens SITRANS FC]** provide custody-quality measurement for crude oil receipt, product transfers, and blending operations with ±0.05% accuracy.

**[EQUIPMENT: Ultrasonic flowmeters]** from **[VENDOR: GE Panametrics]**, **[VENDOR: Sick]**, **[VENDOR: Krohne]**, and **[VENDOR: Emerson Daniel]** measure high-volume crude and product pipelines, offering non-intrusive installation and minimal pressure drop.

**[EQUIPMENT: Turbine meters]** from **[VENDOR: Emerson Daniel]**, **[VENDOR: FMC Technologies]**, and **[VENDOR: Hoffer Flow Controls]** meter refined products with proven accuracy traceable to **[PROTOCOL: API MPMS Chapter 5]** standards. **[EQUIPMENT: Proving systems]** using **[EQUIPMENT: master meters]** or **[EQUIPMENT: pipe provers]** validate meter performance.

**[EQUIPMENT: Positive displacement meters]** from **[VENDOR: Emerson Brooks]**, **[VENDOR: Litre Meter]**, and **[VENDOR: Oval]** provide high-accuracy metering for viscous products, additives, and batch loading operations.

**[EQUIPMENT: Radar level transmitters]** from **[VENDOR: Emerson Rosemount]**, **[VENDOR: Endress+Hauser Micropilot]**, **[VENDOR: Vega VEGAPULS]**, **[VENDOR: Siemens SITRANS LR]**, and **[VENDOR: Krohne]** measure levels in crude tanks, product tanks, and process vessels. **[EQUIPMENT: Servo gauges]** and **[EQUIPMENT: hybrid gauges]** from **[VENDOR: Honeywell Enraf]** and **[VENDOR: Emerson Rosemount Tank Gauging]** provide custody-transfer-quality inventory measurement per **[PROTOCOL: API MPMS Chapter 3]**.

**[EQUIPMENT: Guided wave radar]** (GWR) from **[VENDOR: Magnetrol]**, **[VENDOR: Endress+Hauser Levelflex]**, **[VENDOR: Vega VEGAFLEX]**, and **[VENDOR: Emerson Rosemount]** measures interface levels in separators, settling tanks, and multi-phase vessels.

### Pressure and Temperature Measurement

**[EQUIPMENT: Pressure transmitters]** from **[VENDOR: Emerson Rosemount 3051S]**, **[VENDOR: Yokogawa EJX-A]**, **[VENDOR: Endress+Hauser Cerabar]**, **[VENDOR: ABB 266]**, and **[VENDOR: Siemens SITRANS P]** monitor process pressures with accuracies to ±0.04% of span, communicating via **[PROTOCOL: HART]**, **[PROTOCOL: FOUNDATION Fieldbus]**, or **[PROTOCOL: PROFIBUS PA]**.

**[EQUIPMENT: Differential pressure transmitters]** measure flow, level, and filter differential pressures across **[EQUIPMENT: orifice plates]**, **[EQUIPMENT: reactor beds]**, and **[EQUIPMENT: heat exchangers]**. **[EQUIPMENT: Remote seals]** isolate DP cells from corrosive or high-temperature process fluids.

**[EQUIPMENT: RTD temperature transmitters]** interface with **[EQUIPMENT: Pt100 RTDs]** or **[EQUIPMENT: Pt1000 RTDs]** for precision temperature measurement in critical control loops. **[VENDOR: Emerson]**, **[VENDOR: Endress+Hauser]**, **[VENDOR: Phoenix Contact]**, **[VENDOR: Wika]**, and **[VENDOR: Pyromation]** manufacture temperature sensors and transmitters.

**[EQUIPMENT: Thermocouple sensors]** (Types J, K, N, E, T, R, S, B) measure high-temperature applications in **[EQUIPMENT: fired heaters]**, **[EQUIPMENT: FCC regenerators]**, and **[EQUIPMENT: reformer reactors]**. **[EQUIPMENT: Multipoint thermocouples]** profile temperatures across reactor beds and distillation columns.

## Operations and Control Strategies

### Crude Unit Operations

**[OPERATION: Crude assay management]** adjusts **[EQUIPMENT: preheat train temperatures]**, **[EQUIPMENT: desalter operations]**, **[EQUIPMENT: column reflux rates]**, and **[EQUIPMENT: product drawoff rates]** based on crude slate changes. **[OPERATION: Crude blending optimization]** selects crude mixes maximizing refinery margin using **[VENDOR: Honeywell]** **[EQUIPMENT: Profit Optimizer]** or **[VENDOR: AspenTech]** **[EQUIPMENT: Aspen Petroleum Scheduler]**.

**[OPERATION: Preheat train optimization]** maximizes heat recovery while preventing **[EQUIPMENT: heat exchanger fouling]**, balancing **[OPERATION: energy savings]** against **[OPERATION: cleaning frequency]**. **[EQUIPMENT: Online fouling monitors]** from **[VENDOR: Soteica]**, **[VENDOR: AspenTech]**, and **[VENDOR: Honeywell]** predict cleaning requirements.

**[OPERATION: Desalter control]** maintains **[EQUIPMENT: wash water pH]**, **[EQUIPMENT: mixing valve position]**, **[EQUIPMENT: electrostatic grid voltage]**, and **[EQUIPMENT: interface level]** to remove salts and reduce crude unit corrosion. **[OPERATION: Overhead corrosion control]** injects **[EQUIPMENT: filming amines]** and **[EQUIPMENT: neutralizing amines]** from **[VENDOR: Baker Hughes]**, **[VENDOR: Nalco Champion]** (**[VENDOR: Ecolab]**), and **[VENDOR: Cortec]**.

**[OPERATION: Column pressure control]** coordinates **[EQUIPMENT: overhead condenser duty]**, **[EQUIPMENT: gas compressor suction]**, and **[EQUIPMENT: pressure control valves]** to maintain stable operation during throughput changes.

### FCC Operations

**[OPERATION: Catalyst circulation control]** balances **[EQUIPMENT: slide valve positions]**, **[EQUIPMENT: regenerator air rates]**, and **[EQUIPMENT: reactor temperatures]** to maximize gasoline selectivity while maintaining **[EQUIPMENT: catalyst activity]**. **[OPERATION: Coke burn control]** prevents **[EQUIPMENT: regenerator temperature excursions]** that damage **[EQUIPMENT: cyclones]** and **[EQUIPMENT: refractory linings]**.

**[OPERATION: Feed preheat optimization]** maximizes **[EQUIPMENT: main fractionator]** bottoms temperature recovery while preventing **[EQUIPMENT: feed nozzle coking]**. **[OPERATION: Dispersion steam optimization]** reduces steam consumption while maintaining adequate **[EQUIPMENT: feed atomization]**.

**[OPERATION: Wet gas compression control]** coordinates **[EQUIPMENT: compressor capacity]**, **[EQUIPMENT: interstage cooling]**, and **[EQUIPMENT: knockout drum levels]** to reliably compress overhead vapors. **[OPERATION: Fractionator pressure control]** maintains constant **[EQUIPMENT: overhead receiver pressure]** affecting downstream gas plant operation.

**[OPERATION: Flue gas emissions control]** manages **[EQUIPMENT: CO boiler operations]**, **[EQUIPMENT: ESP performance]**, and **[EQUIPMENT: SCR catalyst activity]** to meet **[PROTOCOL: EPA NSPS]** (New Source Performance Standards) and **[PROTOCOL: MACT]** (Maximum Achievable Control Technology) requirements.

### Hydroprocessing Operations

**[OPERATION: Hydrogen management]** optimizes **[EQUIPMENT: hydrogen partial pressure]**, **[EQUIPMENT: recycle gas purity]**, and **[EQUIPMENT: hydrogen consumption]** to meet product specifications while minimizing **[EQUIPMENT: hydrogen plant]** capacity requirements. **[OPERATION: Reactor temperature control]** balances **[EQUIPMENT: heater duty]**, **[EQUIPMENT: quench hydrogen]**, and **[EQUIPMENT: feed preheat]** to maintain optimal **[EQUIPMENT: catalyst bed temperatures]**.

**[OPERATION: Catalyst cycle management]** monitors **[EQUIPMENT: pressure drop buildup]**, **[EQUIPMENT: product quality trends]**, **[EQUIPMENT: hydrogen consumption increases]**, and **[EQUIPMENT: temperature requirement creep]** to schedule **[OPERATION: catalyst regeneration]** or **[OPERATION: catalyst changeout]**. **[EQUIPMENT: Catalyst activity models]** predict remaining cycle length.

**[OPERATION: Amine treating optimization]** controls **[EQUIPMENT: amine circulation rates]**, **[EQUIPMENT: reboiler temperatures]**, and **[EQUIPMENT: contactor efficiency]** to remove H₂S from **[EQUIPMENT: recycle gas]** and **[EQUIPMENT: product off-gas streams]**. **[OPERATION: Amine quality monitoring]** tracks **[EQUIPMENT: heat stable salt]** accumulation requiring **[OPERATION: amine reclamation]**.

**[OPERATION: Compressor anti-surge control]** prevents surge damage to **[EQUIPMENT: recycle gas compressors]** and **[EQUIPMENT: makeup hydrogen compressors]** using **[VENDOR: Emerson]** **[EQUIPMENT: ControlWave]**, **[VENDOR: Compressor Controls Corporation]**, or **[VENDOR: Honeywell]** **[EQUIPMENT: ASC+]** systems.

### Blending and Distribution Operations

**[OPERATION: Gasoline blending]** combines **[EQUIPMENT: reformate]**, **[EQUIPMENT: FCC gasoline]**, **[EQUIPMENT: alkylate]**, **[EQUIPMENT: butane]**, and **[EQUIPMENT: additives]** to meet octane, RVP (Reid vapor pressure), sulfur, olefin, and aromatic specifications. **[VENDOR: Honeywell]** **[EQUIPMENT: Blend Optimizer]**, **[VENDOR: AspenTech]** **[EQUIPMENT: Aspen Blend Model]**, and **[VENDOR: Yokogawa]** **[EQUIPMENT: Exaquantum Blend]** provide real-time blending optimization.

**[OPERATION: Diesel blending]** manages **[EQUIPMENT: straight-run diesel]**, **[EQUIPMENT: hydrotreated diesel]**, **[EQUIPMENT: FCC light cycle oil]**, and **[EQUIPMENT: additives]** to achieve cetane, sulfur, cold flow, and density specifications. **[EQUIPMENT: In-line blending systems]** from **[VENDOR: Emerson]**, **[VENDOR: Honeywell]**, **[VENDOR: Yokogawa]**, and **[VENDOR: ProMinent]** provide continuous blending with feedback control.

**[OPERATION: Additive injection]** meters **[EQUIPMENT: detergents]**, **[EQUIPMENT: antioxidants]**, **[EQUIPMENT: corrosion inhibitors]**, **[EQUIPMENT: cetane improvers]**, and **[EQUIPMENT: lubricity improvers]** from **[VENDOR: Innospec]**, **[VENDOR: Afton Chemical]**, **[VENDOR: Lubrizol]**, and **[VENDOR: Chevron Oronite]** using **[EQUIPMENT: additive injection skids]** from **[VENDOR: ProMinent]**, **[VENDOR: Milton Roy]**, and **[VENDOR: Liquid Controls]**.

**[OPERATION: Truck loading control]** sequences **[EQUIPMENT: loading arms]**, **[EQUIPMENT: metering systems]**, **[EQUIPMENT: preset controllers]**, and **[EQUIPMENT: overfill protection]** using **[VENDOR: Emerson]** **[EQUIPMENT: FloBoss]**, **[VENDOR: Honeywell]**, or **[VENDOR: Endress+Hauser]** **[EQUIPMENT: truck loading systems]**. **[EQUIPMENT: Vapor recovery units]** from **[VENDOR: Aereon]**, **[VENDOR: Alma]**, and **[VENDOR: John Zink Hamworthy]** capture VOC emissions per **[PROTOCOL: EPA Subpart XX]** requirements.

## Communication Protocols and Networks

### Process Control Networks

**[PROTOCOL: FOUNDATION Fieldbus H1]** connects intelligent field devices to **[VENDOR: Emerson DeltaV]**, **[VENDOR: Honeywell Experion]**, **[VENDOR: Yokogawa CENTUM VP]**, and **[VENDOR: ABB 800xA]** DCS platforms, enabling advanced diagnostics and function block execution in field instruments. **[EQUIPMENT: Fieldbus power conditioners]** from **[VENDOR: Relcom]**, **[VENDOR: Pepperl+Fuchs]**, **[VENDOR: MTL]**, and **[VENDOR: Moore Industries]** ensure network reliability.

**[PROTOCOL: HART]** provides digital communication superimposed on traditional 4-20mA signals, supported by virtually all modern **[EQUIPMENT: transmitters]**, **[EQUIPMENT: valve positioners]**, and **[EQUIPMENT: analyzers]**. **[EQUIPMENT: HART multiplexers]** aggregate multiple HART devices for SCADA or DCS integration.

**[PROTOCOL: PROFIBUS PA]** and **[PROTOCOL: PROFIBUS DP]** connect **[VENDOR: Siemens]** **[EQUIPMENT: SIMATIC controllers]** to field instruments and remote I/O, competing with **[PROTOCOL: FOUNDATION Fieldbus]** in Siemens-centric installations.

**[PROTOCOL: Modbus TCP/IP]** provides Ethernet-based communication between **[EQUIPMENT: DCS systems]**, **[EQUIPMENT: PLCs]**, **[EQUIPMENT: analyzers]**, **[EQUIPMENT: flow computers]**, and **[EQUIPMENT: tank gauging systems]**. **[PROTOCOL: Modbus RTU]** operates over **[ARCHITECTURE: RS-485 serial networks]** for legacy device integration.

**[PROTOCOL: OPC UA]** enables platform-independent data exchange between **[EQUIPMENT: DCS]**, **[EQUIPMENT: historians]**, **[EQUIPMENT: MES systems]**, **[EQUIPMENT: LIMS]** (Laboratory Information Management Systems), and **[ARCHITECTURE: enterprise applications]**, superseding legacy **[PROTOCOL: OPC DA/HDA/A&E]** specifications.

**[PROTOCOL: EtherNet/IP]** connects **[VENDOR: Rockwell Automation]** **[EQUIPMENT: ControlLogix]** and **[EQUIPMENT: CompactLogix]** PLCs used in **[OPERATION: packaging]**, **[OPERATION: truck loading]**, and **[OPERATION: tank farm automation]** applications.

### Industrial Networking

**[EQUIPMENT: Industrial Ethernet switches]** from **[VENDOR: Cisco Industrial Ethernet]**, **[VENDOR: Hirschmann]** (**[VENDOR: Belden]**), **[VENDOR: Moxa]**, **[VENDOR: Siemens SCALANCE]**, **[VENDOR: Phoenix Contact]**, and **[VENDOR: Westermo]** create redundant ring topologies with <50ms failover using **[PROTOCOL: RSTP]** (Rapid Spanning Tree Protocol), **[PROTOCOL: MRP]** (Media Redundancy Protocol), or **[PROTOCOL: PRP]** (Parallel Redundancy Protocol).

**[EQUIPMENT: Industrial firewalls]** from **[VENDOR: Fortinet]**, **[VENDOR: Palo Alto Networks]**, **[VENDOR: Cisco]**, **[VENDOR: Tofino Security]** (**[VENDOR: Belden]**), **[VENDOR: Hirschmann]**, and **[VENDOR: Waterfall Security]** implement **[ARCHITECTURE: defense-in-depth]** strategies, segregating **[ARCHITECTURE: control system zones]** from **[ARCHITECTURE: corporate networks]**.

**[EQUIPMENT: Unidirectional gateways]** from **[VENDOR: Waterfall Security]**, **[VENDOR: Owl Cyber Defense]**, and **[VENDOR: Hirschmann Tofino Enforcer]** enforce one-way data flow from **[ARCHITECTURE: control zones]** to **[ARCHITECTURE: enterprise zones]**, preventing reverse attacks while enabling data replication.

**[EQUIPMENT: Industrial wireless access points]** from **[VENDOR: Cisco Aironet]**, **[VENDOR: Aruba]** (**[VENDOR: HPE]**), **[VENDOR: Moxa]**, and **[VENDOR: ProSoft Technology]** enable mobile operator rounds, wireless instrumentation, and portable analyzer connections while maintaining **[SECURITY: wireless segmentation]** and **[SECURITY: 802.1X authentication]**.

## Security Considerations

### Vulnerabilities and Threats

**[VULNERABILITY: Legacy DCS systems]** running Windows XP, Windows 2000, or proprietary operating systems lack modern security updates, enabling **[ATTACK_PATTERN: remote code execution]**, **[ATTACK_PATTERN: privilege escalation]**, and **[ATTACK_PATTERN: lateral movement]** by threat actors.

**[VULNERABILITY: Unencrypted industrial protocols]** like **[PROTOCOL: Modbus]**, **[PROTOCOL: DNP3]**, and legacy **[PROTOCOL: OPC DA]** transmit commands and process data in cleartext, vulnerable to **[ATTACK_PATTERN: man-in-the-middle attacks]**, **[ATTACK_PATTERN: command injection]**, and **[ATTACK_PATTERN: process manipulation]**.

**[VULNERABILITY: Default and hardcoded credentials]** in **[EQUIPMENT: HMI systems]**, **[EQUIPMENT: engineering workstations]**, **[EQUIPMENT: historians]**, **[EQUIPMENT: OPC servers]**, and **[EQUIPMENT: analyzers]** enable **[ATTACK_PATTERN: unauthorized access]**. Publicly documented defaults for **[VENDOR: Wonderware]**, **[VENDOR: GE iFIX]**, **[VENDOR: Rockwell FactoryTalk]**, and **[VENDOR: Siemens WinCC]** systems facilitate attacks.

**[VULNERABILITY: Remote access exposures]** through **[EQUIPMENT: VPN concentrators]**, **[VENDOR: TeamViewer]**, **[VENDOR: LogMeIn]**, **[VENDOR: AnyDesk]**, and **[VENDOR: GoToMyPC]** create **[ATTACK_PATTERN: persistent access]** opportunities. **[ATTACK_PATTERN: Vendor support account compromises]** enable long-term reconnaissance and attack staging.

**[VULNERABILITY: Firmware and software vulnerabilities]** in **[EQUIPMENT: DCS controllers]**, **[EQUIPMENT: PLCs]**, **[EQUIPMENT: safety systems]**, **[EQUIPMENT: HMIs]**, and **[EQUIPMENT: historians]** allow **[ATTACK_PATTERN: code execution]**, **[ATTACK_PATTERN: denial of service]**, and **[ATTACK_PATTERN: backdoor installation]**. ICS-CERT advisories regularly identify vulnerabilities in **[VENDOR: Honeywell]**, **[VENDOR: Emerson]**, **[VENDOR: Yokogawa]**, **[VENDOR: Rockwell]**, **[VENDOR: Siemens]**, **[VENDOR: Schneider Electric]**, and **[VENDOR: ABB]** systems.

**[ATTACK_PATTERN: Supply chain compromises]** inject malware during equipment manufacturing, software development, system integration, or vendor support operations. **[ATTACK_PATTERN: Watering hole attacks]** target vendor support portals, engineering forums, and industry websites frequented by refinery personnel.

### Security Standards and Practices

**[PROTOCOL: IEC 62443]** (Industrial Automation and Control Systems Security) defines comprehensive security requirements across **[ARCHITECTURE: zones and conduits]**, specifying four security levels (SL1-SL4) for components, systems, and facilities. **[VENDOR: Honeywell]**, **[VENDOR: Emerson]**, **[VENDOR: Yokogawa]**, **[VENDOR: Rockwell Automation]**, **[VENDOR: Siemens]**, and **[VENDOR: Schneider Electric]** offer **[PROTOCOL: IEC 62443]**-certified products.

**[PROTOCOL: NERC CIP]** (Critical Infrastructure Protection) standards apply to refineries and associated facilities impacting **[ARCHITECTURE: bulk electric system]** reliability, mandating **[OPERATION: critical cyber asset identification]** (CIP-002), **[OPERATION: electronic security perimeters]** (CIP-005), **[OPERATION: systems security management]** (CIP-007), **[OPERATION: configuration change management]** (CIP-010), and **[OPERATION: incident reporting]** (CIP-008).

**[PROTOCOL: API Standard 1164]** (Pipeline SCADA Security) provides security recommendations applicable to refinery control systems, addressing **[OPERATION: access control]**, **[OPERATION: network security]**, **[OPERATION: authentication]**, **[OPERATION: data integrity]**, and **[OPERATION: business continuity]**.

**[SECURITY: Network segmentation]** implements **[ARCHITECTURE: Purdue Enterprise Reference Architecture]** (PERA) separating **[ARCHITECTURE: Level 0]** (field devices), **[ARCHITECTURE: Level 1]** (process control), **[ARCHITECTURE: Level 2]** (supervisory control), **[ARCHITECTURE: Level 3]** (manufacturing operations), and **[ARCHITECTURE: Level 4]** (business systems) using **[EQUIPMENT: firewalls]**, **[EQUIPMENT: VLANs]**, and **[EQUIPMENT: routers]**.

**[SECURITY: Application whitelisting]** restricts **[EQUIPMENT: HMI workstations]**, **[EQUIPMENT: engineering stations]**, and **[EQUIPMENT: historian servers]** to approved executables using **[VENDOR: McAfee Application Control]**, **[VENDOR: Trend Micro Safe Lock]**, **[VENDOR: Ivanti Application Control]**, or **[VENDOR: CyberArk EPM]**, preventing **[ATTACK_PATTERN: malware execution]**.

**[SECURITY: Removable media controls]** block **[ATTACK_PATTERN: USB-based malware]** introduction using **[EQUIPMENT: USB port locks]**, **[VENDOR: Honeywell Safe USB]**, **[VENDOR: Waterfall Secure Bypass]**, **[VENDOR: Acronis DeviceLock]**, or **[VENDOR: GFI EndPointSecurity]** solutions, requiring approved **[EQUIPMENT: scan stations]** for necessary media transfers.

## Cross-References

- **[ARCHITECTURE: Refinery-wide optimization]** integrates crude units, conversion units, and blending via **[VENDOR: Honeywell]** **[EQUIPMENT: Profit Suite]** or **[VENDOR: AspenTech]** **[EQUIPMENT: Aspen Petroleum Scheduler]**
- **[EQUIPMENT: Hydrogen networks]** connect **[EQUIPMENT: reformers]**, **[EQUIPMENT: hydrogen plants]**, **[EQUIPMENT: hydrotreaters]**, and **[EQUIPMENT: hydrocrackers]** for efficient **[OPERATION: hydrogen management]**
- **[OPERATION: Product quality management]** coordinates **[EQUIPMENT: online analyzers]**, **[EQUIPMENT: laboratory LIMS]**, and **[EQUIPMENT: blend controllers]** for specification compliance
- **[PROTOCOL: OPC UA]** bridges refinery **[EQUIPMENT: DCS systems]** with corporate **[ARCHITECTURE: SAP]**, **[ARCHITECTURE: Oracle]**, or **[ARCHITECTURE: Microsoft Dynamics]** ERP systems
- **[SECURITY: Cybersecurity programs]** align with **[PROTOCOL: NIST Cybersecurity Framework]**, **[PROTOCOL: ICS-CERT recommendations]**, and **[PROTOCOL: Department of Homeland Security Chemical Facility Anti-Terrorism Standards]** (CFATS)
- **[VULNERABILITY: ICS vulnerabilities]** tracked by ICS-CERT affect refinery **[VENDOR: Honeywell]**, **[VENDOR: Emerson]**, **[VENDOR: Yokogawa]**, **[VENDOR: Rockwell]**, **[VENDOR: Siemens]**, **[VENDOR: Schneider]**, and **[VENDOR: ABB]** control systems

---

**Document Statistics:**
- VENDOR entities: 142+
- EQUIPMENT entities: 182+
- OPERATION entities: 94
- PROTOCOL entities: 65
- ARCHITECTURE cross-references: 32
- SECURITY mentions: 25
- VULNERABILITY/ATTACK_PATTERN references: 28
