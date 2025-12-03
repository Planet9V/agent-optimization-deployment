
Exhaustive Inventory and Geocoding of United States Water Treatment Facilities: A Regulatory Data Synthesis


I. Executive Synthesis: The Regulatory and Data Landscape of U.S. Water Infrastructure

The successful compilation of an exhaustive national inventory of water treatment facilities requires synthesizing data from distinct federal regulatory universes. The term "water treatment facilities" encompasses two large and separate infrastructure sets managed by the U.S. Environmental Protection Agency (EPA): Public Drinking Water Systems (PWS) and Wastewater Treatment Plants (WWTPs).

1.1. The Bifurcated Infrastructure Inventory

The totality of regulated water infrastructure in the United States comprises approximately 168,000 systems.1 This inventory is fundamentally divided by statute:
Public Drinking Water Systems (PWS): These facilities, numbering roughly 152,000 nationwide, are governed by the Safe Drinking Water Act (SDWA). Their primary function is providing potable water for human consumption, and they are centrally tracked by the Safe Drinking Water Information System (SDWIS).1
Wastewater Treatment Plants (WWTPs): These facilities, exceeding 16,000 systems, are primarily regulated under the Clean Water Act (CWA) via the National Pollutant Discharge Elimination System (NPDES) permit program. These facilities process sewage and industrial wastewater before discharge, and their data is managed within the Integrated Compliance Information System (ICIS).1
Due to the sheer number of facilities and the high complexity of the data requirements (Name, Type, Size, Full Address, City, County, State, Country), the only viable mechanism for achieving a complete inventory is through the bulk data download files provided by the EPA, rather than relying on interactive search interfaces.4

1.2. The Central Data Repository: EPA’s ECHO System

The definitive source for this exhaustive inventory is the Enforcement and Compliance History Online (ECHO) system, which functions as the central portal for EPA regulatory databases. ECHO facilitates the bulk download of national datasets, ensuring data integrity and comprehensive coverage.4
SDWIS Data: PWS data is provided through the SDWA Dataset files, which are released quarterly. Key files include SDWA_PUB_WATER_SYSTEMS.csv, which contains system names and basic identification data, and associated files like SDWA_FACILITIES.csv and SDWA_GEOGRAPHIC_AREAS.csv for spatial information.4
ICIS-NPDES Data: WWTP data is found by accessing the ICIS-NPDES datasets, which provide detailed information on pollutant loadings, permit status, and treatment technologies.3

1.3. The Facility Linkage Mechanism: Facility Registry Service (FRS)

A crucial technical step in unifying the drinking water and wastewater inventories and accurately locating facilities is utilizing the EPA’s Facility Registry Service (FRS).5 SDWIS and ICIS-NPDES employ distinct internal identification schemas (PWSID and NPDES ID, respectively).3 To reliably merge records from these two disparate regulatory systems and acquire a standardized, verified location, the common denominator is the FRS ID (also known as the Unique Identification Number or UIN).7
The FRS acts as the definitive geocoding layer for all EPA-regulated entities.5 By joining the PWS and WWTP records via the FRS ID, analysts can pull consistent and validated address data from the FRS Location Reference Database. This process ensures that the requested "Full Address," City, County, and State fields are standardized and prevents conflicts that arise from relying solely on proprietary regulatory addresses recorded in SDWIS or ICIS.3

II. Data Acquisition and Structuring for Drinking Water Facilities (PWS)

The inventory of 152,000 public water systems requires precise mapping of regulatory codes to the requested tabular output fields.

2.1. Locating the Core PWS Data (SDWIS Download)

The core data files, available in CSV format via the ECHO SDWA Download Summary, provide the raw components necessary for the drinking water inventory.4 Essential fields—such as the PWS identification number (PWSID), system name, population served, and geographic codes—are contained within files like SDWA_PUB_WATER_SYSTEMS.csv and its related tables.2

2.2. Defining the "Type" Field: PWS Regulatory Classifications

