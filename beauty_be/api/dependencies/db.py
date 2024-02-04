from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.conf.db import async_session


async def get_db_session() -> 'AsyncSession':  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session
