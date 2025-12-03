# Critical Manufacturing: Physical Security Patterns

**File:** 02_Security_Patterns_Physical.md
**Created:** 2025-11-05 14:30:00 UTC
**Version:** v1.0.0
**Author:** Security Architecture Team
**Purpose:** Comprehensive physical security patterns for critical manufacturing facilities
**Status:** ACTIVE

## Pattern Categories

This document covers **150+ physical security patterns** across:
- Perimeter Security (25 patterns)
- Access Control (30 patterns)
- Clean Room Security (25 patterns)
- Surveillance Systems (20 patterns)
- Intrusion Detection (20 patterns)
- Emergency Response (30 patterns)

---

## 1. PERIMETER SECURITY PATTERNS

### Pattern PS-001: Multi-Layer Perimeter Defense

**Context:** Critical manufacturing facilities require defense-in-depth against unauthorized access.

**Problem:** Single-layer perimeter security provides insufficient protection against determined adversaries.

**Solution:**
Implement concentric security zones with increasing security controls:

**Layer 1 - Property Boundary:**
- Fencing: 8-foot chain link with 3-strand barbed wire outrigger
- Signage: "No Trespassing" and "Security Cameras in Use"
- Lighting: 1-2 foot-candles at ground level
- Clear zone: 20 feet inside fence line, vegetation management
- Bollards at vehicle entry points

**Layer 2 - Facility Perimeter:**
- Building envelope security (hardened doors, windows)
- Mantrap vestibules at all entry points
- Vehicle barriers: K12-rated bollards at loading docks
- Exterior lighting: 5-10 foot-candles at doors
- CCTV coverage: 100% of perimeter with no blind spots

**Layer 3 - Internal Zoning:**
- Badge-controlled interior doors
- Clean room airlocks with gowning areas
- Restricted area designation and marking
- Server room/network closet hardening
- Storage cage for high-value materials

**Layer 4 - Asset-Level Protection:**
- Equipment lockout/tagout procedures
- Tool crib access controls
- Safe/vault for sensitive documents
- Laptop cable locks for mobile devices
- Escort requirements for visitors in restricted areas

**Consequences:**
- ✅ Defense-in-depth reduces single-point-of-failure risks
- ✅ Layered approach increases detection probability
- ✅ Delays intruders, allowing security response time
- ⚠️ Higher implementation and maintenance costs
- ⚠️ Potential impact on operational efficiency

**Related Patterns:** PS-002 (Fence Line Sensors), AC-001 (Badge Access Control), SD-005 (Perimeter Camera Design)

---

### Pattern PS-002: Intelligent Fence Line Detection

**Context:** Perimeter fences are primary barrier but easily breached without detection systems.

**Problem:** Physical fences alone do not alert security personnel to breach attempts in real-time.

**Solution:**
Deploy integrated fence-mounted intrusion detection with analytics:

**Technology Options:**

*Fiber Optic Sensors:*
- Distributed acoustic sensing (DAS) cables
- Detects vibrations from climbing, cutting, lifting
- Low false alarm rate (< 1 per zone per day)
- Installation: Woven through chain link or mounted to posts
- Zone length: 100-300 feet per sensor segment

*Buried Cable Sensors:*
- Coaxial or fiber optic buried sensors
- Detects ground vibrations and pressure changes
- Installation: 12-18 inches deep, 3-6 feet from fence
- Immune to weather and environmental interference
- Requires clear zone maintenance

*Microwave/Infrared Barriers:*
- Dual-technology transmitter-receiver pairs
- Creates invisible detection zone along fence line
- Adjustable detection zones (5-200 feet)
- Height: 6-12 inches above grade to 8 feet high
- Weather-resistant, suitable for all climates

**Integration Requirements:**
- Connect to video management system (VMS) for visual verification
- Integrate with physical security information management (PSIM)
- Alarm prioritization: Immediate dispatch for fence alarms
- GPS coordinates for precise breach location
- Historical data logging for pattern analysis

**Operational Procedures:**
- Regular sensor testing (weekly walk-test)
- Nuisance alarm tracking and adjustment
- Vegetation trimming schedule to prevent interference
- Security officer training on sensor locations and response
- Maintenance contract with 24-hour support

