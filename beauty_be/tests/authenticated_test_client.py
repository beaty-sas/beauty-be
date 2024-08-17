# mypy: ignore-errors
from types import TracebackType

from httpx import AsyncClient
from httpx import Response

from beauty_be.api.dependencies.auth import authenticate_merchant
from beauty_be.models import Merchant


class AuthenticatedTestClient(AsyncClient):
    def __init__(self, merchant: Merchant, *args, **kwargs):
        super(AuthenticatedTestClient, self).__init__(*args, **kwargs)
        self.merchant = merchant

    async def request(self, *args, **kwargs) -> Response:
        headers = kwargs.get('headers') or {}
        headers['Authorization'] = 'Bearer secure_token'
        kwargs['headers'] = headers
        return await super(AuthenticatedTestClient, self).request(*args, **kwargs)

    def _mock_auth_dependency(self):
        self._transport.app.dependency_overrides[authenticate_merchant] = lambda: self.merchant

    def _unmock_auth_dependency(self):
        if authenticate_merchant in self._transport.app.dependency_overrides:
            del self._transport.app.dependency_overrides[authenticate_merchant]

    async def __aenter__(self):
        self._mock_auth_dependency()
        await super().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ):
        self._unmock_auth_dependency()
        await super().__aexit__(exc_type, exc_value, traceback)
