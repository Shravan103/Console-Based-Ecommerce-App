from service.order_service import OrderService
from exceptions.empty_cart_exception import EmptyCartException
from exceptions.insufficient_stock_exception import InsufficientStockException


class OrderController:

    def __init__(self):
        self.order_service = OrderService()

    def place_order(self, user_id):
        print("\n========== PLACE ORDER ==========")

        try:
            order = self.order_service.place_order(user_id)

            print("\nOrder placed successfully!")
            print("Order ID:", order.order_id)
            print(
                f"Total Amount: ₹{order.total_amount:.2f}"
            )

        except (
            EmptyCartException,
            InsufficientStockException,
            ValueError
        ) as e:
            print("\nFailed to place order:", e)

    def order_history(self, user_id):
        print("\n========== ORDER HISTORY ==========")

        orders = self.order_service.get_order_history(user_id)

        if not orders:
            print("No orders found.")
            return

        print(
            f"{'Order ID':<12}"
            f"{'Date':<25}"
            f"{'Total':<15}"
        )
        print("-" * 52)

        for order in orders:
            print(
                f"{order.order_id:<12}"
                f"{str(order.order_date):<25}"
                f"₹{order.total_amount:<14.2f}"
            )
