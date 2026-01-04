from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, CartItem, Product

bp = Blueprint('checkout', __name__)

@bp.route('/process', methods=['POST'])
@login_required
def process_checkout():
    """Process checkout and create order"""
    try:
        data = request.get_json()
        
        # Get user's cart
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            return jsonify({'success': False, 'message': 'Cart is empty'}), 400
        
        # Calculate total
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Get shipping address
        shipping_address = data.get('shipping_address', current_user.address)
        if not shipping_address:
            return jsonify({'success': False, 'message': 'Shipping address is required'}), 400
        
        # Get payment method (not actually processing payment)
        payment_method = data.get('payment_method', 'Credit Card')
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            shipping_address=shipping_address,
            payment_method=payment_method,
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and update stock
        for cart_item in cart_items:
            # Check stock availability
            if cart_item.product.stock_quantity < cart_item.quantity:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Insufficient stock for {cart_item.product.name}'
                }), 400
            
            # Create order item
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update stock
            cart_item.product.stock_quantity -= cart_item.quantity
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    """Get user's order history"""
    try:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'orders': [order.to_dict() for order in orders]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """Get specific order details"""
    try:
        order = Order.query.filter_by(
            id=order_id,
            user_id=current_user.id
        ).first()
        
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'}), 404
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/payment-methods', methods=['GET'])
def get_payment_methods():
    """Get available payment methods (demo only)"""
    payment_methods = [
        {'id': 'credit_card', 'name': 'Credit Card', 'icon': 'credit-card'},
        {'id': 'debit_card', 'name': 'Debit Card', 'icon': 'credit-card'},
        {'id': 'paypal', 'name': 'PayPal', 'icon': 'paypal'},
        {'id': 'upi', 'name': 'UPI', 'icon': 'mobile'},
        {'id': 'cod', 'name': 'Cash on Delivery', 'icon': 'money-bill'}
    ]
    
    return jsonify({
        'success': True,
        'payment_methods': payment_methods
    }), 200
