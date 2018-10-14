"""Test user API endpoint"""
import json
import requests

from user.models import User


def create_user(client, fake):
    """Create a user."""
    rv = client.post('/users', data=dict({
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": fake.password()
    }), follow_redirects=True)

    return rv


def update_current_location(client, access_token):
    """Update user current location"""

    data = dict({
        'lat': 51.5112139,
        'lng': -0.1198244})

    rv = client.put(
        '/user/location',
        headers=dict({
           "Authorization": "Bearer %s" % access_token
        }),
        data=data)

    return rv


def test_create_user(client, fake):
    """Test create user."""
    rv = create_user(client, fake)
    user = json.loads(rv.data.decode('utf-8'))

    user_from_db = User.query.get_by_id(user['id'])

    # Make sure the password getter properties is protected
    try:
        user_from_db.password
    except AttributeError:
        assert True

    assert rv.status_code == requests.codes.ok


def test_get_user(client, fake):
    """Test get a user."""
    rv = create_user(client, fake)

    # Get access token
    user = json.loads(rv.data.decode('utf-8'))

    # Retrieve user information
    rv = client.get(
        '/user/%d' % user['id'],
        headers=dict({
           "Authorization": "Bearer %s" % user['access_token']
        }))

    assert rv.status_code == requests.codes.ok


def test_get_non_exists_user(client, fake):
    """Test get a user."""
    rv = create_user(client, fake)

    # Get access token
    user = json.loads(rv.data.decode('utf-8'))

    # Retrieve user information
    rv = client.get(
        '/user/0',
        headers=dict({
           "Authorization": "Bearer %s" % user['access_token']
        }))

    assert rv.status_code == requests.codes.not_found


def test_update_current_location(client, fake):
    rv = create_user(client, fake)

    # Get access token
    user = json.loads(rv.data.decode('utf-8'))

    # Update current location
    rv = update_current_location(client, user['access_token'])
    assert rv.status_code == requests.codes.ok


def search_user_within_radius(client, fake):

    rv = create_user(client, fake)

    # Get access token
    user = json.loads(rv.data.decode('utf-8'))

    # Update current location
    rv = update_current_location(client, user['access_token'])

    # Search users within radius
    uri = '/user/location?lat=%lat&lng=%lng&radius=%radius'.format(**{
        lat: 51.510912,
        lng: 0.123149,
        radius: 250
    })
    rv = client.get(
        uri,
        headers=dict({
           "Authorization": "Bearer %s" % user['access_token']
        }),
        data=data)

    assert rv.status_code == requests.codes.ok
    users = json.loads(rv.data.decode('utf-8'))
    assert len(users) == 1
