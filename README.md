# E-Commerce Platform - Load Balanced Web Application

A scalable, high-availability e-commerce web application with load balancing using Nginx, multiple Flask application servers, and real-time features.

## 🏗️ Architecture Overview

This application demonstrates a real-world scalable architecture:

```
                           Internet
                              |
                              v
                    ┌─────────────────┐
                    │  Nginx (Port 80) │
                    │  Load Balancer   │
                    └─────────────────┘
                            |
           ┌────────────────┼────────────────┐
           v                v                v
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ Server 1 │     │ Server 2 │     │ Server 3 │
    │ Port 5001│     │ Port 5002│     │ Port 5003│
    └──────────┘     └──────────┘     └──────────┘
           |                |                |
           └────────────────┼────────────────┘
                            v
                   ┌─────────────────┐
                   │   PostgreSQL    │
                   │    Database     │
                   └─────────────────┘
                            |
                   ┌─────────────────┐
                   │     Redis       │
                   │ Session Store   │
                   └─────────────────┘
```

### Key Features

- **Load Balancing**: Nginx distributes traffic across 3 application servers using round-robin
- **High Availability**: If one server fails, traffic automatically routes to healthy servers
- **Session Management**: Redis ensures session persistence across all servers
- **Real-time Chat**: WebSocket-based live chat with Socket.IO
- **Scalability**: Add more servers easily by updating Nginx configuration
- **Database Sharing**: All servers connect to a shared PostgreSQL database

## 🚀 Features

### User Features
- ✅ User Registration and Authentication
- ✅ Product Browsing with Search and Filters
- ✅ Shopping Cart Management
- ✅ Wishlist Functionality
- ✅ Checkout Process
- ✅ Payment Interface (Demo mode)
- ✅ Real-time Live Chat Support
- ✅ Contact and Call Options
- ✅ Order History

### Technical Features
- ✅ RESTful API Architecture
- ✅ Load Balancing with Nginx
- ✅ Multiple Application Server Instances
- ✅ Shared Database Architecture
- ✅ Redis for Session Management
- ✅ WebSocket for Real-time Communication
- ✅ Responsive Bootstrap UI
- ✅ Server Health Monitoring
- ✅ Zero-downtime Deployment Ready

## 📋 Prerequisites

- Ubuntu Linux (20.04 or later)
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Nginx 1.18+

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ecommerce-project
```

### 2. Automated Setup (Recommended)

Run the automated setup script (requires sudo):

```bash
sudo chmod +x deployment/setup.sh
sudo deployment/setup.sh
```

This script will:
- Install all system dependencies
- Set up PostgreSQL database
- Install and configure Redis
- Configure Nginx load balancer
- Create systemd service files
- Set up the project directory

### 3. Manual Setup

If you prefer manual installation:

#### Install System Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server
```

#### Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure Database

```bash
chmod +x deployment/init_database.sh
./deployment/init_database.sh
```

#### Configure Redis

```bash
chmod +x deployment/install_redis.sh
./deployment/install_redis.sh
```

### 4. Environment Configuration

Copy and configure the environment file:

```bash
cp .env.example .env
nano .env
```

Update the following variables:
```
DATABASE_URL=postgresql://ecommerce_user:your_password@localhost:5432/ecommerce_db
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379/0
```

### 5. Initialize Database

Seed the database with sample data:

```bash
python3 seed_database.py
```

## 🚀 Running the Application

### Method 1: Using Deployment Script

```bash
# Start all servers
chmod +x deployment/deploy.sh
./deployment/deploy.sh start

# Check status
./deployment/deploy.sh status

# Restart servers
./deployment/deploy.sh restart

# Stop servers
./deployment/deploy.sh stop
```

### Method 2: Using Systemd Services

```bash
# Start individual servers
sudo systemctl start ecommerce-server1
sudo systemctl start ecommerce-server2
sudo systemctl start ecommerce-server3

# Enable on boot
sudo systemctl enable ecommerce-server1
sudo systemctl enable ecommerce-server2
sudo systemctl enable ecommerce-server3

# Check status
sudo systemctl status ecommerce-server1
```

### Method 3: Manual Start (Development)

```bash
# Terminal 1 - Server 1
export PORT=5001 SERVER_NAME=Server-1
python3 run.py

# Terminal 2 - Server 2
export PORT=5002 SERVER_NAME=Server-2
python3 run.py

# Terminal 3 - Server 3
export PORT=5003 SERVER_NAME=Server-3
python3 run.py
```

### Configure Nginx

```bash
# Copy Nginx configuration
sudo cp nginx/nginx.conf /etc/nginx/sites-available/ecommerce
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## 🌐 Accessing the Application

Once all services are running:

- **Main Application**: http://localhost or http://your-server-ip
- **Direct Server Access** (for testing):
  - Server 1: http://localhost:5001
  - Server 2: http://localhost:5002
  - Server 3: http://localhost:5003

### Default Credentials

```
Admin Account:
Username: admin
Password: admin123

Test User Accounts:
Username: john_doe
Password: password123

Username: jane_smith
Password: password123
```

## 🧪 Testing Load Balancing

### Test 1: Manual Server Rotation

```bash
# Make multiple requests and check which server responds
for i in {1..10}; do
  curl -s http://localhost/ | grep "Server"
done
```

### Test 2: Server Failure Simulation

```bash
# Stop one server
sudo systemctl stop ecommerce-server2

