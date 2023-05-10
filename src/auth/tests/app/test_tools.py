from datetime import datetime, timedelta

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from logrich.logger_ import errlog, log  # noqa
from logrich.logger_assets import console  # noqa
from pydantic import EmailStr

from src.auth.config import config
from src.django_space.indicators.config import config as indicator_config
from src.django_space.indicators.models import Indicator, Log


async def create_user(
    username: str = config.FIRST_USER_USERNAME,
    email: EmailStr = config.FIRST_USER_EMAIL,
    password: str = config.FIRST_USER_PASSWORD,
    is_superuser: bool = False,
    is_staff: bool = False,
    is_active: bool = True,
    first_name: str = "",
    last_name: str = "",
) -> User:
    """create user"""
    user_model = get_user_model()
    user = await sync_to_async(user_model.objects.create_user)(
        username=username,
        email=email,
        password=password,
        is_superuser=is_superuser,
        is_staff=is_staff,
        is_active=is_active,
        first_name=first_name,
        last_name=last_name,
    )
    return user


async def create_indicator(
    name: str = indicator_config.TEST_IND_NAME,
    unit: str = indicator_config.TEST_IND_UNIT,
    desc: str = indicator_config.TEST_IND_DESC,
) -> Indicator:
    """create indicator"""
    indicator_model = Indicator
    ind = await sync_to_async(indicator_model.objects.get_or_create)(
        name=name,
        unit=unit,
        desc=desc,
    )
    return ind


async def create_log(
    val: float = indicator_config.TEST_LOG_VAL,
    indicator: str | int = 1,
    uid: int = 1,
    date: datetime | str = datetime.now(),
) -> Log:
    """create log"""
    if isinstance(indicator, str) and indicator.isdigit():
        indicator = await Indicator.objects.filter(pk=indicator).afirst()
    else:
        indicator = await Indicator.objects.filter(name=indicator).afirst()
    user = await User.objects.filter(pk=uid).afirst()
    log_model = Log
    log_ = await sync_to_async(log_model.objects.get_or_create)(indicator=indicator, val=val, user=user, date=date)
    return log_
