# E-Commerce Platform - Visual Architecture Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS / CLIENTS                          │
│                    (Web Browsers, Mobile)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX LOAD BALANCER                           │
│                        (Port 80/443)                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  • Round-Robin Load Balancing                           │   │
│  │  • Health Checks (max_fails=3, timeout=30s)             │   │
│  │  • WebSocket Support (Socket.IO)                        │   │
│  │  • Static File Serving                                  │   │
│  │  • SSL/TLS Termination                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
└───┬─────────────────┬─────────────────┬─────────────────────────┘
    │                 │                 │
    │ Forward         │ Forward         │ Forward
    │ to Server 1     │ to Server 2     │ to Server 3
    │                 │                 │
    ▼                 ▼                 ▼
┌─────────┐      ┌─────────┐      ┌─────────┐
│ SERVER 1│      │ SERVER 2│      │ SERVER 3│
│Port 5001│      │Port 5002│      │Port 5003│
├─────────┤      ├─────────┤      ├─────────┤
│ Flask   │      │ Flask   │      │ Flask   │
│ App     │      │ App     │      │ App     │
├─────────┤      ├─────────┤      ├─────────┤
│Gunicorn │      │Gunicorn │      │Gunicorn │
│4 workers│      │4 workers│      │4 workers│
├─────────┤      ├─────────┤      ├─────────┤
│Eventlet │      │Eventlet │      │Eventlet │
│Support  │      │Support  │      │Support  │
└────┬────┘      └────┬────┘      └────┬────┘
     │                │                │
     │                │                │
     └────────────────┼────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│   POSTGRESQL     │      │      REDIS       │
│   Port 5432      │      │    Port 6379     │
├──────────────────┤      ├──────────────────┤
│  • users         │      │  • Sessions      │
│  • products      │      │  • Cache         │
│  • cart_items    │      │  • Socket.IO     │
│  • wishlist      │      │    Message Queue │
│  • orders        │      └──────────────────┘
│  • chat_messages │
└──────────────────┘
```

## Request Flow Diagram

### Regular HTTP Request

```
User Browser
    │
    │ 1. HTTP GET /products
    ▼
Nginx Load Balancer
    │
    │ 2. Select server (Round-Robin)
    │    Request #1 → Server 1
    │    Request #2 → Server 2
    │    Request #3 → Server 3
    │    Request #4 → Server 1 (cycle repeats)
    ▼
Flask Application Server (Selected)
    │
    │ 3. Process request
    │
    ├─→ 4a. Query Database (if needed)
    │       PostgreSQL
    │       SELECT * FROM products
    │
    ├─→ 4b. Check Session (if needed)
    │       Redis
    │       GET session:user123
    │
    │ 5. Render response
    ▼
Return to Nginx
    │
    │ 6. Send response
    ▼
User Browser
    │
    │ 7. Display products
```

### WebSocket Connection (Chat)

```
User Opens Chat
    │
    │ 1. WebSocket handshake
    ▼
Nginx Load Balancer
    │
    │ 2. Upgrade to WebSocket
    │    Use ip_hash for sticky session
    ▼
Flask Server + Socket.IO
    │
    │ 3. Establish connection
    │
    ├─→ 4. Join chat room
    │       socket.emit('join_chat')
    │
User Sends Message
    │
    │ 5. Message event
    ▼
Flask Server
    │
    ├─→ 6a. Save to Database
    │       PostgreSQL
    │       INSERT INTO chat_messages
    │
    ├─→ 6b. Publish to Redis
    │       Redis Pub/Sub
    │       PUBLISH chat:messages
    │
    │ 7. All servers subscribed
    │    receive from Redis
    │
    └─→ 8. Broadcast to all connected clients
            socket.emit('new_message')
            
All Users Receive Message
```

## Load Balancing Visual

### Round-Robin Distribution

```
Time: T1
User Request → Nginx → Server 1 ✓

Time: T2
User Request → Nginx → Server 2 ✓

Time: T3
User Request → Nginx → Server 3 ✓

Time: T4
User Request → Nginx → Server 1 ✓ (cycle repeats)
```

### Server Failure Scenario

```
Normal State:
Server 1: ✓ Healthy
Server 2: ✓ Healthy
Server 3: ✓ Healthy
Nginx distributes: 33% | 33% | 33%

Server 2 Fails:
Server 1: ✓ Healthy
Server 2: ✗ Failed (max_fails exceeded)
Server 3: ✓ Healthy
Nginx distributes: 50% | 0% | 50%

Server 2 Recovers:
Server 1: ✓ Healthy
Server 2: ✓ Recovered
Server 3: ✓ Healthy
Nginx distributes: 33% | 33% | 33%
```

## Data Flow Diagram

### User Registration

```
User submits form
    │
    ▼
POST /auth/register
    │
    ▼
Flask validates data
    │
    ├─→ Check username exists?
    │       SELECT FROM users WHERE username = ?
    │
    ├─→ Check email exists?
    │       SELECT FROM users WHERE email = ?
    │
    ├─→ Hash password
    │       generate_password_hash()
    │
    └─→ Create user
            INSERT INTO users
    │
    ▼
