from aiohttp import web
from routes import setup_routes
from aiohttp_jinja2 import setup as setup_jinja2
from aiohttp_swagger import setup_swagger
from jinja2 import FileSystemLoader
import pathlib
import sys
import logging

from db import setup_db
from middlewares import setup_middlewares
from settings import access_log_format

BASE_PATH = pathlib.Path(__file__).parent


async def init_app(argv=None):
    app = web.Application()

    setup_routes(app)
    setup_jinja2(app, loader=FileSystemLoader(BASE_PATH / 'templates'))
    setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)
    setup_middlewares(app)
    setup_db(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.INFO)
    app = init_app(argv)
    web.run_app(
        app,
        access_log_format=access_log_format
    )


if __name__ == '__main__':
    main(sys.argv[1:])
