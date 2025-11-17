# 🗄️ SQLite Database Configuration - Docker Setup

## Overview

Your Docker setup uses **SQLite databases** for each backend service. Each database is stored in a **persistent Docker volume** to ensure data survives container restarts.

---

## 📊 Database Files

| Service | Database File | Docker Volume | Container Path |
|---------|--------------|---------------|----------------|
| Authentication | `auth.db` | `auth_data` | `/app/data/auth.db` |
| Document Ingestion | `database.db` | `ingestion_data` | `/app/data/database.db` |
| Document Parsing | `parsing.db` | `parsing_data` | `/app/data/parsing.db` |
| Information Structuring | `structuring.db` | `structuring_data` | `/app/data/structuring.db` |
| Risk Prediction | `predictions.db` | `risk_data` | `/app/data/predictions.db` |

---

## ✅ Why This Won't Mess Up Your Local Setup

1. **Isolated Storage**: Docker containers use their own volumes, completely separate from your local filesystem
2. **No Conflicts**: Your local SQLite files (if any) won't be touched by Docker
3. **Persistent Data**: Docker volumes ensure databases persist across:
   - Container restarts
   - Container rebuilds
   - System reboots (as long as volumes aren't deleted)

---

## 🔍 Managing Docker Volumes

### List All Volumes
```bash
docker volume ls | grep odomos-dsi
```

Expected output:
```
odomos-dsi_auth_data
odomos-dsi_ingestion_data
odomos-dsi_parsing_data
odomos-dsi_structuring_data
odomos-dsi_risk_data
odomos-dsi_ingestion_storage
odomos-dsi_parsing_storage
odomos-dsi_structuring_storage
```

### Inspect a Volume
```bash
docker volume inspect odomos-dsi_auth_data
```

### Backup a Database
```bash
# Copy database out of container
docker-compose exec authentication cp /app/data/auth.db /app/data/auth_backup_$(date +%Y%m%d).db

# Or copy to your local machine
docker cp mammography-authentication:/app/data/auth.db ./auth_backup.db
```

### Restore a Database
```bash
# Copy backup into container
docker cp ./auth_backup.db mammography-authentication:/app/data/auth.db

# Restart the service
docker-compose restart authentication
```

---

## 🗑️ Cleaning Up

### Remove All Data (Fresh Start)
```bash
# Stop containers and remove volumes
docker-compose down -v
```

⚠️ **Warning**: This deletes ALL database data!

### Remove Specific Volume
```bash
# Stop services first
docker-compose down

# Remove specific volume
docker volume rm odomos-dsi_auth_data

# Start again (will create fresh empty database)
docker-compose up
```

---

## 🔄 Switching Between Docker and Local

### Running Locally (Non-Docker)
Your local setup scripts (`setup_and_run.sh`) will create databases in:
```
backend/authentication/auth.db
backend/document-ingestion/database.db
backend/document-parsing/parsing.db
backend/information-structuring/structuring.db
backend/risk-prediction/predictions.db
```

These are **completely separate** from Docker volumes.

### Running with Docker
Docker creates databases in volumes:
```
docker volume: odomos-dsi_auth_data
  └─ /app/data/auth.db (inside container)
```

**No overlap or conflicts!**

---

## 📈 When to Migrate to PostgreSQL

Consider migrating if:
- **High concurrency**: Many simultaneous users/requests
- **Multi-container scaling**: Running multiple replicas of services
- **Replication needs**: Need database backups/replicas
- **Advanced features**: Need transactions, complex queries, full-text search

### How to Migrate

1. Uncomment PostgreSQL service in `docker-compose.yml`:
   ```yaml
   postgres:
     image: postgres:15-alpine
     environment:
       - POSTGRES_DB=mammography_db
       - POSTGRES_USER=admin
       - POSTGRES_PASSWORD=password
     ports:
       - "5432:5432"
     volumes:
       - postgres_data:/var/lib/postgresql/data
   ```

2. Update service environment variables:
   ```yaml
   environment:
     - DATABASE_URL=postgresql://admin:password@postgres:5432/mammography_db
   ```

3. Run migrations to create tables in PostgreSQL

---

## 🎯 Current Setup Advantages

✅ **Simple**: No database server to configure  
✅ **Fast**: SQLite is fast for small-to-medium workloads  
✅ **Portable**: Database files are just files  
✅ **Isolated**: Each service has its own database (microservice best practice)  
✅ **Persistent**: Docker volumes keep your data safe  
✅ **Zero conflicts**: Doesn't interfere with local development  

---

## 🛡️ Data Safety

Your data is safe because:

1. **Persistent Volumes**: Data survives container restarts
2. **Named Volumes**: Won't be deleted unless explicitly removed with `-v`
3. **Isolated from Host**: Local files are untouched
4. **Easy Backup**: Simple `docker cp` commands

To ensure maximum safety:
```bash
# Regular backups (add to cron)
docker-compose exec authentication cp /app/data/auth.db /app/data/auth_$(date +%Y%m%d).db
docker-compose exec risk-prediction cp /app/data/predictions.db /app/data/predictions_$(date +%Y%m%d).db
```

---

**Summary**: Your Docker setup is completely isolated from local development. SQLite databases are stored in Docker volumes, persist across restarts, and won't interfere with any local `.db` files you might create when running services locally.
