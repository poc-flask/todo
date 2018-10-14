from geoalchemy2 import Geometry
from core import db


class PointColumn(Geometry):

    def __init__(self, **kwargs):
        if 'use_st_prefix' in kwargs:
            kwargs.pop('use_st_prefix')

        kwargs['use_st_prefix'] = db.engine.name != 'sqlite'
        super().__init__(**kwargs)
