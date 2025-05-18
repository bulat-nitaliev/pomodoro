import pytest
from app.tasks import TaskService


@pytest.fixture
def task_service(task_cache, task_repository):
    return TaskService(task_cache=task_cache, task_repo=task_repository)
