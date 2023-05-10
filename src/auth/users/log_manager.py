from django.contrib.auth.models import User
from django.db.models import Avg, F, Max, Min, QuerySet
from django.db.models.functions import Round
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.log import LogCreate, LogGetDB
from src.django_space.indicators.models import Indicator, Log


class LogManager:
    def __init__(self) -> None:
        """Объект для работы с БД"""
        self.objects = Log.objects

    async def create(self, payload: LogCreate, indicator: Indicator, user: User) -> Log:
        """Вернуть или создать запись лога"""

        log_, _ = await self.objects.aupdate_or_create(
            indicator=indicator,
            date=payload.date,
            defaults={
                **payload.dict(exclude_none=True, exclude_unset=True),
                "indicator": indicator,
                "user": user,
            },
        )
        return log_

    @staticmethod
    async def get_list_log(payload: LogGetDB) -> QuerySet:
        """Вернет список логов"""
        data = payload.dict(exclude_none=True, exclude_unset=True)
        logs = (
            Log.objects.filter(**data)
            .values(indicator_name=F("indicator__name"))
            .annotate(max=Round(Max("val"), 3), min=Round(Min("val"), 3), avg=Round(Avg("val"), 3))
        )
        return logs
