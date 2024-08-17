import factory

from beauty_be.models import WorkingHours
from beauty_be.tests.factories import BusinessFactory
from beauty_be.tests.factories.base import BaseFactory


class WorkingHoursFactory(BaseFactory):
    date_from = factory.Faker('date_object')
    date_to = factory.Faker('date_object')
    business = factory.SubFactory(BusinessFactory)

    class Meta:
        model = WorkingHours
        sqlalchemy_session_persistence = 'commit'
