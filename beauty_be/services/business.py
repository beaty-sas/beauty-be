from sqlalchemy.orm import selectinload

from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import AuthError
from beauty_be.exceptions import DoesNotExistError
from beauty_be.schemas.business import UpdateBusinessSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Business
from beauty_models.beauty_models.models import Merchant


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

    async def is_merchant_business(self, business_id: int, merchant_id: int) -> bool:
        if await self.fetch_one(filters=(self.MODEL.id == business_id, self.MODEL.owner_id == merchant_id)):
            return True
        raise AuthError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    async def get_info_by_merchant(self, merchant_id: int) -> Business:
        if obj := await self.fetch_one(
            filters=(self.MODEL.owner_id == merchant_id,),
            options=(selectinload(self.MODEL.logo), selectinload(self.MODEL.location)),
        ):
            return obj

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=merchant_id))

    async def update_info(self, business_id: int, merchant: Merchant, data: UpdateBusinessSchema) -> Business:
        if await self.is_merchant_business(business_id, int(merchant.id)):
            await self.update(
                filters=(self.MODEL.id == business_id,),
                values={
                    'display_name': data.display_name,
                    'phone_number': data.phone_number,
                    'logo_id': data.logo_id,
                },
            )
            await self.session.commit()
            return await self.get_info(business_id)

        raise AuthError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)
