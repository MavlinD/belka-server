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


@pytest.mark.skipif(skip, reason=reason)
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
    log.debug("ответ на создание показателя.", o=data)
    assert resp.status_code == 201
    # assert data.get("id") == 2


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_read_indicator(
    client: AsyncClient, routes: Routs, add_test_indicator: Callable, add_test_image: Callable
) -> None:
    """Тест получения показателя"""
    await create_log(path="картинко.jpg", ads_id=1)
    resp = await client.get(
        routes.request_read_indicator(ad_attr=1),
    )
    log.debug(resp)
    data = resp.json()
    log.debug("запрос тестового показателя по ID", o=data)
    assert resp.status_code == 200
    assert Decimal(data.get("price")).quantize(Decimal("1.00")) == Decimal(config.TEST_AD_PRICE)
    assert len(data.get("image_set")) == 2
    await create_log(path="картинко.jpg", ads_id=1)
    resp = await client.get(
        routes.request_read_indicator(ad_attr=1),
    )
    log.debug(resp)
    data = resp.json()
    log.debug("попытка добавить второе изображение с тем же именем и тому же объявлению", o=data)
    assert len(data.get("image_set")) == 2


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_update_indicator(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест обновления показателя"""
    name_indicator = config.TEST_AD_NAME
    data = {"name": name_indicator, "price": 123, "desc": f"desc of ind {name_indicator}"}
    resp = await client.patch(
        routes.request_to_update_indicator(1),
        json=data,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание показателя", o=data)
    assert resp.status_code == 200


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_update_indicator_partial_name(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест частичного обновления показателя - только имя"""
    name_indicator = "Новое имя"
    data = {"name": name_indicator}
    resp = await client.patch(
        routes.request_to_update_indicator(1),
        json=data,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на частичное обновление показателя", o=data)
    assert resp.status_code == 200
    assert data.get("name") == name_indicator


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_update_indicator_partial_price(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест частичного обновления показателя - только цена"""
    payload = {"price": 98098.10}
    resp = await client.patch(
        routes.request_to_update_indicator(1),
        json=payload,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на частичное обновление показателя.", o=data)
    assert resp.status_code == 200
    assert data.get("price") == payload.get("price")


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_update_indicator_partial_desc(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест частичного обновления показателя - только описание"""
    payload = {"desc": "Новое описание"}
    resp = await client.patch(
        routes.request_to_update_indicator(1),
        json=payload,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на обновление - только описание", o=data)
    assert resp.status_code == 200
    assert data.get("desc") == payload.get("desc")


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_list_indicators(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест списка объявлений"""
    name_indicator = "второе тестовое объявление"
    data = {"name": name_indicator, "price": 123, "desc": f"desc of ind {name_indicator}"}

    resp = await client.put(
        routes.create_indicator,
        json=data,
        headers=user_active_auth_headers,
    )
    assert resp.status_code == 201
    resp = await client.get(routes.read_indicators)
    log.debug(resp)
    data = resp.json()
    log.debug("список объявлений", o=data)
    assert resp.status_code == 200
    assert len(data.get("items")) == 2


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_delete_indicator(
    client: AsyncClient, routes: Routs, user_active_auth_headers: Headers, add_test_indicator: Callable
) -> None:
    """Тест удаления показателя"""
    name_indicator = config.TEST_AD_NAME
    data = {"name": name_indicator, "price": 123, "desc": f"desc of ind {name_indicator}"}

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
    log.debug("список объявлений", o=data)
    assert resp.status_code == 200
    assert len(data.get("items")) == 1
