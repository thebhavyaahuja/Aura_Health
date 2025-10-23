# 🚀 Quick Reference - Backend Services

## Setup & Run (First Time)
```bash
cd backend
./setup_and_run.sh setup    # Install all dependencies
./setup_and_run.sh start    # Start all services
```

## Common Commands
```bash
./setup_and_run.sh status   # Check service status
./setup_and_run.sh logs     # View all logs
./setup_and_run.sh stop     # Stop all services
./setup_and_run.sh restart  # Restart all services
```

## Using Makefile (Alternative)
```bash
make setup-local     # Same as: ./setup_and_run.sh setup
make start-local     # Same as: ./setup_and_run.sh start
make stop-local      # Same as: ./setup_and_run.sh stop
make status-local    # Same as: ./setup_and_run.sh status
```

## Service Endpoints
- Authentication: http://localhost:8010/docs
- Document Ingestion: http://localhost:8001/docs
- Document Parsing: http://localhost:8002/docs
- Information Structuring: http://localhost:8003/docs

## View Service Logs
```bash
./setup_and_run.sh logs authentication        # Specific service
./setup_and_run.sh logs document-ingestion
./setup_and_run.sh logs document-parsing
./setup_and_run.sh logs information-structuring
```

## Troubleshooting
```bash
./setup_and_run.sh status   # Check what's running
./setup_and_run.sh clean    # Clean everything
./setup_and_run.sh setup    # Reinstall dependencies
./setup_and_run.sh start    # Start fresh
```

## Directory Structure
```
backend/
├── setup_and_run.sh           # Main script
├── logs/                      # All service logs
├── authentication/venv/       # Virtual environments
├── document-ingestion/venv/
├── document-parsing/venv/
└── information-structuring/venv/
```

---

📖 **Full Documentation**: See `SETUP_GUIDE.md` for complete details
