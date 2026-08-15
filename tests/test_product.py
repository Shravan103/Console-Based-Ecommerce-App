import pytest

from service.product_service import ProductService


def test_add_product_rejects_negative_stock():
    service = ProductService()

    with pytest.raises(ValueError):
        service.add_product(
            "Laptop",
            "Test laptop",
            50000,
            -1
        )


def test_add_product_rejects_zero_price():
    service = ProductService()

    with pytest.raises(ValueError):
        service.add_product(
            "Laptop",
            "Test laptop",
            0,
            10
        )


def test_add_product_rejects_empty_name():
    service = ProductService()

    with pytest.raises(ValueError):
        service.add_product(
            "",
            "Test laptop",
            50000,
            10
        )
