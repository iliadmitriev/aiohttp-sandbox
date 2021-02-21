import pathlib
from os import environ as env


BASE_PATH = pathlib.Path(__file__).parent

access_log_format = '%r %s %b %t "%a"'

conf = {
    'engine': env.get('ENGINE'),
    'database': env.get('POSTGRES_DB'),
    'user': env.get('POSTGRES_USER'),
    'password': env.get('POSTGRES_PASSWORD'),
    'host': env.get('POSTGRES_HOST', 'localhost'),
    'port': env.get('POSTGRES_PORT', 5432)
}

if env.get('ENGINE') == 'postgres':
    dsn = f'{conf["engine"]}://{conf["user"]}:{conf["password"]}'\
        f'@{conf["host"]}:{conf["port"]}/{conf["database"]}'
else:
    dsn = 'sqlite:///:memory:'
