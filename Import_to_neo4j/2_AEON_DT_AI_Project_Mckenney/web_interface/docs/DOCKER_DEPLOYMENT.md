# AEON UI Docker Deployment Guide

## Prerequisites

1. **OpenSPG Infrastructure Running**
   - Verify the `openspg-network` exists
   - All OpenSPG services are healthy (Neo4j, MySQL, Qdrant, MinIO, Server)

2. **Verify Network**
   ```bash
   docker network inspect openspg-network
   ```

   Expected subnet: `172.18.0.0/16`

   Existing IPs in use:
   - 172.18.0.2 - openspg-neo4j
   - 172.18.0.3 - openspg-mysql
   - 172.18.0.4 - openspg-qdrant
   - 172.18.0.5 - openspg-minio
   - 172.18.0.6 - openspg-server
   - **172.18.0.8 - aeon-ui (this service)**

## Configuration

### 1. Create `.env.production` File

Create `.env.production` in the web_interface directory:

```bash
# Security - CHANGE THESE IN PRODUCTION!
NEXTAUTH_SECRET=your-secure-random-secret-here
NEXTAUTH_URL=http://your-domain.com  # or http://localhost:3000 for local

# Optional: Override default database credentials
NEO4J_PASSWORD=neo4j@openspg
MYSQL_PASSWORD=openspg
MINIO_SECRET_KEY=minio@openspg
QDRANT_API_KEY=deqUCd5v5tL3NNTlcY3tXuPX+9vNZ7P1NMt/WlBUOZQ=
```

### 2. Generate Secure Secrets

```bash
# Generate NEXTAUTH_SECRET
openssl rand -base64 32
```

## Deployment

### Build and Start

```bash
# Build the production image
docker-compose -f docker-compose.aeon-ui.yml build

# Start the service
docker-compose -f docker-compose.aeon-ui.yml up -d

# View logs
docker-compose -f docker-compose.aeon-ui.yml logs -f aeon-ui
```

### Verify Deployment

```bash
# Check service status
docker-compose -f docker-compose.aeon-ui.yml ps

# Check health
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui wget -O- http://localhost:3000/api/health

# Test from host
curl http://localhost:3000/api/health
```

### Verify Network Configuration

```bash
# Inspect container network
docker inspect aeon-ui | grep -A 10 Networks

# Should show:
# - Network: openspg-network
# - IPAddress: 172.18.0.8
```

## Service Endpoints

- **Web UI**: http://localhost:3000
- **Health Check**: http://localhost:3000/api/health
- **Container IP**: http://172.18.0.8:3000 (from within openspg-network)

## Integration with OpenSPG Services

The AEON UI connects to OpenSPG services via internal Docker network:

| Service | Container Name | Internal URL |
|---------|---------------|--------------|
| Neo4j | openspg-neo4j | bolt://openspg-neo4j:7687 |
| MySQL | openspg-mysql | openspg-mysql:3306 |
| Qdrant | openspg-qdrant | http://openspg-qdrant:6333 |
| MinIO | openspg-minio | http://openspg-minio:9000 |
| OpenSPG Server | openspg-server | http://openspg-server:8887 |

## Troubleshooting

### Service Won't Start

```bash
# Check if network exists
docker network ls | grep openspg-network

# If not, OpenSPG infrastructure may not be running
# Start OpenSPG first, then retry
```

### IP Conflict

```bash
# Check what IPs are in use
docker network inspect openspg-network | grep IPv4Address

# If 172.18.0.8 is taken, edit docker-compose.aeon-ui.yml
# and choose a different IP in the 172.18.0.0/16 range
```

### Health Check Failing

```bash
# Check if the app is running
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui ps aux

# Check application logs
docker-compose -f docker-compose.aeon-ui.yml logs aeon-ui

# Manually test health endpoint
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui wget -O- http://localhost:3000/api/health
```

### Database Connection Issues

```bash
# Verify OpenSPG services are accessible
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui ping openspg-neo4j
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui ping openspg-mysql

# Check if credentials are correct
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui env | grep -E '(NEO4J|MYSQL|QDRANT|MINIO)'
```

## Maintenance

### View Logs

```bash
# Real-time logs
docker-compose -f docker-compose.aeon-ui.yml logs -f

# Last 100 lines
docker-compose -f docker-compose.aeon-ui.yml logs --tail=100

# Application logs volume
docker volume inspect web_interface_aeon-ui-logs
```

### Restart Service

```bash
# Restart without rebuilding
docker-compose -f docker-compose.aeon-ui.yml restart

# Rebuild and restart
docker-compose -f docker-compose.aeon-ui.yml up -d --build
```

### Stop Service

```bash
# Stop service (keeps volumes)
docker-compose -f docker-compose.aeon-ui.yml down

# Stop and remove volumes
docker-compose -f docker-compose.aeon-ui.yml down -v
```

### Update Configuration

```bash
# 1. Edit .env.production or docker-compose.aeon-ui.yml
# 2. Recreate container with new config
docker-compose -f docker-compose.aeon-ui.yml up -d --force-recreate
```

## Resource Management

The service has resource limits configured:

- **CPU Limit**: 2.0 cores
- **Memory Limit**: 2GB
- **CPU Reservation**: 1.0 core
- **Memory Reservation**: 1GB

Adjust in `docker-compose.aeon-ui.yml` under `deploy.resources` if needed.

## Security Considerations

1. **Change Default Secrets**: Update `NEXTAUTH_SECRET` in `.env.production`
2. **Network Isolation**: Service only accessible via openspg-network internally
3. **Credential Management**: Use Docker secrets or external secret management in production
4. **HTTPS**: Add reverse proxy (Traefik/Nginx) for TLS termination
5. **Database Credentials**: Rotate default passwords for Neo4j, MySQL, MinIO

## Production Checklist

- [ ] Generated secure `NEXTAUTH_SECRET`
- [ ] Updated `NEXTAUTH_URL` for production domain
- [ ] Changed default database passwords
- [ ] Configured backup strategy for logs volume
- [ ] Set up monitoring/alerting for health checks
- [ ] Configured reverse proxy with HTTPS
- [ ] Tested database connectivity
- [ ] Verified OpenSPG integration
- [ ] Documented custom configuration changes
- [ ] Set up log rotation/aggregation

## Integration Testing

```bash
# Test Neo4j connection
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui \
  sh -c 'wget -O- http://localhost:3000/api/test/neo4j'

# Test MySQL connection
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui \
  sh -c 'wget -O- http://localhost:3000/api/test/mysql'

# Test Qdrant connection
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui \
  sh -c 'wget -O- http://localhost:3000/api/test/qdrant'

# Test MinIO connection
docker-compose -f docker-compose.aeon-ui.yml exec aeon-ui \
  sh -c 'wget -O- http://localhost:3000/api/test/minio'
```

## Support

For issues or questions:
- Check logs: `docker-compose -f docker-compose.aeon-ui.yml logs`
- Verify OpenSPG services are running
- Check network configuration
- Review environment variables
