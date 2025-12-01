# MinIO Object Storage API Documentation

**File**: MinIO-Object-Storage.md
**Created**: 2025-11-03 (Current System Date)
**Version**: v1.0.0
**Author**: AEON Documentation System
**Purpose**: MinIO S3-compatible object storage API reference and integration guide
**Status**: ACTIVE

**Tags**: #minio #s3 #object-storage #files #docker #api

**Related Documentation**: [[Docker-Architecture]] [[AEON-UI]] [[Security-Policies]]

---

## Executive Summary

MinIO is a high-performance, S3-compatible object storage system running as `openspg-minio` container. It provides distributed file storage for documents, images, backups, and large files with full S3 API compatibility.

**Container Configuration**:
- **Container Name**: openspg-minio
- **Image**: minio/minio:latest
- **Status**: Healthy ✅
- **Network**: aeon-network (172.18.0.4)

**Service Endpoints**:
- **S3 API**: http://172.18.0.4:9000
- **Web Console**: http://172.18.0.4:9001
- **External Access**: http://localhost:9000 (API), http://localhost:9001 (Console)

**Authentication**:
- **Access Key**: minio
- **Secret Key**: minio@openspg
- **Console Login**: minio / minio@openspg

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [S3 API Reference](#s3-api-reference)
3. [Bucket Operations](#bucket-operations)
4. [Object Operations](#object-operations)
5. [Python SDK Examples](#python-sdk-examples)
6. [Web Console](#web-console)
7. [Security & Access Control](#security--access-control)
8. [AEON UI Integration](#aeon-ui-integration)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Access Web Console

```bash
# Open browser
http://localhost:9001

# Login credentials
Username: minio
Password: minio@openspg
```

### Install MinIO Client (mc)

```bash
# Download MinIO client
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/

# Configure alias
mc alias set local http://localhost:9000 minio minio@openspg

# Verify connection
mc admin info local
```

### Python Quick Start

```python
from minio import Minio

# Initialize client
client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio@openspg",
    secure=False  # Use True for HTTPS
)

# Check connection
buckets = client.list_buckets()
print(f"Connected! Found {len(buckets)} buckets")
```

---

## S3 API Reference

### Base Configuration

**Endpoint**: `http://172.18.0.4:9000`
**Region**: `us-east-1` (default)
**Signature Version**: AWS Signature Version 4

### Common HTTP Headers

```http
# Authentication
Authorization: AWS4-HMAC-SHA256 Credential=...
X-Amz-Date: 20251103T120000Z
X-Amz-Content-Sha256: <content-hash>

# Content
Content-Type: application/octet-stream
Content-Length: <size-in-bytes>
Content-MD5: <md5-checksum>

# Custom Metadata
X-Amz-Meta-<key>: <value>
```

### Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 204 | No Content | Delete successful |
| 400 | Bad Request | Invalid parameters |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Bucket/object not found |
| 409 | Conflict | Bucket already exists |
| 500 | Server Error | Internal error |

---

## Bucket Operations

### Create Bucket

**MinIO Client**:
```bash
mc mb local/my-bucket
mc mb local/documents --region us-east-1
```

**Python (boto3)**:
```python
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minio',
    aws_secret_access_key='minio@openspg'
)

# Create bucket
s3.create_bucket(Bucket='my-bucket')

# With configuration
s3.create_bucket(
    Bucket='documents',
    CreateBucketConfiguration={'LocationConstraint': 'us-east-1'}
)
```

**Python (minio)**:
```python
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio@openspg",
    secure=False
)

# Create bucket
if not client.bucket_exists("my-bucket"):
    client.make_bucket("my-bucket")
    print("Bucket 'my-bucket' created successfully")
```

**cURL**:
```bash
curl -X PUT http://localhost:9000/my-bucket \
  -H "Authorization: AWS4-HMAC-SHA256 ..." \
  -H "X-Amz-Date: 20251103T120000Z"
```

### List Buckets

**MinIO Client**:
```bash
mc ls local
```

**Python (boto3)**:
```python
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(f"Bucket: {bucket['Name']}, Created: {bucket['CreationDate']}")
```

**Python (minio)**:
```python
buckets = client.list_buckets()
for bucket in buckets:
    print(f"Bucket: {bucket.name}, Created: {bucket.creation_date}")
```

### Delete Bucket

**MinIO Client**:
```bash
mc rb local/my-bucket
mc rb --force local/my-bucket  # Force delete with objects
```

**Python (boto3)**:
```python
# Delete empty bucket
s3.delete_bucket(Bucket='my-bucket')

# Delete bucket with objects
bucket = boto3.resource('s3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minio',
    aws_secret_access_key='minio@openspg'
).Bucket('my-bucket')

bucket.objects.all().delete()
bucket.delete()
```

---

## Object Operations

### Upload Object

**MinIO Client**:
```bash
# Upload file
mc cp document.pdf local/documents/document.pdf

# Upload directory
mc cp --recursive ./reports/ local/documents/reports/

# With metadata
mc cp --attr "x-amz-meta-author=John Doe" file.txt local/documents/
```

**Python (boto3)**:
```python
# Upload file
s3.upload_file('document.pdf', 'documents', 'document.pdf')

# Upload with metadata
s3.upload_file(
    'document.pdf',
    'documents',
    'document.pdf',
    ExtraArgs={
        'Metadata': {
            'author': 'John Doe',
            'category': 'Reports'
        },
        'ContentType': 'application/pdf'
    }
)

# Upload bytes
s3.put_object(
    Bucket='documents',
    Key='data.json',
    Body=b'{"key": "value"}',
    ContentType='application/json'
)
```

**Python (minio)**:
```python
from minio import Minio

# Upload file
client.fput_object(
    "documents",
    "document.pdf",
    "/path/to/document.pdf",
    content_type="application/pdf"
)

# Upload bytes
import io
data = b"Hello, MinIO!"
client.put_object(
    "documents",
    "greeting.txt",
    io.BytesIO(data),
    length=len(data),
    content_type="text/plain"
)

# Upload with metadata
client.fput_object(
    "documents",
    "report.pdf",
    "/path/to/report.pdf",
    metadata={
        "x-amz-meta-author": "John Doe",
        "x-amz-meta-category": "Reports"
    }
)
```

### Download Object

**MinIO Client**:
```bash
mc cp local/documents/document.pdf ./downloaded.pdf
mc cp --recursive local/documents/reports/ ./reports/
```

**Python (boto3)**:
```python
# Download to file
s3.download_file('documents', 'document.pdf', 'downloaded.pdf')

# Get object data
response = s3.get_object(Bucket='documents', Key='document.pdf')
data = response['Body'].read()

# With byte range
response = s3.get_object(
    Bucket='documents',
    Key='large-file.bin',
    Range='bytes=0-1023'  # First 1KB
)
```

**Python (minio)**:
```python
# Download to file
client.fget_object("documents", "document.pdf", "downloaded.pdf")

# Get object data
response = client.get_object("documents", "document.pdf")
data = response.read()
response.close()
response.release_conn()
```

### List Objects

**MinIO Client**:
```bash
mc ls local/documents
mc ls --recursive local/documents/reports/
```

**Python (boto3)**:
```python
# List objects
response = s3.list_objects_v2(Bucket='documents')
for obj in response.get('Contents', []):
    print(f"Key: {obj['Key']}, Size: {obj['Size']}, Modified: {obj['LastModified']}")

# List with prefix
response = s3.list_objects_v2(Bucket='documents', Prefix='reports/')

# Paginated listing
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket='documents'):
    for obj in page.get('Contents', []):
        print(obj['Key'])
```

**Python (minio)**:
```python
# List all objects
objects = client.list_objects("documents", recursive=True)
for obj in objects:
    print(f"Key: {obj.object_name}, Size: {obj.size}, Modified: {obj.last_modified}")

# List with prefix
objects = client.list_objects("documents", prefix="reports/", recursive=True)
```

### Delete Object

**MinIO Client**:
```bash
mc rm local/documents/document.pdf
mc rm --recursive --force local/documents/old/
```

**Python (boto3)**:
```python
# Delete single object
s3.delete_object(Bucket='documents', Key='document.pdf')

# Delete multiple objects
s3.delete_objects(
    Bucket='documents',
    Delete={
        'Objects': [
            {'Key': 'file1.txt'},
            {'Key': 'file2.txt'}
        ]
    }
)
```

**Python (minio)**:
```python
# Delete single object
client.remove_object("documents", "document.pdf")

# Delete multiple objects
from minio import DeleteObject
delete_list = [DeleteObject("file1.txt"), DeleteObject("file2.txt")]
errors = client.remove_objects("documents", delete_list)
for error in errors:
    print(f"Error deleting {error}")
```

### Copy Object

**MinIO Client**:
```bash
mc cp local/documents/file.txt local/backup/file.txt
```

**Python (boto3)**:
```python
s3.copy_object(
    CopySource={'Bucket': 'documents', 'Key': 'file.txt'},
    Bucket='backup',
    Key='file.txt'
)
```

**Python (minio)**:
```python
from minio import CopySource

client.copy_object(
    "backup",
    "file.txt",
    CopySource("documents", "file.txt")
)
```

---

## Python SDK Examples

### Complete Upload/Download Example

```python
from minio import Minio
from minio.error import S3Error
import io

class MinIOManager:
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            access_key="minio",
            secret_key="minio@openspg",
            secure=False
        )
        self.bucket = "aeon-storage"
        self._ensure_bucket()

    def _ensure_bucket(self):
        """Create bucket if it doesn't exist"""
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
            print(f"Created bucket: {self.bucket}")

    def upload_file(self, file_path, object_name=None, metadata=None):
        """Upload file to MinIO"""
        if object_name is None:
            object_name = file_path.split('/')[-1]

        try:
            self.client.fput_object(
                self.bucket,
                object_name,
                file_path,
                metadata=metadata or {}
            )
            print(f"Uploaded: {object_name}")
            return True
        except S3Error as e:
            print(f"Error uploading {object_name}: {e}")
            return False

    def download_file(self, object_name, file_path):
        """Download file from MinIO"""
        try:
            self.client.fget_object(self.bucket, object_name, file_path)
            print(f"Downloaded: {object_name} -> {file_path}")
            return True
        except S3Error as e:
            print(f"Error downloading {object_name}: {e}")
            return False

    def upload_bytes(self, data, object_name, content_type="application/octet-stream"):
        """Upload bytes data to MinIO"""
        try:
            data_stream = io.BytesIO(data)
            self.client.put_object(
                self.bucket,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type
            )
            print(f"Uploaded bytes: {object_name}")
            return True
        except S3Error as e:
            print(f"Error uploading bytes: {e}")
            return False

    def list_files(self, prefix=None):
        """List all files in bucket"""
        try:
            objects = self.client.list_objects(
                self.bucket,
                prefix=prefix,
                recursive=True
            )
            return [(obj.object_name, obj.size, obj.last_modified) for obj in objects]
        except S3Error as e:
            print(f"Error listing files: {e}")
            return []

    def delete_file(self, object_name):
        """Delete file from MinIO"""
        try:
            self.client.remove_object(self.bucket, object_name)
            print(f"Deleted: {object_name}")
            return True
        except S3Error as e:
            print(f"Error deleting {object_name}: {e}")
            return False

    def get_presigned_url(self, object_name, expires_seconds=3600):
        """Generate temporary download URL"""
        try:
            url = self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=expires_seconds
            )
            return url
        except S3Error as e:
            print(f"Error generating URL: {e}")
            return None

# Usage example
if __name__ == "__main__":
    manager = MinIOManager()

    # Upload file with metadata
    manager.upload_file(
        "document.pdf",
        "docs/document.pdf",
        metadata={"author": "AEON", "category": "research"}
    )

    # List files
    files = manager.list_files(prefix="docs/")
    for name, size, modified in files:
        print(f"{name} - {size} bytes - {modified}")

    # Generate shareable URL
    url = manager.get_presigned_url("docs/document.pdf")
    print(f"Shareable URL: {url}")
```

---

## Web Console

### Access Console

**URL**: http://localhost:9001

**Features**:
- Visual bucket management
- File upload/download interface
- User and policy management
- Monitoring and metrics
- Access key generation

### Console Operations

1. **Create Bucket**:
   - Click "Create Bucket"
   - Enter bucket name (lowercase, no spaces)
   - Select versioning/encryption options
   - Click "Create"

2. **Upload Files**:
   - Navigate to bucket
   - Click "Upload" button
   - Drag files or browse
   - Monitor upload progress

3. **Manage Access**:
   - Navigate to "Identity" → "Users"
   - Create service accounts
   - Generate access keys
   - Assign policies

4. **Monitor Usage**:
   - Dashboard shows storage metrics
   - Bandwidth usage statistics
   - Request analytics

---

## Security & Access Control

### Access Policies

**Create Read-Only Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::documents/*",
        "arn:aws:s3:::documents"
      ]
    }
  ]
}
```

**Create Upload-Only Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::uploads/*"
      ]
    }
  ]
}
```

### Create Service Account

**MinIO Client**:
```bash
# Create admin user
mc admin user add local newuser secretpassword

# Create policy file
cat > readonly.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::documents/*"]
    }
  ]
}
EOF

# Apply policy
mc admin policy create local readonly readonly.json
mc admin policy attach local readonly --user newuser
```

### Bucket Encryption

```bash
# Enable encryption
mc encrypt set sse-s3 local/sensitive-data

# Verify encryption
mc encrypt info local/sensitive-data
```

---

## AEON UI Integration

### React Component Example

```typescript
// services/minioService.ts
import { Minio } from 'minio';

class MinIOService {
  private client: Minio;

  constructor() {
    this.client = new Minio({
      endPoint: '172.18.0.4',
      port: 9000,
      useSSL: false,
      accessKey: 'minio',
      secretKey: 'minio@openspg'
    });
  }

  async uploadDocument(file: File, category: string): Promise<string> {
    const bucket = 'aeon-documents';
    const objectName = `${category}/${Date.now()}-${file.name}`;

    await this.client.fPutObject(
      bucket,
      objectName,
      file.path,
      {
        'Content-Type': file.type,
        'x-amz-meta-upload-date': new Date().toISOString(),
        'x-amz-meta-uploader': 'AEON-UI'
      }
    );

    return objectName;
  }

  async getDownloadUrl(objectName: string): Promise<string> {
    return await this.client.presignedGetObject('aeon-documents', objectName, 3600);
  }

  async listDocuments(category: string): Promise<any[]> {
    const stream = this.client.listObjectsV2('aeon-documents', category, true);
    const objects: any[] = [];

    return new Promise((resolve, reject) => {
      stream.on('data', obj => objects.push(obj));
      stream.on('end', () => resolve(objects));
      stream.on('error', reject);
    });
  }
}

export default new MinIOService();
```

```typescript
// components/DocumentUpload.tsx
import React, { useState } from 'react';
import minioService from '../services/minioService';

export const DocumentUpload: React.FC = () => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const objectName = await minioService.uploadDocument(file, 'research');
      const url = await minioService.getDownloadUrl(objectName);
      alert(`File uploaded! Download URL: ${url}`);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <input
        type="file"
        onChange={handleUpload}
        disabled={uploading}
      />
      {uploading && <div>Uploading... {progress}%</div>}
    </div>
  );
};
```

---

## Performance Optimization

### Multipart Upload (Large Files)

```python
from minio import Minio

client = Minio("localhost:9000", access_key="minio", secret_key="minio@openspg", secure=False)

# Automatic multipart for files > 5MB
client.fput_object(
    "large-files",
    "video.mp4",
    "/path/to/large-video.mp4",
    part_size=10*1024*1024  # 10MB chunks
)
```

### Parallel Upload

```python
from concurrent.futures import ThreadPoolExecutor
from minio import Minio

client = Minio("localhost:9000", access_key="minio", secret_key="minio@openspg", secure=False)

def upload_file(file_path):
    object_name = file_path.split('/')[-1]
    client.fput_object("documents", object_name, file_path)
    return object_name

files = [f"/data/file{i}.txt" for i in range(100)]

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(upload_file, files))
    print(f"Uploaded {len(results)} files")
```

### Caching Strategy

```python
import redis
from minio import Minio

cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
client = Minio("localhost:9000", access_key="minio", secret_key="minio@openspg", secure=False)

def get_document(object_name, cache_ttl=3600):
    # Check cache first
    cached_url = cache.get(f"minio:{object_name}")
    if cached_url:
        return cached_url

    # Generate presigned URL
    url = client.presigned_get_object("documents", object_name, expires=cache_ttl)

    # Cache URL
    cache.setex(f"minio:{object_name}", cache_ttl, url)

    return url
```

---

## Troubleshooting

### Common Issues

**Connection Refused**:
```bash
# Check container status
docker ps | grep minio

# Check network connectivity
docker exec aeon-ui ping -c 3 openspg-minio

# Verify endpoint
curl http://localhost:9000/minio/health/live
```

**Access Denied**:
```bash
# Verify credentials
mc admin info local

# Check bucket policy
mc policy get local/my-bucket

# List user permissions
mc admin user list local
```

**Slow Uploads**:
```bash
# Check network performance
iperf3 -c 172.18.0.4 -p 9000

# Monitor container resources
docker stats openspg-minio

# Enable compression (if applicable)
mc admin config set local compression enable=on
```

### Health Check

```bash
# Container health
docker inspect openspg-minio | jq '.[0].State.Health'

# MinIO health endpoint
curl http://localhost:9000/minio/health/live

# Detailed server info
mc admin info local --json
```

### Logs

```bash
# View MinIO logs
docker logs openspg-minio

# Follow logs
docker logs -f openspg-minio

# Last 100 lines
docker logs --tail 100 openspg-minio
```

---

## Reference Links

**Official Documentation**:
- MinIO Docs: https://min.io/docs/minio/linux/index.html
- Python SDK: https://min.io/docs/minio/linux/developers/python/minio-py.html
- S3 API: https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html

**Container Management**:
- [[Docker-Architecture]] - Container infrastructure
- [[Security-Policies]] - Access control policies
- [[AEON-UI]] - Frontend integration

**Best Practices**:
- Use versioning for critical buckets
- Enable encryption for sensitive data
- Implement lifecycle policies for cost optimization
- Use presigned URLs for temporary access
- Monitor storage usage regularly

---

**Document Status**: ✅ ACTIVE
**Last Updated**: 2025-11-03
**Maintainer**: AEON Documentation Team
**Review Cycle**: Quarterly
