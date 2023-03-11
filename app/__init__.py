import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Load environment variables from .env file
load_dotenv()

# Read environment variables from .env file
FLASK_DEBUG = int(os.getenv('FLASK_DEBUG'))

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Login Manager
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Set up configuration
    if FLASK_DEBUG:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object('app.config.ProductionConfig')

    # Initialize database
    db.init_app(app)

    # Initialize login manager
    login_manager.init_app(app)

    # Set login view for login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'warning'

    # Register blueprints here
    from .views.user.base import main_bp
    app.register_blueprint(main_bp)

    return app