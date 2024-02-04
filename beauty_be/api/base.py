from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from beauty_be.api.dependencies.db import get_db_session
from beauty_be.schemas.base import HealthSchema
from beauty_be.schemas.base import VersionSchema

router = APIRouter()


@router.get(
    '/health',
    summary='Health check',
    status_code=HTTPStatus.OK,
    response_model=HealthSchema,
    responses={
        200: {'model': HealthSchema},
        500: {'model': HealthSchema},
    },
)
async def health(db_session: AsyncSession = Depends(get_db_session)) -> HealthSchema:
    await db_session.execute(select(1))
    return HealthSchema(db=True)


@router.get(
    '/version',
    summary='API version',
    response_model=VersionSchema,
)
async def version(request: Request) -> VersionSchema:
    return VersionSchema(version=request.app.version)
