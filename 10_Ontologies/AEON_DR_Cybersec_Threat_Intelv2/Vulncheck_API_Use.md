# API Overview

> All available v3 API resources

### Overview

VulnCheck API endpoints are optimized for programmatic access and deliver JSON machine-readable data.

[VulnCheck indices](https://docs.vulncheck.com/indices/intro) can be accessed using either the `backup` endpoint, which provides a complete copy of the index for download, or the `index` endpoint, which provides a paginated list of documents and can be used to query individual records.

A list of the 'index' and 'backup' API endpoints that you have access to, can be found in the [VulnCheck API Sandbox](https://vulncheck.com/api) located in the VulnCheck dashboard.

### First Steps

1. [Sign up for a VulnCheck Account](https://vulncheck.com/signin). This will give you immediate access to our [community resources](/community/vulncheck-kev/introduction).
2. Log into the [VulnCheck Dashboard](https://vulncheck.com/signin).
3. Click on the [API Sandbox](https://vulncheck.com/api) to explore the VulnCheck indexes that you have permission to access.
4. [Generate a token](https://vulncheck.com/settings/tokens) for programmatic API access.

### API Details

All API methods use [https://api.vulncheck.com/](https://api.vulncheck.com/) for the base URL.

<table>
<thead>
  <tr>
    <th>
      Method
    </th>
    
    <th>
      Name
    </th>
    
    <th>
      Description
    </th>
  </tr>
</thead>

<tbody>
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/indexes">
        /v3/index
      </a>
    </td>
    
    <td>
      Return a list of indexes with endpoint links
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/indice">
        /v3/index/{index}
      </a>
    </td>
    
    <td>
      Retrieve a paginated list of documents from the index of your choice
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/backups">
        /v3/backup
      </a>
    </td>
    
    <td>
      Return a list of backups with endpoint links
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/backup">
        /v3/backup/{index}
      </a>
    </td>
    
    <td>
      Request a link to the backup of an index
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/cpe">
        /v3/cpe
      </a>
    </td>
    
    <td>
      Request vulnerabilities related to a CPE
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/purl">
        /v3/purl
      </a>
    </td>
    
    <td>
      Request vulnerabilities related to a PURL
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/rules">
        /v3/rules/initial-access/{rules}
      </a>
    </td>
    
    <td>
      Request Initial Access Intelligence Suricata or Snort rules
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/tags">
        /v3/tags/{filter}
      </a>
    </td>
    
    <td>
      Return a list of newline-separated (or JSON) IP addresses based on a IP tag
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/pdns">
        /v3/pdns/{filter}
      </a>
    </td>
    
    <td>
      Return a list of newline-separated (or JSON) hostnames based on a hostname list for Protective DNS
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/openapi">
        /v3/openapi
      </a>
    </td>
    
    <td>
      Retrieve the current OpenAPI Specification (OAS)
    </td>
  </tr>
  
  <tr>
    <td>
      GET
    </td>
    
    <td>
      <a href="/api/search_cpe">
        /v3/search/cpe
      </a>
    </td>
    
    <td>
      Request vulnerabilities by CPE Part, Vendor, Product, and/or Version
    </td>
  </tr>
</tbody>
</table>

### API Example Request

<code-group>

```sh [curl]
curl --request GET \
    --url https://api.vulncheck.com/v3/backup/vulncheck-kev \
    --header 'Accept: application/json' \
    --header 'Authorization: Bearer insert_token_here'
```

```go [Go]
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "os"

    vulncheck "github.com/vulncheck-oss/sdk-go-v2/v2"
)

func main() {
    configuration := vulncheck.NewConfiguration()
    configuration.Scheme = "https"
    configuration.Host = "api.vulncheck.com"

    client := vulncheck.NewAPIClient(configuration)

    token := os.Getenv("VULNCHECK_API_TOKEN")
    auth := context.WithValue(
        context.Background(),
        vulncheck.ContextAPIKeys,
        map[string]vulncheck.APIKey{
            "Bearer": {Key: token},
        },
    )
    resp, httpRes, err := client.EndpointsAPI.BackupIndexGet(auth, "vulncheck-kev").Execute()

    if err != nil || httpRes.StatusCode != 200 {
        log.Fatal(err)
    }

    prettyJSON, err := json.MarshalIndent(resp.Data, "", "  ")
    if err != nil {
        log.Fatalf("Failed to generate JSON: %v", err)
        return
    }

    fmt.Println(string(prettyJSON))
}
```

```python [Python]
import vulncheck_sdk

configuration = vulncheck_sdk.Configuration(host="https://api.vulncheck.com/v3")
configuration.api_key["Bearer"] = "insert_token_here"

with vulncheck_sdk.ApiClient(configuration) as api_client:
    endpoints_client = vulncheck_sdk.EndpointsApi(api_client)

    api_response = endpoints_client.backup_index_get("vulncheck-kev")

    print(api_response.data[0].url)
```

```sh [CLI]
vulncheck backup download vulncheck-kev
```

</code-group>

## API Date Format

VulnCheck utilizes [RFC3339Nano](https://pkg.go.dev/time#pkg-constants) formatted dates across our datasets. This format has the peculiarity of removing trailing zeros from the seconds field, leading to slightly inconsistent timestamps. For example, both of the following are valid RFC3339Nano timestamps::

```text
2024-02-14T16:15:00Z
2024-02-23T10:38:41.361178Z
```

Although they appear inconsistent, they are both valid and parsable RFC3339Nano date formats.