**Consequences:**
- ✅ Early detection of perimeter breaches (15-30 seconds)
- ✅ Precise location information for security response
- ✅ Recorded evidence for investigations
- ⚠️ Requires ongoing maintenance and calibration
- ⚠️ Environmental factors (wildlife, weather) may cause nuisance alarms

**Related Patterns:** PS-003 (Clear Zone Management), SD-006 (Slew-to-Cue Cameras), EM-002 (Alarm Response Procedures)

---

### Pattern PS-003: Clear Zone Management

**Context:** Vegetation and objects near perimeter fences create security vulnerabilities.

**Problem:** Overgrown vegetation provides concealment for intruders and interferes with detection systems.

**Solution:**
Establish and maintain clear zones around all perimeter fences:

**Clear Zone Specifications:**

*Inside Fence (Facility Side):*
- Width: Minimum 20 feet from fence line
- Surface: Gravel, concrete, or maintained grass (< 3 inches)
- Objects: No vehicles, equipment, materials, or structures
- Vegetation: No trees, shrubs, or tall grasses
- Lighting: Unobstructed fixture placement and light distribution

*Outside Fence (Property Boundary):*
- Width: Minimum 10 feet where property allows
- Vegetation: Tree trimming to 8 feet above grade
- Objects: No objects that could aid climbing or concealment
- Sight lines: Maintain visibility from security posts and cameras
- Landscaping: Low-profile ornamental options only

**Maintenance Schedule:**
- Weekly: Visual inspection of clear zone condition
- Bi-weekly: Grass mowing and weed control
- Monthly: Tree and shrub trimming
- Quarterly: Gravel/surface material replenishment
- Annual: Herbicide application and major vegetation removal

**Monitoring and Enforcement:**
- Security patrol checklist includes clear zone inspection
- Facilities/grounds team responsible for maintenance
- Photo documentation of condition (monthly)
- Metrics: Percentage of perimeter in compliance
- Remediation timeline: 24-48 hours for identified issues

**Consequences:**
- ✅ Improved camera sight lines and lighting effectiveness
- ✅ Reduced false alarms from sensor systems
- ✅ Eliminates concealment for intruders
- ✅ Easier security patrol and visual assessment
- ⚠️ Ongoing maintenance costs (labor and materials)
- ⚠️ Aesthetic considerations may conflict with security needs

**Related Patterns:** PS-002 (Fence Line Sensors), SD-005 (Perimeter Camera Design), PS-007 (Security Lighting Design)

---

### Pattern PS-004: Vehicle Barrier Systems

**Context:** Vehicular ramming attacks pose significant risk to critical manufacturing facilities.

**Problem:** Standard bollards may not provide adequate protection against large vehicles at high speed.

**Solution:**
Deploy crash-rated vehicle barriers appropriate to threat level and operational needs:

**Threat Assessment:**
- Vehicle type: Sedan (5,000 lbs), SUV (7,500 lbs), Truck (15,000+ lbs)
- Speed: 30 mph, 40 mph, 50 mph
- Rating: K4 (30 mph), K8 (40 mph), K12 (50 mph)
- Penetration allowance: 3 feet, 1 foot, or zero penetration
- Attack scenarios: Intentional ramming vs. accidental vehicle loss

**Barrier Types:**

*Fixed Bollards:*
- Steel pipe filled with concrete
- Diameter: 8-12 inches
- Depth: 36-48 inches below grade
- Spacing: 3-5 feet center-to-center
- Surface mount or embedded
- K8 or K12 rated for critical areas

*Removable Bollards:*
- Receivers embedded in concrete
- Lockable cap when removed
- Use for occasional vehicle access needs
- Slower deployment than automatic systems
- Same crash rating as fixed bollards

*Automatic/Hydraulic Barriers:*
- Rising bollards or barriers
- Deploy in < 5 seconds
- Remote or automatic control
- Battery backup for power outage
- LED lights for visibility
- Higher cost but flexible operations

*Passive Barriers:*
- Jersey barriers (concrete)
- Earthen berms
- Water-filled barriers
- Strategically placed landscape features
- Lower cost but less aesthetic

**Strategic Placement:**

