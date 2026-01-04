from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@bp.route('/products')
def products_page():
    """Products listing page"""
    return render_template('products.html')

@bp.route('/cart')
def cart_page():
    """Shopping cart page"""
    return render_template('cart.html')

@bp.route('/wishlist')
def wishlist_page():
    """Wishlist page"""
    return render_template('wishlist.html')

@bp.route('/checkout')
def checkout_page():
    """Checkout page"""
    return render_template('checkout.html')

@bp.route('/contact')
def contact_page():
    """Contact/Support page"""
    return render_template('contact.html')
