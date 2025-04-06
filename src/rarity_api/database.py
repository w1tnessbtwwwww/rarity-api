import sqlalchemy
from settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

meta = sqlalchemy.MetaData()
engine = create_async_engine(settings.db_url, echo=True)
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    metadata = meta


async def get_session():
    async with async_session() as session:
        yield session
