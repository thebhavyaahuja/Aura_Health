# 🏥 Mammography Report Analysis - Backend Services

This directory contains all the microservices for the mammography report analysis system.

## 📁 Service Structure

```
backend/
├── document-ingestion/     # Document upload and file handling
├── document-parsing/       # OCR and text extraction using docling
├── information-structuring/ # LLM-based data structuring
├── feature-engineering/    # Feature preparation for ML models
├── risk-prediction/        # ML model inference and risk assessment
├── model-training/         # Model training and versioning
├── authentication/         # User authentication and authorization
├── api-gateway/           # Request routing and cross-cutting concerns
├── notification/          # Alerts and notifications
├── shared/                # Common utilities and shared code
├── infrastructure/        # Docker, K8s, and deployment configs
├── docs/                  # API documentation and architecture docs
├── setup_and_run.sh       # 🆕 Setup and run services without Docker
├── SETUP_GUIDE.md         # 🆕 Detailed setup documentation
└── QUICKSTART.md          # 🆕 Quick reference guide
```

## 🚀 Quick Start

### Option 1: Without Docker (Recommended for Development)

```bash
# Setup all services (first time only)
./setup_and_run.sh setup

# Start all services
./setup_and_run.sh start

# Check status
./setup_and_run.sh status

# View logs
./setup_and_run.sh logs

# Stop all services
./setup_and_run.sh stop
```

**📖 See [QUICKSTART.md](QUICKSTART.md) for quick reference or [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed documentation.**

### Option 2: With Docker

```bash
# Build and start all services
make build
make up

# View logs
make logs

# Stop services
make down
```

## 🎯 Active Services

1. **Authentication** (Port 8010)
   - User authentication and authorization
   - JWT token management

2. **Document Ingestion** (Port 8001)
   - File upload and validation
   - Document storage management

3. **Document Parsing** (Port 8002)
   - OCR and text extraction using docling
   - PDF processing

4. **Information Structuring** (Port 8003)
   - LLM-based data extraction
   - Structured data generation

## 🔮 Future Services

- `feature-engineering/` - Feature preparation
- `risk-prediction/` - ML inference
- `model-training/` - Model training pipeline
- `api-gateway/` - Request routing
- `notification/` - Alerts and notifications

## 🔧 Development Setup

### Using the Setup Script (No Docker)

```bash
# First time setup
./setup_and_run.sh setup

# Start development
./setup_and_run.sh start

# Each service will run with auto-reload enabled
```

### Using Makefile

```bash
# No-Docker commands
make setup-local      # Setup all services
make start-local      # Start all services
make stop-local       # Stop all services
make status-local     # Check status
make logs-local       # View logs

# Docker commands
make build           # Build Docker images
make up              # Start with Docker
make down            # Stop Docker services
```

## 📋 Service Endpoints

Once services are running, access the API documentation:

- Authentication: http://localhost:8010/docs
- Document Ingestion: http://localhost:8001/docs
- Document Parsing: http://localhost:8002/docs
- Information Structuring: http://localhost:8003/docs

## 📋 Service Dependencies

```
Client → Authentication → Document Ingestion → Document Parsing → Information Structuring → Feature Engineering → Risk Prediction → Notification
```

## 🧪 Testing

```bash
# Test specific service
cd <service-name>
source venv/bin/activate
pytest tests/ -v
deactivate
```

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick reference for common commands
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup and troubleshooting guide
- Individual service READMEs in each service directory

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test locally using `./setup_and_run.sh`
4. Submit a pull request
