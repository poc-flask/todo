from flask import abort
from flask import request
from flask_restful import (
    Resource,
    fields,
    marshal_with,
    marshal,
    reqparse
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)


from core import api
from core.utils import resource_update_success

from .models import User


resource_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'access_token': fields.String
}


#################################################################
# UserResource
# show a single user
#################################################################


class UserResource(Resource):

    @marshal_with(resource_fields)
    def get(self, user_id):
        user = User.query.get_by_id(user_id)
        if user is None:
            abort(404)
        else:
            return user

#################################################################
# UserLocationResource
# update user current location
#################################################################

coordinate_parser = reqparse.RequestParser()
coordinate_parser.add_argument('lat', type=float)
coordinate_parser.add_argument('lng', type=float)
coordinate_parser.add_argument('radius', type=float)

location_resource_fields = {
    'id': fields.Integer,
    'lat': fields.Float,
    'lng': fields.Float,
    'first_name': fields.String,
    'last_name': fields.String
}


class UserLocationResource(Resource):

    @jwt_required
    def put(self):
        coordinate = coordinate_parser.parse_args()
        user_id = get_jwt_identity()

        user = User.query.get_by_id(user_id)
        user.update_location(**coordinate)

        return resource_update_success()

    @jwt_required
    @marshal_with(location_resource_fields)
    def get(self):
        """
        Return a list of user within radius in meteres.
        """
        args = request.args

        # Center point
        lat = float(args.get('lat', 0))
        lng = float(args.get('lng', 0))

        # Radius in meter
        radius = float(args.get('radius', 0))

        # Query user within radius from center point (lat, lng)
        users = User.query.filter_within_radius(lat, lng, radius).all()

        return users


#################################################################
# UserListResource
# lets you POST to create a new user
#################################################################

parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('first_name', type=str)
parser.add_argument('last_name', type=str)
parser.add_argument('password', type=str)


class UserListResource(Resource):

    def post(self):
        data = parser.parse_args()
        user = User.create_new_user(data)
        user.access_token = create_access_token(identity=user.id)
        return marshal(user, resource_fields)

# Register API
api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(UserLocationResource, '/user/location')
