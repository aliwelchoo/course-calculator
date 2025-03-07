from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

import jsonpickle

from logic import User


class UserDB(ABC):
    @abstractmethod
    def get_user_by_name(self, user_name: str) -> User: ...

    @abstractmethod
    def set_user(self, new_user: User) -> None: ...


@dataclass
class MockUserDB(UserDB):
    users: list[User] = field(default_factory=list)

    def get_user_by_name(self, user_name: str) -> User:
        return next((user for user in self.users if user.name == user_name), None)

    def set_user(self, new_user: User) -> None:
        user_index = next(
            (i for i, user in enumerate(self.users) if user.name == new_user.name), None
        )
        if user_index:
            self.users[user_index] = new_user
        else:
            self.users.append(new_user)


@dataclass
class JsonUserDB(UserDB):
    root_path: Path = Path("json_store")

    def user_path(self, user_name: str) -> Path:
        return (self.root_path / user_name).with_suffix(".json")

    def get_user_by_name(self, user_name: str) -> User:
        if user_name is None:
            return None
        if not self.user_path(user_name).exists():
            return None
        with open(self.user_path(user_name)) as f:
            new_user: str = jsonpickle.decode(f.read())
        return new_user

    def set_user(self, new_user: User) -> None:
        with open(self.user_path(new_user.name), "w") as f:
            f.write(jsonpickle.encode(new_user))
