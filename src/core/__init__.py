from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from sqlalchemy.event import listen

from .api import CoreApi
from .models import db
from .create_app import create_app

app = create_app(__name__)

# Configuration
# Create API
api = CoreApi(app)

# Sync up database
db.app = app
db.init_app(app)
print('debug')
print(type(db.engine))

def load_spatialite(dbapi_conn, connection_record):
    print('ahihi')
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/local/lib/mod_spatialite.dylib')

listen(db.engine, 'connect', load_spatialite)


bcrypt = Bcrypt()
bcrypt.init_app(app)

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

migrate = Migrate(app, db) # this
print(type(migrate))
