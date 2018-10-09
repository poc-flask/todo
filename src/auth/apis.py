from flask import abort
from flask_jwt_extended import create_access_token
from flask_restful import (
    Resource,
    reqparse
)

from core import api
from user.models import User

#################################################################
# Authentication Resource
#################################################################

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


class AuthenticationResource(Resource):
    def post(self):
        data = parser.parse_args()
        user = User.query.get_by_email(data['username'])
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        else:
            abort(401)


# Register API
api.add_resource(AuthenticationResource, '/auth')
