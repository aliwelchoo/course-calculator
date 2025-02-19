from unittest.mock import patch

from src import data
from src.data import get_user_by_name, User, set_user_by_name


def test_get_user_by_name():
    with patch.object(data, 'users', [User("Other", []), User("Alistair", []), User("Other", [])]):
        user = get_user_by_name("Alistair")
    assert isinstance(user, User)
    assert user.name == "Alistair"


def test_set_user_by_name(mocker):
    mocker.patch("src.data.users", [])
    set_user_by_name("Alistair", User("Alistair", ["test"]))
    user = get_user_by_name("Alistair")
    assert user.name == "Alistair"
    assert user.modules == ["test"]
