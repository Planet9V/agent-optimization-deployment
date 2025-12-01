# API / Schema

> Integrate with VulnCheck KEV using an open API / JSON schema that is easy to follow.

VulnCheck provides VulnCheck KEV as a Community service, helping provide timely visibility into known exploited vulnerabilities. The service is available using the VulnCheck community dashboard, API endpoint and machine readable JSON.

## VulnCheck KEV API

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

## JSON Schema

VulnCheck KEV has an easy to follow schema, which is made up of strings, arrays of strings, and times (as well as objects including these data types).

Included below is an example VulnCheck KEV record with every field filled out. Included further below are the data structures for parsing this JSON object in the Go programming language.

## Example VulnCheck KEV entry

Below is an example complete record for VulnCheck KEV, with all fields filled out.

```json
"data": [
    {
      "vendorProject": "PHP Group",
      "product": "PHP",
      "shortDescription": "PHP, specifically Windows-based PHP used in CGI mode, contains an OS command injection vulnerability that allows for arbitrary code execution. This vulnerability is a patch bypass for CVE-2012-1823.",
      "vulnerabilityName": "PHP-CGI OS Command Injection Vulnerability",
      "required_action": "Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.",
      "knownRansomwareCampaignUse": "Known",
      "cve": [
        "CVE-2024-4577"
      ],
      "cwes": [
        "CWE-78"
      ],
      "vulncheck_xdb": [
        {
          "xdb_id": "024996c990cc",
          "xdb_url": "https://vulncheck.com/xdb/024996c990cc",
          "date_added": "2025-02-14T19:38:10Z",
          "exploit_type": "initial-access",
          "clone_ssh_url": "git@github.com:Didarul342/CVE-2024-4577.git"
        },
        {
          "xdb_id": "081170ce66e7",
          "xdb_url": "https://vulncheck.com/xdb/081170ce66e7",
          "date_added": "2024-06-18T13:19:21Z",
          "exploit_type": "initial-access",
          "clone_ssh_url": "git@github.com:jakabakos/CVE-2024-4577-PHP-CGI-argument-injection-RCE.git"
        },
        {
          "xdb_id": "0b2ec7cacbad",
          "xdb_url": "https://vulncheck.com/xdb/0b2ec7cacbad",
          "date_added": "2024-07-11T02:22:32Z",
          "exploit_type": "initial-access",
          "clone_ssh_url": "git@github.com:bibo318/CVE-2024-4577-RCE-ATTACK.git"
        },
        {
          "xdb_id": "0c4b91081cb3",
          "xdb_url": "https://vulncheck.com/xdb/0c4b91081cb3",
          "date_added": "2023-01-13T08:18:15Z",
          "exploit_type": "initial-access",
          "clone_ssh_url": "git@github.com:0xPugal/my-nuclei-templates.git"
        },
        // ..
      ],
      "vulncheck_reported_exploitation": [
        {
          "url": "https://www.imperva.com/blog/imperva-protects-against-critical-php-vulnerability-cve-2024-4577/",
          "date_added": "2024-06-07T00:00:00Z"
        },
        {
          "url": "https://x.com/Shadowserver/status/1799053497490698548",
          "date_added": "2024-06-07T00:00:00Z"
        },
        {
          "url": "https://infosec.exchange/@ntkramer/112582375921224782",
          "date_added": "2024-06-08T00:00:00Z"
        },
        {
          "url": "https://isc.sans.edu/diary/Attacker%20Probing%20for%20New%20PHP%20Vulnerablity%20CVE-2024-4577/30994",
          "date_added": "2024-06-09T00:00:00Z"
        },
        {
          "url": "https://www.imperva.com/blog/update-cve-2024-4577-quickly-weaponized-to-distribute-tellyouthepass-ransomware/",
          "date_added": "2024-06-10T00:00:00Z"
        },
        {
          "url": "https://dashboard.shadowserver.org/statistics/honeypot/vulnerability/map/?day=2024-06-11&host_type=src&vulnerability=cve-2024-4577",
          "date_added": "2024-06-11T00:00:00Z"
        },
        {
          "url": "https://api.vulncheck.com/v3/index/vulncheck-canaries?cve=CVE-2024-4577&date=2025-10-21",
          "date_added": "2025-10-21T22:37:21Z"
        },
        {
          "url": "https://api.vulncheck.com/v3/index/vulncheck-canaries?cve=CVE-2024-4577&date=2025-10-22",
          "date_added": "2025-10-22T14:42:59Z"
          // ..
        }
      ],
      "reported_exploited_by_vulncheck_canaries": true,
      "dueDate": "2024-07-03T00:00:00Z",
      "cisa_date_added": "2024-06-12T00:00:00Z",
      "date_added": "2024-06-07T00:00:00Z",
      "_timestamp": "2025-10-22T17:27:39.163357849Z"
```

## Example data structures for VulnCheck KEV

Below are example data structures for marshalling or unmarshalling VulnCheck KEV data structures.

```go
type VulnCheckKEV struct {
    VendorProject              string `json:"vendorProject"`
    Product                    string `json:"product"`
    Description                string `json:"shortDescription"`
    Name                       string `json:"vulnerabilityName"`
    RequiredAction             string `json:"required_action"`
    KnownRansomwareCampaignUse string `json:"knownRansomwareCampaignUse"`

    CVE []string `json:"cve"`

    VulnCheckXDB                  []XDB             `json:"vulncheck_xdb"`
    VulnCheckReportedExploitation []ReportedExploit `json:"vulncheck_reported_exploitation"`

    ReportedExploitedByVulnCheckCanaries bool `json:"reported_exploited_by_vulncheck_canaries"`

    DueDate       *time.Time `json:"dueDate,omitempty"`
    CisaDateAdded *time.Time `json:"cisa_date_added,omitempty"`
    DateAdded     time.Time  `json:"date_added"`
}

type ReportedExploit struct {
    Url       string    `json:"url"`
    DateAdded time.Time `json:"date_added"`
}

type XDB struct {
    XDBID       string    `json:"xdb_id"`
    XDBURL      string    `json:"xdb_url"`
    DateAdded   time.Time `json:"date_added"`
    ExploitType string    `json:"exploit_type"`
    CloneSSHURL string    `json:"clone_ssh_url"`
}
```
