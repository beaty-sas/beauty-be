from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Sequence

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from beauty_be.clients import aws_sqs_client
from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import DoesNotExistError
from beauty_be.models import Attachment
from beauty_be.models import Booking
from beauty_be.models import BookingStatus
from beauty_be.models import Business
from beauty_be.models import Merchant
from beauty_be.models import Offer
from beauty_be.models import User
from beauty_be.schemas.analytic import BookingAnalyticSchema
from beauty_be.schemas.booking import BookingCreateSchema
from beauty_be.schemas.booking import BookingUpdateSchema
from beauty_be.schemas.notification import SMSTemplate
from beauty_be.schemas.notification import SQSNotificationSchema
from beauty_be.services.base import BaseService


class BookingService(BaseService[Booking]):
    MODEL = Booking

    async def get_info(self, booking_id: int) -> Booking:
        if booking := await self.fetch_one(
                filters=(self.MODEL.id == booking_id,),
                options=(
                        selectinload(self.MODEL.business).selectinload(Business.owner),
                        selectinload(self.MODEL.user),
                        selectinload(self.MODEL.offers),
                        selectinload(self.MODEL.attachments),
                ),
        ):
            return booking
        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=booking_id))

    async def create_booking(
            self,
            data: BookingCreateSchema,
            offers: Sequence[Offer],
            attachments: Sequence[Attachment],
            user: User,
    ) -> Booking:
        duration = timedelta(seconds=sum(offer.duration for offer in offers))  # type: ignore
        start_time = data.start_time.replace(tzinfo=timezone.utc)
        booking = self.MODEL(
            start_time=start_time,
            end_time=start_time + duration,
            business_id=data.business_id,
            user_id=user.id,
            price=sum(offer.price for offer in offers),
            comment=data.comment,
        )
        booking.offers.extend(offers)
        booking.attachments.extend(attachments)
        obj = await self.insert_obj(booking)
        booking = await self.get_info(obj.id)
        await self.send_new_booking_notification(booking, user)
        return booking

    @staticmethod
    async def send_new_booking_notification(booking: Booking, user: User) -> None:
        destination = booking.business.owner.telegram_id or booking.business.phone_number
        provider = 'telegram' if booking.business.owner.telegram_id else 'sns'
        body = SQSNotificationSchema(
            destination=destination.replace(' ', ''),
            provider=provider,
            template=SMSTemplate.NEW_ORDER,
            values={
                'name': user.display_name,
                'phone_number': user.phone_number.replace(' ', ''),
                'date_time': booking.start_time.strftime('%d.%m.%Y %H:%M'),
            },
        )
        await aws_sqs_client.send_sms_notification(body, int(user.id))

    async def get_by_business(self, business_id: int, merchant: Merchant) -> Sequence[Booking]:
        query = (
            select(self.MODEL)
            .filter(
                self.MODEL.business_id == business_id,
                self.MODEL.business.has(Business.owner_id == merchant.id),
            )
            .options(
                selectinload(self.MODEL.offers),
                selectinload(self.MODEL.user),
                selectinload(self.MODEL.attachments),
            )
        )
        return await self.fetch_all(query=query)

    async def cancel_booking(self, booking_id: int, merchant: Merchant) -> Booking | None:
        await self.update(
            filters=(self.MODEL.id == booking_id, self.MODEL.business.has(Business.owner_id == merchant.id)),
            values={'status': BookingStatus.CANCELLED},
        )
        await self.session.commit()
        return await self.fetch_one(filters=(self.MODEL.id == booking_id,))

    async def confirm_booking(self, booking_id: int, merchant: Merchant) -> Booking:
        await self.update(
            filters=(self.MODEL.id == booking_id, self.MODEL.business.has(Business.owner_id == merchant.id)),
            values={'status': BookingStatus.CONFIRMED},
        )
        await self.session.commit()
        return await self.get_info(booking_id)

    async def get_info_by_merchant(self, booking_id: int, merchant: Merchant) -> Booking:
        if booking := await self.fetch_one(
                filters=(self.MODEL.id == booking_id, self.MODEL.business.has(Business.owner_id == merchant.id)),
                options=(
                        selectinload(self.MODEL.offers),
                        selectinload(self.MODEL.user),
                        selectinload(self.MODEL.attachments),
                ),
        ):
            return booking
        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=booking_id))

    async def update_booking(self, booking_id: int, merchant: Merchant, data: BookingUpdateSchema) -> Booking:
        await self.update(
            filters=(self.MODEL.id == booking_id, self.MODEL.business.has(Business.owner_id == merchant.id)),
            values=data.model_dump(),
        )
        await self.session.commit()
        return await self.get_info_by_merchant(booking_id, merchant)

    async def get_analytic(self, merchant: Merchant) -> BookingAnalyticSchema:
        now_date = datetime.now().date()
        query = select(count(self.MODEL.id)).filter(self.MODEL.business.has(Business.owner_id == merchant.id))
        total = await self.fetch_count(query=query)
        future = await self.fetch_count(
            query=query.filter(
                self.MODEL.start_time > now_date,
            )
        )
        today = await self.fetch_count(
            query=query.filter(
                func.date(self.MODEL.start_time) == now_date,
            )
        )
        return BookingAnalyticSchema(total=total, future=future, today=today)