*High Priority Locations:*
1. Main entrance gatehouse approach
2. Loading dock areas
3. Facility entry doors within 50 feet of vehicle paths
4. Clean room exterior walls within 100 feet of roads
5. Utility infrastructure (transformers, chillers, generators)
6. Parking areas adjacent to buildings

**Operational Considerations:**
- Emergency vehicle access requirements
- Delivery truck access and scheduling
- Employee parking convenience
- Visitor experience and aesthetic impact
- Maintenance access for landscaping and utilities
- Snow removal and drainage

**Maintenance:**
- Monthly: Visual inspection of bollard condition
- Quarterly: Hydraulic system testing and lubrication
- Annual: Structural assessment and paint/coating refresh
- After impact: Immediate inspection and repair/replacement
- Documentation: Photos and condition reports

**Consequences:**
- ✅ Protection against vehicle-borne improvised explosives (VBIED)
- ✅ Prevent accidental vehicle collisions with buildings
- ✅ Clearly demarcate vehicle and pedestrian zones
- ✅ Durable and long-lasting security control
- ⚠️ High initial cost ($500-$5,000 per bollard installed)
- ⚠️ May conflict with accessibility requirements
- ⚠️ Requires civil engineering and permitting

**Related Patterns:** PS-001 (Multi-Layer Perimeter), AC-006 (Vehicle Access Control), EM-005 (Emergency Vehicle Access)

---

### Pattern PS-005: Shipping/Receiving Security

**Context:** Loading docks and shipping areas present high-risk access points for theft, sabotage, and espionage.

**Problem:** Operational demands for fast cargo handling often conflict with security protocols.

**Solution:**
Implement structured shipping/receiving security that balances operational efficiency with protection:

**Physical Security Measures:**

*Dock Design:*
- Separate inbound and outbound docks where possible
- Dock levelers with security locks when not in use
- Dock shelters/seals to prevent gap access
- Interior roll-up doors between dock and facility
- Mantrap design: Exterior and interior doors never open simultaneously
- Security cage or holding area for unverified shipments

*Access Control:*
- Badge readers: Shipping/receiving personnel only
- Escort requirements: All drivers remain with security or escort
- Driver check-in: Separate entrance, not through dock area
- Visitor badges: High-visibility, temporary, tracked
- Vehicle placarding: Pre-registered vehicles only
- Time windows: Deliveries only during staffed hours

**Procedural Security:**

*Inbound Shipments:*
1. Driver arrival: Check-in at security post, verification against delivery schedule
2. Vehicle inspection: Visual inspection of trailer interior (no unauthorized persons/materials)
3. Seal verification: Record seal numbers, verify against shipping documents
4. Dock assignment: Designated dock door based on shipment type/security
5. Unloading supervision: Shipping/receiving staff present during entire unloading
6. Count and inspect: Verify quantity and condition against packing list
7. Segregation: Hold shipments in secure area until inspection complete
8. Documentation: Sign BOL, record seal removal, photograph discrepancies
9. Vehicle egress: Security inspection before allowing departure

*Outbound Shipments:*
1. Internal authorization: Approved shipping order from authorized personnel
2. Staging: Product moved to shipping area by authorized personnel only
3. Documentation: Generate packing list, shipping labels, export paperwork
4. Inspection: Quality and security verification before loading
5. Loading supervision: Authorized personnel only during loading
6. Seal application: Apply numbered, tamper-evident seals, record in system
7. Driver signature: Obtain signature on BOL, provide shipping documents
8. Departure verification: Security confirms seal intact before gate release

**Technology Integration:**

*Video Surveillance:*
- Camera coverage: All dock doors, staging areas, holding areas
- Recording: Continuous recording, 90-day retention
- Analytics: Loitering detection, unusual activity alerts
- Remote monitoring: Security operations center (SOC) view

*Access Control:*
- Badge readers: Interior and exterior doors
- Alarm integration: After-hours access alerts
- Interlock system: Prevent simultaneous door opening
- Override capability: Emergency egress always available

*Inventory Management:*
- Barcode scanning: Track all items in/out
- RFID: High-value or serialized items
- Weight verification: Platform scales for outbound loads
- Discrepancy alerts: Automatic notification of quantity variances

