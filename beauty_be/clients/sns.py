import logging

from beauty_be.clients.aws import AWSClient
from beauty_be.conf.settings import settings
from beauty_be.schemas.notification import SMSPayloadSchema

logger = logging.getLogger(__name__)


class AWSSNSClient(AWSClient):
    CLIENT_TYPE = 'sns'

    async def send_sms_notification(self, body: SMSPayloadSchema, user_id: int) -> None:
        # Форматирование сообщения
        message = (
            f"Нове бронювання від {body.values['name']}, "
            f"за номером {body.values['phone_number']} "
            f"на {body.values['date_time']}."
        )

        await self.client.publish(
            PhoneNumber=body.phone_number,
            Message=message
            # TopicArn=settings.SNS_SMS_TOPIC_ARN,
        )
        logger.info({
            'message': 'SNS sms notification has been sent',
            'user_id': user_id,
            'json': body.dict()
        })
