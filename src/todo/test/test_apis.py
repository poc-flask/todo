"""Test ToDo API endpoint
We use requets.codes to verify the http status code return from api endpoint.
Please refer to https://github.com/requests/requests/blob/master/requests/status_codes.py
for all codes.
"""

import json
import requests

from todo.models import Todo


######################################################################
# Functions help to create user, todo items for testing purpose
######################################################################

def create_user(client, fake, email, pwd):
    """
    Create user for testing authentication
    """
    rv = client.post('/users', data=dict({
        "email": email,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": pwd
    }), follow_redirects=True)

    return json.loads(rv.data.decode('utf-8'))


def create_todo(client, fake, access_token):
    """
    Create a todo item
    """

    rv = client.post('/todos', 
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }),
        data=dict({
	        "title": fake.sentence(),
	        "due_date": fake.date_time().strftime('%Y-%m-%dT%H:%M:%S'),
    }), follow_redirects=True)
    return rv


def update_todo(client, fake, access_token, id, completed=False):
    """
    Update a todo item
    """

    data=dict({
        "title": fake.sentence(),
        "due_date": fake.date_time().strftime('%Y-%m-%dT%H:%M:%S'),
        "completed": completed})

    rv = client.put('/todo/%s' % id, 
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }),
        data=data, follow_redirects=True)
    return rv


def create_todo_list(client, fake):
    """Generate a list of todo items"""

    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)
    access_token = user['access_token']
    
    # Create a list of todo items
    todo_ids = []
    todo_count = 4
    for i in range(0, todo_count):
        rv = create_todo(client, fake, access_token)
        todo = json.loads(rv.data.decode('utf-8'))
        todo_ids.append(todo['id'])

    return (access_token, todo_ids)


######################################################################
# Testing section
######################################################################

def test_create_todo(client, fake,):
    """User can create a todo item"""

    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)
    access_token = user['access_token']
    rv = create_todo(client, fake, access_token)

    assert rv.status_code == requests.codes.ok


def test_create_todo_unauthorized(client, fake):
    """User can't create a todo item with invalid token"""

    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)
    invalid_access_token = user['access_token'] + "invalid"

    rv = create_todo(client, fake, invalid_access_token)

    assert rv.status_code == requests.codes.unprocessable_entity


def test_get_a_todo_item(client, fake):
    """User can see a todo item by id"""

    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)
    access_token = user['access_token']
    
    rv = create_todo(client, fake, access_token)
    todo = json.loads(rv.data.decode('utf-8'))

    # Make sure we receive the todo id
    id = todo.get('id', None)
    assert id

    # Retrieve todo by id
    rv = client.get('/todo/%s' % id, 
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }), follow_redirects=True)
    assert rv.status_code == requests.codes.ok


def test_get_not_exists_todo_item(client, fake):
    """User cant see a todo item by a non-exist id"""

    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)
    access_token = user['access_token']
    
    rv = create_todo(client, fake, access_token)
    todo = json.loads(rv.data.decode('utf-8'))

    # Make sure we receive the todo id
    id = todo.get('id', None)
    assert id

    # Retrieve todo by id
    rv = client.get('/todo/%s' % 0, 
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }), follow_redirects=True)

    assert rv.status_code == requests.codes.not_found


def test_update_a_todo_item(client, fake):
    """User can update a todo item"""

    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)
    access_token = user['access_token']

    rv = create_todo(client, fake, access_token)
    todo = json.loads(rv.data.decode('utf-8'))

    # Make sure we receive the todo id
    id = todo.get('id', None)
    assert id

    # Update a todo item
    rv = update_todo(client, fake, access_token, id, completed=fake.boolean())
    todo = json.loads(rv.data.decode('utf-8'))
    
    # Retrieve todo from DB
    todo_from_db = Todo.query.filter_by(id=id).first()
    
    # Check data is updated
    assert todo['title'] == todo_from_db.title
    assert todo['completed'] == todo_from_db.completed

    # Check http status code
    assert rv.status_code == requests.codes.ok


def test_delete_a_todo_item(client, fake):
    """User can delete a todo item"""

    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)
    access_token = user['access_token']
    
    rv = create_todo(client, fake, access_token)
    todo = json.loads(rv.data.decode('utf-8'))

    # Make sure we receive the todo id
    id = todo.get('id', None)
    assert id

    # Delete a todo item
    rv = client.delete('/todo/%s' % id, 
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }), follow_redirects=True)

    assert rv.status_code == requests.codes.ok

    # Make sure the item is deleted in database.
    todo_from_db = Todo.query.filter_by(id=id).first()
    assert todo_from_db == None
    

def test_get_completed_todo(client, fake):
    """User can see a list of completed todo item"""

    access_token, todo_ids = create_todo_list(client, fake)

    # Mark completed all todo items
    for i in range(0, len(todo_ids)):
        rv = update_todo(client, fake, access_token, todo_ids[i], completed=True)

    # Retrieve all completed todo items
    rv = client.get('/todos/completed', 
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }), follow_redirects=True)
    completed_todos = json.loads(rv.data.decode('utf-8'))

    # Check http status code
    assert rv.status_code == requests.codes.ok

    # Check data is updated
    completed_ids = [todo['id'] for todo in completed_todos if todo['completed'] == True]
    assert len(todo_ids) == len(completed_ids)
    assert todo_ids.sort() == completed_ids.sort()


def test_get_uncompleted_todo(client, fake):
    """User can see a list of uncompleted todo item"""

    access_token, todo_ids = create_todo_list(client, fake)

    # Mark completed all todo items
    for i in range(0, len(todo_ids)):
        rv = update_todo(client, fake, access_token, todo_ids[i], completed=False)

    # Retrieve all completed todo items
    rv = client.get('/todos/uncompleted', 
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }), follow_redirects=True)
    completed_todos = json.loads(rv.data.decode('utf-8'))

    # Check http status code
    assert rv.status_code == requests.codes.ok

    # Check data is updated
    completed_ids = [todo['id'] for todo in completed_todos if todo['completed'] == False]
    assert len(todo_ids) == len(completed_ids)
    assert todo_ids.sort() == completed_ids.sort()
