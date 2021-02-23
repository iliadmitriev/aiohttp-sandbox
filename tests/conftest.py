import pytest
import pathlib
import sys
import time
from aiohttp import web
import jwt

BASE_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(BASE_PATH)


@pytest.fixture
def fixture_setup_app():
    from routes import setup_routes
    from middlewares import setup_middlewares
    from db import setup_db
    app = web.Application()
    setup_routes(app)
    setup_middlewares(app)
    setup_db(app)
    return app


@pytest.fixture
def cli(loop, aiohttp_client, fixture_setup_app):
    """
    fixtures loop, aiohttp_client - loaded from pytest-aiohttp
    """
    return loop.run_until_complete(aiohttp_client(fixture_setup_app))


@pytest.fixture
def admin_access_token():
    from settings import JWT_SECRET_KEY
    payload = {
        'token_type': 'access',
        # expires in 300 seconds = 5 min
        'exp': int(time.time() + 300),
        'username': 'admin',
        'user_id': 100,
        'scope': 'admin'
    }
    return jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm='HS256')


@pytest.fixture
def unprivileged_access_token():
    from settings import JWT_SECRET_KEY
    payload = {
        'token_type': 'access',
        # expires in 300 seconds = 5 min
        'exp': int(time.time() + 300),
        'username': 'common-user',
        'user_id': 200,
    }
    return jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm='HS256')
