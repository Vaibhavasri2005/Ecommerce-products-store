from flask import Blueprint, render_template, request
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio, db
from app.models import ChatMessage
import uuid

bp = Blueprint('chat', __name__)

# Store active chat sessions
active_sessions = {}

@bp.route('/')
def chat_page():
    """Chat interface page"""
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('connection_response', {'status': 'connected', 'sid': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'Client disconnected: {request.sid}')

@socketio.on('join_chat')
def handle_join_chat(data):
    """Handle user joining a chat session"""
    try:
        session_id = data.get('session_id')
        username = data.get('username', 'Guest')
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Join the room
        join_room(session_id)
        
        # Store session info
        active_sessions[request.sid] = {
            'session_id': session_id,
            'username': username
        }
        
        # Load previous messages for this session
        previous_messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
        messages = [msg.to_dict() for msg in previous_messages]
        
        emit('chat_joined', {
            'session_id': session_id,
            'username': username,
            'messages': messages
        })
        
        # Notify others in the room
        emit('user_joined', {
            'username': username,
            'message': f'{username} joined the chat'
        }, room=session_id, skip_sid=request.sid)
        
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('leave_chat')
def handle_leave_chat(data):
    """Handle user leaving a chat session"""
    try:
        session_id = data.get('session_id')
        username = data.get('username', 'Guest')
        
        leave_room(session_id)
        
        # Remove session info
        if request.sid in active_sessions:
            del active_sessions[request.sid]
        
        # Notify others in the room
        emit('user_left', {
            'username': username,
            'message': f'{username} left the chat'
        }, room=session_id)
        
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending a chat message"""
    try:
        session_id = data.get('session_id')
        message_text = data.get('message')
        username = data.get('username', 'Guest')
        is_support = data.get('is_support', False)
        
        if not session_id or not message_text:
            emit('error', {'message': 'Session ID and message are required'})
            return
        
        # Save message to database
        user_id = current_user.id if current_user.is_authenticated else None
        
        chat_message = ChatMessage(
            session_id=session_id,
            user_id=user_id,
            username=username,
            message=message_text,
            is_support=is_support
        )
        
        db.session.add(chat_message)
        db.session.commit()
        
        # Broadcast message to all users in the room
        emit('new_message', {
            'message': chat_message.to_dict()
        }, room=session_id)
        
        # Auto-reply from support bot if not a support message
        if not is_support:
            import time
            from datetime import datetime
            time.sleep(1)  # Small delay to simulate typing
            
            # Generate auto-response
            auto_response = generate_auto_response(message_text.lower())
            
            # Save support response
            support_message = ChatMessage(
                session_id=session_id,
                user_id=None,
                username='Support Bot',
                message=auto_response,
                is_support=True
            )
            
            db.session.add(support_message)
            db.session.commit()
            
            # Broadcast support response
            emit('new_message', {
                'message': support_message.to_dict()
            }, room=session_id)
        
    except Exception as e:
        db.session.rollback()
        emit('error', {'message': str(e)})

def generate_auto_response(message):
    """Generate automatic response based on message content"""
    message = message.lower()
    
    # Keyword-based responses
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! Welcome to E-Shop support. How can I assist you today?"
    
    elif any(word in message for word in ['order', 'track', 'tracking', 'delivery']):
        return "To track your order, please go to 'My Orders' in your account dashboard. You can view the status and tracking information there."
    
    elif any(word in message for word in ['return', 'refund', 'exchange']):
        return "We accept returns within 30 days of delivery. Please visit our Returns page for more information, or contact support@eshop.com for assistance."
    
    elif any(word in message for word in ['payment', 'pay', 'checkout']):
        return "We accept various payment methods including credit cards, debit cards, and digital wallets. All transactions are secure and encrypted."
    
    elif any(word in message for word in ['shipping', 'delivery', 'ship']):
        return "We offer free shipping on orders over $50. Standard delivery takes 3-5 business days. Express shipping is also available."
    
    elif any(word in message for word in ['product', 'item', 'stock', 'available']):
        return "You can check product availability on each product page. If an item is out of stock, you can sign up for restock notifications."
    
    elif any(word in message for word in ['cancel', 'cancellation']):
        return "Orders can be cancelled within 1 hour of placement. After that, please contact our support team for assistance."
    
    elif any(word in message for word in ['discount', 'coupon', 'promo', 'offer']):
        return "Check our Deals section for current promotions! Sign up for our newsletter to receive exclusive discount codes."
    
    elif any(word in message for word in ['help', 'support', 'assistance']):
        return "I'm here to help! You can ask me about orders, shipping, returns, payments, or any other questions about our store."
    
    elif any(word in message for word in ['thank', 'thanks']):
        return "You're welcome! Is there anything else I can help you with?"
    
    else:
        return "Thank you for your message! A support representative will assist you shortly. Meanwhile, you can explore our Help Center for quick answers."

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    try:
        session_id = data.get('session_id')
        username = data.get('username', 'Guest')
        is_typing = data.get('is_typing', False)
        
        # Broadcast typing status to others in the room
        emit('user_typing', {
            'username': username,
            'is_typing': is_typing
        }, room=session_id, skip_sid=request.sid)
        
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('support_request')
def handle_support_request(data):
    """Handle support request from user"""
    try:
        session_id = data.get('session_id')
        username = data.get('username', 'Guest')
        
        # Notify support team (in production, this would alert support staff)
        emit('support_alert', {
            'session_id': session_id,
            'username': username,
            'message': f'{username} requested support'
        }, room='support_room')  # Support staff would join this room
        
        # Confirm to user
        emit('support_notified', {
            'message': 'Support team has been notified. Someone will be with you shortly.'
        })
        
    except Exception as e:
        emit('error', {'message': str(e)})
