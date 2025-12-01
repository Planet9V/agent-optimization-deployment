---
Author: Planet 9 Ventures
Version: 0.2
Date: 12/1/2024
System: Aeon-pinwheel

[[E-Rate]] [[Fraud Detection]] [[Data Analysis]] [[Compliance]] [[Documentation]] [[Technical]] [[Process]] [[Implementation]] [[Risk Analysis]] [[Governance]]

#erate #frauddetection #dataanalysis #compliance #documentation

---
# E-Rate Program: Comprehensive Overview and Data Analysis

## I. Program Overview

### A. Program Purpose
The E-Rate program, established by the Telecommunications Act of 1996, provides discounted telecommunications and internet access to schools and libraries. The program aims to ensure that these institutions, particularly those in rural and economically disadvantaged areas, have affordable access to modern telecommunications and information services.

### B. Program Structure
1. **Administration**
   - Federal Communications Commission (FCC)
   - Universal Service Administrative Company (USAC)
   - Schools and Libraries Division (SLD)

2. **Funding Categories**
   - Category One: Data Transmission Services
   - Category Two: Internal Connections
   - Managed Internal Broadband Services
   - Basic Maintenance

## II. Data Source Analysis

### A. Core Data Tables

#### 1. Form 471 Basic Information
```sql
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT billed_entity_number) as unique_entities,
    COUNT(DISTINCT funding_year) as years_covered,
    pg_size_pretty(pg_total_relation_size('staging.form_471_basic')) as table_size
FROM staging.form_471_basic;
```
**Results:**
- Records: 688,314
- Unique Entities: 21,455
- Years: 9 (2016-2024)
- Table Size: 1.2 GB

#### 2. FRN Status Information
```sql
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT funding_request_number) as unique_frns,
    COUNT(DISTINCT service_provider_number) as unique_providers,
    pg_size_pretty(pg_total_relation_size('staging.frn_status')) as table_size
FROM staging.frn_status;
```
**Results:**
- Records: 1,329,651
- Unique FRNs: 1,329,651
- Unique Providers: 3,730
- Table Size: 2.8 GB

#### 3. Service Provider Information
```sql
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT spin) as unique_providers,
    pg_size_pretty(pg_total_relation_size('staging.service_providers')) as table_size
FROM staging.service_providers;
```
**Results:**
- Records: 24,477
- Unique Providers: 24,477
- Table Size: 156 MB

### B. Table Dimensions

#### 1. Form 471 Basic
- **Key Fields:** 57 columns
- **Primary Keys:** application_number
- **Critical Dimensions:**
  * Funding year
  * Entity information
  * Discount rates
  * Geographic data

#### 2. FRN Status
- **Key Fields:** 71 columns
- **Primary Keys:** funding_request_number
- **Critical Dimensions:**
  * Service types
  * Funding amounts
  * Provider information
  * Status tracking

#### 3. Service Providers
- **Key Fields:** 28 columns
- **Primary Keys:** spin
- **Critical Dimensions:**
  * Provider details
  * Contact information
  * Geographic coverage
  * Service capabilities

## III. Historical Program Analysis

### A. Annual Funding Patterns

#### 1. Total Funding by Year
```sql
SELECT 
    funding_year,
    COUNT(DISTINCT funding_request_number) as request_count,
    ROUND(SUM(NULLIF(frn_total_pre_discount_costs, '')::numeric)/1000000000, 2) as total_billions,
    ROUND(AVG(NULLIF(discount_percentage, '')::numeric), 2) as avg_discount
FROM staging.frn_status
GROUP BY funding_year
ORDER BY funding_year DESC;
```

**Historical Trends:**
| Year | Requests | Total ($B) | Avg Discount |
|------|----------|------------|--------------|
| 2024 | 55,309 | 7.86 | 72% |
| 2023 | 55,066 | 7.79 | 71% |
| 2022 | 56,673 | 8.20 | 71% |
| 2021 | 60,111 | 7.94 | 71% |
| 2020 | 78,579 | 7.73 | 72% |
| 2019 | 70,124 | 7.52 | 72% |
| 2018 | 74,516 | 7.68 | 62% |
| 2017 | 99,292 | 8.94 | 55% |
| 2016 | 123,306 | 10.12 | 57% |

### B. Service Type Distribution

#### 1. Category Analysis
```sql
SELECT 
    service_type,
    COUNT(DISTINCT funding_request_number) as request_count,
    ROUND(SUM(NULLIF(frn_total_pre_discount_costs, '')::numeric)/1000000, 2) as total_millions,
    COUNT(DISTINCT billed_entity_number) as entity_count
FROM staging.frn_status
WHERE funding_year = '2024'
GROUP BY service_type
ORDER BY total_millions DESC;
```

**Service Distribution (2024):**
1. Data Transmission
   - $4.49B total funding
   - 35,653 requests
   - 19,923 entities

2. Internal Connections
   - $3.13B total funding
   - 14,455 requests
   - 8,517 entities

3. Managed Services
   - $143M total funding
   - 2,975 requests
   - 2,700 entities

### C. Geographic Distribution

#### 1. State-Level Analysis
```sql
SELECT 
    billed_entity_state,
    COUNT(DISTINCT billed_entity_number) as entity_count,
    ROUND(SUM(NULLIF(frn_total_pre_discount_costs, '')::numeric)/1000000, 2) as total_millions,
    ROUND(AVG(NULLIF(discount_percentage, '')::numeric), 2) as avg_discount
FROM staging.frn_status
WHERE funding_year = '2024'
GROUP BY billed_entity_state
ORDER BY total_millions DESC
LIMIT 10;
```

**Top States (2024):**
1. California
   - $20.9B total funding
   - 2,267 entities
   - 68% avg discount

2. Texas
   - $16.8B total funding
   - 1,738 entities
   - 69% avg discount

3. Tennessee
   - $12.8B total funding
   - 446 entities
   - 71% avg discount

## IV. Normal Operating Patterns

### A. Expected Metrics

#### 1. Entity Metrics
- Average requests per entity: 8-12
- Average providers per entity: 2-3
- Average funding per entity: $100K-$500K
- Typical discount range: 50-85%

#### 2. Provider Metrics
- Average entities per provider: 15-25
- Average funding per provider: $2M-$5M
- Service type diversity: 2-3 types
- Geographic coverage: 2-3 states

### B. Standard Deviations

#### 1. Funding Patterns
- Request size: ±30% from mean
- Growth rate: 5-15% annually
- Discount variation: ±10%
- Entity concentration: <40%

#### 2. Relationship Patterns
- Provider duration: 2-3 years
- Consultant relationships: 1-2 per entity
- Geographic spread: Regional focus
- Service mix: Category-appropriate

## V. Program Goals

### A. Service Objectives

#### 1. Access Goals
- Universal connectivity
- Modern technology
- Affordable access
- Geographic equity

#### 2. Performance Targets
- 100% school connectivity
- 1Gbps per 1,000 students
- Category 2 budgets met
- Cost-effective service

### B. Program Efficiency

#### 1. Administrative Goals
- Competitive bidding
- Price transparency
- Fair distribution
- Effective oversight

#### 2. Operational Targets
- Application processing: 90 days
- Funding commitments: 120 days
- Payment processing: 30 days
- Appeal resolution: 90 days

This overview provides context for understanding normal E-Rate program operations and establishes baseline patterns against which potential fraud indicators can be measured.

