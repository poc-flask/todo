from flask import abort
from flask_restful import (
    Resource,
    fields,
    marshal_with,
    marshal,
    reqparse)
from flask_jwt_extended import create_access_token

from core import api
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
