# AEON SaaS Development Environment - Docker Setup

Complete Docker-based development environment for AEON Digital Twin SaaS application, extending the ixartz/SaaS-Boilerplate with AEON features.

## Architecture Overview

### Multi-Database Strategy

This development environment implements a **hybrid multi-database architecture**:

1. **PostgreSQL (Local)** - SaaS-Boilerplate data
   - User accounts, teams, RBAC
   - Team subscriptions, billing
   - Managed by Drizzle ORM
   - Runs in `postgres-dev` container

2. **Neo4j (Remote)** - AEON Knowledge Graph
   - Cybersecurity threat intelligence
   - CVE relationships, attack patterns
   - Accessed via `openspg-network`

3. **Qdrant (Remote)** - AEON Vector Search
   - Document embeddings
   - Semantic search capabilities
   - Accessed via `openspg-network`

4. **MySQL (Remote)** - AEON OpenSPG Metadata
   - Knowledge graph metadata
   - Accessed via `openspg-network`

5. **MinIO (Remote)** - AEON Object Storage
   - File uploads, documents
   - Accessed via `openspg-network`

6. **OpenSPG Server (Remote)** - AEON Knowledge Graph Operations
   - Schema management
   - Accessed via `openspg-network`

### Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    openspg-network (external)                │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ aeon-saas-dev│  │ postgres-dev │  │   adminer    │      │
│  │  (Next.js)   │  │ (PostgreSQL) │  │ (DB Manager) │      │
│  │  Port: 3000  │  │  Port: 5432  │  │  Port: 8080  │      │
│  └──────┬───────┘  └──────────────┘  └──────────────┘      │
│         │                                                     │
│         │ Connects to Remote AEON Services:                  │
│         ├──────────────► openspg-neo4j:7687                  │
│         ├──────────────► openspg-qdrant:6333                 │
│         ├──────────────► openspg-mysql:3306                  │
│         ├──────────────► openspg-minio:9000                  │
│         └──────────────► openspg-server:8887                 │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Required

1. **Docker & Docker Compose**
   ```bash
   docker --version  # Should be 20.10+
   docker-compose --version  # Should be 2.0+
   ```

2. **OpenSPG Network** (must exist)
   ```bash
   docker network ls | grep openspg-network
   ```

   If not present, create it:
   ```bash
   docker network create openspg-network
   ```

