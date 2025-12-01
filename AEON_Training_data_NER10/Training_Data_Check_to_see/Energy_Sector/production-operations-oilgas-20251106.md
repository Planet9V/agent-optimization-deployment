# Production Operations - Oil & Gas Sector

## Entity-Rich Introduction
Oil and gas production operations coordinate {OPERATION}well production monitoring{/OPERATION} through {EQUIPMENT}Schneider Electric SCADAPack 575 remote terminal units (RTUs){/EQUIPMENT} acquiring data from {EQUIPMENT}Rosemount 3051S multivariable pressure transmitters{/EQUIPMENT}, {EQUIPMENT}Emerson Micro Motion F-Series Coriolis flow meters{/EQUIPMENT}, and {EQUIPMENT}ABB TotalFlow flow computers{/EQUIPMENT}. {OPERATION}Artificial lift optimization{/OPERATION} utilizes {EQUIPMENT}Lufkin SAM-L pump-off controllers{/EQUIPMENT} managing {OPERATION}rod pump stroke rates{/OPERATION} between 3-12 SPM via {EQUIPMENT}Baldor-Reliance 50HP electric motors{/EQUIPMENT} controlled by {EQUIPMENT}Allen-Bradley PowerFlex 525 variable frequency drives (VFDs){/EQUIPMENT}. {PROTOCOL}SCADA protocols including Modbus RTU, DNP3, and OPC UA{/PROTOCOL} enable {OPERATION}real-time production data aggregation{/OPERATION} from 250+ well sites to {ARCHITECTURE}Wonderware System Platform 2017 Update 3 centralized control room{/ARCHITECTURE}.

## Well Production Control

