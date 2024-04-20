from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.logger import LoggingRoute
from beauty_be.api.dependencies.service import get_business_service
from beauty_be.api.dependencies.service import get_merchant_service
from beauty_be.schemas.merchant import MerchantSchema
from beauty_be.schemas.merchant import MerchantUpdateSchema
from beauty_be.services.business import BusinessService
from beauty_be.services.merchant import MerchantService
from beauty_models.beauty_models.models import Merchant

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/me',
    summary='Get merchant profile',
    status_code=HTTPStatus.OK,
    response_model=MerchantSchema,
    responses={
        200: {'model': MerchantSchema},
    },
)
async def get_merchant_profile(
    merchant: Merchant = Depends(authenticate_merchant),
    business_service: BusinessService = Depends(get_business_service),
) -> MerchantSchema:
    return await business_service.get_info_by_merchant(int(merchant.id))


@router.patch(
    '/me',
    summary='Update merchant profile',
    status_code=HTTPStatus.OK,
    response_model=MerchantSchema,
    responses={
        200: {'model': MerchantSchema},
    },
)
async def update_merchant_profile(
    request_data: MerchantUpdateSchema,
    merchant: Merchant = Depends(authenticate_merchant),
    merchant_service: MerchantService = Depends(get_merchant_service),
) -> MerchantSchema:
    return await merchant_service.update_merchant(merchant, request_data)
