from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.db.models import QuerySet
from fastapi import Depends
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.indicators import IndicatorAttr
from src.auth.schemas.log import LogCreate, LogGetPy, LogScheme
from src.auth.users.exceptions import LogNotExists

# from src.auth.users.indicator_manager import IndicatorManager
# from src.auth.users.init import get_indicator_manager
from src.django_space.indicators.models import Indicator, Log


class LogManager:
    def __init__(self) -> None:
        """Объект для работы с БД"""
        self.objects = Log.objects
        # self.indicator_manager: IndicatorManager = Depends(get_indicator_manager)

    async def create(self, payload: LogCreate, indicator: Indicator, user: User) -> Log:
        """Вернуть или создать запсиь лога"""

        log_, _ = await self.objects.aget_or_create(
            **payload.dict(exclude_none=True, exclude_unset=True), indicator_id=indicator, uid=user
        )
        return log_

    async def get_list_log(self, payload: LogGetPy) -> QuerySet:
        """Вернет список логов"""
        # indicator_attr = IndicatorAttr(attr=payload.indicator_attr)
        # indicator = await self.indicator_manager.get_one_by_uniq_attr(indicator_attr=indicator_attr)
        logs = self.objects.all().filter(**payload.dict(exclude_none=True, exclude_unset=True))
        return logs

    # async def get_one_by_uniq_attr(self, indicator_attr: int) -> Log | None:
    #     """get one ind by uniq attr"""
    #     image_in_db = await self.objects.filter(pk=indicator_attr).afirst()
    #     if not image_in_db:
    #         raise LogNotExists(image=indicator_attr)
    #     return image_in_db
