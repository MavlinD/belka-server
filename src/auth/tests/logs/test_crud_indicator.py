from decimal import Decimal
from typing import Callable

import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.conftest import Routs
from src.auth.tests.app.test_tools import create_log
from src.django_space.indicators.config import config

# skip = False
skip = True
reason = "Temporary off"
pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_indicator(client: AsyncClient, routes: Routs, user_active_auth_headers: Headers) -> None:
    """Тест создания показателя"""
    name_indicator = "тестовый индикатор"
    resp = await client.put(
        routes.create_indicator,
        json={"name": name_indicator, "unit": "кг", "desc": f"desc of ind {name_indicator}"},
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание показателя", o=data)
    assert resp.status_code == 201
    # assert data.get("id") == 2


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_read_indicator(
    client: AsyncClient,
    routes: Routs,
    add_test_indicator: Callable,
) -> None:
    """Тест получения показателя"""
    resp = await client.get(routes.request_read_indicator(indicator_attr=1))
    log.debug(resp)
    data = resp.json()
    log.debug("запрос тестового показателя по ID", o=data)
    assert resp.status_code == 200


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_update_indicator(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест обновления показателя, частичное обновление"""
    name_indicator = "Калифорний"
    data = {"name": name_indicator, "desc": f"desc of ind {name_indicator}"}
    resp = await client.patch(
        routes.request_to_update_indicator(1),
        json=data,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на обновление показателя", o=data)
    assert resp.status_code == 200
    assert data.get("name") == name_indicator
    assert data.get("unit") == config.TEST_IND_UNIT


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_list_indicators(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест списка показателей"""
    name_indicator = "второй тестовый показатель"
    data = {"name": name_indicator, "unit": "mg/sq", "desc": f"desc of ind {name_indicator}"}

    resp = await client.put(
        routes.create_indicator,
        json=data,
        headers=user_active_auth_headers,
    )
    assert resp.status_code == 201
    resp = await client.get(routes.read_indicators)
    log.debug(resp)
    data = resp.json()
    log.debug("список показателей", o=data)
    assert resp.status_code == 200
    assert len(data.get("items")) == 2


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_delete_indicator(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест удаления показателя"""
    name_indicator = "Сера"
    data = {"name": name_indicator, "unit": "mg/sq", "desc": f"desc of ind {name_indicator}"}

    resp = await client.put(
        routes.create_indicator,
        json=data,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание показателя", o=data)
    assert resp.status_code == 201

    resp = await client.delete(routes.request_delete_indicator(2), headers=user_active_auth_headers)
    assert resp.status_code == 204
    resp = await client.get(routes.read_indicators)
    log.debug(resp)
    data = resp.json()
    log.debug("список показателей", o=data)
    assert resp.status_code == 200
    assert len(data.get("items")) == 1
