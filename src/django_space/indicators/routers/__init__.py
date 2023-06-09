from fastapi import FastAPI

from src.auth.config import config
from src.django_space.indicators.config import config as indicators_config
from src.django_space.indicators.routers.indicator_crud import router as ad_crud
from src.django_space.indicators.routers.log_crud import router as image_crud

prefix = config.API_PATH_PREFIX
__version__ = config.API_VERSION


def init_router(app: FastAPI) -> None:
    """order is important !!!"""
    app.include_router(ad_crud, prefix=f"{prefix}{__version__}/indicator", tags=[indicators_config.OPEN_API_TAG_IND])
    app.include_router(image_crud, prefix=f"{prefix}{__version__}/log", tags=[indicators_config.OPEN_API_TAG_LOG])
