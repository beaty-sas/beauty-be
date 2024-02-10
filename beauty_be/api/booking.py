from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends

from beauty_be.api.dependencies.service import get_booking_service
from beauty_be.api.dependencies.service import get_offer_service
from beauty_be.api.dependencies.service import get_user_service
from beauty_be.schemas.booking import BookingCreateSchema
from beauty_be.schemas.booking import BookingSchema
from beauty_be.services.booking import BookingService
from beauty_be.services.offer import OfferService
from beauty_be.services.user import UserService

router = APIRouter()


@router.post(
    '/booking/business/{business_id}',
    summary='Make a booking',
    status_code=HTTPStatus.CREATED,
    response_model=BookingSchema,
    responses={
        201: {'model': BookingSchema},
    },
)
async def make_new_booking(
    request_data: BookingCreateSchema,
    user_service: UserService = Depends(get_user_service),
    offer_service: OfferService = Depends(get_offer_service),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingSchema:
    user = await user_service.get_or_create_by_phone_number(request_data.user)
    offers = await offer_service.get_by_ids(request_data.offers)
    return await booking_service.create_booking(request_data, offers, user)
