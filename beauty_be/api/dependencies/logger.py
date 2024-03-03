import logging
from json import JSONDecodeError
from typing import Callable

import ujson
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingRoute(APIRoute):
    @staticmethod
    async def get_request_body(request: Request) -> dict:
        try:
            return await request.json()
        except JSONDecodeError:
            return {}

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            body = await self.get_request_body(request)
            logger.info({'message': f'External {request.method} request to {request.url}', 'text': ujson.dumps(body)})
            try:
                response = await original_route_handler(request)
                logger.info(
                    {
                        'message': f'External response from {request.url}',
                        'text': response.body.decode(),
                    }
                )
            except Exception as err:
                logger.info(
                    {
                        'message': f'External response from {request.url}',
                        'json': {'error': str(err)},
                    }
                )
                raise err
            return response

        return custom_route_handler
