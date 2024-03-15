from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile

from beauty_be.api.dependencies.service import get_attachment_service
from beauty_be.schemas.attachment import AttachmentSchema
from beauty_be.services.attachment_service import AttachmentService

router = APIRouter()


@router.post(
    '/attachments',
    summary='Upload attachments',
    status_code=HTTPStatus.CREATED,
    response_model=AttachmentSchema,
    responses={
        201: {'model': AttachmentSchema},
    },
)
async def upload_attachments(
    attachment: UploadFile,
    attachment_service: AttachmentService = Depends(get_attachment_service),
) -> AttachmentSchema:
    return await attachment_service.upload(attachment)
