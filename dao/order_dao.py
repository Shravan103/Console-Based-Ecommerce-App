from config.database import get_connection
from model.order import Order
from model.order_item import OrderItem


class OrderDAO:

    def create_order(self, order):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO orders
                (user_id, total_amount)
                VALUES (%s, %s)
                """,
                (
                    order.user_id,
                    order.total_amount
                )
            )

            connection.commit()
            order.order_id = cursor.lastrowid

            return order

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def add_order_item(self, order_item):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO order_items
                (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    order_item.order_id,
                    order_item.product_id,
                    order_item.quantity,
                    order_item.price
                )
            )

            connection.commit()
            order_item.order_item_id = cursor.lastrowid

            return order_item

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def create_order_with_connection(self, connection, order):
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO orders
                (user_id, total_amount)
                VALUES (%s, %s)
                """,
                (
                    order.user_id,
                    order.total_amount
                )
            )

            order.order_id = cursor.lastrowid
            return order

        finally:
            cursor.close()

    def add_order_item_with_connection(self, connection, order_item):
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO order_items
                (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    order_item.order_id,
                    order_item.product_id,
                    order_item.quantity,
                    order_item.price
                )
            )

            order_item.order_item_id = cursor.lastrowid
            return order_item

        finally:
            cursor.close()

    def get_orders_by_user(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT order_id,
                       user_id,
                       order_date,
                       total_amount
                FROM orders
                WHERE user_id = %s
                ORDER BY order_date DESC
                """,
                (user_id,)
            )

            rows = cursor.fetchall()

            return [
                Order(
                    order_id=row[0],
                    user_id=row[1],
                    order_date=row[2],
                    total_amount=row[3]
                )
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

    def get_order_items(self, order_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT order_item_id,
                       order_id,
                       product_id,
                       quantity,
                       price
                FROM order_items
                WHERE order_id = %s
                """,
                (order_id,)
            )

            rows = cursor.fetchall()

            return [
                OrderItem(
                    order_item_id=row[0],
                    order_id=row[1],
                    product_id=row[2],
                    quantity=row[3],
                    price=row[4]
                )
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()
