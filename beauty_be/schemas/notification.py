from enum import Enum
from typing import Any

from pydantic import BaseModel


class SMSTemplate(str, Enum):
    NEW_ORDER = 'NEW_ORDER'
    ORDER_CONFIRMED = 'ORDER_CONFIRMED'
    ORDER_CANCELLED = 'ORDER_CANCELLED'


class SMSPayloadSchema(BaseModel):
    phone_number: str
    template: SMSTemplate
    values: dict[str, Any]
