@acceptance
Feature: Parts Purchaser
    Acceptance tests for parts purchaser

Background:
        Given a set of specific parts
            | name      | description   | quantity |
            | partA     | descriptionA  | 10       |
            | partB     | descriptionB  | 0        |
            | partC     | descriptionC  | 0        |   
        Given a set of specific purchases
            | date      | shop   | shop_part_no | price | quantity | part  |
            | 2020-11-01| RS     | RS001        | 0.99  | 100      | partA |
            | 2021-02-02| CPC    | C002         | 0.09  | 101      | partA |
            | 2022-03-13| Farnell| F000003      | 0.009 | 1        | partA |
             
        Given a bag type "bagtype1" with parts list of
            | name  | part      | quantity |
            | A     | partA     | 1        |
            | B     | partB     | 2        |
        Given a bag type "bagtype2" with parts list of
            | name  | part      | quantity |
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
    Scenario: US1: As a parts purchaser, I want to see a parts inventory, so that I can see how many parts I have stocked.
        When I read all "part"
        Then the first item should have "name" equal to "partA"
        And the first item should have "quantity" equal to number "10"
        But the last item should have "name" equal to "partC"
        And the last item should have "quantity" equal to number "0"

    Scenario: US2: As a parts purchaser, I want to update a parts inventory, so that I can add and remove parts.
        When I read all "part"
        When I update the first part as follows
            | name      | description   | quantity |
            | partE     | descriptionE  | 9        |
        And I read all "part"
        Then the first item should have "name" equal to "partE"
        And the first item should have "quantity" equal to number "9"  

        When I create a "part" called "partD"
        And I read all "part"
        Then the last item should have "name" equal to "partD"
        And the last item should have "quantity" equal to number "0"          

        When I delete the first "part"
        And I read all "part"
        Then the first item should have "name" equal to "partB"   

    Scenario: US3: As a parts purchaser, I want to see which parts to buy to do a specified number of kits, so that I do not understock nor overstock.
        When I request a partlist for "100" of "kittype1"
        Then the parts list should contain "partA" with quantity "90"
        And the parts list should contain "partB" with quantity "600"
        And the parts list should contain "partC" with quantity "600"

    Scenario: US16: As a parts purchaser, I want to see where a part has been bought previously and its part number, so that I can easily restock.
        When I read "part" with "name" "partA"
        Then the first purchase should have "shop" equal to "RS"
        And the first purchase should have "shop_part_no" equal to "RS001"   
        But the last purchase should have "shop" equal to "Farnell"
        And the last purchase should have "shop_part_no" equal to "F000003"    

    Scenario: US17: As a parts purchaser, I want to see past prices paid for a part, so that I can see how a part price has changed over time.
        When I read "part" with "name" "partA"
        Then the first purchase should have "date" equal to "2020-11-01"
        And the first purchase should have "price" equal to "0.99"   
        But the last purchase should have "date" equal to "2022-03-13"
        And the last purchase should have "price" equal to "0.009"          