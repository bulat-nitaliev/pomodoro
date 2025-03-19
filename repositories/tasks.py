from sqlalchemy.orm import Session
from sqlalchemy import select, Result, delete, update
from core import get_db_session, Tasks
from schema import TasksSchema
from .task_cache import TaskCache


class TasksRepository:
    def __init__(self, db_session:Session):
        self.db_session = db_session

    def get_task(self,task_id:int):
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            res:Result  = session.execute(query).scalar()
            return res
        
    def get_tasks(self):
        query = select(Tasks).order_by(Tasks.id.desc())
        with self.db_session() as session:
            res:Result  = session.execute(query).scalars().all()
            return list(res)


    def add_task(self, task:TasksSchema, task_cache: TaskCache):
        stmt = Tasks(**task.model_dump())
        with self.db_session() as session:
            session.add(stmt)
            session.commit()
        task_cache.drop_tasks()
        return task
        
    def update_task(self,task_id:int, task:TasksSchema,  task_cache: TaskCache):
        query = update(Tasks).where(Tasks.id == task_id).values(
            **task.model_dump()
            ).returning(Tasks.id)
        with self.db_session() as session:
            id:int  = session.execute(query).scalar_one_or_none()
            session.commit()
            task_cache.drop_tasks()
            return self.get_task(id)
        
    def delete_task(self,task_id:int,  task_cache: TaskCache):
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()
            task_cache.drop_tasks()
            return {"message": f"task {task_id} deleted"}
            
        

def get_task_repository():
    db_session = get_db_session()
    return TasksRepository(db_session)