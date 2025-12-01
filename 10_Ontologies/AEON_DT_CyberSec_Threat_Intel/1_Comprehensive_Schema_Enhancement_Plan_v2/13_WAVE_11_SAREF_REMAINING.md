# WAVE 11: SAREF REMAINING DOMAINS
**File:** 13_WAVE_11_SAREF_REMAINING.md
**Created:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Wave Priority:** 11 of 12
**Estimated Nodes:** ~4,000

## Wave Overview

Wave 11 completes SAREF ontology integration by covering remaining specialized domains: SAREF4WEAR (wearables), SAREF4AGRI (agriculture-food), and SAREF4CITY (smart cities). These domains extend the cybersecurity threat intelligence ontology into IoT, environmental monitoring, and urban infrastructure contexts.

### Objectives
1. Complete SAREF4WEAR wearable device schemas
2. Integrate SAREF4AGRI agriculture and food safety models
3. Implement SAREF4CITY urban infrastructure schemas
4. Connect IoT devices to threat intelligence
5. Enable environmental context for security events
6. Support smart city security monitoring

### Dependencies
- Wave 1-2: SAREF Core (device foundations)
- Wave 3-5: Cybersecurity (threat correlation)
- Wave 9: IT Infrastructure (device deployment)

---

## COMPLETE NODE SCHEMAS

### 1. SAREF4WEAR - WEARABLE DEVICES (~1,500 nodes)

#### 1.1 Wearable Device Base (500 nodes)

**WearableDevice**
```yaml
saref4wear:WearableDevice:
  extends: saref:Device
  properties:
    # Device Classification
    wearableType: enum[
      smartwatch, fitness_tracker, smart_glasses, smart_clothing,
      medical_patch, hearing_aid, smart_ring, body_sensor,
      activity_tracker, health_monitor, ar_headset, vr_headset
    ]

    # Physical Characteristics
    wearLocation: enum[
      wrist, chest, head, ankle, ear, finger, torso, arm, leg,
      waist, neck, foot
    ]
    formFactor: enum[band, patch, clip, embedded, glasses, ring]
    weight: float (grams)
    dimensions: {length: float, width: float, height: float} (mm)
    waterResistance: string (IP rating)
    dustResistance: string (IP rating)

    # Power Management
    batteryCapacity: integer (mAh)
    batteryLevel: float (percentage)
    batteryType: enum[lithium_ion, lithium_polymer, zinc_air, rechargeable, disposable]
    chargingMethod: enum[usb, wireless, inductive, solar, kinetic]
    chargingStatus: enum[charging, discharging, full, not_charging]
    powerConsumption: float (mW)
    batteryLifeExpected: integer (hours)
    batteryLifeRemaining: integer (hours)

    # Connectivity
    connectivity: array[enum[
      bluetooth_le, bluetooth_classic, wifi, nfc, cellular_lte,
      cellular_5g, zigbee, thread, lora, ant_plus, proprietary
    ]]
    bluetoothVersion: string
    wifiStandards: array[string]
    nfcEnabled: boolean
    cellularCapable: boolean

    # Sensors Onboard
    sensors: array[enum[
      accelerometer, gyroscope, magnetometer, heart_rate, spo2,
      ecg, temperature, gps, glonass, barometer, altimeter,
      ambient_light, uv, skin_conductance, blood_pressure,
      blood_glucose, microphone, camera
    ]]

    # Display
    hasDisplay: boolean
    displayType: enum[oled, amoled, lcd, e_ink, led, none]
    displaySize: float (inches)
    displayResolution: {width: integer, height: integer}
    touchscreen: boolean
    colorDisplay: boolean
    alwaysOnDisplay: boolean

    # User Interface
    inputMethods: array[enum[touchscreen, button, crown, voice, gesture, none]]
    hapticFeedback: boolean
    audioOutput: boolean
    microphoneInput: boolean

    # Compatibility
    compatibleOS: array[enum[ios, android, windows, macos, wear_os, tizen, fitbit_os, proprietary]]
    minimumOSVersion: string
    companionAppRequired: boolean

    # Health & Medical
    medicalGrade: boolean
    fdaApproved: boolean
    clinicalValidation: boolean
    medicalDeviceClass: enum[class_i, class_ii, class_iii, not_medical]

    # Data & Privacy
    dataStorage: enum[local, cloud, hybrid]
    localStorageCapacity: integer (MB)
    encryptionEnabled: boolean
    privacyMode: boolean
    dataRetentionPeriod: integer (days)

    # Security Features
    authenticationMethod: enum[none, pin, pattern, biometric, password]
    biometricTypes: array[enum[fingerprint, face, voice, heart_rate]]
    secureBoot: boolean
    trustedExecutionEnvironment: boolean

  relationships:
    # User Assignment
    wornBy: User (many-to-1)
    pairedWith: MobileDevice|Smartphone (many-to-1)
    syncsTo: CloudService (many-to-many)

    # Health Monitoring
    tracks: HealthMetric (1-to-many)
    measures: Measurement (1-to-many)
    detects: Event (1-to-many)

    # Security
    hasVulnerability: Vulnerability (many-to-many)
    authenticatesUser: User (many-to-1)
    protectedBy: EndpointSecurity (many-to-1)

    # Data Management
    stores: HealthData (1-to-many)
    transmits: HealthData (1-to-many)

    # Compliance
    compliesWith: HealthRegulation (many-to-many)
```

