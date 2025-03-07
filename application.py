from dataclasses import dataclass

from data import UserDB
from logic import User


@dataclass
class Application:
    user_name: str
    user_data: UserDB

    def login(self, name: str) -> User:
        self.user_name = name
        user = self.user_data.get_user_by_name(name)
        if not user:
            user = User(name)
            self.user_data.set_user(user)
        return user

    def get_user(self) -> User:
        return self.user_data.get_user_by_name(self.user_name)

    def update_user(self, new_user: User) -> None:
        assert new_user.name == self.user_name
        self.user_data.set_user(new_user)
