#!/usr/bin/env python3
"""
Sample data seeder for E-Commerce Platform
This script populates the database with sample products for testing
"""

import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product, User

def seed_database():
    """Seed database with sample data"""
    
    app = create_app('development')
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Create admin user
        print("\nCreating admin user...")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@eshop.com',
                full_name='Administrator',
                phone='+1-555-0000',
                address='123 Admin Street, Tech City'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Admin user created (username: admin, password: admin123)")
        else:
            print("Admin user already exists")
        
        # Create sample users
        print("\nCreating sample users...")
        sample_users = [
            {'username': 'john_doe', 'email': 'john@example.com', 'full_name': 'John Doe', 'password': 'password123'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'full_name': 'Jane Smith', 'password': 'password123'},
        ]
        
        for user_data in sample_users:
            user = User.query.filter_by(username=user_data['username']).first()
            if not user:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    full_name=user_data['full_name']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                print(f"✓ Created user: {user_data['username']}")
        
        # Sample products
        print("\nCreating sample products...")
        
        sample_products = [
            {
                'name': 'Laptop Pro 15',
                'description': 'High-performance laptop with 16GB RAM, 512GB SSD, and Intel Core i7 processor',
                'price': 1299.99,
                'category': 'Electronics',
                'stock_quantity': 25,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop'
            },
            {
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with precision tracking and long battery life',
                'price': 29.99,
                'category': 'Electronics',
                'stock_quantity': 100,
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=300&h=300&fit=crop'
            },
            {
                'name': 'Mechanical Keyboard',
                'description': 'RGB mechanical keyboard with blue switches and customizable lighting',
                'price': 89.99,
                'category': 'Electronics',
                'stock_quantity': 50,
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=300&h=300&fit=crop'
            },
            {
                'name': 'USB-C Hub',
                'description': '7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader, and power delivery',
                'price': 49.99,
                'category': 'Electronics',
                'stock_quantity': 75,
                'image_url': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=300&h=300&fit=crop'
            },
            {
                'name': 'Noise Cancelling Headphones',
                'description': 'Premium wireless headphones with active noise cancellation and 30-hour battery',
                'price': 249.99,
                'category': 'Audio',
                'stock_quantity': 40,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop'
            },
            {
                'name': 'Portable SSD 1TB',
                'description': 'Fast external SSD with USB 3.2 Gen 2 for quick file transfers',
                'price': 129.99,
                'category': 'Storage',
                'stock_quantity': 60,
                'image_url': 'https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=300&h=300&fit=crop'
            },
            {
                'name': 'Webcam HD 1080p',
                'description': 'Full HD webcam with auto-focus and built-in microphone',
                'price': 79.99,
                'category': 'Electronics',
                'stock_quantity': 45,
                'image_url': 'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=300&h=300&fit=crop'
            },
            {
                'name': 'Monitor 27" 4K',
                'description': '27-inch 4K UHD monitor with IPS panel and HDR support',
                'price': 399.99,
                'category': 'Electronics',
                'stock_quantity': 20,
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=300&h=300&fit=crop'
            },
            {
                'name': 'Desk Lamp LED',
                'description': 'Adjustable LED desk lamp with touch controls and USB charging port',
                'price': 39.99,
                'category': 'Office',
                'stock_quantity': 80,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop'
            },
            {
                'name': 'Laptop Stand Aluminum',
                'description': 'Ergonomic aluminum laptop stand with adjustable height and angle',
                'price': 44.99,
                'category': 'Office',
                'stock_quantity': 55,
                'image_url': 'https://images.unsplash.com/photo-1625225233840-695456021cde?w=300&h=300&fit=crop'
            },
            {
                'name': 'Wireless Charger',
                'description': 'Fast wireless charging pad compatible with Qi-enabled devices and wearables',
                'price': 24.99,
                'category': 'Accessories',
                'stock_quantity': 90,
                'image_url': 'https://images.unsplash.com/photo-1609712509268-f70f2a196f6c?w=300&h=300&fit=crop'
            },
            {
                'name': 'Bluetooth Speaker',
                'description': 'Portable Bluetooth speaker with 360-degree sound and waterproof design',
                'price': 69.99,
                'category': 'Audio',
                'stock_quantity': 65,
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=300&h=300&fit=crop'
            },
            {
                'name': 'Smart Watch',
                'description': 'Fitness tracker smart watch with heart rate monitor and GPS',
                'price': 199.99,
                'category': 'Wearables',
                'stock_quantity': 35,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop'
            },
            {
                'name': 'Phone Case Premium',
                'description': 'Protective phone case with shock absorption and slim design',
                'price': 19.99,
                'category': 'Accessories',
                'stock_quantity': 150,
                'image_url': 'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=300&h=300&fit=crop'
            },
            {
                'name': 'Cable Organizer Set',
                'description': 'Set of cable organizers and clips for desk cable management',
                'price': 14.99,
                'category': 'Office',
                'stock_quantity': 120,
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop'
            },
            {
                'name': 'Gaming Mouse Pad',
                'description': 'Large gaming mouse pad with smooth surface and anti-slip base',
                'price': 19.99,
                'category': 'Gaming',
                'stock_quantity': 85,
                'image_url': 'https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=300&h=300&fit=crop'
            }
        ]
        
        for product_data in sample_products:
            product = Product.query.filter_by(name=product_data['name']).first()
            if not product:
                product = Product(**product_data)
                db.session.add(product)
                print(f"✓ Created product: {product_data['name']}")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*50)
        print("Database seeded successfully!")
        print("="*50)
        print(f"\nTotal products: {Product.query.count()}")
        print(f"Total users: {User.query.count()}")
        print("\nSample login credentials:")
        print("  Admin - username: admin, password: admin123")
        print("  User  - username: john_doe, password: password123")
        print("  User  - username: jane_smith, password: password123")

if __name__ == '__main__':
    seed_database()
