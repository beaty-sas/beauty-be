from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter
from fastapi import Depends

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.logger import LoggingRoute
from beauty_be.api.dependencies.service import get_business_service
from beauty_be.api.dependencies.service import get_location_service
from beauty_be.api.dependencies.service import get_offer_service
from beauty_be.models import Business
from beauty_be.models import Merchant
from beauty_be.models import Offer
from beauty_be.schemas.business import BusinessSchema
from beauty_be.schemas.business import UpdateBusinessSchema
from beauty_be.schemas.offer import OfferSchema
from beauty_be.services.business import BusinessService
from beauty_be.services.location import LocationService
from beauty_be.services.offer import OfferService

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/businesses/my',
    summary='Get business info',
    status_code=HTTPStatus.OK,
    response_model=BusinessSchema,
)
async def get_my_business_info(
        merchant: Merchant = Depends(authenticate_merchant),
        business_service: BusinessService = Depends(get_business_service),
) -> Business:
    return await business_service.get_info_by_merchant(int(merchant.id))


@router.get(
    '/businesses/available',
    summary='Get businesses ids',
    status_code=HTTPStatus.OK,
    response_model=list[str],
)
async def get_businesses_slug(
        business_service: BusinessService = Depends(get_business_service),
) -> Sequence[str]:
    return await business_service.get_businesses_slug()


@router.get(
    '/businesses/{slug}',
    summary='Get business info',
    status_code=HTTPStatus.OK,
    response_model=BusinessSchema,
)
async def get_business_info(
        slug: str,
        business_service: BusinessService = Depends(get_business_service),
) -> Business:
    return await business_service.get_info(slug)


@router.patch(
    '/businesses/{business_id}',
    summary='Update business info',
    status_code=HTTPStatus.OK,
    response_model=BusinessSchema,
)
async def update_business_info(
        business_id: int,
        request_data: UpdateBusinessSchema,
        merchant: Merchant = Depends(authenticate_merchant),
        business_service: BusinessService = Depends(get_business_service),
        location_service: LocationService = Depends(get_location_service),
) -> Business:
    business = await business_service.update_info(business_id, merchant, request_data)
    if request_data.location:
        await location_service.update_or_create_name(business, request_data.location.name)
    return business


@router.get(
    '/businesses/{slug}/offers',
    summary='Get business offers',
    status_code=HTTPStatus.OK,
    response_model=list[OfferSchema],
)
async def get_business_offers(
        slug: str,
        offer_service: OfferService = Depends(get_offer_service),
) -> Sequence[Offer]:
    return await offer_service.get_by_business_slug(slug)
