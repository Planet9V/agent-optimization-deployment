import subprocess
import json

print("═"*70)
print("CRITICAL FIX: Creating Missing Facility Nodes")
print("═"*70)

# Healthcare Facilities (60)
healthcare_facilities = [
    # Major Hospitals (20)
    ("HEALTH-ATL-001", "Hospital", "GA", 33.7490, -84.3880, "Grady Memorial Hospital"),
    ("HEALTH-BOS-001", "Hospital", "MA", 42.3601, -71.0589, "Massachusetts General Hospital"),
    ("HEALTH-CHI-001", "Hospital", "IL", 41.8781, -87.6298, "Northwestern Memorial Hospital"),
    ("HEALTH-DEN-001", "Hospital", "CO", 39.7392, -104.9903, "Denver Health Medical Center"),
    ("HEALTH-HOU-001", "Hospital", "TX", 29.7604, -95.3698, "Houston Methodist Hospital"),
    ("HEALTH-LA-001", "Hospital", "CA", 34.0522, -118.2437, "Cedars-Sinai Medical Center"),
    ("HEALTH-MIA-001", "Hospital", "FL", 25.7617, -80.1918, "Jackson Memorial Hospital"),
    ("HEALTH-NY-001", "Hospital", "NY", 40.7128, -74.0060, "Mount Sinai Hospital"),
    ("HEALTH-PHI-001", "Hospital", "PA", 39.9526, -75.1652, "Penn Presbyterian Medical Center"),
    ("HEALTH-PHX-001", "Hospital", "AZ", 33.4484, -112.0740, "Banner University Medical Center"),
    ("HEALTH-SEA-001", "Hospital", "WA", 47.6062, -122.3321, "Harborview Medical Center"),
    ("HEALTH-SF-001", "Hospital", "CA", 37.7749, -122.4194, "UCSF Medical Center"),
    ("HEALTH-DAL-001", "Hospital", "TX", 32.7767, -96.7970, "Parkland Memorial Hospital"),
    ("HEALTH-DET-001", "Hospital", "MI", 42.3314, -83.0458, "Detroit Medical Center"),
    ("HEALTH-MIN-001", "Hospital", "MN", 44.9778, -93.2650, "Hennepin County Medical Center"),
    ("HEALTH-STL-001", "Hospital", "MO", 38.6270, -90.1994, "Barnes-Jewish Hospital"),
    ("HEALTH-CLE-001", "Hospital", "OH", 41.4993, -81.6944, "Cleveland Clinic"),
    ("HEALTH-PIT-001", "Hospital", "PA", 40.4406, -79.9959, "UPMC Presbyterian"),
    ("HEALTH-BAL-001", "Hospital", "MD", 39.2904, -76.6122, "Johns Hopkins Hospital"),
    ("HEALTH-POR-001", "Hospital", "OR", 45.5152, -122.6784, "Oregon Health & Science University"),

    # Medical Centers (15)
    ("HEALTH-ATL-MED-001", "Medical Center", "GA", 33.7580, -84.3963, "Emory University Hospital"),
    ("HEALTH-BOS-MED-001", "Medical Center", "MA", 42.3370, -71.1061, "Brigham and Women's Hospital"),
    ("HEALTH-CHI-MED-001", "Medical Center", "IL", 41.7906, -87.6000, "University of Chicago Medical Center"),
    ("HEALTH-LA-MED-001", "Medical Center", "CA", 34.0689, -118.4452, "UCLA Medical Center"),
    ("HEALTH-NY-MED-001", "Medical Center", "NY", 40.7614, -73.9776, "NYU Langone Health"),
    ("HEALTH-SF-MED-001", "Medical Center", "CA", 37.7562, -122.4584, "Kaiser Permanente SF Medical Center"),
    ("HEALTH-SEA-MED-001", "Medical Center", "WA", 47.6232, -122.3080, "Swedish Medical Center"),
    ("HEALTH-DAL-MED-001", "Medical Center", "TX", 32.8136, -96.8489, "UT Southwestern Medical Center"),
    ("HEALTH-MIA-MED-001", "Medical Center", "FL", 25.7907, -80.2100, "University of Miami Hospital"),
    ("HEALTH-PHX-MED-001", "Medical Center", "AZ", 33.5023, -112.0740, "Mayo Clinic Phoenix"),
    ("HEALTH-DEN-MED-001", "Medical Center", "CO", 39.7456, -105.0019, "University of Colorado Hospital"),
    ("HEALTH-MIN-MED-001", "Medical Center", "MN", 44.0225, -92.4802, "Mayo Clinic Rochester"),
    ("HEALTH-POR-MED-001", "Medical Center", "OR", 45.4989, -122.6859, "Legacy Emanuel Medical Center"),
    ("HEALTH-PHI-MED-001", "Medical Center", "PA", 39.9496, -75.1956, "Temple University Hospital"),
    ("HEALTH-HOU-MED-001", "Medical Center", "TX", 29.7078, -95.3982, "MD Anderson Cancer Center"),

    # Urgent Care (10)
    ("HEALTH-LA-UC-001", "Urgent Care Facility", "CA", 34.0407, -118.2468, "LA Urgent Care Center"),
    ("HEALTH-NY-UC-001", "Urgent Care Facility", "NY", 40.7589, -73.9851, "Manhattan Urgent Care"),
    ("HEALTH-CHI-UC-001", "Urgent Care Facility", "IL", 41.8339, -87.8720, "Chicago Immediate Care"),
    ("HEALTH-HOU-UC-001", "Urgent Care Facility", "TX", 29.7355, -95.4010, "Houston Express Care"),
    ("HEALTH-PHX-UC-001", "Urgent Care Facility", "AZ", 33.4942, -112.0743, "Phoenix Urgent Care"),
    ("HEALTH-SF-UC-001", "Urgent Care Facility", "CA", 37.7858, -122.4364, "SF Quick Care Center"),
    ("HEALTH-SEA-UC-001", "Urgent Care Facility", "WA", 47.6205, -122.3493, "Seattle Urgent Care"),
    ("HEALTH-DEN-UC-001", "Urgent Care Facility", "CO", 39.7294, -104.8319, "Denver Urgent Care"),
    ("HEALTH-MIA-UC-001", "Urgent Care Facility", "FL", 25.7753, -80.2089, "Miami Urgent Care"),
    ("HEALTH-BOS-UC-001", "Urgent Care Facility", "MA", 42.3505, -71.0587, "Boston Immediate Care"),

    # Community Clinics (8)
    ("HEALTH-LA-CLINIC-001", "Community Clinic", "CA", 34.0219, -118.2816, "South LA Community Clinic"),
    ("HEALTH-NY-CLINIC-001", "Community Clinic", "NY", 40.8448, -73.8648, "Bronx Community Health Center"),
    ("HEALTH-CHI-CLINIC-001", "Community Clinic", "IL", 41.8487, -87.7405, "West Side Community Clinic"),
    ("HEALTH-HOU-CLINIC-001", "Community Clinic", "TX", 29.7230, -95.3439, "East Houston Clinic"),
    ("HEALTH-MIA-CLINIC-001", "Community Clinic", "FL", 25.8171, -80.2707, "Liberty City Health Center"),
    ("HEALTH-PHX-CLINIC-001", "Community Clinic", "AZ", 33.4153, -112.0764, "South Phoenix Clinic"),
    ("HEALTH-SF-CLINIC-001", "Community Clinic", "CA", 37.7272, -122.4031, "Bayview Community Clinic"),
    ("HEALTH-SEA-CLINIC-001", "Community Clinic", "WA", 47.5480, -122.3302, "Rainier Beach Clinic"),

    # Rehabilitation Centers (4)
    ("HEALTH-ATL-REHAB-001", "Rehabilitation Center", "GA", 33.7926, -84.3240, "Atlanta Rehab Center"),
    ("HEALTH-LA-REHAB-001", "Rehabilitation Center", "CA", 34.0736, -118.3994, "Los Angeles Rehab"),
    ("HEALTH-CHI-REHAB-001", "Rehabilitation Center", "IL", 41.9278, -87.6512, "Chicago Rehab Institute"),
    ("HEALTH-NY-REHAB-001", "Rehabilitation Center", "NY", 40.7896, -73.9537, "Rusk Rehabilitation"),

    # Diagnostic Labs (3)
    ("HEALTH-SF-LAB-001", "Diagnostic Laboratory", "CA", 37.7937, -122.3965, "Quest Diagnostics SF"),
    ("HEALTH-NY-LAB-001", "Diagnostic Laboratory", "NY", 40.7411, -73.9897, "LabCorp Manhattan"),
    ("HEALTH-CHI-LAB-001", "Diagnostic Laboratory", "IL", 41.8858, -87.6229, "Abbott Diagnostics Chicago")
]

