# KAG OpenSPG Schema Guide
**File:** KAG_Schema_Guide.md
**Created:** 2025-10-26
**Version:** 1.0.0
**Author:** Research Agent
**Purpose:** Technical guide for creating OpenSPG schemas in KAG framework
**Status:** ACTIVE

## Executive Summary

This guide provides comprehensive documentation for creating domain-specific knowledge graphs using KAG's OpenSPG schema system. Based on analysis of KAG source code and examples, it covers schema syntax, entity/concept/event modeling, property definitions, relationship specifications, logical rules, and integration workflows.

**Key Findings:**
- OpenSPG uses a declarative schema language with namespace-scoped type definitions
- Three primary type categories: EntityType, ConceptType, EventType
- Properties support semantic typing, indexing strategies, and constraints
- Advanced features include logical rules, derived properties, and multi-value constraints
- Schema commitment follows a standardized workflow using `knext` CLI commands

---

## Table of Contents
1. [OpenSPG Schema Syntax Reference](#openspg-schema-syntax-reference)
2. [Core Schema Components](#core-schema-components)
3. [Schema Type Definitions](#schema-type-definitions)
4. [Property Specifications](#property-specifications)
5. [Relationship Modeling](#relationship-modeling)
6. [Advanced Features](#advanced-features)
7. [Schema Workflow Process](#schema-workflow-process)
8. [Example Schemas](#example-schemas)
9. [Best Practices](#best-practices)
10. [Ontology Mapping Strategy](#ontology-mapping-strategy)

---

## OpenSPG Schema Syntax Reference

### Basic Structure

```
namespace <NamespaceName>

<TypeName>(<ChineseName>): <TypeCategory>
    properties:
        <propertyName>(<chineseName>): <PropertyType>
            index: <IndexStrategy>
            constraint: <ConstraintType>
            rule: [[<LogicalRule>]]
    relations:
        <relationName>(<chineseName>): <TargetType>
            properties:
                <edgeProperty>: <PropertyType>
            rule: [[<LogicalRule>]]
```

### Syntax Elements

| Element | Description | Example |
|---------|-------------|---------|
| `namespace` | Schema namespace declaration | `namespace Medicine` |
| `TypeName` | English type identifier | `Disease`, `Company`, `Product` |
| `(ChineseName)` | Chinese label (optional) | `(疾病)`, `(企业)`, `(产品)` |
| `TypeCategory` | Type classification | `EntityType`, `ConceptType`, `EventType` |
| `properties` | Property block declaration | Properties defined in this block |
| `relations` | Relationship block declaration | Relations defined in this block |
| `index` | Indexing strategy | `Text`, `TextAndVector`, `Vector` |
| `constraint` | Property constraints | `MultiValue`, `Required` |
| `rule` | Logical rule definition | DSL-based rule expressions |

---

## Core Schema Components

### 1. Namespace Declaration

**Purpose:** Organizes schemas and prevents naming conflicts

**Syntax:**
```
namespace <ProjectName>
```

**Examples from KAG:**
```
namespace Medicine
namespace SupplyChain
namespace DomainKG
namespace RiskMining
```

**Guidelines:**
- Use PascalCase for namespace names
- Keep namespace names concise and domain-specific
- One namespace per schema file

---

### 2. Type Categories

OpenSPG supports three fundamental type categories:

#### EntityType
**Purpose:** Represents concrete entities with unique identity

**Characteristics:**
- Has unique identifiers (IDs)
- Represents physical or logical objects
- Can have properties and relationships
- Examples: Person, Company, Disease, Product

**Syntax:**
```
<EntityName>(<Label>): EntityType
    properties:
        <propertyName>: <Type>
    relations:
        <relationName>: <TargetEntity>
```

#### ConceptType
**Purpose:** Represents abstract concepts and taxonomies

**Characteristics:**
- Forms hierarchical concept taxonomies
- Uses `hypernymPredicate` for parent-child relationships
- Typically used for classification systems
- Examples: Industry taxonomy, Product categories, Disease classifications

**Syntax:**
```
<ConceptName>(<Label>): ConceptType
    hypernymPredicate: isA
```

**Key Feature - `hypernymPredicate`:**
- Defines the relationship for concept hierarchy
- `isA` is the standard hypernym predicate
- Enables multi-level taxonomies automatically

#### EventType
**Purpose:** Represents temporal occurrences with multiple participants

**Characteristics:**
- Captures spatio-temporal relationships
- Links multiple entities as event participants
- Properties describe event attributes
- Examples: CompanyEvent, ProductChainEvent, Transaction

**Syntax:**
```
<EventName>(<Label>): EventType
    properties:
        subject(<label>): <EntityType>
        object(<label>): <EntityType>
        time(<label>): Date
        index(<label>): <ConceptType>
        trend(<label>): <ConceptType>
    relations:
        leadTo(<label>): <EventType>
```

---

## Schema Type Definitions

### Entity Type Examples

#### Simple Entity
```
Person(自然人): EntityType
    properties:
        age(年龄): Integer
        certNo(证件号码): Text
```

#### Entity with Semantic Properties
```
Company(企业): EntityType
    properties:
        product(经营产品): Product
            constraint: MultiValue
        totalTransInAmt(总共流入金额): Float
    relations:
        fundTrans(资金往来): Company
            properties:
                transDate(交易日期): Text
                transAmt(交易金额): Integer
```

#### Domain-Specific Entity (Medical)
```
Disease(疾病): EntityType
    properties:
        desc(描述): Text
            index: Text
        semanticType(语义类型): Text
            index: Text
        complication(并发症): Disease
            constraint: MultiValue
        commonSymptom(常见症状): Symptom
            constraint: MultiValue
        applicableMedicine(适用药品): Medicine
            constraint: MultiValue
        hospitalDepartment(就诊科室): HospitalDepartment
            constraint: MultiValue
        diseaseSite(发病部位): HumanBodyPart
            constraint: MultiValue
    relations:
        abnormal(异常指征): Indicator
```

### Concept Type Examples

#### Simple Concept Taxonomy
```
Industry(产业): ConceptType
    hypernymPredicate: isA

TaxOfProduct(产品分类): ConceptType
    hypernymPredicate: isA
```

#### Concept with Rules
```
TaxOfRiskUser(风险用户): ConceptType
    hypernymPredicate: isA

# Specific risk user classification with rule
`TaxOfRiskUser`/`高风险用户`:
    rule: [[
        Define (u:Person)-[p:belongTo]->(o:`TaxOfRiskUser`/`高风险用户`) {
            Structure {
                (u)-[:uses]->(a:App)
            }
            Constraint {
                R1: a.riskLevel > 0.8
            }
        }
    ]]
```

### Event Type Examples

#### Company Event
```
CompanyEvent(公司事件): EventType
    properties:
        subject(主体): Company
        index(指标): Index
        trend(趋势): Trend
        IND#belongTo(属于): TaxOfCompanyEvent
        CAU#leadTo(导致): CompanyEvent
```

#### Product Chain Event
```
ProductChainEvent(产业链事件): EventType
    properties:
        subject(主体): Product
        index(指标): Index
        trend(趋势): Trend
        IND#belongTo(属于): TaxOfProdEvent
    relations:
        CAU#leadTo(导致): CompanyEvent
```

---

## Property Specifications

### Property Types

#### Basic Types
```
properties:
    name(姓名): Text
    age(年龄): Integer
    salary(工资): Float
    isActive(激活状态): Boolean
    birthDate(出生日期): Date
```

#### Semantic Types (Entity/Concept References)
```
properties:
    product(经营产品): Product              # References Product type
    hospitalDepartment(就诊科室): HospitalDepartment  # References concept
    semanticType(语义类型): SemanticConcept  # Semantic classification
```

### Indexing Strategies

**Purpose:** Controls how properties are indexed for search/retrieval

| Index Type | Use Case | Example |
|------------|----------|---------|
| `Text` | Full-text search | Keyword search, exact match |
| `Vector` | Semantic similarity | Embedding-based retrieval |
| `TextAndVector` | Hybrid search | Combined text + semantic search |

**Syntax:**
```
properties:
    content(内容): Text
        index: TextAndVector    # Enables both text and vector search
    desc(描述): Text
        index: Text             # Text-only indexing
    semanticType(语义类型): Text
        index: Text
```

**Index Strategy Selection:**
- **Text**: Use for exact match, keyword search, structured data
- **Vector**: Use for semantic search, similarity matching, unstructured content
- **TextAndVector**: Use for maximum flexibility, important fields requiring both

### Constraints

#### MultiValue Constraint
**Purpose:** Allows property to hold multiple values

```
properties:
    complication(并发症): Disease
        constraint: MultiValue    # A disease can have multiple complications
    product(经营产品): Product
        constraint: MultiValue    # A company can have multiple products
```

**When to use:**
- One-to-many relationships as properties
- List-valued attributes
- Multiple classifications

---

## Relationship Modeling

### Basic Relationships

**Syntax:**
```
relations:
    <relationName>(<chineseName>): <TargetType>
        properties:
            <edgeProperty>: <PropertyType>
```

**Example:**
```
Company(企业): EntityType
    relations:
        fundTrans(资金往来): Company
            properties:
                transDate(交易日期): Text
                transAmt(交易金额): Integer
```

### Relationship with Logical Rules

**Advanced Pattern:** Derived relationships computed from graph patterns

```
Company(企业): EntityType
    relations:
        belongToIndustry(所在行业): Industry
            rule: [[
                Define (s:Company)-[p:belongToIndustry]->(o:Industry) {
                    Structure {
                        (s)-[:product]->(c:Product)-[:belongToIndustry]->(o)
                    }
                    Constraint {
                    }
                }
            ]]
```

**Key Elements:**
- **Define**: Declares the relationship signature
- **Structure**: Graph pattern to match
- **Constraint**: Conditions that must be satisfied
- **Action**: (Optional) Actions to perform when rule fires

---

## Advanced Features

### 1. Logical Rules (DSL)

OpenSPG provides a Domain-Specific Language (DSL) for expressing logical rules.

#### Rule Structure
```
rule: [[
    Define (s:<SourceType>)-[p:<Predicate>]->(o:<TargetType>) {
        Structure {
            <GraphPattern>
        }
        Constraint {
            <LogicalConstraints>
        }
        Action {
            <ActionsToExecute>
        }
    }
]]
```

#### Example: Derived Property Rule
```
Company(企业): EntityType
    properties:
        totalTransInAmt(总共流入金额): Float
            rule: [[
                Define (s:Company)-[p:totalTransInAmt]->(o:Float) {
                    STRUCTURE {
                        (inCompany:Company)-[fundIn:fundTrans]->(s)
                    }
                    CONSTRAINT {
                        otherTransSum("总共转入金额") = group(s).sum(fundIn.transAmt)
                        o = otherTransSum
                    }
                }
            ]]
```

#### Example: Time-Based Derived Property
```
fundTrans1Month(近1月流出): Float
    rule: [[
        Define (s:Company)-[p:fundTrans1Month]->(o:Float) {
            STRUCTURE {
                (s)-[f:fundTrans]->(c:Company)
            }
            CONSTRAINT {
                R1("近1个月的流出资金"): date_diff(from_unix_time(now(), 'yyyyMMdd'),f.transDate) < 30
                totalOut = group(s).sum(f.transAmt)
                o = totalOut
            }
        }
    ]]
```

### 2. Concept Classification Rules

**Purpose:** Dynamically classify entities based on properties

**Example from concept.rule:**
```
`TaxOfCompanyEvent`/`成本上涨`:
    rule: [[
        Define (e:CompanyEvent)-[p:belongTo]->(o:`TaxOfCompanyEvent`/`成本上涨`) {
            Structure {
            }
            Constraint {
                R1: e.index == '成本'
                R2: e.trend == '上涨'
            }
        }
    ]]
```

### 3. Event Chain Rules (Causal Reasoning)

**Purpose:** Model causal relationships between events

**Example:**
```
`TaxOfProdEvent`/`价格上涨`:TaxOfCompanyEvent/`成本上涨`
    rule: [[
        Define (s:`TaxOfProdEvent`/`价格上涨`)-[p:leadTo]->(o:`TaxOfCompanyEvent`/`成本上涨`) {
            Structure {
                (s)-[:subject]->(prod:Product)-[:hasSupplyChain]->(down:Product)<-[:product]-(c:Company)
            }
            Constraint {
                eventName = concat(c.name, "成本上升事件")
            }
            Action {
                downEvent = createNodeInstance(
                    type=CompanyEvent,
                    value = {
                        subject=c.id
                        name=eventName
                        trend="上涨"
                        index="成本"
                    }
                )
                createEdgeInstance(
                    src=s,
                    dst=downEvent,
                    type=leadTo,
                    value={}
                )
            }
        }
    ]]
```

**Key Functions:**
- `createNodeInstance()`: Creates new entity/event nodes
- `createEdgeInstance()`: Creates relationships
- `concat()`: String concatenation
- `date_diff()`: Date arithmetic
- `group().sum()`: Aggregation functions

### 4. Semantic Attributes vs Relations

**OpenSPG Innovation:** Properties can reference types, auto-converting to relations

**Traditional Approach (Relations):**
```
Company(企业): EntityType
    relations:
        product(经营产品): Product
```
**Requires:** Data in multiple rows

**OpenSPG Approach (Semantic Attributes):**
```
Product(产品): ConceptType
    hypernymPredicate: isA

Company(企业): EntityType
    properties:
        product(经营产品): Product
            constraint: MultiValue
```
**Benefits:**
- Single-row data import: `"医疗器械批发,医药批发,制药,其他化学药品"`
- Automatic attribute-to-relation conversion
- Simplified data management

---

## Schema Workflow Process

### Step 1: Project Initialization

**Command:**
```bash
knext project restore --host_addr http://127.0.0.1:8887 --proj_path .
```

**Purpose:**
- Initializes KAG project with OpenSPG server
- Sets up project configuration
- Establishes connection to graph database

**Prerequisites:**
- OpenSPG server running (typically on port 8887)
- Project directory with `kag_config.yaml`
- Schema files in `schema/` directory

---

### Step 2: Schema Commitment

**Command:**
```bash
knext schema commit
```

**Purpose:**
- Submits schema definition to OpenSPG server
- Creates type definitions in graph database
- Establishes schema constraints and indexes

**What Happens:**
1. Parses `.schema` files in project schema directory
2. Validates syntax and semantic correctness
3. Registers types, properties, and relationships
4. Creates database indexes based on index strategies
5. Stores schema metadata in OpenSPG

**Output:**
- Schema committed successfully
- Type definitions available for data ingestion
- Graph database ready for knowledge construction

---

### Step 3: Concept Rule Registration (Optional)

**Command:**
```bash
knext schema reg_concept_rule --file ./schema/concept.rule
```

**Purpose:**
- Registers dynamic classification rules
- Enables runtime concept inference
- Supports event chain reasoning

**When to Use:**
- Dynamic entity classification based on properties
- Causal event chains
- Derived taxonomies

**Example Use Cases:**
- Risk user classification: `TaxOfRiskUser/高风险用户`
- Event classification: `TaxOfCompanyEvent/成本上涨`
- Causal chains: Price increase → Cost increase → Profit decline

---

### Step 4: Knowledge Construction

**Two Approaches:**

#### A. Domain Knowledge Injection
```bash
cd builder && python injection.py && cd ..
```

**Purpose:**
- Inject structured domain knowledge (taxonomies, ontologies)
- Pre-populate concept hierarchies
- Establish domain knowledge base

**Use Case:** Medical terminologies, product taxonomies, industry classifications

#### B. Document-Based Construction
```bash
cd builder && python indexer.py && cd ..
```

**Purpose:**
- Extract entities and relationships from documents
- Build knowledge graph from unstructured text
- Link extracted entities to domain knowledge

**Process:**
1. Document chunking and parsing
2. Named Entity Recognition (NER)
3. Relationship extraction
4. Entity linking to schema types
5. Graph construction and storage

---

### Step 5: Query and Reasoning

**Command:**
```bash
cd solver && python qa.py && cd ..
```

**Purpose:**
- Execute question-answering tasks
- Perform logical reasoning over knowledge graph
- Retrieve and synthesize answers

---

## Example Schemas

### Example 1: Simple Domain Knowledge Graph

**File:** `DomainKG.schema`

```
namespace DomainKG

Chunk(文本块): EntityType
    properties:
        content(内容): Text
            index: TextAndVector

Medicine(药物): EntityType
    properties:
        desc(描述): Text
            index: TextAndVector
        semanticType(语义类型): Text
            index: Text

Person(人物): EntityType
    properties:
        desc(描述): Text
            index: TextAndVector
        semanticType(语义类型): Text
            index: Text

Organization(组织机构): EntityType
    properties:
        desc(描述): Text
            index: TextAndVector
        semanticType(语义类型): Text
            index: Text
```

**Characteristics:**
- Simple entity types with descriptions
- Semantic type classification
- Hybrid text+vector indexing for all descriptions
- Suitable for general-purpose knowledge extraction

---

### Example 2: Medical Knowledge Graph

**File:** `Medicine.schema`

```
namespace Medicine

Chunk(文本块): EntityType
    properties:
        content(内容): Text
            index: TextAndVector

HospitalDepartment(科室): ConceptType
    hypernymPredicate: isA

HumanBodyPart(人体部位): ConceptType
    hypernymPredicate: isA

Disease(疾病): EntityType
    properties:
        desc(描述): Text
            index: Text
        semanticType(语义类型): Text
            index: Text
        complication(并发症): Disease
            constraint: MultiValue
        commonSymptom(常见症状): Symptom
            constraint: MultiValue
        applicableMedicine(适用药品): Medicine
            constraint: MultiValue
        hospitalDepartment(就诊科室): HospitalDepartment
            constraint: MultiValue
        diseaseSite(发病部位): HumanBodyPart
            constraint: MultiValue
    relations:
        abnormal(异常指征): Indicator

Symptom(症状): EntityType
    properties:
        desc(描述): Text
            index: Text
        semanticType(语义类型): Text
            index: Text

Medicine(药品): EntityType
    properties:
        desc(描述): Text
            index: Text
        semanticType(语义类型): Text
            index: Text
```

**Characteristics:**
- Domain-specific concepts (departments, body parts)
- Complex multi-valued properties
- Semantic references between entities
- Medical relationship modeling

---

### Example 3: Supply Chain with Rules

**File:** `SupplyChain.schema`

```
namespace SupplyChain

Industry(产业): ConceptType
    hypernymPredicate: isA

TaxOfProduct(产品分类): ConceptType
    hypernymPredicate: isA

Product(产品): EntityType
    properties:
        hasSupplyChain(供应链): Product
            constraint: MultiValue
        belongToIndustry(所属产业): Industry
        IND#belongTo(所属产品分类): TaxOfProduct

Company(企业): EntityType
    properties:
        product(经营产品): Product
            constraint: MultiValue
        totalTransInAmt(总共流入金额): Float
            rule: [[
                Define (s:Company)-[p:totalTransInAmt]->(o:Float) {
                    STRUCTURE {
                        (inCompany:Company)-[fundIn:fundTrans]->(s)
                    }
                    CONSTRAINT {
                        otherTransSum("总共转入金额") = group(s).sum(fundIn.transAmt)
                        o = otherTransSum
                    }
                }
            ]]
        fundTrans1Month(近1月流出): Float
            rule: [[
                Define (s:Company)-[p:fundTrans1Month]->(o:Float) {
                    STRUCTURE {
                        (s)-[f:fundTrans]->(c:Company)
                    }
                    CONSTRAINT {
                        R1("近1个月的流出资金"): date_diff(from_unix_time(now(), 'yyyyMMdd'),f.transDate) < 30
                        totalOut = group(s).sum(f.transAmt)
                        o = totalOut
                    }
                }
            ]]
    relations:
        fundTrans(资金往来): Company
            properties:
                transDate(交易日期): Text
                transAmt(交易金额): Integer
        mainSupply(主要客户): Company
            rule: [[
                Define (s:Company)-[p:mainSupply]->(o:Company) {
                    STRUCTURE {
                        (s)-[:product]->(upProd:Product)-[:hasSupplyChain]->(downProd:Product)<-[:product]-(o),
                        (o)-[f:fundTrans]->(s)
                    }
                    CONSTRAINT {
                        targetTransSum("供应链公司转入金额") = group(s,o).sum(f.transAmt)
                        R1("占比必须超过50%"): targetTransSum*1.0/s.totalTransInAmt > 0.5
                    }
                }
            ]]

Person(自然人): EntityType
    properties:
        age(年龄): Integer
        certNo(证件号码): Text
        legalRepresentative(法人代表): Company
            constraint: MultiValue

Index(指标): ConceptType
    hypernymPredicate: isA

Trend(趋势): ConceptType
    hypernymPredicate: isA

TaxOfCompanyEvent(公司事件分类): ConceptType
    hypernymPredicate: isA

CompanyEvent(公司事件): EventType
    properties:
        subject(主体): Company
        index(指标): Index
        trend(趋势): Trend
        IND#belongTo(属于): TaxOfCompanyEvent
        CAU#leadTo(导致): CompanyEvent

TaxOfProdEvent(产业链事件分类): ConceptType
    hypernymPredicate: isA
    relations:
        CAU#leadTo(导致): TaxOfCompanyEvent

ProductChainEvent(产业链事件): EventType
    properties:
        subject(主体): Product
        index(指标): Index
        trend(趋势): Trend
        IND#belongTo(属于): TaxOfProdEvent
    relations:
        CAU#leadTo(导致): CompanyEvent
```

**Characteristics:**
- Complex derived properties using aggregation
- Time-based analytics (monthly cash flow)
- Supply chain relationship modeling
- Event-driven causal reasoning
- Multi-type system (entities, concepts, events)

---

## Best Practices

### 1. Schema Design Principles

#### Start with Entities
- Identify core domain entities first
- Define unique identifiers and key properties
- Establish primary relationships

#### Add Concepts for Taxonomies
- Use ConceptType for classification systems
- Define `hypernymPredicate: isA` for hierarchies
- Keep concept hierarchies shallow (3-5 levels max)

#### Model Events for Temporal Data
- Use EventType for occurrences with time dimension
- Include subject/object/time as standard properties
- Link events with causal relationships

### 2. Property Design

#### Indexing Strategy
- **TextAndVector** for important descriptive fields
- **Text** for exact-match fields (IDs, codes)
- **Vector** for pure semantic search
- Minimize over-indexing to reduce storage/performance impact

#### Semantic vs Basic Types
- Prefer semantic types (entity/concept references) over Text
- Use `constraint: MultiValue` for one-to-many as properties
- Balance between properties and relations based on query patterns

### 3. Relationship Modeling

#### When to Use Properties vs Relations
**Properties:**
- One-to-many with simple values
- Classification/categorization
- Derived/computed values

**Relations:**
- Many-to-many relationships
- Relationships with rich edge properties
- Navigation-critical paths

### 4. Logical Rules

#### Rule Design Guidelines
- Keep rules simple and focused
- Use descriptive constraint names (R1: "description")
- Test rules with sample data before deployment
- Document complex aggregations and calculations

#### Performance Considerations
- Avoid deep graph pattern matching (>3 hops)
- Use indexes on properties used in constraints
- Consider materialization for frequently-computed rules

### 5. Naming Conventions

#### Consistency
- Use PascalCase for types: `Company`, `ProductChainEvent`
- Use camelCase for properties/relations: `totalTransInAmt`, `belongToIndustry`
- Include both English and Chinese labels when applicable

#### Clarity
- Make names self-documenting: `fundTrans1Month` vs `ft1m`
- Use domain terminology consistently
- Avoid abbreviations unless widely understood

### 6. Schema Evolution

#### Versioning Strategy
- Plan for schema changes (adding types/properties)
- Avoid breaking changes to existing types
- Use concept rules for flexible classification

#### Backward Compatibility
- Additive changes are safe (new types, optional properties)
- Avoid renaming or removing existing types/properties
- Migrate data when restructuring relationships

---

## Ontology Mapping Strategy

### From OWL/TTL to OpenSPG Schema

KAG does not currently include direct OWL/TTL import functionality, but provides a clear mapping path:

### Mapping Table

| OWL/TTL Construct | OpenSPG Schema Equivalent | Notes |
|-------------------|---------------------------|-------|
| `owl:Class` | `EntityType` or `ConceptType` | Use ConceptType for abstract concepts |
| `rdfs:subClassOf` | `hypernymPredicate: isA` | For ConceptType hierarchies |
| `owl:DatatypeProperty` | `properties: <Type>` | Basic property definition |
| `owl:ObjectProperty` | `relations: <EntityType>` or semantic property | Depends on cardinality |
| `rdfs:domain` | Type where property is defined | Property belongs to domain type |
| `rdfs:range` | Property type specification | Property value type |
| `owl:FunctionalProperty` | Single-valued property (default) | No constraint needed |
| `owl:InverseFunctionalProperty` | N/A | Handle via inverse relation |
| `owl:SymmetricProperty` | Define both directions | Create bidirectional relations |
| `owl:TransitiveProperty` | Use logical rule | Implement with DSL rule |
| `owl:equivalentClass` | Multiple type definitions | Create alias or use rules |
| `rdfs:label` | Chinese name in parentheses | `TypeName(中文名)` |
| `rdfs:comment` | Property `desc` | Add description property |

### Conversion Process

#### Step 1: Identify Core Concepts
**OWL Example:**
```turtle
:Disease rdf:type owl:Class ;
    rdfs:label "Disease" ;
    rdfs:comment "A medical condition affecting health" .

:Symptom rdf:type owl:Class ;
    rdfs:label "Symptom" .
```

**OpenSPG Schema:**
```
Disease(疾病): EntityType
    properties:
        desc(描述): Text
            index: Text

Symptom(症状): EntityType
    properties:
        desc(描述): Text
            index: Text
```

#### Step 2: Map Class Hierarchies
**OWL Example:**
```turtle
:MedicalCondition rdf:type owl:Class .
:Disease rdfs:subClassOf :MedicalCondition .
:ChronicDisease rdfs:subClassOf :Disease .
```

**OpenSPG Schema:**
```
MedicalCondition(医疗状况): ConceptType
    hypernymPredicate: isA

# Hierarchy created via data import:
# MedicalCondition/Disease
# MedicalCondition/Disease/ChronicDisease
```

#### Step 3: Convert Properties
**OWL Example:**
```turtle
:hasSymptom rdf:type owl:ObjectProperty ;
    rdfs:domain :Disease ;
    rdfs:range :Symptom .

:diseaseCode rdf:type owl:DatatypeProperty ;
    rdfs:domain :Disease ;
    rdfs:range xsd:string .
```

**OpenSPG Schema:**
```
Disease(疾病): EntityType
    properties:
        diseaseCode(疾病代码): Text
        commonSymptom(常见症状): Symptom
            constraint: MultiValue
```

#### Step 4: Handle Complex Axioms
**OWL Example (Transitive Property):**
```turtle
:partOf rdf:type owl:TransitiveProperty ;
    rdfs:domain :BodyPart ;
    rdfs:range :BodyPart .
```

**OpenSPG Schema with Rule:**
```
HumanBodyPart(人体部位): ConceptType
    hypernymPredicate: isA
    relations:
        partOf(部分): HumanBodyPart
            rule: [[
                # Transitivity implemented via graph pattern
                Define (s:HumanBodyPart)-[p:partOf]->(o:HumanBodyPart) {
                    Structure {
                        (s)-[:partOf]->(mid:HumanBodyPart)-[:partOf]->(o)
                    }
                    Constraint {
                    }
                }
            ]]
```

### Conversion Tools and Workflow

**Manual Conversion Process:**

1. **Extract OWL/TTL Classes**
   - List all `owl:Class` definitions
   - Identify class hierarchies (`rdfs:subClassOf`)
   - Determine EntityType vs ConceptType classification

2. **Extract Properties**
   - Map `owl:DatatypeProperty` to basic-typed properties
   - Map `owl:ObjectProperty` to semantic properties or relations
   - Identify cardinality constraints

3. **Map Restrictions and Axioms**
   - Convert cardinality restrictions to `constraint: MultiValue`
   - Implement complex axioms using logical rules
   - Handle property characteristics (functional, symmetric, transitive)

4. **Generate OpenSPG Schema File**
   - Create namespace declaration
   - Define types with properties and relations
   - Add indexing strategies based on usage patterns
   - Include logical rules for complex semantics

5. **Validate and Test**
   - Commit schema to OpenSPG server
   - Import sample data
   - Verify relationships and constraints
   - Test query patterns

**Automation Considerations:**
- Custom Python script using `rdflib` for OWL parsing
- Template-based schema generation
- Manual review required for complex rules and axioms

---

## References

### KAG Examples Analyzed
- `/kag/examples/domain_kg/` - Basic domain knowledge graph
- `/kag/examples/medicine/` - Medical knowledge graph
- `/kag/examples/supplychain/` - Supply chain with advanced rules
- `/kag/examples/riskmining/` - Risk mining with concept rules

### OpenSPG Documentation
- Schema Documentation: https://openspg.yuque.com/ndx6g9/cwh47i/fiq6zum3qtzr7cne
- KAG Repository: https://github.com/OpenSPG/KAG
- OpenSPG Server: https://github.com/OpenSPG/openspg

### Key Source Files
- `/kag/common/parser/schema_std.py` - Schema parsing logic
- `/kag/interface/solver/model/schema_utils.py` - Schema utilities
- `/kag/builder/component/extractor/schema_constraint_extractor.py` - Schema-based extraction

---

## Appendix: Complete Schema Template

```
namespace <YourDomain>

# ============================================
# Core Entity Types
# ============================================

Chunk(文本块): EntityType
    properties:
        content(内容): Text
            index: TextAndVector

<MainEntity>(<中文名>): EntityType
    properties:
        desc(描述): Text
            index: TextAndVector
        semanticType(语义类型): Text
            index: Text
        <relatedEntity>(<中文名>): <EntityType>
            constraint: MultiValue
    relations:
        <relationName>(<中文名>): <TargetEntity>
            properties:
                <edgeProperty>: <Type>

# ============================================
# Concept Types (Taxonomies)
# ============================================

<TaxonomyName>(<中文名>): ConceptType
    hypernymPredicate: isA

# ============================================
# Event Types
# ============================================

<EventName>(<中文名>): EventType
    properties:
        subject(主体): <EntityType>
        object(客体): <EntityType>
        time(时间): Date
        index(指标): <ConceptType>
        trend(趋势): <ConceptType>
    relations:
        CAU#leadTo(导致): <EventType>

# ============================================
# Catch-All Type
# ============================================

Others(其他): EntityType
    properties:
        desc(描述): Text
            index: TextAndVector
        semanticType(语义类型): Text
            index: Text
```

---

**Document Version:** 1.0.0
**Last Updated:** 2025-10-26
**Maintained By:** Research Agent
**Related Documents:** KAG Project README, OpenSPG Documentation
