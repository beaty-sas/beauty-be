from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.service import get_business_service
from beauty_be.api.dependencies.service import get_offer_service
from beauty_be.schemas.offer import CreateOfferRequestSchema
from beauty_be.schemas.offer import OfferSchema
from beauty_be.services.business import BusinessService
from beauty_be.services.offer import OfferService
from beauty_models.beauty_models.models import Merchant
from beauty_models.beauty_models.models import Offer

router = APIRouter()


@router.get(
    '/offers',
    summary='Get merchant offers',
    status_code=HTTPStatus.OK,
    response_model=list[OfferSchema],
    responses={
        200: {'model': list[OfferSchema]},
    },
)
async def get_merchant_offers(
    business_id: int = Query(..., description='Business id'),
    merchant: Merchant = Depends(authenticate_merchant),
    offer_service: OfferService = Depends(get_offer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> Sequence[Offer]:
    await business_service.is_merchant_business(business_id, int(merchant.id))
    return await offer_service.get_by_business_id(business_id)


@router.post(
    '/offers',
    summary='Create new offer',
    status_code=HTTPStatus.CREATED,
    response_model=OfferSchema,
    responses={
        201: {'model': OfferSchema},
    },
)
async def create_offer(
    request_data: CreateOfferRequestSchema,
    merchant: Merchant = Depends(authenticate_merchant),
    offer_service: OfferService = Depends(get_offer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> Offer:
    await business_service.is_merchant_business(request_data.business_id, int(merchant.id))
    return await offer_service.create_offer(request_data)


@router.patch(
    '/offers/{offer_id}',
    summary='Update offer',
    status_code=HTTPStatus.OK,
    response_model=OfferSchema,
    responses={
        200: {'model': OfferSchema},
    },
)
async def update_offer(
    offer_id: int,
    request_data: CreateOfferRequestSchema,
    merchant: Merchant = Depends(authenticate_merchant),
    offer_service: OfferService = Depends(get_offer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> Offer:
    await business_service.is_merchant_business(request_data.business_id, int(merchant.id))
    return await offer_service.update_offer(offer_id, request_data)
