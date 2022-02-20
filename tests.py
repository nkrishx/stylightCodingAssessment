import unittest
from unittest import mock
from database import Database
from main import check_shops_budgets, check_and_update_shops_notify_status


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        

    def test_fetch_budgets(self):
        # Test method to fetch all the budgets where
        # monthly expenditure is greater than 50%
        result = self.database.fetch_budgets()
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 5)

    def test_set_shop_offline(self):
        # Test method to set shops in offline
        # This will not update any record int the a_shops table as
        # we don't have no record for shop ids 10 and 11 
        # Just to test if the update query to database works
        result = self.database.set_shop_offline(shop_ids=['10', '11'])
        self.assertEqual(result, None)

    def test_update_notify_status(self):
        # Test method to update notification statuses to 1
        # This will not update any record int the a_shops table as
        # we don't have no record for shop ids 10 and 11 
        # Just to test if the update query to database works
        result = self.database.set_shop_offline(shop_ids=['10', '11'])
        # Excpeted result is None
        self.assertEqual(result, None)

    def test_fetch_shop_with_budget_changes(self):
        # Test method to fetch all shops with budget changes
        # for the current month. This helps to update the notify 
        # status to 0  or set shop to online again provided the consition of expedicture besing less than 50% is true
        # in given dataset no such results are available.
        result = self.database.fetch_shop_with_budget_changes()
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 0)

class TestMainService(unittest.TestCase):

    def test_check_shops_budgets(self):
        # Test method to checks all shops' budgets and 
        # expenditures for the current month.
         with mock.patch('main.Database') as database:
             result = check_shops_budgets()
            
             # check if fetch_budgets method is called
             database().fetch_budgets.assert_called()

             # if check_shops_budgets is call successful then 
             # result should be None
             self.assertEqual(result, None)

    def test_check_and_update_shops_notify_status(self):
        # Test method to fetch all shops with budget changes
        # for the current month. This helps to update the notify 
        # status to 0 or set shop to online again provided the consition of expedicture besing less than 50% is true
         with mock.patch('main.Database') as database:
             result = check_and_update_shops_notify_status()
            
             # check if fetch_shop_with_budget_changes
             #  method is called
             database().fetch_shop_with_budget_changes.assert_called()

             # if check_shops_budgets is call successful then 
             # result should be None
             self.assertEqual(result, None)

if __name__ == "__main__":
    unittest.main()
