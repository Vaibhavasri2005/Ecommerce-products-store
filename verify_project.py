#!/usr/bin/env python3
"""
Project verification script
Checks if all required files and dependencies are in place
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ {description} - MISSING: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ {description} - MISSING: {dirpath}")
        return False

def main():
    print("="*60)
    print("E-Commerce Platform - Project Verification")
    print("="*60)
    print()
    
    all_good = True
    
    # Check main files
    print("Checking main application files...")
    all_good &= check_file("run.py", "Application entry point")
    all_good &= check_file("config.py", "Configuration file")
    all_good &= check_file("requirements.txt", "Python dependencies")
    all_good &= check_file("seed_database.py", "Database seeder")
    all_good &= check_file(".env.example", "Environment template")
    all_good &= check_file("README.md", "Main documentation")
    all_good &= check_file("QUICKSTART.md", "Quick start guide")
    all_good &= check_file("ARCHITECTURE.md", "Architecture documentation")
    print()
    
    # Check app directory
    print("Checking app directory...")
    all_good &= check_directory("app", "App directory")
    all_good &= check_file("app/__init__.py", "App factory")
    all_good &= check_file("app/models.py", "Database models")
    print()
    
    # Check routes
    print("Checking route blueprints...")
    all_good &= check_directory("app/routes", "Routes directory")
    all_good &= check_file("app/routes/__init__.py", "Routes package init")
    all_good &= check_file("app/routes/main.py", "Main routes")
    all_good &= check_file("app/routes/auth.py", "Authentication routes")
    all_good &= check_file("app/routes/products.py", "Product routes")
    all_good &= check_file("app/routes/cart.py", "Cart routes")
    all_good &= check_file("app/routes/wishlist.py", "Wishlist routes")
    all_good &= check_file("app/routes/checkout.py", "Checkout routes")
    all_good &= check_file("app/routes/chat.py", "Chat routes")
    print()
    
    # Check templates
    print("Checking templates...")
    all_good &= check_directory("templates", "Templates directory")
    all_good &= check_file("templates/base.html", "Base template")
    all_good &= check_file("templates/index.html", "Home page")
    all_good &= check_file("templates/products.html", "Products page")
    all_good &= check_file("templates/cart.html", "Cart page")
    all_good &= check_file("templates/wishlist.html", "Wishlist page")
    all_good &= check_file("templates/checkout.html", "Checkout page")
    all_good &= check_file("templates/contact.html", "Contact page")
    all_good &= check_file("templates/chat.html", "Chat page")
    print()
    
    # Check static files
    print("Checking static files...")
    all_good &= check_directory("static", "Static directory")
    all_good &= check_directory("static/css", "CSS directory")
    all_good &= check_directory("static/js", "JavaScript directory")
    print()
    
    # Check deployment files
    print("Checking deployment scripts...")
    all_good &= check_directory("deployment", "Deployment directory")
    all_good &= check_file("deployment/setup.sh", "Setup script")
    all_good &= check_file("deployment/deploy.sh", "Deployment script")
    all_good &= check_file("deployment/init_database.sh", "Database init script")
    all_good &= check_file("deployment/install_redis.sh", "Redis install script")
    all_good &= check_file("deployment/health_check.py", "Health check script")
    all_good &= check_file("deployment/load_test.sh", "Load test script")
    print()
    
    # Check Nginx config
    print("Checking Nginx configuration...")
    all_good &= check_directory("nginx", "Nginx directory")
    all_good &= check_file("nginx/nginx.conf", "Nginx config file")
    print()
    
    # Check tests
    print("Checking test files...")
    all_good &= check_directory("tests", "Tests directory")
    all_good &= check_file("tests/test_app.py", "Application tests")
    print()
    
    # Check Python installation
    print("Checking Python environment...")
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"  ✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"  ✗ Python version too old. Need 3.8+, found {python_version.major}.{python_version.minor}")
        all_good = False
    print()
    
    # Final summary
    print("="*60)
    if all_good:
        print("✓ All files present! Project structure is complete.")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env file: cp .env.example .env")
        print("3. Initialize database: python seed_database.py")
        print("4. Run application: python run.py")
        print()
        print("For detailed instructions, see QUICKSTART.md")
        return 0
    else:
        print("✗ Some files are missing. Please check the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
