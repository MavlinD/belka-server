from __future__ import annotations

from typing import Annotated

from asgiref.sync import sync_to_async
from djantic import ModelSchema
from fastapi import Body
from logrich.logger_ import log  # noqa
from pydantic import BaseModel, Field
from pydantic.types import Decimal

from src.django_space.indicators.config import config
from src.django_space.indicators.models import Indicator, Log

constrain_ad_name = Body(
    title="Имя объявления",
    # min_length=config.AD_NAME_MIN_LENGTH,
    # max_length=config.AD_NAME_MAX_LENGTH,
)

constrain_ad_desc = Body(
    title="Описание объявления",
    # min_length=config.AD_DESC_MIN_LENGTH,
    # max_length=config.AD_DESC_MAX_LENGTH,
)

constrain_price = Field(title="Цена", max_digits=11, decimal_places=2)
# constrain_price = Field(title="Цена", max_digits=config.AD_MAX_PRICE_DIGITS, decimal_places=2)


class IndicatorCreate(BaseModel):
    """Схема для создания показателя"""

    name: str = constrain_ad_name
    desc: str = constrain_ad_desc
    price: Annotated[Decimal, constrain_price]


class IndicatorUpdate(BaseModel):
    """Схема для обновления показателя"""

    name: Annotated[str | None, constrain_ad_name] = None
    desc: Annotated[str | None, constrain_ad_desc] = None
    price: Annotated[Decimal | None, constrain_price] = None


class IndicatorAttr(BaseModel):
    """Схема для валидации параметров внутри приложения"""

    attr: str | int = constrain_ad_name


class LogSchemeWithoutIndicators(ModelSchema):
    """Схема для списка логов."""

    class Config:
        model = Log
        include = ["id", "path", "is_main"]


class IndicatorScheme(ModelSchema):
    """Общая схема показателя"""

    image_set: list[LogSchemeWithoutIndicators] = []

    class Config:
        model = Indicator
        include = ["id", "name", "price", "desc", "image_set"]

    @classmethod
    async def from_orms(cls, v):
        """reload from_orm method"""
        return await sync_to_async(cls.from_orm)(v)
