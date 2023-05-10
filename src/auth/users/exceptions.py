from fastapi import HTTPException
from logrich.logger_ import log  # noqa
from starlette import status

from src.auth.schemas.token import UserScheme
from src.django_space.indicators.models import Log


class FastAPIUsersException(HTTPException):
    def __init__(self) -> None:
        self.detail: str = "Некорректный запрос"
        self.status_code: int = status.HTTP_400_BAD_REQUEST


class UserNotExists(FastAPIUsersException):
    def __init__(self, user: str = None) -> None:
        self.detail = f"User {user} не существует"
        self.status_code = status.HTTP_404_NOT_FOUND


class IndicatorNotExists(FastAPIUsersException):
    def __init__(self, indicator: str) -> None:
        self.detail = f"Индикатор <{indicator}> не существует"
        self.status_code = status.HTTP_404_NOT_FOUND


class IndicatorExists(FastAPIUsersException):
    def __init__(self, indicator: str) -> None:
        self.detail = f"Индикатор <{indicator}> существует"
        self.status_code = status.HTTP_400_BAD_REQUEST


class LogNotExists(FastAPIUsersException):
    def __init__(self, log_: str | int) -> None:
        self.detail = f"Изображение <{log_}> не существует"
        self.status_code = status.HTTP_404_NOT_FOUND


class LogExists(FastAPIUsersException):
    def __init__(self, log_: Log) -> None:
        self.detail = f"Log <{log_}> уже существует"
        self.status_code = status.HTTP_400_BAD_REQUEST


class UserInactive(FastAPIUsersException):
    def __init__(self, user: UserScheme | None = None) -> None:
        if user:
            self.detail = f"User {user.username} inactive"
        else:
            self.detail = str(self)
        self.status_code = status.HTTP_400_BAD_REQUEST


class InvalidVerifyToken(FastAPIUsersException):
    def __init__(self, msg: Exception | str | None = None) -> None:
        self.detail = f"Токен не валиден: {msg}"
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class InvalidCredentials(FastAPIUsersException):
    def __init__(self, msg: Exception | str | None = None) -> None:
        self.detail = f"Пользователь {msg} не существует или пароль не подходит."
        self.status_code = status.HTTP_400_BAD_REQUEST
