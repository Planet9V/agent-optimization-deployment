// Neo4j Schema Enhancement for Customer and Tag Support
// Execute this file to create the complete schema for document management with customers and tags

// ====================================
// CONSTRAINTS (Data Integrity)
// ====================================

// Ensure unique customer IDs
CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
FOR (c:Customer) REQUIRE c.id IS UNIQUE;

// Ensure unique tag names (case-insensitive)
CREATE CONSTRAINT tag_name_unique IF NOT EXISTS
FOR (t:Tag) REQUIRE t.name IS UNIQUE;

// Ensure unique document IDs (if not already exists)
CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (d:Document) REQUIRE d.id IS UNIQUE;

// ====================================
// INDEXES (Performance Optimization)
// ====================================

// Index on Customer properties for fast lookup
CREATE INDEX customer_name_index IF NOT EXISTS
FOR (c:Customer) ON (c.name);

CREATE INDEX customer_email_index IF NOT EXISTS
FOR (c:Customer) ON (c.email);

CREATE INDEX customer_created_index IF NOT EXISTS
FOR (c:Customer) ON (c.createdAt);

// Index on Tag properties
CREATE INDEX tag_name_index IF NOT EXISTS
FOR (t:Tag) ON (t.name);

CREATE INDEX tag_category_index IF NOT EXISTS
FOR (t:Tag) ON (t.category);

CREATE INDEX tag_created_index IF NOT EXISTS
FOR (t:Tag) ON (t.createdAt);

// Index on Document properties for customer relationship queries
CREATE INDEX document_customer_index IF NOT EXISTS
FOR (d:Document) ON (d.customerId);

CREATE INDEX document_created_index IF NOT EXISTS
FOR (d:Document) ON (d.createdAt);

// ====================================
// SAMPLE CUSTOMER NODES
// ====================================

// Create sample customers for testing
MERGE (c1:Customer {id: 'cust_001'})
SET c1.name = 'Acme Corporation',
    c1.email = 'contact@acme.com',
    c1.phone = '+1-555-0100',
    c1.address = '123 Business St, Tech City, TC 12345',
    c1.createdAt = datetime(),
    c1.updatedAt = datetime(),
    c1.status = 'active',
    c1.tier = 'enterprise';

MERGE (c2:Customer {id: 'cust_002'})
SET c2.name = 'Global Innovations Inc',
    c2.email = 'hello@globalinnovations.com',
    c2.phone = '+1-555-0200',
    c2.address = '456 Innovation Ave, Startup Valley, SV 54321',
    c2.createdAt = datetime(),
    c2.updatedAt = datetime(),
    c2.status = 'active',
    c2.tier = 'professional';

MERGE (c3:Customer {id: 'cust_003'})
SET c3.name = 'Small Business Solutions',
    c3.email = 'info@smallbizsolutions.com',
    c3.phone = '+1-555-0300',
    c3.address = '789 Main St, Hometown, HT 98765',
    c3.createdAt = datetime(),
    c3.updatedAt = datetime(),
    c3.status = 'active',
    c3.tier = 'basic';

// ====================================
// SAMPLE TAG NODES
// ====================================

// Create sample tags organized by category
MERGE (t1:Tag {name: 'urgent'})
SET t1.category = 'priority',
    t1.color = '#FF0000',
    t1.description = 'Requires immediate attention',
    t1.createdAt = datetime(),
    t1.usageCount = 0;

MERGE (t2:Tag {name: 'invoice'})
SET t2.category = 'document-type',
    t2.color = '#4CAF50',
    t2.description = 'Financial invoice documents',
    t2.createdAt = datetime(),
    t2.usageCount = 0;

MERGE (t3:Tag {name: 'contract'})
SET t3.category = 'document-type',
    t3.color = '#2196F3',
    t3.description = 'Legal contract documents',
    t3.createdAt = datetime(),
    t3.usageCount = 0;

MERGE (t4:Tag {name: 'q4-2024'})
SET t4.category = 'period',
    t4.color = '#9C27B0',
    t4.description = 'Q4 2024 fiscal period',
    t4.createdAt = datetime(),
    t4.usageCount = 0;

MERGE (t5:Tag {name: 'reviewed'})
SET t5.category = 'status',
    t5.color = '#FF9800',
    t5.description = 'Document has been reviewed',
    t5.createdAt = datetime(),
    t5.usageCount = 0;

MERGE (t6:Tag {name: 'confidential'})
SET t6.category = 'security',
    t6.color = '#F44336',
    t6.description = 'Confidential information',
    t6.createdAt = datetime(),
    t6.usageCount = 0;

MERGE (t7:Tag {name: 'archived'})
SET t7.category = 'status',
    t7.color = '#607D8B',
    t7.description = 'Archived document',
    t7.createdAt = datetime(),
    t7.usageCount = 0;

MERGE (t8:Tag {name: 'marketing'})
SET t8.category = 'department',
    t8.color = '#E91E63',
    t8.description = 'Marketing department',
    t8.createdAt = datetime(),
    t8.usageCount = 0;

// ====================================
// RELATIONSHIP TYPES DOCUMENTATION
// ====================================

