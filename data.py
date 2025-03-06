from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Assignment:
    credits: int
    score: int = None


@dataclass
class Module:
    assignments: dict[str, Assignment] = field(default_factory=dict)


@dataclass
class User:
    name: str
    modules: dict[str, Module] = field(default_factory=dict)

    def get_modules(self) -> list[Module]:
        return list(self.modules.keys())

    def add_module(self, module: str) -> None:
        self.modules[module] = Module({})

    def update_module_name(self, module: str, new_module: str) -> None:
        self.modules[new_module] = self.modules.pop(module)


class UserDB(ABC):
    @abstractmethod
    def get_user_by_name(self, user_name: str) -> User: ...

    @abstractmethod
    def set_user_by_name(self, user_name: str, new_user: User) -> None: ...


@dataclass
class MockUserDB(UserDB):
    users: list[User] = field(default_factory=list)

    def get_user_by_name(self, user_name: str) -> User:
        return next((user for user in self.users if user.name == user_name), None)

    def set_user_by_name(self, user_name: str, new_user: User) -> None:
        user_index = next(
            (i for i, user in enumerate(self.users) if user.name == user_name), None
        )
        if user_index:
            self.users[user_index] = new_user
        else:
            self.users.append(new_user)
