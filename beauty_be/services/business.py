from sqlalchemy.orm import selectinload

from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import DoesNotExistError
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Business


class BusinessService(BaseService[Business]):
    MODEL = Business

    async def get_info(self, business_id: int) -> Business:
        filters = (self.MODEL.id == business_id,)
        options = (
            selectinload(self.MODEL.logo),
            selectinload(self.MODEL.location),
        )
        if obj := await self.fetch_one(filters=filters, options=options):
            return obj

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=business_id))
