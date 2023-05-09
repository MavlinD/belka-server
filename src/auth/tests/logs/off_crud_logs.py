import json
from datetime import datetime
from typing import Callable

import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.conftest import Routs
from src.auth.tests.app.test_tools import create_indicator
from src.django_space.indicators.config import config as indicator_config

# skip = False
skip = True
reason = "Temporary off"
pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_from_arr(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест создания лога из множества записей"""
    # return
    await create_indicator()
    data = [
        [indicator_config.TEST_IND_NAME, "100.23", "2023-5-06T07:40"],
        [indicator_config.TEST_IND_NAME, "30.19", "2023-5-16T07:40"],
        [indicator_config.TEST_IND_NAME, "760.75", "2023-5-23T12:10"],
        # ["с", "760.75", "2023-5-23T12:10"],
        # ["кальций", "42342.17", "ascac"],
        # ["кальций", "fake", "2023-5-06T07:40"],
        # ["r/sm", "760.75"],
    ]
    payload = {"data": data}
    resp = await client.put(
        routes.create_log_from_list,
        json=payload,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание записи логов", o=data)
    assert resp.status_code == 201
    # assert len(data.get("items")) == 3
    # resp = await client.get(routes.read_logs, params={})
    # log.debug(resp)
    # data = resp.json()
    # log.debug("логи с пагинацией", o=data)
    # assert resp.status_code == 200


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_from_arr_with_unexist_indicator(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers
) -> None:
    """Тест создания лога из множества записей с несуществующим показателем"""
    # return
    await create_indicator()
    data = [
        ["fake ind", "100.23", "2023-5-06T07:40"],
        # [indicator_config.TEST_IND_NAME, "30.19", "2023-5-16T07:40"],
        # [indicator_config.TEST_IND_NAME, "760.75", "2023-5-23T12:10"],
        # ["с", "760.75", "2023-5-23T12:10"],
        # ["кальций", "42342.17", "ascac"],
        # ["кальций", "fake", "2023-5-06T07:40"],
        # ["r/sm", "760.75"],
    ]
    payload = {"data": data}
    resp = await client.put(
        routes.create_log_from_list,
        json=payload,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание записи логов с несущ. показателем", o=data)
    assert resp.status_code == 404


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_from_arr_with_invalid_data(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест НЕ создания лога из множества записей, среди которых есть невалидные значения"""
    # return
    await create_indicator()
    data = [
        [indicator_config.TEST_IND_NAME, "100.23", "2023-5-06T07:40"],
        [indicator_config.TEST_IND_NAME, "30.19", "2023-5-16T07:40"],
        [indicator_config.TEST_IND_NAME, "760.75", "2023-5-23T12:10"],
        ["с", "760.75", "2023-5-23T12:10"],
        # ["кальций", "42342.17", "ascac"],
        # ["кальций", "fake", "2023-5-06T07:40"],
        # ["r/sm", "760.75"],
    ]
    payload = {"data": data}
    resp = await client.put(
        routes.create_log_from_list,
        json=payload,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание записи логов, создаётся всё или ничего", o=data)
    assert resp.status_code == 422
    resp = await client.get(routes.read_logs, params={})
    log.debug(resp)
    data = resp.json()
    log.debug("логи с пагинацией", o=data)
    assert resp.status_code == 200
    assert len(data.get("items")) == 1


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log_from_arr_with_duplicate_data(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест НЕ создания лога из множества записей, среди которых есть дубликаты значений"""
    await create_indicator()
    dt_val = datetime.now().strftime("%Y-%m-%dT%H:%M")
    data = [
        [indicator_config.TEST_IND_NAME, "100.23", dt_val],
        # [indicator_config.TEST_IND_NAME, "200.23", "2023-5-06T07:40"],
    ]
    payload = {"data": data}
    resp = await client.put(
        routes.create_log_from_list,
        json=payload,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание дубликата записи логов", o=data)
    # assert resp.status_code == 400
    resp = await client.put(
        routes.create_log_from_list,
        json=payload,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание дубликата записи логов", o=data)


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
    # return
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
