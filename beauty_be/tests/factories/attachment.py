import factory

from beauty_be.models import Attachment
from beauty_be.tests.factories.base import BaseFactory


class AttachmentFactory(BaseFactory):
    original = factory.Faker('uri')
    thumbnail = factory.Faker('uri')

    class Meta:
        model = Attachment
        sqlalchemy_session_persistence = 'commit'
