import logging
import uuid
from typing import Dict

from beauty_be.clients.aws import AWSClient
from beauty_be.conf.settings import settings
from beauty_be.schemas.notification import SMSPayloadSchema

logger = logging.getLogger(__name__)


class AWSSQSClient(AWSClient):
    CLIENT_TYPE = 'sqs'

    async def send_message(self, queue: str, body: str, user_id: int, fifo: bool = False) -> None:
        logger.info({'message': f'Sending sqs message to {queue}. Body: {body}', 'user_id': user_id})
        if fifo:
            response = await self.client.send_message(
                QueueUrl=queue,
                MessageBody=body,
                MessageDeduplicationId=str(uuid.uuid4()),
                MessageGroupId=str(uuid.uuid4()),
            )
        else:
            response = await self.client.send_message(QueueUrl=queue, MessageBody=body)
        self._check_response(response, queue, user_id=user_id)

    async def send_sms_notification(self, body: SMSPayloadSchema, user_id: int) -> None:
        await self.send_message(settings.SQS_SMS_NOTIFICATION_QUEUE, body.json(), user_id)
        logger.info({'message': 'SQS sms notification has been send', 'user_id': user_id, 'json': body.dict()})

    @staticmethod
    def _check_response(response: Dict, queue: str, user_id: int) -> None:
        response_metadata = response.get('ResponseMetadata')
        status_code = response_metadata.get('HTTPStatusCode') if response_metadata else None
        logger.info(
            {
                'message': f'Receiver response from {queue} with status code {status_code}',
                'user_id': user_id,
                'game_id': None,
                'match_id': None,
            }
        )
