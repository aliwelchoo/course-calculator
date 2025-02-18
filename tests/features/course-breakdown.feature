Feature: Course breakdown
    A site where you can detail the module and credit breakdown of your course.

    Scenario: Creating a new module
        When I go to the course breakdown page
        And I put a new module name in the new module input
        And I press the add module button
        Then the module should be added to my course

    Scenario: Creating an existing module
        Given I have modules in my course breakdown
        When I go to the course breakdown page
        And I put an existing module name in the new module input
        And I press the add module button
        Then the module should not be added to my course
        And the duplicate module error should be shown

    Scenario: Updating an existing module
        Given I have "existing_module" in my course breakdown
        When I go to the course breakdown page
        And I put "new_module" in the "existing_module" name input
        Then "new_module" should replace "existing_module" in my course breakdown
