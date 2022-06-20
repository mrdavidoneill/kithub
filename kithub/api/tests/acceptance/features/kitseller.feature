@acceptance
Feature: Kit seller
    Acceptance tests for kit seller

Background:
        Given a set of specific parts
            | name      | description   | quantity |
            | partA     | descriptionA  | 12       |
            | partB     | descriptionB  | 8        |
            | partC     | descriptionC  | 5        |   
        Given a bag type "bagtype1" with parts list of
            | name  | part      | quantity |
            | A     | partA     | 1        |
            | B     | partB     | 2        |
        Given a bag type "bagtype2" with parts list of
            | name  | part      | quantity |
            | A     | partB     | 2        |
            | B     | partC     | 3        |  
        Given a bag type "bagtype3" with parts list of
            | name  | part      | quantity |
            | A     | partC     | 1        |                                    
        Given a set of specific bags
            | name  | kind      | quantity | complete   |
            | AB    | bagtype1  | 10       | X          |
            | AB    | bagtype2  | 10       | X          |     
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
    Scenario: US4: As a kit seller, I want to see a kits inventory, so that I know how many kits I can currently supply to clients.
        When I read all "kit"
        Then the first item should have "name" equal to "A"
        And the first item should have "quantity" equal to number "10"
        But the last item should have "name" equal to "ABC"
        And the last item should have "quantity" equal to number "11"

    Scenario: US5: As a kit seller, I want to update the kits inventory, so that I can prepare and sell kits.
        When I read all "kit"
        When I update the first kit as follows
            | name  | kind      | quantity | complete   |
            | AB    | kittype1  | 20       | X          |
        And I read all "kit"
        Then the first item should have "name" equal to "AB"
        And the first item should have "quantity" equal to number "20"  

        When I create "10" "kit" of "kittype2" "kittype" with name "AB"
        And I read all "kit"
        Then the last item should have "name" equal to "AB"
        And the last item should have "quantity" equal to number "10"          

        When I read all "kit"
        When I delete the first "kit"
        And I read all "kit"
        Then the first item should have "name" equal to "ABC"   

    Scenario: US6: As a kit seller, I want to see how many kits are possible with the currently stocked parts, so that I know how many kits I could potentially sell to clients.
        When I request potential kits of "kittype1"
        Then I should see the "potential_kits" is number "10"

    Scenario: US7: As a kit seller, I want to add a kit, so that I can manage new kits that I start selling.
        When I create a kit type "kittype4" with bags list of
            | name  | bagtype   | quantity |
            | A     | bagtype1  | 1        |
            | B     | bagtype2  | 1        |         
        
        And I read all "kittype"
        Then the last item should have "kind" equal to "kittype4"

    Scenario: US8: As a kit seller, I want to remove a kit, so that I can manage old kits that I no longer sell.
        When I read all "kittype"
        When I delete the first "kittype"
        And I read all "kittype"
        Then the first item should have "kind" equal to "kittype2"   
