from aiohttp import web
from routes import setup_routes
from aiohttp_jinja2 import setup as setup_jinja2
from aiohttp_swagger import setup_swagger
from aiohttp_apispec import setup_aiohttp_apispec
from jinja2 import FileSystemLoader
import sys
import logging

from db import setup_db
from middlewares import setup_middlewares
from settings import access_log_format, BASE_PATH, APP_PORT, APP_HOST


async def init_app(argv=None):
    app = web.Application()

    setup_routes(app)
    setup_jinja2(app, loader=FileSystemLoader(BASE_PATH / 'templates'))
    setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)
    setup_aiohttp_apispec(
        app=app,
        title="Profiles documentation",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
        static_path="/api/static"
    )
    setup_middlewares(app)
    setup_db(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.INFO)
    app = init_app(argv)
    web.run_app(
        app,
        access_log_format=access_log_format,
        host=APP_HOST,
        port=APP_PORT
    )


if __name__ == '__main__':
    main(sys.argv[1:])
