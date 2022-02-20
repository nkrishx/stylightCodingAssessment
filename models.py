from datetime import date

class Budget(object):

    def __init__(self, shop_id: int, budget_amount: float,
        amount_spent: float, month: str, notify_status: int):
        self.shop_id = shop_id
        self.budget_amount = budget_amount
        self.amount_spent = amount_spent
        self.month = month
        self.notify_status = notify_status

    @property
    def budget_percentage(self):
        """
        Return expenditure budget in Percentage
        """
        return round((1 -((self.budget_amount - 
            self.amount_spent)/self.budget_amount))*100, 2)

    def notify_shop(self):
        """
        Method to notify shop
        """
        today = date.today()
        message = ('*[{shop_id}]*'
                   ' Your monthly expenditure reaches certain thresholds\n'
                   ' - Shop ID: {shop_id}\n'
                   ' - Current Date: {current_date}\n'
                   ' - Current Month\'s Budget: {budget_amount}\n'
                   ' - Current Month\'s Expenditure: {amount_spent}\n'
                   ' - Current Month\'s Expenditure budget\'s Percentage: {budget_percentage}%\n').format(
            shop_id=self.shop_id,
            current_date=str(today),
            budget_amount=self.budget_amount,
            amount_spent=self.amount_spent,
            budget_percentage=self.budget_percentage
        )
        
        print(message)
