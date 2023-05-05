from fastapi import Depends, status
from fastapi_pagination import paginate as paginate_
from fastapi_pagination.bases import AbstractPage
from logrich.logger_ import log  # noqa
from pydantic import BaseModel

from src.auth.assets import APIRouter
from src.auth.schemas.indicators import IndicatorCreate, IndicatorScheme, IndicatorUpdate
from src.auth.schemas.scheme_tools import get_qset
from src.auth.users.indicator_manager import IndicatorManager
from src.auth.users.dependencies import get_current_active_user
from src.auth.users.init import get_indicator_manager
from src.django_space.indicators.models import Indicator
from src.django_space.django_space.adapters import Page, retrieve_ad
from src.django_space.django_space.routers.jwt_obtain import unauthorized_responses

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
async def create_ad(
    ad: IndicatorCreate,
    ad_manager: IndicatorManager = Depends(get_indicator_manager),
) -> IndicatorScheme:
    """Создать или вернуть объявление"""
    resp = await ad_manager.create(ad_create=ad)
    return resp


@router.patch(
    "/{ad_attr:str}",
    response_model=IndicatorScheme,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
    responses={
        **unauthorized_responses,
    },
)
async def update_ad(
    payload: IndicatorUpdate,
    ad: Indicator = Depends(retrieve_ad),
    ad_manager: IndicatorManager = Depends(get_indicator_manager),
) -> IndicatorScheme:
    """Обновить объявление по имени или id"""
    ad = await ad_manager.update(ad=ad, payload=payload.dict(exclude_unset=True, exclude_none=True))
    resp = await IndicatorScheme.from_orms(ad)
    return resp


@router.get(
    "/list",
    response_model=Page[IndicatorScheme],
    status_code=status.HTTP_200_OK,
    responses={
        **unauthorized_responses,
    },
)
async def read_ads(
    ad_manager: IndicatorManager = Depends(get_indicator_manager),
) -> AbstractPage[BaseModel]:
    """Получить список объявлений"""
    indicators = await ad_manager.get_list_ads()
    resp = await get_qset(qset=indicators, model=IndicatorScheme)
    return paginate_(list(resp))


@router.get(
    "/{ad_attr:str}",
    response_model=IndicatorScheme,
    status_code=status.HTTP_200_OK,
    responses={
        **unauthorized_responses,
    },
)
async def read_ad(
    ad: Indicator = Depends(retrieve_ad),
) -> IndicatorScheme:
    """Получить объявление по имени или id"""
    resp = await IndicatorScheme.from_orms(ad)
    return resp


@router.delete(
    "/{ad_attr:str}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
    responses={
        **unauthorized_responses,
        status.HTTP_404_NOT_FOUND: {
            "description": "Объявление не найдено.",
        },
    },
)
async def delete_ad(
    ad: Indicator = Depends(retrieve_ad),
    ad_manager: IndicatorManager = Depends(get_indicator_manager),
) -> None:
    """Удалить объявление по id"""
    await ad_manager.delete(ad)