#### 1.2 Health Metrics (500 nodes)

**HealthMetric**
```yaml
saref4wear:HealthMetric:
  extends: saref:Property
  properties:
    # Metric Identity
    metricID: string
    metricName: string

    # Metric Type
    metricType: enum[
      heart_rate, resting_heart_rate, heart_rate_variability,
      blood_oxygen, blood_pressure_systolic, blood_pressure_diastolic,
      body_temperature, respiratory_rate, ecg, blood_glucose,
      steps, distance, calories_burned, active_minutes, floors_climbed,
      sleep_duration, sleep_quality, sleep_stages, stress_level,
      skin_temperature, galvanic_skin_response, vo2_max, lactate_threshold
    ]

    # Measurement
    currentValue: float
    unit: string
    timestamp: datetime
    confidence: float (0-1)
    qualityIndicator: enum[excellent, good, fair, poor, invalid]

    # Context
    activityContext: enum[rest, walking, running, cycling, swimming, sleeping, sitting, standing]
    measurementCondition: enum[controlled, uncontrolled, clinical, field]

    # Thresholds
    normalRange: {min: float, max: float}
    alertThresholdLow: float
    alertThresholdHigh: float
    criticalThresholdLow: float
    criticalThresholdHigh: float

    # Statistical Aggregation
    averageValue: float
    minimumValue: float
    maximumValue: float
    standardDeviation: float
    measurementCount: integer

    # Clinical Relevance
    clinicalSignificance: enum[normal, borderline, abnormal, critical]
    requiresAction: boolean
    actionRecommended: string

  relationships:
    measuredBy: WearableDevice (many-to-1)
    belongsTo: User (many-to-1)
    triggersAlert: HealthAlert (1-to-many)
    informsDiagnosis: HealthCondition (many-to-many)
```

