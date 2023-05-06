from typing import Any

from fastapi import Depends, Path, Request
from fastapi_pagination import Page
from logrich.logger_ import log  # noqa
from pydantic import Field

from src.auth.schemas.indicators import IndicatorAttr
from src.auth.schemas.log import LogScheme
from src.auth.schemas.scheme_tools import get_qset
from src.auth.users.indicator_manager import IndicatorManager
from src.auth.users.init import get_indicator_manager, get_log_manager
from src.auth.users.log_manager import LogManager
from src.django_space.indicators.config import config as indicator_config

# from src.django_space.indicators.exception import OverLimitAmountLogs, OverLimitMainLogs
from src.django_space.indicators.models import Indicator, Log


async def retrieve_indicator(
    indicator_attr: int = Path(
        description="ID или name показателя",
    ),
    indicators_manager: IndicatorManager = Depends(get_indicator_manager),
) -> Indicator:
    """получить показатель"""
    attr = IndicatorAttr(attr=indicator_attr)
    indicator: Indicator = await indicators_manager.get_one_by_uniq_attr(indicator_attr=attr)
    return indicator


class LogLimitChecker:
    def __init__(
        self,
        image_max_amount: int = indicator_config.IND_NAME_MAX_LENGTH,
        image_main_max_amount: int = indicator_config.IND_NAME_MAX_LENGTH,
    ) -> None:
        """
        проверить ограничение:
        - на максимальное кол-во прикрепленных изображений
        - на максимальное кол-во главных изображений
        """
        self.image_max_amount = image_max_amount
        self.image_main_max_amount = image_main_max_amount

    async def __call__(self, request: Request, indicator: Indicator = Depends(retrieve_indicator)) -> Any:
        ...
        # amount_images = await get_qset(qset=indicator.image_set, model=LogScheme)
        # all_images = list(amount_images)
        # is_main = [image for image in all_images if image.is_main]
        # req = await request.json()
        # if req.get("is_main") and len(is_main) >= self.image_main_max_amount:
        #     raise OverLimitMainLogs(indicator=indicator)
        # if len(all_images) >= self.image_max_amount:
        #     raise OverLimitAmountLogs(indicator=indicator)


async def retrieve_log(
    image_attr: int = Path(
        description="ID изображения",
    ),
    images_manager: LogManager = Depends(get_log_manager),
) -> Log:
    """получить изображение"""
    ...
    # log: Log = await images_manager.get_one_by_uniq_attr(image_id=image_attr)
    # return log


# параметры пагинации по умолчанию
Page = Page.with_custom_options(
    size=Field(10, ge=1, le=15),
)