Return success
```

### Shopping Cart Flow

```
User adds product to cart
    │
    ▼
POST /api/cart/add
    │
    ├─→ Check user logged in?
    │       Session in Redis
    │
    ├─→ Check product exists?
    │       SELECT FROM products WHERE id = ?
    │
    ├─→ Check stock available?
    │       product.stock_quantity > 0?
    │
    ├─→ Item already in cart?
    │       SELECT FROM cart_items
    │       WHERE user_id = ? AND product_id = ?
    │   
    │   Yes: UPDATE quantity
    │   No:  INSERT new cart_item
    │
    └─→ Return updated cart
            SELECT cart with products
```

### Checkout Process

```
User clicks "Place Order"
    │
    ▼
POST /api/checkout/process
    │
    ├─→ 1. Get user's cart
    │       SELECT cart_items WHERE user_id = ?
    │
    ├─→ 2. Validate stock for all items
    │       For each item:
    │       CHECK product.stock_quantity >= quantity
    │
    ├─→ 3. Calculate total
    │       SUM(price * quantity)
    │
    ├─→ 4. Create order
    │       INSERT INTO orders
    │
    ├─→ 5. Create order items
    │       For each cart item:
    │       INSERT INTO order_items
    │
    ├─→ 6. Update stock
    │       For each product:
    │       UPDATE products SET stock_quantity -= quantity
    │
    ├─→ 7. Clear cart
    │       DELETE FROM cart_items WHERE user_id = ?
    │
    └─→ 8. Return order confirmation
```

## Component Interaction

```
┌─────────────────┐
│   User Action   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Frontend (JS)  │─────▶│ Socket.IO    │
└────────┬────────┘      │ (Real-time)  │
         │               └──────────────┘
         │ AJAX/Fetch
         ▼
┌─────────────────┐
│  Flask Routes   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐  ┌──────┐
│Database│  │Redis │
│(Persist)  │(Cache)│
└────────┘  └──────┘
```

## Deployment Architecture

### Development Environment

```
┌──────────────────────────┐
│   Developer Machine      │
│                          │
│  ┌────────────────────┐ │
│  │  Flask Dev Server  │ │
│  │  Port 5001         │ │
│  └────────────────────┘ │
│           │              │
│  ┌────────┴────────┐    │
│  │                 │    │
│  ▼                 ▼    │
│ SQLite        No Redis  │
│ (or local     (optional)│
│  PostgreSQL)            │
└──────────────────────────┘
```

### Production Environment

```
┌───────────────────────────────────────────┐
│         Ubuntu Linux Server               │
│                                           │
│  ┌─────────────────────────────────────┐ │
│  │         Nginx (systemd)             │ │
│  │         Port 80/443                 │ │
│  └──────────┬──────────┬───────────────┘ │
│             │          │                  │
│  ┌──────────▼──┐  ┌───▼──────┐  ┌──────▼┐│
│  │ Server 1    │  │ Server 2 │  │Server 3││
│  │ (systemd)   │  │(systemd) │  │(systemd││
│  │ Port 5001   │  │Port 5002 │  │ 5003)  ││
│  └──────────┬──┘  └───┬──────┘  └──────┬─┘│
│             │         │               │   │
│             └─────────┼───────────────┘   │
│                       │                    │
│         ┌─────────────┴──────────┐        │
│         │                        │        │
│    ┌────▼─────┐           ┌─────▼────┐   │
│    │PostgreSQL│           │  Redis   │   │
│    │(systemd) │           │(systemd) │   │
│    └──────────┘           └──────────┘   │
└───────────────────────────────────────────┘
```

## Scaling Strategy

### Current: 3 Servers

```
Load: 1000 concurrent users
│
├─ Server 1: 333 users
├─ Server 2: 333 users
└─ Server 3: 334 users
```

### Scale to 6 Servers

```
Load: 2000 concurrent users
│
├─ Server 1: 333 users
├─ Server 2: 333 users
├─ Server 3: 333 users
├─ Server 4: 333 users
├─ Server 5: 333 users
└─ Server 6: 335 users

Just add to nginx.conf:
  server 127.0.0.1:5004;
  server 127.0.0.1:5005;
  server 127.0.0.1:5006;
```

## Security Layers

```
┌─────────────────────────────────┐
│    Firewall (UFW)               │
│    Allow: 80, 443, 22           │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│    Nginx                        │
│    • Rate Limiting              │
│    • SSL/TLS                    │
│    • Request Filtering          │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│    Flask Application            │
│    • CSRF Protection            │
│    • Input Validation           │
│    • SQL Injection Prevention   │
│    • XSS Protection             │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│    Database Layer               │
│    • Password Hashing           │
│    • Parameterized Queries      │
│    • Access Control             │
└─────────────────────────────────┘
```

---

## Legend

```
│  = Connection/Flow
▼  = Direction
┌─┐ = Container/Component
✓  = Healthy/Active
✗  = Failed/Inactive
→  = Data Flow
```

This visual guide helps understand:
- How components interact
- Request flow paths
- Load distribution
- Scaling approach
- Security layers
- Deployment structure

Use this alongside the README and ARCHITECTURE documents for complete understanding.
