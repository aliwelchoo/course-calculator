Feature: Course breakdown
    A site where you can detail the module and credit breakdown of your course.

    Background:
        Given the site is running without error
        And I am test_user

    Scenario: Adding a new module
        When I go to the course breakdown page
        And I put new_module_name in the new module input
        And I press the add module button
        Then new_module_name should be in my course

    Scenario: Adding an existing module
        Given I have existing_module_name module in my course breakdown
        When I go to the course breakdown page
        And I put an existing_module_name in the new module input
        And I press the add module button
        Then existing_module_name should not be in my course
        And the duplicate module error should be shown

    Scenario: Updating an existing module
        Given I have existing_module_name in my course breakdown
        When I go to the course breakdown page
        And I put new_module_name in the existing_module_name name input
        Then existing_module_name should not be in my course
        And new_module_name should be in my course
