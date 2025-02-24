from dataclasses import dataclass

from src.data import User, UserDB


@dataclass
class Application:
    user_name: str
    user_data: UserDB

    def login(self, name: str) -> User:
        self.user_name = name
        user = self.user_data.get_user_by_name(name)
        if not user:
            user = User(name, [])
            self.user_data.set_user_by_name(name, user)
        return user

    def get_user(self) -> User:
        return self.user_data.get_user_by_name(self.user_name)

