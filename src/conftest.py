import os

import pytest
from faker import Faker
import flask_migrate


from core import app
from todo.models import Todo


@pytest.fixture(scope="session")
def client():
    """
    Setup flask client in session scope to test API
    """

    # Delete test db file
    db_path = "./db_test.sqlite3"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create test db file and migration
    db_path = os.path.abspath(db_path)
    uri = "sqlite:////%s" % db_path
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        flask_migrate.upgrade(directory="src/migrations")

    return client

@pytest.fixture(scope="session")
def fake():
    """
    Initialize faker.Faker instance to generate dummy testing data such as: Name, Email,...
    """
    return Faker()
