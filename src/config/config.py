import os
from datetime import timedelta

db_config = {
    'user_name': os.getenv('DB_USER_NAME', 'postgres'),
    'password': os.getenv('DB_PWD', 'postgres'),
    'db_host': os.getenv('DB_HOST', 'localhost'),
    'db_name': os.getenv('DB_NAME', 'api')
}
postgres_uri = 'postgresql://{user_name}:{password}@{db_host}/{db_name}'.format(**db_config)

class BaseConfig():
    """
    Base application configuration
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'invisible_key')
    JWT_SECRET_KEY = 'super-secret'
    # Config JWT expires time in minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 120))


class DevelopmentConfig(BaseConfig):
    """
    Configuration for development env
    """
    # Issue: If we use relative path the bin folder and flask app in src folder will point 2
    # different DB file.
    # Fixed: Convert DB file relative path to absolute path to put 
    # the bin folder outside of the src folder.

    db_path = os.path.abspath("../db.sqlite3")
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "sqlite:////%s" % db_path)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/postgis_test'

postgres_uri = 'postgresql://{user_name}:{password}@{db_host}/{db_name}'.format(**db_config)
# https://medium.com/@Umesh_Kafle/postgresql-and-postgis-installation-in-mac-os-87fa98a6814d
# sudo lsof -n -i4TCP:5432 | grep LISTEN

class ProductionConfig(BaseConfig):
    """
    Configuration for production env
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', postgres_uri)
