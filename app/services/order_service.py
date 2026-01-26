from datetime import datetime
from uuid import uuid4

# Repos
from app.repos.orders.order import Order
from sqlmodel import select

# Helpers
from app.helpers.internal.calculate_total_price import calculate_total_price

class OrderService(): 
    def __init__(self, db):
        self.db = db

    def create_order(self, order):
        """
        Docstring for create_order

        :param order: OrderCreateSchema
        """
        try:
            order_dict = order.model_dump(exclude_unset=True)
            print("Order Dict:", order_dict)

            total_price  = calculate_total_price(order_dict['orders'])

            order_db = Order(
                order_id = str(uuid4()),
                total_price= total_price,
                created_at = datetime.utcnow(),**order.model_dump())

            self.db.add(order_db)
            self.db.commit()
            self.db.refresh(order_db)

        except Exception as e:
            raise e  
        return order_db.model_dump(exclude_unset=True)