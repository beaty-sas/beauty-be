import logging

from beauty_be.clients.aws import AWSClient
from beauty_be.conf.settings import settings
from beauty_be.schemas.notification import SMSPayloadSchema
from beauty_be.schemas.notification import SMSTemplate

logger = logging.getLogger(__name__)


def get_message_text(body: SMSPayloadSchema) -> str:
    if body.template == SMSTemplate.NEW_ORDER:
        return f'Нове бронювання від {body.name} на {body.date_time}'
    if body.template == SMSTemplate.ORDER_CONFIRMED:
        return f'Ваше бронювання на {body.date_time} підтверджено'
    if body.template == SMSTemplate.ORDER_CANCELLED:
        return f'Ваше бронювання на {body.date_time} скасовано'


class AWSSNSClient(AWSClient):
    CLIENT_TYPE = 'sns'

    async def send_sms_notification(self, body: SMSPayloadSchema, user_id: int) -> None:
        message = get_message_text(body)
        await self.client.publish(
            PhoneNumber=body.phone_number,
            Message=message
        )
        logger.info({
            'message': 'SNS sms notification has been sent',
            'user_id': user_id,
            'json': body.dict()
        })
