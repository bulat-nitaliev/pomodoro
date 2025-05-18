import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.config import settings as config
from app.infrastructure.db.database import Base
from redis import asyncio as redis
from app.config import settings


@pytest.fixture
def settings():
    return Settings()


@pytest_asyncio.fixture(scope="function")
def test_cache_get_connect() -> redis.Redis:
    return redis.Redis(
        host=config.TEST_CACHE_HOST,
        port=config.TEST_CACHE_PORT,
        db=config.TEST_CACHE_DB,
    )


engine = create_async_engine(
    url=config.get_test_db_url, future=True, echo=False, pool_pre_ping=True
)


AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models(task_cache):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await task_cache.drop_tasks()
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session() -> AsyncSession:
    yield AsyncSessionFactory()
