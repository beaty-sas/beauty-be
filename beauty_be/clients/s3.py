import uuid

from fastapi import UploadFile
from pydantic import AnyHttpUrl

from beauty_be.clients.aws import AWSClient
from beauty_be.conf.settings import settings


class AWSS3Client(AWSClient):
    CLIENT_TYPE = 's3'

    class ROUTES:
        IMAGE: str = '{env}/attachments/{uuid}.{type}'

    async def save_image(self, file: UploadFile) -> AnyHttpUrl:
        async with self.session.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        ) as s3:
            s3_route = self.ROUTES.IMAGE.format(
                env=settings.ENV,
                uuid=str(uuid.uuid4()),
                type=str(file.filename).split('.')[-1],
            )
            await s3.upload_fileobj(file, settings.S3_BUCKET_NAME, s3_route, ExtraArgs={'ACL': 'public-read'})
            return self._generate_s3_path(s3_route)

    @staticmethod
    def _generate_s3_path(path: str) -> AnyHttpUrl:
        url = 'https://{bucket_name}.s3.{region}.amazonaws.com/{path}'.format(
            bucket_name=settings.S3_BUCKET_NAME,
            region=settings.AWS_DEFAULT_REGION,
            path=path,
        )
        return AnyHttpUrl(url=url)

    async def delete_s3_obj(self, url: AnyHttpUrl) -> None:
        file_key = '/'.join(str(url).split('/')[-3:])
        async with self.session.resource('s3') as s3:
            bucket = await s3.Bucket(settings.S3_BUCKET_NAME)
            await bucket.objects.filter(Key=file_key).delete()
