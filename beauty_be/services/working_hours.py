from datetime import datetime
from datetime import timedelta
from typing import Sequence

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select

from beauty_be.conf.settings import settings
from beauty_be.exceptions import ValidationError
from beauty_be.schemas.working_hours import AvailableBookHourSchema
from beauty_be.schemas.working_hours import WorkingHoursCreateSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Booking
from beauty_models.beauty_models.models import BookingStatus
from beauty_models.beauty_models.models import Business
from beauty_models.beauty_models.models import Merchant
from beauty_models.beauty_models.models import Offer
from beauty_models.beauty_models.models import WorkingHours


class WorkingHoursService(BaseService[WorkingHours]):
    MODEL = WorkingHours

    async def get_merchant_working_hours(self, business_id: int, merchant: Merchant) -> Sequence[WorkingHours]:
        query = select(self.MODEL).where(
            self.MODEL.business_id == business_id,
            self.MODEL.business.has(Business.owner_id == merchant.id),
            self.MODEL.date_from >= datetime.now().date(),
        )
        return await self.fetch_all(query=query)

    async def get_working_hours(self, slug: str, date: datetime) -> Sequence[WorkingHours]:
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)

        query = select(self.MODEL).where(
            self.MODEL.business.has(Business.slug == slug),
            self.MODEL.date_from <= end_of_day,
            self.MODEL.date_to >= start_of_day,
        )
        return await self.fetch_all(query=query)

    async def get_available_hours(
        self,
        slug: str,
        date: str,
        duration: int,
    ) -> list[AvailableBookHourSchema]:
        formatted_date = datetime.strptime(date, settings.DEFAULT_DATE_FORMAT)
        working_hours = await self.get_working_hours(slug, formatted_date)
        bookings = await self.fetch_all(
            query=(
                select(Booking).where(
                    and_(
                        Booking.business.has(Business.slug == slug),
                        Booking.status != BookingStatus.CANCELLED,
                        func.date(Booking.start_time) == datetime.strptime(date, settings.DEFAULT_DATE_FORMAT),
                    )
                )
            )
        )
        return self._calculate_available_hours(bookings, working_hours, duration)

    @staticmethod
    def _calculate_available_hours(
        bookings: Sequence[Booking],
        working_hours: Sequence[WorkingHours],
        duration: int,
    ) -> list[AvailableBookHourSchema]:
        booked_slots = set()
        for booking in bookings:
            start_time = booking.start_time
            while start_time < booking.end_time:
                booked_slots.add(start_time.hour)
                start_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)  # type: ignore

        available_slots = []
        for hour in working_hours:
            current_time = hour.date_from
            now = datetime.now(tz=hour.date_from.tzinfo)

            while current_time <= hour.date_to:
                slot_end_time = current_time + timedelta(seconds=duration)

                if current_time < now:
                    current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)  # type: ignore
                    continue

                if slot_end_time > hour.date_to or (current_time + timedelta(seconds=duration)) > hour.date_to:
                    current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)  # type: ignore
                    continue

                if current_time.hour in booked_slots:
                    current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)  # type: ignore
                    continue

                available_slots.append(AvailableBookHourSchema(time=current_time.strftime('%-H:%M')))  # type: ignore
                current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)  # type: ignore

        return available_slots

    async def create_working_hours(
        self,
        data: list[WorkingHoursCreateSchema],
        business_id: int,
    ) -> Sequence[WorkingHours]:
        objs = []
        for item in data:
            obj = self.MODEL(
                date_from=item.date_from,
                date_to=item.date_to,
                business_id=business_id,
            )
            await self.insert_obj(obj, commit=False)
            objs.append(obj)
        await self.session.commit()
        return objs

    async def delete_working_hour(self, working_hours_id: int) -> None:
        await self.bulk_delete(filters=(self.MODEL.id == working_hours_id,))
        await self.session.commit()

    async def validate_booking(self, start_time: datetime, business: Business, offers: Sequence[Offer]) -> None:
        duration: int = sum(int(offer.duration) for offer in offers)
        available_slots = await self.get_available_hours(
            str(business.slug),
            start_time.strftime(settings.DEFAULT_DATE_FORMAT),
            duration,
        )
        available_time_slots = [slot.time for slot in available_slots]
        booking_end_time = start_time + timedelta(seconds=duration)
        booking_time_slots = [f'{i}:00' for i in range(start_time.hour, booking_end_time.hour)]

        for slot in booking_time_slots:
            if slot not in available_time_slots:
                raise ValidationError('Booking time is not available')
