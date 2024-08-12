from beauty_be.clients import aws_sqs_client
from beauty_be.schemas.notification import SMSPayloadSchema
from beauty_be.schemas.notification import SMSTemplate
from beauty_be.schemas.user import UserSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Booking
from beauty_models.beauty_models.models import User


class UserService(BaseService[User]):
    MODEL = User

    async def get_or_create_by_phone_number(self, user_data: UserSchema) -> User:
        if user := await self.fetch_one(filters=(self.MODEL.phone_number == user_data.phone_number,)):
            return user

        user = self.MODEL(phone_number=user_data.phone_number, display_name=user_data.display_name)
        return await self.insert_obj(user)

    async def notify_user(self, booking: Booking, template: SMSTemplate) -> None:
        user = await self.fetch_one(
            filters=(self.MODEL.bookings.any(Booking.id == booking.id),),
        )
        if not user:
            return

        body = SMSPayloadSchema(
            phone_number=str(user.phone_number.replace(' ', '')),
            template=template,
            values={
                'date_time': booking.start_time.strftime('%d.%m.%Y %H:%M'),
            },
        )
        await aws_sqs_client.send_sms_notification(body, int(user.id))
