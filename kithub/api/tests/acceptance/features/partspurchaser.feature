@acceptance
Feature: Parts Purchaser
    Acceptance tests for parts purchaser

Background:
        Given a set of specific parts
            | name      | description   | quantity |
            | partA     | descriptionA  | 10       |
            | partB     | descriptionB  | 0        |
            | partC     | descriptionC  | 0        |   
    
    Scenario: US1: As a parts purchaser, I want to see a parts inventory, so that I can see how many parts I have stocked.
        When I read all "part"
        Then the first item should have "name" equal to "partA"
        And the first item should have "quantity" equal to number "10"
        But the last item should have "name" equal to "partC"
        And the last item should have "quantity" equal to number "0"

    Scenario: US2: As a parts purchaser, I want to update a parts inventory, so that I can add and remove parts.
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


    # Scenario: US3: As a parts purchaser, I want to see which parts to buy to do a specified number of kits, so that I do not understock nor overstock.
    #     When I create a "part" called "partD"
    #     Then I should see the "name" is "partD"
    #     And I should see the "quantity" is number "0"
    
    # Scenario: Parts read

    # Scenario: Single part read
    #     When I read the first "part"
    #     Then I should see the "name" is "partA"
    #     And I should see the "quantity" is number "10"

    # Scenario: Single part update
    #     When I update the first part as follows
    #         | name      | description   | quantity |
    #         | partE     | descriptionE  | 9        |
         
    #     Then I should see the "name" is "partE"
    #     And I should see the "quantity" is number "9"        
    #     And I should see the "description" is "descriptionE"
    #     When I read all "part"
    #     Then the first item should have "name" equal to "partE"
    #     And the first item should have "quantity" equal to number "9"  
    #     And the first item should have "description" equal to "descriptionE"  


    # Scenario: Single part delete
    #     When I delete the first "part"
    #     Then the status code should be "204"
    #     When I read all "part"
    #     Then the first item should have "name" equal to "partB"      


    