**Personnel Security:**

*Shipping/Receiving Staff:*
- Background screening: Criminal history, employment verification
- Training: Security procedures, export control, incident reporting
- Rotation: Periodic rotation to different duties
- Supervision: Oversight by management
- Dual control: Two-person integrity for high-value shipments

*Drivers/Carriers:*
- Vetted carriers: Pre-approved carrier list with security requirements
- Driver check-in: Photo ID verification, purpose of visit
- Escort: Remain with security or designated escort at all times
- Restricted areas: No access beyond loading dock area
- Monitoring: Continuous supervision while on-site

**Audit and Compliance:**
- Daily: Review shipping/receiving logs for completeness
- Weekly: Physical inventory spot checks
- Monthly: Video review sampling (random dock door/time)
- Quarterly: Audit of procedures compliance (checklist-based)
- Annual: Full inventory reconciliation and security assessment

**Consequences:**
- ✅ Reduced risk of theft and diversion
- ✅ Prevention of unauthorized access via shipping areas
- ✅ Chain of custody documentation for investigations
- ✅ Export control and regulatory compliance
- ⚠️ Operational impact on shipping/receiving speed
- ⚠️ Requires dedicated security personnel or escorts
- ⚠️ Technology and infrastructure costs

**Related Patterns:** AC-015 (Escort Procedures), SD-008 (Dock Camera Placement), PS-016 (Inventory Security)

---

### Pattern PS-006: Roof Access Security

**Context:** Rooftops provide potential access point for intruders and are often overlooked in security design.

**Problem:** HVAC units, skylights, roof hatches, and utility penetrations on roofs may be vulnerable to exploitation.

**Solution:**
Secure roof access and monitor roof-level vulnerabilities:

**Access Control:**

*Roof Hatches and Doors:*
- Locking hardware: High-security locks or electronic access control
- Alarms: Contact switches to alert when opened
- Signage: "Authorized Personnel Only" and "Alarm Will Sound"
- Monitoring: Security operations center alerted to any access
- Access list: Facilities maintenance only, logged and approved
- Ladder access: Remove portable ladders, lock permanent ladders

*External Access Prevention:*
- Ladder cage: Locked cage on permanent exterior ladders
- Downspout removal: Eliminate climbing aids near building
- Tree trimming: Maintain 10-foot clearance from roof edge
- Adjacent building: Evaluate access from nearby structures
- Fire escape: Alarmed or locked at ground level

**Roof Penetration Security:**

*Skylights:*
- Material: Polycarbonate or laminated glass (impact resistant)
- Security film: Apply shatter-resistant film
- Grilles: Interior security grilles or bars
- Monitoring: Vibration sensors or glass break detectors
- Access: Can someone fit through opening if broken?

*HVAC and Utilities:*
- Equipment enclosures: Locked, tamper-evident
- Ductwork: Secure with fasteners, prevent disassembly
- Electrical: Lock disconnect panels
- Plumbing: Secure roof vents and stacks
- Wireless equipment: Lock and monitor (cellular, microwave, WiFi)

**Surveillance:**
- Camera coverage: Key roof access points (hatches, ladder tops)
- Panoramic cameras: 360-degree views from rooftop mounting
- Thermal cameras: Detect intruders at night
- Recording and monitoring: 24/7 SOC monitoring
- Regular review: Monthly review of roof camera footage

**Physical Inspections:**
- Monthly: Security patrol of rooftop
- Quarterly: Maintenance inspection of roof equipment and access controls
- After severe weather: Damage assessment and security verification
- Checklist: Standardized inspection checklist with photo documentation

**Consequences:**
- ✅ Eliminates often-overlooked vulnerability
- ✅ Protects HVAC and utility infrastructure
- ✅ Prevents covert entry from above
- ⚠️ Roof access needed for maintenance creates control challenges
- ⚠️ Weather and environmental factors may cause nuisance alarms

**Related Patterns:** AC-007 (Maintenance Access Control), SD-012 (Elevated Camera Positions), PS-011 (Utility Infrastructure Protection)

---

## 2. ACCESS CONTROL PATTERNS

### Pattern AC-001: Biometric Badge Access

