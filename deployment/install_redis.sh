#!/bin/bash

# Redis installation and configuration script
# Redis is used for session management across multiple servers and Socket.IO message queue

echo "==================================="
echo "Installing Redis"
echo "==================================="

# Check if Redis is already installed
if command -v redis-server &> /dev/null; then
    echo "Redis is already installed"
    redis-server --version
else
    echo "Installing Redis..."
    
    # Update package list
    sudo apt update
    
    # Install Redis
    sudo apt install -y redis-server
    
    if [ $? -eq 0 ]; then
        echo "✓ Redis installed successfully!"
    else
        echo "✗ Error installing Redis"
        exit 1
    fi
fi

# Configure Redis
echo ""
echo "Configuring Redis..."

# Backup original config
sudo cp /etc/redis/redis.conf /etc/redis/redis.conf.backup

# Update Redis configuration for better performance and security
sudo sed -i 's/^supervised no/supervised systemd/' /etc/redis/redis.conf
sudo sed -i 's/^bind 127.0.0.1 ::1/bind 127.0.0.1/' /etc/redis/redis.conf

# Set maxmemory policy (useful for session management)
echo "maxmemory 256mb" | sudo tee -a /etc/redis/redis.conf
echo "maxmemory-policy allkeys-lru" | sudo tee -a /etc/redis/redis.conf

# Enable persistence
sudo sed -i 's/^save 900 1/save 900 1/' /etc/redis/redis.conf
sudo sed -i 's/^save 300 10/save 300 10/' /etc/redis/redis.conf
sudo sed -i 's/^save 60 10000/save 60 10000/' /etc/redis/redis.conf

# Restart Redis
echo ""
echo "Starting Redis service..."
sudo systemctl restart redis-server
sudo systemctl enable redis-server

# Verify Redis is running
if sudo systemctl is-active --quiet redis-server; then
    echo "✓ Redis is running!"
else
    echo "✗ Redis failed to start"
    exit 1
fi

# Test Redis connection
echo ""
echo "Testing Redis connection..."
if redis-cli ping | grep -q "PONG"; then
    echo "✓ Redis connection successful!"
else
    echo "✗ Redis connection failed"
    exit 1
fi

echo ""
echo "==================================="
echo "Redis Setup Complete!"
echo "==================================="
echo "Redis URL: redis://localhost:6379/0"