The definition of a facility's "Type" for drinking water systems is strictly governed by the SDWA based on the population served and the frequency of service. This classification is captured by the PWS Type Code (PWS_TYPE_CODE).8
The three main classifications are:
Community Water Systems (CWS): These systems provide water to the same residents year-round, serving at least 15 service connections or 25 year-round residents. Examples include municipalities and residential developments.9 Approximately 50,000 community water systems exist nationwide.1
Non-Transient Non-Community Water Systems (NTNCWS): These non-community systems regularly serve a stable population of at least 25 people over six months per year, such as schools, hospitals, and factories.9
Transient Non-Community Water Systems (TNCWS): These systems serve at least 25 individuals daily for at least 60 days per year, but not the same persons regularly. Examples include campgrounds, gas stations, and restaurants.10 TNCWS represent the smallest and often most numerous segment of the PWS inventory.

2.3. Deriving the "Size" Field: The Population Served Proxy

A significant data requirement challenge arises in defining the "Size" field for PWS facilities. While wastewater facilities use Million Gallons per Day (MGD) capacity, the primary regulatory metric used by SDWIS for PWS is the Population Served (POPULATION_SERVED).2 For the numerous smaller systems, particularly TNCWS, engineered MGD flow capacity is frequently not tracked or reported to the EPA.
Consequently, to ensure a complete inventory of all 152,000 systems, the "Size" metric for PWS must be based on the population served count.2 This is a necessary substitution because the regulatory definition of a PWS hinges on serving a minimum of 25 individuals daily.10 While an estimated MGD capacity could be derived using standard per capita usage rates, the raw SDWIS output provides the definitive Population Served count, requiring the final unified table to include a clear unit designation to prevent misinterpretation.

2.4. Mapping Location Data (City, County, State, Full Address)

Location details are derived from multiple SDWIS and FRS files. SDWIS tracks basic system details, including the City or County served.2 However, obtaining the verified, standardized "Full Address" for geocoding purposes necessitates the aforementioned linkage via the FRS ID.5 Once the PWSID is linked to its corresponding FRS ID, the FRS Location Reference Database provides the authoritative street address, city, county, and state codes necessary for precise mapping.3

III. Data Acquisition and Structuring for Wastewater Facilities (WWTPs)

The inventory of over 16,000 wastewater facilities is fundamentally different from the PWS inventory, relying on engineering metrics (capacity) and discharge permit status (NPDES).

3.1. Locating the Core WWTP Data (ICIS-NPDES Download)

Wastewater treatment plants are identified by their unique NPDES ID within the ICIS-NPDES database.3 These data elements, including facility name, address, and compliance history, are available through the ECHO data downloads interface, specifically by selecting FRS and ICIS-NPDES datasets.5 This database also links to other relevant data sources like the Clean Watershed Needs Survey (CWNS).3

3.2. Defining the "Type" Field: Treatment Level and Permit Status

For wastewater facilities, the "Type" field is best defined by the level of treatment implemented and the facility's regulatory status (Major or Minor permit). The complexity of treatment determines the environmental impact and capital investment required. Treatment levels often range from primary and secondary treatment to advanced processes, such as:
Denitrification and Filtration: Used to achieve stringent permit limits, as seen at DC Water's Blue Plains facility.13
Biological Nutrient Removal (BNR): Targeted removal of nitrogen and phosphorus, which contribute to nutrient pollution in receiving waters.14
Facilities with enhanced treatment systems are often able to optimize operations or incorporate technology upgrades to reduce nutrient loads significantly.15

3.3. Deriving the "Size" Field: Capacity in Million Gallons per Day (MGD)