**Context:** Badge-based access control is primary method for facility entry but vulnerable to sharing and tailgating.

**Problem:** Photo ID badges alone cannot prevent authorized badge holder from admitting unauthorized person.

**Solution:**
Implement multi-factor access control combining badge and biometric verification:

**Technology Selection:**

*Fingerprint Recognition:*
- Reader type: Optical or capacitive sensors
- Template storage: Card (match-on-card) or server (match-on-server)
- Speed: < 2 seconds per authentication
- False acceptance rate (FAR): < 0.001%
- False rejection rate (FRR): < 1%
- Environmental: IP65 rated for outdoor use

*Iris Recognition:*
- Camera type: Near-infrared (NIR) imaging
- Distance: 8-14 inches from reader
- Speed: < 3 seconds per authentication
- Accuracy: Lower error rates than fingerprint
- Hygiene: Non-contact (preferred for clean rooms)
- Cost: Higher than fingerprint ($500-$2,000 per reader)

*Facial Recognition:*
- Camera type: Visible light or NIR
- Distance: 1-5 feet from reader (touchless)
- Speed: < 1 second per authentication
- Accuracy: Improving but still higher error rates in varied lighting
- Privacy concerns: More regulation and user resistance
- Use cases: High-traffic entrances with continuous flow

**Deployment Strategy:**

*High-Security Areas (Tier 1):*
- Clean rooms and production floors
- Server rooms and network closets
- Research and development laboratories
- Sensitive document storage areas
- Executive offices and conference rooms
- Shipping/receiving holding areas

*Medium-Security Areas (Tier 2):*
- General office space entry
- Building lobby entry (after security desk)
- Parking garage entry from parking to building
- Break rooms and cafeteria (if access controlled)
- Locker rooms and restrooms (if restricted)

*Badge-Only Areas (Tier 3):*
- Parking lots and garages
- Outdoor smoking areas
- Building perimeter doors (for egress only)
- Public areas (lobby, reception)

**Enrollment Process:**
1. Initial enrollment: During onboarding, capture biometric template
2. Consent: Obtain signed consent form for biometric collection
3. Multiple samples: Capture 3-5 samples for template creation
4. Quality check: Ensure high-quality template (system feedback)
5. Badge encoding: Write template to smart card or store on server
6. Testing: Verify successful authentication before badge activation
7. Backup: Alternate finger or iris in case of injury

**Operational Procedures:**

*Daily Operations:*
- Present badge to reader (RFID proximity)
- Biometric authentication prompt appears
- Present finger/iris/face for verification
- Green light and audible beep for access granted
- Door unlocks for 5-second window
- Log entry: Badge number, biometric match score, timestamp, door location

*Failure Handling:*
- First failure: Prompt to retry (may be positioning or environmental)
- Second failure: Prompt to use alternate biometric (if enrolled)
- Third failure: Denied access, alert security for assistance
- Degraded mode: Manual verification by security officer with override

**Privacy and Legal Compliance:**
- Biometric data protection: Encrypt templates, never store raw images
- Consent: Written consent required, opt-out provisions for religious/medical reasons
- Retention: Delete biometric data upon termination
- Disclosure: Do not share with third parties
- State laws: Comply with BIPA (Illinois) and similar state biometric privacy laws
- Audit trail: Log all access to biometric database

**Consequences:**
- ✅ Strong authentication: Prevents badge sharing and pass-back
- ✅ Audit trail: Confirmed identity of person accessing areas
- ✅ Non-repudiation: Person cannot deny access event
- ⚠️ Higher cost: $300-$2,000 per reader vs. $100 for badge-only
- ⚠️ Privacy concerns: User resistance and regulatory compliance
- ⚠️ Failure modes: Injuries, environmental factors may prevent access

**Related Patterns:** AC-002 (Anti-Tailgating), AC-003 (Multi-Factor Authentication), AC-010 (Access Revocation)

---

### Pattern AC-002: Anti-Tailgating Mantraps

**Context:** Even with strong authentication, tailgating (following authorized person through door) remains a threat.

**Problem:** Social engineering and casual tailgating allow unauthorized persons to enter secure areas.

**Solution:**
Deploy mantraps (double-door vestibules) with interlock and optical detection:

