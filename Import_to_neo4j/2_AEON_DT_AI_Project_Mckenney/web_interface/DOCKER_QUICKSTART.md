# AEON SaaS - Docker Development Quick Start

Get up and running with the AEON Digital Twin SaaS development environment in minutes.

## 🚀 Quick Start (5 Minutes)

### 1. Configure Environment

```bash
# Copy the example environment file
cp .env.development.example .env.development

# Edit .env.development with your API keys
nano .env.development  # or use your preferred editor
```


# Clerk Authentication
## .ENV Clerk Public Key
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_dmFsaWQtc2FpbGZpc2gtOTUuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=sk_test_5jjk7jSqlDy3FXX8OVWAH4JFfhcQ5ohI3m3cBDL6bm

# Open AI Key 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

### 2. Verify Prerequisites

```bash
# Check Docker setup
bash scripts/verify-docker-setup.sh
```

### 3. Start Development Environment

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up
```

Or run in background:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 4. Access the Application

- **Web UI**: http://localhost:3000
- **Database Admin**: http://localhost:8080 (credentials: postgres/postgres)
- **Health Check**: http://localhost:3000/api/health

## 🛠️ Common Commands

### Start/Stop

```bash
# Start (foreground)
docker-compose -f docker-compose.dev.yml up

# Start (background)
docker-compose -f docker-compose.dev.yml up -d

# Stop
docker-compose -f docker-compose.dev.yml down

# Stop and remove volumes (⚠️ deletes data)
docker-compose -f docker-compose.dev.yml down -v

# Rebuild and start
docker-compose -f docker-compose.dev.yml up --build
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.dev.yml logs -f

# Specific service
docker-compose -f docker-compose.dev.yml logs -f aeon-saas-dev
docker-compose -f docker-compose.dev.yml logs -f postgres-dev

# Last 100 lines
docker-compose -f docker-compose.dev.yml logs --tail=100 aeon-saas-dev
```

### Run Commands Inside Container

```bash
# Install a new package
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm install <package>

# Run tests
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm test

# Run database migrations
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run db:migrate

# Type check
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm run typecheck

# Open shell
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev sh
```

### Database Access

**Web UI (Adminer):**
1. Open http://localhost:8080
2. System: PostgreSQL
3. Server: postgres-dev
4. Username: postgres
5. Password: postgres
6. Database: aeon_saas_dev

**Command Line:**
```bash
docker-compose -f docker-compose.dev.yml exec postgres-dev psql -U postgres -d aeon_saas_dev
```

## 📁 What Was Created

### New Files

```
web_interface/
├── docker-compose.dev.yml           # Development orchestration
├── Dockerfile.dev                    # Development image
├── .env.development                  # Your environment variables (gitignored)
├── .env.development.example          # Environment template
├── DOCKER_QUICKSTART.md             # This file
├── scripts/
│   ├── init-db.sql                  # PostgreSQL schema initialization
│   └── verify-docker-setup.sh       # Prerequisites checker
└── docs/
    ├── DOCKER_DEVELOPMENT_README.md         # Comprehensive documentation
    └── DOCKER_SETUP_IMPLEMENTATION_SUMMARY.md  # Implementation details
```

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│           openspg-network (external)                 │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ aeon-saas-dev│  │ postgres-dev │                │
│  │  (Next.js)   │  │ (PostgreSQL) │                │
│  │  Port: 3000  │  │  Port: 5432  │                │
│  └──────┬───────┘  └──────────────┘                │
│         │                                             │
│         │ Connects to AEON Services:                 │
│         ├──► openspg-neo4j:7687                     │
│         ├──► openspg-qdrant:6333                    │
│         ├──► openspg-mysql:3306                     │
│         ├──► openspg-minio:9000                     │
│         └──► openspg-server:8887                    │
│                                                       │
└───────────────────────────────────────────────────────┘
```

## 🔧 Prerequisites

### Required

1. **Docker Desktop** (20.10+) - https://www.docker.com/products/docker-desktop
2. **Docker Compose** (2.0+) - Included with Docker Desktop
3. **openspg-network** - Docker network for AEON backend services
   ```bash
   docker network create openspg-network
   ```

### Optional (for full functionality)

