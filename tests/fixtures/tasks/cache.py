from app.tasks import TaskCache
import pytest
from dataclasses import dataclass
from redis import asyncio as Redis


@dataclass
class FakeTaskCache:
    redis:Redis


@pytest.fixture
def task_cache():
    return FakeTaskCache(redis=Redis())




