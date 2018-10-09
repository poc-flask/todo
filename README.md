# TODO Application Backend

This code base provides the backend apis for Todo application.

Project Organization
------------
    ├── bin                         <- Bash scripts to start flask server, migration tools.
    │
    ├── doc                         <- API documentation.
    │
    ├── src                         <- Contains all todo application's modules
    │   │
    │   ├── auth                    <- Authentication module
    │   │    │
    │   │    └── apis.py            <- Authentication Resource - Provide the authentication API
    │   │
    │   └── config                  <- Environments configuration
    │   │    │
    │   │    └── config.py          <- Configure environment for Development and Production
    │   │
    │   └── core                    <- Todo application core modules
    │   │    │
    │   │    └── create_app.py      <- Create flask application to using across this application.
    │   │    │
    │   │    └── models.py          <- Base models will be reused, inherited by other models.
    │   │    │
    │   │    └── utils.py           <- Application util functions.
    │   │
    │   └── migrations              <- Database migration files
    │   │
    │   ├── todo                    <- Todo module
    │   │    │
    │   │    └── apis.py            <- ToDo Resource - Provide the Todo API.
    │   │    │
    │   │    └── models.py          <- Todo models
    │   │
    │   ├── user                    <- User module
    │   │    │
    │   │    └── apis.py            <- User Resource - Provide API for User.
    │   │    │
    │   │    └── models.py          <- Todo models
    │   │
    │   └── manage.py               <- Flask application executation file.
    │
    ├── docker-compose.yml          <- Docker compose file to start containers: api and migrate.
    │
    ├── Dockerfile                  <- Docker build configuration file.
    │
    ├── local.env                   <- Local environment variable for docker compose.
    │
    ├── Procfile                    <- Heroku deployment file.
    |
    ├── README.md                   <- The top-level README for developers using this project.
    |
    └── requirements.txt            <- Python library is used in this project.

Development Environment setup for local
------------

### Pre-requirements

    - Git
    - Python 3.5.0
    - Docker

### Get Started

There are 2 ways to start the application on local.

### 1. By Docker

```
<!-- Migration data -->
docker-compose up migrate
<!-- Start flask application -->
docker-compose up api
```

### 2. Without Docker

The easiest way to work with the backend application is to run it as a standalone server.
You would need to install [Virtual Environment Wrapper](https://virtualenvwrapper.readthedocs.io).

To set up a new virtual environment

#### Step 1: Setup virtual environment

```
$ mkvirtualenv --python=`which python3` p-todo-app
```

To install all python dependencies

```
$ workon p-todo-app
$ pip install -r requirements.txt
```

#### Step 2: Setup the PYTHONPATH point to our application folder

Append the following statements to the ~/.bash_profile or any start up script in your system.

```
export PYTHONPATH="${TODO_APP_FOLDER}/app-api/:$PYTHONPATH"
```

then execute the bash profile.

```
$ source ~/.bash_profile
```

#### Step 3: Database migration

```
./bin/flask-upgrade.sh
```

#### Step 4: Start the application server

```
./bin/flask-run.sh
```

Technical Stack
------------

* [Flask](http://flask.pocoo.org)
    - Flask is a microframework for Python based on Werkzeug.

* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
    - Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application.

* [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)
    - SQLAlchemy database migrations for Flask applications using Alembic.

* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
    - Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.

* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
    - Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for your application.

* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
    - Flask-JWT-Extended is a Flask extension that provides JSON Web Token utils.

* [Psycopg](http://initd.org/psycopg/)
    - Psycopg is the most popular PostgreSQL adapter for the Python programming language.

* [Gunicorn](https://gunicorn.org/)
  * Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's used for heroku deployment.

Additional Documentations
------------
* [Todo Apis document](doc/index.md)