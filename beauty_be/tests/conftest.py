import asyncio
import time
from asyncio import AbstractEventLoop
from typing import AsyncGenerator
from typing import Generator

import pytest
import sqlalchemy as sa
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from beauty_be.app import create_app
from beauty_be.conf.db import async_session
from beauty_be.conf.settings import Settings
from beauty_be.conf.settings import settings
from beauty_be.tests.factories import FACTORIES
from beauty_models.beauty_models.models import metadata


async def _create_test_db(engine: 'AsyncEngine', new_db_name: str):
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(sa.text('DROP DATABASE IF EXISTS %s' % new_db_name))
        await conn.execute(sa.text('CREATE DATABASE %s' % new_db_name))


async def _drop_test_db(engine: 'AsyncEngine', new_db_name: str):
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(sa.text('DROP DATABASE %s' % new_db_name))


@pytest.fixture(scope='session')
def test_db_name() -> str:
    return f'companion_tests_{int(time.time())}'


@pytest.fixture(scope='session')
def test_settings(test_db_name: str):
    return Settings(DB_NAME=test_db_name)


@pytest.fixture(scope='session', autouse=True)
async def init_test_db(
    event_loop: 'AbstractEventLoop',
    test_settings: Settings,
    test_db_name: str,
) -> AsyncGenerator[None, None]:
    conn_url = settings.sqlalchemy_database_uri
    engine = create_async_engine(conn_url)
    await _create_test_db(engine, test_db_name)
    test_engine = create_async_engine(test_settings.sqlalchemy_database_uri)
    async with test_engine.begin() as conn:
        await conn.execute(sa.text('CREATE EXTENSION postgis'))
        await conn.run_sync(metadata.create_all)

    yield

    await test_engine.dispose()
    if metadata.bind:  # type: ignore
        await metadata.bind.dispose()  # type: ignore
    await _drop_test_db(engine, test_db_name)


@pytest.fixture(scope='session')
def app(test_settings: Settings) -> 'FastAPI':
    app = create_app(test_settings)
    return app


@pytest.fixture(scope='session')
async def session(app: 'FastAPI') -> AsyncGenerator['AsyncSession', None]:
    async with async_session() as session:  # type: ignore
        for factory_ in FACTORIES:
            factory_._meta.sqlalchemy_session = session

        yield session


@pytest.fixture(scope='function', autouse=True)
async def clear_db(session: 'AsyncSession') -> AsyncGenerator[None, None]:
    yield

    await session.execute(text('TRUNCATE {};'.format(','.join(table.name for table in metadata.tables.values()))))
    await session.commit()


@pytest.fixture(scope='session')
async def client(app: 'FastAPI') -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
def event_loop() -> Generator['AbstractEventLoop', None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def non_mocked_hosts() -> list:
    return ['test']