# Application should still work via other servers
curl http://localhost/

# Restart the server
sudo systemctl start ecommerce-server2
```

### Test 3: Load Testing (using Apache Bench)

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Run load test
ab -n 1000 -c 10 http://localhost/
```

## 📊 Monitoring

### Check Server Logs

```bash
# Application logs
tail -f /opt/ecommerce/logs/server1-access.log
tail -f /opt/ecommerce/logs/server1-error.log

# Nginx logs
tail -f /var/log/nginx/ecommerce_access.log
tail -f /var/log/nginx/ecommerce_error.log

# System logs
sudo journalctl -u ecommerce-server1 -f
```

### Nginx Status

Access http://localhost/nginx_status (from localhost only)

### Monitor Redis

```bash
redis-cli
> INFO
> MONITOR
```

### Monitor Database

```bash
sudo -u postgres psql -d ecommerce_db
\dt  -- List tables
\d+ users  -- Describe users table
SELECT count(*) FROM users;
```

## 📁 Project Structure

```
ecommerce-project/
│
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   └── routes/               # API routes
│       ├── auth.py           # Authentication
│       ├── products.py       # Product management
│       ├── cart.py           # Shopping cart
│       ├── wishlist.py       # Wishlist
│       ├── checkout.py       # Checkout process
│       ├── chat.py           # Real-time chat
│       └── main.py           # Main routes
│
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── products.html        # Product listing
│   ├── cart.html            # Shopping cart
│   ├── wishlist.html        # Wishlist
│   ├── checkout.html        # Checkout page
│   ├── contact.html         # Contact page
│   └── chat.html            # Live chat
│
├── static/                   # Static files (CSS, JS, images)
│
├── deployment/              # Deployment scripts
│   ├── setup.sh            # Complete setup script
│   ├── deploy.sh           # Deployment script
│   ├── init_database.sh    # Database initialization
│   └── install_redis.sh    # Redis installation
│
├── nginx/
│   └── nginx.conf          # Nginx configuration
│
├── config.py               # Application configuration
├── run.py                  # Application entry point
├── seed_database.py        # Database seeder
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 Configuration

### Nginx Load Balancer

Edit `nginx/nginx.conf` to:
- Add/remove backend servers
- Change load balancing algorithm (round-robin, least_conn, ip_hash)
- Configure SSL/TLS
- Adjust timeout values

### Application Servers

Edit `config.py` to adjust:
- Database connection
- Session settings
- Upload limits
- Security settings

### Scaling

To add more servers:

1. Start new server instance:
```bash
gunicorn --bind 0.0.0.0:5004 --workers 4 --worker-class eventlet run:app
```

2. Add to Nginx configuration:
```nginx
upstream ecommerce_backend {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
    server 127.0.0.1:5004;  # New server
}
```

3. Reload Nginx:
```bash
sudo systemctl reload nginx
```

## 🔐 Security Considerations

- Change default passwords in production
- Use HTTPS (SSL/TLS) in production
- Configure firewall rules
- Enable Redis authentication
- Use environment variables for sensitive data
- Implement rate limiting
- Regular security updates

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :5001
# Kill process
sudo kill -9 <PID>
```

### Database Connection Error

```bash
# Check PostgreSQL status
sudo systemctl status postgresql
# Check database exists
sudo -u postgres psql -l
```

### Redis Connection Error

```bash
# Check Redis status
sudo systemctl status redis-server
# Test connection
redis-cli ping
```

### Nginx Configuration Error

```bash
# Test configuration
sudo nginx -t
# Check error logs
sudo tail -f /var/log/nginx/error.log
```

## 📝 API Endpoints

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - User login
- POST `/auth/logout` - User logout
- GET `/auth/current-user` - Get current user

### Products
- GET `/api/products/` - Get all products
- GET `/api/products/<id>` - Get single product
- GET `/api/products/categories` - Get categories

### Cart
- GET `/api/cart/` - Get cart items
- POST `/api/cart/add` - Add to cart
- PUT `/api/cart/update/<id>` - Update quantity
- DELETE `/api/cart/remove/<id>` - Remove item

### Wishlist
- GET `/api/wishlist/` - Get wishlist
- POST `/api/wishlist/add` - Add to wishlist
- DELETE `/api/wishlist/remove/<id>` - Remove item

### Checkout
- POST `/api/checkout/process` - Process order
- GET `/api/checkout/orders` - Get order history

## 🎯 Performance Optimization

- Database connection pooling
- Redis caching for sessions
- Gzip compression in Nginx
- Static file caching
- CDN integration ready
- Database query optimization
- Lazy loading for images

## 📚 Technologies Used

- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **Cache/Session**: Redis
- **Load Balancer**: Nginx
- **App Server**: Gunicorn with Eventlet
- **Real-time**: Socket.IO
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Deployment**: Ubuntu Linux, Systemd

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is created for educational purposes.

## 👥 Support

For issues and questions:
- Check the troubleshooting section
- Review application logs
- Contact: support@eshop.com

## 🎓 Educational Value

This project demonstrates:
- Horizontal scaling with load balancing
- Shared database architecture
- Session management across servers
- Real-time communication
- RESTful API design
- Production deployment practices
- High availability principles
- Cloud-ready architecture

---

**Built with ❤️ for learning scalable web architecture**
