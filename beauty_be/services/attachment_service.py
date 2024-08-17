from typing import Sequence

from fastapi import UploadFile
from sqlalchemy import select

from beauty_be.clients import aws_s3_client
from beauty_be.models import Attachment
from beauty_be.services.base import BaseService


class AttachmentService(BaseService[Attachment]):
    MODEL = Attachment

    async def upload(self, file: UploadFile) -> Attachment:
        image_url = await aws_s3_client.save_image(file)
        obj = self.MODEL(original=str(image_url), thumbnail=str(image_url))
        return await self.insert_obj(obj)

    async def get_by_ids(self, ids: list[int]) -> Sequence[Attachment]:
        query = select(self.MODEL).where(self.MODEL.id.in_(ids))
        return await self.fetch_all(query=query)
