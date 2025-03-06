import pytest

from application import Application
from services import create_services


@pytest.fixture()
def application() -> Application:
    return create_services()
