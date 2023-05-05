from fastapi import Depends, status
from logrich.logger_ import log  # noqa

from src.auth.assets import APIRouter
from src.auth.schemas.log import LogCreate, LogScheme
from src.auth.users.dependencies import get_current_active_user
from src.auth.users.log_manager import LogManager
from src.auth.users.init import get_log_manager
from src.django_space.indicators.config import config
from src.django_space.indicators.models import Indicator, Log
from src.django_space.django_space.adapters import (
    LogLimitChecker,
    retrieve_ad,
    retrieve_log,
)
from src.django_space.django_space.routers.jwt_obtain import unauthorized_responses

router = APIRouter()


@router.put(
    "/{ad_attr:str}",
    response_model=LogScheme,
    description=f"К объявлению можно прикрепить до **{config.IND_NAME_MAX_LENGTH}** изображений включительно.<br>"
    f"И назначить до **{config.IND_NAME_MAX_LENGTH}** изображений(я) главными.",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(get_current_active_user),
        Depends(LogLimitChecker()),
    ],
    responses={
        **unauthorized_responses,
    },
)
async def create_log(
    payload: LogCreate,
    ad: Indicator = Depends(retrieve_ad),
    log_manager: LogManager = Depends(get_log_manager),
) -> LogScheme:
    """Создать (прикрепить) изображение."""
    resp = await log_manager.create(payload=payload.dict(exclude_unset=True, exclude_none=True), ad=ad)
    return resp


@router.patch(
    "/{log_attr:str}",
    response_model=LogScheme,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
    responses={
        **unauthorized_responses,
    },
)
async def update_log(
    payload: LogCreate,
    log: Log = Depends(retrieve_log),
    log_manager: LogManager = Depends(get_log_manager),
) -> LogScheme:
    """Обновить изображение по имени или id."""
    log = await log_manager.update(log=log, payload=payload.dict(exclude_unset=True, exclude_none=True))
    resp = await LogScheme.from_orms(log)
    return resp


@router.delete(
    "/{log_attr:str}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
    responses={
        **unauthorized_responses,
        status.HTTP_404_NOT_FOUND: {
            "description": "The log does not exist.",
        },
    },
)
async def delete_log(
    log: Log = Depends(retrieve_log),
    log_manager: LogManager = Depends(get_log_manager),
) -> None:
    """Удалить изображение по id."""
    await log_manager.delete(log)
