class OrderItem:

    def __init__(
        self,
        order_item_id=None,
        order_id=None,
        product_id=None,
        quantity=1,
        price=0.0
    ):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
