import pytest

from service.cart_service import CartService
from model.product import Product
from model.cart import Cart
from model.cart_item import CartItem
from exceptions.insufficient_stock_exception import InsufficientStockException


def test_add_to_cart_rejects_insufficient_stock():
    service = CartService()

    class FakeProductDAO:
        def get_product_by_id(self, product_id):
            return Product(
                product_id=product_id,
                name="Laptop",
                price=50000,
                stock=2
            )

    class FakeCartDAO:
        def get_cart_by_user(self, user_id):
            return Cart(cart_id=1, user_id=user_id)

        def get_cart_items(self, cart_id):
            return []

    service.product_dao = FakeProductDAO()
    service.cart_dao = FakeCartDAO()

    with pytest.raises(InsufficientStockException):
        service.add_to_cart(1, 1, 5)


def test_add_to_cart_success():
    service = CartService()

    class FakeProductDAO:
        def get_product_by_id(self, product_id):
            return Product(
                product_id=product_id,
                name="Mouse",
                price=800,
                stock=10
            )

    class FakeCartDAO:
        def get_cart_by_user(self, user_id):
            return Cart(cart_id=1, user_id=user_id)

        def get_cart_items(self, cart_id):
            return []

        def add_to_cart(self, cart_item):
            self.saved_item = cart_item

    fake_cart_dao = FakeCartDAO()

    service.product_dao = FakeProductDAO()
    service.cart_dao = fake_cart_dao

    service.add_to_cart(1, 1, 2)

    assert fake_cart_dao.saved_item.quantity == 2
    assert fake_cart_dao.saved_item.product_id == 1
