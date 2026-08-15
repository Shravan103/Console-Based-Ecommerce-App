from dao.order_dao import OrderDAO
from dao.cart_dao import CartDAO
from dao.product_dao import ProductDAO
from config.database import get_connection

from model.order import Order
from model.order_item import OrderItem

from utils.logger import AppLogger
from exceptions.empty_cart_exception import EmptyCartException
from exceptions.insufficient_stock_exception import InsufficientStockException


class OrderService:

    def __init__(self):
        self.order_dao = OrderDAO()
        self.cart_dao = CartDAO()
        self.product_dao = ProductDAO()
        self.logger = AppLogger.get_logger()

    def place_order(self, user_id):
        connection = None

        try:
            connection = get_connection()

            cart = self.cart_dao.get_cart_by_user(user_id)

            if cart is None:
                raise EmptyCartException(
                    "Cart is empty."
                )

            cart_items = self.cart_dao.get_cart_items(
                cart.cart_id
            )

            if not cart_items:
                raise EmptyCartException(
                    "Cart is empty."
                )

            total_amount = 0
            products = []

            for item in cart_items:
                product = self.product_dao.get_product_by_id(
                    item.product_id
                )

                if product is None:
                    raise ValueError(
                        f"Product {item.product_id} not found."
                    )

                if item.quantity <= 0:
                    raise ValueError(
                        "Product quantity must be greater than zero."
                    )

                if item.quantity > product.stock:
                    raise InsufficientStockException(
                        f"Insufficient stock for {product.name}. "
                        f"Available stock: {product.stock}."
                    )

                total_amount += product.price * item.quantity
                products.append((item, product))

            order = Order(
                user_id=user_id,
                total_amount=total_amount
            )

            self.order_dao.create_order_with_connection(
                connection,
                order
            )

            for item, product in products:
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    quantity=item.quantity,
                    price=product.price
                )

                self.order_dao.add_order_item_with_connection(
                    connection,
                    order_item
                )

                self.product_dao.update_stock(
                    connection,
                    product.product_id,
                    item.quantity
                )

            self.cart_dao.clear_cart_with_connection(
                connection,
                cart.cart_id
            )

            connection.commit()

            self.logger.info(
                f"Order placed successfully: "
                f"order_id={order.order_id}, "
                f"user_id={user_id}, "
                f"total_amount={order.total_amount}"
            )

            return order

        except Exception as e:
            if connection is not None:
                connection.rollback()

            self.logger.error(
                f"Order failed: user_id={user_id}, reason={e}"
            )

            raise

        finally:
            if connection is not None:
                connection.close()

    def get_order_history(self, user_id):
        return self.order_dao.get_orders_by_user(user_id)

    def get_order_items(self, order_id):
        return self.order_dao.get_order_items(order_id)
