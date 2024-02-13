from beauty_be.clients.base import BaseHTTPClient
from beauty_be.conf.settings import settings
from beauty_be.schemas.auth0 import Auth0UserSchema


class Auth0Client(BaseHTTPClient):
    SCOPE: str = 'openid profile email offline_access'

    class ROUTES:
        USER_INFO: str = '/userinfo'

    async def get_user_info(self, token: str) -> Auth0UserSchema:
        headers = {'Authorization': f'Bearer {token}'}
        response = await self.get(self.ROUTES.USER_INFO, headers=headers)
        return Auth0UserSchema(**response.json())


auth0_client = Auth0Client(settings.AUTH0_URL)
