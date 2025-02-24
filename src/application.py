from dataclasses import dataclass

from src.data import User, UserDB


@dataclass
class Application:
    user_name: str
    user_data: UserDB

    def login(self, name: str) -> None:
        self.user_name = name
        if not self.user_data.get_user_by_name(name):
            self.user_data.set_user_by_name(name, User(name, []))

    def get_user(self) -> User:
        return self.user_data.get_user_by_name(self.user_name)

