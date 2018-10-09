import os
from .config import DevelopmentConfig, ProductionConfig

def get_application_config():
    """
    Load configuration config base on Environement variable
    """
    # Load configuration
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'development':
        app_settings = DevelopmentConfig
    elif env == 'production':
        app_settings = ProductionConfig
    else:
        raise Exception('Unknow environment')

    return app_settings
