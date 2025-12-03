https://www.epa.gov/frs/frs-api

https://www.epa.gov/frs/frs-data-download-options

FRS Data Download Options
FRS data is available as Web Services, Prepackaged Downloads, and Custom Downloads.


Web Services
Resource Hyperlink	Resource Format	Public / Intranet	Description
FRS API	REST/JSON/JSONP/XML	Public	Public FRS API REST service to access FRS database tables from the FRS data model
Advanced Envirofacts API (example given)	CSV/Excel/REST/JSON/XML	Public	Advanced Envirofacts API that accesses FRS data

FRS Facilities Map Service	REST ArcGIS Map Service	Public	REST ArcGIS Map Service - several program interest layers; some include all facilities; others contain only “majors”.  Public version excludes sensitive data.
FRS ESF-10 Service	REST ArcGIS Map Service	Intranet	Emergency Response Map Service (Oil/Hazmat) - active facilities from RMP, Oil (FRP only), TRI, and RCRAInfo (TSD only).

FRS ESF-3 Service	REST ArcGIS Map Service	Intranet	Emergency Response Map Service (Public Works) - active waste water treatment plants from NPDES and non-transient drinking water facilities from SDWIS
FRS FacID 3.0 Service	SOAP/XML	Public	Exchange Network Facility Data Flow (current version)
Intergovernmental Facility Registry Service (FRS) API	REST/JSON	Public	Intergovernmental FRS API exposes several RESTful web services for querying and submitting data with FRS - requires authentication



FRS API
The FRS API exposes several REST services that allows developers to utilize a live feed of data from the FRS database. This web page is intended for a technical audience and describes the content and purpose of each service available. This is a collection of query-only or GET web services, that are available through a simple URL http link and provide output in either XML, JSON, or JSONP formats. 

Currently three services are available:
 
get_facilities
get_facilities_wbd
get_cd_11
See the FRS API description below or reference the FRS API Documentation.

get_facilities Service Specifications
get_facilities provides multiple selection criteria against FRS Facilities Data and their associated Program Facility Data.
Selection Criteria
Outputs
Example
Selection Criteria
Of the selection criteria listed below, those that have an Equal value under the Search Operator column will provide the best performance.  Examples are provided at the end of the section to illustrate how selection criteria can be combined.

Search Term	Variable Name	Search Operator	Other
Facility Registry Id	registry_id	Equal, Optional	 
FRS Facility Name	facility_name	Contains, Optional	Full text search on Program Name
Program Facility Name	program_name	Contains, Optional	Full text search on Program Name
Street Address	street_address	Contains, Optional	
Because of the many variabilities involved with street address it is hard to use an address as a search criteria. May be able to provide an address parser to validate address if needed.  Suggest you limit to street base name if you want to do a search on street address.

City	city_name	Equal, Optional	 
County	county_name	Equal, Optional	 
Zip Code	zip_code	Equal, Optional	Will use only first 5 digits of zip code only
State Abbreviation	state_abbr	Equal, Optional	 
Program Acronym	pgm_sys_acrnm	Equal, Optional	See Appendix A for list of  Acronyms
Program System Id	pgm_sys_id	Equal, Optional	 
Program Output	program_output	Yes/No, Optional	Default is no.  Controls whether or not the Program Facility object is output
Output Format	output	XML, JSON, JSONP Optional	Default is XML.
Call back JSONP Function	callback	Optional	Default is callback.  Can only be used when the output value is JSONP
Latitude (NAD83)	latitude83	Equal, Optional	The latitude coordinate, in decimal degrees format, using the US Standard NAD83 horizontal Datum.  Used in conjunction with Search Radius and Longitude (NAD83) to restrict facility selection to a spatial circle of the provide search radius around the provided spatial coordinate.  All 3 selection criteria  are required.
Longitude (NAD83)	longitude83	Equal, Optional	The longitude coordinate, in decimal degrees format, using the US Standard NAD83 horizontal datum.  See Latitude (NAD83) description.
Search Radius (Miles)	search_radius	Maximum, Optional	The maximum search radius is 25 miles.  See Latitude (NAD83).
Coordinates Output	coordinates_output	Yes/No, Optional	A value of "Yes" will output all associated program coordinates for the facilities returned by the query.
Outputs
An XML, JSON, or JSONP formatted document with the following output:
For each facility returned there will be a FRS Facility complex object comprised of the following simple and complex objects.

