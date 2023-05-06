from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any

from asgiref.sync import sync_to_async
from djantic import ModelSchema
from fastapi import Body, Query
from logrich.logger_ import log  # noqa
from pydantic import BaseModel, Field

from src.auth.schemas.indicators import IndicatorScheme
from src.django_space.indicators.config import config
from src.django_space.indicators.models import Indicator, Log


class LogCreate(BaseModel):
    """Схема для создания записи лога"""

    val: float = Body(ge=0, title="Значение показателя")
    date: Annotated[datetime, Field(title="Период регистрации")] = False


@dataclass
class LogGet:
    indicator_attr = Annotated[
        str,
        Query(
            description="Уникальный идентификатор показателя, ID или name",
            max_length=config.IND_NAME_MAX_LENGTH,
        ),
    ]
    date_start = Annotated[datetime, Query(description="Начало периода")]
    date_end = Annotated[datetime, Query(description="Конец периода")]


class LogGetPy(BaseModel):
    indicator_id: str | None
    date_start: datetime | None
    date_end: datetime | None


class IndicatorScheme2(ModelSchema):
    """Схема для списка изображений."""

    class Config:
        model = Indicator
        # exclude = ["id", "name"]
        include = ["id", "unit", "name"]
        # include = ["id", "unit", "name"]


class LogScheme(BaseModel):
    # class LogScheme(ModelSchema):
    """Общая схема лога"""

    # indicator_set: list[IndicatorScheme2] = []
    # indicator: IndicatorScheme2
    val: Any
    date: Any
    indicator_id: IndicatorScheme2
    # indicator_id: Any

    class Config:
        orm_mode = True
        # model = Log
        # include = ["id", "val", "date", "indicator", "indicator_set"]
        # include = ["id", "val", "date", "indicator_set"]
        # include = ["id", "val", "date" ]

    @classmethod
    async def from_orms(cls, v):
        """reload from_orm method"""
        return await sync_to_async(cls.from_orm)(v)
