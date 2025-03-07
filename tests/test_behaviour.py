from time import sleep, time

from dash.testing import newhooks
from dash.testing.browser import Browser
from dash.testing.wait import until
from pytest_bdd import scenarios, given, when, then, parsers

import services
from app import app
from data import MockUserDB
from services import create_services

from selenium.webdriver.chrome.options import Options


def new_pytest_setup_options(browser):
    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ['user-data-dir'])
    return options


Browser._get_wd_options = new_pytest_setup_options
scenarios("features")


def pattern_matching_selector(index: int, type: str) -> str:
    return r'#\{\"index\"\:' + str(index) + r'\,\"type\"\:\"' + type + r'\"\}'


def wait_for_callbacks(dash_duo):
    sleep(1)
    until(dash_duo._wait_for_callbacks, timeout=40, poll=0.3)


@given("the site is running without error")
def run_app(dash_duo):
    dash_duo._last_ts = time()
    dash_duo.start_server(app, port=8060)
    dash_duo.wait_for_page(timeout=20)
    services.application = create_services(MockUserDB)
    wait_for_callbacks(dash_duo)
    logs = dash_duo.get_logs()
    important_logs = [log for log in logs if "Error: Callback failed: the server did not respond." not in log["message"]]
    assert important_logs == [], "browser console should contain no error"


@given(parsers.parse("I am {user}"))
def logged_in_as(user):
    services.application.login(user)


@given(parsers.parse("I have {module_name} in my course breakdown"))
def module_already_in_course(module_name):
    me = services.application.get_user()
    me.add_module(module_name)
    services.application.update_user(me)


@when("I go to the course breakdown page")
def go_to_course_breakdown(dash_duo):
    dash_duo.multiple_click("#Course-breakdown-link", 1)
    wait_for_callbacks(dash_duo)


@when(parsers.parse("I put {module_name} in the new module input"))
def new_module_add_name(module_name, dash_duo):
    dash_duo.find_element("#new_module_name").send_keys(module_name)


@when(parsers.parse("I put {new_module_name} in the {existing_module_name} name input"))
def existing_module_add_name(dash_duo, new_module_name, existing_module_name):
    existing_index = services.application.get_user().get_module_names().index(existing_module_name)
    name_input = dash_duo.find_element(pattern_matching_selector(existing_index, "modules"))
    name_input.clear()
    name_input.send_keys(new_module_name)


@when("I press the add module button")
def click_add_module(dash_duo):
    dash_duo.find_element("#add_module").click()
    wait_for_callbacks(dash_duo)


@when(parsers.parse("I press the {existing_module_name} update button"))
def click_update_module(dash_duo, existing_module_name):
    existing_index = services.application.get_user().get_module_names().index(existing_module_name)
    dash_duo.find_element(pattern_matching_selector(existing_index, "update_module_name")).click()
    wait_for_callbacks(dash_duo)


@then(parsers.parse("{module_name} should be in my course"))
def module_in_course(module_name):
    assert module_name in services.application.get_user().get_module_names()


@then(parsers.parse("{module_name} should not be in my course"))
def module_not_in_course(module_name):
    assert module_name not in services.application.get_user().get_module_names()


@then(parsers.parse("{module_name} should exist only once in my course"))
def module_not_duplicated_in_course(module_name):
    assert services.application.get_user().get_module_names().count(module_name) == 1


@then("the duplicate module error should be shown")
def showing_duplicate_module_error(dash_duo):
    assert dash_duo.find_element("#new_module_name").get_attribute("invalid")
