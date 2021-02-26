import pathlib
import sys
import time
import jwt
from sqlalchemy import create_engine
from models import Base
import pytest
import psycopg2
import secrets
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings import dsn, conf, JWT_SECRET_KEY

BASE_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(BASE_PATH)


def create_test_db():
    test_db_name = f'test_{secrets.token_hex(nbytes=10)}'
    con = psycopg2.connect(dsn=dsn)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(test_db_name))
    )
    cur.close()
    return test_db_name


def drop_test_db(test_db_name):

    con = psycopg2.connect(dsn=dsn)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(
        sql.Identifier(test_db_name))
    )
    cur.close()


def setup_test_db_dsn():
    test_db = create_test_db()
    test_db_dsn = f'{conf["engine"]}://{conf["user"]}:{conf["password"]}'\
        f'@{conf["host"]}:{conf["port"]}/{test_db}'
    return test_db_dsn, test_db


def create_and_migrate_test_db_dsn():
    test_db_dsn, test_db = setup_test_db_dsn()
    engine = create_engine(test_db_dsn)
    Base.metadata.create_all(engine)
    return test_db_dsn, test_db


@pytest.fixture(scope='class')
def get_dsn(request):
    test_dsn, test_db = create_and_migrate_test_db_dsn()
    request.cls.dsn = test_dsn
    yield test_dsn
    drop_test_db(test_db)


def get_admin_access_token(user_id=100):
    payload = {
        'token_type': 'access',
        # expires in 300 seconds = 5 min
        'exp': int(time.time() + 300),
        'username': 'admin',
        'user_id': user_id,
        'scope': 'admin'
    }
    return jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm='HS256')


def get_unprivileged_access_token(user_id=200):
    payload = {
        'token_type': 'access',
        # expires in 300 seconds = 5 min
        'exp': int(time.time() + 300),
        'username': 'common-user',
        'user_id': user_id,
    }
    return jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm='HS256')


