from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.tests.factories.business import BusinessFactory


async def test_get_businesses(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    BusinessFactory.create_batch(10)
    await session.commit()

    response = await client.get('/businesses')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 10
