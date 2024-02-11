import factory

from beauty_models.beauty_models.models import Business


class BusinessFactory(factory.Factory):
    """Business factory"""

    name = factory.Faker('word')
    display_name = factory.Faker('word')
    phone_number = factory.Faker('phone_number')
    web_site = factory.Faker('url')

    @factory.post_generation
    def services(self, create, extracted, **_):
        if not create:
            return

        if extracted:
            for service in extracted:
                self.services.append(service)

    class Meta:
        model = Business
