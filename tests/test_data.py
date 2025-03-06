from data import User, MockUserDB, Module


def test_get_user_by_name():
    data = MockUserDB([User("Name1"), User("Alistair"), User("Name2")])
    user = data.get_user_by_name("Alistair")
    assert isinstance(user, User)
    assert user.name == "Alistair"


def test_set_user_by_name():
    data = MockUserDB([])
    data.set_user(User("Alistair", {"test": Module()}))
    user = data.get_user_by_name("Alistair")
    assert user.name == "Alistair"
    assert user.get_module_names() == ["test"]
