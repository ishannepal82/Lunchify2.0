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
                created_at = datetime.utcnow(),

                user_snapshot={
                "name": order_dict["user"]["name"],
                "phone": order_dict["user"]["phone"],
                "address": order_dict["user"]["address"],
                },

             restaurant_snapshot={
                "name": order_dict["restaurant"]["name"],
                "address": order_dict["restaurant"]["address"],
                "phone": order_dict["restaurant"]["phone"],
                },
                

              order_items=order_dict["orders"])

            self.db.add(order_db)
            self.db.commit()
            self.db.refresh(order_db)

        except Exception as e:
            print(e)
            raise e  
        return order_db.model_dump(exclude_unset=True)
    
    def get_all_orders(self): 
        try: 
            orders = self.db.exec(select(Order)).all()
            orders_dict = [order.model_dump() for order in orders]

        except Exception as e: 
            print(f"Error in : {e}")

        return orders_dict
    
    def approve_order (self, order_id): 
        try: 
           order_db = self.db.get(Order, order_id)

           if not order_db:
               raise ValueError("Order not found")
           
           print(order_db)
           order_db.is_approved_by_restaurant = True
           self.db.commit()

        except Exception as e: 
            print(f"Error in : {e}")

        return self 