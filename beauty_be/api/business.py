from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter
from fastapi import Depends

from beauty_be.api.dependencies.service import get_business_service
from beauty_be.api.dependencies.service import get_offer_service
from beauty_be.schemas.business import BusinessSchema
from beauty_be.schemas.offer import OfferSchema
from beauty_be.services.business import BusinessService
from beauty_be.services.offer import OfferService
from beauty_models.beauty_models.models import Business
from beauty_models.beauty_models.models import Offer

router = APIRouter()


@router.get(
    '/businesses/{business_id}',
    summary='Get business info',
    status_code=HTTPStatus.OK,
    response_model=BusinessSchema,
    responses={
        200: {'model': BusinessSchema},
    },
)
async def get_business_info(
    business_id: int,
    business_service: BusinessService = Depends(get_business_service),
) -> Business:
    return await business_service.get_info(business_id)


@router.get(
    '/businesses/{business_id}/offers',
    summary='Get business offers',
    status_code=HTTPStatus.OK,
    response_model=list[OfferSchema],
    responses={
        200: {'model': list[OfferSchema]},
    },
)
async def get_business_offers(
    business_id: int,
    offer_service: OfferService = Depends(get_offer_service),
) -> Sequence[Offer]:
    return await offer_service.get_by_business_id(business_id)
