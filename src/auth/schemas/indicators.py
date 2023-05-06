from __future__ import annotations

from typing import Annotated

from asgiref.sync import sync_to_async
from djantic import ModelSchema
from fastapi import Body
from logrich.logger_ import log  # noqa
from pydantic import BaseModel

from src.django_space.indicators.config import config
from src.django_space.indicators.models import Indicator

constrain_indicator_name = Body(
    title="Имя показателя",
    min_length=config.IND_NAME_MIN_LENGTH,
    max_length=config.IND_NAME_MAX_LENGTH,
)

constrain_indicator_unit = Body(
    title="Ед. измерения показателя",
    min_length=config.IND_UNIT_MIN_LENGTH,
    max_length=config.IND_UNIT_MAX_LENGTH,
)

constrain_indicator_desc = Body(
    title="Описание показателя",
    min_length=config.IND_DESC_MIN_LENGTH,
    max_length=config.IND_DESC_MAX_LENGTH,
)


class IndicatorCreate(BaseModel):
    """Схема для создания показателя"""

    name: str = constrain_indicator_name
    unit: str = constrain_indicator_unit
    desc: str = constrain_indicator_desc


class IndicatorUpdate(BaseModel):
    """Схема для обновления показателя"""

    name: Annotated[str | None, constrain_indicator_name] = None
    unit: Annotated[str | None, constrain_indicator_unit] = None
    desc: Annotated[str | None, constrain_indicator_desc] = None


class IndicatorAttr(BaseModel):
    """Схема для валидации параметров внутри приложения"""

    attr: str | int = constrain_indicator_name


class IndicatorScheme(ModelSchema):
    """Общая схема показателя"""

    class Config:
        model = Indicator
        include = ["id", "name", "unit", "desc"]

    @classmethod
    async def from_orms(cls, v):
        """reload from_orm method"""
        return await sync_to_async(cls.from_orm)(v)
