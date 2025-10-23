#!/bin/bash

# 🚀 Setup and Run Backend Services Without Docker
# Mammography Report Analysis System
# Author: Backend Team
# Date: October 23, 2025

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Service definitions with their ports and directories
declare -A SERVICES=(
    ["authentication"]="8010"
    ["document-ingestion"]="8001"
    ["document-parsing"]="8002"
    ["information-structuring"]="8003"
)

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR"

# Log file
LOG_DIR="$BACKEND_DIR/logs"
mkdir -p "$LOG_DIR"

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to print section headers
print_header() {
    echo ""
    print_message "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "$CYAN" "  $1"
    print_message "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Function to check if Python 3 is installed
check_python() {
    print_header "🐍 Checking Python Installation"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_message "$GREEN" "✅ Python found: $PYTHON_VERSION"
        return 0
    else
        print_message "$RED" "❌ Python 3 is not installed!"
        print_message "$YELLOW" "Please install Python 3.8 or higher"
        exit 1
    fi
}

# Function to check if pip is installed
check_pip() {
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
        print_message "$GREEN" "✅ pip found: $PIP_VERSION"
        return 0
    else
        print_message "$RED" "❌ pip3 is not installed!"
        print_message "$YELLOW" "Please install pip3"
        exit 1
    fi
}

# Function to create virtual environment for a service
create_venv() {
    local service=$1
    local service_dir="$BACKEND_DIR/$service"
    local venv_dir="$service_dir/venv"
    
    print_message "$BLUE" "📦 Setting up virtual environment for $service..."
    
    if [ -d "$venv_dir" ]; then
        print_message "$YELLOW" "   Virtual environment already exists. Skipping creation."
    else
        cd "$service_dir"
        python3 -m venv venv
        print_message "$GREEN" "   ✅ Virtual environment created"
    fi
}

# Function to install dependencies for a service
install_dependencies() {
    local service=$1
    local service_dir="$BACKEND_DIR/$service"
    local venv_dir="$service_dir/venv"
    local requirements="$service_dir/requirements.txt"
    
    print_message "$BLUE" "📥 Installing dependencies for $service..."
    
    if [ ! -f "$requirements" ]; then
        print_message "$YELLOW" "   ⚠️  No requirements.txt found for $service. Skipping."
        return
    fi
    
    cd "$service_dir"
    source "$venv_dir/bin/activate"
    
    # Upgrade pip first
    pip install --upgrade pip > /dev/null 2>&1
    
    # Install dependencies
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_message "$GREEN" "   ✅ Dependencies installed successfully"
    else
        print_message "$RED" "   ❌ Failed to install dependencies"
        exit 1
    fi
    
    deactivate
}

# Function to setup a single service
setup_service() {
    local service=$1
    local service_dir="$BACKEND_DIR/$service"
    
    if [ ! -d "$service_dir" ]; then
        print_message "$YELLOW" "   ⚠️  Service directory not found: $service_dir. Skipping."
        return
    fi
    
    print_message "$MAGENTA" "\n🔧 Setting up: $service"
    echo "   Location: $service_dir"
    
    create_venv "$service"
    install_dependencies "$service"
}

# Function to setup all services
setup_all_services() {
    print_header "🛠️  Setting Up All Backend Services"
    
    for service in "${!SERVICES[@]}"; do
        setup_service "$service"
    done
    
    print_message "$GREEN" "\n✅ All services setup complete!"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on a port
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        print_message "$YELLOW" "   Killing process $pid on port $port"
        kill -9 $pid 2>/dev/null || true
        sleep 1
    fi
}

# Function to run a service
run_service() {
    local service=$1
    local port=${SERVICES[$service]}
    local service_dir="$BACKEND_DIR/$service"
    local venv_dir="$service_dir/venv"
    local log_file="$LOG_DIR/$service.log"
    
    if [ ! -d "$service_dir" ]; then
        print_message "$YELLOW" "   ⚠️  Service directory not found: $service. Skipping."
        return
    fi
    
    print_message "$BLUE" "🚀 Starting: $service on port $port"
    
    # Check if port is already in use
    if check_port $port; then
        print_message "$YELLOW" "   ⚠️  Port $port is already in use"
        read -p "   Kill existing process and restart? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill_port $port
        else
            print_message "$YELLOW" "   Skipping $service"
            return
        fi
    fi
    
    # Start the service
    cd "$service_dir"
    
    # Check if run.py exists
    if [ -f "run.py" ]; then
        source "$venv_dir/bin/activate"
        nohup python3 run.py > "$log_file" 2>&1 &
        local pid=$!
        echo $pid > "$LOG_DIR/$service.pid"
        print_message "$GREEN" "   ✅ Started with PID: $pid"
        print_message "$CYAN" "   📋 Logs: $log_file"
        deactivate
    else
        print_message "$RED" "   ❌ run.py not found for $service"
    fi
}

# Function to run all services
run_all_services() {
    print_header "🚀 Starting All Backend Services"
    
    # Start services in order (authentication first, then others)
    local services_order=("authentication" "document-ingestion" "document-parsing" "information-structuring")
    
    for service in "${services_order[@]}"; do
        if [[ -v SERVICES[$service] ]]; then
            run_service "$service"
            sleep 2  # Wait a bit before starting next service
        fi
    done
    
    print_message "$GREEN" "\n✅ All services started!"
    print_services_status
}

# Function to stop all services
stop_all_services() {
    print_header "🛑 Stopping All Backend Services"
    
    for service in "${!SERVICES[@]}"; do
        local pid_file="$LOG_DIR/$service.pid"
        
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            if ps -p $pid > /dev/null 2>&1; then
                print_message "$YELLOW" "Stopping $service (PID: $pid)..."
                kill $pid 2>/dev/null || true
                sleep 1
                # Force kill if still running
                if ps -p $pid > /dev/null 2>&1; then
                    kill -9 $pid 2>/dev/null || true
                fi
                rm "$pid_file"
                print_message "$GREEN" "   ✅ Stopped $service"
            else
                print_message "$YELLOW" "   Service $service not running"
                rm "$pid_file"
            fi
        else
            # Try to kill by port
            local port=${SERVICES[$service]}
            if check_port $port; then
                kill_port $port
                print_message "$GREEN" "   ✅ Stopped process on port $port"
            fi
        fi
    done
    
    print_message "$GREEN" "\n✅ All services stopped!"
}

# Function to show status of all services
print_services_status() {
    print_header "📊 Services Status"
    
    printf "%-30s %-10s %-10s %-10s\n" "SERVICE" "PORT" "STATUS" "PID"
    printf "%-30s %-10s %-10s %-10s\n" "-------" "----" "------" "---"
    
    for service in "${!SERVICES[@]}"; do
        local port=${SERVICES[$service]}
        local pid_file="$LOG_DIR/$service.pid"
        local status="❌ Stopped"
        local pid="-"
        
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            if ps -p $pid > /dev/null 2>&1; then
                status="✅ Running"
            else
                status="❌ Dead"
                rm "$pid_file"
            fi
        elif check_port $port; then
            status="✅ Running"
            pid=$(lsof -ti:$port)
        fi
        
        printf "%-30s %-10s %-10s %-10s\n" "$service" "$port" "$status" "$pid"
    done
    
    echo ""
    print_message "$CYAN" "Endpoints:"
    for service in "${!SERVICES[@]}"; do
        local port=${SERVICES[$service]}
        echo "  • $service: http://localhost:$port"
    done
}

# Function to tail logs
tail_logs() {
    local service=$1
    local log_file="$LOG_DIR/$service.log"
    
    if [ -z "$service" ]; then
        print_message "$YELLOW" "Usage: $0 logs <service-name>"
        echo "Available services:"
        for s in "${!SERVICES[@]}"; do
            echo "  • $s"
        done
        return
    fi
    
    if [ ! -f "$log_file" ]; then
        print_message "$RED" "Log file not found: $log_file"
        return
    fi
    
    print_message "$CYAN" "📋 Tailing logs for $service..."
    print_message "$YELLOW" "Press Ctrl+C to stop"
    echo ""
    tail -f "$log_file"
}

# Function to show all logs
show_all_logs() {
    print_header "📋 Recent Logs for All Services"
    
    for service in "${!SERVICES[@]}"; do
        local log_file="$LOG_DIR/$service.log"
        if [ -f "$log_file" ]; then
            print_message "$MAGENTA" "\n━━━ $service ━━━"
            tail -n 20 "$log_file"
        fi
    done
}

# Function to clean up
cleanup() {
    print_header "🧹 Cleaning Up"
    
    print_message "$YELLOW" "This will:"
    echo "  • Stop all running services"
    echo "  • Remove all virtual environments"
    echo "  • Clear all logs"
    echo ""
    read -p "Are you sure? (y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_message "$YELLOW" "Cleanup cancelled"
        return
    fi
    
    # Stop services
    stop_all_services
    
    # Remove virtual environments
    print_message "$YELLOW" "Removing virtual environments..."
    for service in "${!SERVICES[@]}"; do
        local venv_dir="$BACKEND_DIR/$service/venv"
        if [ -d "$venv_dir" ]; then
            rm -rf "$venv_dir"
            print_message "$GREEN" "   ✅ Removed venv for $service"
        fi
    done
    
    # Clear logs
    print_message "$YELLOW" "Clearing logs..."
    rm -rf "$LOG_DIR"/*
    print_message "$GREEN" "   ✅ Logs cleared"
    
    print_message "$GREEN" "\n✅ Cleanup complete!"
}

# Function to show help
show_help() {
    print_header "🩺 Mammography Report Analysis - Backend Services (No Docker)"
    
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  setup              Install dependencies for all services"
    echo "  start              Start all services"
    echo "  stop               Stop all services"
    echo "  restart            Restart all services"
    echo "  status             Show status of all services"
    echo "  logs [service]     Tail logs for a specific service or all services"
    echo "  clean              Stop services and clean up virtual environments"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup                    # Setup all services"
    echo "  $0 start                    # Start all services"
    echo "  $0 logs authentication      # Tail logs for authentication service"
    echo "  $0 status                   # Check status of all services"
    echo ""
    echo "Available Services:"
    for service in "${!SERVICES[@]}"; do
        local port=${SERVICES[$service]}
        echo "  • $service (Port: $port)"
    done
    echo ""
}

# Main script logic
main() {
    local command=${1:-help}
    
    case $command in
        setup)
            check_python
            check_pip
            setup_all_services
            ;;
        start)
            run_all_services
            ;;
        stop)
            stop_all_services
            ;;
        restart)
            stop_all_services
            sleep 2
            run_all_services
            ;;
        status)
            print_services_status
            ;;
        logs)
            if [ -z "$2" ]; then
                show_all_logs
            else
                tail_logs "$2"
            fi
            ;;
        clean)
            cleanup
            ;;
        help|*)
            show_help
            ;;
    esac
}

# Run main function
main "$@"
