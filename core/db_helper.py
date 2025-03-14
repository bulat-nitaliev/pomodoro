from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from core.config import settings

class DatabaseHelper:
    def __init__(self, url, echo:bool=False):
        self.engine = create_engine(url=url, echo_pool=echo)
        self.sessionfactory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )
    def get_db_session(self):
        return self.sessionfactory

    def get_scopedsession(self):
        session = scoped_session(
            session_factory=self.sessionfactory,
            )
        return session
    
db_helper  = DatabaseHelper(url=settings.db_url)


