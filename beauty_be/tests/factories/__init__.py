from typing import Type

import factory

from beauty_be.tests.factories.business import BusinessFactory
from beauty_be.tests.factories.service import ServiceFactory

FACTORIES: list[Type[factory.alchemy.SQLAlchemyModelFactory]] = [
    BusinessFactory,
    ServiceFactory,
]