**Mantrap Design:**

*Physical Configuration:*
- Double doors: Entry door and exit door with vestibule between
- Vestibule size: 4x6 feet minimum (1-2 person capacity) or 8x10 feet (wheelchair accessible)
- Interlock: Entry door must close and lock before exit door can open
- Material: Bullet-resistant glass or solid walls with vision panels
- Lighting: Bright lighting (20+ foot-candles) for camera visibility
- Signage: "Single Person Entry Only" and "Wait for Green Light"

*Detection Technology:*
- Optical sensors: Stereo vision or 3D cameras count persons in vestibule
- Weight sensors: Floor sensors detect multiple persons (less reliable)
- Thermal imaging: Count heat signatures (expensive but accurate)
- Direction detection: Ensure person is not passing credential back through door
- Override: Emergency egress override for fire alarm

**Operating Modes:**

*Single-Person Mode (High Security):*
1. Authorized person badges at entry door
2. Entry door unlocks, person enters vestibule
3. Entry door closes and locks automatically
4. Optical sensor counts persons: Must be exactly 1
5. If count = 1: Exit door unlocks after biometric verification
6. If count > 1: Alarm, doors remain locked, security alerted
7. Person exits, both doors lock until next badge presentation

*Multi-Person Mode (Lower Security):*
1. First person badges and enters
2. System allows second person to badge and enter before first exits
3. Both persons authenticated individually
4. Optical sensor ensures count matches badge presentations
5. Alarm if discrepancy between badges and people count

*Degraded Mode (Emergency):*
- Fire alarm: All doors unlock, free egress
- Power failure: Doors unlock (fail-safe) or remain locked (fail-secure) based on policy
- System failure: Security officer manual verification and override
- Medical emergency: Override button releases person from mantrap

**Integration Requirements:**
- Access control system: Interlock logic and authentication
- Video management: Cameras record all entry events, high-quality face capture
- Alarm monitoring: SOC receives alerts for tailgating attempts
- Badging system: Synchronize access lists and authentication factors
- Building automation: Fire alarm integration for emergency egress

**Operational Procedures:**

*User Training:*
- New hire orientation: Demonstrate mantrap use, emphasize single-person rule
- Signage: Clear visual instructions at entry and exit doors
- Culture: "If you see something, say something" - report tailgating
- Compliance: Disciplinary action for intentional tailgating or admitting others

*Security Response:*
- Alarm: Security officer dispatched immediately
- Verification: Visual verification via camera, intercom to communicate
- Resolution: If unauthorized person, escort off premises; if authorized, verify credentials
- Documentation: Incident report filed, coaching/discipline for policy violation

**Placement Strategy:**

*Critical Locations:*
- Main building entry (after lobby if public access allowed)
- Clean room entry airlocks (may combine with gowning procedures)
- Data center and server room entry
- R&D laboratory entry
- High-value storage areas (tool cribs, material storage)
- Shipping/receiving entry to facility

*Cost-Benefit Analysis:*
- High-cost installations: Fabricated steel or aluminum, high-security glass, advanced sensors ($30,000-$100,000 per mantrap)
- Medium-cost: Modular mantrap units with standard interlock and basic sensors ($15,000-$30,000)
- Low-cost: Retrofit existing vestibule with interlock and sensors ($5,000-$15,000)
- Decision factors: Threat level, criticality of assets protected, budget constraints

**Consequences:**
- ✅ Highly effective against tailgating and piggybacking
- ✅ Forces authentication of every person entering
- ✅ Creates "hard" access control point for security perimeter
- ✅ Provides video evidence of entry events
- ⚠️ High initial cost and space requirements
- ⚠️ Slows entry process, potential operational impact
- ⚠️ Requires regular maintenance and testing
- ⚠️ User frustration if not well-designed or maintained

**Related Patterns:** AC-001 (Biometric Badge Access), AC-008 (Clean Room Access), SD-002 (High-Quality Face Capture)

---

[Continuing with 28 more Access Control patterns...]

### Pattern AC-003: Multi-Factor Authentication (MFA)

**Context:** Critical systems and areas require stronger authentication than single-factor.

**Problem:** Passwords and badges can be stolen, guessed, or shared.