### Rod Pump (Sucker Rod) Operations
- **OPERATION**: {OPERATION}Pumping unit startup sequence{/OPERATION} - Verify {EQUIPMENT}Lufkin 228D-256-120 beam pumping unit{/EQUIPMENT} gearbox oil level, engage {OPERATION}manual brake release{/OPERATION}, initiate {OPERATION}slow-speed rotation{/OPERATION} at 4 SPM via {EQUIPMENT}SAM-L controller{/EQUIPMENT}
- **OPERATION**: {OPERATION}Dynamometer card analysis{/OPERATION} - {EQUIPMENT}Echometer Total Well Management (TWM) analyzer{/EQUIPMENT} processing {OPERATION}polished rod load{/OPERATION} (15,000 lbs peak) vs {OPERATION}position data{/OPERATION}, identifying {OPERATION}pump fillage issues{/OPERATION}, {OPERATION}gas interference{/OPERATION}, {OPERATION}worn plunger conditions{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Weatherford Mark II polished rod load cell{/EQUIPMENT} - Measuring {OPERATION}cyclic rod loads{/OPERATION} at 50 Hz sampling rate, transmitting via {PROTOCOL}4-20mA analog signal{/PROTOCOL} to {EQUIPMENT}Lufkin SAM-L controller{/EQUIPMENT}
- **OPERATION**: {OPERATION}Pump-off detection{/OPERATION} - {OPERATION}Automatic stroke rate reduction{/OPERATION} when downhole fluid level drops below pump intake depth (4,500 feet), preventing dry-running damage, resuming production at 6 SPM when fluid rebuilds
- **OPERATION**: {OPERATION}Rod string integrity monitoring{/OPERATION} - {EQUIPMENT}Ambyint AI-powered rod pump optimization{/EQUIPMENT} detecting {OPERATION}rod parting signatures{/OPERATION}, {OPERATION}tubing leaks{/OPERATION}, {OPERATION}valve failures{/OPERATION} via machine learning analysis of dyno cards

### Electric Submersible Pump (ESP) Operations
- **EQUIPMENT**: {EQUIPMENT}Schlumberger REDA Maximus ESP system{/EQUIPMENT} - 400 HP downhole pump (250 stages, 5,500 BPD capacity at 6,000 feet total dynamic head) driven by {EQUIPMENT}562 Series motor{/EQUIPMENT}, controlled via {EQUIPMENT}Phoenix Plus surface VFD{/EQUIPMENT}
- **OPERATION**: {OPERATION}ESP startup procedure{/OPERATION} - Ramp motor frequency from 0 to 60 Hz over 300 seconds, monitor {OPERATION}motor current (125A full load){/OPERATION}, {OPERATION}intake pressure (800 PSI){/OPERATION}, {OPERATION}discharge pressure (2,400 PSI){/OPERATION} via {EQUIPMENT}Centrilift Guardian sentinel downhole sensor{/EQUIPMENT}
- **OPERATION**: {OPERATION}Gas avoidance{/OPERATION} - Deploy {EQUIPMENT}Schlumberger Vortex II gas separator{/EQUIPMENT} below ESP intake, centrifugally separating free gas, venting to annulus via {OPERATION}reverse flow path{/OPERATION}
- **OPERATION**: {OPERATION}Variable speed control{/OPERATION} - {EQUIPMENT}Phoenix Plus VFD{/EQUIPMENT} modulating frequency 35-65 Hz based on {OPERATION}casing pressure setpoint control{/OPERATION} (450 PSI target), maintaining {OPERATION}pump intake pressure above bubble point{/OPERATION}
- **VENDOR**: {VENDOR}Baker Hughes Centrilift ESP monitoring{/VENDOR} - {EQUIPMENT}Odo downhole monitoring system{/EQUIPMENT} transmitting {OPERATION}motor temperature (185°F){/OPERATION}, {OPERATION}vibration (0.3 in/sec RMS){/OPERATION}, {OPERATION}shaft torque{/OPERATION} via {PROTOCOL}modulated power line carrier communication{/PROTOCOL}

### Gas Lift Operations
- **OPERATION**: {OPERATION}Gas injection rate control{/OPERATION} - {EQUIPMENT}Fisher ED 1-inch globe control valve{/EQUIPMENT} with {EQUIPMENT}DVC6200 digital positioner{/EQUIPMENT} throttling {OPERATION}injection gas flow{/OPERATION} from 250 MSCFD to 600 MSCFD, controlled by {EQUIPMENT}Emerson DeltaV PK controller{/EQUIPMENT}
- **EQUIPMENT**: {OPERATION}Gas lift mandrels{/OPERATION} - Install 6 mandrels at depths 3,500-6,200 feet, each housing {EQUIPMENT}Camco 1.5-inch nitrogen-charged gas lift valves{/EQUIPMENT} with {OPERATION}dome pressures ranging 400-900 PSI{/OPERATION}
- **OPERATION**: {OPERATION}Unloading sequence{/OPERATION} - Initiate high-rate gas injection (800 MSCFD) to activate deepest valve, progressively {OPERATION}lighten fluid column{/OPERATION}, transfer injection point to operating valve at 5,800 feet depth
- **OPERATION**: {OPERATION}Injection gas compression{/OPERATION} - {EQUIPMENT}Ariel JGK/4 reciprocating compressor (900 HP){/EQUIPMENT} boosting {OPERATION}low-pressure sales gas (80 PSI){/OPERATION} to {OPERATION}injection pressure (1,200 PSI){/OPERATION}, cooled via {EQUIPMENT}Hudson aftercooler (120°F discharge){/EQUIPMENT}
- **PROTOCOL**: {PROTOCOL}API RP 11V7 gas lift system design{/PROTOCOL} - Governing {OPERATION}mandrel spacing calculations{/OPERATION}, {OPERATION}valve selection criteria{/OPERATION}, {OPERATION}gradient curve analysis{/OPERATION}

### Hydraulic Jet Pump Operations
- **OPERATION**: {OPERATION}Power fluid circulation{/OPERATION} - {EQUIPMENT}Weatherford HydroJet surface power fluid unit{/EQUIPMENT} pumping {EQUIPMENT}filtered produced water{/EQUIPMENT} (5 micron) at 3,500 PSI, 450 BPD via {EQUIPMENT}National Oilwell Varco quintuplex plunger pump{/EQUIPMENT}
- **EQUIPMENT**: {EQUIPMENT}Downhole hydraulic jet pump{/EQUIPMENT} - {OPERATION}Nozzle/throat assembly{/OPERATION} creating {OPERATION}Venturi suction effect{/OPERATION}, lifting reservoir fluids from 7,500 feet, {OPERATION}nozzle sizing 10/64 inch{/OPERATION}, {OPERATION}throat sizing 18/64 inch{/OPERATION}
- **OPERATION**: {OPERATION}Free pump retrieval{/OPERATION} - Circulate power fluid at reduced pressure (1,800 PSI), hydraulic pump travels upward in tubing, retrieve via wireline jar at surface, replace with {OPERATION}alternate nozzle/throat configuration{/OPERATION}
- **OPERATION**: {OPERATION}Surface return flow metering{/OPERATION} - {EQUIPMENT}Emerson Micro Motion F300 Coriolis meter{/EQUIPMENT} measuring {OPERATION}combined production stream{/OPERATION} (power fluid + produced fluids), subtracting {OPERATION}known power fluid rate{/OPERATION} to calculate {OPERATION}net well production{/OPERATION}
- **VENDOR**: {VENDOR}Schlumberger JetPump services{/VENDOR} - {OPERATION}Hydraulic modeling software{/OPERATION} optimizing {OPERATION}nozzle/throat sizing{/OPERATION} based on {OPERATION}pump setting depth{/OPERATION}, {OPERATION}reservoir pressure{/OPERATION}, {OPERATION}fluid properties{/OPERATION}

## Production Separation

### Three-Phase Separator Operations
- **EQUIPMENT**: {EQUIPMENT}Sivalls 60-inch × 20-foot horizontal three-phase separator{/EQUIPMENT} - Rated 5,000 BPD liquid, 10 MMSCFD gas, {OPERATION}inlet gas scrubbing{/OPERATION}, {OPERATION}gravity settling{/OPERATION}, {OPERATION}coalescing pack oil/water separation{/OPERATION}
- **OPERATION**: {OPERATION}Pressure control{/OPERATION} - {EQUIPMENT}Fisher EZ 6-inch pressure control valve{/EQUIPMENT} maintaining {OPERATION}separator operating pressure 80 PSI{/OPERATION}, venting excess gas to {OPERATION}sales gas pipeline{/OPERATION} via {EQUIPMENT}Mooney M6300 pressure regulator{/EQUIPMENT}
- **OPERATION**: {OPERATION}Level control{/OPERATION} - {EQUIPMENT}Rosemount 5900S radar level transmitters{/EQUIPMENT} monitoring {OPERATION}oil/gas interface{/OPERATION}, {OPERATION}oil/water interface{/OPERATION}, modulating {EQUIPMENT}oil dump valve{/EQUIPMENT} and {EQUIPMENT}water dump valve{/EQUIPMENT} via {EQUIPMENT}Fisher 1052 level controllers{/EQUIPMENT}
- **OPERATION**: {OPERATION}Water removal{/OPERATION} - {EQUIPMENT}electrostatic coalescer pack{/EQUIPMENT} promoting {OPERATION}water droplet coalescence{/OPERATION}, achieving {OPERATION}< 1% BS&W (basic sediment and water) in oil outlet{/OPERATION}
- **PROTOCOL**: {PROTOCOL}API Spec 12J separator specification{/PROTOCOL} - Design requirements for {OPERATION}pressure vessel integrity{/OPERATION}, {OPERATION}safety relief sizing{/OPERATION}, {OPERATION}liquid retention time calculations{/OPERATION}

### Free Water Knockout (FWKO) Operations
- **EQUIPMENT**: {EQUIPMENT}National Tank Company 8-foot × 30-foot FWKO vessel{/EQUIPMENT} - {OPERATION}Inlet diverter baffle{/OPERATION}, {OPERATION}spreader system{/OPERATION}, {OPERATION}10-minute oil retention time{/OPERATION}, {OPERATION}water clarification section{/OPERATION}
- **OPERATION**: {OPERATION}Chemical injection{/OPERATION} - {EQUIPMENT}Milton Roy metering pump{/EQUIPMENT} injecting {EQUIPMENT}Champion X demulsifier (10-50 PPM){/EQUIPMENT} at separator inlet, enhancing {OPERATION}oil/water separation efficiency{/OPERATION}
- **OPERATION**: {OPERATION}Temperature control{/OPERATION} - {EQUIPMENT}indirect-fired heater treater{/EQUIPMENT} raising {OPERATION}emulsion temperature to 140°F{/OPERATION}, reducing {OPERATION}viscosity{/OPERATION}, accelerating {OPERATION}gravity separation{/OPERATION}
- **OPERATION**: {OPERATION}Skim oil recovery{/OPERATION} - {EQUIPMENT}adjustable weir skimmer{/OPERATION} collecting {OPERATION}oil layer{/OPERATION}, routing to {OPERATION}clean oil storage tank{/OPERATION}, {OPERATION}clarified water discharge{/OPERATION} to {OPERATION}produced water treatment system{/OPERATION}
- **VENDOR**: {VENDOR}NATCO Group separation equipment{/VENDOR} - Engineered systems including {OPERATION}electrostatic treaters{/OPERATION}, {OPERATION}gas flotation units{/OPERATION}, {OPERATION}hydrocyclone separators{/OPERATION}

### Gas Dehydration Operations
- **OPERATION**: {OPERATION}Glycol contacting{/OPERATION} - {EQUIPMENT}Peerless 24-inch × 15-foot triethylene glycol (TEG) contactor{/EQUIPMENT}, wet gas contacting {EQUIPMENT}95.5% lean glycol{/EQUIPMENT} over {OPERATION}12 bubble cap trays{/OPERATION}, achieving {OPERATION}< 7 lbs H2O/MMSCF outlet dew point{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Exterran glycol reboiler{/EQUIPMENT} - {OPERATION}Indirect-fired design{/OPERATION}, heating {OPERATION}rich glycol (88% concentration){/OPERATION} to {OPERATION}350°F{/OPERATION}, evaporating water, restoring {OPERATION}lean glycol concentration 95.5%{/OPERATION}
- **OPERATION**: {OPERATION}Glycol circulation control{/OPERATION} - {EQUIPMENT}Kimray glycol pump{/EQUIPMENT} (pneumatic diaphragm type) circulating 3-7 gallons glycol per pound of water removed, controlled via {EQUIPMENT}Kimray back pressure regulator{/OPERATION}
- **OPERATION}: {OPERATION}Regeneration gas stripping{/OPERATION} - Inject {OPERATION}0.5 SCFM stripping gas{/OPERATION} at reboiler bottom, enhancing {OPERATION}water removal efficiency{/OPERATION}, achieving {OPERATION}99.5% glycol purity{/OPERATION}
- **PROTOCOL**: {PROTOCOL}GPA 2174 water content measurement{/PROTOCOL} - Chilled mirror hygrometer testing per {OPERATION}sales gas specification requirements{/OPERATION} (typically 7 lbs/MMSCF maximum)

### Crude Oil Stabilization
- **EQUIPMENT**: {EQUIPMENT}Process Group 48-inch × 20-foot stabilizer column{/EQUIPMENT} - {OPERATION}12-tray distillation tower{/OPERATION} operating at {OPERATION}50 PSI, 250°F{/OPERATION}, separating {OPERATION}light ends (C1-C3){/OPERATION} from {OPERATION}stabilized crude oil{/OPERATION}
- **OPERATION**: {OPERATION}Reflux control{/OPERATION} - {EQUIPMENT}overhead condenser{/EQUIPMENT} cooling {OPERATION}vapor stream{/OPERATION} via {EQUIPMENT}air-cooled heat exchanger{/EQUIPMENT}, {EQUIPMENT}reflux drum{/EQUIPMENT} collecting condensate, {EQUIPMENT}pump{/EQUIPMENT} returning {OPERATION}10-30% reflux ratio{/OPERATION} to column top tray
- **OPERATION**: {OPERATION}Reboiler heating{/OPERATION} - {EQUIPMENT}kettle-type reboiler{/EQUIPMENT} with {OPERATION}hot oil circulation system (Therminol 66){/OPERATION}, maintaining {OPERATION}bottom temperature 300°F{/OPERATION}, {OPERATION}vaporizing light hydrocarbons{/OPERATION}
- **OPERATION**: {OPERATION}Vapor recovery{/OPERATION} - {OPERATION}Overhead vapor stream{/OPERATION} (primarily propane, butane) compressed via {EQUIPMENT}Ariel JGJ/2 compressor{/EQUIPMENT}, routed to {OPERATION}NGL recovery plant{/OPERATION} or {OPERATION}fuel gas system{/OPERATION}
- **VENDOR**: {VENDOR}UOP/Honeywell crude stabilization design{/VENDOR} - Process simulation using {EQUIPMENT}UniSim Design Suite{/EQUIPMENT}, optimizing {OPERATION}tray count{/OPERATION}, {OPERATION}feed stage location{/OPERATION}, {OPERATION}heat integration{/OPERATION}

## Production Metering and Allocation

### Multiphase Flow Metering
- **EQUIPMENT**: {EQUIPMENT}Schlumberger Vx Spectra multiphase meter{/EQUIPMENT} - {OPERATION}Dual-energy gamma ray absorption{/OPERATION}, {OPERATION}Venturi throat differential pressure{/OPERATION}, measuring {OPERATION}individual oil, water, gas rates{/OPERATION} ±5% accuracy across 0-100% water cut
- **OPERATION**: {OPERATION}Real-time composition analysis{/OPERATION} - Calculating {OPERATION}gas volume fraction (GVF 0-100%){/OPERATION}, {OPERATION}water liquid ratio (WLR 0-100%){/OPERATION}, {OPERATION}total liquid flow rate (50-8,000 BPD){/OPERATION}
- **PROTOCOL}: {PROTOCOL}ISO 20460 multiphase metering standard{/PROTOCOL} - Defining {OPERATION}performance requirements{/OPERATION}, {OPERATION}uncertainty calculations{/OPERATION}, {OPERATION}reference conditions{/OPERATION} for custody transfer applications
- **OPERATION**: {OPERATION}Well testing validation{/OPERATION} - Periodic comparison against {OPERATION}test separator measurements{/OPERATION}, {EQUIPMENT}Rosemount Daniel orifice meters{/EQUIPMENT} for gas, {EQUIPMENT}Emerson Coriolis meters{/EQUIPMENT} for liquid, verifying multiphase meter accuracy
- **VENDOR**: {VENDOR}Weatherford Red Eye MPFM{/VENDOR} - {OPERATION}Non-intrusive ultrasonic flow measurement{/OPERATION}, {OPERATION}microwave water cut analysis{/OPERATION}, suitable for {OPERATION}subsea installations{/OPERATION}

