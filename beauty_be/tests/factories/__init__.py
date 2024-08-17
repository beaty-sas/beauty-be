from typing import Type

import factory

from beauty_be.tests.factories.attachment import AttachmentFactory
from beauty_be.tests.factories.booking import BookingFactory
from beauty_be.tests.factories.business import BusinessFactory
from beauty_be.tests.factories.location import LocationFactory
from beauty_be.tests.factories.merchant import MerchantFactory
from beauty_be.tests.factories.offer import OfferFactory
from beauty_be.tests.factories.user import UserFactory
from beauty_be.tests.factories.working_hour import WorkingHoursFactory

FACTORIES: list[Type[factory.Factory]] = [
    OfferFactory,
    BusinessFactory,
    MerchantFactory,
    AttachmentFactory,
    LocationFactory,
    BookingFactory,
    UserFactory,
    WorkingHoursFactory,
]