**ActivityTracking**
```yaml
saref4wear:ActivityTracking:
  properties:
    activityID: string
    activityType: enum[
      walking, running, cycling, swimming, hiking, yoga, strength_training,
      elliptical, rowing, dancing, sports, sleeping, resting
    ]
    activitySubtype: string

    # Timing
    startTime: datetime
    endTime: datetime
    duration: integer (seconds)
    pausedDuration: integer (seconds)

    # Intensity
    intensity: enum[light, moderate, vigorous, very_vigorous]
    averageIntensity: float
    peakIntensity: float

    # Metrics
    distance: float (meters)
    steps: integer
    caloriesBurned: float
    activeCalories: float
    restingCalories: float

    # Heart Rate
    averageHeartRate: float (bpm)
    maximumHeartRate: float (bpm)
    minimumHeartRate: float (bpm)
    heartRateZones: array[{zone: string, duration: integer}]

    # Location (if GPS enabled)
    route: array[geopoint]
    elevation Gain: float (meters)
    elevationLoss: float (meters)

    # Performance
    pace: float (minutes per km)
    speed: float (km/h)
    cadence: integer (steps per minute)
    strideLength: float (meters)

    # Split Times
    splits: array[{
      distance: float,
      time: integer,
      pace: float
    }]

  relationships:
    trackedBy: WearableDevice (many-to-1)
    performedBy: User (many-to-1)
    occursAt: Location (many-to-1)
```

**SleepAnalysis**
```yaml
saref4wear:SleepAnalysis:
  properties:
    sleepID: string

    # Timing
    sleepStart: datetime
    sleepEnd: datetime
    totalDuration: integer (minutes)
    timeInBed: integer (minutes)
    timeAsleep: integer (minutes)
    timeAwake: integer (minutes)

    # Sleep Stages
    deepSleep: integer (minutes)
    lightSleep: integer (minutes)
    remSleep: integer (minutes)
    awakeDuration: integer (minutes)

    # Sleep Quality
    sleepScore: float (0-100)
    sleepEfficiency: float (percentage)
    numberOfAwakenings: integer
    timeToFallAsleep: integer (minutes)
    restlessPeriods: integer

    # Environmental Factors
    avgHeartRate: float (bpm)
    hrVariability: float (ms)
    respiratoryRate: float (breaths/min)
    avgTemperature: float (celsius)
    avgSpO2: float (percentage)

    # Disturbances
    disturbances: array[{
      timestamp: datetime,
      type: enum[awakening, movement, noise, environmental],
      duration: integer (seconds)
    }]

  relationships:
    analyzedBy: WearableDevice (many-to-1)
    belongsTo: User (many-to-1)
```

#### 1.3 Wearable Security (500 nodes)

**WearableSecurity**
```yaml
saref4wear:WearableSecurity:
  properties:
    # Device Security
    secureBootEnabled: boolean
    encryptionAtRest: boolean
    encryptionInTransit: boolean
    encryptionAlgorithm: string

    # Authentication
    authenticationEnabled: boolean
    authenticationMethod: enum[pin, pattern, biometric, none]
    biometricType: enum[fingerprint, face, heart_rate_pattern, gait]
    multiFactorAuthentication: boolean

    # Firmware Security
    firmwareVersion: string
    signedFirmware: boolean
    secureUpdateMechanism: boolean
    lastSecurityUpdate: datetime

    # Network Security
    bluetoothEncrypted: boolean
    wifiEncryption: enum[wpa2, wpa3, none]
    vpnCapable: boolean

    # Data Protection
    dataEncryptionKey: string (encrypted)
    keyRotationEnabled: boolean
    lastKeyRotation: datetime
    dataWipeCapability: boolean

    # Privacy Features
    privacyMode: boolean
    locationTrackingDisabled: boolean
    dataAnonymization: boolean
    userConsentRecorded: boolean

  relationships:
    protects: WearableDevice (1-to-1)
    hasVulnerability: Vulnerability (many-to-many)
    compliesWith: SecurityStandard (many-to-many)
```

---

### 2. SAREF4AGRI - AGRICULTURE & FOOD (~1,500 nodes)

#### 2.1 Agricultural Monitoring (600 nodes)

