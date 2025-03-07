from dataclasses import dataclass

from data import User, UserDB


@dataclass
class Logic:
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


def score_needed(total_credits, score_so_far, credits_so_far, target_score):
    return (
        100
        * (total_credits * target_score - score_so_far)
        / (total_credits - credits_so_far)
    )