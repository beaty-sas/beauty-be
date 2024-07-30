from enum import Enum
from typing import Any

from pydantic import BaseModel


class SMSTemplate(str, Enum):
    NEW_ORDER = 'NEW_ORDER'
    ORDER_CONFIRMED = 'ORDER_CONFIRMED'
    ORDER_CANCELLED = 'ORDER_CANCELLED'


class SMSPayloadSchema(BaseModel):
    phone_number: str
    name: str
    date_time: str
    template: SMSTemplate
    values: dict[str, Any]


class SQSNotificationSchema(BaseModel):
    send_sms: bool = True
    sms_data: SMSPayloadSchema
