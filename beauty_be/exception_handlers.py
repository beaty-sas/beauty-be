import logging
from http import HTTPStatus

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from beauty_be import exceptions

logger = logging.getLogger(__name__)


def http_client_exception_handler(request: Request, exc: exceptions.HTTPClientError) -> Response:
    logger.error(
        {
            'message': str(exc),
            'user_id': getattr(request.state, 'user_id', None),
            'event_id': getattr(request.state, 'event_id', None),
        }
    )
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content=HTTPStatus.BAD_GATEWAY.phrase,
    )


async def validation_exception_handler(request: Request, exc: exceptions.ValidationError) -> Response:
    return await request_validation_exception_handler(
        request=request, exc=RequestValidationError(errors=[{'loc': ['body'], 'msg': str(exc), 'type': 'value_error'}])
    )


async def does_not_exist_exception_handler(request: Request, exc: exceptions.DoesNotExistError) -> Response:
    return await http_exception_handler(
        request=request, exc=HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    )


async def already_exist_exception_handler(request: Request, exc: exceptions.AlreadyExistError) -> Response:
    return await http_exception_handler(
        request=request, exc=HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(exc))
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(exceptions.ValidationError)(validation_exception_handler)
    app.exception_handler(exceptions.HTTPClientError)(http_client_exception_handler)
    app.exception_handler(exceptions.DoesNotExistError)(does_not_exist_exception_handler)
    app.exception_handler(exceptions.AlreadyExistError)(already_exist_exception_handler)
