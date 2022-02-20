from database import Database
from models import Budget


def check_shops_budgets():
    """"
    Method to checks all shops' budgets and 
    expenditures for the current month and notify shop.
    """

    # Create MySQL DB connection
    database = Database()
    try:
        data = database.fetch_budgets()
        shop_ids_to_offline = []
        shop_ids_to_update_notify_status = []
        for item in data:
            budget = Budget(shop_id=str(item[0]),
                budget_amount=item[1], 
                amount_spent=item[2],
                month=str(item[3]),
                notify_status=item[4])
            if (budget.budget_percentage >= 100):
                # case they reach 100% of the current 
                # month's budget.
                shop_ids_to_offline.append(budget.shop_id)
                
                if budget.notify_status == 0:
                    shop_ids_to_update_notify_status.append(budget.shop_id)
                
                # Notify shop
                budget.notify_shop()
            else:
                # case they reach 50% of the current 
                # month's budget.
                if budget.notify_status == 0:
                    shop_ids_to_update_notify_status.append(budget.shop_id)
                    # Notify shop
                    budget.notify_shop()

        if shop_ids_to_offline:
            database.set_shop_offline(
                shop_ids=shop_ids_to_offline)
        if shop_ids_to_update_notify_status:
            database.update_notify_status(
                shop_ids=shop_ids_to_update_notify_status)
    except Exception as error:
        raise error
    
    
def check_and_update_shops_notify_status():
    """"
    Method to fetch all shops with budget changes
    for the current month. This helps to update the notify 
    status to 0 or set shop to online again
    """

    # Create MySQL DB connection
    database = Database()
    try:
        data = database.fetch_shop_with_budget_changes()
        shop_ids_to_online = []
        shop_ids_to_update_notify_status = []
        for item in data:
            shop_id=str(item[0])
            online_status = item[1]
            shop_ids_to_update_notify_status.append(shop_id)
            if online_status == 0:
                shop_ids_to_online.append(shop_id)

        if shop_ids_to_update_notify_status:
            database.update_notify_status(shop_ids=shop_ids_to_update_notify_status,
            status=0)
        if shop_ids_to_online:
            database.set_shop_offline(shop_ids=shop_ids_to_online, online=1)
    except Exception as error:
        raise error
    
if __name__ == "__main__":
    # Method to checks all shops' budgets and 
    # expenditures for the current month and notify shop.
    check_shops_budgets()

    # call to fetch all shops with budget changes
    # for the current month. This helps to update the notify 
    # status to 0 or set shop to online again provided the consition of expedicture besing less than 50% is true
    check_and_update_shops_notify_status()
