// ═══════════════════════════════════════════════════════════════
// GAP-004 MANUFACTURING SECTOR DEPLOYMENT
// ═══════════════════════════════════════════════════════════════
// Target: 400 Equipment + 50 Facilities + Relationships + 5D Tags
// Pattern: PATTERN-7 Comprehensive 3-Phase Deployment
// ═══════════════════════════════════════════════════════════════

// PHASE 1: CREATE 50 MANUFACTURING FACILITIES
// ═══════════════════════════════════════════════════════════════

// Automotive Assembly Plants (10 facilities)
CREATE (f:Facility {
  facilityId: 'MFG-MI-AUTO-001',
  name: 'Detroit Automotive Assembly Plant',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'MI',
  city: 'Detroit',
  zipcode: '48201',
  coordinates: point({latitude: 42.3314, longitude: -83.0458}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-OH-AUTO-001',
  name: 'Columbus Auto Manufacturing',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'OH',
  city: 'Columbus',
  zipcode: '43215',
  coordinates: point({latitude: 39.9612, longitude: -82.9988}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-KY-AUTO-001',
  name: 'Louisville Vehicle Assembly',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'KY',
  city: 'Louisville',
  zipcode: '40202',
  coordinates: point({latitude: 38.2527, longitude: -85.7585}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-TN-AUTO-001',
  name: 'Nashville Auto Plant',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'TN',
  city: 'Nashville',
  zipcode: '37201',
  coordinates: point({latitude: 36.1627, longitude: -86.7816}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-AL-AUTO-001',
  name: 'Birmingham Automotive Assembly',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'AL',
  city: 'Birmingham',
  zipcode: '35203',
  coordinates: point({latitude: 33.5207, longitude: -86.8025}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-SC-AUTO-001',
  name: 'Greenville Auto Manufacturing',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'SC',
  city: 'Greenville',
  zipcode: '29601',
  coordinates: point({latitude: 34.8526, longitude: -82.3940}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-TX-AUTO-001',
  name: 'San Antonio Auto Plant',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'TX',
  city: 'San Antonio',
  zipcode: '78201',
  coordinates: point({latitude: 29.4241, longitude: -98.4936}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-CA-AUTO-001',
  name: 'Los Angeles Auto Assembly',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'CA',
  city: 'Los Angeles',
  zipcode: '90001',
  coordinates: point({latitude: 34.0522, longitude: -118.2437}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-IN-AUTO-001',
  name: 'Indianapolis Auto Plant',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'IN',
  city: 'Indianapolis',
  zipcode: '46201',
  coordinates: point({latitude: 39.7684, longitude: -86.1581}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-IL-AUTO-001',
  name: 'Chicago Auto Manufacturing',
  facilityType: 'Automotive Assembly',
  sector: 'Manufacturing',
  state: 'IL',
  city: 'Chicago',
  zipcode: '60601',
  coordinates: point({latitude: 41.8781, longitude: -87.6298}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AUTOMOTIVE'],
  created_date: datetime(),
  updated_date: datetime()
});

// Electronics Manufacturing (10 facilities)
CREATE (f:Facility {
  facilityId: 'MFG-CA-ELEC-001',
  name: 'Silicon Valley Electronics Plant',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'CA',
  city: 'San Jose',
  zipcode: '95101',
  coordinates: point({latitude: 37.3382, longitude: -121.8863}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-TX-ELEC-001',
  name: 'Austin Electronics Fab',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'TX',
  city: 'Austin',
  zipcode: '78701',
  coordinates: point({latitude: 30.2672, longitude: -97.7431}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-OR-ELEC-001',
  name: 'Portland Semiconductor Plant',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'OR',
  city: 'Portland',
  zipcode: '97201',
  coordinates: point({latitude: 45.5152, longitude: -122.6784}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-AZ-ELEC-001',
  name: 'Phoenix Electronics Assembly',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'AZ',
  city: 'Phoenix',
  zipcode: '85001',
  coordinates: point({latitude: 33.4484, longitude: -112.0740}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-MA-ELEC-001',
  name: 'Boston Electronics Manufacturing',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'MA',
  city: 'Boston',
  zipcode: '02101',
  coordinates: point({latitude: 42.3601, longitude: -71.0589}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-NY-ELEC-001',
  name: 'New York Electronics Plant',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'NY',
  city: 'New York',
  zipcode: '10001',
  coordinates: point({latitude: 40.7128, longitude: -74.0060}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-NC-ELEC-001',
  name: 'Raleigh Electronics Fab',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'NC',
  city: 'Raleigh',
  zipcode: '27601',
  coordinates: point({latitude: 35.7796, longitude: -78.6382}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-CO-ELEC-001',
  name: 'Denver Electronics Assembly',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'CO',
  city: 'Denver',
  zipcode: '80201',
  coordinates: point({latitude: 39.7392, longitude: -104.9903}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-MN-ELEC-001',
  name: 'Minneapolis Electronics Plant',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'MN',
  city: 'Minneapolis',
  zipcode: '55401',
  coordinates: point({latitude: 44.9778, longitude: -93.2650}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-WA-ELEC-001',
  name: 'Seattle Electronics Manufacturing',
  facilityType: 'Electronics Manufacturing',
  sector: 'Manufacturing',
  state: 'WA',
  city: 'Seattle',
  zipcode: '98101',
  coordinates: point({latitude: 47.6062, longitude: -122.3321}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_ELECTRONICS'],
  created_date: datetime(),
  updated_date: datetime()
});

// Aerospace Manufacturing (8 facilities)
CREATE (f:Facility {
  facilityId: 'MFG-WA-AERO-001',
  name: 'Seattle Aerospace Assembly',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'WA',
  city: 'Seattle',
  zipcode: '98102',
  coordinates: point({latitude: 47.6205, longitude: -122.3493}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-CA-AERO-001',
  name: 'Los Angeles Aerospace Plant',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'CA',
  city: 'Los Angeles',
  zipcode: '90002',
  coordinates: point({latitude: 33.9806, longitude: -118.2447}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-TX-AERO-001',
  name: 'Fort Worth Aerospace Manufacturing',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'TX',
  city: 'Fort Worth',
  zipcode: '76101',
  coordinates: point({latitude: 32.7555, longitude: -97.3308}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-CT-AERO-001',
  name: 'Hartford Aerospace Plant',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'CT',
  city: 'Hartford',
  zipcode: '06101',
  coordinates: point({latitude: 41.7658, longitude: -72.6734}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-FL-AERO-001',
  name: 'Cape Canaveral Aerospace Facility',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'FL',
  city: 'Cape Canaveral',
  zipcode: '32920',
  coordinates: point({latitude: 28.3922, longitude: -80.6077}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-AL-AERO-001',
  name: 'Huntsville Aerospace Manufacturing',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'AL',
  city: 'Huntsville',
  zipcode: '35801',
  coordinates: point({latitude: 34.7304, longitude: -86.5861}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-CO-AERO-001',
  name: 'Colorado Springs Aerospace Plant',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'CO',
  city: 'Colorado Springs',
  zipcode: '80901',
  coordinates: point({latitude: 38.8339, longitude: -104.8214}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-AZ-AERO-001',
  name: 'Tucson Aerospace Assembly',
  facilityType: 'Aerospace Manufacturing',
  sector: 'Manufacturing',
  state: 'AZ',
  city: 'Tucson',
  zipcode: '85701',
  coordinates: point({latitude: 32.2226, longitude: -110.9747}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_AEROSPACE'],
  created_date: datetime(),
  updated_date: datetime()
});

// Heavy Machinery Manufacturing (8 facilities)
CREATE (f:Facility {
  facilityId: 'MFG-IL-HEAVY-001',
  name: 'Peoria Heavy Machinery Plant',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'IL',
  city: 'Peoria',
  zipcode: '61601',
  coordinates: point({latitude: 40.6936, longitude: -89.5890}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-WI-HEAVY-001',
  name: 'Milwaukee Machinery Manufacturing',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'WI',
  city: 'Milwaukee',
  zipcode: '53201',
  coordinates: point({latitude: 43.0389, longitude: -87.9065}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-IA-HEAVY-001',
  name: 'Des Moines Heavy Equipment Plant',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'IA',
  city: 'Des Moines',
  zipcode: '50301',
  coordinates: point({latitude: 41.5868, longitude: -93.6250}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-PA-HEAVY-001',
  name: 'Pittsburgh Machinery Manufacturing',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'PA',
  city: 'Pittsburgh',
  zipcode: '15201',
  coordinates: point({latitude: 40.4406, longitude: -79.9959}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-GA-HEAVY-001',
  name: 'Atlanta Heavy Machinery Plant',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'GA',
  city: 'Atlanta',
  zipcode: '30301',
  coordinates: point({latitude: 33.7490, longitude: -84.3880}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-NC-HEAVY-001',
  name: 'Charlotte Machinery Manufacturing',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'NC',
  city: 'Charlotte',
  zipcode: '28201',
  coordinates: point({latitude: 35.2271, longitude: -80.8431}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-OH-HEAVY-001',
  name: 'Cincinnati Heavy Equipment Plant',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'OH',
  city: 'Cincinnati',
  zipcode: '45201',
  coordinates: point({latitude: 39.1031, longitude: -84.5120}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-MO-HEAVY-001',
  name: 'Kansas City Machinery Manufacturing',
  facilityType: 'Heavy Machinery Manufacturing',
  sector: 'Manufacturing',
  state: 'MO',
  city: 'Kansas City',
  zipcode: '64101',
  coordinates: point({latitude: 39.0997, longitude: -94.5786}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_HEAVY_MACHINERY'],
  created_date: datetime(),
  updated_date: datetime()
});

// Food Processing Plants (7 facilities)
CREATE (f:Facility {
  facilityId: 'MFG-IA-FOOD-001',
  name: 'Cedar Rapids Food Processing',
  facilityType: 'Food Processing',
  sector: 'Manufacturing',
  state: 'IA',
  city: 'Cedar Rapids',
  zipcode: '52401',
  coordinates: point({latitude: 41.9779, longitude: -91.6656}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_FOOD_PROCESSING'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-WI-FOOD-001',
  name: 'Green Bay Food Manufacturing',
  facilityType: 'Food Processing',
  sector: 'Manufacturing',
  state: 'WI',
  city: 'Green Bay',
  zipcode: '54301',
  coordinates: point({latitude: 44.5133, longitude: -88.0133}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_FOOD_PROCESSING'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-CA-FOOD-001',
  name: 'Fresno Food Processing Plant',
  facilityType: 'Food Processing',
  sector: 'Manufacturing',
  state: 'CA',
  city: 'Fresno',
  zipcode: '93701',
  coordinates: point({latitude: 36.7378, longitude: -119.7871}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_FOOD_PROCESSING'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-AR-FOOD-001',
  name: 'Little Rock Food Manufacturing',
  facilityType: 'Food Processing',
  sector: 'Manufacturing',
  state: 'AR',
  city: 'Little Rock',
  zipcode: '72201',
  coordinates: point({latitude: 34.7465, longitude: -92.2896}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_FOOD_PROCESSING'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-NE-FOOD-001',
  name: 'Omaha Food Processing',
  facilityType: 'Food Processing',
  sector: 'Manufacturing',
  state: 'NE',
  city: 'Omaha',
  zipcode: '68101',
  coordinates: point({latitude: 41.2565, longitude: -95.9345}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_FOOD_PROCESSING'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-KS-FOOD-001',
  name: 'Wichita Food Manufacturing',
  facilityType: 'Food Processing',
  sector: 'Manufacturing',
  state: 'KS',
  city: 'Wichita',
  zipcode: '67201',
  coordinates: point({latitude: 37.6872, longitude: -97.3301}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_FOOD_PROCESSING'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-MN-FOOD-001',
  name: 'Minneapolis Food Processing',
  facilityType: 'Food Processing',
  sector: 'Manufacturing',
  state: 'MN',
  city: 'Minneapolis',
  zipcode: '55402',
  coordinates: point({latitude: 44.9833, longitude: -93.2667}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_FOOD_PROCESSING'],
  created_date: datetime(),
  updated_date: datetime()
});

// Pharmaceutical/Medical Device Manufacturing (7 facilities)
CREATE (f:Facility {
  facilityId: 'MFG-NJ-PHARMA-001',
  name: 'New Brunswick Pharmaceutical Plant',
  facilityType: 'Pharmaceutical Manufacturing',
  sector: 'Manufacturing',
  state: 'NJ',
  city: 'New Brunswick',
  zipcode: '08901',
  coordinates: point({latitude: 40.4862, longitude: -74.4518}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_PHARMACEUTICAL'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-MA-PHARMA-001',
  name: 'Cambridge Biotech Manufacturing',
  facilityType: 'Pharmaceutical Manufacturing',
  sector: 'Manufacturing',
  state: 'MA',
  city: 'Cambridge',
  zipcode: '02138',
  coordinates: point({latitude: 42.3736, longitude: -71.1097}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_PHARMACEUTICAL'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-PA-PHARMA-001',
  name: 'Philadelphia Pharmaceutical Plant',
  facilityType: 'Pharmaceutical Manufacturing',
  sector: 'Manufacturing',
  state: 'PA',
  city: 'Philadelphia',
  zipcode: '19101',
  coordinates: point({latitude: 39.9526, longitude: -75.1652}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_PHARMACEUTICAL'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-CA-PHARMA-001',
  name: 'San Diego Biotech Manufacturing',
  facilityType: 'Pharmaceutical Manufacturing',
  sector: 'Manufacturing',
  state: 'CA',
  city: 'San Diego',
  zipcode: '92101',
  coordinates: point({latitude: 32.7157, longitude: -117.1611}),
  operational_status: 'active',
  capacity: 'high',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_PHARMACEUTICAL'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-NC-PHARMA-001',
  name: 'Research Triangle Pharma Plant',
  facilityType: 'Pharmaceutical Manufacturing',
  sector: 'Manufacturing',
  state: 'NC',
  city: 'Durham',
  zipcode: '27701',
  coordinates: point({latitude: 35.9940, longitude: -78.8986}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_PHARMACEUTICAL'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-IL-PHARMA-001',
  name: 'Chicago Pharmaceutical Manufacturing',
  facilityType: 'Pharmaceutical Manufacturing',
  sector: 'Manufacturing',
  state: 'IL',
  city: 'Chicago',
  zipcode: '60602',
  coordinates: point({latitude: 41.8819, longitude: -87.6278}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_PHARMACEUTICAL'],
  created_date: datetime(),
  updated_date: datetime()
});

CREATE (f:Facility {
  facilityId: 'MFG-IN-PHARMA-001',
  name: 'Indianapolis Medical Device Plant',
  facilityType: 'Pharmaceutical Manufacturing',
  sector: 'Manufacturing',
  state: 'IN',
  city: 'Indianapolis',
  zipcode: '46202',
  coordinates: point({latitude: 39.7910, longitude: -86.1480}),
  operational_status: 'active',
  capacity: 'medium',
  tags: ['MFG_FACILITY', 'SECTOR_MANUFACTURING', 'SUBSECTOR_PHARMACEUTICAL'],
  created_date: datetime(),
  updated_date: datetime()
});
