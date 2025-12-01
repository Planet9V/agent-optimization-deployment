/**
 * OpenSPG Knowledge Graph Client
 * Singleton pattern for OpenSPG server API access
 */

let openspgBaseUrl: string | null = null;

export function getOpenSPGUrl(): string {
  if (!openspgBaseUrl) {
    openspgBaseUrl = process.env.OPENSPG_SERVER_URL || 'http://openspg-server:8887';
    console.log('✅ OpenSPG client initialized:', openspgBaseUrl);
  }
  return openspgBaseUrl;
}

export async function testOpenSPGConnection(): Promise<boolean> {
  try {
    const url = getOpenSPGUrl();
    const response = await fetch(`${url}/api/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      console.log('✅ OpenSPG connected');
      return true;
    } else {
      console.warn('⚠️ OpenSPG health check returned non-OK status:', response.status);
      return false;
    }
  } catch (error) {
    console.error('❌ OpenSPG connection failed:', error);
    return false;
  }
}

interface OpenSPGRequestOptions {
  endpoint: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: any;
  headers?: Record<string, string>;
}

export async function openspgRequest<T = any>(
  options: OpenSPGRequestOptions
): Promise<{ success: boolean; data?: T; error?: string }> {
  const { endpoint, method = 'GET', body, headers = {} } = options;
  const url = `${getOpenSPGUrl()}${endpoint}`;

  try {
    const requestHeaders = {
      'Content-Type': 'application/json',
      ...headers,
    };

    const requestOptions: RequestInit = {
      method,
      headers: requestHeaders,
    };

    if (body && method !== 'GET') {
      requestOptions.body = JSON.stringify(body);
    }

    const response = await fetch(url, requestOptions);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    return {
      success: true,
      data,
    };
  } catch (error) {
    console.error('OpenSPG request error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

export async function querySchema(schemaName?: string) {
  const endpoint = schemaName ? `/api/schema/${schemaName}` : '/api/schema';
  return openspgRequest({ endpoint, method: 'GET' });
}

export interface EntityQueryParams {
  entityType: string;
  filters?: Record<string, any>;
  limit?: number;
  offset?: number;
}

export async function queryEntities(params: EntityQueryParams) {
  const { entityType, filters, limit = 100, offset = 0 } = params;

  return openspgRequest({
    endpoint: '/api/entities/query',
    method: 'POST',
    body: {
      entityType,
      filters: filters || {},
      limit,
      offset,
    },
  });
}

export async function getStatistics() {
  return openspgRequest({
    endpoint: '/api/statistics',
    method: 'GET',
  });
}

export default {
  getOpenSPGUrl,
  testOpenSPGConnection,
  openspgRequest,
  querySchema,
  queryEntities,
  getStatistics,
};
