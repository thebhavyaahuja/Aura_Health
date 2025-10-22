#!/bin/bash
# Start Information Structuring Service with virtual environment

echo "🚀 Starting Information Structuring Service..."
echo "📁 Activating virtual environment..."

# Activate virtual environment
source venv_is/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "💡 Please create .env file with GEMINI_API_KEY"
    exit 1
fi

# Start the service
echo "🔧 Starting service..."
python3 run.py
