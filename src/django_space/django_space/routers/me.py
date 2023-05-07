from fastapi import Depends, status
from logrich.logger_ import log  # noqa

from src.auth.assets import APIRouter
from src.auth.schemas.token import UserScheme
from src.auth.users.dependencies import get_current_active_user

router = APIRouter()


@router.get(
    "/",
    response_model=UserScheme,
    name="get current user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
    },
)
async def read_me(
    user: UserScheme = Depends(get_current_active_user),
) -> UserScheme:
    """get current user"""
    resp = await UserScheme.from_orms(user)
    return resp
