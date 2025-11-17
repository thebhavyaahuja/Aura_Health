#!/bin/bash

# Quick rebuild script for optimized Docker containers
echo "🔧 Rebuilding optimized containers..."

# Stop all containers
echo "⏹️  Stopping containers..."
docker-compose down

# Rebuild only the services that need model preloading
echo "🏗️  Rebuilding risk-prediction with model preload..."
docker-compose build --no-cache risk-prediction

echo "🏗️  Rebuilding document-parsing with model preload..."
docker-compose build --no-cache document-parsing

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d

echo "✅ Done! Waiting for services to be healthy..."
sleep 10

# Show status
docker-compose ps

echo ""
echo "📊 Service URLs:"
echo "  - Frontend: http://localhost:3000"
echo "  - Authentication: http://localhost:8010"
echo "  - Document Ingestion: http://localhost:8001"
echo "  - Document Parsing: http://localhost:8002"
echo "  - Information Structuring: http://localhost:8003"
echo "  - Risk Prediction: http://localhost:8004"
echo ""
echo "🔍 Check logs with: docker-compose logs -f [service-name]"
