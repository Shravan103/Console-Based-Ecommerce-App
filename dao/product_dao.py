from config.database import get_connection
from model.product import Product
from exceptions.insufficient_stock_exception import InsufficientStockException


class ProductDAO:

    def add_product(self, product):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO products
                (name, description, price, stock)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    product.name,
                    product.description,
                    product.price,
                    product.stock
                )
            )

            connection.commit()
            product.product_id = cursor.lastrowid

            return product

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def get_all_products(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT product_id, name, description, price, stock
                FROM products
                ORDER BY product_id
                """
            )

            rows = cursor.fetchall()

            return [
                Product(
                    product_id=row[0],
                    name=row[1],
                    description=row[2],
                    price=row[3],
                    stock=row[4]
                )
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

    def get_product_by_id(self, product_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT product_id, name, description, price, stock
                FROM products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Product(
                product_id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                stock=row[4]
            )

        finally:
            cursor.close()
            connection.close()

    def update_product(self, product):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE products
                SET name = %s,
                    description = %s,
                    price = %s,
                    stock = %s
                WHERE product_id = %s
                """,
                (
                    product.name,
                    product.description,
                    product.price,
                    product.stock,
                    product.product_id
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Product not found.")

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def delete_product(self, product_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            if cursor.rowcount == 0:
                raise ValueError("Product not found.")

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def update_stock(self, connection, product_id, quantity):
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE products
                SET stock = stock - %s
                WHERE product_id = %s
                  AND stock >= %s
                """,
                (quantity, product_id, quantity)
            )

            if cursor.rowcount == 0:
                raise InsufficientStockException(
                    "Insufficient stock."
                )

        finally:
            cursor.close()
