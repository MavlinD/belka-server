from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.indicators import IndicatorAttr, IndicatorCreate, IndicatorUpdate
from src.auth.users.exceptions import IndicatorExists, IndicatorNotExists
from src.django_space.indicators.models import Indicator


class IndicatorManager:
    def __init__(self) -> None:
        """Объект для работы с БД"""
        self.objects = Indicator.objects

    async def create(self, payload: IndicatorCreate) -> Indicator:
        """Вернуть или создать показатель"""

        indicator, _ = await self.objects.aget_or_create(**payload.dict(exclude_none=True, exclude_unset=True))
        return indicator

    async def update(self, indicator: Indicator, payload: IndicatorUpdate) -> Indicator:
        """Обновить показатель"""

        await self.objects.filter(pk=indicator.pk).aupdate(**payload.dict(exclude_none=True, exclude_unset=True))
        indicator: Indicator = await self.get_one_by_uniq_attr(IndicatorAttr(attr=indicator.pk))

        return indicator

    async def delete(self, indicator: Indicator) -> None:
        """Удалить показатель"""

        await self.objects.filter(pk=indicator.pk).adelete()

    async def get_one_by_uniq_attr(self, indicator_attr: IndicatorAttr) -> Indicator | None:
        """Получить показатель по уникальному атрибуту (pk, name)"""

        attr = indicator_attr.attr
        if isinstance(attr, int) or attr.isdigit():
            indicator_in_db = await self.objects.filter(pk=attr).afirst()
        else:
            indicator_in_db = await self.objects.filter(name=attr).afirst()
        if not indicator_in_db:
            raise IndicatorNotExists(indicator=attr)
        return indicator_in_db

    async def check_one_by_uniq_attr(self, indicator_attr: IndicatorAttr) -> None:
        """Проверить существование показателя по уникальному атрибуту (pk, name)"""

        try:
            indicator: Indicator = await self.get_one_by_uniq_attr(indicator_attr=indicator_attr)
            if indicator:
                raise IndicatorExists(indicator.name)
        except IndicatorNotExists:
            # нужен противоположный ответ
            pass

    async def get_list_indicators(self) -> QuerySet:
        """Вернёт список показателей"""

        indicators = await sync_to_async(self.objects.all)()
        return indicators
