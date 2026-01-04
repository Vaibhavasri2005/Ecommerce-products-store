"""
Test suite for E-Commerce Platform
Run with: pytest tests/
"""

import pytest
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Product, CartItem

@pytest.fixture
def app():
    """Create test application"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    """Create a sample user"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            full_name='Test User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def sample_product(app):
    """Create a sample product"""
    with app.app_context():
        product = Product(
            name='Test Product',
            description='Test Description',
            price=99.99,
            category='Test',
            stock_quantity=10
        )
        db.session.add(product)
        db.session.commit()
        return product

class TestAuth:
    """Test authentication endpoints"""
    
    def test_register(self, client):
        """Test user registration"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        })
        assert response.status_code == 201
        assert response.json['success'] == True
    
    def test_login(self, client, sample_user):
        """Test user login"""
        response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert response.json['success'] == True
    
    def test_invalid_login(self, client):
        """Test login with invalid credentials"""
        response = client.post('/auth/login', json={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401

class TestProducts:
    """Test product endpoints"""
    
    def test_get_products(self, client, sample_product):
        """Test getting product list"""
        response = client.get('/api/products/')
        assert response.status_code == 200
        assert response.json['success'] == True
        assert len(response.json['products']) > 0
    
    def test_get_single_product(self, client, sample_product):
        """Test getting single product"""
        response = client.get(f'/api/products/{sample_product.id}')
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['product']['name'] == 'Test Product'

class TestCart:
    """Test shopping cart endpoints"""
    
    def test_add_to_cart(self, client, sample_user, sample_product):
        """Test adding item to cart"""
        # Login first
        client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.post('/api/cart/add', json={
            'product_id': sample_product.id,
            'quantity': 1
        })
        assert response.status_code == 200
        assert response.json['success'] == True
    
    def test_get_cart(self, client, sample_user):
        """Test getting cart contents"""
        # Login first
        client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/api/cart/')
        assert response.status_code == 200
        assert response.json['success'] == True

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
