from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from sqlalchemy.event import listen

from .api import CoreApi
from .models import db
from .create_app import create_app
from .spatialite_extension import load as load_spatialite_extension

app = create_app(__name__)

# Configuration
# Create API
api = CoreApi(app)

# Sync up database
db.app = app
db.init_app(app)
load_spatialite_extension(db.engine)

bcrypt = Bcrypt()
bcrypt.init_app(app)

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

migrate = Migrate(app, db)
