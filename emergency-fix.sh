#!/bin/bash

echo "🚀 EMERGENCY FIX - Running optimizations..."
echo ""
echo "This will:"
echo "1. Rebuild risk-prediction with model preload"
echo "2. Rebuild document-parsing with model preload  "
echo "3. Restart all services"
echo ""
echo "⏱️  Estimated time: 5-10 minutes"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

cd /Users/jallu/odomos-dsi

echo "📦 Step 1/4: Stopping services..."
docker-compose stop risk-prediction document-parsing information-structuring

echo "🏗️  Step 2/4: Rebuilding risk-prediction (BioGPT preload)..."
docker-compose build --no-cache risk-prediction

echo "🏗️  Step 3/4: Rebuilding document-parsing (Docling preload)..."
docker-compose build --no-cache document-parsing

echo "🚀 Step 4/4: Starting all services..."
docker-compose up -d

echo ""
echo "⏳ Waiting 15 seconds for services to stabilize..."
sleep 15

echo ""
echo "✅ DONE! Checking status..."
echo ""

docker-compose ps

echo ""
echo "🧪 Testing services..."
./diagnose.sh

echo ""
echo "✨ All set! Test at http://localhost:3000"
echo ""
echo "📊 Login credentials:"
echo "   Super Admin: super@gmail.com / pw"
echo "   Clinic Admin: admin@gmail.com / admin"
echo ""
