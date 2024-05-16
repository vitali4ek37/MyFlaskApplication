Feature: Application stores users properly

    Scenario: New users can be created successfully
        Given a Create User request
        When request is sent
        Then new user appears in the database
        And can be obtained by API
