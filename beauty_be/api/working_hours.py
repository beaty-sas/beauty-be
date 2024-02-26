from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.service import get_business_service
from beauty_be.api.dependencies.service import get_working_hours_service
from beauty_be.schemas.business import BusinessSchema
from beauty_be.schemas.working_hours import AvailableBookHourSchema
from beauty_be.schemas.working_hours import WorkingHoursBaseSchema
from beauty_be.schemas.working_hours import WorkingHoursCreateSchema
from beauty_be.services.business import BusinessService
from beauty_be.services.working_hours import WorkingHoursService
from beauty_models.beauty_models.models import Merchant

router = APIRouter()


@router.get(
    '/working-hours/{business_id}/available',
    summary='Get business working hours',
    status_code=HTTPStatus.OK,
    response_model=list[AvailableBookHourSchema],
    responses={
        200: {'model': BusinessSchema},
    },
)
async def get_business_available_hours(
    business_id: int,
    date: str = Query(..., description='Date in format YYYY-MM-DD'),
    duration: int = Query(3600, description='Duration of the booking in seconds'),
    working_hours_service: WorkingHoursService = Depends(get_working_hours_service),
) -> list[AvailableBookHourSchema]:
    return await working_hours_service.get_available_hours(business_id, date, duration)


@router.get(
    '/working-hours/{business_id}',
    summary='Get business working hours',
    status_code=HTTPStatus.OK,
    response_model=list[WorkingHoursBaseSchema],
    responses={
        200: {'model': list[WorkingHoursBaseSchema]},
    },
)
async def get_business_working_hours(
    business_id: int,
    merchant: Merchant = Depends(authenticate_merchant),
    working_hours_service: WorkingHoursService = Depends(get_working_hours_service),
) -> Sequence[WorkingHoursBaseSchema]:
    return await working_hours_service.get_merchant_working_hours(business_id, merchant)


@router.post(
    '/working-hours/{business_id}',
    summary='Set business working hours',
    status_code=HTTPStatus.CREATED,
    response_model=list[WorkingHoursBaseSchema],
    responses={
        201: {'model': list[WorkingHoursBaseSchema]},
    },
)
async def create_business_working_hours(
    business_id: int,
    request_data: list[WorkingHoursCreateSchema],
    merchant: Merchant = Depends(authenticate_merchant),
    business_service: BusinessService = Depends(get_business_service),
    working_hours_service: WorkingHoursService = Depends(get_working_hours_service),
) -> Sequence[WorkingHoursBaseSchema]:
    await business_service.is_merchant_business(business_id, int(merchant.id))
    return await working_hours_service.create_working_hours(request_data, business_id)
