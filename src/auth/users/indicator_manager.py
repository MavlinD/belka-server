from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.indicators import IndicatorAttr, IndicatorCreate, IndicatorScheme
from src.auth.users.exceptions import IndicatorNotExists
from src.django_space.indicators.models import Indicator


class IndicatorManager:
    def __init__(self) -> None:
        self.objects = Indicator.objects

    async def create(self, ad_create: IndicatorCreate) -> IndicatorScheme:
        """Вернуть или создать объявление"""
        ad, _ = await self.objects.aget_or_create(
            name=ad_create.name,
            price=ad_create.price,
            desc=ad_create.desc,
        )
        return await sync_to_async(IndicatorScheme.from_orm)(ad)

    async def update(self, ad: Indicator, payload: dict) -> Indicator:
        """update ad"""

        await self.objects.filter(pk=ad.pk).aupdate(**payload)
        ad: Indicator = await self.get_one_by_uniq_attr(IndicatorAttr(attr=ad.pk))

        return ad

    async def delete(self, ad: Indicator) -> None:
        """remove ad"""
        await self.objects.filter(pk=ad.pk).adelete()

    async def get_one_by_uniq_attr(self, ad_attr: IndicatorAttr) -> Indicator | None:
        """get one ad by uniq attr"""
        attr = ad_attr.attr
        if isinstance(attr, int) or attr.isdigit():
            ad_in_db = await self.objects.filter(pk=attr).afirst()
        else:
            ad_in_db = await self.objects.filter(name=attr).afirst()
        if not ad_in_db:
            raise IndicatorNotExists(ad=attr)
        return ad_in_db

    async def get_list_ads(self) -> QuerySet:
        """Вернёт список объявлений"""
        indicators = await sync_to_async(self.objects.all)()
        return indicators
