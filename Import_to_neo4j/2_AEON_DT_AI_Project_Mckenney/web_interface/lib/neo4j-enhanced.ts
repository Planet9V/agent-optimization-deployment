// Neo4j Enhanced Operations for Customer and Tag Management
// TypeScript implementation for customer CRUD, tag operations, and multi-tag assignments

import neo4j, { Driver, Session, Result } from 'neo4j-driver';

// ====================================
// TYPE DEFINITIONS
// ====================================

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone?: string;
  address?: string;
  createdAt: Date;
  updatedAt: Date;
  status: 'active' | 'inactive' | 'suspended';
  tier: 'basic' | 'professional' | 'enterprise';
}

export interface Tag {
  name: string;
  category: string;
  color: string;
  description?: string;
  createdAt: Date;
  usageCount: number;
}

export interface DocumentWithCustomer {
  id: string;
  title: string;
  type: string;
  createdAt: Date;
  customerId: string;
  customerName: string;
  tags: string[];
}

export interface ShareDocumentParams {
  documentId: string;
  customerId: string;
  permissions: string[];
  sharedBy: string;
}

// ====================================
// CONNECTION HELPER
// ====================================

export class Neo4jEnhanced {
  private driver: Driver;

  constructor(uri: string = 'bolt://localhost:7687', username: string = 'neo4j', password: string = 'neo4j@openspg') {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(username, password));
  }

  async close(): Promise<void> {
    await this.driver.close();
  }

  private getSession(): Session {
    return this.driver.session();
  }

  // ====================================
  // CUSTOMER CRUD OPERATIONS
  // ====================================

  async createCustomer(customer: Omit<Customer, 'createdAt' | 'updatedAt'>): Promise<Customer> {
    const session = this.getSession();
    try {
      const params: any = {
        id: customer.id,
        name: customer.name,
        email: customer.email,
        status: customer.status,
        tier: customer.tier,
        phone: customer.phone || null,
        address: customer.address || null
      };

      const result = await session.run(
        `
        CREATE (c:Customer {
          id: $id,
          name: $name,
          email: $email,
          createdAt: datetime(),
          updatedAt: datetime(),
          status: $status,
          tier: $tier
        })
        SET c += CASE WHEN $phone IS NOT NULL THEN {phone: $phone} ELSE {} END
        SET c += CASE WHEN $address IS NOT NULL THEN {address: $address} ELSE {} END
        RETURN c
        `,
        params
      );

      const record = result.records[0];
      return this.parseCustomer(record.get('c'));
    } finally {
      await session.close();
    }
  }

  async getCustomer(customerId: string): Promise<Customer | null> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (c:Customer {id: $customerId})
        RETURN c
        `,
        { customerId }
      );

      if (result.records.length === 0) return null;
      return this.parseCustomer(result.records[0].get('c'));
    } finally {
      await session.close();
    }
  }

  async getAllCustomers(): Promise<Customer[]> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (c:Customer)
        RETURN c
        ORDER BY c.createdAt DESC
        `
      );

      return result.records.map(record => this.parseCustomer(record.get('c')));
    } finally {
      await session.close();
    }
  }

  async updateCustomer(customerId: string, updates: Partial<Omit<Customer, 'id' | 'createdAt'>>): Promise<Customer | null> {
    const session = this.getSession();
    try {
      const setClauses = Object.keys(updates)
        .filter(key => key !== 'id' && key !== 'createdAt')
        .map(key => `c.${key} = $${key}`)
        .join(', ');

      if (!setClauses) return await this.getCustomer(customerId);

      const result = await session.run(
        `
        MATCH (c:Customer {id: $customerId})
        SET ${setClauses}, c.updatedAt = datetime()
        RETURN c
        `,
        { customerId, ...updates }
      );

      if (result.records.length === 0) return null;
      return this.parseCustomer(result.records[0].get('c'));
    } finally {
      await session.close();
    }
  }

  async deleteCustomer(customerId: string): Promise<boolean> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (c:Customer {id: $customerId})
        OPTIONAL MATCH (c)-[r]-()
        DELETE r, c
        RETURN count(c) as deletedCount
        `,
        { customerId }
      );

      return result.records[0].get('deletedCount').toNumber() > 0;
    } finally {
      await session.close();
    }
  }

  async getCustomerDocuments(customerId: string): Promise<DocumentWithCustomer[]> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (c:Customer {id: $customerId})-[:OWNS]->(d:Document)
        OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
        RETURN d, c.name as customerName, collect(DISTINCT t.name) as tags
        ORDER BY d.createdAt DESC
        `,
        { customerId }
      );

      return result.records.map(record => ({
        ...this.parseDocument(record.get('d')),
        customerName: record.get('customerName'),
        tags: record.get('tags').filter((tag: string) => tag !== null)
      }));
    } finally {
      await session.close();
    }
  }

  // ====================================
  // TAG OPERATIONS
  // ====================================

  async createTag(tag: Omit<Tag, 'createdAt' | 'usageCount'>): Promise<Tag> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MERGE (t:Tag {name: $name})
        ON CREATE SET
          t.category = $category,
          t.color = $color,
          t.description = $description,
          t.createdAt = datetime(),
          t.usageCount = 0
        ON MATCH SET
          t.category = $category,
          t.color = $color,
          t.description = $description
        RETURN t
        `,
        tag
      );

      return this.parseTag(result.records[0].get('t'));
    } finally {
      await session.close();
    }
  }

  async getTag(tagName: string): Promise<Tag | null> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (t:Tag {name: $tagName})
        RETURN t
        `,
        { tagName }
      );

      if (result.records.length === 0) return null;
      return this.parseTag(result.records[0].get('t'));
    } finally {
      await session.close();
    }
  }

  async getAllTags(): Promise<Tag[]> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (t:Tag)
        RETURN t
        ORDER BY t.usageCount DESC, t.name ASC
        `
      );

      return result.records.map(record => this.parseTag(record.get('t')));
    } finally {
      await session.close();
    }
  }

  async getTagsByCategory(category: string): Promise<Tag[]> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (t:Tag {category: $category})
        RETURN t
        ORDER BY t.usageCount DESC, t.name ASC
        `,
        { category }
      );

      return result.records.map(record => this.parseTag(record.get('t')));
    } finally {
      await session.close();
    }
  }

  async deleteTag(tagName: string): Promise<boolean> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (t:Tag {name: $tagName})
        OPTIONAL MATCH (t)-[r]-()
        DELETE r, t
        RETURN count(t) as deletedCount
        `,
        { tagName }
      );

      return result.records[0].get('deletedCount').toNumber() > 0;
    } finally {
      await session.close();
    }
  }

  // ====================================
  // MULTI-TAG ASSIGNMENT
  // ====================================

  async assignTagsToDocument(documentId: string, tagNames: string[], taggedBy: string = 'system'): Promise<void> {
    const session = this.getSession();
    try {
      await session.run(
        `
        MATCH (d:Document {id: $documentId})
        UNWIND $tagNames AS tagName
        MERGE (t:Tag {name: tagName})
        ON CREATE SET
          t.category = 'general',
          t.color = '#808080',
          t.createdAt = datetime(),
          t.usageCount = 0
        MERGE (d)-[r:HAS_TAG]->(t)
        ON CREATE SET
          r.taggedAt = datetime(),
          r.taggedBy = $taggedBy,
          t.usageCount = t.usageCount + 1
        `,
        { documentId, tagNames, taggedBy }
      );
    } finally {
      await session.close();
    }
  }

  async removeTagsFromDocument(documentId: string, tagNames: string[]): Promise<void> {
    const session = this.getSession();
    try {
      await session.run(
        `
        MATCH (d:Document {id: $documentId})-[r:HAS_TAG]->(t:Tag)
        WHERE t.name IN $tagNames
        DELETE r
        WITH t
        SET t.usageCount = CASE WHEN t.usageCount > 0 THEN t.usageCount - 1 ELSE 0 END
        `,
        { documentId, tagNames }
      );
    } finally {
      await session.close();
    }
  }

  async getDocumentTags(documentId: string): Promise<Tag[]> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (d:Document {id: $documentId})-[:HAS_TAG]->(t:Tag)
        RETURN t
        ORDER BY t.name ASC
        `,
        { documentId }
      );

      return result.records.map(record => this.parseTag(record.get('t')));
    } finally {
      await session.close();
    }
  }

  async searchDocumentsByTags(tagNames: string[], matchAll: boolean = false): Promise<DocumentWithCustomer[]> {
    const session = this.getSession();
    try {
      const query = matchAll
        ? `
          MATCH (d:Document)
          WHERE ALL(tagName IN $tagNames WHERE EXISTS {
            MATCH (d)-[:HAS_TAG]->(:Tag {name: tagName})
          })
          MATCH (d)<-[:OWNS]-(c:Customer)
          OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
          RETURN d, c.name as customerName, collect(DISTINCT t.name) as tags
          ORDER BY d.createdAt DESC
          `
        : `
          MATCH (d:Document)-[:HAS_TAG]->(t:Tag)
          WHERE t.name IN $tagNames
          MATCH (d)<-[:OWNS]-(c:Customer)
          OPTIONAL MATCH (d)-[:HAS_TAG]->(allTags:Tag)
          RETURN DISTINCT d, c.name as customerName, collect(DISTINCT allTags.name) as tags
          ORDER BY d.createdAt DESC
          `;

      const result = await session.run(query, { tagNames });

      return result.records.map(record => ({
        ...this.parseDocument(record.get('d')),
        customerName: record.get('customerName'),
        tags: record.get('tags').filter((tag: string) => tag !== null)
      }));
    } finally {
      await session.close();
    }
  }

  // ====================================
  // CUSTOMER-DOCUMENT RELATIONSHIPS
  // ====================================

  async assignDocumentToCustomer(documentId: string, customerId: string, permissions: string[] = ['read', 'write', 'delete']): Promise<void> {
    const session = this.getSession();
    try {
      await session.run(
        `
        MATCH (c:Customer {id: $customerId}), (d:Document {id: $documentId})
        MERGE (c)-[r:OWNS]->(d)
        ON CREATE SET
          r.ownedSince = datetime(),
          r.permissions = $permissions
        SET d.customerId = $customerId
        `,
        { documentId, customerId, permissions }
      );
    } finally {
      await session.close();
    }
  }

  async shareDocument(params: ShareDocumentParams): Promise<void> {
    const session = this.getSession();
    try {
      await session.run(
        `
        MATCH (d:Document {id: $documentId}), (c:Customer {id: $customerId})
        MERGE (d)-[r:SHARED_WITH]->(c)
        ON CREATE SET
          r.sharedAt = datetime(),
          r.permissions = $permissions,
          r.sharedBy = $sharedBy
        ON MATCH SET
          r.permissions = $permissions,
          r.sharedBy = $sharedBy
        `,
        params
      );
    } finally {
      await session.close();
    }
  }

  async unshareDocument(documentId: string, customerId: string): Promise<void> {
    const session = this.getSession();
    try {
      await session.run(
        `
        MATCH (d:Document {id: $documentId})-[r:SHARED_WITH]->(c:Customer {id: $customerId})
        DELETE r
        `,
        { documentId, customerId }
      );
    } finally {
      await session.close();
    }
  }

  async getSharedDocuments(customerId: string): Promise<DocumentWithCustomer[]> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (d:Document)-[s:SHARED_WITH]->(c:Customer {id: $customerId})
        MATCH (d)<-[:OWNS]-(owner:Customer)
        OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
        RETURN d, owner.name as customerName, collect(DISTINCT t.name) as tags, s.permissions as sharedPermissions
        ORDER BY d.createdAt DESC
        `,
        { customerId }
      );

      return result.records.map(record => ({
        ...this.parseDocument(record.get('d')),
        customerName: record.get('customerName'),
        tags: record.get('tags').filter((tag: string) => tag !== null)
      }));
    } finally {
      await session.close();
    }
  }

  // ====================================
  // HELPER PARSERS
  // ====================================

  private parseCustomer(node: any): Customer {
    const props = node.properties;
    return {
      id: props.id,
      name: props.name,
      email: props.email,
      phone: props.phone || undefined,
      address: props.address || undefined,
      createdAt: props.createdAt ? new Date(props.createdAt.toString()) : new Date(),
      updatedAt: props.updatedAt ? new Date(props.updatedAt.toString()) : new Date(),
      status: props.status || 'active',
      tier: props.tier || 'basic'
    };
  }

  private parseTag(node: any): Tag {
    const props = node.properties;
    return {
      name: props.name,
      category: props.category,
      color: props.color,
      description: props.description || undefined,
      createdAt: new Date(props.createdAt.toString()),
      usageCount: props.usageCount.toNumber()
    };
  }

  private parseDocument(node: any): Omit<DocumentWithCustomer, 'customerName' | 'tags'> {
    const props = node.properties;
    return {
      id: props.id,
      title: props.title,
      type: props.type,
      createdAt: new Date(props.createdAt.toString()),
      customerId: props.customerId || ''
    };
  }

  // ====================================
  // UTILITY FUNCTIONS
  // ====================================

  async getStatistics(): Promise<{
    totalCustomers: number;
    totalDocuments: number;
    totalTags: number;
    totalSharedDocuments: number;
  }> {
    const session = this.getSession();
    try {
      const result = await session.run(
        `
        MATCH (c:Customer)
        WITH count(c) as customers
        MATCH (d:Document)
        WITH customers, count(d) as documents
        MATCH (t:Tag)
        WITH customers, documents, count(t) as tags
        MATCH ()-[s:SHARED_WITH]->()
        RETURN customers, documents, tags, count(s) as sharedDocs
        `
      );

      const record = result.records[0];
      return {
        totalCustomers: record.get('customers').toNumber(),
        totalDocuments: record.get('documents').toNumber(),
        totalTags: record.get('tags').toNumber(),
        totalSharedDocuments: record.get('sharedDocs').toNumber()
      };
    } finally {
      await session.close();
    }
  }

  async testConnection(): Promise<boolean> {
    const session = this.getSession();
    try {
      await session.run('RETURN 1');
      return true;
    } catch (error) {
      console.error('Neo4j connection test failed:', error);
      return false;
    } finally {
      await session.close();
    }
  }
}

// ====================================
// EXPORT DEFAULT INSTANCE
// ====================================

export const neo4jEnhanced = new Neo4jEnhanced();

// ====================================
// SIMPLE DRIVER GETTER FOR API ROUTES
// ====================================

let _driverInstance: Driver | null = null;

export function getNeo4jDriver(): Driver {
  if (!_driverInstance) {
    const uri = process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687';
    const username = process.env.NEO4J_USERNAME || 'neo4j';
    const password = process.env.NEO4J_PASSWORD || 'neo4j@openspg';

    _driverInstance = neo4j.driver(uri, neo4j.auth.basic(username, password));
    console.log('✅ Neo4j driver initialized:', uri);
  }

  return _driverInstance;
}
