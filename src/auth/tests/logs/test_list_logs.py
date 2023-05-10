import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.conftest import Routs
from src.auth.tests.app.test_tools import create_indicator

# skip = False
skip = True
reason = "Temporary off"
pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


# @pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_list_log_with_annotate(client: AsyncClient, routes: Routs, user_active_auth_headers: Headers) -> None:
    """Тест списка логов с агрегацией"""
    SIZE = 5
    PAGE = 1
    for ind in ["медь", "сера"]:
        await create_indicator(name=ind, unit="гр", desc="---")

    logs = [
        ["медь", 100.23, "2023-5-06T07:40"],
        ["медь", 30.19, "2023-5-16T07:40"],
        ["медь", 260.75, "2023-5-23T12:10"],
        ["медь", 760.75, "2023-5-23T12:10"],
        # ----------------------------------
        ["сера", 80.23, "2023-5-06T07:40"],
        ["сера", 20.19, "2023-5-16T07:40"],
        ["сера", 260.75, "2023-5-23T12:10"],
        ["сера", 450.88, "2023-5-23T12:10"],
    ]
    for log_ in logs:
        await client.put(
            routes.request_create_log(indicator_attr=log_[0]),
            json={
                "val": log_[1],
                "date": log_[2],
            },
            headers=user_active_auth_headers,
        )

    params = {"page": PAGE, "size": SIZE}

    resp = await client.get(routes.read_logs, params=params)
    log.debug(resp)
    data = resp.json()
    log.debug("логи с аггрегацией-", o=data)
    assert resp.status_code == 200
    assert data.get("items")[0].get("min") == 30.19
    assert data.get("items")[1].get("min") == 20.19
    assert data.get("items")[0].get("avg") == 297.057
    assert data.get("items")[1].get("avg") == 183.767
