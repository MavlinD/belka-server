from fastapi_users.openapi import OpenAPIResponseType
from starlette import status


def obj_exist_responses(obj: str) -> OpenAPIResponseType:
    """исп-ся в Swagger"""
    return {
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{obj} уже существует.",
        },
    }


def obj_not_exist_responses(obj: str) -> OpenAPIResponseType:
    """исп-ся в Swagger"""
    return {
        status.HTTP_404_NOT_FOUND: {
            "description": f"{obj} не существует.",
        },
    }
