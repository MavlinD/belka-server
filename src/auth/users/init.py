from datetime import timedelta

from src.auth.config import config
from src.auth.users.indicator_manager import IndicatorManager
from src.auth.users.log_manager import LogManager
from src.auth.users.security.jwt_actions import JWTStrategy
from src.auth.users.user_manager import UserManager


async def get_user_manager() -> UserManager:
    """user manager object"""
    return UserManager()


async def get_indicator_manager() -> IndicatorManager:
    """group manager object"""
    return IndicatorManager()


async def get_log_manager() -> LogManager:
    """group manager object"""
    return LogManager()


def get_jwt_strategy() -> JWTStrategy:
    """main JWT strategy"""
    return JWTStrategy(
        token_audience=config.TOKEN_AUDIENCE,
        secret=config.PRIVATE_KEY,
        algorithm=config.JWT_ALGORITHM,
        lifetime=timedelta(minutes=config.JWT_ACCESS_KEY_EXPIRES_TIME_MINUTES),
        public_key=config.PUBLIC_KEY,
    )
