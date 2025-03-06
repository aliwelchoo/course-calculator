from time import sleep

from pytest_bdd import scenarios, given, when, then, parsers

import services
from app import app
from services import create_services

scenarios("features")


@given("the site is running without error")
def run_app(dash_duo):
    dash_duo.start_server(app, port=8060)
    dash_duo.wait_for_page(timeout=20)
    services.application = create_services()
    assert dash_duo.get_logs() == [], "browser console should contain no error"


@given(parsers.parse("I am {user}"))
def logged_in_as(user):
    services.application.login(user)


@given(parsers.parse("I have {module_name} module in my course breakdown"))
def module_already_in_course(module_name):
    me = services.application.get_user()
    me.modules.append(module_name)
    services.application.update_user(me)


@when("I go to the course breakdown page")
def go_to_course_breakdown(dash_duo):
    dash_duo.multiple_click("#Course-breakdown-link", 1)


@when(parsers.parse("I put {module_name} in the new module input"))
def new_module_add_name(module_name, dash_duo):
    dash_duo.find_element("#new_module_name").send_keys(module_name)


@when(parsers.parse("I put {new_module_name} in the {existing name} name input"))
def existing_module_add_name(new_module_name, existing_module_name):
    pass


@when("I press the add module button")
def click_add_module(dash_duo):
    dash_duo.find_element("#add_module").click()


@then(parsers.parse("{module_name} should be in my course"))
def module_in_course(module_name):
    assert module_name in services.application.get_user().modules


@then(parsers.parse("{module_name} should exist only once in my course"))
def module_not_duplicated_in_course(module_name):
    assert services.application.get_user().modules.count(module_name) == 1


@then("the duplicate module error should be shown")
def showing_duplicate_module_error():
    pass
