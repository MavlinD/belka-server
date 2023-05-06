import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.conftest import Routs
from src.auth.tests.logs.conftest import insert_fake_indicators, insert_fake_logs

skip = False
# skip = True
reason = "Temporary off"
pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_list_log_with_paginate(client: AsyncClient, routes: Routs, user_active_auth_headers: Headers) -> None:
    """Тест списка логов с пагинацией"""
    AMOUNT_INDICATORS = 5
    AMOUNT_LOGS = 30
    SIZE = 5
    PAGE = 1
    INDICATOR_ATTR = 1
    # return
    await insert_fake_indicators(amount_indicators=AMOUNT_INDICATORS)
    await insert_fake_logs(amount_logs=AMOUNT_LOGS, amount_indicators=AMOUNT_INDICATORS)

    params = {"page": PAGE, "size": SIZE, "indicator_attr": INDICATOR_ATTR}

    resp = await client.get(routes.read_logs, params=params)
    log.debug(resp)
    data = resp.json()
    log.debug("логи с пагинацией", o=data)
    assert resp.status_code == 200
    # отфильтруем рез-т по параметру запроса и сравним с общим кол-вом записей
    filtered_items = [item for item in data.get("items") if item.get("indicator", {}).get("id") == INDICATOR_ATTR]
    assert len(filtered_items) == len(data.get("items"))
    # запрос с периодом
    params = {
        "page": PAGE,
        "size": SIZE,
        "date__gte": "2023-5-01T00:00",
        "date__lte": "2023-5-31T23:59",
        "indicator_attr": INDICATOR_ATTR,
    }

    resp = await client.get(routes.read_logs, params=params)
    log.debug(resp)
    data = resp.json()
    log.debug("логи с пагинацией, запрос с периодом", o=data)
    assert resp.status_code == 200