# Chemical Facilities (40)
chemical_facilities = [
    # Chemical Manufacturing Plants (10)
    ("CHEM-TX-001", "Chemical Manufacturing Plant", "TX", 29.7433, -95.3461, "Houston Chemical Complex"),
    ("CHEM-LA-001", "Chemical Manufacturing Plant", "LA", 30.2241, -92.0198, "Louisiana Chemical Plant"),
    ("CHEM-NJ-001", "Chemical Manufacturing Plant", "NJ", 40.8426, -74.2734, "New Jersey Chemical Works"),
    ("CHEM-OH-001", "Chemical Manufacturing Plant", "OH", 41.0814, -81.5190, "Cleveland Chemical Plant"),
    ("CHEM-IL-001", "Chemical Manufacturing Plant", "IL", 41.5051, -90.5151, "Illinois Chemical Facility"),
    ("CHEM-PA-001", "Chemical Manufacturing Plant", "PA", 40.4406, -79.9959, "Pittsburgh Chemical Works"),
    ("CHEM-MI-001", "Chemical Manufacturing Plant", "MI", 42.9634, -82.4242, "Michigan Chemical Plant"),
    ("CHEM-CA-001", "Chemical Manufacturing Plant", "CA", 33.9425, -118.4081, "Los Angeles Chemical Complex"),
    ("CHEM-NC-001", "Chemical Manufacturing Plant", "NC", 35.2271, -80.8431, "Charlotte Chemical Plant"),
    ("CHEM-TN-001", "Chemical Manufacturing Plant", "TN", 35.0456, -85.3097, "Tennessee Chemical Facility"),

    # Petrochemical Plants (8)
    ("CHEM-TX-PETRO-001", "Petrochemical Plant", "TX", 29.6994, -95.2089, "Baytown Petrochemical Complex"),
    ("CHEM-LA-PETRO-001", "Petrochemical Plant", "LA", 29.9499, -90.0701, "Baton Rouge Petrochemical"),
    ("CHEM-TX-PETRO-002", "Petrochemical Plant", "TX", 29.7502, -95.0632, "Pasadena Petrochemical"),
    ("CHEM-LA-PETRO-002", "Petrochemical Plant", "LA", 30.0075, -90.4782, "Lake Charles Petrochemical"),
    ("CHEM-AL-PETRO-001", "Petrochemical Plant", "AL", 30.6944, -88.0431, "Mobile Petrochemical"),
    ("CHEM-MS-PETRO-001", "Petrochemical Plant", "MS", 30.3960, -89.0928, "Pascagoula Petrochemical"),
    ("CHEM-TX-PETRO-003", "Petrochemical Plant", "TX", 28.0369, -97.0403, "Corpus Christi Petrochemical"),
    ("CHEM-CA-PETRO-001", "Petrochemical Plant", "CA", 33.7701, -118.1937, "Long Beach Petrochemical"),

    # Pharmaceutical Manufacturing (6)
    ("CHEM-NJ-PHARMA-001", "Pharmaceutical Manufacturing", "NJ", 40.4862, -74.4518, "Princeton Pharma Plant"),
    ("CHEM-PA-PHARMA-001", "Pharmaceutical Manufacturing", "PA", 40.0379, -75.0811, "Philadelphia Pharma"),
    ("CHEM-CA-PHARMA-001", "Pharmaceutical Manufacturing", "CA", 37.5485, -121.9886, "Bay Area Pharma"),
    ("CHEM-MA-PHARMA-001", "Pharmaceutical Manufacturing", "MA", 42.4072, -71.3824, "Boston Pharma Plant"),
    ("CHEM-NC-PHARMA-001", "Pharmaceutical Manufacturing", "NC", 35.9132, -79.0558, "Research Triangle Pharma"),
    ("CHEM-IL-PHARMA-001", "Pharmaceutical Manufacturing", "IL", 41.7606, -87.7036, "Chicago Pharma Plant"),

    # Fertilizer Production Plants (6)
    ("CHEM-IA-FERT-001", "Fertilizer Production Plant", "IA", 42.0308, -93.6319, "Iowa Fertilizer Plant"),
    ("CHEM-IL-FERT-001", "Fertilizer Production Plant", "IL", 40.1164, -88.2434, "Illinois Fertilizer"),
    ("CHEM-KS-FERT-001", "Fertilizer Production Plant", "KS", 38.8403, -97.6114, "Kansas Fertilizer Plant"),
    ("CHEM-NE-FERT-001", "Fertilizer Production Plant", "NE", 41.2565, -95.9345, "Nebraska Fertilizer"),
    ("CHEM-OK-FERT-001", "Fertilizer Production Plant", "OK", 35.4676, -97.5164, "Oklahoma Fertilizer Plant"),
    ("CHEM-TX-FERT-001", "Fertilizer Production Plant", "TX", 33.2148, -97.1331, "North Texas Fertilizer"),

    # Hazardous Material Storage (5)
    ("CHEM-TX-HAZ-001", "Hazardous Material Storage", "TX", 29.7355, -95.5133, "Houston Hazmat Storage"),
    ("CHEM-LA-HAZ-001", "Hazardous Material Storage", "LA", 30.4515, -91.1871, "Baton Rouge Hazmat"),
    ("CHEM-NJ-HAZ-001", "Hazardous Material Storage", "NJ", 40.5796, -74.3227, "New Jersey Hazmat Storage"),
    ("CHEM-CA-HAZ-001", "Hazardous Material Storage", "CA", 33.8366, -118.3897, "LA Hazmat Storage"),
    ("CHEM-IL-HAZ-001", "Hazardous Material Storage", "IL", 41.7658, -87.7321, "Chicago Hazmat Storage"),

    # Waste Treatment Facilities (5)
    ("CHEM-TX-WASTE-001", "Chemical Waste Treatment", "TX", 29.5805, -95.6389, "Houston Waste Treatment"),
    ("CHEM-LA-WASTE-001", "Chemical Waste Treatment", "LA", 30.2672, -92.0211, "Louisiana Waste Treatment"),
    ("CHEM-OH-WASTE-001", "Chemical Waste Treatment", "OH", 41.2565, -81.8552, "Cleveland Waste Treatment"),
    ("CHEM-CA-WASTE-001", "Chemical Waste Treatment", "CA", 34.0007, -118.2468, "LA Waste Treatment"),
    ("CHEM-MI-WASTE-001", "Chemical Waste Treatment", "MI", 42.7325, -84.5555, "Lansing Waste Treatment")
]

