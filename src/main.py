# isort: skip_file
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from logrich.logger_ import errlog, log  # noqa
from logrich.logger_assets import console
from rich.style import Style
from starlette.staticfiles import StaticFiles

from src.auth.assets import get_project
from src.auth.config import config
from src.auth.handlers.errors.handlers import init_err_handlers
from src.auth.helpers.tools import show_dbs_engine
from src.auth.middleware import init_middleware
from src.auth.users.router.open_api import reset_open_api
from src.on_startup import print_modes

project = get_project()

sw_params = {
    "title": project["name"],
    "version": project["version"],
    "description": f'{project["description"]} <br>Current database engine: **{show_dbs_engine()}**',
    "debug": config.DEBUG,
}

sw_ui = {"defaultModelsExpandDepth": -1}

tags_metadata = [
    {
        "name": "JWT",
        "description": "Всё для работы с **JWT**.",
    },
    {
        "name": "CRUD for Ads",
        "description": "Базовые операции с объявлениями.",
    },
    {
        "name": "CRUD for Images",
        "description": "Базовые операции с изображениями.",
    },
]


def run_app() -> FastAPI:
    """start main app - one entrypoint"""
    app = FastAPI(
        **sw_params,
        swagger_ui_parameters=sw_ui,
        contact={
            "name": project["name"],
            "url": config.ROOT_API_URL,
        },
        openapi_tags=tags_metadata,
    )
    try:
        from src.django_space.django_space.asgi import django_app
        from src.django_space.django_space.routers import init_base_router
        from src.django_space.indicators.routers import init_router as init_indicator_router

        # start django urls
        init_base_router(app)
        init_indicator_router(app)

        # order important!
        app.mount("/static", StaticFiles(directory="src/auth/static"), name="open-api")
        app.mount(
            "/django/static",
            StaticFiles(directory="src/django_space/staticfiles"),
            name="django-static",
        )
        app.mount("/django", django_app)

    except Exception as err:
        log.warning(err)

    init_err_handlers(app)
    # отключи линию ниже, если нужен стиль по умолчанию
    reset_open_api(app)
    add_pagination(app)
    # uncomment below if you need middleware
    init_middleware(app)

    return app


@errlog.catch
def main() -> None:
    console.rule(f"[green]{sw_params['title']}[/]", style=Style(color="magenta"))
    print_modes()

    uvicorn.run(
        "main:run_app",
        debug=config.DEBUG,
        reload=config.RELOAD,
        factory=True,
        port=config.API_PORT_INTERNAL,
        host=config.API_HOSTNAME,
    )


if __name__ == "__main__":
    if config.TESTING:
        log.warning("отключите режим тестирования - установите переменную TESTING=False")
        exit(128)

    main()
