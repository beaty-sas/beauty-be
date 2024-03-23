import urllib.parse

from beauty_be.clients.base import BaseHTTPClient
from beauty_be.conf.settings import settings
from beauty_be.schemas.auth import LoginRequestSchema
from beauty_be.schemas.auth import RegisterSocialRequestSchema
from beauty_be.schemas.auth import RegisterSocialResponseSchema
from beauty_be.schemas.auth import TokenSchema
from beauty_be.schemas.auth0 import Auth0UserSchema


class Auth0Client(BaseHTTPClient):
    SCOPE: str = 'openid profile email offline_access'

    class ROUTES:
        USER_INFO: str = '/userinfo'
        SIGN_IN: str = '/oauth/token'
        SIGN_UP: str = '/dbconnections/signup'
        SIGN_UP_PROVIDER: str = '/authorize'

    async def get_user_info(self, token: str) -> Auth0UserSchema:
        headers = {'Authorization': f'Bearer {token}'}
        response = await self.get(self.ROUTES.USER_INFO, headers=headers)
        return Auth0UserSchema(**response.json())

    async def login_with_password(self, data: LoginRequestSchema) -> TokenSchema:
        body = {
            'client_id': settings.AUTH0_CLIENT_ID,
            'username': data.email,
            'password': data.password.get_secret_value(),
            'realm': 'Username-Password-Authentication',
            'scope': self.SCOPE,
            'audience': settings.AUTH0_AUDIENCE,
            'grant_type': 'http://auth0.com/oauth/grant-type/password-realm',
            'client_secret': settings.AUTH0_CLIENT_SECRET,
        }
        response = await self.post(url=self.ROUTES.SIGN_IN, data=body)
        return TokenSchema(**response.json())

    async def get_social_auth_url(self, data: RegisterSocialRequestSchema) -> RegisterSocialResponseSchema:
        params = {
            'response_type': 'token',
            'client_id': settings.AUTH0_CLIENT_ID,
            'connection': data.provider.value,
            'redirect_uri': data.redirect_url,
            'audience': settings.AUTH0_AUDIENCE,
            'scope': self.SCOPE,
        }
        url = f'{self.get_url(self.ROUTES.SIGN_UP_PROVIDER)}?{urllib.parse.urlencode(params)}'
        return RegisterSocialResponseSchema(url=url)

    async def sign_up_user(self, data: LoginRequestSchema) -> dict:
        body = {
            'client_id': settings.AUTH0_CLIENT_ID,
            'email': data.email,
            'name': data.email,
            'password': data.password.get_secret_value(),
            'connection': settings.AUTH0_DATABASE,
        }
        response = await self.post(self.ROUTES.SIGN_UP, data=body)
        return response.json()


auth0_client = Auth0Client(settings.AUTH0_URL)
