from service.cart_service import CartService
from service.product_service import ProductService
from exceptions.insufficient_stock_exception import InsufficientStockException
from exceptions.empty_cart_exception import EmptyCartException


class CartController:

    def __init__(self):
        self.cart_service = CartService()
        self.product_service = ProductService()

    def add_to_cart(self, user_id):
        print("\n========== ADD TO CART ==========")

        try:
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity: "))

            self.cart_service.add_to_cart(
                user_id,
                product_id,
                quantity
            )

            print("\nProduct added to cart successfully!")

        except (ValueError, InsufficientStockException) as e:
            print("\nFailed to add product:", e)

    def view_cart(self, user_id):
        print("\n========== SHOPPING CART ==========")

        cart_items = self.cart_service.get_cart_items(user_id)

        if not cart_items:
            print("Your cart is empty.")
            return

        total = 0

        print(
            f"{'Product':<20}"
            f"{'Quantity':<10}"
            f"{'Price':<15}"
            f"{'Subtotal':<15}"
        )
        print("-" * 60)

        for item in cart_items:
            try:
                product = self.product_service.get_product_by_id(
                    item.product_id
                )
            except ValueError:
                print(
                    f"{'Unavailable product':<20}"
                    f"{item.quantity:<10}"
                )
                continue

            subtotal = product.price * item.quantity
            total += subtotal

            print(
                f"{product.name:<20}"
                f"{item.quantity:<10}"
                f"₹{product.price:<14.2f}"
                f"₹{subtotal:<14.2f}"
            )

        print("-" * 60)
        print(f"Total: ₹{total:.2f}")

    def remove_from_cart(self, user_id):
        print("\n========== REMOVE FROM CART ==========")

        try:
            product_id = int(input("Enter product ID: "))

            self.cart_service.remove_from_cart(
                user_id,
                product_id
            )

            print("\nProduct removed from cart.")

        except (ValueError, EmptyCartException) as e:
            print("\nFailed to remove product:", e)
