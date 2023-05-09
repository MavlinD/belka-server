from functools import lru_cache

from dotenv import load_dotenv
from logrich.logger_ import log  # noqa
from pydantic import BaseSettings

load_dotenv()


@lru_cache()
class Settings(BaseSettings):
    """
    Ad config settings
    """

    OPEN_API_TAG_IND: str = "CRUD for Indicator"
    OPEN_API_TAG_LOG: str = "CRUD for Log"

    # ограничения на имя показателя
    IND_NAME_MIN_LENGTH: int = 3
    IND_NAME_MAX_LENGTH: int = 200

    # ограничения на единицы измерения показателя
    IND_UNIT_MIN_LENGTH: int = 1
    IND_UNIT_MAX_LENGTH: int = 30

    # ограничения на описание показателя
    IND_DESC_MIN_LENGTH: int = 3
    IND_DESC_MAX_LENGTH: int = 1000

    # тестовая запись лога
    TEST_IND_NAME: str = "Адамантий"
    TEST_IND_UNIT: str = "мг/см.куб"
    TEST_IND_DESC: str = "Подозрительный элемент"
    TEST_LOG_VAL: float = 100.25

    class Config:
        env_file_encoding = "utf-8"


config = Settings()
