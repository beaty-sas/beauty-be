from datetime import datetime
from datetime import timedelta
from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.tests.authenticated_test_client import AuthenticatedTestClient
from beauty_be.tests.factories import BookingFactory
from beauty_be.tests.factories import BusinessFactory


async def test_get_booking_analytic_zero(auth_client: AsyncClient) -> None:
    response = await auth_client.get('/analytics/booking')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'total': 0,
        'future': 0,
        'today': 0,
    }


async def test_get_booking_analytic_total(auth_client: AuthenticatedTestClient, session: AsyncSession) -> None:
    business = BusinessFactory(owner=auth_client.merchant)
    BookingFactory.create_batch(
        size=15,
        business=business,
        start_time=datetime.now() - timedelta(days=100),
        end_time=datetime.now() - timedelta(days=99),
    )
    await session.commit()

    response = await auth_client.get('/analytics/booking')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'total': 15,
        'future': 0,
        'today': 0,
    }


async def test_get_booking_analytic_total_and_future(
        auth_client: AuthenticatedTestClient,
        session: AsyncSession,
) -> None:
    business = BusinessFactory(owner=auth_client.merchant)
    BookingFactory.create_batch(
        size=20,
        business=business,
        start_time=datetime.now() - timedelta(days=100),
        end_time=datetime.now() - timedelta(days=99),
    )
    BookingFactory.create_batch(
        size=10,
        business=business,
        start_time=datetime.now() + timedelta(days=2),
        end_time=datetime.now() + timedelta(days=2),
    )
    await session.commit()

    response = await auth_client.get('/analytics/booking')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'total': 30,
        'future': 10,
        'today': 0,
    }


async def test_get_booking_analytic_total_and_future_and_today(
        auth_client: AuthenticatedTestClient,
        session: AsyncSession,
) -> None:
    business = BusinessFactory(owner=auth_client.merchant)
    BookingFactory.create_batch(
        size=20,
        business=business,
        start_time=datetime.now() - timedelta(days=100),
        end_time=datetime.now() - timedelta(days=99),
    )
    BookingFactory.create_batch(
        size=10,
        business=business,
        start_time=datetime.now() + timedelta(days=2),
        end_time=datetime.now() + timedelta(days=2),
    )
    BookingFactory.create_batch(
        size=10,
        business=business,
        start_time=datetime.now() + timedelta(seconds=1),
        end_time=datetime.now() + timedelta(minutes=2),
    )
    await session.commit()

    response = await auth_client.get('/analytics/booking')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'total': 40,
        'future': 20,
        'today': 10,
    }


async def test_get_booking_analytic_not_auth(
        client: AsyncClient,
        session: AsyncSession,
) -> None:
    business = BusinessFactory()
    BookingFactory.create_batch(
        size=20,
        business=business,
        start_time=datetime.now() - timedelta(days=100),
        end_time=datetime.now() - timedelta(days=99),
    )
    await session.commit()

    response = await client.get('/analytics/booking')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated.'}
