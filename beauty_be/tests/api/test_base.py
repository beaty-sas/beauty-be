from http import HTTPStatus

from httpx import AsyncClient

from beauty_be import __version__


async def test_health(client: AsyncClient) -> None:
    response = await client.get('/health')
    assert response.status_code == HTTPStatus.OK


async def test_version(client: AsyncClient) -> None:
    response = await client.get('/version')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['version'] == __version__
