# 🛠️ Makefile for Backend Services
# Mammography Report Analysis System

.PHONY: help build up down logs clean test lint format

# Default target
help:
	@echo "🩺 Mammography Report Analysis - Backend Services"
	@echo ""
	@echo "Docker Commands:"
	@echo "  build          Build all Docker images"
	@echo "  up             Start all services with Docker"
	@echo "  down           Stop all Docker services"
	@echo "  logs           Show logs for all services"
	@echo "  clean          Clean up containers and volumes"
	@echo ""
	@echo "No-Docker Commands (uses setup_and_run.sh):"
	@echo "  setup-local    Setup all services without Docker"
	@echo "  start-local    Start all services without Docker"
	@echo "  stop-local     Stop all local services"
	@echo "  status-local   Show status of local services"
	@echo "  logs-local     Show logs for local services"
	@echo ""
	@echo "Development Commands:"
	@echo "  test           Run tests for all services"
	@echo "  lint           Run linting for all services"
	@echo "  format         Format code for all services"
	@echo ""
	@echo "Service-specific commands:"
	@echo "  build-ingestion    Build Document Ingestion service"
	@echo "  build-parsing      Build Document Parsing service"
	@echo "  build-structuring  Build Information Structuring service"
	@echo "  logs-ingestion     Show logs for Document Ingestion"
	@echo "  logs-parsing       Show logs for Document Parsing"
	@echo "  logs-structuring   Show logs for Information Structuring"
	@echo ""
	@echo "📖 For detailed setup guide, see: SETUP_GUIDE.md"

# Build all services
build:
	@echo "🔨 Building all Docker images..."
	docker-compose build

# Start all services
up:
	@echo "🚀 Starting all services..."
	docker-compose up -d

# Stop all services
down:
	@echo "🛑 Stopping all services..."
	docker-compose down

# Show logs
logs:
	@echo "📋 Showing logs for all services..."
	docker-compose logs -f

# Clean up
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run tests
test:
	@echo "🧪 Running tests for all services..."
	@for service in document-ingestion document-parsing information-structuring; do \
		echo "Testing $$service..."; \
		cd $$service && python -m pytest tests/ -v && cd ..; \
	done

# Run linting
lint:
	@echo "🔍 Running linting for all services..."
	@for service in document-ingestion document-parsing information-structuring; do \
		echo "Linting $$service..."; \
		cd $$service && flake8 app/ && cd ..; \
	done

# Format code
format:
	@echo "✨ Formatting code for all services..."
	@for service in document-ingestion document-parsing information-structuring; do \
		echo "Formatting $$service..."; \
		cd $$service && black app/ && isort app/ && cd ..; \
	done

# Service-specific builds
build-ingestion:
	@echo "🔨 Building Document Ingestion service..."
	docker-compose build document-ingestion

build-parsing:
	@echo "🔨 Building Document Parsing service..."
	docker-compose build document-parsing

build-structuring:
	@echo "🔨 Building Information Structuring service..."
	docker-compose build information-structuring

# Service-specific logs
logs-ingestion:
	@echo "📋 Showing logs for Document Ingestion..."
	docker-compose logs -f document-ingestion

logs-parsing:
	@echo "📋 Showing logs for Document Parsing..."
	docker-compose logs -f document-parsing

logs-structuring:
	@echo "📋 Showing logs for Information Structuring..."
	docker-compose logs -f information-structuring

# Development helpers
dev-setup:
	@echo "🛠️ Setting up development environment..."
	@echo "Creating virtual environments for each service..."
	@for service in document-ingestion document-parsing information-structuring; do \
		echo "Setting up $$service..."; \
		cd $$service && python -m venv venv && cd ..; \
	done
	@echo "✅ Development setup complete!"

install-deps:
	@echo "📦 Installing dependencies for all services..."
	@for service in document-ingestion document-parsing information-structuring; do \
		echo "Installing dependencies for $$service..."; \
		cd $$service && pip install -r requirements.txt && cd ..; \
	done

# No-Docker commands using setup_and_run.sh
setup-local:
	@./setup_and_run.sh setup

start-local:
	@./setup_and_run.sh start

stop-local:
	@./setup_and_run.sh stop

restart-local:
	@./setup_and_run.sh restart

status-local:
	@./setup_and_run.sh status

logs-local:
	@./setup_and_run.sh logs

clean-local:
	@./setup_and_run.sh clean
