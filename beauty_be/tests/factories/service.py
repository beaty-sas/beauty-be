import factory

from beauty_models.beauty_models.models import Offer


class ServiceFactory(factory.Factory):
    """Service factory"""

    name = factory.Faker('word')

    class Meta:
        model = Offer
