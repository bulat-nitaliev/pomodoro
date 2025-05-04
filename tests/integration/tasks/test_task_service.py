import pytest
from tests.fixtures.tasks.tasks_model import FakeCategory, FakeTasks
from tests.fixtures.users.user_model import FakeUserProfile
from app.tasks.schema import  TasksCreateSchema






@pytest.mark.asyncio
async def test_get_tasks__one__success(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    await task_service.create_task(
        body=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        user_id=user_create.user_id
    )
    tasks = await task_service.get_tasks()

    assert isinstance(tasks, list)

    assert tasks[0].name == fake_tasks.name
    assert tasks[0].pomodoro_count == fake_tasks.pomodoro_count
    assert tasks[0].category_id == category.id
    assert tasks[0].user_id == user_create.user_id


# @pytest.mark.asyncio
# async def test_get_tasks__empty(task_service):
#     tasks = await task_service.get_tasks()

#     assert isinstance(tasks, list)

#     assert tasks == []