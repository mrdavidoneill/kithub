Feature: Create Part
    In order to prove that Parts can be:
    created, read, updated, and deleted

    Background:
        Given a set of specific parts
            | name      | description   | quantity |
            | partA     | descriptionA  | 10       |
            | partB     | descriptionB  | 0        |
            | partC     | descriptionC  | 0        |   
        And I read all "part"
    
    Scenario: Part create without quantity
        When I create a "part" called "partD"
        Then I should see the "name" is "partD"
        And I should see the "quantity" is number "0"
    
    Scenario: Parts read
        When I read all "part"
        Then the first part should have "name" equal to "partA"
        And the first part should have "quantity" equal to number "10"
        But the last part should have "name" equal to "partC"
        And the last part should have "quantity" equal to number "0"

    Scenario: Single part read
        When I read the first "part"
        Then I should see the "name" is "partA"
        And I should see the "quantity" is number "10"

    Scenario: Single part update
        When I update the first part as follows
            | name      | description   | quantity |
            | partE     | descriptionE  | 9        |
         
        Then I should see the "name" is "partE"
        And I should see the "quantity" is number "9"        
        And I should see the "description" is "descriptionE"  

    Scenario: Single part delete
        When I delete the first "part"
        Then the status code should be "204"
        When I read all "part"
        Then the first part should have "name" equal to "partB"      