@system
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
    
    Scenario: UC1 Part create without quantity
        When I create a "part" called "partD"
        Then I should see the "name" is "partD"
        And I should see the "quantity" is number "0"

    Scenario: UC1 Part create with quantity
        When I create a "part" called "partD" with quantity "3"
        Then I should see the "name" is "partD"
        And I should see the "quantity" is number "3"

    Scenario: UC1 Part create with quantity and description
        When I create a "part" called "partD" with quantity "3" and description "partD description"
        Then I should see the "name" is "partD"
        And I should see the "quantity" is number "3"

    Scenario: UC2 Parts read
        When I read all "part"
        Then the first item should have "name" equal to "partA"
        And the first item should have "quantity" equal to number "10"
        But the last item should have "name" equal to "partC"
        And the last item should have "quantity" equal to number "0"

    Scenario: UC2 Single part read
        When I read the first "part"
        Then I should see the "name" is "partA"
        And I should see the "quantity" is number "10"

    Scenario: UC3 Single part update
        When I update the first part as follows
            | name      | description   | quantity |
            | partE     | descriptionE  | 9        |
         
        Then I should see the "name" is "partE"
        And I should see the "quantity" is number "9"        
        And I should see the "description" is "descriptionE"
        When I read all "part"
        Then the first item should have "name" equal to "partE"
        And the first item should have "quantity" equal to number "9"  
        And the first item should have "description" equal to "descriptionE"  

    Scenario: UC4 Single part delete
        When I delete the first "part"
        Then the status code should be "204"
        When I read all "part"
        Then the first item should have "name" equal to "partB"      