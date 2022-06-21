@acceptance
Feature: Kit packer
    Acceptance tests for kit packer

Background:
        Given a set of specific parts
            | name      | description   | quantity |
            | partA     | descriptionA  | 12       |
            | partB     | descriptionB  | 8        |
            | partC     | descriptionC  | 1        |   
            | partD     | descriptionC  | 4        |   
        Given a bag type "bagtype1" with parts list of
            | name  | part      | quantity |
            | A     | partA     | 1        |
            | B     | partB     | 2        |
            | C     | partC     | 1        |
        Given a bag type "bagtype2" with parts list of
            | name  | part      | quantity |
            | A     | partB     | 2        |
            | B     | partC     | 3        |  
        Given a bag type "bagtype3" with parts list of
            | name  | part      | quantity |
            | A     | partC     | 1        |                                    
        Given a set of specific bags
            | name  | kind      | quantity | complete   |
            | AB    | bagtype1  | 5        |            |            
            | ABC   | bagtype1  | 10       | X          |
            |       | bagtype2  | 10       |            |               
            | AB    | bagtype2  | 11       | X          |     
        Given a kit type "kittype1" with bags list of
            | name  | bagtype   | quantity |
            | A     | bagtype1  | 1        |
            | B     | bagtype2  | 1        | 
        Given a kit type "kittype2" with bags list of
            | name  | bagtype   | quantity |
            | A     | bagtype1  | 1        |
            | B     | bagtype2  | 2        |             
            | C     | bagtype3  | 3        |  
        Given a set of specific kits
            | name  | kind      | quantity | complete   |
            | A     | kittype1  | 10       |            |            
            | ABC   | kittype2  | 11       | X          |           
    Scenario: US9: As a kit packer, I want to see a bag inventory, so that I know how many bags are currently ready.
        When I read all "bag"
        Then the first item should have "name" equal to "AB"
        And the first item should have "quantity" equal to number "5"
        But the last item should have "name" equal to "AB"
        And the last item should have "quantity" equal to number "11"

    Scenario: US10: As a kit packer, I want to update a bag inventory, so that I can pack bags and prepare
        When I read all "bag"
        When I update the first bag as follows
            | name  | kind      | quantity | complete   |
            | ABC   | bagtype1  | 20       | X          |
        And I read all "bag"
        Then the first item should have "name" equal to "ABC"
        And the first item should have "quantity" equal to number "20"  

        When I create "12" "bag" of "bagtype2" "bagtype" with name "A"
        And I read all "bag"
        Then the last item should have "name" equal to "A"
        And the last item should have "quantity" equal to number "12"          

        When I read all "bag"
        When I delete the first "bag"
        And I read all "bag"
        Then the first item should have "name" equal to "ABC" 
        And the first item should have "quantity" equal to number "10"   

    Scenario: US11: As a kit packer, I want to see a list of unfinished bags, so that I know which parts are missing from bags that have been started.
        When I request unfinished bags
        Then "bagtype2" "bagtype" should need to buy "12" "partB" 
        And "bagtype2" "bagtype" should need to buy "29" "partC" 

    Scenario: US12: As a kit packer, I want to divide bags, so that when I find I am low on parts to complete all the bags, I can complete some, keeping track of everything along the way.
        When I read all "bag"
        And I divide off "2" of the first bag  
        Then the first item should have "quantity" equal to number "3"         
        And the last item should have "quantity" equal to number "2"
        When I read all "bag"
        Then the first item should have "name" equal to "AB" 
        And the first item should have "quantity" equal to number "3"         
        And the last item should have "quantity" equal to number "2"                 

    Scenario: US13: As a kit packer, I want to divide kits, so that when I find I am low on bags to complete all the kits, I can complete some, keeping track of everything along the way.
        When I read all "kit"
        And I divide off "4" of the first kit  
        Then the first item should have "quantity" equal to number "6"         
        And the last item should have "quantity" equal to number "4"
        When I read all "kit"
        Then the first item should have "name" equal to "A" 
        And the first item should have "quantity" equal to number "6"         
        And the last item should have "quantity" equal to number "4"                 

    Scenario: US14: As a kit packer, I want to see how many bags are possible, so that I do not get delayed by missing parts half-way through.
        When I request potential bags of "bagtype1"
        Then I should see the "potential_bags" is number "1"

    Scenario: US15: As a kit packer, I want to see a list of parts that a bag needs, so that I fill the bag correctly.
        When I request the ingredients of bagtype "bagtype1"
        Then I should see "A" is "1" of part "partA"
        Then I should see "B" is "2" of part "partB"
        Then I should see "C" is "1" of part "partC"