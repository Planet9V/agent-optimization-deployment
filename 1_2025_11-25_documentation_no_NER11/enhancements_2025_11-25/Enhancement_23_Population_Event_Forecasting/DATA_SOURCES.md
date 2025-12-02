# Enhancement E23: Data Sources for Population-Level Event Forecasting

**File:** DATA_SOURCES.md
**Created:** 2025-11-26 12:00:00 UTC
**Version:** v1.0.0
**Author:** Research Analysis Agent
**Purpose:** Comprehensive catalog of data sources for population-scale cybersecurity forecasting
**Status:** ACTIVE

## Executive Summary

Population-level cybersecurity forecasting requires diverse data spanning demographics, economics, news sentiment, social media, technology adoption, and cultural factors. This document catalogs primary and secondary data sources, access methods, update frequencies, and integration strategies for the 10-agent forecasting swarm.

---

## 1. Demographic Data Sources

### US Census Bureau
```yaml
Official_Name: "United States Census Bureau"
Website: "https://www.census.gov/"
API_Endpoint: "https://api.census.gov/data"
Authentication: "API key (free registration)"

Datasets:
  American_Community_Survey_5Year:
    coverage: "Detailed demographics for all US geographies"
    variables:
      - "B01001: Age and Sex"
      - "B15003: Educational Attainment"
      - "B19013: Median Household Income"
      - "B23025: Employment Status"
      - "C24030: Occupation by Sex"
      - "C24050: Industry by Class of Worker"
    granularity: "Nation, State, County, Metro Area, Zip Code"
    update_frequency: "Annual (1-year lag)"
    api_rate_limit: "Unlimited (with key)"

  Population_Estimates_Program:
    coverage: "Current population estimates and projections"
    variables:
      - "PEP: Population Estimates"
      - "Age distribution by single year"
      - "Race and Hispanic origin"
    update_frequency: "Annual (July release)"

Integration_Code:
python: |
  import requests

  API_KEY = os.getenv('CENSUS_API_KEY')
  BASE_URL = 'https://api.census.gov/data'

  def fetch_demographics(year, geography, variables):
      url = f"{BASE_URL}/{year}/acs/acs5"
      params = {
          'get': ','.join(variables),
          'for': geography,
          'key': API_KEY
      }
      response = requests.get(url, params=params)
      return response.json()

  # Example: Fetch age and education for all states
  data = fetch_demographics(
      year=2022,
      geography='state:*',
      variables=['NAME', 'B01001_001E', 'B15003_001E']
  )

Licensing: "Public domain (US government data)"
Cost: "Free"
```

### Pew Research Center - Technology Surveys
```yaml
Official_Name: "Pew Research Center"
Website: "https://www.pewresearch.org/internet/"
Access: "Downloadable datasets (registration required)"

Datasets:
  Technology_Adoption:
    focus: "Device ownership and internet usage by demographic"
    surveys:
      - "Mobile Technology and Home Broadband 2024"
      - "Social Media Use 2024"
      - "Americans and Privacy 2023"
    variables:
      - "Smartphone ownership by age, income, education"
      - "Social media platform usage"
      - "Privacy concerns and practices"
      - "Cybersecurity awareness"
    sample_size: "~3,000-10,000 US adults per survey"
    update_frequency: "Quarterly to annually"

Integration_Method:
  - Manual download of CSV/SPSS files
  - Parse into structured format for Neo4j ingestion
  - Cross-reference with Census demographics

Licensing: "Free for research use (citation required)"
Cost: "Free"
```

### OECD Data (International Demographics)
```yaml
Official_Name: "Organisation for Economic Co-operation and Development"
Website: "https://data.oecd.org/"
API: "OECD.Stat API (REST)"

Datasets:
  Population_Statistics:
    coverage: "38 OECD member countries + partners"
    variables:
      - "Population by age and sex"
      - "Labor force participation"
      - "Educational attainment"
      - "Income distribution"
    update_frequency: "Annual"

  Digital_Economy_Outlook:
    variables:
      - "Internet access by household"
      - "ICT infrastructure"
      - "Digital skills"
    update_frequency: "Biennial"

Integration_Code:
python: |
  from pandasdmx import Request

  oecd = Request('OECD')

  # Fetch population data
  data = oecd.data('POP_PROJ', key={'COUNTRY': 'USA+CAN+MEX', 'AGE': '15-64'})
  df = data.to_pandas()

Licensing: "Creative Commons BY 4.0"
Cost: "Free"
```

---

## 2. News and Event Data

