class OrderService(): 
    def __init__(self, db):
        self.db = db

    def create_order(self, order):
        """
        Docstring for create_order

        :param order: OrderCreateSchema
        """
        