# Manufacturing Facilities (50)
manufacturing_facilities = [
    # Automotive Manufacturing (10)
    ("MFG-MI-AUTO-001", "Automotive Manufacturing", "MI", 42.3314, -83.0458, "Detroit Auto Plant"),
    ("MFG-OH-AUTO-001", "Automotive Manufacturing", "OH", 39.9612, -82.9988, "Columbus Auto Assembly"),
    ("MFG-IN-AUTO-001", "Automotive Manufacturing", "IN", 39.7684, -86.1581, "Indianapolis Auto Plant"),
    ("MFG-KY-AUTO-001", "Automotive Manufacturing", "KY", 38.2527, -85.7585, "Louisville Auto Assembly"),
    ("MFG-TN-AUTO-001", "Automotive Manufacturing", "TN", 35.8456, -86.3903, "Smyrna Auto Plant"),
    ("MFG-AL-AUTO-001", "Automotive Manufacturing", "AL", 32.3668, -86.2999, "Tuscaloosa Auto Assembly"),
    ("MFG-TX-AUTO-001", "Automotive Manufacturing", "TX", 32.7555, -97.3308, "Fort Worth Auto Plant"),
    ("MFG-IL-AUTO-001", "Automotive Manufacturing", "IL", 41.5868, -88.0819, "Belvidere Auto Assembly"),
    ("MFG-MO-AUTO-001", "Automotive Manufacturing", "MO", 38.5767, -92.1736, "Kansas City Auto Plant"),
    ("MFG-SC-AUTO-001", "Automotive Manufacturing", "SC", 34.5034, -82.6501, "Greenville Auto Assembly"),

    # Aerospace Manufacturing (8)
    ("MFG-WA-AERO-001", "Aerospace Manufacturing", "WA", 47.9064, -122.2814, "Everett Aerospace Plant"),
    ("MFG-CA-AERO-001", "Aerospace Manufacturing", "CA", 33.6846, -117.8265, "Long Beach Aerospace"),
    ("MFG-TX-AERO-001", "Aerospace Manufacturing", "TX", 32.8483, -96.8511, "Fort Worth Aerospace"),
    ("MFG-FL-AERO-001", "Aerospace Manufacturing", "FL", 28.5383, -81.3792, "Orlando Aerospace"),
    ("MFG-CT-AERO-001", "Aerospace Manufacturing", "CT", 41.7658, -72.6734, "East Hartford Aerospace"),
    ("MFG-AZ-AERO-001", "Aerospace Manufacturing", "AZ", 33.3062, -111.8413, "Mesa Aerospace Plant"),
    ("MFG-GA-AERO-001", "Aerospace Manufacturing", "GA", 33.6407, -84.4277, "Marietta Aerospace"),
    ("MFG-OH-AERO-001", "Aerospace Manufacturing", "OH", 39.7817, -84.0773, "Dayton Aerospace Plant"),

    # Steel Mills (6)
    ("MFG-IN-STEEL-001", "Steel Mill", "IN", 41.5892, -87.3095, "Gary Steel Works"),
    ("MFG-PA-STEEL-001", "Steel Mill", "PA", 40.4406, -79.9959, "Pittsburgh Steel Mill"),
    ("MFG-OH-STEEL-001", "Steel Mill", "OH", 41.5051, -81.6934, "Cleveland Steel Works"),
    ("MFG-IL-STEEL-001", "Steel Mill", "IL", 41.5394, -87.6648, "Chicago Steel Mill"),
    ("MFG-MI-STEEL-001", "Steel Mill", "MI", 42.2395, -83.1753, "Dearborn Steel Works"),
    ("MFG-AL-STEEL-001", "Steel Mill", "AL", 33.5186, -86.8104, "Birmingham Steel Mill"),

    # Shipbuilding (6)
    ("MFG-VA-SHIP-001", "Shipbuilding Yard", "VA", 36.8508, -76.2859, "Newport News Shipyard"),
    ("MFG-MS-SHIP-001", "Shipbuilding Yard", "MS", 30.3674, -88.5558, "Pascagoula Shipyard"),
    ("MFG-ME-SHIP-001", "Shipbuilding Yard", "ME", 43.6591, -70.2568, "Bath Iron Works"),
    ("MFG-CA-SHIP-001", "Shipbuilding Yard", "CA", 32.7157, -117.1611, "San Diego Shipyard"),
    ("MFG-WA-SHIP-001", "Shipbuilding Yard", "WA", 47.5480, -122.6501, "Bremerton Shipyard"),
    ("MFG-CT-SHIP-001", "Shipbuilding Yard", "CT", 41.3557, -72.0995, "Groton Shipyard"),

    # Engine/Turbine Manufacturing (6)
    ("MFG-NC-ENG-001", "Engine Manufacturing", "NC", 35.5951, -82.5515, "Asheville Engine Plant"),
    ("MFG-WI-ENG-001", "Engine Manufacturing", "WI", 43.0389, -87.9065, "Milwaukee Engine Works"),
    ("MFG-OH-ENG-001", "Engine Manufacturing", "OH", 40.1084, -83.0188, "Columbus Engine Plant"),
    ("MFG-IL-ENG-001", "Engine Manufacturing", "IL", 40.6331, -89.3985, "Peoria Engine Works"),
    ("MFG-IN-ENG-001", "Engine Manufacturing", "IN", 39.5237, -87.3887, "Terre Haute Engine Plant"),
    ("MFG-NY-ENG-001", "Engine Manufacturing", "NY", 42.9634, -78.7381, "Buffalo Engine Works"),

    # Defense Manufacturing (6)
    ("MFG-CT-DEF-001", "Defense Systems Manufacturing", "CT", 41.2033, -73.1123, "Stratford Defense Plant"),
    ("MFG-MA-DEF-001", "Defense Systems Manufacturing", "MA", 42.4184, -71.0656, "Tewksbury Defense Systems"),
    ("MFG-VA-DEF-001", "Defense Systems Manufacturing", "VA", 38.9072, -77.4739, "Fairfax Defense Plant"),
    ("MFG-CA-DEF-001", "Defense Systems Manufacturing", "CA", 32.8801, -117.2340, "San Diego Defense Systems"),
    ("MFG-AZ-DEF-001", "Defense Systems Manufacturing", "AZ", 33.4255, -111.9400, "Scottsdale Defense Plant"),
    ("MFG-TX-DEF-001", "Defense Systems Manufacturing", "TX", 32.7295, -97.1081, "Fort Worth Defense Systems"),

    # Aluminum Production (4)
    ("MFG-WA-ALU-001", "Aluminum Production", "WA", 48.7519, -122.4787, "Ferndale Aluminum Smelter"),
    ("MFG-NY-ALU-001", "Aluminum Production", "NY", 44.6995, -75.1449, "Massena Aluminum Plant"),
    ("MFG-MT-ALU-001", "Aluminum Production", "MT", 48.1918, -114.3122, "Columbia Falls Aluminum"),
    ("MFG-KY-ALU-001", "Aluminum Production", "KY", 37.0688, -87.5594, "Hawesville Aluminum Plant"),

    # Heavy Machinery (4)
    ("MFG-IL-HEAVY-001", "Heavy Machinery Manufacturing", "IL", 40.6936, -89.5890, "Peoria Heavy Equipment"),
    ("MFG-IA-HEAVY-001", "Heavy Machinery Manufacturing", "IA", 42.0046, -93.6140, "Waterloo Heavy Machinery"),
    ("MFG-WI-HEAVY-001", "Heavy Machinery Manufacturing", "WI", 44.5192, -88.0198, "Green Bay Heavy Equipment"),
    ("MFG-PA-HEAVY-001", "Heavy Machinery Manufacturing", "PA", 40.2732, -76.8867, "Lancaster Heavy Machinery")
]

