from django.contrib.auth.models import User
from django.db.models import QuerySet
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.log import LogCreate, LogCreateFromList, LogGetDB
from src.django_space.indicators.models import Indicator, Log


class LogManager:
    def __init__(self) -> None:
        """Объект для работы с БД"""
        self.objects = Log.objects

    async def create(self, payload: LogCreate, indicator: Indicator, user: User) -> Log:
        """Вернуть или создать запись лога"""

        log_, _ = await self.objects.aget_or_create(
            **payload.dict(exclude_none=True, exclude_unset=True), indicator=indicator, user=user
        )
        return log_

    async def create_all(self, payload: LogCreateFromList, user: User) -> list[Log]:
        """Создать записи лога"""
        bulk_data = []
        for item in payload.data:
            bulk_data.append(
                Log(
                    val=item.val,
                    date=item.date,
                    user=user,
                    indicator=await Indicator.objects.filter(name=item.name).afirst(),
                )
            )
        log_ = await self.objects.abulk_create(bulk_data)
        return log_

    async def get_list_log(self, payload: LogGetDB) -> QuerySet:
        """Вернет список логов"""
        data = payload.dict(exclude_none=True, exclude_unset=True)
        logs = self.objects.all().filter(**data)
        return logs
