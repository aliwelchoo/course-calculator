from typing import Type

from logic import Logic
from data import UserDB, JsonUserDB


def create_logic(db: Type[UserDB]) -> Logic:
    data: UserDB = db()
    app: Logic = Logic(None, data)
    return app


logic: Logic = create_logic(JsonUserDB)
