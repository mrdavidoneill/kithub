Feature: Create Part
    In order to prove that Parts can be:
    created, read, updated, and deleted

    Background:
        Given a set of specific parts
            | name      | description   | quantity |
            | partA     | descriptionA  | 10       |
            | partB     | descriptionB  | 0        |
            | partC     | descriptionC  | 0        |   
    
    Scenario: Part create without quantity
        When I create a "part" called "partD"
        Then I should see the "name" is "partD"
        And I should see the "quantity" is number "0"
    
    Scenario: Parts read
        When I read all "part"
        Then the first part should have "name" equal to "partA"
        And the first part should have "quantity" equal to number "10"
