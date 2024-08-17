from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.tests.authenticated_test_client import AuthenticatedTestClient
from beauty_be.tests.factories import BusinessFactory


async def test_get_merchant_profile_not_auth(client: AsyncClient) -> None:
    response = await client.get('/me')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_get_merchant_profile(auth_client: AuthenticatedTestClient) -> None:
    response = await auth_client.get('/me')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'sub': auth_client.merchant.sub,
        'display_name': auth_client.merchant.display_name,
        'phone_number': auth_client.merchant.phone_number,
        'logo_id': auth_client.merchant.logo_id,
        'businesses': [],
    }


async def test_get_merchant_profile_with_business(
        auth_client: AuthenticatedTestClient,
        session: AsyncSession,
) -> None:
    businesses = BusinessFactory.create_batch(3, owner=auth_client.merchant)
    await session.commit()

    response = await auth_client.get('/me')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'sub': auth_client.merchant.sub,
        'display_name': auth_client.merchant.display_name,
        'phone_number': auth_client.merchant.phone_number,
        'logo_id': auth_client.merchant.logo_id,
        'businesses': [
            {
                'id': business.id,
                'display_name': business.display_name,
                'phone_number': business.phone_number,
                'slug': business.slug,
            }
            for business in businesses
        ],
    }


async def test_patch_merchant_profile(auth_client: AuthenticatedTestClient) -> None:
    request_data = {
        'display_name': 'new_display_name',
        'phone_number': '380502924991',
    }

    response = await auth_client.patch('/me', json=request_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'sub': auth_client.merchant.sub,
        'display_name': request_data['display_name'],
        'phone_number': request_data['phone_number'],
        'logo_id': auth_client.merchant.logo_id,
        'businesses': [],
    }
