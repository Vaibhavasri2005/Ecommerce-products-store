from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_name='development'):
    """Application factory pattern"""
    # Use parent directory for templates and static files
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    CORS(app)
    
    # Initialize SocketIO with Redis message queue for multi-server support
    socketio.init_app(
        app,
        message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'],
        cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS']
    )
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes import auth, products, cart, wishlist, checkout, chat, main
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(products.bp, url_prefix='/api/products')
    app.register_blueprint(cart.bp, url_prefix='/api/cart')
    app.register_blueprint(wishlist.bp, url_prefix='/api/wishlist')
    app.register_blueprint(checkout.bp, url_prefix='/api/checkout')
    app.register_blueprint(chat.bp, url_prefix='/chat')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
