from functools import lru_cache

from dotenv import load_dotenv
from logrich.logger_ import log  # noqa
from pydantic import BaseSettings, Field
from pydantic.schema import Decimal

load_dotenv()


@lru_cache()
class Settings(BaseSettings):
    """
    Ad config settings
    """

    # ограничения на имя показателя
    IND_NAME_MIN_LENGTH: int = 3
    IND_NAME_MAX_LENGTH: int = 200

    # ограничения на единицы измерения показателя
    IND_UNIT_MIN_LENGTH: int = 3
    IND_UNIT_MAX_LENGTH: int = 1000

    # ограничения на описание показателя
    IND_DESC_MIN_LENGTH: int = 3
    IND_DESC_MAX_LENGTH: int = 1000

    # ограничения на стоимость объявления
    IND_MAX_PRICE_DIGITS: int = 9

    # тестовое объявление
    TEST_IND_NAME: str = "Продам славянский шкаф"
    TEST_IND_PRICE: Decimal | None = Field(15730.45, decimal_places=2)
    TEST_IND_DESC: str = "Прекрасный шкаф светлого дерева"

    # тестовое изображение
    TEST_IMAGE_PATH: str = "test-image.png"

    class Config:
        env_file_encoding = "utf-8"


config = Settings()
