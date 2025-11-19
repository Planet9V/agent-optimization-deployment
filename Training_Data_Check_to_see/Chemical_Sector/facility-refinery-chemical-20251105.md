# Refinery and Chemical Processing Facility Architecture

## Entity-Rich Introduction
Modern petroleum refinery facilities process 200,000+ barrels per day (BPD) crude oil through integrated process units including atmospheric/vacuum distillation columns (48-inch diameter, 80-foot tall fractioning towers operating at 350°F/15 psig atmospheric pressure, 750°F/5 mmHg vacuum pressure), fluid catalytic cracking (FCC) units with regenerator temperatures at 1,250°F circulating 60 tons/hour zeolite catalyst through riser/reactor/regenerator vessels, hydrotreating units removing sulfur compounds via catalytic hydrodesulfurization over Criterion DN-3531 cobalt-molybdenum catalysts at 650°F/1,200 psig hydrogen partial pressure, and alkylation units producing high-octane gasoline blendstocks via sulfuric acid-catalyzed isobutane/olefin reactions at 40°F in 50,000-gallon jacketed reactors. Control system architecture deploys Honeywell Experion PKS R510.2 with 125+ C300 controller clusters managing 12,500+ I/O points, Yokogawa CENTUM VP R6.09 coordinating batch polymerization operations across 8 parallel 50,000-liter glass-lined reactors, and Emerson DeltaV v14.3 LX executing advanced process control (DMCplus R490.2 MPC optimizing 35 controlled variables across main fractionator).

## Technical Facility Architecture Specifications

### Crude Distillation Unit (CDU) Design
- **Atmospheric Distillation Column**: 48-inch internal diameter carbon steel A516 Grade 70 vessel with 40 sieve trays (24-inch tray spacing), top temperature 350°F producing naphtha/kerosene/diesel/atmospheric gas oil (AGO) fractions, bottom residue at 650°F feeding vacuum distillation unit
- **Vacuum Distillation Unit (VDU)**: 60-inch diameter column operating at 5 mmHg absolute pressure (vacuum ejector system with 3-stage steam ejectors), 750°F flash zone temperature, producing light vacuum gas oil (LVGO), heavy vacuum gas oil (HVGO), and vacuum residue
- **Crude Preheat Train**: 12-stage shell-and-tube heat exchanger network (Alfa Laval Compabloc welded plate exchangers) preheating crude from 100°F to 550°F via heat recovery from product streams, fired heater (Chromalox RM circulation heater 75 MMBtu/hr capacity) final heating to 650°F
- **Overhead Condensing System**: Air-cooled heat exchangers (Hudson Products AERO-FIN 50 MMBtu/hr duty) condensing overhead vapors, accumulator drum (10-foot diameter, 30-foot length horizontal vessel) separating hydrocarbon liquid/water phases, reflux pump (Sulzer A-Series API 610 OH2 centrifugal 500 GPM)

### Fluid Catalytic Cracking (FCC) Unit Architecture
- **Riser/Reactor Configuration**: Vertical riser (36-inch diameter, 120-foot height) with 3-second hydrocarbon contact time, regenerated catalyst injection at 1,200°F via standpipe/slide valve, disengaging cyclones separating catalyst from cracked vapors
- **Regenerator Design**: 40-foot diameter fluid bed regenerator operating at 1,250°F burning coke deposits on spent catalyst, air blower (Elliott H-200M centrifugal compressor 80,000 SCFM capacity) supplying combustion air, CO boiler recovering heat from flue gas
- **Main Fractionator**: 48-inch diameter column with 45 sieve trays separating cracked products (light ends C3/C4, naphtha, light cycle oil LCO, heavy cycle oil HCO, clarified slurry oil CSO), 8 pump-around heat removal circuits controlling temperature profile
- **Catalyst Handling System**: Dense-phase pneumatic conveying transporting fresh catalyst (Honeywell UOP CCR Platforming zeolite) from storage silos, spent catalyst withdrawal to regenerator via slide valves, cyclone catalyst recovery minimizing emissions

### Hydrotreating Unit Process Design
- **Reactor Configuration**: Fixed-bed catalytic reactors (12-foot diameter, 60-foot tall vertical vessels) packed with Criterion DN-3531 cobalt-molybdenum catalyst (12,000 cubic feet catalyst volume), internal quench zones mixing hydrogen for temperature control
- **Hydrogen Compression System**: Reciprocating compressor (Ariel JGK/4 four-stage 2,500 HP) compressing hydrogen-rich recycle gas from 300 psig separator to 1,500 psig reactor inlet pressure, inter-stage cooling via fin-fan heat exchangers
- **High-Pressure Separator**: Three-phase separator (8-foot diameter, 24-foot length horizontal vessel) operating at 1,200 psig, separating hydrogen gas (recycle to compressor), sour water (to amine treating), and hydrotreated product (to stripper column)
- **Product Stripper**: 24-inch diameter column with 20 sieve trays stripping dissolved H2S from product using steam, overhead vapors to amine treating unit, bottoms product to storage (ULSD <10 ppm sulfur specification)

