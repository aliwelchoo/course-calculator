from src.data import get_user_by_name, set_user_by_name, User

user_name: str


def login(name):
    global user_name
    user_name = name
    if not get_user_by_name(name):
        set_user_by_name(name, User(name, []))