### Gas Flow Metering
- **EQUIPMENT**: {EQUIPMENT}Daniel Senior orifice fitting with 3-inch orifice plate{/EQUIPMENT} - {OPERATION}Flange-mounted design{/OPERATION}, {EQUIPMENT}Rosemount 3051S pressure transmitter{/EQUIPMENT} measuring {OPERATION}differential pressure 0-200 inH2O{/OPERATION}, calculating gas rate per {PROTOCOL}AGA Report No. 3 orifice metering{/PROTOCOL}
- **OPERATION**: {OPERATION}Flow computer calculations{/OPERATION} - {EQUIPMENT}Bristol Babcock ControlWave flow computer{/EQUIPMENT} applying {OPERATION}AGA-8 compressibility corrections{/OPERATION}, {OPERATION}pressure/temperature compensation{/OPERATION}, archiving {OPERATION}hourly/daily totalizations{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Ultrasonic gas meter{/EQUIPMENT} - {EQUIPMENT}Sick Maihak FLOWSIC600-XT 6-path meter{/EQUIPMENT}, {OPERATION}transit-time measurement{/OPERATION}, ±0.7% accuracy, {OPERATION}bidirectional flow capability{/OPERATION}
- **OPERATION}: {OPERATION}Gas quality monitoring{/OPERATION} - {EQUIPMENT}ABB NGC8206 gas chromatograph{/EQUIPMENT} analyzing {OPERATION}composition (C1-C6+, CO2, N2){/OPERATION} every 6 minutes, transmitting {OPERATION}heating value{/OPERATION}, {OPERATION}specific gravity{/OPERATION} to flow computer
- **PROTOCOL**: {PROTOCOL}API MPMS Chapter 14.3 orifice metering{/PROTOCOL} - Specifying {OPERATION}installation requirements{/OPERATION}, {OPERATION}straight run piping (10D upstream, 5D downstream){/OPERATION}, {OPERATION}flow conditioning{/OPERATION}