3. **AEON Backend Services** (must be running)
   - openspg-neo4j (bolt://openspg-neo4j:7687)
   - openspg-qdrant (http://openspg-qdrant:6333)
   - openspg-mysql (mysql://openspg-mysql:3306)
   - openspg-minio (http://openspg-minio:9000)
   - openspg-server (http://openspg-server:8887)

### Optional

1. **Clerk Account** (for authentication)
   - Sign up at https://dashboard.clerk.com
   - Create a new application
   - Copy development API keys

2. **OpenAI API Key** (for AI chat features)
   - Get from https://platform.openai.com/api-keys

## Quick Start

### 1. Environment Configuration

Copy the example environment file:
```bash
cp .env.development.example .env.development
```

Edit `.env.development` and configure:

**Required:**
```bash
# Clerk Authentication (get from dashboard.clerk.com)
CLERK_PUBLISHABLE_KEY_DEV=pk_test_your_key_here
CLERK_SECRET_KEY_DEV=sk_test_your_key_here

# OpenAI (get from platform.openai.com)
OPENAI_API_KEY=sk-your-openai-key-here
```

**Optional (if not using openspg-network):**
```bash
# Uncomment and configure local database URLs
# NEO4J_URI=bolt://localhost:7687
# QDRANT_URL=http://localhost:6333
# etc.
```

### 2. Start Development Environment

**Option A: Start all services**
```bash
docker-compose -f docker-compose.dev.yml up
```

**Option B: Start in background**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

**Option C: Rebuild and start**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### 3. Access the Application

- **Web UI**: http://localhost:3000
- **Database Admin** (Adminer): http://localhost:8080
- **Health Check**: http://localhost:3000/api/health

### 4. Initial Database Setup

The PostgreSQL database is automatically initialized with the schema defined in `scripts/init-db.sql`. This includes:

- Users, teams, roles tables
- Team membership and invitations
- Subscriptions and billing
- Audit logs
- API keys

To verify initialization:
```bash
docker-compose -f docker-compose.dev.yml logs postgres-dev | grep "initialized successfully"
```

### 5. Stop Development Environment

```bash
docker-compose -f docker-compose.dev.yml down
```

To also remove volumes (⚠️ deletes all data):
```bash
docker-compose -f docker-compose.dev.yml down -v
```

## Development Workflow

### Hot Reload

All source code directories are mounted as volumes for instant hot reload:
- `./app` - Next.js pages and API routes
- `./components` - React components
- `./lib` - Database clients and utilities
- `./styles` - CSS and styling
- `./hooks` - React hooks
- `./public` - Static assets

Simply edit files in your local editor, and changes will be reflected immediately in the browser.

### Database Access

**Using Adminer (Web UI):**
1. Navigate to http://localhost:8080
2. Login with:
   - System: PostgreSQL
   - Server: postgres-dev
   - Username: postgres
   - Password: postgres
   - Database: aeon_saas_dev

**Using psql (CLI):**
```bash
docker-compose -f docker-compose.dev.yml exec postgres-dev psql -U postgres -d aeon_saas_dev
```

**Using Drizzle Studio:**
```bash
# Inside the container
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run db:studio
```

### Viewing Logs

**All services:**
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

**Specific service:**
```bash
docker-compose -f docker-compose.dev.yml logs -f aeon-saas-dev
docker-compose -f docker-compose.dev.yml logs -f postgres-dev
```

**Last N lines:**
```bash
docker-compose -f docker-compose.dev.yml logs --tail=100 aeon-saas-dev
```

### Running Commands Inside Container

**Install new package:**
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm install <package-name>
```

**Run database migrations:**
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run db:migrate
```

**Generate TypeScript types:**
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run typecheck
```

**Run tests:**
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm test
```

### Connecting to Backend Services

All AEON backend services are accessed through the `openspg-network`:

**Neo4j:**
```bash
# Inside container
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev sh
npm run test:neo4j
```

**Qdrant:**
```bash
curl http://openspg-qdrant:6333/collections
```

**MySQL:**
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev sh
npx mysql -h openspg-mysql -u root -p openspg
```

## Troubleshooting

### Issue: Cannot connect to openspg-network

**Symptoms:**
```
ERROR: Network openspg-network declared as external, but could not be found
```

**Solution:**
```bash
docker network create openspg-network
```

### Issue: Port 3000 already in use

**Symptoms:**
```
Error: bind: address already in use
```

**Solutions:**

1. Stop conflicting process:
```bash
# Find process
lsof -i :3000
# Kill process
kill -9 <PID>
```

2. Change port in `docker-compose.dev.yml`:
```yaml
ports:
  - "3001:3000"  # Map to different host port
```

### Issue: Hot reload not working

**Symptoms:** Changes not reflected in browser

**Solutions:**

1. Check volume mounts in `docker-compose.dev.yml`
2. Restart container:
```bash
docker-compose -f docker-compose.dev.yml restart aeon-saas-dev
```

3. Clear Next.js cache:
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev rm -rf .next
docker-compose -f docker-compose.dev.yml restart aeon-saas-dev
```

### Issue: Database connection failed

**Symptoms:**
```
Error: connect ECONNREFUSED
```

**Solutions:**

1. Check PostgreSQL is running:
```bash
docker-compose -f docker-compose.dev.yml ps postgres-dev
```

2. Verify environment variables:
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev env | grep DATABASE_URL
```

3. Test connection manually:
```bash
docker-compose -f docker-compose.dev.yml exec postgres-dev pg_isready
```

### Issue: Cannot connect to AEON backend services

**Symptoms:**
```
Error: getaddrinfo ENOTFOUND openspg-neo4j
```

**Solutions:**

1. Verify services are running:
```bash
docker ps | grep openspg
```

2. Check network connectivity:
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev ping openspg-neo4j
```

3. Verify openspg-network exists:
```bash
docker network inspect openspg-network
```

### Issue: Node modules not found

**Symptoms:**
```
Error: Cannot find module 'xxx'
```

**Solutions:**

1. Rebuild image:
```bash
docker-compose -f docker-compose.dev.yml build --no-cache aeon-saas-dev
```

2. Reinstall dependencies inside container:
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm install
```

## Performance Optimization

### Resource Limits

Current configuration (can be adjusted in `docker-compose.dev.yml`):

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G
```

### Build Cache

Use BuildKit for faster builds:
```bash
COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker-compose.dev.yml build
```

### Volume Performance

For better I/O performance on macOS:
1. Use `:delegated` flag (already configured)
2. Consider using Docker for Desktop's VirtioFS

For Windows with WSL2:
1. Clone repository inside WSL2 filesystem (not /mnt/c/)
2. Run Docker commands from WSL2

## Testing

### Unit Tests
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm test
```

### E2E Tests (Playwright)
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run test:e2e
```

### Integration Tests
```bash
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run test:integration
```

### Backend Connectivity Tests
```bash
# Test all backend connections
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev node scripts/verify-backend-connections.js

# Test specific services
npm run test:neo4j
npm run test:qdrant
npm run test:mysql
npm run test:minio
```

## Additional Tools

### Enable Adminer (Database UI)

Adminer is available via the `tools` profile:

```bash
docker-compose -f docker-compose.dev.yml --profile tools up -d
```

Access at: http://localhost:8080

## Environment Variables Reference

See `.env.development.example` for complete list. Key variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `CLERK_PUBLISHABLE_KEY_DEV` | Clerk public API key | Yes |
| `CLERK_SECRET_KEY_DEV` | Clerk secret API key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Auto-configured |
| `NEO4J_URI` | Neo4j bolt connection | Auto-configured |
| `QDRANT_URL` | Qdrant HTTP endpoint | Auto-configured |
| `OPENAI_API_KEY` | OpenAI API key for chat | Yes (for chat) |

## Security Considerations

### Development Mode

This configuration is for **development only** and includes:
- Exposed ports for easy access
- Debug logging enabled
- Non-production database credentials
- CORS enabled for localhost
- Source maps enabled

### Production Deployment

For production, use:
- `docker-compose.aeon-ui.yml` (production config)
- `Dockerfile` (multi-stage production build)
- Proper secrets management
- SSL/TLS encryption
- Reverse proxy (Traefik, nginx)

## Next Steps

1. **Clone SaaS-Boilerplate** (if extending):
   ```bash
   git clone https://github.com/ixartz/SaaS-Boilerplate.git
   ```

2. **Review Integration Plan**:
   See `SAAS_BOILERPLATE_AEON_INTEGRATION_PLAN.md` in the Front End UI Builder directory

3. **Start Development**:
   - Week 1-2: Foundation setup
   - Week 3-4: Database integration layer
   - Week 5-6: UI component library
   - Week 7-16: AEON pages implementation

## Support & Documentation

- **Integration Plan**: `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Front End UI Builder/SAAS_BOILERPLATE_AEON_INTEGRATION_PLAN.md`
- **Technical Spec**: `TECHNICAL_SPECIFICATION_UI.md`
- **SaaS-Boilerplate**: https://github.com/ixartz/SaaS-Boilerplate
- **Docker Compose Docs**: https://docs.docker.com/compose/

## License

See main project LICENSE file.
