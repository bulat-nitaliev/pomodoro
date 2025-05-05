import pytest
from tests.fixtures.tasks.tasks_model import FakeCategory, FakeTasks
from tests.fixtures.users.user_model import FakeUserProfile
from app.tasks.schema import  TasksCreateSchema, TasksSchema
from app.exception import TaskNotFoundException






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


@pytest.mark.asyncio
async def test_get_tasks__empty(task_service):
    tasks = await task_service.get_tasks()

    assert isinstance(tasks, list)

    assert tasks == []


@pytest.mark.asyncio
async def test_get_task_by_id__empty(task_service):
    try:
        tasks = await task_service.get_task_by_id(task_id=1)
    except TaskNotFoundException as e:
        assert e.detail == 'task not found'


@pytest.mark.asyncio
async def test_get_task_by_id__success(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    task_create = await task_service.task_repo.add_task(
        task=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        task_cache=task_service.task_cache,
        user_id=user_create.user_id
    )
    task = await task_service.get_task_by_id(task_id=task_create)

    assert isinstance(task, TasksSchema)
    assert task.name == fake_tasks.name
    assert task.pomodoro_count == fake_tasks.pomodoro_count
    assert task.category_id == category.id
    assert task.user_id == user_create.user_id
    


#update_task
@pytest.mark.asyncio
async def test_update_task__success(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    task_create = await task_service.task_repo.add_task(
        task=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        task_cache=task_service.task_cache,
        user_id=user_create.user_id
    )
    fake_task_update = FakeTasks()
    task = await task_service.update_task(
        task_id=task_create,
        task=TasksCreateSchema(
            name=fake_task_update.name,
            pomodoro_count=fake_task_update.pomodoro_count,
            category_id=category.id
        ),
        user_id=user_create.user_id
        )

    assert isinstance(task, TasksSchema)
    assert task.name == fake_task_update.name
    assert task.pomodoro_count == fake_task_update.pomodoro_count
    assert task.category_id == category.id
    assert task.user_id == user_create.user_id

@pytest.mark.asyncio
async def test_update_task_not_current_user(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    task_create = await task_service.task_repo.add_task(
        task=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        task_cache=task_service.task_cache,
        user_id=user_create.user_id
    )
    fake_task_update = FakeTasks()
    

    try:
        await task_service.update_task(
            task_id=task_create,
            task=TasksCreateSchema(
                name=fake_task_update.name,
                pomodoro_count=fake_task_update.pomodoro_count,
                category_id=category.id
            ),
            user_id=user.id
            )
    except TaskNotFoundException as e:
        assert e.detail == 'task not found'


@pytest.mark.asyncio
async def test_update_task_not_current_task(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    await task_service.task_repo.add_task(
        task=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        task_cache=task_service.task_cache,
        user_id=user_create.user_id
    )
    fake_task_update = FakeTasks()
    

    try:
        await task_service.update_task(
            task_id=fake_tasks.id,
            task=TasksCreateSchema(
                name=fake_task_update.name,
                pomodoro_count=fake_task_update.pomodoro_count,
                category_id=category.id
            ),
            user_id=user_create.user_id
            )
    except TaskNotFoundException as e:
        assert e.detail == 'task not found'


#delete_task
@pytest.mark.asyncio
async def test_delete_task__success(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    task_create = await task_service.task_repo.add_task(
        task=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        task_cache=task_service.task_cache,
        user_id=user_create.user_id
    )
    task = await task_service.delete_task(
        task_id=task_create,
        user_id=user_create.user_id
        )

    tasks = await task_service.get_tasks()

    assert isinstance(tasks, list)

    assert tasks == []


@pytest.mark.asyncio
async def test_delete_task_not_current_user(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    task_create = await task_service.task_repo.add_task(
        task=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        task_cache=task_service.task_cache,
        user_id=user_create.user_id
    )
    try:
        await task_service.delete_task(
            task_id=task_create,
            user_id=user.id
            )
    except TaskNotFoundException as e:
        assert e.detail == 'task not found'


@pytest.mark.asyncio
async def test_delete_task_not_current_task(task_service, user_service):
    user = FakeUserProfile()
    user_create = await user_service.create_user(username=user.username, password=user.password)
   
    category = FakeCategory()

    fake_tasks = FakeTasks()
    await task_service.task_repo.add_task(
        task=TasksCreateSchema(
            name=fake_tasks.name,
            pomodoro_count=fake_tasks.pomodoro_count,
            category_id=category.id
        ),
        task_cache=task_service.task_cache,
        user_id=user_create.user_id
    )

    try:
        await task_service.delete_task(
            task_id=fake_tasks.id,
            user_id=user_create.user_id
            )
    except TaskNotFoundException as e:
        assert e.detail == 'task not found'