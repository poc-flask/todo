from flask import Flask
from config import get_application_config

def create_app(name):
    app = Flask(__name__)
    # Load configuration
    app_settings = get_application_config()
    app.config.from_object(app_settings)

    return app
