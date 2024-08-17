import factory

from beauty_be.models import Business
from beauty_be.tests.factories.attachment import AttachmentFactory
from beauty_be.tests.factories.base import BaseFactory
from beauty_be.tests.factories.merchant import MerchantFactory


class BusinessFactory(BaseFactory):
    name = factory.Faker('word')
    slug = factory.Faker('word')
    display_name = factory.Faker('word')
    description = factory.Faker('word')
    phone_number = factory.Faker('phone_number')

    owner = factory.SubFactory(MerchantFactory)
    logo = factory.SubFactory(AttachmentFactory)
    banner = factory.SubFactory(AttachmentFactory)

    class Meta:
        model = Business
        sqlalchemy_session_persistence = 'commit'

    @factory.post_generation
    def offers(self, create, extracted, **_):
        if not create:
            return

        if extracted:
            for offer in extracted:
                self.offers.append(offer)