The "Size" of a WWTP is quantified by its engineered design capacity, typically measured in Million Gallons per Day (MGD).14 This is a direct measure of the plant’s ability to treat, move, or reuse water.16
For large, critical infrastructure facilities, it is necessary to capture two key capacity metrics, both available in ICIS-NPDES reports:
Dry-Weather Capacity: The average daily flow capacity, which is the standard operational size metric.
Wet-Weather/Peak Capacity: The maximum daily flow the plant can accommodate during heavy rainfall or storm events.17
These metrics are essential for understanding the resilience and operational envelope of the infrastructure. Capacity may be reported in cubic meters per day ($m^{3}/\text{day}$) in some databases, where $1 \text{ MGD}$ is approximately equivalent to $3,785 \text{ m}^{3}/\text{day}$.14

3.4. Exemplar Analysis: The Giants of U.S. Wastewater Infrastructure

Analysis of the largest U.S. wastewater treatment facilities demonstrates the scale and complexity of this critical infrastructure sector and provides definitive examples of capacity reporting:
Exemplar Data: Major U.S. Wastewater Treatment Facilities (WWTPs)

Name
Type
Size (Dry-Weather Capacity)
Location (Address)
City, County, State, Country
Stickney Water Reclamation Plant
WWTP (Advanced Secondary/Nutrient Recovery)
704 MGD ($2,665,000 \text{ m}^{3}/\text{day}$)
5901 West Pershing Road
Stickney, Cook, IL, USA 17
Blue Plains Advanced WWTP
WWTP (Advanced Treatment)
384 MGD ($1,450,000 \text{ m}^{3}/\text{day}$)
1385 Canal Street SE / 5000 Overlook Ave SW
Washington, DC, DC, USA 13
Detroit Wastewater Treatment Plant
WWTP (Secondary)
650 MGD ($2,460,000 \text{ m}^{3}/\text{day}$)
Address via FRS
Detroit, Wayne, MI, USA 17
Passaic Valley Sewerage Commission
WWTP (Secondary)
348 MGD ($1,320,000 \text{ m}^{3}/\text{day}$)
600 Wilson Avenue
Newark, Essex, NJ, USA 20
Deer Island Waste Water Treatment Plant
WWTP (Secondary)
380 MGD ($1,438,000 \text{ m}^{3}/\text{day}$)
Address via FRS
Boston, Suffolk, MA, USA 17
South Bay International WWTP
WWTP (Secondary/Binational)
25 MGD (Expandable to 100 MGD)
Near San Ysidro Port of Entry
San Ysidro, San Diego, CA, USA 22

The Blue Plains Advanced WWTP, for instance, is the world's largest advanced wastewater treatment plant, treating nearly 300 million gallons of wastewater on an average day with a peak capacity exceeding 780 million gallons per day, serving a complex region spanning Washington D.C., Maryland, and Virginia.13 The size and operational footprint of these facilities underscore the need for accurate geographic data linked via FRS, especially since facilities like the Stickney WRP are transitioning into resource recovery centers that produce high-value fertilizer.24

IV. Comprehensive Data Integration and Geocoding Strategy

Unifying the 152,000 PWS records and the 16,000+ WWTP records into a single, cohesive table requires a multi-step data integration and standardization procedure.

4.1. Technical Procedure for Data Unification

The reliable merger of the SDWIS and ICIS-NPDES inventories must proceed as follows:
PWS Data Extraction: Download the core SDWIS files. Isolate key fields: PWSID, PWS NAME, PWS TYPE CODE, POPULATION SERVED, and the FRS ID.2
WWTP Data Extraction: Download the ICIS-NPDES datasets. Isolate key fields: NPDES ID, PERMITTEE NAME, DESIGN CAPACITY (MGD), and the FRS ID.3
FRS Address Merging: This is the critical linkage step. The FRS bulk file contains standardized location data for most regulated facilities. Joining both the PWS and WWTP datasets to the FRS file using the FRS ID ensures that the "Full Address," standardized City, County, and State are sourced from the authoritative geocoding database.3
Schema Standardization: Map the disparate source fields (PWS NAME/PERMITTEE NAME; POPULATION SERVED/DESIGN CAPACITY) into the final unified table structure, ensuring data consistency across the two regulatory systems.

4.2. Addressing Location Data Nuances and Contradictions

