from datetime import datetime
from typing import Sequence

from sqlalchemy import insert
from sqlalchemy import select

from beauty_be.conf.constants import ErrorMessages
from beauty_be.exceptions import DoesNotExistError
from beauty_be.models import Business
from beauty_be.models import business_offers
from beauty_be.models import Offer
from beauty_be.schemas.offer import CreateOfferRequestSchema
from beauty_be.services.base import BaseService


class OfferService(BaseService[Offer]):
    MODEL = Offer

    async def get_by_business_slug(self, slug: str) -> Sequence[Offer]:
        query = select(self.MODEL).where(
            self.MODEL.businesses.any(Business.slug == slug),
            self.MODEL.deleted_at.is_(None),
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
        exist_offer = await self.fetch_one(
            filters=(
                self.MODEL.businesses.any(Business.id == data.business_id),
                self.MODEL.name == data.name,
            )
        )

        if exist_offer:
            updated_offer = await self.update_obj(
                exist_offer,
                values={
                    'deleted_at': None,
                    'price': data.price,
                    'duration': data.duration,
                    'allow_photo': data.allow_photo,
                },
            )
            return updated_offer

        offer = await self.insert(
            values={
                'name': data.name,
                'price': data.price,
                'duration': data.duration,
                'allow_photo': data.allow_photo,
            }
        )
        query = insert(business_offers).values(business_id=data.business_id, offer_id=offer.id)
        await self.session.execute(query)
        await self.session.commit()
        return offer

    async def update_offer(self, offer_id: int, data: CreateOfferRequestSchema) -> Offer:
        if offer := await self.get_by_id(offer_id):
            values = {
                'name': data.name,
                'price': data.price,
                'duration': data.duration,
                'allow_photo': data.allow_photo,
            }
            return await self.update_obj(obj=offer, values=values)

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=offer_id))

    async def delete_offer(self, offer_id: int) -> None:
        if offer := await self.get_by_id(offer_id):
            await self.update_obj(offer, values={'deleted_at': datetime.now()})
            return

        raise DoesNotExistError(ErrorMessages.OBJECT_NOT_FOUND.format(object_type=self.MODEL.__name__, id=offer_id))
