from dao.product_dao import ProductDAO
from model.product import Product


class ProductService:

    def __init__(self):
        self.product_dao = ProductDAO()

    def add_product(self, name, description, price, stock):
        name = name.strip()

        if not name:
            raise ValueError(
                "Product name cannot be empty."
            )

        if price <= 0:
            raise ValueError(
                "Price must be greater than zero."
            )

        if stock < 0:
            raise ValueError(
                "Stock cannot be negative."
            )

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock
        )

        return self.product_dao.add_product(product)

    def get_all_products(self):
        return self.product_dao.get_all_products()

    def get_product_by_id(self, product_id):
        product = self.product_dao.get_product_by_id(product_id)

        if product is None:
            raise ValueError("Product not found.")

        return product

    def update_product(
        self,
        product_id,
        name,
        description,
        price,
        stock
    ):
        name = name.strip()

        if not name:
            raise ValueError(
                "Product name cannot be empty."
            )

        if price <= 0:
            raise ValueError(
                "Price must be greater than zero."
            )

        if stock < 0:
            raise ValueError(
                "Stock cannot be negative."
            )

        product = self.get_product_by_id(product_id)

        product.name = name
        product.description = description
        product.price = price
        product.stock = stock

        self.product_dao.update_product(product)

        return product

    def delete_product(self, product_id):
        product = self.get_product_by_id(product_id)

        self.product_dao.delete_product(product_id)

        return product
