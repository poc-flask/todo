from flask_sqlalchemy import BaseQuery
from shapely import wkb
from sqlalchemy import cast
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import query_expression, with_expression
from geoalchemy2 import Geometry, Geography, func
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from core import bcrypt
from core.models import db, TimestampMixin

#################################################
# User model and query set
#################################################


class UserQuery(BaseQuery):
    def get_by_id(self, id):
        return self.get(ident=id)

    def get_by_email(self, email):
        return self.filter_by(email=email).first()

    def filter_within_radius(self, lat, lng, radius):
        """
        Filter user within radius from a center (lat, lng) coordinate
        """
        # Define center point
        center_point = Point(lng, lat)
        wkb_element = from_shape(center_point, srid=4326)

        # Define expression to calculate distance from center point
        # to users location
        distance = User.location \
            .distance_centroid(wkb_element) \
            .cast(db.Float) \
            .label('distance')

        # Define lat, lng query set
        lat = func.ST_Y(cast(User.location, Geometry)).label('lat')
        lng = func.ST_X(cast(User.location, Geometry)).label('lng')

        # Filter user within radius from center point
        qs = User.query \
            .filter(func.ST_DWithin(User.location, wkb_element, radius))

        # Append Query-time SQL expressions distance as mapped attributes
        # https://docs.sqlalchemy.org/en/latest/orm/mapped_sql_expr.html
        qs = qs.options(
                with_expression(
                    User.distance, distance),
                with_expression(
                    User.lat, lat),
                with_expression(
                    User.lng, lng)
            )

        return qs


class User(db.Model, TimestampMixin):
    query_class = UserQuery
    id = db.Column(db.Integer, primary_key=True)
    todos = db.relationship('Todo', backref='user', lazy=True)

    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))

    first_name = db.Column(db.Unicode(100))
    last_name = db.Column(db.Unicode(100))

    auth_sub = db.Column(db.String(100))
    notifications_enabled = db.Column(db.Boolean())
    notifications_radius_meters = db.Column(db.Float())
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    expires_at = db.Column(db.DateTime())

    # Store last location of User. This properties is just used for postgis POC
    location = db.Column(Geography(
        geometry_type='POINT', management=True, use_st_prefix=True))

    # Distance from user current location to a coordinate
    distance = query_expression()
    lat = query_expression()
    lng = query_expression()

    @hybrid_property
    def coordinate(self):
        """
        Return (latitude, longitute) of the location property
        """
        point = wkb.loads(bytes(self.localtion.data))
        return (point.x, point.y)

    @property
    def password(self):
        raise AttributeError('password is a write only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt \
            .generate_password_hash(password) \
            .decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def create_new_user(cls, data):
        user = User.query.get_by_email(email=data['email'])

        if not user:
            new_user = User(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )

            db.session.add(new_user)
            db.session.commit()
            return new_user

    def update_location(self, lat, lng):
        wkb_element = from_shape(Point(lng, lat), srid=4326)
        self.location = wkb_element
        db.session.add(self)
        db.session.commit()
        return self
