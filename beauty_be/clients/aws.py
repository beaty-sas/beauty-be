import contextlib
import logging
from typing import TYPE_CHECKING

import aioboto3

from beauty_be.conf.settings import settings
from beauty_be.exceptions import AWSClientError

if TYPE_CHECKING:
    from aiobotocore.client import AioBaseClient

logger = logging.getLogger(__name__)


class AWSClient:
    CLIENT_TYPE: str

    def __init__(self):
        self._client = None
        self._context_stack = contextlib.AsyncExitStack()
        self.session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    @property
    def client(self) -> 'AioBaseClient':
        if not self._client:
            raise AWSClientError(f'AWS {self.CLIENT_TYPE.upper()} client not configured')
        return self._client

    async def configure(self, region: str = settings.AWS_DEFAULT_REGION):
        self._client = await self._context_stack.enter_async_context(
            self.session.client(self.CLIENT_TYPE, region_name=region)
        )
        logger.info({'message': f'AWS {self.CLIENT_TYPE.upper()} client has been configured.'})

    async def close(self):
        await self._context_stack.aclose()
