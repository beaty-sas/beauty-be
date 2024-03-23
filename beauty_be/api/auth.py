from http import HTTPStatus

from fastapi import APIRouter

from beauty_be.api.dependencies.logger import LoggingRoute
from beauty_be.clients.auth0 import auth0_client
from beauty_be.schemas.auth import LoginRequestSchema
from beauty_be.schemas.auth import RegisterSocialRequestSchema
from beauty_be.schemas.auth import RegisterSocialResponseSchema
from beauty_be.schemas.auth import TokenSchema

router = APIRouter(route_class=LoggingRoute)


@router.post(
    '/auth/sign-in',
    summary='Login user with email and password',
    response_model=TokenSchema,
    status_code=HTTPStatus.OK,
)
async def sign_in_with_password(
    request_data: LoginRequestSchema,
) -> TokenSchema:
    return await auth0_client.login_with_password(request_data)


@router.post(
    '/auth/sign-in/social',
    summary='Login user with social provider',
    response_model=RegisterSocialResponseSchema,
)
async def sign_in_with_social_provider(
    request_data: RegisterSocialRequestSchema,
) -> RegisterSocialResponseSchema:
    return await auth0_client.get_social_auth_url(request_data)


@router.post(
    '/auth/sign-up',
    summary='Register user with email and password',
    response_model=TokenSchema,
)
async def register_user_with_password(
    request_data: LoginRequestSchema,
) -> TokenSchema:
    await auth0_client.sign_up_user(request_data)
    return await auth0_client.login_with_password(request_data)
