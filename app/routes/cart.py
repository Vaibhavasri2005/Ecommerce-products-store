from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Product

bp = Blueprint('cart', __name__)

@bp.route('/', methods=['GET'])
@login_required
def get_cart():
    """Get user's shopping cart"""
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        items = [item.to_dict() for item in cart_items]
        
        total = sum(item['subtotal'] for item in items)
        
        return jsonify({
            'success': True,
            'cart_items': items,
            'total': total,
            'item_count': len(items)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    """Add item to shopping cart"""
    try:
        data = request.get_json()
        
        if 'product_id' not in data:
            return jsonify({'success': False, 'message': 'Product ID is required'}), 400
        
        product_id = int(data['product_id'])
        quantity = int(data.get('quantity', 1))
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        # Check stock availability
        if product.stock_quantity < quantity:
            return jsonify({'success': False, 'message': 'Insufficient stock'}), 400
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item added to cart',
            'cart_item': cart_item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/update/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        data = request.get_json()
        
        cart_item = CartItem.query.filter_by(
            id=item_id,
            user_id=current_user.id
        ).first()
        
        if not cart_item:
            return jsonify({'success': False, 'message': 'Cart item not found'}), 404
        
        quantity = int(data.get('quantity', 1))
        
        # Check stock availability
        if cart_item.product.stock_quantity < quantity:
            return jsonify({'success': False, 'message': 'Insufficient stock'}), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cart item updated',
            'cart_item': cart_item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.query.filter_by(
            id=item_id,
            user_id=current_user.id
        ).first()
        
        if not cart_item:
            return jsonify({'success': False, 'message': 'Cart item not found'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item removed from cart'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/clear', methods=['DELETE'])
@login_required
def clear_cart():
    """Clear all items from cart"""
    try:
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cart cleared'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
