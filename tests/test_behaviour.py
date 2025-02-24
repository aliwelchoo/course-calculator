from unittest.mock import patch

from pytest_bdd import scenarios, given, when, then, parsers

from src import services
from src.data import MockUserDB
from src.main import app
from src.services import application

scenarios("features")


@given("the site is running without error")
def run_app(dash_duo):
    dash_duo.start_server(app, port=8060)
    dash_duo.wait_for_page(timeout=10)
    assert dash_duo.get_logs() == [], "browser console should contain no error"


@given("I am {user}")
def logged_in_as(user):
    with patch.object(services, "data", MockUserDB([])):
        application.login(user)
        yield


@given(parsers.parse("I have {module_name} module in my course breakdown"))
def module_already_in_course(module_name):
    me = application.get_user()
    me.modules.append(module_name)


@when("I go to the course breakdown page")
def go_to_course_breakdown(dash_duo):
    dash_duo.multiple_click("#Course-breakdown-link", 1)


@when(parsers.parse("I put {module_name} in the new module input"))
def new_module_add_name(module_name, dash_duo):
    name_input = dash_duo.find_element("#new_module_name")
    name_input.send_keys(module_name)


@when("I put {new_module_name} in the {existing name} name input")
def existing_module_add_name(new_module_name, existing_module_name):
    pass


@when("I press the add module button")
def click_add_module():
    pass


@then("{module_name} should be in my course")
def module_in_course(module_name):
    pass


@then("{module_name} should be in my course")
def module_not_in_course(module_name):
    return not module_in_course(module_name)


@then("the duplicate module error should be shown")
def showing_duplicate_module_error():
    pass
