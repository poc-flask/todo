from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from core.models import db


class Lake(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type='POINT', management=True, use_st_prefix=False))

