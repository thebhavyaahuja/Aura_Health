# 📦 Docker Setup - Files Added

This document summarizes all Docker-related files added to the project for containerized deployment.

---

## 🗂️ Files Created

### Root Level
- **`docker-compose.yml`** - Orchestrates all backend services, frontend, PostgreSQL, and Redis
- **`.env.example`** - Environment variables template for Docker deployment
- **`.env`** - Active environment variables (created from `.env.example`)
- **`DOCKER_SETUP.md`** - Complete Docker setup guide for users

### Backend Services

#### New Dockerfiles Created:
- **`backend/information-structuring/Dockerfile`** - Python 3.11 service with Gemini AI
- **`backend/risk-prediction/Dockerfile`** - Python 3.11 service with HuggingFace models

#### Existing Dockerfiles (already present):
- `backend/authentication/Dockerfile`
- `backend/document-ingestion/Dockerfile`
- `backend/document-parsing/Dockerfile`

#### Build Optimization:
- **`backend/.dockerignore`** - Excludes unnecessary files from Docker build context

### Frontend
- **`frontend/Dockerfile`** - Multi-stage build with pnpm for Next.js app
- **`frontend/.dockerignore`** - Excludes `node_modules`, `.next`, etc.

---

## 🔧 Service Configuration

### Backend Services & Ports
| Service | Port | Container Name | Dockerfile Location |
|---------|------|----------------|---------------------|
| Authentication | 8010 | mammography-authentication | `backend/authentication/Dockerfile` |
| Document Ingestion | 8001 | mammography-ingestion | `backend/document-ingestion/Dockerfile` |
| Document Parsing | 8002 | mammography-parsing | `backend/document-parsing/Dockerfile` |
| Information Structuring | 8003 | mammography-structuring | `backend/information-structuring/Dockerfile` |
| Risk Prediction | 8004 | mammography-risk-prediction | `backend/risk-prediction/Dockerfile` |

### Frontend
| Service | Port | Container Name | Dockerfile Location |
|---------|------|----------------|---------------------|
| Next.js Frontend | 3000 | mammography-frontend | `frontend/Dockerfile` |

### Infrastructure
| Service | Port | Container Name | Image |
|---------|------|----------------|-------|
| PostgreSQL | 5432 | mammography-postgres | `postgres:15-alpine` |
| Redis | 6379 | mammography-redis | `redis:7-alpine` |

---

## 🌐 Service Architecture

```
┌─────────────────────────────────────────┐
│    Frontend (Next.js) - Port 3000      │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────────┐  ┌────▼─────────────────────────┐
│ Authentication │  │   Backend Microservices      │
│   Port 8010    │  │   Ports: 8001-8004           │
└───┬────────────┘  └────┬─────────────────────────┘
    │                    │
    └────────┬───────────┘
             │
    ┌────────┴──────────┐
    │                   │
┌───▼──────┐      ┌─────▼─────┐
│ Postgres │      │   Redis   │
│   5432   │      │   6379    │
└──────────┘      └───────────┘
```

---

## 🚀 Quick Start Commands

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Build and Run
```bash
docker-compose up --build
```

### 3. Access Services
- Frontend: http://localhost:3000
- Backend APIs: http://localhost:8001-8004, 8010

### 4. View Logs
```bash
docker-compose logs -f
```

### 5. Stop Services
```bash
docker-compose down
```

---

## 📋 Environment Variables Required

### Critical (Must Set):
- **`GEMINI_API_KEY`** - Required for information-structuring service

### Optional (Have Defaults):
- `JWT_SECRET` - Auth secret (default provided, change for production)
- `GEMINI_MODEL` - AI model to use (default: `gemini-2.0-flash`)
- `LOG_LEVEL` - Logging verbosity (default: `INFO`)
- `CORS_ORIGINS` - CORS configuration (default: `*`)

---

## 🔄 Docker Compose Features

### Service Dependencies
Services start in proper order:
1. Infrastructure (Postgres, Redis)
2. Core services (Authentication, Ingestion)
3. Processing services (Parsing, Structuring)
4. Prediction service
5. Frontend

### Health Checks
- PostgreSQL: `pg_isready` check every 10s
- Redis: `redis-cli ping` check every 10s

### Data Persistence
Volumes created for persistent storage:
- `postgres_data` - Database data
- `ingestion_storage` - Uploaded files
- `parsing_storage` - Parsed documents
- `structuring_storage` - Structured results

### Auto-restart
All services configured with `restart: unless-stopped`

---

## 🎯 Next Steps After Docker Setup

1. **Configure API Keys**: Edit `.env` and add your `GEMINI_API_KEY`
2. **Start Services**: Run `docker-compose up --build`
3. **Create Admin User**: Follow backend authentication README
4. **Upload Test Report**: Use the frontend at http://localhost:3000
5. **Monitor Logs**: Use `docker-compose logs -f <service-name>`

---

## 📚 Additional Resources

- **Full Setup Guide**: [`DOCKER_SETUP.md`](./DOCKER_SETUP.md)
- **Backend Guide**: [`backend/SETUP_GUIDE.md`](./backend/SETUP_GUIDE.md)
- **Service READMEs**: Each service has its own README in `backend/<service-name>/README.md`

---

**Date Created**: November 16, 2025  
**Docker Compose Version**: 3.8  
**Python Base Image**: python:3.11-slim  
**Node Base Image**: node:18-alpine
