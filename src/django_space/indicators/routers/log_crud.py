from django.contrib.auth.models import User
from fastapi import Depends, Query, status
from fastapi_pagination import paginate as paginate_
from fastapi_pagination.bases import AbstractPage
from logrich.logger_ import log  # noqa
from pydantic import BaseModel

from src.auth.assets import APIRouter
from src.auth.schemas.log import LogCreate, LogGet, LogGetPy, LogScheme
from src.auth.schemas.scheme_tools import get_qset
from src.auth.users.dependencies import get_current_active_user
from src.auth.users.init import get_log_manager
from src.auth.users.log_manager import LogManager
from src.django_space.django_space.adapters import (
    LogLimitChecker,
    Page,
    retrieve_indicator,
    retrieve_log,
)
from src.django_space.django_space.routers.jwt_obtain import unauthorized_responses
from src.django_space.indicators.config import config
from src.django_space.indicators.models import Indicator, Log

router = APIRouter()


@router.put(
    "/{indicator_attr:str}",
    response_model=LogScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        # Depends(LogLimitChecker()),
    ],
    responses={
        **unauthorized_responses,
    },
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
    response_model=Page[LogScheme],
    status_code=status.HTTP_200_OK,
    responses={
        **unauthorized_responses,
    },
)
async def read_logs(
    indicator_attr: LogGet.indicator_attr = None,
    date_start: LogGet.date_start = None,
    date_end: LogGet.date_end = None,
    # payload: LogGet,
    log_manager: LogManager = Depends(get_log_manager),
) -> AbstractPage[BaseModel]:
    """Получить список записей лога"""
    # log.debug(payload)
    # log.debug(indicator_attr)
    # log.debug(date_end)
    # payload = {}
    # resp = ""
    # log.debug(payload)
    # payload={
    #     'indicator_id': indicator_attr,
    #     'date_start': date_start,
    #     'date_end': date_end
    # }

    payload = LogGetPy(indicator_id=indicator_attr, date_start=date_start, date_end=date_end)
    logs = await log_manager.get_list_log(payload=payload)
    resp = await get_qset(qset=logs, model=LogScheme)
    log.debug(resp)
    for ls in resp:
        log.trace(ls.val)
    return paginate_(list(resp))


# @router.patch(
#     "/{log_attr:str}",
#     response_model=LogScheme,
#     status_code=status.HTTP_200_OK,
#     dependencies=[Depends(get_current_active_user)],
#     responses={
#         **unauthorized_responses,
#     },
# )
# async def update_log(
#     # payload: LogCreate,
#     # log: Log = Depends(retrieve_log),
#     # log_manager: LogManager = Depends(get_log_manager),
# ) -> LogScheme:
#     """Обновить изображение по имени или id."""
#     ...
#     # log = await log_manager.update(log=log, payload=payload.dict(exclude_unset=True, exclude_none=True))
#     # resp = await LogScheme.from_orms(log)
#     # return resp
#
#
# @router.delete(
#     "/{log_attr:str}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     dependencies=[Depends(get_current_active_user)],
#     responses={
#         **unauthorized_responses,
#         status.HTTP_404_NOT_FOUND: {
#             "description": "The log does not exist.",
#         },
#     },
# )
# async def delete_log(
#     # log: Log = Depends(retrieve_log),
#     log_manager: LogManager = Depends(get_log_manager),
# ) -> None:
#     """Удалить изображение по id."""
#     await log_manager.delete(log)
