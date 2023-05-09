import json
from datetime import datetime
from typing import Callable

import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.conftest import Routs
from src.auth.tests.app.test_tools import create_indicator
from src.django_space.indicators.config import config as indicator_config

skip = False
# skip = True
reason = "Temporary off"
pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_from_arr(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест создания лога из множества записей"""
    # return
    resp = await client.put(
        routes.request_create_log(indicator_attr=1),
        json={
            "val": 50.23,
            # "date": "01.01.2022",
            "date": "2023-5-06T07:40",
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание записи логов", o=data)
    assert resp.status_code == 201


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_from_arr_with_unexist_indicator(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест создания лога с несуществующим показателем"""
    # return
    resp = await client.put(
        routes.request_create_log(indicator_attr="fake-ind"),
        json={
            "val": 50.23,
            "date": "2023-5-06T07:40",
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание записи логов с несущ. показателем", o=data)
    assert resp.status_code == 404


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_with_invalid_datatime(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест НЕ создания лога с невалидным значением даты-воемени"""
    resp = await client.put(
        routes.request_create_log(indicator_attr=1),
        json={
            "val": 50.232435,
            "date": "2023-15-06T07:40",
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание невалидной записи лога", o=data)
    assert resp.status_code == 422


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_with_invalid_val(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест НЕ создания лога с невалидным значением показателя"""
    resp = await client.put(
        routes.request_create_log(indicator_attr=1),
        json={
            "val": "fake val",
            "date": "2023-5-06T07:40",
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание невалидной записи лога", o=data)
    assert resp.status_code == 422


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_duplicate_data(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест НЕ создания дубля лога"""
    dt_val = datetime.now().strftime("%Y-%m-%dT%H:%M")
    resp = await client.put(
        routes.request_create_log(indicator_attr=indicator_config.TEST_IND_NAME),
        json={
            "val": indicator_config.TEST_LOG_VAL,
            "date": dt_val,
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание дубликата записи логов", o=data)
    resp = await client.put(
        routes.request_create_log(indicator_attr=indicator_config.TEST_IND_NAME),
        json={
            "val": indicator_config.TEST_LOG_VAL + 100,
            "date": dt_val,
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание или обновление существующей записи логов", o=data)
    assert resp.status_code == 201
    assert data.get("val") == indicator_config.TEST_LOG_VAL + 100


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест создания лога"""
    # return
    resp = await client.put(
        routes.request_create_log(indicator_attr=1),
        json={"val": 50},
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание записи лога", o=data)
    assert resp.status_code == 201
    # уставновка произвольной даты-времени
    resp = await client.put(
        routes.request_create_log(indicator_attr=1),
        json={
            "val": 50.23,
            "date": "2022-5-06T07:40",  # ISO format
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание лога с произвольной датой в виде строки", o=data)
    assert resp.status_code == 201

    # уставновка произвольной даты-времени
    resp = await client.put(
        routes.request_create_log(indicator_attr=1),
        json={
            "val": 50.23,
            # "date": "01.01.2022",
            "date": "10 октября 2020",
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание лога с произвольной датой в виде строки", o=data)
    assert resp.status_code == 422

    # установка произвольной даты-времени
    dt_val = datetime.now().strftime("%Y-%m-%dT%H:%M")
    resp = await client.put(
        routes.request_create_log(indicator_attr=1),
        json={
            "val": 50.23,
            "date": dt_val,
        },
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug(f"ответ на создание лога с произвольной датой в виде объекта даты-времени: {dt_val}", o=data)
    assert resp.status_code == 201
