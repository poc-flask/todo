"""Test Authentication API endpoint"""
import json
import requests

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


def test_login_success(client, fake):
    """Test create user."""
    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)

    rv = client.post('/auth', data=dict({
	    "username": email,
	    "password": pwd
    }), follow_redirects=True)

    assert rv.status_code == requests.codes.ok


def test_login_fail(client, fake):
    """Test create user."""
    email = fake.email()
    pwd = fake.password()
    user = create_user(client, fake, email, pwd)

    rv = client.post('/auth', data=dict({
	    "username": email,
	    "password": pwd + fake.password()
    }), follow_redirects=True)

    assert rv.status_code == requests.codes.unauthorized
