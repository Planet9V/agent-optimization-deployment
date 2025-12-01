# Installation Best Practices - Commercial Facilities Security

## Pre-Installation Planning

**Site Survey and Assessment**
- Walk-through: document existing infrastructure and challenges
- Coverage mapping: identify camera placement for optimal field of view
- Network assessment: verify switch capacity, PoE budget, bandwidth
- Power requirements: calculate total PoE/AC power draw
- Cable pathway: conduit, j-hooks, cable tray routing plan
- Mounting surface: verify wall/ceiling construction (drywall, concrete, metal)
- Environmental: temperature, humidity, weather exposure analysis
- Lighting assessment: natural light, artificial lighting, day/night conditions
- Obstructions: identify trees, signs, vehicles blocking camera views
- Stakeholder interviews: security staff, operations, IT, facilities

**Network Infrastructure Requirements**
- Bandwidth calculation: resolution × fps × codec compression × camera count
- PoE budget: IEEE 802.3af (15.4W), 802.3at (30W), 802.3bt (60-90W) per device
- Switch selection: managed switches with VLAN, QoS, IGMP snooping
- Network segmentation: separate VLAN for security devices (cameras, access control)
- Firewall rules: allow RTSP (554), HTTP (80), HTTPS (443), ONVIF (80/8080)
- NTP server: configure network time synchronization
- DNS resolution: assign DNS for camera hostname resolution
- IP addressing: static IP assignments or DHCP reservations
- Redundancy: dual uplinks with spanning tree or link aggregation
- Documentation: network diagram with IP schema and port assignments

**Cable Infrastructure Design**
- Cable type: Cat6/Cat6a for PoE+, Cat5e for basic PoE
- Maximum distance: 328 feet (100m) for Ethernet, PoE extenders for beyond
- Conduit sizing: 40% fill ratio for future expansion
- Pull boxes: every 100 feet for long runs and direction changes
- Outdoor burial: direct burial Cat6 or conduit with drainage
- Labeling: cable labeling at both ends with device ID
- Testing: certify all cables with fluke tester before termination
- Grounding: proper grounding for outdoor cameras to prevent lightning damage
- Fire rating: plenum-rated (CMP) cables for HVAC spaces
- Separation: maintain 12-inch separation from AC power lines

## Camera Installation Standards

**Mounting Height and Angle**
- Facial recognition: 5-7 feet height with 10-15° downward angle
- License plate capture: 3-6 feet height with 5-10° downward angle
- Perimeter overview: 10-15 feet height with 20-30° downward angle
- Parking lot coverage: 20-30 feet on light poles with 35-45° angle
- Hallway monitoring: 8-10 feet height with corridor format (9:16 aspect)
- Entrance doors: 7-8 feet opposite door at 15-20° for facial capture
- Cash register: 6-8 feet height directly above for transaction view
- PTZ cameras: 15-25 feet height for wide area coverage
- 360° fisheye: ceiling mount 8-12 feet for panoramic coverage
- Avoid backlighting: position to avoid windows and direct sunlight

**Camera Aiming and Field of View**
- Rule of thirds: position subject in upper or lower third of frame
- Horizon line: keep horizon level to prevent Dutch angle distortion
- Overlap zones: 20-30% overlap between adjacent cameras for continuity
- Focus verification: test focus at near, middle, far distances
- White balance: auto white balance or manual for mixed lighting
- Exposure: center-weighted or spot metering for subject
- WDR tuning: adjust WDR strength for entrance backlight scenarios
- IR illumination: verify IR coverage without overexposure
- Privacy masking: configure masks for neighbor property and sensitive areas
- Test footage: record 24-hour test to verify day/night performance

**Weatherproofing and Environmental Protection**
- Gasket inspection: verify camera gasket integrity before mounting
- Cable entry: seal cable entry with silicone or cable gland
- Drip loop: create downward cable loop before entry point
- Mounting surface: seal screw holes with silicone after installation
- Sunshield: install sunshields for west-facing cameras
- Heater/blower: enable internal heater for sub-zero operation
- Desiccant: replace desiccant packs in humid environments
- Vandal housing: IK10-rated housings for accessible locations
- Corrosion protection: stainless steel hardware for coastal environments
- Inspection: quarterly weatherproofing inspection and resealing

## Access Control Installation

