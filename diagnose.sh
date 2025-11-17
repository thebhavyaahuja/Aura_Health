#!/bin/bash

# Quick diagnostic script for Docker services
echo "🔍 Checking service health..."
echo ""

echo "📊 Service Status:"
docker-compose ps
echo ""

echo "🏥 Health Checks:"
services=("authentication:8010" "document-ingestion:8001" "document-parsing:8002" "information-structuring:8003" "risk-prediction:8004")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    echo -n "  $name ($port): "
    if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ HEALTHY"
    else
        echo "❌ NOT RESPONDING"
    fi
done

echo ""
echo "📜 Recent logs (last 20 lines per service):"
echo ""

for service in authentication document-ingestion document-parsing information-structuring risk-prediction; do
    echo "=== $service ==="
    docker-compose logs --tail=20 $service | tail -10
    echo ""
done
