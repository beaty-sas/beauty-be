from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.logger import LoggingRoute
from beauty_be.api.dependencies.service import get_booking_service
from beauty_be.schemas.analytic import BookingAnalyticSchema
from beauty_be.services.booking import BookingService
from beauty_models.beauty_models.models import Merchant

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/analytics/booking',
    summary='Get bookings analytics',
    status_code=HTTPStatus.OK,
    response_model=BookingAnalyticSchema,
    responses={
        HTTPStatus.OK: {'model': BookingAnalyticSchema},
    },
)
async def get_bookings_analytic(
    merchant: Merchant = Depends(authenticate_merchant),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingAnalyticSchema:
    return await booking_service.get_analytic(merchant)
