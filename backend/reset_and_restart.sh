#!/usr/bin/env bash

# 🔄 Reset and Restart Backend Services
# This script stops all services, cleans databases, and restarts everything

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR"

print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo ""
    print_message "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "$CYAN" "  $1"
    print_message "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Step 1: Stop all services
print_header "🛑 Step 1: Stopping All Services"
cd "$BACKEND_DIR"
./setup_and_run.sh stop || true

# Step 2: Clean all databases
print_header "🗑️  Step 2: Cleaning All Databases"

databases=(
    "authentication/auth.db"
    "document-ingestion/database.db"
    "document-parsing/parsing.db"
    "information-structuring/structuring.db"
    "risk-prediction/predictions.db"
)

for db in "${databases[@]}"; do
    db_path="$BACKEND_DIR/$db"
    if [ -f "$db_path" ]; then
        print_message "$YELLOW" "Removing: $db"
        rm "$db_path"
        print_message "$GREEN" "   ✅ Removed"
    else
        print_message "$BLUE" "   Not found: $db (skipping)"
    fi
done

# Step 3: Clean uploaded files (optional)
print_header "🗑️  Step 3: Cleaning Uploaded Files"

print_message "$YELLOW" "Do you want to clean uploaded files? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    storage_dirs=(
        "document-ingestion/storage/uploads/*"
        "document-ingestion/storage/temp/*"
        "document-parsing/storage/temp/*"
        "document-parsing/storage/parsed/*"
        "information-structuring/storage/results/*"
    )
    
    for dir in "${storage_dirs[@]}"; do
        full_path="$BACKEND_DIR/$dir"
        if [ -d "$(dirname "$full_path")" ]; then
            print_message "$YELLOW" "Cleaning: $dir"
            rm -rf $full_path 2>/dev/null || true
            print_message "$GREEN" "   ✅ Cleaned"
        fi
    done
else
    print_message "$BLUE" "Skipping file cleanup"
fi

# Step 4: Recreate super admin
print_header "👤 Step 4: Creating Super Admin User"
cd "$BACKEND_DIR/authentication"
if [ -d "venv" ]; then
    ./venv/bin/python create_super_admin.py
    print_message "$GREEN" "✅ Super admin created"
    print_message "$CYAN" "   Email: super@gmail.com"
    print_message "$CYAN" "   Password: pw"
else
    print_message "$RED" "❌ Authentication venv not found. Run setup first!"
fi

# Step 5: Configure risk-prediction to use HuggingFace model
print_header "🤗 Step 5: Configuring HuggingFace Model"
cd "$BACKEND_DIR/risk-prediction"

# Create or update .env file
if [ ! -f ".env" ]; then
    print_message "$YELLOW" "Creating .env file for risk-prediction..."
    cat > .env << 'EOF'
# Risk Prediction Service Configuration

# Model Configuration - Use HuggingFace Model
USE_HUGGINGFACE_MODEL=true
HUGGINGFACE_MODEL_REPO=ishro/biogpt-aura

# Database
DATABASE_URL=sqlite:///./predictions.db

# Logging
LOG_LEVEL=INFO
EOF
    print_message "$GREEN" "   ✅ .env file created"
else
    print_message "$YELLOW" "   .env file already exists"
fi

print_message "$GREEN" "✅ Configured to use HuggingFace model: ishro/biogpt-aura"

# Step 6: Restart all services
print_header "🚀 Step 6: Restarting All Services"
cd "$BACKEND_DIR"
./setup_and_run.sh start

# Wait a bit for services to start
sleep 3

# Step 7: Show status
print_header "📊 Final Status"
./setup_and_run.sh status

print_header "✨ Reset Complete!"
print_message "$GREEN" "All services have been reset and restarted."
print_message "$CYAN" "\nSuper Admin Credentials:"
print_message "$CYAN" "  Email: super@gmail.com"
print_message "$CYAN" "  Password: pw"
print_message "$YELLOW" "\nModel Configuration:"
print_message "$YELLOW" "  Using HuggingFace model: ishro/biogpt-aura"
print_message "$BLUE" "\nCheck logs with: ./setup_and_run.sh logs"

