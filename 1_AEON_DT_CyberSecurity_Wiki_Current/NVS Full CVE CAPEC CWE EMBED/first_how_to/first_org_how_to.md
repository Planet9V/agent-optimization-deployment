verview
FIRST API is a simple way to query FIRST database in order to build web apps or integrate to other CSIRT databases. It currently doesn't support authentication, so only public information is available. One sample application is the Members around the world map.

This documentation refers to the FIRST API, which endpoint URL is be located at: https://api.first.org/data/v1.

Queries
The queries at FIRST APIs should follow this URL scheme:

[Endpoint URL][method][.format]?[parameters]
The Endpoint URL contains the collection and the version of the API under the endpoint. Current endpoints URL is:

Repository (sourcename)	Endpoint URL	Status
FIRST API v1	https://api.first.org/data/v1	Stable
In order to query FIRST API, use the following URL pattern:

https://api.first.org/data/v1[method][.format]?[parameters]
The available methods and parameters are described in this document.

Each method is an available dataset, like Teams, Countries, Events and so on. The URLs listed in this document are prefixed by the HTTP method required to use them, followed by the method address relative to the Endpoint URL. Take for example the teams listing, which uses the address GET /teams. It must be read as a GET request to the [Endpoint URL]/teams — to query FIRST API you should then use curl -X GET https://api.first.org/data/v1/teams.

The .format is optional, it's the content type expected for the response. The default output format is application/json. Additional formats (see table) are supported when properly requested. The output format should be requested either as a Accept: header or as an extension to the requested URL. These are the additional formats supported:

HTTP Accept	Extension	Format
application/json	.json (default)	JSON. This will be the format used if no extension or Accept: header is provided.
application/yaml	.yml	YAML, a more human-readable format. Applications should use two spaces as indentation and maximum column width of 80 characters.
application/xml	.xml	XML. Should not contain namespaces and different encodings.
application/csv	.csv	Comma-separated values. The first line contains the column names.
application/xls	.xls	Microsoft Excel format (legacy).
application/xlsx	.xlsx	Microsoft Excel 2007 and Excel 97/2000/XP/2003 binary file.
 
Please note: the API uses UTF8 as its encoding. This means that when importing this information in other applications, like spreadsheet applications, you must set the encoding to UTF8 (or Unicode if this one is missing).