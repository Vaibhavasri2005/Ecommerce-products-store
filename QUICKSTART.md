# Quick Start Guide - E-Commerce Platform

## For Windows Development (Current Environment)

### 1. Install Prerequisites

1. **Install Python 3.8+**
   - Download from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH"

2. **Install PostgreSQL**
   - Download from https://www.postgresql.org/download/windows/
   - Remember the password you set for postgres user

3. **Install Redis**
   - Download from https://github.com/microsoftarchive/redis/releases
   - Or use Redis on WSL2 or Docker

### 2. Setup Project

```powershell
# Navigate to project directory
cd "C:\Users\vaibhava sri\Documents\Ecommerce project"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database

```powershell
# Create .env file from example
copy .env.example .env

# Edit .env file and update DATABASE_URL
# Example: DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce_db
notepad .env
```

Create database using pgAdmin or psql:
```sql
CREATE DATABASE ecommerce_db;
```

### 4. Initialize Database with Sample Data

```powershell
python seed_database.py
```

### 5. Run Development Server

#### Option 1: Single Server (Simple)
```powershell
python run.py
```
Access at: http://localhost:5001

#### Option 2: Multiple Servers (Load Balancing Test)

**Terminal 1:**
```powershell
$env:PORT="5001"; $env:SERVER_NAME="Server-1"
python run.py
```

**Terminal 2:**
```powershell
$env:PORT="5002"; $env:SERVER_NAME="Server-2"
python run.py
```

**Terminal 3:**
```powershell
$env:PORT="5003"; $env:SERVER_NAME="Server-3"
python run.py
```

### 6. Testing Without Nginx (Development)

You can test individual servers directly:
- Server 1: http://localhost:5001
- Server 2: http://localhost:5002
- Server 3: http://localhost:5003

## For Ubuntu/Linux Production Deployment

### Quick Deploy

```bash
# Clone or copy project to server
cd /opt
sudo git clone <your-repo> ecommerce
cd ecommerce

# Run automated setup (installs everything)
sudo chmod +x deployment/setup.sh
sudo deployment/setup.sh

# Seed database
python3 seed_database.py

# Start services
sudo systemctl start ecommerce-server1
sudo systemctl start ecommerce-server2
sudo systemctl start ecommerce-server3

# Check status
sudo systemctl status ecommerce-server1
```

### Manual Commands

```bash
# Start all servers using deployment script
chmod +x deployment/deploy.sh
./deployment/deploy.sh start

# Check health
python3 deployment/health_check.py

# View logs
tail -f /opt/ecommerce/logs/server1-access.log
```

## Default Login Credentials

After running `seed_database.py`:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test User Accounts:**
- Username: `john_doe`, Password: `password123`
- Username: `jane_smith`, Password: `password123`

## Testing the Application

1. **Register a new account** - Click "Account" → "Register"
2. **Browse products** - Go to "Products" page
3. **Add to cart** - Click "Add to Cart" on any product
4. **Manage wishlist** - Click heart icon to add to wishlist
5. **Checkout** - Go to cart and click "Proceed to Checkout"
6. **Live chat** - Click the chat button (bottom right)
7. **Contact support** - Visit "Contact" page

## Troubleshooting

### Issue: Cannot connect to database
**Solution:**
- Check PostgreSQL is running: `pg_ctl status` (Windows) or `sudo systemctl status postgresql` (Linux)
- Verify DATABASE_URL in .env file
- Check credentials are correct

### Issue: Redis connection error
**Solution:**
- Check Redis is running: `redis-cli ping` should return "PONG"
- Windows: Start Redis service or use WSL2
- Linux: `sudo systemctl start redis-server`

### Issue: Port already in use
**Solution:**
- Windows: `netstat -ano | findstr :5001`
- Linux: `sudo lsof -i :5001`
- Kill the process or use a different port

### Issue: Import errors
**Solution:**
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

## Project Structure Quick Reference

```
app/
├── __init__.py          # App factory
├── models.py            # Database models
└── routes/              # All API endpoints
    ├── auth.py         # Login/Register
    ├── products.py     # Product APIs
    ├── cart.py         # Cart management
    ├── wishlist.py     # Wishlist
    ├── checkout.py     # Order processing
    └── chat.py         # Real-time chat

templates/              # HTML pages
deployment/            # Setup scripts
nginx/                 # Load balancer config
```

## Next Steps

1. **Customize** - Modify templates, add more products
2. **Deploy** - Use deployment scripts for production
3. **Scale** - Add more servers to Nginx config
4. **Secure** - Enable HTTPS, change passwords
5. **Monitor** - Set up logging and monitoring

## Need Help?

- Check README.md for detailed documentation
- Review logs for error messages
- Test individual components separately

---

**Happy coding! 🚀**