### GDELT (Global Database of Events, Language, and Tone)
```yaml
Official_Name: "GDELT Project"
Website: "https://www.gdeltproject.org/"
Access: "Google BigQuery public dataset"

Datasets:
  GDELT_Events_2.0:
    coverage: "Global news events from 100+ languages, 1979-present"
    update_frequency: "Every 15 minutes"
    records: "300+ million events"

    cyber_event_codes:
      - "1723: Cyberattack, hack, compromise"
      - "1724: Data breach, information theft"
      - "1725: Ransomware attack"
      - "1726: DDoS attack"
      - "1727: Supply chain compromise"

    fields:
      - "SQLDATE: Event date"
      - "Actor1Name, Actor2Name: Entities involved"
      - "EventCode: CAMEO event classification"
      - "GoldsteinScale: Conflict-cooperation scale (-10 to +10)"
      - "AvgTone: Average sentiment (-100 to +100)"
      - "ActionGeo_FullName: Location"
      - "SOURCEURL: Original article URL"

Integration_Code:
python: |
  from google.cloud import bigquery

  client = bigquery.Client()

  query = """
  SELECT SQLDATE, Actor1Name, Actor2Name, EventCode, AvgTone, SOURCEURL
  FROM `gdelt-bq.gdeltv2.events`
  WHERE SQLDATE BETWEEN '20240101' AND '20241231'
    AND EventCode IN ('1723', '1724', '1725', '1726', '1727')
  LIMIT 10000
  """

  df = client.query(query).to_dataframe()

Licensing: "Open access"
Cost: "Free (BigQuery query costs apply after 1TB/month)"
```

### NewsAPI
```yaml
Official_Name: "NewsAPI.org"
Website: "https://newsapi.org/"
API: "REST API"

Coverage:
  - "70,000+ news sources"
  - "15 languages"
  - "Search historical articles (up to 1 month)"

Endpoints:
  Everything:
    purpose: "Search all articles"
    parameters:
      - "q: Search keywords (e.g., 'cybersecurity breach')"
      - "sources: Specific news outlets"
      - "language: Filter by language"
      - "from/to: Date range"
    rate_limit: "1,000 requests/day (developer), 250/day (free)"

  Top_Headlines:
    purpose: "Latest breaking news"
    parameters:
      - "category: Technology, Business"
      - "country: US, GB, etc."

Integration_Code:
python: |
  import requests

  API_KEY = os.getenv('NEWSAPI_KEY')
  url = 'https://newsapi.org/v2/everything'

  params = {
      'q': 'ransomware OR data breach',
      'language': 'en',
      'sortBy': 'publishedAt',
      'apiKey': API_KEY
  }

  response = requests.get(url, params=params)
  articles = response.json()['articles']

Licensing: "Commercial use requires paid plan"
Cost: "Free (250 req/day), Developer ($449/mo for 250K req/mo)"
```

---

## 3. Social Media Data

### Twitter API v2
```yaml
Official_Name: "Twitter (X) API"
Website: "https://developer.twitter.com/"
API: "REST API v2"

Access_Tiers:
  Free:
    rate_limit: "1,500 tweets/month"
    endpoints: "Recent search (7 days)"

  Basic:
    cost: "$100/month"
    rate_limit: "10,000 tweets/month"
    endpoints: "Recent search (7 days)"

  Pro:
    cost: "$5,000/month"
    rate_limit: "1,000,000 tweets/month"
    endpoints: "Full archive search, streaming"

Endpoints:
  Search_Recent_Tweets:
    url: "https://api.twitter.com/2/tweets/search/recent"
    query_operators:
      - "#databreach: Hashtag search"
      - "from:username: Tweets from specific account"
      - "0day OR zeroday: Keyword search"
      - "-is:retweet: Exclude retweets"
    fields: "created_at, author_id, public_metrics, entities"

Integration_Code:
python: |
  import tweepy

  client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

  query = "(#databreach OR #ransomware OR #0day) -is:retweet"
  tweets = client.search_recent_tweets(
      query=query,
      max_results=100,
      tweet_fields=['created_at', 'author_id', 'public_metrics']
  )

  for tweet in tweets.data:
      print(tweet.text)

Licensing: "Commercial use allowed"
Cost: "Free to $5,000/month depending on volume"
```

### Reddit API (PRAW - Python Reddit API Wrapper)
```yaml
Official_Name: "Reddit API"
Website: "https://www.reddit.com/dev/api/"
Wrapper: "PRAW (https://praw.readthedocs.io/)"

Access:
  authentication: "OAuth2 (client ID + secret)"
  rate_limit: "60 requests/minute"

Relevant_Subreddits:
  - "r/cybersecurity (1.5M members)"
  - "r/netsec (1.1M members)"
  - "r/hacking (730K members)"
  - "r/AskNetsec (150K members)"
  - "r/blueteamsec (80K members)"

Integration_Code:
python: |
  import praw

  reddit = praw.Reddit(
      client_id=os.getenv('REDDIT_CLIENT_ID'),
      client_secret=os.getenv('REDDIT_SECRET'),
      user_agent='PopulationForecaster/1.0'
  )

  subreddit = reddit.subreddit('cybersecurity')
  for post in subreddit.new(limit=100):
      if 'breach' in post.title.lower():
          print(post.title, post.score, post.num_comments)

Licensing: "Free for non-commercial use"
Cost: "Free"
```

