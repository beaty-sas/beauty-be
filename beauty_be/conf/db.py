from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async_session = sessionmaker(None, expire_on_commit=False, class_=AsyncSession)
