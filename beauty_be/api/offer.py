from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.logger import LoggingRoute
from beauty_be.api.dependencies.service import get_business_service
from beauty_be.api.dependencies.service import get_offer_service
from beauty_be.schemas.offer import CreateOfferRequestSchema
from beauty_be.schemas.offer import OfferSchema
from beauty_be.services.business import BusinessService
from beauty_be.services.offer import OfferService
from beauty_models.beauty_models.models import Merchant
from beauty_models.beauty_models.models import Offer

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/offers',
    summary='Get merchant offers',
    status_code=HTTPStatus.OK,
    response_model=list[OfferSchema],
    responses={
        HTTPStatus.OK: {'model': list[OfferSchema]},
    },
)
async def get_merchant_offers(
    slug: str = Query(..., description='Business slug'),
    merchant: Merchant = Depends(authenticate_merchant),
    offer_service: OfferService = Depends(get_offer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> Sequence[Offer]:
    await business_service.is_merchant_business(slug, int(merchant.id))
    return await offer_service.get_by_business_slug(slug)


@router.post(
    '/offers',
    summary='Create new offer',
    status_code=HTTPStatus.CREATED,
    response_model=OfferSchema,
    responses={
        HTTPStatus.CREATED: {'model': OfferSchema},
    },
)
async def create_offer(
    request_data: CreateOfferRequestSchema,
    merchant: Merchant = Depends(authenticate_merchant),
    offer_service: OfferService = Depends(get_offer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> Offer:
    await business_service.is_merchant_business_by_id(request_data.business_id, int(merchant.id))
    return await offer_service.create_offer(request_data)


@router.patch(
    '/offers/{offer_id}',
    summary='Update offer',
    status_code=HTTPStatus.OK,
    response_model=OfferSchema,
    responses={
        HTTPStatus.OK: {'model': OfferSchema},
    },
)
async def update_offer(
    offer_id: int,
    request_data: CreateOfferRequestSchema,
    merchant: Merchant = Depends(authenticate_merchant),
    offer_service: OfferService = Depends(get_offer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> Offer:
    await business_service.is_merchant_business_by_id(request_data.business_id, int(merchant.id))
    return await offer_service.update_offer(offer_id, request_data)


@router.delete(
    '/offers/{offer_id}/delete',
    summary='Delete offer',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_offer(
    offer_id: int,
    slug: str = Query(..., description='Business slug'),
    merchant: Merchant = Depends(authenticate_merchant),
    offer_service: OfferService = Depends(get_offer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> None:
    await business_service.is_merchant_business(slug, int(merchant.id))
    await offer_service.delete_offer(offer_id)
