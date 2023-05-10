from django.contrib.auth.models import User
from fastapi import Depends, status
from fastapi_pagination import paginate as paginate_
from fastapi_pagination.bases import AbstractPage
from logrich.logger_ import log  # noqa

from src.auth.assets import APIRouter
from src.auth.schemas.log import (
    LogAnnotate,
    LogCreate,
    LogGetDB,
    LogGetQuery,
    LogScheme,
)
from src.auth.users.dependencies import get_current_active_user
from src.auth.users.init import get_log_manager
from src.auth.users.log_manager import LogManager
from src.django_space.django_space.adapters import Page, retrieve_indicator
from src.django_space.django_space.routers.jwt_obtain import unauthorized_responses
from src.django_space.indicators.models import Indicator

router = APIRouter()


@router.put(
    "/{indicator_attr:str}",
    response_model=LogScheme,
    status_code=status.HTTP_201_CREATED,
    responses={**unauthorized_responses},
)
async def create_log(
    payload: LogCreate,
    user: User = Depends(get_current_active_user),
    indicator: Indicator = Depends(retrieve_indicator),
    log_manager: LogManager = Depends(get_log_manager),
) -> LogScheme:
    """Создать запись лога"""
    log_ = await log_manager.create(payload=payload, indicator=indicator, user=user)
    resp = await LogScheme.from_orms(log_)
    return resp


@router.get(
    "/list",
    response_model=Page[LogAnnotate],
    status_code=status.HTTP_200_OK,
    responses={**unauthorized_responses},
)
async def read_logs(
    indicator_attr: LogGetQuery.indicator_attr = None,
    date__gte: LogGetQuery.date__gte = None,
    date__lte: LogGetQuery.date__lte = None,
    log_manager: LogManager = Depends(get_log_manager),
) -> AbstractPage[LogAnnotate]:
    """Получить список записей лога"""
    payload = LogGetDB(indicator_id=indicator_attr, date__gte=date__gte, date__lte=date__lte)
    logs = await log_manager.get_list_log(payload=payload)
    return paginate_(list(logs))