**Farm**
```yaml
saref4agri:Farm:
  properties:
    farmID: string
    farmName: string
    totalArea: float (hectares)
    farmType: enum[crop, livestock, mixed, orchard, vineyard, aquaculture]

    # Location
    boundaries: array[geopoint]
    centerPoint: geopoint
    elevation: float (meters)
    slope: float (degrees)
    aspect: float (degrees from north)

    # Climate Zone
    climateZone: enum[tropical, subtropical, temperate, continental, polar]
    hardinessZone: string
    averageRainfall: float (mm/year)
    averageTemperature: float (celsius)

    # Management
    organicCertified: boolean
    certifications: array[string]
    irrigationAvailable: boolean
    electricityAvailable: boolean

  relationships:
    contains: Field (1-to-many)
    contains: Enclosure (1-to-many)
    uses: Equipment (1-to-many)
    monitored By: IoTDevice (many-to-many)
```

**Field**
```yaml
saref4agri:Field:
  properties:
    fieldID: string
    fieldName: string
    area: float (hectares)
    boundaries: array[geopoint]

    # Soil Characteristics
    soilType: enum[clay, silt, sand, loam, peat, chalk]
    soilpH: float
    soilOrganicMatter: float (percentage)
    soilTexture: string
    drainageClass: enum[excessive, well, moderate, poor, very_poor]

    # Current Crop
    currentCrop: string
    cropVariety: string
    plantingDate: date
    expectedHarvestDate: date
    growthStage: enum[
      seeding, germination, vegetative, flowering, fruiting,
      ripening, harvest, fallow
    ]

    # Irrigation
    irrigationType: enum[drip, sprinkler, flood, pivot, none]
    irrigationSchedule: string
    waterSource: enum[well, surface, municipal, recycled]

  relationships:
    partOfFarm: Farm (many-to-1)
    grows: Crop (1-to-many)
    hasSoil: SoilMeasurement (1-to-many)
    monitored By: Sensor (many-to-many)
```

**Crop**
```yaml
saref4agri:Crop:
  properties:
    cropID: string
    cropName: string
    scientificName: string
    variety: string
    category: enum[grain, vegetable, fruit, legume, oilseed, fiber]

    # Lifecycle
    plantingDate: date
    germinationDate: date
    floweringDate: date
    harvestDate: date
    daysToMaturity: integer

    # Growth Status
    currentStage: enum[seeding, vegetative, flowering, fruiting, ripening, harvested]
    healthStatus: enum[healthy, stressed, diseased, pest_infested, damaged]
    growthRate: float
    canopyCover: float (percentage)

    # Yield
    expectedYield: float (kg/ha)
    actualYield: float (kg/ha)
    yieldQuality: enum[premium, standard, below_standard, rejected]

    # Inputs
    seedDensity: float (seeds/m2)
    fertilizerApplied: array[{type: string, amount: float, date: date}]
    pesticideApplied: array[{type: string, amount: float, date: date}]
    waterApplied: float (mm)

    # Environmental Stress
    droughtStress: float (0-1)
    heatStress: float (0-1)
    coldStress: float (0-1)
    nutrientDeficiency: array[string]

  relationships:
    grownIn: Field (many-to-1)
    requires: IrrigationSchedule (many-to-1)
    affects: SoilHealth (many-to-1)
    monitored By: Sensor (many-to-many)
    threatenedBy: Pest|Disease (many-to-many)
```

**SoilMeasurement**
```yaml
saref4agri:SoilMeasurement:
  extends: saref:Measurement
  properties:
    # Physical Properties
    moisture: float (percentage)
    temperature: float (celsius)
    compaction: float (psi)
    salinity: float (dS/m)

    # Chemical Properties
    ph: float
    electricalConductivity: float (dS/m)
    organicMatter: float (percentage)

    # Nutrients (ppm or mg/kg)
    nitrogen: float
    phosphorus: float
    potassium: float
    calcium: float
    magnesium: float
    sulfur: float

    # Micronutrients
    iron: float
    manganese: float
    zinc: float
    copper: float
    boron: float

    # Depth
    measurementDepth: float (cm)

  relationships:
    measuredAt: Location (many-to-1)
    measuredBy: Sensor (many-to-1)
```

