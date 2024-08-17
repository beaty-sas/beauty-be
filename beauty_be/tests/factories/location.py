import factory

from beauty_be.models import Location
from beauty_be.tests.factories.base import BaseFactory


class LocationFactory(BaseFactory):
    name = factory.Faker('pystr')
    geom = factory.Faker('pyfloat')

    class Meta:
        model = Location
        sqlalchemy_session_persistence = 'commit'
