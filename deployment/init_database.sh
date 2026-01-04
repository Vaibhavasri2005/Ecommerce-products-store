#!/bin/bash

# Database initialization script for E-Commerce Platform
# This script sets up the PostgreSQL database for the application

echo "==================================="
echo "E-Commerce Database Setup"
echo "==================================="

# Database configuration
DB_NAME="ecommerce_db"
DB_USER="ecommerce_user"
DB_PASSWORD="secure_password_here"
DB_HOST="localhost"
DB_PORT="5432"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Installing..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

echo "Creating database and user..."

# Switch to postgres user and create database
sudo -u postgres psql <<EOF
-- Create user if not exists
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;

-- Create database if not exists
SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

EOF

if [ $? -eq 0 ]; then
    echo "✓ Database created successfully!"
else
    echo "✗ Error creating database"
    exit 1
fi

# Update .env file
echo ""
echo "Updating .env file..."

if [ ! -f .env ]; then
    cp .env.example .env
fi

# Update database URL in .env
sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME|g" .env

echo "✓ Database configuration complete!"
echo ""
echo "Database Details:"
echo "  Name: $DB_NAME"
echo "  User: $DB_USER"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo ""
echo "Connection string has been updated in .env file"