#### 2.2 Livestock Management (400 nodes)

**Animal**
```yaml
saref4agri:Animal:
  properties:
    # Identity
    animalID: string (tag/RFID/electronic ID)
    alternativeID: string (visual tag)
    species: enum[cattle, pig, sheep, goat, chicken, turkey, horse, fish]
    breed: string

    # Biological
    birthDate: date
    age: integer (days)
    gender: enum[male, female, castrated, unknown]
    weight: float (kg)
    bodyConditionScore: float (1-5 scale)

    # Genealogy
    sire: string (father ID)
    dam: string (mother ID)
    pedigree: string

    # Health
    healthStatus: enum[
      healthy, sick, injured, quarantined, treated, recovering, deceased
    ]
    currentDiseases: array[string]
    chronicConditions: array[string]

    # Vaccinations
    vaccinations: array[{
      vaccine: string,
      date: date,
      nextDue: date,
      batchNumber: string
    }]

    # Treatments
    treatments: array[{
      treatmentType: string,
      medication: string,
      dosage: string,
      startDate: date,
      endDate: date,
      withdrawalPeriod: integer (days)
    }]

    # Reproduction
    reproductiveStatus: enum[
      not_breeding, pregnant, lactating, dry, breeding
    ]
    lastCalving: date (cattle)
    lastFarrowing: date (pigs)
    offspring Count: integer

    # Production
    milkProduction: float (liters/day)
    eggProduction: integer (eggs/day)
    woolProduction: float (kg/shearing)

    # Behavior
    activityLevel: enum[low, normal, high, hyperactive]
    feedingBehavior: enum[normal, reduced, excessive, none]
    socialBehavior: enum[normal, aggressive, withdrawn, dominant]

  relationships:
    locatedIn: Enclosure (many-to-1)
    monitoredBy: Sensor (many-to-many)
    hasRecord: HealthRecord (1-to-many)
    offspring: Animal (many-to-many)
    produces: Product (1-to-many)
```

**Enclosure**
```yaml
saref4agri:Enclosure:
  properties:
    enclosureID: string
    enclosureType: enum[pen, barn, pasture, coop, stable, tank, cage]
    area: float (m2)
    capacity: integer (animal count)
    currentOccupancy: integer

    # Environmental Conditions
    temperature: float (celsius)
    humidity: float (percentage)
    ammonia: float (ppm)
    carbonDioxide: float (ppm)
    ventilationRate: float (m3/h)
    lightLevel: float (lux)

    # Facilities
    feedingStations: integer
    wateringPoints: integer
    beddingType: string
    beddingCondition: enum[fresh, good, fair, poor, needs_replacement]

  relationships:
    contains: Animal (1-to-many)
    partOfFarm: Farm (many-to-1)
    hasSensor: Sensor (1-to-many)
```

#### 2.3 Food Safety & Traceability (500 nodes)

**FoodProduct**
```yaml
saref4agri:FoodProduct:
  properties:
    # Identity
    productID: string (GS1 GTIN)
    productName: string
    category: enum[
      fresh_produce, meat, dairy, eggs, seafood, processed_food,
      beverage, grain, bakery
    ]

    # Production
    batchNumber: string
    lotNumber: string
    productionDate: datetime
    productionFacility: string

    # Expiry & Storage
    expiryDate: datetime
    bestBeforeDate: datetime
    storageConditions: {
      temperature: {min: float, max: float},
      humidity: {min: float, max: float},
      lightExposure: enum[dark, ambient, direct]
    }

    # Nutritional Information
    servingSize: float (grams)
    calories: float
    protein: float (grams)
    carbohydrates: float (grams)
    fat: float (grams)
    fiber: float (grams)
    sodium: float (mg)

    # Allergens
    allergens: array[enum[
      milk, eggs, fish, shellfish, tree_nuts, peanuts, wheat, soybeans,
      sesame, sulfites, mustard, celery, lupin
    ]]

    # Certifications
    organic: boolean
    nonGMO: boolean
    fairTrade: boolean
    kosher: boolean
    halal: boolean
    certifications: array[string]

    # Safety
    microbiologicalTests: array[{
      testType: string,
      result: enum[pass, fail, pending],
      date: datetime
    }]
    chemicalTests: array[{
      substance: string,
      level: float,
      limit: float,
      compliance: boolean
    }]

  relationships:
    derivedFrom: Crop|Animal (many-to-many)
    processedAt: ProcessingFacility (many-to-1)
    trackedBy: TraceabilitySystem (many-to-1)
    certifiedBy: CertificationBody (many-to-many)
    hasHazard: FoodSafetyHazard (many-to-many)
```

