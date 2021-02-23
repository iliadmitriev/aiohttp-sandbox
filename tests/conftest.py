import pathlib
import sys
import time
import jwt
from sqlalchemy import create_engine
import pytest

from models import Base

BASE_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(BASE_PATH)


def create_test_db():
    import secrets
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from settings import dsn
    test_db_name = f'test_{secrets.token_hex(nbytes=10)}'

    con = psycopg2.connect(dsn=dsn)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(test_db_name))
    )
    cur.close()
    return test_db_name


def setup_test_db_dsn():
    test_db = create_test_db()
    from settings import conf
    test_db_dsn = f'{conf["engine"]}://{conf["user"]}:{conf["password"]}'\
        f'@{conf["host"]}:{conf["port"]}/{test_db}'
    return test_db_dsn


def create_and_migrate_test_db_dsn():
    test_db_dsn = setup_test_db_dsn()
    engine = create_engine(test_db_dsn)
    Base.metadata.create_all(engine)
    return test_db_dsn


def get_admin_access_token(user_id=100):
    from settings import JWT_SECRET_KEY
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
    from settings import JWT_SECRET_KEY
    payload = {
        'token_type': 'access',
        # expires in 300 seconds = 5 min
        'exp': int(time.time() + 300),
        'username': 'common-user',
        'user_id': user_id,
    }
    return jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm='HS256')
