import datetime
from typing import Generic
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar

from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query
from sqlalchemy.sql import Select

from beauty_be.models.base import Base

ModelT = TypeVar('ModelT', bound=Base)


class BaseService(Generic[ModelT]):
    MODEL: Type[ModelT] = Base

    def __init__(self, session: 'AsyncSession'):
        self.session = session

    async def fetch_one(self, filters: Sequence, options: Sequence = ()) -> Optional[ModelT]:
        query = select(self.MODEL).filter(*filters).options(*options).limit(1)
        return await self.session.scalar(query)

    async def fetch_all(self, query: Query | Select) -> Sequence[ModelT]:
        return (await self.session.scalars(query)).all()

    async def fetch_count(self, query: Query | Select) -> int:
        return await self.session.scalar(query)

    async def update(self, filters: Sequence, values: dict) -> None:
        now = datetime.datetime.now(tz=None)
        if hasattr(self.MODEL, 'updated_at'):
            values['updated_at'] = now
        query = update(self.MODEL).where(*filters).values(**values).execution_options(synchronize_session='fetch')
        await self.session.execute(query)

    async def update_obj(self, obj: ModelT, values: dict, commit: bool = True) -> ModelT:
        await self.update(filters=(self.MODEL.id == obj.id,), values=values)
        obj.__dict__.update(values)  # type: ignore
        if commit:
            await self.session.commit()
        return obj

    async def insert(self, values: dict) -> ModelT:
        return await self.insert_obj(self.MODEL(**values))

    async def insert_obj(self, obj: ModelT, commit: bool = True) -> ModelT:
        now = datetime.datetime.now(tz=None)
        if hasattr(self.MODEL, 'created_at'):
            obj.created = now
        if hasattr(self.MODEL, 'updated_at'):
            obj.updated = now
        self.session.add(obj)
        if commit:
            await self.session.commit()
        return obj

    async def exist(self, filters: Sequence) -> bool:
        query = exists(self.MODEL).where(*filters).select()
        return await self.session.scalar(query)

    async def bulk_delete(self, filters: Sequence) -> None:
        query = delete(self.MODEL).where(*filters)
        await self.session.execute(query)
        await self.session.commit()