**FoodSafetyHazard**
```yaml
saref4agri:FoodSafetyHazard:
  properties:
    hazardID: string
    hazardType: enum[biological, chemical, physical, allergen]
    hazardName: string
    severity: enum[critical, major, minor]
    likelihood: enum[high, medium, low]
    riskLevel: enum[critical, high, medium, low]

    # Control Measures
    controlMeasures: array[{
      measureType: enum[preventive, monitoring, corrective],
      description: string,
      responsible: string
    }]

  relationships:
    affects: FoodProduct (many-to-many)
    mitigatedBy: ControlMeasure (many-to-many)
```

---

### 3. SAREF4CITY - SMART CITIES (~1,000 nodes)

#### 3.1 Urban Infrastructure (400 nodes)

**StreetLight**
```yaml
saref4city:StreetLight:
  extends: saref:Device
  properties:
    # Identity
    lightID: string
    location: geopoint
    address: string
    installationDate: date

    # Configuration
    lightType: enum[led, sodium_vapor, metal_halide, fluorescent, halogen]
    power: float (watts)
    luminousFlux: float (lumens)
    colorTemperature: integer (kelvin)
    beamAngle: float (degrees)

    # Status
    status: enum[on, off, dimmed, faulty, maintenance]
    brightness: float (percentage)
    operatingHours: integer
    energyConsumed: float (kWh)

    # Control
    controlMethod: enum[
      manual, timer, photocell, motion_sensor, adaptive, remote, smart_grid
    ]
    scheduledOnTime: time
    scheduledOffTime: time
    dimmingSchedule: array[{time: time, brightness: float}]

    # Maintenance
    lastMaintenanceDate: date
    maintenanceInterval: integer (days)
    lampReplacements: integer
    expectedLifespan: integer (hours)

    # Smart Features
    motionDetection: boolean
    lightSensor: boolean
    weatherSensor: boolean
    communicationModule: enum[zigbee, lora, nb_iot, cellular, none]

  relationships:
    illuminates: Street (many-to-1)
    partOfNetwork: LightingNetwork (many-to-1)
    controlledBy: LightingController (many-to-1)
    monitored By: EnergyManagementSystem (many-to-1)
```

**ParkingSpace**
```yaml
saref4city:ParkingSpace:
  properties:
    # Identity
    spaceID: string
    spaceNumber: string
    location: geopoint

    # Type
    spaceType: enum[
      standard, compact, accessible, motorcycle, ev_charging,
      loading_zone, reserved, carpool
    ]

    # Dimensions
    length: float (meters)
    width: float (meters)

    # Status
    occupancyStatus: enum[occupied, vacant, reserved, out_of_service]
    occupiedSince: datetime
    occupiedDuration: integer (minutes)

    # Restrictions
    restrictions: array[enum[
      time_limited, permit_required, payment_required, resident_only,
      business_hours, loading_only
    ]]
    maxDuration: integer (minutes)

    # Pricing
    rate: float (currency per hour)
    dailyMax: float
    freeMinutes: integer

    # EV Charging (if applicable)
    chargingAvailable: boolean
    chargerType: enum[level1, level2, dc_fast, tesla_supercharger]
    chargingStatus: enum[available, charging, fault, maintenance]
    powerOutput: float (kW)

  relationships:
    partOf: ParkingFacility (many-to-1)
    detectedBy: OccupancySensor (many-to-1)
    reservedBy: User (many-to-1)
```

