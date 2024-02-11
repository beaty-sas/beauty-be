from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from beauty_be.api.dependencies.service import get_working_hours_service
from beauty_be.schemas.business import BusinessSchema
from beauty_be.schemas.working_hours import AvailableBookHourSchema
from beauty_be.services.working_hours import WorkingHoursService

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
