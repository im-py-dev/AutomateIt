import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read environment variables from .env file
FLASK_DEBUG = int(os.getenv('FLASK_DEBUG'))


def create_app():
    app = Flask(__name__)

    # Set up configuration
    if FLASK_DEBUG:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object('app.config.ProductionConfig')

    # Register blueprints here
    from .views.user.base import main_bp
    app.register_blueprint(main_bp)

    return app