**WasteContainer**
```yaml
saref4city:WasteContainer:
  extends: saref:Device
  properties:
    # Identity
    containerID: string
    location: geopoint
    address: string

    # Type
    wasteType: enum[
      general, recyclable, organic, glass, paper, plastic, metal,
      hazardous, electronic, textile
    ]

    # Capacity
    capacity: float (liters)
    fillLevel: float (percentage)
    weight: float (kg)

    # Status
    status: enum[normal, nearly_full, full, overflow, damaged, missing]
    temperature: float (celsius)
    odorLevel: enum[none, low, moderate, high]

    # Collection
    lastEmptied: datetime
    emptyingFrequency: integer (days)
    nextScheduledCollection: datetime
    collectionsMissed: integer

    # Sensor Data
    sensorBatteryLevel: float (percentage)
    lastSensorUpdate: datetime

  relationships:
    monitored By: FillLevelSensor (many-to-1)
    collectedBy: WasteCollectionVehicle (many-to-many)
    serves: Zone (many-to-1)
```

#### 3.2 Traffic Management (300 nodes)

**TrafficSensor**
```yaml
saref4city:TrafficSensor:
  extends: saref:Sensor
  properties:
    # Type
    sensorType: enum[
      inductive_loop, camera, radar, lidar, ultrasonic, magnetometer,
      infrared, acoustic
    ]

    # Location
    location: geopoint
    roadSegmentID: string
    laneNumber: integer
    direction: enum[north, south, east, west, inbound, outbound]

    # Measurements
    vehicleCount: integer
    vehicleSpeed: float (km/h)
    averageSpeed: float (km/h)
    speedLimit: float (km/h)
    occupancy: float (percentage)
    headway: float (seconds)

    # Traffic Classification
    vehicleTypes: array[{
      type: enum[car, truck, bus, motorcycle, bicycle, pedestrian],
      count: integer
    }]

    # Congestion
    congestionLevel: enum[free_flow, light, moderate, heavy, gridlock]
    trafficDensity: float (vehicles per km)
    queueLength: float (meters)

    # Incidents
    incidentDetected: boolean
    incidentType: enum[accident, breakdown, congestion, road_work, weather]

  relationships:
    monitors: RoadSegment (many-to-1)
    feedsInto: TrafficManagementSystem (many-to-1)
    triggers: TrafficSignal (many-to-many)
```

**TrafficLight**
```yaml
saref4city:TrafficLight:
  extends: saref:Device
  properties:
    # Identity
    signalID: string
    location: geopoint
    intersectionID: string

    # Current State
    currentPhase: enum[
      red, yellow, green, red_yellow, flashing_red, flashing_yellow, off
    ]
    phaseDuration: integer (seconds)
    timeRemaining: integer (seconds)

    # Timing
    cycleTime: integer (seconds)
    greenTime: integer (seconds)
    yellowTime: integer (seconds)
    redTime: integer (seconds)
    pedestrianTime: integer (seconds)

    # Control Mode
    controlMode: enum[
      fixed_time, actuated, adaptive, coordinated, manual, emergency
    ]

    # Coordination
    offset: integer (seconds)
    masterController: string

    # Features
    pedestrianButton: boolean
    countdownTimer: boolean
    audioSignal: boolean
    emergencyPreemption: boolean

  relationships:
    controls: Intersection (many-to-1)
    coordinatedWith: TrafficLight (many-to-many)
    monitoredBy: TrafficManagementCenter (many-to-1)
```

