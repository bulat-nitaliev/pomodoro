from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session, async_sessionmaker
from asyncio import current_task
from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine , AsyncSession


class DatabaseHelper:
    def __init__(self, url, echo:bool=False):
        self.engine = create_async_engine(url=url, echo_pool=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    # async def session_dependency(self) -> AsyncSession:
    #     async with self.session_factory() as session:
    #         yield session
    #         await session.close()


    async def get_scoped_session(self):
        session = async_scoped_session(session_factory=self.session_factory, scopefunc=current_task)
        return session
    
    async def session_dependency(self)->AsyncSession:
        session:AsyncSession = self.get_scoped_session()
        yield session
        await session.remove()
    
helper  = DatabaseHelper(url=settings.get_db_url)


# async def get_db_session():
#     async with db_helper.session_factory() as session:
#         yield session
#         await session.close()