When compiling the "Full Address" field, it is important to recognize that physical locations of vast facilities may cause address ambiguities. For instance, while the Stickney Water Reclamation Plant's official registry location is 5901 West Pershing Road, Stickney, IL 60650 18, navigational software may cite the address in Cicero, IL.25 Similarly, the Blue Plains Advanced WWTP location is sometimes cited using its postal address (1385 Canal Street SE) and sometimes its physical access point (5000 Overlook Avenue, SW).13
These discrepancies occur because EPA regulatory data often records the permittee’s official mailing address, which may differ from the facility’s physical location. For accurate spatial analysis of these critical assets, it is recommended that the FRS-linked data utilizes the validated geographic coordinates (centroid) whenever possible, as this spatial data is superior to textual street addresses for infrastructure mapping.5

4.3. Standardizing Capacity Metrics for the Unified Table

The final unified table must accommodate two distinct definitions of "Size." If the inventory contains both PWS and WWTP records, the "Size" column requires standardization with an auxiliary "Units" column.
PWS systems will populate the "Size" field with a numerical value representing the Population Served, with the corresponding unit listed as "PERSONS SERVED".2
WWTP systems will populate the "Size" field with the numerical value of the Dry-Weather Capacity, with the corresponding unit listed as "MGD" or $m^{3}/\text{day}$.14
Failing to include this explicit unit distinction would lead to significant data misinterpretation, confusing population counts with millions of gallons of daily flow.

Unified Inventory Schema and Data Dictionary

The following table defines the required schema for the final, integrated inventory, cross-referencing the required user field with the technical data element names from the source systems:

User Requested Field
SDWIS/PWS Field
ICIS-NPDES/WWTP Field
FRS Geocoding Field
ID Linkage Key
PWSID
NPDES ID
FRS ID 3
Name
PWS NAME
PERMITTEE NAME
FACILITY NAME
Type
PWS TYPE CODE 8
PERMIT TYPE / TREATMENT LEVEL
-
Size Value
POPULATION_SERVED 2
DESIGN_FLOW_RATE (MGD) 14
-
Size Unit
PERSONS SERVED
MGD / $m^{3}/\text{day}$ 16
-
Location (Full Address)
-
-
ADDRESS LINE 1, POSTAL CODE 5
City
PWS CITY NAME
SITE CITY
CITY NAME
County
COUNTY NAME
SITE COUNTY
COUNTY NAME
State
STATE CODE
STATE CODE
STATE CODE
Country
COUNTRY CODE
COUNTRY CODE
COUNTRY CODE


V. Advanced Analysis: Operational Insights and Regulatory Context

Beyond mere inventory creation, understanding the operational priorities and regulatory drivers of these two infrastructure sectors provides critical context for the data collected.

5.1. PWS Operational Focus: Source Water and Compliance

PWS facilities operate primarily to ensure compliance with the National Primary Drinking Water Regulations, which establish enforceable Maximum Contaminant Levels (MCLs) and treatment techniques designed to protect public health.26 The required treatment processes are heavily influenced by the source water type, which is categorized in SDWIS as Ground Water (GW), Surface Water (SW), or Ground water Under the Direct Influence of Surface water (GWUDI).27
For instance, surface water systems or GWUDI systems serving fewer than 10,000 people must comply with the Long Term 1 Enhanced Surface Water Treatment Rule provisions, requiring specific turbidity standards and pathogen removal requirements.26 This operational requirement highlights that the "Type" of facility includes not only its CWS/NTNCWS status but also its source water vulnerability.

5.2. WWTP Operational Focus: Nutrient Removal and Resource Recovery

