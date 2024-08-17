from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.tests.authenticated_test_client import AuthenticatedTestClient
from beauty_be.tests.factories import AttachmentFactory
from beauty_be.tests.factories import BusinessFactory
from beauty_be.tests.factories import OfferFactory


async def test_get_my_business_info(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    business = BusinessFactory(owner=auth_client.merchant)
    await session.commit()

    response = await auth_client.get('/businesses/my')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': business.id,
        'display_name': business.display_name,
        'slug': business.slug,
        'phone_number': business.phone_number,
        'location': None,
        'logo': {
            'id': business.logo.id,
            'original': business.logo.original,
            'thumbnail': business.logo.thumbnail,
        },
        'banner': {
            'id': business.banner.id,
            'original': business.banner.original,
            'thumbnail': business.banner.thumbnail,
        },
    }


async def test_get_my_business_not_exist(auth_client: AuthenticatedTestClient) -> None:
    response = await auth_client.get('/businesses/my')

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_get_my_business_not_auth(client: AsyncClient) -> None:
    response = await client.get('/businesses/my')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_get_business_ids_empty_list(client: AsyncClient) -> None:
    response = await client.get('/businesses/available')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


async def test_get_business_ids(client: AsyncClient, session: AsyncSession) -> None:
    business = BusinessFactory.create_batch(10)
    await session.commit()

    response = await client.get('/businesses/available')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [business.slug for business in business]


async def test_get_business_info(client: AsyncClient, session: AsyncSession) -> None:
    business = BusinessFactory()
    await session.commit()

    response = await client.get(f'/businesses/{business.slug}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': business.id,
        'display_name': business.display_name,
        'slug': business.slug,
        'phone_number': business.phone_number,
        'location': None,
        'logo': {
            'id': business.logo.id,
            'original': business.logo.original,
            'thumbnail': business.logo.thumbnail,
        },
        'banner': {
            'id': business.banner.id,
            'original': business.banner.original,
            'thumbnail': business.banner.thumbnail,
        },
    }


async def test_get_business_info_not_found(client: AsyncClient) -> None:
    response = await client.get('/businesses/business_slug')

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_patch_business_info_not_found(auth_client: AsyncClient) -> None:
    response = await auth_client.patch('/businesses/1', json={'display_name': 'display_name'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions.'}


async def test_patch_not_my_business(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    business = BusinessFactory()
    await session.commit()

    response = await auth_client.patch(f'/businesses/{business.id}', json={'display_name': 'display_name'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions.'}


async def test_patch_my_business_info(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    business = BusinessFactory(owner=auth_client.merchant)
    logo, banner = AttachmentFactory.create_batch(2)
    await session.commit()

    request_data = {
        'display_name': 'new_display_name',
        'phone_number': 'new_phone_number',
        'description': 'description',
        'location': {
            'name': 'new_location_name',
        },
        'logo_id': logo.id,
        'banner_id': banner.id,
    }
    response = await auth_client.patch(f'/businesses/{business.id}', json=request_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': business.id,
        'display_name': request_data['display_name'],
        'slug': 'new-display-name',
        'phone_number': request_data['phone_number'],
        'location': None,
        'logo': {
            'id': logo.id,
            'original': logo.original,
            'thumbnail': logo.thumbnail,
        },
        'banner': {
            'id': banner.id,
            'original': banner.original,
            'thumbnail': banner.thumbnail,
        },
    }


async def test_get_business_offers(client: AsyncClient, session: AsyncSession) -> None:
    offers = OfferFactory.create_batch(10)
    business = BusinessFactory(offers=offers)
    await session.commit()

    response = await client.get(f'/businesses/{business.slug}/offers')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': offer.id,
            'name': offer.name,
            'price': f'{offer.price}.00',
            'duration': offer.duration,
            'allow_photo': offer.allow_photo,
        }
        for offer in offers
    ]


async def test_get_business_offers_empty(client: AsyncClient, session: AsyncSession) -> None:
    business = BusinessFactory()
    await session.commit()

    response = await client.get(f'/businesses/{business.slug}/offers')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []
