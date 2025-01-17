from typing import Sequence

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import AuthError
from beauty_be.exceptions import DoesNotExistError
from beauty_be.models import Business
from beauty_be.models import Merchant
from beauty_be.schemas.business import UpdateBusinessSchema
from beauty_be.services.base import BaseService


class BusinessService(BaseService[Business]):
    MODEL = Business

    async def get_info(self, slug: str) -> Business:
        filters = (self.MODEL.slug == slug,)
        options = (
            selectinload(self.MODEL.logo),
            selectinload(self.MODEL.banner),
            selectinload(self.MODEL.location),
        )
        if obj := await self.fetch_one(filters=filters, options=options):
            return obj

        raise DoesNotExistError(ErrorMessages.EXPERT_NOT_FOUND.format(object_type=self.MODEL.__name__, slug=slug))

    async def get_info_by_id(self, business_id: int) -> Business:
        filters = (self.MODEL.id == business_id,)
        options = (
            selectinload(self.MODEL.logo),
            selectinload(self.MODEL.banner),
            selectinload(self.MODEL.location),
        )
        if obj := await self.fetch_one(filters=filters, options=options):
            return obj

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=business_id))

    async def is_merchant_business(self, slug: str, merchant_id: int) -> bool:
        if await self.fetch_one(filters=(self.MODEL.slug == slug, self.MODEL.owner_id == merchant_id)):
            return True
        raise AuthError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    async def is_merchant_business_by_id(self, business_id: int, merchant_id: int) -> bool:
        if await self.fetch_one(filters=(self.MODEL.id == business_id, self.MODEL.owner_id == merchant_id)):
            return True
        raise AuthError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

    async def get_info_by_merchant(self, merchant_id: int) -> Business:
        if obj := await self.fetch_one(
                filters=(self.MODEL.owner_id == merchant_id,),
                options=(
                        selectinload(self.MODEL.logo),
                        selectinload(self.MODEL.location),
                        selectinload(self.MODEL.banner),
                ),
        ):
            return obj

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=merchant_id))

    async def update_info(self, business_id: int, merchant: Merchant, data: UpdateBusinessSchema) -> Business:
        if not await self.is_merchant_business_by_id(business_id, int(merchant.id)):
            raise AuthError(ErrorMessages.NOT_ENOUGH_PERMISSIONS)

        values_to_update = data.model_dump(exclude_unset=True, exclude_none=True)
        values_to_update.pop('location', None)
        if data.display_name:
            values_to_update['slug'] = str(slugify(data.display_name))

        await self.update(filters=(self.MODEL.id == business_id,), values=values_to_update)
        await self.session.commit()
        return await self.get_info_by_id(business_id)

    async def create_business(self, merchant: Merchant) -> Business:
        business = Business(
            owner_id=merchant.id,
            display_name=merchant.display_name,
            logo_id=merchant.logo_id,
            name=merchant.display_name,
            slug=slugify(merchant.display_name),  # type: ignore
            phone_number=merchant.phone_number,
        )
        return await self.insert_obj(business)

    async def get_businesses_slug(self) -> Sequence[str]:
        return await self.fetch_all(query=select(self.MODEL.slug))

    async def get_by_id(self, business_id: int) -> Business:
        if obj := await self.fetch_one(filters=(self.MODEL.id == business_id,)):
            return obj

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=business_id))
