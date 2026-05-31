from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Engine for sessions (SQLite)
session_engine = create_async_engine(
    settings.database_url,
)

SessionLocal = async_sessionmaker(
    bind=session_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Engine for data analysis (PostgreSQL)
data_engine = create_async_engine(
    settings.data_database_url,
)

DataSessionLocal = async_sessionmaker(
    bind=data_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_data_db():
    async with DataSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
