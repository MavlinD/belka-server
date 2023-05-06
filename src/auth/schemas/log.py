from __future__ import annotations

from datetime import datetime
from typing import Annotated

from asgiref.sync import sync_to_async
from djantic import ModelSchema
from fastapi import Body
from logrich.logger_ import log  # noqa
from pydantic import BaseModel, Field

from src.django_space.indicators.models import Log


class LogCreate(BaseModel):
    """Схема для создания записи лога"""

    val: float = Body(ge=0, title="Значение показателя")
    date: Annotated[datetime, Field(title="Период регистрации")] = False
    # date: Annotated[bool, Field(title="Признак главного изображения")] = False


class LogScheme(ModelSchema):
    """Общая схема лога"""

    class Config:
        model = Log

    @classmethod
    async def from_orms(cls, v):
        """reload from_orm method"""
        return await sync_to_async(cls.from_orm)(v)
