class Order:

    def __init__(
        self,
        order_id=None,
        user_id=None,
        order_date=None,
        total_amount=0.0
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.total_amount = total_amount
