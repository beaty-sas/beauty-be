from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from beauty_be.models.base import BaseModel


class Location(BaseModel):
    __tablename__ = 'locations'

    name = Column(String, nullable=False)
    geom = Column(Geometry('POINT', srid=4326))

    businesses = relationship('Business', back_populates='location')

    def __str__(self):
        return f'{self.id}: {self.name}'
