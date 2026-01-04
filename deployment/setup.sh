#!/bin/bash

# Complete setup script for E-Commerce Platform on Ubuntu
# This script installs all dependencies and configures the system

echo "=========================================="
echo "E-Commerce Platform - Complete Setup"
echo "=========================================="

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo or as root"
    exit 1
fi

# Update system
echo ""
echo "Step 1: Updating system packages..."
apt update && apt upgrade -y

# Install Python and dependencies
echo ""
echo "Step 2: Installing Python and dependencies..."
apt install -y python3 python3-pip python3-venv python3-dev
apt install -y build-essential libpq-dev

# Install PostgreSQL
echo ""
echo "Step 3: Installing PostgreSQL..."
apt install -y postgresql postgresql-contrib
systemctl start postgresql
systemctl enable postgresql

# Install Redis
echo ""
echo "Step 4: Installing Redis..."
apt install -y redis-server
systemctl start redis-server
systemctl enable redis-server

# Install Nginx
echo ""
echo "Step 5: Installing Nginx..."
apt install -y nginx
systemctl start nginx
systemctl enable nginx

# Create project directory
echo ""
echo "Step 6: Setting up project directory..."
PROJECT_DIR="/opt/ecommerce"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Create virtual environment
echo ""
echo "Step 7: Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo ""
echo "Step 8: Installing Python packages..."
pip install --upgrade pip
pip install gunicorn eventlet

# Install project requirements (assuming requirements.txt is present)
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "✓ Python packages installed"
else
    echo "⚠ requirements.txt not found. Please copy project files and run: pip install -r requirements.txt"
fi

# Configure PostgreSQL
echo ""
echo "Step 9: Configuring database..."
sudo -u postgres psql <<EOF
CREATE USER ecommerce_user WITH PASSWORD 'secure_password_change_me';
CREATE DATABASE ecommerce_db OWNER ecommerce_user;
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
EOF

# Configure firewall
echo ""
echo "Step 10: Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw --force enable

# Create systemd service files for application servers
echo ""
echo "Step 11: Creating systemd service files..."

# Service for Server 1
cat > /etc/systemd/system/ecommerce-server1.service <<'EOF'
[Unit]
Description=E-Commerce Server 1
After=network.target postgresql.service redis-server.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/ecommerce
Environment="PATH=/opt/ecommerce/venv/bin"
Environment="PORT=5001"
Environment="SERVER_NAME=Server-1"
Environment="FLASK_ENV=production"
ExecStart=/opt/ecommerce/venv/bin/gunicorn --bind 0.0.0.0:5001 --workers 4 --worker-class eventlet --timeout 120 run:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Service for Server 2
cat > /etc/systemd/system/ecommerce-server2.service <<'EOF'
[Unit]
Description=E-Commerce Server 2
After=network.target postgresql.service redis-server.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/ecommerce
Environment="PATH=/opt/ecommerce/venv/bin"
Environment="PORT=5002"
Environment="SERVER_NAME=Server-2"
Environment="FLASK_ENV=production"
ExecStart=/opt/ecommerce/venv/bin/gunicorn --bind 0.0.0.0:5002 --workers 4 --worker-class eventlet --timeout 120 run:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Service for Server 3
cat > /etc/systemd/system/ecommerce-server3.service <<'EOF'
[Unit]
Description=E-Commerce Server 3
After=network.target postgresql.service redis-server.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/ecommerce
Environment="PATH=/opt/ecommerce/venv/bin"
Environment="PORT=5003"
Environment="SERVER_NAME=Server-3"
Environment="FLASK_ENV=production"
ExecStart=/opt/ecommerce/venv/bin/gunicorn --bind 0.0.0.0:5003 --workers 4 --worker-class eventlet --timeout 120 run:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

echo "✓ Systemd services created"

# Configure Nginx
echo ""
echo "Step 12: Configuring Nginx load balancer..."

# Backup default config
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup

# Copy Nginx configuration
if [ -f nginx/nginx.conf ]; then
    cp nginx/nginx.conf /etc/nginx/sites-available/ecommerce
    ln -sf /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Test Nginx configuration
    nginx -t
    
    if [ $? -eq 0 ]; then
        systemctl reload nginx
        echo "✓ Nginx configured successfully"
    else
        echo "✗ Nginx configuration error"
    fi
else
    echo "⚠ Nginx config file not found. Please configure manually."
fi

# Set permissions
echo ""
echo "Step 13: Setting permissions..."
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR

# Create log directories
mkdir -p /var/log/ecommerce
chown -R www-data:www-data /var/log/ecommerce

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy your project files to $PROJECT_DIR"
echo "2. Update .env file with your configuration"
echo "3. Initialize database: python3 run.py"
echo "4. Start services:"
echo "   sudo systemctl start ecommerce-server1"
echo "   sudo systemctl start ecommerce-server2"
echo "   sudo systemctl start ecommerce-server3"
echo "5. Enable services on boot:"
echo "   sudo systemctl enable ecommerce-server1"
echo "   sudo systemctl enable ecommerce-server2"
echo "   sudo systemctl enable ecommerce-server3"
echo ""
echo "Access your application at: http://your-server-ip"
echo ""
