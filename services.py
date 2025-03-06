from application import Application
from data import UserDB, MockUserDB


def create_services() -> Application:
    blank_data: UserDB = MockUserDB()
    blank_application: Application = Application(None, blank_data)
    return blank_application


application: Application = create_services()
