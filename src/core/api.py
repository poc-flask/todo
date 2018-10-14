"""
Extend flask_restful.Api to add some enhancements.
This CoreApi will be using instead of flask_restful.Api
in this Todo application
"""
from flask_restful import Api, abort


class CoreApi(Api):

    """
    Handle exception
    """
    def handle_error(self, e):
        abort(e.code, str(e))
