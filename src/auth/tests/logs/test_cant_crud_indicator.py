from typing import Callable

import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.conftest import Routs
from src.django_space.indicators.config import config

skip = False
# skip = True
reason = "Temporary off"
pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_create_indicator(
    client: AsyncClient,
    routes: Routs,
    user_active_auth_headers: Headers,
    add_test_indicator: Callable,
) -> None:
    """Тест НЕ возможности создания показателя"""
    name_indicator = "ts"
    resp = await client.put(
        routes.create_indicator,
        json={"name": name_indicator, "unit": "any/str", "desc": f"desc of ind {name_indicator}"},
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на создание показателя.", o=data)
    assert resp.status_code == 422

    name_indicator = config.TEST_IND_NAME
    data = {"name": name_indicator, "unit": "any/str", "desc": f"desc of ind {name_indicator}"}
    resp = await client.put(
        routes.create_indicator,
        json=data,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на обновление показателя - уже существует", o=data)
    assert resp.status_code == 400


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_update_indicator(
    client: AsyncClient,
    routes: Routs,
    user_active_auth_headers: Headers,
    add_test_indicator: Callable,
) -> None:
    """Тест НЕ возможности обновления показателя"""
    name_indicator = config.TEST_IND_NAME
    data = {"name": name_indicator, "unit": "any/str" * 5, "desc": f"desc of ind {name_indicator}"}
    resp = await client.patch(
        routes.request_to_update_indicator(1),
        json=data,
        headers=user_active_auth_headers,
    )
    log.debug(resp)
    data = resp.json()
    log.debug("ответ на обновление показателя", o=data)
    assert resp.status_code == 422
