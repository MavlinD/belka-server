from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from djantic import ModelSchema
from fastapi import Body, Query
from logrich.logger_ import log  # noqa
from pydantic import BaseModel, Field, validator

from src.django_space.indicators.config import config
from src.django_space.indicators.models import Indicator


class DataItem(BaseModel):
    """Схема для валидации строки в массиве входящих на запись данных"""

    name: Annotated[
        str,
        Field(title="Имя показателя", min_length=config.IND_NAME_MIN_LENGTH, max_length=config.IND_NAME_MAX_LENGTH),
    ]
    val: float
    date: datetime


class LogCreateFromList(BaseModel):
    """Схема для создания записей лога"""

    data: list[DataItem] = Body(title="Значения показателей, кортежи из трех полей")

    @validator("data", pre=True, each_item=True)
    def get_data(cls, val):
        return DataItem(name=val[0], val=val[1], date=val[2])


class LogCreate(BaseModel):
    """Схема для создания записи лога"""

    val: float = Body(ge=0, title="Значение показателя")
    date: Annotated[datetime, Field(title="Период регистрации")] = False


@dataclass
class LogGetQuery:
    """Схема валидации параметров запроса логов"""

    indicator_attr = Annotated[
        str,
        Query(
            description="Уникальный идентификатор показателя, ID или name",
            max_length=config.IND_NAME_MAX_LENGTH,
        ),
    ]
    date__gte = Annotated[datetime, Query(description="Начало периода")]
    date__lte = Annotated[datetime, Query(description="Конец периода")]


class LogGetDB(BaseModel):
    """Схема валидации параметров запроса к БД"""

    indicator_id: str | None
    date__gte: datetime | None
    date__lte: datetime | None


class IndicatorInLog(ModelSchema):
    """Схема для списка логов"""

    class Config:
        model = Indicator
        include = ["id", "unit", "name"]


class UserInLog(ModelSchema):
    """Схема для списка логов"""

    class Config:
        model = User
        include = ["id", "username"]


class LogScheme(BaseModel):
    """Общая схема лога"""

    id: int
    val: float
    date: datetime
    user: UserInLog
    indicator: IndicatorInLog

    class Config:
        orm_mode = True

    @classmethod
    async def from_orms(cls, v):
        """reload from_orm method"""
        return await sync_to_async(cls.from_orm)(v)