---

## 4. Economic Indicators

### Bureau of Labor Statistics (BLS)
```yaml
Official_Name: "US Bureau of Labor Statistics"
Website: "https://www.bls.gov/"
API: "BLS Public Data API"

Datasets:
  Local_Area_Unemployment_Statistics:
    series_prefix: "LAU"
    coverage: "States, metro areas, counties"
    variables:
      - "Unemployment rate"
      - "Labor force participation"
      - "Employment level"
    update_frequency: "Monthly"

  Current_Employment_Statistics:
    series_prefix: "CE"
    coverage: "Employment by industry"
    variables:
      - "Nonfarm payroll by sector"
      - "Average hourly earnings"
    update_frequency: "Monthly"

Integration_Code:
python: |
  import requests

  API_KEY = os.getenv('BLS_API_KEY')
  url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

  series_ids = ['LAUMT060606000000003']  # Example: NY metro unemployment

  payload = {
      'seriesid': series_ids,
      'startyear': '2020',
      'endyear': '2024',
      'registrationkey': API_KEY
  }

  response = requests.post(url, json=payload)
  data = response.json()

Licensing: "Public domain"
Cost: "Free"
```

### Federal Reserve Economic Data (FRED)
```yaml
Official_Name: "Federal Reserve Bank of St. Louis"
Website: "https://fred.stlouisfed.org/"
API: "FRED API"

Datasets:
  Interest_Rates:
    - "FEDFUNDS: Federal funds rate"
    - "MORTGAGE30US: 30-year mortgage rate"

  Economic_Indicators:
    - "GDP: Gross Domestic Product"
    - "CPIAUCSL: Consumer Price Index (inflation)"
    - "UMCSENT: University of Michigan Consumer Sentiment"

Integration_Code:
python: |
  from fredapi import Fred

  fred = Fred(api_key=os.getenv('FRED_API_KEY'))

  unemployment = fred.get_series('UNRATE')  # US unemployment rate
  inflation = fred.get_series('CPIAUCSL')

Licensing: "Public domain"
Cost: "Free"
```

---

## 5. Technology and Cybersecurity Data

### CVE Database (NVD)
```yaml
Official_Name: "National Vulnerability Database"
Website: "https://nvd.nist.gov/"
API: "NVD REST API 2.0"

Data:
  CVE_Records:
    fields:
      - "CVE ID"
      - "Published date"
      - "CVSS score and severity"
      - "Affected products (CPE)"
      - "Vulnerability type (CWE)"
    update_frequency: "Real-time"

Integration_Code:
python: |
  import requests

  url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
  params = {
      'pubStartDate': '2024-01-01T00:00:00.000',
      'pubEndDate': '2024-12-31T23:59:59.999'
  }

  response = requests.get(url, params=params)
  cves = response.json()['vulnerabilities']

Licensing: "Public domain"
Cost: "Free"
Rate_Limit: "5 requests per 30 seconds (without API key), 50/30s (with key)"
```

### MITRE ATT&CK
```yaml
Official_Name: "MITRE ATT&CK Framework"
Website: "https://attack.mitre.org/"
Access: "STIX/TAXII server, GitHub repo"

Data:
  Techniques:
    - "14 tactics (e.g., Initial Access, Execution)"
    - "200+ techniques and sub-techniques"
    - "Mappings to threat groups and software"

  Threat_Groups:
    - "140+ tracked APT groups"
    - "Techniques used by each group"

Integration:
python: |
  from stix2 import TAXIICollectionSource, Filter
  from taxii2client.v20 import Server

  server = Server('https://cti-taxii.mitre.org/taxii/')
  api_root = server.api_roots[0]
  collection = api_root.collections[0]

  tc_source = TAXIICollectionSource(collection)
  attack_patterns = tc_source.query([Filter('type', '=', 'attack-pattern')])

Licensing: "Apache 2.0 (free for any use)"
Cost: "Free"
```

---

## 6. Cultural and Behavioral Data

### Hofstede Insights
```yaml
Official_Name: "Hofstede Insights - National Culture Dimensions"
Website: "https://www.hofstede-insights.com/"
Access: "Country comparison tool (web), dataset purchase"

Dimensions:
  - "Power Distance Index (PDI)"
  - "Individualism vs Collectivism (IDV)"
  - "Masculinity vs Femininity (MAS)"
  - "Uncertainty Avoidance Index (UAI)"
  - "Long-term Orientation (LTO)"
  - "Indulgence vs Restraint (IND)"

Coverage: "100+ countries"

Integration:
  - Manual data entry from published scores
  - Academic dataset access via research agreement

Licensing: "Commercial use requires license"
Cost: "Free (comparison tool), Contact for dataset pricing"
```