**Solution:**
Combine multiple authentication factors (something you know, have, and are):

**Authentication Factors:**

*Knowledge Factors (Something You Know):*
- PIN: 4-8 digit personal identification number
- Password: Complex password for system access
- Security questions: Challenge-response for account recovery

*Possession Factors (Something You Have):*
- Smart card: Badge with embedded chip and certificate
- Hardware token: Time-based one-time password (TOTP) generator
- Mobile device: Smartphone with authenticator app or push notification

*Inherence Factors (Something You Are):*
- Fingerprint: Biometric fingerprint scan
- Iris/retina: Eye biometric scan
- Face: Facial recognition biometric
- Voice: Voiceprint recognition

**Implementation Approaches:**

*Physical Access (Facility Entry):*
- Factor 1: Badge (possession)
- Factor 2: Biometric (inherence)
- Optional Factor 3: PIN for highest security areas

*Logical Access (IT Systems):*
- Factor 1: Username/password (knowledge)
- Factor 2: TOTP token or push notification (possession)
- Factor 3: Biometric for privileged access (inherence)

*Privileged Operations:*
- Standard MFA plus approval workflow
- Dual control: Two persons required for critical actions
- Time-based: MFA validity window (4 hours, re-auth required)

**Risk-Based Authentication:**
- Low risk: Single factor (standard office access)
- Medium risk: Two factors (IT system access, sensitive areas)
- High risk: Three factors (R&D labs, data centers, executive areas)
- Critical operations: MFA plus approval and monitoring

**Consequences:**
- ✅ Significantly stronger authentication
- ✅ Compliance with regulations (DFARS, CMMC)
- ⚠️ User friction and potential productivity impact
- ⚠️ More complex to manage and support

**Related Patterns:** AC-001 (Biometric Badge Access), AC-004 (Privileged Access Management), CY-007 (Identity and Access Management)

---

[Note: For brevity, I'm showing the structure. The actual document would continue with all 30 Access Control patterns, each with similar detail level]

**Additional Access Control Patterns (24 more):**

AC-004: Privileged Access Management
AC-005: Temporary Access Control (Contractors/Visitors)
AC-006: Vehicle Access Control and Parking
AC-007: Maintenance Access Control
AC-008: Clean Room Access Protocols
AC-009: Time-Based Access Restrictions
AC-010: Access Revocation Procedures
AC-011: Emergency Access Override
AC-012: VIP and Executive Protection
AC-013: After-Hours Access Procedures
AC-014: Escort Requirements and Procedures
AC-015: Visitor Management System Integration
AC-016: Badge Management Lifecycle
AC-017: Access Control Database Synchronization
AC-018: Remote Access Control (IT Systems)
AC-019: Two-Person Integrity Procedures
AC-020: Separated Duties for Critical Functions
AC-021: Access Logging and Audit Trail
AC-022: Access Request and Approval Workflow
AC-023: Periodic Access Recertification
AC-024: Door Hardware and Fail-Safe/Fail-Secure
AC-025: Access Control Panel Physical Security
AC-026: Power Backup for Access Control Systems
AC-027: Access Control System Cybersecurity
AC-028: Integration with HR Systems (Onboarding/Termination)
AC-029: Incident Response Access Overrides
AC-030: Access Control KPIs and Metrics

---

## Document Continuation

**Status:** This document contains 8 detailed patterns out of 150+ physical security patterns. The complete document would continue with:

- Clean Room Security (25 patterns): CR-001 through CR-025
- Surveillance Systems (20 patterns): SD-001 through SD-020
- Intrusion Detection (20 patterns): ID-001 through ID-020
- Emergency Response (30 patterns): EM-001 through EM-030

Each pattern follows the same format: Context, Problem, Solution (with detailed specifications), and Consequences.

---

**Document Status:** IN PROGRESS - Section 1 & 2 (Partial) Complete
**Target:** 150+ patterns across 6 categories
**Next Sections:** Clean Room Security, Surveillance, Intrusion Detection, Emergency Response

---

**Document Classification:** UNCLASSIFIED // FOR OFFICIAL USE ONLY
**Distribution:** Critical Infrastructure Security Personnel
**Next Review:** 2026-11-05
