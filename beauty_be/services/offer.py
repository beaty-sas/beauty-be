from typing import Sequence

from sqlalchemy import select

from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import DoesNotExistError
from beauty_be.schemas.offer import CreateOfferRequestSchema
from beauty_be.services.base import BaseService
from beauty_models.beauty_models.models import Business
from beauty_models.beauty_models.models import Offer


class OfferService(BaseService[Offer]):
    MODEL = Offer

    async def get_by_business_id(self, business_id: int) -> Sequence[Offer]:
        query = select(self.MODEL).where(
            self.MODEL.businesses.any(Business.id == business_id),
        )
        return await self.fetch_all(query=query)

    async def get_by_ids(self, offer_ids: Sequence[int]) -> Sequence[Offer]:
        query = select(self.MODEL).where(
            self.MODEL.id.in_(offer_ids),
        )
        return await self.fetch_all(query=query)

    async def get_by_id(self, offer_id: int) -> Offer | None:
        return await self.fetch_one(filters=(self.MODEL.id == offer_id,))

    async def create_offer(self, data: CreateOfferRequestSchema) -> Offer:
        return await self.insert(values=data.dict())

    async def update_offer(self, offer_id: int, data: CreateOfferRequestSchema) -> Offer:
        if offer := await self.get_by_id(offer_id):
            return await self.update_obj(obj=offer, values=data.dict())

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=offer_id))
