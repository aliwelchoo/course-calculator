from src.application import Application
from src.data import UserDB, MockUserDB

data: UserDB = MockUserDB()
application = Application(None, data)