// OWNS: Customer owns a Document
// Properties: ownedSince (datetime), permissions (string[])
// Example: (Customer)-[:OWNS {ownedSince: datetime(), permissions: ['read', 'write', 'delete']}]->(Document)

// SHARED_WITH: Document shared with Customer
// Properties: sharedAt (datetime), permissions (string[]), sharedBy (string)
// Example: (Document)-[:SHARED_WITH {sharedAt: datetime(), permissions: ['read'], sharedBy: 'user_123'}]->(Customer)

// HAS_TAG: Document has Tag
// Properties: taggedAt (datetime), taggedBy (string)
// Example: (Document)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'user_123'}]->(Tag)

// TAGGED: Alternative relationship (Tag tagged to Document)
// Properties: appliedAt (datetime), appliedBy (string)
// Example: (Tag)-[:TAGGED {appliedAt: datetime(), appliedBy: 'user_123'}]->(Document)

// ====================================
// SAMPLE RELATIONSHIPS (for testing)
// ====================================

// Create sample Document nodes if they don't exist
MERGE (d1:Document {id: 'doc_001'})
SET d1.title = 'Q4 2024 Invoice - Acme Corp',
    d1.type = 'invoice',
    d1.createdAt = datetime(),
    d1.customerId = 'cust_001';

MERGE (d2:Document {id: 'doc_002'})
SET d2.title = 'Service Agreement - Global Innovations',
    d2.type = 'contract',
    d2.createdAt = datetime(),
    d2.customerId = 'cust_002';

MERGE (d3:Document {id: 'doc_003'})
SET d3.title = 'Marketing Campaign Brief',
    d3.type = 'brief',
    d3.createdAt = datetime(),
    d3.customerId = 'cust_001';

// Create ownership relationships
MATCH (c:Customer {id: 'cust_001'}), (d:Document {id: 'doc_001'})
MERGE (c)-[:OWNS {
    ownedSince: datetime(),
    permissions: ['read', 'write', 'delete', 'share']
}]->(d);

MATCH (c:Customer {id: 'cust_002'}), (d:Document {id: 'doc_002'})
MERGE (c)-[:OWNS {
    ownedSince: datetime(),
    permissions: ['read', 'write', 'delete', 'share']
}]->(d);

MATCH (c:Customer {id: 'cust_001'}), (d:Document {id: 'doc_003'})
MERGE (c)-[:OWNS {
    ownedSince: datetime(),
    permissions: ['read', 'write', 'delete', 'share']
}]->(d);

// Create sharing relationship (doc_001 shared with cust_002)
MATCH (d:Document {id: 'doc_001'}), (c:Customer {id: 'cust_002'})
MERGE (d)-[:SHARED_WITH {
    sharedAt: datetime(),
    permissions: ['read'],
    sharedBy: 'cust_001'
}]->(c);

// Create tag relationships
MATCH (d:Document {id: 'doc_001'}), (t:Tag {name: 'invoice'})
MERGE (d)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'system'}]->(t)
SET t.usageCount = t.usageCount + 1;

MATCH (d:Document {id: 'doc_001'}), (t:Tag {name: 'q4-2024'})
MERGE (d)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'system'}]->(t)
SET t.usageCount = t.usageCount + 1;

MATCH (d:Document {id: 'doc_001'}), (t:Tag {name: 'urgent'})
MERGE (d)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'user_123'}]->(t)
SET t.usageCount = t.usageCount + 1;

MATCH (d:Document {id: 'doc_002'}), (t:Tag {name: 'contract'})
MERGE (d)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'system'}]->(t)
SET t.usageCount = t.usageCount + 1;

MATCH (d:Document {id: 'doc_002'}), (t:Tag {name: 'reviewed'})
MERGE (d)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'user_456'}]->(t)
SET t.usageCount = t.usageCount + 1;

MATCH (d:Document {id: 'doc_002'}), (t:Tag {name: 'confidential'})
MERGE (d)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'user_456'}]->(t)
SET t.usageCount = t.usageCount + 1;

MATCH (d:Document {id: 'doc_003'}), (t:Tag {name: 'marketing'})
MERGE (d)-[:HAS_TAG {taggedAt: datetime(), taggedBy: 'system'}]->(t)
SET t.usageCount = t.usageCount + 1;

// ====================================
// USEFUL QUERIES FOR VERIFICATION
// ====================================

// Count nodes by type
// MATCH (n) RETURN labels(n) AS type, count(*) AS count ORDER BY count DESC;

// View all customers with their document counts
// MATCH (c:Customer)
// OPTIONAL MATCH (c)-[:OWNS]->(d:Document)
// RETURN c.name, c.email, c.tier, count(d) AS documentCount
// ORDER BY documentCount DESC;

// View all tags with usage counts
// MATCH (t:Tag)
// RETURN t.name, t.category, t.color, t.usageCount
// ORDER BY t.usageCount DESC;

// View documents with their owners and tags
// MATCH (d:Document)<-[:OWNS]-(c:Customer)
// OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
// RETURN d.title, c.name AS owner, collect(t.name) AS tags;

// View shared documents
// MATCH (d:Document)-[s:SHARED_WITH]->(c:Customer)
// RETURN d.title, c.name AS sharedWith, s.permissions, s.sharedBy;

// ====================================
// SCHEMA COMPLETE
// ====================================
