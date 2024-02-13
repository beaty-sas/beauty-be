from fastapi import UploadFile

from beauty_be.clients import aws_client
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Attachment


class AttachmentService(BaseService[Attachment]):
    MODEL = Attachment

    async def upload(self, file: UploadFile) -> 'Attachment':
        image_url = await aws_client.save_image(file)
        obj = self.MODEL(original=str(image_url), thumbnail=str(image_url))
        return await self.insert_obj(obj)
