from asgiref.sync import sync_to_async
from fastapi import Depends, status
from fastapi_pagination import paginate as paginate_
from fastapi_pagination.bases import AbstractPage
from logrich.logger_ import log  # noqa
from pydantic import BaseModel

from src.auth.assets import APIRouter
from src.auth.schemas.indicators import (
    IndicatorCreate,
    IndicatorScheme,
    IndicatorUpdate,
)
from src.auth.schemas.scheme_tools import get_qset
from src.auth.users.dependencies import get_current_active_user
from src.auth.users.indicator_manager import IndicatorManager
from src.auth.users.init import get_indicator_manager
from src.django_space.django_space.adapters import Page, retrieve_indicator
from src.django_space.django_space.routers.jwt_obtain import unauthorized_responses
from src.django_space.indicators.models import Indicator

router = APIRouter()


@router.put(
    "/create",
    response_model=IndicatorScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
    responses={
        **unauthorized_responses,
    },
)
async def create_indicator(
    indicator: IndicatorCreate,
    indicator_manager: IndicatorManager = Depends(get_indicator_manager),
) -> IndicatorScheme:
    """Создать или вернуть показатель"""
    ind = await indicator_manager.create(payload=indicator)
    resp = await IndicatorScheme.from_orms(ind)
    return resp


@router.patch(
    "/{indicator_attr:str}",
    response_model=IndicatorScheme,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
    responses={
        **unauthorized_responses,
    },
)
async def update_indicator(
    payload: IndicatorUpdate,
    ind: Indicator = Depends(retrieve_indicator),
    indicator_manager: IndicatorManager = Depends(get_indicator_manager),
) -> IndicatorScheme:
    """Обновить показатель по имени или id"""
    ind = await indicator_manager.update(ind=ind, payload=payload)
    resp = await IndicatorScheme.from_orms(ind)
    return resp


@router.get(
    "/list",
    response_model=Page[IndicatorScheme],
    status_code=status.HTTP_200_OK,
    responses={
        **unauthorized_responses,
    },
)
async def read_indicators(
    indicator_manager: IndicatorManager = Depends(get_indicator_manager),
) -> AbstractPage[BaseModel]:
    """Получить список показателей"""
    indicators = await indicator_manager.get_list_indicators()
    resp = await get_qset(qset=indicators, model=IndicatorScheme)
    return paginate_(list(resp))


@router.get(
    "/{indicator_attr:str}",
    response_model=IndicatorScheme,
    status_code=status.HTTP_200_OK,
    responses={
        **unauthorized_responses,
    },
)
async def read_indicator(
    ind: Indicator = Depends(retrieve_indicator),
) -> IndicatorScheme:
    """Получить показатель по имени или id"""
    resp = await IndicatorScheme.from_orms(ind)
    return resp


@router.delete(
    "/{indicator_attr:str}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
    responses={
        **unauthorized_responses,
        status.HTTP_404_NOT_FOUND: {
            "description": "Объявление не найдено.",
        },
    },
)
async def delete_indicator(
    ad: Indicator = Depends(retrieve_indicator),
    indicator_manager: IndicatorManager = Depends(get_indicator_manager),
) -> None:
    """Удалить показатель по имени или id"""
    await indicator_manager.delete(ad)
