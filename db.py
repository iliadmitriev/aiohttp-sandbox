import aiopg.sa
from sqlalchemy.sql import select, update, insert, delete
from settings import dsn
from exceptions import BadRequest, RecordNotFound
from sqlalchemy.exc import CompileError


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


async def get_objects(conn, obj):
    select_query = select([obj])
    cursor = await conn.execute(select_query)
    records = await cursor.fetchall()
    objs = [dict(p) for p in records]
    return objs


async def get_object_by_id(conn, obj, pk):
    result = await conn.execute(select([obj]).where(obj.id == pk))
    record = await result.first()
    if not record:
        raise RecordNotFound(f'{obj.__name__} with id={pk} is not found')
    return record


async def update_object_by_id(conn, obj, pk, values):
    try:
        result = await conn.execute(
            update(obj)
            .values(**values)
            .where(obj.id == pk)
            .returning(*obj.__table__.columns)
        )
        record = await result.first()
    except CompileError as e:
        raise BadRequest(str(e))
    if not record:
        raise RecordNotFound(f'{obj.__name__} with id={pk} is not found')
    return record


async def insert_object(conn, obj, values):
    try:
        result = await conn.execute(
            insert(obj)
            .values(**values)
            .returning(*obj.__table__.columns)
        )
        record = await result.first()
    except Exception as e:
        raise BadRequest(str(e))

    return record

