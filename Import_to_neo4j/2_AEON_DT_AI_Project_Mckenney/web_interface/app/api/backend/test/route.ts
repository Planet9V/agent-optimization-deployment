import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { getNeo4jDriver } from '@/lib/neo4j-enhanced';
import { testQdrantConnection } from '@/lib/qdrant';
import { testMySQLConnection } from '@/lib/mysql';
import { testMinIOConnection } from '@/lib/minio';
import { testOpenSPGConnection } from '@/lib/openspg';

/**
 * GET /api/backend/test
 * Tests connectivity to all backend services
 */
export async function GET(request: NextRequest) {
  try {
    // Skip auth for diagnostic endpoint
    const results: Record<string, any> = {
      timestamp: new Date().toISOString(),
      services: {},
    };

    // Test Neo4j
    try {
      const driver = getNeo4jDriver();
      const session_neo4j = driver.session();
      try {
        await session_neo4j.run('RETURN 1');
        results.services.neo4j = { status: 'connected', error: null };
      } catch (error: any) {
        results.services.neo4j = { status: 'error', error: error.message };
      } finally {
        await session_neo4j.close();
      }
    } catch (error: any) {
      results.services.neo4j = { status: 'error', error: error.message };
    }

    // Test Qdrant
    try {
      const qdrantConnected = await testQdrantConnection();
      results.services.qdrant = {
        status: qdrantConnected ? 'connected' : 'error',
        error: qdrantConnected ? null : 'Connection failed',
      };
    } catch (error: any) {
      results.services.qdrant = { status: 'error', error: error.message };
    }

    // Test MySQL
    try {
      const mysqlConnected = await testMySQLConnection();
      results.services.mysql = {
        status: mysqlConnected ? 'connected' : 'error',
        error: mysqlConnected ? null : 'Connection failed',
      };
    } catch (error: any) {
      results.services.mysql = { status: 'error', error: error.message };
    }

    // Test MinIO
    try {
      const minioConnected = await testMinIOConnection();
      results.services.minio = {
        status: minioConnected ? 'connected' : 'error',
        error: minioConnected ? null : 'Connection failed',
      };
    } catch (error: any) {
      results.services.minio = { status: 'error', error: error.message };
    }

    // Test OpenSPG
    try {
      const openspgConnected = await testOpenSPGConnection();
      results.services.openspg = {
        status: openspgConnected ? 'connected' : 'error',
        error: openspgConnected ? null : 'Connection failed',
      };
    } catch (error: any) {
      results.services.openspg = { status: 'error', error: error.message };
    }

    // Calculate overall status
    const allConnected = Object.values(results.services).every(
      (service: any) => service.status === 'connected'
    );
    const someConnected = Object.values(results.services).some(
      (service: any) => service.status === 'connected'
    );

    results.overall = allConnected
      ? 'all_connected'
      : someConnected
      ? 'partial'
      : 'all_failed';

    return NextResponse.json(results);
  } catch (error) {
    console.error('Error testing backend connections:', error);

    return NextResponse.json(
      {
        error: 'Backend connection test failed',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