---

## 7. Cryptocurrency Data (Ransomware Payment Tracking)

### CoinGecko API
```yaml
Official_Name: "CoinGecko"
Website: "https://www.coingecko.com/"
API: "CoinGecko API v3"

Data:
  Price_History:
    cryptocurrencies: "Bitcoin, Ethereum, Monero, etc."
    fields:
      - "Price (USD)"
      - "Market cap"
      - "Trading volume"
    granularity: "Daily, hourly, minute"

Integration_Code:
python: |
  import requests

  url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
  params = {
      'vs_currency': 'usd',
      'days': '90'
  }

  response = requests.get(url, params=params)
  prices = response.json()['prices']

Licensing: "Free tier for non-commercial use"
Cost: "Free (50 calls/min), Pro ($129/mo for higher limits)"
```

---

## Data Integration Architecture

### ETL Pipeline
```yaml
Extract:
  - API clients for each data source
  - Error handling and rate limit respect
  - Caching layer (Redis) for frequently accessed data

Transform:
  - Normalize schemas to common format
  - Geocode and standardize location data
  - Time zone conversion to UTC
  - Data validation and cleaning

Load:
  - Neo4j graph database (primary storage)
  - PostgreSQL (time-series data)
  - Redis (real-time cache)
```

### Update Schedule
```yaml
Real-Time (15-min):
  - GDELT events
  - Twitter mentions

Hourly:
  - Reddit posts
  - Cryptocurrency prices

Daily:
  - NewsAPI articles
  - CVE database

Weekly:
  - Social media sentiment aggregation

Monthly:
  - BLS unemployment
  - Economic indicators

Annually:
  - Census demographics
  - Hofstede cultural data
```

---

## Data Quality and Reliability

### Source Credibility Tiers
```yaml
Tier_1 (Highest):
  - US Census Bureau
  - Bureau of Labor Statistics
  - National Vulnerability Database
  - MITRE ATT&CK

Tier_2:
  - GDELT Project
  - Federal Reserve Economic Data
  - OECD Statistics
  - Pew Research

Tier_3:
  - NewsAPI (curated sources)
  - Twitter (verified accounts)
  - Reddit (moderated subreddits)

Tier_4 (Use with caution):
  - Cryptocurrency market data (volatility)
  - Dark web forums (legal and ethical constraints)
```

### Validation Methods
- Cross-reference multiple sources for critical data
- Statistical outlier detection
- Time-series consistency checks
- Manual spot-checks by Agent 10 (Quality Validator)

---

## Legal and Ethical Considerations

### Compliance
- **Terms of Service:** All API usage complies with provider ToS
- **Rate Limits:** Respect rate limits; implement backoff strategies
- **Attribution:** Cite data sources in reports and publications

### Privacy
- **Aggregate-Only Analysis:** No individual-level tracking
- **Anonymization:** Remove personally identifiable information
- **GDPR/CCPA:** Ensure compliance for international data

### Ethical Constraints
- **Dark Web Forums:** Read-only access, no interaction
- **Social Media:** Public posts only, no private messages
- **Responsible Disclosure:** Report critical vulnerabilities found

---

## Cost Estimate

```yaml
Monthly_Costs:
  Census_API: $0
  GDELT_BigQuery: $20 (estimated query costs)
  NewsAPI_Developer: $449
  Twitter_Basic: $100
  Reddit_API: $0
  BLS_API: $0
  FRED_API: $0
  NVD_API: $0
  CoinGecko_Pro: $129

Total_Monthly: ~$698
Annual_Budget: ~$8,376

Notes:
  - Costs scalable based on query volume
  - Academic/research discounts may apply
  - Open-source alternatives available for most sources
```

---

## Conclusion

This comprehensive data infrastructure supports population-level cybersecurity forecasting by integrating demographics, economics, news, social media, technology trends, and cultural factors. The multi-source approach ensures robustness, with redundancy to handle individual source failures.

**Key Principle:** Diverse data → Robust predictions. No single source can capture population dynamics; synthesis across domains is essential.

---

**References:**
1. US Census Bureau. (2024). American Community Survey 5-Year Data. https://www.census.gov/programs-surveys/acs
2. Leetaru, K., & Schrodt, P. A. (2013). GDELT: Global Data on Events, Location, and Tone. ISA Annual Convention.
3. NIST. (2024). National Vulnerability Database. https://nvd.nist.gov/
4. MITRE Corporation. (2024). ATT&CK Framework. https://attack.mitre.org/
5. Hofstede, G. (2001). Culture's Consequences (2nd ed.). SAGE Publications.

---

*Enhancement E23: Data Sources | v1.0.0 | Population Forecasting Infrastructure*
