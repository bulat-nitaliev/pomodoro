from sqlalchemy.orm import Session
from sqlalchemy import select, Result, delete, update
from core import get_db_session, Tasks
from schema import TasksSchema, TasksCreateSchema
from .task_cache import TaskCache


class TasksRepository:
    def __init__(self, db_session:Session):
        self.db_session = db_session

    def get_task(self,task_id:int):
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            res:Result  = session.execute(query).scalar()
            return res
        
    def get_tasks(self):
        query = select(Tasks).order_by(Tasks.id.desc())
        with self.db_session as session:
            res:Result  = session.execute(query).scalars().all()
            return list(res)


    def add_task(self, task:TasksCreateSchema, task_cache: TaskCache, user_id:int):
        stmt = Tasks(**task.model_dump(), user_id=user_id)
        with self.db_session as session:
            session.add(stmt)
            session.commit()
            task_cache.drop_tasks()
            return stmt.id
        
    def update_task(
            self,
            task_id:int, 
            task:TasksCreateSchema,  
            task_cache: TaskCache,
            user_id:int
            ):
       
        query = update(Tasks).where(Tasks.id == task_id).values(
            **task.model_dump(),
            user_id=user_id
            ).returning(Tasks.id)
        with self.db_session as session:
            id:int  = session.execute(query).scalar_one_or_none()
            session.commit()
            task_cache.drop_tasks()
            return self.get_task(id)
        
    def delete_task(self,task_id:int,  task_cache: TaskCache):
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()
            task_cache.drop_tasks()
            
    
    def get_user_task(self,task_id:int, user_id:int):
        query = select(Tasks).where(Tasks.id==task_id, Tasks.user_id==user_id)
        with self.db_session as session:
            task = session.execute(query).one_or_none()
            return task
        

def get_task_repository():
    db_session = get_db_session()
    return TasksRepository(db_session)