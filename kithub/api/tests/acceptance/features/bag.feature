@system
Feature: Bag
    In order to prove that Bags can be:
    created, read, updated, and deleted

    Background:
        Given a set of specific parts
            | name      | description   | quantity |
            | partA     | descriptionA  | 10       |
            | partB     | descriptionB  | 0        |
            | partC     | descriptionC  | 0        |   
        Given a bag type "bagtype1" with parts list of
            | name  | part      | quantity |
            | A     | partA     | 1        |
            | B     | partB     | 2        |
            | C     | partC     | 3        |              
        Given a set of specific bags
            | name  | kind      | quantity | complete   |
            | A     | bagtype1  | 1        |            |
            | B     | bagtype1  | 2        |            |
            | C     | bagtype1  | 3        |            |  

    Scenario: Bag create with 100 quantity
        When I create "100" "bag" of "bagtype1" "bagtype"
        Then I should see the "quantity" is number "100"
    
    Scenario: Bags read
        When I read all "bag"
        Then the first item should have "name" equal to "A"
        And the first item should have "quantity" equal to number "1"
        But the last item should have "name" equal to "C"
        And the last item should have "quantity" equal to number "3"

    Scenario: Single bag read
        When I read the first "bag"
        Then I should see the "name" is "A"
        And I should see the "quantity" is number "1"

    Scenario: Single part update
        When I update the first bag as follows
            | name  | kind      | quantity | complete   |
            | AB    | bagtype1  | 10       | X          |
         
        Then I should see the "name" is "AB"
        And I should see the "quantity" is number "10"        
        # And I should see the "complete" is boolean "True"
        When I read all "bag"
        Then the first item should have "name" equal to "AB"
        And the first item should have "quantity" equal to number "10"  
        # And the first item should have "description" equal to "descriptionE"  


    Scenario: Single bag delete
        When I delete the first "bag"
        Then the status code should be "204"
        When I read all "bag"
        Then the first item should have "name" equal to "B"      