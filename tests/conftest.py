import asyncio

import pytest



pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.users.service",
    "tests.fixtures.tasks.service",
    "tests.fixtures.tasks.cache",
    "tests.fixtures.tasks.repository",
    "tests.fixtures.auth.client",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.config",
    "tests.fixtures.users.user_model",
    "tests.fixtures.infrastructure",
]



@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()