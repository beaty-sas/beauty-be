from datetime import timedelta
from datetime import timezone
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import DoesNotExistError
from beauty_be.schemas.booking import BookingCreateSchema
from beauty_be.schemas.booking import BookingUpdateSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Booking
from beauty_models.beauty_models.models import BookingStatus
from beauty_models.beauty_models.models import Business
from beauty_models.beauty_models.models import Merchant
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
        duration = timedelta(seconds=sum(offer.duration for offer in offers))  # type: ignore
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

    async def get_by_business_id(self, business_id: int, merchant: Merchant) -> Sequence[Booking]:
        query = (
            select(self.MODEL)
            .filter(
                self.MODEL.business_id == business_id,
                self.MODEL.business.has(Business.owner_id == merchant.id),
            )
            .options(
                selectinload(self.MODEL.offers),
                selectinload(self.MODEL.user),
            )
        )
        return await self.fetch_all(query=query)

    async def cancel_booking(self, booking_id: int, merchant: Merchant) -> None:
        await self.update(
            filters=(self.MODEL.id == booking_id, self.MODEL.business.has(Business.owner_id == merchant.id)),
            values={'status': BookingStatus.CANCELLED},
        )
        await self.session.commit()

    async def get_info_by_merchant(self, booking_id: int, merchant: Merchant) -> Booking:
        if booking := await self.fetch_one(
            filters=(self.MODEL.id == booking_id, self.MODEL.business.has(Business.owner_id == merchant.id)),
            options=(selectinload(self.MODEL.offers), selectinload(self.MODEL.user)),
        ):
            return booking
        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=booking_id))

    async def update_booking(self, booking_id: int, merchant: Merchant, data: BookingUpdateSchema) -> Booking:
        await self.update(
            filters=(self.MODEL.id == booking_id, self.MODEL.business.has(Business.owner_id == merchant.id)),
            values=data.dict(),
        )
        await self.session.commit()
        return await self.get_info_by_merchant(booking_id, merchant)
