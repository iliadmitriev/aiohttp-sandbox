import aiopg.sa
from sqlalchemy.sql import select, update
from settings import dsn


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        dsn=dsn
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def setup_db(app):
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)


async def get_object_by_id(conn, obj, pk):
    result = await conn.execute(select([obj]).where(obj.id == pk))
    record = await result.first()
    if not record:
        raise RecordNotFound(f'{obj.__name__} with id={pk} is not found')
    return record


async def update_object_by_id(conn, obj, pk, values):
    result = await conn.execute(
        update(obj)
        .values(**values)
        .where(obj.id == pk)
        .returning(obj.c)
    )
    record = await result.first()
    if not record:
        raise RecordNotFound(f'{obj.__name__} with id={pk} is not found')
    return record


class RecordNotFound(Exception):
    """Requested record in database was not found"""
