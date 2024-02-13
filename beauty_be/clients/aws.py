import uuid

import aioboto3
from fastapi import UploadFile
from pydantic import AnyHttpUrl

from beauty_be.conf.settings import settings


class AWSClient:
    class ROUTES:
        IMAGE: str = '{env}/attachments/{uuid}.{type}'

    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket_name = settings.S3_BUCKET_NAME

    async def save_image(self, file: UploadFile) -> AnyHttpUrl:
        async with self.session.client('s3') as s3:
            s3_route = self.ROUTES.IMAGE.format(
                env=settings.ENV,
                uuid=str(uuid.uuid4()),
                type=str(file.filename).split('.')[-1],
            )
            await s3.upload_fileobj(file, self.bucket_name, s3_route, ExtraArgs={'ACL': 'public-read'})
            return self._generate_s3_path(s3_route)

    def _generate_s3_path(self, path: str) -> AnyHttpUrl:
        url = 'https://{bucket_name}.s3.{region}.amazonaws.com/{path}'.format(
            bucket_name=self.bucket_name,
            region=settings.AWS_DEFAULT_REGION,
            path=path,
        )
        return AnyHttpUrl(url=url)

    async def delete_s3_obj(self, url: AnyHttpUrl) -> None:
        file_key = '/'.join(str(url).split('/')[-3:])
        async with self.session.resource('s3') as s3:
            bucket = await s3.Bucket(self.bucket_name)
            await bucket.objects.filter(Key=file_key).delete()
