from http import HTTPStatus
from unittest.mock import ANY
from unittest.mock import patch

from httpx import AsyncClient
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from beauty_be.clients.s3 import AWSS3Client
from beauty_be.models import Attachment


async def test_create_new_attachment(auth_client: AsyncClient, session: AsyncSession) -> None:
    mock_image_url = 'https://mock-bucket.s3.mock-region.amazonaws.com/mock-path'

    with patch.object(AWSS3Client, 'save_image', return_value=mock_image_url):
        response = await auth_client.post('/attachments', files={'attachment': ('image.jpg', b'fake_image')})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': ANY,
        'original': mock_image_url,
        'thumbnail': mock_image_url,
    }

    attachment = await session.scalar(select(Attachment).filter(Attachment.id == response.json()['id']))
    assert attachment is not None


async def test_create_new_attachment_bad_request(auth_client: AsyncClient, session: AsyncSession) -> None:
    mock_image_url = 'https://mock-bucket.s3.mock-region.amazonaws.com/mock-path'
    start_count = await session.scalar(select(func.count(Attachment.id)))

    with patch.object(AWSS3Client, 'save_image', return_value=mock_image_url):
        response = await auth_client.post('/attachments')

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    after_request_call_count = await session.scalar(select(func.count(Attachment.id)))
    assert start_count == after_request_call_count


async def test_create_new_attachment_not_auth(client: AsyncClient, session: AsyncSession) -> None:
    mock_image_url = 'https://mock-bucket.s3.mock-region.amazonaws.com/mock-path'

    with patch.object(AWSS3Client, 'save_image', return_value=mock_image_url):
        response = await client.post('/attachments', files={'attachment': ('image.jpg', b'fake_image')})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': ANY,
        'original': mock_image_url,
        'thumbnail': mock_image_url,
    }

    attachment = await session.scalar(select(Attachment).filter(Attachment.id == response.json()['id']))
    assert attachment is not None
