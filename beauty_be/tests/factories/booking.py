import factory

from beauty_be.models import Booking
from beauty_be.tests.factories.business import BusinessFactory
from beauty_be.tests.factories.base import BaseFactory
from beauty_be.tests.factories.user import UserFactory


class BookingFactory(BaseFactory):
    start_time = factory.Faker('date_time')
    end_time = factory.Faker('date_time')
    price = factory.Faker('random_int')
    status = factory.Faker('random_element', elements=['NEW', 'CONFIRMED', 'COMPLETED', 'CANCELLED'])
    comment = factory.Faker('text')

    user = factory.SubFactory(UserFactory)
    business = factory.SubFactory(BusinessFactory)

    class Meta:
        model = Booking
        sqlalchemy_session_persistence = 'commit'
