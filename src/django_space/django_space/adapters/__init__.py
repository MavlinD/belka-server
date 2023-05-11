from fastapi import Depends, Path
from fastapi_pagination import Page
from logrich.logger_ import log  # noqa
from pydantic import Field

from src.auth.schemas.indicators import IndicatorAttr, IndicatorCreate
from src.auth.users.indicator_manager import IndicatorManager
from src.auth.users.init import get_indicator_manager
from src.django_space.indicators.models import Indicator


async def retrieve_indicator(
    indicator_attr: str = Path(
        description="ID или name показателя",
    ),
    indicators_manager: IndicatorManager = Depends(get_indicator_manager),
) -> Indicator:
    """получить показатель"""
    attr = IndicatorAttr(attr=indicator_attr)
    indicator: Indicator = await indicators_manager.get_one_by_uniq_attr(indicator_attr=attr)
    return indicator


async def check_cant_exist_indicator(
    indicator: IndicatorCreate,
    indicator_manager: IndicatorManager = Depends(get_indicator_manager),
) -> None:
    """Проверяет отсутствие индикатора"""
    attr = IndicatorAttr(attr=indicator.name)
    await indicator_manager.check_one_by_uniq_attr(indicator_attr=attr)


# параметры пагинации по умолчанию
Page = Page.with_custom_options(
    size=Field(10, ge=1, le=15),
)
