/**
 * MinIO Object Storage Client
 * Singleton pattern for file uploads and document management
 */

import { Client as MinioClient } from 'minio';

let minioClient: MinioClient | null = null;

export function getMinIOClient(): MinioClient {
  if (!minioClient) {
    const endpoint = process.env.MINIO_ENDPOINT || 'openspg-minio:9000';
    const [host, portStr] = endpoint.split(':');
    const port = parseInt(portStr || process.env.MINIO_PORT || '9000');

    const config = {
      endPoint: host,
      port,
      useSSL: process.env.MINIO_USE_SSL === 'true',
      accessKey: process.env.MINIO_ACCESS_KEY || 'minio',
      secretKey: process.env.MINIO_SECRET_KEY || 'minio@openspg',
    };

    minioClient = new MinioClient(config);
    console.log('✅ MinIO client initialized:', `${host}:${port}`);
  }

  return minioClient;
}

export async function testMinIOConnection(): Promise<boolean> {
  try {
    const client = getMinIOClient();
    const buckets = await client.listBuckets();
    console.log('✅ MinIO connected. Buckets:', buckets.length);
    return true;
  } catch (error) {
    console.error('❌ MinIO connection failed:', error);
    return false;
  }
}

export async function ensureBucket(bucketName: string): Promise<boolean> {
  const client = getMinIOClient();

  try {
    const exists = await client.bucketExists(bucketName);
    if (!exists) {
      await client.makeBucket(bucketName, 'us-east-1');
      console.log(`✅ Bucket created: ${bucketName}`);
    }
    return true;
  } catch (error) {
    console.error('Ensure bucket error:', error);
    return false;
  }
}

export interface UploadOptions {
  bucketName: string;
  objectName: string;
  buffer: Buffer;
  metadata?: Record<string, string>;
  contentType?: string;
}

export async function uploadFile(options: UploadOptions) {
  const client = getMinIOClient();
  const { bucketName, objectName, buffer, metadata = {}, contentType = 'application/octet-stream' } = options;

  try {
    await ensureBucket(bucketName);

    const uploadMetadata = {
      'Content-Type': contentType,
      ...metadata,
    };

    await client.putObject(bucketName, objectName, buffer, buffer.length, uploadMetadata);

    const presignedUrl = await client.presignedGetObject(bucketName, objectName, 24 * 60 * 60 * 7);

    return {
      success: true,
      objectName,
      bucketName,
      size: buffer.length,
      url: presignedUrl,
    };
  } catch (error) {
    console.error('Upload file error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

export async function listObjects(bucketName: string, prefix: string = '', recursive: boolean = true) {
  const client = getMinIOClient();

  try {
    const stream = client.listObjects(bucketName, prefix, recursive);
    const objects: any[] = [];

    return new Promise<{ success: boolean; objects?: any[]; error?: string }>((resolve, reject) => {
      stream.on('data', (obj) => objects.push(obj));
      stream.on('end', () => {
        resolve({
          success: true,
          objects,
        });
      });
      stream.on('error', (error) => {
        reject({
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        });
      });
    });
  } catch (error) {
    console.error('List objects error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

export async function listBuckets() {
  const client = getMinIOClient();

  try {
    const buckets = await client.listBuckets();
    return {
      success: true,
      buckets,
    };
  } catch (error) {
    console.error('List buckets error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

export default {
  getMinIOClient,
  testMinIOConnection,
  ensureBucket,
  uploadFile,
  listObjects,
  listBuckets,
};
