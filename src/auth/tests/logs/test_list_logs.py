from typing import Callable

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
    # return
    # await insert_fake_indicators(amount_indicators=AMOUNT_INDICATORS)
    await insert_fake_logs(amount_logs=AMOUNT_LOGS, amount_indicators=AMOUNT_INDICATORS)

    params = {"page": PAGE, "size": SIZE, "indicator_attr": 1}

    resp = await client.get(routes.read_logs, params=params)
    log.debug(resp)
    data = resp.json()
    log.debug("логи с пагинацией-", o=data)
    # assert resp.status_code == 200
    # assert data.get("total") == AMOUNT_ADS + 1
    # # assert len(data) == 2
    # # return
    # assert len(data.get("items")) == SIZE
    # assert data.get("page") == PAGE
    # assert data.get("size") == SIZE