**Door Hardware Installation**
- Strike alignment: verify strike and latch alignment for smooth operation
- Gap measurement: maintain 1/8" gap for magnetic locks
- Bond sensor: install bond sensor on maglocks for lock status monitoring
- Request-to-exit: install PIR or push-button REx 42" from floor
- Door contact: recessed contact preferred, surface mount as backup
- Hinge side: ensure reader and REX on hinge side for safety
- ADA compliance: ensure 5 lbs maximum door opening force
- Fire code: verify fail-safe operation for fire-rated doors
- Conduit routing: route conduit through door frame or hinge
- Cable management: use door loop or power transfer for wire protection

**Reader Placement Standards**
- Mounting height: 42-48 inches from floor to reader center (ADA compliant)
- Wall clearance: 6-12 inches from door frame for hand clearance
- Card presentation: reader face parallel to approach direction
- Dual readers: both sides of door for entry/exit tracking
- Weatherproofing: use weather-resistant readers for exterior doors
- Lighting: verify adequate lighting for visual feedback (LEDs)
- Vandal protection: recessed or armored readers in public areas
- Wiring: minimum 6-conductor shielded cable for Wiegand
- OSDP wiring: 4-conductor for RS-485 OSDP communication
- Testing: verify read range (2-6 inches typical for Prox/iCLASS)

**Controller Installation and Wiring**
- Location: secure electrical room or IT closet with access control
- Power supply: dedicated 12VDC or 24VDC power supply with battery backup
- Voltage drop: calculate voltage drop for long cable runs to locks
- Fire alarm integration: relay connection to fire panel for unlock
- Tamper protection: enclosure tamper switch for security
- Network connection: Ethernet drop with PoE for IP-based controllers
- RS-485 termination: 120Ω termination resistor at each bus end
- Surge protection: install surge suppressors on network and power
- Labeling: label all wiring with device ID and circuit number
- Documentation: wiring diagram and as-built drawings

## Intrusion System Installation

**Sensor Placement Guidelines**
- PIR motion: corner mount 6-8 feet high for 90° coverage
- Pet immunity: adjust downward angle to create pet alley
- Glass break: mount on wall or ceiling within 25-foot radius
- Door/window contacts: recessed preferred, surface as alternative
- Shock sensors: mount on window frame for glass vibration detection
- Perimeter protection: exterior doors and accessible windows
- Interior protection: motion detectors in main corridors and rooms
- Redundant zones: dual detection in high-value areas
- Avoid HVAC: do not place PIRs near vents or heat sources
- Test walk: perform walk test to verify coverage and sensitivity

**Wiring and Communication**
- 4-conductor: minimum 22/4 for sensors with EOL supervision
- 6-conductor: for sensors with tamper circuits
- EOL resistor: install 5600Ω resistor for supervised zones
- Doubling: avoid doubling (parallel) zones for audit trail
- Class A/B wiring: Class A for critical zones requiring redundancy
- Cable color: use consistent color coding (red/black power, green/yellow zone)
- Wire nuts: avoid wire nuts, use crimp terminals or screw terminals
- Cable support: secure cables every 4 feet with staples or j-hooks
- Testing: test all zones for normal, alarm, tamper, open/short
- Documentation: zone list with sensor locations and wiring diagram

**Keypad and Annunciator Placement**
- Primary keypad: near main entrance within 30 feet of entry
- Secondary keypads: additional exits and high-traffic areas
- Mounting height: 48-52 inches to keypad center for ADA compliance
- Visibility: avoid placing keypads visible from exterior windows
- Lighting: ensure adequate lighting for keypad visibility
- Proximity: within reach of entry door for entry delay compliance
- Backup keypad: remote location for emergency disarm
- Wiring: 4-conductor or data bus for addressable keypads
- Power: local power supply or power from panel bus
- Testing: verify all function keys, display, and audio features

## Video Management System Setup

**NVR/Server Configuration**
- RAID configuration: RAID 5 minimum, RAID 6 for critical systems
- Storage allocation: calculate days of retention × bitrate × cameras
- Network settings: assign static IP on management VLAN
- Time synchronization: configure NTP server for accurate timestamps
- User accounts: create role-based accounts with strong passwords
- Recording schedule: continuous, motion, or scheduled by camera
- Retention policy: set automatic deletion after retention period
- Health monitoring: enable email alerts for HDD failure, camera offline
- Backup: schedule weekly configuration backup to external storage
- Firmware: maintain current firmware with quarterly update schedule

