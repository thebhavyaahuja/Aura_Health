# 🐳 Docker Setup Guide - Mammography Report Analysis System

> **Simple Docker setup** for running the entire project locally or deploying to production.

---

## 📋 Prerequisites

- **Docker** (20.10+)  
- **Docker Compose** (2.0+)

Check with:
```bash
docker --version
docker-compose --version
```

---

## 🚀 Quick Start (3 Steps)

### 1. Configure Environment Variables

Copy the example env file and **update with your API keys**:

```bash
cp .env.example .env
```

**Edit `.env` and set:**
- `GEMINI_API_KEY` — Your Google Gemini API key (required for information-structuring service)
- `JWT_SECRET` — Change to a strong secret for production
- Other optional settings (see `.env.example`)

---

### 2. Build & Run

From the **project root** directory:

```bash
docker-compose up --build
```

This will:
- Build all backend microservices (authentication, ingestion, parsing, structuring, risk-prediction)
- Build the Next.js frontend
- Start PostgreSQL and Redis
- Wire everything together

**First build takes ~5-10 minutes.** Subsequent runs are faster.

---

### 3. Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main web interface |
| **Authentication** | http://localhost:8010 | Auth API |
| **Document Ingestion** | http://localhost:8001 | Upload service |
| **Document Parsing** | http://localhost:8002 | PDF parsing |
| **Information Structuring** | http://localhost:8003 | AI structuring |
| **Risk Prediction** | http://localhost:8004 | BI-RADS prediction |
| **Redis** | localhost:6379 | Cache/queue |

**Note:** All services use **SQLite databases** stored in Docker volumes, so your data persists across container restarts.

---

## 🛑 Stop Services

```bash
docker-compose down
```

To **remove volumes** (clears database data):
```bash
docker-compose down -v
```

---

## 🔄 Restart a Specific Service

```bash
docker-compose restart <service-name>
```

Example:
```bash
docker-compose restart information-structuring
```

---

## 📝 View Logs

**All services:**
```bash
docker-compose logs -f
```

**Specific service:**
```bash
docker-compose logs -f frontend
docker-compose logs -f authentication
docker-compose logs -f risk-prediction
```

---

## 🐛 Troubleshooting

### Database Files Location
Your SQLite databases are stored in Docker volumes:
```bash
# List all volumes
docker volume ls | grep mammography

# Inspect a volume
docker volume inspect odomos-dsi_auth_data
```

To backup your databases:
```bash
docker-compose exec authentication cp /app/data/auth.db /app/data/auth_backup.db
```

### Port Already in Use
If you see "port already allocated", stop conflicting services:
```bash
# Check what's using a port (e.g., 3000)
lsof -i :3000

# Kill the process
kill -9 <PID>
```

### Missing API Keys
If `information-structuring` fails:
- Verify `GEMINI_API_KEY` is set in `.env`
- Check logs: `docker-compose logs information-structuring`

### Build Errors
Clean rebuild:
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

## 🔧 Development Mode

To enable **hot-reload** for development:

1. Update `docker-compose.yml` volumes to mount source code:
   ```yaml
   services:
     frontend:
       volumes:
         - ./frontend:/app
         - /app/node_modules
   ```

2. Use `docker-compose up` (without `--build` after first build)

---

## 🚢 Production Deployment

For production:

1. **Set strong secrets** in `.env`
2. **Update CORS_ORIGINS** to your domain
3. **Consider PostgreSQL** instead of SQLite for multi-user scenarios:
   - Update `DATABASE_URL` in `.env` to use PostgreSQL
   - Uncomment postgres service in `docker-compose.yml` if needed
4. Add SSL/TLS termination (nginx, Traefik, etc.)
5. Set `NODE_ENV=production` (already default)
6. **Backup SQLite volumes regularly** or migrate to PostgreSQL

**SQLite Limitations in Production:**
- SQLite is fine for **low-to-medium traffic** and **single-container deployments**
- For **high concurrency** or **multi-replica setups**, migrate to PostgreSQL
- Current setup: Each service has isolated SQLite DB (good for microservices)

---

## 📦 Service Architecture

```
┌─────────────────────────────────────────┐
│          Frontend (Next.js)             │
│           Port 3000                     │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐  ┌─────────────▼────────────┐
│  Auth  │  │  Backend Microservices   │
│  8010  │  │  8001, 8002, 8003, 8004  │
│ SQLite │  │  Each with own SQLite    │
└───┬────┘  └─────────────┬────────────┘
    │                     │
    └──────────┬──────────┘
               │
         ┌─────▼─────┐
         │   Redis   │
         │   6379    │
         └───────────┘
```

**Database Architecture:**
- Each backend service has its **own SQLite database** in a persistent Docker volume
- Databases are stored in `/app/data/*.db` inside containers
- Volumes persist data across container restarts and rebuilds

---

## ✅ Success Indicators

When everything is running correctly, you should see:

```
✅ mammography-frontend       ... running
✅ mammography-authentication ... running
✅ mammography-ingestion      ... running
✅ mammography-parsing        ... running
✅ mammography-structuring    ... running
✅ mammography-risk-prediction... running
✅ mammography-postgres       ... healthy
✅ mammography-redis          ... healthy
```

Check with:
```bash
docker-compose ps
```

---

## 🎯 Next Steps

1. Visit http://localhost:3000
2. Create a super admin account (see backend authentication README)
3. Upload a mammography report PDF
4. View structured results and risk predictions

For more details on each service, see `backend/<service-name>/README.md`.

---

**Need help?** Check the main `README.md` or open an issue.
