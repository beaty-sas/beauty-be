import factory

from beauty_be.models import Merchant
from beauty_be.tests.factories.attachment import AttachmentFactory
from beauty_be.tests.factories.base import BaseFactory


class MerchantFactory(BaseFactory):
    sub = factory.Faker('word')
    display_name = factory.Faker('word')
    phone_number = factory.Faker('phone_number')

    logo = factory.SubFactory(AttachmentFactory)

    @factory.post_generation
    def businesses(self, create, extracted, **_):
        if not create:
            return

        if extracted:
            for business in extracted:
                self.businesses.append(business)

    class Meta:
        model = Merchant
        sqlalchemy_session_persistence = 'commit'
