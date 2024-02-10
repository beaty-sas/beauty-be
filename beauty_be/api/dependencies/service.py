from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.api.dependencies.db import get_db_session
from beauty_be.services.booking import BookingService
from beauty_be.services.business import BusinessService
from beauty_be.services.offer import OfferService
from beauty_be.services.user import UserService
from beauty_be.services.working_hours import WorkingHoursService


async def get_offer_service(session: AsyncSession = Depends(get_db_session)) -> OfferService:
    return OfferService(session)


async def get_business_service(session: AsyncSession = Depends(get_db_session)) -> BusinessService:
    return BusinessService(session)


async def get_working_hours_service(session: AsyncSession = Depends(get_db_session)) -> WorkingHoursService:
    return WorkingHoursService(session)


async def get_user_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(session)


async def get_booking_service(session: AsyncSession = Depends(get_db_session)) -> BookingService:
    return BookingService(session)
