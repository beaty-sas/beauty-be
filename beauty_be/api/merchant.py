from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.api.dependencies.logger import LoggingRoute
from beauty_be.api.dependencies.service import get_merchant_service
from beauty_be.models import Merchant
from beauty_be.schemas.merchant import MerchantSchema
from beauty_be.schemas.merchant import MerchantUpdateSchema
from beauty_be.services.merchant import MerchantService

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/me',
    summary='Get merchant profile',
    status_code=HTTPStatus.OK,
    response_model=MerchantSchema,
)
async def get_merchant_profile(
        merchant: Merchant = Depends(authenticate_merchant),
        merchant_service: MerchantService = Depends(get_merchant_service),
) -> Merchant:
    return await merchant_service.get_with_business(int(merchant.id))


@router.patch(
    '/me',
    summary='Update merchant profile',
    status_code=HTTPStatus.OK,
    response_model=MerchantSchema,
)
async def update_merchant_profile(
        request_data: MerchantUpdateSchema,
        merchant: Merchant = Depends(authenticate_merchant),
        merchant_service: MerchantService = Depends(get_merchant_service),
) -> Merchant:
    return await merchant_service.update_merchant(merchant, request_data)
