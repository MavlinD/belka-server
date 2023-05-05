from __future__ import annotations

from typing import Annotated

from asgiref.sync import sync_to_async
from djantic import ModelSchema
from fastapi import Body
from logrich.logger_ import log  # noqa
from pydantic import BaseModel, Field

from src.django_space.indicators.models import Log


class LogCreate(BaseModel):
    """Схема для создания записи лога"""

    path: str = Body(max_length=256)
    is_main: Annotated[bool, Field(title="Признак главного изображения")] = False


class LogScheme(ModelSchema):
    """Общая схема лога"""

    class Config:
        model = Log

    @classmethod
    async def from_orms(cls, v):
        """reload from_orm method"""
        return await sync_to_async(cls.from_orm)(v)
