// Jest setup file
// Add custom matchers, global test utilities, etc.

// Extend timeout for integration tests
jest.setTimeout(30000);

// Mock environment variables if needed
process.env.NEO4J_URI = process.env.NEO4J_URI || 'bolt://localhost:7687';
process.env.NEO4J_USER = process.env.NEO4J_USER || 'neo4j';
process.env.NEO4J_PASSWORD = process.env.NEO4J_PASSWORD || 'P@ssw0rd-2024';
process.env.QDRANT_URL = process.env.QDRANT_URL || 'http://localhost:6333';
process.env.QDRANT_API_KEY = process.env.QDRANT_API_KEY || 'aeon-dt-qdrant-key-2024';
