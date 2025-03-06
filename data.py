from abc import ABC, abstractmethod
from dataclasses import dataclass, field


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


class UserDB(ABC):
    @abstractmethod
    def get_user_by_name(self, user_name: str) -> User:
        ...

    @abstractmethod
    def set_user_by_name(self, user_name: str, new_user: User) -> None:
        ...


@dataclass
class MockUserDB(UserDB):
    users: list[User] = field(default_factory=list)

    def get_user_by_name(self, user_name: str) -> User:
        return next((user for user in self.users if user.name == user_name), None)

    def set_user_by_name(self, user_name: str, new_user: User) -> None:
        user_index = next((i for i, user in enumerate(self.users) if user.name == user_name), None)
        if user_index:
            self.users[user_index] = new_user
        else:
            self.users.append(new_user)
