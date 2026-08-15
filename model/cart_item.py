class CartItem:

    def __init__(
        self,
        cart_item_id=None,
        cart_id=None,
        product_id=None,
        quantity=1
    ):
        self.cart_item_id = cart_item_id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
