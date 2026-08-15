class Product:

    def __init__(
        self,
        product_id=None,
        name=None,
        description=None,
        price=0.0,
        stock=0
    ):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
