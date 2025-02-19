from dataclasses import dataclass


@dataclass
class Assignment:
    credits: int


@dataclass
class Module:
    assignments: list[Assignment]


@dataclass
class User:
    name: str
    modules: list[Module]


users: list[User] = []


def get_user_by_name(user_name: str) -> User:
    return next((user for user in users if user.name == user_name), None)


def set_user_by_name(user_name: str, new_user: User) -> None:
    user_index = next((i for i, user in enumerate(users) if user.name == user_name), None)
    if user_index:
        users[user_index] = new_user
    else:
        users.append(new_user)
