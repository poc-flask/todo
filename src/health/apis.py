from flask_restful import Resource
from core import api


class HealthResource(Resource):
    """
    Health check resource
    """
    def get(self):
        return "OK"

# Register the resource so the Load balancer can connect to this endpoint
# to check our service health.
api.add_resource(HealthResource, '/healthz')