### Crude Oil LACT Units
- **EQUIPMENT**: {EQUIPMENT}Smith Meter 4-inch turbine meter{/EQUIPMENT} in {EQUIPMENT}API LACT (Lease Automatic Custody Transfer) unit{/EQUIPMENT} - {OPERATION}Strainer (40 mesh){/OPERATION}, {OPERATION}air eliminator{/OPERATION}, {OPERATION}meter prover connection{/OPERATION}, {OPERATION}BS&W monitor{/OPERATION}, {OPERATION}sampling system{/OPERATION}
- **OPERATION**: {OPERATION}Automatic sampling{/OPERATION} - {EQUIPMENT}Welker FLOWSTREAM proportional sampler{/EQUIPMENT} extracting {OPERATION}representative sample{/OPERATION} every 250 barrels, collecting in {OPERATION}composite sample container{/OPERATION} for {OPERATION}API gravity and BS&W testing{/OPERATION}
- **OPERATION**: {OPERATION}Bidirectional proving{/OPERATION} - {EQUIPMENT}10-barrel unidirectional prover{/EQUIPMENT}, {OPERATION}5-run proving sequence{/OPERATION} establishing {OPERATION}meter factor (typically 0.995-1.005){/OPERATION}, {OPERATION}repeatability < 0.05%{/OPERATION}
- **OPERATION**: {OPERATION}BS&W monitoring{/OPERATION} - {EQUIPMENT}AMETEK Grabner miniLAB analyzer{/EQUIPMENT} continuously measuring {OPERATION}water content{/OPERATION}, shutting LACT unit via {OPERATION}motorized block valve{/OPERATION} if BS&W exceeds 1.0%
- **PROTOCOL}: {PROTOCOL}API MPMS Chapter 6 LACT systems{/PROTOCOL} - Requirements for {OPERATION}automatic sampling{/OPERATION}, {OPERATION}BS&W monitoring{/OPERATION}, {OPERATION}automatic tank gauging{/OPERATION}, {OPERATION}data retention{/OPERATION}

### Allocation Metering Systems
- **ARCHITECTURE**: {ARCHITECTURE}Wellhead allocation system{/ARCHITECTURE} - {EQUIPMENT}Schlumberger Multiscan cluster manifold{/EQUIPMENT} sequencing {OPERATION}individual well production{/OPERATION} through {OPERATION}single test separator{/OPERATION}, {OPERATION}12-well automatic switching{/OPERATION} via {EQUIPMENT}pneumatic ball valves{/EQUIPMENT}
- **OPERATION**: {OPERATION}Test duration control{/OPERATION} - {EQUIPMENT}Allen-Bradley CompactLogix L36ERM controller{/EQUIPMENT} managing {OPERATION}2-hour test cycles per well{/OPERATION}, {OPERATION}valve actuation sequences{/OPERATION}, {OPERATION}settling time allowances{/OPERATION}
- **OPERATION**: {OPERATION}Back-allocation calculations{/OPERATION} - {EQUIPMENT}OSIsoft PI System{/EQUIPMENT} proportioning {OPERATION}commingled production{/OPERATION} based on {OPERATION}individual well test ratios{/OPERATION}, accounting for {OPERATION}production changes{/OPERATION}, {OPERATION}downtime events{/OPERATION}
- **VENDOR**: {VENDOR}Cameron Well Test Systems{/VENDOR} - {OPERATION}Mobile well testing units{/OPERATION}, {OPERATION}automated test separators{/OPERATION}, {OPERATION}data acquisition systems{/OPERATION}
- **PROTOCOL**: {PROTOCOL}SPE 101202 production allocation{/PROTOCOL} - Best practices for {OPERATION}measurement frequency{/OPERATION}, {OPERATION}allocation methodologies{/OPERATION}, {OPERATION}uncertainty analysis{/OPERATION}

