from http import HTTPStatus
from unittest.mock import ANY

from httpx import AsyncClient
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.models import Offer
from beauty_be.tests.authenticated_test_client import AuthenticatedTestClient
from beauty_be.tests.factories import BusinessFactory
from beauty_be.tests.factories import OfferFactory


async def test_get_offers_not_auth(client: AsyncClient) -> None:
    response = await client.get('/offers', params={'slug': 'not_existing_slug'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated.'}


async def test_get_offers_not_exist(auth_client: AuthenticatedTestClient) -> None:
    response = await auth_client.get('/offers', params={'slug': 'not_existing_slug'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions.'}


async def test_get_offers(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offers = OfferFactory.create_batch(5)
    business = BusinessFactory(owner=auth_client.merchant, offers=offers)
    await session.commit()

    response = await auth_client.get('/offers', params={'slug': business.slug})

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


async def test_create_offer(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offers = OfferFactory.create_batch(5)
    business = BusinessFactory(owner=auth_client.merchant, offers=offers)
    await session.commit()

    request_data = {
        'name': 'name',
        'price': 100,
        'duration': 30,
        'allow_photo': True,
        'business_id': business.id,
    }

    response = await auth_client.post('/offers', json=request_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': ANY,
        'name': request_data['name'],
        'price': '100',
        'duration': 30,
        'allow_photo': True,
    }
    count = await session.scalar(select(func.count(Offer.id)))
    assert count == 6


async def test_create_offer_already_exist(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offer = OfferFactory(name='my name')
    business = BusinessFactory(owner=auth_client.merchant, offers=[offer])
    await session.commit()

    request_data = {
        'name': 'my name',
        'price': 100,
        'duration': 30,
        'allow_photo': True,
        'business_id': business.id,
    }

    response = await auth_client.post('/offers', json=request_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': ANY,
        'name': request_data['name'],
        'price': '100',
        'duration': 30,
        'allow_photo': True,
    }
    count = await session.scalar(select(func.count(Offer.id)))
    assert count == 1


async def test_create_offer_not_my_business(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offer = OfferFactory()
    business = BusinessFactory(offers=[offer])
    await session.commit()

    request_data = {
        'name': 'my name',
        'price': 100,
        'duration': 30,
        'allow_photo': True,
        'business_id': business.id,
    }

    response = await auth_client.post('/offers', json=request_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions.'}


async def test_update_offer(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offer = OfferFactory(name='my name')
    business = BusinessFactory(owner=auth_client.merchant, offers=[offer])
    await session.commit()

    request_data = {
        'name': 'my name',
        'price': 100,
        'duration': 30,
        'allow_photo': True,
        'business_id': business.id,
    }

    response = await auth_client.patch(f'/offers/{offer.id}', json=request_data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': ANY,
        'name': request_data['name'],
        'price': '100',
        'duration': 30,
        'allow_photo': True,
    }
    await session.refresh(offer)
    count = await session.scalar(select(func.count(Offer.id)))
    assert count == 1
    assert offer.name == 'my name'
    assert offer.price == 100
    assert offer.duration == 30
    assert offer.allow_photo is True


async def test_update_offer_not_my_business(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offer = OfferFactory()
    business = BusinessFactory(offers=[offer])
    await session.commit()

    request_data = {
        'name': 'my name',
        'price': 100,
        'duration': 30,
        'allow_photo': True,
        'business_id': business.id,
    }

    response = await auth_client.patch(f'/offers/{offer.id}', json=request_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions.'}


async def test_delete_offer(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offer = OfferFactory()
    business = BusinessFactory(owner=auth_client.merchant, offers=[offer])
    await session.commit()

    response = await auth_client.delete(f'/offers/{offer.id}/delete', params={'slug': business.slug})

    assert response.status_code == HTTPStatus.NO_CONTENT
    count = await session.scalar(select(func.count(Offer.id)))
    assert count == 1
    await session.refresh(offer)
    assert offer.deleted_at is not None


async def test_delete_offer_not_my_business(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    offer = OfferFactory()
    business = BusinessFactory(offers=[offer])
    await session.commit()

    response = await auth_client.delete(f'/offers/{offer.id}/delete', params={'slug': business.slug})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not enough permissions.'}
