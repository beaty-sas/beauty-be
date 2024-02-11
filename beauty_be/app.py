from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from beauty_be import __version__
from beauty_be.api import attachments
from beauty_be.api import base
from beauty_be.api import booking
from beauty_be.api import business
from beauty_be.api import merchant
from beauty_be.api import offer
from beauty_be.api import working_hours
from beauty_be.conf.db import async_session
from beauty_be.conf.settings import Settings
from beauty_be.conf.settings import settings
from beauty_be.exception_handlers import init_exception_handlers
from beauty_be.middlewares import init_middlewares
from beauty_models.beauty_models.models import metadata


def init_routes(app: 'FastAPI') -> None:
    app.include_router(base.router, tags=['Base'])
    app.include_router(offer.router, tags=['Offer'])
    app.include_router(booking.router, tags=['Booking'])
    app.include_router(business.router, tags=['Business'])
    app.include_router(merchant.router, tags=['Merchant'])
    app.include_router(attachments.router, tags=['Attachment'])
    app.include_router(working_hours.router, tags=['Working Hours'])


def init_db(app_settings: Settings):
    engine = create_async_engine(app_settings.sqlalchemy_database_uri)
    async_session.configure(bind=engine)
    metadata.bind = engine  # type: ignore


def create_app(app_settings: Settings | None = None) -> FastAPI:
    app_settings = app_settings if app_settings is not None else settings
    init_db(app_settings)
    app = FastAPI(
        title='Beauty API',
        debug=app_settings.DEBUG,
        docs_url='/docs',
        redoc_url='/redoc',
        version=__version__,
    )
    init_middlewares(app, app_settings)
    init_exception_handlers(app)
    init_routes(app)
    return app
