import mysql.connector
import settings

class Database(object):

    def __init__(self):
        self.connection = self._create_db_connection()

    def _create_db_connection(self):
        """
        Method to create MySQL DB Connection
        settings.py contains the parameters required for setting up the connection
        """
        return mysql.connector.connect(
            user=settings.DB_USER, 
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT, 
            database=settings.DB_NAME)

    def fetch_budgets(self):
        """
        Method to fetch all the budgets where
        monthly expenditure is greater than or equals to 50%
        """

        cursor = self.connection.cursor()
        query = ('SELECT b.a_shop_id, b.a_budget_amount,'
        ' b.a_amount_spent, b.a_month, b.a_notify_status FROM t_budgets b,'
        ' t_shops s WHERE b.a_shop_id = s.a_id AND '
        'DATE_FORMAT(b.a_month, "%Y-%m")=DATE_FORMAT(CURRENT_DATE(), "%Y-%m") '
        'AND (b.a_budget_amount -b.a_amount_spent)/b.a_budget_amount <= 0.5'
        'AND s.a_online = 1')
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    
    def update_notify_status(self, shop_ids: list, status=1):
        """
        Method to update notification statuses to 1 or 0
        1 indicates notified and 0 is not notified
        """
        
        cursor = self.connection.cursor()
        values = '({0})'.format(', '.join(shop_ids))
        sql = ('UPDATE t_budgets SET a_notify_status = {0} WHERE '
        'DATE_FORMAT(a_month, "%Y-%m")=DATE_FORMAT(CURRENT_DATE(),'
        ' "%Y-%m") AND a_shop_id IN {1}').format(
            status, values
        )
        try:
            cursor.execute(sql)
            cursor.close()
            self.connection.commit() 
        except Exception as error:
            raise error

    def set_shop_offline(self, shop_ids: list, online=0):
        """
        Method to set shops in offline or online
        1 indicates online and 0 is offline
        """
        
        cursor = self.connection.cursor()
        values = '({0})'.format(', '.join(shop_ids))
        sql = 'UPDATE t_shops SET a_online = {0} WHERE a_id IN {1}'.format(
            online, values
        )
        try:
            cursor.execute(sql)
            cursor.close()
            self.connection.commit()
        except Exception as error:
            raise error

    def fetch_shop_with_budget_changes(self):
        """
        Method to fetch all shops with budget changes
        for the current month. This helps to update the notify 
        status to 0 or set shop to online again
        provided the consition of expedicture besing less than 50% is true
        """
        cursor = self.connection.cursor()
        query = ('SELECT b.a_shop_id, s.a_online FROM t_budgets b,'
        ' t_shops s WHERE b.a_shop_id = s.a_id AND '
        'DATE_FORMAT(b.a_month, "%Y-%m")=DATE_FORMAT(CURRENT_DATE(), "%Y-%m") '
        'AND (b.a_budget_amount -b.a_amount_spent)/b.a_budget_amount > 0.5'
        'AND b.a_notify_status = 1')
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

