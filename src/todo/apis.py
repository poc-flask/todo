from datetime import datetime
from flask import abort
from flask_restful import(
    Resource,
    Api,
    reqparse,
    marshal,
    marshal_with,
    fields)
from flask_restful.inputs import boolean
from flask_jwt_extended import get_jwt_identity, jwt_required
from core.utils import date_time_parsing, SerializeDateTime
from core import api
from .models import Todo

resource_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'due_date': SerializeDateTime(attribute='due_date'),
    'completed': fields.Boolean,
    'completed_date': SerializeDateTime(attribute='completed_date'),
}

#################################################################
# TodoResource
# lets you GET/DELETE or UPDATE a Todo item
#################################################################

todo_parser = reqparse.RequestParser()
todo_parser.add_argument('title', type=str)
todo_parser.add_argument('due_date', type=date_time_parsing)
todo_parser.add_argument('completed', type=boolean)


class TodoResource(Resource):

    def get_todo(self, user_id, id):
        todo = Todo.query \
            .by_owner_and_id(user_id, id) \
            .first()
        if todo:
            return todo
        else:
            abort(404)

    @jwt_required
    @marshal_with(resource_fields)
    def get(self, id):
        user_id = get_jwt_identity()
        return self.get_todo(user_id, id)

    @jwt_required
    @marshal_with(resource_fields)
    def put(self, id):
        """
        Update a Todo item
        """
        data = todo_parser.parse_args()
        user_id = get_jwt_identity()
        todo = self.get_todo(user_id, id)
        todo.update(data)
        return todo

    @jwt_required
    def delete(self, id):
        """
        Delete a Todo item
        """
        user_id = get_jwt_identity()
        todo = self.get_todo(user_id, id)
        todo.delete()
        return {'message': 'OK'}


#################################################################
# TodoListResource
# lets you POST to create a Todo item
#################################################################

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('due_date', type=date_time_parsing)

class TodoListResource(Resource):

    @jwt_required
    def post(self):
        data = parser.parse_args()
        data['user_id'] = get_jwt_identity()
        todo = Todo.create_todo(data)
        return marshal(todo, resource_fields)


#################################################################
# CompletedTodoListResource
# lets you GET a list of completed todos
#################################################################

class CompletedTodoListResource(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self):
        user_id = get_jwt_identity()
        todos = Todo.query \
            .by_owner(user_id) \
            .completed().all()
        return todos


#################################################################
# UnCompletedTodoListResource
# lets you GET a list of completed todos
#################################################################

class UnCompletedTodoListResource(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self):
        user_id = get_jwt_identity()
        todos = Todo.query \
            .by_owner(user_id) \
            .uncompleted().all()
        return todos


# Register API
api.add_resource(TodoResource, '/todo/<id>')
api.add_resource(TodoListResource, '/todos')
api.add_resource(CompletedTodoListResource, '/todos/completed')
api.add_resource(UnCompletedTodoListResource, '/todos/uncompleted')
