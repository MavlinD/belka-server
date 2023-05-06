from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.indicators import IndicatorAttr, IndicatorCreate, IndicatorUpdate
from src.auth.users.exceptions import IndicatorNotExists
from src.django_space.indicators.models import Indicator


class IndicatorManager:
    def __init__(self) -> None:
        self.objects = Indicator.objects

    async def create(self, payload: IndicatorCreate) -> Indicator:
        """Вернуть или создать показатель"""
        ind, _ = await self.objects.aget_or_create(**payload.dict(exclude_none=True, exclude_unset=True))
        return ind
        # return await sync_to_async(IndicatorScheme.from_orm)(ind)

    async def update(self, ind: Indicator, payload: IndicatorUpdate) -> Indicator:
        """Обновить показатель"""

        await self.objects.filter(pk=ind.pk).aupdate(**payload.dict(exclude_none=True, exclude_unset=True))
        ind: Indicator = await self.get_one_by_uniq_attr(IndicatorAttr(attr=ind.pk))

        return ind

    async def delete(self, ind: Indicator) -> None:
        """Удалить показатель"""
        await self.objects.filter(pk=ind.pk).adelete()

    async def get_one_by_uniq_attr(self, ind_attr: IndicatorAttr) -> Indicator | None:
        """Получить показатель по уникальному атрибуту (pk, name)"""
        attr = ind_attr.attr
        if isinstance(attr, int) or attr.isdigit():
            ad_in_db = await self.objects.filter(pk=attr).afirst()
        else:
            ad_in_db = await self.objects.filter(name=attr).afirst()
        if not ad_in_db:
            raise IndicatorNotExists(ad=attr)
        return ad_in_db

    async def get_list_ads(self) -> QuerySet:
        """Вернёт список показателей"""
        indicators = await sync_to_async(self.objects.all)()
        return indicators