### Alkylation Unit Configuration
- **Reactor System**: Eight 50,000-gallon jacketed glass-lined reactors operating at 40°F, 93% sulfuric acid catalyst concentration, isobutane/olefin (isobutene, propylene) feed ratio 8:1 mass basis, intense agitation via Chemineer HE-3 hydrofoil impellers (300 RPM, 150 HP motors)
- **Acid Settler**: Horizontal drum separator (10-foot diameter, 40-foot length) with internal coalescer packs separating spent acid (specific gravity 1.83) from alkylate hydrocarbon (specific gravity 0.68), acid recirculation pump (Goulds 3196 ANSI process pump)
- **Refrigeration System**: Ammonia vapor compression refrigeration (Vilter VSM 601 single-screw compressor 500 TR capacity) maintaining reactor jacket temperature at 35°F, evaporator heat exchangers (Alfa Laval CBXP brazed plate) cooling circulating propane refrigerant
- **Caustic Wash System**: Caustic tower (36-inch diameter packed column with 20 feet Raschig rings) neutralizing acid carryover with 10% NaOH solution, washed alkylate routed to fractionation for C3/C4/alkylate separation

### Polymerization Reactor Farm Design
- **Batch Reactor Configuration**: Eight parallel 50,000-liter glass-lined steel reactors (Pfaudler Model 12000, 12-foot diameter, 14-foot straight side), operating pressure 100 psig, temperature range 40-180°C, full vacuum capability for distillation/drying
- **Agitation Systems**: Top-entering agitators with Philadelphia Mixers TriFoil impellers (200 RPM, 75 HP ABB ACS880 VFD-controlled motors), bottom-mount magnetic drive mixers (Fusion Fluid Equipment MaxMag 50 HP) for low-clearance applications
- **Jacket Temperature Control**: Julabo Presto A80 circulating baths (80 kW heating/cooling capacity) with Dow Dowtherm MX heat transfer fluid (-40°C to +200°C operating range), PID temperature control ±0.5°C setpoint accuracy via Eurotherm 3216 controllers
- **Material Charging**: Automated ingredient addition via Coriolis mass flowmeters (Micro Motion Elite CMF300 ±0.10% accuracy), weigh-scale charging (Mettler-Toledo PowerMount 0745C load cells 5,000 kg capacity), powder dosing via loss-in-weight feeders (Schenck AccuRate 300)

### Tank Farm and Storage Infrastructure
- **Crude Storage**: Ten 500,000-barrel floating-roof tanks (120-foot diameter, 48-foot height carbon steel API 650 design), internal floating roof (aluminum pontoon-type) minimizing vapor losses, foam fire suppression (Tyco TY5233 deluge nozzles)
- **Product Storage**: Fixed-roof tanks for finished products (gasoline, diesel, jet fuel), 100,000-barrel capacity tanks (80-foot diameter, 40-foot height), vapor recovery systems (John Zink VRU 1,000 SCFM capacity) reducing VOC emissions
- **Chemical Storage**: Stainless steel 316L tanks for sulfuric acid (98% concentration), caustic (50% NaOH), amine solutions (DEA/MEA), fiberglass-reinforced plastic (FRP) tanks for corrosive materials, secondary containment dikes per EPA 40 CFR 112
- **Tank Instrumentation**: Radar level transmitters (Rosemount 5900S ±1 mm accuracy), temperature monitoring via multi-point RTD sensors (Rosemount 3144P), tank overfill protection systems (Mobrey MSP400RH high-level switches), inventory management via Yokogawa Exaquantum R2.80

### Utility Systems Architecture
- **Steam Generation**: Package boilers (Cleaver-Brooks CBLE-700 700 HP fire-tube boilers) producing 600 psig superheated steam, deaerators removing dissolved oxygen (<0.005 ppm specification), steam distribution headers at 600/150/50 psig pressure levels
- **Cooling Water Systems**: Recirculating cooling water system with induced-draft cooling towers (SPX Marley NC8000 series 20,000 GPM circulation rate), circulating pumps (Flowserve ANSI B73.1 3x4x10 horizontal pumps), treatment chemicals for scaling/fouling/microbiological control
- **Compressed Air**: Oil-free reciprocating compressors (Gardner Denver EBE-99Q 500 SCFM capacity) producing instrument air at 125 psig, air dryers (Zeks HeatSinkless Dryer -40°F pressure dewpoint), distribution headers with automatic drains and filtration
- **Electrical Distribution**: 138 kV utility substation stepped down to 13.8 kV medium-voltage distribution, 4,160V motor control centers for large motors (>250 HP), 480V low-voltage switchgear, 208/120V control power via UPS systems (Eaton 93PM 500 kVA)

### Safety and Emergency Systems
- **Flare System**: Elevated flare (150-foot height) burning emergency relief loads, flare KO drum (20-foot diameter horizontal vessel) separating liquid hydrocarbon from vapor, smokeless operation via steam injection (Cashco Steam Injection Nozzles)
- **Fire Water Distribution**: Underground piping loop (12-inch ductile iron) fed by electric motor-driven pumps (Sulzer SNP Series 2,500 GPM at 150 psig) and diesel engine-driven emergency pump (Clarke Fire Protection JU12H-MBC 2,500 GPM)
- **Deluge Systems**: Water spray deluge systems protecting fired heaters, compressors, and storage tanks (2,500 GPM design density 0.25 GPM/ft²), activated via Det-Tronics X3301 flame detection with 2oo3 voting logic
- **Emergency Shutdown**: Schneider Electric Triconex v11.3 safety instrumented systems executing facility-wide ESD logic, pneumatic shutdown valves isolating process units, depressurization valves routing inventory to flare system
