from datetime import timedelta
from datetime import timezone
from typing import Sequence

from sqlalchemy.orm import selectinload

from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import DoesNotExistError
from beauty_be.schemas.booking import BookingCreateSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Booking
from beauty_models.beauty_models.models import Offer
from beauty_models.beauty_models.models import User


class BookingService(BaseService[Booking]):
    MODEL = Booking

    async def get_info(self, booking_id: int) -> Booking:
        if booking := await self.fetch_one(
            filters=(self.MODEL.id == booking_id,),
            options=(selectinload(self.MODEL.business),),
        ):
            return booking
        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=booking_id))

    async def create_booking(self, data: BookingCreateSchema, offers: Sequence[Offer], user: User) -> Booking:
        duration = timedelta(seconds=sum(offer.duration for offer in offers))
        start_time = data.start_time.replace(tzinfo=timezone.utc)
        booking = self.MODEL(
            start_time=start_time,
            end_time=start_time + duration,
            business_id=data.business_id,
            user_id=user.id,
            price=sum(offer.price for offer in offers),
        )
        booking.offers.extend(offers)
        obj = await self.insert_obj(booking)
        return await self.get_info(obj.id)