## Tank Farm Operations

### Storage Tank Gauging
- **EQUIPMENT**: {EQUIPMENT}Rosemount 5900S radar level gauge{/EQUIPMENT} - Non-contact measurement in {EQUIPMENT}500-barrel production tanks{/EQUIPMENT}, ±1mm accuracy, {OPERATION}level{/OPERATION}, {OPERATION}temperature{/OPERATION}, {OPERATION}interface detection{/OPERATION}
- **OPERATION**: {OPERATION}Automatic tank gauging (ATG){/OPERATION} - {EQUIPMENT}Emerson TankMaster inventory management system{/EQUIPMENT} calculating {OPERATION}gross volume{/OPERATION}, {OPERATION}net standard volume{/OPERATION} per {PROTOCOL}API MPMS Chapter 12{/PROTOCOL}, applying {OPERATION}CTL (temperature correction){/OPERATION}, {OPERATION}CPL (pressure correction){/OPERATION}
- **OPERATION}: {OPERATION}Tank strapping{/OPERATION} - Physical measurement generating {OPERATION}tank capacity table{/OPERATION}, {OPERATION}height-to-volume correlation{/OPERATION}, accounting for {OPERATION}tank bottom irregularities{/OPERATION}, {OPERATION}dead volume{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Varec 2500 tank gauge{/EQUIPMENT} - {OPERATION}Float and tape mechanical gauge{/OPERATION}, {OPERATION}manual gauging reference{/OPERATION} for {OPERATION}ATG validation{/OPERATION}, {OPERATION}custody transfer witnessing{/OPERATION}
- **PROTOCOL**: {PROTOCOL}API MPMS Chapter 3 tank gauging{/PROTOCOL} - Standards for {OPERATION}manual gauging procedures{/OPERATION}, {OPERATION}temperature measurement{/OPERATION}, {OPERATION}water detection{/OPERATION}

### Vapor Recovery Systems
- **OPERATION}: {OPERATION}Tank vapor capture{/OPERATION} - {EQUIPMENT}Cimarron Energy vapor recovery unit (VRU){/EQUIPMENT} collecting {OPERATION}tank vapors{/OPERATION} via {EQUIPMENT}collection header (6-inch){/EQUIPMENT}, compressing to {OPERATION}sales gas pressure{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Blackmer HD332B rotary vane compressor{/EQUIPMENT} - {OPERATION}Two-stage compression{/OPERATION}, {OPERATION}inlet pressure -4 inH2O to +4 inH2O{/OPERATION}, {OPERATION}discharge pressure 80 PSI{/OPERATION}, {OPERATION}250 SCFM capacity{/OPERATION}
- **OPERATION**: {OPERATION}Pressure-vacuum relief{/OPERATION} - {EQUIPMENT}Groth VentSaver emergency relief valves{/EQUIPMENT}, {OPERATION}pressure setting +2 inH2O{/OPERATION}, {OPERATION}vacuum setting -8 inH2O{/OPERATION}, preventing {OPERATION}tank overpressure{/OPERATION} or {OPERATION}structural collapse{/OPERATION}
- **OPERATION**: {OPERATION}Flame arrestor protection{/OPERATION} - {EQUIPMENT}Protectoseal Series 2000 flame arrestors{/EQUIPMENT} on {OPERATION}tank thief hatches{/OPERATION}, preventing {OPERATION}flashback ignition{/OPERATION} during {OPERATION}gauging operations{/OPERATION}
- **PROTOCOL**: {PROTOCOL}40 CFR 60 Subpart OOOO NSPS{/PROTOCOL} - {OPERATION}VOC emission standards{/OPERATION} requiring {OPERATION}95% vapor capture efficiency{/OPERATION}, {OPERATION}annual performance testing{/OPERATION}

### Transfer Pumping Operations
- **EQUIPMENT**: {EQUIPMENT}Goulds 3196 centrifugal transfer pump (150 HP, 1,000 BPD){/EQUIPMENT} - Moving {OPERATION}crude oil{/OPERATION} from {OPERATION}production tanks{/OPERATION} to {OPERATION}pipeline custody transfer point{/OPERATION}
- **OPERATION**: {OPERATION}Pump VFD control{/OPERATION} - {EQUIPMENT}ABB ACS880 drive{/EQUIPMENT} modulating {OPERATION}pump speed 1,200-1,800 RPM{/OPERATION}, maintaining {OPERATION}pipeline pressure setpoint 350 PSI{/OPERATION} via {EQUIPMENT}Rosemount 3051S pressure transmitter feedback{/EQUIPMENT}
- **OPERATION**: {OPERATION}Suction strainer protection{/OPERATION} - {EQUIPMENT}Eaton Model 85 automatic backwashing strainer (200 mesh){/EQUIPMENT}, {OPERATION}differential pressure monitoring{/OPERATION}, initiating {OPERATION}backwash cycle{/OPERATION} when ΔP exceeds 15 PSI
- **OPERATION**: {OPERATION}Pump seal monitoring{/OPERATION} - {EQUIPMENT}John Crane Type 2100 mechanical seal{/EQUIPMENT} with {OPERATION}API Plan 11 flush{/OPERATION}, {EQUIPMENT}seal pot level switches{/EQUIPMENT} alarming on {OPERATION}low level indication{/OPERATION}
- **VENDOR**: {VENDOR}Flowserve pumping systems{/VENDOR} - {OPERATION}Hydraulic design{/OPERATION}, {OPERATION}NPSH calculations{/OPERATION}, {OPERATION}vibration analysis{/OPERATION}, {OPERATION}seal selection{/OPERATION}

## Produced Water Treatment

### Oil/Water Separation
- **EQUIPMENT**: {EQUIPMENT}NATCO skim tank (10-foot diameter × 30-foot){/EQUIPMENT} - {OPERATION}Gravity settling{/OPERATION}, {OPERATION}adjustable weir skimmer{/OPERATION}, reducing {OPERATION}oil content from 2,000 PPM to 500 PPM{/OPERATION}
- **OPERATION**: {OPERATION}Induced gas flotation{/OPERATION} - {EQUIPMENT}Wemco 12-foot diameter IGF cell{/EQUIPMENT}, {OPERATION}recycled water saturated with gas{/OPERATION} at {OPERATION}40 PSI{/OPERATION}, {OPERATION}pressure release{/OPERATION} creating {OPERATION}micro-bubbles{/OPERATION} floating oil droplets, achieving {OPERATION}< 50 PPM oil{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Hydrocyclone separator{/EQUIPMENT} - {EQUIPMENT}NATCO/CETCO 10-inch deoiling hydrocyclones{/EQUIPMENT}, {OPERATION}tangential injection{/OPERATION}, {OPERATION}centrifugal separation{/OPERATION}, {OPERATION}oil concentrate recycle to FWKO{/OPERATION}, {OPERATION}clean water to polishing treatment{/OPERATION}
- **OPERATION**: {OPERATION}Walnut shell filtration{/OPERATION} - {EQUIPMENT}US Filter 120-inch diameter media filters{/EQUIPMENT}, {OPERATION}crushed walnut shell media{/OPERATION}, {OPERATION}10 GPM/ft² loading rate{/OPERATION}, achieving {OPERATION}< 10 PPM oil content{/OPERATION}
- **PROTOCOL**: {PROTOCOL}EPA 40 CFR 435 offshore discharge limits{/PROTOCOL} - {OPERATION}Daily maximum 42 PPM oil{/OPERATION}, {OPERATION}monthly average 29 PPM{/OPERATION}, requiring {OPERATION}continuous monitoring{/OPERATION} via {EQUIPMENT}Turner Designs TD-4100XD fluorometer{/EQUIPMENT}

### Chemical Treatment
- **OPERATION**: {OPERATION}Biocide injection{/OPERATION} - {EQUIPMENT}Milton Roy MR metering pump{/EQUIPMENT} injecting {EQUIPMENT}glutaraldehyde biocide (100-200 PPM){/EQUIPMENT}, controlling {OPERATION}sulfate-reducing bacteria (SRB){/OPERATION}, preventing {OPERATION}microbiologically-influenced corrosion (MIC){/OPERATION}
- **OPERATION**: {OPERATION}Oxygen scavenging{/OPERATION} - {EQUIPMENT}sodium bisulfite injection{/EQUIPMENT} removing {OPERATION}dissolved oxygen{/OPERATION} from {OPERATION}injection water{/OPERATION}, maintaining {OPERATION}< 20 PPB O2{/OPERATION} per {PROTOCOL}NACE SP0198 injection water standard{/PROTOCOL}
- **OPERATION**: {OPERATION}Scale inhibitor treatment{/OPERATION} - {EQUIPMENT}polyaspartic acid scale inhibitor{/EQUIPMENT} preventing {OPERATION}calcium carbonate{/OPERATION}, {OPERATION}barium sulfate precipitation{/OPERATION} in {OPERATION}injection system{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Chemical injection skid{/EQUIPMENT} - {EQUIPMENT}multiple metering pumps{/EQUIPMENT}, {OPERATION}day tanks{/OPERATION}, {OPERATION}injection quills{/OPERATION}, controlled via {ARCHITECTURE}Allen-Bradley MicroLogix 1400 PLC{/ARCHITECTURE}
- **VENDOR**: {VENDOR}Baker Hughes production chemicals{/VENDOR} - {OPERATION}Corrosion inhibitors{/OPERATION}, {OPERATION}scale inhibitors{/OPERATION}, {OPERATION}biocides{/OPERATION}, {OPERATION}demulsifiers{/OPERATION}, {OPERATION}paraffin inhibitors{/OPERATION}

### Water Injection Operations
- **EQUIPMENT**: {EQUIPMENT}Sulzer HPT high-pressure triplex plunger pump{/EQUIPMENT} - {OPERATION}3,000 BPD capacity{/OPERATION}, {OPERATION}3,500 PSI discharge pressure{/OPERATION}, driven by {EQUIPMENT}500 HP electric motor{/EQUIPMENT} via {EQUIPMENT}Rexnord Omega fluid coupling{/EQUIPMENT}
- **OPERATION**: {OPERATION}Suction filtration{/OPERATION} - {EQUIPMENT}Eaton MHF100 automatic backwash filter (2 micron){/EQUIPMENT}, {OPERATION}cartridge filter polishing (0.5 micron){/EQUIPMENT}, preventing {OPERATION}formation plugging{/OPERATION}
- **OPERATION**: {OPERATION}Injection well allocation{/OPERATION} - {EQUIPMENT}Header manifold{/EQUIPMENT} distributing water to {OPERATION}12 injection wells{/OPERATION}, {EQUIPMENT}individual well orifice plates{/EQUIPMENT} controlling {OPERATION}injection rates 150-400 BPD per well{/OPERATION}
- **OPERATION**: {OPERATION}Injection rate control{/OPERATION} - {EQUIPMENT}Fisher ED control valves{/EQUIPMENT} at each wellhead, {OPERATION}flow control loops{/OPERATION} maintaining {OPERATION}target injection rates{/OPERATION}, compensating for {OPERATION}wellhead pressure variations{/OPERATION}
- **PROTOCOL**: {PROTOCOL}API RP 27 waterflood operations{/PROTOCOL} - {OPERATION}Water quality requirements{/OPERATION}, {OPERATION}filtration standards{/OPERATION}, {OPERATION}injection monitoring{/OPERATION}, {OPERATION}falloff testing{/OPERATION}

## Facility Automation and SCADA

### RTU and PLC Systems
- **ARCHITECTURE**: {ARCHITECTURE}Schneider Electric SCADAPack 575 RTU{/ARCHITECTURE} - {OPERATION}32 analog inputs (4-20mA){/OPERATION}, {OPERATION}16 digital inputs{/OPERATION}, {OPERATION}8 analog outputs{/OPERATION}, {OPERATION}12 digital outputs{/OPERATION}, {PROTOCOL}Modbus RTU/TCP protocol{/PROTOCOL}
- **OPERATION**: {OPERATION}Local logic execution{/OPERATION} - {OPERATION}PID control loops{/OPERATION} for {OPERATION}separator pressure{/OPERATION}, {OPERATION}tank level control{/OPERATION}, {OPERATION}gas lift valve positioning{/OPERATION}, {OPERATION}automatic well shutdown{/OPERATION} on alarm conditions
- **EQUIPMENT**: {EQUIPMENT}Allen-Bradley CompactLogix L33ER controller{/EQUIPMENT} - {OPERATION}Distributed I/O{/OPERATION} via {PROTOCOL}EtherNet/IP{/PROTOCOL}, {EQUIPMENT}FLEX I/O modules{/EQUIPMENT}, {OPERATION}HMI connection{/OPERATION} to {EQUIPMENT}PanelView Plus 7 touchscreens{/EQUIPMENT}
- **OPERATION**: {OPERATION}Sequential control{/OPERATION} - {OPERATION}Startup/shutdown sequences{/OPERATION}, {OPERATION}valve interlocking{/OPERATION}, {OPERATION}permissive logic{/OPERATION}, programmed in {OPERATION}Rockwell RSLogix 5000{/OPERATION}
- **PROTOCOL**: {PROTOCOL}DNP3 Secure Authentication{/PROTOCOL} - {OPERATION}Encrypted SCADA communications{/OPERATION} between {OPERATION}field RTUs{/OPERATION} and {OPERATION}central control room{/OPERATION}, per {PROTOCOL}IEEE 1815-2012 standard{/PROTOCOL}

### SCADA Host System
- **ARCHITECTURE**: {ARCHITECTURE}Wonderware System Platform 2017 Update 3{/ARCHITECTURE} - {OPERATION}Distributed SCADA architecture{/OPERATION}, {OPERATION}InTouch HMI{/OPERATION}, {OPERATION}Historian data archiving{/OPERATION}, {OPERATION}alarm management{/OPERATION}
- **OPERATION**: {OPERATION}Real-time monitoring{/OPERATION} - {OPERATION}Production dashboard displays{/OPERATION}, {OPERATION}250+ well sites{/OPERATION}, {OPERATION}50+ tank batteries{/OPERATION}, {OPERATION}gas compression stations{/OPERATION}, {OPERATION}water injection facilities{/OPERATION}
- **OPERATION**: {OPERATION}Alarm management{/OPERATION} - {OPERATION}Priority-based alarming{/OPERATION} (critical, high, medium, low), {OPERATION}alarm shelving{/OPERATION}, {OPERATION}SMS text notifications{/OPERATION} via {EQUIPMENT}MultiTech wireless modem{/EQUIPMENT}
- **EQUIPMENT**: {EQUIPMENT}OSIsoft PI System{/EQUIPMENT} - {OPERATION}High-resolution data historian{/OPERATION}, {OPERATION}1-second data capture{/OPERATION}, {OPERATION}compression algorithms{/OPERATION}, {OPERATION}multi-year trending{/OPERATION}, {OPERATION}production reporting{/OPERATION}
- **VENDOR**: {VENDOR}Honeywell Experion SCADA{/VENDOR} - Alternative platform with {OPERATION}redundant servers{/OPERATION}, {OPERATION}OPC UA connectivity{/OPERATION}, {OPERATION}mobile HMI access{/OPERATION}

### Communication Infrastructure
- **PROTOCOL}: {PROTOCOL}Licensed 900 MHz radio network{/PROTOCOL} - {EQUIPMENT}MDS 9710 broadband radios{/EQUIPMENT}, {OPERATION}point-to-multipoint topology{/OPERATION}, {OPERATION}1.5 Mbps throughput{/OPERATION}, {OPERATION}20-mile range{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Cisco 819 industrial integrated services routers{/EQUIPMENT} - {OPERATION}4G LTE cellular backup{/OPERATION}, {OPERATION}VPN tunneling{/OPERATION}, {OPERATION}firewall{/OPERATION}, {OPERATION}routing{/OPERATION} for {OPERATION}remote site connectivity{/OPERATION}
- **OPERATION**: {OPERATION}Network redundancy{/OPERATION} - {OPERATION}Primary 900 MHz radio path{/OPERATION}, {OPERATION}failover to cellular LTE{/OPERATION}, {OPERATION}automatic switchover{/OPERATION} within {OPERATION}60 seconds{/OPERATION}
- **PROTOCOL**: {PROTOCOL}IEC 62351 security standards{/PROTOCOL} - {OPERATION}Encrypted SCADA communications{/OPERATION}, {OPERATION}certificate-based authentication{/OPERATION}, {OPERATION}role-based access control{/OPERATION}
- **ARCHITECTURE**: {ARCHITECTURE}Industrial DMZ{/ARCHITECTURE} - {EQUIPMENT}Palo Alto PA-220 firewalls{/EQUIPMENT} segregating {OPERATION}production control network{/OPERATION} from {OPERATION}corporate IT{/OPERATION}, {OPERATION}unidirectional data diodes{/OPERATION} for historian replication

### Production Optimization Software
- **VENDOR**: {VENDOR}Weatherford ForeSite production optimization{/VENDOR} - {OPERATION}ESP surveillance{/OPERATION}, {OPERATION}gas lift optimization{/OPERATION}, {OPERATION}beam pump diagnostics{/OPERATION}, {OPERATION}well performance analytics{/OPERATION}
- **OPERATION**: {OPERATION}Artificial lift optimization{/OPERATION} - {OPERATION}Machine learning algorithms{/OPERATION} recommending {OPERATION}optimal ESP frequencies{/OPERATION}, {OPERATION}gas lift injection rates{/OPERATION}, {OPERATION}pump stroke rates{/OPERATION}, maximizing {OPERATION}production{/OPERATION} while minimizing {OPERATION}energy consumption{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}PI Vision analytics{/EQUIPMENT} - {OPERATION}Production performance dashboards{/OPERATION}, {OPERATION}KPI calculations{/OPERATION} (uptime, production efficiency, gas-oil ratio trends), {OPERATION}predictive maintenance alerts{/OPERATION}
- **OPERATION**: {OPERATION}Virtual flow metering{/OPERATION} - {OPERATION}Physics-based models{/OPERATION} estimating {OPERATION}well production rates{/OPERATION} from {OPERATION}readily available measurements{/OPERATION} (pressure, temperature), reducing {OPERATION}well testing frequency{/OPERATION}
- **PROTOCOL**: {PROTOCOL}OPC UA data exchange{/PROTOCOL} - {OPERATION}Seamless integration{/OPERATION} between {OPERATION}SCADA systems{/OPERATION}, {OPERATION}optimization software{/OPERATION}, {OPERATION}corporate ERP systems{/OPERATION}

## Safety and Environmental Compliance

### Fire and Gas Detection
- **EQUIPMENT**: {EQUIPMENT}Det-Tronics Eagle Quantum Premier fire and gas system{/EQUIPMENT} - {OPERATION}Addressable analog detectors{/OPERATION}, {OPERATION}flame detectors (UV/IR){/OPERATION}, {OPERATION}combustible gas detectors (catalytic bead){/OPERATION}, {OPERATION}H2S monitors{/OPERATION}
- **OPERATION**: {OPERATION}Voting logic{/OPERATION} - {OPERATION}2-out-of-3 voting{/OPERATION} for {OPERATION}critical shutdown actions{/OPERATION}, preventing {OPERATION}spurious trips{/OPERATION} while ensuring {OPERATION}safety integrity{/OPERATION}
- **OPERATION**: {OPERATION}Emergency shutdown (ESD) sequences{/OPERATION} - {OPERATION}Isolate fuel gas to heaters/engines{/OPERATION}, {OPERATION}close wellhead master valves{/OPERATION}, {OPERATION}activate deluge systems{/OPERATION}, {OPERATION}sound evacuation alarms{/OPERATION}
- **EQUIPMENT**: {EQUIPMENT}Draeger Polytron 8720 IR combustible gas detector{/EQUIPMENT} - {OPERATION}0-100% LEL methane detection{/OPERATION}, {OPERATION}alarm setpoints 20% LEL and 40% LEL{/OPERATION}, {OPERATION}4-20mA output{/OPERATION} to {OPERATION}fire panel{/OPERATION}
- **PROTOCOL**: {PROTOCOL}API RP 14C fire protection analysis{/PROTOCOL} - {OPERATION}Hazard identification{/OPERATION}, {OPERATION}fire scenario modeling{/OPERATION}, {OPERATION}detector spacing calculations{/OPERATION}, {OPERATION}deluge system design{/OPERATION}

### Emission Monitoring and Reporting
- **OPERATION**: {OPERATION}Continuous emissions monitoring{/OPERATION} - {EQUIPMENT}SICK MCS100FT flare gas analyzer{/EQUIPMENT} measuring {OPERATION}methane, CO2{/OPERATION} in {OPERATION}flare gas stream{/OPERATION}, calculating {OPERATION}emissions reporting{/OPERATION} per {PROTOCOL}EPA Greenhouse Gas Reporting Rule{/PROTOCOL}
- **EQUIPMENT**: {EQUIPMENT}FLIR GF320 infrared camera{/EQUIPMENT} - {OPERATION}Optical gas imaging (OGI){/OPERATION} for {OPERATION}leak detection and repair (LDAR) surveys{/OPERATION}, identifying {OPERATION}fugitive methane emissions{/OPERATION}
- **OPERATION**: {OPERATION}Quarterly LDAR inspections{/OPERATION} - Per {PROTOCOL}40 CFR 60 Subpart OOOO{/PROTOCOL}, inspect {OPERATION}valves, connectors, pump seals{/OPERATION}, tag leaks, {OPERATION}repair within 30 days{/OPERATION}, document via {EQUIPMENT}LDAR tracking software{/EQUIPMENT}
- **OPERATION**: {OPERATION}Flare minimization{/OPERATION} - {OPERATION}Vapor recovery units{/OPERATION} capturing {OPERATION}tank vapors{/OPERATION}, {OPERATION}routing to sales gas{/OPERATION}, reducing {OPERATION}routine flaring{/OPERATION}, meeting {OPERATION}zero routine flaring initiatives{/OPERATION}
- **VENDOR**: {VENDOR}Heath Consultants LDAR services{/VENDOR} - {OPERATION}Method 21 monitoring{/OPERATION}, {OPERATION}OGI surveys{/OPERATION}, {OPERATION}regulatory reporting{/OPERATION}, {OPERATION}repair tracking{/OPERATION}

### Spill Prevention and Response
- **PROTOCOL**: {PROTOCOL}40 CFR 112 SPCC Plan{/PROTOCOL} - {OPERATION}Secondary containment design{/OPERATION}, {OPERATION}tank dike volume calculations{/OPERATION}, {OPERATION}integrity testing{/OPERATION}, {OPERATION}personnel training{/OPERATION}, {OPERATION}equipment inspection schedules{/OPERATION}
- **OPERATION**: {OPERATION}Tank dike inspection{/OPERATION} - {OPERATION}Monthly visual inspection{/OPERATION} of {OPERATION}earthen dikes{/OPERATION}, {OPERATION}liner integrity{/OPERATION}, {OPERATION}drain valve closures{/OPERATION}, {OPERATION}precipitation removal{/OPERATION}
- **EQUIPMENT**: {OPERATION}Spill response equipment{/OPERATION} - {OPERATION}Absorbent pads and booms{/EQUIPMENT}, {OPERATION}portable transfer pumps{/EQUIPMENT}, {OPERATION}temporary storage tanks{/EQUIPMENT}, staged at {OPERATION}central facilities{/OPERATION}
- **OPERATION**: {OPERATION}Spill reporting procedures{/OPERATION} - {OPERATION}Immediate notification{/OPERATION} to {OPERATION}National Response Center{/OPERATION} for spills {OPERATION}> 1 barrel to navigable waters{/OPERATION}, {OPERATION}state agencies{/OPERATION}, {OPERATION}operator management{/OPERATION}
- **VENDOR**: {VENDOR}Clean Harbors emergency response{/VENDOR} - {OPERATION}24/7 spill response{/OPERATION}, {OPERATION}vacuum truck services{/OPERATION}, {OPERATION}contaminated soil remediation{/OPERATION}, {OPERATION}waste disposal{/OPERATION}
