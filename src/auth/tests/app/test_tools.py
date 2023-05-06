import decimal

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


async def create_log() -> Log:
    # async def create_log(path: str = indicator_config.TEST_IMAGE_PATH, ads_id: int = 1, is_main: bool = False)
    # -> Log:
    """create ind"""
    ...
    # indicator = await Indicator.objects.filter(pk=ads_id).afirst()
    # image_model = Log
    # image = await sync_to_async(image_model.objects.get_or_create)(path=path, ads_id=indicator, is_main=is_main)
    # return image
