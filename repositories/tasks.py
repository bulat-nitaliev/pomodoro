from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, delete, update
from core import  Tasks
from schema import TasksSchema, TasksCreateSchema
from .task_cache import TaskCache


class TasksRepository:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def get_task(self,task_id:int):
        query = select(Tasks).where(Tasks.id == task_id)
        async with self.db_session as session:
            res:Result  = await session.execute(query)
            return res.scalar()
        
        # return await self.db_session.get(Tasks, task_id)
        
    async def get_tasks(self):
        query = select(Tasks).order_by(Tasks.id.desc())
        async with self.db_session as session:
            res:Result  = await session.execute(query)
            res = res.scalars().all()
            print(res)
            return list(res)
        
    



    async def add_task(self, task:TasksCreateSchema, task_cache: TaskCache, user_id:int):
        stmt = Tasks(**task.model_dump(), user_id=user_id)
        print(task)
        async with self.db_session as session:
            
            await session.add(stmt)
            
            await session.commit()
            await session.flush()
            print(stmt.id)
            await task_cache.drop_tasks()
            return stmt.id
        
    async def update_task(
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
        async with self.db_session as session:
            id:int  = await  session.execute(query)
            await session.commit()
            await task_cache.drop_tasks()
            return self.get_task(id.scalar_one_or_none())
        
    async def delete_task(self,task_id:int,  task_cache: TaskCache):
        query = delete(Tasks).where(Tasks.id == task_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
            await task_cache.drop_tasks()
            
    
    async def get_user_task(self,task_id:int, user_id:int):
        query = select(Tasks).where(Tasks.id==task_id, Tasks.user_id==user_id)
        with self.db_session as session:
            task = session.execute(query).one_or_none()
            return task
        

