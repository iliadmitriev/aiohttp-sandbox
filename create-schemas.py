from sqlalchemy import create_engine
from settings import dsn
from models import Base


engine = create_engine(dsn)
Base.metadata.create_all(engine)

