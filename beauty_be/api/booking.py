from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter
from fastapi import Depends

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.logger import LoggingRoute
from beauty_be.api.dependencies.service import get_booking_service
from beauty_be.api.dependencies.service import get_offer_service
from beauty_be.api.dependencies.service import get_user_service
from beauty_be.schemas.booking import BookingCreateSchema
from beauty_be.schemas.booking import BookingSchema
from beauty_be.schemas.booking import BookingUpdateSchema
from beauty_be.services.booking import BookingService
from beauty_be.services.offer import OfferService
from beauty_be.services.user import UserService
from beauty_models.beauty_models.models import Booking
from beauty_models.beauty_models.models import Merchant

router = APIRouter(route_class=LoggingRoute)


@router.post(
    '/booking',
    summary='Make a booking',
    status_code=HTTPStatus.CREATED,
    response_model=BookingSchema,
    responses={
        HTTPStatus.CREATED: {'model': BookingSchema},
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


@router.get(
    '/booking/{booking_id}',
    summary='Get booking info',
    status_code=HTTPStatus.OK,
    response_model=BookingSchema,
    responses={
        HTTPStatus.OK: {'model': BookingSchema},
    },
)
async def get_booking_info(
    booking_id: int,
    merchant: Merchant = Depends(authenticate_merchant),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingSchema:
    return await booking_service.get_info_by_merchant(booking_id, merchant)


@router.patch(
    '/booking/{booking_id}',
    summary='Update a booking',
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {'model': BookingSchema},
    },
)
async def update_booking(
    booking_id: int,
    request_data: BookingUpdateSchema,
    merchant: Merchant = Depends(authenticate_merchant),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingSchema:
    return await booking_service.update_booking(booking_id, merchant, request_data)


@router.get(
    '/booking/business/{business_id}',
    summary='Get all bookings for a business',
    status_code=HTTPStatus.OK,
    response_model=list[BookingSchema],
    responses={
        HTTPStatus.OK: {'model': list[BookingSchema]},
    },
)
async def get_bookings_for_business(
    business_id: int,
    merchant: Merchant = Depends(authenticate_merchant),
    booking_service: BookingService = Depends(get_booking_service),
) -> Sequence[BookingSchema]:
    return await booking_service.get_by_business(business_id, merchant)


@router.patch(
    '/booking/{booking_id}/cancel',
    summary='Cancel a booking',
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.NO_CONTENT: {},
    },
)
async def cancel_booking(
    booking_id: int,
    merchant: Merchant = Depends(authenticate_merchant),
    booking_service: BookingService = Depends(get_booking_service),
) -> None:
    await booking_service.cancel_booking(booking_id, merchant)


@router.patch(
    '/booking/{booking_id}/confirm',
    summary='Confirm a booking',
    status_code=HTTPStatus.OK,
    response_model=BookingSchema,
    responses={
        HTTPStatus.OK: {'model': BookingSchema},
    },
)
async def confirm_booking(
    booking_id: int,
    merchant: Merchant = Depends(authenticate_merchant),
    booking_service: BookingService = Depends(get_booking_service),
) -> Booking:
    return await booking_service.confirm_booking(booking_id, merchant)