def create_facilities(facilities, sector_name):
    count = 0
    print(f"\n{'─'*70}")
    print(f"Creating {len(facilities)} {sector_name} Facility nodes...")
    print(f"{'─'*70}")

    for fac_id, fac_type, state, lat, lon, name in facilities:
        query = f"""
CREATE (f:Facility {{
  facilityId: '{fac_id}',
  name: '{name}',
  facilityType: '{fac_type}',
  state: '{state}',
  latitude: {lat},
  longitude: {lon},
  geographic_point: point({{latitude: {lat}, longitude: {lon}}}),
  customer_namespace: 'CISA',
  tags: ['CISA_SECTOR', 'SECTOR_{sector_name.upper()}'],
  created_date: datetime(),
  updated_date: datetime()
}});
"""

        result = subprocess.run(
            ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            count += 1
            if count % 10 == 0:
                print(f"  Created {count}/{len(facilities)} facilities...")

    print(f"✅ {sector_name} Facilities created: {count}/{len(facilities)}")
    return count

# Create all facilities
total = 0
total += create_facilities(healthcare_facilities, "Healthcare")
total += create_facilities(chemical_facilities, "Chemical")
total += create_facilities(manufacturing_facilities, "Manufacturing")

print(f"\n{'═'*70}")
print(f"FACILITY CREATION COMPLETE")
print(f"{'═'*70}")
print(f"Total Facilities Created: {total}")

# Verify
verify = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg',
     """MATCH (f:Facility)
     WHERE f.facilityId STARTS WITH 'HEALTH-' OR f.facilityId STARTS WITH 'CHEM-' OR f.facilityId STARTS WITH 'MFG-'
     RETURN SUBSTRING(f.facilityId, 0, 6) AS prefix, COUNT(f) AS count
     ORDER BY prefix;"""],
    capture_output=True,
    text=True
)

print(f"\nFacility Verification:")
print(verify.stdout)

print("\n✅ Ready to re-run Phase 2 (relationships) and Phase 3 (tagging)")
