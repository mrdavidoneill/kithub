@system
Feature: Kit
    In order to prove that Kits can be:
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
        Given a bag type "bagtype2" with parts list of
            | name  | part      | quantity |
            | A     | partA     | 1        |
            | B     | partB     | 2        |
            | C     | partC     | 3        |                          
        Given a set of specific bags
            | name  | kind      | quantity | complete   |
            | AB    | bagtype1  | 10       | X          |
            | AB    | bagtype2  | 10       | X          |     
        Given a kit type "kittype1" with bags list of
            | name  | bagtype   | quantity |
            | A     | bagtype1  | 1        |
            | B     | bagtype2  | 2        |
        Given a set of specific kits
            | name  | kind      | quantity | complete   |
            | A     | kittype1  | 10       |            |            
            | AB    | kittype1  | 10       | X          |

    Scenario: Kit create with 100 quantity
        When I create "100" "kit" of "kittype1" "kittype"
        Then I should see the "quantity" is number "100"
        And I should see the "complete" is boolean "False"
    
    Scenario: Kits read
        When I read all "kit"
        Then the first item should have "name" equal to "A"
        And the first item should have "quantity" equal to number "10"
        But the last item should have "name" equal to "AB"
        And the last item should have "quantity" equal to number "10"

    Scenario: Single kit read
        When I read the first "kit"
        Then I should see the "name" is "A"
        And I should see the "quantity" is number "10"
        And I should see the "complete" is boolean "False"

    Scenario: Single kit update
        When I update the first kit as follows
            | name  | kind      | quantity | complete   |
            | AB    | kittype1  | 100      | X          |
         
        Then I should see the "name" is "AB"
        And I should see the "quantity" is number "100"        
        And I should see the "complete" is boolean "True"
        When I read all "kit"
        Then the first item should have "name" equal to "AB"
        And the first item should have "quantity" equal to number "100"  


    Scenario: Single kit delete
        When I delete the first "kit"
        Then the status code should be "204"
        When I read all "kit"
        Then the first item should have "name" equal to "AB"      