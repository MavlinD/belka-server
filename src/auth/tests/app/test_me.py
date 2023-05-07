# type: ignore
import pytest
from httpx import AsyncClient, Headers
from logrich.logger_ import log  # noqa

from src.auth.config import config
from src.auth.conftest import Routs

skip = False
# skip = True
reason = "Temporary off!-"

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.mark.skipif(skip, reason=reason)
@pytest.mark.asyncio
async def test_you_self(client: AsyncClient, routes: Routs, user_active_auth_headers: Headers) -> None:
    """Тест запроса св-в активного пол-ля"""

    resp = await client.get(routes.read_me, headers=user_active_auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    log.debug("", o=data)
    assert data.get("username") == config.TEST_USER_USERNAME
