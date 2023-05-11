from typing import Type

from django.db.models import QuerySet
from logrich.logger_ import log  # noqa
from pydantic import BaseModel

from src.auth.schemas.log import LogScheme


async def get_qset(qset: QuerySet, model: Type[BaseModel]) -> list[BaseModel | LogScheme]:
    """get data from QuerySet with DB model"""
    # https://blog.etianen.com/blog/2013/06/08/django-querysets/
    resp = []
    if qset.aexists():
        async for item in qset.aiterator():
            if hasattr(model, "from_orms"):
                entity = await model.from_orms(item)
                resp.append(entity)
    return resp


async def get_qset_base(qset: QuerySet) -> list[BaseModel | LogScheme]:
    """get data from QuerySet"""
    resp = []
    if qset.aexists():
        async for item in qset.aiterator():
            resp.append(item)
    return resp
