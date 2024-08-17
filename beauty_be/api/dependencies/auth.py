import logging
from typing import Any

import jwt
from fastapi import Depends
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from beauty_be.api.dependencies.service import get_business_service
from beauty_be.api.dependencies.service import get_merchant_service
from beauty_be.conf.constants import ErrorMessages
from beauty_be.conf.constants import JWK_URL
from beauty_be.conf.constants import JWT_ACCESS_TOKEN_ALGORITHMS
from beauty_be.conf.settings import settings
from beauty_be.exceptions import AuthError
from beauty_be.services.business import BusinessService
from beauty_be.services.merchant import MerchantService
from beauty_be.models.merchant import Merchant

logger = logging.getLogger(__name__)
oauth2_scheme = HTTPBearer(scheme_name='ServiceAuthHTTPBearer', auto_error=False)
jwk_client = jwt.PyJWKClient(JWK_URL, cache_keys=True)


def get_jwk_key(token: str) -> jwt.PyJWK:
    try:
        return jwk_client.get_signing_key_from_jwt(token)
    except jwt.PyJWTError:
        raise AuthError(ErrorMessages.INVALID_TOKEN)


def validate_access_token(token: str) -> dict[str, Any]:
    jwk_key = get_jwk_key(token)
    try:
        token_data = jwt.decode(
            token,
            jwk_key.key,
            algorithms=JWT_ACCESS_TOKEN_ALGORITHMS,
            options={
                'verify_signature': True,
                'verify_exp': True,
                'verify_aud': False,
                'require': ['sub', 'exp', 'iss'],
            },
        )
        if token_data.get('iss', '').rstrip('/') != settings.AUTH0_URL.rstrip('/'):
            logger.info({'message': 'Invalid "iss" claim'})
            raise AuthError(ErrorMessages.INVALID_TOKEN)

    except jwt.PyJWTError as err:
        logger.info({'message': str(err)})
        raise AuthError(ErrorMessages.INVALID_TOKEN)

    else:
        return token_data


async def authenticate_merchant(
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
        merchant_service: MerchantService = Depends(get_merchant_service),
        business_service: BusinessService = Depends(get_business_service),
) -> Merchant:
    if not token:
        raise AuthError(ErrorMessages.NOT_AUTH)

    token_data = validate_access_token(token.credentials)
    merchant = await merchant_service.get_by_sub(token_data['sub'])

    if not merchant:
        merchant = await merchant_service.create(token.credentials, token_data['sub'])
        await business_service.create_business(merchant)

    request.state.merchant = merchant
    return merchant
