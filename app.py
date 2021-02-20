from aiohttp import web
from routes import setup_routes
from aiohttp_jinja2 import setup as setup_jinja2
from aiohttp_swagger import setup_swagger
from jinja2 import FileSystemLoader
import os
import logging

BASE_PATH = os.path.dirname(__file__)

app = web.Application()


setup_routes(app)
setup_jinja2(app, loader=FileSystemLoader(BASE_PATH + '/templates'))
setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    web.run_app(app, access_log_format='%r %s %b %t "%a"')