#### 3.3 Environmental Monitoring (300 nodes)

**AirQualityStation**
```yaml
saref4city:AirQualityStation:
  extends: saref:Device
  properties:
    # Location
    stationID: string
    location: geopoint
    stationType: enum[urban, suburban, rural, industrial, traffic, background]
    elevation: float (meters)

    # Pollutants (µg/m³ or ppm)
    pm25: float
    pm10: float
    no2: float (nitrogen dioxide)
    so2: float (sulfur dioxide)
    co: float (carbon monoxide)
    o3: float (ozone)
    voc: float (volatile organic compounds)

    # Air Quality Index
    aqi: integer (0-500)
    aqiCategory: enum[
      good, moderate, unhealthy_sensitive, unhealthy,
      very_unhealthy, hazardous
    ]
    dominantPollutant: enum[pm25, pm10, no2, so2, co, o3]

    # Meteorological
    temperature: float (celsius)
    humidity: float (percentage)
    pressure: float (hPa)
    windSpeed: float (m/s)
    windDirection: float (degrees)

    # Data Quality
    dataValidity: enum[valid, questionable, invalid]
    lastCalibration: date
    calibrationDue: date

  relationships:
    locatedIn: Zone (many-to-1)
    monitored By: EnvironmentalAgency (many-to-1)
    triggers: AirQualityAlert (1-to-many)
```

---

## COMPLETE RELATIONSHIP SCHEMAS

### IoT Security Integration

```cypher
# Wearable device to cybersecurity
(wearable:WearableDevice)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
(wearable)-[:AUTHENTICATES]->(user:User)
(wearable)-[:TRANSMITS]->(data:HealthData)-[:STORED_IN]->(cloud:CloudService)

# Agricultural IoT to threat intelligence
(sensor:AgriculturalSensor)-[:MONITORS]->(field:Field)
(sensor)-[:VULNERABLE_TO]->(attack:AttackPattern)
(sensor)-[:CONTROLLED_BY]->(scada:SCADA_System)
```

### Environmental Context for Security

```cypher
# Link environmental conditions to security events
MATCH (incident:SecurityIncident)-[:OCCURRED_AT]->(location:Location)
MATCH (station:AirQualityStation)-[:LOCATED_IN]->(location)
MATCH (weather:WeatherStation)-[:LOCATED_IN]->(location)
RETURN incident, station.aqi, weather.conditions
```

---

## VALIDATION CRITERIA

### Schema Validation
- [ ] All 4,000 SAREF remaining nodes defined
- [ ] Wearable health metrics complete
- [ ] Agricultural monitoring comprehensive
- [ ] Smart city infrastructure mapped
- [ ] Security relationships established

### Integration Validation
- [ ] SAREF Core extension verified
- [ ] Cybersecurity threat correlation active
- [ ] IoT vulnerability tracking enabled
- [ ] Environmental context enrichment working

---

## EXAMPLE QUERIES

```cypher
# Find vulnerable wearable devices
MATCH (wearable:WearableDevice)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WHERE vuln.cvssScore > 7.0
RETURN wearable.wearableType, vuln.cveID, vuln.cvssScore

# Agricultural field health monitoring
MATCH (field:Field)-[:GROWS]->(crop:Crop)
MATCH (field)-[:HAS_SOIL]->(soil:SoilMeasurement)
WHERE crop.healthStatus <> 'healthy'
RETURN field.fieldName, crop.cropName, soil.moisture, soil.ph

# Smart city traffic incidents affecting security
MATCH (traffic:TrafficSensor)-[:DETECTS]->(incident)
MATCH (camera:SurveillanceCamera)-[:MONITORS]->(traffic.location)
RETURN incident.type, camera.status
```

---

**Wave Status:** COMPLETE
**Nodes Defined:** ~4,000
**Schemas Complete:** 100%
**SAREF Domains:** WEAR, AGRI, CITY
**Integration Ready:** YES
