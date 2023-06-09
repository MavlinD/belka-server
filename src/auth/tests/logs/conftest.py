from datetime import datetime, timedelta
from typing import Callable

import pytest
from faker import Faker
from fastapi import FastAPI, HTTPException
from logrich.logger_ import log  # noqa

from src.auth.tests.app.test_tools import create_indicator, create_log
from src.django_space.indicators.models import Indicator, Log


@pytest.fixture
async def add_test_indicator(app: FastAPI) -> Indicator | HTTPException:
    """Добавляет тестовый индикатор в БД"""
    ind = await create_indicator()
    return ind


@pytest.fixture
async def add_test_log(app: FastAPI, add_test_indicator: Callable) -> Log | HTTPException:
    """Добавляет тестовую запись в БД"""
    log_ = await create_log()
    return log_


async def insert_fake_indicators(amount_indicators: int) -> None:
    """fill db with fake data - Indicators"""
    fake = Faker("ru_RU")
    for i in range(amount_indicators):
        await create_indicator(
            name=fake.texts(nb_texts=1, max_nb_chars=20)[0],
            # unit=fake.pystr(min_chars=2, max_chars=5),
            unit=fake.pystr_format(
                string_format="?##/###{{random_letter}}",
                letters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
            ),
            desc=fake.texts(nb_texts=1, max_nb_chars=200)[0],
        )


async def insert_fake_logs(
    amount_indicators: int, amount_logs: int, date: datetime = datetime.now(), tdelta: timedelta = timedelta(days=3)
) -> None:
    """fill db with fake data - Logs"""
    fake = Faker()
    for i in range(1, amount_logs):
        val = fake.pyfloat(right_digits=3, min_value=0, max_value=1000)
        indicator_id = fake.pyint(min_value=1, max_value=amount_indicators)
        # log.trace(indicator_id)
        uid = fake.pyint(min_value=1, max_value=2)
        date += tdelta
        await create_log(val=val, indicator=indicator_id, uid=uid, date=date)