Wastewater treatment, while fundamentally focused on discharge standards, has increasingly shifted towards managing nutrient pollution (nitrogen and phosphorus).15 These elements, found in human waste and detergents, contribute to oxygen depletion and algal blooms in receiving water bodies.15
The largest facilities are undergoing technological transformation to address this challenge. For example, the Stickney WRP implemented nutrient recovery facilities that extract phosphorus and nitrogen to create 10,000 tons of high-value fertilizer annually, transforming the facility into a resource recovery center rather than solely a treatment plant.24 These advanced treatment systems, such as those employing Biological Nutrient Removal (BNR) 14, are tracked via the Wastewater Treatment Technology Information section of ICIS-NPDES reports.3

5.3. Interdependence and Critical Functions

The entire US water and wastewater sector, encompassing approximately 168,000 systems, is designated as a critical infrastructure sector.1 CISA recognizes both the ability to supply water and to manage wastewater as National Critical Functions (NCFs).1
The existence of such a massive, interconnected network—serving over 80 percent of the U.S. population with drinking water and 75 percent with sewage treatment—means that disruptions can cause widespread public health crises and severe economic impacts.1 The vulnerability of this sector extends beyond physical attacks and contamination to include cyberattacks and natural disasters. The data compiled in this exhaustive inventory is therefore foundational for regional governance, resilience planning, and national security efforts.1

VI. Implementation Guide and Data Delivery

The delivery of this comprehensive inventory relies entirely upon the user successfully navigating the EPA’s bulk data download systems and executing the prescribed FRS linkage strategy.

6.1. Definitive Access Point for Bulk Data

The single authoritative location for accessing the raw data files necessary for this inventory is the EPA ECHO Data Downloads page.4
For the PWS inventory, the user must download the Safe Drinking Water Act (SDWA) bulk data files, which are refreshed quarterly.4 For the WWTP inventory and definitive location data, the user must access the bulk files for the ICIS-NPDES and Facility Registry Service (FRS) databases.5

6.2. Conclusion and Final Deliverable Structure

A full, exhaustive inventory of all water treatment facilities in the United States requires the structured synthesis of approximately 168,000 records from two distinct regulatory programs (SDWA and CWA). The resulting data product, when standardized according to the schema provided in Section IV, will deliver a reliable tabular format necessary for rigorous geospatial and regulatory analysis. The reliability of the "Full Address" and consistency of the "Size" metric depends entirely on the successful technical procedure of cross-referencing PWSID and NPDES ID records through the common FRS ID.
The final deliverable, encompassing this entire scope, must adhere to the Unified Inventory Schema:
ID Linkage Key
Name
Type
Size Value
Size Unit
Location (Full Address)
City
County
State
Country
PWSID/NPDES ID
Facility Name
CWS/WWTP (Level)
Numeric Value
Persons Served/MGD
Street Address, Zip Code
City Name
County Name
State Code
USA