**Camera Integration and Configuration**
- Auto-discovery: use ONVIF discovery or manufacturer tool
- Manual addition: add cameras via IP address and credentials
- Default password: change default camera passwords immediately
- Streaming profiles: configure main stream (recording) and sub stream (live view)
- Frame rate: 15-30 fps for general surveillance, 30+ fps for fast motion
- Bitrate: 4-8 Mbps for 1080p, 8-12 Mbps for 4K depending on scene complexity
- GOP structure: I-frame interval 2x frame rate (30fps = 60 GOP)
- Compression: H.265 for bandwidth savings, H.264 for compatibility
- Analytics: enable motion detection, line crossing, intrusion detection
- Testing: verify 24-hour recording and playback functionality

**Network Video Storage Optimization**
- Tiered storage: SSD for recent footage, HDD for archive, NAS for long-term
- Deduplication: enable if supported to reduce storage consumption
- Compression: enable smart codecs (Zipstream, H.265+, SmartCodec)
- Pre/post-alarm: record 5-10 seconds pre-alarm, 30-60 seconds post-alarm
- Motion-based: reduce frame rate/bitrate during no-motion periods
- Edge storage: enable SD card recording for network failure resilience
- Archiving: export critical footage to external media for evidence
- Monitoring: track storage usage and expansion planning
- Bandwidth: limit bandwidth per camera to prevent network saturation
- Multicast: use multicast streaming for multiple simultaneous viewers

## Testing and Commissioning

**Functional Testing Checklist**
- Camera live view: verify all cameras streaming live video
- Recording: confirm recording to NVR/server storage
- Playback: test playback with timeline scrubbing
- Motion detection: trigger motion events and verify alerts
- PTZ control: test pan/tilt/zoom/preset functionality
- Analytics: verify line crossing, intrusion, loitering detection
- Two-way audio: test microphone and speaker functionality
- Access control: test card read, door unlock, REx operation
- Alarm system: test all zones for alarm, tamper, supervisory
- Integration: verify access control + video, intrusion + video linkage

**Performance and Load Testing**
- Concurrent streams: test maximum simultaneous live viewers
- Recording throughput: verify all cameras recording at target bitrate
- Playback performance: test multiple simultaneous playback streams
- Network bandwidth: measure actual bandwidth usage vs. calculated
- Storage write speed: verify RAID array write performance
- Failover: test server/controller failover and recovery time
- Camera offline: verify automatic reconnection after network loss
- System reboot: test automatic service startup after power cycle
- Remote access: verify mobile app and web client functionality
- Stress test: run 48-hour continuous operation test

**Documentation and Training**
- As-built drawings: CAD drawings with actual device locations
- IP address schedule: spreadsheet with all device IPs, MAC, credentials
- Wiring diagrams: detailed wiring schematics for all systems
- User manual: custom manual with site-specific procedures
- Standard operating procedures: alarm response, incident reporting
- Operator training: hands-on training for security staff (8-16 hours)
- Administrator training: advanced training for IT staff (16-24 hours)
- Video tutorials: record training sessions for future reference
- Warranty documentation: collect all warranty certificates
- Service contacts: list of integrator, manufacturer support contacts

## Maintenance and Preventive Care

**Quarterly Maintenance Schedule**
- Camera cleaning: clean dome/lens with microfiber cloth and lens cleaner
- Focus verification: verify focus has not drifted
- Weatherproofing: inspect seals, gaskets, and cable entries
- Mounting hardware: tighten all mounting screws and brackets
- HDD health: check SMART status and replace failing drives
- Firmware updates: apply security patches and feature updates
- Backup verification: test restore from backup
- Access control: test card readers, door hardware, REx sensors
- Intrusion sensors: walk test all motion detectors and contacts
- Battery backup: load test UPS and panel backup batteries

**Annual Comprehensive Inspection**
- Cable certification: re-test critical cables for degradation
- Network infrastructure: audit switch configurations and firmware
- Video audit: review camera coverage for changes in environment
- Analytics tuning: adjust detection zones and sensitivity
- User audit: review user accounts and remove terminated employees
- Security assessment: vulnerability scan and penetration test
- Disaster recovery: full disaster recovery drill
- Storage expansion: plan for storage upgrades based on usage trends
- Technology refresh: evaluate new camera/system replacements
- Contract renewal: review service agreements and warranties
