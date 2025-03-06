from typing import Type

from application import Application
from data import UserDB, JsonUserDB


def create_services(db: Type[UserDB]) -> Application:
    data: UserDB = db()
    app: Application = Application(None, data)
    return app


application: Application = create_services(JsonUserDB)
