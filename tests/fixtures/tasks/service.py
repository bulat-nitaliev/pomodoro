import pytest
from app.tasks import TaskService

@pytest.fixture
def auth_service(task_cache,task_repo):
    return TaskService(
        task_cache=task_cache,
        task_repo=task_repo
        )