Object Name	Object Type
RegistryId	Simple
FacilityName	Simple
LocationAddress	Simple
SupplementalLocation	Simple
CityName	Simple
CountyName	Simple
StateAbbr	Simple
ZipCode	Simple
FIPSCode	Simple
Latitude83	Simple
Longitude83	Simple
ProgramFacilities	Complex (optional output)
Program Facility	Complex (child of ProgramFacilities – one for each program facility comprised of the following simple elements listed below.
ProgramSystemAcronym	Simple
ProgramSystemId	Simple
ProgramFacilityName	Simple
ProgramCoordinates	Complex (optional output)
ProgramCoordinate	Complex (optional output). Complex (child of ProgramCoordinates) – one for each program coordinate comprised of the following simple elements listed below. Data element definitions can be found in the V_GEO_PGM_COORDINATE_ALL view of the FRS Geospatial Data model at FRS Geospatial Data Model
ProgramSystemAcronym	Simple
ProgramSystemI	Simple
SubId	Simple
ObjectId	Simple
Latitude83	Simple
Longitude83	Simple
HDatum	Simple
BestPick	Simple
CollectionMethod	Simple
AccuracyValue	Simple
AccuracyScore	Simple
ReferencePoint	Simple
DerivedCity	Simple
DerivedCounty	Simple
DerivedZip	Simple
DerivedWBD	Simple
DerivedCB2010	Simple
DerivedCD112	Simple
MetersToBP	Simple - the distance in Meters from the program coordinate to the Best Pick Coordinate
Example
URL for Facility Name Search containing “Mobil Oil” in State of Virginia, City of Newport News
https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?state_abbr=VA&city_name=Newport%20News&facility_name=mobil%20oil

URL for searching SEMS (Superfund) facilities in zip code 60085, with the Program Facility Output turned on and JSON output.

https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?pgm_sys_acrnm=SEMS&zip_code=60085&program_output=yes&output=JSON

URL for searching SEMS (Superfund) facilities within a 3 mile radius of latitude 38.8/longitude -77.01. 
https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?latitude83=38.8&longitude83=-77.01&search_radius=3&pgm_sys_acrnm=SEMS&output=JSON

get_facilities_wbd Service Specifications
get_facilities_wbd returns USGS Watershed Boundary Dataset information for a passed FRS Facility or Program Facility Identifier.
Selection Criteria
Outputs
Example
Selection Criteria
Of the selection criteria listed below, those that have an “Equal” value under the Search Operator column will provide the best performance.  Examples are provided at the end of the section to illustrate how selection criteria can be combined.

Search Term	Variable Name	Search Operator	Other
Registry ID	registry_id	Equal, Optional	The facility’s FRS Registry ID
Program Acronym	pgm_sys_acrnm	Equal, Optional	See Appendix A for list of  Acronyms
Program System ID	pgm_sys_id	Equal, Optional	The program facility system identifier
Outputs
An XML, JSON, or JSONP formatted document with the following output:

Object Name	Object Type	Comments
RegistryId	Simple	The facility’s FRS Registry Identifier
Chesapeake Bay	Simple	A Y value indicates the facility is within the Chesapeake Bay watershed
Region Complex	Complex	Lists the HUC 2 USGS Hydroregion number and name for the facility
Subregion	Complex	Lists the HUC 4 USGS Sub-hydroregion number and name for the facility
Basin Complex	Complex	Lists the HUC 6 USGS Basin number and name for the facility
Subbasin	Complex	Lists the HUC 8 USGS Sub-basin number and name for the facility
Watershed	Complex	Lists the HUC 10 USGS Watershed number and name for the facility
Subwatershed	Complex	Lists the HUC 12 USGS Sub-watershed number and name for the facility
Example
URL for a FRS Registry ID
https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facility_wbd?registry_id=110015778176


Appendix A
PGM_SYS_ACRNM	PGM_SYS_ACRNM
ACES	MD-RCRA
ACRES	MD-TEMPO
AIRS/AFS	ME-EFIS
AIRS/AQS	MI-DEQ
AZURITE	MN-DELTA
BIA INDIAN SCHOOL	MO-DNR
BR	MS-ENSITE
BRAC	MT-CEDARS
CA-CERS	NCDB
CA-ENVIROVIEW	NC-FITS
CAMDBS	NDEQ
CASWIS	ND-FP
CDAFLP	NEI
CEDRI	NH-DES
CEDS	NJ-NJEMS
CIM	NM-TEMPO
CNFRS	NNEMS
CWNS	NPDES
DEN	NV-FP
DTSC-ENVIROSTOR	OH-CORE
ECOMAP	OR-DEQ
ECRM	OSHA-OIS
E-GGRT	OTAQREG
EGRID	PA-EFACTS
EIA-860	PDS
EIS	PERMIT TRACKING
EPS	RADINFO
FARR	RBLC
FDM	RCRAINFO
FFDOCKET	REGION
FFEP	RFS
FIS	RI-PLOVER
GEIMS	RMP
HI-EHW	SC-EFIS
HWTS-DATAMART	SEMS
ICIS	SFDW
IDDEQ	SIMS
IDNR_EFD	SRPMICEMS
IN-FRS	SSTS
IN-TEMPO	STATE
ISD	SWIPR
KS-FP	TRIS
KY-TEMPO	TSCA
LA-TEMPO	TX-TCEQ ACR
LMOP	UORS
LUST-ARRA	UST
MA-EPICS	WA-FSIS
MD-EPSC	WI-ESR
MD-PEMIS	 
get_cd_111 Service Specifications
get_cd_111 returns the 111th Congress Identifier based on passed latitude/longitude geographic coordinates.
Selection Criteria
Outputs
Example
Selection Criteria
Of the selection criteria listed below, those that have an "Equal" value under the Search Operator column will provide the best performance.  Examples are provided at the end of the section to illustrate how selection criteria can be combined.

Latitude	latitude	Equals, Required	In decimal degrees
Latitude	latitude	Equal, Optional	In decimal degrees
Longitude	longitude	Equals, Required	In decimal degrees
Horizontal Datum	hdatum	Equal, Optional	Default is NAD83, WGS84 is also accepted
Outputs
An XML, JSON, or JSONP formatted document with the following output:

Object Name	Object Type	Comment
State	Simple	 
CD	Simple	Congressional District Number
CDName	Simple	Congressional District Name
Example
Example URL
https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_cd_111?latitude=38.8&longitude=-77.01&hdatum=wgs84

Facility Registry Service (FRS)
FRS Home
FRS Description

Search for FRS data

Facility Linkage Application (FLA)

Contact Us About FRS
Last updated on September 5, 2025