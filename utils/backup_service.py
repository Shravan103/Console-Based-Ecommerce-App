from config.database import get_connection
from utils.file_handler import FileHandler


class BackupService:

    def backup_users(self):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT user_id, name, email, role
                FROM users
                """
            )

            users = cursor.fetchall()

            FileHandler.write_json(
                "backup/users.json",
                users
            )

        finally:
            cursor.close()
            connection.close()

    def backup_products(self):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT product_id,
                       name,
                       description,
                       price,
                       stock
                FROM products
                """
            )

            products = cursor.fetchall()

            FileHandler.write_json(
                "backup/products.json",
                products
            )

        finally:
            cursor.close()
            connection.close()

    def backup_orders(self):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT order_id,
                       user_id,
                       order_date,
                       total_amount
                FROM orders
                """
            )

            orders = cursor.fetchall()

            FileHandler.write_json(
                "backup/orders.json",
                orders
            )

        finally:
            cursor.close()
            connection.close()

    def backup_all(self):
        self.backup_users()
        self.backup_products()
        self.backup_orders()
