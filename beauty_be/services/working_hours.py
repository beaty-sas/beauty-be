from datetime import datetime
from datetime import timedelta
from typing import Sequence

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select

from beauty_be.conf import settings
from beauty_be.schemas.working_hours import AvailableBookHourSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Booking
from beauty_models.beauty_models.models import WorkingHours


class WorkingHoursService(BaseService[WorkingHours]):
    MODEL = WorkingHours

    async def get_working_hours(self, business_id: int, date: str) -> Sequence[WorkingHours]:
        query = select(self.MODEL).where(
            self.MODEL.business_id == business_id,
            self.MODEL.date == datetime.strptime(date, settings.DEFAULT_DATE_FORMAT),
        )
        return await self.fetch_all(query=query)

    async def get_available_hours(
        self,
        business_id: int,
        date: str,
        duration: int,
    ) -> list[AvailableBookHourSchema]:
        working_hours = await self.get_working_hours(business_id, date)
        bookings = await self.fetch_all(
            query=(
                select(Booking).where(
                    and_(
                        Booking.business_id == business_id,
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
            current_time = datetime.combine(hour.date, hour.opening_time)  # type: ignore
            end_time = datetime.combine(hour.date, hour.closing_time)  # type: ignore
            while current_time <= end_time:
                slot_end_time = current_time + timedelta(seconds=duration)

                if slot_end_time > end_time:
                    current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)
                    continue

                if current_time + timedelta(seconds=duration) > end_time:
                    current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)
                    continue

                if current_time.hour in booked_slots:
                    current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)
                    continue

                if (current_time + timedelta(seconds=duration)).hour in booked_slots:
                    current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)
                    continue

                available_slots.append(AvailableBookHourSchema(time=current_time))
                current_time += timedelta(seconds=settings.DEFAULT_BOOKING_TIME_STEP)
        return available_slots