Works cited
Water and Wastewater Systems | Cybersecurity and Infrastructure Security Agency CISA, accessed November 13, 2025, https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors/water-and-wastewater-sector
Safe Drinking Water Information System (SDWIS) Federal Reporting Services | US EPA, accessed November 13, 2025, https://www.epa.gov/ground-water-and-drinking-water/safe-drinking-water-information-system-sdwis-federal-reporting
Pollutant Loading Report Help - DMR | ECHO | US EPA, accessed November 13, 2025, https://echo.epa.gov/help/loading-tool/reports/pollutant-loading-report-help-dmr
SDWA Data Download Summary and Data Element Dictionary | ECHO | US EPA, accessed November 13, 2025, https://echo.epa.gov/tools/data-downloads/sdwa-download-summary
Data Downloads | US EPA, accessed November 13, 2025, https://www.epa.gov/enviro/data-downloads
Detailed Facility Report Data Dictionary | ECHO | US EPA, accessed November 13, 2025, https://echo.epa.gov/help/reports/dfr-data-dictionary
Custom Search Results Help | ECHO | US EPA, accessed November 13, 2025, https://echo.epa.gov/help/loading-tool/custom-search/custom-search-results-help
Column Name: PWS_TYPE_CODE - Envirofacts - Environmental Protection Agency, accessed November 13, 2025, https://enviro.epa.gov/enviro/EF_METADATA_HTML.sdwis_page?p_column_name=PWS_TYPE_CODE
Drinking Water Dashboard Help | ECHO | US EPA, accessed November 13, 2025, https://echo.epa.gov/help/drinking-water-qlik-dashboard-help
Types of Water Systems in Connecticut - CT.gov, accessed November 13, 2025, https://portal.ct.gov/dph/-/media/departments-and-agencies/dph/dph/drinking_water/pdf/types_of_water_systems.pdf
Public Water Systems - Ohio EPA, accessed November 13, 2025, https://epa.ohio.gov/divisions-and-offices/drinking-and-ground-waters/public-water-systems
Community Water System Service Area Boundaries | US EPA, accessed November 13, 2025, https://www.epa.gov/ground-water-and-drinking-water/community-water-system-service-area-boundaries
The Largest Advanced Wastewater Treatment Plant in the World - DC Water, accessed November 13, 2025, https://www.dcwater.com/about-dc-water/what-we-do/wastewater-treatment/blue-plains
Recommended Standards for Wastewater Facilities - Minnesota Department of Health, accessed November 13, 2025, https://www.health.state.mn.us/communities/environment/water/docs/tenstates/tenstatestan2014.pdf
Sources and Solutions: Wastewater | US EPA, accessed November 13, 2025, https://www.epa.gov/nutrientpollution/sources-and-solutions-wastewater
Capacity vs Flow | Florida Department of Environmental Protection, accessed November 13, 2025, https://floridadep.gov/water/domestic-wastewater/content/capacity-vs-flow
List of largest wastewater treatment plants - Wikipedia, accessed November 13, 2025, https://en.wikipedia.org/wiki/List_of_largest_wastewater_treatment_plants
Office of the Illinois State Fire Marshal UST Search: Facility Details for Stickney Water Reclamation Plant, accessed November 13, 2025, https://webapps.sfm.illinois.gov/ustsearch/Facility.aspx?ID=2035318
NCPC File No. 7267 DEWATERING BUILDING BLUE PLAINS ADVANCED WASTEWATER TREATMENT PLANT 5000 Overlook Avenue, SW Washington, D.C., accessed November 13, 2025, https://www.ncpc.gov/docs/actions/2011July/WASA_Dewatering_Building_Delegated_7267_July2011_.pdf
Connections Unit - Passaic Valley Sewerage Commission | What We Do, accessed November 13, 2025, https://www.nj.gov/pvsc/what/connect/
Driving directions to Passaic Valley Sewerage Commission, 600 Wilson Ave, Newark, accessed November 13, 2025, https://www.waze.com/live-map/directions/passaic-valley-sewerage-commission-wilson-ave-600-newark?to=place.w.187367831.1873416167.3907661
Wastewater Treatment Plants - IBWC, accessed November 13, 2025, https://www.ibwc.gov/wastewater-treatment-plants/
Blue Plains Advanced Wastewater Treatment Plant - Wikipedia, accessed November 13, 2025, https://en.wikipedia.org/wiki/Blue_Plains_Advanced_Wastewater_Treatment_Plant
One Water Spotlight: Stickney Water Reclamation Plant - US Water Alliance, accessed November 13, 2025, https://uswateralliance.org/resources/one-water-spotlight-stickney-water-reclamation-plant/
Driving directions to Stickney Water Reclamation Plant, W Pershing Rd, 6001, Cicero - Waze, accessed November 13, 2025, https://www.waze.com/el/live-map/directions/us/il/cicero/stickney-water-reclamation-plant?to=place.ChIJ0YMS8f4zDogRw8k7DoWslgU
National Primary Drinking Water Regulations | US EPA, accessed November 13, 2025, https://www.epa.gov/ground-water-and-drinking-water/national-primary-drinking-water-regulations
SDWIS -- List Validations By Element - Exchange Network, accessed November 13, 2025, http://www.exchangenetwork.net/schema/SDWA/2/ListValidationsByElement.pdf