4. **Clerk Account** - For authentication (https://dashboard.clerk.com)
5. **OpenAI API Key** - For AI chat features (https://platform.openai.com)
6. **AEON Backend Services** - Neo4j, Qdrant, MySQL, MinIO, OpenSPG (on openspg-network)

## ❓ Troubleshooting

### Port Already in Use

**Error:** `bind: address already in use`

**Solution:**
```bash
# Find and kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or change the port in docker-compose.dev.yml
ports:
  - "3001:3000"  # Map to different port
```

### Cannot Connect to openspg-network

**Error:** `Network openspg-network declared as external, but could not be found`

**Solution:**
```bash
docker network create openspg-network
```

### Hot Reload Not Working

**Solution:**
```bash
# Clear Next.js cache
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev rm -rf .next

# Restart container
docker-compose -f docker-compose.dev.yml restart aeon-saas-dev
```

### Database Connection Failed

**Solution:**
```bash
# Check PostgreSQL is running
docker-compose -f docker-compose.dev.yml ps postgres-dev

# Test connection
docker-compose -f docker-compose.dev.yml exec postgres-dev pg_isready
```

## 📚 Documentation

- **Complete Guide**: [`docs/DOCKER_DEVELOPMENT_README.md`](docs/DOCKER_DEVELOPMENT_README.md)
- **Implementation Details**: [`docs/DOCKER_SETUP_IMPLEMENTATION_SUMMARY.md`](docs/DOCKER_SETUP_IMPLEMENTATION_SUMMARY.md)
- **Integration Plan**: See the comprehensive plan in Front End UI Builder directory
- **Technical Spec**: [`TECHNICAL_SPECIFICATION_UI.md`](TECHNICAL_SPECIFICATION_UI.md)

## 🎯 Development Workflow

### Standard Development Cycle

1. **Start environment** (if not running):
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Make changes** to files in:
   - `./app` - Pages and API routes
   - `./components` - React components
   - `./lib` - Database clients and utilities
   - `./styles` - CSS and styling

3. **Changes auto-reload** in browser (hot module replacement)

4. **View logs** if needed:
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f aeon-saas-dev
   ```

5. **Run tests**:
   ```bash
   docker-compose -f docker-compose.dev.yml exec aeon-saas-dev npm test
   ```

6. **Stop environment** when done:
   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```

### Testing Backend Connectivity

```bash
# Test Neo4j connection
docker-compose -f docker-compose.dev.yml exec aeon-saas-dev node scripts/verify-backend-connections.js

# Test individual services
npm run test:neo4j
npm run test:qdrant
npm run test:mysql
npm run test:minio
```

## 🔐 Security Notes

### Development vs Production

This Docker configuration is for **development only**:
- ⚠️ Uses non-production database credentials
- ⚠️ Exposes debugging ports
- ⚠️ Enables verbose logging
- ⚠️ Includes source maps

For production deployment:
- ✅ Use `docker-compose.aeon-ui.yml`
- ✅ Use `Dockerfile` (multi-stage production build)
- ✅ Manage secrets properly (not in .env files)
- ✅ Enable SSL/TLS
- ✅ Use reverse proxy (Traefik, nginx)

### Protecting Sensitive Data

- ✅ `.env.development` is gitignored
- ✅ Use `.env.development.example` for templates
- ✅ Never commit API keys or passwords
- ✅ Rotate keys if accidentally committed

## 🚀 Next Steps

### Week 1-2: Foundation Setup

1. **Clone SaaS-Boilerplate** (optional):
   ```bash
   git clone https://github.com/ixartz/SaaS-Boilerplate.git
   ```

2. **Review Integration Plan**:
   - See comprehensive plan in Front End UI Builder directory
   - Understand the 16-week roadmap
   - Identify dependencies to merge

3. **Start Development**:
   - Week 3-4: Database integration layer
   - Week 5-6: UI component library
   - Week 7-16: AEON pages implementation

## 🆘 Support

### If You Need Help

1. **Run verification script**:
   ```bash
   bash scripts/verify-docker-setup.sh
   ```

2. **Check logs**:
   ```bash
   docker-compose -f docker-compose.dev.yml logs
   ```

3. **Review documentation**:
   - [`docs/DOCKER_DEVELOPMENT_README.md`](docs/DOCKER_DEVELOPMENT_README.md)
   - Troubleshooting section above

4. **Common issues**:
   - Docker not running? Start Docker Desktop
   - Port in use? Check and kill the process
   - Network not found? Create openspg-network
   - No hot reload? Restart the container

## ✅ Success Checklist

- [ ] Docker and Docker Compose installed
- [ ] openspg-network created
- [ ] .env.development configured with API keys
- [ ] Verification script runs successfully
- [ ] Environment starts with `docker-compose up`
- [ ] Application accessible at http://localhost:3000
- [ ] Database accessible via Adminer at http://localhost:8080
- [ ] Hot reload works when editing files
- [ ] Tests run successfully

---

**Implementation Date:** 2025-11-04
**Status:** ✅ Ready for Development
**Next Phase:** Database Integration Layer (Week 3-4)
