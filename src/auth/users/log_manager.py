from datetime import datetime

from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth.models import User
from django.db.models import QuerySet
from fastapi import HTTPException
from logrich.logger_ import errlog, log  # noqa

from src.auth.schemas.log import LogCreate, LogCreateFromList, LogGetDB
from src.auth.users.exceptions import IndicatorNotExists, LogExists
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

    async def get_list_log(self, payload: LogGetDB) -> QuerySet:
        """Вернет список логов"""
        data = payload.dict(exclude_none=True, exclude_unset=True)
        logs = self.objects.all().filter(**data)
        return logs
