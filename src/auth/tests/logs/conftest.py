from typing import Callable

import pytest
from faker import Faker
from fastapi import FastAPI, HTTPException
from logrich.logger_ import log  # noqa

from src.auth.tests.app.test_tools import create_indicator, create_log
from src.django_space.indicators.config import config
from src.django_space.indicators.models import Indicator, Log


@pytest.fixture
async def add_test_indicator(app: FastAPI) -> Indicator | HTTPException:
    """Добавляет тестовое объявление в БД"""
    ad = await create_indicator()
    return ad


@pytest.fixture
async def add_test_image(app: FastAPI, add_test_indicator: Callable) -> Log | HTTPException:
    """Добавляет тестовое изображение в БД"""
    image = await create_log()
    return image


async def insert_fake_indicators(amount_indicators: int) -> None:
    """fill db with fake data - Indicators"""
    fake = Faker("ru_RU")
    for i in range(amount_indicators):
        await create_indicator(
            price=fake.pydecimal(left_digits=7, right_digits=2, positive=True),
            name=fake.texts(nb_texts=1, max_nb_chars=100)[0],
            desc=fake.texts(nb_texts=1, max_nb_chars=500)[0],
        )


async def insert_fake_logs(amount_indicators: int) -> None:
    """fill db with fake data - Logs"""
    fake = Faker()
    for i in range(1, amount_indicators + 2):
        for image in range(config.IND_NAME_MAX_LENGTH):
            path = fake.file_path(depth=3, category="image")
            is_main = False
            if image == 1:
                is_main = True
            await create_log(path=path, ads_id=i, is_main=is_main)
