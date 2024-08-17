import factory

from beauty_be.models import User
from beauty_be.tests.factories.base import BaseFactory


class UserFactory(BaseFactory):
    sub = factory.Faker('uuid4')
    display_name = factory.Faker('name')
    phone_number = factory.Faker('phone_number')

    class Meta:
        model = User
        sqlalchemy_session_persistence = 'commit'
