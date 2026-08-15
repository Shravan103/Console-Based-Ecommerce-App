import pytest

from service.order_service import OrderService
from model.cart import Cart
from model.cart_item import CartItem
from model.product import Product
from exceptions.empty_cart_exception import EmptyCartException


def test_empty_cart_raises_exception(monkeypatch):
    service = OrderService()

    class FakeConnection:
        def rollback(self):
            pass

        def close(self):
            pass

    class FakeCartDAO:
        def get_cart_by_user(self, user_id):
            return None

    monkeypatch.setattr(
        "service.order_service.get_connection",
        lambda: FakeConnection()
    )

    service.cart_dao = FakeCartDAO()

    with pytest.raises(EmptyCartException):
        service.place_order(1)


def test_order_total_calculation(monkeypatch):
    service = OrderService()

    class FakeConnection:
        def commit(self):
            pass

        def rollback(self):
            pass

        def close(self):
            pass

    class FakeCartDAO:
        def get_cart_by_user(self, user_id):
            return Cart(cart_id=1, user_id=user_id)

        def get_cart_items(self, cart_id):
            return [
                CartItem(
                    cart_id=1,
                    product_id=10,
                    quantity=2
                )
            ]

        def clear_cart_with_connection(self, connection, cart_id):
            pass

    class FakeProductDAO:
        def get_product_by_id(self, product_id):
            return Product(
                product_id=10,
                name="Mouse",
                price=800,
                stock=10
            )

        def update_stock(self, connection, product_id, quantity):
            pass

    class FakeOrderDAO:
        def create_order_with_connection(self, connection, order):
            order.order_id = 100
            return order

        def add_order_item_with_connection(self, connection, order_item):
            order_item.order_item_id = 1
            return order_item

    monkeypatch.setattr(
        "service.order_service.get_connection",
        lambda: FakeConnection()
    )

    service.cart_dao = FakeCartDAO()
    service.product_dao = FakeProductDAO()
    service.order_dao = FakeOrderDAO()

    order = service.place_order(1)

    assert order.order_id == 100
    assert order.total_amount == 1600
