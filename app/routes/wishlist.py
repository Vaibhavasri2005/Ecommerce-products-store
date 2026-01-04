from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import WishlistItem, Product

bp = Blueprint('wishlist', __name__)

@bp.route('/', methods=['GET'])
@login_required
def get_wishlist():
    """Get user's wishlist"""
    try:
        wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
        items = [item.to_dict() for item in wishlist_items]
        
        return jsonify({
            'success': True,
            'wishlist_items': items,
            'item_count': len(items)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/add', methods=['POST'])
@login_required
def add_to_wishlist():
    """Add item to wishlist"""
    try:
        data = request.get_json()
        
        if 'product_id' not in data:
            return jsonify({'success': False, 'message': 'Product ID is required'}), 400
        
        product_id = int(data['product_id'])
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        # Check if item already in wishlist
        existing_item = WishlistItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if existing_item:
            return jsonify({'success': False, 'message': 'Item already in wishlist'}), 400
        
        # Create new wishlist item
        wishlist_item = WishlistItem(
            user_id=current_user.id,
            product_id=product_id
        )
        
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item added to wishlist',
            'wishlist_item': wishlist_item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_wishlist(item_id):
    """Remove item from wishlist"""
    try:
        wishlist_item = WishlistItem.query.filter_by(
            id=item_id,
            user_id=current_user.id
        ).first()
        
        if not wishlist_item:
            return jsonify({'success': False, 'message': 'Wishlist item not found'}), 404
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item removed from wishlist'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/clear', methods=['DELETE'])
@login_required
def clear_wishlist():
    """Clear all items from wishlist"""
    try:
        WishlistItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Wishlist cleared'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
