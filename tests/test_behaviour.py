from pytest_bdd import scenarios, given, when, then

scenarios("features")


@given("I'm an author user")
def author_user():
    pass


@given("I have an article")
def article():
    pass


@when("I go to the course breakdown page")
def go_to_course_breakdown():
    pass


@when("I put a new module name in the new module input")
def new_module_add_name():
    pass


@then("I should not see the error message")
def no_error_message():
    pass


@then("the article should be published")
def article_is_published():
    assert True
