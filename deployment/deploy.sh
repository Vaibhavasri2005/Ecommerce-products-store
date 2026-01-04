#!/bin/bash

# Deployment script for E-Commerce Platform on Ubuntu servers
# This script sets up and starts multiple application server instances

echo "=========================================="
echo "E-Commerce Platform Deployment Script"
echo "=========================================="

# Configuration
PROJECT_DIR="/opt/ecommerce"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="$PROJECT_DIR/logs"
PID_DIR="$PROJECT_DIR/pids"

# Create necessary directories
echo "Creating directories..."
mkdir -p $LOG_DIR
mkdir -p $PID_DIR

# Function to start a server instance
start_server() {
    local server_num=$1
    local port=$2
    
    echo ""
    echo "Starting Server $server_num on port $port..."
    
    # Set environment variables
    export PORT=$port
    export SERVER_NAME="Server-$server_num"
    export FLASK_ENV=production
    
    # Start server with Gunicorn
    cd $PROJECT_DIR
    $VENV_DIR/bin/gunicorn \
        --bind 0.0.0.0:$port \
        --workers 4 \
        --worker-class eventlet \
        --timeout 120 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 50 \
        --access-logfile $LOG_DIR/server$server_num-access.log \
        --error-logfile $LOG_DIR/server$server_num-error.log \
        --pid $PID_DIR/server$server_num.pid \
        --daemon \
        "run:app"
    
    if [ $? -eq 0 ]; then
        echo "✓ Server $server_num started successfully on port $port"
    else
        echo "✗ Failed to start Server $server_num"
        return 1
    fi
}

# Function to stop servers
stop_servers() {
    echo "Stopping all server instances..."
    
    for pid_file in $PID_DIR/server*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat $pid_file)
            if ps -p $pid > /dev/null 2>&1; then
                kill $pid
                echo "✓ Stopped server with PID $pid"
            fi
            rm -f $pid_file
        fi
    done
}

# Function to check server status
check_status() {
    echo ""
    echo "Server Status:"
    echo "===================="
    
    for i in {1..3}; do
        port=$((5000 + i))
        pid_file="$PID_DIR/server$i.pid"
        
        if [ -f "$pid_file" ]; then
            pid=$(cat $pid_file)
            if ps -p $pid > /dev/null 2>&1; then
                echo "✓ Server $i (PID: $pid, Port: $port) - RUNNING"
            else
                echo "✗ Server $i - STOPPED (stale PID file)"
                rm -f $pid_file
            fi
        else
            echo "✗ Server $i - NOT RUNNING"
        fi
    done
}

# Main deployment logic
case "$1" in
    start)
        echo "Starting application servers..."
        
        # Start 3 server instances
        start_server 1 5001
        start_server 2 5002
        start_server 3 5003
        
        echo ""
        echo "All servers started!"
        check_status
        ;;
        
    stop)
        stop_servers
        echo "All servers stopped!"
        ;;
        
    restart)
        echo "Restarting servers..."
        stop_servers
        sleep 2
        $0 start
        ;;
        
    status)
        check_status
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
