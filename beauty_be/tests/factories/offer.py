import factory

from beauty_be.models import Offer
from beauty_be.tests.factories.base import BaseFactory


class OfferFactory(BaseFactory):
    name = factory.Faker('word')
    price = factory.Faker('pyint')
    duration = factory.Faker('pyint')

    class Meta:
        model = Offer
        sqlalchemy_session_persistence = 'commit'
