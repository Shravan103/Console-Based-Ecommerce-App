from config.database import get_connection
from model.cart import Cart
from model.cart_item import CartItem


class CartDAO:

    def get_cart_by_user(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT cart_id, user_id
                FROM carts
                WHERE user_id = %s
                """,
                (user_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Cart(
                cart_id=row[0],
                user_id=row[1]
            )

        finally:
            cursor.close()
            connection.close()

    def create_cart(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO carts (user_id)
                VALUES (%s)
                """,
                (user_id,)
            )

            connection.commit()

            return Cart(
                cart_id=cursor.lastrowid,
                user_id=user_id
            )

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def add_to_cart(self, cart_item):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO cart_items
                (cart_id, product_id, quantity)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                quantity = quantity + %s
                """,
                (
                    cart_item.cart_id,
                    cart_item.product_id,
                    cart_item.quantity,
                    cart_item.quantity
                )
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def remove_from_cart(self, cart_id, product_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM cart_items
                WHERE cart_id = %s
                  AND product_id = %s
                """,
                (cart_id, product_id)
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "Product is not in the cart."
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def get_cart_items(self, cart_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT cart_item_id,
                       cart_id,
                       product_id,
                       quantity
                FROM cart_items
                WHERE cart_id = %s
                """,
                (cart_id,)
            )

            rows = cursor.fetchall()

            return [
                CartItem(
                    cart_item_id=row[0],
                    cart_id=row[1],
                    product_id=row[2],
                    quantity=row[3]
                )
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

    def clear_cart(self, cart_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM cart_items
                WHERE cart_id = %s
                """,
                (cart_id,)
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def clear_cart_with_connection(self, connection, cart_id):
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM cart_items
                WHERE cart_id = %s
                """,
                (cart_id,)
            )

        finally:
            cursor.close()
