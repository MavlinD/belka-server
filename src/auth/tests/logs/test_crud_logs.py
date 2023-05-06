from datetime import datetime
from typing import Callable

import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.conftest import Routs

skip = False
# skip = True
reason = "Temporary off"
pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_log(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_log: Callable
) -> None:
    """Тест создания изображения"""
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

    # уставновка произвольной даты-времени
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
