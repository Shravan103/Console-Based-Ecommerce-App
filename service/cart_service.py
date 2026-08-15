from dao.cart_dao import CartDAO
from dao.product_dao import ProductDAO
from model.cart_item import CartItem
from exceptions.insufficient_stock_exception import InsufficientStockException
from exceptions.empty_cart_exception import EmptyCartException


class CartService:

    def __init__(self):
        self.cart_dao = CartDAO()
        self.product_dao = ProductDAO()

    def get_or_create_cart(self, user_id):
        cart = self.cart_dao.get_cart_by_user(user_id)

        if cart is None:
            cart = self.cart_dao.create_cart(user_id)

        return cart

    def add_to_cart(self, user_id, product_id, quantity):
        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        product = self.product_dao.get_product_by_id(product_id)

        if product is None:
            raise ValueError("Product not found.")

        cart = self.get_or_create_cart(user_id)

        existing_items = self.cart_dao.get_cart_items(
            cart.cart_id
        )

        existing_quantity = 0

        for item in existing_items:
            if item.product_id == product_id:
                existing_quantity = item.quantity
                break

        if existing_quantity + quantity > product.stock:
            raise InsufficientStockException(
                f"Insufficient stock for {product.name}. "
                f"Available stock: {product.stock}."
            )

        cart_item = CartItem(
            cart_id=cart.cart_id,
            product_id=product_id,
            quantity=quantity
        )

        self.cart_dao.add_to_cart(cart_item)

    def remove_from_cart(self, user_id, product_id):
        cart = self.cart_dao.get_cart_by_user(user_id)

        if cart is None:
            raise EmptyCartException(
                "Cart is empty."
            )

        self.cart_dao.remove_from_cart(
            cart.cart_id,
            product_id
        )

    def get_cart_items(self, user_id):
        cart = self.cart_dao.get_cart_by_user(user_id)

        if cart is None:
            return []

        return self.cart_dao.get_cart_items(cart.cart_id)

    def clear_cart(self, user_id):
        cart = self.cart_dao.get_cart_by_user(user_id)

        if cart is not None:
            self.cart_dao.clear_cart(cart.cart_id)

    def calculate_total(self, user_id):
        cart = self.cart_dao.get_cart_by_user(user_id)

        if cart is None:
            return 0

        cart_items = self.cart_dao.get_cart_items(
            cart.cart_id
        )

        total = 0

        for item in cart_items:
            product = self.product_dao.get_product_by_id(
                item.product_id
            )

            if product is not None:
                total += product.price * item.quantity

        return total
