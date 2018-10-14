import os
import sqlite3
from sqlalchemy.event import listen
from sqlalchemy.engine import Engine


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    spatialite_lib_path = os.getenv('SPATIALITE_LIB_PATH', None)

    if type(dbapi_conn) is sqlite3.Connection:
        assert spatialite_lib_path, 'SQLite3 require spatialite ' \
            'extension to enable Gis feature.'

    # On MacOS:
    # Install: brew install spatialite-tools
    # SPATIALITE_LIB_PATH=/usr/local/lib/mod_spatialite.dylib

    # On Alpine:
    # Install: TBD
    # SPATIALITE_LIB_PATH=/usr/lib/x86_64-linux-gnu/libspatialite.so.5

    dbapi_conn.load_extension(spatialite_lib_path)
    dbapi_conn.enable_load_extension(False)


def load(engine):
    if engine.name == 'sqlite':
        listen(Engine, 'connect', load_spatialite)
